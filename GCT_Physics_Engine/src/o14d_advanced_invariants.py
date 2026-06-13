#!/usr/bin/env python3
"""
o14d_advanced_invariants.py - Routes (alpha') and (beta) for O.14d closure.

Route (alpha'): I-character analysis to distinguish T_1 vs T_2 irrep
multiplicities (the "n_T" aggregate in o14d_irrep_decomp.py).
Uses standard I character table + permutation-representation character
trace = fixed-point count per group element.

Route (beta):  Discrete topological / spectral invariants of the bond graph:
    - Total bond count
    - Number of triangles (3-cycles)
    - Number of 4-cycles
    - Spectral moments Tr(A^k) for k = 2..6
    - Adjacency-matrix determinant
    - Permanent of A_{pos eigenvalues sign matrix}
Hypothesis: at least one invariant uniquely identifies pair (8, 13).
"""

import math
import json
import sys
from itertools import combinations, product
from pathlib import Path
from collections import Counter
import numpy as np

# SSOT import (canonical PHI from gct_constants.yaml via gct_utils)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from gct_utils import C  # noqa: E402
PHI = float(C.PHI)
PHI_CONJ = -1.0 / PHI

ENGINE_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = ENGINE_ROOT / "data" / "o14d_advanced_invariants_results.json"

# Standard I character table (conjugacy classes: e, 12 C_5, 12 C_5^2, 20 C_3, 15 C_2)
# Order matters: index 0 = identity, 1 = C_5 (5-fold rot by 2pi/5), 2 = C_5^2 (4pi/5),
#                3 = C_3 (3-fold rot by 2pi/3), 4 = C_2 (2-fold rot by pi)
CLASS_NAMES = ["E", "C5", "C5sq", "C3", "C2"]
CLASS_SIZES = [1, 12, 12, 20, 15]
I_ORDER = 60

# Characters indexed by (irrep, class)
PHI_VAL = PHI
INV_PHI = 1.0 / PHI
CHAR_TABLE = {
    "A":  [1,  1,         1,         1, 1],
    "T1": [3,  PHI_VAL,  -INV_PHI,   0, -1],
    "T2": [3, -INV_PHI,   PHI_VAL,   0, -1],
    "G":  [4, -1,        -1,         1, 0],
    "H":  [5,  0,         0,        -1, 1],
}


def get_m_perp():
    ip = PHI_CONJ
    raw = np.array([
        [1.0, ip,  0.0, -1.0, ip,  0.0],
        [ip,  0.0, 1.0, ip,  0.0, -1.0],
        [0.0, 1.0, ip,  0.0, -1.0, ip],
    ], dtype=np.float64)
    N_perp = 1.0 / np.sqrt(2.0 * (2.0 + ip))
    return N_perp * raw


def gen_z6_points(R=3, perp_cutoff=3.0):
    M_perp = get_m_perp()
    pts_6d = []
    pts_perp = []
    for coords in product(range(-R, R + 1), repeat=6):
        x = np.array(coords, dtype=np.float64)
        if np.all(x == 0):
            continue
        xp = M_perp @ x
        if np.linalg.norm(xp) <= perp_cutoff:
            pts_6d.append(x)
            pts_perp.append(xp)
    return np.array(pts_6d), np.array(pts_perp)


def icosahedral_rotations(vertices_perp):
    axis5 = vertices_perp[0] / np.linalg.norm(vertices_perp[0])
    dists = np.linalg.norm(vertices_perp - vertices_perp[0], axis=1)
    nearest_idx = np.argsort(dists)[1:6]
    nb = vertices_perp[nearest_idx]
    edge = dists[nearest_idx[0]]
    triangle_partner = None
    for i in range(len(nearest_idx)):
        for j in range(i + 1, len(nearest_idx)):
            if abs(np.linalg.norm(nb[i] - nb[j]) - edge) < 0.05 * edge:
                triangle_partner = (i, j)
                break
        if triangle_partner:
            break
    face_center = (vertices_perp[0] + nb[triangle_partner[0]] + nb[triangle_partner[1]]) / 3.0
    axis3 = face_center / np.linalg.norm(face_center)

    def rot(axis, theta):
        a = axis / np.linalg.norm(axis)
        K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
        return np.eye(3) + math.sin(theta) * K + (1 - math.cos(theta)) * (K @ K)

    R5 = rot(axis5, 2 * math.pi / 5)
    R3 = rot(axis3, 2 * math.pi / 3)
    rotations = [np.eye(3)]
    queue = [np.eye(3)]
    while queue and len(rotations) < 60:
        g = queue.pop(0)
        for h in (R5, R3, R5.T, R3.T):
            new = g @ h
            if not any(np.allclose(e, new, atol=1e-8) for e in rotations):
                rotations.append(new)
                queue.append(new)
                if len(rotations) >= 60:
                    break
    return rotations


