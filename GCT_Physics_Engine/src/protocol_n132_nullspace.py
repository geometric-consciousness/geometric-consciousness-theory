#!/usr/bin/env python3
"""
protocol_n132_nullspace.py - Structural investigation of the 42-dim
nullspace of the N=132 cage's golden-weighted adjacency matrix.

Background (protocol_n132_investigation.py): the N=132 I_h-closed cage
that admits integer-APS recovery of n=-107 has a striking spectrum:
45 positive + 45 negative + 42 zero eigenvalues. The 42-dim nullspace
is too large for a generic graph of this size (~1/3 of the spectrum).
This protocol asks: does the nullspace have a representation-theoretic
origin (e.g., specific I_h irrep blocks identically zero), or is it
"graph redundancy" (many vertices with identical neighbourhoods)?

Steps:
  1. Compute the nullspace basis explicitly.
  2. Test whether the nullspace is I_h-invariant: for each lifted
     6D-signed-permutation matrix M_g in I_h, verify M_g maps the
     nullspace to itself.
  3. If I_h-invariant: decompose the nullspace by I_h irreps via
     character theory (m_rho = (1/|G|) sum_g chi_rho(g) trace(P_g | ker A)).
  4. Test for "graph redundancy" -- count pairs of vertices with
     identical adjacency rows (a known source of zero eigenvalues).
  5. Per-orbit analysis -- which of the 4 I_h orbits contribute
     most to the nullspace dimension?
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

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


def build_n132_cage(group_ih: list[np.ndarray]) -> tuple[np.ndarray, list[dict]]:
    lattice = GCTLattice(R=3, perp_cutoff=3.5)
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
            "nodes_6d_set": orbit,
        })

    all_nodes_set: set[tuple[int, ...]] = set()
    for o in orbits:
        all_nodes_set |= o["nodes_6d_set"]
    nodes_arr = np.array(sorted(all_nodes_set), dtype=np.float64)
    return nodes_arr, orbits


def build_cage_adjacency(nodes_6d: np.ndarray) -> np.ndarray:
    nodes_perp = nodes_6d @ proj.get_m_perp().T
    N = nodes_6d.shape[0]
    A = np.zeros((N, N))
    for i in range(N):
        for j in range(i + 1, N):
            d = float(np.linalg.norm(nodes_perp[i] - nodes_perp[j]))
            if abs(d - 1.0) < 0.05:
                A[i, j] = A[j, i] = 1.0
            elif abs(d - 1.0 / PHI) < 0.05:
                A[i, j] = A[j, i] = PHI
    return A


def cage_permutation_matrix(nodes_6d: np.ndarray, M: np.ndarray) -> np.ndarray | None:
    """Build the NxN permutation matrix P_g induced by the I_h action M
    on the cage. Returns None if M does not preserve the cage."""
    N = nodes_6d.shape[0]
    nodes_int = np.round(nodes_6d).astype(np.int64)
    coord_to_index = {tuple(row): i for i, row in enumerate(nodes_int)}
    images = nodes_6d.astype(np.float64) @ M.T
    images_int = np.round(images).astype(np.int64)
    P = np.zeros((N, N))
    for i in range(N):
        j = coord_to_index.get(tuple(images_int[i]))
        if j is None:
            return None
        P[j, i] = 1.0
    return P


def main():
    print("=" * 76)
    print("N=132 nullspace investigation")
    print("=" * 76)

    print("\n--- Building cage + adjacency ---")
    group_ih = build_Ih_120()
    nodes_6d, orbits = build_n132_cage(group_ih)
    N = nodes_6d.shape[0]
    print(f"  N = {N}")
    print(f"  Orbit sizes: {[o['size'] for o in orbits]} = {sum(o['size'] for o in orbits)}")

    A = build_cage_adjacency(nodes_6d)
    n_edges = int(A.astype(bool).sum() / 2)
    print(f"  Edges: {n_edges}")

    print("\n--- Step 1: Compute nullspace ---")
    evals, evecs = np.linalg.eigh(A)
    null_mask = np.abs(evals) < 1e-9
    null_basis = evecs[:, null_mask]   # (N, dim_null)
    dim_null = int(np.sum(null_mask))
    print(f"  dim(ker A) = {dim_null}")
    print(f"  (vs 132 - rank ≈ {N - int(np.sum(~null_mask))} from sign count)")

    print("\n--- Step 2: Test I_h-invariance of the nullspace ---")
    group_60 = group_ih[:60]
    permutations: list[np.ndarray] = []
    failed = 0
    for M in group_60:
        P = cage_permutation_matrix(nodes_6d, M)
        if P is None:
            failed += 1
            continue
        permutations.append(P)
    print(f"  Cage is preserved by {len(permutations)}/60 I rotations; {failed} failed")

    # For each permutation P_g, check whether P_g maps ker(A) -> ker(A)
    # That is, for each null basis vector v, P_g @ v should also be in ker(A)
    # which means A @ (P_g @ v) = 0
    invariance_ok = True
    max_violation = 0.0
    for P in permutations:
        for k in range(dim_null):
            v = null_basis[:, k]
            Pv = P @ v
            APv = A @ Pv
            norm = float(np.linalg.norm(APv))
            if norm > max_violation:
                max_violation = norm
            if norm > 1e-6:
                invariance_ok = False
    print(f"  ker(A) is I-invariant: {invariance_ok}")
    print(f"  Max |A @ P_g @ v| over (g, v): {max_violation:.3e}")

    print("\n--- Step 3: Restrict each P_g to ker(A) and compute trace ---")
    G = len(permutations)
    # Project P_g restricted to ker(A): tr(P_g | ker A) = sum_k <v_k | P_g | v_k>
    # = tr(N^T P_g N) where N = null_basis (N x dim_null) is orthonormal
    traces_on_kernel = []
    for P in permutations:
        T = null_basis.T @ P @ null_basis   # (dim_null, dim_null)
        tr = float(np.trace(T))
        traces_on_kernel.append(tr)
    avg_trace_kernel = sum(traces_on_kernel) / len(traces_on_kernel) if traces_on_kernel else 0
    print(f"  trace(P_g | ker A) averaged over 60 rotations: {avg_trace_kernel:.3f}")
    print(f"  This is dim(ker A) / |G| × (trace of identity) = {dim_null}/{G} = {dim_null / G:.3f}")
    print(f"  if the kernel is the trivial irrep; not the case here since dim_null > 1")

    # Decompose ker(A) by I-irreps via character theory.
    # For each conjugacy class, we need the average trace over that class.
    # Classify the 60 rotations into conjugacy classes by their 6D-trace.
    # I has 5 classes: e (tr=6), C5 (tr=1+1/phi≈1.618), C5^2 (tr=1-phi≈-0.618), C3 (tr=0), C2 (tr=-2)
    class_centroids = [6.0, 1.0 + 1.0 / PHI, 1.0 - PHI, 0.0, -2.0]
    class_names = ["e", "C5", "C5^2", "C3", "C2"]
    class_sizes = [1, 12, 12, 20, 15]

    class_trace_sums = [0.0] * 5
    class_counts = [0] * 5
    for k, P in enumerate(permutations):
        # Re-derive M from P? No, easier: track them together
        pass  # handled below

    # Better: iterate over (P, M) pairs, classify M, accumulate.
    pairs: list[tuple[np.ndarray, np.ndarray]] = []
    for M in group_60:
        P = cage_permutation_matrix(nodes_6d, M)
        if P is None:
            continue
        pairs.append((P, M))

    for P, M in pairs:
        tr6 = float(np.trace(M))
        # Classify by closeness to centroids
        diffs = [abs(tr6 - c) for c in class_centroids]
        cls = int(np.argmin(diffs))
        if diffs[cls] > 0.2:
            continue   # unclassifiable
        T = null_basis.T @ P @ null_basis
        tr_ker = float(np.trace(T))
        class_trace_sums[cls] += tr_ker
        class_counts[cls] += 1

    class_trace_avg = [s / c if c > 0 else 0.0 for s, c in zip(class_trace_sums, class_counts)]
    print(f"\n  Per-class average trace(P_g | ker A):")
    for name, sz, c, t in zip(class_names, class_sizes, class_counts, class_trace_avg):
        print(f"    {name:>4}  (size {sz}, observed {c}): avg trace on kernel = {t:.3f}")

    # I-irrep characters: A (trivial), T_1, T_2, G, H
    char_table = {
        "A":  [1, 1, 1, 1, 1],
        "T1": [3, PHI, 1.0 - PHI, 0, -1],
        "T2": [3, 1.0 - PHI, PHI, 0, -1],
        "G":  [4, -1, -1, 1, 0],
        "H":  [5, 0, 0, -1, 1],
    }

    print(f"\n  I-irrep multiplicities in ker(A):")
    G_order = 60
    irrep_results = {}
    total = 0.0
    for name, chars in char_table.items():
        m = sum(class_sizes[k] * chars[k] * class_trace_avg[k] for k in range(5)) / G_order
        dim = chars[0]
        contribution = dim * m
        total += contribution
        irrep_results[name] = {"dim": dim, "multiplicity": m, "contribution": contribution}
        print(f"    {name:>3}  dim={dim}  mult={m:+.3f}  dim*mult={contribution:+.3f}")
    print(f"    Total: {total:.3f}  (should be {dim_null})")

    print("\n--- Step 4: Check for graph redundancy (identical adjacency rows) ---")
    # Group rows by their multiset of (column index, weight) pairs
    from collections import defaultdict
    row_signature_groups = defaultdict(list)
    for i in range(N):
        sig = tuple(sorted([(j, round(A[i, j], 6)) for j in range(N) if abs(A[i, j]) > 1e-9]))
        row_signature_groups[sig].append(i)

    duplicate_groups = [(sig, idxs) for sig, idxs in row_signature_groups.items() if len(idxs) > 1]
    n_dups = sum(len(g[1]) - 1 for g in duplicate_groups)
    print(f"  Distinct row signatures: {len(row_signature_groups)}")
    print(f"  Rows with duplicates: {n_dups} extra rows in {len(duplicate_groups)} duplicate groups")
    if duplicate_groups:
        sizes = sorted([len(g[1]) for g in duplicate_groups], reverse=True)
        print(f"  Duplicate group sizes (top 10): {sizes[:10]}")
    print(f"  Note: identical adjacency rows in symmetric A give zero eigenvalues; this is")
    print(f"  one structural mechanism for the large nullspace.")

    print("\n--- Step 5: Per-orbit nullspace contribution ---")
    # Assign each cage node to its orbit.
    node_to_orbit = {}
    for o_idx, o in enumerate(orbits):
        for n in o["nodes_6d_set"]:
            node_to_orbit[tuple(n)] = o_idx

    nodes_int_t = [tuple(int(c) for c in row) for row in nodes_6d]
    orbit_of_index = [node_to_orbit[nt] for nt in nodes_int_t]

    # For each nullvector v, compute the fraction of its norm coming from each orbit
    per_orbit_weight = np.zeros((dim_null, 4))
    for k in range(dim_null):
        v = null_basis[:, k]
        v2 = v ** 2
        for i in range(N):
            per_orbit_weight[k, orbit_of_index[i]] += v2[i]

    avg_per_orbit = per_orbit_weight.mean(axis=0)
    print(f"  Average (over {dim_null} null vectors) of |v|^2 contribution per orbit:")
    for o_idx, frac in enumerate(avg_per_orbit):
        print(f"    orbit {o_idx} (size {orbits[o_idx]['size']}, perp_norm {orbits[o_idx]['perp_norm']:.4f}): "
              f"{frac:.4f}  ({frac * 100:.1f}%)")

    print("\n" + "=" * 76)
    print("INTERPRETATION")
    print("=" * 76)
    if invariance_ok:
        print(f"  ker(A) IS I-invariant -> it decomposes into I-irrep blocks.")
        dominant = max(irrep_results.items(), key=lambda kv: kv[1]["contribution"])
        print(f"  Largest contributor to dim(ker) = {dim_null}: {dominant[0]} "
              f"(dim {dominant[1]['dim']} x mult {dominant[1]['multiplicity']:.3f} = "
              f"{dominant[1]['contribution']:.3f})")
        # Check if the irrep decomp matches a clean integer pattern
        ints_round = {k: round(v["multiplicity"]) for k, v in irrep_results.items()}
        consistency = all(abs(irrep_results[k]["multiplicity"] - ints_round[k]) < 0.05
                          for k in ints_round)
        print(f"  Integer-multiplicity consistency: {consistency} (multiplicities round to {ints_round})")
    else:
        print(f"  ker(A) is NOT I-invariant (max violation {max_violation:.3e}).")
        print(f"  -> The nullspace is not a clean union of I-irrep blocks.")
        print(f"  -> The eta_scalar = 0 result is not from representation-theoretic cancellation.")

    if n_dups > 0:
        print(f"  Graph redundancy is present: {n_dups} extra rows from {len(duplicate_groups)} duplicate groups.")
        print(f"  This contributes {n_dups} dimensions to the nullspace (one per duplicate per group).")
    else:
        print(f"  No row duplicates: the nullspace dimension is NOT from trivial row redundancy.")
    print("=" * 76)

    verdict = {
        "N_total": int(N),
        "dim_nullspace": int(dim_null),
        "n_edges": int(n_edges),
        "kernel_is_I_invariant": bool(invariance_ok),
        "max_invariance_violation": float(max_violation),
        "class_trace_avg_on_kernel": class_trace_avg,
        "irrep_decomposition_of_kernel": {
            k: {"dim": v["dim"], "multiplicity": v["multiplicity"], "contribution": v["contribution"]}
            for k, v in irrep_results.items()
        },
        "irrep_decomp_total": total,
        "row_duplicate_groups": [(len(g[1]), g[1][:5]) for g in duplicate_groups[:10]],
        "n_extra_rows_from_duplicates": int(n_dups),
        "avg_per_orbit_kernel_weight": [float(v) for v in avg_per_orbit],
    }
    out_path = ENGINE_ROOT / "data" / "protocol_n132_nullspace_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(verdict, f, indent=2)
    print(f"\nFull results saved to: {out_path}")
    print("=" * 76)


if __name__ == "__main__":
    main()
