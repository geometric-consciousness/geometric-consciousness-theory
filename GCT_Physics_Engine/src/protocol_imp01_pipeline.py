#!/usr/bin/env python3
"""
protocol_imp01_pipeline.py
===========================

Implements the biogenic dark energy w(z) prediction pipeline from
Ch14 Sec 14.5 of the GCT manuscript. Produces an internally-consistent
(z_cross, w_0, w_a) CPL parameterization, addressing Open Problem O.13.

Pipeline (manuscript Sec 14.5.1 + Sec 14.5.2):
    1. Madau-Dickinson 2014 cosmic SFR psi(z)               [standard]
    2. Time-integrated complexity:
            I_dot(t) ~ integral_0^t SFR(t' - tau_bio) * P_evolve(t') dt'
        with tau_bio ~ 4-5 Gyr (Tier 3 biological delay)
    3. Lag-kernel integration (Sec 14.5.1):
            P_info(t) = lambda_bio * integral_0^t I_dot(t') K(t-t') dt'
        with K(tau) = exp(-tau/tau_lag), tau_lag = 5 Gyr, lambda_bio = alpha
    4. Map to w(z):
            w(z) = -1 - delta_w * P_info(z) / P_info(0)
        where delta_w calibrated to give the registered w(0) amplitude -1.005 (per Sec 14.5.1)
    5. Fit CPL form w(a) = w_0 + w_a (1-a) to the resulting curve
        over z in [0, 1]; report the CPL linear-extrapolation z_cross
        diagnostic while the underlying w(z) has no physical crossing.

Manuscript-specified pieces (used as-is):
    - Madau-Dickinson SFR (Madau & Dickinson 2014 ARA&A)
    - tau_lag = 5 Gyr (Parameter Ledger, Tier 3)
    - tau_bio = 4-5 Gyr (Sec 14.5.2, Tier 3) -- using 4.5 Gyr midpoint
    - lambda_bio = alpha (Parameter Ledger / Sec 14.3.1, Tier 3 fit)
    - w_0 ~ -1.005 target from the registered full-integration amplitude (Sec 14.5.1)
    - K(tau) = exp(-tau/tau_lag) exponential lag-kernel (Sec 14.5.1)
    - Lagrangian Sec 14.3 kinetic-modification -> w deviation proportional to
        (I_dot / I_0)

Manuscript-UNSPECIFIED pieces (chosen with explicit justification):
    - P_evolve(t'): "exponential technological complexity multiplier" per
        Sec 14.6.2; specific form chosen as a logistic turn-on around the
        Cambrian-like emergence of complex life followed by exponential
        growth (parameters: t_origin = 9 Gyr post-Big-Bang, tau_evolve = 2 Gyr).
        This is the simplest form consistent with "biological complexity
        requires billions of years of stable evolution" (Sec 14.5.2) and
        "complexity grows exponentially" (Sec 14.6.2). SENSITIVITY: see
        SENSITIVITY_ANALYSIS below.
    - Cosmology: flat LambdaCDM with Omega_m = 0.315, Omega_L = 0.685, H_0 = 67.4
        km/s/Mpc (Planck 2018 CODATA-cited values consistent with Sec 14.4.3).

SENSITIVITY: the CPL output (w_0, w_a) and the linear-extrapolation
crossing z_cross^CPL depend on the chosen P_evolve parameters. The
pipeline reports the result and characterizes the sensitivity to
(t_origin, tau_evolve). The underlying w(z) curve produced by the
lag-kernel integration asymptotes to -1 from below WITHOUT physically
crossing the phantom divide (direct-brentq integration returns NaN).
The CPL linear-extrapolation crossing reported by the curve_fit is a
fit-artifact, not a physical crossing. The z ~ 0.28 figure is the
low-redshift sensitivity marker; the operative Class-2 envelope at that
marker is |Delta w| in [2, 5]e-5, below Roman Year-5 / DESI joint-bin
precision and requiring Roman Year-10 / Stage-V sub-5e-5 precision for
a clean cosmic-mean test.

This protocol implements Open Problem O.13 fingerprint (i) — the
biogenic channel's asymptote-from-below shape — and exposes the
(w_0, w_a, z_cross_CPL_fit) triple as the diagnostic projection,
not as a literal phantom-crossing prediction. See App H O.13 and
V2 Ch14 Sec 14.6.3 for the fingerprint-set framing.
"""

