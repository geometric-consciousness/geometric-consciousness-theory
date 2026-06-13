#!/usr/bin/env python3
"""
protocol_o17_delta_h_local.py
=============================

Quantitative derivation of the local Hubble excess delta H_local from the
GCT biogenic-driving action (V2 Ch14 Sec 14.5.1 lag-kernel + Sec 14.5.4
local-environment framing). Addresses Open Problem O.17.

PHYSICAL SETUP
--------------

The biogenic-driven dark-energy equation of state at cosmic mean is:
    w_cosmic(z) = -1 + delta_w_cosmic(z),  delta_w_cosmic(0) approx -0.005
calibrated by the biogenic DE pipeline (`protocol_imp01_pipeline.py`).

In a region with biogenic-information overdensity factor delta_bio
(defined as rho_bio,local/rho_bio,cosmic - 1), the local informational
pressure P_info,local scales linearly with the local information density,
since Sec 14.5.1 P_info = lambda_bio * integral i_dot * K dt' is a single
integral linear in i_dot. So:
    w_local(z) = -1 + (1 + delta_bio) * delta_w_cosmic(z)

LOCAL H_0 EXCESS INFERRED VIA q_0 CORRECTION
--------------------------------------------

The SH0ES distance ladder infers H_0 from the local Hubble flow at
median redshift z ~ 0.05-0.1 via:
    d_L(z) = (c z / H_0_inferred) * [1 + (1/2)(1 - q_0) z + O(z^2)]
so that
    H_0_inferred = (c z / d_L_measured) * [1 + (1/2)(1 - q_0) z + ...]

Two regions with the same H_0 at z=0 but different q_0 give different
H_0_inferred from the same distance-ladder measurement at finite z.

The local q_0 is:
    q_0_local = (1/2) Omega_m + (1/2)(1 + 3 w_local(0)) Omega_Lambda
              = q_0_cosmic + (3/2) Omega_Lambda * (w_local(0) - w_cosmic(0))
              = q_0_cosmic + (3/2) Omega_Lambda * delta_bio * delta_w_cosmic(0)

For phantom delta_w < 0 in an overdense region (delta_bio > 0), q_0_local
is MORE NEGATIVE (more accelerating), but the SH0ES-style cosmographic
inference shifts the fitted H_0 downward:
    H_0_inferred_local - H_0_inferred_cosmic =
        -(1/2) z * Omega_Lambda * (3/2) * delta_bio * delta_w_cosmic(0) * H_0

i.e.
    delta_H_local / H_0 = +(3/4) Omega_Lambda * z_SH0ES * delta_bio * delta_w_cosmic(0)

For Omega_Lambda = 0.685, z_SH0ES = 0.075 (SH0ES median), delta_w_cosmic(0) = -0.005:
    delta_H_local / H_0 = (3/4) * 0.685 * 0.075 * delta_bio * (-0.005)
                        = -1.9e-4 * delta_bio                           [eqn A]

INTEGRAL ENHANCEMENT FROM SUSTAINED PHANTOM PHASE
-------------------------------------------------

A stronger effect comes from the integrated lookback-time enhancement of
the local dark-energy density relative to the cosmic mean. Solving the
modified Friedmann equation with a sustained phantom w_local(z) yields:
    rho_Lambda_local(z) / rho_Lambda_cosmic(z) =
        exp[ 3 * integral_0^z (w_local - w_cosmic)/(1+z') dz' ]
      = exp[ 3 delta_bio * integral_0^z delta_w_cosmic(z')/(1+z') dz' ]

For SH0ES inference at z_SH0ES ~ 0.075, the integral over the Hubble-flow
window is small (delta_w_cosmic is small + the window is narrow), so the
exponent stays at the few-percent level for plausible delta_bio.

We compute the FULL local Hubble rate at z=0 from a locally-modified
Friedmann equation with w_local(z) replacing w_cosmic(z) everywhere, then
extract the SH0ES-style inferred H_0 from the d_L(z) curve in the Hubble-
flow window via fit to the small-z expansion above.

OBSERVATIONAL OVERDENSITY ANCHORS
---------------------------------

Realistic biogenic-information overdensity factors at scales probed by
the SH0ES distance ladder (~100 Mpc):
  Local Sheet               delta_bio ~ 1-2     (Tully et al. 2014)
  Laniakea supercluster     delta_bio ~ 2-5     (Tully et al. 2014)
  Galaxy filament (Mpc)     delta_bio ~ 5-10    (Cautun et al. 2014)
  Dense cluster core (Mpc)  delta_bio ~ 10-100  (Hoffman et al. 2017)
  Cosmic void               delta_bio ~ -0.7    (Pan et al. 2012)

The SH0ES distance ladder samples a heterogeneous mix; the effective
average delta_bio at the volume-average over the SH0ES sample is ~1-3
(Local Sheet to Laniakea scale).

VERDICT FRAMEWORK
-----------------

Closure of O.17 has two possible outcomes:
  (i)  if delta_H_local / H_0 (delta_bio = 1-3) reproduces the ~0.09
       observed SH0ES-vs-Planck tension --> promote Sec 14.5.4 from
       Tier 3 consistency to Tier 2 prediction
  (ii) if delta_H_local / H_0 (delta_bio = 1-3) is too small (<< 0.09)
       to account for the tension --> classify the row as a non-solution
       for the full Hubble tension and report the sign and magnitude at
       realistic overdensity

This protocol computes the predicted delta_H_local across the realistic
delta_bio range and reports the verdict.
"""

