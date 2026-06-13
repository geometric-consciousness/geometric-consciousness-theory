#!/usr/bin/env python3
"""
protocol_o14_n107_combinatorial_enum.py
========================================

Combinatorial enumeration of icosahedral integers up to ~250, checking
whether n = 107 surfaces from any natural icosahedral count, sum,
difference, or product of orbit sizes.

PROBLEM STATEMENT (App H O.14)

The electron gap-label n = -107 in the AF-core dimension group / trace
image of the AKN substitution algebra is empirically necessary (m_e =
M_P phi^-107 (1-5alpha) matches CODATA to 1006 ppm), but lacks a
first-principles uniqueness proof. The full Cuntz-Krieger K_0(O_A) for
A=[[1,1],[1,0]] is trivial since coker(I-A^T) is trivial; see App Y
§Y.3 for the canonical AF-core-vs-full-O_A distinction. App H lists 10
paths explored under the O.14 closure program, all negative.

This protocol adds a SUPPLEMENTARY ENUMERATION: list all icosahedral
combinatorial integers in the range [1, 250] arising from natural
sums, differences, and products of:
  - Group orders: |I| = 60, |I_h| = 120
  - Polytope element counts: 12, 20, 30 (icosa); 12, 20, 30 (dodeca)
  - Irrep dimensions: 1, 3, 3, 4, 5
  - Coxeter h_3 = 10
  - Other natural icosahedral counts (24-cell, etc.)

GOAL

Document explicitly whether 107 appears from any natural icosahedral
combinatorial expression. A negative result strengthens the App H
O.14 status: "Tier 3 empirical anchor; Tier 1 uniqueness genuinely
open pending O.5/QLQCD-1L".

This is COMPLEMENTARY to the 10 paths listed in App H --
not a new positive closure, but additional documented negative evidence.
"""

import json
import math
from pathlib import Path

try:
    from gct_utils import get_output_path
    OUTPUT_DIR_AVAILABLE = True
except ImportError:
    OUTPUT_DIR_AVAILABLE = False

# Icosahedral combinatorial primitives
ICOSAHEDRAL_PRIMITIVES = {
    "I_order": 60,
    "Ih_order": 120,
    "icosa_vertices": 12,
    "icosa_edges": 30,
    "icosa_faces": 20,
    "dodeca_vertices": 20,
    "dodeca_edges": 30,
    "dodeca_faces": 12,
    "Coxeter_h3": 10,
    "rank_H3": 3,
    "irrep_5": 5,
    "irrep_4": 4,
    "irrep_3a": 3,
    "irrep_1": 1,
    "N_cage_GCT": 144,
    "tetrahedral_subgroup": 12,
    "dihedral_D5": 10,
    "dihedral_D3": 6,
    "C5_axes": 6,
    "C3_axes": 10,
    "C2_axes": 15,
    "24_cell_vertices": 24,
    "24_cell_edges": 96,
    "24_cell_faces": 96,
    "Cox_pol_index": 32,    # icosahedral binary polyhedral group has 120 elements
    "I_x_Z2": 120,
}

TARGET = 107
MAX_VALUE = 250


def enumerate_combinations(primitives, max_value=MAX_VALUE):
    """Enumerate sums, differences, products, and ratios of primitive pairs."""
    values = list(primitives.values())
    names = list(primitives.keys())

    expressions = {}  # integer -> list of expressions
    # Singletons
    for name, v in primitives.items():
        if 1 <= v <= max_value:
            expressions.setdefault(v, []).append(name)

    # Pairs: sums, differences, products
    for i, vi in enumerate(values):
        for j, vj in enumerate(values):
            if i == j:
                continue
            # Sum
            s = vi + vj
            if 1 <= s <= max_value:
                expressions.setdefault(s, []).append(f"{names[i]} + {names[j]}")
            # Difference (positive only)
            d = vi - vj
            if 1 <= d <= max_value:
                expressions.setdefault(d, []).append(f"{names[i]} - {names[j]}")
            # Product
            p = vi * vj
            if 1 <= p <= max_value:
                expressions.setdefault(p, []).append(f"{names[i]} * {names[j]}")
            # Integer ratios
            if vj != 0 and vi % vj == 0:
                r = vi // vj
                if 1 <= r <= max_value:
                    expressions.setdefault(r, []).append(f"{names[i]} / {names[j]}")

    # Triples: sums of three, e.g., a + b - c
    for i, vi in enumerate(values):
        for j, vj in enumerate(values):
            for k, vk in enumerate(values):
                if len({i, j, k}) < 2:
                    continue
                v3 = vi + vj - vk
                if 1 <= v3 <= max_value:
                    expressions.setdefault(v3, []).append(
                        f"{names[i]} + {names[j]} - {names[k]}"
                    )

    return expressions


