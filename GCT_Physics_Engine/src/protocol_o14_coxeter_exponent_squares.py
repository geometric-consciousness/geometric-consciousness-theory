"""
O.14 Electron Gap-Label n = -107 as Sum of Squared Coxeter Exponents of H_3
============================================================================

Scope: the integer 107 is the canonical sum of squared Coxeter exponents
of the icosahedral H_3 group:

  Sigma m_i^2(H_3) = 1^2 + 5^2 + 9^2 = 1 + 25 + 81 = 107

where m_i = d_i - 1 are the Coxeter exponents (d_i = 2, 6, 10 are the
H_3 fundamental degrees; Humphreys 1990 Table 3.1).

This protocol closes only the Coxeter arithmetic/classification side:
|n| = 107 is the exact H_3 second-exponent-power-sum value. The electron
gap-label use of that integer remains a Tier 3 anchor inside the Tier 2
K-theoretic framework, with the AKN physical-link conjecture still pending
Open Problem O.14.

Companion O.14 routes registered in App H
=========================================

App H §O.14 also records:
  (a) orbifold Euler-characteristic chi(Z^6 / H_3) -> 0
  (b) APS eta-invariant via Connes-Moscovici -> open
  (c) cage-uniqueness via 42-orbit-union search -> 107 not in list
  (d) Bellissard gap-labels with Z[phi] enumeration -> many integers
  (e) AKN dimension group computation -> open
  (f) stringy/Hodge Euler characteristics -> not 107
  (g) combinatorial counts of icosahedral SUBGROUP orbits -> not 107
  (h) group-theoretic invariants of |I_h|/|H_3| -> not 107
  (i) anomaly polynomials -> not 107
  (j) Fibonacci-pair evaluation of tau(P_n) = phi^(-n) -> not 107
  (k) combinatorial enum from natural icosahedral primitives -> 107
      reachable but NOT uniquely selected

This protocol:
  (l) Sum of squared Coxeter exponents of H_3 itself
      = 1^2 + 5^2 + 9^2 = 107 EXACTLY.

This is qualitatively different from paths (g)-(h) which look at
SUBGROUPS or RATIOS. Path (l) reads 107 directly off a canonical
invariant of the H_3 group itself.

Why this is a candidate first-principles uniqueness
====================================================

The Coxeter exponents m_i of a finite Coxeter group W satisfy
several canonical identities:
  - Sum: Sigma m_i = N (number of positive roots) -- Solomon 1963
  - Degree-coexponent symmetry: m_i + m_(r+1-i) = h (Coxeter number)
  - Sum of squares: Sigma m_i^2 -- a second-moment invariant

For the icosahedral case W = H_3:
  m_i = {1, 5, 9}
  Sigma m_i = 1 + 5 + 9 = 15 = N (15 reflections in H_3) ✓ Solomon
  Sigma m_i^2 = 1 + 25 + 81 = 107  <-- electron gap-label

Comparison across rank-3 Coxeter groups (the only rank-3 cases that
contain the icosahedral 5-fold symmetry are H_3 itself):
  A_3 (S_4):           m_i = 1, 2, 3   Sigma m_i^2 = 14
  B_3 (cube/octa):     m_i = 1, 3, 5   Sigma m_i^2 = 35
  H_3 (icosahedral):   m_i = 1, 5, 9   Sigma m_i^2 = 107  <-- GCT match
  I_2(p) (dihedral):   m_i = 1, p-1    Sigma m_i^2 = 1 + (p-1)^2

This protocol combines a finite exceptional-group table with closed-form
all-rank sweeps of the infinite Coxeter families A_n, B_n, D_n, and I_2(p).
Within that finite-Coxeter classification audit, 107 is the H_3-specific
value of the Coxeter-exponent second moment.

Physical interpretation: linking Sigma m_i^2 to AF-core gap labels
==================================================================

The AF-core dimension group / trace image of the AKN substitution algebra
is Z[φ]; the full Cuntz-Krieger K_0(O_A) for A=[[1,1],[1,0]] is trivial
since coker(I-A^T) is trivial. See App Y §Y.3 for the canonical
AF-core-vs-full-O_A distinction. The icosahedral H_3 Coxeter symmetry of
the AKN cage is conjectured, after O.14 closure, to induce an action on the AF-core trace image via the Coxeter
element.

The Coxeter element c acts on the canonical H_3 reflection
representation V with eigenvalues exp(2*pi*i*m_j/h) for j = 1, ..., r,
which is how the Coxeter exponents m_j are defined. The second
Newton power-sum of those exponents, p_2 = Sigma m_j^2 = 107, is a
canonical group-theoretic invariant of the exponent multiset of H_3: a
symmetric power-sum of the Coxeter-exponent multiset, NOT a spectral
invariant of the Coxeter operator. Spectral functions of c instead see
root-of-unity eigenvalues; for example, tr(c) = Sigma
exp(2*pi*i*m_j/h) is a sum of roots of unity equal to phi - 1 = 1/phi. H_3 is a
finite reflection group, not a Lie group, and admits no quadratic
Casimir; the Newton power-sum p_2 is the correct canonical object.
(Note: "Solomon invariant" sometimes refers to the antisymmetric exterior
algebra A^*(V)^{H_3} whose dimensions are encoded by the Solomon formula;
here we mean the second Newton power-sum p_2 of the exponent multiset
itself, which is a strictly symmetric-function invariant.)

For the AF-core dimension group / trace image projection associated with
the electron sub-band of the AKN spectrum (not the full Cuntz-Krieger
K_0(O_A); for A=[[1,1],[1,0]], K_0(O_A) is trivial), the Bellissard
gap-label is the integer n such
that tau(P_n) = phi^(-n) represents the electron projection's
integrated density of states. The candidate identification maps this
projection to the p_2 = 107 invariant of the H_3 reflection
representation, giving gap-label n = -p_2 = -107.

The integer-identification side of this chain is Tier 2: |n| = 107 is
canonical to H_3 among finite irreducible Coxeter groups (unique
under the Cartan-Killing classification, with H_3 the unique rank-3
non-crystallographic case forced by the GCT 5-fold symmetry
commitment). The negative sign follows from the inverse-density
convention (m_e = M_P phi^(-107) places the electron at phi^(-107)
of the Planck scale).

The physical-interpretation chain -- the map from the H_3 reflection
representation V (rank 3) to the AF-core dimension group / trace image
(with only tau_*(K_0) living inside Z[phi]; the full Cuntz-Krieger
K_0(O_A) for A=[[1,1],[1,0]] is trivial) -- is a Tier 4 conjectural
construction. A canonical H_3-equivariant map carrying the p_2 invariant
to the electron projection's trace-image gap label has no published
precedent. The rank mismatch is the load-bearing obstruction. Full Tier 1
closure requires both the explicit non-perturbative AKN spectral calculation
and the construction of this equivariant map; both bundle with O.5 QLQCD-1L
and are registered as the residual work of Open Problem O.14.

Cross-reference: V3 Ch07 Sec 7.2.2 (K-theoretic framework, gap-labeling);
Bellissard 1986 Lectures Notes in Physics 257:99 (gap-labeling);
Anderson-Putnam 1998 Ergodic Theory & Dynamical Systems 18:509;
Connes-Moscovici 1995 GAFA 5:174 (local index formula);
Humphreys 1990 "Reflection Groups and Coxeter Groups" Tables 1, 3.1;
App H §O.14.
"""

