#!/usr/bin/env python3
"""
protocol_de_multichannel.py
============================

DIAGNOSTIC: registered-menu no-go over convex-combination SHAPE PROXIES,
NOT physical density-weighted multi-fluid cosmology and NOT a DESI covariance
likelihood. Physical rho_c(z) evolution + likelihood comparison is pending
O.13 channel-C2. Omega_bio (Madau-Dickinson SFR proxy), Omega_chiral (tanh
step), and Omega_pert (constant amplitude) are shape proxies, not
energy-density evolutions through the continuity equations.

Multi-channel dark-energy shape-proxy partition diagnostic.

Audits Ch14 §14.6.3 by computing the diagnostic total dark-energy
shape-proxy equation-of-state

    w_total(z) = sum_c Omega_c(z) w_c(z) / sum_c Omega_c(z)

(Copeland-Sami-Tsujikawa 2006, Amendola-Tsujikawa 2010) over the
five-channel decomposition registered in Ch14 §14.6.3:

    c in {
        Lambda-baseline,                    # frozen-phason VEV
        biogenic-terrestrial,               # protocol_imp01_pipeline.py channel
        biogenic-non-terrestrial,           # extragalactic biogenic channel
        abiotic-chiral,                     # early-universe chirality onset
        frozen-phason perturbation,         # weak quintessence-like channel
    }.

Channel-fraction parametrizations (per-channel shape proxy Omega_c(z)):

    Lambda-baseline:
        Omega_Lambda(z) = Omega_Lambda_0
        w_Lambda(z)     = -1 exact
        Omega_Lambda_0 is swept across a defensible cosmological range
        (see grid below) so that the closure verdict carries no implicit
        dependence on any single imported value of the dark-energy
        density fraction.
        [Tier 2 mechanism (frozen phason VEV), Tier 1 amplitude (Planck
        central value 0.685 anchors the canonical point of the sweep)]

    biogenic-terrestrial:
        Omega_bio,terr(z) ~ psi_SFR(z) (Madau-Dickinson 2014 ARA&A 52:415)
            psi_SFR(z) = 0.015 * (1+z)^2.7 / (1 + ((1+z)/2.9)^5.6)
        normalised so today's contribution matches the biogenic DE pipeline:
            today contribution -> delta_w today ~ -0.005
        w_bio,terr(z) = w_0_bio + w_a_bio * z/(1+z)
            with (w_0_bio, w_a_bio) = (-1.0037973296449392, +0.013560610917121069)
            (biogenic DE pipeline CPL output, Ch14 §14.6.3 headline)
        [Tier 2 mechanism + Tier 3 amplitude from biogenic DE pipeline calibration]

    biogenic-non-terrestrial:
        Omega_bio,ext(z) = f_ext * Omega_bio,terr(z)
        w_bio,ext(z)     = -1.01 + 0.05 * z/(1+z)
        f_ext in [0, 100] (extragalactic-vs-terrestrial amplitude ratio)
        [Tier 3 calibrated structure — extragalactic life-prevalence prior]

    abiotic-chiral:
        Omega_chiral(z) = f_chiral * 0.5 * (1 + tanh((z - z_chiral)/width_chiral))
            with z_chiral in [5, 20], width_chiral = 2
        w_chiral(z) = -1.5 exact (phantom early-universe contribution)
        f_chiral in [0, 0.5]
        [Tier 3 calibrated structure — chirality-onset model]

    frozen-phason perturbation:
        Omega_pert(z) = f_pert constant
        w_pert(z)     = -0.9 (weak quintessence-like)
        f_pert in [0, 0.05]
        [Tier 3 calibrated structure]

Sensitivity grid
----------------
    Omega_Lambda_0 in {0.50, 0.55, 0.60, 0.65, 0.685, 0.72, 0.75}  (7)
    f_ext          in {0.0, 0.01, 0.1, 1.0, 10.0, 100.0}           (6)
    f_chiral       in {0.0, 0.02, 0.05, 0.10, 0.20, 0.40}          (6)
    f_pert         in {0.0, 0.01, 0.02, 0.05}                      (4)
    z_chiral       in {5.0, 10.0, 15.0, 20.0}                      (4)
    total = 7 * 6 * 6 * 4 * 4 = 4032 parameter combinations

For each combination the protocol fits the CPL form

    w(z) = w_0 + w_a * z/(1+z)

to w_total(z) over z in [0, 1.5] (the DESI BAO comparison range) and computes
a diagonal marginal-distance diagnostic against the DES-Dovekie recalibrated
DESI DR2 + CMB reference triple:

    w_0_DESI = -0.803 +/- 0.054
    w_a_DESI = -0.72  +/- 0.21
    joint dynamical-DE significance = 3.2 sigma under the
    DES-Dovekie recalibrated comparison
    (DES-Dovekie recalibration, arXiv:2511.07517, CPL parametrization,
    DESI DR2 BAO + CMB + DES-Dovekie joint fit).

    sigma_w0     = (w_0_GCT - w_0_DESI) / err_w_0
    sigma_wa     = (w_a_GCT - w_a_DESI) / err_w_a
    joint_marginal_distance_diagnostic = sqrt(sigma_w0^2 + sigma_wa^2)

This scalar is diagnostic only. It uses DESI marginal errors without the DESI
covariance matrix or likelihood surface and must not be read as a closure
threshold, model likelihood, evidence ratio, or P.6 numerical likelihood test.

Structural ceiling
------------------
The shape-proxy total is a convex combination of the per-channel
equation-of-state values: at every redshift,

    min_c w_c(z)  <=  w_total(z)  <=  max_c w_c(z),

with the bounds independent of the channel-fraction parameters
(Omega_Lambda_0, f_ext, f_chiral, f_pert, z_chiral). Every channel in
the registered decomposition carries w_c(z) <= -0.9 across the fit
window (the frozen-phason perturbation channel at w_pert = -0.9 is the
least-negative channel; the biogenic and chiral channels are more
negative). Hence

    w_total(z)  <=  -0.9   for all z in [0, 1.5]   and all sweep points.

The DES-Dovekie recalibrated central value w_0 = -0.803 lies *above* this ceiling.
The multi-channel shape-proxy partition therefore cannot reproduce the DESI w_0
for any choice of channel fractions: the registered-menu no-go is a
structural property of the decomposition, not an artefact of any
particular imported Omega_Lambda_0.

Registered-menu no-go verdict:

    The diagonal diagnostic ranks sweep points but does not define a
    scalar-score closure rule. The registered-menu verdict is determined by
    the convex-combination ceiling: if the DES-Dovekie CPL target sits outside
    the reachable channel envelope, the registered five-channel menu fails.
    Any positive reconciliation requires a GCT-native likelihood using the
    DESI covariance surface or a new O.13 channel-menu closure path.

Tier discipline
---------------
The convex-combination EoS identity (Copeland-Sami-Tsujikawa 2006)
is Tier 2 as an algebraic mixture rule, but this protocol's per-channel
Omega_c(z) inputs are Tier 3 shape proxies, not continuity-equation
energy-density evolutions. The per-channel amplitudes (f_ext, f_chiral, f_pert), the
chirality-onset epoch z_chiral, and the dark-energy density fraction
Omega_Lambda_0 are swept across defensible ranges, so the verdict
inherits no conditional dependence on a single imported value.
"""

