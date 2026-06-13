#!/usr/bin/env python3
"""
cage_builder.py - Canonical I_h-symmetric cage construction.

Provides the canonical orbit-union cage construction for the icosahedral
I_h acceptance window: a cage is I_h-closed iff for every cage node x,
every I_h image of x is also in the cage. This is the construction
required by the I_h orthogonality theorem invoked in App M Sec M.7 for
the 1/(2N) finite-N correction.

A naive "top-N-by-perp-norm" cage of size 144 truncates the outermost
icosahedral I_h orbit asymmetrically and breaks the I_h orthogonality
theorem; this module exposes the orbit-union alternative.

Conventions
-----------
- 6D lattice points x in Z^6 are projected to E_perp via M_perp; their
  perp-radius |x_perp| sorts naturally into discrete I_h orbits.
- A cage is "I_h-closed" iff for every cage node x, every I_h image of x
  is also in the cage.
- Two canonical I_h-closed cages at perp_cutoff = 2.0:
    SIZE_92 = (12, 30, 20, 30)                       (4 inner orbits)
    SIZE_152 = (12, 30, 20, 30, 60)                  (all 5 orbits up to 0.489)

The 152-cage is the natural orbit-union counterpart to a top-144-by-
perp-norm truncation: it includes the 8 outermost-orbit vertices that an
asymmetric top-144 selection would omit.

Usage:
    from cage_builder import build_canonical_cage
    nodes_6d, nodes_perp = build_canonical_cage(size=152)
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

_SRC = Path(__file__).resolve().parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from gct_lattice import GCTLattice
import gct_projections as proj
from protocol_cage_repair import (
    vertex_pairs_from_projection,
    icosahedral_rotations_lattice_frame,
    lift_to_6d_signed_perm,
)


_IH_GROUP_CACHE: list[np.ndarray] | None = None


def _build_Ih_group() -> list[np.ndarray]:
    """Construct (or return cached) the 120 signed-permutation matrices of I_h."""
    global _IH_GROUP_CACHE
    if _IH_GROUP_CACHE is not None:
        return _IH_GROUP_CACHE
    vertices_perp, _ = vertex_pairs_from_projection()
    rots3 = icosahedral_rotations_lattice_frame(vertices_perp)
    group60 = []
    for R in rots3:
        M = lift_to_6d_signed_perm(R, vertices_perp)
        if M is None:
            continue
        group60.append(M)
    minus_I6 = -np.eye(6)
    _IH_GROUP_CACHE = group60 + [minus_I6 @ M for M in group60]
    return _IH_GROUP_CACHE


def _full_orbit(seed: tuple[int, ...], group: list[np.ndarray]) -> set[tuple[int, ...]]:
    seed_v = np.array(seed, dtype=np.float64)
    orbit = {seed}
    for M in group:
        mapped = M @ seed_v
        orbit.add(tuple(int(round(c)) for c in mapped))
    return orbit


def build_canonical_cage(size: int = 152, R: int = 2, perp_cutoff: float = 2.0
                         ) -> tuple[np.ndarray, np.ndarray]:
    """Build an I_h-closed cage of the given size.

    Parameters
    ----------
    size : int
        Target cage size. Must equal the sum of I_h orbits at the chosen
        perp_cutoff. Supported values at perp_cutoff=2.0:
            size=92  -> 4 inner orbits: (12, 30, 20, 30)
            size=152 -> 5 orbits:      (12, 30, 20, 30, 60)
    R : int
        Z^6 bounding-box parameter for GCTLattice. Default 2.
    perp_cutoff : float
        Perp-space cutoff for GCTLattice. Default 2.0.

    Returns
    -------
    nodes_6d : (N, 6) integer array of Z^6 lattice points
    nodes_perp : (N, 3) array of E_perp projections (for shell structure)

    Raises
    ------
    ValueError if size is not realisable as an orbit-union at the given cutoff.
    """
    lattice = GCTLattice(R=R, perp_cutoff=perp_cutoff)
    x_eq = lattice.x_equilibrium
    x_perp_all = proj.project_perp(x_eq)
    norms = np.linalg.norm(x_perp_all, axis=1)
    idx_sorted = np.argsort(norms)
    if norms[idx_sorted[0]] < 1e-8:
        idx_sorted = idx_sorted[1:]   # drop origin

    group = _build_Ih_group()

    # Walk outward in perp-norm; accumulate full I_h orbits one at a time
    # until the cage reaches `size`.
    accumulated_nodes: set[tuple[int, ...]] = set()
    visited_seeds: set[tuple[int, ...]] = set()
    for j in idx_sorted:
        seed = tuple(int(c) for c in x_eq[j])
        if seed in visited_seeds or seed in accumulated_nodes:
            continue
        orbit = _full_orbit(seed, group)
        visited_seeds |= orbit
        if len(accumulated_nodes) + len(orbit) > size:
            # Adding this orbit would overshoot; stop here.
            break
        accumulated_nodes |= orbit
        if len(accumulated_nodes) == size:
            break

    if len(accumulated_nodes) != size:
        # Cage doesn't have an orbit-union of exactly `size` at this cutoff.
        # Report what IS available.
        sizes_available = []
        cumulative = 0
        visited2: set[tuple[int, ...]] = set()
        for j in idx_sorted:
            seed = tuple(int(c) for c in x_eq[j])
            if seed in visited2:
                continue
            orbit = _full_orbit(seed, group)
            visited2 |= orbit
            cumulative += len(orbit)
            sizes_available.append(cumulative)
        raise ValueError(
            f"Cage size {size} not realisable as an I_h-orbit union at "
            f"R={R}, perp_cutoff={perp_cutoff}. Available cumulative sizes: "
            f"{sizes_available}"
        )

    nodes_6d = np.array(sorted(accumulated_nodes), dtype=np.float64)
    nodes_perp = nodes_6d @ proj.get_m_perp().T
    return nodes_6d, nodes_perp


def cage_summary(nodes_6d: np.ndarray, nodes_perp: np.ndarray) -> dict:
    """Return a summary dict for the cage (shell counts, sizes)."""
    from collections import Counter

    perp_norms = np.linalg.norm(nodes_perp, axis=1)
    shell_counts = Counter(np.round(perp_norms, 4).tolist())
    return {
        "N": nodes_6d.shape[0],
        "perp_norm_min": float(perp_norms.min()),
        "perp_norm_max": float(perp_norms.max()),
        "shell_counts": {f"{r:.4f}": int(shell_counts[r])
                         for r in sorted(shell_counts.keys())},
    }


if __name__ == "__main__":
    print("Canonical I_h-closed cage builder")
    print("=" * 60)
    for size in (92, 152):
        try:
            nodes_6d, nodes_perp = build_canonical_cage(size=size)
            summary = cage_summary(nodes_6d, nodes_perp)
            print(f"\nsize={size}: built successfully")
            print(f"  shells: {summary['shell_counts']}")
            print(f"  perp_norm range: [{summary['perp_norm_min']:.4f}, "
                  f"{summary['perp_norm_max']:.4f}]")
        except ValueError as e:
            print(f"\nsize={size}: FAILED -- {e}")
    try:
        build_canonical_cage(size=144)
    except ValueError as e:
        print(f"\nsize=144: FAILED (expected -- not an I_h orbit-union closed size)")
        print(f"  {e}")
