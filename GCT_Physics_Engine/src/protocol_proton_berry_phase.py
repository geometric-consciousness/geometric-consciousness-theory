#!/usr/bin/env python3
"""
protocol_proton_berry_phase.py — SU(2) Berry Phase and Proton Mass Exponent
================================================================
Derives the exact +phi^{-1} additive correction to the proton mass exponent
from SU(2) Weak fiber-bundle holonomy around a 5-fold baryonic loop.

Method: Path-Ordered SU(2) Holonomy
-------------------------------------
1. Parameterize the baryonic 2pi circuit around the 5-fold dodecahedral axis.
2. Compute U_weak = P.exp(i * ∮ A_mu^weak dq^mu) by a path-ordered product
   of N=10000 SU(2) infinitesimal steps.
3. Verify U_weak = -I_2  (Berry phase = pi, i.e., half-winding N_weak = 1/2).
4. Apply projection ratio R = 2 * phi^{-1}:
       phi_correction = N_weak * R = (1/2) * (2/phi) = 1/phi
5. Reconstruct Phi_total = 15 + phi^{-1}.

PASS criterion: the Tier 1 SU(2) identities only, i.e.
U_weak = -I_2 (N_weak = 1/2) and the parity sweep U_n = (-1)^n I_2. The
projection ratio R = 2*phi^{-1} is typed in, so phi_correction = phi^{-1} and
Phi_total = 15 + phi^{-1} hold by construction; they are recorded as INPUTS,
not as computed checks, and no longer gate the PASS.

Output
------
  data/proton_berry_phase_results.json
"""

import sys
import json
import numpy as np
from pathlib import Path

# ---------------------------------------------------------------------------
# Path bootstrap — ensure src/ is importable when run from any cwd
# ---------------------------------------------------------------------------
_SRC = Path(__file__).resolve().parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from gct_utils import get_output_path, C


