#!/usr/bin/env python3
"""
protocol_o15a_h3_invariant_degrees.py
======================================

Identification of the exponent 18 in K_perp/K_parallel = phi^(-18) as the
canonical Shephard-Todd invariant-degree sum of the icosahedral H_3
Coxeter group. Partial closure of Open Problem O.15(a) direction.

CONTEXT (App K §K.3-K.4)

The GCT prediction K_perp/K_parallel = phi^(-18) is currently a Tier 2
POSTULATE with a Tier 3 specific exponent. App K §K.4 derives 18 via a
heuristic "rank 3 × Galois 2 × dim 3 = 18" count, acknowledged in the
manuscript as a counting heuristic, not a derivation. App H O.15(a)
records the need for "a genuine RG calculation in the symmetry-adapted
phason elasticity framework producing phi^(-18) from icosahedral
group-theoretic axioms".

This protocol provides a SHARPER IDENTIFICATION of the integer 18 as
the standard Shephard-Todd / Coxeter-group invariant for H_3.

H_3 COXETER GROUP FACTS (Humphreys 1990 "Reflection Groups and
Coxeter Groups" Tables 1, 3.1)

  Rank r = 3
  Order |H_3| = 120
  Coxeter number h = 10
  Positive roots N = 15
  Reflections (= positive roots) = 15
  Fundamental degrees: d_1 = 2, d_2 = 6, d_3 = 10
  Sum of degrees: d_1 + d_2 + d_3 = 2 + 6 + 10 = 18
  Shephard-Todd identity: sum(d_i) = N + r
  Check: 18 = 15 + 3 ✓

STRUCTURAL IDENTIFICATION

The integer 18 appearing in phi^(-18) is the SUM OF FUNDAMENTAL
DEGREES of the icosahedral H_3 Coxeter group. This is a canonical
invariant of the reflection group, not a heuristic count.

Equivalently: 18 = N + r where N = 15 is the number of positive roots
(reflections) and r = 3 is the rank. The Shephard-Todd identity
sum(d_i) = N + r is a standard result for any finite Coxeter group.

For other rank-3 Coxeter groups (comparison):
  A_3 (S_4):          degrees 2, 3, 4;   sum =  9
  B_3 (BC_3):         degrees 2, 4, 6;   sum = 12
  H_3 (icosahedral):  degrees 2, 6, 10;  sum = 18

The icosahedral case gives the largest invariant-degree sum among
rank-3 finite Coxeter groups (the only rank-3 non-crystallographic
case; H_3 is the only finite Coxeter group containing 5-fold symmetry).

CONSEQUENCE FOR O.15(a)

The exponent 18 in phi^(-18) is now identified with the canonical
H_3 invariant-degree sum rather than the heuristic "rank × Galois × dim"
counting in App K §K.4. This SHARPENS the structural origin of the
exponent but does NOT close the FULL RG derivation: the connection
between (a) the sum of invariant degrees and (b) the phason-elasticity
stiffness ratio still requires a symmetry-adapted RG argument that
maps the Coxeter invariant to the phason-mode renormalization. The
identification of 18 with the canonical Coxeter invariant is a
Tier 2 sharpening of the Tier 3 heuristic count.

STATUS

  The integer 18 is the canonical Shephard-Todd invariant-degree sum of
  H_3 = N + r = 15 + 3 (Tier 2 structural identification). This is the
  canonical form of the App K §K.4 "rank × Galois × dim" count, which
  gives the same value at the Tier 3 heuristic level.

  Remaining open piece (full Tier 1 closure of O.15(a)): the
  symmetry-adapted phason-elasticity RG flow that maps the Coxeter
  invariant-degree sum to the K_perp/K_parallel exponent. This is the
  research-level math beyond session scope; the structural identification
  here SHARPENS the heuristic but does NOT fully derive phi^(-18) from
  first principles.
"""

import json
import math
from pathlib import Path

try:
    from gct_utils import get_output_path
    OUTPUT_DIR_AVAILABLE = True
except ImportError:
    OUTPUT_DIR_AVAILABLE = False

# Coxeter group data (Humphreys 1990)
COXETER_DATA = {
    "A_3": {
        "rank": 3,
        "order": 24,
        "Coxeter_h": 4,
        "positive_roots_N": 6,
        "degrees": [2, 3, 4],
        "description": "S_4 = symmetric group on 4 elements",
    },
    "B_3": {
        "rank": 3,
        "order": 48,
        "Coxeter_h": 6,
        "positive_roots_N": 9,
        "degrees": [2, 4, 6],
        "description": "Symmetries of the cube/octahedron",
    },
    "H_3": {
        "rank": 3,
        "order": 120,
        "Coxeter_h": 10,
        "positive_roots_N": 15,
        "degrees": [2, 6, 10],
        "description": "Icosahedral group (non-crystallographic)",
    },
    "H_4": {
        "rank": 4,
        "order": 14400,
        "Coxeter_h": 30,
        "positive_roots_N": 60,
        "degrees": [2, 12, 20, 30],
        "description": "600-cell symmetry (4D non-crystallographic)",
    },
}


def verify_shephard_todd_identity(group_data):
    """Check sum(d_i) = N + r."""
    sum_deg = sum(group_data["degrees"])
    n_plus_r = group_data["positive_roots_N"] + group_data["rank"]
    return sum_deg, n_plus_r, sum_deg == n_plus_r


