#!/usr/bin/env python3
"""
protocol_o17p_isw_amplitude.py
==============================

Quantitative derivation of the biogenic-DE perturbation to the late-time
Integrated Sachs-Wolfe (ISW) signal from the V2 Ch14 Sec 14.5.1
lag-kernel action. Addresses the V3 Ch12 Sec 12.4.2 prediction that GCT
predicts an "anomalous ISW signal correlated with the 'age' and
'biological potential' of galaxy clusters rather than their simple
gravitational mass."

PHYSICAL SETUP
--------------

Standard ISW (Sachs & Wolfe 1967; Crittenden & Turok 1996):
    Delta_T_ISW(n_hat) / T_CMB = 2 * integral_0^{z_LSS} dPhi/dz * dz
where Phi is the Newtonian gravitational potential along the line of
sight. In LambdaCDM, dPhi/dz != 0 only at late times when the matter-
dominated epoch ends and DE drives the linear growth factor D(z) below
its EdS value.

The cross-correlation of ISW with galaxy density g(n_hat) at angular
scale l is:
    C_l^{ISW-g} = (3 H_0^2 Omega_m / c^2) * integral dz f_g(z) Phi_dot(z) P_m(k)
peaking at l ~ 10-30 and amplitude ~ 0.5 muK at l ~ 20 (Crittenden &
Turok 1996; Boughn & Crittenden 2004; Stoelzner+ 2018 ApJ 870:60).

BIOGENIC-DE PERTURBATION
------------------------

The GCT biogenic-DE adds delta_w(z) = -0.005 * P_info(z)/P_info(0) to
the equation of state. This modifies the linear growth factor D(z) via
the standard linear-growth ODE:
    D''(a) + (3/a + dlnH/dlna) D'(a) - (3/2) Omega_m(a) D(a) / a^2 = 0
with Omega_m(a) = Omega_m_0 / [Omega_m_0 + Omega_L exp(3 int(1+w(z'))/(1+z') dz')].

The fractional ISW amplitude shift is bounded by the fractional growth-
factor shift integrated over the ISW kernel:
    delta(C_l^{ISW-g}) / C_l^{ISW-g} ~ <delta D(z) / D(z)>_{ISW kernel}
where the average is weighted by the ISW kernel (peaks at z ~ 0.4).

BIOGENIC vs GRAVITATIONAL CROSS-CORRELATION DIFFERENTIAL
--------------------------------------------------------

V3 Ch12 Sec 12.4.2 claims the GCT signal correlates with BIOGENIC
potential rather than purely gravitational mass. In a region of biogenic
overdensity delta_bio (relative to cosmic mean), the local w(z) is more
phantom: w_local(z) = -1 + (1+delta_bio) * delta_w_cosmic(z), and the
local ISW contribution scales as ~(1+delta_bio) * standard ISW.

Cross-correlation of CMB with a BIOGENIC-tracer map (e.g., galaxy
stellar mass weighted by integrated SFR) vs. a GRAVITATIONAL-tracer
map (pure halo mass) measures the DIFFERENTIAL:
    C_l^{ISW-bio} - C_l^{ISW-grav} ~ <delta_bio - delta_m> * standard ISW
where the angle bracket is the cross-correlation of (biogenic - mass)
overdensity with the matter density on scales probed.

OBSERVATIONAL SENSITIVITIES
---------------------------

Current Planck x galaxy survey ISW:
  - Stoelzner+ 2018 ApJ 870:60: 4.0 sigma ISW detection (Planck +
    KiDS-450 + 2dFLenS); amplitude consistent with LambdaCDM to ~25%.
  - Hang+ 2021 MNRAS 501:1481: 5.2 sigma ISW (Planck PR3 + DES Y3);
    ~20% precision on A_ISW vs LambdaCDM prediction.

Future:
  - CMB-S4 (operational 2030+): factor ~3 improvement in ISW SNR.
  - SPHEREx + LSST (cross-correlation): factor ~5 improvement in
    differential cross-correlation precision.

VERDICT FRAMEWORK
-----------------

Closure of O.17p has two possible outcomes:
  (i)  If the biogenic-DE ISW perturbation is >= 10% of standard ISW
       --> promote V3 Ch12 Sec 12.4.2 from Tier 3 to Tier 2 prediction;
       observationally detectable with CMB-S4 + SPHEREx joint analysis.
  (ii) If the biogenic-DE ISW perturbation is << 10% of standard ISW
       --> carry Sec 12.4.2 with explicit magnitude; identify the
       smallest near-future experiment that could detect it (if any);
       acknowledge the prediction is too small for current measurement.

Unlike O.17 (Hubble tension closure), the ISW perturbation sign is
expected to be CONSISTENT with the standard ISW direction (both source
from late-time potential decay), so the sign issue from O.17 does not
recur here.
"""

