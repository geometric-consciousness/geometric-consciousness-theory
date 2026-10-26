#!/usr/bin/env python3
"""
GCT Protocol B: Conditional Electroweak Flow Audit
Filename: protocol_electroweak.py

This protocol distinguishes canonical projector geometry from two registered
physical hypotheses:

* phi^-3 is the OPEN_CONDITIONAL_GAUGE_KINETIC_HYPOTHESIS for the bare
  electroweak angle;
* phi^-18 is the OPEN_CONDITIONAL_P3B_O15 stiffness hypothesis.

The numerical running uses the physical-hypercharge convention

    alpha_Y = g'^2/(4 pi),  alpha_2 = g^2/(4 pi),
    sin^2(theta_W) = alpha_Y/(alpha_Y + alpha_2),

and the full-content Standard-Model one-loop coefficients b_Y=41/6 and
b_2=-19/6 over the interval M_Z..M_GUT.  This deliberately transparent
full-SM approximation is used instead of a particle-by-particle threshold
split, which would require a declared scheme and matching conditions.

The calculation imports the measured alpha_2(M_Z) through alpha_em(M_Z) and
sin^2(theta_W)(M_Z).  It is therefore a one-coupling-conditioned diagnostic,
not a first-principles endpoint prediction.

Three P3b-conditioned scale choices are compared.  Their numerical residuals
are diagnostics; none is treated as a verified unification solution.
"""

import numpy as np
import sys
import os
import json
import math

# Ensure local imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gct_utils import PHI, get_output_path, GCTReporter
from gct_utils import C
from gct_projections import (
    get_m_parallel,
    get_m_parallel_unnormalized,
    get_m_perp,
    get_m_perp_unnormalized,
)

# =============================================================================
# 2. PROJECTOR NORMALIZATION + RAW-FRAME DIAGNOSTIC
# =============================================================================

def verify_gram_projection():
    """Audit canonical projector weights and raw-frame coordinate ratios.

    Canonical proper projectors assign squared norm 1/2 to every Z6 basis
    vector in both sectors.  The raw Galois row frames reproduce phi^-2 and
    phi^-3 coordinate diagnostics, but B -> phi B leaves the proper projector
    fixed while mapping those ratios to one.  Hence neither raw number is a
    physical gauge boundary without an independent kinetic normalization.
    """

    def projector_from_rows(matrix):
        return matrix.T @ np.linalg.solve(matrix @ matrix.T, matrix)

    m_para = get_m_parallel()
    m_perp = get_m_perp()
    p_para = projector_from_rows(m_para)
    p_perp = projector_from_rows(m_perp)
    canonical_para_sq = np.diag(p_para)
    canonical_perp_sq = np.diag(p_perp)

    m_para_raw = get_m_parallel_unnormalized()
    m_perp_raw = get_m_perp_unnormalized()
    raw_para_sq = np.sum(m_para_raw**2, axis=0)
    raw_perp_sq = np.sum(m_perp_raw**2, axis=0)
    raw_squared_ratio = float(raw_perp_sq[0] / raw_para_sq[0])
    raw_length_ratio = math.sqrt(raw_squared_ratio)
    raw_volume_ratio = raw_length_ratio**3

    scaled_perp_raw = PHI * m_perp_raw
    scaled_perp_sq = np.sum(scaled_perp_raw**2, axis=0)
    scaled_squared_ratio = float(scaled_perp_sq[0] / raw_para_sq[0])
    scaled_projector = projector_from_rows(scaled_perp_raw)

    machine_pass = bool(
        np.allclose(canonical_para_sq, np.full(6, 0.5), atol=1e-12)
        and np.allclose(canonical_perp_sq, np.full(6, 0.5), atol=1e-12)
        and np.allclose(p_para + p_perp, np.eye(6), atol=1e-12)
        and np.isclose(raw_squared_ratio, PHI**-2, atol=1e-12)
        and np.isclose(raw_volume_ratio, PHI**-3, atol=1e-12)
        and np.isclose(scaled_squared_ratio, 1.0, atol=1e-12)
        and np.allclose(p_perp, scaled_projector, atol=1e-12)
    )

    return {
        "machine_pass": machine_pass,
        "canonical_projected_basis_norm_sq_parallel": canonical_para_sq.tolist(),
        "canonical_projected_basis_norm_sq_perp": canonical_perp_sq.tolist(),
        "canonical_per_axis_squared_ratio": 1.0,
        "canonical_volume_ratio": 1.0,
        "raw_galois_squared_ratio": raw_squared_ratio,
        "raw_galois_length_ratio": raw_length_ratio,
        "raw_galois_volume_ratio": raw_volume_ratio,
        "raw_ratio_coordinate_invariant": False,
        "scaled_raw_squared_ratio": scaled_squared_ratio,
        "proper_projector_unchanged_under_rescaling": bool(
            np.allclose(p_perp, scaled_projector, atol=1e-12)
        ),
        "bare_angle_hypothesis": PHI**-3,
        "bare_angle_status": "OPEN_CONDITIONAL_GAUGE_KINETIC_HYPOTHESIS",
        "physical_boundary_derived_from_projection": False,
    }