def main():
    print("=" * 76)
    print("O.15(a) PROTOCOL: H_3 invariant-degree identification for exponent 18")
    print("=" * 76)

    print(f"\nCoxeter-group data (Humphreys 1990 Tables):")
    print(f"  {'group':>5} {'rank':>5} {'order':>6} {'h':>4} {'N_pos':>6} "
          f"{'degrees':>15} {'sum':>5} {'N+r':>5} {'match':>6}")
    for name, data in COXETER_DATA.items():
        sum_deg, n_plus_r, matches = verify_shephard_todd_identity(data)
        deg_str = str(data["degrees"])
        print(f"  {name:>5} {data['rank']:>5} {data['order']:>6} "
              f"{data['Coxeter_h']:>4} {data['positive_roots_N']:>6} "
              f"{deg_str:>15} {sum_deg:>5} {n_plus_r:>5} {str(matches):>6}")

    h3 = COXETER_DATA["H_3"]
    print(f"\nIcosahedral H_3 specifically:")
    print(f"  Fundamental degrees                : {h3['degrees']}")
    print(f"  Sum (= the GCT exponent 18)        : {sum(h3['degrees'])}")
    print(f"  Shephard-Todd: N + r               : {h3['positive_roots_N']} + {h3['rank']} = {h3['positive_roots_N'] + h3['rank']}")
    print(f"  Identification matches             : {sum(h3['degrees']) == 18}")

    print(f"\nComparison to the App K §K.4 heuristic count:")
    print(f"  Heuristic count: rank * Galois * dim = 3 * 2 * 3 = 18")
    print(f"  Canonical Coxeter-invariant: sum of fundamental degrees of H_3 = 18")
    print(f"  Both give the same numerical answer; the Coxeter-invariant")
    print(f"  identification is the canonical (Shephard-Todd) form, not an")
    print(f"  ad hoc product.")

    # Rank-3 comparison
    rank_3_groups = ["A_3", "B_3", "H_3"]
    sums = {g: sum(COXETER_DATA[g]["degrees"]) for g in rank_3_groups}
    print(f"\nRank-3 finite Coxeter group invariant-degree sums:")
    for g in rank_3_groups:
        print(f"  {g}: {sums[g]}")
    print(f"  H_3 has the LARGEST sum (=18) among rank-3 finite Coxeter groups.")
    print(f"  Reason: H_3 is non-crystallographic (5-fold symmetry); its Coxeter")
    print(f"  number h = 10 exceeds crystallographic bounds (B_3 has h=6, A_3 h=4).")

    print(f"\n" + "=" * 76)
    print("VERDICT FOR O.15(a) -- structural sharpening")
    print("=" * 76)
    print(f"  CANONICAL IDENTIFICATION (Shephard-Todd):")
    print(f"    18 = sum of H_3 fundamental degrees = 2 + 6 + 10")
    print(f"       = N_pos_roots + rank = 15 + 3")
    print(f"    Standard finite-Coxeter-group invariant; canonical, not ad hoc.")
    print(f"")
    print(f"  App K §K.4 heuristic count (same value at Tier 3):")
    print(f"    18 = rank * Galois * dim = 3 * 2 * 3")
    print(f"")
    print(f"  STATUS: TIER 2 structural sharpening of the integer 18 identification.")
    print(f"          NOT a full first-principles RG derivation of phi^(-18).")
    print(f"")
    print(f"  Remaining open piece (full Tier 1 closure of O.15(a)):")
    print(f"    The symmetry-adapted phason-elasticity RG flow that maps the")
    print(f"    Coxeter invariant-degree sum to the K_perp/K_parallel exponent.")
    print(f"    This requires research-level RG calculation in the Lubensky-")
    print(f"    Ramaswamy-Toner framework with explicit H_3 symmetry-breaking")
    print(f"    pattern.")
    print("=" * 76)

    out = {
        "coxeter_data": COXETER_DATA,
        "H_3_invariant_degree_sum": sum(h3["degrees"]),
        "shephard_todd_identity_check": {
            name: {"sum_degrees": sum(d["degrees"]),
                   "N_plus_r": d["positive_roots_N"] + d["rank"],
                   "matches": sum(d["degrees"]) == d["positive_roots_N"] + d["rank"]}
            for name, d in COXETER_DATA.items()
        },
        "rank_3_invariant_sums": sums,
        "H_3_is_largest_rank_3_sum": True,
        "structural_identification": (
            "18 in phi^(-18) is the sum of H_3 fundamental degrees "
            "= 2 + 6 + 10 = N_pos_roots + rank = 15 + 3. This is the "
            "canonical Shephard-Todd invariant of the icosahedral H_3 "
            "Coxeter group, NOT an ad-hoc rank*Galois*dim count."
        ),
        "status": "Tier 2 structural sharpening; full first-principles RG derivation still open",
        "remaining_open": (
            "The symmetry-adapted phason-elasticity RG flow mapping the Coxeter "
            "invariant-degree sum to the K_perp/K_parallel exponent. Research-level "
            "LRT-style calculation with explicit H_3 symmetry-breaking."
        ),
    }
    if OUTPUT_DIR_AVAILABLE:
        out_path = get_output_path("protocol_o15a_h3_invariant_degrees_results.json")
    else:
        out_path = Path(__file__).resolve().parent.parent / "data" / "protocol_o15a_h3_invariant_degrees_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nResults saved to: {out_path}")
    print("=" * 76)


if __name__ == "__main__":
    main()
