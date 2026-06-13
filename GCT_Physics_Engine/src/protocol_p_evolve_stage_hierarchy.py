#!/usr/bin/env python3
"""
protocol_p_evolve_stage_hierarchy.py - Astrobiology-anchored stage-hierarchy
derivation of P_evolve(t) for the biogenic dark-energy pipeline.

Background: the broad reference |Delta w(z=0.28)| ~ 6e-4 (see
protocol_p_evolve_first_principles.py) is sensitive to the P_evolve functional
form (cross-variant spread 2.7e-3 across 5 candidates). The operative
Class-2 envelope is [2,5]e-5 at z=0.28 pending O.13 closure.
This protocol drills into the most physically-motivated candidate (the
stage-hierarchy model) with astrobiology-anchored parameters and an explicit
cosmological-time convolution treating each biosphere's emergence as an
independent event with a per-biosphere complexity trajectory C(tau).

Astrobiology stage anchors (Earth template):
  Stage 0: pre-life delay        ~ 0.5 Gyr post-formation (LUCA ~3.8-4.0 Gya;
                                   Earth formed ~4.54 Gya -> tau_0 ~ 0.5-0.7 Gyr)
  Stage 1: bacterial             ~ 0.5-2.4 Gyr post-formation
  Stage 2: eukaryotic            ~ 2.4-3.7 Gyr (eukaryotes ~2.1 Gya = ~2.4 Gyr post)
  Stage 3: multicellular         ~ 3.7-4.5 Gyr (Cambrian ~600 Mya = ~3.9 Gyr post)
  Stage 4: intelligent           ~ 4.5+  Gyr (humans ~300 Kya = ~4.5 Gyr post)

Relative information densities (rough order-of-magnitude per-stage):
  w_0 (no life)                  = 0
  w_1 (bacterial baseline)       = 1
  w_2 (eukaryotic)               ~ 100   (cellular complexity ~2 orders)
  w_3 (multicellular w/ brains)  ~ 10^5  (body-plan + neural complexity)
  w_4 (intelligent / symbolic)   ~ 10^8  (symbolic / technological)

These are Tier 4 (order-of-magnitude) per-stage; the ratios are robust to
factor-of-10 changes (the biogenic DE CPL output is logarithmically sensitive).

Two computations:

  (A) Direct cosmic-time evaluation. Approximate P_evolve(t') = C(t' - t_anchor)
      where t_anchor is the cosmic-time of typical biosphere formation
      (SFR peak at z = 2, cosmic time ~3.3 Gyr). Compares stage-hierarchy
      step function vs the V1 sigmoid x exp ansatz.

  (B) Full convolution. The "true" cosmological P_evolve(t') is the
      SFR-weighted average per-biosphere complexity at cosmic time t':
          P_evolve(t') = integral SFR(t_form) * C(t' - t_form) dt_form
                          / integral SFR(t_form) dt_form
      This gives a SMOOTH function rather than discrete steps, anchored
      to actual SFR + Earth stage hierarchy. Compares smooth-convolved
      P_evolve to V1 ansatz.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit

ENGINE_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = ENGINE_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

from protocol_imp01_pipeline import (
    age_at_z, sfr_at_time, ALPHA, TAU_LAG_GYR, TAU_BIO_GYR,
    W0_TARGET, DELTA_W_TARGET, cpl,
)


# Astrobiology stage anchors (Earth template; in Gyr post-formation)
STAGE_TIMES_GYR = (0.5, 2.4, 3.7, 4.5)
STAGE_WEIGHTS_LOG10 = (0.0, 2.0, 5.0, 8.0)  # log10 of relative info density
STAGE_WEIGHTS = tuple(10.0 ** w for w in STAGE_WEIGHTS_LOG10)


def per_biosphere_C(tau_gyr: np.ndarray) -> np.ndarray:
    """Per-biosphere complexity trajectory C(tau) using Earth-template stage
    anchors. tau is biosphere age post-formation."""
    tau = np.atleast_1d(tau_gyr).astype(np.float64)
    pe = np.zeros_like(tau)
    for i, t in enumerate(tau):
        if t < STAGE_TIMES_GYR[0]:
            pe[i] = 0.0   # pre-life
        elif t < STAGE_TIMES_GYR[1]:
            pe[i] = STAGE_WEIGHTS[0]   # bacterial
        elif t < STAGE_TIMES_GYR[2]:
            pe[i] = STAGE_WEIGHTS[1]   # eukaryotic
        elif t < STAGE_TIMES_GYR[3]:
            pe[i] = STAGE_WEIGHTS[2]   # multicellular
        else:
            pe[i] = STAGE_WEIGHTS[3]   # intelligent
    return pe if pe.ndim == tau_gyr.ndim else pe[0]


def p_evolve_A_step(t_prime_gyr: np.ndarray,
                      t_anchor_gyr: float = 3.3) -> np.ndarray:
    """(A) Direct cosmic-time evaluation. P_evolve(t') = C(t' - t_anchor)
    where t_anchor is the cosmic-time anchor for the typical biosphere
    formation (SFR peak at z = 2, ~3.3 Gyr cosmic time).
    """
    return per_biosphere_C(t_prime_gyr - t_anchor_gyr)


def precompute_p_evolve_B(age_today_gyr: float, n_grid: int = 80,
                            n_int: int = 100) -> tuple[np.ndarray, np.ndarray]:
    """Precompute the convolved P_evolve_B on a coarse cosmic-time grid.
    Returns (t_grid, pe_grid). Use np.interp for downstream lookups instead
    of re-integrating per call.
    """
    t_grid = np.linspace(0.0, age_today_gyr + 0.1, n_grid)
    pe_grid = np.zeros_like(t_grid)
    for i, t_prime in enumerate(t_grid):
        if t_prime <= 0:
            pe_grid[i] = 0.0
            continue
        t_form_grid = np.linspace(0.001, t_prime, n_int)
        sfr_vals = sfr_at_time(t_form_grid, age_today_gyr)
        c_vals = per_biosphere_C(t_prime - t_form_grid)
        numer = np.trapz(sfr_vals * c_vals, t_form_grid)  # noqa: NPY201
        denom = np.trapz(sfr_vals, t_form_grid)            # noqa: NPY201
        pe_grid[i] = numer / denom if denom > 0 else 0.0
    return t_grid, pe_grid


def make_p_evolve_B_interpolated(t_grid: np.ndarray, pe_grid: np.ndarray):
    """Return a callable that interpolates the precomputed P_evolve_B."""
    def pe_fn(t_query):
        return np.interp(np.atleast_1d(t_query), t_grid, pe_grid)
    return pe_fn


# ---------------------------------------------------------------------------
# Pipeline (same machinery as protocol_p_evolve_first_principles)
# ---------------------------------------------------------------------------

def i_dot_for_pe(t_gyr: np.ndarray, age_today_gyr: float, p_evolve_fn) -> np.ndarray:
    if np.isscalar(t_gyr):
        t_gyr = np.array([t_gyr])
    result = np.zeros_like(t_gyr, dtype=float)
    for i, t in enumerate(t_gyr):
        if t <= 0:
            result[i] = 0.0
            continue
        t_prime_grid = np.linspace(0.0, t, 800)
        t_eff = np.maximum(t_prime_grid - TAU_BIO_GYR, 0.001)
        sfr = sfr_at_time(t_eff, age_today_gyr)
        pe = p_evolve_fn(t_prime_grid)
        integrand = sfr * pe
        result[i] = np.trapz(integrand, t_prime_grid)   # noqa: NPY201
    return result


def p_info_for_pe(t_gyr: np.ndarray, age_today_gyr: float, p_evolve_fn) -> np.ndarray:
    if np.isscalar(t_gyr):
        t_gyr = np.array([t_gyr])
    result = np.zeros_like(t_gyr, dtype=float)
    t_int_grid = np.linspace(0.01, age_today_gyr + 0.1, 150)
    i_dot_grid = i_dot_for_pe(t_int_grid, age_today_gyr, p_evolve_fn)
    for i, t in enumerate(t_gyr):
        if t <= 0:
            result[i] = 0.0
            continue
        t_prime_grid = np.linspace(0.01, t, 400)
        i_dot_t_prime = np.interp(t_prime_grid, t_int_grid, i_dot_grid)
        kernel = np.exp(-(t - t_prime_grid) / TAU_LAG_GYR)
        integrand = i_dot_t_prime * kernel
        result[i] = ALPHA * np.trapz(integrand, t_prime_grid)   # noqa: NPY201
    return result


def w_of_z_for_pe(z_array: np.ndarray, age_today_gyr: float, p_evolve_fn) -> np.ndarray:
    t_array, _ = age_at_z(z_array)
    p_info_array = p_info_for_pe(t_array, age_today_gyr, p_evolve_fn)
    p_info_today = p_info_for_pe(np.array([age_today_gyr]), age_today_gyr, p_evolve_fn)[0]
    if p_info_today == 0:
        return -np.ones_like(z_array)
    return -1.0 + DELTA_W_TARGET * (p_info_array / p_info_today)


def fit_cpl(z_grid: np.ndarray, w_grid: np.ndarray) -> tuple[float, float, float]:
    a_grid = 1.0 / (1.0 + z_grid)
    popt, _ = curve_fit(cpl, a_grid, w_grid, p0=[-1.0, 0.0])
    w0_fit, wa_fit = popt
    if abs(wa_fit) < 1e-12:
        return w0_fit, wa_fit, float("nan")
    a_cross = 1.0 + (1.0 + w0_fit) / wa_fit
    z_cross_fit = 1.0 / a_cross - 1.0 if a_cross > 0 else float("nan")
    return w0_fit, wa_fit, z_cross_fit


def run_one_pe(label: str, pe_fn) -> dict:
    _, age_today = age_at_z(np.array([0.0]))
    z_grid = np.linspace(0.001, 1.5, 50)
    w_grid = w_of_z_for_pe(z_grid, age_today, pe_fn)
    z_lo = np.linspace(0.001, 0.5, 25)
    w_lo = w_of_z_for_pe(z_lo, age_today, pe_fn)
    w0, wa, z_cross = fit_cpl(z_lo, w_lo)
    return {
        "label": label,
        "w_at_z_0": float(w_grid[0]),
        "w_at_z_015": float(np.interp(0.15, z_grid, w_grid)),
        "w_at_z_028": float(np.interp(0.28, z_grid, w_grid)),
        "w_at_z_05": float(np.interp(0.5, z_grid, w_grid)),
        "w_at_z_10": float(np.interp(1.0, z_grid, w_grid)),
        "w0_CPL_fit": float(w0),
        "wa_CPL_fit": float(wa),
        "z_cross_CPL_fit": float(z_cross),
    }


def main():
    print("=" * 76)
    print("O.13 deep-dive: astrobiology-anchored stage-hierarchy P_evolve")
    print("=" * 76)

    print(f"\nAstrobiology anchors (Earth template):")
    print(f"  Stage emergence times (post-formation): {STAGE_TIMES_GYR} Gyr")
    print(f"  Per-stage info-density weights (log10): {STAGE_WEIGHTS_LOG10}")
    print(f"    -> weights: {STAGE_WEIGHTS}")
    print(f"  SFR-peak cosmic-time anchor (z=2 ~ 3.3 Gyr post-BB)")

    print("\n--- Compute per-biosphere complexity trajectory C(tau) ---")
    tau_grid = np.linspace(0.0, 8.0, 17)
    c_vals = per_biosphere_C(tau_grid)
    for t, c in zip(tau_grid, c_vals):
        print(f"  tau = {t:.1f} Gyr  ->  C(tau) = {c:.3e}")

    _, age_today = age_at_z(np.array([0.0]))
    print(f"\nAge of universe today: {age_today:.3f} Gyr")

    print("\n--- (A) Direct step P_evolve(t') = C(t' - 3.3) ---")
    t_prime_grid = np.linspace(0.0, age_today, 50)
    pe_A_vals = p_evolve_A_step(t_prime_grid, t_anchor_gyr=3.3)
    for k in range(0, len(t_prime_grid), 5):
        print(f"  t' = {t_prime_grid[k]:.2f} Gyr  ->  P_evolve_A = {pe_A_vals[k]:.3e}")

    print("\n--- (B) Convolved P_evolve(t') = <C(t' - t_form)>_SFR (precomputed) ---")
    t_pe_grid, pe_B_grid = precompute_p_evolve_B(age_today)
    pe_B_fn = make_p_evolve_B_interpolated(t_pe_grid, pe_B_grid)
    pe_B_vals = pe_B_fn(t_prime_grid)
    for k in range(0, len(t_prime_grid), 5):
        print(f"  t' = {t_prime_grid[k]:.2f} Gyr  ->  P_evolve_B = {pe_B_vals[k]:.3e}")

    # Run pipeline for both
    print("\n--- Pipeline runs ---")
    r_A = run_one_pe("V2A astrobiology step (t_anchor=3.3 Gyr)",
                       lambda t: p_evolve_A_step(t, t_anchor_gyr=3.3))
    r_B = run_one_pe("V2B astrobiology convolved", pe_B_fn)

    # Comparison to V1 ansatz
    from protocol_p_evolve_first_principles import p_evolve_V1_sigmoid_exp
    r_V1 = run_one_pe("V1 sigmoid x exp (current ansatz)",
                        p_evolve_V1_sigmoid_exp)

    print("\n" + "=" * 76)
    print("PIPELINE OUTPUT COMPARISON")
    print("=" * 76)
    print(f"  {'variant':<45}  {'w(z=0)':>9}  {'w(z=.28)':>9}  {'w_a CPL':>9}  {'z_cross':>9}")
    for r in [r_V1, r_A, r_B]:
        print(f"  {r['label']:<45}  {r['w_at_z_0']:>+9.5f}  {r['w_at_z_028']:>+9.5f}  "
              f"{r['wa_CPL_fit']:>+9.5f}  {r['z_cross_CPL_fit']:>+9.4f}")

    # Sensitivity assessment
    w028_arr = np.array([r["w_at_z_028"] for r in [r_V1, r_A, r_B]])
    spread_w028 = abs(w028_arr.max() - w028_arr.min())
    print(f"\n  Spread of w(z=0.28) across {{V1, V2A, V2B}}: {spread_w028:.5f}; operative Class-2 envelope target is [2,5] x 10^-5")
    print("  Roman Year-10 / Stage-V target precision: <5 x 10^-5")
    print(f"  Joint-bin Roman+DESI threshold: ~3-5 x 10^-4")

    print("\n" + "=" * 76)
    print("INTERPRETATION")
    print("=" * 76)
    if spread_w028 < 5e-4:
        verdict = "ASTROBIOLOGY_ROBUST"
        verdict_text = (
            f"The astrobiology-anchored variants (V2A, V2B) agree with the V1 ansatz "
            f"on w(z=0.28) to within {spread_w028:.1e}, below the joint-bin "
            f"observational threshold. The current ansatz V1 sigmoid x exp is "
            f"effectively a smooth approximation to the astrobiology-derived "
            f"stage-hierarchy convolution. The biogenic-DE prediction remains Tier 3, "
            f"with the independent astrobiological derivation as a consistency check; "
            f"its closure target is O.13."
        )
    elif spread_w028 < 5e-3:
        verdict = "PARTIAL_AGREEMENT"
        verdict_text = (
            f"Astrobiology-anchored P_evolve gives w(z=0.28) differing from the V1 "
            f"ansatz by {spread_w028:.1e}, above the Roman Year-10 / Stage-V "
            f"sub-5e-5 target. The V1 ansatz is only a broad reference; the "
            f"operative Class-2 envelope is [2,5]e-5 at z=0.28. Closure of O.13 "
            f"should select between V1, V2A, V2B based on additional physical "
            f"arguments (saturation bound, peak alignment with SFR + complexity "
            f"hierarchy)."
        )
    else:
        verdict = "DISAGREEMENT"
        verdict_text = (
            f"Astrobiology-anchored P_evolve gives w(z=0.28) differing from the V1 "
            f"ansatz by {spread_w028:.1e}, exceeding the Roman Year-10 / Stage-V "
            f"target precision. The current V1 ansatz is NOT a good approximation "
            f"to the astrobiology-derived expectation. The manuscript's operative "
            f"biogenic DE prediction is the Class-2 envelope; the Tier 3 label "
            f"remains until O.13 selects the canonical P_evolve variant."
        )

    print(f"  Sensitivity verdict: {verdict}")
    print(f"  {verdict_text}")
    print("=" * 76)

    summary = {
        "astrobiology_anchors": {
            "stage_times_gyr": list(STAGE_TIMES_GYR),
            "stage_weights_log10": list(STAGE_WEIGHTS_LOG10),
            "stage_weights": list(STAGE_WEIGHTS),
            "t_anchor_cosmic_gyr": 3.3,
            "anchor_rationale": "SFR peak at z=2 corresponds to cosmic time ~3.3 Gyr post-Big-Bang.",
        },
        "pipeline_runs": {
            "V1_current_ansatz": r_V1,
            "V2A_astrobiology_step": r_A,
            "V2B_astrobiology_convolved": r_B,
        },
        "spread_w028_across_V1_V2A_V2B": float(spread_w028),
        "sensitivity_verdict": verdict,
        "verdict_text": verdict_text,
    }
    out_path = ENGINE_ROOT / "data" / "protocol_p_evolve_stage_hierarchy_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nFull results saved to: {out_path}")
    print("=" * 76)


if __name__ == "__main__":
    main()