# =============================================================================
# 1. PHYSICAL PARAMETERS
# =============================================================================
M_Z             = C.M_Z                  # 91.1876 GeV
ALPHA_EM_INV_MZ = C.ALPHA_EM_INV_MZ      # 127.94
SIN2_W_OBS      = C.SIN2_THETA_W_OBS     # 0.23122
SIN2_W_BARE_HYPOTHESIS = PHI**(-3)  # Tier 3 conditional gauge-kinetic input
RAW_GALOIS_RATIO = PHI**(-2)         # Tier 1 raw coordinate-frame diagnostic

# =============================================================================
# TIER CLASSIFICATION
# =============================================================================
# RAW_GALOIS_RATIO = PHI**-2 → TIER 1 raw-frame arithmetic only.
# SIN2_W_BARE_HYPOTHESIS    → TIER 3 conditional gauge-kinetic input.
# SIN2_W_OBS = 0.23122       → TIER 3 OBSERVATIONAL IMPORT (NOT a prediction)
#                              This value is imported from experiment as the RGE endpoint.
# With the declared phi^-3 boundary and the corrected full-SM one-loop
# coefficients, the reduced-Planck diagnostic misses the Z-pole by about 41%.
# Using the raw phi^-2 coordinate diagnostic as the UV angle is reported only
# as a counterfactual (about 9.4% low); it is not a physical boundary.
# Physical boundary and IR-flow closure remain open.
# =============================================================================

PLANCK_MASS_GEV = 1.2209e19
REDUCED_PLANCK_MASS_GEV = PLANCK_MASS_GEV / np.sqrt(8.0 * np.pi)

# Physical-hypercharge convention.  In the SU(5)-normalised convention one
# instead writes alpha_1=(5/3)alpha_Y and b_1=41/10; mixing the two conventions
# is forbidden.  This protocol stays in the physical alpha_Y convention.
B_Y_SM_FULL = 41.0 / 6.0
B_2_SM_FULL = -19.0 / 6.0
RGE_CONVENTION = "PHYSICAL_HYPERCHARGE_ALPHA_Y"

def get_beta_coeffs(energy):
    """Return the full-content SM one-loop coefficients above M_Z.

    A precision threshold treatment would require a declared renormalisation
    scheme and matching conditions, so this audit uses the standard
    full-content approximation.
    """
    _ = energy
    return B_Y_SM_FULL, B_2_SM_FULL

def get_gct_scales():
    # Explicit P3b/O.15 hypothesis.  This value is not sourced from projection
    # Gram determinants.
    eta = float(C.ETA_STIFFNESS)
    
    # Scale A: M_P * phi^-9 (Light)
    m_gut_light = PLANCK_MASS_GEV * (PHI**-9)
    # Scale B: M_P * phi^-18 (Stiffness)
    m_gut_stiff = PLANCK_MASS_GEV * eta
    # Scale C: M_red * phi^-9 (Reduced Light)
    m_gut_red   = REDUCED_PLANCK_MASS_GEV * (PHI**-9)
    
    return m_gut_light, m_gut_stiff, m_gut_red

# =============================================================================
# RGE INTEGRATION
# =============================================================================

def run_rge_step(energy, dt, a_y_inv, a2_inv):
    b_y, b2 = get_beta_coeffs(energy)
    a_y_inv -= (b_y / (2.0 * np.pi)) * dt
    a2_inv -= (b2 / (2.0 * np.pi)) * dt
    return a_y_inv, a2_inv