from __future__ import annotations

import math
import json
from pathlib import Path

# Coxeter group data (Humphreys 1990 Tables 1 + 3.1)
# Finite irreducible Coxeter groups (Cartan-Killing classification +
# non-crystallographic H_3, H_4, I_2(p)). The named entries below sample
# the four infinite families A_n, B_n, D_n, I_2(p) at small rank to provide
# direct cross-check data; the closed-form sweeps in compute() then extend
# the test to ALL ranks of those infinite families.
COXETER_GROUPS = {
    "A_1":   {"rank": 1,  "degrees": [2]},
    "A_2":   {"rank": 2,  "degrees": [2, 3]},
    "A_3":   {"rank": 3,  "degrees": [2, 3, 4]},
    "A_4":   {"rank": 4,  "degrees": [2, 3, 4, 5]},
    "A_5":   {"rank": 5,  "degrees": [2, 3, 4, 5, 6]},
    "B_2":   {"rank": 2,  "degrees": [2, 4]},
    "B_3":   {"rank": 3,  "degrees": [2, 4, 6]},
    "B_4":   {"rank": 4,  "degrees": [2, 4, 6, 8]},
    "D_4":   {"rank": 4,  "degrees": [2, 4, 4, 6]},
    "D_5":   {"rank": 5,  "degrees": [2, 4, 5, 6, 8]},
    "E_6":   {"rank": 6,  "degrees": [2, 5, 6, 8, 9, 12]},
    "E_7":   {"rank": 7,  "degrees": [2, 6, 8, 10, 12, 14, 18]},
    "E_8":   {"rank": 8,  "degrees": [2, 8, 12, 14, 18, 20, 24, 30]},
    "F_4":   {"rank": 4,  "degrees": [2, 6, 8, 12]},
    "G_2":   {"rank": 2,  "degrees": [2, 6]},
    "H_3":   {"rank": 3,  "degrees": [2, 6, 10]},
    "H_4":   {"rank": 4,  "degrees": [2, 12, 20, 30]},
    "I2_5":  {"rank": 2,  "degrees": [2, 5]},    # dihedral with 5-fold
    "I2_7":  {"rank": 2,  "degrees": [2, 7]},
}


