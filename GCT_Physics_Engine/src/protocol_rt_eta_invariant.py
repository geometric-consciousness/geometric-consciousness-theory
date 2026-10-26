#!/usr/bin/env python3
"""
protocol_rt_eta_invariant.py
=============================
Finite-matrix diagnostic: compute the sign count of a 90x90 doubled-incidence
matrix built from the Rhombic Triacontahedron (RT) face graph. This matrix is
not a qualifying APS boundary operator, and its sign count is independent of
the separate undefined eta-alpha coupling ansatz.

Setup:
  - RT face adjacency = icosidodecahedron edge graph (the dual polyhedron)
  - 30 vertices (= RT faces), 60 edges, valency 4
  - Built combinatorially: rectified icosahedron — vertices are midpoints of
    the 30 icosahedron edges; edges of the icosidodecahedron connect midpoints
    of icosahedron edges that share an icosahedron face.

For every finite self-adjoint matrix the nonzero-eigenvalue sign count is an
integer, regardless of whether its entries are integer, golden-weighted, or
otherwise real/complex. That elementary fact neither constrains a regularised
APS eta-invariant nor rules on eta-alpha. The open outcome is the absence of a
specified operator/domain/comparison map.
"""

import math
import json
import numpy as np
from pathlib import Path
from itertools import combinations
from gct_utils import C

PHI = float(C.PHI)


def icosahedron_combinatorial():
    """
    Return 12-vertex icosahedron as (vertices, edges).
    Vertex coords: standard (0, ±1, ±φ) + cyclic perms, 12 total.
    Edge: pair of vertices at distance 2 (the icosahedron edge length).
    """
    verts = []
    for c1, c2 in [(1, PHI), (-1, PHI), (1, -PHI), (-1, -PHI)]:
        verts.append(np.array([0.0, c1, c2]))
        verts.append(np.array([c1, c2, 0.0]))
        verts.append(np.array([c2, 0.0, c1]))
    edges = []
    edge_len_sq = 4.0  # for these coords, icosahedron edge length = 2
    for i in range(12):
        for j in range(i + 1, 12):
            if abs(np.linalg.norm(verts[i] - verts[j]) ** 2 - edge_len_sq) < 1e-6:
                edges.append((i, j))
    assert len(edges) == 30, f"expected 30 ico edges, got {len(edges)}"
    return verts, edges


def icosidodecahedron_face_adjacency():
    """
    Return adjacency matrix A (30x30) of the icosidodecahedron graph.
    Vertices = icosahedron edge midpoints; two midpoints are connected if
    their underlying icosahedron edges share an icosahedron face (i.e., share
    a common vertex AND lie in a common triangle).

    Equivalent (simpler) description: two midpoints are connected iff
    their underlying icosahedron edges share exactly one vertex.
    (Two edges sharing a vertex always lie in a unique common face because
    the icosahedron is 3-connected; the linkage gives valency 4 per midpoint.)
    """
    ico_verts, ico_edges = icosahedron_combinatorial()
    n_ico_edges = len(ico_edges)  # = 30
    # Build vertex-adjacency for icosahedron (to check triangle membership)
    ico_vert_adj = set()
    for (u, v) in ico_edges:
        ico_vert_adj.add((u, v))
        ico_vert_adj.add((v, u))
    A = np.zeros((n_ico_edges, n_ico_edges), dtype=int)
    for a in range(n_ico_edges):
        for b in range(a + 1, n_ico_edges):
            shared = set(ico_edges[a]) & set(ico_edges[b])
            if len(shared) == 1:
                # Other two vertices: one from each edge
                a_other = (set(ico_edges[a]) - shared).pop()
                b_other = (set(ico_edges[b]) - shared).pop()
                # Triangle condition: the two "other" endpoints must be ico-adjacent
                if (a_other, b_other) in ico_vert_adj:
                    A[a, b] = 1
                    A[b, a] = 1
    return A, ico_edges


def discrete_dirac_chiral(A):
    """
    Build a discrete Dirac-like operator. Use the signed incidence matrix
    construction: pick an orientation on each edge, build incidence matrix C
    of shape (n_edges, n_vertices) with +1/-1 entries. Then the chiral Dirac
    operator on the doubled space {vertices, edges} is
        D = [[0, C^T], [C, 0]]
    with chirality γ = diag(+I_n, -I_m). η = Σ sign(λ) for λ in spec(D).
    """
    n = A.shape[0]
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if A[i, j] != 0:
                edges.append((i, j))
    n_edges = len(edges)
    C = np.zeros((n_edges, n))
    for e, (i, j) in enumerate(edges):
        C[e, i] = +1.0
        C[e, j] = -1.0
    # Block-off-diagonal Dirac
    D = np.zeros((n + n_edges, n + n_edges))
    D[:n, n:] = C.T
    D[n:, :n] = C
    return D, edges


def compute_sign_count(D, eps=1e-9):
    """Return Σ sign(λ) for the non-zero eigenvalues of finite matrix D."""
    eigs = np.linalg.eigvalsh(D)
    nonzero = eigs[np.abs(eigs) > eps]
    sign_count = float(np.sum(np.sign(nonzero)))
    n_kernel = int(len(eigs) - len(nonzero))
    return sign_count, n_kernel, eigs


