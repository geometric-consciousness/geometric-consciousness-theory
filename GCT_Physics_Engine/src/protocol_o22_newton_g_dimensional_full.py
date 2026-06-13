#!/usr/bin/env python3
"""
protocol_o22_newton_g_dimensional_full.py
==========================================

Full dimensional analysis of the three-route Newton-G claim (App K §K.7).
Open Problem O.22 is carried with the invariant disposition: Routes 2/3
with a single power of a_6 are dimensionally inconsistent as SI expressions;
the dimensionally corrected a_6^2 scaling differs from Route 1 by
phi^(-18)/(32*pi). Route 1 remains the numerical anchor.

ROUTE 1 (Jacobson, dimensionally clean)

    G_1 = c^3 a_6^2 / (4 hbar)
    [G_1] = L^3 T^(-3) * L^2 / (M L^2 T^(-1)) = L^3 M^(-1) T^(-2)  ✓

    Closes to G = hbar c / M_P^2 via a_6 = 2 hbar / (M_P c).

ROUTE 2 SINGLE-a_6 FORM (App K §K.7, equation 8.1.4)

    G_2 = c_hat^4 / (8 pi K_perp a_6)
    [c_hat]^4 = L^4 T^(-4)
    [K_perp]  = energy density = M L^(-1) T^(-2)
    [a_6]     = L
    [G_2]     = L^4 T^(-4) / (M L^(-1) T^(-2) * L)
              = L^4 T^(-4) / (M T^(-2))
              = L^4 M^(-1) T^(-2)   ✗  (one extra factor of L)

  The single-a_6 Route 2 expression is dimensionally INCONSISTENT with Newton's G.

DIMENSIONALLY-CORRECTED ROUTE 2

The minimal correction to restore correct dimensions is to replace
a_6 with a_6^2 in the denominator:

    G_2_corrected = c_hat^4 / (8 pi K_perp a_6^2)
    [G_2_corrected] = L^4 T^(-4) / (M L^(-1) T^(-2) * L^2)
                    = L^4 T^(-4) / (M L T^(-2))
                    = L^3 M^(-1) T^(-2)   ✓

  Numerically with GCT inputs (c_hat = phi^(-9) c, K_perp = phi^(-18) E_P/ell_P^3,
  a_6 = 2 ell_P):

    G_2_corrected = (phi^(-9) c)^4 / (8 pi * phi^(-18) E_P/ell_P^3 * (2 ell_P)^2)
                  = phi^(-36) c^4 ell_P^3 / (32 pi phi^(-18) E_P ell_P^2)
                  = phi^(-18) c^2 ell_P / (32 pi M_P)

  Using ell_P = hbar / (M_P c):
                  = phi^(-18) hbar c / (32 pi M_P^2)
                  = [phi^(-18) / (32 pi)] * G

  So G_2_corrected = phi^(-18)/(32 pi) * G ≈ 1.7e-6 * G  (off by 6 OOM)

CONCLUSION

  Route 1 closes cleanly to G = hbar c / M_P^2.

  Routes 2/3 with a_6 to the first power are dimensionally
  inconsistent and CANNOT equal G in any unit system.

  Routes 2/3 dimensionally-corrected (with a_6^2) give a result that
  differs from G by phi^(-18)/(32 pi) ~ 1.7e-6, a finite-but-substantial
  factor (~6 OOM smaller than G).

  The framework does not currently absorb the phi^(-18)/(32 pi) factor
  via any natural GCT-internal substitution. Routes 2/3 should be
  interpreted as STRUCTURAL CROSS-CHECKS (the form G ~ c_hat^4/(K_perp L^2)
  has the right dimensional scaling) but NOT as standalone SI-unit G
  formulas. The 2274 ppm CODATA agreement of G derives from Route 1
  alone.

CLOSURE STATUS

  This is a full closure of O.22 in the direction:

    "Routes 2/3 reduce to Route 1 only as structural scaling checks"

  The invariant statement is: not in SI units with the single-a_6 expression;
  only as a STRUCTURAL identification at the natural-units / order-of-
  magnitude scaling level. App K §K.7 carries the same disposition:
  dimensional inconsistency of the single-a_6 Route 2 expression, corrected
  a_6^2 form, unabsorbed phi^(-18)/(32*pi) residual, and restriction of
  "three-route equivalence" to structural scaling rather than numerical
  SI-unit identity.
"""

