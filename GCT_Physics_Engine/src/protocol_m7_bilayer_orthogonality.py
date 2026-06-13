#!/usr/bin/env python3
"""
protocol_m7_bilayer_orthogonality.py - App M S M.7 finite-N trace claims
==================================================================================
App M S M.7 grounds the alpha^-1 finite-N correction 1/(2N) = 1/288 in three
stacked claims:

  (C1) Single-shell decomposition Pi(0)|_N = sum_i G_ii^2 + sum_{i!=j} G_ij^2
       with the off-diagonal sum VANISHING "by the group orthogonality theorem"
       for any I_h-symmetric shell.                       [stated as rigorous]
  (C2) The surviving diagonal correction scales as 1/N.    [stated as rigorous]
  (C3) The two-level 144 = 12x12 cage structure, via the bilayer trace
       G^(2L) = G^(outer) (x) G^(inner), halves the correction: 1/N -> 1/(2N).
                                       [Tier 3 integer-factor handle; O.5]

This protocol evaluates what a finite computation can settle:

  T1 (literal C1): for real symmetric G, sum_{i!=j} G_ij^2 is a sum of squares;
     it vanishes iff every off-diagonal entry vanishes. Computed explicitly on
     exact I_h-symmetric shells under multiple natural Green's-function
     conventions. A nonzero value means the literal vanishing claim does not
     hold as written.
  T2 (charitable C1+C2): is there a reading under which the finite-N piece is
     diagonal-dominated with relative weight 1/N? We compute, per shell and per
     convention, the diagonal/off-diagonal split of Tr(G^2) and the vertex-
     transitivity identity sum_i G_ii^2 = (Tr G)^2 / N (exact on any vertex-
     transitive shell), which is the only rigorous 1/N structure available at
     this level: sum_i G_ii^2 / (Tr G)^2 = 1/N.
  T3 (C3): build G^(2L) = G_outer (x) G_inner literally (the manuscript's own
     tensor decomposition on 144 = 12x12) and compute the same quantities. The
     tensor identities give sum_d (G^2L_dd)^2 = [sum G_ii^2][sum g_jj^2] and
     (Tr G^2L)^2 = (Tr G)^2 (Tr g)^2, hence
        sum_d (G^2L_dd)^2 / (Tr G^2L)^2 = (1/12)(1/12) = 1/144 = 1/N,
     NOT 1/(2N). Any factor 2 must therefore come from structure OUTSIDE the
     stated tensor construction. The protocol verifies this numerically.

Green's-function conventions tested (reported side by side; none privileged):
  A) Laplacian resolvent  G = (L + m^2 I)^{-1},  m^2 in {0.01, 0.1, 1.0}
  B) Adjacency resolvent  G = (E I - A)^{-1},    E in {1.1, 2.0} * lambda_max
Shells: icosahedron (12), dodecahedron (20), icosidodecahedron (30), and the
12-vertex inner orbit of the canonical 152-cage. Bonds: nearest-neighbour
(minimal nonzero pairwise distance, tol 5%).
"""

import json
import os
import sys
import io

import numpy as np

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

try:
    from gct_utils import get_output_path, C
except ImportError:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from gct_utils import get_output_path, C

PHI = float(C.PHI)


# ---------------------------------------------------------------- shells
def icosahedron():
    v = []
    for s1 in (1, -1):
        for s2 in (1, -1):
            v += [(0, s1, s2 * PHI), (s1, s2 * PHI, 0), (s2 * PHI, 0, s1)]
    return np.array(sorted(set(v)), dtype=float)


def dodecahedron():
    v = []
    for s1 in (1, -1):
        for s2 in (1, -1):
            for s3 in (1, -1):
                v.append((s1, s2, s3))
    for s1 in (1, -1):
        for s2 in (1, -1):
            v += [(0, s1 / PHI, s2 * PHI), (s1 / PHI, s2 * PHI, 0),
                  (s2 * PHI, 0, s1 / PHI)]
    return np.array(sorted(set(v)), dtype=float)


