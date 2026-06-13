#!/usr/bin/env python3
"""
protocol_o32_ko_dimension.py - O.32: KO-dimension of the finite cage spectral triple
=====================================================================================
Tests whether the GCT finite spectral triple built on the canonical 152-node
I_h-closed cage carries KO-dimension == 6 (mod 8), the value required by the
Connes Standard Model (Chamseddine-Connes-Marcolli 2007).

KO-dimension is fixed by three signs of the real structure J and grading gamma:
    J^2     = eps   * 1          (Connes sign table)
    J D     = eps'  * D J
    J gamma = eps'' * gamma J
KO-dim == 6 (mod 8)  <=>  (eps, eps', eps'') = (+1, +1, -1).

The real structure and grading are FIXED by cage geometry (declared before any
sign is computed; not chosen to hit a target):

    J     = P . C   where P = central-inversion permutation (x -> -x), C = conj
    gamma = real diagonal +/-1 grading g(x)

Because D_F is real and inversion-symmetric (P D_F = D_F P), eps and eps' are
FORCED:
    eps  = +1 : J^2 = P^2 = 1
    eps' = +1 : J D_F J^{-1} = P conj(D_F) P^{-1} = P D_F P^{-1} = D_F
So the entire KO-dim question reduces to whether a grading gamma with eps''=-1
exists. For a real diagonal grading, eps''=-1 means g(-x) = -g(x)
(inversion-odd), and the spectral-triple axiom gamma D_F = -D_F gamma means
g(x_i) g(x_j) = -1 on every bond (bond graph is bipartite). Hence:

    KO-dim 6 achievable on the bare cage
      <=>  the cage bond-graph admits an INVERSION-ODD proper 2-coloring.

This script decides that question.

SCOPE (load-bearing): the reduction fixes gamma to a real DIAGONAL grading,
which is the correct grading class only for the COMMUTATIVE point-algebra
C(cage nodes). The Connes Standard-Model finite triple uses the NONcommutative
A_F = C (+) H (+) M_3(C), whose grading need not be diagonal. A negative result
here therefore eliminates only the bare-cage / commutative-grading route to
KO-dim 6; it does NOT refute KO-dim 6 for the full noncommutative finite triple,
whose positive resolution requires the dressed (bimodule) Dirac operator and
bundles with Open Problem O.5.
"""

import json
import os
import sys
from collections import deque

import numpy as np

try:
    from gct_utils import get_output_path, PHI
except ImportError:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from gct_utils import get_output_path, PHI

from cage_builder import build_canonical_cage


def build_D_F(nodes_perp):
    """Cage adjacency: golden-weighted bonds at perp-distances {1, 1/phi}."""
    N = nodes_perp.shape[0]
    D = np.zeros((N, N))
    for i in range(N):
        for j in range(i + 1, N):
            d = np.linalg.norm(nodes_perp[i] - nodes_perp[j])
            if abs(d - 1.0) < 0.05:
                D[i, j] = D[j, i] = 1.0
            elif abs(d - (1.0 / PHI)) < 0.05:
                D[i, j] = D[j, i] = PHI
    return D


def inversion_permutation(nodes_6d):
    """Return sigma with nodes_6d[sigma[i]] = -nodes_6d[i], or None if not closed."""
    N = nodes_6d.shape[0]
    key = {tuple(np.round(x).astype(int)): i for i, x in enumerate(nodes_6d)}
    sigma = np.full(N, -1, dtype=int)
    for i, x in enumerate(nodes_6d):
        anti = tuple(np.round(-x).astype(int))
        if anti not in key:
            return None
        sigma[i] = key[anti]
    return sigma


def odd_cycle_certificate(adj_bool):
    """Return (triangle_nodes_or_None, total_triangle_count): an explicit
    triangle is a finite, human-checkable certificate of non-bipartiteness."""
    N = adj_bool.shape[0]
    first = None
    count = 0
    for i in range(N):
        Ni = np.nonzero(adj_bool[i])[0]
        Ni = Ni[Ni > i]
        for a in range(len(Ni)):
            for b in range(a + 1, len(Ni)):
                u, v = int(Ni[a]), int(Ni[b])
                if adj_bool[u, v]:
                    count += 1
                    if first is None:
                        first = (i, u, v)
    return first, count


