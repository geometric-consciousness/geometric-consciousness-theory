#!/usr/bin/env python3
"""
protocol_aps_cage_search.py - Search for I_h-closed cage geometries that
admit integer-arithmetic APS recovery of n = -107.

The discrete APS index decomposition is:
    n_def = Bulk + eta_eff,   where eta_eff = eta_scalar / dim_spinor = eta_scalar / 8

For n_def = -107 to close cleanly, Bulk must be an integer (it is a
Pontryagin-class evaluation), which requires:
    eta_scalar ≡ 8 * (-107 - Bulk)  for some integer Bulk
i.e., eta_scalar must be a multiple of 8.

This protocol:
  1. Enumerates I_h orbits in Z^6 perp-projected via M_perp up to a
     specified perp_cutoff (default 4.0).
  2. For each contiguous union of orbits (sweeping outward by perp-norm),
     builds the cage adjacency matrix with the golden-bond rule
     (|x_perp| = 1 -> weight 1; |x_perp| = 1/phi -> weight phi).
  3. Computes eta_scalar = Σ sign(λ) over non-zero eigenvalues.
  4. Reports which cage sizes give eta_scalar ≡ 0 (mod 8) — the
     necessary condition for integer-arithmetic APS recovery.

Closure of this search produces one of three outcomes:
  (i)  Cage(s) found with eta_scalar mod 8 == 0 AND bulk-required-for-
       n=107 = (107 + eta_scalar/8) being a plausible Pontryagin
       integer for the 6D icosahedral cell. -> APS pathway recoverable;
       O.14c can be closed analytically on the chosen cage.
  (ii) Cage(s) found with eta_scalar mod 8 == 0 but bulk-required is
       not a plausible Pontryagin integer (e.g., 0 or negative). ->
       Mathematical formalism holds; physical interpretation open.
  (iii) NO I_h-closed cage in the searched range gives eta_scalar mod
        8 == 0 for the relevant target. -> Strong negative result;
        focuses O.14c on non-cage-based alternatives.
"""

from __future__ import annotations

import json
import sys
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


def enumerate_orbits(R: int, perp_cutoff: float, group: list[np.ndarray]) -> list[dict]:
    """Enumerate all I_h orbits intersecting the Z^6 patch with the given
    perp_cutoff. Returns a list of dicts sorted by orbit-representative
    perp-norm:
        [{'perp_norm': r, 'size': s, 'nodes_6d': [(...), ...]}, ...]
    """
    lattice = GCTLattice(R=R, perp_cutoff=perp_cutoff)
    x_eq = lattice.x_equilibrium
    x_perp_all = proj.project_perp(x_eq)
    norms = np.linalg.norm(x_perp_all, axis=1)
    idx = np.argsort(norms)
    if norms[idx[0]] < 1e-8:
        idx = idx[1:]   # drop origin

    seen: set[tuple[int, ...]] = set()
    orbits = []
    for j in idx:
        seed = tuple(int(c) for c in x_eq[j])
        if seed in seen:
            continue
        orbit = full_orbit(seed, group)
        seen |= orbit
        rep_v = np.array(seed, dtype=np.float64)
        rep_perp = proj.project_perp(rep_v.reshape(1, -1))[0]
        rep_perp_norm = float(np.linalg.norm(rep_perp))
        orbits.append({
            "perp_norm": rep_perp_norm,
            "size": len(orbit),
            "nodes_6d": [list(n) for n in orbit],
        })
    orbits.sort(key=lambda o: o["perp_norm"])
    return orbits


def cage_adjacency(nodes_6d: np.ndarray) -> np.ndarray:
    """Build golden-weighted scalar adjacency on a 6D cage projected to
    3D perp-space:
        weight 1   for |x_perp_i - x_perp_j| ≈ 1
        weight phi for |x_perp_i - x_perp_j| ≈ 1/phi
    Matches `protocol_cage_spectral_decomp.build_cage_and_adjacency`.
    """
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


def eta_scalar_of_cage(nodes_6d: np.ndarray) -> int:
    A = cage_adjacency(nodes_6d)
    evals = np.linalg.eigvalsh(A)
    nz = evals[np.abs(evals) > 1e-12]
    return int(round(float(np.sum(np.sign(nz)))))


