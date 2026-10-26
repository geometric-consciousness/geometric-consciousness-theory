#!/usr/bin/env python3
"""
protocol_weinberg_uniqueness.py — raw-frame integer-exponent identity for the
volume ratio V_perp,0/V_parallel,0 = φ⁻³ of the declared AKN row frames.

The claim (Tier 1 coordinate arithmetic, App USS §USS.9):
    For the declared unnormalised Galois-conjugate frames, the exponent is
    n = -dim(E_⊥) = -3 from:
      (T1.a)  dim(E_⊥) = 3 (cut-and-project to 3D physical space)
      (T1.b)  raw per-axis scale ratio φ^{-1} of the declared frames
              (V3 Ch04 §4.1.2)
      (T1.c)  Volume scales as length^dim (Euclidean measure theory).
    The ratio changes under row rescaling B -> sB while the proper projectors
    do not, so it is not a physical invariant; the canonical projector shares
    are 1/2 + 1/2.  sin^2(theta_W)^bare = φ⁻³ is the separate Tier 3
    gauge-kinetic hypothesis H-EW (V3 Ch04 §4.3.2).

The composition forces n = -dim · (length-exponent) = -3 · 1 = -3.

This script:
  (1) Computes the squared parallel/perp norms |E^∥|², |E^⊥|² from the
      canonical unnormalised AKN projection matrices, verifying the column
      norms 1+φ² and 1+φ⁻² and the row-Gram scalars
      2(1+φ²)I_3 and 2(1+φ⁻²)I_3 to machine precision.
  (2) Verifies |E^⊥|/|E^∥| = φ^{-1} exactly.
  (3) Cubes the ratio to get V_⊥/V_∥ = φ^{-3}. Identifying this mathematical
      ratio with the physical bare Weinberg angle is the Tier 3 hypothesis H-EW.
  (4) Verifies the exact exponent identity n = -dim(E_⊥) = -3 over the
      declared integer-power domain, without treating a finite sweep as proof.
  (5) Outputs a verification certificate.
"""

from __future__ import annotations
import math, json, sys
from pathlib import Path
import numpy as np
from gct_utils import C

ENGINE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENGINE_ROOT / "src"))

DATA_PATH = ENGINE_ROOT / "data" / "protocol_weinberg_uniqueness_results.json"
PHI = float(C.PHI)
PHI_INV = 1.0 / PHI


