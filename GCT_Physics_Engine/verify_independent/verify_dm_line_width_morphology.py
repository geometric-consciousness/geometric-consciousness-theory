"""
verify_dm_line_width_morphology.py — Independent P.3 width + morphology gate

P.3 is not falsified by the 3.55 keV centroid alone. The operative forward
statistic is the frozen Protocol C stress-aperture rule:

  the operative aperture is mass-weighted stress-gated regions with
  pre-line P_proxy >= sigma_crit = 0.53 keV cm^-3 within the XRISM
  stacked-cluster sample. The Perseus core is sub-sigma_crit and is
  not a falsification aperture. The registered decisive statistic is the full
  Protocol C package: terminal no-line sensitivity
  Gamma <= 2.0e-28 s^-1 in >=94 Ms equivalent stacked exposure, obtained by
  scaling the XRISM 3.75 Ms ten-cluster reference limit Gamma <= 1.0e-27
  s^-1 by sqrt(3.75/94). The 26 Ms / 3.8e-28 s^-1 value is a
  morphology and linewidth milestone, not a terminal no-line falsifier
  for a Bulbul-normalized signal. The background-limited calculation gives
  F_3sigma ~= 1.1e-8 ph/cm^2/s and Gamma <= 1.2e-30 s^-1, but that is
  a theoretical ceiling, not the operative gate for real stacks.
  Decisive null gate operates on the Bulbul-level empirical-derived Gamma floor
  (2.0e-28 s^-1 at >=94 Ms equivalent stacked exposure), not the background-limited
  theoretical flux floor. The flux value, if present, is informational only.
  W_int (deconvolved intrinsic line-width residual after instrumental response
  and the registered kinematic/turbulence model are removed), and a
  stress-gated rho_above_sigma_crit^2 morphology template that must beat both
  smooth rho and smooth rho^2 templates by Delta chi^2 >= 9, with pre-line
  template separation D_sep >= 0.25 so statistical ties do not become false
  morphology failures.

The current public stack is sensitivity-limited, so this verifier executes the
decision rule and returns OPEN_CONDITIONAL until a decisive W_int + morphology
measurement is available.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from report import make_result, write_result, print_summary

W_INT_FALSIFICATION_EV = 20.0
W_INT_CONFIRMATION_EV = 5.0
W_INT_STERILE_COMPATIBLE_EV = 1.0
F_3SIGMA_BACKGROUND_LIMITED_THEORETICAL_PH_CM2_S = 1.1e-8
REQUIRED_STACKED_EXPOSURE_MS = 94.0
GAMMA_DECISIVE_FLOOR_PER_S = 2.0e-28
MORPHOLOGY_MILESTONE_EXPOSURE_MS = 26.0
MORPHOLOGY_MILESTONE_GAMMA_PER_S = 3.8e-28
XRISM_REFERENCE_GAMMA_LIMIT_S_INV = 1.0e-27
XRISM_REFERENCE_EXPOSURE_MS = 3.75
BACKGROUND_LIMITED_THEORETICAL_DECAY_RATE_S_INV = 1.2e-30
HITOMI_EQUIV_BACKGROUND_LIMITED_THEORETICAL_PH_CM2_S = 2.8e-8
MORPHOLOGY_DELTA_CHI2_REQUIRED = 9.0
SIGMA_CRIT_KEV_CM3 = 0.53
P_PERSEUS_CORE_KEV_CM3 = 0.07
P_BULLET_SHOCK_CENTRAL_KEV_CM3 = 4.0
MORPHOLOGY_BACKGROUND_COUNTS_26MS = 343.0
MORPHOLOGY_SOURCE_COUNTS_3SIGMA_26MS = 55.6
FROZEN_TARGET_CELLS = (
    "Bullet bow-shock/Mach shell; Coma merger/radio-relic shells; "
    "A2142 cold-front/merger shell; A3667/A2256/A2319 shock or merger "
    "shells; off-core Perseus/A2029/A1795 annuli only where pre-line "
    "P_proxy >= 0.53 keV cm^-3; relaxed cool cores excluded unless their "
    "pre-line maps exceed the cut."
)


def evaluate_gate(
    line_detected=None,
    line_flux_ph_cm2_s=None,
    stacked_exposure_Ms=None,
    gamma_limit_s_inv=None,
    w_int_eV=None,
    stress_vs_smooth_rho_delta_chi2=None,
    stress_vs_smooth_rho2_delta_chi2=None,
    template_separation_D_sep=None,
    s1_s6_controls_pass=False,
) -> str:
    """Return the registered P.3 decision for a supplied XRISM/Athena result.

    Decisive null gate operates on the Bulbul-level empirical-derived Gamma floor
    (2.0e-28 s^-1 at >=94 Ms equivalent stacked exposure), not the background-limited
    theoretical flux floor. The flux value, if present, is informational only.
    """
    if not s1_s6_controls_pass:
        return "OPEN_CONDITIONAL"

    if stacked_exposure_Ms is None or gamma_limit_s_inv is None:
        return "OPEN_CONDITIONAL"

    decisive_sensitivity = (
        stacked_exposure_Ms >= REQUIRED_STACKED_EXPOSURE_MS
        and gamma_limit_s_inv <= GAMMA_DECISIVE_FLOOR_PER_S
    )
    if not decisive_sensitivity:
        return "OPEN_CONDITIONAL"

    no_line_at_decisive_flux = decisive_sensitivity and line_detected is False
    if no_line_at_decisive_flux:
        return "FAIL"

    if line_detected is not True:
        return "OPEN_CONDITIONAL"

    if w_int_eV is None:
        return "OPEN_CONDITIONAL"
    if w_int_eV > W_INT_FALSIFICATION_EV:
        return "FAIL"

    if template_separation_D_sep is None:
        return "OPEN_CONDITIONAL"
    if template_separation_D_sep < 0.25:
        return "OPEN_CONDITIONAL"

    if (
        stress_vs_smooth_rho_delta_chi2 is None
        or stress_vs_smooth_rho2_delta_chi2 is None
    ):
        return "OPEN_CONDITIONAL"

    smooth_template_wins = (
        stress_vs_smooth_rho_delta_chi2 <= -MORPHOLOGY_DELTA_CHI2_REQUIRED
        or stress_vs_smooth_rho2_delta_chi2 <= -MORPHOLOGY_DELTA_CHI2_REQUIRED
    )
    if smooth_template_wins:
        return "FAIL"

    morphology_passes = (
        stress_vs_smooth_rho_delta_chi2 >= MORPHOLOGY_DELTA_CHI2_REQUIRED
        and stress_vs_smooth_rho2_delta_chi2 >= MORPHOLOGY_DELTA_CHI2_REQUIRED
    )
    if not morphology_passes:
        return "OPEN_CONDITIONAL"

    if w_int_eV <= W_INT_CONFIRMATION_EV:
        return "PASS"
    return "OPEN_CONDITIONAL"


def main():
    status = evaluate_gate()
    res = make_result(
        name="dm_line_width_morphology",
        app_r_label="3.55 keV line width + morphology gate (P.3)",
        formula="P.3 decisive gate: terminal no-line Gamma<=2.0e-28 s^-1 in >=94 Ms equivalent (XRISM 3.75 Ms stack Gamma<=1.0e-27 scaled by sqrt(3.75/94)); 26 Ms/Gamma<=3.8e-28 is a morphology-linewidth milestone; W_int>20 eV; morphology Delta chi^2>=9 vs smooth rho and smooth rho^2 with D_sep>=0.25. Background-limited Gamma<=1.2e-30 is theoretical, not operative.",
        predicted=W_INT_FALSIFICATION_EV,
        observed=None,
        unit="eV",
        app_r_predicted=20.0,
        app_r_precision_str="OPEN_CONDITIONAL (awaiting decisive Gamma/exposure + W_int + Delta chi^2 morphology)",
        tier="Tier 2 linewidth/morphology mechanism",
        status=status,
        tolerance_ppm=None,
        extra={
            "falsification_width_eV": W_INT_FALSIFICATION_EV,
            "confirmation_width_eV": W_INT_CONFIRMATION_EV,
            "sterile_compatible_width_eV": W_INT_STERILE_COMPATIBLE_EV,
            "f_3sigma_background_limited_theoretical_ph_cm2_s": F_3SIGMA_BACKGROUND_LIMITED_THEORETICAL_PH_CM2_S,
            "hitomi_equivalent_3p75Ms_background_limited_theoretical_ph_cm2_s": HITOMI_EQUIV_BACKGROUND_LIMITED_THEORETICAL_PH_CM2_S,
            "required_stacked_exposure_Ms": REQUIRED_STACKED_EXPOSURE_MS,
            "gamma_decisive_floor_per_s": GAMMA_DECISIVE_FLOOR_PER_S,
            "morphology_milestone_exposure_Ms": MORPHOLOGY_MILESTONE_EXPOSURE_MS,
            "morphology_milestone_gamma_per_s": MORPHOLOGY_MILESTONE_GAMMA_PER_S,
            "xrism_reference_gamma_limit_s_inv": XRISM_REFERENCE_GAMMA_LIMIT_S_INV,
            "xrism_reference_exposure_Ms": XRISM_REFERENCE_EXPOSURE_MS,
            "background_limited_theoretical_decay_rate_s_inv": BACKGROUND_LIMITED_THEORETICAL_DECAY_RATE_S_INV,
            "morphology_delta_chi2_required_vs_each_smooth_template": MORPHOLOGY_DELTA_CHI2_REQUIRED,
            "minimum_template_separation_D_sep": 0.25,
            "sigma_crit_keV_cm3": SIGMA_CRIT_KEV_CM3,
            "sigma_crit_derivation": (
                "sqrt(P_Perseus_core * P_Bullet_shock_central) = "
                "sqrt(0.07 * 4.0) keV cm^-3"
            ),
            "p_perseus_core_keV_cm3": P_PERSEUS_CORE_KEV_CM3,
            "p_bullet_shock_central_keV_cm3": P_BULLET_SHOCK_CENTRAL_KEV_CM3,
            "frozen_target_cells": FROZEN_TARGET_CELLS,
            "morphology_background_counts_26Ms": MORPHOLOGY_BACKGROUND_COUNTS_26MS,
            "morphology_source_counts_3sigma_26Ms": MORPHOLOGY_SOURCE_COUNTS_3SIGMA_26MS,
            "decision_rule": (
                "Protocol C operative aperture is mass-weighted stress-gated "
                "regions with pre-line P_proxy >= sigma_crit = 0.53 keV cm^-3 "
                "in the XRISM stacked-cluster sample. "
                "GCT is falsified at terminal no-line sensitivity if no 3.55 "
                "keV line is detected at Gamma<=2.0e-28 s^-1 in >=94 Ms "
                "equivalent, or if a detected line has W_int>20 eV, "
                "or if a smooth rho or smooth rho^2 template beats the "
                "stress-gated rho_above_sigma_crit^2 template by Delta chi^2 "
                ">=9 after pre-line template separation D_sep>=0.25 is "
                "established. If the stress template does not beat both smooth "
                "templates by Delta chi^2>=9 but neither smooth template wins "
                "decisively, the morphology branch remains OPEN_CONDITIONAL, "
                "not FAIL. "
                "The background-limited F_3sigma~=1.1e-8 ph/cm^2/s "
                "(Gamma<=1.2e-30 s^-1) is theoretical, not operative. "
                "At 26 Ms, B~=343 and 3sqrt(B)~=55.6 counts power "
                "Delta chi^2>=9 for the registered morphology degree of "
                "freedom when the pre-line stress template is separated from "
                "both smooth templates. Centroid agreement is postdiction context."
            ),
        },
    )
    print_summary(res)
    write_result(res)
    return res


if __name__ == "__main__":
    main()
