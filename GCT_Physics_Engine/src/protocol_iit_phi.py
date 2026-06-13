#!/usr/bin/env python3
"""
protocol_iit_phi.py

Necessary-condition graph-theoretic checks for possible IIT Phi > 0 on the
k=12 icosahedral adjacency graph (degree-5 regular).

Engine binding: V1 Ch17 §17.5.1 uses this script as the graph-theoretic
necessary-condition witness (min-cut + spectral gap). The full IIT Phi
sub-graph computation is in protocol_iit_phi_pyphi.py; the full k=12 Phi_max
calculation remains Open Problem O.28.

The script computes three well-defined quantities on the adjacency graph:

  1. min_cut_edges:                the minimum number of edges crossing any
                                   bipartition (S, V\S) with 1 <= |S| <= |V|/2.
                                   For a connected graph this is strictly
                                   positive, which is a necessary (not
                                   sufficient) condition for the canonical
                                   IIT 3.0 Phi to be non-zero on any TPM
                                   derived from this connectivity. For the
                                   canonical k=12 icosahedron, min_cut = 5
                                   (the single-vertex cut from its 5 neighbours).

  2. balanced_bisection_cut_at_k_half: the minimum number of cut edges over
                                   bipartitions with |S| = |V|/2. For the
                                   canonical k=12 icosahedron this is 10
                                   (the equator cut between the upper and
                                   lower pentagonal antiprism caps).

  3. spectral_gap:                 lambda_1 - |lambda_2| of the normalized
                                   adjacency matrix (the random-walk TPM
                                   spectral gap). For the regular icosahedral
                                   graph this is a closed-form invariant of
                                   the geometry.

A genuine IIT 3.0 Phi computation requires building the full transition-
probability matrix and integrating over partitions (NP-hard for N > ~10).
A full PyPhi implementation on the k=12 icosahedral TPM is registered as
Open Problem O.28 (consciousness-sector code closure). The two quantities
above are the engine-side necessary-condition witnesses; the manuscript's
quantitative GCT-vs-IIT divergence framing is conditional on O.28 closure.
"""

import json
import os
import sys
from itertools import combinations

import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from gct_lattice import GCTLattice