import json
import math
import numpy as np
from pathlib import Path
from scipy.optimize import curve_fit

try:
    from gct_utils import get_output_path
    OUTPUT_DIR_AVAILABLE = True
except ImportError:
    OUTPUT_DIR_AVAILABLE = False


# ---------------------------------------------------------------------------
# Cosmological / DESI comparison inputs
# ---------------------------------------------------------------------------

# External empirical prior: Planck 2018 central value for the canonical sweep point.
OMEGA_LAMBDA_0 = 0.685

# DESI CPL diagnostic target retained for the multichannel stress test.
# Verification target / external empirical prior: DES-Dovekie recalibrated CPL central values
# and 1-sigma uncertainties; these are not GCT fit parameters and are not
# selected by this protocol.
DESI_DR2_CPL_TARGET = {
    "w0": -0.803,
    "wa": -0.72,
    "err_w0": 0.054,
    "err_wa": 0.21,
    "joint_significance_sigma": 3.2,
    "des_sn5yr_significance_sigma": 4.2,
    "source": "DESI DR2 BAO + CMB + DES-Dovekie recalibrated CPL diagnostic target (arXiv:2511.07517)",
    "role": "external diagnostic target, not selected for fit",
}
W0_DESI       = DESI_DR2_CPL_TARGET["w0"]
WA_DESI       = DESI_DR2_CPL_TARGET["wa"]
ERR_W0_DESI   = DESI_DR2_CPL_TARGET["err_w0"]
ERR_WA_DESI   = DESI_DR2_CPL_TARGET["err_wa"]