import json
import numpy as np
from pathlib import Path
from scipy.integrate import cumulative_trapezoid, odeint
from scipy.interpolate import interp1d

try:
    from gct_utils import get_output_path
    OUTPUT_DIR_AVAILABLE = True
except ImportError:
    OUTPUT_DIR_AVAILABLE = False

# Re-use biogenic DE constants for consistency with V2 Ch14 Sec 14.5.1
H0_KM_S_MPC = 67.4
OMEGA_M = 0.315
OMEGA_L = 0.685
ALPHA = 1.0 / 137.036
TAU_LAG_GYR = 5.0
TAU_BIO_GYR = 4.5
W0_TARGET = -1.005
DELTA_W_TARGET = W0_TARGET - (-1.0)

MPC_TO_KM = 3.0857e19
SEC_PER_GYR = 3.1557e16
HUBBLE_TIME_GYR = (MPC_TO_KM / H0_KM_S_MPC) / SEC_PER_GYR

# ISW signal kernel peak redshift (where dPhi/dz is maximal)
Z_ISW_PEAK = 0.4

# Observational anchors
ISW_AMPLITUDE_PRECISION_PLANCK = 0.20  # Hang+ 2021 fractional precision on A_ISW
ISW_DETECTABILITY_THRESHOLD_CURRENT = 0.20  # Planck-era detectability
ISW_DETECTABILITY_THRESHOLD_CMBS4_SPHEREX = 0.04  # CMB-S4 + SPHEREx joint


def hubble_z(z, w_z=None, z_array=None):
    """H(z)/H_0 for flat cosmology with optional w(z) input.

    If w_z is None: LambdaCDM (w = -1).
    Else w_z[i] is w at z_array[i]; interpolated to z and integrated.
    """
    if w_z is None:
        return np.sqrt(OMEGA_M * (1.0 + z) ** 3 + OMEGA_L)
    # Compute rho_L(z)/rho_L(0) = exp[3 * int_0^z (1+w(z'))/(1+z') dz']
    integrand = 3.0 * (1.0 + w_z) / (1.0 + z_array)
    log_ratio = cumulative_trapezoid(integrand, z_array, initial=0.0)
    rho_L_ratio_at_z = np.interp(z, z_array, np.exp(log_ratio))
    return np.sqrt(OMEGA_M * (1.0 + z) ** 3 + OMEGA_L * rho_L_ratio_at_z)


def age_at_z(z_array, z_max=1000.0, n_int=20000):
    z_grid = np.linspace(0.0, z_max, n_int)
    integrand = 1.0 / ((1.0 + z_grid) * hubble_z(z_grid))
    elapsed_from_now = cumulative_trapezoid(integrand, z_grid, initial=0.0) * HUBBLE_TIME_GYR
    age_total = HUBBLE_TIME_GYR * np.trapz(integrand, z_grid)
    age_at_z_grid = age_total - elapsed_from_now
    return np.interp(z_array, z_grid, age_at_z_grid), age_total


def z_at_age(t_array_gyr, age_today_gyr, z_grid_max=1000.0, n_int=20000):
    z_grid = np.linspace(0.0, z_grid_max, n_int)
    ages_grid, _ = age_at_z(z_grid)
    return np.interp(t_array_gyr, ages_grid[::-1], z_grid[::-1])


def sfr_madau_dickinson(z):
    return 0.015 * (1.0 + z) ** 2.7 / (1.0 + ((1.0 + z) / 2.9) ** 5.6)


def sfr_at_time(t_array_gyr, age_today_gyr):
    z = z_at_age(t_array_gyr, age_today_gyr)
    return sfr_madau_dickinson(z)


