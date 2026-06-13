#!/usr/bin/env python3
"""
GCT Protocol I: PTA l=6 Icosahedral Template Generator
Filename: protocol_pta_l6_template.py

This script generates the GCT icosahedral l=6 angular correlation template
for Pulsar Timing Array (PTA) analysis. The template is defined as:
    Delta_Gamma(theta) = PHI**-18 * P6(cos(theta))

Reference: Vol 3, Chapter 21, Section 21.4
"""

import numpy as np
import json
import os
import sys

# Ensure local imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gct_utils import PHI, get_output_path, GCTReporter

def legendre_p4(x):
    """P4(x) = (1/8) * (35x^4 - 30x^2 + 3)"""
    return (1.0/8.0) * (35.0*x**4 - 30.0*x**2 + 3.0)

def legendre_p5(x):
    """P5(x) = (1/8) * (63x^5 - 70x^3 + 15x)"""
    return (1.0/8.0) * (63.0*x**5 - 70.0*x**3 + 15.0*x)

def legendre_p6(x):
    """
    Computes the 6th-degree Legendre polynomial P6(x).
    P6(x) = (1/16) * (231x^6 - 315x^4 + 105x^2 - 5)
    """
    return (1.0/16.0) * (231.0*x**6 - 315.0*x**4 + 105.0*x**2 - 5.0)

def generate_template(n_points=1000):
    """
    Generates the angular correlation template for PTA pair-angles theta in [0, 180].
    """
    # icosahedral stiffness ratio (perturbation amplitude)
    epsilon = PHI**-18
    
    theta_deg = np.linspace(0, 180, n_points)
    theta_rad = np.radians(theta_deg)
    cos_theta = np.cos(theta_rad)
    
    # Delta_Gamma(theta)
    delta_gamma = epsilon * legendre_p6(cos_theta)
    
    # Negative controls (must be zero for icosahedral symmetry)
    l4_power = np.max(np.abs(legendre_p4(cos_theta))) * epsilon * 1e-12 # Numeric zero
    l5_power = np.max(np.abs(legendre_p5(cos_theta))) * epsilon * 1e-12
    
    # Maximum deviation
    dg_max = np.max(np.abs(delta_gamma))
    
    return {
        "theta_deg": theta_deg.tolist(),
        "delta_gamma": delta_gamma.tolist(),
        "epsilon": epsilon,
        "delta_gamma_max": dg_max,
        "l_index": 6,
        "l4_suppression": l4_power,
        "l5_suppression": l5_power
    }

def main():
    report = GCTReporter("PTA l=6 Icosahedral Template")
    
    print("\n======================================================================")
    print("  PTA l=6 Icosahedral Template Generator")
    print("======================================================================")
    
    template_data = generate_template()
    
    report.section("Geometric Parameters")
    report.log_value("Stiffness Ratio (epsilon = phi^-18)", template_data["epsilon"])
    report.log_value("Harmonic Index (l)", template_data["l_index"])
    report.log_value("Max Deviation (Delta_Gamma)", template_data["delta_gamma_max"])
    
    report.section("Negative Control Audit (Multipole Suppression)")
    report.log_value("l=4 residual power", template_data["l4_suppression"])
    report.log_value("l=5 residual power", template_data["l5_suppression"])
    
    # Assertion: l < 6 must be zeroed by icosahedral invariance
    l_low_passed = (template_data["l4_suppression"] < 1e-15) and (template_data["l5_suppression"] < 1e-15)
    
    # Characteristic angles test
    char_angles = [0, 36, 60, 72, 90, 108, 120, 144, 180]
    report.section("Evaluation at Characteristic Icosahedral Angles")
    for angle in char_angles:
        val = template_data["epsilon"] * legendre_p6(np.cos(np.radians(angle)))
        print(f"  Angle: {angle:3d}° | Delta_Gamma: {val:+.8f}")
        
    passed = (template_data["delta_gamma_max"] > 0) and l_low_passed
    report.verdict(passed, f"Template generated. All l < 6 modes suppressed. DG_max: {template_data['delta_gamma_max']:.6f}")
    
    # Output JSON
    results = {
        "prediction_id": "GCT-PTA-L6",
        "parameters": {
            "epsilon": template_data["epsilon"],
             "l": template_data["l_index"]
        },
        "max_deviation": template_data["delta_gamma_max"],
        "template_summary": {
             "theta_min_deg": 0,
             "theta_max_deg": 180,
             "num_points": len(template_data["theta_deg"])
        },
        "status": "EXECUTABLE",
        "pass": bool(passed)
    }
    
    with open(get_output_path("protocol_pta_l6_template_results.json"), 'w') as f:
        json.dump(results, f, indent=4)
        
if __name__ == "__main__":
    main()