def lift_to_6d(R, vertices_perp):
    M = np.zeros((6, 6))
    for i in range(6):
        rv = R @ vertices_perp[i]
        best_j, best_sign, best_err = -1, 0, float('inf')
        for j in range(6):
            for sign in (+1, -1):
                err = np.linalg.norm(rv - sign * vertices_perp[j])
                if err < best_err:
                    best_err, best_j, best_sign = err, j, sign
        if best_err > 0.05:
            return None
        M[best_j, i] = best_sign
    return M


def classify_rotation(R_3d):
    """Assign 3D rotation to conjugacy class via its trace."""
    tr = np.trace(R_3d)
    # Class traces: E=3, C5=phi, C5^2=-1/phi, C3=0, C2=-1
    if abs(tr - 3) < 1e-4:
        return 0  # E
    if abs(tr - PHI) < 1e-4:
        return 1  # C5
    if abs(tr - (-INV_PHI)) < 1e-4:
        return 2  # C5^2
    if abs(tr) < 1e-4:
        return 3  # C3
    if abs(tr - (-1)) < 1e-4:
        return 4  # C2
    return -1


def enumerate_i_orbits(pts_6d, six_d_matrices):
    N = len(pts_6d)
    visited = [False] * N
    orbits = []
    for start in range(N):
        if visited[start]:
            continue
        orbit = [start]
        visited[start] = True
        queue = [start]
        while queue:
            i = queue.pop()
            for M in six_d_matrices:
                img = M @ pts_6d[i]
                for j in range(N):
                    if not visited[j] and np.linalg.norm(pts_6d[j] - img) < 1e-6:
                        visited[j] = True
                        orbit.append(j)
                        queue.append(j)
                        break
        orbits.append(orbit)
    return orbits


def build_adjacency(nodes_perp):
    N = len(nodes_perp)
    A = np.zeros((N, N))
    for i in range(N):
        for j in range(i + 1, N):
            d = np.linalg.norm(nodes_perp[i] - nodes_perp[j])
            if abs(d - 1.0) < 0.05:
                A[i, j] = A[j, i] = 1.0
            elif abs(d - 1.0 / PHI) < 0.05:
                A[i, j] = A[j, i] = PHI
    return A


def fixed_point_count(cage_6d, M):
    """Count cage nodes fixed by 6D matrix M."""
    images = cage_6d @ M.T
    n_fixed = 0
    for i in range(len(cage_6d)):
        if np.linalg.norm(images[i] - cage_6d[i]) < 1e-6:
            n_fixed += 1
    return n_fixed


def character_decomposition(cage_6d, six_d_matrices, rot_class):
    """Compute multiplicity of each I-irrep in the permutation representation
    of I on the cage. Uses character orthogonality:
        n_rho = (1/|I|) sum_g chi_rho(g)^* * chi_perm(g)
    chi_perm(g) = number of fixed points of g on the cage.
    """
    # Sum fixed points by conjugacy class
    class_fp = [0] * 5
    for k, M in enumerate(six_d_matrices):
        c = rot_class[k]
        if c >= 0:
            class_fp[c] += fixed_point_count(cage_6d, M)
    # Average within each class
    class_fp_avg = [class_fp[c] / CLASS_SIZES[c] for c in range(5)]
    # chi_perm(g) for g in class c is class_fp_avg[c] (since all g in a class have same fp count)
    # n_rho = (1/|I|) sum_c |c| * chi_rho(c) * chi_perm(c)
    mults = {}
    for rho_name, chi in CHAR_TABLE.items():
        n = sum(CLASS_SIZES[c] * chi[c] * class_fp_avg[c] for c in range(5)) / I_ORDER
        mults[rho_name] = round(n)
    return mults, class_fp_avg