# Biogenic DE single-channel CPL output (Ch14 §14.6.3 headline; protocol_imp01_pipeline.py)
# Tier 3 calibrated anchor [Ledger C-sector]: imported single-channel
# biogenic-DE diagnostic output, not adjusted inside this multichannel stress test.
W0_BIO_TERR   = -1.0037973296449392
WA_BIO_TERR   = +0.013560610917121069

# Extragalactic biogenic channel (stronger phantom)
# Tier 3 calibrated channel-menu value [App H O.13]: stress-test shape.
W0_BIO_EXT    = -1.01
WA_BIO_EXT    = +0.05

# Abiotic-chiral phantom early-universe channel
# Tier 3 calibrated channel-menu value [App H O.13]: stress-test shape.
W_CHIRAL      = -1.5
WIDTH_CHIRAL  = 2.0

# Frozen-phason perturbation channel
# Tier 3 calibrated channel-menu value [App H O.13]: stress-test shape.
W_PERT        = -0.9

# DESI fit window
# Verification target: CPL fit interval used for the DESI-comparison projection.
Z_FIT_MIN     = 0.0
Z_FIT_MAX     = 1.5
N_Z_GRID      = 200

# Tier 3 calibrated anchor [Ledger C-sector]: density-partition amplitude used
# for the channel-mixture stress test; it is not normalized to force agreement.
# Biogenic-DE partition amplitude. A_BIO is a small dimensionless density
# weight assigned to the terrestrial biogenic channel at z = 0 for the
# multi-channel stress test. It is not normalized to reproduce the
# single-channel headline delta_w = -0.005 by itself; once the density
# partition denominator is included, the run asks whether any allowed
# channel mixture can approach the DESI CPL target. The answer is the
# reported registered-menu no-go, not a hidden normalization success.
A_BIO         = 0.01          # biogenic-terrestrial amplitude at z=0


# ---------------------------------------------------------------------------
# Per-channel density fractions and equation-of-state shapes
# ---------------------------------------------------------------------------

def sfr_madau_dickinson(z):
    """psi(z) per Madau & Dickinson 2014 ARA&A 52:415 eq. 15.

    psi_SFR(z) = 0.015 * (1+z)^2.7 / (1 + ((1+z)/2.9)^5.6)
    [M_sun yr^-1 Mpc^-3]; only the z-dependence enters the shape-proxy
    partition (the absolute units cancel in the convex-combination ratio).
    """
    # External empirical prior: Madau-Dickinson SFR shape. The absolute
    # normalization cancels in the shape-proxy partition.
    return 0.015 * (1.0 + z) ** 2.7 / (1.0 + ((1.0 + z) / 2.9) ** 5.6)


def omega_lambda(z, omega_lambda_0):
    """Frozen-phason VEV channel — constant Omega_Lambda,0 contribution."""
    return np.full_like(z, omega_lambda_0, dtype=float)


def omega_bio_terr(z):
    """Biogenic-terrestrial channel — tracks Madau-Dickinson SFR shape,
    normalised so the z=0 amplitude is A_BIO.
    """
    psi = sfr_madau_dickinson(z)
    psi_0 = sfr_madau_dickinson(np.array([0.0]))[0]
    return A_BIO * psi / psi_0


def omega_bio_ext(z, f_ext):
    """Biogenic-non-terrestrial channel — f_ext times the terrestrial shape."""
    return f_ext * omega_bio_terr(z)


def omega_chiral(z, f_chiral, z_chiral):
    """Abiotic-chiral channel — tanh step onset at z = z_chiral."""
    return f_chiral * 0.5 * (1.0 + np.tanh((z - z_chiral) / WIDTH_CHIRAL))


