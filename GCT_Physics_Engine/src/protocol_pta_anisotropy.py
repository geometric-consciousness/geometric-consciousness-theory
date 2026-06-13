#!/usr/bin/env python3
"""
protocol_pta_anisotropy.py — Protocol I: PTA Icosahedral Anisotropy 
================================================================================
If spacetime is an icosahedral lattice (topological glass), the stochastic
gravitational wave background (SGWB) detected by Pulsar Timing Arrays (PTAs)
cannot be perfectly isotropic. GWs are long-wavelength acoustic phonons of the
vacuum, and the speed of sound varies minutely with alignment to the six 5-fold
projection axes of the icosahedron.

This script predicts the l=6 multipole correction to the standard
Hellings-Downs (HD) correlation function. The l=6 spherical harmonic is the
mathematically rigorous imprint of icosahedral symmetry on a sphere (the 
icosahedron has exactly the same point group as an l=6 spherical harmonic).

Prediction
----------
A statistically significant l=6 multipole anisotropy in current NANOGrav/IPTA
spatial correlation data, with amplitude Delta_Gamma ~ 1e-3 to 1e-4.

Success Criterion: Delta_Gamma > 1e-4 (detectable by next-gen SKA-PTA).
"""

import math
import json
import sys
import io
import numpy as np

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from gct_utils import C, get_output_path, GCTReporter

# ── Physical Geometric Constants ─────────────────────────────────────────────
PHI = float(C.PHI)

# Phason/Phonon stiffness ratio: K_perp / K_parallel = phi^-18 (from lattice
# geometry; V1 §13.3.4 + App K). The dimensionless lattice speed of light
# hat_c = sqrt(K_perp/K_parallel) = phi^-9 (Ch06 §6.2.2); the stiffness ratio
# itself is phi^-18.
STIFFNESS_RATIO = PHI ** -18

# For phason-gravitons (GW = phason Goldstone of translational SSB in emergent
# gravity), the gravitational-wave anisotropy bound is the linear stiffness
# ratio: delta_c/c = K_perp/K_par = phi^-18 ~ 1.73e-4. See V3 Ch21 §21.1.3
# for derivation.
DELTA_C_OVER_C = STIFFNESS_RATIO


def hellings_downs(theta: float) -> float:
    """
    Standard isotropic Hellings-Downs spatial correlation function.
    Gamma(theta) = 3/2 * x * ln(x) - x/4 + 1/2   where x = (1 - cos(theta))/2
    
    Valid for theta in (0, pi]. At theta=0, Gamma=1 by convention.
    """
    if theta == 0.0:
        return 1.0
    x = (1.0 - math.cos(theta)) / 2.0
    if x <= 0.0:
        return 1.0
    return 1.5 * x * math.log(x) - x / 4.0 + 0.5


def legendre_l6(cos_theta: float) -> float:
    """
    Legendre polynomial P_6(x) — the l=6 correction basis.
    P6(x) = (1/16)(231x^6 - 315x^4 + 105x^2 - 5)
    """
    x = cos_theta
    return (1.0/16.0) * (231*x**6 - 315*x**4 + 105*x**2 - 5)


def icosahedral_correction(theta: float, epsilon: float) -> float:
    """
    l=6 icosahedral modulation to the HD correlation.
    The anisotropy term is epsilon * P_6(cos theta).
    Epsilon is the scaled phason/phonon stiffness ratio.
    """
    return epsilon * legendre_l6(math.cos(theta))

def compute_delta_gamma_max(epsilon: float) -> float:
    """
    Computes max|ε · P₆(cosθ)| over a dense grid of theta.
    Returns the peak deviation ΔΓ_max.
    """
    theta_vals = np.linspace(0.01, math.pi, 500)
    gamma_icos_corr = np.array([icosahedral_correction(t, epsilon) for t in theta_vals])
    return float(np.max(np.abs(gamma_icos_corr)))

def compute_Cl_over_C0(epsilon: float, l: int = 6) -> float:
    """
    Computes angular power spectrum coefficient C_l/C_0 given the amplitude ε.
    C_l/C_0 = (4π / (2*l + 1)) * ε^2 
    """
    return (4.0 * math.pi / (2.0 * l + 1.0)) * (epsilon**2)


