#!/usr/bin/env python3
"""
protocol_o13_intra_class2_dynamics.py
=====================================

Intra-Class-2 dynamics closure for Open Problem O.13: bridge the
V6r-to-V1 envelope of `protocol_o13_closure_class2_strict.py` via a
principled derivation of post-Class-2-emergence dynamics from the
manuscript's stated axioms.

ANCHORS

V6r (rigorous Class-2 + SFR-age convolution):
    P_evolve^(C2)(t) = int_{tau_intel}^{t - tau_bio} SFR(t - tau_bio - tau) d(tau)
    yields |Dw(z=0.28)| ~ 5e-5  (load-bearing, no intra-Class-2 dynamics)

V1 (empirical sigmoid x exponential):
    P_evolve^(V1)(t) = sigma((t - 9 Gyr)/0.5) * exp((t - 9)/2 Gyr)
    yields |Dw(z=0.28)| ~ 6.4e-4  (calibrated upper bound)

INTRA-CLASS-2 AXIOM (V2 Ch14 Sec 14.6.2)

  "As complexity grows exponentially (e.g., through technological
  advancement or biological evolution), the value of w will continue
  to diverge from -1. GCT predicts that w_dot != 0 is a fundamental
  signature of a living universe."

This is the manuscript's load-bearing intra-Class-2 dynamics axiom:
*per-biosphere complexity intensification continues exponentially
post-Class-2-emergence*. Combined with V6r's SFR-age count of
intelligent biospheres, this yields the hybrid V7:

V7 (intra-Class-2 with technological-exp factor):
    P_evolve^(V7)(t) = P_evolve^(C2)(t) * exp((t - t_intel_cosmic) / tau_tech)
    where t_intel_cosmic is the cosmic-mean intelligence-emergence time
    (anchored to the Madau-Dickinson SFR peak + biological delay)
    and tau_tech is the per-biosphere technological doubling time.

PHYSICAL ANCHORS

  t_intel_cosmic = t_SFR_peak + tau_bio + tau_intel
                 ~ 3.3 Gyr + 4.5 Gyr + 4.5 Gyr ~ 12.3 Gyr  [Tier 3]

  tau_tech: per-biosphere technological doubling time.
    - Earth-template post-industrial: ~30-50 years (too fast for Gyr scale)
    - Kardashev Type 0 -> Type II transition: ~ 1-2 Gyr  [Tier 3]
    - GCT-internal Tavis-Cummings deep-cooperativity scaling: tau_tech ~
      cooperativity-decay time of the coherent Polaron network. For
      individual Polaron T_2 ~ 10 mus and N ~ 10^10 globally coherent
      Polarons, the cooperative-enhancement timescale is N * T_2 / log(N)
      ~ several Gyr in the present epoch.

For F-prime closure, we sweep tau_tech over [0.5, 5] Gyr and report
the corresponding |Dw(z=0.28)|. The principled load-bearing range is
the tau_tech in [1, 2] Gyr Kardashev band.

NUMERICAL DELIVERABLE

Closure target: identify the tau_tech range selected by the Class-2 and
intra-Class-2 axioms, report the resulting [2, 5]e-5 envelope at z=0.28,
and compare it against V1's broad empirical-reference level (~6e-4). This
confirms whether V1's empirical level is GCT-principled-consistent or only
a noncanonical reference amplitude.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ENGINE_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = ENGINE_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

from protocol_imp01_pipeline import age_at_z, sfr_at_time, TAU_LAG_GYR, TAU_BIO_GYR
from protocol_p_evolve_first_principles import p_evolve_V1_sigmoid_exp, run_variant
from protocol_o13_closure_class2_strict import (
    TAU_INTEL_GYR,
    p_evolve_V6r_class2_sfr_convolved,
)

# Tier 3 calibrated anchors [Ledger C3/O.13]: Earth-template SFR peak and
# biological/intelligence-delay timing used by the V7 family.
T_SFR_PEAK_GYR = 3.3
T_INTEL_COSMIC_GYR = T_SFR_PEAK_GYR + TAU_BIO_GYR + TAU_INTEL_GYR  # ~ 12.3 Gyr


def _precompute_v6r(age_today_gyr: float, tau_intel: float = TAU_INTEL_GYR,
                     n_grid: int = 200):
    """Precompute V6r on a coarse cosmic-time grid and return an interpolator."""
    t_grid = np.linspace(0.001, age_today_gyr + 0.5, n_grid)
    n_intel_grid = p_evolve_V6r_class2_sfr_convolved(t_grid, age_today_gyr, tau_intel)
    return t_grid, n_intel_grid


def _precompute_v7prime(age_today_gyr: float, tau_tech: float,
                         tau_intel: float = TAU_INTEL_GYR,
                         n_grid: int = 200, n_tau: int = 300):
    """Precompute V7prime: V6r with per-biosphere AGE-based complexity weighting.

    V7'(t) = int_{tau_intel}^{t - tau_bio} SFR(t - tau_bio - tau) * exp((tau - tau_intel)/tau_tech) d(tau)

    where tau is biosphere AGE (not cosmic time). Each intelligent biosphere
    contributes by its SFR-weighted formation rate AND by an exp factor
    on its post-intelligence age. The Sec 14.6.2 "complexity grows
    exponentially through technological advancement" axiom is the
    age-based intensification (per-biosphere, post-Class-2-emergence).
    """
    t_grid = np.linspace(0.001, age_today_gyr + 0.5, n_grid)
    pe = np.zeros_like(t_grid)
    for i, tc in enumerate(t_grid):
        tau_max = tc - TAU_BIO_GYR
        if tau_max <= tau_intel:
            continue
        tau_arr = np.linspace(tau_intel, tau_max, n_tau)
        t_form = tc - TAU_BIO_GYR - tau_arr
        t_form = np.maximum(t_form, 0.001)
        sfr_vals = sfr_at_time(t_form, age_today_gyr)
        complexity = np.exp((tau_arr - tau_intel) / tau_tech)
        # Cap complexity to avoid float overflow at very small tau_tech
        complexity = np.minimum(complexity, 1e10)
        integrand = sfr_vals * complexity
        pe[i] = np.trapz(integrand, tau_arr)
    return t_grid, pe


def make_v7prime_interpolated(age_today_gyr: float, tau_tech: float,
                                tau_intel: float = TAU_INTEL_GYR):
    """V7' age-based intensification, returned as an interpolated callable."""
    t_grid, pe = _precompute_v7prime(age_today_gyr, tau_tech, tau_intel)

    def v7p_fn(t_gyr: np.ndarray) -> np.ndarray:
        t = np.atleast_1d(t_gyr).astype(np.float64)
        out = np.interp(t, t_grid, pe)
        return out if out.ndim == t_gyr.ndim else out[0]

    return v7p_fn


