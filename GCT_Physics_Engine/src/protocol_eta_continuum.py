#!/usr/bin/env python3
"""
protocol_eta_continuum.py — Finite-Orbit Fixed-Point Ansatz Diagnostic
========================================================================

Evaluates a finite sum over nine binary-icosahedral conjugacy
classes for trial integers n in {-3,...,3}.  The numerical kernel is used
as a reproducible ansatz diagnostic only.

This script does not specify an elliptic self-adjoint boundary operator, its
Hilbert-space domain, boundary conditions, kernel, spectrum, or regularised
eta function.  Consequently it does not evaluate a raw eta-invariant, an APS
reduced invariant, a relative rho-invariant, or a Connes–Moscovici local-index
pairing.  Fixed-point formulas for equivariant indices cannot be relabelled as
raw eta evaluations without the missing operator-theoretic construction.

The three reported normalisations are alternative finite-orbit sums, not
conventions for one established invariant.  Their values must not be compared
to scalar-adjacency/8 as independent analytic confirmation.  Output is written
to data/protocol_eta_continuum_results.json with explicit object/domain status.
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
#          so the diagnostic kernel is zero in the no-rotation branch.
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
# FINITE-ORBIT FIXED-POINT ANSATZ (NOT AN ETA-INVARIANT)
# ════════════════════════════════════════════════════════════════════════════
# The kernel below resembles a fixed-point contribution and is
# summed over the declared finite class table.  No theorem identifies this
# finite sum with a raw eta-invariant for a specified boundary operator.

def fixed_point_kernel_value(theta: float, n: int) -> float:
    """Trigonometric kernel used by the finite-orbit ansatz."""
    if abs(math.sin(theta / 2.0)) < 1e-12:
        return 0.0
    numer = math.sin((n + 0.5) * theta)
    denom = 2.0 * (math.sin(theta / 2.0) ** 2)
    return numer / denom


def finite_orbit_average(n: int) -> float:
    """First normalisation of the finite-orbit ansatz."""
    total = 0.0
    G = 120
    # The "e" and "-e" classes have no fixed-point rotation on S² and
    # contribute trivially. For "-e" (central spinor flip), the spinor
    # sign multiplies but no rotation, so the diagnostic kernel vanishes.
    for c in CLASSES:
        if c["theta"] == 0.0:
            continue
        # Two trial fixed-point contributions per rotation.
        local_north = fixed_point_kernel_value(c["theta"], n)
        local_south = fixed_point_kernel_value(c["theta"], n)
        # The south pole has the supplementary angle; for our averaging we
        # take the same θ since both poles are equivalent under inversion.
        local_pair = local_north + local_south
        weighted = c["size"] * c["spinor_sign"] * local_pair / 2.0
        # Divide local_pair by 2 because Atiyah–Bott sums BOTH poles; the
        # /2 normalises to per-element. Different convention chains use
        # /1; we report both.
        total += weighted
    return total / G


def finite_orbit_sum_over_group(n: int) -> float:
    """Second normalisation of the same finite-orbit ansatz."""
    total = 0.0
    G = 120
    for c in CLASSES:
        if c["theta"] == 0.0:
            continue
        local_north = fixed_point_kernel_value(c["theta"], n)
        local_pair = 2.0 * local_north  # both fixed points equal contribution
        weighted = c["size"] * c["spinor_sign"] * local_pair
        total += weighted
    return total / G


def finite_orbit_sum_over_rotation_subgroup(n: int) -> float:
    """Third normalisation of the same finite-orbit ansatz."""
    total = 0.0
    for c in CLASSES:
        if c["theta"] == 0.0:
            continue
        local = fixed_point_kernel_value(c["theta"], n)
        weighted = c["size"] * c["spinor_sign"] * local
        total += weighted
    return total / 60.0  # |I| = 60 (proper rotation subgroup)


# ════════════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════════════

def main() -> dict:
    print("=" * 80)
    print("  Finite-Orbit Fixed-Point Ansatz Diagnostic on the 2I class table")
    print("=" * 80)
    print(f"  Binary icosahedral group: |2I| = 120, |I| = 60, 9 conjugacy classes")
    print()
    print("  Conjugacy classes (rotation angle θ, class size, spinor sign):")
    for c in CLASSES:
        print(f"    {c['name']:<8}  size={c['size']:<3}  θ={c['theta']:.4f}  ε={c['spinor_sign']:+d}")
    print()
    print("  Trial integer n → finite-orbit values under three normalisations:")
    print(f"    {'n':>3}  {'norm-A (avg /2)':>20}  {'norm-B (sum/G)':>18}  {'norm-C (over |I|)':>20}")
    rows = []
    for n in range(-3, 4):
        a = finite_orbit_average(n)
        b = finite_orbit_sum_over_group(n)
        c = finite_orbit_sum_over_rotation_subgroup(n)
        rows.append({"n": n, "normalisation_A_avg": a, "normalisation_B_group": b, "normalisation_C_rotation_subgroup": c})
        print(f"    {n:>3}  {a:>20.6f}  {b:>18.6f}  {c:>20.6f}")

    # Report the numerical comparison as a diagnostic only.
    print()
    print("  Numerical coincidences with the selected-cage scalar/8 diagnostic -1 (±0.05):")
    matches = []
    for r in rows:
        for label, val in (("normalisation-A", r["normalisation_A_avg"]),
                           ("normalisation-B", r["normalisation_B_group"]),
                           ("normalisation-C", r["normalisation_C_rotation_subgroup"])):
            if abs(val + 1.0) < 0.05:
                matches.append({"n": r["n"], "normalisation": label, "finite_orbit_value": val})
                print(f"    n={r['n']:+d}  {label}  value = {val:.6f}")
    if not matches:
        print("    (no match within tolerance; the conventions surveyed do not")
        print("    cleanly land on -1. This has no APS significance: neither")
        print("    the finite-orbit sum nor the cage scalar/8 diagnostic is an")
        print("    eta-invariant of a specified qualifying boundary operator.)")

    print()
    print("=" * 80)

    results = {
        "schema_version": "0.2",
        "group": "2I = SL(2,5)",
        "declared_orbit_space": "finite 2I conjugacy-class table with trial S² rotation angles",
        "classes": [
            {"name": c["name"], "size": c["size"], "order": c["order"],
             "theta": c["theta"], "spinor_sign": c["spinor_sign"]}
            for c in CLASSES
        ],
        "finite_orbit_diagnostic_table": rows,
        "numerical_coincidences_with_selected_cage_scalar_over_8": matches,
        "qualifying_boundary_operator_specified": False,
        "operator_domain_specified": False,
        "spectrum_computed": False,
        "regularised_eta_function_computed": False,
        "aps_eta_evaluated": False,
        "aps_reduced_invariant_evaluated": False,
        "relative_rho_evaluated": False,
        "connes_moscovici_pairing_evaluated": False,
        "topological_invariance_claimed": False,
        "pass": False,
        "scope_disposition": (
            "Finite-orbit fixed-point ansatz only. No elliptic self-adjoint "
            "boundary operator, Hilbert-space domain, boundary conditions, "
            "kernel, spectrum, or regularised eta function is specified. "
            "The values are not raw eta, APS xi, relative rho, or a "
            "Connes–Moscovici pairing, and do not independently confirm any "
            "finite-cage graph diagnostic."
        ),
    }
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DATA_PATH.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"  Results written to {DATA_PATH}")

    return results


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