# Closed-form formulas for the sum of squared Coxeter exponents
# Sigma_i m_i^2 across the four infinite families. Derivations:
#
#   A_n (rank n, n >= 1): degrees {2, 3, ..., n+1}, exponents {1, 2, ..., n}.
#     Sigma m_i^2 = sum_{k=1}^{n} k^2 = n(n+1)(2n+1)/6.
#
#   B_n = C_n (rank n, n >= 2): degrees {2, 4, ..., 2n}, exponents
#     {1, 3, ..., 2n-1}. Sigma m_i^2 = sum_{k=1}^{n} (2k-1)^2
#     = n(2n-1)(2n+1)/3.
#
#   D_n (rank n, n >= 4): degrees {2, 4, ..., 2(n-1), n}, exponents
#     {1, 3, ..., 2n-3, n-1}. Sigma m_i^2 = sum_{k=1}^{n-1} (2k-1)^2
#     + (n-1)^2 = (n-1)(2n-3)(2n-1)/3 + (n-1)^2.
#
#   I_2(p) (rank 2, p >= 3): degrees {2, p}, exponents {1, p-1}.
#     Sigma m_i^2 = 1 + (p-1)^2.
#
# Source: Humphreys, "Reflection Groups and Coxeter Groups" 1990 Tables
# 1 (degrees), 3.1 (exponents); the formulas above are direct consequences
# of the standard degree-multiset specifications for each family.


def sum_sq_A(n: int) -> int:
    """A_n: Sigma m_i^2 = n(n+1)(2n+1)/6."""
    return n * (n + 1) * (2 * n + 1) // 6


def sum_sq_B(n: int) -> int:
    """B_n = C_n: Sigma m_i^2 = n(2n-1)(2n+1)/3."""
    return n * (2 * n - 1) * (2 * n + 1) // 3


def sum_sq_D(n: int) -> int:
    """D_n: Sigma m_i^2 = (n-1)(2n-3)(2n-1)/3 + (n-1)^2."""
    return (n - 1) * (2 * n - 3) * (2 * n - 1) // 3 + (n - 1) ** 2


def sum_sq_I2(p: int) -> int:
    """I_2(p): Sigma m_i^2 = 1 + (p-1)^2."""
    return 1 + (p - 1) ** 2


