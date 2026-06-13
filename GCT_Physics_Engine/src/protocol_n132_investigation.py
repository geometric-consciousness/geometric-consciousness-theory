#!/usr/bin/env python3
"""
protocol_n132_investigation.py - Structural investigation of the N=132
I_h-closed cage that admits integer-arithmetic APS recovery of n = -107.

Background (protocol_aps_cage_search.py): the APS-cage search at
perp_cutoff = 3.5 found three I_h-closed cages where Bulk + eta_eff = -107
closes at integer arithmetic, of which the most physically suggestive is
N = 132 (4-orbit composition; 873 edges; eta_scalar = 0 -> bulk = -107
exactly). The canonical postulate-anchored N = 144 / N = 152 cages do NOT
admit such closure at perp_cutoff = 2.0.

This protocol drills into N = 132:
  1. Identify the 4 I_h orbits that compose it (perp-norms + sizes).
  2. Test bipartiteness of the cage's scalar adjacency graph (2-coloring).
  3. Compute the I-irrep decomposition of the adjacency spectrum
     (like protocol_cage_spectral_decomp.py for the canonical 152-cage).
  4. Verify the eta_scalar = 0 result via per-irrep sign sums.
  5. Compare orbit composition to the canonical N=152 cage and look for
     a natural geometric relation (sub-cage / complement / dual).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ENGINE_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = ENGINE_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

from gct_utils import C
from gct_lattice import GCTLattice
import gct_projections as proj
from protocol_cage_repair import (
    vertex_pairs_from_projection,
    icosahedral_rotations_lattice_frame,
    lift_to_6d_signed_perm,
)

PHI = float(C.PHI)


def build_Ih_60_and_120() -> tuple[list[np.ndarray], list[np.ndarray]]:
    """Return (I-60-rotations, I_h-120-full) as 6x6 signed-perm matrices."""
    vertices_perp, _ = vertex_pairs_from_projection()
    rots3 = icosahedral_rotations_lattice_frame(vertices_perp)
    group60 = []
    for R in rots3:
        M = lift_to_6d_signed_perm(R, vertices_perp)
        if M is None:
            continue
        group60.append(M)
    minus_I6 = -np.eye(6)
    return group60, group60 + [minus_I6 @ M for M in group60]


def full_orbit(seed: tuple[int, ...], group: list[np.ndarray]) -> set[tuple[int, ...]]:
    seed_v = np.array(seed, dtype=np.float64)
    orbit = {seed}
    for M in group:
        mapped = M @ seed_v
        orbit.add(tuple(int(round(c)) for c in mapped))
    return orbit


def build_n132_cage(R: int = 3, perp_cutoff: float = 3.5) -> tuple[np.ndarray, list[dict]]:
    """Construct the N=132 cage by taking the 4 innermost I_h orbits at
    the given perp_cutoff."""
    _, group_ih = build_Ih_60_and_120()
    lattice = GCTLattice(R=R, perp_cutoff=perp_cutoff)
    x_eq = lattice.x_equilibrium
    x_perp_all = proj.project_perp(x_eq)
    norms = np.linalg.norm(x_perp_all, axis=1)
    idx = np.argsort(norms)
    if norms[idx[0]] < 1e-8:
        idx = idx[1:]

    seen: set[tuple[int, ...]] = set()
    orbits = []
    for j in idx:
        if len(orbits) >= 4:
            break
        seed = tuple(int(c) for c in x_eq[j])
        if seed in seen:
            continue
        orbit = full_orbit(seed, group_ih)
        seen |= orbit
        rep_v = np.array(seed, dtype=np.float64)
        rep_perp = proj.project_perp(rep_v.reshape(1, -1))[0]
        rep_perp_norm = float(np.linalg.norm(rep_perp))
        orbits.append({
            "perp_norm": rep_perp_norm,
            "size": len(orbit),
            "nodes_6d": [list(n) for n in orbit],
        })

    all_nodes_set: set[tuple[int, ...]] = set()
    for o in orbits:
        for n in o["nodes_6d"]:
            all_nodes_set.add(tuple(n))
    nodes_arr = np.array(sorted(all_nodes_set), dtype=np.float64)
    return nodes_arr, orbits


def build_cage_adjacency(nodes_6d: np.ndarray) -> tuple[np.ndarray, int]:
    """Golden-weighted scalar adjacency. Returns (A, n_edges)."""
    nodes_perp = nodes_6d @ proj.get_m_perp().T
    N = nodes_6d.shape[0]
    A = np.zeros((N, N))
    n_edges = 0
    for i in range(N):
        for j in range(i + 1, N):
            d = float(np.linalg.norm(nodes_perp[i] - nodes_perp[j]))
            if abs(d - 1.0) < 0.05:
                A[i, j] = A[j, i] = 1.0
                n_edges += 1
            elif abs(d - 1.0 / PHI) < 0.05:
                A[i, j] = A[j, i] = PHI
                n_edges += 1
    return A, n_edges


def test_bipartite(A: np.ndarray) -> tuple[bool, np.ndarray]:
    """BFS 2-coloring; returns (is_bipartite, color_assignment)."""
    N = A.shape[0]
    color = -np.ones(N, dtype=int)
    is_bipartite = True
    for start in range(N):
        if color[start] != -1:
            continue
        color[start] = 0
        queue = [start]
        while queue:
            u = queue.pop(0)
            for v in range(N):
                if A[u, v] > 0:
                    if color[v] == -1:
                        color[v] = 1 - color[u]
                        queue.append(v)
                    elif color[v] == color[u]:
                        is_bipartite = False
        if not is_bipartite:
            break
    return is_bipartite, color


def main():
    print("=" * 76)
    print("N=132 investigation: structural origin of integer-APS recovery")
    print("=" * 76)

    print("\n--- Step 1: Build the N=132 cage ---")
    nodes_6d, orbits = build_n132_cage()
    print(f"  Total cage size: {nodes_6d.shape[0]}")
    print(f"  Orbit composition:")
    for k, o in enumerate(orbits):
        print(f"    orbit {k}: perp_norm = {o['perp_norm']:.4f}, size = {o['size']}")
    total = sum(o["size"] for o in orbits)
    print(f"  Sum of orbit sizes: {total}")

    print("\n--- Step 2: Adjacency + edge count + bipartite test ---")
    A, n_edges = build_cage_adjacency(nodes_6d)
    print(f"  Edges (golden-weighted): {n_edges}")
    is_bipartite, color = test_bipartite(A)
    n_class_0 = int(np.sum(color == 0))
    n_class_1 = int(np.sum(color == 1))
    print(f"  Is bipartite (2-colorable): {is_bipartite}")
    print(f"    Color 0: {n_class_0}, Color 1: {n_class_1}")

    print("\n--- Step 3: Adjacency spectrum + eta_scalar verification ---")
    evals = np.linalg.eigvalsh(A)
    nz = evals[np.abs(evals) > 1e-12]
    eta_scalar = int(round(float(np.sum(np.sign(nz)))))
    n_pos = int(np.sum(nz > 0))
    n_neg = int(np.sum(nz < 0))
    n_zero = int(len(evals) - len(nz))
    print(f"  Eigenvalue range: [{evals.min():.4f}, {evals.max():.4f}]")
    print(f"  Positive: {n_pos}, Negative: {n_neg}, Zero: {n_zero}")
    print(f"  eta_scalar = sum(sign(non-zero)) = {eta_scalar}")
    print(f"  eta_eff = {eta_scalar / 8.0:+.4f}")

    print("\n--- Step 4: I-irrep decomposition deferred ---")
    print("  (the symbolic computation uses the same character-theoretic machinery as")
    print("   protocol_cage_spectral_decomp.py; the per-irrep breakdown of the eta = 0")
    print("   result is bookmarked for the full irrep-block spectral analysis.)")
    irrep = {"deferred": True}

    print("\n--- Step 5: Relationship to canonical N=152 cage ---")
    from cage_builder import build_canonical_cage
    nodes_152, _ = build_canonical_cage(size=152)
    nodes_132_set = set(tuple(int(c) for c in row) for row in nodes_6d)
    nodes_152_set = set(tuple(int(c) for c in row) for row in nodes_152)
    common = nodes_132_set & nodes_152_set
    only_132 = nodes_132_set - nodes_152_set
    only_152 = nodes_152_set - nodes_132_set
    print(f"  |N=132 cage|: {len(nodes_132_set)}")
    print(f"  |N=152 cage|: {len(nodes_152_set)}")
    print(f"  Common nodes (both cages): {len(common)}")
    print(f"  Only in N=132: {len(only_132)}")
    print(f"  Only in N=152: {len(only_152)}")
    if len(common) > 0 and len(only_132) == 0:
        print(f"  -> N=132 is a SUB-CAGE of N=152 (all 132 nodes are in N=152).")
    elif len(common) > 0 and len(only_152) == 0:
        print(f"  -> N=152 is a SUB-CAGE of N=132 (impossible if 132 < 152).")
    elif len(common) == 0:
        print(f"  -> The two cages are disjoint.")
    else:
        print(f"  -> Partial overlap (neither contains the other).")

    print("\n" + "=" * 76)
    print("SUMMARY")
    print("=" * 76)
    if is_bipartite:
        print(f"  Bipartiteness: YES (color partition {n_class_0} + {n_class_1})")
        print(f"  This explains the eta_scalar = 0 result: bipartite graphs")
        print(f"  have spectra symmetric about 0, so positive and negative")
        print(f"  eigenvalue counts are equal (eta = 0 automatically).")
    else:
        print(f"  Bipartiteness: NO. The eta_scalar = 0 result has a different")
        print(f"  structural origin (e.g., a cancellation among I-irrep blocks).")
    print(f"  Orbit composition: {[(o['perp_norm'], o['size']) for o in orbits]}")
    print(f"  Cage-overlap with canonical N=152: {len(common)} / 132 nodes shared.")
    print("=" * 76)

    verdict = {
        "N_total": int(nodes_6d.shape[0]),
        "orbit_composition": [(o["perp_norm"], o["size"]) for o in orbits],
        "n_edges": n_edges,
        "is_bipartite": bool(is_bipartite),
        "bipartite_color_partition": [n_class_0, n_class_1],
        "eigenvalue_range": [float(evals.min()), float(evals.max())],
        "n_positive_evals": n_pos,
        "n_negative_evals": n_neg,
        "n_zero_evals": n_zero,
        "eta_scalar": int(eta_scalar),
        "eta_eff": float(eta_scalar) / 8.0,
        "irrep_decomp": irrep,
        "overlap_with_canonical_152": {
            "n_shared": len(common),
            "only_in_132": len(only_132),
            "only_in_152": len(only_152),
            "n132_is_subcage_of_152": (len(only_132) == 0 and len(common) > 0),
        },
    }
    out_path = ENGINE_ROOT / "data" / "protocol_n132_investigation_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(verdict, f, indent=2)
    print(f"\nFull results saved to: {out_path}")
    print("=" * 76)


if __name__ == "__main__":
    main()
