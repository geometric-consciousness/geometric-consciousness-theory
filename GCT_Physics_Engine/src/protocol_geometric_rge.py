#!/usr/bin/env python3
"""
protocol_geometric_rge.py — Quarantined Spectral-Kernel Integrator Audit
========================================================================

Choosing the overall kernel coefficient as

    K = (sin^2(theta_W)_UV - sin^2(theta_W)_observed) / integral(beta dt)

imposes the observed endpoint algebraically, so the endpoint cannot be a
prediction.  This protocol therefore separates:

1. the Tier-3 H-EW boundary hypothesis sin^2(theta_W)^UV = phi^-3;
2. a unit-normalised numerical integration check for the stored kernel shape;
3. an explicitly target-normalised counterfactual that uses the observed
   endpoint as an input and therefore has no physical-prediction status.

No action-level coefficient is currently derived for the spectral kernel, so
the protocol intentionally has intrinsic pass=False.  Raw phi^-2 appears only
as a coordinate-frame diagnostic.
"""

import json
import os
import sys

import numpy as np
from scipy.interpolate import interp1d

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from gct_utils import C, PHI, get_output_path, GCTReporter


# =============================================================================
# DECLARED INPUTS AND STATUS
# =============================================================================

M_Z_GEV = float(C.M_Z)
SIN2_W_OBS = float(C.SIN2_THETA_W_OBS)
PLANCK_MASS_GEV = 1.2209e19
REDUCED_PLANCK = PLANCK_MASS_GEV / np.sqrt(8.0 * np.pi)
M_GUT_GEV = REDUCED_PLANCK * (PHI ** -9)
T_GUT = np.log(M_GUT_GEV / M_Z_GEV)

H_EW_SIN2_UV_HYPOTHESIS = PHI ** -3
H_EW_STATUS = "OPEN_CONDITIONAL_GAUGE_KINETIC_HYPOTHESIS"
RAW_PHI_MINUS_2_DIAGNOSTIC = PHI ** -2
PROTOCOL_STATUS = "QUARANTINED_ENDPOINT_BY_CONSTRUCTION"


# =============================================================================
# KERNEL INGESTION AND UNIT NORMALISATION
# =============================================================================

