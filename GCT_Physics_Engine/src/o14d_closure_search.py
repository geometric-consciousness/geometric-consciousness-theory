#!/usr/bin/env python3
"""
o14d_closure_search.py - Standalone reproduction of the O.14d cage uniqueness search.

This script reproduces the protocol_orbit_union_search.py logic with
explicit orbit-index logging to identify the winning [12, 60, 12, 60]
subset (specific 60-orbit pair) that yields eta_scalar = -8.

Then tests three candidate selection rules against the winner:
    (i)   minimum-radial-extent
    (ii)  inner-outer shell-radius matching
    (iii) chiral-parity-preserving pair

Standalone: does not import from gct_lattice / gct_projections. It
reproduces just enough to identify the winner.
"""

import math
import json
import sys
from itertools import combinations, product
from pathlib import Path
import numpy as np

# SSOT import (canonical PHI from gct_constants.yaml via gct_utils)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from gct_utils import C  # noqa: E402
PHI = float(C.PHI)
PHI_CONJ = -1.0 / PHI

ENGINE_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = ENGINE_ROOT / "data" / "o14d_closure_search_results.json"


def get_m_perp():
    """Canonical perp projection matrix M_perp (3x6) — Galois conjugate slopes."""
    ip = PHI_CONJ
    raw = np.array([
        [1.0, ip,  0.0, -1.0, ip,  0.0],
        [ip,  0.0, 1.0, ip,  0.0, -1.0],
        [0.0, 1.0, ip,  0.0, -1.0, ip],
    ], dtype=np.float64)
    N_perp = 1.0 / np.sqrt(2.0 * (2.0 + ip))
    return N_perp * raw


def get_m_para():
    """Canonical parallel projection matrix M_para (3x6)."""
    p = PHI
    raw = np.array([
        [1.0, p,   0.0, -1.0, p,   0.0],
        [p,   0.0, 1.0, p,   0.0, -1.0],
        [0.0, 1.0, p,   0.0, -1.0, p],
    ], dtype=np.float64)
    N_para = 1.0 / np.sqrt(2.0 * (2.0 + p))
    return N_para * raw


def gen_z6_points(R: int = 3, perp_cutoff: float = 3.0):
    """Generate Z^6 lattice points with perp-projection norm in [0, perp_cutoff]."""
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


def icosahedral_rotations(vertices_perp: np.ndarray) -> list:
    """Generate 60 SO(3) rotations of the icosahedral group I in the lattice frame."""
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
    if triangle_partner is None:
        raise RuntimeError("No triangle on icosahedron")
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


def lift_to_6d(R: np.ndarray, vertices_perp: np.ndarray):
    """Lift 3D rotation to 6x6 signed permutation acting on Z^6."""
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


def enumerate_i_orbits(pts_6d, six_d_matrices):
    """Group lattice points into I-orbits."""
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


def compute_eta_scalar(nodes_perp: np.ndarray) -> tuple:
    """Golden-weighted adjacency on the perp-projected nodes; return eta_scalar."""
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
    return eta, evals