def _build_icosahedral_adjacency() -> np.ndarray:
    """
    Construct the k=12 icosahedral nearest-neighbour adjacency matrix from the
    GCT lattice projection. If the lattice projection does not yield the
    canonical degree-5 regular structure, fall back to the explicit canonical
    icosahedron edge list (Schlegel-projection labelling).
    """
    lattice = GCTLattice(R=1, perp_cutoff=2.5)
    origin_idx = np.argmin(np.linalg.norm(lattice.x_equilibrium, axis=1))
    neighbors = lattice.neighbor_indices[origin_idx]
    k = len(neighbors)

    x_nodes = lattice.x_equilibrium[neighbors]
    A = np.zeros((k, k))
    for i in range(k):
        for j in range(k):
            if i != j:
                dist2 = float(np.sum((x_nodes[i] - x_nodes[j]) ** 2))
                if abs(dist2 - 2.0) < 1e-4:
                    A[i, j] = 1

    degrees = np.sum(A, axis=1)
    if not np.allclose(degrees, 5):
        # Canonical icosahedron edge list (12 vertices, 30 edges, degree 5).
        # Indexing: 0 = north pole, 1-5 = upper pentagon, 6-10 = lower pentagon,
        # 11 = south pole.
        edges = [
            (0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
            (1, 2), (2, 3), (3, 4), (4, 5), (5, 1),
            (1, 6), (1, 10), (2, 6), (2, 7), (3, 7), (3, 8),
            (4, 8), (4, 9), (5, 9), (5, 10),
            (6, 7), (7, 8), (8, 9), (9, 10), (10, 6),
            (6, 11), (7, 11), (8, 11), (9, 11), (10, 11),
        ]
        A = np.zeros((12, 12))
        for u, v in edges:
            A[u, v] = 1
            A[v, u] = 1

    return A


def _min_cut_over_bipartitions(A: np.ndarray) -> int:
    """
    Compute the minimum number of cut edges over all bipartitions (S, V\S)
    with 1 <= |S| <= |V|/2. Strictly positive iff the graph is connected.
    """
    k = A.shape[0]
    nodes = list(range(k))
    min_cut = float("inf")
    for r in range(1, k // 2 + 1):
        for S in combinations(nodes, r):
            S_set = set(S)
            S_bar = [n for n in nodes if n not in S_set]
            cut = 0
            for u in S:
                for v in S_bar:
                    if A[u, v] == 1:
                        cut += 1
            if cut < min_cut:
                min_cut = cut
    return int(min_cut)


def _balanced_bisection_cut(A: np.ndarray) -> int:
    """
    Compute the minimum number of cut edges over balanced bipartitions
    (|S| = k/2). For the canonical k=12 icosahedral graph this is the
    |S| = 6 balanced-bisection cut, which the manuscript reports as 10.
    """
    k = A.shape[0]
    half = k // 2
    nodes = list(range(k))
    min_cut = float("inf")
    for S in combinations(nodes, half):
        S_set = set(S)
        S_bar = [n for n in nodes if n not in S_set]
        cut = 0
        for u in S:
            for v in S_bar:
                if A[u, v] == 1:
                    cut += 1
        if cut < min_cut:
            min_cut = cut
    return int(min_cut)


def _spectral_gap_normalized(A: np.ndarray) -> float:
    """
    Spectral gap of the normalized adjacency (random-walk TPM): lambda_1 - |lambda_2|.
    For a degree-d regular graph, lambda_1 = 1 and the gap is 1 - |lambda_2|.
    """
    d = np.sum(A, axis=1)
    P = A / d[:, None]
    eigvals = np.sort(np.abs(np.linalg.eigvals(P).real))[::-1]
    if len(eigvals) < 2:
        return 0.0
    return float(eigvals[0] - eigvals[1])


def run_iit_phi() -> dict:
    print("Initializing protocol_iit_phi...")
    A = _build_icosahedral_adjacency()
    k = A.shape[0]
    degrees = np.sum(A, axis=1)
    print(f"Icosahedral shell nodes (k): {k}")
    print(f"Graph degrees: {degrees}")

    min_cut = _min_cut_over_bipartitions(A)
    balanced_bisection_cut = _balanced_bisection_cut(A)
    spectral_gap = round(_spectral_gap_normalized(A), 12)

    print(f"Minimum cut edges over all bipartitions: {min_cut}")
    print(f"Balanced-bisection cut (|S|={k//2}): {balanced_bisection_cut}")
    print(f"Normalized adjacency spectral gap (lambda_1 - |lambda_2|): {spectral_gap:.4f}")

    graph_connectivity_witness_holds = min_cut > 0
    verdict_text = (
        "Necessary-condition witness PASSES: graph is connected (min_cut > 0) "
        "and spectrally non-trivial (gap > 0). A non-zero IIT 3.0 Phi on the "
        "k=12 icosahedral TPM is not excluded by the connectivity/spectral test. "
        "Full Phi quantification requires PyPhi integration (O.28)."
        if graph_connectivity_witness_holds and spectral_gap > 0
        else
        "Necessary-condition witness FAILS: graph is disconnected or spectrally trivial. "
        "IIT 3.0 Phi = 0 on this connectivity."
    )

    results = {
        "k_nodes": int(k),
        "graph_degree": int(degrees[0]) if np.allclose(degrees, degrees[0]) else None,
        "min_cut_edges": min_cut,
        "balanced_bisection_cut_at_k_half": balanced_bisection_cut,
        "spectral_gap_normalized": spectral_gap,
        "necessary_condition_holds": bool(graph_connectivity_witness_holds),
        "verdict": verdict_text,
        "phi_full_quantification": "DEFERRED — requires PyPhi build on the k=12 icosahedral TPM; registered as Open Problem O.28",
    }

    out_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "protocol_iit_phi_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=4)
    print(f"Results saved to {out_path}")
    return results


if __name__ == "__main__":
    run_iit_phi()