def topological_invariants(A):
    """Compute several discrete topological invariants of the bond graph."""
    N = A.shape[0]
    # Binary adjacency (1 if bonded, else 0) - for cycle counts use unweighted version
    A_bool = (np.abs(A) > 1e-8).astype(int)
    A_pow = np.eye(N, dtype=int)
    moments = []
    A2 = A_bool @ A_bool
    A3 = A2 @ A_bool
    A4 = A3 @ A_bool
    n_edges = int(np.sum(A_bool)) // 2
    # Triangle count: tr(A^3) / 6
    n_triangles = int(np.trace(A3)) // 6
    # 4-cycle count: (tr(A^4) - 2*n_edges - 4*P_2) / 8 where P_2 = number of paths of length 2 = sum d_i*(d_i-1)/2
    degrees = A_bool.sum(axis=1)
    n_paths_2 = int(sum(d * (d - 1) // 2 for d in degrees))
    n_4cycles = (int(np.trace(A4)) - 2 * n_edges - 4 * n_paths_2) // 8
    # Spectral moments (weighted adjacency)
    spec_moments = []
    Akw = np.eye(N)
    for k in range(1, 7):
        Akw = Akw @ A
        spec_moments.append(round(float(np.trace(Akw)), 4))
    # Determinant
    det_A = round(float(np.linalg.det(A)), 4)
    return {
        "n_edges": n_edges,
        "n_triangles": n_triangles,
        "n_4cycles": n_4cycles,
        "max_degree": int(max(degrees)),
        "min_degree": int(min(degrees)),
        "degree_dist": dict(Counter(degrees.tolist())),
        "tr_A2": spec_moments[1],
        "tr_A3": spec_moments[2],
        "tr_A4": spec_moments[3],
        "tr_A5": spec_moments[4],
        "tr_A6": spec_moments[5],
        "det_A": det_A,
    }


def main():
    print("=" * 80)
    print("  O.14d routes (alpha') + (beta): refined invariant analysis")
    print("=" * 80)

    M_perp = get_m_perp()
    vertices_6d = np.vstack([np.eye(6), -np.eye(6)])
    vertices_perp = vertices_6d @ M_perp.T

    print("\n[1] Setup I-group + classify rotations by conjugacy class...")
    rotations_3d = icosahedral_rotations(vertices_perp)
    six_d_matrices = [lift_to_6d(R, vertices_perp) for R in rotations_3d]
    keep = [(R, M) for R, M in zip(rotations_3d, six_d_matrices) if M is not None]
    rotations_3d = [r for r, _ in keep]
    six_d_matrices = [m for _, m in keep]
    rot_class = [classify_rotation(R) for R in rotations_3d]
    cls_hist = Counter(rot_class)
    print(f"    Conjugacy class distribution: {dict(sorted(cls_hist.items()))}")
    print(f"    (Expected: 0:1, 1:12, 2:12, 3:20, 4:15)")

    print("\n[2] Enumerate Z^6 + I-orbits...")
    pts_6d, pts_perp = gen_z6_points(R=3, perp_cutoff=3.0)
    norms = np.linalg.norm(pts_perp, axis=1)
    order = np.argsort(norms)[:600]
    pts_6d, pts_perp, norms = pts_6d[order], pts_perp[order], norms[order]
    orbits_idx = enumerate_i_orbits(pts_6d, six_d_matrices)
    orbits = []
    for ob in orbits_idx:
        orbits.append({"size": len(ob), "min_perp_norm": float(min(norms[i] for i in ob)),
                       "indices": ob, "nodes_perp": pts_perp[ob], "nodes_6d": pts_6d[ob]})
    orbits.sort(key=lambda o: o["min_perp_norm"])
    twelve_idx = [k for k, o in enumerate(orbits) if o["size"] == 12]
    sixty_idx = [k for k, o in enumerate(orbits) if o["size"] == 60]
    print(f"    12-orbits at {twelve_idx}, 60-orbits at {sixty_idx}")

    print("\n[3] For each [12, 60, 12, 60] pairing: T_1/T_2 character decomp + topological invariants...")
    results = []
    for combo in combinations(sixty_idx, 2):
        sub = twelve_idx + list(combo)
        nodes_perp = np.vstack([orbits[i]["nodes_perp"] for i in sub])
        nodes_6d = np.vstack([orbits[i]["nodes_6d"] for i in sub])
        A = build_adjacency(nodes_perp)
        evals = np.linalg.eigvalsh(A)
        nz = evals[np.abs(evals) > 1e-12]
        eta = float(np.sum(np.sign(nz)))

        # Route (alpha') -- character decomposition with T_1 / T_2 distinguished
        mults, class_fp_avg = character_decomposition(nodes_6d, six_d_matrices, rot_class)

        # Route (beta) -- topological invariants
        invs = topological_invariants(A)

        results.append({
            "pair": list(combo),
            "eta": eta,
            "char_mults": mults,
            "class_fp_avg": [round(x, 3) for x in class_fp_avg],
            "topo": invs,
        })

    # Print table
    print(f"\n    {'pair':>8} {'eta':>6} {'A':>3} {'T1':>3} {'T2':>3} {'G':>3} {'H':>3} {'tri':>4} {'4c':>5} {'edges':>6}")
    for r in results:
        m = r["char_mults"]
        t = r["topo"]
        marker = " <-- WINNER" if abs(r["eta"] - (-8)) < 0.5 else ""
        print(f"    {str(r['pair']):>8} {r['eta']:>6.1f} {m['A']:>3} {m['T1']:>3} {m['T2']:>3} {m['G']:>3} {m['H']:>3} {t['n_triangles']:>4} {t['n_4cycles']:>5} {t['n_edges']:>6}{marker}")

    print()
    winner = next(r for r in results if abs(r["eta"] - (-8)) < 0.5)
    print(f"[4] Winner = pair {winner['pair']}")
    print(f"    char_mults = {winner['char_mults']}  (A, T1, T2, G, H)")
    print(f"    topo = {winner['topo']}")

    print("\n[5] Test each invariant for uniqueness on the winner...")

    # Check route (alpha') -- T_1 vs T_2 split
    char_profiles = [(tuple(r["char_mults"][k] for k in ("A", "T1", "T2", "G", "H")), r["pair"]) for r in results]
    winner_char = next(p for p, pair in char_profiles if pair == winner["pair"])
    n_match_char = sum(1 for p, _ in char_profiles if p == winner_char)
    print(f"    Route (alpha') T1/T2 character profile: {n_match_char}/21 pairings match winner")
    if n_match_char == 1:
        print(f"      *** UNIQUE: route (alpha') closes O.14d ***")

    # Check route (beta) candidate invariants
    print("\n    Route (beta) invariants:")
    invariant_keys = ["n_edges", "n_triangles", "n_4cycles", "tr_A2", "tr_A3", "tr_A4", "tr_A5", "tr_A6", "det_A"]
    for key in invariant_keys:
        values = [(r["topo"][key], r["pair"]) for r in results]
        winner_v = next(v for v, p in values if p == winner["pair"])
        n_match = sum(1 for v, _ in values if v == winner_v)
        flag = " *** UNIQUE -- CLOSES O.14d via " + key + " ***" if n_match == 1 else ""
        print(f"      {key:>15} = {winner_v} -> {n_match}/21 pairings match{flag}")

    # Combinations of multiple invariants
    print("\n    Compound invariant: (n_triangles, n_4cycles)")
    pairs_to_topo = [((r["topo"]["n_triangles"], r["topo"]["n_4cycles"]), r["pair"]) for r in results]
    winner_t = next(t for t, p in pairs_to_topo if p == winner["pair"])
    n_match = sum(1 for t, _ in pairs_to_topo if t == winner_t)
    print(f"      winner (n_tri, n_4c) = {winner_t} -> {n_match}/21 pairings match{' *** UNIQUE ***' if n_match == 1 else ''}")

    print("\n    Compound: (n_triangles, n_4cycles, tr_A4)")
    cmp2 = [((r["topo"]["n_triangles"], r["topo"]["n_4cycles"], r["topo"]["tr_A4"]), r["pair"]) for r in results]
    winner_c = next(c for c, p in cmp2 if p == winner["pair"])
    n_match = sum(1 for c, _ in cmp2 if c == winner_c)
    print(f"      winner profile -> {n_match}/21 pairings match{' *** UNIQUE ***' if n_match == 1 else ''}")

    print("\n    Compound: full topo signature (all invariants)")
    full = [(tuple(r["topo"][k] for k in invariant_keys), r["pair"]) for r in results]
    winner_f = next(f for f, p in full if p == winner["pair"])
    n_match = sum(1 for f, _ in full if f == winner_f)
    print(f"      winner full topo -> {n_match}/21 pairings match{' *** UNIQUE ***' if n_match == 1 else ''}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        json.dump({
            "winner_pair": winner["pair"],
            "winner_char_mults": winner["char_mults"],
            "winner_topo": winner["topo"],
            "all_results": results,
        }, f, indent=2)
    print(f"\n  Output: {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
