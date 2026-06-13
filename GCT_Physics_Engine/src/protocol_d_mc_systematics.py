#!/usr/bin/env python3
"""
protocol_d_mc_systematics.py

End-to-end Monte Carlo for Protocol D (Drosophila ^17O LORR
isotope-shift assay), propagating the six systematics enumerated in
V3 Ch16 sec 16.3.4 through a Hill-equation C50 estimator
and reporting:

  - The empirical false-positive rate at the Delta_C50 / C50 = 0.10%
    falsification gate under the null hypothesis (zero true effect).
  - The empirical statistical power at the predicted effect sizes
    Delta_C50 / C50 = 0.10% and 0.20% under a parametric Gaussian
    z-test gate (the parametric gate has well-defined precision at the
    N=10,000 sample size; empirical-quantile gates at small N return
    sample-size artefacts).
  - The systematic-only uncertainty budget per source.
  - C1-tightened-budget and C2-widened-gate sub-runs.

The six systematics modelled (V3 Ch16 sec 16.3.4):

  S1  LORR scorer variance              (inter-rater dispersion)
  S2  ^17O enrichment efficiency        (95 +/- 2.5% substitution) —
                                         perturbs BOTH the true-effect
                                         signal attenuation AND the
                                         synthetic control dose-response
                                         data (per-trial independent
                                         draws on both branches, so S2
                                         enters the null-distribution
                                         SD via a residual enrichment-
                                         efficiency-induced spurious
                                         shift)
  S3  Multi-generation rearing confound (lineage drift)
  S4  Anaesthetic atmosphere uniformity (+/- 2% chamber variation)
  S5  Dose-response curve-fit method    (logistic vs probit ~1% spread)
  S6  Drug pharmacokinetics             (Drosophila partition coefficient)

The naive false-positive rate at the 0.10% gate under the null is
reported explicitly as a top-level field
(`false_positive_rate_at_confidence_99pct_gate_under_null_naive`) in the JSON
output and is disclosed in the §16.3.4 chapter prose's operative-
implication paragraph. C1-tightened and C2-widened-gate sub-runs are
executed and their empirical powers reported alongside the registered-
budget result.

Tier 2 mechanism (Hill-equation fit on bootstrap synthetic data) +
Tier 3 specific systematic-variance values (calibrated from V3 Ch16
sec 16.3.4).

Output: data/protocol_d_mc_systematics_results.json
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np


# -----------------------------------------------------------------------------
# Verification target: Protocol D design parameters registered in V3 Ch16
# sec 16.3.4. These are experimental-design inputs, not GCT anchors.
# -----------------------------------------------------------------------------

N_FLIES_PER_POINT = 250
N_CONCENTRATION_POINTS = 5
N_F2_GENERATIONS = 3
N_ANAESTHETICS = 3            # isoflurane, sevoflurane, propofol

# External empirical prior: reference C50 for isoflurane in Drosophila
# (Olufs et al. 2018 Sci Rep 8:2348).
C50_REF_ISO = 0.40            # vol% MAC, approximate central value

# External empirical prior: Hill slope literature range 5-15 for volatile
# anaesthetic LORR; 8 is representative.
HILL_SLOPE_REF = 8.0

# Verification target: concentration grid for the registered assay design.
DOSE_GRID_FRAC = np.array([0.5, 0.7, 1.0, 1.4, 2.0])

# MD-derived sensitivity band [O.21/O.33]: the operative central branch is
# n_rp = 0 pending O.21 closure. The n_rp = 1 branch is retained only as a
# conditional sensitivity scenario for systematics sizing.
DELTA_C50_LOWER_BAND = 0.0010   # 0.10% (n_rp = 1 sensitivity lower; O.21/O.33)
DELTA_C50_UPPER_BAND = 0.0020   # 0.20% (n_rp = 1 sensitivity upper; O.21/O.33)
P_THRESHOLD = 0.001              # Bonferroni-corrected per anaesthetic

# Tier 3 calibrated anchor [V3 Ch16]: registered systematic budgets
# (multiplicative SD on the relevant parameter).
SYSTEMATIC_BUDGETS_REGISTERED = {
    "S1_scorer_variance":          0.005,   # 0.5% per-fly scoring uncertainty
    "S2_17O_enrichment":           0.025,   # 95 +/- 2.5% substitution
    "S3_multi_generation":         0.003,   # 0.3% lineage drift
    "S4_atmosphere_uniformity":    0.020,   # +/- 2% chamber concentration
    "S5_curve_fit_method":         0.010,   # 1% logistic-vs-probit
    "S6_pharmacokinetics":         0.015,   # 1.5% PK variability
}

# Verification target: C1 closure-path budgets halve S2 + S4 for assay-design
# sensitivity; not a theoretical fit.
SYSTEMATIC_BUDGETS_C1 = dict(SYSTEMATIC_BUDGETS_REGISTERED)
SYSTEMATIC_BUDGETS_C1["S2_17O_enrichment"] = 0.0125
SYSTEMATIC_BUDGETS_C1["S4_atmosphere_uniformity"] = 0.010

# Verification target: C2 closure path widens the gate to the upper edge of
# the operative band.
DELTA_C50_GATE_C2 = 0.0020

# Numerical reproducibility settings for the Monte Carlo estimator; not
# physical constants.
N_MC_TRIALS = 10000
RNG_SEED = 20260524


# -----------------------------------------------------------------------------
# Hill equation
# -----------------------------------------------------------------------------

def hill(c, top, bottom, c50, hill_slope):
    """4-parameter logistic Hill equation."""
    return bottom + (top - bottom) / (1.0 + (c50 / np.maximum(c, 1e-12)) ** hill_slope)


def realize_systematics(rng, budgets):
    """Draw one realization of the 6 systematics for a single trial."""
    return {
        "S1_scorer_sigma":   abs(rng.normal(0.0, budgets["S1_scorer_variance"] * N_FLIES_PER_POINT)),
        "S2_17O_enrich":     rng.normal(0.0, budgets["S2_17O_enrichment"]),
        "S3_generation":     rng.normal(0.0, budgets["S3_multi_generation"]),
        "S4_atmosphere":     rng.normal(0.0, budgets["S4_atmosphere_uniformity"]),
        "S5_fit_method":     rng.normal(0.0, budgets["S5_curve_fit_method"]),
        "S6_pk":             rng.normal(0.0, budgets["S6_pharmacokinetics"]),
    }


def generate_synthetic_dose_response(c50_true, hill_slope, n_per_point, dose_grid, rng, sys_realization):
    """Generate synthetic LORR data with one realization of the 6 systematics
    applied. The systematics that affect C50 *both* on the ^16O control cohort
    and the ^17O cohort are S3, S4, S5, S6, and S2."""
    # S2 contributes a residual ¹⁶O <-> ¹⁷O enrichment-mismatch shift on
    # any cohort whose enrichment efficiency drifts from the nominal 95%.
    # Even on the ¹⁶O control cohort there is a sub-percent residual ¹⁷O
    # baseline contribution from natural-isotope abundance + enrichment-
    # process residuals, which S2 captures as a per-cohort C50 perturbation.
    c50_eff = c50_true \
        * (1.0 + sys_realization["S2_17O_enrich"]) \
        * (1.0 + sys_realization["S4_atmosphere"]) \
        * (1.0 + sys_realization["S6_pk"]) \
        * (1.0 + sys_realization["S3_generation"])
    hill_eff = hill_slope * (1.0 + sys_realization["S5_fit_method"])

    p_lorr = hill(dose_grid, top=1.0, bottom=0.0, c50=c50_eff, hill_slope=hill_eff)
    p_lorr = np.clip(p_lorr, 1e-6, 1.0 - 1e-6)
    n_lorr = rng.binomial(n_per_point, p_lorr)
    scorer_smear = rng.normal(0.0, sys_realization["S1_scorer_sigma"], size=n_lorr.shape)
    n_lorr = np.clip(n_lorr + scorer_smear, 0, n_per_point).astype(int)
    return dose_grid, n_lorr


def fit_hill_extract_c50(dose_grid, n_lorr, n_per_point, hill_slope_init):
    """Estimate C50 from the Hill-equation logit form.

    With top=1 and bottom=0, logit(y) = h*log(c) - h*log(C50).
    A two-parameter least-squares fit on the logit transform preserves the
    Hill C50 statistic while avoiding a nonlinear optimizer inside each MC
    trial.
    """
    y = np.asarray(n_lorr, dtype=float) / float(n_per_point)
    eps = 0.5 / float(n_per_point)
    y = np.clip(y, eps, 1.0 - eps)
    logit_y = np.log(y / (1.0 - y))
    x = np.log(np.asarray(dose_grid, dtype=float))
    design = np.column_stack([np.ones_like(x), x])
    try:
        intercept, slope = np.linalg.lstsq(design, logit_y, rcond=None)[0]
        if not math.isfinite(slope) or abs(slope) < 1e-12:
            return float("nan")
        c50 = math.exp(-intercept / slope)
        if 1e-3 <= c50 <= 10.0:
            return c50
    except Exception:
        pass
    return float("nan")


def one_trial(true_effect_size, rng, budgets):
    """One MC trial. Independent S2 draws on the ¹⁶O and ¹⁷O cohorts."""
    sys_16 = realize_systematics(rng, budgets)
    c50_16_true = C50_REF_ISO
    _, n_lorr_16 = generate_synthetic_dose_response(
        c50_16_true, HILL_SLOPE_REF, N_FLIES_PER_POINT,
        DOSE_GRID_FRAC * c50_16_true, rng, sys_16,
    )
    c50_16_fit = fit_hill_extract_c50(
        DOSE_GRID_FRAC * c50_16_true, n_lorr_16, N_FLIES_PER_POINT, HILL_SLOPE_REF
    )

    sys_17 = realize_systematics(rng, budgets)
    # Effective true effect is attenuated by enrichment efficiency drift on
    # the ¹⁷O cohort — and S2 ALSO perturbs the
    # synthetic data on the ¹⁷O cohort via the c50_eff multiplication above.
    enrichment_efficiency = max(0.0, min(1.0, 0.95 * (1.0 + sys_17["S2_17O_enrich"])))
    effective_effect = true_effect_size * enrichment_efficiency
    c50_17_true = c50_16_true * (1.0 - effective_effect)
    _, n_lorr_17 = generate_synthetic_dose_response(
        c50_17_true, HILL_SLOPE_REF, N_FLIES_PER_POINT,
        DOSE_GRID_FRAC * c50_16_true, rng, sys_17,
    )
    c50_17_fit = fit_hill_extract_c50(
        DOSE_GRID_FRAC * c50_16_true, n_lorr_17, N_FLIES_PER_POINT, HILL_SLOPE_REF
    )

    if not (math.isfinite(c50_16_fit) and math.isfinite(c50_17_fit)):
        return float("nan")
    return (c50_16_fit - c50_17_fit) / c50_16_fit


def run_mc(true_effect_size, n_trials, rng, budgets):
    measured = np.zeros(n_trials)
    for i in range(n_trials):
        measured[i] = one_trial(true_effect_size, rng, budgets)
    return measured[np.isfinite(measured)]


def parametric_power(null_dist, effect_dist, p_critical):
    """parametric Gaussian z-test power at Bonferroni-
    corrected significance. Uses the null-distribution SD as the
    z-statistic denominator; the gate is a two-tailed |z| > z_critical
    threshold derived from p_critical, applied to the measured
    |Delta_C50/C50| - 0 difference from the null mean."""
    from scipy.stats import norm
    z_critical = float(norm.ppf(1.0 - p_critical / 2.0))
    null_sd = float(np.std(null_dist))
    if null_sd <= 0:
        return float("nan")
    gate = z_critical * null_sd
    return float(np.mean(np.abs(effect_dist) >= gate))


def empirical_fpr(measured_distribution, gate_threshold):
    """Empirical one-sided false-positive rate: fraction of trials in
    which the measured |Delta_C50/C50| exceeds the gate threshold."""
    return float(np.mean(np.abs(measured_distribution) >= gate_threshold))


def summarize_distribution(d):
    if len(d) == 0:
        return None
    return {
        "n_valid": int(len(d)),
        "mean": float(np.mean(d)),
        "sd": float(np.std(d)),
        "p5_p95": (float(np.percentile(d, 5)), float(np.percentile(d, 95))),
    }


def run():
    rng = np.random.default_rng(RNG_SEED)

    p_critical = P_THRESHOLD / N_ANAESTHETICS

    print(f"Running Monte Carlo for Protocol D systematics (N={N_MC_TRIALS} trials)...")
    print(f"  Bonferroni p_critical per anaesthetic: {p_critical:.2e}")
    print()

    # === REGISTERED BUDGET MC ===
    print("=== Registered §16.3.4 systematic-error budget ===")
    print("  ... null hypothesis (true effect = 0)")
    null_reg = run_mc(0.0, N_MC_TRIALS, rng, SYSTEMATIC_BUDGETS_REGISTERED)
    print(f"     ({len(null_reg)}/{N_MC_TRIALS} valid)")

    print("  ... lower-band effect (true effect = 0.10%)")
    lower_reg = run_mc(DELTA_C50_LOWER_BAND, N_MC_TRIALS, rng, SYSTEMATIC_BUDGETS_REGISTERED)
    print(f"     ({len(lower_reg)}/{N_MC_TRIALS} valid)")

    print("  ... upper-band effect (true effect = 0.20%)")
    upper_reg = run_mc(DELTA_C50_UPPER_BAND, N_MC_TRIALS, rng, SYSTEMATIC_BUDGETS_REGISTERED)
    print(f"     ({len(upper_reg)}/{N_MC_TRIALS} valid)")

    # === C1 TIGHTENED BUDGET MC (halve S2 + S4) ===
    print()
    print("=== C1 closure path: halved S2 + S4 budgets ===")
    print("  ... null + lower-band + upper-band")
    null_C1 = run_mc(0.0, N_MC_TRIALS, rng, SYSTEMATIC_BUDGETS_C1)
    lower_C1 = run_mc(DELTA_C50_LOWER_BAND, N_MC_TRIALS, rng, SYSTEMATIC_BUDGETS_C1)
    upper_C1 = run_mc(DELTA_C50_UPPER_BAND, N_MC_TRIALS, rng, SYSTEMATIC_BUDGETS_C1)
    print(f"     ({len(null_C1)}/{N_MC_TRIALS} valid each)")

    # === Statistics: registered budget ===
    null_reg_sd = float(np.std(null_reg))
    fpr_naive_reg = empirical_fpr(null_reg, DELTA_C50_LOWER_BAND)

    power_reg_027_parametric = parametric_power(null_reg, lower_reg, p_critical)
    power_reg_055_parametric = parametric_power(null_reg, upper_reg, p_critical)

    # === Statistics: C1 closure path ===
    null_C1_sd = float(np.std(null_C1))
    power_C1_027 = parametric_power(null_C1, lower_C1, p_critical)
    power_C1_055 = parametric_power(null_C1, upper_C1, p_critical)

    # === Statistics: C2 closure path (widen gate to 0.20%) ===
    # C2 is a *gate change* under the *registered* budget, not a budget change
    fpr_C2_reg = empirical_fpr(null_reg, DELTA_C50_GATE_C2)
    # Empirical-gate-based power at the widened gate (C2 is essentially a
    # one-sided | measured | >= gate test; we report the empirical power)
    power_C2_055_empirical_gate = empirical_fpr(upper_reg, DELTA_C50_GATE_C2)
    power_C2_027_empirical_gate = empirical_fpr(lower_reg, DELTA_C50_GATE_C2)

    PASS_target_power = 0.80
    PASS_max_fpr = 0.05
    c2_valid_power = (
        power_C2_055_empirical_gate >= PASS_target_power
        and fpr_C2_reg <= PASS_max_fpr
    )
    # Pass criterion: a closure path must recover power >= PASS_target_power
    # without losing the false-positive-rate gate. C2's high empirical
    # "power" is invalid if it is just the null false-positive rate.
    closure_pass = (
        power_C1_027 >= PASS_target_power
        or power_C1_055 >= PASS_target_power
        or c2_valid_power
    )

    target_met_registered = power_reg_027_parametric >= PASS_target_power

    # Verdict status: the registered budget pre-registered '>= 0.85 at 0.10%'
    # is operationally unsupported by the MC; the disposition is the
    # EXPECTED_NON_PASS structural finding.
    if target_met_registered:
        verdict_status = "PASS_PROTOCOL_D_POWER_TARGET_AT_010_PCT_EFFECT"
    else:
        verdict_status = "BELOW_TARGET_POWER_AT_010_PCT_EFFECT_UNDER_BONFERRONI_CORRECTION"

    results = {
        "tier": "Tier 2 mechanism (Hill-equation C50 estimator on bootstrap synthetic data, with parametric Gaussian z-test gate at Bonferroni-corrected significance) + Tier 3 specific systematic-variance values (calibrated from V3 Ch16 sec 16.3.4)",
        "inputs": {
            "N_flies_per_point": N_FLIES_PER_POINT,
            "N_concentration_points": N_CONCENTRATION_POINTS,
            "N_F2_generations": N_F2_GENERATIONS,
            "N_anaesthetics": N_ANAESTHETICS,
            "C50_ref_iso": C50_REF_ISO,
            "Hill_slope_ref": HILL_SLOPE_REF,
            "dose_grid_frac": DOSE_GRID_FRAC.tolist(),
            "delta_C50_lower_band": DELTA_C50_LOWER_BAND,
            "delta_C50_upper_band": DELTA_C50_UPPER_BAND,
            "delta_C50_gate_C2": DELTA_C50_GATE_C2,
            "p_threshold_per_anaesthetic": p_critical,
            "systematic_budgets_registered": SYSTEMATIC_BUDGETS_REGISTERED,
            "systematic_budgets_C1": SYSTEMATIC_BUDGETS_C1,
            "N_MC_trials": N_MC_TRIALS,
            "pass_target_power": PASS_target_power,
            "pass_max_false_positive_rate": PASS_max_fpr,
        },
        "registered_budget": {
            "null_distribution": summarize_distribution(null_reg),
            "lower_band_distribution": summarize_distribution(lower_reg),
            "upper_band_distribution": summarize_distribution(upper_reg),
            "false_positive_rate_at_confidence_99pct_gate_under_null_naive": fpr_naive_reg,
            "systematic_only_SD_total": null_reg_sd,
            "systematic_only_SD_relative_to_gate": null_reg_sd / DELTA_C50_LOWER_BAND,
            "statistical_power_at_0p10pct_effect_confidence_99pct_gaussian_gate": power_reg_027_parametric,
            "statistical_power_at_0p20pct_effect_confidence_99pct_gaussian_gate": power_reg_055_parametric,
            "target_met_at_0p10pct_effect": target_met_registered,
        },
        "closure_path_C1_halve_S2_S4": {
            "null_distribution": summarize_distribution(null_C1),
            "systematic_only_SD_total": null_C1_sd,
            "systematic_only_SD_reduction_factor_vs_registered": null_reg_sd / null_C1_sd if null_C1_sd > 0 else float("nan"),
            "statistical_power_at_0p10pct_effect": power_C1_027,
            "statistical_power_at_0p20pct_effect": power_C1_055,
            "target_met_at_0p10pct_effect": power_C1_027 >= PASS_target_power,
            "target_met_at_0p20pct_effect": power_C1_055 >= PASS_target_power,
        },
        "closure_path_C2_widen_gate_to_020_pct": {
            "false_positive_rate_at_0p20pct_gate_under_null_registered_budget": fpr_C2_reg,
            "statistical_power_at_0p10pct_effect_with_0p20pct_gate_empirical": power_C2_027_empirical_gate,
            "statistical_power_at_0p20pct_effect_with_0p20pct_gate_empirical": power_C2_055_empirical_gate,
            "target_met_at_0p20pct_effect": power_C2_055_empirical_gate >= PASS_target_power,
            "target_met_at_0p20pct_effect_with_false_positive_gate": c2_valid_power,
        },
        "closure_path_pass_at_least_one_of_C1_C2": closure_pass,
        "verdict_status": verdict_status,
        "verdict": (
            f"Under the §16.3.4 registered systematic-error budget, the empirical "
            f"statistical power at the predicted lower-bound effect 0.10% under "
            f"Bonferroni-corrected per-anaesthetic significance (p < {p_critical:.4f}, "
            f"parametric Gaussian z-test) is {power_reg_027_parametric:.2f}; "
            f"at 0.20% true effect it is {power_reg_055_parametric:.2f}. "
            f"The systematic-only SD = {null_reg_sd:.4f} sits at "
            f"{null_reg_sd / DELTA_C50_LOWER_BAND:.2f}x the naive 0.10% gate, "
            f"and the naive 0.10% gate has a {fpr_naive_reg:.2f} false-positive "
            f"rate under the null hypothesis — the gate is below the noise "
            f"floor. The C1 closure path (halve S2 + S4 budgets) reduces the "
            f"systematic SD by {null_reg_sd / null_C1_sd:.2f}x and recovers "
            f"power {power_C1_027:.2f} at 0.10% and {power_C1_055:.2f} at 0.20%. "
            f"The C2 closure path (widen gate to 0.20%) reports empirical-gate "
            f"power {power_C2_055_empirical_gate:.2f} at the 0.20% effect under "
            f"the registered budget, but its null false-positive rate is "
            f"{fpr_C2_reg:.2f}; because the allowed false-positive rate is "
            f"{PASS_max_fpr:.2f}, C2 is not a valid closure path unless that "
            f"gate is also satisfied. {'At least one closure path achieves the ≥ 0.80 target power with false-positive control.' if closure_pass else 'No closure path achieves the target with false-positive control.'}"
        ),
        "pass": target_met_registered,  # registered-budget pass criterion;
                                          # closure_path_pass is reported separately
    }

    out_dir = Path(__file__).parent.parent / "data"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "protocol_d_mc_systematics_results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=4, default=str)
    print(f"\nResults written to {out_path}")
    return results


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    r = run()
    print("\n" + "=" * 76)
    print("Protocol D Monte Carlo Systematics — Verdict Summary")
    print("=" * 76)
    rb = r["registered_budget"]
    print(f"  REGISTERED budget:")
    print(f"    Systematic-only SD vs gate: {rb['systematic_only_SD_relative_to_gate']:.2f}x")
    print(f"    Naive 0.10% FPR under null: {rb['false_positive_rate_at_confidence_99pct_gate_under_null_naive']:.3f}")
    print(f"    Parametric power at 0.10%: {rb['statistical_power_at_0p10pct_effect_confidence_99pct_gaussian_gate']:.2f}")
    print(f"    Parametric power at 0.20%: {rb['statistical_power_at_0p20pct_effect_confidence_99pct_gaussian_gate']:.2f}")
    c1 = r["closure_path_C1_halve_S2_S4"]
    print(f"  C1 (halve S2 + S4):")
    print(f"    SD reduction factor: {c1['systematic_only_SD_reduction_factor_vs_registered']:.2f}x")
    print(f"    Power at 0.10%: {c1['statistical_power_at_0p10pct_effect']:.2f}")
    print(f"    Power at 0.20%: {c1['statistical_power_at_0p20pct_effect']:.2f}")
    c2 = r["closure_path_C2_widen_gate_to_020_pct"]
    print(f"  C2 (widen gate to 0.20%):")
    print(f"    Empirical-gate power at 0.20%: {c2['statistical_power_at_0p20pct_effect_with_0p20pct_gate_empirical']:.2f}")
    print(f"    Null false-positive rate: {c2['false_positive_rate_at_0p20pct_gate_under_null_registered_budget']:.2f}")
    print(f"    Valid after FPR gate: {c2['target_met_at_0p20pct_effect_with_false_positive_gate']}")
    print(f"\n  Verdict: {r['verdict_status']}")
    print(f"  Closure path pass: {r['closure_path_pass_at_least_one_of_C1_C2']}")