def main():
    print("=" * 72)
    print("Finite 90x90 RT doubled-incidence sign-count diagnostic")
    print("=" * 72)

    # Step 1: Build the icosidodecahedron face graph (= RT face adjacency)
    A, ico_edges = icosidodecahedron_face_adjacency()
    n = A.shape[0]
    degrees = A.sum(axis=1)
    print(f"\nRT face adjacency (via icosidodecahedron edge graph):")
    print(f"  Vertices (= RT faces): {n} (expected 30)")
    print(f"  Edges: {A.sum() // 2} (expected 60)")
    print(f"  Valency: min={degrees.min()}, max={degrees.max()} (expected 4 uniformly)")
    assert n == 30
    assert A.sum() // 2 == 60
    assert (degrees == 4).all()
    print(f"  ✓ Geometry verified")

    # Step 2: Discrete Dirac
    D, dirac_edges = discrete_dirac_chiral(A)
    print(f"\nDiscrete Dirac operator: {D.shape} (30 face vertices + 60 edges = 90 dim)")

    # Step 3: finite spectrum and sign count
    sign_count, n_kernel, eigs = compute_sign_count(D)
    n_pos = int((eigs > 1e-9).sum())
    n_neg = int((eigs < -1e-9).sum())
    print(f"\nSpectrum of D:")
    print(f"  Total eigenvalues: {len(eigs)}")
    print(f"  Kernel (zero modes): {n_kernel}")
    print(f"  Positive: {n_pos}")
    print(f"  Negative: {n_neg}")
    print(f"  Spectral range: [{eigs.min():.4f}, {eigs.max():.4f}]")
    print(f"\n  sign count = Σ sign(λ) = n_pos - n_neg = {n_pos - n_neg} = {sign_count:+.6f}")

    # Step 4: Compare to target
    alpha_inv_CODATA  = 137.035999177
    alpha_inv_tree    = 360.0 * PHI ** (-2)
    alpha_inv_bilayer = alpha_inv_tree * (1.0 - 1.0 / 288.0)
    twice_residual_pre   = 2.0 * (alpha_inv_CODATA - alpha_inv_tree)
    twice_residual_post  = 2.0 * (alpha_inv_CODATA - alpha_inv_bilayer)

    print(f"\nNumerical non-identification comparison only:")
    print(f"  Twice the pre-bilayer residual:  {twice_residual_pre:+.6f}")
    print(f"  Twice the post-bilayer residual: {twice_residual_post:+.6f}")

    matches_pre  = abs(sign_count - twice_residual_pre) < 0.05
    matches_post = abs(sign_count - twice_residual_post) < 0.005

    print(f"\nResult:")
    print(f"  Pre-bilayer closure: {'PASS' if matches_pre else 'FAIL'}")
    print(f"  Post-bilayer closure: {'PASS' if matches_post else 'FAIL'}")

    # Object/domain observation
    print(f"\n--- OBJECT/DOMAIN STATUS ---")
    sign_count_is_integer = abs(sign_count - round(sign_count)) < 1e-6
    print(f"  Finite sign count is integer-valued? {sign_count_is_integer}")
    print(f"  This is true for any finite self-adjoint matrix, independent of weights.")
    print(f"  No qualifying APS operator/domain/index or graph-to-smooth comparison is supplied.")
    print(f"  Therefore this diagnostic neither evaluates APS eta nor constrains eta-alpha.")

    out = {
        "rt_face_graph": {
            "vertices": int(n),
            "edges": int(A.sum() // 2),
            "valency": 4,
            "is_distance_regular": True,
            "matches_icosidodecahedron": True,
        },
        "dirac_operator": {
            "construction": "doubled-space chiral, [[0,C^T],[C,0]] with signed incidence",
            "dim": int(D.shape[0]),
            "weighting": "integer (±1 on edges)",
        },
        "spectrum": {
            "n_eigenvalues": len(eigs),
            "n_kernel": n_kernel,
            "n_positive": n_pos,
            "n_negative": n_neg,
            "eigenvalue_min": float(eigs.min()),
            "eigenvalue_max": float(eigs.max()),
        },
        "finite_matrix_sign_count": sign_count,
        "sign_count_is_integer": bool(sign_count_is_integer),
        "alpha_inv_CODATA": alpha_inv_CODATA,
        "alpha_inv_tree": alpha_inv_tree,
        "alpha_inv_bilayer": alpha_inv_bilayer,
        "twice_residual_pre_bilayer": twice_residual_pre,
        "twice_residual_post_bilayer": twice_residual_post,
        "pre_bilayer_pass": bool(matches_pre),
        "post_bilayer_pass": bool(matches_post),
        "object_status": (
            "Finite 90x90 doubled-incidence sign count only; integer-valued for any "
            "finite self-adjoint matrix regardless of weights. No qualifying APS "
            "operator/domain/index or comparison to eta-alpha is supplied."
        ),
        "test_outcome": "OPEN_CONDITIONAL — finite sign-count diagnostic only; APS operator/domain/comparison absent",
    }
    out_path = Path(__file__).parent.parent / "data" / "protocol_rt_eta_invariant_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nFull results: {out_path}")
    print("=" * 72)


if __name__ == "__main__":
    main()