def p_evolve(t_gyr, t_origin=9.0, tau_evolve=2.0):
    sigmoid = 1.0 / (1.0 + np.exp(-(t_gyr - t_origin) / 0.5))
    growth = np.exp((t_gyr - t_origin) / tau_evolve)
    return sigmoid * growth


def i_dot(t_gyr, age_today_gyr, t_origin=9.0, tau_evolve=2.0):
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
        result[i] = np.trapz(integrand, t_prime_grid)
    return result


def p_info_cosmic(t_gyr, age_today_gyr, t_origin=9.0, tau_evolve=2.0):
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
        result[i] = ALPHA * np.trapz(integrand, t_prime_grid)
    return result


def w_cosmic_of_z(z_array, age_today_gyr, t_origin=9.0, tau_evolve=2.0):
    """Cosmic-mean w(z) = -1 + DELTA_W_TARGET * P_info(z)/P_info(0)."""
    t_array, _ = age_at_z(z_array)
    p_info_array = p_info_cosmic(t_array, age_today_gyr, t_origin, tau_evolve)
    p_info_today = p_info_cosmic(np.array([age_today_gyr]), age_today_gyr,
                                 t_origin, tau_evolve)[0]
    if p_info_today == 0:
        return -np.ones_like(z_array)
    return -1.0 + DELTA_W_TARGET * (p_info_array / p_info_today)


def linear_growth_factor(z_grid, w_z=None):
    """Solve the linear-growth ODE for D(a) under arbitrary w(z).

    D''(a) + (3/a + dlnH/dlna) D'(a) - (3/2) Omega_m(a) D(a) / a^2 = 0
    Normalisation: D(a=1) = 1.

    Returns D(z) on the input z_grid.
    """
    a_grid = 1.0 / (1.0 + z_grid[::-1])  # ascending in a
    z_grid_asc = z_grid[::-1]

    # H(a) under modified w(z)
    if w_z is None:
        rho_L_ratio = np.ones_like(z_grid_asc)
    else:
        # w_z is on the original z_grid (descending), reorder ascending
        w_z_asc = w_z[::-1]
        integrand = 3.0 * (1.0 + w_z_asc) / (1.0 + z_grid_asc)
        log_ratio = cumulative_trapezoid(integrand, z_grid_asc, initial=0.0)
        rho_L_ratio = np.exp(log_ratio)

    h_sq = OMEGA_M * (1.0 + z_grid_asc) ** 3 + OMEGA_L * rho_L_ratio
    h = np.sqrt(h_sq)
    omega_m_of_a = OMEGA_M * (1.0 + z_grid_asc) ** 3 / h_sq

    # dlnH/dlna interpolant
    lna = np.log(a_grid)
    lnh = np.log(h)
    dlnh_dlna = np.gradient(lnh, lna)

    h_of_a = interp1d(a_grid, h, fill_value="extrapolate")
    om_of_a = interp1d(a_grid, omega_m_of_a, fill_value="extrapolate")
    dlnh_of_a = interp1d(a_grid, dlnh_dlna, fill_value="extrapolate")

    def growth_ode(D_state, a):
        D, Dp = D_state
        Dpp = -(3.0 / a + dlnh_of_a(a)) * Dp + (3.0 / 2.0) * om_of_a(a) * D / a ** 2
        return [Dp, Dpp]

    # Integrate from a_init small (deep matter era) to a = 1
    a_init = 1e-3
    D_init = a_init  # matter-era growth D(a) ~ a
    Dp_init = 1.0  # dD/da ~ 1 in matter era
    a_int_grid = np.linspace(a_init, 1.0, 5000)
    sol = odeint(growth_ode, [D_init, Dp_init], a_int_grid)
    D_a = sol[:, 0]

    # Normalize so D(a=1) = 1
    D_a = D_a / D_a[-1]

    # Interpolate to the original z_grid
    z_int = 1.0 / a_int_grid - 1.0
    D_of_z = interp1d(z_int[::-1], D_a[::-1], fill_value="extrapolate")
    return D_of_z(z_grid)


def isw_kernel_amplitude(z_grid, w_z=None):
    """Compute the ISW kernel amplitude |dPhi/dz| at each z.

    Phi(z) propto Omega_m(a) * D(a) / a -- the growth-suppressed potential.
    dPhi/dz captures the late-time potential decay sourcing ISW.
    Returns the normalized ISW source function (peaked at z ~ 0.4 in LCDM).
    """
    a_grid = 1.0 / (1.0 + z_grid)
    D_z = linear_growth_factor(z_grid, w_z=w_z)
    # Phi ~ D(a) / a
    phi_a = D_z / a_grid
    # dPhi/dz; gradient w.r.t. z
    dphi_dz = np.gradient(phi_a, z_grid)
    return dphi_dz, D_z


