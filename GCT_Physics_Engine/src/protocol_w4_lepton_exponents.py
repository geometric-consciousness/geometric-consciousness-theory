#!/usr/bin/env python3
"""
protocol_w4_lepton_exponents.py - W4: canonical-integer audit of N=11, N=17
============================================================================
The electron mass exponent 107 is canonically identified as a UNIQUE H_3
invariant: the second power sum of the Coxeter exponents,
    sum_i m_i^2 = 1^2 + 5^2 + 9^2 = 107   ({m_i} = {1,5,9}),
unique to H_3 among finite irreducible Coxeter groups (engine
protocol_o14_coxeter_exponent_squares.py). The phason-stiffness exponent 18 is
the Shephard-Todd degree sum 2+6+10. W4 asks whether the lepton harmonic
exponents N=11 (muon) and N=17 (tau) admit an analogous canonical-invariant
identification, or only the phenomenological 6k-1 ladder of Ch08 S8.1
(11 = 2*6-1, 17 = 11+6), which the manuscript labels Tier 3.

Decidable tests:
  T1 (107-analog / power sums): is 11 or 17 a power sum sum_i m_i^p or sum_i d_i^p
     of the H_3 exponent/degree multisets? (107 IS; 18 IS.) If neither 11 nor 17
     is, they do not belong to the canonical power-sum family that anchors 107.
  T2 (distinctiveness): over a FIXED, pre-declared set of canonical H_3 integer
     formulas, count how many produce each target in {11, 17, 18, 107}. A
     distinctive integer (like 107) is produced by few formulas; an
     under-determined one (small integer) by many. Report the hit count and the
     producing formulas per target.
  T3 (ladder structure): verify the 6k-1 ladder (k=2->11, k=3->17, spacing 6),
     identify the cleanest single-integer hooks (11 = h+1; 17 = sum d_i - 1),
     and note which pieces remain un-derived handles (the generator choice 6=d_2,
     the -1 offset / Decoupling Unit, the generation indexing).

Verdict target: whether N=11, N=17 can be PROMOTED via a 107-style canonical
identification (closing the Tier-3 anchor) or stay Tier 3 (residual = the
non-perturbative lepton-eigenvalue extraction, O.5).
"""

import json
import os
import sys
import io
from itertools import combinations

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

try:
    from gct_utils import get_output_path
except ImportError:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from gct_utils import get_output_path

# Canonical H_3 data (Humphreys 1990 Table 3.1)
EXPONENTS = [1, 5, 9]          # m_i
DEGREES = [2, 6, 10]           # d_i = m_i + 1
H_COXETER = 10                 # Coxeter number
ICOSA = {"vertices": 12, "edges": 30, "faces": 20}
GROUP = {"|I|": 60, "|I_h|": 120}

TARGETS = [11, 17, 18, 107]    # muon, tau, stiffness, electron


def power_sums(multiset, pmax=3):
    return {p: sum(x ** p for x in multiset) for p in range(1, pmax + 1)}


def canonical_formula_set():
    """A fixed, pre-declared, SYMMETRIC set of canonical H_3 integer formulas.
    Each base value v contributes v, v-1, v+1 (so composites are treated like
    singles -- no asymmetry that would spuriously zero a target). Declared
    before looking at which hit the targets (no cherry-picking)."""
    base = {}  # name -> value

    # power sums of exponents and degrees (p=1,2,3)
    for p in (1, 2, 3):
        base[f"sum m_i^{p}"] = sum(m ** p for m in EXPONENTS)
        base[f"sum d_i^{p}"] = sum(d ** p for d in DEGREES)
    # k-subset sums of exponents and degrees (k=1,2,3)
    for k in (1, 2, 3):
        for c in combinations(EXPONENTS, k):
            base[f"sum exps{c}"] = sum(c)
        for c in combinations(DEGREES, k):
            base[f"sum degs{c}"] = sum(c)
    # single canonical integers
    for nm, v in {"h": H_COXETER, **{f"deg{d}": d for d in DEGREES},
                  **{f"exp{m}": m for m in EXPONENTS},
                  "icosa_V": 12, "icosa_E": 30, "icosa_F": 20,
                  "|I|": 60, "|I_h|": 120}.items():
        base[nm] = v
    # pairwise products of small canonical integers
    for a, b in combinations(sorted({1, 2, 5, 6, 9, 10, 12}), 2):
        base[f"{a}*{b}"] = a * b

    # expand each base value symmetrically with +/-1 neighbours
    F = {}
    for nm, v in base.items():
        for off, tag in ((0, ""), (-1, "-1"), (1, "+1")):
            F.setdefault(int(v + off), []).append(nm + tag)
    return F