import sys
import json
import math
import numpy as np
from pathlib import Path
from scipy.integrate import cumulative_trapezoid
from scipy.optimize import curve_fit, brentq

try:
    from gct_utils import get_output_path, C
    OUTPUT_DIR_AVAILABLE = True
except ImportError:
    OUTPUT_DIR_AVAILABLE = False
    C = None


def _json_safe(value):
    """Convert numpy scalars and NaN/Inf floats to strict-JSON values."""
    if isinstance(value, dict):
        return {k: _json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_json_safe(v) for v in value]
    if isinstance(value, tuple):
        return [_json_safe(v) for v in value]
    if isinstance(value, np.generic):
        value = value.item()
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


# External empirical prior: Planck/LambdaCDM baseline values used by the
# time-redshift conversion; not GCT parameter anchors.
H0_KM_S_MPC = 67.4
OMEGA_M = 0.315
OMEGA_L = 0.685
# Tier 3 calibrated anchor [Ledger C1]: lambda_bio sourced from the YAML SSOT.
# The pipeline normalizes by P_info(today), so this factor cancels from w(z).
PHI_FALLBACK = (1.0 + math.sqrt(5.0)) / 2.0
ALPHA = (
    float(C.LAMBDA_BIO)
    if C is not None and hasattr(C, "LAMBDA_BIO")
    else 1.0 / (360.0 * PHI_FALLBACK ** (-2))
)
# Tier 3 calibrated anchors [Ledger C2/C3]: biogenic lag and biological delay.
TAU_LAG_GYR = 5.0
TAU_BIO_GYR = 4.5
# Tier 3 calibrated anchor [Ledger C-sector]: registered single-channel CPL amplitude target.
W0_TARGET = -1.005
DELTA_W_TARGET = W0_TARGET - (-1.0)

# External empirical prior: unit conversions for cosmological time integration.
MPC_TO_KM = 3.0857e19
SEC_PER_GYR = 3.1557e16
HUBBLE_TIME_GYR = (MPC_TO_KM / H0_KM_S_MPC) / SEC_PER_GYR


def hubble_z(z):
    """H(z)/H_0 for flat LambdaCDM."""
    return np.sqrt(OMEGA_M * (1.0 + z) ** 3 + OMEGA_L)


def age_at_z(z_array, z_max=1000.0, n_int=20000):
    """Cosmic time t (in Gyr) at redshift z, measured from Big Bang."""
    z_grid = np.linspace(0.0, z_max, n_int)
    integrand = 1.0 / ((1.0 + z_grid) * hubble_z(z_grid))
    elapsed_from_now = cumulative_trapezoid(integrand, z_grid, initial=0.0) * HUBBLE_TIME_GYR
    age_total = HUBBLE_TIME_GYR * np.trapz(integrand, z_grid)  # noqa: NPY201
    age_at_z_grid = age_total - elapsed_from_now
    return np.interp(z_array, z_grid, age_at_z_grid), age_total


def z_at_age(t_array_gyr, age_today_gyr, z_grid_max=1000.0, n_int=20000):
    """Inverse of age_at_z: given cosmic age t, find z."""
    z_grid = np.linspace(0.0, z_grid_max, n_int)
    ages_grid, _ = age_at_z(z_grid)
    return np.interp(t_array_gyr, ages_grid[::-1], z_grid[::-1])


def sfr_madau_dickinson(z):
    """psi(z) per Madau & Dickinson 2014 ARA&A eq. 15."""
    # External empirical prior: Madau-Dickinson SFR shape. The absolute
    # normalization cancels after P_info(today) normalization.
    return 0.015 * (1.0 + z) ** 2.7 / (1.0 + ((1.0 + z) / 2.9) ** 5.6)


def sfr_at_time(t_array_gyr, age_today_gyr):
    """SFR as a function of cosmic time."""
    z = z_at_age(t_array_gyr, age_today_gyr)
    return sfr_madau_dickinson(z)


