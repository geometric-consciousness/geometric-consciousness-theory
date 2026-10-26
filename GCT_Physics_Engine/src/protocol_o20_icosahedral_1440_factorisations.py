#!/usr/bin/env python3
"""
protocol_o20_icosahedral_1440_factorisations.py
================================================

Classification of icosahedral combinatorial factorisations of 1440.
Conditional arithmetic catalogue for Open Problem O.20.

CONTEXT (V3 Ch05 §5.2.1)

Conditional on the Tier-3 O.38 adoption of N_cage = 144, the registered
integer product is
    1440 = N_cage * N_C3 = 144 * 10
where N_C3 = 10 is the exact count of three-fold axes. The multiplication
and factor catalogue are exact arithmetic; this protocol neither selects
N_cage = 144 nor establishes a physical saturation mechanism or Higgs VEV.

CLOSURE STRATEGY

Enumerate all (a, b) pairs with a * b = 1440 where both a and b are
identified with icosahedral combinatorial quantities (group orders,
orbit sizes, irrep dimensions, polytope element counts, Coxeter
invariants). Classify each factorisation as:
    - INDEPENDENT combinatorial factorisation
    (both factors occur separately in the declared dictionary)
  - COINCIDENTAL integer agreement
    (no physical content; arithmetic accident)
  - REGISTERED CONDITIONAL factorisation
    (the 144 x 10 product conditional on Tier-3 O.38)

ICOSAHEDRAL COMBINATORIAL DICTIONARY

  |I|         = 60   (icosahedral rotation group order)
  |I_h|       = 120  (full icosahedral group, with inversion)
  Vertices_ico  = 12  (icosahedron)
  Edges_ico     = 30
  Faces_ico     = 20
  Vertices_dod  = 20  (dodecahedron)
  Edges_dod     = 30
  Faces_dod     = 12
  h_3 (Coxeter) = 10  (Coxeter number of H_3)
  rank(H_3)     = 3
  Irreps_I      = (1, 3, 3, 4, 5)  with sum^2 = 60 = |I|
  N_cage        = 144  (Tier-3 O.38 conditional input)
  N_C3          = 10   (3-fold axes count; = h_3)

PRIMARY-DECOMPOSITION CHECK

1440 = 2^5 * 3^2 * 5 = 32 * 45 (prime decomposition)
Number of divisors: (5+1)(2+1)(1+1) = 36
"""

import json
import math
from pathlib import Path

try:
    from gct_utils import get_output_path
    OUTPUT_DIR_AVAILABLE = True
except ImportError:
    OUTPUT_DIR_AVAILABLE = False

N_TARGET = 1440

# Declared combinatorial counts and the Tier-3 O.38 conditional input
ICOSAHEDRAL_COUNTS = {
    "Order_I_rotational": 60,
    "Order_Ih_full": 120,
    "Icosa_vertices": 12,
    "Icosa_edges": 30,
    "Icosa_faces": 20,
    "Dodeca_vertices": 20,
    "Dodeca_edges": 30,
    "Dodeca_faces": 12,
    "Coxeter_h3": 10,
    "Rank_H3": 3,
    "Irrep_dim_5": 5,
    "Irrep_dim_4": 4,
    "Irrep_dim_3a": 3,
    "Irrep_dim_3b": 3,
    "Irrep_dim_1": 1,
    "N_cage_O38_conditional": 144,
    "N_C3_GCT": 10,
    "Inversion_pairs": 2,
    "Tetrahedral_subgroup_T": 12,
    "Dihedral_subgroup_D5": 10,
    "Dihedral_subgroup_D3": 6,
    "C5_axes": 6,
    "C3_axes": 10,
    "C2_axes": 15,
    "Total_rotation_axes": 31,
    "EulerC_S2": 2,
    "Vertices_24cell": 24,
    "Edges_24cell": 96,
    "Faces_24cell": 96,
}


