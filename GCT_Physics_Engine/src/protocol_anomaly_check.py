#!/usr/bin/env python3
"""
protocol_anomaly_check.py — Anomaly Audit 
======================================================
Verifies that the GCT-derived particle spectrum constitutes a consistent,
anomaly-free quantum field theory.

Checks:
1. U(1)-Gravitational Anomaly (Sum Y)
2. SU(2)^2 * U(1) Anomaly
3. SU(3)^2 * U(1) Anomaly
4. U(1)^3 Anomaly

Input:
- Spectrum derived from Geometric Topology (Vertex -> -1, Face -> 1/3).
"""

import json
import numpy as np
from pathlib import Path

from gct_algebra_consistency import ConsistencyChecker
from gct_utils import get_output_path

def run_anomaly_audit():
    print("="*60)
    print("GCT Protocol: Anomaly Cancellation Audit")
    print("="*60)
    
    results = {}
    
    # 1. Load Spectrum
    # In GCT, the spectrum is "Generated" by the tiling.
    # We use the standard model generation structure derived in V3 Ch04.
    spectrum = ConsistencyChecker.get_standard_model_generation()
    
    print(f"\nParticle Spectrum (Gen 1):")
    print(f"{'Particle':<10} {'SU(3)':<8} {'SU(2)':<8} {'Y (GCT)':<10}")
    print("-" * 50)
    for p in spectrum:
        print(f"{p['name']:<10} {p['su3']:<8} {p['su2']:<8} {p['Y']:<10.3f}")
        
    # 2. Compute Anomalies
    print("\nComputing Anomaly Coefficients...")
    anomalies = ConsistencyChecker.check_anomaly_cancellation(spectrum)
    
    print("\nResults:")
    all_pass = True
    tolerance = 1e-12
    
    for key, val in anomalies.items():
        note = "PASS" if abs(val) < tolerance else "FAIL"
        print(f"  {key:<20}: {val: .4e}  [{note}]")
        
        results[key] = {
            "value": float(val),
            "verdict": note
        }
        if note == "FAIL":
            all_pass = False
            
    # Check Right-Handed Neutrino Impact
    # nu_R has Y=0, so it naturally contributes 0 to all Y-dependent anomalies.
    # It assumes nu_R is a singlet under everything (1, 1, 0).
    # Check if nu_R was in the spectrum
    has_nu_r = any(p['name'] == 'nu_R' for p in spectrum)
    print(f"\nRight-Handed Neutrino (nu_R) present? {has_nu_r}")
    
    # Summary
    print("\n" + "="*60)
    if all_pass:
        print("PASS: Standard Model hypercharge anomaly traces cancel for the registered L/R-asymmetric assignment.")
        print("This checks algebraic consistency of the assignment; it is not a standalone derivation of the full spectrum.")
    else:
        print("FAILURE: Anomaly cancellation failed.")
    print("="*60)
    
    results["overall_verdict"] = "PASS" if all_pass else "FAIL"
    results["pass"] = bool(all_pass)
    
    # Save
    out_path = get_output_path("protocol_anomaly_check_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
        
    return results

if __name__ == "__main__":
    run_anomaly_audit()
