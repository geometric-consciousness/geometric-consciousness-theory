#!/usr/bin/env python3
"""
protocol_quark_mismatch_scaling.py — FK Determinant Finite-Size Scaling
========================================================================
Objective: Test whether the m_d residual under the engine's tree-level FK
construction closes toward PDG 2024 (m_d = 4.70 MeV) as the icosahedral cage size
N -> infinity, or whether it surfaces a structural issue.

Method:
  1. Construct an enlarged 6D lattice (R=4, perp_cutoff=3.0).
  2. Identify the natural icosahedral shells via gaps in the sorted |x_perp|
     sequence.
  3. At each shell boundary N, build the adjacency D_F with edges between
     nodes whose ambient-space distance is exactly 1.0, weight phi.
  4. Compute the FK gap ratio via gct_spectrum.SpectrumAnalyzer.
  5. Tabulate fk_det vs N and compare to the heuristic target phi^phi.

Output:
  - Scaling table on stdout.
  - JSON file at <output>/fk_scaling.json with the full result.
"""

import sys
import io
import json
import math
from pathlib import Path

import numpy as np

# Force UTF-8 stdout for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

_SRC = Path(__file__).resolve().parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from gct_utils import C, get_output_path
from gct_lattice import GCTLattice
import gct_projections as proj
from gct_hamiltonian import GCTHamiltonian
from gct_spectrum import SpectrumAnalyzer


def discover_shells(norms_sorted, gap_threshold=0.005, n_max=3000):
    """Locate natural icosahedral shell boundaries in the |x_perp| sequence."""
    gaps = np.diff(norms_sorted[:n_max])
    breaks = np.where(gaps > gap_threshold)[0]
    shells = []
    for idx in breaks:
        N_shell = int(idx) + 1
        shells.append({
            "N": N_shell,
            "perp_cut": float(norms_sorted[idx]),
            "perp_next": float(norms_sorted[idx + 1]),
            "gap": float(gaps[idx]),
        })
    return shells


