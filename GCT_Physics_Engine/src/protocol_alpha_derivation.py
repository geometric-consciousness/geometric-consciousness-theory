#!/usr/bin/env python3
"""
protocol_alpha_derivation.py — Fine Structure Constant Derivation
=================================================================
Establish the bare geometric tree-level prediction for Alpha.

Methodology:
1. Bare Coupling: alpha_0^-1 = 360 * Phi^-2 approx 137.508.
2. Residual: The 0.34% shift to CODATA identifies Phason Anti-Screening.
"""

import json
import math
import numpy as np
from pathlib import Path

# GCT Imports
from gct_alpha import AlphaCalculator
from gct_utils import C, get_output_path, resolve_a3

# Verification target (CODATA): empirical comparison value only; the
# derivation input is AlphaCalculator.compute_geometric_impedance().
_, ALPHA_INV_OBS = resolve_a3(C)

# Verification gate: broad tree-level tolerance for the bare alpha check,
# not a tuned model parameter.
TOLERANCE_PPM = 5000
FORMULA_REL_TOL = 1.0e-12


def evaluate_alpha_derivation(
    alpha_calc_inv: float,
    *,
    alpha_obs_inv: float = ALPHA_INV_OBS,
    formula_expected_inv: float | None = None,
    tolerance_ppm: float = TOLERANCE_PPM,
) -> dict:
    """Evaluate the external comparison and internal regression separately.

    ``alpha_obs_inv`` is the independent CODATA comparison target.  The
    formula regression only checks that the implementation still evaluates
    ``360 * phi**-2``; it is not empirical evidence for that formula.
    """
    if formula_expected_inv is None:
        formula_expected_inv = 360.0 * float(C.PHI) ** -2
    if alpha_obs_inv <= 0 or tolerance_ppm <= 0:
        raise ValueError("alpha observation and registered tolerance must be positive")

    formula_regression_pass = math.isclose(
        alpha_calc_inv,
        formula_expected_inv,
        rel_tol=FORMULA_REL_TOL,
        abs_tol=FORMULA_REL_TOL,
    )
    diff = alpha_calc_inv - alpha_obs_inv
    ppm_error = abs(diff) / alpha_obs_inv * 1e6
    external_comparison_pass = (
        abs(diff) <= alpha_obs_inv * tolerance_ppm / 1_000_000.0
    )
    verdict = (
        "OPEN_CONDITIONAL"
        if formula_regression_pass and external_comparison_pass
        else "FAIL"
    )

    return {
        "alpha_bare_inv": alpha_calc_inv,
        "alpha_obs_inv": alpha_obs_inv,
        "ppm_error": ppm_error,
        "derivation": "Tree-Level Bare Geometric Impedance (360 * phi^-2)",
        "residual_target": f"Phason Anti-Screening ({ppm_error/1e4:.2f}%)",
        "status": verdict,
        "external_comparison_scope": "CODATA 2022 alpha^-1 empirical comparison",
        "external_comparison_tolerance_ppm": tolerance_ppm,
        "external_comparison_pass": external_comparison_pass,
        "external_target_provenance": (
            "Mohr, Newell, Taylor & Tiesinga (2025), CODATA Recommended "
            "Values of the Fundamental Physical Constants: 2022, Rev. Mod. "
            "Phys. 97, 025002, DOI 10.1103/RevModPhys.97.025002"
        ),
        "formula_expected_inv": formula_expected_inv,
        "formula_regression_rel_tolerance": FORMULA_REL_TOL,
        "formula_regression_pass": formula_regression_pass,
        "formula_regression_scope": (
            "Internal implementation regression only; not external validation"
        ),
        "tree_level_within_0p5pct_band": external_comparison_pass,
        "precision_validation_pass": False,
        "status_note": (
            f"Tree-level residual {ppm_error:.1f} ppm against independent CODATA 2022; "
            "Tier 3 numerical residual pending O.5 (1/(2N) integer-factor closure) "
            "and O.19 (phason 1-loop magnitude closure). The registered 5000 ppm "
            "comparison is a broad tree-level band, not precision validation. "
            f"Internal 360*phi^-2 formula regression: {formula_regression_pass}."
        ),
        "verdict": verdict,
        "pass": False,
        "pass_interpretation": (
            "False by design: reproducing 360*phi^-2 is an internal regression, "
            "while agreement with CODATA is only within the broad tree-level band; "
            "the claim remains OPEN_CONDITIONAL pending O.5/O.19."
        ),
    }

def run_alpha_derivation():
    print("="*60)
    print("GCT Protocol: Fine Structure Constant Derivation")
    print("="*60)
    
    # 1. Bare Coupling (Geometric Impedance)
    print("\n1. Calculating Bare Geometric Impedance...")
    alpha_calc_inv = AlphaCalculator.compute_geometric_impedance()
    print(f"   Formula: 360 * Phi^-2")
    print(f"   Alpha_Calc^-1: {alpha_calc_inv:.6f}")
    
    # 2. Verification target (CODATA); not a derivation input.
    print("\n2. Comparison with Observation (CODATA)...")
    print(f"   Target:   {ALPHA_INV_OBS:.6f}")
    print(f"   Derived:  {alpha_calc_inv:.6f}")
    
    results = evaluate_alpha_derivation(alpha_calc_inv)
    diff = alpha_calc_inv - ALPHA_INV_OBS
    ppm_error = results["ppm_error"]
    
    print(f"\n3. Result Analysis")
    print(f"   Discrepancy: {diff:.6f}")
    print(f"   PPM Error:   {ppm_error:.1f} ppm ({ppm_error/1e4:.2f}%)")

    print("\n[PHYSICAL INTERPRETATION]")
    print("Tier 3 numerical relation (Tier 3 360 multiplier; mechanism open, RT solid-angle construction withdrawn): alpha^-1 = 360 * phi^-2.")
    print(f"Tier 3 bare residual: {int(round(ppm_error))} ppm pending")
    print("QLQCD-1L closure of the phason anti-screening residual (O.5/O.19).")

    verdict = results["verdict"]
    
    # Save
    out_path = get_output_path("protocol_alpha_derivation_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
        
    print("\n" + "="*60)
    if verdict == "OPEN_CONDITIONAL":
        print(
            f"Status: OPEN_CONDITIONAL — Tree-level residual {ppm_error:.1f} ppm; "
            "Tier 3 numerical residual pending O.5 (1/(2N) integer-factor closure) "
            "and O.19 (phason 1-loop magnitude closure). Within 0.5% tolerance "
            "band but NOT a precision validation."
        )
    else:
        print("FAIL: external 5000 ppm band or internal formula regression failed.")
    print("="*60)
    
    return results

if __name__ == "__main__":
    run_alpha_derivation()