def two_color_components(adj_bool):
    """BFS 2-coloring. Returns (colors in {0,1} or -1, list of components,
    is_bipartite)."""
    N = adj_bool.shape[0]
    color = np.full(N, -1, dtype=int)
    components = []
    bipartite = True
    for s in range(N):
        if color[s] != -1:
            continue
        comp = []
        color[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            comp.append(u)
            for v in np.nonzero(adj_bool[u])[0]:
                if color[v] == -1:
                    color[v] = color[u] ^ 1
                    q.append(v)
                elif color[v] == color[u]:
                    bipartite = False
        components.append(comp)
    return color, components, bipartite


def inversion_odd_2coloring_exists(adj_bool, sigma):
    """Given a bipartite bond graph, decide whether a proper 2-coloring exists
    that is also inversion-odd: g(sigma[i]) = -g(i) for all i.

    Within each connected component the proper 2-coloring is fixed up to a global
    flip. Encode each component's flip as a boolean f_c in GF(2). The base BFS
    coloring c0(i) yields g(i) = (-1)^(c0(i) XOR f_{comp(i)}).
    The inversion-odd constraint g(sigma[i]) = -g(i) becomes, in GF(2):
        c0(i) XOR f_{comp(i)} XOR c0(sigma[i]) XOR f_{comp(sigma[i])} = 1
    i.e.  f_a XOR f_b = 1 XOR c0(i) XOR c0(sigma[i])   (a=comp(i), b=comp(sigma[i]))
    This is a 2-coloring / union-find-with-parity feasibility problem.
    """
    color, components, bipartite = two_color_components(adj_bool)
    if not bipartite:
        return False, "bond graph is NOT bipartite", color, components

    comp_of = np.empty(adj_bool.shape[0], dtype=int)
    for ci, comp in enumerate(components):
        for u in comp:
            comp_of[u] = ci

    nC = len(components)
    parent = list(range(nC))
    rel = [0] * nC  # parity relative to parent

    def find(x):
        if parent[x] == x:
            return x, 0
        root, pr = find(parent[x])
        parent[x] = root
        rel[x] ^= pr
        return root, rel[x]

    def union(a, b, want):  # enforce f_a XOR f_b = want
        ra, pa = find(a)
        rb, pb = find(b)
        if ra == rb:
            return (pa ^ pb) == want
        parent[ra] = rb
        rel[ra] = pa ^ pb ^ want
        return True

    feasible = True
    for i in range(adj_bool.shape[0]):
        j = sigma[i]
        a, b = comp_of[i], comp_of[j]
        want = 1 ^ int(color[i]) ^ int(color[j])
        if a == b:
            # constraint must be self-consistent within one component
            ra, pa = find(a)
            # f_a XOR f_a = 0 must equal want
            if want != 0:
                feasible = False
                break
        else:
            if not union(a, b, want):
                feasible = False
                break
    msg = "inversion-odd proper 2-coloring EXISTS" if feasible else \
          "no inversion-odd proper 2-coloring (parity obstruction)"
    return feasible, msg, color, components


def run():
    print("=" * 68)
    print("GCT Protocol O.32 - KO-dimension of the finite cage spectral triple")
    print("=" * 68)

    nodes_6d, nodes_perp = build_canonical_cage(size=152)
    N = nodes_6d.shape[0]
    print(f"\n  Cage: N = {N} nodes (canonical I_h-closed orbit union)")

    D_F = build_D_F(nodes_perp)
    n_bonds = int((np.abs(D_F) > 1e-9).sum() // 2)
    print(f"  D_F bonds: {n_bonds}")
    if n_bonds == 0:
        print("  [!] No bonds at perp-distances {1, 1/phi}; D_F is trivial.")

    sigma = inversion_permutation(nodes_6d)
    if sigma is None:
        print("  [!] Cage NOT closed under central inversion -> J undefined.")
        return
    n_fixed = int((sigma == np.arange(N)).sum())
    print(f"  Central inversion P: well-defined involution "
          f"(fixed points = {n_fixed}, expected 0)")
    assert np.array_equal(sigma[sigma], np.arange(N)), "P not an involution"

    # --- eps, eps' : forced by D_F real + inversion-symmetric ---
    Pmat = np.zeros((N, N))
    Pmat[np.arange(N), sigma] = 1.0
    commute = np.allclose(Pmat @ D_F, D_F @ Pmat)
    print(f"\n  P commutes with D_F: {commute}  -> eps'=+1 forced")
    eps = +1     # J^2 = P^2 = 1
    eps_p = +1 if commute else None
    print(f"  eps  (J^2)   = {eps:+d}")
    print(f"  eps' (J D)   = {eps_p:+d}")

    # --- eps'' : the real question, reduced to a graph property ---
    adj_bool = np.abs(D_F) > 1e-9
    feasible, msg, color, comps = inversion_odd_2coloring_exists(adj_bool, sigma)
    eps_pp = -1 if feasible else None
    print(f"\n  Grading gamma test (reduces to inversion-odd 2-coloring):")
    print(f"    connected components: {len(comps)}")
    color_tmp, _, bip = two_color_components(adj_bool)
    print(f"    bond graph bipartite: {bip}")
    tri, tri_count = odd_cycle_certificate(adj_bool)
    if tri is not None:
        print(f"    odd-cycle certificate (triangle): {tri}  "
              f"(total triangles: {tri_count})")
    print(f"    -> {msg}")

    if feasible:
        ko = 6
        signs = (eps, eps_p, eps_pp)
        verdict = ("CAGE ADMITS KO-dim == 6 (mod 8): signs (eps,eps',eps'') "
                   "= (+1,+1,-1) achieved by geometrically-forced J and gamma.")
        passed = True
    else:
        ko = None
        signs = (eps, eps_p, None)
        verdict = ("NEGATIVE RESULT (scoped): the bare cage adjacency with a real "
                   "DIAGONAL grading does NOT admit a KO-dim-6 structure (eps''=-1 "
                   "unrealisable: bond graph non-bipartite). This eliminates the "
                   "bare-cage / commutative-grading route only; it does NOT refute "
                   "KO-dim 6 for the full noncommutative A_F triple, whose positive "
                   "resolution requires the dressed (bimodule) D_F and bundles with O.5.")
        passed = False

    print("\n  " + "-" * 64)
    print(f"  SIGNS (eps, eps', eps''): {signs}")
    print(f"  KO-dimension (mod 8): {ko}")
    print(f"  VERDICT: {verdict}")
    print("=" * 68)

    results = {
        "N": N,
        "n_bonds": n_bonds,
        "inversion_well_defined": True,
        "P_commutes_with_D_F": bool(commute),
        "eps_Jsq": eps,
        "eps_p_JD": eps_p,
        "eps_pp_Jgamma": eps_pp,
        "bond_graph_bipartite": bool(bip),
        "odd_cycle_certificate_triangle": list(tri) if tri is not None else None,
        "triangle_count": tri_count,
        "n_components": len(comps),
        "inversion_odd_2coloring_exists": bool(feasible),
        "ko_dimension_mod8": ko,
        "ko_dimension_check_performed": True,
        "signs_required_for_ko6": [1, 1, -1],
        "pass_ko6": bool(passed),
        "verdict": verdict,
        "method": ("J = central-inversion . conjugation; gamma = inversion-odd "
                   "real diagonal grading; eps,eps' forced by D_F real + "
                   "inversion-symmetric; eps'' reduced to inversion-odd proper "
                   "2-coloring of the cage bond graph."),
    }
    out = get_output_path("protocol_o32_ko_dimension_results.json")
    with open(out, "w") as fp:
        json.dump(results, fp, indent=2)
    print(f"\n[Saved JSON] -> {out}")
    return results


if __name__ == "__main__":
    run()
