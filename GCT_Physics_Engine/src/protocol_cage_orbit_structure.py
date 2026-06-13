#!/usr/bin/env python3
"""
protocol_cage_orbit_structure.py - Audit the I_h orbit structure of the
engine 144-node cage.

Diagnostic: the cage constructed by `protocol_aps_index_proof.py` via the
GCTLattice(R=2, perp_cutoff=2.0) + top-144-by-perp-norm-excluding-origin
pipeline is supposed to realise the App M Sec M.7 'bilayer of two
dodecahedral shells of 72 nodes each'. This protocol partitions the actual
cage nodes into I_h orbits and reports:

  - The 3D-perp-space radius of each I_h orbit intersecting the cage.
  - The full size of each such I_h orbit.
  - Whether the cage is closed under I_h (a strict requirement for the
    Sec M.7 orthogonality-theorem argument that gives the 1/(2N) finite-N
    correction).
  - Whether any subset of orbits sums to 72 (the App M Sec M.7 shell size).

The protocol does not attempt to repair the cage; it reports the structural
state for the cage-construction audit.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ENGINE_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = ENGINE_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

from gct_lattice import GCTLattice
import gct_projections as proj
from protocol_cage_repair import (
    vertex_pairs_from_projection,
    icosahedral_rotations_lattice_frame,
    lift_to_6d_signed_perm,
)


def build_Ih_120() -> list[np.ndarray]:
    """Construct the 120 signed-permutation matrices of I_h acting on Z^6."""
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


def full_Ih_orbit(seed: tuple[int, ...], group: list[np.ndarray]) -> set[tuple[int, ...]]:
    """Return the full I_h orbit of a Z^6 lattice point, regardless of
    which subset of the orbit is present in any given cage."""
    seed_v = np.array(seed, dtype=np.float64)
    orbit = {seed}
    for M in group:
        mapped = M @ seed_v
        mapped_t = tuple(int(round(c)) for c in mapped)
        orbit.add(mapped_t)
    return orbit


def main():
    print("=" * 76)
    print("Cage orbit-structure audit (engine 144-node cage vs App M Sec M.7)")
    print("=" * 76)

    lattice = GCTLattice(R=2, perp_cutoff=2.0)
    x_eq = lattice.x_equilibrium
    x_perp_all = proj.project_perp(x_eq)
    norms = np.linalg.norm(x_perp_all, axis=1)
    idx = np.argsort(norms)
    if norms[idx[0]] < 1e-8:
        idx = idx[1:145]
    else:
        idx = idx[:144]

    cage_6d = x_eq[idx]
    cage_perp = x_perp_all[idx]
    cage_set = set(tuple(int(c) for c in n) for n in cage_6d)
    perp_norms = np.linalg.norm(cage_perp, axis=1)

    print(f"\nCage size: {len(cage_set)}")

    # Perp-shell distribution (by perp-norm only)
    shell_counter = Counter(np.round(perp_norms, 4).tolist())
    perp_shells_sorted = sorted(shell_counter.keys())
    print(f"\nPerp-shell vertex counts (in the cage, by perp-norm):")
    for r in perp_shells_sorted:
        print(f"  r = {r:.4f}: {shell_counter[r]} vertices")

    print(f"\nBuilding I_h group (120 signed permutations on Z^6)...")
    group = build_Ih_120()

    # Identify I_h orbits whose representatives are in the cage
    remaining_cage = set(cage_set)
    orbits_intersecting_cage = []
    while remaining_cage:
        seed = next(iter(remaining_cage))
        full_orbit = full_Ih_orbit(seed, group)
        in_cage = full_orbit & cage_set
        # Representative perp-norm
        rep_perp = proj.project_perp(np.array(seed, dtype=np.float64).reshape(1, -1))[0]
        rep_perp_norm = float(np.linalg.norm(rep_perp))
        orbits_intersecting_cage.append({
            "rep": seed,
            "perp_norm": rep_perp_norm,
            "full_orbit_size": len(full_orbit),
            "in_cage_size": len(in_cage),
            "is_closed_in_cage": len(in_cage) == len(full_orbit),
        })
        remaining_cage -= full_orbit

    orbits_intersecting_cage.sort(key=lambda o: o["perp_norm"])

    print(f"\nI_h orbits intersecting the cage:")
    print(f"  {'perp_norm':>10}  {'full_orbit':>11}  {'in_cage':>8}  {'closed?':>8}")
    total_full = 0
    total_in_cage = 0
    n_closed = 0
    for o in orbits_intersecting_cage:
        flag = "yes" if o["is_closed_in_cage"] else "no"
        print(f"  {o['perp_norm']:>10.4f}  {o['full_orbit_size']:>11}  {o['in_cage_size']:>8}  {flag:>8}")
        total_full += o["full_orbit_size"]
        total_in_cage += o["in_cage_size"]
        if o["is_closed_in_cage"]:
            n_closed += 1

    print(f"\n  Total full-orbit vertices: {total_full}")
    print(f"  Total in-cage vertices:    {total_in_cage}")
    print(f"  Closed orbits / total:     {n_closed} / {len(orbits_intersecting_cage)}")

    cage_is_Ih_symmetric = (total_full == total_in_cage)
    if cage_is_Ih_symmetric:
        print(f"\n  Cage IS closed under I_h.")
    else:
        missing = total_full - total_in_cage
        print(f"\n  Cage is NOT closed under I_h: {missing} vertices in I_h orbits")
        print(f"  are outside the cage. Either:")
        print(f"    (i)  perp_cutoff=2.0 + top-144 selection truncates an outermost")
        print(f"         I_h orbit asymmetrically, or")
        print(f"    (ii) the top-144 selection is not the canonical cage construction")
        print(f"         that App M Sec M.7 has in mind.")

    # Search for (72, 72) bilayer composition
    print(f"\nSubsets of full-orbit sizes summing to 72:")
    sizes = [o["full_orbit_size"] for o in orbits_intersecting_cage]
    found_72 = []
    if len(sizes) <= 18:
        for mask in range(1, 1 << len(sizes)):
            s = sum(sizes[i] for i in range(len(sizes)) if (mask >> i) & 1)
            if s == 72:
                indices = [i for i in range(len(sizes)) if (mask >> i) & 1]
                composition = [(orbits_intersecting_cage[i]["perp_norm"],
                                orbits_intersecting_cage[i]["full_orbit_size"])
                               for i in indices]
                found_72.append(composition)

    if not found_72:
        print(f"  NO subset of the cage's intersecting full-orbits sums to 72.")
        print(f"  The App M Sec M.7 'shell of 72' is therefore NOT realisable as")
        print(f"  any sub-union of the cage's I_h orbits at this perp_cutoff.")
    else:
        print(f"  Found {len(found_72)} subsets summing to 72:")
        for comp in found_72[:5]:
            print(f"    {comp}")

    # Verdict
    print(f"\n" + "=" * 76)
    print("STATUS")
    print("=" * 76)
    if cage_is_Ih_symmetric and any(s == 72 for s in sizes):
        print("OK: cage is I_h-symmetric and a 72-vertex shell exists.")
    elif cage_is_Ih_symmetric:
        print("PARTIAL: cage is I_h-symmetric, but no (72, 72) bilayer composition exists.")
        print("App M Sec M.7's '72 per shell' is not realisable from the present orbit set.")
    else:
        print("STRUCTURAL ISSUE:")
        print(f"  (1) Cage is NOT closed under I_h ({total_full - total_in_cage} missing vertices).")
        if not found_72:
            print(f"  (2) Even with full I_h closure, no subset sums to 72.")
        print(f"  -> App M Sec M.7 'bilayer of two 72-vertex shells' is not realisable")
        print(f"     as a closed I_h-orbit composition of the engine cage geometry at")
        print(f"     this perp_cutoff. The eta_analytic = 1 - 1/(2N) prediction matching")
        print(f"     alpha^-1 to 41.6 ppm DESPITE this is noted as a separate open question;")
        print(f"     either the App M Sec M.7 derivation is robust under generalisations")
        print(f"     of the bilayer assumption, or the engine cage construction differs")
        print(f"     from the manuscript's.")
    print("=" * 76)

    verdict = {
        "cage_size": len(cage_set),
        "perp_shell_counts": {f"{r:.4f}": int(shell_counter[r]) for r in perp_shells_sorted},
        "Ih_orbit_breakdown": [
            {
                "perp_norm": o["perp_norm"],
                "full_orbit_size": o["full_orbit_size"],
                "in_cage_size": o["in_cage_size"],
                "is_closed_in_cage": o["is_closed_in_cage"],
            }
            for o in orbits_intersecting_cage
        ],
        "cage_is_Ih_symmetric": cage_is_Ih_symmetric,
        "total_full_orbit_vertices": total_full,
        "total_in_cage_vertices": total_in_cage,
        "missing_vertices_for_Ih_closure": total_full - total_in_cage,
        "subsets_summing_to_72_count": len(found_72),
        "subsets_summing_to_72": found_72,
        "App_M_M7_bilayer_realisable": cage_is_Ih_symmetric and len(found_72) >= 2,
        "tier": "Tier 3 structural audit of cage geometry.",
    }
    out_path = ENGINE_ROOT / "data" / "protocol_cage_orbit_structure_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(verdict, f, indent=2)
    print(f"\nFull results saved to: {out_path}")
    print("=" * 76)


if __name__ == "__main__":
    main()