def evolve_couplings(start_energy, end_energy, start_a_y_inv, start_a2_inv, n_steps=2000):
    log_mu_start = np.log(start_energy)
    log_mu_end   = np.log(end_energy)
    log_mu_array = np.linspace(log_mu_start, log_mu_end, n_steps)
    
    a_y_inv = start_a_y_inv
    a2_inv = start_a2_inv
    history = []
    
    for i in range(len(log_mu_array) - 1):
        t1 = log_mu_array[i]
        t2 = log_mu_array[i+1]
        dt = t2 - t1
        energy = np.exp(t1)
        
        a_y_inv, a2_inv = run_rge_step(energy, dt, a_y_inv, a2_inv)
        
        val_a_y = 1.0 / a_y_inv
        val_a2 = 1.0 / a2_inv
        curr_sin2 = val_a_y / (val_a_y + val_a2)
        
        history.append((np.exp(t2), curr_sin2, a_y_inv, a2_inv))
        
    return history

def run_test_case(name, m_gut, report, target_sin2=SIN2_W_BARE_HYPOTHESIS):
    report.section(f"Test Case: {name}")
    report.log_value("GUT Scale", m_gut, "GeV")
    
    # Run UP to match alpha_2 scale
    start_a2_inv = SIN2_W_OBS * ALPHA_EM_INV_MZ
    start_a_y_inv = (1.0 - SIN2_W_OBS) * ALPHA_EM_INV_MZ
    
    hist_up = evolve_couplings(M_Z, m_gut, start_a_y_inv, start_a2_inv)
    _, _, final_a_y_inv_from_observed, final_a2_inv_sm = hist_up[-1]
    
    # Conditional gauge-kinetic boundary hypothesis.  The observed Z-pole
    # endpoint above was used to initialize the comparison flow, so this is a
    # postdictive consistency calculation rather than an autonomous prediction.
    target_ratio = target_sin2 / (1.0 - target_sin2)
    
    new_a2_inv_gut = final_a2_inv_sm
    new_a_y_inv_gut = new_a2_inv_gut / target_ratio
    
    # Run DOWN
    hist_down = evolve_couplings(m_gut, M_Z, new_a_y_inv_gut, new_a2_inv_gut)
    final_e_down, final_sin2_down, final_a_y_inv, final_a2_inv = hist_down[-1]
    
    report.log_value("Postdictive output @ Z-Pole", final_sin2_down)
    report.log_comparison("Observed", final_sin2_down, SIN2_W_OBS)
    
    signed_err = (final_sin2_down - SIN2_W_OBS) / SIN2_W_OBS
    implied_uv_sin2_from_observed = final_a2_inv_sm / (
        final_a_y_inv_from_observed + final_a2_inv_sm
    )
    return {
        "sin2_mz": final_sin2_down,
        "relative_error_abs": abs(signed_err),
        "relative_error_signed": signed_err,
        "target_sin2_uv": target_sin2,
        "alpha_y_inv_gut": new_a_y_inv_gut,
        "alpha_2_inv_gut": new_a2_inv_gut,
        "alpha_y_inv_mz": final_a_y_inv,
        "alpha_2_inv_mz": final_a2_inv,
        "implied_uv_sin2_from_observed_couplings": implied_uv_sin2_from_observed,
        "final_energy_gev": final_e_down,
    }