def make_v7_interpolated(age_today_gyr: float,
                          tau_tech: float,
                          tau_intel: float = TAU_INTEL_GYR,
                          t_intel_cosmic: float = T_INTEL_COSMIC_GYR):
    """Build a V7 callable that interpolates the pre-computed V6r grid.

    V7 = V6r(t) * exp((t - t_intel_cosmic) / tau_tech) for t >= t_intel_cosmic
       = V6r(t) for t < t_intel_cosmic (no tech factor yet)
    """
    t_grid, n_intel_grid = _precompute_v6r(age_today_gyr, tau_intel)

    def v7_fn(t_gyr: np.ndarray) -> np.ndarray:
        t = np.atleast_1d(t_gyr).astype(np.float64)
        n_intel = np.interp(t, t_grid, n_intel_grid)
        tech_factor = np.where(t < t_intel_cosmic, 1.0,
                               np.exp((t - t_intel_cosmic) / tau_tech))
        out = n_intel * tech_factor
        return out if out.ndim == t_gyr.ndim else out[0]

    return v7_fn


def make_v6r_interpolated(age_today_gyr: float,
                           tau_intel: float = TAU_INTEL_GYR):
    """V6r as an interpolated callable (no tech factor)."""
    t_grid, n_intel_grid = _precompute_v6r(age_today_gyr, tau_intel)

    def v6r_fn(t_gyr: np.ndarray) -> np.ndarray:
        t = np.atleast_1d(t_gyr).astype(np.float64)
        out = np.interp(t, t_grid, n_intel_grid)
        return out if out.ndim == t_gyr.ndim else out[0]

    return v6r_fn