def main() -> int:
    print("=" * 90)
    print("  Raw-frame φ^(-3) integer-exponent identity (App USS §USS.9 / TP-G)")
    print("=" * 90)

    # Step 1: load the canonical UNNORMALISED projection matrices. An overall
    # normalization convention changes the absolute column/Gram scalars but
    # not their parallel/perpendicular ratio or the forced exponent.
    from gct_projections import get_m_parallel_unnormalized, get_m_perp_unnormalized
    M_para = get_m_parallel_unnormalized()
    M_perp = get_m_perp_unnormalized()
    print(f"  M_∥ shape: {M_para.shape},  M_⊥ shape: {M_perp.shape}")
    print()

    # Step 2: row-space Gram matrices for the unnormalised convention.
    # They are scalar matrices, but they are not identity matrices.
    G_para = M_para @ M_para.T
    G_perp = M_perp @ M_perp.T
    expected_para_sq = 1 + PHI**2
    expected_perp_sq = 1 + PHI**(-2)
    expected_G_para_scalar = 2 * expected_para_sq
    expected_G_perp_scalar = 2 * expected_perp_sq
    print(f"  G_∥ = M_∥ M_∥^T (3×3):")
    print(f"    {G_para}")
    print(f"  G_⊥ = M_⊥ M_⊥^T (3×3):")
    print(f"    {G_perp}")
    para_gram_match = np.allclose(G_para, expected_G_para_scalar * np.eye(3), atol=1e-12)
    perp_gram_match = np.allclose(G_perp, expected_G_perp_scalar * np.eye(3), atol=1e-12)
    print(f"  Expected G_∥ = 2(1+φ²)I_3 = {expected_G_para_scalar:.10f} I_3")
    print(f"  Expected G_⊥ = 2(1+φ⁻²)I_3 = {expected_G_perp_scalar:.10f} I_3")
    print(f"  Gram-scalar matches? para: {para_gram_match}, perp: {perp_gram_match}")
    print()

    # Step 3: the per-AXIS squared norms (one per Z^6 basis vector)
    # |E^∥_i|² = ||M_para[:, i]||² (column norm), using UNNORMALIZED matrix
    sq_norms_para = np.array([np.linalg.norm(M_para[:, i])**2 for i in range(6)])
    sq_norms_perp = np.array([np.linalg.norm(M_perp[:, i])**2 for i in range(6)])
    print(f"  Per-axis squared norms |E^∥_i|² (unnormalized): {sq_norms_para}")
    print(f"  Per-axis squared norms |E^⊥_i|² (unnormalized): {sq_norms_perp}")
    # The chapter's (1+φ²)/5 and (1+φ⁻²)/5 use a 5-normalization (divide by 5).
    # The unnormalized values are 1+φ² and 1+φ⁻² respectively.
    print(f"  Expected (unnormalized) |E^∥_i|² = 1+φ² = {expected_para_sq:.10f}")
    print(f"  Expected (unnormalized) |E^⊥_i|² = 1+φ⁻² = {expected_perp_sq:.10f}")
    para_match = np.allclose(sq_norms_para, expected_para_sq, atol=1e-12)
    perp_match = np.allclose(sq_norms_perp, expected_perp_sq, atol=1e-12)
    print(f"  All axes match? para: {para_match}, perp: {perp_match}")
    print(f"  (The 1/5 in the chapter's (1+φ²)/5 is a per-basis normalization;")
    print(f"   the RATIO (1+φ⁻²)/(1+φ²) = φ⁻² is convention-independent.)")
    print()

    # Step 4: compute the ratio |E^⊥|/|E^∥| per axis
    ratio_sq = sq_norms_perp / sq_norms_para
    ratio = np.sqrt(ratio_sq)
    expected_ratio = PHI**(-1)
    expected_ratio_sq = PHI**(-2)
    print(f"  Per-axis squared length ratio |E^⊥|² / |E^∥|² = {ratio_sq[0]:.10f}")
    print(f"  Expected = φ⁻² = {expected_ratio_sq:.10f}")
    print(f"  Match? {np.isclose(ratio_sq[0], expected_ratio_sq, atol=1e-12)}")
    print()
    print(f"  Per-axis LENGTH ratio |E^⊥| / |E^∥| = {ratio[0]:.10f}")
    print(f"  Expected = φ⁻¹ = {expected_ratio:.10f}")
    print(f"  Match? {np.isclose(ratio[0], expected_ratio, atol=1e-12)}")
    print()

    # Step 5: cube it to get the volume ratio. Its physical identification
    # with the bare Weinberg angle is the Tier 3 hypothesis H-EW.
    volume_ratio = ratio[0]**3
    expected_phi_inv_3 = PHI**(-3)
    print(f"  Volume ratio (length)³ = φ⁻³ = {volume_ratio:.10f}")
    print(f"  Expected φ⁻³           = {expected_phi_inv_3:.10f}")
    print(f"  Match? {np.isclose(volume_ratio, expected_phi_inv_3, atol=1e-12)}")
    print()
    print(f"  ✓ V_⊥/V_∥ = (φ⁻¹)³ = φ⁻³ = {expected_phi_inv_3:.10f}")
    print("    Identifying sin²θ_W^bare with V_⊥/V_∥ is the Tier 3 hypothesis H-EW;")
    print("    the coordinate arithmetic above does not fix it (V3 Ch04 §4.3.2).")
    print()

    # Step 6: verify the exponent identity over the declared integer domain.
    dim_e_perp = int(M_perp.shape[0])
    length_exponent = -1
    forced_exponent = dim_e_perp * length_exponent
    exponent_identity_pass = dim_e_perp == 3 and forced_exponent == -3
    verification_pass = (
        para_gram_match and perp_gram_match and para_match and perp_match
        and np.allclose(ratio_sq, expected_ratio_sq, atol=1e-12)
        and np.allclose(ratio, expected_ratio, atol=1e-12)
        and np.isclose(volume_ratio, expected_phi_inv_3, atol=1e-12)
        and exponent_identity_pass
    )
    print("  ─── Integer-exponent identity ───")
    print("  Domain: n ∈ ℤ")
    print(f"  dim(E_⊥)                = {dim_e_perp}")
    print(f"  per-axis φ exponent     = {length_exponent}")
    print(f"  n = -dim(E_⊥)           = {forced_exponent}")
    print(f"  Exact exponent identity : {'PASS' if exponent_identity_pass else 'FAIL'}")
    print()

    # Step 7: emit verification certificate
    cert = {
        "claim": "For the declared raw frames, V_⊥,0/V_∥,0 = φ⁻³ with n = -dim(E_⊥) = -3; coordinate identity, not a physical invariant; bare-angle identification is the Tier 3 hypothesis H-EW",
        "integer_power_domain": "n ∈ ℤ",
        "dim_E_perp": dim_e_perp,
        "per_axis_phi_exponent": length_exponent,
        "forced_integer_exponent": forced_exponent,
        "exponent_identity_pass": bool(exponent_identity_pass),
        "tier_1_inputs": {
            "T1.a — dim(E_⊥) = 3": "Cut-and-project to 3D physical space; fixed by GCT axiom + Lemma III (V1 Ch02 + App USS §USS.6).",
            "T1.b — length ratio = φ⁻¹": f"Raw Galois-frame scale ratio (V3 Ch04 §4.1.2, Tier 1 coordinate arithmetic). Verified numerically: |E^⊥|/|E^∥| = {ratio[0]:.10f}, expected φ⁻¹ = {expected_ratio:.10f}.",
            "T1.c — vol = len^dim": "Euclidean measure theory; Tier 1 axiomatic.",
        },
        "derivation_chain": "V_⊥/V_∥ = (|E^⊥|/|E^∥|)^dim = (φ⁻¹)^3 = φ⁻³",
        "numerical_value": float(volume_ratio),
        "expected_phi_minus_3": float(expected_phi_inv_3),
        "numerical_match": bool(np.isclose(volume_ratio, expected_phi_inv_3, atol=1e-12)),
        "unnormalised_gram_matrices": {
            "parallel_scalar_times_I3": float(G_para[0, 0]),
            "perpendicular_scalar_times_I3": float(G_perp[0, 0]),
            "expected_parallel_scalar": float(expected_G_para_scalar),
            "expected_perpendicular_scalar": float(expected_G_perp_scalar),
            "parallel_match": bool(para_gram_match),
            "perpendicular_match": bool(perp_gram_match),
        },
        "integer_exponent_proof": (
            "The declared domain is n in Z. T1.b supplies per-axis exponent -1; "
            "T1.a fixes dim(E_perp)=3; T1.c multiplies the exponent by the "
            "dimension. Therefore n=(-1)*dim(E_perp)=-3, without a finite "
            "case enumeration."
        ),
        "normalization_disclosure": (
            "The producer uses unnormalised AKN projection matrices with per-axis "
            "squared norms 1+phi^2 and 1+phi^-2. The chapter's convention divides "
            "both by 5; the ratio and forced exponent are unchanged."
        ),
        "tier_disposition": "Tier 1 raw-frame identity from dim=3, raw per-axis exponent=-1, and Euclidean volume scaling; coordinate-dependent under row rescaling; physical bare angle is the Tier 3 hypothesis H-EW",
        "verification_pass": bool(verification_pass),
    }
    print("  ─── Verification certificate ───")
    print(json.dumps(cert, indent=2, ensure_ascii=False))
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DATA_PATH.open("w", encoding="utf-8") as f:
        json.dump(cert, f, indent=2, ensure_ascii=False)
    print(f"\n  Results: {DATA_PATH}")
    return 0 if verification_pass else 1


if __name__ == "__main__":
    sys.exit(main())