import json
import math
from pathlib import Path

try:
    from gct_utils import get_output_path, C
    OUTPUT_DIR_AVAILABLE = True
except ImportError:
    OUTPUT_DIR_AVAILABLE = False

PHI = float(C.PHI)
C_LIGHT = 2.99792458e8
HBAR = 1.054571817e-34
G_NEWTON = 6.67430e-11

M_P = math.sqrt(HBAR * C_LIGHT / G_NEWTON)
ELL_P = math.sqrt(HBAR * G_NEWTON / C_LIGHT ** 3)
E_P = M_P * C_LIGHT ** 2
A_6 = 2.0 * HBAR / (M_P * C_LIGHT)  # = 2 ell_P


def route_1_G():
    """G_1 = c^3 a_6^2 / (4 hbar) -- dimensionally clean."""
    return C_LIGHT ** 3 * A_6 ** 2 / (4.0 * HBAR)


def route_2_single_a6():
    """G_2 = c_hat^4 / (8 pi K_perp a_6) -- dimensionally inconsistent.
    Returns the numerical value treating it as if dimensionally correct."""
    c_hat = PHI ** (-9) * C_LIGHT
    K_perp = (E_P / ELL_P ** 3) * PHI ** (-18)
    return c_hat ** 4 / (8.0 * math.pi * K_perp * A_6)


def route_2_corrected():
    """G_2 = c_hat^4 / (8 pi K_perp a_6^2) -- dimensionally corrected."""
    c_hat = PHI ** (-9) * C_LIGHT
    K_perp = (E_P / ELL_P ** 3) * PHI ** (-18)
    return c_hat ** 4 / (8.0 * math.pi * K_perp * A_6 ** 2)


def expected_residual_factor():
    """Expected ratio G_2_corrected / G_1 = phi^(-18) / (32 pi)."""
    return PHI ** (-18) / (32.0 * math.pi)