def p_evolve(t_gyr, t_origin=9.0, tau_evolve=2.0):
    """Logistic turn-on of complexity followed by exponential growth.

    Tier 3 calibrated anchor [Ledger C-sector]: default t_origin = 9 Gyr
    (~Cambrian-like; complex multicellular life
    emerges ~4.6 Gyr after Big Bang on Earth, but cosmologically distributed
    biospheres begin contributing ~9 Gyr in to allow integration through to
    the present epoch ~13.8 Gyr).

    Physical anchor: Sec 14.5.2 -- "biological complexity requires billions
    of years of stable evolution after star formation"; SFR peak at z=2
    corresponds to t ~ 3.3 Gyr; biological complexity at scale follows
    by >= 4-5 Gyr (the tau_bio shift). So P_evolve turn-on ~9 Gyr is
    consistent with SFR_peak (3.3) + tau_bio (4.5) + ~1 Gyr ramp.
    """
    sigmoid = 1.0 / (1.0 + np.exp(-(t_gyr - t_origin) / 0.5))
    growth = np.exp((t_gyr - t_origin) / tau_evolve)
    return sigmoid * growth


def i_dot(t_gyr, age_today_gyr, t_origin=9.0, tau_evolve=2.0):
    """I_dot(t) ~ integral_0^t SFR(t' - tau_bio) * P_evolve(t') dt'."""
    if np.isscalar(t_gyr):
        t_gyr = np.array([t_gyr])
    result = np.zeros_like(t_gyr, dtype=float)
    for i, t in enumerate(t_gyr):
        if t <= 0:
            result[i] = 0.0
            continue
        t_prime_grid = np.linspace(0.0, t, 1000)
        t_eff = np.maximum(t_prime_grid - TAU_BIO_GYR, 0.001)
        sfr = sfr_at_time(t_eff, age_today_gyr)
        pe = p_evolve(t_prime_grid, t_origin, tau_evolve)
        integrand = sfr * pe
        result[i] = np.trapz(integrand, t_prime_grid)  # noqa: NPY201
    return result


def p_info(t_gyr, age_today_gyr, t_origin=9.0, tau_evolve=2.0):
    """P_info(t) = lambda_bio * integral_0^t I_dot(t') K(t-t') dt'.

    K(tau) = exp(-tau/tau_lag)
    """
    if np.isscalar(t_gyr):
        t_gyr = np.array([t_gyr])
    result = np.zeros_like(t_gyr, dtype=float)
    t_int_grid = np.linspace(0.01, age_today_gyr + 0.1, 200)
    i_dot_grid = i_dot(t_int_grid, age_today_gyr, t_origin, tau_evolve)
    for i, t in enumerate(t_gyr):
        if t <= 0:
            result[i] = 0.0
            continue
        t_prime_grid = np.linspace(0.01, t, 500)
        i_dot_t_prime = np.interp(t_prime_grid, t_int_grid, i_dot_grid)
        kernel = np.exp(-(t - t_prime_grid) / TAU_LAG_GYR)
        integrand = i_dot_t_prime * kernel
        result[i] = ALPHA * np.trapz(integrand, t_prime_grid)  # noqa: NPY201
    return result


def w_of_z(z_array, age_today_gyr, t_origin=9.0, tau_evolve=2.0):
    """w(z) = -1 - delta_w * P_info(z) / P_info(0).

    Calibrated such that w(0) = w_0_target = -1.005.
    """
    t_array, _ = age_at_z(z_array)
    p_info_array = p_info(t_array, age_today_gyr, t_origin, tau_evolve)
    p_info_today = p_info(np.array([age_today_gyr]), age_today_gyr, t_origin, tau_evolve)[0]
    if p_info_today == 0:
        return -np.ones_like(z_array)
    return -1.0 + DELTA_W_TARGET * (p_info_array / p_info_today)


def cpl(a, w0, wa):
    """w(a) = w_0 + w_a (1-a)."""
    return w0 + wa * (1.0 - a)


def fit_cpl_and_find_crossing(z_grid, w_grid):
    """Fit CPL form to w(z) curve over the given z grid; return (w0, wa, z_cross_CPL, z_cross_direct)."""
    a_grid = 1.0 / (1.0 + z_grid)
    popt, _ = curve_fit(cpl, a_grid, w_grid, p0=[-1.0, 0.0])
    w0_fit, wa_fit = popt

    if abs(wa_fit) < 1e-12:
        z_cross_fit = float('nan')
    else:
        a_cross = 1.0 + (1.0 + w0_fit) / wa_fit
        z_cross_fit = 1.0 / a_cross - 1.0 if a_cross > 0 else float('nan')

    z_cross_direct = None
    if w_grid[0] < -1.0 and w_grid[-1] > -1.0 + 1e-6:
        try:
            z_cross_direct = brentq(
                lambda z: np.interp(z, z_grid, w_grid) - (-1.0),
                z_grid[0] + 1e-6, z_grid[-1] - 1e-6
            )
        except ValueError:
            pass

    return w0_fit, wa_fit, z_cross_fit, z_cross_direct