def omega_pert(z, f_pert):
    """Frozen-phason perturbation channel — constant amplitude."""
    return np.full_like(z, f_pert, dtype=float)


def w_lambda(z):
    """w_Lambda(z) = -1 exact."""
    return np.full_like(z, -1.0, dtype=float)


def w_bio_terr(z):
    """w_bio,terr(z) = w_0 + w_a * z/(1+z) per biogenic DE pipeline CPL output."""
    return W0_BIO_TERR + WA_BIO_TERR * z / (1.0 + z)


def w_bio_ext(z):
    """w_bio,ext(z) = w_0 + w_a * z/(1+z) for the extragalactic channel."""
    return W0_BIO_EXT + WA_BIO_EXT * z / (1.0 + z)


def w_chiral(z):
    """w_chiral(z) = -1.5 exact (phantom early-universe)."""
    return np.full_like(z, W_CHIRAL, dtype=float)


def w_pert(z):
    """w_pert(z) = -0.9 (weak quintessence-like perturbation)."""
    return np.full_like(z, W_PERT, dtype=float)


# ---------------------------------------------------------------------------
# Multi-channel shape-proxy total
# ---------------------------------------------------------------------------

def w_total_multichannel(z, omega_lambda_0, f_ext, f_chiral, f_pert, z_chiral):
    """Shape-proxy total w(z) over the five channels.

    w_total(z) = sum_c Omega_c(z) w_c(z) / sum_c Omega_c(z)
    """
    z = np.asarray(z, dtype=float)

    o_lam  = omega_lambda(z, omega_lambda_0)
    o_bt   = omega_bio_terr(z)
    o_bx   = omega_bio_ext(z, f_ext)
    o_ch   = omega_chiral(z, f_chiral, z_chiral)
    o_pe   = omega_pert(z, f_pert)

    w_lam  = w_lambda(z)
    w_bt   = w_bio_terr(z)
    w_bx   = w_bio_ext(z)
    w_ch   = w_chiral(z)
    w_pe   = w_pert(z)

    num = o_lam * w_lam + o_bt * w_bt + o_bx * w_bx + o_ch * w_ch + o_pe * w_pe
    den = o_lam + o_bt + o_bx + o_ch + o_pe

    return num / den


def channel_w_ceiling(z):
    """Pointwise maximum (least-negative) per-channel w_c(z).

    The shape-proxy total is a convex combination of the per-channel
    w_c, so w_total(z) <= channel_w_ceiling(z) for every choice of channel
    fractions. Returns the array max_c w_c(z) over the five channels.
    """
    z = np.asarray(z, dtype=float)
    stack = np.vstack([
        w_lambda(z),
        w_bio_terr(z),
        w_bio_ext(z),
        w_chiral(z),
        w_pert(z),
    ])
    return np.max(stack, axis=0)


def channel_w_floor(z):
    """Pointwise minimum (most-negative) per-channel w_c(z).

    Companion to channel_w_ceiling: w_total(z) >= channel_w_floor(z) for
    every choice of channel fractions.
    """
    z = np.asarray(z, dtype=float)
    stack = np.vstack([
        w_lambda(z),
        w_bio_terr(z),
        w_bio_ext(z),
        w_chiral(z),
        w_pert(z),
    ])
    return np.min(stack, axis=0)


# ---------------------------------------------------------------------------
# CPL fit
# ---------------------------------------------------------------------------

def cpl_form(z, w0, wa):
    """w(z) = w_0 + w_a * z / (1 + z)."""
    return w0 + wa * z / (1.0 + z)


def cpl_fit(z_grid, w_grid):
    """Fit w(z) = w_0 + w_a * z/(1+z) over the supplied (z, w) grid."""
    popt, _ = curve_fit(cpl_form, z_grid, w_grid, p0=[-1.0, 0.0])
    return float(popt[0]), float(popt[1])


# ---------------------------------------------------------------------------
# Sensitivity sweep
# ---------------------------------------------------------------------------