import json
import numpy as np
from pathlib import Path
from scipy.integrate import cumulative_trapezoid
from scipy.optimize import curve_fit

try:
    from gct_utils import get_output_path
    OUTPUT_DIR_AVAILABLE = True
except ImportError:
    OUTPUT_DIR_AVAILABLE = False

# Re-use biogenic DE constants for consistency with Ch14 Sec 14.5.1
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

# SH0ES distance ladder median redshift (Riess et al. 2022 ApJ 934:L7)
Z_SH0ES = 0.075

# Observed Hubble tension magnitude (SH0ES vs Planck)
# Riess+ 2022: H0_SH0ES = 73.04 +/- 1.04
# Planck 2020: H0_Planck = 67.4 +/- 0.5
# Fractional tension: (73.04 - 67.4) / 67.4 = 0.0837 -- "~9%" colloquially
H0_SH0ES_OBS = 73.04
H0_PLANCK_OBS = 67.4
TENSION_FRACTIONAL = (H0_SH0ES_OBS - H0_PLANCK_OBS) / H0_PLANCK_OBS  # = 0.0837

# Overdensity anchors at the SH0ES distance-ladder scale (~100 Mpc)
DELTA_BIO_ANCHORS = {
    "void": -0.7,
    "cosmic_mean": 0.0,
    "local_sheet": 1.5,
    "laniakea": 3.5,
    "filament": 7.5,
    "cluster_core": 30.0,
}


def hubble_z(z):
    """H(z)/H_0 for flat LambdaCDM cosmic mean."""
    return np.sqrt(OMEGA_M * (1.0 + z) ** 3 + OMEGA_L)


def age_at_z(z_array, z_max=1000.0, n_int=20000):
    """Cosmic time t (in Gyr) at redshift z, measured from Big Bang."""
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
    """Cosmic-mean P_info(t) from the biogenic DE pipeline (lambda_bio = alpha)."""
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


def w_local_of_z(z_array, delta_bio, age_today_gyr,
                 t_origin=9.0, tau_evolve=2.0):
    """Local w(z) with biogenic overdensity factor delta_bio.

    Linear scaling: P_info_local = (1 + delta_bio) * P_info_cosmic
    --> delta_w_local(z) = (1 + delta_bio) * delta_w_cosmic(z)
    """
    w_cosmic = w_cosmic_of_z(z_array, age_today_gyr, t_origin, tau_evolve)
    delta_w_cosmic = w_cosmic + 1.0
    return -1.0 + (1.0 + delta_bio) * delta_w_cosmic


def rho_lambda_ratio(z_array, w_z_array):
    """rho_Lambda(z) / rho_Lambda(0) for arbitrary w(z) curve.

    Standard result: rho_L(z)/rho_L(0) = exp[3 * int_0^z (1 + w(z'))/(1+z') dz'].
    """
    z_sorted_idx = np.argsort(z_array)
    z_sorted = z_array[z_sorted_idx]
    w_sorted = w_z_array[z_sorted_idx]
    integrand = 3.0 * (1.0 + w_sorted) / (1.0 + z_sorted)
    log_ratio = cumulative_trapezoid(integrand, z_sorted, initial=0.0)
    # Undo sorting
    out = np.empty_like(z_array)
    out[z_sorted_idx] = np.exp(log_ratio)
    return out