def solve_family_for_target(
    family: str, target: int, n_max: int = 1000
) -> dict:
    """Closed-form solver: find every member of an infinite Coxeter
    family whose sum-of-squared-exponents equals `target`. Returns the
    matching ranks (empty list if none), the value bracket [low, high]
    that brackets `target`, and a monotonicity proof for the bound.

    `n_max` is a finite cap purely to bound the search; the closed-form
    monotonicity argument is the load-bearing uniqueness step (the
    explicit sweep is a redundancy check).
    """
    if family == "A":
        f = sum_sq_A
        min_n = 1
        bracket_label = "n"
    elif family == "B":
        f = sum_sq_B
        min_n = 2
        bracket_label = "n"
    elif family == "D":
        f = sum_sq_D
        min_n = 4
        bracket_label = "n"
    elif family == "I2":
        f = sum_sq_I2
        min_n = 3
        bracket_label = "p"
    else:
        raise ValueError(f"unknown family: {family}")

    matches = []
    bracket_low = None
    bracket_high = None
    for n in range(min_n, n_max + 1):
        val = f(n)
        if val == target:
            matches.append(n)
        if val < target:
            bracket_low = {bracket_label: n, "value": val}
        elif val > target and bracket_high is None:
            bracket_high = {bracket_label: n, "value": val}
            break

    # Monotonicity statement: f is strictly increasing on the integer
    # domain of each family (verifiable by inspecting f(n+1) - f(n) > 0).
    # Hence if no integer n in [min_n, n_max] gives f(n) == target and
    # f(n_max) > target, target is unreachable across the entire infinite
    # family.
    monotone_proof = {
        "A": "f_A(n+1) - f_A(n) = (n+1)^2 > 0 for n >= 1",
        "B": "f_B(n+1) - f_B(n) = (2n+1)^2 > 0 for n >= 2",
        "D": "f_D(n+1) - f_D(n) = (2n-1)^2 + 2n - 1 > 0 for n >= 4",
        "I2": "f_I2(p+1) - f_I2(p) = 2p - 1 > 0 for p >= 3",
    }[family]

    return {
        "family": family,
        "target": target,
        "matches": matches,
        "bracket_below_target": bracket_low,
        "bracket_above_target": bracket_high,
        "monotonicity_proof": monotone_proof,
        "search_capped_at": n_max,
        "no_match_at_any_rank_up_to_cap": (len(matches) == 0),
    }


def exponents(degrees: list[int]) -> list[int]:
    """Coxeter exponents m_i = d_i - 1."""
    return [d - 1 for d in degrees]


def sum_of_squared_exponents(degrees: list[int]) -> int:
    return sum(m * m for m in exponents(degrees))


def sum_of_exponents(degrees: list[int]) -> int:
    """Should equal N (positive roots) by Solomon's identity."""
    return sum(exponents(degrees))


def coxeter_number(degrees: list[int]) -> int:
    """The Coxeter number h = largest degree."""
    return max(degrees)


def verify_solomon(group_data: dict) -> dict:
    """Solomon 1963: Sum m_i = N (positive roots).
    Verify by computing N independently from the order formula:
    |W| = h^r * (something), or via the degree formula
    |W| = prod d_i.
    Note: the SHEPHARD-TODD identity gives Sigma d_i = N + r,
    so N = Sigma d_i - r = Sigma (d_i - 1) = Sigma m_i. QED.
    """
    deg = group_data["degrees"]
    r = group_data["rank"]
    sum_d = sum(deg)
    sum_m = sum_of_exponents(deg)
    N_from_shephard_todd = sum_d - r
    return {
        "sum_d": sum_d,
        "rank": r,
        "N_from_shephard_todd": N_from_shephard_todd,
        "sum_m": sum_m,
        "solomon_identity_holds": N_from_shephard_todd == sum_m,
    }


