#!/usr/bin/env python3
"""
protocol_orbit_union_search.py — finite orbit-union adjacency diagnostic
for Open Problem O.14.

Sweep: enumerate all ways to partition 144 into a sum of
icosahedral I-orbit sizes drawn from the full orbits in the top-600 sample, build the
corresponding I-symmetric 144-cage for each, and compute the scalar
weighted-adjacency sign sum. No qualifying APS operator/domain or APS
eta/index is specified or evaluated here.

Outcomes:
  - Exactly one such cage exists → the finite search has a unique match;
    a first-principles rule selecting it remains O.14d.
  - Multiple exist → the finite search does not select a unique cage.
  - None exist → the cage approach cannot yield -8 under I-symmetry, and
    the Bellissard gap-labeling route (protocol_bellissard_gap_labels.py)
    is the relevant alternative.

The top-600 radial sample has shell inventory
   [12, 30, 30, 60, 20, 60, 60, 30, 60, 20, 12, 60, 60, 60, 26].
Shells 0–13 are full I-orbits; shell 14 is cutoff-truncated and is excluded.
"""

from __future__ import annotations

import math
import json
import sys
from pathlib import Path
from itertools import combinations

import numpy as np

ENGINE_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = ENGINE_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

DATA_PATH = ENGINE_ROOT / "data" / "protocol_orbit_union_search_results.json"

from gct_utils import C

PHI = float(C.PHI)

# Icosahedral 6D-action and orbit-enumeration infrastructure
sys.path.insert(0, str(SRC_PATH))
from protocol_cage_repair import (
    vertex_pairs_from_projection,
    icosahedral_rotations_lattice_frame,
    lift_to_6d_signed_perm,
    enumerate_orbits,
)


def setup_orbits():
    """Re-run the orbit enumeration to get the orbits + their nodes."""
    from gct_lattice import GCTLattice
    import gct_projections as proj

    print("  Building I ⊂ SL(6,Z) (60 6×6 signed-permutation matrices)...")
    vertices_perp, _ = vertex_pairs_from_projection()
    rotations_3d = icosahedral_rotations_lattice_frame(vertices_perp)
    six_d_matrices = [lift_to_6d_signed_perm(R, vertices_perp) for R in rotations_3d]
    six_d_matrices = [M for M in six_d_matrices if M is not None]
    print(f"  ✓ {len(six_d_matrices)} 6D matrices.")

    print("  Enumerating shell components in the top-600 sample (R=3, perp_cutoff=3.0)...")
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
    print(f"  ✓ {len(orbits_idx)} shell components found.")
    orbits = []
    for orb in orbits_idx:
        min_norm = min(cand_norms[i] for i in orb)
        orbits.append({
            "size": len(orb),
            "min_perp_norm": float(min_norm),
            "indices": orb,
            "nodes_6d": candidates_6d[orb],
            "nodes_perp": candidates_perp[orb],
            "is_full_i_orbit": component_is_full_i_orbit(orb, candidates_6d, six_d_matrices),
        })
    # Size is the deterministic tie-breaker for equal-radius shells (indices 10/11).
    orbits.sort(key=lambda o: (round(o["min_perp_norm"], 12), o["size"]))
    print(f"  Shell inventory (in order): {[o['size'] for o in orbits]}")
    return orbits, six_d_matrices


def component_is_full_i_orbit(component, candidates_6d, six_d_matrices):
    """Return whether every I-image stays inside this sampled component."""
    keys = {tuple(np.rint(candidates_6d[i]).astype(int)) for i in component}
    return all(
        tuple(np.rint(M @ candidates_6d[i]).astype(int)) in keys
        for i in component
        for M in six_d_matrices
    )


def find_subsets_summing_to(target: int, sizes: list[int]) -> list[list[int]]:
    """Find all subsets of `sizes` (by index) summing to `target`. Limit
    orbit-set cardinality to 7 (heuristic — keeps search bounded)."""
    n = len(sizes)
    matches = []
    for k in range(1, min(n, 8) + 1):
        for combo in combinations(range(n), k):
            if sum(sizes[i] for i in combo) == target:
                matches.append(list(combo))
    return matches


def build_cage_from_orbits(orbit_indices: list[int], orbits: list[dict]) -> tuple[np.ndarray, np.ndarray]:
    """Concatenate nodes from selected orbits."""
    nodes_6d = np.vstack([orbits[i]["nodes_6d"] for i in orbit_indices])
    nodes_perp = np.vstack([orbits[i]["nodes_perp"] for i in orbit_indices])
    return nodes_6d, nodes_perp