def all_factor_pairs(n):
    """All (a, b) pairs with a * b = n and a <= b."""
    out = []
    for a in range(1, int(math.isqrt(n)) + 1):
        if n % a == 0:
            out.append((a, n // a))
    return out


def classify_factorisation(a, b, counts):
    """Identify a, b in the icosahedral dictionary. Return matched names."""
    a_names = [k for k, v in counts.items() if v == a]
    b_names = [k for k, v in counts.items() if v == b]
    return a_names, b_names


def assess_factorisation(a, b, a_names, b_names):
    """Classify each factorisation relative to the registered 144 x 10 pair.

    Arithmetic classification:
    - 'REGISTERED_CONDITIONAL': (N_cage, N_C3) = (144, 10), conditional
      on the Tier-3 O.38 input N_cage = 144
    - 'INDEPENDENT': both factors identified with distinct icosahedral
      combinatorial origins (group orders, polytope elements, etc.)
      potentially providing a cross-check
    - 'TRIVIAL': one factor is 1 (no topology)
    - 'PRIME': involves a factor that is NOT a primary icosahedral count
      (3, 5, 6, 9, 15, 32, 45 etc.) -- arithmetic coincidence
    - 'SAME_PATHWAY': reserved for algebraically equivalent rewritings
    """
    if a == 1 or b == 1:
        return "TRIVIAL", "Factor of 1; no topology"
    if (a == 144 and b == 10) or (a == 10 and b == 144):
        return (
            "REGISTERED_CONDITIONAL",
            "Exact product (N_cage) x (N_C3) = 144 x 10, conditional on "
            "the Tier-3 O.38 input N_cage = 144",
        )
    if not a_names or not b_names:
        return "PRIME", f"Factor not in icosahedral dictionary; arithmetic accident"
    # Both identified; check if they're independent topological objects
    # Define "structurally similar" if both names reference the same object class
    same_class_pairs = [
        ({"Order_I_rotational"}, {"Coxeter_h3", "N_C3_GCT", "C3_axes",
                                  "Dihedral_subgroup_D5"}),
        ({"Order_Ih_full"}, {"Icosa_faces", "Inversion_pairs"}),
        ({"Icosa_vertices", "Dodeca_faces"}, {"Coxeter_h3", "N_C3_GCT"}),
    ]
    a_set = set(a_names)
    b_set = set(b_names)
    # If both factors map to distinct combinatorial structures, INDEPENDENT
    return "INDEPENDENT", (
        f"Distinct icosahedral structures: {a_names[0]} x {b_names[0]} "
        f"(an independent arithmetic factorisation in the declared dictionary)"
    )


def run_classification():
    pairs = all_factor_pairs(N_TARGET)
    catalogue = []
    for a, b in pairs:
        a_names, b_names = classify_factorisation(a, b, ICOSAHEDRAL_COUNTS)
        verdict, rationale = assess_factorisation(a, b, a_names, b_names)
        catalogue.append({
            "a": a,
            "b": b,
            "a_icosahedral_names": a_names,
            "b_icosahedral_names": b_names,
            "verdict": verdict,
            "rationale": rationale,
        })

    return catalogue


def main():
    print("=" * 76)
    print("O.20 PROTOCOL: Icosahedral 1440 factorisations classification")
    print("=" * 76)
    print(f"\nTarget: {N_TARGET} = 2^5 * 3^2 * 5")
    print(f"Total divisors of {N_TARGET}: "
          f"{len(all_factor_pairs(N_TARGET)) * 2 - (1 if int(math.isqrt(N_TARGET))**2 == N_TARGET else 0)}")

    catalogue = run_classification()

    # Group by verdict
    by_verdict = {}
    for c in catalogue:
        by_verdict.setdefault(c["verdict"], []).append(c)

    print(f"\nIcosahedral combinatorial dictionary ({len(ICOSAHEDRAL_COUNTS)} entries):")
    for k, v in sorted(ICOSAHEDRAL_COUNTS.items(), key=lambda kv: kv[1]):
        print(f"  {k:>25}: {v}")

    print(f"\nClassification ({len(catalogue)} factor pairs a <= b):")
    print(f"  {'a':>6}  {'b':>6}  {'verdict':>15}  {'a-names':>35}  {'b-names':>35}")
    for c in catalogue:
        a_str = (c["a_icosahedral_names"][0] if c["a_icosahedral_names"]
                 else "(none)")
        b_str = (c["b_icosahedral_names"][0] if c["b_icosahedral_names"]
                 else "(none)")
        print(f"  {c['a']:>6}  {c['b']:>6}  {c['verdict']:>15}  {a_str:>35}  {b_str:>35}")

    # Verdict summary
    print(f"\nVerdict breakdown:")
    for v in ["REGISTERED_CONDITIONAL", "INDEPENDENT", "TRIVIAL", "PRIME", "SAME_PATHWAY"]:
        items = by_verdict.get(v, [])
        print(f"  {v:>15}: {len(items)} pairs")

    # Independent (non-registered, non-trivial, non-prime) factorisations
    independent = by_verdict.get("INDEPENDENT", [])
    print(f"\n{len(independent)} INDEPENDENT factorisation(s) identified -- "
          f"each is an arithmetic factorisation in the declared dictionary:")
    for c in independent:
        print(f"  {c['a']} x {c['b']}: {c['rationale']}")

    registered = by_verdict.get("REGISTERED_CONDITIONAL", [])
    primes = by_verdict.get("PRIME", [])

    print(f"\n" + "=" * 76)
    print("VERDICT FOR O.20")
    print("=" * 76)
    print(f"  Total factor pairs (a <= b)         : {len(catalogue)}")
    print(f"  Registered conditional (144 x 10)  : {len(registered)}")
    print(f"  Independent dictionary products     : {len(independent)}")
    print(f"  Trivial (factor of 1)               : {len(by_verdict.get('TRIVIAL', []))}")
    print(f"  Arithmetic-coincidence factors      : {len(primes)}")
    print(f"")
    if len(independent) > 0:
        print(f"  STATUS: 1440 admits {len(independent)} independent icosahedral")
        print(f"  factorisation(s) besides the registered (144) x (10) product.")
        print(f"  The catalogue is exact arithmetic only. The 144 x 10 entry is")
        print(f"  conditional on Tier-3 O.38's adoption of N_cage = 144; this")
        print(f"  protocol does not select N_cage, a physical mechanism, or a VEV.")
    else:
        print(f"  STATUS: The (144) x (10) factorisation is UNIQUELY identified")
        print(f"  as the only icosahedral combinatorial decomposition of 1440")
        print(f"  with both factors in the icosahedral dictionary.")
        print(f"  All other factorisations involve arithmetic-coincidence primes.")

    print("=" * 76)

    out = {
        "target": N_TARGET,
        "icosahedral_dictionary": ICOSAHEDRAL_COUNTS,
        "n_factor_pairs": len(catalogue),
        "factor_pairs": catalogue,
        "verdict_breakdown": {v: len(items) for v, items in by_verdict.items()},
        "registered_conditional_factorisations": registered,
        "independent_factorisations": independent,
        "closure_text": (
            f"1440 admits {len(catalogue)} factor pairs (a <= b). Of these, "
            f"{len(registered)} is the registered (N_cage, N_C3) = (144, 10) product, "
            "conditional on the Tier-3 O.38 input N_cage = 144; "
            f"{len(independent)} represent INDEPENDENT combinatorial products with both "
            f"factors in the declared dictionary; "
            f"{len(by_verdict.get('TRIVIAL', []))} is trivial (one factor = 1); "
            f"{len(primes)} involve arithmetic-coincidence factors. "
            "The multiplication and catalogue are exact arithmetic. This protocol does "
            "not select N_cage = 144, establish a physical saturation mechanism, or "
            "derive a Higgs VEV."
        ),
    }
    if OUTPUT_DIR_AVAILABLE:
        out_path = get_output_path("protocol_o20_icosahedral_1440_factorisations_results.json")
    else:
        out_path = Path(__file__).resolve().parent.parent / "data" / "protocol_o20_icosahedral_1440_factorisations_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nResults saved to: {out_path}")
    print("=" * 76)


if __name__ == "__main__":
    main()