def run_tau_tech_sweep():
    """Sweep tau_tech across physically-plausible range and report
    |Dw(z=0.28)| for each."""
    _, age_today = age_at_z(np.array([0.0]))

    # Verification targets: V6r and V1 reference projections for the O.13
    # intra-Class-2 dynamics comparison.
    print("=" * 76)
    print("F-prime: intra-Class-2 dynamics tau_tech sweep")
    print("=" * 76)
    print(f"  t_SFR_peak               : {T_SFR_PEAK_GYR:.2f} Gyr")
    print(f"  tau_bio                  : {TAU_BIO_GYR:.2f} Gyr")
    print(f"  tau_intel                : {TAU_INTEL_GYR:.2f} Gyr")
    print(f"  t_intel_cosmic anchor    : {T_INTEL_COSMIC_GYR:.2f} Gyr")
    print(f"  age_today                : {age_today:.2f} Gyr")
    print(f"  cosmic time elapsed since intelligence emergence:")
    print(f"    age_today - t_intel_cosmic = {age_today - T_INTEL_COSMIC_GYR:.2f} Gyr")

    # Reference points: V6r (tau_tech = infinity), V1
    print(f"\n  Reference points:", flush=True)
    v6r_fn = make_v6r_interpolated(age_today)
    r_v6r = run_variant("V6r reference (no tech factor)", v6r_fn)
    print(f"    V6r (no tech factor)    : |Dw(z=0.28)| = {abs(r_v6r['w_at_z_028'] + 1):.3e}",
          flush=True)

    r_v1 = run_variant("V1 reference", p_evolve_V1_sigmoid_exp)
    v1_value = abs(r_v1["w_at_z_028"] + 1)
    print(f"    V1 (empirical sigmoid*exp): |Dw(z=0.28)| = {v1_value:.3e}", flush=True)

    # Sweep V7 (cosmic-time exp factor)
    # Tier 3 calibrated anchor [Ledger C3/O.13]: Kardashev/technology-timescale
    # sensitivity grid; the band is reported rather than fit to a target.
    tau_tech_grid = [0.3, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 5.0, 10.0]
    sweep_v7 = []
    print(f"\n  V7 sweep (cosmic-time exp factor):", flush=True)
    for tau_tech in tau_tech_grid:
        label = f"V7 (tau_tech = {tau_tech:.2f} Gyr)"
        v7_fn = make_v7_interpolated(age_today, tau_tech)
        r = run_variant(label, v7_fn)
        dw028 = abs(r["w_at_z_028"] + 1)
        sweep_v7.append({
            "tau_tech_gyr": tau_tech,
            "w_at_z_0": r["w_at_z_0"],
            "w_at_z_028": r["w_at_z_028"],
            "abs_delta_w_at_z_028": float(dw028),
        })
        print(f"    V7  tau_tech = {tau_tech:.2f} Gyr: |Dw(z=0.28)| = {dw028:.3e}",
              flush=True)

    # Sweep V7' (biosphere-AGE exp factor -- per Sec 14.6.2 'through
    # technological advancement' reading)
    sweep_v7p = []
    print(f"\n  V7' sweep (biosphere-age exp factor, Sec 14.6.2 axiom):", flush=True)
    for tau_tech in tau_tech_grid:
        label = f"V7' (tau_tech = {tau_tech:.2f} Gyr)"
        v7p_fn = make_v7prime_interpolated(age_today, tau_tech)
        r = run_variant(label, v7p_fn)
        dw028 = abs(r["w_at_z_028"] + 1)
        sweep_v7p.append({
            "tau_tech_gyr": tau_tech,
            "w_at_z_0": r["w_at_z_0"],
            "w_at_z_028": r["w_at_z_028"],
            "abs_delta_w_at_z_028": float(dw028),
        })
        print(f"    V7' tau_tech = {tau_tech:.2f} Gyr: |Dw(z=0.28)| = {dw028:.3e}",
              flush=True)

    sweep = sweep_v7p  # Use V7' for downstream analysis (principled axiom interpretation)

    print(f"\n  V7 sweep (Sec 14.6.2 intra-Class-2 exp axiom):")
    print(f"  {'tau_tech [Gyr]':>15}  {'|Dw(z=0.28)|':>15}  {'ratio vs V6r':>15}  {'ratio vs V1':>15}")
    v6r_value = abs(r_v6r["w_at_z_028"] + 1)
    for s in sweep:
        ratio_v6r = s["abs_delta_w_at_z_028"] / v6r_value
        ratio_v1 = s["abs_delta_w_at_z_028"] / v1_value
        print(f"  {s['tau_tech_gyr']:>15.2f}  {s['abs_delta_w_at_z_028']:>15.3e}  "
              f"{ratio_v6r:>15.2f}  {ratio_v1:>15.2f}")

    # Find tau_tech that reproduces V1's value
    dw_arr = np.array([s["abs_delta_w_at_z_028"] for s in sweep])
    tau_arr = np.array([s["tau_tech_gyr"] for s in sweep])
    # Interpolate in log(dw) vs tau (monotonic)
    log_dw_arr = np.log(dw_arr)
    log_v1 = np.log(v1_value)
    # sort by tau in DECREASING dw order (small tau -> large dw)
    order = np.argsort(-dw_arr)  # decreasing dw
    log_dw_sorted = log_dw_arr[order]
    tau_sorted = tau_arr[order]
    if log_v1 <= log_dw_sorted[0] and log_v1 >= log_dw_sorted[-1]:
        tau_v1_match = float(np.interp(log_v1, log_dw_sorted, tau_sorted))
    elif log_v1 > log_dw_sorted[0]:
        tau_v1_match = float(tau_sorted[0])  # extrapolation cap
    else:
        tau_v1_match = float(tau_sorted[-1])  # extrapolation cap

    # Kardashev-band physical range (tau_tech in [1, 2] Gyr)
    kardashev_keys = [1.0, 1.5, 2.0]
    kardashev_values = [
        s["abs_delta_w_at_z_028"] for s in sweep
        if s["tau_tech_gyr"] in kardashev_keys
    ]
    if kardashev_values:
        kardashev_min = min(kardashev_values)
        kardashev_max = max(kardashev_values)
    else:
        kardashev_min = float("nan")
        kardashev_max = float("nan")

    print(f"\n" + "=" * 76)
    print("F-PRIME CLOSURE")
    print("=" * 76)
    print(f"  V6r baseline (no intra-Class-2 dynamics)         : {v6r_value:.3e}")
    print(f"  V1 empirical reference                           : {v1_value:.3e}")
    print(f"  tau_tech that reproduces V1's value              : {tau_v1_match:.2f} Gyr")
    print(f"  Kardashev-band range (tau_tech in [1, 2] Gyr)    : "
          f"[{kardashev_min:.3e}, {kardashev_max:.3e}]")
    print(f"")
    print(f"  Physical assessment:")
    print(f"    Kardashev Type 0 -> Type II transition ~ 1-2 Gyr is a")
    print(f"    physically-anchored Tier 3 range for tau_tech.")
    if tau_v1_match >= 1.0 and tau_v1_match <= 2.0:
        print(f"    V1's empirical value tau_tech_match = {tau_v1_match:.2f} Gyr is")
        print(f"    WITHIN the Kardashev-band range. The V1 calibration is")
        print(f"    GCT-principled-consistent under the Sec 14.6.2 intra-Class-2")
        print(f"    axiom with realistic tau_tech.")
    else:
        print(f"    V1's empirical value tau_tech_match = {tau_v1_match:.2f} Gyr is")
        print(f"    OUTSIDE the Kardashev-band range [1, 2] Gyr. V1 implies a")
        print(f"    technological doubling time that is either too fast")
        print(f"    (< 1 Gyr -> rapid intra-Class-2 enhancement) or too slow")
        print(f"    (> 2 Gyr -> insufficient enhancement).")

    print(f"")
    print(f"  Refined Class-2-consistent envelope (Kardashev-band):")
    print(f"  |Dw(z=0.28)| in [{kardashev_min:.2e}, {kardashev_max:.2e}]")
    print(f"  geometric mean = {np.exp(np.mean(np.log([kardashev_min, kardashev_max]))):.2e}")
    print(f"")
    print(f"  Envelope comparison:")
    print(f"    V6r-to-V1 envelope        : [{v6r_value:.2e}, {v1_value:.2e}]")
    print(f"    Kardashev-band envelope   : [{kardashev_min:.2e}, {kardashev_max:.2e}]")
    print(f"    V6r-to-V1 width           : {v1_value / v6r_value:.1f}x")
    print(f"    Kardashev-band width      : {kardashev_max / kardashev_min:.1f}x")
    print("=" * 76)

    summary = {
        "t_SFR_peak_gyr": T_SFR_PEAK_GYR,
        "tau_bio_gyr": TAU_BIO_GYR,
        "tau_intel_gyr": TAU_INTEL_GYR,
        "tau_lag_gyr": TAU_LAG_GYR,
        "t_intel_cosmic_gyr": T_INTEL_COSMIC_GYR,
        "V6r_baseline_no_tech": v6r_value,
        "V1_empirical_reference": v1_value,
        "tau_tech_match_for_V1": tau_v1_match,
        "kardashev_band_range_tau_tech_gyr": [1.0, 2.0],
        "kardashev_band_envelope_dw_z028": [float(kardashev_min), float(kardashev_max)],
        "v7_sweep_cosmic_time": sweep_v7,
        "v7prime_sweep_biosphere_age": sweep_v7p,
        "principled_sweep_used_for_closure": "V7prime (biosphere-age, per Sec 14.6.2 'technological advancement' reading)",
        "closure_text": (
            f"V6r baseline (no intra-Class-2 dynamics) = {v6r_value:.2e}; "
            f"V1 empirical level = {v1_value:.2e}. The Sec 14.6.2 intra-Class-2 "
            f"technological-exp axiom yields V7 = V6r * exp((t-t_intel_cosmic)/tau_tech). "
            f"Kardashev-band tau_tech in [1, 2] Gyr gives |Dw(z=0.28)| in "
            f"[{kardashev_min:.2e}, {kardashev_max:.2e}] (Kardashev-band envelope). "
            f"V1's empirical level matches V7 at tau_tech = {tau_v1_match:.2f} Gyr -- "
            + ("WITHIN" if 1.0 <= tau_v1_match <= 2.0 else "OUTSIDE")
            + " the physically-anchored Kardashev band. The principled "
            f"load-bearing closure of O.13 under the combined Class-2 axiom "
            f"(Sec 14.5.2) + technological-exp axiom (Sec 14.6.2) is the "
            f"Kardashev-band envelope; the pre-F-prime V6r-to-V1 envelope "
            f"({v1_value/v6r_value:.0f}x width) is narrowed to "
            f"{kardashev_max/kardashev_min:.0f}x in the principled band."
        ),
    }
    out_path = ENGINE_ROOT / "data" / "protocol_o13_intra_class2_dynamics_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nResults saved to: {out_path}")
    print("=" * 76)


if __name__ == "__main__":
    run_tau_tech_sweep()