def main():
    print("=" * 76)
    print("O.22 FULL: Three-route Newton-G dimensional analysis")
    print("=" * 76)

    g_1 = route_1_G()
    g_2_single_a6 = route_2_single_a6()
    g_2_corr = route_2_corrected()
    expected_ratio = expected_residual_factor()

    print(f"\nDimensional analysis:")
    print(f"  Route 1: G_1 = c^3 a_6^2 / (4 hbar)")
    print(f"    Dimensions: L^3 M^(-1) T^(-2)  -- CORRECT")
    print(f"  Route 2 (single-a_6 form): G_2 = c_hat^4 / (8 pi K_perp a_6)")
    print(f"    Dimensions: L^4 M^(-1) T^(-2)  -- INCONSISTENT (extra L)")
    print(f"  Route 2 (a_6^2 form): G_2 = c_hat^4 / (8 pi K_perp a_6^2)")
    print(f"    Dimensions: L^3 M^(-1) T^(-2)  -- CORRECT")

    print(f"\nNumerical evaluations (SI units):")
    print(f"  G (CODATA)              : {G_NEWTON:.6e}")
    print(f"  G_1 (Route 1)           : {g_1:.6e}")
    print(f"  G_1 / G_CODATA          : {g_1 / G_NEWTON:.6f}")
    print(f"  G_2 (Route 2 single-a_6): {g_2_single_a6:.6e}  [DIMENSIONALLY INVALID]")
    print(f"  G_2 (Route 2 corrected) : {g_2_corr:.6e}")
    print(f"  G_2_corr / G_1          : {g_2_corr / g_1:.6e}")

    print(f"\nExpected residual (theory):")
    print(f"  phi^(-18) / (32 pi)     : {expected_ratio:.6e}")
    print(f"  Match with computed     : {math.isclose(g_2_corr / g_1, expected_ratio, rel_tol=1e-6)}")

    print(f"\n" + "=" * 76)
    print("VERDICT FOR O.22 (full closure direction)")
    print("=" * 76)
    print(f"  Route 2 with a single a_6 factor is dimensionally inconsistent (extra L factor).")
    print(f"  The minimal correction (a_6 -> a_6^2) restores dimensional consistency")
    print(f"  but gives G_2_corrected = [phi^(-18)/(32 pi)] * G_1 = {expected_ratio:.2e} * G_1,")
    print(f"  differing from Route 1 by ~6 orders of magnitude.")
    print(f"")
    print(f"  FULL O.22 CLOSURE (closure direction (b) from App H):")
    print(f"  Routes 2/3 reduce to Route 1 ONLY at the natural-units / order-")
    print(f"  of-magnitude scaling level. They are STRUCTURAL cross-checks that")
    print(f"  the form G ~ c_hat^4/(K_perp L^2) has the right dimensional scaling,")
    print(f"  NOT standalone SI-unit G formulas. The framework does NOT absorb")
    print(f"  the phi^(-18)/(32 pi) residual; this is a documented limitation of")
    print(f"  Routes 2/3, not a hidden equivalence.")
    print(f"")
    print(f"  The 2274 ppm CODATA agreement of G derives from Route 1 alone")
    print(f"  (which closes cleanly via the standard Planck identity); this is")
    print(f"  unaffected by the Routes 2/3 dimensional analysis.")
    print(f"")
    print(f"  App K §K.7 carries the same invariant disposition:")
    print(f"    (a) single-a_6 Route 2 is dimensionally inconsistent")
    print(f"    (b) the corrected a_6^2 form is dimensionally valid")
    print(f"    (c) phi^(-18)/(32 pi) remains unabsorbed by the framework")
    print(f"    (d) 'three-route equivalence' is structural scaling, not SI identity")
    print("=" * 76)

    out = {
        "phi_neg_18": PHI ** (-18),
        "G_CODATA": G_NEWTON,
        "G_1_SI": g_1,
        "G_2_single_a6_SI_numerical_only": g_2_single_a6,
        "G_2_dimensionally_corrected_SI": g_2_corr,
        "G_2_corrected_over_G_1": g_2_corr / g_1,
        "expected_residual_phi_neg_18_over_32pi": expected_ratio,
        "residual_matches_expected": math.isclose(g_2_corr / g_1, expected_ratio, rel_tol=1e-6),
        "dimensional_status_route_2_single_a6": "L^4 M^(-1) T^(-2) -- INCONSISTENT",
        "dimensional_status_route_2_corrected_with_a_6_squared": "L^3 M^(-1) T^(-2) -- CORRECT",
        "closure_text": (
            "Route 2 with a single a_6 factor in App K Sec K.7 is dimensionally inconsistent "
            "(L^4 M^(-1) T^(-2) instead of L^3 M^(-1) T^(-2); extra factor of L). "
            "The corrected form G_2 = c_hat^4 / (8 pi K_perp a_6^2) is dimensionally "
            "correct but gives G_2 = [phi^(-18)/(32 pi)] G_1 = 1.7e-6 * G_1, "
            "differing from Route 1 by 6 orders of magnitude. The framework does "
            "not absorb the phi^(-18)/(32 pi) residual; Routes 2/3 are structural "
            "scaling cross-checks only, NOT standalone SI-unit G formulas. The "
            "2274 ppm CODATA agreement derives from Route 1 alone."
        ),
    }
    if OUTPUT_DIR_AVAILABLE:
        out_path = get_output_path("protocol_o22_newton_g_dimensional_full_results.json")
    else:
        out_path = Path(__file__).resolve().parent.parent / "data" / "protocol_o22_newton_g_dimensional_full_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nResults saved to: {out_path}")
    print("=" * 76)


if __name__ == "__main__":
    main()