def run():
    print("=" * 72)
    print("GCT Protocol W4 - canonical-integer audit of lepton exponents N=11,17")
    print("=" * 72)
    print(f"\n  H_3 exponents {EXPONENTS}, degrees {DEGREES}, Coxeter h={H_COXETER}")

    # T1: power-sum membership
    ps_m = power_sums(EXPONENTS)
    ps_d = power_sums(DEGREES)
    print(f"\n  T1 power sums:  exponents {ps_m}   degrees {ps_d}")
    ps_values = set(ps_m.values()) | set(ps_d.values())
    t1 = {t: (t in ps_values) for t in TARGETS}
    for t in TARGETS:
        print(f"     {t}: power-sum invariant? {t1[t]}")

    # T2: distinctiveness over the fixed formula set
    F = canonical_formula_set()
    print("\n  T2 distinctiveness (count of canonical formulas hitting each target):")
    t2 = {}
    for t in TARGETS:
        hits = F.get(t, [])
        t2[t] = hits
        shown = ", ".join(hits[:6]) + ("  ..." if len(hits) > 6 else "")
        print(f"     {t:>3}: {len(hits):>2} formula(s)   [{shown}]")

    # T3: ladder structure + cleanest hooks
    ladder_ok = (6 * 2 - 1 == 11) and (6 * 3 - 1 == 17) and (17 - 11 == 6)
    hook_11 = (11 == H_COXETER + 1)               # h + 1
    hook_17 = (17 == sum(DEGREES) - 1)            # sum d_i - 1 = 18 - 1
    print("\n  T3 ladder structure:")
    print(f"     6k-1 ladder (k=2->11, k=3->17, spacing 6=d_2): {ladder_ok}")
    print(f"     clean hook  11 = h + 1: {hook_11}")
    print(f"     clean hook  17 = (sum d_i) - 1 = 18 - 1: {hook_17}")
    print(f"     un-derived handles: generator 6=d_2 choice; -1 'Decoupling "
          f"Unit' offset; generation indexing k in {{2,3}}")

    # ---- verdict ----
    n11_17_powersum = t1[11] or t1[17]
    distinctive_gap = (len(t2[107]) <= 2) and (len(t2[11]) >= 3 or len(t2[17]) >= 3)
    verdict = (
        "N=11 and N=17 do NOT admit a 107-style canonical-invariant "
        "identification. (T1) Neither is a power sum of the H_3 exponent or "
        f"degree multisets (those are {sorted(ps_values)}: 15,107 and 18,140), "
        "whereas 107 IS sum m_i^2 and 18 IS sum d_i. (T2) 107 is hit by very few "
        f"canonical formulas ({len(t2[107])}), while 11 and 17 are each hit by "
        f"many ({len(t2[11])}, {len(t2[17])}) -- small integers are not "
        "distinctive. (T3) The operative 6k-1 ladder is real (11=h+1, "
        "17=sum d_i -1, spacing d_2=6) but its generator choice, -1 offset, and "
        "generation indexing are un-derived handles. So N=11,17 cannot be "
        "promoted via a canonical invariant the way 107 was; the Tier-3 status "
        "stands, and the residual is the non-perturbative lepton-eigenvalue "
        "extraction (O.5)."
        if (not n11_17_powersum) else
        "Unexpected: a power-sum identification for 11 or 17 was found - review.")
    print("\n  " + "-" * 66)
    print("  VERDICT:", verdict)
    print("=" * 72)

    results = {
        "h3_exponents": EXPONENTS, "h3_degrees": DEGREES, "coxeter_h": H_COXETER,
        "power_sums_exponents": ps_m, "power_sums_degrees": ps_d,
        "T1_is_power_sum_invariant": t1,
        "T2_formula_hit_counts": {t: len(t2[t]) for t in TARGETS},
        "T2_formulas": {t: t2[t] for t in TARGETS},
        "T3_ladder_6k_minus_1": bool(ladder_ok),
        "T3_hook_11_is_h_plus_1": bool(hook_11),
        "T3_hook_17_is_sumdeg_minus_1": bool(hook_17),
        "T3_underived_handles": ["generator 6=d_2", "-1 Decoupling Unit offset",
                                  "generation indexing k in {2,3}"],
        "verdict": verdict,
        "promotable_via_canonical_invariant": bool(n11_17_powersum),
    }
    out = get_output_path("protocol_w4_lepton_exponents_results.json")
    with open(out, "w") as fp:
        json.dump(results, fp, indent=2)
    print(f"\n[Saved JSON] -> {out}")
    return results


if __name__ == "__main__":
    run()