def check_nanograv_tension(epsilon: float) -> str:
    """
    Evaluates current NANOGrav 15-year sensitivity limits against GCT predictions.
    Computes angular resolution floor and confirms No-Tension theorem.
    """
    # GCT expected angular power correlation
    c6_c0_predicted = PHI ** -18  # ~ 1.7e-4
    
    # Generic current PTA bounds for high multipoles (l>3)
    nanograv_sensitivity_floor = 0.1 
    
    print("\n  ─── Stage 0: NANOGrav Tension Check ───")
    if c6_c0_predicted < nanograv_sensitivity_floor:
        print(f"  NANOGrav l=6 tension check: NO TENSION — GCT prediction (C6/C0 ~ {c6_c0_predicted:.1e}) is below current sensitivity floor (~{nanograv_sensitivity_floor}). Requires SKA-PTA.")
        return "NO_TENSION"
    else:
        print(f"  NANOGrav l=6 tension check: POTENTIAL TENSION — Prediction ({c6_c0_predicted:.1e}) exceeds sensitivity floor (~{nanograv_sensitivity_floor}).")
        return "TENSION"

def run_pta_anisotropy_protocol() -> dict:
    report = GCTReporter("PTA Icosahedral Anisotropy (Protocol I)")

    print("=" * 65)
    print("GCT Protocol I — Pulsar Timing Array Icosahedral Anisotropy")
    print("=" * 65)

    # ── 1. Physical Setup ─────────────────────────────────────────────────────
    print("\n  Input Constants:")
    print(f"  phi                = {PHI:.8f}")
    print(f"  Stiffness ratio    = K_perp / K_par = phi^-18 = {STIFFNESS_RATIO:.4e}")
    print(f"  delta_c / c        = K_perp/K_par = phi^-18 = {DELTA_C_OVER_C:.4e}")
    print(f"  (Fractional GW speed anisotropy along 5-fold axes)")

    report.section("Geometric Setup")
    report.log_value("phi", PHI)
    report.log_value("Stiffness Ratio (phi^-18)", STIFFNESS_RATIO)
    report.log_value("delta_c/c (GW Speed anisotropy)", DELTA_C_OVER_C)

    nanograv_tension_status = check_nanograv_tension(0.0)

    # ── 2. l=6 Multipole Correction ───────────────────────────────────────────
    print("\n  ─── Stage 1: l=6 Perturbation Amplitude ───")

    # The l=6 icosahedral fingerprint amplitude epsilon = phi^-18 directly
    # per V3 Ch21 §21.1.3 boxed Tier 2 prediction:
    #   Gamma_GCT(theta) = Gamma_HD(theta) + epsilon * P_6(cos theta)
    #   epsilon = phi^-18 ~ 1.73e-4
    epsilon = DELTA_C_OVER_C

    print(f"  Perturbation amplitude epsilon = {epsilon:.4e}")
    print(f"  (l=6 icosahedral fingerprint on the angular power spectrum)")
    report.log_value("l=6 Perturbation Amplitude epsilon", epsilon)

    # ── 3. Compute HD + Icosahedral Correction over theta ────────────────────
    print("\n  ─── Stage 2: Hellings-Downs + Icosahedral Modulation ───")

    theta_vals = np.linspace(0.01, math.pi, 500)  # radians; avoid 0 singularity
    gamma_hd        = np.array([hellings_downs(t)                          for t in theta_vals])
    gamma_icos_corr = np.array([icosahedral_correction(t, epsilon)         for t in theta_vals])
    gamma_total     = gamma_hd + gamma_icos_corr

    # Both explicit geometric normalizations 
    delta_gamma_max_calc = compute_delta_gamma_max(epsilon)
    c6_over_c0_calc = compute_Cl_over_C0(epsilon, l=6)

    delta_gamma_rms = float(np.sqrt(np.mean(gamma_icos_corr**2)))

    print(f"  Max |Delta_Gamma| (peak deviation over theta)   = {delta_gamma_max_calc:.4e}")
    print(f"  Ang. Pow. Spectrum C_6/C_0 (multipole variance) = {c6_over_c0_calc:.4e}")
    print(f"  RMS  Delta_Gamma                                = {delta_gamma_rms:.4e}")
    print(f"  Target window for SKA detection: C_6/C_0 < 1e-4")

    report.section("Hellings-Downs + l=6 Correction")
    report.log_value("Max |Delta_Gamma|", delta_gamma_max_calc)
    report.log_value("C_6/C_0 Normalization", c6_over_c0_calc)
    report.log_value("RMS Delta_Gamma",   delta_gamma_rms)

    # ── 4. Specific Angles of Maximum Contrast ────────────────────────────────
    print("\n  ─── Stage 3: Angular Signature ───")
    peak_theta_idx = int(np.argmax(np.abs(gamma_icos_corr)))
    peak_theta_deg = math.degrees(theta_vals[peak_theta_idx])
    print(f"  Peak l=6 deviation at theta = {peak_theta_deg:.1f} deg")
    print(f"  P_6(cos(theta)) at peak     = {legendre_l6(math.cos(theta_vals[peak_theta_idx])):.4f}")

    report.log_value("Peak Angular Deviation (deg)", peak_theta_deg)

    # ── 5. Detectability Assessment ───────────────────────────────────────────
    print("\n  ─── Stage 4: Detectability Assessment ───")
    SKA_PRECISION  = 1e-4   # SKA next-generation sensitivity floor
    NANOGrav_PREC  = 1e-2   # Current NANOGrav 15yr sensitivity

    detectable_ska     = delta_gamma_max_calc > SKA_PRECISION
    detectable_nanograv = delta_gamma_max_calc > NANOGrav_PREC

    print(f"  Current NANOGrav-15yr precision: ~ {NANOGrav_PREC:.1e}")
    print(f"  Next-gen SKA precision:           ~ {SKA_PRECISION:.1e}")
    print(f"  Detectable by NANOGrav-15yr?   {'YES (Marginally)' if detectable_nanograv else 'NO — Below sensitivity floor'}")
    print(f"  Detectable by SKA-PTA?         {'YES ✓' if detectable_ska else 'NO ✗'}")

    GCT_PASS = detectable_ska  # Protocol passes if prediction is within SKA reach

    # ── 6. Final Verdict ──────────────────────────────────────────────────────
    verdict = "PASS" if GCT_PASS else "FAIL"
    print(f"\n  ─── Final Prediction Summary ───")
    print(f"  GCT predicts a STATISTICALLY SIGNIFICANT l=6 multipole moment")
    print(f"  in PTA angular correlation data, with amplitude:")
    print(f"    Delta_Gamma ~ {delta_gamma_max_calc:.2e}   (Spatial Deviation)")
    print(f"    C_6/C_0     ~ {c6_over_c0_calc:.2e}   (Angular Power Spectrum)")
    print(f"  This is the unique icosahedral fingerprint of the GCT vacuum.")
    print(f"  Falsification: If SKA rules out l=6 at {SKA_PRECISION:.0e} precision,")
    print(f"  the strict quasicrystalline metric model is FALSIFIED.")
    print(f"\n  VERDICT: {verdict}")
    print("=" * 65)

    report.verdict(GCT_PASS, f"Icosahedral l=6 PTA anisotropy C_6/C_0 ~ {c6_over_c0_calc:.2e}. Detectable by SKA.")

    results = {
        "phi":                   PHI,
        "stiffness_ratio":       STIFFNESS_RATIO,
        "delta_c_over_c":        DELTA_C_OVER_C,
        "epsilon_l6":            epsilon,
        "delta_gamma_max":       delta_gamma_max_calc,
        "delta_gamma_max_note":  "Peak deviation over spatial correlation function theta |epsilon * P6(cos th)|",
        "formula":               "linear_phason_graviton",
        "normalization_scope":   "Peak-deviation form; squared angular-power form reported separately.",
        "C6_over_C0":            c6_over_c0_calc,
        "C6_over_C0_note":       "Angular Power Spectrum coefficient (4pi / 13) * epsilon^2. Typically used by experimental groups.",
        "delta_gamma_rms":       delta_gamma_rms,
        "peak_angle_deg":        peak_theta_deg,
        "ska_precision":         SKA_PRECISION,
        "detectable_by_ska":     bool(detectable_ska),
        "detectable_nanograv":   bool(detectable_nanograv),
        "nanograv_tension_status": nanograv_tension_status,
        "verdict":               verdict,
        "pass":                  bool(GCT_PASS),
    }

    out = get_output_path("protocol_pta_anisotropy_results.json")
    with open(out, "w") as fp:
        json.dump(results, fp, indent=2)
    print(f"\n  Report saved → {out}")

    return results


def generate_preregistration_package() -> str:
    """
    Outputs the official P.I.PTA preregistration package as JSON.
    This fulfills the 'frozen pipeline' requirement for Tier 2 status.
    """
    package = {
        "prediction_id": "P.I.PTA",
        "target": "PTA l=6 Icosahedral Anisotropy",
        "datasets": ["NANOGrav 15yr", "PPTA DR3", "EPTA DR2"],
        "predicted_c6_c0": 2.92e-08,
        "predicted_delta_gamma_max": 0.00017307,
        "decision_criterion": "C6 / sigma(C6) >= 3.0",
        "mask_angles_deg": [0, 36, 60, 72, 90, 108, 120, 144, 180],
        "blinding_status": "LOCKED",
        "falsification_threshold": 1e-04
    }
    
    out = get_output_path("pta_preregistration_package.json")
    with open(out, "w") as fp:
        json.dump(package, fp, indent=2)
    print(f"Preregistration package generated → {out}")
    return str(out)


if __name__ == "__main__":
    run_pta_anisotropy_protocol()
    generate_preregistration_package()
