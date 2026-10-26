"""
verify_electron_mass.py - Independent re-derivation of m_e

App PSC Sec PSC.1 row 1:
    Formula: m_e = M_P * phi^(-107) * (1 - 5 alpha)
    App PSC claims: 0.511513 MeV (engine), 1006 ppm vs CODATA
    Tier: Tier 2 mechanism + Tier 3 anchor + Tier 4 K-theoretic physical-link conjecture pending O.14

The independent re-derivation uses:
    - CODATA 2022 M_P (standard Planck mass, derived from CODATA hbar, c, G)
    - CODATA 2022 alpha

NB the engine uses M_E_OBS as the dimensional anchor and inverts the formula
to derive a_6, then closes the loop via Jacobson. This script tests the
forward direction: given (M_P, alpha, phi, exponent=-107, drag=5), compute m_e.
That is the direct test of the App PSC formula as stated.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import CODATA, MATH, kg_to_mev, ppm_error
from report import make_result, write_result, print_summary

# GCT formula parameters (from manuscript Sec PSC.1, Ch08, App GPE)
N_GEOM = -107      # 6D vacancy exponent (108 volumetric, +1 vacancy)
N_PHASON = 5       # phason drag channels (5 alpha)


def main():
    phi = MATH.PHI
    M_P_kg = CODATA.M_PLANCK_STD_KG  # CODATA-derived
    alpha = CODATA.ALPHA              # CODATA 2022

    # Forward derivation: m_e = M_P * phi^(-107) * (1 - 5 alpha)
    m_e_kg = M_P_kg * (phi ** N_GEOM) * (1.0 - N_PHASON * alpha)
    m_e_mev = kg_to_mev(m_e_kg)

    observed = CODATA.M_E_MEV
    app_psc_engine_value = 0.5115131    # MeV, App PSC canonical forward-formula value on CODATA inputs
    app_psc_precision_ppm = 1006.166    # App PSC canonical ppm on CODATA inputs

    independent_ppm = ppm_error(m_e_mev, observed)
    # The LOCKED pre-commitment in
    # config/falsification_thresholds.json (1000 ppm) is the binding rule. The
    # 1006 ppm residual misses it by 6 ppm, so the row FAILS the locked rule.
    # The later 1200/1500 ppm bands are non-retroactive and are not used here.
    tolerance_ppm = 1000.0
    status = "PASS" if independent_ppm <= tolerance_ppm else "FAIL"

    result = make_result(
        name="electron_mass",
        app_psc_label="Electron mass (m_e)",
        formula="m_e = M_P_std * phi^(-107) * (1 - 5 alpha)",
        predicted=m_e_mev,
        observed=observed,
        unit="MeV",
        app_psc_predicted=app_psc_engine_value,
        app_psc_precision_str=f"{independent_ppm:.1f} ppm on CODATA-2022 inputs (App PSC canonical: {app_psc_precision_ppm:.0f} ppm)",
        app_psc_precision_ppm=app_psc_precision_ppm,
        tier="Tier 2 mechanism + Tier 3 anchor + Tier 4 K-theoretic physical-link conjecture pending O.14 + Tier 4 as evidence that phi explains the value (constant control test v3 NEGATIVE-FRAGILE; App PSC §PSC.9.6)",
        status=status,
        tolerance_ppm=tolerance_ppm,
        extra={
            "M_P_std_kg": M_P_kg,
            "alpha_used": alpha,
            "alpha_source": "CODATA 2022",
            "N_geom": N_GEOM,
            "drag_factor_5alpha": 5 * alpha,
            "binding_rule": "LOCKED 1000 ppm (config/falsification_thresholds.json)",
            "later_non_retroactive_band_ppm": 1500.0,
        },
    )

    # Cross-branch consistency: also evaluate the formula on GCT-bare alpha
    alpha_gct = (MATH.PHI ** 2) / 360.0
    m_e_gct_alpha_kg = M_P_kg * (phi ** N_GEOM) * (1.0 - N_PHASON * alpha_gct)
    m_e_gct_alpha_mev = kg_to_mev(m_e_gct_alpha_kg)
    ppm_gct = ppm_error(m_e_gct_alpha_mev, observed)
    result["extra"]["alpha_gct_branch_ppm"] = ppm_gct
    result["extra"]["alpha_gct_branch_m_e_MeV"] = m_e_gct_alpha_mev
    result["extra"]["alpha_branch_note"] = (
        "Branch precision on GCT-bare alpha = phi^2/360 reported for transparency; "
        "the canonical App PSC value uses CODATA-2022 alpha throughout."
    )

    engine_ppm = result["independent_precision_ppm"]
    if engine_ppm is not None and abs(engine_ppm - app_psc_precision_ppm) > 50.0:
        result["discrepancy_notes"].append(
            f"Independent ppm ({engine_ppm:.1f}) differs from App PSC canonical "
            f"({app_psc_precision_ppm:.1f} ppm) by {abs(engine_ppm-app_psc_precision_ppm):.1f} ppm."
        )

    print_summary(result)
    write_result(result)
    return result


if __name__ == "__main__":
    main()
