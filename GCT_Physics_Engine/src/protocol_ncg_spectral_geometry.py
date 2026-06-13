#!/usr/bin/env python3
"""
protocol_ncg_spectral_geometry.py
Extracting the mass indices (11, 17) from the raw eigenvalues of the N=144
reference cage diagnostic.

Theory:
The lepton hierarchy emerges as the resonant modes of the dodecahedral cage.
This protocol tests if the topological graph of the cage natively possesses
spectral features (gaps) at indices 11 and 17. Protocols that require the
canonical finite Dirac operator D_F use the 152-node I_h-closed cage.
"""

import numpy as np
import sys
import os
import json

# Add GCT Physics Engine src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from gct_utils import get_output_path, C

def run_spectral_geometry():
    print("Initializing protocol_ncg_spectral_geometry...")
    
    # Build the Adjacency Matrix (A) for the I_h-closed AKN cage.
    # Uses cage_builder.build_canonical_cage(size=152) -- the smallest
    # I_h-closed orbit-union at perp_cutoff = 2.0 that includes the
    # outermost 60-orbit required for I_h-symmetric spectral analysis.
    from cage_builder import build_canonical_cage
    _, nodes_perp = build_canonical_cage(size=152)
    N = nodes_perp.shape[0]

    # Golden-weighted adjacency in perpendicular space, matching the finite
    # Dirac operator described in Ch06: unit-distance bonds carry weight 1,
    # phi^-1-distance bonds carry weight phi.
    A = np.zeros((N, N))
    phi = float(C.PHI)
    phi_inv = 1.0 / phi
    distance_tolerance = 0.05
    unit_bonds = 0
    phi_bonds = 0

    for i in range(N):
        for j in range(i + 1, N):
            dist = float(np.linalg.norm(nodes_perp[i] - nodes_perp[j]))
            if abs(dist - 1.0) < distance_tolerance:
                A[i, j] = A[j, i] = 1.0
                unit_bonds += 1
            elif abs(dist - phi_inv) < distance_tolerance:
                A[i, j] = A[j, i] = phi
                phi_bonds += 1
                
    # 2. Define the Finite Dirac Operator (D_F) as the Adjacency Matrix
    # (Simplified spectral representation for discrete NCG)
    D_F = A
    
    # 3. Compute complete eigenvalue spectrum
    print(f"Computing eigenvalues for N={N} graph...")
    lambdas = np.linalg.eigvalsh(D_F)
    
    # Sort lambdas in descending magnitude for spectral gap analysis
    # We are looking for the "octave" gaps in the vibrational spectrum
    lambdas_sorted = np.sort(np.abs(lambdas))[::-1]
    
    # 4. Calculate Spectral Gaps
    # delta_lambda_k = |lambda_k - lambda_{k+1}|
    gaps = np.abs(np.diff(lambdas_sorted))
    
    # 5. Search for Gaps at Index 11 and 17
    # Note: Indexing in Python is 0-based. 11th gap is gaps[10], 17th is gaps[16].
    gap_11 = gaps[10]
    gap_17 = gaps[16]
    
    # Calculate gap significance (deviation from mean gap)
    mean_gap = np.mean(gaps)
    std_gap = np.std(gaps)
    
    sig_11 = (gap_11 - mean_gap) / std_gap
    sig_17 = (gap_17 - mean_gap) / std_gap
    
    # Require > 2 sigma for Tier 2 status; otherwise retain Tier 3.
    success_11 = sig_11 > 2.0
    success_17 = sig_17 > 2.0
    
    tier = 2 if (success_11 and success_17) else 3
    
    result_note = ""
    if tier == 2:
        result_note = "Clear spectral features detected at indices 11 and 17. Hierarchy is natively encoded."
    else:
        result_note = f"Bare graph eigenvalues show weak clustering (sig11={sig_11:.2f}, sig17={sig_17:.2f}). Geometric indices 11 and 17 remain a Structural Ansatz (Tier 3) pending full non-linear phason dressing."

    print(f"Gap 11 Significance: {sig_11:.2f} sigma")
    print(f"Gap 17 Significance: {sig_17:.2f} sigma")
    print(f"Verdict: {result_note}")
    
    finite_spectrum = bool(np.all(np.isfinite(lambdas_sorted)) and np.all(np.isfinite(gaps)))
    index_available = bool(len(gaps) > 17)
    audit_pass = bool(finite_spectrum and index_available and tier in (2, 3))

    results = {
        "N_nodes": N,
        "eigenvalues_abs_sorted": lambdas_sorted.tolist()[:30],
        "gaps": gaps.tolist()[:30],
        "gap_11_sig": float(sig_11),
        "gap_17_sig": float(sig_17),
        "mean_gap": float(mean_gap),
        "tier": tier,
        "note": result_note,
        "operator_construction": "golden-weighted perpendicular-space adjacency on build_canonical_cage(size=152): distance 1 -> weight 1, distance phi^-1 -> weight phi",
        "unit_distance_bonds": int(unit_bonds),
        "phi_inverse_distance_bonds": int(phi_bonds),
        "finite_spectrum": finite_spectrum,
        "index_available": index_available,
        "spectral_closure_pass": bool(tier == 2),
        "pass_interpretation": "Engine execution/tier-disclosure pass; spectral_closure_pass carries the physics-closure status.",
        "pass": audit_pass
    }
    
    out_path = get_output_path("protocol_ncg_spectral_geometry_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=4)
        
    return results

if __name__ == "__main__":
    run_spectral_geometry()
