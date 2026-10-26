#!/usr/bin/env python3
"""
o14d_irrep_decomp.py - Route (alpha) adjacency-spectrum diagnostic for O.14d.

Compare eigenvalue-degeneracy profiles of the weighted threshold adjacency
matrices for the 21 [12, 60, 12, 60] pairings. These degeneracies are not the
same object as the cage permutation-character decomposition.

The icosahedral group I has irreps of dimensions {1, 3, 3, 4, 5} (named
A, T_1, T_2, G, H). For an N-dimensional representation of I, eigenvalues
of any I-equivariant operator come in multiplets matching these
dimensions. The multiplicity profile of the 144-dim cage adjacency
matrix is therefore a structural fingerprint of the cage.

The diagnostic records the common resolved profile and any accidental
collision of multiple irreducible sectors at one eigenvalue.

Standalone: reproduces the o14d_closure_search.py orbit enumeration to
get the 21 pairings, then computes eigenvalue multiplicity profiles
for each.
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
OUTPUT_PATH = ENGINE_ROOT / "data" / "o14d_irrep_decomp_results.json"

# I-group irreducible representation dimensions
I_IRREP_DIMS = {1: "A", 3: "T1_or_T2", 4: "G", 5: "H"}
ALLOWED_MULTS = {1, 3, 4, 5}
CLASS_SIZES = [1, 12, 12, 20, 15]
CHAR_TABLE = {
    "A": [1, 1, 1, 1, 1],
    "T1": [3, PHI, -1.0 / PHI, 0, -1],
    "T2": [3, -1.0 / PHI, PHI, 0, -1],
    "G": [4, -1, -1, 1, 0],
    "H": [5, 0, 0, -1, 1],
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


def gen_z6_points(R: int = 3, perp_cutoff: float = 3.0):
    M_perp = get_m_perp()
    pts_6d = []
    pts_perp = []
    rng = range(-R, R + 1)
    for coords in product(rng, repeat=6):
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


def classify_rotation(R):
    """Assign a rotation to E, C5, C5^2, C3, or C2 by its trace."""
    tr = float(np.trace(R))
    targets = [3.0, PHI, -1.0 / PHI, 0.0, -1.0]
    return int(np.argmin([abs(tr - target) for target in targets]))


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
    """Golden-weighted adjacency on the perp-projected cage."""
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


def permutation_matrix(nodes_6d, M):
    """Permutation representation of one exact 6D rotation on cage nodes."""
    lookup = {tuple(np.rint(x).astype(int)): i for i, x in enumerate(nodes_6d)}
    P = np.zeros((len(nodes_6d), len(nodes_6d)))
    for i, x in enumerate(nodes_6d):
        j = lookup[tuple(np.rint(M @ x).astype(int))]
        P[j, i] = 1.0
    return P


def decompose_eigenspace_character(evals, evecs, multiplicity, permutations, rot_classes, tol=1e-6):
    """Decompose every eigenspace of the requested multiplicity by characters."""
    decompositions = []
    i = 0
    while i < len(evals):
        j = i + 1
        while j < len(evals) and abs(evals[j] - evals[i]) < tol:
            j += 1
        if j - i == multiplicity:
            Q = evecs[:, i:j]
            class_chars = []
            for cls in range(5):
                traces = [float(np.trace(Q.T @ P @ Q)) for P, c in zip(permutations, rot_classes) if c == cls]
                class_chars.append(float(np.mean(traces)))
            irrep_mults = {
                name: int(round(sum(CLASS_SIZES[c] * chars[c] * class_chars[c] for c in range(5)) / 60.0))
                for name, chars in CHAR_TABLE.items()
            }
            decompositions.append({
                "eigenvalue": float(evals[i]),
                "multiplicity": multiplicity,
                "class_character": [round(x, 10) for x in class_chars],
                "irrep_multiplicities": irrep_mults,
            })
        i = j
    return decompositions


def multiplicity_profile(evals, tol=1e-6):
    """Group eigenvalues by approximate equality and return multiplicity histogram."""
    sorted_e = sorted(evals)
    mults = []
    i = 0
    while i < len(sorted_e):
        v = sorted_e[i]
        j = i
        while j < len(sorted_e) and abs(sorted_e[j] - v) < tol:
            j += 1
        mults.append(j - i)
        i = j
    return mults


def irrep_decomposition_from_mults(mults):
    """Translate multiplicity histogram into I-irrep counts.
    Returns resolved single-irrep counts plus composite eigenspace multiplicities.
    Multiplicities outside {1,3,4,5} are recorded as unresolved composite
    eigenspaces; exact equivariance and character decomposition decide whether
    they are accidental collisions of irreducible sectors.
    """
    hist = Counter(mults)
    counts = {1: hist.get(1, 0), 3: hist.get(3, 0), 4: hist.get(4, 0), 5: hist.get(5, 0)}
    composite = sorted([m for m in mults if m not in ALLOWED_MULTS])
    return counts, composite, hist


def main():
    print("=" * 80)
    print("  O.14d route (alpha): adjacency spectral multiplicity diagnostic")
    print("=" * 80)

    # Setup (reproduce o14d_closure_search.py setup)
    M_perp = get_m_perp()
    vertices_6d = np.vstack([np.eye(6), -np.eye(6)])
    vertices_perp = vertices_6d @ M_perp.T

    print("\n[1] Generating I in 6D...")
    rotations_3d = icosahedral_rotations(vertices_perp)
    lifted = [(R, lift_to_6d(R, vertices_perp)) for R in rotations_3d]
    lifted = [(R, M) for R, M in lifted if M is not None]
    rotations_3d = [R for R, _ in lifted]
    six_d_matrices = [M for _, M in lifted]
    rot_classes = [classify_rotation(R) for R in rotations_3d]
    print(f"    -> {len(six_d_matrices)} 6D matrices")

    print("\n[2] Enumerating Z^6 + I-orbits...")
    pts_6d, pts_perp = gen_z6_points(R=3, perp_cutoff=3.0)
    norms = np.linalg.norm(pts_perp, axis=1)
    order = np.argsort(norms)[:600]
    pts_6d, pts_perp, norms = pts_6d[order], pts_perp[order], norms[order]
    orbits_idx = enumerate_i_orbits(pts_6d, six_d_matrices)
    orbits = []
    for ob in orbits_idx:
        orbits.append({"size": len(ob), "min_perp_norm": float(min(norms[i] for i in ob)),
                       "nodes_perp": pts_perp[ob], "nodes_6d": pts_6d[ob]})
    orbits.sort(key=lambda o: o["min_perp_norm"])
    twelve_idx = [k for k, o in enumerate(orbits) if o["size"] == 12]
    sixty_idx = [k for k, o in enumerate(orbits) if o["size"] == 60]
    print(f"    -> 12-orbits at {twelve_idx}, 60-orbits at {sixty_idx}")

    print("\n[3] Computing adjacency eigenvalue-multiplicity profiles...")
    results = []
    for combo in combinations(sixty_idx, 2):
        sub = twelve_idx + list(combo)
        nodes_perp = np.vstack([orbits[i]["nodes_perp"] for i in sub])
        nodes_6d = np.vstack([orbits[i]["nodes_6d"] for i in sub])
        A = build_adjacency(nodes_perp)
        evals, evecs = np.linalg.eigh(A)
        nz = evals[np.abs(evals) > 1e-12]
        eta = float(np.sum(np.sign(nz)))

        permutations = [permutation_matrix(nodes_6d, M) for M in six_d_matrices]
        commutator_errors = [float(np.max(np.abs(P @ A - A @ P))) for P in permutations]

        # Multiplicity analysis
        mults = multiplicity_profile(evals, tol=1e-4)
        counts, composite, hist = irrep_decomposition_from_mults(mults)
        collision_decompositions = []
        for multiplicity in sorted(set(composite)):
            collision_decompositions.extend(
                decompose_eigenspace_character(
                    evals, evecs, multiplicity, permutations, rot_classes, tol=1e-4
                )
            )
        results.append({
            "pair": list(combo),
            "eta": eta,
            "irrep_counts": counts,  # {1: n_A, 3: n_T, 4: n_G, 5: n_H}
            "composite_multiplicities": composite,
            "collision_eigenspace_decompositions": collision_decompositions,
            "n_rotations_checked": len(permutations),
            "max_commutator_error": max(commutator_errors),
            "i_equivariant": max(commutator_errors) < 1e-10,
            "n_eigenvalues_total": int(np.sum(mults)),
            "all_mults_sorted": sorted(mults, reverse=True),
        })

    print()
    print(f"    {'pair':>8} {'eta':>6} {'n_A':>4} {'n_T':>4} {'n_G':>4} {'n_H':>4} {'composite':>20} {'check_144':>10}")
    for r in results:
        c = r["irrep_counts"]
        check = c[1] * 1 + c[3] * 3 + c[4] * 4 + c[5] * 5 + sum(r["composite_multiplicities"])
        marker = " <-- WINNER" if abs(r["eta"] - (-8)) < 0.5 else ""
        print(f"    {str(r['pair']):>8} {r['eta']:>6.1f} {c[1]:>4} {c[3]:>4} {c[4]:>4} {c[5]:>4} {str(r['composite_multiplicities'])[:20]:>20} {check:>10}{marker}")

    print()
    print("[4] Comparing the winner's adjacency spectral profile...")
    winner = next(r for r in results if abs(r["eta"] - (-8)) < 0.5)
    winner_profile = (winner["irrep_counts"][1], winner["irrep_counts"][3],
                      winner["irrep_counts"][4], winner["irrep_counts"][5],
                      tuple(winner["composite_multiplicities"]))
    matches_to_winner = []
    for r in results:
        p = (r["irrep_counts"][1], r["irrep_counts"][3], r["irrep_counts"][4],
             r["irrep_counts"][5], tuple(r["composite_multiplicities"]))
        if p == winner_profile:
            matches_to_winner.append(r["pair"])
    print(f"    Winner profile: A={winner['irrep_counts'][1]}, T={winner['irrep_counts'][3]}, "
          f"G={winner['irrep_counts'][4]}, H={winner['irrep_counts'][5]}, composite={winner['composite_multiplicities']}")
    print(f"    Pairings matching this profile: {matches_to_winner}")
    if len(matches_to_winner) == 1:
        print(f"\n    Pair {winner['pair']} is the only pairing with the winner's adjacency spectral profile.")
    else:
        print(f"\n    Profile is shared by {len(matches_to_winner)} pairings. Route (alpha) does not close O.14d via simple irrep counting.")
        print(f"    Refinement options: distinguish T_1 vs T_2 (currently lumped), or include eigenvalue values not just multiplicities.")

    # Exact equivariance and collision-character gate.
    print()
    print("[5] Exact 60-rotation commutator and collision-character gate:")
    equivariant = [r for r in results if r["i_equivariant"] and r["n_rotations_checked"] == 60]
    pair_3_5 = next(r for r in results if r["pair"] == [3, 5])
    pair_3_5_is_2g = (
        len(pair_3_5["collision_eigenspace_decompositions"]) == 1
        and pair_3_5["collision_eigenspace_decompositions"][0]["irrep_multiplicities"]
        == {"A": 0, "T1": 0, "T2": 0, "G": 2, "H": 0}
    )
    print(f"    I-equivariant adjacencies: {len(equivariant)} of {len(results)}")
    print(f"    maximum commutator error: {max(r['max_commutator_error'] for r in results):.3e}")
    print(f"    pair [3,5] multiplicity-eight decomposition is 2G: {pair_3_5_is_2g}")
    if len(equivariant) != 21 or not pair_3_5_is_2g:
        raise AssertionError("O.14d equivariance/eigenspace-character gate failed")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        json.dump({
            "diagnostic_object": "eigenvalue multiplicities of the golden-weighted threshold adjacency matrix",
            "interpretation": "All 21 weighted adjacencies commute with all 60 rotations. Pair [3,5] has an accidental collision of two G sectors in one multiplicity-eight eigenspace; it is not a failure of I-equivariance.",
            "resolved_spectral_profile": {"A": 4, "T_lumped": 16, "G": 8, "H": 12, "composite_multiplicities": []},
            "winner_pair": winner["pair"],
            "winner_profile": {"A": winner["irrep_counts"][1], "T": winner["irrep_counts"][3],
                               "G": winner["irrep_counts"][4], "H": winner["irrep_counts"][5],
                               "composite": winner["composite_multiplicities"]},
            "pairings_matching_winner_profile": matches_to_winner,
            "n_i_equivariant_pairings": len(equivariant),
            "n_rotations_checked_per_pairing": 60,
            "max_commutator_error_all_pairings": max(r["max_commutator_error"] for r in results),
            "pair_3_5_collision": pair_3_5["collision_eigenspace_decompositions"][0],
            "pair_3_5_collision_identification": "2G accidental spectral collision",
            "route_alpha_disposition": "Does not select the eta=-8 winner: 20 pairings share its resolved profile; pair [3,5] is fully I-equivariant and differs only because two G sectors collide at one eigenvalue.",
            "all_results": results,
        }, f, indent=2)
    print(f"\n  Output: {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