def hubble_local_of_z(z_array, delta_bio, age_today_gyr,
                      t_origin=9.0, tau_evolve=2.0):
    """Local H(z)/H_0 for a region with biogenic overdensity delta_bio.

    Friedmann with locally-modified dark-energy evolution:
        H_local(z)^2 / H_0^2 = Omega_m * (1+z)^3 + Omega_L * rho_L_local(z)/rho_L(0)

    H_0 here is the GLOBAL H_0 (Planck CMB-anchored); the SH0ES distance
    ladder will infer a DIFFERENT H_0 from this curve at small z.
    """
    w_local = w_local_of_z(z_array, delta_bio, age_today_gyr, t_origin, tau_evolve)
    rho_L_ratio = rho_lambda_ratio(z_array, w_local)
    return np.sqrt(OMEGA_M * (1.0 + z_array) ** 3 + OMEGA_L * rho_L_ratio)


def luminosity_distance_local(z_array, delta_bio, age_today_gyr,
                              t_origin=9.0, tau_evolve=2.0,
                              z_fine_max=2.0, n_fine=2000):
    """d_L(z) for a local region; units of c/H_0."""
    z_fine = np.linspace(0.0, z_fine_max, n_fine)
    h_local_fine = hubble_local_of_z(z_fine, delta_bio, age_today_gyr,
                                     t_origin, tau_evolve)
    # comoving distance D_C(z) = int_0^z dz'/H(z')   in units c/H_0
    one_over_h = 1.0 / h_local_fine
    d_c_fine = cumulative_trapezoid(one_over_h, z_fine, initial=0.0)
    d_c_query = np.interp(z_array, z_fine, d_c_fine)
    return (1.0 + z_array) * d_c_query


def shoes_inferred_h0(delta_bio, age_today_gyr,
                      z_min=0.023, z_max=0.15, n_z=20,
                      t_origin=9.0, tau_evolve=2.0,
                      fit_order="kinematic"):
    """SH0ES-style inferred H_0 from the local Hubble flow.

    fit_order options (recovered H_0_inferred / H_0_global):
      "linear"    : Fit y = A + B z, recover 1/A.  Includes leading
                    cosmography curvature as an offset; small artifact
                    in the recovered intercept from a finite-z window.
      "kinematic" : Fit y = A + B z + C z^2, recover 1/A.  Riess+ 2022
                    methodology: kinematic cosmography (H_0, q_0, j_0)
                    fit over the SH0ES Hubble-flow window.  Recovers
                    the true z=0 intercept to higher accuracy.
    """
    z_grid = np.linspace(z_min, z_max, n_z)
    d_L_grid = luminosity_distance_local(z_grid, delta_bio, age_today_gyr,
                                          t_origin, tau_evolve)
    y = d_L_grid / z_grid

    if fit_order == "linear":
        def model(zz, A, B):
            return A + B * zz
        popt, _ = curve_fit(model, z_grid, y, p0=[1.0, 0.0])
    elif fit_order == "kinematic":
        def model(zz, A, B, C):
            return A + B * zz + C * zz * zz
        popt, _ = curve_fit(model, z_grid, y, p0=[1.0, 0.0, 0.0])
    else:
        raise ValueError(f"unknown fit_order: {fit_order}")
    A_fit = popt[0]
    return 1.0 / A_fit  # H_0_inferred / H_0_global


