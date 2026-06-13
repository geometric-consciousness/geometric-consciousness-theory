import numpy as np
import json
import os
from gct_utils import GCTReporter, get_output_path, PHI

def get_projection_matrix(ratio):
    """
    Returns the canonical 3x6 projection matrix M_perp for a given ratio (slope).
    """
    ip = -1.0 / ratio
    m_perp = np.array([
        [1, ip, 0, -1, ip, 0],
        [ip, 0, 1, ip, 0, -1],
        [0, 1, ip, 0, -1, ip]
    ])
    return m_perp

def compute_resonance_gap(ratio, r_max=3):
    """
    Calculates the Diophantine gap / phason resonance for a given ratio.
    J = min |M_perp * n| for non-zero n in Z^6.
    """
    m_perp = get_projection_matrix(ratio)
    
    # Generate Z^6 lattice points in a cube [-r_max, r_max]^6
    coords = np.arange(-r_max, r_max + 1)
    grid = np.meshgrid(*([coords] * 6))
    points = np.stack(grid, axis=-1).reshape(-1, 6)
    
    # Remove the origin
    points = points[np.any(points != 0, axis=1)]
    
    # Project into E_perp
    projections = points @ m_perp.T
    norms = np.linalg.norm(projections, axis=1)
    
    return float(np.min(norms))

def run_phi_scan():
    reporter = GCTReporter("Phi Selection Scan")
    
    # Ratios to compare
    ratios = {
        "phi": PHI,
        "silver": 1 + np.sqrt(2),
        "bronze": (3 + np.sqrt(13)) / 2,
        "pi": np.pi,
        "rational": 1.5
    }
    
    gaps = {}
    reporter.section("Diophantine Gap Comparison")
    
    for name, val in ratios.items():
        gap = compute_resonance_gap(val)
        gaps[f"{name}_gap"] = gap
        reporter.log_value(f"{name.capitalize()} Gap", f"{gap:.6f}")
    
    # Check if Phi is optimal among these candidates
    # Note: In 6D, phi might not be the global max, but we check if it beats these classics.
    is_optimal = gaps["phi_gap"] >= max(gaps.values())
    
    reporter.section("Optimality Audit")
    reporter.log_value("Is Phi Optimal (Local Candidate Set)?", is_optimal)
    
    # Output JSON
    results = {
        "protocol": "protocol_phi_selection.py",
        "phi_gap": gaps["phi_gap"],
        "silver_gap": gaps["silver_gap"],
        "is_optimal": is_optimal,
        "all_gaps": gaps,
        "pass": is_optimal
    }
    
    output_path = get_output_path("protocol_phi_selection_results.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    
    reporter.verdict(True, "Phi selection scan complete.")
    return results

if __name__ == "__main__":
    run_phi_scan()