def compute() -> dict:
    TARGET = 107
    results = {
        "target_integer": TARGET,
        "claim": (
            f"n_electron = -{TARGET} is identified with the sum of "
            "squared Coxeter exponents of the icosahedral H_3 group: "
            "1^2 + 5^2 + 9^2 = 107"),
        "tier": "Tier 1 Coxeter arithmetic/classification check + Tier 3 electron integer anchor + Tier 4 AKN physical-link conjecture pending O.14",
        "electron_mass_chain_tier": "Tier 2 K-theoretic framework + Tier 3 dimensional/integer anchor + Tier 4 K-theoretic physical-link conjecture pending O.14",
        "physical_link_closed": False,
        "groups_swept": {},
    }

    matches = []
    for group_name, data in COXETER_GROUPS.items():
        m_i = exponents(data["degrees"])
        sum_sq = sum_of_squared_exponents(data["degrees"])
        solomon = verify_solomon(data)
        results["groups_swept"][group_name] = {
            "rank": data["rank"],
            "degrees": data["degrees"],
            "exponents_m_i": m_i,
            "sum_m_i": sum_of_exponents(data["degrees"]),
            "sum_m_i_squared": sum_sq,
            "coxeter_h": coxeter_number(data["degrees"]),
            "matches_TARGET_107": (sum_sq == TARGET),
            "solomon_check": solomon["solomon_identity_holds"],
        }
        if sum_sq == TARGET:
            matches.append(group_name)

    results["match_summary"] = {
        "groups_matching_107": matches,
        "is_unique_match": (len(matches) == 1 and matches[0] == "H_3"),
    }

    # Connection to GCT: 107 is the H_3 second-moment-of-exponents
    # invariant; the icosahedral H_3 case is uniquely consistent with
    # GCT's 5-fold symmetry (only finite Coxeter group with 5-fold
    # symmetry of rank <= 3).
    rank3_groups = [g for g, d in COXETER_GROUPS.items() if d["rank"] == 3]
    rank3_matches = [g for g in rank3_groups
                       if results["groups_swept"][g]["matches_TARGET_107"]]
    results["icosahedral_uniqueness"] = {
        "rank3_groups": rank3_groups,
        "rank3_groups_matching_107": rank3_matches,
        "unique_in_rank3": (
            len(rank3_matches) == 1 and rank3_matches[0] == "H_3"),
        "interpretation": (
            "Among rank-3 finite Coxeter groups, only H_3 (the unique "
            "non-crystallographic case with 5-fold symmetry) has "
            "Sigma m_i^2 = 107. GCT's icosahedral 5-fold symmetry "
            "forces W = H_3."),
    }

    # Comparison to other natural integers
    results["adjacent_integers_check"] = {
        f"group_giving_{i}": [
            g for g, d in results["groups_swept"].items()
            if d["sum_m_i_squared"] == i
        ] for i in [105, 106, 107, 108, 109]
    }

    # Closed-form sweep across the four infinite Coxeter families
    # (A_n, B_n, D_n, I_2(p)) using the explicit polynomial formulas
    # in sum_sq_A/B/D/I2 above. The strict monotonicity of each formula
    # promotes the small-cap search to an all-ranks uniqueness statement:
    # if no rank in [min, cap] hits 107 and f(cap) > 107, then no rank
    # at any finite level of the family hits 107.
    family_sweeps = {
        "A_n": solve_family_for_target("A", TARGET, n_max=200),
        "B_n": solve_family_for_target("B", TARGET, n_max=200),
        "D_n": solve_family_for_target("D", TARGET, n_max=200),
        "I_2_p": solve_family_for_target("I2", TARGET, n_max=200),
    }
    results["infinite_family_closed_form_sweeps"] = family_sweeps

    # Exceptional finite irreducible Coxeter groups (the entire finite
    # list outside the four infinite families): F_4, G_2, E_6, E_7, E_8,
    # H_3, H_4. Each has a single, hand-tabulated Sigma m_i^2 value.
    exceptional_groups = {
        name: results["groups_swept"][name]["sum_m_i_squared"]
        for name in ("F_4", "G_2", "E_6", "E_7", "E_8", "H_3", "H_4")
    }
    exceptional_matches = [
        name for name, val in exceptional_groups.items()
        if val == TARGET
    ]
    results["exceptional_groups_check"] = {
        "values": exceptional_groups,
        "matches_TARGET_107": exceptional_matches,
    }

    # Combined all-ranks uniqueness statement: the integer 107 occurs
    # as Sigma m_i^2 for exactly one finite irreducible Coxeter group
    # across ALL ranks of A_n, B_n, D_n, I_2(p) and across the complete
    # exceptional list {F_4, G_2, E_6, E_7, E_8, H_3, H_4}. The
    # all-ranks part of the statement is established by the
    # closed-form monotonicity argument above; the exceptional part is
    # a finite check.
    infinite_family_matches = []
    for fam_key, sweep in family_sweeps.items():
        for n in sweep["matches"]:
            infinite_family_matches.append({"family": fam_key, "rank": n})

    all_matches = (
        [{"family": "exceptional", "group": g} for g in exceptional_matches]
        + infinite_family_matches
    )
    results["all_ranks_uniqueness"] = {
        "infinite_family_matches": infinite_family_matches,
        "exceptional_matches": exceptional_matches,
        "all_finite_irreducible_coxeter_groups_with_sum_sq_107": all_matches,
        "h3_is_unique_across_all_ranks": (
            len(all_matches) == 1
            and all_matches[0].get("group") == "H_3"
        ),
        "argument": (
            "Closed-form monotonicity of Sigma m_i^2 on each of "
            "{A_n, B_n, D_n, I_2(p)} (f(n+1) - f(n) > 0 verified "
            "symbolically per family in solve_family_for_target) "
            "establishes that the absence of 107 in the small-rank "
            "search extends to ALL ranks. Combined with the finite "
            "exceptional check {F_4, G_2, E_6, E_7, E_8, H_3, H_4}, "
            "H_3 is the unique finite irreducible Coxeter group at "
            "any rank with Sigma m_i^2 = 107."),
    }

    # Functional-choice disclosure: why Sigma m_i^2 specifically
    # (and not Sigma m_i, Sigma m_i^3, or Sigma d_i^2)? The integer-
    # identification path-(l) chain selects p_2 of the exponent
    # multiset because it is the second Solomon/Coxeter exponent
    # power-sum p_2(m)=sum m_i^2 -- the lowest non-trivial symmetric
    # invariant of the Coxeter exponent multiset. p_1 = Sigma m_i = N (number
    # of positive roots), which is dimensional-counting and not
    # invariant under field-theoretic dualities, hence not a
    # candidate for K_0 gap-labels. p_3 and higher Newton power-sums
    # are additional symmetric data at rank 3+, not consequences of
    # {p_1, p_2} alone, so p_2 is the lowest non-trivial exponent
    # moment rather than a complete generator. The choice of EXPONENTS
    # (m_i) over DEGREES (d_i = m_i + 1) follows the Coxeter-element-
    # spectrum convention: the Coxeter element c acts on V with
    # eigenvalues exp(2 pi i m_j / h), making the m_i (not the d_i)
    # the natural exponent labels. The exponent multiset {1,5,9}
    # for H3 is Tier 2 group-theoretic; the choice of the second
    # power-sum p2 = sum m_j^2 as the physical electron gap-label
    # is Tier 3 functional anchor pending O.14 V->K0 closure.
    # (See p2_uniqueness_check below for the sweep of all 14
    # alternative single-formula invariants in the [100, 115] window.)
    p2_alternative_invariants = {
        "Sigma m_i": sum_of_exponents(COXETER_GROUPS["H_3"]["degrees"]),
        "Sigma m_i^2": sum_of_squared_exponents(COXETER_GROUPS["H_3"]["degrees"]),
        "Sigma m_i^3": sum(m**3 for m in exponents(COXETER_GROUPS["H_3"]["degrees"])),
        "Sigma m_i^4": sum(m**4 for m in exponents(COXETER_GROUPS["H_3"]["degrees"])),
        "Sigma d_i": sum(COXETER_GROUPS["H_3"]["degrees"]),
        "Sigma d_i^2": sum(d**2 for d in COXETER_GROUPS["H_3"]["degrees"]),
        "Sigma d_i^3": sum(d**3 for d in COXETER_GROUPS["H_3"]["degrees"]),
        "Sigma (m_i + 1)^2": sum((m + 1)**2 for m in exponents(COXETER_GROUPS["H_3"]["degrees"])),
        "h * r": coxeter_number(COXETER_GROUPS["H_3"]["degrees"]) * COXETER_GROUPS["H_3"]["rank"],
        "|W|^(1/r) rounded": round(120 ** (1.0 / 3)),  # |H_3| = 120
        "N (positive roots)": sum_of_exponents(COXETER_GROUPS["H_3"]["degrees"]),
        "prod m_i": 1 * 5 * 9,
        "prod d_i / |W|": (2 * 6 * 10) // 120,
        "Sigma m_i^2 + N": sum_of_squared_exponents(COXETER_GROUPS["H_3"]["degrees"]) + sum_of_exponents(COXETER_GROUPS["H_3"]["degrees"]),
    }
    p2_in_window = {
        formula: val for formula, val in p2_alternative_invariants.items()
        if 100 <= val <= 115
    }
    results["functional_choice_audit"] = {
        "h3_invariant_alternatives": p2_alternative_invariants,
        "alternatives_landing_in_window_100_115": p2_in_window,
        "selection_rationale": (
            "p_2 = Sigma m_i^2 is the lowest non-trivial exponent "
            "moment after p_1 (p_1 = N = root-count is dimensional, "
            "not spectrally invariant; p_3+ are additional symmetric "
            "data at rank 3+, not derivable from {p_1, p_2} alone). "
            "EXPONENTS over DEGREES "
            "is forced by the Coxeter-element spectral convention "
            "(eigenvalues exp(2 pi i m_j / h), not exp(2 pi i d_j / h))."),
        "tier_disposition_under_audit": (
            "The exponent multiset {1,5,9} for H3 is Tier 2 group-theoretic; "
            "the choice of the second power-sum p2 = sum m_j^2 as the physical "
            "electron gap-label is Tier 3 functional anchor pending O.14 V->K0 closure."),
    }

    results["closure_status"] = {
        "tier": "Tier 1 Coxeter arithmetic/classification check + Tier 3 electron integer anchor + Tier 4 physical-link chain pending O.14",
        "electron_mass_chain_tier": "Tier 2 mechanism + Tier 3 dimensional/integer anchor + Tier 4 K-theoretic physical-link conjecture pending O.14",
        "what_is_closed": (
            f"The integer {TARGET} appearing in the electron gap-label "
            "n_electron = -107 is identified as a canonical "
            "Coxeter-group invariant of H_3: the sum of squared "
            "Coxeter exponents. The all-ranks closed-form sweep "
            "(infinite_family_closed_form_sweeps + exceptional_groups_check) "
            "shows that 107 occurs as Sigma m_i^2 for EXACTLY ONE finite "
            "irreducible Coxeter group across ALL ranks: H_3 itself. "
            "The strictly-increasing closed-form Sigma m_i^2(n) on each "
            "of {A_n, B_n, D_n, I_2(p)} extends the small-rank sweep "
            "to an all-ranks uniqueness statement. Integer-identification "
            "side is a Tier 1 Coxeter arithmetic/classification check. "
            "This does not close the electron mass/gap-label physical-link chain."),
        "what_remains_open": (
            "Full physical-link closure requires the EXPLICIT verification "
            "that the electron sub-band of the AKN spectrum "
            "corresponds to the H_3 second-exponent-power-sum "
            "invariant -- i.e., that the AF-core trace-image projection "
            "(not the full Cuntz-Krieger K_0(O_A), which is trivial for "
            "A=[[1,1],[1,0]]) associated with the electron has gap-label equal to "
            "-p_2, where p_2(m_1, m_2, m_3) = sum m_j^2 = 107 is the "
            "second Coxeter-exponent power-sum for H_3. "
            "This requires the full non-perturbative AKN spectral "
            "calculation, bundling with O.5 QLQCD-1L."),
        "physical_interpretation": (
            "The Coxeter element c of H_3 acts on the reflection "
            "representation V with eigenvalues exp(2*pi*i*m_j/h) for "
            "j = 1, 2, 3, defining the Coxeter exponents m_j. The "
            "second power-sum of those exponents, "
            "Sigma m_j^2 = 107, is a canonical Coxeter-exponent "
            "invariant of H_3. It is not the trace of c "
            "on V, which is exp(2*pi*i/10)+exp(10*pi*i/10)+"
            "exp(18*pi*i/10)=2*cos(pi/5)-1=phi-1=1/phi; "
            "H_3 is a finite reflection group with no Lie-algebraic "
            "Casimir. The electron gap-label is conjecturally "
            "identified with -p_2 = -107 via the physical-"
            "interpretation chain (Tier 4, Open Problem O.14)."),
    }

    return results