# External empirical prior / sensitivity grid: spans plausible Planck/DESI
# and channel-partition ranges; no grid point is selected to fit the result.
OMEGA_LAMBDA_GRID = [0.50, 0.55, 0.60, 0.65, 0.685, 0.72, 0.75]
F_EXT_GRID        = [0.0, 0.01, 0.1, 1.0, 10.0, 100.0]
F_CHIRAL_GRID     = [0.0, 0.02, 0.05, 0.10, 0.20, 0.40]
F_PERT_GRID       = [0.0, 0.01, 0.02, 0.05]
Z_CHIRAL_GRID     = [5.0, 10.0, 15.0, 20.0]


def sigma_against_desi(w0_gct, wa_gct):
    """Diagonal diagnostic score against the DESI CPL reference.

    This intentionally ignores the DESI (w0, wa) covariance and is therefore
    not a likelihood distance. The structural ceiling argument carries the
    closure result; this score only ranks the sweep grid.
    """
    s_w0 = (w0_gct - W0_DESI) / ERR_W0_DESI
    s_wa = (wa_gct - WA_DESI) / ERR_WA_DESI
    return s_w0, s_wa, math.sqrt(s_w0 ** 2 + s_wa ** 2)


def run_sweep():
    """Sweep over (Omega_Lambda_0, f_ext, f_chiral, f_pert, z_chiral)."""
    z_grid = np.linspace(Z_FIT_MIN, Z_FIT_MAX, N_Z_GRID)
    rows = []

    for omega_l in OMEGA_LAMBDA_GRID:
        for f_ext in F_EXT_GRID:
            for f_chiral in F_CHIRAL_GRID:
                for f_pert in F_PERT_GRID:
                    for z_chiral in Z_CHIRAL_GRID:
                        w_grid = w_total_multichannel(
                            z_grid, omega_l, f_ext, f_chiral, f_pert, z_chiral
                        )
                        w0_fit, wa_fit = cpl_fit(z_grid, w_grid)
                        s_w0, s_wa, joint = sigma_against_desi(w0_fit, wa_fit)
                        rows.append({
                            "omega_lambda": omega_l,
                            "f_ext":        f_ext,
                            "f_chiral":     f_chiral,
                            "f_pert":       f_pert,
                            "z_chiral":     z_chiral,
                            "w0_GCT":       w0_fit,
                            "wa_GCT":       wa_fit,
                            "sigma_w0":     s_w0,
                            "sigma_wa":     s_wa,
                            "joint_marginal_distance_diagnostic":  joint,
                        })

    return rows


def select_best(rows):
    """Return the sweep row with the smallest diagonal diagnostic."""
    return min(rows, key=lambda r: r["joint_marginal_distance_diagnostic"])


def best_per_omega_lambda(rows):
    """Best diagonal diagnostic at each swept Omega_Lambda_0 value.

    A flat profile across this dimension demonstrates that the closure
    verdict carries no conditional dependence on the dark-energy density
    fraction.
    """
    out = []
    for omega_l in OMEGA_LAMBDA_GRID:
        subset = [r for r in rows if r["omega_lambda"] == omega_l]
        best = min(subset, key=lambda r: r["joint_marginal_distance_diagnostic"])
        out.append({
            "omega_lambda":     omega_l,
            "best_joint_marginal_distance_diagnostic": best["joint_marginal_distance_diagnostic"],
            "best_w0_GCT":      best["w0_GCT"],
            "best_wa_GCT":      best["wa_GCT"],
        })
    return out


def envelope(rows):
    """Range of (w0, wa) achievable across the full sweep."""
    w0s = [r["w0_GCT"] for r in rows]
    was = [r["wa_GCT"] for r in rows]
    js  = [r["joint_marginal_distance_diagnostic"] for r in rows]
    return {
        "w0_min": float(min(w0s)),
        "w0_max": float(max(w0s)),
        "wa_min": float(min(was)),
        "wa_max": float(max(was)),
        "joint_marginal_distance_diagnostic_min": float(min(js)),
        "joint_marginal_distance_diagnostic_max": float(max(js)),
    }


