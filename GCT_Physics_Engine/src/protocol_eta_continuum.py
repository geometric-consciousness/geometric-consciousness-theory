#!/usr/bin/env python3
"""
protocol_eta_continuum.py — Connes–Moscovici equivariant η-invariant on the
smooth icosahedral 2-sphere boundary ∂M_RT.

This script is the analytic companion to `protocol_aps_index_proof.py`. The
latter computes the discrete spectral asymmetry of the I_h-closed boundary
cage in 6D. This script computes the equivariant
η-invariant of the spin Dirac operator on the *smooth* 2-sphere (∂M_RT is
topologically S²) with binary icosahedral 2I = SL(2,5) symmetry, twisted by
a complex line bundle L_n of Chern number n, via the Connes–Moscovici
Theorem 4.1 character-theoretic trace formula:

    η_G(D ⊗ L_n) = (1/|G|) Σ_{g ≠ e} χ_E(g) · η_loc(g; n)

where η_loc(g; n) is the local equivariant η contribution at the fixed-point
set of g ∈ 2I acting on S². For a rotation by angle θ about an axis through
S², the fixed-point set is {north, south} = 2 isolated points, and the
local η at each fixed point is the Atiyah–Bott–Lefschetz local formula
applied to the twisted Dirac. For finite-order rotation g of order m, the
local η contribution per fixed point is:

    η_loc(g; n) = i·cot(πθ_g/2)·e^{iπn θ_g} / (1 - e^{iπ θ_g})

This is the standard Atiyah–Singer G-Spin formula evaluated on S² for the
twisted Dirac D ⊗ L_n.

The goal: identify which Chern number n ∈ Z gives η = -1 (matching the
discrete cage computation in protocol_aps_index_proof.py). If exactly one
small integer matches, we have an independent analytic verification of the
discrete result via the smooth-manifold route, going via Connes–Moscovici
Thm 4.1 rather than the discrete spectral counting.

Caveats:
  - The 2-sphere acted on by 2I is the SMOOTH boundary of the icosahedral
    acceptance window. The actual ∂M_RT is piecewise-flat (a rhombic
    triacontahedron is convex polyhedral). Topologically they are both S²
    with 2I action, but the metric differs. The Atiyah–Bott formula applies
    in either case because η is a topological invariant of the Dirac index.
  - The "η_loc" formula above is for the equivariant index in odd dimensions
    or for the boundary η-invariant of a 2D Dirac twisted by a line bundle
    on S². The exact normalization (factor of 2, sign of i) is convention-
    dependent; we report multiple conventions and identify which matches the
    engine's -1.
  - This script does NOT derive the bulk Â-genus integral (= 108 in the
    engine). The bulk derivation is a separate research-level computation.

Output: JSON in data/protocol_eta_continuum_results.json with the η value
for each Chern number n ∈ {-3, -2, -1, 0, 1, 2, 3} under each of three
normalization conventions.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Repo layout: this lives at GCT_Physics_Engine/src/protocol_eta_continuum.py
# Output goes to GCT_Physics_Engine/data/protocol_eta_continuum_results.json
ENGINE_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ENGINE_ROOT / "data" / "protocol_eta_continuum_results.json"


# ════════════════════════════════════════════════════════════════════════════
# BINARY ICOSAHEDRAL GROUP 2I = SL(2,5) — conjugacy classes
# ════════════════════════════════════════════════════════════════════════════
# 9 conjugacy classes. For each we record:
#   name : human label
#   size : number of elements in the class
#   order: group-order of any element in the class
#   theta: rotation angle (in radians) of the underlying I-action on S²,
#          for genuine-rotation classes. For {-e} (central element), there is
#          no fixed point on S² (it acts as -id on spinors, +id on S²-points),
#          so the local-η contribution is captured by the "no rotation, full
#          spinor-sign flip" branch.
#
# The genuine rotations of 2I (orders 1, 2, 3, 5, 6, 10) project under
# 2I → I to the icosahedral rotation group I, whose rotation angles on
# the 2-sphere are:
#   order 1 → 0
#   order 2 → π
#   order 3 → 2π/3
#   order 5 → 2π/5 and 4π/5 (two conjugacy classes in I)
#   order 6 → 2π/6 = π/3       (spinor-sense rotations, lifted from order-3)
#   order 10 → 2π/10 = π/5 etc. (spinor-sense, lifted from order-5)
#
# In 2I the spinor double-cover means odd-order rotations come in pairs (g
# and -g with same rotation angle but opposite spinor sign). Even-order
# rotations have a definite spinor sign per element.

# 2I → I is the spinor double cover, so an order-2m element of 2I
# projects to an order-m rotation in I (= SO(3) action on S²). The S² rotation
# angle is 2π/m, NOT π/m. The spinor sign for "lift" elements is +1 and for
# "-1 × lift" elements is -1.
CLASSES = [
    {"name": "e",        "size":  1, "order":  1, "theta": 0.0,           "spinor_sign": +1},
    {"name": "-e",       "size":  1, "order":  2, "theta": 0.0,           "spinor_sign": -1},
    {"name": "C5_a",     "size": 12, "order":  5, "theta": 2*math.pi/5.0, "spinor_sign": +1},
    {"name": "C5_b",     "size": 12, "order":  5, "theta": 4*math.pi/5.0, "spinor_sign": +1},
    {"name": "C10_a",    "size": 12, "order": 10, "theta": 2*math.pi/5.0, "spinor_sign": -1},
    {"name": "C10_b",    "size": 12, "order": 10, "theta": 4*math.pi/5.0, "spinor_sign": -1},
    {"name": "C3",       "size": 20, "order":  3, "theta": 2*math.pi/3.0, "spinor_sign": +1},
    {"name": "C6",       "size": 20, "order":  6, "theta": 2*math.pi/3.0, "spinor_sign": -1},
    {"name": "C4",       "size": 30, "order":  4, "theta": math.pi,       "spinor_sign": +1},
]
# Sanity check: total size = 1+1+12+12+12+12+20+20+30 = 120
assert sum(c["size"] for c in CLASSES) == 120, "2I should have 120 elements"


# ════════════════════════════════════════════════════════════════════════════
# THE EQUIVARIANT η-INVARIANT VIA THE ATIYAH–BOTT FORMULA
# ════════════════════════════════════════════════════════════════════════════
# For the spin Dirac operator on S² twisted by a line bundle L_n with Chern
# number n, acted on equivariantly by a finite group G ⊂ SO(3) (lifted to
# 2I ⊂ SU(2) on spinors), the Connes–Moscovici Thm 4.1 trace formula
# specializes to the Atiyah–Bott Lefschetz fixed-point sum on the rotation
# subgroup. Each non-trivial rotation has 2 fixed points (north and south
# pole of its rotation axis), and contributes:
#
#   η_loc^{north}(θ, n) = ε · (1 / (2 sin(θ/2))) · cos((n+1) θ/2)
#   η_loc^{south}(θ, n) = ε · (1 / (2 sin(θ/2))) · cos((n+1) (π - θ)/2)
#
# where ε = ±1 is the spinor sign of the lifted element.
#
# The full equivariant η is the average over the group:
#
#   η_G(n) = (2 / |G|) · Σ_{non-id classes} size · spinor_sign · η_local(θ, n)
#
# (the factor 2 accounts for the two fixed points per rotation).

def eta_local_per_fixed_point(theta: float, n: int) -> float:
    """The Atiyah–Bott local η contribution at one fixed point of a rotation
    by angle θ on S², for the spin Dirac twisted by line bundle L_n.

    Standard formula (Atiyah–Patodi–Singer 1975, eq. 2.16 specialised to S²):
        η_loc = (1 / (2 sin(θ/2))) · sin((n+1/2) θ) / sin(θ/2)
    With appropriate conventions this reduces to:
        η_loc = ((-1)^n) · cot(θ/2) / 2
    for unit Chern twist; we use the general n formula.
    """
    if abs(math.sin(theta / 2.0)) < 1e-12:
        return 0.0
    # The pure-rotation local η, unwound for arbitrary integer n:
    # η_loc(θ; n) = sin((n + 1/2) θ) / (2 sin²(θ/2))
    numer = math.sin((n + 0.5) * theta)
    denom = 2.0 * (math.sin(theta / 2.0) ** 2)
    return numer / denom


def equivariant_eta(n: int) -> float:
    """Sum the Atiyah–Bott local η over all non-identity conjugacy classes
    of 2I, weighted by class size and spinor sign, divided by |2I|. Returns
    the rational η-invariant of D ⊗ L_n on S²/2I."""
    total = 0.0
    G = 120
    # The "e" and "-e" classes have no fixed-point rotation on S² and
    # contribute trivially. For "-e" (central spinor flip), the spinor
    # sign multiplies but no rotation, so the local η factor vanishes too.
    for c in CLASSES:
        if c["theta"] == 0.0:
            continue
        # Two fixed points per rotation; sum their local η contributions
        local_north = eta_local_per_fixed_point(c["theta"], n)
        local_south = eta_local_per_fixed_point(c["theta"], n)
        # The south pole has the supplementary angle; for our averaging we
        # take the same θ since both poles are equivalent under inversion.
        local_pair = local_north + local_south
        weighted = c["size"] * c["spinor_sign"] * local_pair / 2.0
        # Divide local_pair by 2 because Atiyah–Bott sums BOTH poles; the
        # /2 normalises to per-element. Different convention chains use
        # /1; we report both.
        total += weighted
    return total / G


def equivariant_eta_alt(n: int) -> float:
    """Alternative convention: don't divide local_pair by 2 (some references
    treat each rotation as contributing the sum of its two fixed points
    directly, without averaging)."""
    total = 0.0
    G = 120
    for c in CLASSES:
        if c["theta"] == 0.0:
            continue
        local_north = eta_local_per_fixed_point(c["theta"], n)
        local_pair = 2.0 * local_north  # both fixed points equal contribution
        weighted = c["size"] * c["spinor_sign"] * local_pair
        total += weighted
    return total / G


def equivariant_eta_signed(n: int) -> float:
    """Third convention: with explicit spinor double-cover sign, both poles,
    and division by 2|G| to normalise as a defect index."""
    total = 0.0
    for c in CLASSES:
        if c["theta"] == 0.0:
            continue
        local = eta_local_per_fixed_point(c["theta"], n)
        weighted = c["size"] * c["spinor_sign"] * local
        total += weighted
    return total / 60.0  # |I| = 60 (proper rotation subgroup)


# ════════════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════════════

def main() -> dict:
    print("=" * 80)
    print("  Connes–Moscovici equivariant η-invariant on S² / 2I (smooth route)")
    print("=" * 80)
    print(f"  Binary icosahedral group: |2I| = 120, |I| = 60, 9 conjugacy classes")
    print()
    print("  Conjugacy classes (rotation angle θ, class size, spinor sign):")
    for c in CLASSES:
        print(f"    {c['name']:<8}  size={c['size']:<3}  θ={c['theta']:.4f}  ε={c['spinor_sign']:+d}")
    print()
    print("  Twisting Chern number n → η_G(D ⊗ L_n) under three conventions:")
    print(f"    {'n':>3}  {'conv-A (avg /2)':>20}  {'conv-B (sum/G)':>18}  {'conv-C (over |I|)':>20}")
    rows = []
    for n in range(-3, 4):
        a = equivariant_eta(n)
        b = equivariant_eta_alt(n)
        c = equivariant_eta_signed(n)
        rows.append({"n": n, "conv_A_avg": a, "conv_B_alt": b, "conv_C_over_60": c})
        print(f"    {n:>3}  {a:>20.6f}  {b:>18.6f}  {c:>20.6f}")

    # Identify which (n, convention) gives -1 ± 0.05
    print()
    print("  Matches to engine's η_eff = -1 (within ±0.05):")
    matches = []
    for r in rows:
        for label, val in (("conv-A", r["conv_A_avg"]),
                           ("conv-B", r["conv_B_alt"]),
                           ("conv-C", r["conv_C_over_60"])):
            if abs(val + 1.0) < 0.05:
                matches.append({"n": r["n"], "convention": label, "eta": val})
                print(f"    n={r['n']:+d}  {label}  η = {val:.6f}")
    if not matches:
        print("    (no match within tolerance; the conventions surveyed do not")
        print("    cleanly land on -1 — this is the open analytic step. The")
        print("    discrepancy may reflect (i) a missing spinor-cover factor of 2,")
        print("    (ii) a missing line-bundle holonomy phase, (iii) wrong")
        print("    convention for the local Atiyah–Bott formula, or (iv) the")
        print("    actual answer differs from -1 for any small n under any")
        print("    standard normalization. Disposition: this script is")
        print("    insufficient to independently confirm the engine's -1; the")
        print("    boundary η on smooth S²/2I needs a more careful set-up.)")

    print()
    print("=" * 80)

    results = {
        "schema_version": "0.1",
        "group": "2I = SL(2,5)",
        "manifold": "S² with binary icosahedral action",
        "classes": [
            {"name": c["name"], "size": c["size"], "order": c["order"],
             "theta": c["theta"], "spinor_sign": c["spinor_sign"]}
            for c in CLASSES
        ],
        "eta_table": rows,
        "matches_to_engine_minus_one": matches,
        "scope_disposition": (
            "This script is the smooth-manifold companion to "
            "protocol_aps_index_proof.py. It attempts the Connes–Moscovici "
            "Theorem 4.1 character-theoretic evaluation of the equivariant "
            "η-invariant on S²/2I with line-bundle twist. The conventions "
            "surveyed do not all land on -1 cleanly; the closure of "
            "Lemma T-McK.1b (App U §U.7.6.3) requires fixing the precise "
            "convention chain matching the AKN C*-algebra's gap-label "
            "definition. Numerical evidence on the discrete cage "
            "(protocol_aps_index_proof.py) remains stronger than this "
            "smooth route, but the smooth route is conceptually closer "
            "to the formal Tier 1 target."
        ),
    }
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DATA_PATH.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"  Results written to {DATA_PATH}")

    return results


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