def icosidodecahedron():
    v = []
    for s in (1, -1):
        v += [(s * PHI, 0, 0), (0, s * PHI, 0), (0, 0, s * PHI)]
    for s1 in (1, -1):
        for s2 in (1, -1):
            for s3 in (1, -1):
                v += [(s1 * 0.5, s2 * PHI / 2, s3 * PHI ** 2 / 2),
                      (s2 * PHI / 2, s3 * PHI ** 2 / 2, s1 * 0.5),
                      (s3 * PHI ** 2 / 2, s1 * 0.5, s2 * PHI / 2)]
    return np.array(sorted({tuple(row) for row in np.round(v, 10)}), dtype=float)


def cage12():
    from cage_builder import build_canonical_cage
    _, perp = build_canonical_cage(size=152)
    r = np.linalg.norm(perp, axis=1)
    inner_r = np.min(np.round(r, 4))
    return perp[np.abs(r - inner_r) < 1e-3]


def nn_adjacency(verts):
    d = np.linalg.norm(verts[:, None, :] - verts[None, :, :], axis=2)
    np.fill_diagonal(d, np.inf)
    dmin = d.min()
    A = (d < dmin * 1.05).astype(float)
    return A


# ---------------------------------------------------------- measurements
def measure(G):
    """Diagonal/off-diagonal split of the squared Green's function."""
    N = G.shape[0]
    diag2 = float(np.sum(np.diag(G) ** 2))
    total2 = float(np.sum(G ** 2))            # = Tr(G^2) for symmetric G
    off2 = total2 - diag2
    trG = float(np.trace(G))
    return {
        "N": N,
        "sum_offdiag_Gij_sq": off2,
        "offdiag_vanishes": bool(abs(off2) < 1e-12),
        "offdiag_over_total": off2 / total2 if total2 else None,
        "diag2_over_trG_sq": diag2 / trG ** 2 if trG else None,   # = 1/N iff
        "one_over_N": 1.0 / N,                                    # vertex-transitive
        "diag_const": bool(np.allclose(np.diag(G), np.diag(G)[0], rtol=1e-9)),
    }


def greens(A, convention):
    N = A.shape[0]
    deg = np.diag(A.sum(axis=1))
    L = deg - A
    if convention.startswith("laplacian"):
        m2 = float(convention.split("_")[1])
        return np.linalg.inv(L + m2 * np.eye(N))
    lam = float(convention.split("_")[1])
    lmax = np.max(np.abs(np.linalg.eigvalsh(A)))
    return np.linalg.inv(lam * lmax * np.eye(N) - A)


CONVENTIONS = ["laplacian_0.01", "laplacian_0.1", "laplacian_1.0",
               "adjacency_1.1", "adjacency_2.0"]