def planck_inferred_h0(delta_bio, age_today_gyr,
                       t_origin=9.0, tau_evolve=2.0,
                       z_cmb=1100.0):
    """Planck-style H_0 inferred by fitting the CMB sound-horizon angle
    theta_* = r_s(z_cmb) / D_A(z_cmb) under the FIDUCIAL assumption of
    LambdaCDM (w = -1), while the TRUE cosmology has the local
    biogenic-DE w_local(z) for the delta_bio overdensity.

    Methodology: at fixed theta_* and fixed r_s (both CMB-anchored),
    D_A(z_cmb) is fixed. If true cosmology gives D_A_true(z_cmb) different
    from LambdaCDM-fiducial D_A_fid(z_cmb; H_0), the Planck inference
    adjusts H_0 to compensate. To leading order:
        H_0_Planck_inferred / H_0_true = D_A_fid_LCDM(z_cmb) / D_A_true(z_cmb)
    where both D_A are evaluated at the same H_0_true and Omega_m.

    This captures the bias of the Planck inversion when the true DE
    departs from LambdaCDM.
    """
    # True D_A under biogenic-DE local cosmology
    z_int_max = z_cmb + 5.0
    z_fine = np.geomspace(1e-4, z_int_max, 2000)
    h_local_fine = hubble_local_of_z(
        z_fine, delta_bio, age_today_gyr, t_origin, tau_evolve
    )
    one_over_h = 1.0 / h_local_fine
    d_c_true = np.trapz(one_over_h[z_fine <= z_cmb], z_fine[z_fine <= z_cmb])

    # Fiducial D_A under LambdaCDM (w = -1) at the same H_0, Omega_m
    h_lcdm_fine = np.sqrt(OMEGA_M * (1.0 + z_fine) ** 3 + OMEGA_L)
    one_over_h_lcdm = 1.0 / h_lcdm_fine
    d_c_fid = np.trapz(
        one_over_h_lcdm[z_fine <= z_cmb], z_fine[z_fine <= z_cmb]
    )

    # H_0_inferred / H_0_true = d_c_fid / d_c_true
    # (because D_A = (1/(1+z_cmb)) * d_c, fixed theta_* * r_s fixes D_A,
    #  D_A_true * H_0_true = D_A_fid * H_0_Planck, so
    #  H_0_Planck / H_0_true = D_A_true / D_A_fid = d_c_true / d_c_fid)
    return d_c_true / d_c_fid


def run_o17(t_origin=9.0, tau_evolve=2.0):
    """Compute delta H_local / H_0 across the delta_bio anchor grid.

    Three inference channels are reported per anchor:
      (1) SH0ES linear cosmography
      (2) SH0ES kinematic cosmography (H_0, q_0, j_0)
      (3) Planck CMB inversion under LambdaCDM fiducial

    Channel (3) gives the size of the SH0ES-vs-Planck bias from
    GCT-biogenic phantom DE: if the true cosmology is biogenic-DE
    (cosmic mean) and Planck inverts under LambdaCDM, what H_0 does
    Planck recover relative to the true H_0?
    """
    _, age_today = age_at_z(np.array([0.0]))

    # Cosmic-mean baselines
    h0_shoes_lin_cosmic = shoes_inferred_h0(
        0.0, age_today, t_origin=t_origin, tau_evolve=tau_evolve,
        fit_order="linear"
    )
    h0_shoes_kin_cosmic = shoes_inferred_h0(
        0.0, age_today, t_origin=t_origin, tau_evolve=tau_evolve,
        fit_order="kinematic"
    )
    h0_planck_cosmic = planck_inferred_h0(
        0.0, age_today, t_origin=t_origin, tau_evolve=tau_evolve
    )
    # The implied SH0ES-Planck bias from cosmic-mean biogenic DE alone
    shoes_planck_bias_cosmic = h0_shoes_kin_cosmic - h0_planck_cosmic

    results_by_anchor = {}
    for name, delta_bio in DELTA_BIO_ANCHORS.items():
        h0_shoes_lin = shoes_inferred_h0(
            delta_bio, age_today, t_origin=t_origin, tau_evolve=tau_evolve,
            fit_order="linear"
        )
        h0_shoes_kin = shoes_inferred_h0(
            delta_bio, age_today, t_origin=t_origin, tau_evolve=tau_evolve,
            fit_order="kinematic"
        )
        z_eval = np.array([0.0, 0.075, 0.5, 1.0])
        w_local_pts = w_local_of_z(z_eval, delta_bio, age_today,
                                    t_origin, tau_evolve)
        results_by_anchor[name] = {
            "delta_bio": delta_bio,
            "H0_SH0ES_linear_over_H0_global": h0_shoes_lin,
            "H0_SH0ES_kinematic_over_H0_global": h0_shoes_kin,
            "delta_H_local_linear_percent": 100.0 * (h0_shoes_lin - h0_shoes_lin_cosmic),
            "delta_H_local_kinematic_percent": 100.0 * (h0_shoes_kin - h0_shoes_kin_cosmic),
            "fraction_of_tension_linear": (h0_shoes_lin - h0_shoes_lin_cosmic) / TENSION_FRACTIONAL,
            "fraction_of_tension_kinematic": (h0_shoes_kin - h0_shoes_kin_cosmic) / TENSION_FRACTIONAL,
            "w_local_z0": float(w_local_pts[0]),
            "w_local_z_075": float(w_local_pts[1]),
            "w_local_z_05": float(w_local_pts[2]),
            "w_local_z_10": float(w_local_pts[3]),
        }

    return {
        "age_today_gyr": float(age_today),
        "t_origin_gyr": t_origin,
        "tau_evolve_gyr": tau_evolve,
        "tau_lag_gyr": TAU_LAG_GYR,
        "tau_bio_gyr": TAU_BIO_GYR,
        "lambda_bio": ALPHA,
        "delta_w_cosmic_z0": DELTA_W_TARGET,
        "H0_SH0ES_obs": H0_SH0ES_OBS,
        "H0_Planck_obs": H0_PLANCK_OBS,
        "observed_tension_fractional": TENSION_FRACTIONAL,
        "H0_SH0ES_linear_cosmic_over_global": h0_shoes_lin_cosmic,
        "H0_SH0ES_kinematic_cosmic_over_global": h0_shoes_kin_cosmic,
        "H0_Planck_inferred_cosmic_over_global": h0_planck_cosmic,
        "implied_SH0ES_minus_Planck_bias_cosmic": shoes_planck_bias_cosmic,
        "implied_SH0ES_minus_Planck_bias_fraction_of_tension": shoes_planck_bias_cosmic / TENSION_FRACTIONAL,
        "anchors": results_by_anchor,
    }


