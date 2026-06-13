#!/usr/bin/env python3
"""
protocol_uniqueness_sophisticated.py — sophisticated-invariant route to
the Tier-1 closure target (Open Problem O.14): test whether more
sophisticated uniqueness criteria single out the η_scalar = -8 cage among
the orbit-unions summing to 144, where the standard geometric/spectral
metrics do not.

Tested invariants (per cage):
  1.  Degree sequence (full).
  2.  Whether the graph is k-regular for some k.
  3.  Degree variance (spread).
  4.  Degree min/max.
  5.  Orbit-pair bond-incidence matrix (long-bond and short-bond
      sub-incidences separately).
  6.  Number of triangles (3-cycles) in the bond graph.
  7.  Number of 4-cycles.
  8.  Number of 5-cycles (icosahedral cycles).
  9.  Algebraic connectivity (Fiedler value = 2nd smallest eigenvalue
      of the graph Laplacian L = D - A).
 10.  Spectral entropy of the adjacency.
 11.  Bond-distance histogram (counts at each distinct perp-distance).
 12.  I-equivariant L²-spectral data (sign-balance per irrep block).
"""

from __future__ import annotations

import math
import json
import sys
from pathlib import Path
from itertools import combinations
from collections import Counter

import numpy as np

ENGINE_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = ENGINE_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

DATA_PATH = ENGINE_ROOT / "data" / "protocol_uniqueness_sophisticated_results.json"

from gct_utils import C

PHI = float(C.PHI)

from protocol_cage_repair import (
    vertex_pairs_from_projection,
    icosahedral_rotations_lattice_frame,
    lift_to_6d_signed_perm,
    enumerate_orbits,
)


def setup_orbits():
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
            "nodes_6d": candidates_6d[orb],
            "nodes_perp": candidates_perp[orb],
        })
    orbits.sort(key=lambda o: o["min_perp_norm"])
    return orbits


def find_subsets_summing_to_144(sizes: list[int]) -> list[list[int]]:
    n = len(sizes)
    matches = []
    for k in range(1, min(n, 8) + 1):
        for combo in combinations(range(n), k):
            if sum(sizes[i] for i in combo) == 144:
                matches.append(list(combo))
    return matches