def isw_signal_integrated(z_grid, w_z=None, z_lo=0.0, z_hi=2.0):
    """Total ISW amplitude proxy: integral of |dPhi/dz| over the ISW window.

    This is a SCALING proxy for the ISW C_l amplitude; the absolute
    normalisation depends on cosmology, galaxy bias, and the kernel
    convolution, but the FRACTIONAL ratio between LambdaCDM and modified
    cosmologies is robust at the few-% level.
    """
    dphi_dz, _ = isw_kernel_amplitude(z_grid, w_z=w_z)
    mask = (z_grid >= z_lo) & (z_grid <= z_hi)
    return np.trapz(np.abs(dphi_dz[mask]), z_grid[mask])


def run_o17p(t_origin=9.0, tau_evolve=2.0):
    """Compute biogenic-DE perturbation to ISW signal amplitude."""
    _, age_today = age_at_z(np.array([0.0]))

    # Working z grid for w(z) and growth-factor computation
    z_grid = np.linspace(1e-3, 3.0, 200)

    # LambdaCDM baseline
    isw_lcdm = isw_signal_integrated(z_grid, w_z=None)
    D_lcdm = linear_growth_factor(z_grid, w_z=None)

    # Cosmic-mean biogenic-DE
    w_cosmic = w_cosmic_of_z(z_grid, age_today, t_origin, tau_evolve)
    isw_cosmic = isw_signal_integrated(z_grid, w_z=w_cosmic)
    D_cosmic = linear_growth_factor(z_grid, w_z=w_cosmic)

    isw_perturbation_cosmic = (isw_cosmic - isw_lcdm) / isw_lcdm

    # Growth-factor shift at the ISW kernel peak
    D_lcdm_peak = float(np.interp(Z_ISW_PEAK, z_grid, D_lcdm))
    D_cosmic_peak = float(np.interp(Z_ISW_PEAK, z_grid, D_cosmic))
    delta_D_over_D_peak = (D_cosmic_peak - D_lcdm_peak) / D_lcdm_peak

    # Biogenic-overdensity scaling: at delta_bio overdensity, local
    # ISW perturbation scales as (1 + delta_bio) * cosmic-mean perturbation
    delta_bio_anchors = {
        "void": -0.7,
        "cosmic_mean": 0.0,
        "local_sheet": 1.5,
        "laniakea": 3.5,
        "filament": 7.5,
        "cluster_core": 30.0,
    }
    isw_local_by_anchor = {}
    for name, db in delta_bio_anchors.items():
        # Local w_local = -1 + (1+db) * delta_w_cosmic
        delta_w_cosmic = w_cosmic + 1.0
        w_local = -1.0 + (1.0 + db) * delta_w_cosmic
        isw_local = isw_signal_integrated(z_grid, w_z=w_local)
        isw_perturbation_local = (isw_local - isw_lcdm) / isw_lcdm
        isw_local_by_anchor[name] = {
            "delta_bio": db,
            "ISW_perturbation_local_fractional": float(isw_perturbation_local),
            "ISW_perturbation_local_percent": float(100.0 * isw_perturbation_local),
        }

    # Differential cross-correlation amplitude (biogenic-mass vs gravity-mass)
    # The differential is bounded by:
    #   delta(C_l^{ISW-bio} - C_l^{ISW-grav}) / C_l^{ISW-grav}
    #     ~ <delta_bio - delta_m>_corr * (cosmic-mean ISW perturbation)
    # For LSS, <delta_bio - delta_m> on the relevant scales is set by the
    # bias factor: b_bio / b_m - 1. Realistic values for biogenic-weighted
    # vs mass-weighted tracers: |b_bio/b_m - 1| ~ 0.1 to 0.3 (Hopkins+ 2008
    # for stellar-mass-weighted vs halo-mass-weighted galaxy samples).
    bias_diff_low = 0.1
    bias_diff_high = 0.3
    differential_low = bias_diff_low * isw_perturbation_cosmic
    differential_high = bias_diff_high * isw_perturbation_cosmic

    # Detectability
    detectable_planck = abs(isw_perturbation_cosmic) >= ISW_DETECTABILITY_THRESHOLD_CURRENT
    detectable_cmbs4 = abs(isw_perturbation_cosmic) >= ISW_DETECTABILITY_THRESHOLD_CMBS4_SPHEREX
    differential_detectable_cmbs4 = abs(differential_high) >= ISW_DETECTABILITY_THRESHOLD_CMBS4_SPHEREX

    # Sign analysis
    sign_consistent_with_standard_isw = isw_perturbation_cosmic > 0

    return {
        "age_today_gyr": float(age_today),
        "t_origin_gyr": t_origin,
        "tau_evolve_gyr": tau_evolve,
        "tau_lag_gyr": TAU_LAG_GYR,
        "tau_bio_gyr": TAU_BIO_GYR,
        "lambda_bio": ALPHA,
        "delta_w_cosmic_z0": DELTA_W_TARGET,
        "ISW_LCDM_amplitude_proxy": float(isw_lcdm),
        "ISW_cosmic_biogenic_amplitude_proxy": float(isw_cosmic),
        "ISW_perturbation_cosmic_fractional": float(isw_perturbation_cosmic),
        "ISW_perturbation_cosmic_percent": float(100.0 * isw_perturbation_cosmic),
        "delta_D_over_D_at_z_ISW_peak": float(delta_D_over_D_peak),
        "delta_D_over_D_at_z_ISW_peak_percent": float(100.0 * delta_D_over_D_peak),
        "isw_local_by_anchor": isw_local_by_anchor,
        "differential_cross_correlation_low_bias_pct": float(100.0 * differential_low),
        "differential_cross_correlation_high_bias_pct": float(100.0 * differential_high),
        "current_planck_isw_precision": ISW_AMPLITUDE_PRECISION_PLANCK,
        "current_planck_detectability_threshold": ISW_DETECTABILITY_THRESHOLD_CURRENT,
        "cmbs4_spherex_detectability_threshold": ISW_DETECTABILITY_THRESHOLD_CMBS4_SPHEREX,
        "detectable_with_current_planck": bool(detectable_planck),
        "detectable_with_cmbs4_spherex": bool(detectable_cmbs4),
        "differential_detectable_with_cmbs4_spherex": bool(differential_detectable_cmbs4),
        "sign_consistent_with_standard_isw": bool(sign_consistent_with_standard_isw),
    }