def main():
    print("=" * 80)
    print("  O.14d closure search: identify the winning [12, 60, 12, 60] subset")
    print("=" * 80)

    # Build vertex pairs from Z^6 basis vectors
    M_perp = get_m_perp()
    vertices_6d = np.vstack([np.eye(6), -np.eye(6)])
    vertices_perp = vertices_6d @ M_perp.T

    print("\n[1] Generating icosahedral group I in 6D...")
    rotations_3d = icosahedral_rotations(vertices_perp)
    six_d_matrices = [lift_to_6d(R, vertices_perp) for R in rotations_3d]
    six_d_matrices = [M for M in six_d_matrices if M is not None]
    print(f"    -> {len(six_d_matrices)} 6D signed-permutation matrices")

    print("\n[2] Enumerating Z^6 lattice points within perp_cutoff=3.0...")
    pts_6d, pts_perp = gen_z6_points(R=3, perp_cutoff=3.0)
    norms = np.linalg.norm(pts_perp, axis=1)
    order = np.argsort(norms)[:600]
    pts_6d = pts_6d[order]
    pts_perp = pts_perp[order]
    norms = norms[order]
    print(f"    -> {len(pts_6d)} candidate points (sorted by perp-norm)")

    print("\n[3] Enumerating I-orbits...")
    orbits_idx = enumerate_i_orbits(pts_6d, six_d_matrices)
    orbits = []
    for ob in orbits_idx:
        min_n = min(norms[i] for i in ob)
        max_n = max(norms[i] for i in ob)
        mean_n = float(np.mean([norms[i] for i in ob]))
        orbits.append({
            "size": len(ob),
            "min_perp_norm": float(min_n),
            "max_perp_norm": float(max_n),
            "mean_perp_norm": mean_n,
            "indices_in_pts": ob,
            "nodes_perp": pts_perp[ob],
        })
    orbits.sort(key=lambda o: o["min_perp_norm"])
    print(f"    -> {len(orbits)} I-orbits")
    print(f"\n    Orbit table (radial order):")
    print(f"    {'orbit_idx':>10} {'size':>5} {'min_perp':>9} {'max_perp':>9} {'mean_perp':>10}")
    for k, o in enumerate(orbits):
        print(f"    {k:>10} {o['size']:>5} {o['min_perp_norm']:>9.4f} {o['max_perp_norm']:>9.4f} {o['mean_perp_norm']:>10.4f}")

    # Find indices of the two 12-orbits and the five 60-orbits
    twelve_idx = [k for k, o in enumerate(orbits) if o["size"] == 12]
    sixty_idx = [k for k, o in enumerate(orbits) if o["size"] == 60]
    print(f"\n    12-orbits at indices: {twelve_idx}")
    print(f"    60-orbits at indices: {sixty_idx}")

    if len(twelve_idx) < 2 or len(sixty_idx) < 2:
        print("    ERROR: insufficient orbits for [12, 60, 12, 60] enumeration")
        return 1

    print("\n[4] Enumerating [12, 60, 12, 60] subsets and computing eta_scalar for each...")
    print(f"    Total to test: C({len(sixty_idx)},2) = {len(sixty_idx) * (len(sixty_idx) - 1) // 2} pairings")
    print()
    print(f"    {'rank':>4} {'pair_indices':>14} {'pair_min_perps':>20} {'pair_mean_perps':>22} {'eta':>6}")
    results = []
    for combo in combinations(sixty_idx, 2):
        sub = twelve_idx + list(combo)
        nodes = np.vstack([orbits[i]["nodes_perp"] for i in sub])
        eta, _ = compute_eta_scalar(nodes)
        results.append({
            "sixty_orbit_pair": list(combo),
            "twelve_indices": twelve_idx,
            "pair_min_perps": [orbits[c]["min_perp_norm"] for c in combo],
            "pair_mean_perps": [orbits[c]["mean_perp_norm"] for c in combo],
            "eta_scalar": eta,
        })
    # Sort by sum of pair_min_perps to display in radial order
    results.sort(key=lambda r: sum(r["pair_min_perps"]))
    for k, r in enumerate(results):
        marker = " <-- ETA=-8 MATCH" if abs(r["eta_scalar"] - (-8)) < 0.5 else ""
        print(f"    {k:>4} {str(r['sixty_orbit_pair']):>14} "
              f"{str([round(x, 3) for x in r['pair_min_perps']]):>20} "
              f"{str([round(x, 3) for x in r['pair_mean_perps']]):>22} "
              f"{r['eta_scalar']:>6.1f}{marker}")

    eta_matches = [r for r in results if abs(r["eta_scalar"] - (-8)) < 0.5]
    print()
    if len(eta_matches) == 0:
        print("    NO eta_scalar = -8 match among the 10 [12, 60, 12, 60] pairings!")
        print("    Either the search radius is too small or no match exists at this scale.")
    elif len(eta_matches) == 1:
        winner = eta_matches[0]
        print(f"    UNIQUE WINNER: 60-orbit pair = {winner['sixty_orbit_pair']}")
        print(f"      pair_min_perps  = {winner['pair_min_perps']}")
        print(f"      pair_mean_perps = {winner['pair_mean_perps']}")

        print("\n[5] Testing candidate selection rules against the winner:")
        # Rule (i): minimum-radial-extent (lowest sum of min_perp_norms)
        sums = [(r["sixty_orbit_pair"], sum(r["pair_min_perps"])) for r in results]
        sums.sort(key=lambda x: x[1])
        rule_i_pick = sums[0][0]
        print(f"    (i)  Minimum-radial-extent  -> 60-orbit pair {rule_i_pick} "
              f"({'WINNER MATCH' if rule_i_pick == winner['sixty_orbit_pair'] else 'no match'})")

        # Rule (ii): inner-outer shell-radius matching
        # Each 60-orbit should match the radial shell of one of the 12-orbits
        # 12-orbit radii:
        t12_radii = [orbits[i]["min_perp_norm"] for i in twelve_idx]
        # Score each pair: sum of |60-orbit min_perp - closest 12-orbit radius|
        def shell_match_score(pair):
            score = 0
            for c in pair:
                p = orbits[c]["min_perp_norm"]
                closest = min(abs(p - r) for r in t12_radii)
                score += closest
            return score
        score_pairs = [(r["sixty_orbit_pair"], shell_match_score(r["sixty_orbit_pair"])) for r in results]
        score_pairs.sort(key=lambda x: x[1])
        rule_ii_pick = score_pairs[0][0]
        print(f"    (ii) Inner-outer shell-radius match -> 60-orbit pair {rule_ii_pick} "
              f"({'WINNER MATCH' if rule_ii_pick == winner['sixty_orbit_pair'] else 'no match'})")

        # Rule (iii): chiral-parity-preserving pair
        # In the icosahedral setup, certain 60-orbits at conjugate perp-radii under
        # Galois automorphism phi <-> -1/phi form pairs. Compute Galois-conjugate radius
        # for each 60-orbit and look for pairs at conjugate radii.
        def galois_conjugate_pair_score(pair):
            # The Galois conjugate of a perp-norm swaps phi <-> -1/phi. Test whether
            # mean_perp[a] is approximately phi * mean_perp[b] or (1/phi) * mean_perp[b].
            a, b = pair
            ma, mb = orbits[a]["mean_perp_norm"], orbits[b]["mean_perp_norm"]
            if mb == 0:
                return float('inf')
            ratio = ma / mb
            return min(abs(ratio - PHI), abs(ratio - 1.0 / PHI), abs(ratio - 1.0))
        chiral_pairs = [(r["sixty_orbit_pair"], galois_conjugate_pair_score(r["sixty_orbit_pair"])) for r in results]
        chiral_pairs.sort(key=lambda x: x[1])
        rule_iii_pick = chiral_pairs[0][0]
        print(f"    (iii) Chiral-parity (Galois conjugate radii) -> 60-orbit pair {rule_iii_pick} "
              f"({'WINNER MATCH' if rule_iii_pick == winner['sixty_orbit_pair'] else 'no match'})")

        verdict = []
        if rule_i_pick == winner['sixty_orbit_pair']:
            verdict.append("RULE (i) MINIMUM-RADIAL-EXTENT SELECTS THE WINNER UNIQUELY")
        if rule_ii_pick == winner['sixty_orbit_pair']:
            verdict.append("RULE (ii) SHELL-RADIUS MATCHING SELECTS THE WINNER UNIQUELY")
        if rule_iii_pick == winner['sixty_orbit_pair']:
            verdict.append("RULE (iii) CHIRAL-PARITY SELECTS THE WINNER UNIQUELY")
        if not verdict:
            verdict.append("None of the three candidate rules picks the winner. Closure not yet earned via these rules.")

        print()
        print("    Verdict:")
        for v in verdict:
            print(f"      * {v}")
    else:
        print(f"    {len(eta_matches)} pairings yield eta=-8 (expected 1)")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        json.dump({
            "n_orbits": len(orbits),
            "orbit_sizes": [o["size"] for o in orbits],
            "orbit_min_perps": [o["min_perp_norm"] for o in orbits],
            "twelve_orbit_indices": twelve_idx,
            "sixty_orbit_indices": sixty_idx,
            "results": [{k: v for k, v in r.items() if k != "nodes_perp"} for r in results],
            "eta_minus_8_matches": [{"sixty_orbit_pair": r["sixty_orbit_pair"], "pair_min_perps": r["pair_min_perps"]} for r in eta_matches],
        }, f, indent=2)
    print(f"\n  Output: {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
