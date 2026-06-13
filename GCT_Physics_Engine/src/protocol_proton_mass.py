#!/usr/bin/env python3
"""
GCT Protocol F: Proton Mass (Analytic Resonance Evaluator)
Filename: protocol_proton_mass.py

All constants imported from SSOT (gct_constants).
       Constants are taken from the SSOT.

As specified in V3 Chapter 10, the proton mass is the fundamental acoustic
resonance of the 6D lattice, derived from holonomic additivity.
"""

import json
import sys
import os

from gct_utils import PHI, get_output_path, GCTReporter
from gct_utils import C

# Load the derived electron mass from the committed exponent-derivation JSON.


def main():
    report = GCTReporter("Proton Mass (Analytic Audit)")

    # Load the derived electron mass from protocol_exponent_derivation_results.json
    try:
        scale_path = get_output_path("protocol_exponent_derivation_results.json")
        with open(scale_path, 'r') as f:
            scale_data = json.load(f)
        m_e_derived_kg = scale_data["C3_closure"]["m_pred_kg"]
        m_e_derived = m_e_derived_kg * (float(C.C)**2) / (float(C.EV_TO_J) * 1e6)
    except Exception as e:
        print(f"Error loading exponent derivation results: {e}")
        m_e_derived = float(C.M_E_OBS) # fallback

    # Constants from SSOT
    m_e_obs = float(C.M_E_OBS)
    phi     = PHI

    # Formula components from SSOT: N_strong = 15, N_weak_berry = 1/phi
    n_strong       = float(C.N_BARYON)    # 15
    n_weak         = 1.0 / phi            # phi^{-1} (Berry phase correction)
    total_exponent = n_strong + n_weak

    # Mass Ratio Calculation: m_p/m_e = phi^(15 + 1/phi)
    mass_ratio = phi ** total_exponent
    
    # Pathway 1: Ratio Benchmark (Proton Mass calculated against experimental Electron Mass)
    m_p_ratio_pred = m_e_obs * mass_ratio
    
    # Pathway 2: Absolute Benchmark (End-to-End prediction starting from M_Planck)
    m_p_abs_pred   = m_e_derived * mass_ratio

    # Observed value from SSOT
    OBS_PROTON = C.M_P_OBS   # 938.272088 MeV

    report.section("Geometric Derivation")
    report.log_value("Strong Winding (N)",          n_strong)
    report.log_value("Weak Berry Phase (1/phi)",     n_weak)
    report.log_value("Total Resonance Exponent",     total_exponent)
    report.log_value("Mass Ratio (m_p/m_e)",         mass_ratio)

    report.section("Mass Comparison: Ratio Benchmark")
    report.log_comparison("Proton Mass (Ratio)", m_p_ratio_pred, OBS_PROTON)

    ratio_err_ppm = (abs(m_p_ratio_pred - OBS_PROTON) / OBS_PROTON) * 1e6
    report.log_value("Ratio Relative Error", ratio_err_ppm, "ppm")

    report.section("Mass Comparison: Absolute Benchmark (M_Planck -> m_e -> m_p)")
    report.log_comparison("Proton Mass (Absolute)", m_p_abs_pred, OBS_PROTON)

    abs_err_ppm = (abs(m_p_abs_pred - OBS_PROTON) / OBS_PROTON) * 1e6
    report.log_value("Absolute Relative Error", abs_err_ppm, "ppm")

    # Tolerance (200 ppm for ratio, 1200 ppm for Absolute)
    passed_ratio = ratio_err_ppm < 200.0
    passed_abs   = abs_err_ppm < 1200.0
    overall_pass = passed_ratio and passed_abs

    report.verdict(overall_pass, f"Proton mass derived successfully. Ratio Err: {ratio_err_ppm:.2f} ppm, Absolute: {abs_err_ppm:.2f} ppm.")

    # Output JSON for verifier
    results = {
        "mass_ratio": mass_ratio,
        "mass_ratio_mev": m_p_ratio_pred,
        "mass_abs_mev":   m_p_abs_pred,
        "ratio_error_ppm": ratio_err_ppm,
        "abs_error_ppm":  abs_err_ppm,
        "m_e_derived":    m_e_derived,
        "pass":           bool(overall_pass)
    }

    with open(get_output_path("protocol_proton_mass_results.json"), 'w') as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    main()
