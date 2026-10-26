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

The heavier masses are obtained from oscillation data (SSOT values, config/gct_constants.yaml):
    m₂ = √(m₁² + Δm²₂₁)
    m₃ = √(m₁² + Δm²₃₁)   [Normal Ordering]

Uncertainty Budget
------------------
1. Geometric floor: ±0.1% on m₁ from higher-order phason loops.
2. Δm²₂₁ experimental uncertainty (fallback 1σ): ±0.18e−5 eV²
3. Δm²₃₁ experimental uncertainty (fallback 1σ): ±0.028e−3 eV²

θ₂₃ Epistemic Status: WITHIN_3SIGMA_OCTANT_UNRESOLVED (Tier 3)
---------------------------------------------------------------
GCT predicts a bare θ₂₃ = 45° from the 3-fold symmetry constraints
of the icosahedral window. NuFIT 6.0 (normal ordering) places 45° inside
the 3σ range with SK atmospheric data (best fit 43.3°, 3σ 41.3°–49.9°)
and without it (best fit 48.5°, 3σ 41.0°–50.5°); Δχ²(45°) ≈ 2.0 / 4.2.
The earlier 4.09σ figure (a one-octant Gaussian on 49.5° ± 1.1°) is
withdrawn; the octant is unresolved pending DUNE / Hyper-K.

No MSW closure is needed:
  45° lies inside both NuFIT 6.0 3σ ranges, so there is no θ₂₃ gap to
  close. (For reference, the standard Mikheyev-Smirnov-Wolfenstein matter
  effect on θ₂₃ for NOvA/T2K baselines is ~0.00004° and negligible.)

Status - Itinerant Volume Drag excluded:
  An alternative perturbation Δĥ_drag = γ (J · w) (a +4.5° eigenbasis
  rotation diagnostic) is excluded from the registered prediction. Its
  coupling γ is not derived from the phason elastic action, so it is
  excluded as an undisclosed sector handle (see Ch09 §9.4.2).

  The bare 45° value is a Tier 3 statement within the 3σ ranges; the
  octant is open pending DUNE / Hyper-K. No tier promotion is attached to
  any matter-effect derivation.