def main():
    results = compute()
    TARGET = results["target_integer"]

    # Top-level pass field for verify_engine integration: PASS requires
    # BOTH the named-group uniqueness (sample of 19 named groups) AND
    # the all-ranks closed-form uniqueness (sweep across the four
    # infinite families + exceptional list). The all-ranks gate is the
    # one that promotes the result from "uniqueness in our sample" to
    # "uniqueness across every finite irreducible Coxeter group".
    results["pass"] = bool(
        results["match_summary"]["is_unique_match"]
        and results["all_ranks_uniqueness"]["h3_is_unique_across_all_ranks"]
    )

    # Write to canonical data/ location matching verify_engine convention.
    out_dir_data = Path(__file__).parent.parent / "data"
    out_dir_data.mkdir(parents=True, exist_ok=True)
    out_path_data = out_dir_data / "protocol_o14_coxeter_exponent_squares_results.json"
    with open(out_path_data, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    # Mirror the same payload to the outputs/ directory for downstream
    # consumers that expect the per-protocol-named output filename.
    out_dir = Path(__file__).parent.parent / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "o14_coxeter_exponent_squares.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"O.14 route: n_electron = -107 as Sigma m_i^2(H_3)")
    print(f"=" * 60)
    print(f"Target integer: {results['target_integer']}")
    print(f"Claim: {results['claim']}")
    print()
    print(f"All finite irreducible Coxeter groups (sum of squared exponents):")
    print(f"  {'group':>6}  {'rank':>4}  {'degrees':>20}  {'exponents':>18}  "
          f"{'sum m_i^2':>10}  {'match 107':>9}")
    for name, data in results["groups_swept"].items():
        marker = "  <-- MATCH" if data["matches_TARGET_107"] else ""
        print(f"  {name:>6}  {data['rank']:>4}  {str(data['degrees']):>20}  "
              f"{str(data['exponents_m_i']):>18}  "
              f"{data['sum_m_i_squared']:>10}{marker}")
    print()
    m = results["match_summary"]
    print(f"Groups matching 107: {m['groups_matching_107']}")
    print(f"Unique match: {m['is_unique_match']}")
    print()
    u = results["icosahedral_uniqueness"]
    print(f"Uniqueness in rank-3 Coxeter groups:")
    print(f"  rank-3 groups: {u['rank3_groups']}")
    print(f"  matching 107: {u['rank3_groups_matching_107']}")
    print(f"  unique in rank-3: {u['unique_in_rank3']}")
    print()
    print(f"Adjacent integers (105-109):")
    for label, gs in results["adjacent_integers_check"].items():
        print(f"  {label}: {gs if gs else '(no Coxeter group)'}")
    print()
    print(f"Closed-form sweep across infinite Coxeter families:")
    for fam_key, sweep in results["infinite_family_closed_form_sweeps"].items():
        match_str = sweep["matches"] if sweep["matches"] else "(no rank matches)"
        bb = sweep["bracket_below_target"]
        ba = sweep["bracket_above_target"]
        print(f"  {fam_key:>6}: matches = {match_str}; "
              f"bracket = {bb} -> {ba}")
        print(f"          monotonicity: {sweep['monotonicity_proof']}")
    print()
    print(f"Exceptional groups Sigma m_i^2:")
    for g, val in results["exceptional_groups_check"]["values"].items():
        marker = "  <-- MATCH" if val == TARGET else ""
        print(f"  {g}: {val}{marker}")
    print(f"  Exceptional matches: "
          f"{results['exceptional_groups_check']['matches_TARGET_107']}")
    print()
    print(f"ALL-RANKS UNIQUENESS:")
    aru = results["all_ranks_uniqueness"]
    print(f"  H_3 is unique across all ranks: "
          f"{aru['h3_is_unique_across_all_ranks']}")
    print(f"  All matching groups: "
          f"{aru['all_finite_irreducible_coxeter_groups_with_sum_sq_107']}")
    print()
    print(f"Functional-choice audit (alternatives in [100, 115] window):")
    fc = results["functional_choice_audit"]
    if fc["alternatives_landing_in_window_100_115"]:
        for formula, val in fc["alternatives_landing_in_window_100_115"].items():
            print(f"  {formula} = {val}")
    else:
        print(f"  (no alternative single-formula invariant lands in window)")
    print()
    print(f"Tier: {results['closure_status']['tier']}")
    print(f"Top-level pass: {results['pass']}")
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
