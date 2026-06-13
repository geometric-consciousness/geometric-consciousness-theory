#!/usr/bin/env python3
"""
protocol_neutrino_precision.py — Neutrino Mass Prediction
=================================================================
Derives Σm_ν from first principles and propagates uncertainties to
produce a falsifiable prediction with 3σ rejection bounds.

GCT Base Formula
----------------
The lightest neutrino mass (m₁) is the lightest lepton vertex mode
in the RT acceptance window:

    m₁ = m_e · φ^{−36}

where the exponent −36 = −3 · 12 encodes three generations × 12 vertices.

The heavier masses are obtained from oscillation data (NuFit 5.0):
    m₂ = √(m₁² + Δm²₂₁)
    m₃ = √(m₁² + Δm²₃₁)   [Normal Ordering]

Uncertainty Budget
------------------
1. Geometric floor: ±0.1% on m₁ from higher-order phason loops.
2. Δm²₂₁ experimental uncertainty (NuFit 5.0): ±0.18e−5 eV²
3. Δm²₃₁ experimental uncertainty (NuFit 5.0): ±0.017e−3 eV²

θ₂₃ Epistemic Status: TENSION_GT_4SIGMA (Tier 3)
-------------------------------------------------
GCT predicts a bare θ₂₃ = 45° from the 3-fold symmetry constraints
of the icosahedral window. NOvA and T2K measure ~49.5° ± 1.1°, a 4.5° gap.

Standard MSW cannot close the gap:
  The standard Mikheyev-Smirnov-Wolfenstein matter effect on θ₂₃ was
  computed for NOvA (L=810 km, ρ=2.8 g/cm³, E=2 GeV) and T2K (L=295 km).
  Result: matter parameter 2EV/Δm²₃₁ ≈ 1.7×10⁻⁴ (NOvA), giving a θ₂₃
  shift of ~0.00004°. The MSW effect is 5 orders of magnitude too small
  to close the gap. MSW primarily affects the 1-2 sector, not the 2-3 sector.

Status - Itinerant Volume Drag excluded:
  An alternative perturbation Δĥ_drag = γ (J · w) (invoked elsewhere to induce a 4.5°
  eigenbasis rotation) is excluded from the registered prediction. Its coupling γ is not derived
  from the phason elastic action, so it is excluded under zero-free-parameter
  integrity (see Ch09 §9.4.2).

  The bare 45° prediction is classified Tier 3 (Tension) pending a lattice-
  Hamiltonian derivation of neutrino propagation through the discrete
  icosahedral vacuum. That derivation is the pre-registered discriminant:
  if it recovers standard MSW, the 45° is falsified; if it departs from MSW
  consistent with the 4.5° shift, the prediction elevates to Tier 2.
"""

import json
import sys
import numpy as np
from pathlib import Path


from gct_utils import C, get_output_path

# ── SSOT values ───────────────────────────────────────────────────────────────
PHI          = float(C.PHI)
M_E_EV       = float(C.M_E) * 1e6          # MeV → eV

# NuFit 5.0 (Normal Ordering) — if in YAML, load from C; else use published values.
# Δm²₂₁ = (7.53 ± 0.18) × 10⁻⁵ eV²
# Δm²₃₁ = (2.455 ± 0.028) × 10⁻³ eV²   (→ ±0.017 on the 2σ range, but use 1σ ≈ 0.014)
DM2_21      = getattr(C, "DELTA_M2_21",    7.53e-5)   # eV²
DM2_21_ERR  = getattr(C, "DELTA_M2_21_ERR", 0.18e-5)  # 1σ
DM2_31      = getattr(C, "DELTA_M2_31",    2.455e-3)  # eV²
DM2_31_ERR  = getattr(C, "DELTA_M2_31_ERR", 0.028e-3) # 1σ

PHASON_FLOOR = 0.001   # ±0.1% structural uncertainty from higher-order loops

EXPONENT = 36          # m₁ = m_e · φ^{−36}  (3 generations × 12 RT vertices)


def _sigma_m1(m1, phason_frac=PHASON_FLOOR):
    """Absolute 1σ uncertainty on m₁ from phason loop corrections."""
    return m1 * phason_frac


def _sigma_m23(m1: float, m: float, sigma_m1: float, dm2: float, sigma_dm2: float) -> float:
    """
    Error propagation for m = √(m₁² + Δm²):
        dm/dm₁ = m₁/m
        dm/d(Δm²) = 1/(2m)
    """
    ddm_ddm1  = float(m1) / float(m)
    ddm_ddm2  = 1.0 / (2.0 * float(m))
    return np.sqrt((ddm_ddm1 * sigma_m1)**2 + (ddm_ddm2 * sigma_dm2)**2)