def verdict(results):
    """Determine the closure direction for O.17.

    Two channels for SH0ES inference:
      - linear-cosmography: artifact-prone, sensitive to higher-order corrections
      - kinematic-cosmography: closer to Riess+ 2022 actual methodology
    Plus an independent Planck-bias channel from the cosmic-mean phantom DE.
    """
    anchors = results["anchors"]

    # Channel 1: local-vs-cosmic SH0ES kinematic shift at realistic overdensity
    realistic_keys = ["local_sheet", "laniakea"]
    realistic_fracs_kin = [
        anchors[k]["fraction_of_tension_kinematic"] for k in realistic_keys
    ]
    realistic_fracs_lin = [
        anchors[k]["fraction_of_tension_linear"] for k in realistic_keys
    ]
    filament_frac_kin = anchors["filament"]["fraction_of_tension_kinematic"]

    # Channel 2: cosmic-mean Planck-bias contribution to SH0ES-Planck tension
    planck_bias_frac = results["implied_SH0ES_minus_Planck_bias_fraction_of_tension"]

    abs_kin_max = max(abs(f) for f in realistic_fracs_kin + [filament_frac_kin])
    abs_planck = abs(planck_bias_frac)
    total_explained_upper_bound = abs_kin_max + abs_planck

    sign_consistent_local = bool(all(f > 0 for f in realistic_fracs_kin))
    sign_consistent_planck = bool(planck_bias_frac > 0)

    if total_explained_upper_bound >= 0.5:
        direction = "(i) PROMOTE to Tier 2 prediction"
        framing = (
            f"Combined upper-bound contribution from local-cosmography "
            f"({100.0 * abs_kin_max:.2f}% of H_0) and Planck-bias "
            f"({100.0 * abs_planck:.2f}% of H_0) channels accounts for "
            f"{100.0 * total_explained_upper_bound:.1f}% of the observed "
            f"~{100.0 * results['observed_tension_fractional']:.1f}% Hubble "
            f"tension at realistic delta_bio. Promote V2 Ch14 Sec 14.5.4 from "
            f"Tier 3 consistency to Tier 2 prediction with this magnitude as "
            f"the derived bound."
        )
    else:
        sign_note = ""
        if not sign_consistent_local:
            sign_note += (" Local-cosmography channel has WRONG sign relative "
                          "to the SH0ES > Planck tension framing.")
        if not sign_consistent_planck:
            sign_note += (" Planck-bias channel has WRONG sign relative to "
                          "the SH0ES > Planck tension framing.")
        if sign_consistent_local and sign_consistent_planck:
            sign_note += " Both channels are sign-consistent with the tension."

        direction = "Biogenic-driving action does not account for the Hubble tension"
        framing = (
            f"At realistic SH0ES-volume-average overdensity (delta_bio ~ 1-3), "
            f"the local-cosmography channel of biogenic-DE shifts the SH0ES "
            f"inferred H_0 by "
            f"[{anchors['local_sheet']['delta_H_local_kinematic_percent']:+.4f}%, "
            f"{anchors['laniakea']['delta_H_local_kinematic_percent']:+.4f}%] "
            f"of H_0 (kinematic-fit channel); the Planck-bias channel "
            f"contributes {100.0 * planck_bias_frac:+.2f}% of the observed "
            f"tension. Combined upper bound is at most "
            f"{100.0 * total_explained_upper_bound:.2f}% of the observed "
            f"~{100.0 * results['observed_tension_fractional']:.1f}% tension."
            f"{sign_note} The Hubble tension is not among the framework's "
            f"predictions; this diagnostic is a quantitative non-closure "
            f"bound for the local biogenic-DE channel."
        )

    return {
        "direction": direction,
        "framing": framing,
        "channels": {
            "local_cosmography_kinematic": {
                "realistic_overdensity_range_fraction": [float(min(realistic_fracs_kin)),
                                                          float(max(realistic_fracs_kin))],
                "filament_extreme_fraction": float(filament_frac_kin),
                "sign_consistent_with_tension": sign_consistent_local,
            },
            "local_cosmography_linear": {
                "realistic_overdensity_range_fraction": [float(min(realistic_fracs_lin)),
                                                          float(max(realistic_fracs_lin))],
            },
            "planck_bias_cosmic_mean": {
                "fraction_of_tension": float(planck_bias_frac),
                "sign_consistent_with_tension": sign_consistent_planck,
            },
        },
        "total_explained_upper_bound": float(total_explained_upper_bound),
    }