def structural_ceiling_report():
    """Compute the parameter-independent convex-combination bounds.

    Returns the least-negative achievable w_total over the fit window
    (the channel-w ceiling) and the DESI w_0 gap above it.
    """
    z_grid = np.linspace(Z_FIT_MIN, Z_FIT_MAX, N_Z_GRID)
    ceil_arr = channel_w_ceiling(z_grid)
    floor_arr = channel_w_floor(z_grid)
    w_ceiling = float(np.max(ceil_arr))   # least-negative w_total reachable anywhere
    w_floor   = float(np.min(floor_arr))  # most-negative w_total reachable anywhere
    return {
        "w_total_ceiling": w_ceiling,
        "w_total_floor":   w_floor,
        "desi_w0":         W0_DESI,
        "desi_w0_above_ceiling": bool(W0_DESI > w_ceiling),
        "desi_w0_gap_above_ceiling": float(W0_DESI - w_ceiling),
        "desi_w0_min_sigma_at_ceiling": float((w_ceiling - W0_DESI) / ERR_W0_DESI),
        "note": (
            "w_total(z) is a convex combination of the per-channel w_c(z); "
            "it cannot exceed max_c w_c(z) for any channel-fraction choice. "
            "The DES-Dovekie recalibrated central w_0 lies above this ceiling, so the "
            "registered five-channel partition cannot reproduce it for any "
            "Omega_Lambda_0 or any other swept parameter unless an O.13 "
            "channel-menu closure path adds a channel above the ceiling."
        ),
    }