"""

import json
import sys
import numpy as np
from pathlib import Path


from gct_utils import C, get_output_path

# ── SSOT values ───────────────────────────────────────────────────────────────
PHI          = float(C.PHI)
M_E_EV       = float(C.M_E) * 1e6          # MeV → eV

# Normal Ordering. Central values load from the SSOT (config/gct_constants.yaml:
# Δm²₂₁ = 7.42e-5, Δm²₃₁ = 2.51e-3 eV²); the literals below are fallbacks only.
# 1σ errors used: Δm²₂₁ ± 0.18e-5, Δm²₃₁ ± 0.028e-3 eV².
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
    KATRIN_UPPER_90 = 0.45        # eV  (KATRIN 2025 single-ν mass limit, 90% CL; reference only)

    # The gate is the DESI DR2 BAO + CMB LambdaCDM bound (arXiv:2503.14738),
    # read from the SSOT. The Planck+DESI 2024 (DR1) bound used by
    # verify_independent/verify_neutrino.py and the Planck 2018 bound are kept
    # as named sub-checks; the w0wa bound records the model dependence.
    DESI_DR2_UPPER_95 = float(C.SUM_MNU_BOUND_DESI_DR2)            # 0.0642 eV
    DESI_DR2_W0WA_UPPER_95 = float(C.SUM_MNU_BOUND_DESI_DR2_W0WA)  # 0.16 eV
    PLANCK_DESI_UPPER_95 = float(C.SUM_MNU_BOUND_DESI_2024)        # 0.072 eV
    within_planck_2018 = sigma_sum < PLANCK_UPPER_95
    within_planck = sigma_sum < PLANCK_DESI_UPPER_95
    within_desi_dr2 = sigma_sum < DESI_DR2_UPPER_95
    within_desi_dr2_w0wa = sigma_sum < DESI_DR2_W0WA_UPPER_95
    verdict = ("CONSISTENT_DESI_DR2_LCDM" if within_desi_dr2
               else "TENSION_SIGMA_MNU_ABOVE_DESI_DR2_0P0642_EV_LCDM")

    print(f"  3σ internal precision window: [{lower_3s:.4f}, {upper_3s:.4f}] eV")
    print(f"  Planck 2018 bound  : Σm_ν < {PLANCK_UPPER_95} eV")
    print(f"  Planck+DESI 2024   : Σm_ν < {PLANCK_DESI_UPPER_95} eV")
    print(f"  DESI DR2 + CMB     : Σm_ν < {DESI_DR2_UPPER_95} eV (ΛCDM); < {DESI_DR2_W0WA_UPPER_95} eV (w0wa)")
    print(f"  GCT prediction     : {sigma_sum:.4f} eV; Planck 2018 {'within' if within_planck_2018 else 'outside'}, Planck+DESI 2024 {'within' if within_planck else 'outside'}, DESI DR2 ΛCDM {'within' if within_desi_dr2 else 'outside (tension)'}, DESI DR2 w0wa {'within' if within_desi_dr2_w0wa else 'outside'}")
    print(f"  Verdict            : {verdict}")
    print()
    print(f"  Definitive prediction: Σm_ν = {sigma_sum:.3f} ± {sig_total:.3f} eV")
    print(f"  A Σm_ν measurement outside [{lower_3s:.3f}, {upper_3s:.3f}] eV")
    print("  would flag an internal spectrum-fit inconsistency.")
    print("  Registered App PRG P.4 cosmology gate: Σm_ν < 0.075 eV OR > 0.15 eV.")

    # -- theta23 octant audit (SIG-04) --------------------------------------
    # GCT bare prediction: theta23 = 45 deg  (maximal mixing from 3-fold icosahedral symmetry)
    # NuFIT 6.0 (normal ordering): best fit 48.5 deg without SK atmospheric data,
    # 43.3 deg with it; 45 deg is inside both 3-sigma ranges (octant unresolved).
    # MSW correction contributes a ~0.00004 deg shift and is negligible at this precision.
    #
    # Excluded diagnostic: Itinerant Volume Drag
    #   The formula below is a diagnostic only. Its coupling is not derived from
    #   the phason elastic action and is not a GCT closure mechanism.
    THETA23_BARE_DEG    = 45.0
    THETA23_OBS_DEG     = 48.5     # NuFIT 6.0 NO best fit without SK (upper octant)
    THETA23_OBS_ERR_DEG = 0.9      # NuFIT 6.0 lower 1-sigma error on that fit (non-Gaussian; two-octant likelihood)
    THETA23_DCHI2_45_WITH_SK = 2.02      # NuFIT 6.0 1-D projection, with SK
    THETA23_DCHI2_45_WITHOUT_SK = 4.20   # NuFIT 6.0 1-D projection, without SK

    # Excluded diagnostic branch
    theta23_pred_rad = np.pi / 4 + (PHI**-3) / 3
    theta23_pred_deg = np.degrees(theta23_pred_rad)

    theta23_gap_bare_deg    = THETA23_OBS_DEG - THETA23_BARE_DEG
    theta23_residual_cand   = theta23_pred_deg - THETA23_OBS_DEG   # signed residual

    theta23_flag = "WITHIN_3SIGMA_OCTANT_UNRESOLVED"

    print(f"  {'─'*50}")
    print(f"  theta23 Octant Audit (SIG-04):")
    print(f"    GCT bare prediction          : {THETA23_BARE_DEG:.1f} deg  (icosahedral 3-fold symmetry)")
    print(f"    NuFIT 6.0 (NO, without SK)   : {THETA23_OBS_DEG:.1f} deg (-{THETA23_OBS_ERR_DEG:.1f} deg)")
    print(f"    Delta chi2 at 45 deg          : {THETA23_DCHI2_45_WITH_SK} with SK / {THETA23_DCHI2_45_WITHOUT_SK} without  [WITHIN_3SIGMA_OCTANT_UNRESOLVED]")
    print(f"    MSW correction               : ~0.00004 deg (negligible; no closure needed)")
    print(f"  ─── Excluded diagnostic: Itinerant Volume Drag ─────────────")
    print(f"    Perturbation Hamiltonian      : Delta H_drag = gamma(J . w)")
    print(f"    Diagnostic formula            : theta23 = pi/4 + phi^(-3)/3")
    print(f"    diagnostic theta23 (rad)      : {theta23_pred_rad:.8f} rad")
    print(f"    diagnostic theta23 (deg)      : {theta23_pred_deg:.4f} deg")
    print(f"    NuFIT 6.0 best fit (no SK)   : {THETA23_OBS_DEG:.1f} deg")
    print(f"    Residual (pred - obs)        : {theta23_residual_cand:+.4f} deg  ({abs(theta23_residual_cand)*60:.2f} arcmin)")
    print(f"    Status                       : {theta23_flag}")
    print(f"    Disposition                  : theta23 octant unresolved; diagnostic branch not used")

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
        "within_planck_2018": bool(within_planck_2018),
        "planck_desi_2024_bound_ev": PLANCK_DESI_UPPER_95,
        "within_planck_desi_2024": bool(within_planck),
        "desi_dr2_lcdm_bound_ev": DESI_DR2_UPPER_95,
        "within_desi_dr2_lcdm": bool(within_desi_dr2),
        "desi_dr2_w0wa_bound_ev": DESI_DR2_W0WA_UPPER_95,
        "within_desi_dr2_w0wa": bool(within_desi_dr2_w0wa),
        "gate_source": "DESI DR2 BAO + CMB, 95% CL, LambdaCDM (arXiv:2503.14738); relaxes to < 0.16 eV under w0wa",
        "verdict":        verdict,
        "pass":           bool(within_desi_dr2),
        "prediction_string": (
            f"Sigma_m_nu = {sigma_sum:.3f} +/- {sig_total:.3f} eV  "
            f"(3-sigma internal precision window: [{lower_3s:.3f}, {upper_3s:.3f}] eV; "
            "registered App PRG P.4 cosmology gate: Sigma_m_nu < 0.075 eV OR > 0.15 eV)"
        ),
        "registered_app_v_p4_gate": "Sigma_m_nu < 0.075 eV OR Sigma_m_nu > 0.15 eV",
        "theta23_audit": {
            "bare_prediction_deg": THETA23_BARE_DEG,
            "observed_deg": THETA23_OBS_DEG,
            "observed_err_deg": THETA23_OBS_ERR_DEG,
            "gap_deg": theta23_gap_bare_deg,
            "dchi2_at_45_with_sk": THETA23_DCHI2_45_WITH_SK,
            "dchi2_at_45_without_sk": THETA23_DCHI2_45_WITHOUT_SK,
            "comparator_source": "NuFIT 6.0 (arXiv:2410.05380), normal ordering; gap_deg is against the without-SK best fit",
            "msw_correction_deg": 0.00004,
            "candidate_mechanism": "Itinerant Volume Drag (excluded diagnostic)",
            "candidate_formula": "theta23 = pi/4 + phi^(-3)/3",
            "theta23_candidate_rad": theta23_pred_rad,
            "theta23_candidate_deg": theta23_pred_deg,
            "candidate_residual_deg": theta23_residual_cand,
            "status": "WITHIN_3SIGMA_OCTANT_UNRESOLVED",
            "epistemic_tier": "Tier 3 (theta23 octant unresolved; Itinerant Volume Drag excluded)",
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
