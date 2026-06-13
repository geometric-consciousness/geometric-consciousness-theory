"""
H.4-1 Topological Limit of Complexity
=====================================

Establishes that the physically realized p-adic identity tree has finite
maximum depth, bounded by the ratio of the relevant physical length scale
to the lattice spacing a_6 = 2 ell_P.

The mathematical p-adic fiber Z_p^hat is profinite (depth infinite by
construction); the physical realization is bounded because the lattice
cells that record the p-adic digits via nuclear-spin addresses
(Ch07 Sec 7.6.1) are themselves of finite count.

Outputs:
  - Mathematical depth: infinite (formal).
  - Polaron internal depth: log_p(N_cage) with N_cage = 144 (Ch05 muon
    saturation, V3 Ch05 Sec 5.2.1).
  - Biological substrate depth: log_p(N_Trp) for N_Trp ~ 1e8 local-inward
    Trp candidates per typical pyramidal neuron under the O.21 candidate-only
    disposition (~ 1e5 MTs/neuron x 1,250 dimers/MT x 1 Trp candidate per
    dimer ~= 1.3e8; assembled-lumen-axis verification remains open; V1 Ch17
    Sec 17.1.4 + Hirokawa-Takemura 2005, Conde-Caceres 2009).
  - Hubble-volume depth: log_p(L_H / a_6) with L_H = c/H_0,
    a_6 = 2 ell_P.

Tier 2 structural argument: any countable p-adic register over a
finite-cell lattice has depth <= log_p(N_cells); the "infinite
fractalization of identity" reading is excluded by lattice
discretization, which is itself a foundational postulate of the GCT
cut-and-project framework.
"""

from __future__ import annotations

import math
import json
from pathlib import Path

# Physical constants (SI)
PLANCK_LENGTH_M = 1.616255e-35     # ell_P
SPEED_OF_LIGHT_M_S = 2.99792458e8  # c
HUBBLE_H0_PER_S = 2.197e-18        # H_0 from Planck 2018 ~67.7 km/s/Mpc

# GCT lattice spacing
A6_LATTICE_M = 2.0 * PLANCK_LENGTH_M

# Hubble length
HUBBLE_LENGTH_M = SPEED_OF_LIGHT_M_S / HUBBLE_H0_PER_S

# Polaron cage saturation (V3 Ch05 muon-defect 144 = N_cage)
N_CAGE = 144

# Biological Trp population per typical pyramidal neuron under the conditional
# O.21 sensitivity branch n_rp = 1. The operative central branch remains
# n_rp = 0 until assembled-MT lumen-axis closure (V1 Ch17 Sec 17.1.4 audit:
# ~ 1e5 MTs/neuron x 1,250 dimers/MT x 1 Trp candidate per dimer ~= 1.3e8)
N_TRP_BIOLOGY = 1.0e8

# Hubble-volume lattice cell count
N_CELLS_HUBBLE_3D = (HUBBLE_LENGTH_M / A6_LATTICE_M) ** 3

# Primes to sweep (icosahedral natural primes: 2, 3, 5 from |I_h|=120=2^3*3*5)
ICOSAHEDRAL_PRIMES = [2, 3, 5]


def depth_bound(physical_count: float, p: int) -> float:
    """Maximum p-adic tree depth realizable on a substrate of given size."""
    if physical_count <= 1 or p < 2:
        return 0.0
    return math.log(physical_count) / math.log(p)


def compute_bounds() -> dict:
    results = {
        "constants": {
            "ell_P_m": PLANCK_LENGTH_M,
            "a6_m": A6_LATTICE_M,
            "c_m_s": SPEED_OF_LIGHT_M_S,
            "H0_per_s": HUBBLE_H0_PER_S,
            "L_Hubble_m": HUBBLE_LENGTH_M,
            "N_cage": N_CAGE,
            "N_Trp_biology": N_TRP_BIOLOGY,
            "N_cells_Hubble_3D": N_CELLS_HUBBLE_3D,
        },
        "mathematical_depth": "infinite (profinite Z_p^hat)",
        "physical_depths": {},
    }
    for p in ICOSAHEDRAL_PRIMES:
        results["physical_depths"][f"p={p}"] = {
            "polaron_internal_depth": depth_bound(N_CAGE, p),
            "biological_substrate_depth": depth_bound(N_TRP_BIOLOGY, p),
            "Hubble_volume_depth": depth_bound(N_CELLS_HUBBLE_3D, p),
        }
    return results


def verify_monotonicity(results: dict) -> dict:
    """Depth must decrease as p increases (same N, larger base => fewer digits)."""
    checks = {}
    for substrate in ["polaron_internal_depth",
                       "biological_substrate_depth",
                       "Hubble_volume_depth"]:
        depths = [results["physical_depths"][f"p={p}"][substrate]
                   for p in ICOSAHEDRAL_PRIMES]
        checks[substrate] = {
            "depths_by_p_2_3_5": depths,
            "monotone_decreasing": all(depths[i] >= depths[i+1]
                                         for i in range(len(depths)-1)),
        }
    return checks


def verify_hierarchy(results: dict) -> dict:
    """Polaron internal < biological substrate < Hubble volume."""
    checks = {}
    for p in ICOSAHEDRAL_PRIMES:
        d = results["physical_depths"][f"p={p}"]
        ordered = (d["polaron_internal_depth"]
                    <= d["biological_substrate_depth"]
                    <= d["Hubble_volume_depth"])
        checks[f"p={p}"] = {
            "polaron_le_biology_le_hubble": ordered,
            "values": [d["polaron_internal_depth"],
                        d["biological_substrate_depth"],
                        d["Hubble_volume_depth"]],
        }
    return checks


def main():
    results = compute_bounds()
    results["monotonicity_check"] = verify_monotonicity(results)
    results["hierarchy_check"] = verify_hierarchy(results)
    results["closure_status"] = {
        "tier": "Tier 2 structural bound",
        "claim": ("Physical p-adic tree depth is finite and bounded by "
                   "log_p(N_cells) where N_cells is the count of lattice "
                   "cells comprising the substrate. The infinite-"
                   "fractalization reading is excluded by lattice "
                   "discretization."),
        "remaining_open": ("Tier 1 first-principles derivation of N_cage = "
                           "144 from cut-and-project geometry is closed "
                           "(V3 Ch05); the universal upper bound here is "
                           "a corollary."),
    }

    out_dir = Path(__file__).parent.parent / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "h4_1_topological_limit.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"H.4-1 Topological Limit of Complexity")
    print(f"=" * 60)
    print(f"a_6 = {A6_LATTICE_M:.3e} m")
    print(f"L_Hubble = {HUBBLE_LENGTH_M:.3e} m")
    print(f"N_cells (Hubble volume, 3D) = {N_CELLS_HUBBLE_3D:.3e}")
    print()
    for p in ICOSAHEDRAL_PRIMES:
        d = results["physical_depths"][f"p={p}"]
        print(f"p = {p}:")
        print(f"  Polaron internal depth   = {d['polaron_internal_depth']:.3f}")
        print(f"  Biological substrate     = {d['biological_substrate_depth']:.3f}")
        print(f"  Hubble-volume depth      = {d['Hubble_volume_depth']:.3f}")
    print()
    print("Monotonicity p=2 > p=3 > p=5:",
          all(results["monotonicity_check"][k]["monotone_decreasing"]
               for k in results["monotonicity_check"]))
    print("Hierarchy polaron <= biology <= Hubble:",
          all(results["hierarchy_check"][f"p={p}"]["polaron_le_biology_le_hubble"]
               for p in ICOSAHEDRAL_PRIMES))
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