def verdict(results):
    """Determine the closure direction for O.17p."""
    cosmic_pert_pct = abs(results["ISW_perturbation_cosmic_percent"])
    differential_max_pct = abs(results["differential_cross_correlation_high_bias_pct"])
    sign_consistent = results["sign_consistent_with_standard_isw"]

    if results["detectable_with_current_planck"]:
        direction = "(i) PROMOTE to Tier 2 -- detectable with current Planck"
        framing = (
            f"Cosmic-mean ISW amplitude shift is {cosmic_pert_pct:.2f}% "
            f"of LambdaCDM, above current Planck precision (20%). "
            f"V3 Ch12 Sec 12.4.2 can be promoted to Tier 2 with this "
            f"magnitude as the derived prediction."
        )
    elif results["differential_detectable_with_cmbs4_spherex"]:
        direction = "(i-prospective) PROMOTE conditional on CMB-S4 + SPHEREx"
        framing = (
            f"Cosmic-mean ISW amplitude shift is {cosmic_pert_pct:.2f}% "
            f"of LambdaCDM -- below current Planck precision (20%) but "
            f"the differential cross-correlation amplitude "
            f"(up to {differential_max_pct:.2f}% of standard ISW under "
            f"realistic biogenic-vs-gravitational bias differences) "
            f"approaches the CMB-S4 + SPHEREx detectability threshold "
            f"(~4%). The biogenic-vs-gravitational tracer differential "
            f"is the closer-binding observational signature. Sign is "
            f"{'CONSISTENT' if sign_consistent else 'OPPOSITE'} "
            f"with standard ISW direction."
        )
    else:
        direction = "(ii) MAGNITUDE_DISCLOSURE_BELOW_NEAR_FUTURE_SENSITIVITY"
        framing = (
            f"Cosmic-mean ISW amplitude shift is {cosmic_pert_pct:.2f}% "
            f"of LambdaCDM, with biogenic-vs-gravitational differential "
            f"up to {differential_max_pct:.2f}% of standard ISW under "
            f"realistic bias differences. Both numbers are below the "
            f"CMB-S4 + SPHEREx detectability threshold (~4%). V3 Ch12 "
            f"Sec 12.4.2 carries these explicit magnitudes and the "
            f"smallest experiment that could detect "
            f"the signal identified (likely post-CMB-S5 / 30m-class "
            f"radio + IR spectroscopic surveys, or via population-"
            f"averaged stacking on stellar-mass-weighted galaxy samples). "
            f"Sign is {'CONSISTENT' if sign_consistent else 'OPPOSITE'} "
            f"with standard ISW direction -- {'no sign issue, unlike O.17 closure' if sign_consistent else 'sign issue similar to O.17'}."
        )

    return {
        "direction": direction,
        "framing": framing,
        "cosmic_perturbation_pct": cosmic_pert_pct,
        "differential_max_pct": differential_max_pct,
        "sign_consistent": sign_consistent,
    }