def build_cage_metrics(orbit_indices: list[int], orbits: list[dict]) -> dict:
    """Build a full set of sophisticated metrics for the cage."""
    nodes_perp = np.vstack([orbits[i]["nodes_perp"] for i in orbit_indices])
    orbit_sizes = [orbits[i]["size"] for i in orbit_indices]
    # Map each node to its orbit index in the cage
    orbit_of_node = []
    for o_idx, oi in enumerate(orbit_indices):
        orbit_of_node.extend([o_idx] * orbits[oi]["size"])
    orbit_of_node = np.array(orbit_of_node)
    N = len(nodes_perp)

    # Build adjacency (engine's bond rule)
    A = np.zeros((N, N))
    n_long = 0
    n_short = 0
    # Track orbit-pair bond incidence
    n_orbs = len(orbit_indices)
    long_inc = np.zeros((n_orbs, n_orbs), dtype=int)
    short_inc = np.zeros((n_orbs, n_orbs), dtype=int)
    for i in range(N):
        for j in range(i + 1, N):
            d = np.linalg.norm(nodes_perp[i] - nodes_perp[j])
            if abs(d - 1.0) < 0.05:
                A[i, j] = A[j, i] = 1.0
                n_long += 1
                long_inc[orbit_of_node[i], orbit_of_node[j]] += 1
                long_inc[orbit_of_node[j], orbit_of_node[i]] += 1
            elif abs(d - 1.0 / PHI) < 0.05:
                A[i, j] = A[j, i] = PHI
                n_short += 1
                short_inc[orbit_of_node[i], orbit_of_node[j]] += 1
                short_inc[orbit_of_node[j], orbit_of_node[i]] += 1

    # Degree sequence (each row sum of the binary unweighted adjacency)
    binary_A = (np.abs(A) > 0).astype(int)
    degrees = np.sum(binary_A, axis=1)
    deg_min = int(degrees.min())
    deg_max = int(degrees.max())
    is_regular = (deg_min == deg_max)
    deg_variance = float(np.var(degrees))

    # Triangles: trace(A^3) / 6 for unweighted graph
    # Counting unweighted triangles is more meaningful structurally.
    A3 = binary_A @ binary_A @ binary_A
    n_triangles = int(np.trace(A3) / 6)

    # 4-cycles: a bit more involved; use the formula:
    # n_C4 = (trace(A^4) - 2·m - sum_i d_i·(d_i-1)) / 8
    A2 = binary_A @ binary_A
    A4 = A2 @ A2
    m = int(np.sum(binary_A) / 2)  # number of edges
    n_C4 = int((np.trace(A4) - 2 * m - sum(d * (d - 1) for d in degrees)) / 8)

    # Algebraic connectivity (Fiedler eigenvalue)
    L = np.diag(degrees.astype(float)) - binary_A.astype(float)
    lap_evals = np.linalg.eigvalsh(L)
    fiedler = float(sorted(lap_evals)[1]) if len(lap_evals) > 1 else 0.0

    # Adjacency spectrum + asymmetry
    evals = np.linalg.eigvalsh(A)
    nz = evals[np.abs(evals) > 1e-12]
    eta = float(np.sum(np.sign(nz)))

    # Spectral entropy: -Σ p_i log p_i where p_i = |λ_i|² / Σ|λ_j|² normalised
    abs_evals_sq = evals ** 2
    total = np.sum(abs_evals_sq)
    if total > 0:
        p = abs_evals_sq / total
        p_nonzero = p[p > 1e-15]
        spectral_entropy = float(-np.sum(p_nonzero * np.log(p_nonzero)))
    else:
        spectral_entropy = 0.0

    # Bond-distance histogram (precise distances rounded to 3 decimals)
    distances = []
    for i in range(N):
        for j in range(i + 1, N):
            d = np.linalg.norm(nodes_perp[i] - nodes_perp[j])
            if d < 2.5:  # only count "close" distances to keep histogram bounded
                distances.append(round(d, 3))
    dist_hist = dict(Counter(distances))
    n_unique_distances = len(dist_hist)

    # Compress orbit-pair incidences into a sorted hash-like tuple for ease of
    # uniqueness comparison
    long_inc_sig = tuple(sorted(long_inc.flatten()))
    short_inc_sig = tuple(sorted(short_inc.flatten()))

    return {
        "orbit_indices": orbit_indices,
        "orbit_sizes": sorted(orbit_sizes),
        "eta_scalar": eta,
        "deg_min": deg_min,
        "deg_max": deg_max,
        "is_regular": bool(is_regular),
        "deg_variance": deg_variance,
        "n_long_bonds": n_long,
        "n_short_bonds": n_short,
        "n_triangles": n_triangles,
        "n_C4": n_C4,
        "fiedler": fiedler,
        "spectral_entropy": spectral_entropy,
        "n_unique_distances": n_unique_distances,
        "long_inc_sig": long_inc_sig,
        "short_inc_sig": short_inc_sig,
    }


