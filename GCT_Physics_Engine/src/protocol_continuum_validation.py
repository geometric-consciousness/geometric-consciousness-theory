#!/usr/bin/env python3
"""
protocol_continuum_validation.py — Speed of Light & Lorentz Check
===========================================================================
Validates the emergence of a relativistic continuum from the Phason branch.

Metrics:
1. Measured Phason Speed (c_meas) from Hessian dispersion.
2. Comparison with Theoretical c = Phi^-9.

Generates:
- dual_dispersion.png
- continuum_report.json
"""

import numpy as np
import json
import os
import matplotlib.pyplot as plt

# GCT Imports
from gct_lattice import GCTLattice
from gct_hamiltonian import GCTHamiltonian
from gct_stability import LatticeRelaxer
from gct_lorentz import DispersionAnalyzer
from gct_utils import get_output_path, C

# ── Lattice-resolution toggle ──────────────────────────────────────────────────────────
# FULL_LATTICE_MODE=True uses an R>=10 lattice; the claim is that c_phason
# converges to Phi^-9 = 0.01316 within 10%. The default R=1 mode applies the
# SAME 10% tolerance (the former 2500% R=1 tolerance, which
# passed an 18x miss and the c_meas=0 failure path, is retired). No R>=10 run
# is registered, so the default result is open.
FULL_LATTICE_MODE = os.environ.get("GCT_CONTINUUM_FULL", "0") == "1"

def run_continuum_validation():
    print("="*60)
    print("GCT Protocol: Continuum & Lorentz Validation (Phason Branch)")
    print("="*60)

    c_hat_val = float(C.PHI)**-9

    # ── Analytic-formula mode vs full-lattice mode ─────────────────────────────────────────
    if not FULL_LATTICE_MODE:
        print("[Fast Verification Mode] Running low-resolution convergence certificate (R=1).")
        print("NOTE: Desktop gate uses the finite-size convergence certificate; set GCT_CONTINUUM_FULL=1 for the expensive R>=10 scan.")
        R_val = 1
        tolerance = 0.10
    else:
        print(f"[Full Scan Mode] R>=10 lattice: c_phason converges to Phi^-9 = {c_hat_val:.6f}")
        R_val = 10
        tolerance = 0.10

    # 1. Setup Lattice
    print(f"Initializing Validated Lattice (R={R_val}, Cutoff=1.5)...")
    lattice = GCTLattice(R=R_val, perp_cutoff=1.5)
    print(f"Lattice Nodes: {lattice.N_nodes}")
    print(f"System DOFs:   {lattice.N_nodes * 6}")
    
    hamiltonian = GCTHamiltonian(lattice)
    relaxer = LatticeRelaxer(tol=1e-5)
    analyzer = DispersionAnalyzer(relaxer)
    
    # 2. Relax first to ensure ground state
    print("Relaxing to ground state...")
    relaxer.relax_structure(lattice, hamiltonian)
    
    # 3. Analyze Spectrum
    print("\nAnalyzing Full Spectrum (Hessian Diagonalization)...")
    direction = np.array([1.0, 0.0, 0.0])
    
    data = analyzer.analyze_spectrum(lattice, hamiltonian, direction)
    
    # 4. Plot and Extract Slope
    print("\nGenerating Dispersion Plot...")
    
    c_meas = analyzer.plot_dual_dispersion(
        data, 
        filename=get_output_path("dual_dispersion.png"),
        target_c=c_hat_val
    )
    
    print(f"\nMeasured Phason Speed (c): {c_meas:.6f}")
    print(f"Theoretical Target (Phi^-9): {c_hat_val:.6f}")
    
    deviation = abs(c_meas - c_hat_val) / c_hat_val if c_meas > 0 else 1.0
    print(f"Deviation: {deviation*100:.2f}%")
    
    passed = bool(c_meas > 0 and deviation <= tolerance)
    verdict = (
        "PHASON_SPEED_WITHIN_10PCT_OF_PHI_M9" if passed
        else f"R{R_val}_PHASON_SPEED_NOT_CONVERGED_TO_PHI_M9"
    )
    
    # 5. Save Report
    report = {
        "c_measured": c_meas,
        "c_theory": c_hat_val,
        "deviation_percent": deviation * 100,
        "tolerance_relative": tolerance,
        "pass": passed,
        "verdict": verdict,
        "proxy_status": "R=1 under-resolved run with the 10% tolerance; the R>=10 scan (GCT_CONTINUUM_FULL=1) is not registered" if not FULL_LATTICE_MODE else None,
        "large_matrix_mode": FULL_LATTICE_MODE,
        "full_lattice_mode": FULL_LATTICE_MODE,
        "status": "Passed" if passed else "Failed",
        "mode_counts": {
            "phonon": len(data.get("phonon", {}).get("k", [])),
            "phason": len(data.get("phason", {}).get("k", []))
        }
    }
    
    with open(get_output_path("protocol_continuum_validation_results.json"), "w") as f:
        json.dump(report, f, indent=2)
        
    print("\nValidation Complete.")
    
    if passed:
        print("[SUCCESS] Relativistic Phason speed confirmed!")
    else:
        print(f"[OPEN] {verdict}: c_meas misses Phi^-9 by more than 10% at R={R_val}.")
        
    return report

if __name__ == "__main__":
    run_continuum_validation()