def build_adjacency(nodes, phi, tol=1e-4):
    """Adjacency with edges of weight phi where |ambient_dist - 1.0| < tol."""
    N = len(nodes)
    diffs = nodes[:, None, :] - nodes[None, :, :]
    dists = np.linalg.norm(diffs, axis=2)
    mask = np.abs(dists - 1.0) < tol
    np.fill_diagonal(mask, False)
    D_F = np.where(mask, phi, 0.0)
    edges = int(mask.sum() // 2)
    return D_F, edges


def fk_at(N, x_eq, ordered_indices, lat, analyzer, phi):
    """Compute FK gap ratio for the first N perp-sorted nodes."""
    if N > len(ordered_indices):
        return None
    idx = ordered_indices[:N]
    nodes = x_eq[idx]
    D_F, edges = build_adjacency(nodes, phi)
    if edges == 0:
        return {"N": N, "edges": 0, "fk_det": None, "note": "no edges"}
    try:
        out = analyzer.compute_fuglede_kadison_determinant(D_F)
        return {
            "N": N,
            "edges": edges,
            "fk_det": float(out["fk_determinant"]),
            "lambda_max": float(out["lambda_max"]),
            "lambda_mid": float(out["lambda_mid"]),
            "lambda_min": float(out["lambda_min"]),
        }
    except Exception as e:
        return {"N": N, "edges": edges, "fk_det": None, "error": str(e)}


def main():
    phi = float(C.PHI)
    m_e = float(C.M_E_OBS)
    m_u = m_e * (phi ** 3)
    target_pdg = 4.70
    target_heuristic = phi ** phi

    print("=" * 78)
    print("FK Determinant Finite-Size Scaling — Down Quark Mass Closure Test")
    print("=" * 78)
    print(f"  m_u = m_e * phi^3                  = {m_u:.6f} MeV")
    print(f"  Heuristic target (phi^phi)         = {target_heuristic:.6f}")
    print(f"  PDG m_d                            = {target_pdg:.4f} MeV")
    print(f"  m_d if FK = phi^phi (heuristic)   = {m_u * target_heuristic:.4f} MeV")
    print(f"  m_d if FK = sqrt(3) (engine R=2)  = {m_u * math.sqrt(3):.4f} MeV")
    print()

    # Enlarged lattice
    lat = GCTLattice(R=4, perp_cutoff=3.0)
    x_eq = lat.x_equilibrium
    x_perp = proj.project_perp(x_eq)
    norms = np.linalg.norm(x_perp, axis=1)
    order = np.argsort(norms)
    nonzero = order[norms[order] > 1e-6]
    norms_sorted = norms[nonzero]
    print(f"Lattice generated: {len(x_eq)} total, {len(nonzero)} non-origin nodes.")
    print(f"|x_perp| range = [{norms_sorted[0]:.4f}, {norms_sorted[-1]:.4f}]")
    print()

    shells = discover_shells(norms_sorted)
    print(f"Discovered {len(shells)} natural shell boundaries (gap > 0.005) within N<=3000.")
    print()

    analyzer = SpectrumAnalyzer(lat, GCTHamiltonian(lat))

    print(f'{"N":>6} {"|x_perp| cut":>13} {"edges":>8} {"fk_det":>10} '
          f'{"m_d (MeV)":>11} {"err vs PDG":>11} {"vs phi^phi":>11}')
    print("-" * 78)

    rows = []
    for shell in shells[:25]:
        N = shell["N"]
        r = fk_at(N, x_eq, nonzero, lat, analyzer, phi)
        if r is None:
            continue
        rows.append({**r, "perp_cut": shell["perp_cut"]})
        if r["fk_det"] is None:
            print(f'{N:>6} {shell["perp_cut"]:>13.4f} {r["edges"]:>8}  --- no FK ---')
            continue
        m_d = m_u * r["fk_det"]
        err_pdg = (m_d - target_pdg) / target_pdg * 100.0
        ratio_heur = r["fk_det"] / target_heuristic
        print(f'{N:>6} {shell["perp_cut"]:>13.4f} {r["edges"]:>8} '
              f'{r["fk_det"]:>10.6f} {m_d:>11.4f} '
              f'{err_pdg:>+10.2f}% {ratio_heur:>+10.4f}x')

    # Persist results
    out = {
        "constants": {
            "phi": phi,
            "m_e_mev": m_e,
            "m_u_mev": m_u,
            "target_pdg_mev": target_pdg,
            "target_heuristic_phi_phi": target_heuristic,
        },
        "lattice": {
            "R": 4,
            "perp_cutoff": 3.0,
            "total_nodes": len(x_eq),
            "non_origin_nodes": len(nonzero),
        },
        "shells_discovered": shells,
        "fk_scaling_rows": rows,
    }
    out_path = get_output_path("fk_scaling.json")
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print()
    print(f"Saved scaling data to: {out_path}")

    print()
    print("Algebraic identification of N=634 (the R=2 cage):")
    r_634 = next((r for r in rows if r["N"] == 634), None)
    if r_634 and r_634["fk_det"] is not None:
        print(f"  lambda_min = {r_634['lambda_min']:.6f}   vs sqrt(2)    = {math.sqrt(2):.6f}")
        print(f"  lambda_mid = {r_634['lambda_mid']:.6f}   vs phi*sqrt(2)= {phi*math.sqrt(2):.6f}")
        print(f"  lambda_max = {r_634['lambda_max']:.6f}   vs phi*sqrt(6)= {phi*math.sqrt(6):.6f}")
        print(f"  fk_det     = {r_634['fk_det']:.6f}   vs sqrt(3)    = {math.sqrt(3):.6f}")
        print(f"  fk_det != phi^phi ({target_heuristic:.6f}); ratio = {r_634['fk_det']/target_heuristic:.4f}")


if __name__ == "__main__":
    main()