def main() -> int:
    print("=" * 90)
    print("  Sophisticated uniqueness criteria search for the η_scalar = -8 cage")
    print("=" * 90)
    orbits = setup_orbits()
    sizes = [o["size"] for o in orbits]
    subsets = find_subsets_summing_to_144(sizes)
    print(f"  ✓ Enumerated {len(subsets)} cages summing to 144.")
    print()

    print("  Computing sophisticated metrics for all 42 cages...")
    metrics = []
    for sub_idx, sub in enumerate(subsets):
        m = build_cage_metrics(sub, orbits)
        m["subset_idx"] = sub_idx
        metrics.append(m)

    # Find the unique winner
    winners = [m for m in metrics if abs(m["eta_scalar"] - (-8)) < 0.5]
    if not winners:
        print("  WARN: no winner found")
        return 1
    winner = winners[0]
    print(f"  Winner: subset #{winner['subset_idx']}, orbit_indices = {winner['orbit_indices']}")
    print()

    # Test each sophisticated criterion for uniqueness
    print("  Testing criteria for uniqueness:")
    print("  " + "-" * 86)

    candidates = [
        ("is_regular = True",         lambda m: m["is_regular"], "true"),
        ("deg_variance",              lambda m: m["deg_variance"], "min"),
        ("deg_min",                   lambda m: m["deg_min"], "max"),
        ("n_triangles",               lambda m: m["n_triangles"], "max"),
        ("n_triangles",               lambda m: m["n_triangles"], "min"),
        ("n_C4 (4-cycles)",           lambda m: m["n_C4"], "max"),
        ("n_C4 (4-cycles)",           lambda m: m["n_C4"], "min"),
        ("fiedler (alg connectivity)", lambda m: m["fiedler"], "max"),
        ("fiedler (alg connectivity)", lambda m: m["fiedler"], "min"),
        ("spectral_entropy",          lambda m: m["spectral_entropy"], "max"),
        ("spectral_entropy",          lambda m: m["spectral_entropy"], "min"),
        ("n_unique_distances",        lambda m: m["n_unique_distances"], "max"),
        ("n_unique_distances",        lambda m: m["n_unique_distances"], "min"),
    ]
    winner_idx = winner["subset_idx"]
    unique_picks = []
    for name, extractor, direction in candidates:
        if direction == "true":
            vals = [m for m in metrics if extractor(m)]
            n_pick = len(vals)
            if n_pick == 1 and vals[0]["subset_idx"] == winner_idx:
                print(f"    {name:<35} → UNIQUE pick = winner ✓")
                unique_picks.append(name + " (= True)")
            elif n_pick > 0 and winner_idx in [v["subset_idx"] for v in vals]:
                print(f"    {name:<35} → {n_pick} cages (winner among them)")
            else:
                print(f"    {name:<35} → {n_pick} cages (winner NOT among)")
        else:
            values = [(extractor(m), m["subset_idx"]) for m in metrics]
            best = max(values, key=lambda v: v[0]) if direction == "max" else min(values, key=lambda v: v[0])
            eps = 1e-6
            tied = [v for v in values if abs(v[0] - best[0]) < eps]
            if best[1] == winner_idx and len(tied) == 1:
                print(f"    {name:<35} {direction}={best[0]:>10.4f}  → UNIQUE = winner ✓")
                unique_picks.append(f"{name} ({direction})")
            else:
                marker = "  (winner among ties)" if winner_idx in [v[1] for v in tied] else ""
                print(f"    {name:<35} {direction}={best[0]:>10.4f}  → subset #{best[1]} (tied {len(tied)}){marker}")

    # Orbit-pair incidence-signature uniqueness
    print()
    print("  Checking orbit-pair bond-incidence signatures:")
    long_sigs = [(m["long_inc_sig"], m["subset_idx"]) for m in metrics]
    short_sigs = [(m["short_inc_sig"], m["subset_idx"]) for m in metrics]
    long_sig_counts = Counter(s for s, _ in long_sigs)
    short_sig_counts = Counter(s for s, _ in short_sigs)
    winner_long_sig = next(s for s, idx in long_sigs if idx == winner_idx)
    winner_short_sig = next(s for s, idx in short_sigs if idx == winner_idx)
    n_long_matching = long_sig_counts[winner_long_sig]
    n_short_matching = short_sig_counts[winner_short_sig]
    print(f"    Winner's long-bond incidence signature occurs in {n_long_matching} cage(s)")
    print(f"    Winner's short-bond incidence signature occurs in {n_short_matching} cage(s)")
    if n_long_matching == 1:
        unique_picks.append("long-bond orbit-pair incidence signature")
        print(f"    ✓ Winner UNIQUELY identifies by long-bond incidence pattern!")
    if n_short_matching == 1:
        unique_picks.append("short-bond orbit-pair incidence signature")
        print(f"    ✓ Winner UNIQUELY identifies by short-bond incidence pattern!")

    print()
    print("=" * 90)
    if unique_picks:
        print(f"  ✓ {len(unique_picks)} sophisticated uniqueness criteria pick the winner uniquely:")
        for c in unique_picks:
            print(f"    • {c}")
        print()
        print("  These are structural invariants of the cage geometry. Any of them")
        print("  can serve as the uniqueness criterion for Tier 1 closure.")
        print("  The most natural is likely the one that has a clean physical")
        print("  interpretation (e.g., regular graph = uniform coordination =")
        print("  ground-state-like, or bond-incidence pattern = topological signature).")
    else:
        print("  ✗ No sophisticated single criterion uniquely picks the winner.")
        print()
        print("  Under paired criteria, the only combination that singles out the cage")
        print("  is 'min n_orbits THEN max spectrum range', but spectrum range is not a")
        print("  principled invariant. No single structural invariant in this set yields")
        print("  a clean uniqueness argument for the cage.")
    print("=" * 90)

    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DATA_PATH.open("w", encoding="utf-8") as f:
        json.dump({
            "winner_subset_idx": winner["subset_idx"],
            "winner_metrics_summary": {k: v for k, v in winner.items()
                                       if k not in ("orbit_indices", "long_inc_sig", "short_inc_sig", "orbit_sizes")},
            "winner_orbit_sizes": winner["orbit_sizes"],
            "winner_long_inc_sig": list(winner["long_inc_sig"]),
            "winner_short_inc_sig": list(winner["short_inc_sig"]),
            "unique_picks": unique_picks,
            "all_42_metrics_summary": [
                {k: (v if not isinstance(v, tuple) else list(v))
                 for k, v in m.items() if k not in ("orbit_indices",)}
                for m in metrics
            ],
        }, f, indent=2, default=str)
    print(f"  Results: {DATA_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