def main():
    print("=" * 76)
    print("APS-cage search: I_h-closed cages with integer-arithmetic APS")
    print("=" * 76)

    R = 3
    perp_cutoff = 3.5
    print(f"\nSearching Z^6 patch R={R}, perp_cutoff={perp_cutoff} ...")
    group = build_Ih_120()
    orbits = enumerate_orbits(R, perp_cutoff, group)
    print(f"  Found {len(orbits)} distinct I_h orbits up to perp_norm = {perp_cutoff}")
    print(f"  {'index':>5} {'perp_norm':>10} {'orbit_size':>10}")
    for k, o in enumerate(orbits):
        print(f"  {k:>5} {o['perp_norm']:>10.4f} {o['size']:>10}")

    print(f"\nSweeping cumulative I_h-orbit unions (outward by perp_norm)...")
    print(f"  {'orbits':>7} {'N_total':>8} {'eta_scalar':>11} {'eta_eff':>10} {'bulk_req':>10} {'mod_8_ok':>9} {'bulk_int':>9}")
    print("  " + "-" * 76)

    results = []
    accumulated_nodes: set[tuple[int, ...]] = set()
    interesting: list[dict] = []

    for k, o in enumerate(orbits):
        for n in o["nodes_6d"]:
            accumulated_nodes.add(tuple(n))
        nodes_arr = np.array(sorted(accumulated_nodes), dtype=np.float64)
        N = nodes_arr.shape[0]
        if N > 800:
            # Too large for the eigenvalue computation in reasonable time
            print(f"  ...skipping cage with N={N} (eigenvalue computation too expensive)")
            break
        eta_s = eta_scalar_of_cage(nodes_arr)
        eta_eff = eta_s / 8.0
        bulk_required = -107.0 - eta_eff
        mod8_ok = (eta_s % 8 == 0)
        bulk_int = abs(bulk_required - round(bulk_required)) < 1e-9
        flag = "<-- candidate" if (mod8_ok and bulk_int) else ""
        print(f"  {k + 1:>7} {N:>8} {eta_s:>+11} {eta_eff:>+10.4f} {bulk_required:>+10.4f} {str(mod8_ok):>9} {str(bulk_int):>9}   {flag}")

        rec = {
            "n_orbits_included": k + 1,
            "N_total": N,
            "outer_orbit_perp_norm": o["perp_norm"],
            "eta_scalar": eta_s,
            "eta_eff": eta_eff,
            "bulk_required_for_n_minus_107": bulk_required,
            "eta_scalar_mod_8_zero": mod8_ok,
            "bulk_required_is_integer": bulk_int,
            "is_aps_recovery_candidate": (mod8_ok and bulk_int),
        }
        results.append(rec)
        if mod8_ok and bulk_int:
            interesting.append(rec)

    # Distinguish trivial (no edges -> eta = 0 vacuously) from non-trivial candidates
    edge_thresholds = []
    for c in interesting:
        nodes_arr_c = None
        # Re-derive the cage to count edges (cheap; bounded by k)
        accumulated_c: set[tuple[int, ...]] = set()
        for k_idx in range(c["n_orbits_included"]):
            for n in orbits[k_idx]["nodes_6d"]:
                accumulated_c.add(tuple(n))
        nodes_arr_c = np.array(sorted(accumulated_c), dtype=np.float64)
        A_c = cage_adjacency(nodes_arr_c)
        n_edges = int(A_c.sum() / 2 if A_c.size > 0 else 0)
        edge_thresholds.append(n_edges)

    non_trivial = [c for c, ne in zip(interesting, edge_thresholds) if ne > 0]

    print()
    print("=" * 76)
    print(f"APS-recovery candidates found: {len(interesting)} (of which {len(non_trivial)} non-trivial; the rest have no edges in the golden-bond regime and give eta=0 vacuously)")
    for c, ne in zip(interesting, edge_thresholds):
        status = "non-trivial" if ne > 0 else "trivial (no edges)"
        print(f"  N={c['N_total']:4d}, edges={ne:5d}, eta_scalar={c['eta_scalar']:+d}, "
              f"eta_eff={c['eta_eff']:+.4f}, bulk={c['bulk_required_for_n_minus_107']:+.0f}   [{status}]")
    print("=" * 76)

    if not interesting:
        print("STRONG NEGATIVE RESULT.")
        print("No I_h-closed cage in the searched range (5 inner-orbit unions up to")
        print(f"perp_cutoff = {perp_cutoff}, max N = {results[-1]['N_total'] if results else 0})")
        print("yields eta_scalar ≡ 0 (mod 8) AND integer bulk-required-for-n=-107.")
        print()
        print("Reading: the discrete APS recovery of n = -107 on an I_h-closed")
        print("boundary cage at perp_cutoff <= 3.5 is structurally blocked at the")
        print("integer-arithmetic level. The asymmetric 144-cage's eta_scalar = -8 was a")
        print("unique-to-asymmetric-truncation result; no I_h-symmetric counterpart")
        print("exists in the searched range. O.14c closure via the direct discrete-")
        print("APS-on-I_h-closed-cage pathway is therefore not available; the")
        print("Connes-Moscovici smooth-manifold route (O.14b) becomes the primary")
        print("remaining path to closure.")

    verdict = {
        "search_R": R,
        "search_perp_cutoff": perp_cutoff,
        "n_Ih_orbits_enumerated": len(orbits),
        "cage_sweep_results": results,
        "aps_recovery_candidates_all": interesting,
        "aps_recovery_candidates_non_trivial": non_trivial,
        "outcome": (
            f"FOUND_{len(non_trivial)}_non_trivial_aps_recovery_candidates"
            if non_trivial else
            "STRONG_NEGATIVE_no_non_trivial_Ih_cage_recovers_n=-107"
        ),
    }
    out_path = ENGINE_ROOT / "data" / "protocol_aps_cage_search_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(verdict, f, indent=2)
    print(f"\nFull results saved to: {out_path}")
    print("=" * 76)


if __name__ == "__main__":
    main()