def run_imp01(t_origin=9.0, tau_evolve=2.0, fit_range=(0.001, 1.5)):
    """Run the biogenic DE pipeline at given P_evolve parameters."""
    _, age_today = age_at_z(np.array([0.0]))
    z_grid_full = np.linspace(0.001, 1.5, 200)
    w_grid_full = w_of_z(z_grid_full, age_today, t_origin, tau_evolve)
    z_fit = np.linspace(fit_range[0], fit_range[1], 100)
    w_fit = w_of_z(z_fit, age_today, t_origin, tau_evolve)
    w0_fit, wa_fit, z_cross_fit, z_cross_direct = fit_cpl_and_find_crossing(z_fit, w_fit)
    return {
        "age_today_gyr": age_today,
        "t_origin_gyr": t_origin,
        "tau_evolve_gyr": tau_evolve,
        "tau_lag_gyr": TAU_LAG_GYR,
        "tau_bio_gyr": TAU_BIO_GYR,
        "lambda_bio": ALPHA,
        "w0_target": W0_TARGET,
        "delta_w_target": DELTA_W_TARGET,
        "fit_range_z": list(fit_range),
        "w0_CPL_fit": w0_fit,
        "wa_CPL_fit": wa_fit,
        "z_cross_CPL_fit": z_cross_fit,
        "z_cross_direct_brentq": z_cross_direct,
        "w_at_z_0": float(w_grid_full[0]),
        "w_at_z_028": float(np.interp(0.28, z_grid_full, w_grid_full)),
        "w_at_z_05": float(np.interp(0.5, z_grid_full, w_grid_full)),
        "w_at_z_10": float(np.interp(1.0, z_grid_full, w_grid_full)),
        "w_at_z_015": float(np.interp(0.15, z_grid_full, w_grid_full)),
        "w_minimum_value": float(np.min(w_grid_full)),
        "z_of_w_minimum": float(z_grid_full[np.argmin(w_grid_full)]),
    }


def run_sensitivity():
    """Run sensitivity over plausible (t_origin, tau_evolve) ranges."""
    results = []
    # Tier 3 calibrated anchor [Ledger C-sector]: sensitivity grid around the
    # biogenic-kernel timing choices; no grid point is selected to fit DESI.
    for t_origin in [7.0, 9.0, 10.5, 11.5, 12.5, 13.0, 13.4]:
        for tau_evolve in [0.5, 1.0, 2.0, 3.0]:
            r = run_imp01(t_origin, tau_evolve)
            results.append(r)
    return results


def run_tau_lag_sweep():
    """Sweep tau_lag and report the CPL linear-fit (w_0, w_a, z_cross_CPL_fit) triple as a function of the biogenic lag scale. The reported z_cross_CPL is a linear-extrapolation artifact, not a physical phantom crossing; the underlying w(z) asymptotes to -1 from below for all parameter choices in the sweep."""
    global TAU_LAG_GYR
    original = TAU_LAG_GYR
    results = []
    # Tier 3 calibrated anchor [Ledger C2]: tau_lag sensitivity grid.
    for tau_lag_test in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 7.0]:
        TAU_LAG_GYR = tau_lag_test
        r = run_imp01(t_origin=12.0, tau_evolve=1.0)
        r["tau_lag_swept"] = tau_lag_test
        results.append(r)
    TAU_LAG_GYR = original
    return results


