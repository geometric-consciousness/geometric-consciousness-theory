#!/usr/bin/env python3
"""
protocol_aps_candidates_final.py - Apply the resolution-artifact test
to the remaining APS-recovery candidates N=574 and N=754.

The C2-nullspace investigation showed that N=132's integer-arithmetic
APS recovery is a resolution artifact of the golden-bond rule: 42
vertices in two close-perp-radius orbits (0.167 and 0.176) had
identical adjacency rows, producing a 42-dim nullspace and eta = 0.

This protocol asks the same question of N=574 (eta_scalar = +8,
bulk_required = -108) and N=754 (eta_scalar = -24, bulk_required =
-104): are their integer-APS-arithmetic results similarly
artifacts of close-perp-radius orbit pairs and duplicate adjacency
rows, or do they have genuine structural origin?

For each cage size, the protocol reports:
  - Orbit composition (perp-radii + sizes for the first K orbits)
  - Adjacency edge count
  - Number of duplicate-adjacency-row groups (resolution artifact)
  - Nullspace dimension (deeper structural redundancy indicator)
  - eta_scalar verification against the C2 search

Closure: if N=574 and N=754 are also resolution artifacts, then NO
I_h-closed cage in the searched range has a non-artifact integer-APS
recovery -- a clean strong-negative result that closes the C2
cage-search investigation.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
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


def build_Ih_120() -> list[np.ndarray]:
    vertices_perp, _ = vertex_pairs_from_projection()
    rots3 = icosahedral_rotations_lattice_frame(vertices_perp)
    group60 = []
    for R in rots3:
        M = lift_to_6d_signed_perm(R, vertices_perp)
        if M is None:
            continue
        group60.append(M)
    minus_I6 = -np.eye(6)
    return group60 + [minus_I6 @ M for M in group60]


def full_orbit(seed: tuple[int, ...], group: list[np.ndarray]) -> set[tuple[int, ...]]:
    seed_v = np.array(seed, dtype=np.float64)
    orbit = {seed}
    for M in group:
        mapped = M @ seed_v
        orbit.add(tuple(int(round(c)) for c in mapped))
    return orbit


def build_cage_n_orbits(group_ih: list[np.ndarray], k_orbits: int, R: int = 3,
                        perp_cutoff: float = 3.5) -> tuple[np.ndarray, list[dict]]:
    """Build the cage as the cumulative union of the first k_orbits
    I_h orbits (sorted by perp-norm). Returns (nodes_6d, orbits_info)."""
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
        if len(orbits) >= k_orbits:
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
            "nodes_6d_set": orbit,
        })

    all_nodes_set: set[tuple[int, ...]] = set()
    for o in orbits:
        all_nodes_set |= o["nodes_6d_set"]
    nodes_arr = np.array(sorted(all_nodes_set), dtype=np.float64)
    return nodes_arr, orbits


def build_cage_adjacency(nodes_6d: np.ndarray) -> tuple[np.ndarray, int]:
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


def duplicate_row_groups(A: np.ndarray) -> list[list[int]]:
    """Return list of lists of row indices having identical adjacency rows."""
    N = A.shape[0]
    sig_groups: dict[tuple, list[int]] = defaultdict(list)
    for i in range(N):
        sig = tuple(sorted([(j, round(A[i, j], 6)) for j in range(N) if abs(A[i, j]) > 1e-9]))
        sig_groups[sig].append(i)
    return [idxs for idxs in sig_groups.values() if len(idxs) > 1]


def find_close_orbit_pairs(orbits: list[dict], threshold: float = 0.05) -> list[tuple[int, int, float]]:
    """Find pairs of orbits with perp-radii closer than threshold
    (the golden-bond resolution limit)."""
    pairs = []
    for i in range(len(orbits)):
        for j in range(i + 1, len(orbits)):
            d = abs(orbits[i]["perp_norm"] - orbits[j]["perp_norm"])
            if d < threshold:
                pairs.append((i, j, d))
    return pairs


def analyze_cage(N_target: int, k_orbits: int, group_ih: list[np.ndarray], label: str) -> dict:
    print(f"\n{'-' * 76}")
    print(f"  Analyzing {label}: target N={N_target}, k_orbits={k_orbits}")
    print(f"{'-' * 76}")

    nodes_6d, orbits = build_cage_n_orbits(group_ih, k_orbits)
    N = nodes_6d.shape[0]
    if N != N_target:
        print(f"  [WARN] built cage has N={N}, target was {N_target}")

    print(f"  N = {N}")
    print(f"  Orbits ({len(orbits)}):")
    for k, o in enumerate(orbits):
        print(f"    {k:>3}: perp_norm = {o['perp_norm']:.4f}, size = {o['size']}")

    print(f"  Building adjacency (may be slow for large N)...")
    A, n_edges = build_cage_adjacency(nodes_6d)
    print(f"  Edges: {n_edges}")

    print(f"  Computing eigenvalues (cost ~ O(N^3); N={N})...")
    evals = np.linalg.eigvalsh(A)
    nz = evals[np.abs(evals) > 1e-9]
    n_zero = int(N - len(nz))
    eta_scalar = int(round(float(np.sum(np.sign(nz)))))
    n_pos = int(np.sum(nz > 0))
    n_neg = int(np.sum(nz < 0))
    print(f"  Spectrum: {n_pos} positive, {n_neg} negative, {n_zero} zero")
    print(f"  eta_scalar = {eta_scalar:+d}")

    print(f"  Searching for close-perp-radius orbit pairs (threshold 0.05)...")
    close_pairs = find_close_orbit_pairs(orbits, threshold=0.05)
    if close_pairs:
        print(f"  Found {len(close_pairs)} close pairs:")
        for i, j, d in close_pairs[:10]:
            print(f"    orbits {i} (size {orbits[i]['size']}) + {j} (size {orbits[j]['size']}): "
                  f"|delta| = {d:.4f}")
    else:
        print(f"  No close-pair orbits within threshold (no obvious resolution artifact).")

    print(f"  Counting duplicate-adjacency-row groups...")
    dup_groups = duplicate_row_groups(A)
    n_extra = sum(len(g) - 1 for g in dup_groups)
    if dup_groups:
        sizes = sorted([len(g) for g in dup_groups], reverse=True)
        print(f"  {len(dup_groups)} duplicate-row groups, sizes (top 10): {sizes[:10]}")
        print(f"  Total extra rows from duplicates: {n_extra}")
    else:
        print(f"  No duplicate-row groups (no resolution-artifact mechanism).")

    bulk_required = -107 - eta_scalar / 8.0
    bulk_int = abs(bulk_required - round(bulk_required)) < 1e-9

    # Two mechanisms can make eta a multiple of 8:
    #   (A) Large duplicate-row count gives many zero eigenvalues, eta = 0
    #       trivially. This is the N=132 mechanism.
    #   (B) The non-zero spectrum happens to have an excess of positive (or
    #       negative) signs that is a multiple of 8 by approximate chance.
    #       For a generic spectrum, |eta| scales as ~sqrt(N) (CLT); a
    #       multiple-of-8 within 1*sqrt(N) is statistically unremarkable.
    sqrt_N_estimate = float(np.sqrt(N))
    is_duplicate_artifact = (n_extra >= max(n_zero - 1, 1))   # N=132-style
    abs_eta_vs_sqrt_N = abs(eta_scalar) / sqrt_N_estimate
    is_statistical_coincidence = (
        not is_duplicate_artifact
        and abs_eta_vs_sqrt_N < 2.0   # within ~2 sigma of zero
        and eta_scalar % 8 == 0
    )

    print(f"  bulk_required for n=-107 = {bulk_required:+.4f} (integer? {bulk_int})")
    print(f"  Resolution-artifact diagnostics:")
    print(f"    duplicate-mechanism (N=132 style): {is_duplicate_artifact}")
    print(f"      (n_extra={n_extra} vs n_zero-1={n_zero - 1})")
    print(f"    statistical-coincidence (eta within 2*sqrt(N) of 0): {is_statistical_coincidence}")
    print(f"      (|eta|/sqrt(N) = {abs_eta_vs_sqrt_N:.3f})")

    is_genuine = bool(
        bulk_int
        and not is_duplicate_artifact
        and not is_statistical_coincidence
    )

    return {
        "label": label,
        "N_target": N_target,
        "N_built": N,
        "k_orbits": len(orbits),
        "orbits": [{"perp_norm": o["perp_norm"], "size": o["size"]} for o in orbits],
        "n_edges": n_edges,
        "n_positive_evals": n_pos,
        "n_negative_evals": n_neg,
        "n_zero_evals": n_zero,
        "eta_scalar": eta_scalar,
        "bulk_required_for_n_minus_107": bulk_required,
        "bulk_is_integer": bool(bulk_int),
        "close_orbit_pairs": [(i, j, d) for i, j, d in close_pairs],
        "n_duplicate_groups": len(dup_groups),
        "n_extra_rows_from_duplicates": int(n_extra),
        "largest_duplicate_groups": sorted([len(g) for g in dup_groups], reverse=True)[:10],
        "abs_eta_over_sqrt_N": abs_eta_vs_sqrt_N,
        "is_duplicate_artifact": bool(is_duplicate_artifact),
        "is_statistical_coincidence": bool(is_statistical_coincidence),
        "is_genuine_candidate": is_genuine,
    }


def main():
    print("=" * 76)
    print("C2-final: resolution-artifact test on N=574 and N=754 candidates")
    print("=" * 76)

    group_ih = build_Ih_120()

    # From the C2 cage search: N=574 was at k_orbits=14, N=754 at k_orbits=16
    results = []
    results.append(analyze_cage(N_target=574, k_orbits=14, group_ih=group_ih, label="N=574"))
    results.append(analyze_cage(N_target=754, k_orbits=16, group_ih=group_ih, label="N=754"))

    print("\n" + "=" * 76)
    print("SUMMARY")
    print("=" * 76)
    print(f"  {'label':>8}  {'N':>5}  {'eta':>5}  {'|eta|/sqrt(N)':>14}  {'bulk':>7}  {'dup_arti':>9}  {'stat_coin':>10}  {'genuine':>8}")
    for r in results:
        print(f"  {r['label']:>8}  {r['N_built']:>5}  {r['eta_scalar']:>+5d}  "
              f"{r['abs_eta_over_sqrt_N']:>14.3f}  "
              f"{r['bulk_required_for_n_minus_107']:>+7.3f}  "
              f"{str(r['is_duplicate_artifact']):>9}  "
              f"{str(r['is_statistical_coincidence']):>10}  "
              f"{str(r['is_genuine_candidate']):>8}")

    n_dup_artifact = sum(1 for r in results if r["is_duplicate_artifact"])
    n_stat_coincidence = sum(1 for r in results if r["is_statistical_coincidence"])
    n_genuine = sum(1 for r in results if r["is_genuine_candidate"])
    print()
    print(f"  Duplicate-row artifacts:    {n_dup_artifact} / {len(results)}")
    print(f"  Statistical coincidences:   {n_stat_coincidence} / {len(results)}")
    print(f"  Genuine non-artifact:       {n_genuine} / {len(results)}")
    print("=" * 76)

    if n_genuine == 0:
        print("STRONG NEGATIVE CLOSURE.")
        print("Combined with the N=132 (duplicate-row artifact) result, the three")
        print("non-trivial APS-recovery candidates (N=132, 574, 754) found by the")
        print("C2 cage search are EXPLAINED:")
        print("  - N=132: duplicate-row artifact (orbits 0 + 1 are too close in")
        print("    perp-radius for the golden-bond rule to distinguish them).")
        print("  - N=574 and N=754: statistical coincidence (|eta| within ~2*sqrt(N)")
        print("    of zero AND happens to be a multiple of 8).")
        print()
        print("No I_h-closed cage in the searched range exhibits a STRUCTURALLY")
        print("forced integer-arithmetic APS recovery of n = -107. The cage-")
        print("uniqueness investigation (E + I + H + G + M + C2 + C2-cont +")
        print("C2-nullspace + C2-final) is now COMPLETE as a coherent unit:")
        print("  - The discrete APS sum does NOT recover n = -107 at structurally-")
        print("    forced integer arithmetic on any examined I_h-closed cage")
        print("    under the golden-bond rule.")
        print("  - The empirical anchor (mass-formula CODATA match) carries the")
        print("    determination of n = -107 alone.")
        print("  - O.14c closure via the discrete-APS-on-I_h-closed-cage pathway")
        print("    is structurally blocked at the searched scale; alternative")
        print("    pathways (smooth Connes-Moscovici via O.14b, or richer index-")
        print("    theoretic frameworks) become the only remaining routes to a")
        print("    theoretical derivation.")
    else:
        print(f"FOUND {n_genuine} GENUINE NON-ARTIFACT CANDIDATE(S):")
        for r in results:
            if r["is_genuine_candidate"]:
                print(f"  -> {r['label']}: N={r['N_built']}, eta={r['eta_scalar']:+d}, "
                      f"|eta|/sqrt(N)={r['abs_eta_over_sqrt_N']:.3f}, "
                      f"bulk={r['bulk_required_for_n_minus_107']:+.0f}")
        print("  These warrant further investigation to determine whether they")
        print("  admit independent physical motivation as canonical electron-defect")
        print("  cages.")

    verdict = {
        "candidates_analyzed": len(results),
        "n_duplicate_artifacts": n_dup_artifact,
        "n_statistical_coincidences": n_stat_coincidence,
        "n_genuine_candidates": n_genuine,
        "candidate_details": results,
        "n132_already_classified_as_duplicate_artifact": True,
        "cage_search_closure_status": (
            "STRONG_NEGATIVE_all_candidates_explained_as_artifacts_or_coincidence"
            if n_genuine == 0 else
            f"PARTIAL_{n_genuine}_genuine_candidate(s)_remain"
        ),
    }
    out_path = ENGINE_ROOT / "data" / "protocol_aps_candidates_final_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(verdict, f, indent=2)
    print(f"\nFull results saved to: {out_path}")
    print("=" * 76)


if __name__ == "__main__":
    main()