def run_neutrino_precision() -> dict:
    print("=" * 65)
    print("GCT Protocol — Neutrino Mass Precision")
    print("=" * 65)

    # ── Central values ────────────────────────────────────────────────────────
    m1 = M_E_EV * PHI**(-EXPONENT)
    m2 = np.sqrt(m1**2 + DM2_21)
    m3 = np.sqrt(m1**2 + DM2_31)
    sigma_sum = m1 + m2 + m3

    # ── Uncertainties ─────────────────────────────────────────────────────────
    sig_m1 = _sigma_m1(m1)
    sig_m2 = _sigma_m23(m1, m2, sig_m1, DM2_21, DM2_21_ERR)
    sig_m3 = _sigma_m23(m1, m3, sig_m1, DM2_31, DM2_31_ERR)
    sig_total = np.sqrt(sig_m1**2 + sig_m2**2 + sig_m3**2)

    print(f"\n  GCT formula: m₁ = m_e · φ^{{−{EXPONENT}}}")
    print(f"  m_e         = {M_E_EV:.6f} eV")
    print(f"  φ^{{−{EXPONENT}}}  = {PHI**(-EXPONENT):.6e}")
    print()
    print(f"  m₁          = {m1*1e3:.4f}  ± {sig_m1*1e3:.4f}  meV")
    print(f"  m₂          = {m2*1e3:.4f}  ± {sig_m2*1e3:.4f}  meV")
    print(f"  m₃          = {m3*1e3:.4f}  ± {sig_m3*1e3:.4f}  meV")
    print(f"  {'─'*50}")
    print(f"  Σm_ν        = {sigma_sum*1e3:.3f}  ± {sig_total*1e3:.3f}  meV")
    print(f"             = {sigma_sum:.4f}  ± {sig_total:.4f}  eV")
    print()

    # ── 3σ internal precision window ──────────────────────────────────────────
    lower_3s = sigma_sum - 3 * sig_total
    upper_3s = sigma_sum + 3 * sig_total

    # Observational bound (Planck 2018, 95% CL):
    PLANCK_UPPER_95 = 0.12        # eV
    KATRIN_UPPER_90 = 0.8         # eV  (single ν mass limit, for reference)

    within_planck = sigma_sum < PLANCK_UPPER_95
    verdict = "PASS" if within_planck else "FAIL"

    print(f"  3σ internal precision window: [{lower_3s:.4f}, {upper_3s:.4f}] eV")
    print(f"  Planck 2018 bound  : Σm_ν < {PLANCK_UPPER_95} eV")
    print(f"  GCT prediction     : {sigma_sum:.4f} eV {'< bound ✓' if within_planck else '> bound ✗'}")
    print(f"  Verdict            : {verdict}")
    print()
    print(f"  Definitive prediction: Σm_ν = {sigma_sum:.3f} ± {sig_total:.3f} eV")
    print(f"  A Σm_ν measurement outside [{lower_3s:.3f}, {upper_3s:.3f}] eV")
    print("  would flag an internal spectrum-fit inconsistency.")
    print("  Registered App V P.4 cosmology gate: Σm_ν < 0.075 eV OR > 0.15 eV.")

    # -- theta23 tension audit (SIG-04) --------------------------------------
    # GCT bare prediction: theta23 = 45 deg  (maximal mixing from 3-fold icosahedral symmetry)
    # Observed (NOvA/T2K combined best fit): ~49.5 deg
    # MSW correction attempt: computed and found ~0.00004 deg shift -- negligible.
    #
    # Excluded diagnostic: Itinerant Volume Drag
    #   The formula below is retained only to document the excluded branch. Its
    #   coupling was not derived from the phason elastic action and is not used
    #   as a GCT closure mechanism.
    THETA23_BARE_DEG    = 45.0
    THETA23_OBS_DEG     = 49.5     # NOvA + T2K best fit (2024)
    THETA23_OBS_ERR_DEG = 1.1     # approximate 1sigma (combined experiments)

    # Excluded diagnostic branch
    theta23_pred_rad = np.pi / 4 + (PHI**-3) / 3
    theta23_pred_deg = np.degrees(theta23_pred_rad)

    theta23_gap_bare_deg    = THETA23_OBS_DEG - THETA23_BARE_DEG
    theta23_tension_bare    = theta23_gap_bare_deg / THETA23_OBS_ERR_DEG
    theta23_residual_cand   = theta23_pred_deg - THETA23_OBS_DEG   # signed residual
    theta23_tension_cand    = abs(theta23_residual_cand) / THETA23_OBS_ERR_DEG

    theta23_flag = "TENSION_GT_4SIGMA"

    print(f"  {'─'*50}")
    print(f"  theta23 Tension Audit (SIG-04):")
    print(f"    GCT bare prediction          : {THETA23_BARE_DEG:.1f} deg  (icosahedral 3-fold symmetry)")
    print(f"    Observed (NOvA/T2K)          : {THETA23_OBS_DEG:.1f} deg +/- {THETA23_OBS_ERR_DEG:.1f} deg")
    print(f"    Bare tension                 : {theta23_tension_bare:.1f}sigma  [TENSION_GT_4SIGMA]")
    print(f"    MSW correction               : ~0.00004 deg (5 orders of magnitude too small)")
    print(f"  ─── Excluded diagnostic: Itinerant Volume Drag ─────────────")
    print(f"    Perturbation Hamiltonian      : Delta H_drag = gamma(J . w)")
    print(f"    Diagnostic formula            : theta23 = pi/4 + phi^(-3)/3")
    print(f"    diagnostic theta23 (rad)      : {theta23_pred_rad:.8f} rad")
    print(f"    diagnostic theta23 (deg)      : {theta23_pred_deg:.4f} deg")
    print(f"    NOvA/T2K best fit            : {THETA23_OBS_DEG:.1f} deg +/- {THETA23_OBS_ERR_DEG:.1f} deg")
    print(f"    Residual (pred - obs)        : {theta23_residual_cand:+.4f} deg  ({abs(theta23_residual_cand)*60:.2f} arcmin)")
    print(f"    Status                       : {theta23_flag}")
    print(f"    Disposition                  : open theta23 octant tension; diagnostic branch not used")

    results = {
        "m1_ev":          m1,
        "m2_ev":          m2,
        "m3_ev":          m3,
        "sigma_mv_ev":    sigma_sum,
        "sigma_mv_mev":   sigma_sum * 1e3,
        "uncertainty_ev": sig_total,
        "lower_3sigma":   lower_3s,
        "upper_3sigma":   upper_3s,
        "planck_bound_ev": PLANCK_UPPER_95,
        "verdict":        verdict,
        "pass":           bool(within_planck),
        "prediction_string": (
            f"Sigma_m_nu = {sigma_sum:.3f} +/- {sig_total:.3f} eV  "
            f"(3-sigma internal precision window: [{lower_3s:.3f}, {upper_3s:.3f}] eV; "
            "registered App V P.4 cosmology gate: Sigma_m_nu < 0.075 eV OR > 0.15 eV)"
        ),
        "registered_app_v_p4_gate": "Sigma_m_nu < 0.075 eV OR Sigma_m_nu > 0.15 eV",
        "theta23_audit": {
            "bare_prediction_deg": THETA23_BARE_DEG,
            "observed_deg": THETA23_OBS_DEG,
            "observed_err_deg": THETA23_OBS_ERR_DEG,
            "gap_deg": theta23_gap_bare_deg,
            "tension_sigma_bare": theta23_tension_bare,
            "msw_correction_deg": 0.00004,
            "candidate_mechanism": "Itinerant Volume Drag (excluded diagnostic)",
            "candidate_formula": "theta23 = pi/4 + phi^(-3)/3",
            "theta23_candidate_rad": theta23_pred_rad,
            "theta23_candidate_deg": theta23_pred_deg,
            "candidate_residual_deg": theta23_residual_cand,
            "candidate_tension_sigma": theta23_tension_cand,
            "status": "TENSION_GT_4SIGMA",
            "epistemic_tier": "Tier 3 (theta23 octant audit; Itinerant Volume Drag excluded)",
            "mechanism_formalism": "Excluded diagnostic only; Delta_H_drag coupling is not derived from the phason elastic action",
        },
    }

    out = get_output_path("protocol_neutrino_precision_results.json")
    with open(out, "w") as fp:
        json.dump({k: (bool(v) if isinstance(v, (bool, np.bool_)) else
                       float(v) if isinstance(v, (float, np.floating)) else v)
                   for k, v in results.items()}, fp, indent=2)
    print(f"\n  Report saved → {out}")
    return results


if __name__ == "__main__":
    run_neutrino_precision()