def main():
    print("=" * 76)
    print("O.14 COMPLEMENTARY: icosahedral combinatorial enumeration, target n=107")
    print("=" * 76)

    print(f"\nIcosahedral primitives ({len(ICOSAHEDRAL_PRIMITIVES)} entries):")
    for k, v in sorted(ICOSAHEDRAL_PRIMITIVES.items(), key=lambda kv: kv[1]):
        print(f"  {k:>25}: {v}")

    expressions = enumerate_combinations(ICOSAHEDRAL_PRIMITIVES)

    print(f"\nNumber of distinct integers reached in [1, {MAX_VALUE}]: "
          f"{len(expressions)}")

    # Check if 107 is reached
    target_expressions = expressions.get(TARGET, [])
    if target_expressions:
        print(f"\n*** 107 IS reached via: ***")
        for expr in target_expressions[:10]:
            print(f"  {expr}")
        verdict = ("(positive direction) 107 is reached via "
                   f"{len(target_expressions)} icosahedral combinatorial "
                   "expression(s). However, REACHABILITY does not establish "
                   "UNIQUENESS; many integers in [1, 250] are reachable from "
                   "the icosahedral primitives. The empirical anchor at n=-107 "
                   "needs additional structural justification to be uniquely "
                   "distinguished from other reachable integers by a first-principles argument.")
    else:
        print(f"\n*** 107 is NOT reached from any natural icosahedral combinatorial expression ***")
        verdict = ("(negative direction supporting O.14 status) 107 does NOT "
                   "arise from any natural sum, difference, product, or ratio "
                   "of the standard icosahedral combinatorial primitives "
                   f"(|I|, |I_h|, polytope counts, irrep dimensions, Coxeter "
                   "invariants). Consistent with the 10 App H O.14 paths "
                   "in App H O.14 (all negative). 107 = 107 is prime in Z, "
                   "and the icosahedral combinatorial structure produces "
                   "primarily small composites of {2, 3, 5} (the prime "
                   "factors of 60 = |I| and 120 = |I_h|).")

    # Distribution of reachable integers
    reached = sorted(expressions.keys())
    print(f"\nFirst 30 reachable integers: {reached[:30]}")
    print(f"Reachable integers in [100, 120]: {[v for v in reached if 100 <= v <= 120]}")

    # Check neighbors of 107
    print(f"\nNeighbors of 107 reachable status:")
    for n in range(100, 115):
        if n in expressions:
            print(f"  {n}: reachable via {expressions[n][0]}")
        else:
            print(f"  {n}: NOT reachable")

    print(f"\n" + "=" * 76)
    print("VERDICT FOR O.14 (COMPLEMENTARY DATA POINT)")
    print("=" * 76)
    print(f"  Verdict text: {verdict}")
    print(f"")
    print(f"  STATUS: This is COMPLEMENTARY EVIDENCE for the App H O.14 status,")
    print(f"  NOT a new closure. The n = -107 empirical anchor remains")
    print(f"  Tier 3 (empirically necessary, first-principles uniqueness open).")
    print(f"  Full Tier 1 uniqueness closure remains bundled with O.5 QLQCD-1L.")
    print("=" * 76)

    out = {
        "icosahedral_primitives": ICOSAHEDRAL_PRIMITIVES,
        "target_integer": TARGET,
        "max_value_enumerated": MAX_VALUE,
        "n_distinct_integers_reached": len(expressions),
        "is_107_reached": TARGET in expressions,
        "expressions_for_107": target_expressions[:10],
        "reachable_integers_near_107": {
            str(n): expressions.get(n, [])[:3] for n in range(100, 115)
        },
        "verdict_text": verdict,
        "status": "COMPLEMENTARY -- not a new closure; supports App H O.14 'uniqueness open' status",
    }
    if OUTPUT_DIR_AVAILABLE:
        out_path = get_output_path("protocol_o14_n107_combinatorial_enum_results.json")
    else:
        out_path = Path(__file__).resolve().parent.parent / "data" / "protocol_o14_n107_combinatorial_enum_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nResults saved to: {out_path}")
    print("=" * 76)


if __name__ == "__main__":
    main()