def closure_verdict(ceiling_report):
    """Classify the registered-menu verdict without treating the diagnostic as a likelihood."""
    if ceiling_report["desi_w0_above_ceiling"]:
        return "CLOSURE-FAILS"
    return "DIAGNOSTIC_ONLY_NATIVE_LIKELIHOOD_REQUIRED"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 72)
    print("Multi-channel dark-energy shape-proxy partition diagnostic")
    print("=" * 72)
    print(f"DES-Dovekie target: w_0 = {W0_DESI:+.3f} +/- {ERR_W0_DESI:.3f}, "
          f"w_a = {WA_DESI:+.3f} +/- {ERR_WA_DESI:.3f}, "
          f"joint significance = {DESI_DR2_CPL_TARGET['joint_significance_sigma']:.1f} sigma")
    print(f"Sweep grid sizes : omega_lambda={len(OMEGA_LAMBDA_GRID)}, "
          f"f_ext={len(F_EXT_GRID)}, "
          f"f_chiral={len(F_CHIRAL_GRID)}, "
          f"f_pert={len(F_PERT_GRID)}, "
          f"z_chiral={len(Z_CHIRAL_GRID)}")
    n_total = (len(OMEGA_LAMBDA_GRID) * len(F_EXT_GRID) * len(F_CHIRAL_GRID)
               * len(F_PERT_GRID) * len(Z_CHIRAL_GRID))
    print(f"Total combinations: {n_total}")
    print()

    rows = run_sweep()
    best = select_best(rows)
    env  = envelope(rows)
    per_omega = best_per_omega_lambda(rows)
    ceiling = structural_ceiling_report()
    verdict = closure_verdict(ceiling)

    print("Best-fit point")
    print("-" * 72)
    print(f"  omega_lambda : {best['omega_lambda']}")
    print(f"  f_ext        : {best['f_ext']}")
    print(f"  f_chiral     : {best['f_chiral']}")
    print(f"  f_pert       : {best['f_pert']}")
    print(f"  z_chiral     : {best['z_chiral']}")
    print(f"  w_0_GCT      : {best['w0_GCT']:+.4f}")
    print(f"  w_a_GCT      : {best['wa_GCT']:+.4f}")
    print(f"  sigma_w0     : {best['sigma_w0']:+.3f}")
    print(f"  sigma_wa     : {best['sigma_wa']:+.3f}")
    print(f"  joint marginal-distance diagnostic : "
          f"{best['joint_marginal_distance_diagnostic']:.3f}")
    print()

    print("Best diagonal diagnostic per Omega_Lambda_0")
    print("-" * 72)
    for entry in per_omega:
        print(f"  Omega_Lambda = {entry['omega_lambda']:.3f}  ->  "
              f"best diagnostic = {entry['best_joint_marginal_distance_diagnostic']:.3f}  "
              f"(w_0 = {entry['best_w0_GCT']:+.4f}, "
              f"w_a = {entry['best_wa_GCT']:+.4f})")
    print()

    print("Structural ceiling (parameter-independent convex-combination bound)")
    print("-" * 72)
    print(f"  w_total ceiling (least-negative reachable) : "
          f"{ceiling['w_total_ceiling']:+.4f}")
    print(f"  w_total floor   (most-negative reachable)  : "
          f"{ceiling['w_total_floor']:+.4f}")
    print(f"  DESI w_0                                   : "
          f"{ceiling['desi_w0']:+.4f}")
    print(f"  DESI w_0 above ceiling                     : "
          f"{ceiling['desi_w0_above_ceiling']}")
    print(f"  minimum |sigma_w0| even at the ceiling     : "
          f"{abs(ceiling['desi_w0_min_sigma_at_ceiling']):.3f}")
    print()

    print("Sweep envelope")
    print("-" * 72)
    print(f"  w_0 range          : [{env['w0_min']:+.4f}, {env['w0_max']:+.4f}]")
    print(f"  w_a range          : [{env['wa_min']:+.4f}, {env['wa_max']:+.4f}]")
    print(f"  diagnostic range   : "
          f"[{env['joint_marginal_distance_diagnostic_min']:.3f}, "
          f"{env['joint_marginal_distance_diagnostic_max']:.3f}]")
    print()

    print(f"Registered-menu no-go verdict: {verdict}")
    omega_independent = (
        max(e["best_joint_marginal_distance_diagnostic"] for e in per_omega)
        - min(e["best_joint_marginal_distance_diagnostic"] for e in per_omega)
    )
    print(f"Diagnostic spread across Omega_Lambda_0 grid: {omega_independent:.3f} score units")
    print()

    output = {
        "scope": (
            "Registered-menu no-go over convex-combination shape proxies. "
            "This output is not a physical density-weighted multi-fluid "
            "background calculation and not a covariance-aware DESI likelihood."
        ),
        "desi_target": {
            **DESI_DR2_CPL_TARGET,
            "diagnostic_score_scope": "Diagnostic diagonal-error score only; DESI covariance is not included, so joint_marginal_distance_diagnostic is not a likelihood distance or closure threshold.",
        },
        "multichannel_eos_shape_proxy": {
            "lambda_baseline":      {"omega_swept": OMEGA_LAMBDA_GRID, "w": -1.0,
                                     "canonical_omega": OMEGA_LAMBDA_0,
                                     "source": "Frozen-phason VEV; Omega_Lambda_0 swept across a defensible cosmological range"},
            "biogenic_terrestrial": {"omega_z0": A_BIO,
                                     "w0": W0_BIO_TERR,
                                     "wa": WA_BIO_TERR,
                                     "source": "Madau-Dickinson 2014 SFR shape; biogenic DE pipeline CPL amplitude"},
            "biogenic_extra":       {"w0": W0_BIO_EXT,
                                     "wa": WA_BIO_EXT,
                                     "source": "Extragalactic biogenic channel, stronger phantom amplitude"},
            "abiotic_chiral":       {"w": W_CHIRAL,
                                     "width_chiral": WIDTH_CHIRAL,
                                     "source": "Tier 3 chirality-onset model"},
            "frozen_phason_pert":   {"w": W_PERT,
                                     "source": "Tier 3 weak quintessence-like perturbation"},
        },
        "channels": {
            "alias_of": "multichannel_eos_shape_proxy",
            "scope": "compatibility alias for consumers; not a physical multi-fluid density evolution",
        },
        "sweep_grids": {
            "omega_lambda": OMEGA_LAMBDA_GRID,
            "f_ext":        F_EXT_GRID,
            "f_chiral":     F_CHIRAL_GRID,
            "f_pert":       F_PERT_GRID,
            "z_chiral":     Z_CHIRAL_GRID,
        },
        "best_fit":               best,
        "best_per_omega_lambda":  per_omega,
        "structural_ceiling":     ceiling,
        "envelope":               env,
        "closure_verdict":        verdict,
        "omega_lambda_diagnostic_spread": omega_independent,
        "sweep":                  rows,
    }

    if OUTPUT_DIR_AVAILABLE:
        out_path = get_output_path("protocol_de_multichannel_results.json")
    else:
        out_path = Path(__file__).resolve().parent.parent / "data" / "protocol_de_multichannel_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Full results written to {out_path}")
    print("=" * 72)

    return output


if __name__ == "__main__":
    main()