def main():
    print("=" * 72)
    print("O.17p PROTOCOL: Biogenic-DE perturbation to ISW signal amplitude")
    print("=" * 72)

    results = run_o17p(t_origin=9.0, tau_evolve=2.0)

    print(f"\nBaselines and biogenic-DE inputs:")
    print(f"  Age of universe today                       : {results['age_today_gyr']:.3f} Gyr")
    print(f"  delta_w_cosmic(z=0)                         : {results['delta_w_cosmic_z0']:+.4f}")
    print(f"  delta_D / D at z_ISW_peak ({Z_ISW_PEAK:.2f})              : {results['delta_D_over_D_at_z_ISW_peak_percent']:+.4f}%")
    print(f"  ISW_LambdaCDM_amplitude_proxy               : {results['ISW_LCDM_amplitude_proxy']:.6f}")
    print(f"  ISW_cosmic_biogenic_amplitude_proxy         : {results['ISW_cosmic_biogenic_amplitude_proxy']:.6f}")
    print(f"  ISW_perturbation_cosmic                     : {results['ISW_perturbation_cosmic_percent']:+.4f}%")
    print(f"  Sign consistent with standard ISW direction : {results['sign_consistent_with_standard_isw']}")

    print(f"\nLocal ISW perturbation by biogenic overdensity anchor:")
    print(f"  {'Anchor':<16} {'delta_bio':>10} {'ISW shift [%]':>16}")
    for name, data in results["isw_local_by_anchor"].items():
        print(f"  {name:<16} {data['delta_bio']:>+10.2f} "
              f"{data['ISW_perturbation_local_percent']:>+16.4f}")

    print(f"\nDifferential cross-correlation (biogenic vs gravitational tracers):")
    print(f"  Low-bias-diff scenario   (|b_bio/b_m - 1| = 0.1): {results['differential_cross_correlation_low_bias_pct']:+.4f}% of LCDM ISW")
    print(f"  High-bias-diff scenario  (|b_bio/b_m - 1| = 0.3): {results['differential_cross_correlation_high_bias_pct']:+.4f}% of LCDM ISW")

    print(f"\nDetectability:")
    print(f"  Current Planck precision (~20%)             : {'YES' if results['detectable_with_current_planck'] else 'NO'}")
    print(f"  CMB-S4 + SPHEREx (~4%) cosmic-mean signal   : {'YES' if results['detectable_with_cmbs4_spherex'] else 'NO'}")
    print(f"  CMB-S4 + SPHEREx differential (high-bias)   : {'YES' if results['differential_detectable_with_cmbs4_spherex'] else 'NO'}")

    v = verdict(results)
    print(f"\nVerdict for O.17p:")
    print(f"  Direction : {v['direction']}")
    print(f"  Framing   : {v['framing']}")

    output = {"results": results, "verdict": v}
    if OUTPUT_DIR_AVAILABLE:
        out_path = get_output_path("protocol_o17p_isw_amplitude_results.json")
    else:
        out_path = Path(__file__).resolve().parent.parent / "data" / "protocol_o17p_isw_amplitude_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nFull results written to {out_path}")
    print("=" * 72)

    return output


if __name__ == "__main__":
    main()