def main():
    print("=" * 72)
    print("O.17 PROTOCOL: delta H_local from GCT biogenic-driving action")
    print("=" * 72)

    results = run_o17(t_origin=9.0, tau_evolve=2.0)

    print(f"\nCosmic-mean baselines:")
    print(f"  Age of universe today                       : {results['age_today_gyr']:.3f} Gyr")
    print(f"  delta_w_cosmic(z=0)                         : {results['delta_w_cosmic_z0']:+.4f}")
    print(f"  H_0_SH0ES_linear  / H_0_global              : {results['H0_SH0ES_linear_cosmic_over_global']:.6f}")
    print(f"  H_0_SH0ES_kinematic / H_0_global            : {results['H0_SH0ES_kinematic_cosmic_over_global']:.6f}")
    print(f"  H_0_Planck (LCDM-fid inversion) / H_0_global: {results['H0_Planck_inferred_cosmic_over_global']:.6f}")
    print(f"  Implied SH0ES-Planck bias (cosmic-mean)     : {100.0 * results['implied_SH0ES_minus_Planck_bias_cosmic']:+.4f}% of H_0")
    print(f"  Fraction of observed tension                : {100.0 * results['implied_SH0ES_minus_Planck_bias_fraction_of_tension']:+.2f}%")
    print(f"  Observed SH0ES-Planck tension               : {100.0 * results['observed_tension_fractional']:.2f}%")

    print(f"\nLocal-cosmography channel (KINEMATIC fit) by overdensity anchor:")
    print(f"  {'Anchor':<16} {'delta_bio':>10} {'delta_H/H_0 [%]':>18} {'frac of tension':>18}")
    for name, data in results["anchors"].items():
        print(f"  {name:<16} {data['delta_bio']:>+10.2f} "
              f"{data['delta_H_local_kinematic_percent']:>+18.4f} "
              f"{100.0 * data['fraction_of_tension_kinematic']:>+17.2f}%")

    print(f"\nLocal-cosmography channel (LINEAR fit; cosmography artifact) by anchor:")
    print(f"  {'Anchor':<16} {'delta_bio':>10} {'delta_H/H_0 [%]':>18} {'frac of tension':>18}")
    for name, data in results["anchors"].items():
        print(f"  {name:<16} {data['delta_bio']:>+10.2f} "
              f"{data['delta_H_local_linear_percent']:>+18.4f} "
              f"{100.0 * data['fraction_of_tension_linear']:>+17.2f}%")

    v = verdict(results)
    print(f"\nVerdict for O.17:")
    print(f"  Direction : {v['direction']}")
    print(f"  Total explained upper bound: {100.0 * v['total_explained_upper_bound']:.2f}% of tension")
    print(f"  Framing   : {v['framing']}")

    output = {"results": results, "verdict": v}
    if OUTPUT_DIR_AVAILABLE:
        out_path = get_output_path("protocol_o17_delta_h_local_results.json")
    else:
        out_path = Path(__file__).resolve().parent.parent / "data" / "protocol_o17_delta_h_local_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nFull results written to {out_path}")
    print("=" * 72)

    return output


if __name__ == "__main__":
    main()
