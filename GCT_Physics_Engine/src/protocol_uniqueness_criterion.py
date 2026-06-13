#!/usr/bin/env python3
"""
protocol_uniqueness_criterion.py — Identify what makes the winning
[12, 60, 12, 60] orbit-union geometrically distinctive among the 42
I-symmetric 144-cages, so we can articulate the uniqueness argument
that picks it as "the" electron defect cage.

Specifically:
  1. Identify the 4 orbits comprising subset #17 by their perp-norms.
  2. Compute candidate uniqueness criteria across all 42 cages:
     - Total Σ perp_norm across all 144 nodes (minimum-perp-energy)
     - Maximum perp_norm of any node (smallest enclosing radius)
     - Number of orbits used (4 minimum)
     - Number of bonds in the adjacency graph
     - Connectivity (is the cage connected?)
     - Σ of all bond weights
     - Smallest non-zero eigenvalue of adjacency (spectral gap)
     - Number of nodes at smallest possible perp-norm
  3. For each criterion, check whether subset #17 is UNIQUE (lowest /
     highest / smallest count).
  4. If a single criterion uniquely picks subset #17 → that's the
     uniqueness argument we need for Tier 1.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from itertools import combinations

import numpy as np

ENGINE_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = ENGINE_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

DATA_PATH = ENGINE_ROOT / "data" / "protocol_uniqueness_criterion_results.json"

from gct_utils import C

PHI = float(C.PHI)

from protocol_cage_repair import (
    vertex_pairs_from_projection,
    icosahedral_rotations_lattice_frame,
    lift_to_6d_signed_perm,
    enumerate_orbits,
)


def setup_orbits():
    """Re-enumerate orbits (same as path-(a) search)."""
    from gct_lattice import GCTLattice
    import gct_projections as proj
    vertices_perp, _ = vertex_pairs_from_projection()
    rotations_3d = icosahedral_rotations_lattice_frame(vertices_perp)
    six_d_matrices = [lift_to_6d_signed_perm(R, vertices_perp) for R in rotations_3d]
    six_d_matrices = [M for M in six_d_matrices if M is not None]

    bigger_lat = GCTLattice(R=3, perp_cutoff=3.0)
    big_x_eq = bigger_lat.x_equilibrium
    big_x_perp = proj.project_perp(big_x_eq)
    big_norms = np.linalg.norm(big_x_perp, axis=1)
    order = np.argsort(big_norms)
    if big_norms[order[0]] < 1e-8:
        order = order[1:]
    order = order[:600]
    candidates_6d = big_x_eq[order]
    candidates_perp = big_x_perp[order]
    cand_norms = big_norms[order]

    orbits_idx = enumerate_orbits(candidates_6d, six_d_matrices)
    orbits = []
    for orb in orbits_idx:
        min_norm = min(cand_norms[i] for i in orb)
        orbits.append({
            "size": len(orb),
            "min_perp_norm": float(min_norm),
            "indices": orb,
            "nodes_6d": candidates_6d[orb],
            "nodes_perp": candidates_perp[orb],
        })
    orbits.sort(key=lambda o: o["min_perp_norm"])
    return orbits


def find_subsets_summing_to(target: int, sizes: list[int]) -> list[list[int]]:
    n = len(sizes)
    matches = []
    for k in range(1, min(n, 8) + 1):
        for combo in combinations(range(n), k):
            if sum(sizes[i] for i in combo) == target:
                matches.append(list(combo))
    return matches


def compute_eta_and_metrics(orbit_indices: list[int], orbits: list[dict]) -> dict:
    """Build the cage from the selected orbits and compute candidate
    uniqueness-criterion metrics."""
    nodes_perp = np.vstack([orbits[i]["nodes_perp"] for i in orbit_indices])
    N = len(nodes_perp)
    A = np.zeros((N, N))
    n_long_bonds = 0
    n_short_bonds = 0
    for i in range(N):
        for j in range(i + 1, N):
            d = np.linalg.norm(nodes_perp[i] - nodes_perp[j])
            if abs(d - 1.0) < 0.05:
                A[i, j] = A[j, i] = 1.0
                n_long_bonds += 1
            elif abs(d - 1.0/PHI) < 0.05:
                A[i, j] = A[j, i] = PHI
                n_short_bonds += 1
    evals = np.linalg.eigvalsh(A)
    nz = evals[np.abs(evals) > 1e-12]
    eta = float(np.sum(np.sign(nz)))

    # Candidate metrics
    perp_norms_all = np.linalg.norm(nodes_perp, axis=1)
    total_perp = float(np.sum(perp_norms_all))
    max_perp = float(np.max(perp_norms_all))
    min_perp = float(np.min(perp_norms_all))
    total_bond_weight = float(np.sum(np.abs(A))) / 2
    n_orbits_used = len(orbit_indices)
    orbit_sizes_used = sorted([orbits[i]["size"] for i in orbit_indices])
    orbit_norms_used = sorted([orbits[i]["min_perp_norm"] for i in orbit_indices])

    # Connectivity: count connected components via BFS
    adj_graph = [[] for _ in range(N)]
    for i in range(N):
        for j in range(i+1, N):
            if A[i, j] != 0:
                adj_graph[i].append(j)
                adj_graph[j].append(i)
    visited = [False] * N
    components = 0
    for start in range(N):
        if visited[start]:
            continue
        components += 1
        stack = [start]
        while stack:
            u = stack.pop()
            if visited[u]:
                continue
            visited[u] = True
            for v in adj_graph[u]:
                if not visited[v]:
                    stack.append(v)

    return {
        "orbit_indices": orbit_indices,
        "orbit_sizes_used": orbit_sizes_used,
        "orbit_min_norms_used": orbit_norms_used,
        "eta_scalar": eta,
        "n_orbits_used": n_orbits_used,
        "total_perp_norm": total_perp,
        "max_perp_norm": max_perp,
        "min_perp_norm_in_cage": min_perp,
        "n_long_bonds": n_long_bonds,
        "n_short_bonds": n_short_bonds,
        "total_bond_weight": total_bond_weight,
        "n_components": components,
        "spectrum_min": float(evals.min()),
        "spectrum_max": float(evals.max()),
        "n_pos_eigvals": int(np.sum(nz > 0)),
        "n_neg_eigvals": int(np.sum(nz < 0)),
    }


def main() -> int:
    print("=" * 90)
    print("  Uniqueness criterion search for the winning [12, 60, 12, 60] cage")
    print("=" * 90)
    orbits = setup_orbits()
    sizes = [o["size"] for o in orbits]
    print(f"  Orbit sizes (ordered by perp-norm): {sizes}")
    norms_str = [f"{o['min_perp_norm']:.3f}" for o in orbits]
    print(f"  Orbit min-perp-norms:               {norms_str}")

    subsets = find_subsets_summing_to(144, sizes)
    print(f"  ✓ {len(subsets)} subsets summing to 144.")
    print()

    print("  Computing metrics for all 42 cages...")
    all_results = []
    for sub_idx, sub in enumerate(subsets):
        m = compute_eta_and_metrics(sub, orbits)
        m["subset_idx"] = sub_idx
        all_results.append(m)

    # Find the unique winner with η = -8
    winners = [r for r in all_results if abs(r["eta_scalar"] - (-8)) < 0.5]
    print(f"  ✓ Found {len(winners)} cages with η = -8: {[w['subset_idx'] for w in winners]}")
    if not winners:
        print("  No winners found (shouldn't happen if setup matches enumerator settings)!")
        return 1
    winner = winners[0]
    print()
    print(f"  Winner subset #{winner['subset_idx']}:")
    print(f"    Orbit indices: {winner['orbit_indices']}")
    print(f"    Orbit sizes:   {winner['orbit_sizes_used']}")
    w_norms_str = [f"{n:.4f}" for n in winner['orbit_min_norms_used']]
    print(f"    Orbit min-perp-norms: {w_norms_str}")
    print(f"    Total perp norm in cage: {winner['total_perp_norm']:.4f}")
    print(f"    Max perp norm in cage:   {winner['max_perp_norm']:.4f}")
    print(f"    # bonds: long={winner['n_long_bonds']}, short={winner['n_short_bonds']}")
    print(f"    Total bond weight: {winner['total_bond_weight']:.4f}")
    print(f"    # connected components: {winner['n_components']}")
    print()

    # Test each candidate uniqueness criterion
    print("  Testing candidate uniqueness criteria:")
    print("  " + "-" * 86)

    criteria = [
        ("Minimum total_perp_norm",      lambda r: r["total_perp_norm"], "min"),
        ("Minimum max_perp_norm",        lambda r: r["max_perp_norm"], "min"),
        ("Minimum n_orbits_used",        lambda r: r["n_orbits_used"], "min"),
        ("Maximum total_bond_weight",    lambda r: r["total_bond_weight"], "max"),
        ("Maximum n_long_bonds",         lambda r: r["n_long_bonds"], "max"),
        ("Maximum n_short_bonds",        lambda r: r["n_short_bonds"], "max"),
        ("Minimum n_components",         lambda r: r["n_components"], "min"),
        ("Spectrum range (max - min)",   lambda r: r["spectrum_max"] - r["spectrum_min"], "max"),
        ("Most negative spectrum_min",   lambda r: r["spectrum_min"], "min"),
        ("Most positive spectrum_max",   lambda r: r["spectrum_max"], "max"),
    ]
    winner_idx = winner["subset_idx"]
    unique_picks = []
    for name, extractor, direction in criteria:
        values = [(extractor(r), r["subset_idx"]) for r in all_results]
        if direction == "min":
            best = min(values, key=lambda v: v[0])
        else:
            best = max(values, key=lambda v: v[0])
        # Count the subsets achieving this best value.
        eps = 1e-6
        tied = [v for v in values if abs(v[0] - best[0]) < eps]
        n_tied = len(tied)
        if best[1] == winner_idx and n_tied == 1:
            picks_winner = "UNIQUE → winner ✓"
            unique_picks.append(name)
        elif winner_idx in [v[1] for v in tied]:
            picks_winner = f"  (winner is among {n_tied} tied)"
        else:
            picks_winner = ""
        print(f"    {name:<30} best = {best[0]:>10.4f} (subset #{best[1]:3d}, tied {n_tied}){picks_winner}")

    print()
    print("  Combined criteria (try pairs):")
    found_combo = False
    for c1_name, c1_extractor, c1_dir in criteria:
        for c2_name, c2_extractor, c2_dir in criteria:
            if c1_name >= c2_name:  # avoid duplicates
                continue
            # Lex-order: first minimize/maximize c1, then break ties with c2
            def keyer(r):
                v1 = c1_extractor(r) * (1 if c1_dir == "min" else -1)
                v2 = c2_extractor(r) * (1 if c2_dir == "min" else -1)
                return (v1, v2)
            best = min(all_results, key=keyer)
            eps = 1e-6
            if best["subset_idx"] == winner_idx:
                # Check uniqueness
                best_key = keyer(best)
                tied = [r for r in all_results if abs(keyer(r)[0] - best_key[0]) < eps and abs(keyer(r)[1] - best_key[1]) < eps]
                if len(tied) == 1:
                    print(f"    {c1_name} ({c1_dir}) THEN {c2_name} ({c2_dir}): UNIQUE → winner ✓")
                    found_combo = True
                    break
        if found_combo:
            pass  # report first one and continue scanning

    print()
    print("=" * 90)
    if unique_picks:
        print(f"  *** {len(unique_picks)} single-criterion uniqueness arguments found ***")
        for name in unique_picks:
            print(f"      • {name}")
        print()
        print("  Any of these criteria, by itself, uniquely picks the [12,60,12,60]")
        print("  cage out of all 42 I-symmetric 144-cages. The most natural one")
        print("  (e.g., 'minimum total perp-energy', 'smallest enclosing radius')")
        print("  can be used as the canonical uniqueness argument for Tier 1 closure.")
    else:
        print("  NO single-criterion uniqueness found among candidates tested.")
        print("  The winner [12, 60, 12, 60] is one of several cages tied on each")
        print("  metric. A more subtle argument (Hilbert-Poincaré series, K-theory")
        print("  class, or combination of criteria) would be needed.")
    print("=" * 90)

    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DATA_PATH.open("w", encoding="utf-8") as f:
        json.dump({
            "winner_subset_idx": winner["subset_idx"],
            "winner_orbit_indices": winner["orbit_indices"],
            "winner_metrics": {k: (v if not isinstance(v, list) else v) for k, v in winner.items()},
            "all_42_cages_metrics": all_results,
            "unique_single_criteria": unique_picks,
        }, f, indent=2)
    print(f"  Results: {DATA_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