def main():
    print("=" * 72)
    print("Biogenic DE w(z) Pipeline: (z_cross, w_0, w_a) CPL fit")
    print("=" * 72)

    default_run = run_imp01(t_origin=9.0, tau_evolve=2.0, fit_range=(0.001, 0.5))
    full_range_run = run_imp01(t_origin=9.0, tau_evolve=2.0, fit_range=(0.001, 1.5))

    print(f"\nHeadline run (t_origin = 9.0 Gyr, tau_evolve = 2.0 Gyr):")
    print(f"  Age of universe today       : {default_run['age_today_gyr']:.3f} Gyr")
    print(f"  tau_lag                     : {TAU_LAG_GYR} Gyr (Ledger)")
    print(f"  tau_bio                     : {TAU_BIO_GYR} Gyr (Sec 14.5.2)")
    print(f"  lambda_bio = alpha          : {ALPHA:.6f}")
    print(f"  delta_w target (Sec 14.5.1) : {DELTA_W_TARGET:+.4f}")
    print(f"  ---")
    print(f"  w(z=0)                      : {default_run['w_at_z_0']:+.4f}")
    print(f"  w(z=0.15)                   : {default_run['w_at_z_015']:+.4f}")
    print(f"  w(z=0.28)                   : {default_run['w_at_z_028']:+.4f}")
    print(f"  w(z=0.5)                    : {default_run['w_at_z_05']:+.4f}")
    print(f"  w(z=1.0)                    : {default_run['w_at_z_10']:+.4f}")
    print(f"  w minimum                   : {default_run['w_minimum_value']:+.4f} at z = {default_run['z_of_w_minimum']:.4f}")
    direct_z = default_run["z_cross_direct_brentq"]
    direct_z_str = f"{direct_z:+.4f}" if direct_z is not None else "null"
    print(f"  Direct z_cross (full w(z))  : {direct_z_str} (null = no mathematical crossing in scan range)")
    print(f"  ---")
    print(f"  LOW-Z CPL fit over z in [0, 0.5] (observational practice):")
    print(f"    w_0                       : {default_run['w0_CPL_fit']:+.4f}")
    print(f"    w_a                       : {default_run['wa_CPL_fit']:+.4f}")
    print(f"    CPL-extrapolated z_cross  : {default_run['z_cross_CPL_fit']:+.4f}")
    print(f"  ---")
    print(f"  FULL-RANGE CPL fit over z in [0, 1.5]:")
    print(f"    w_0                       : {full_range_run['w0_CPL_fit']:+.4f}")
    print(f"    w_a                       : {full_range_run['wa_CPL_fit']:+.4f}")
    print(f"    CPL-extrapolated z_cross  : {full_range_run['z_cross_CPL_fit']:+.4f}")

    print("\nSensitivity sweep over P_evolve parameters (tau_lag = 5 Gyr fixed per Ledger):")
    print(f"  {'t_orig':>7} {'tau_evolve':>11} {'w_0':>10} {'w_a':>10} {'z_cross':>10}")
    sensitivity = run_sensitivity()
    for r in sensitivity:
        zc = r['z_cross_CPL_fit']
        zc_str = f"{zc:+.4f}" if not math.isnan(zc) else "       nan"
        print(f"  {r['t_origin_gyr']:>7.1f} {r['tau_evolve_gyr']:>11.1f} "
              f"{r['w0_CPL_fit']:>+10.4f} {r['wa_CPL_fit']:>+10.4f} {zc_str:>10}")

    print("\ntau_lag sensitivity sweep (t_origin = 12.0, tau_evolve = 1.0 held):")
    print(f"  {'tau_lag':>9} {'w_0':>10} {'w_a':>10} {'z_cross':>10}")
    tau_lag_sweep = run_tau_lag_sweep()
    for r in tau_lag_sweep:
        zc = r['z_cross_CPL_fit']
        zc_str = f"{zc:+.4f}" if not math.isnan(zc) else "       nan"
        print(f"  {r['tau_lag_swept']:>9.1f} "
              f"{r['w0_CPL_fit']:>+10.4f} {r['wa_CPL_fit']:>+10.4f} {zc_str:>10}")

    output = {
        "headline_run": default_run,
        "continuous_phantom_no_direct_crossing": (
            default_run["w0_CPL_fit"] < -1.0
            and default_run["z_cross_direct_brentq"] is None
        ),
        "sensitivity_sweep": sensitivity,
        "tau_lag_sweep": tau_lag_sweep,
    }
    if OUTPUT_DIR_AVAILABLE:
        out_path = get_output_path("protocol_imp01_pipeline_results.json")
    else:
        out_path = Path(__file__).resolve().parent.parent / "data" / "protocol_imp01_pipeline_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(_json_safe(output), f, indent=2, allow_nan=False)
    print(f"\nFull results written to {out_path}")
    print("=" * 72)

    return output


if __name__ == "__main__":
    main()