def run():
    print("=" * 74)
    print("GCT Protocol M.7 - bilayer orthogonality / 1/(2N) trace claims")
    print("=" * 74)

    shells = {
        "icosahedron_12": icosahedron(),
        "dodecahedron_20": dodecahedron(),
        "icosidodeca_30": icosidodecahedron(),
        "cage_inner_12": cage12(),
    }

    results = {"shells": {}, "bilayer": {}}
    t1_refuted_everywhere = True
    t2_holds_everywhere = True

    for name, verts in shells.items():
        A = nn_adjacency(verts)
        results["shells"][name] = {}
        print(f"\n  Shell {name}  (N={len(verts)}, "
              f"edges={int(A.sum()) // 2}, degree={int(A.sum(axis=1)[0])})")
        for conv in CONVENTIONS:
            G = greens(A, conv)
            m = measure(G)
            results["shells"][name][conv] = m
            if m["offdiag_vanishes"]:
                t1_refuted_everywhere = False
            ok_1overN = abs(m["diag2_over_trG_sq"] - m["one_over_N"]) < 1e-9
            if not ok_1overN:
                t2_holds_everywhere = False
            print(f"    {conv:>15}: off-diag sum sq = {m['sum_offdiag_Gij_sq']:.6e} "
                  f"(vanishes: {m['offdiag_vanishes']}); "
                  f"diag^2/(TrG)^2 = {m['diag2_over_trG_sq']:.6f} "
                  f"vs 1/N = {m['one_over_N']:.6f} -> {'OK' if ok_1overN else 'NO'}")

    # ------------------------------------------------ T3: bilayer tensor
    print("\n  Bilayer test: G^(2L) = G_outer (x) G_inner on 144 = 12 x 12")
    A12 = nn_adjacency(shells["icosahedron_12"])
    for conv in CONVENTIONS:
        G12 = greens(A12, conv)
        G2L = np.kron(G12, G12)
        m = measure(G2L)
        results["bilayer"][conv] = m
        print(f"    {conv:>15}: N={m['N']}  diag^2/(TrG)^2 = "
              f"{m['diag2_over_trG_sq']:.6f}  vs 1/N = {1 / 144:.6f}  "
              f"vs 1/(2N) = {1 / 288:.6f}")

    bilayer_gives_1_over_N = all(
        abs(m["diag2_over_trG_sq"] - 1.0 / 144.0) < 1e-9
        for m in results["bilayer"].values())

    print("\n  " + "-" * 70)
    print("  RESULTS")
    print(f"  T1 (literal off-diagonal vanishing): the off-diagonal sum of "
          f"squares evaluates to "
          f"{'strictly positive' if t1_refuted_everywhere else 'zero'} on every "
          f"I_h-symmetric shell under every convention tested, so the literal "
          f"vanishing claim "
          f"{'does not hold as written' if t1_refuted_everywhere else 'holds'}.")
    print(f"  T2 (1/N diagonal structure): "
          f"{'CONFIRMED' if t2_holds_everywhere else 'MIXED'} - on every "
          f"vertex-transitive shell, sum_i G_ii^2 / (Tr G)^2 = 1/N exactly "
          f"(constant-diagonal identity), independent of convention. This is "
          f"the rigorous content recoverable from the single-shell argument.")
    print(f"  T3 (bilayer factor 2): the manuscript's own tensor construction "
          f"gives diag^2/(TrG)^2 = 1/144 = 1/N "
          f"({'verified' if bilayer_gives_1_over_N else 'NOT verified'}), "
          f"NOT 1/(2N) = 1/288. The factor of 2 does not follow from the "
          f"stated G_outer (x) G_inner decomposition; it requires structure "
          f"outside that construction (O.5 closure target), consistent with "
          f"its Tier 3 integer-factor-handle status.")

    results["verdicts"] = {
        "T1_literal_offdiag_vanishing": "REFUTED" if t1_refuted_everywhere else "NOT_REFUTED",
        "T2_one_over_N_diagonal_identity": "CONFIRMED" if t2_holds_everywhere else "MIXED",
        "T3_bilayer_tensor_gives": "1/N (= 1/144), not 1/(2N)" if bilayer_gives_1_over_N else "inconsistent",
        "implication": ("S M.7's single-shell vanishing claim does not hold as "
                        "literally written (sum of squares); the rigorous core "
                        "is the vertex-transitivity identity sum G_ii^2/(Tr G)^2 "
                        "= 1/N. The bilayer factor 2 does not follow "
                        "from the stated tensor decomposition - it is a "
                        "Tier 3 handle pending O.5, as the IMPORTANT box "
                        "states."),
    }
    path = get_output_path("protocol_m7_bilayer_orthogonality_results.json")
    with open(path, "w") as fp:
        json.dump(results, fp, indent=2)
    print(f"\n[Saved JSON] -> {path}")
    return results


if __name__ == "__main__":
    run()