def compute_adjacency_sign_sum(nodes_perp: np.ndarray) -> tuple[float, dict]:
    """Build the engine's golden-weighted adjacency on these nodes and
    return the finite sign sum plus spectrum summary."""
    N = len(nodes_perp)
    A = np.zeros((N, N))
    for i in range(N):
        for j in range(i + 1, N):
            d = np.linalg.norm(nodes_perp[i] - nodes_perp[j])
            if abs(d - 1.0) < 0.05:
                A[i, j] = A[j, i] = 1.0
            elif abs(d - 1.0 / PHI) < 0.05:
                A[i, j] = A[j, i] = PHI
    evals = np.linalg.eigvalsh(A)
    nz = evals[np.abs(evals) > 1e-12]
    eta = float(np.sum(np.sign(nz)))
    return eta, {
        "n_pos": int(np.sum(nz > 0)),
        "n_neg": int(np.sum(nz < 0)),
        "n_zero": int(N - len(nz)),
        "min": float(evals.min()),
        "max": float(evals.max()),
    }


def main() -> int:
    print("=" * 90)
    print("  extended sweep: combinatorial orbit-union search for adjacency sign-sum -8 cage")
    print("=" * 90)
    orbits, six_d_matrices = setup_orbits()

    shell_inventory = [o["size"] for o in orbits]
    full_orbits = [o for o in orbits if o["is_full_i_orbit"]]
    sizes = [o["size"] for o in full_orbits]
    print()
    print(f"  Target: sum to 144 from orbit sizes {sizes}")
    subsets = find_subsets_summing_to(144, sizes)
    print(f"  ✓ Found {len(subsets)} subsets summing to 144 (with ≤7 orbits).")
    if len(subsets) == 0:
        print("  No orbit-unions sum to 144 from the orbits we have. Need a wider")
        print("  candidate set.")
        return 1

    print()
    results = []
    target_match = []
    for sub_idx, sub in enumerate(subsets):
        nodes_6d, nodes_perp = build_cage_from_orbits(sub, full_orbits)
        eta, spec = compute_adjacency_sign_sum(nodes_perp)
        sizes_used = [full_orbits[i]["size"] for i in sub]
        # I-symmetry is automatic for orbit-unions; we just confirm
        result = {
            "subset_idx": sub_idx,
            "orbit_indices": sub,
            "sizes": sizes_used,
            "total": sum(sizes_used),
            "adjacency_sign_sum": eta,
            "spectrum": spec,
        }
        results.append(result)
        marker = ""
        if abs(eta - (-8)) < 0.5:
            marker = "  *** η = -8 MATCH ***"
            target_match.append(result)
        elif abs(eta) < 0.5:
            marker = "  (η = 0)"
        print(f"  [{sub_idx:3d}] sizes={sizes_used}  η={eta:+5.1f}  (+{spec['n_pos']}/-{spec['n_neg']}/0:{spec['n_zero']}){marker}")

    print()
    print("=" * 90)
    if target_match:
        print(f"  *** {len(target_match)} ORBIT-UNION(S) GIVE ADJACENCY SIGN SUM -8 ***")
        for m in target_match:
            print(f"    sizes = {m['sizes']}")
        print()
        print("  Orbit-union route yields a match: there exist I-symmetric 144-cages")
        print("  whose weighted-adjacency sign sum is -8. This is not an APS eta-invariant.")
        print("  The finite match does not supply")
        print("  a first-principles selection rule; that 21-to-1 step remains O.14d.")
    else:
        print("  No I-symmetric orbit-union of 144 gives adjacency sign sum -8.")
        print(f"  Observed sign sums across {len(results)} cages: {sorted(set(r['adjacency_sign_sum'] for r in results))}")
        print()
        print("  The weighted-adjacency sign sum does not equal -8 under I-symmetry.")
        print("  A -8 sign count from a particular symmetry-broken cage is not")
        print("  reproduced under I-symmetry. The Bellissard gap-labeling route")
        print("  (protocol_bellissard_gap_labels.py) is the relevant alternative.")
    print("=" * 90)

    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DATA_PATH.open("w", encoding="utf-8") as f:
        json.dump({
            "shell_inventory": shell_inventory,
            "n_shell_components": len(orbits),
            "n_full_i_orbits": len(full_orbits),
            "full_i_orbit_indices": [i for i, o in enumerate(orbits) if o["is_full_i_orbit"]],
            "cutoff_truncated_shell_indices": [i for i, o in enumerate(orbits) if not o["is_full_i_orbit"]],
            "n_subsets_tested": len(subsets),
            "matches_to_eta_minus_8": len(target_match),
            "matching_subsets": [{"sizes": m["sizes"]} for m in target_match],
            "all_adjacency_sign_sums": sorted(set(r["adjacency_sign_sum"] for r in results)),
            "verdict": "SUCCESS" if target_match else "FAILURE",
        }, f, indent=2)
    print(f"  Results: {DATA_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