class _NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, (np.bool_,)):
            return bool(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


# ============================================================================
# SECTION 1: Constants
# ============================================================================

PHI     = float(C.PHI)      # golden ratio (1+sqrt(5))/2
INV_PHI = 1.0 / PHI         # phi^{-1} = phi - 1 ≈ 0.6180339887

# Target exponent from proton mass formula
N_STRONG_TARGET = 15.0       # strong winding number (Z3 x Z5 template; base-exponent selection Tier 3)
PHI_TOTAL_TARGET = 15.0 + INV_PHI  # 15 + phi^{-1} ≈ 15.6180339887

# SU(2) Pauli matrices
SIGMA_X = np.array([[0, 1],  [1, 0]],  dtype=complex)
SIGMA_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
SIGMA_Z = np.array([[1, 0],  [0, -1]], dtype=complex)
I2      = np.eye(2, dtype=complex)


# ============================================================================
# SECTION 2: Path-Ordered SU(2) Holonomy
# ============================================================================

def compute_su2_holonomy(n_steps: int = 10_000, n: int = 1) -> np.ndarray:
    """
    Compute the SU(2) holonomy for a full 2*pi loop around the 5-fold axis.

    Physical setup
    --------------
    The baryonic circuit is a loop in the SO(3) base space parameterized by
    theta in [0, 2*pi], corresponding to a full rotation around the 5-fold
    dodecahedral axis (the symmetry axis of the pentagonal face).

    The axial SU(2) connection in the fiber is:
        A_theta = (n/2) * sigma_z,  n in Z.

    Its exact holonomy is exp(i*n*pi*sigma_z) = (-1)^n I_2. Thus the
    2I stabilizer condition distinguishes parity only: even n gives I_2 and
    odd n gives -I_2. The baryonic branch selects n=1 through the explicitly
    adopted least-positive/nontrivial-winding physical minimality premise,
    not through algebraic uniqueness in 2I.
    Formal theorem: App USS §USS.8 (Theorem USS.8 — Parity of Axial SU(2) Holonomy).
    Detailed derivation: Vol. 3 Ch18 §18.2.3.A.

    The path-ordered exponential:
        U_n = P.exp(i * integral_0^{2pi} A_theta dtheta)
            = exp(i * n*pi * sigma_z)
            = cos(n*pi)*I + i*sin(n*pi)*sigma_z
            = (-1)^n I_2

    This is computed numerically by the product of N infinitesimal steps:
        U_step(k) = exp(i * (n*dtheta/2) * sigma_z)  dtheta = 2*pi/N
        U_weak    = U_step(1) * U_step(2) * ... * U_step(N)

    The path-ordering is trivial here because [sigma_z, sigma_z] = 0 (all
    infinitesimals commute) — the product converges exactly to
    exp(i*n*pi*sigma_z) for any finite N.

    Parameters
    ----------
    n_steps : int
        Number of discretization steps (default 10,000 for numerical precision).
    n : int
        Integer axial weight.

    Returns
    -------
    U_weak : np.ndarray (2x2 complex)
        The holonomy matrix.
    """
    if not isinstance(n, (int, np.integer)):
        raise TypeError("n must be an integer axial weight")

    dtheta = 2.0 * np.pi / n_steps

    # Each infinitesimal step:
    # U_step = exp(i * (n*dtheta/2) * sigma_z)
    #        = cos(n*dtheta/2)*I + i*sin(n*dtheta/2)*sigma_z
    half_dtheta = n * dtheta / 2.0
    c = np.cos(half_dtheta)
    s = np.sin(half_dtheta)
    U_step = c * I2 + 1j * s * SIGMA_Z

    # Path-ordered product: U_weak = (U_step)^N
    # Since all steps are identical and commute, this equals matrix power.
    # We use repeated squaring for efficiency.
    U_weak = np.linalg.matrix_power(U_step, n_steps)

    return U_weak


def verify_integer_parity(n_steps: int = 10_000, n_min: int = -6, n_max: int = 6) -> tuple[list[dict], bool]:
    """Verify U_n = (-1)^n I_2 across negative, zero, and positive integers."""
    sweep = []
    for n in range(n_min, n_max + 1):
        U_n = compute_su2_holonomy(n_steps=n_steps, n=n)
        parity = "even" if n % 2 == 0 else "odd"
        expected_sign = 1 if n % 2 == 0 else -1
        expected = expected_sign * I2
        deviation = float(np.linalg.norm(U_n - expected))
        sweep.append({
            "n": n,
            "parity": parity,
            "expected_holonomy": "I_2" if expected_sign == 1 else "-I_2",
            "trace": float(np.trace(U_n).real),
            "deviation_frobenius": deviation,
            "pass": deviation < 1e-9,
        })
    return sweep, all(row["pass"] for row in sweep)


def verify_minus_identity(U: np.ndarray, tol: float = 1e-9) -> tuple[float, bool]:
    """
    Check if a 2x2 matrix equals -I_2.
    Returns (||U + I_2||_F, is_minus_identity).
    """
    deviation = float(np.linalg.norm(U + I2))
    return deviation, deviation < tol


# ============================================================================
# SECTION 3: Projection Ratio and Exponent Reconstruction
# ============================================================================

def compute_berry_correction(U_weak: np.ndarray) -> dict:
    """
    From the holonomy U_weak derive the Weak Berry phase correction to the
    proton mass exponent.

    The Berry phase is:
        gamma = i * log(eigenvalue of U_weak along the loop)
              = i * log(-1) = pi

    This corresponds to a half-winding: N_weak = gamma / (2*pi) = 1/2.

    The E_perp projection ratio for the 5-fold baryonic loop onto the
    SU(2) Lie algebra is:
        R = 2 * phi^{-1}

    This ratio comes from the geometric projection of the dodecahedral cage's
    5-fold pentagonal face area onto the fundamental domain — the edge-to-diagonal
    ratio of a regular pentagon is phi^{-1}, and the factor 2 accounts for the
    symmetric projection (both hemispheres contribute equally).

    The Weak correction:
        phi_correction = N_weak * R = (1/2) * (2 * phi^{-1}) = phi^{-1}

    Total proton mass exponent:
        Phi_total = N_strong + phi_correction = 15 + phi^{-1}
    """
    # Extract Berry phase from trace: Tr(U) = 2*cos(gamma)
    trace_U = np.trace(U_weak).real
    cos_gamma = np.clip(trace_U / 2.0, -1.0, 1.0)
    gamma = np.arccos(cos_gamma)    # Berry phase in [0, pi]

    # Winding number: N_weak = gamma / (2*pi)
    N_weak = gamma / (2.0 * np.pi)

    # Projection ratio: R = 2 * phi^{-1}
    R_projection = 2.0 * INV_PHI

    # Phi correction
    phi_correction = N_weak * R_projection

    # Total exponent
    Phi_total = N_STRONG_TARGET + phi_correction

    return {
        "trace_U_weak":    float(trace_U),
        "Berry_phase_rad": float(gamma),
        "N_weak":          float(N_weak),
        "R_projection":    float(R_projection),
        "phi_inv":         float(INV_PHI),
        "phi_correction":  float(phi_correction),
        "Phi_total":       float(Phi_total),
    }

def extend_berry_to_ckm():
    PHI = float(C.PHI)
    # From proton proof: SU(2) step gives N_weak = 1/2, R = 2*phi^-1
    berry_correction = 0.5 * (2 / PHI) # = phi^-1
    
    alpha = float(C.ALPHA_OBS)
    s12 = PHI**-3 * (1 - 5*alpha)
    s23_bare = PHI**-6
    s23_berry = PHI**(-(6 + 1/PHI))
    s13_bare = PHI**-11
    s13_berry = PHI**(-(11 + 1/PHI))
    
    # PDG 2024 values
    s12_pdg = 0.22501
    s23_pdg = 0.04108
    s13_pdg = 0.003735
    
    return {
        "berry_correction": berry_correction,
        "s23_bare": s23_bare, "s23_berry": s23_berry, "s23_pdg": s23_pdg,
        "s13_bare": s13_bare, "s13_berry": s13_berry, "s13_pdg": s13_pdg,
        "berry_improves_s23": abs(s23_berry - s23_pdg) < abs(s23_bare - s23_pdg),
        "berry_improves_s13": abs(s13_berry - s13_pdg) < abs(s13_bare - s13_pdg),
        "physical_interpretation": "Tier 3 ansatz: each generation-changing off-diagonal CKM element acquires one SU(2) holonomy step."
    }

# ============================================================================
# MAIN
# ============================================================================

def main() -> int:
    print("=" * 70)
    print("  Structural Analysis")
    print("  Proton Berry Phase: SU(2) Weak Holonomy Derivation of phi^{-1}")
    print("=" * 70)

    print(f"\n  phi          = {PHI:.10f}")
    print(f"  phi^{{-1}}     = {INV_PHI:.10f}")
    print(f"  Target Phi   = 15 + phi^{{-1}} = {PHI_TOTAL_TARGET:.10f}")

    # ------------------------------------------------------------------
    # Step 1–2: Compute holonomy
    # ------------------------------------------------------------------
    N_STEPS = 10_000
    print(f"\n[Step 1-2] Path-ordered SU(2) holonomy ({N_STEPS} steps)...")
    print(f"  Loop: 2π circuit around 5-fold dodecahedral axis")
    print(f"  Connection: A_θ = (1/2) σ_z  [spin-1/2 axial gauge]")
    U_weak = compute_su2_holonomy(n_steps=N_STEPS, n=1)

    print(f"\n  U_weak =")
    print(f"    [{U_weak[0,0].real:+.10f}{U_weak[0,0].imag:+.2e}j,  "
          f"{U_weak[0,1].real:+.2e}{U_weak[0,1].imag:+.2e}j]")
    print(f"    [{U_weak[1,0].real:+.2e}{U_weak[1,0].imag:+.2e}j,  "
          f"{U_weak[1,1].real:+.10f}{U_weak[1,1].imag:+.2e}j]")
    print(f"  Tr(U_weak) = {np.trace(U_weak).real:.10f}  (expected -2.0)")
    print(f"  det(U_weak) = {np.linalg.det(U_weak).real:.10f}  (expected +1.0, SU(2))")

    # ------------------------------------------------------------------
    # Step 3: Verify U_weak = -I_2
    # ------------------------------------------------------------------
    print("\n[Step 3] Verifying U_weak = -I_2  (Berry phase = π)...")
    deviation, minus_id_pass = verify_minus_identity(U_weak)
    print(f"  ||U_weak + I_2||_F = {deviation:.4e}   "
          f"{'[PASS]' if minus_id_pass else '[FAIL]'}  (threshold 1e-9)")
    print(f"  U_weak is -I_2     : {minus_id_pass}")
    print(f"  => Berry Phase γ   = π  (half-winding N_weak = 1/2)")

    # ------------------------------------------------------------------
    # Step 4–5: Apply projection and reconstruct exponent
    # ------------------------------------------------------------------
    print("\n[Step 4-5] Applying Weak projection ratio and reconstructing Phi_total...")
    berry_data = compute_berry_correction(U_weak)

    print(f"  Berry phase γ      = {berry_data['Berry_phase_rad']:.10f} rad  (expected π ≈ 3.14159...)")
    print(f"  Winding N_weak     = γ/(2π) = {berry_data['N_weak']:.10f}  (expected 0.5)")
    print(f"  Projection R       = 2·φ⁻¹  = {berry_data['R_projection']:.10f}")
    print(f"  φ_correction       = N_weak·R = {berry_data['phi_correction']:.10f}  (expected φ⁻¹ = {INV_PHI:.10f})")
    print(f"  N_strong           = {N_STRONG_TARGET}")
    print(f"  Φ_total            = {berry_data['Phi_total']:.10f}")
    print(f"  Target             = {PHI_TOTAL_TARGET:.10f}")

    phi_total_deviation = abs(berry_data['Phi_total'] - PHI_TOTAL_TARGET)
    phi_total_pass = phi_total_deviation < 1e-6
    print(f"\n  |Φ_total - 15.6180339887| = {phi_total_deviation:.4e}   "
          f"{'[PASS]' if phi_total_pass else '[FAIL]'}  (threshold 1e-6)")

    # Verify N_weak = 0.5 exactly
    n_weak_pass = abs(berry_data['N_weak'] - 0.5) < 1e-9
    print(f"  N_weak = 0.5 exactly : {'[PASS]' if n_weak_pass else '[FAIL]'}")

    # Verify phi_correction = phi^{-1}
    corr_pass = abs(berry_data['phi_correction'] - INV_PHI) < 1e-9
    print(f"  φ_correction = φ⁻¹  : {'[PASS]' if corr_pass else '[FAIL]'}")

    # ------------------------------------------------------------------
    # Exact integer-parity sweep and physical minimality disclosure
    # ------------------------------------------------------------------
    print("\n[Step 6] Sweeping integer weights n=-6,...,+6...")
    parity_sweep, parity_pass = verify_integer_parity(N_STEPS, -6, 6)
    for row in parity_sweep:
        print(
            f"  n={row['n']:+d} ({row['parity']}) -> {row['expected_holonomy']}; "
            f"deviation={row['deviation_frobenius']:.3e} "
            f"{'[PASS]' if row['pass'] else '[FAIL]'}"
        )
    print(f"  Exact parity sweep: {'PASS' if parity_pass else 'FAIL'}")
    print("  Physical selection: require nontrivial holonomy and choose the least positive integer weight; n=1.")

    # ------------------------------------------------------------------
    # Final verdict
    # ------------------------------------------------------------------
    all_pass = bool(minus_id_pass and n_weak_pass and parity_pass)
    # exp(i*pi*sigma_z) = -I_2 and (-1)^n are SU(2)
    # identities with no GCT input, so the result is recorded, not confirmed.
    verdict  = "SU2_HOLONOMY_IDENTITY_NO_GCT_INPUT_PHI_INV_INPUT" if all_pass else "FAIL"

    print("\n" + "=" * 70)
    print("  FINAL VERDICT")
    print("=" * 70)
    print(f"  U_weak = -I_2 (Berry phase π) : {'PASS' if minus_id_pass else 'FAIL'}")
    print(f"  N_weak = 1/2                  : {'PASS' if n_weak_pass else 'FAIL'}")
    print(f"  φ_correction = φ⁻¹            : INPUT (R = 2φ⁻¹ typed; holds by construction)")
    print(f"  Φ_total = 15 + φ⁻¹            : INPUT (not a computed check)")
    print(f"  U_n = (-1)^n I_2 parity sweep : {'PASS' if parity_pass else 'FAIL'}")
    print(f"\n  VERDICT: {verdict}")
    if all_pass:
        print("  The Tier 1 parity identity gives U_n = (-1)^n I_2 for every tested integer.")
        print("  Under the Tier 2 least-positive/nontrivial-winding premise, n=1 gives")
        print("  U_weak = -I_2 and Berry phase π  =>  N_weak = 1/2.")
        print("  With R = 2φ⁻¹: correction = N_weak·R = φ⁻¹.")
        print(f"  Φ_total = 15 + φ⁻¹ = {berry_data['Phi_total']:.10f}  (base 15: Tier 3 exponent handle)")

    # ------------------------------------------------------------------
    # Save JSON
    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    # Step 6: Extend Berry Phase to CKM geometry
    # ------------------------------------------------------------------
    ckm_extension = extend_berry_to_ckm()

    results = {
        "n_holonomy_steps":               N_STEPS,
        "U_weak_trace":                   float(np.trace(U_weak).real),
        "U_weak_det":                     float(np.linalg.det(U_weak).real),
        "U_weak_is_minus_identity":       minus_id_pass,
        "holonomy_deviation":             float(deviation),
        "N_weak":                         berry_data['N_weak'],
        "R_projection":                   berry_data['R_projection'],
        "phi_inv":                        berry_data['phi_inv'],
        "phi_correction":                 berry_data['phi_correction'],
        "N_strong":                       N_STRONG_TARGET,
        "Phi_total":                      berry_data['Phi_total'],
        "Phi_total_target":               PHI_TOTAL_TARGET,
        "phi_total_deviation":            phi_total_deviation,
        "phi_inv_status":                 "INPUT: R_projection = 2*phi^-1 is typed, so phi_correction = phi^-1 and Phi_total = 15 + phi^-1 hold by construction; not part of pass",
        "input_consistency_phi_correction": bool(corr_pass),
        "input_consistency_phi_total":      bool(phi_total_pass),
        "holonomy_parity_theorem":        "For every integer n, exp(i*n*pi*sigma_z) = (-1)^n I_2; even n gives I_2 and odd n gives -I_2.",
        "parity_sweep":                    parity_sweep,
        "parity_sweep_pass":               bool(parity_pass),
        "n_selection_premise":             "Tier 2 physical premise: require nontrivial holonomy and choose the least positive integer weight, selecting n=1; 2I equivariance alone distinguishes only parity.",
        "tier_split":                      "Tier 1 exact holonomy parity; Tier 2 least-positive/nontrivial-winding physical minimality premise; Tier 3 deployment in the absolute proton-mass exponent.",
        "verdict":                        verdict,
        "identity_holds":                 bool(all_pass),
        "pass":                           False,
        "ckm_berry_extension":            ckm_extension,
    }

    out_path = get_output_path("protocol_proton_berry_phase_results.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2, cls=_NumpyEncoder)
    print(f"\n  Results saved to: {out_path}")
    print("=" * 70)

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