def load_spectral_kernel():
    kernel_path = os.path.join(
        os.path.dirname(__file__), "..", "data", "spectral_rge_kernel.json"
    )
    if not os.path.exists(kernel_path):
        raise FileNotFoundError(
            f"Kernel not found at {kernel_path}. Run protocol_spectral_action.py first."
        )

    with open(kernel_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    l_points = np.asarray(data["L_points"], dtype=float)
    beta_vals = np.asarray(data["beta_vals"], dtype=float)
    interpolator = interp1d(
        l_points,
        beta_vals,
        kind="quadratic",
        fill_value="extrapolate",
    )
    return interpolator, float(l_points[0]), float(l_points[-1]), kernel_path


F_BETA, L_MIN, L_MAX, KERNEL_PATH = load_spectral_kernel()


def resolution_coordinate(t, t_gut=T_GUT):
    return L_MIN + (L_MAX - L_MIN) * (t / t_gut)


def compute_kernel_integral(t_gut=T_GUT, n_points=20001):
    t_values = np.linspace(0.0, t_gut, n_points)
    beta_values = F_BETA(resolution_coordinate(t_values, t_gut))
    return float(np.trapezoid(beta_values, t_values))


RAW_KERNEL_INTEGRAL = compute_kernel_integral()
if not np.isfinite(RAW_KERNEL_INTEGRAL) or abs(RAW_KERNEL_INTEGRAL) < 1e-15:
    raise ValueError("Spectral kernel has zero or non-finite integral; cannot audit.")


def unit_beta(t, t_gut=T_GUT):
    """Unit-area kernel shape; this is mathematical normalisation only."""
    return float(F_BETA(resolution_coordinate(t, t_gut)) / RAW_KERNEL_INTEGRAL)


def integrate_response(initial_value, amplitude, t_gut=T_GUT, n_steps=5000):
    """RK4 integration of d(response)/dt = amplitude * unit_beta(t)."""
    t_values = np.linspace(t_gut, 0.0, n_steps + 1)
    value = float(initial_value)
    history = [(float(t_values[0]), float(M_Z_GEV * np.exp(t_values[0])), value)]

    for i in range(n_steps):
        t = float(t_values[i])
        dt = float(t_values[i + 1] - t_values[i])
        k1 = amplitude * unit_beta(t, t_gut)
        k2 = amplitude * unit_beta(t + dt / 2.0, t_gut)
        k3 = amplitude * unit_beta(t + dt / 2.0, t_gut)
        k4 = amplitude * unit_beta(t + dt, t_gut)
        value += dt * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
        history.append(
            (
                float(t_values[i + 1]),
                float(M_Z_GEV * np.exp(t_values[i + 1])),
                float(value),
            )
        )
    return history


def main():
    report = GCTReporter("Quarantined Spectral-Kernel Integrator Audit")

    report.section("Declared boundary and kernel")
    report.log_value("M_GUT", M_GUT_GEV, "GeV")
    report.log_value("T_GUT", T_GUT)
    report.log_value("H-EW sin^2(theta_W)^UV = phi^-3", H_EW_SIN2_UV_HYPOTHESIS)
    report.log_value("Raw phi^-2 coordinate diagnostic", RAW_PHI_MINUS_2_DIAGNOSTIC)
    report.log_value("Raw spectral-kernel integral", RAW_KERNEL_INTEGRAL)

    # Unit-response test: integrating the unit-area kernel from T_GUT down to
    # zero must give -1.  This tests interpolation and RK4 only.
    unit_history = integrate_response(0.0, 1.0)
    unit_response = unit_history[-1][2]
    unit_integral_pass = bool(abs(unit_response + 1.0) < 1e-6)

    # Counterfactual endpoint-normalised branch.  The amplitude below is solved
    # from the observed endpoint and the measured unit response.  Agreement is
    # therefore expected by construction and is not a physical prediction.
    imposed_amplitude = (
        SIN2_W_OBS - H_EW_SIN2_UV_HYPOTHESIS
    ) / unit_response
    target_history = integrate_response(H_EW_SIN2_UV_HYPOTHESIS, imposed_amplitude)
    imposed_endpoint = target_history[-1][2]
    endpoint_integrator_error = abs(imposed_endpoint - SIN2_W_OBS)
    endpoint_integrator_pass = bool(endpoint_integrator_error < 1e-10)

    report.section("Numerical checks")
    report.log_value("Unit response T_GUT -> 0", unit_response)
    report.log_value("Target-normalised amplitude", imposed_amplitude)
    report.log_value("Target-normalised endpoint", imposed_endpoint)
    report.log_value("Observed endpoint used as input", SIN2_W_OBS)
    report.log_value("Integrator error", endpoint_integrator_error)

    print("\n" + "=" * 60)
    print("PHYSICAL VERDICT: NOT TESTED — ACTION-LEVEL KERNEL AMPLITUDE OPEN")
    print(f"PROTOCOL STATUS: {PROTOCOL_STATUS}")
    print(
        "The target-normalised endpoint is an integrator check because the "
        "observed endpoint fixes its amplitude."
    )
    print("=" * 60)

    results = {
        "protocol": "Quarantined Spectral-Kernel Integrator Audit",
        "pass": False,
        "status": PROTOCOL_STATUS,
        "m_gut_gev": M_GUT_GEV,
        "t_gut": T_GUT,
        "h_ew_boundary": {
            "sin2_theta_W_uv_phi_minus_3": H_EW_SIN2_UV_HYPOTHESIS,
            "status": H_EW_STATUS,
            "derived_from_kernel": False,
            "derived_from_canonical_projector": False,
        },
        "raw_phi_minus_2": {
            "value": RAW_PHI_MINUS_2_DIAGNOSTIC,
            "status": "COORDINATE_DIAGNOSTIC_NOT_PHYSICAL_BOUNDARY",
            "prediction": False,
        },
        "kernel_audit": {
            "kernel_file": os.path.basename(KERNEL_PATH),
            "raw_kernel_integral": RAW_KERNEL_INTEGRAL,
            "unit_response_TGUT_to_zero": unit_response,
            "expected_unit_response": -1.0,
            "unit_integral_pass": unit_integral_pass,
            "shape_physically_derived": False,
            "amplitude_physically_derived": False,
        },
        "target_normalized_integrator_check": {
            "observed_endpoint_used_as_input": True,
            "sin2_theta_W_observed_input": SIN2_W_OBS,
            "h_ew_initial_value": H_EW_SIN2_UV_HYPOTHESIS,
            "amplitude_solved_from_observed_endpoint": imposed_amplitude,
            "output_endpoint": imposed_endpoint,
            "absolute_integrator_error": endpoint_integrator_error,
            "integrator_pass": endpoint_integrator_pass,
            "physical_prediction": False,
        },
        "physical_closure": {
            "physical_endpoint_predicted": False,
            "sin2_theta_W_MZ_prediction": None,
            "action_level_kernel_coefficient_derived": False,
            "overall_physical_pass": False,
        },
        # Summary fields: no endpoint prediction exists, so the predicted
        # value and error are null.
        "sin2_w_gut_bc": H_EW_SIN2_UV_HYPOTHESIS,
        "sin2_w_predicted": None,
        "sin2_w_observed": SIN2_W_OBS,
        "error_pct": None,
        "method": "Target-normalised spectral-kernel integrator quarantine",
        "sm_beta_functions": False,
    }

    out_path = get_output_path("protocol_geometric_rge_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to: {out_path}")


if __name__ == "__main__":
    main()