def main():
    report = GCTReporter("Conditional Electroweak Flow Audit")

    # -------------------------------------------------------------------------
    # PROJECTOR NORMALIZATION + RAW-FRAME DIAGNOSTIC
    # -------------------------------------------------------------------------
    gp = verify_gram_projection()
    report.section("Canonical Projector Audit [Tier 1]")
    print("  Canonical projected basis norms: parallel = perp = 1/2")
    print(f"  Canonical per-axis squared ratio      = {gp['canonical_per_axis_squared_ratio']:.10f}")
    print(f"  Canonical volume ratio                = {gp['canonical_volume_ratio']:.10f}")
    print(f"  Raw Galois squared ratio diagnostic   = {gp['raw_galois_squared_ratio']:.10f}")
    print(f"  Raw Galois volume diagnostic          = {gp['raw_galois_volume_ratio']:.10f}")
    print(f"  Conditional bare-angle hypothesis     = {gp['bare_angle_hypothesis']:.10f}")
    machine_status = "PASS (machine precision)" if gp['machine_pass'] else "FAIL"
    print(f"  Machine-precision audit               : {machine_status}")
    print(f"  Physical boundary derived?            : {gp['physical_boundary_derived_from_projection']}")
    print(f"  Bare-angle status                     : {gp['bare_angle_status']}")
    print()

    # -------------------------------------------------------------------------
    # RGE ELECTROWEAK RUNNING — Test cases
    # -------------------------------------------------------------------------
    m_light, m_stiff, m_red = get_gct_scales()

    # Comparisons
    case_light = run_test_case("Light Scale (phi^-9)", m_light, report)
    case_stiff = run_test_case("Stiffness Scale (phi^-18)", m_stiff, report)
    case_red = run_test_case("Reduced Light Scale (M_red * phi^-9)", m_red, report)

    # Counterfactual audit only: the raw phi^-2 coordinate diagnostic used as
    # if it were the physical UV sin^2.
    raw_red = run_test_case(
        "Raw-phi^-2 counterfactual at reduced scale",
        m_red,
        report,
        target_sin2=RAW_GALOIS_RATIO,
    )
    res_light, err_light = case_light["sin2_mz"], case_light["relative_error_abs"]
    res_stiff, err_stiff = case_stiff["sin2_mz"], case_stiff["relative_error_abs"]
    res_red, err_red = case_red["sin2_mz"], case_red["relative_error_abs"]

    # Verdict
    pass_red = err_red < 0.005 # < 0.5%

    report.section("Summary Analysis")
    report.log_value("Stiffness Error", err_stiff*100, "%")
    report.log_value("Light Error", err_light*100, "%")
    report.log_value("Reduced Light Error", err_red*100, "%")

    print("\n" + "=" * 60)
    print(f"FLOW-CONSISTENCY CHECK: {'PASSED' if pass_red else 'FAILED'}")
    print("PROTOCOL STATUS: FAILED_CHECK__H_EW_HYPOTHESIS_OPEN")
    print(
        f"Reduced-Planck comparison residual: {err_red*100:.2f}%. "
        "This does not derive the UV gauge-kinetic boundary."
    )
    print("=" * 60)

    with open(get_output_path("protocol_electroweak_results.json"), 'w') as f:
        json.dump({
            "run_type": "scale_comparison",
            "pass": False,
            "status": "FAILED_CHECK__H_EW_HYPOTHESIS_OPEN",
            "flow_consistency_pass": bool(pass_red),
            "physical_boundary_derived": False,
            "physical_endpoint_predicted_autonomously": False,
            "projector_audit": gp,
            "rge_convention": {
                "name": RGE_CONVENTION,
                "sin2_definition": "alpha_Y / (alpha_Y + alpha_2)",
                "b_Y_full_sm": B_Y_SM_FULL,
                "b_2_full_sm": B_2_SM_FULL,
                "full_sm_above_mz_approximation": True,
                "sm_coefficient_audit_pass": bool(
                    np.isclose(B_Y_SM_FULL, 41.0 / 6.0)
                    and np.isclose(B_2_SM_FULL, -19.0 / 6.0)
                ),
                "su5_normalized_alpha1_used": False,
            },
            "m_gut_light": m_light,
            "m_gut_stiff": m_stiff,
            "m_gut_red": m_red,
            "sin2_light": res_light,
            "sin2_stiff": res_stiff,
            "sin2_red": res_red,
            "error_light": err_light,
            "error_stiff": err_stiff,
            "error_red": err_red,
            "signed_error_red": case_red["relative_error_signed"],
            "reduced_scale_case": case_red,
            "raw_phi_minus_2_counterfactual": {
                **raw_red,
                "status": "COORDINATE_DIAGNOSTIC_NOT_PHYSICAL_BOUNDARY",
                "prediction": False,
            },
            "conditional_inputs": {
                "bare_sin2_phi_minus_3": "OPEN_CONDITIONAL_GAUGE_KINETIC_HYPOTHESIS",
                "stiffness_phi_minus_18": "OPEN_CONDITIONAL_P3B_O15",
                "sin2theta_W_Mz": "Imported to construct measured alpha_2(M_Z)",
                "alpha_em_inv_Mz": "Imported observational coupling",
                "calibration_status": "ONE_COUPLING_CONDITIONED_DIAGNOSTIC"
            }
        }, f, indent=2)

if __name__ == "__main__":
    main()
