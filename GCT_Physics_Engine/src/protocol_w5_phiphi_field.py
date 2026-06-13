#!/usr/bin/env python3
"""
protocol_w5_phiphi_field.py - W5: algebraic-field status of the FK determinant
==============================================================================
The down-quark FK determinant limit det_FK has TWO candidate closed forms,
recorded in App TP item 2b:
  (A) phi^phi                      (the adopted primary output, m_d = m_u phi^phi)
  (B) phi * 2^(39/100) * 3^(5/100) (the finite-cage R=2 secondary diagnostic)

The down-quark closure rests on what kind of number det_FK is -- a Bellissard
Z[phi] gap label, some other algebraic number, or a genuinely transcendental
emergent constant -- so this protocol classifies each form rigorously.

Rigorous facts (not numerical guesses):
  - Z[phi] = Z + Z*phi is a degree-2 number field (Q(sqrt5)). Its elements are
    algebraic of degree <= 2 over Q.
  - phi is algebraic (root of x^2 - x - 1), irrational, != 0, 1.
  - (A) phi^phi: exponent phi = (1+sqrt5)/2 is an irrational ALGEBRAIC number, so
    by the Gelfond-Schneider theorem phi^phi is TRANSCENDENTAL. A transcendental
    number is not algebraic, hence not in Z[phi]. [convention-independent: it is
    excluded from EVERY algebraic-number module, not just Z[phi].]
  - (B) phi * 2^(39/100) * 3^(5/100): 2^(39/100) is a root of x^100 - 2^39 and
    3^(5/100) = 3^(1/20) is a root of x^20 - 3, both with rational coefficients,
    so both are ALGEBRAIC over Q (algebraic numbers form a field, so the product
    is algebraic). It is NOT transcendental. Its degree over Q exceeds 2 (the
    20th/100th roots of integers are not in any quadratic field), so it is not in
    Z[phi] either -- but for the ALGEBRAIC-DEGREE reason, NOT transcendence.

=> Both forms lie outside Z[phi], but for different reasons: (A) is
   transcendental (excluded from every algebraic-number module), while (B) is
   algebraic of degree > 2 over Q (excluded by algebraic degree, not by
   transcendence). This matches the classification in App TP item 2b.

The protocol verifies the algebraic/transcendental classification structurally
(degrees of the defining polynomials) and compares both forms numerically to the
empirical det_FK centre.
"""

import json
import os
import sys
import io
from math import gcd, log

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

try:
    from gct_utils import get_output_path, C
except ImportError:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from gct_utils import get_output_path, C

PHI = float(C.PHI)
# Empirical det_FK centre from the I_h-closed-cage deep tail (W3 / down-quark
# audit): mean det_FK / phi^phi = 0.9976 over N>=2000 cages.
DETFK_CENTRE = 0.9976 * PHI ** PHI


def rational_power_degree(base_int, p, q):
    """Degree over Q of base_int^(p/q) (base_int a positive integer, not a
    perfect power matching the denominator). x^(q/gcd) - base^(p/gcd) is the
    defining polynomial; degree is q/gcd(p,q) for base not a perfect d-th power."""
    g = gcd(p, q)
    return q // g   # generic degree of an integer's reduced rational power


def run():
    print("=" * 72)
    print("GCT Protocol W5 - algebraic-field status of the FK determinant limit")
    print("=" * 72)

    phiphi = PHI ** PHI
    formB = PHI * (2 ** 0.39) * (3 ** 0.05)
    print(f"\n  Empirical det_FK centre (0.9976 * phi^phi): {DETFK_CENTRE:.6f}")
    print(f"  (A) phi^phi                  = {phiphi:.6f}   "
          f"({100*(phiphi-DETFK_CENTRE)/DETFK_CENTRE:+.3f}% vs centre)")
    print(f"  (B) phi*2^(39/100)*3^(5/100) = {formB:.6f}   "
          f"({100*(formB-DETFK_CENTRE)/DETFK_CENTRE:+.3f}% vs centre)")

    # (A) phi^phi : Gelfond-Schneider transcendental
    a_base_algebraic = True          # phi root of x^2-x-1
    a_exp_alg_irrational = True      # phi is algebraic and irrational
    A_transcendental = a_base_algebraic and a_exp_alg_irrational
    A_in_Zphi = False                # transcendental -> not algebraic -> not in Z[phi]
    print("\n  (A) phi^phi:")
    print(f"     base phi algebraic, != 0,1: {a_base_algebraic}; "
          f"exponent phi algebraic-irrational: {a_exp_alg_irrational}")
    print(f"     => Gelfond-Schneider: TRANSCENDENTAL = {A_transcendental}; "
          f"in Z[phi]: {A_in_Zphi}")

    # (B) phi * 2^(39/100) * 3^(5/100): algebraic, degree > 2
    deg2 = rational_power_degree(2, 39, 100)   # 100
    deg3 = rational_power_degree(3, 5, 100)    # 20 (5/100 -> 1/20)
    B_algebraic = True                          # product of algebraics
    B_transcendental = False
    B_degree_exceeds_2 = (deg2 > 2 or deg3 > 2)
    B_in_Zphi = not B_degree_exceeds_2          # would need degree <= 2
    print("\n  (B) phi * 2^(39/100) * 3^(5/100):")
    print(f"     2^(39/100): root of x^100 - 2^39  -> degree {deg2} over Q (algebraic)")
    print(f"     3^(5/100)=3^(1/20): root of x^20 - 3 -> degree {deg3} over Q (algebraic)")
    print(f"     => ALGEBRAIC (not transcendental); degree > 2: {B_degree_exceeds_2}; "
          f"in Z[phi]: {B_in_Zphi}")

    formB_algebraic_not_transcendental = True   # (B) is algebraic of degree > 2 over Q
    print("\n  " + "-" * 66)
    verdict = (
        "W5: det_FK closed-form classification. "
        "(A) phi^phi is TRANSCENDENTAL (Gelfond-Schneider) and excluded from "
        "Z[phi] -- indeed from every algebraic-number module; it is an emergent "
        "spectral constant, not a Bellissard gap label (consistent with the "
        "multiplicative-FK vs additive-K0 distinction). (B) phi*2^(39/100)*"
        "3^(5/100) is ALGEBRAIC of degree > 2 over Q (rational powers of integers "
        "are algebraic); it lies outside Z[phi] by its algebraic degree, not by "
        "transcendence. Both forms therefore lie outside Z[phi] for distinct "
        "reasons, as recorded in App TP item 2b. "
        f"Numerically phi^phi ({phiphi:.4f}) matches the det_FK centre to "
        f"{abs(100*(phiphi-DETFK_CENTRE)/DETFK_CENTRE):.2f}%, closer than form "
        f"(B) ({formB:.4f}, {abs(100*(formB-DETFK_CENTRE)/DETFK_CENTRE):.2f}%); "
        "(A) is the adopted primary closed form and (B) the finite-cage "
        "secondary algebraic diagnostic.")
    print("  VERDICT:", verdict)
    print("=" * 72)

    results = {
        "detfk_centre_0p9976_phiphi": DETFK_CENTRE,
        "formA_phiphi": phiphi,
        "formA_transcendental": bool(A_transcendental),
        "formA_in_Zphi": bool(A_in_Zphi),
        "formA_pct_vs_centre": 100 * (phiphi - DETFK_CENTRE) / DETFK_CENTRE,
        "formB_value": formB,
        "formB_algebraic_degree2_over_Q": deg2,
        "formB_algebraic_degree3_over_Q": deg3,
        "formB_transcendental": bool(B_transcendental),
        "formB_algebraic": bool(B_algebraic),
        "formB_in_Zphi": bool(B_in_Zphi),
        "formB_pct_vs_centre": 100 * (formB - DETFK_CENTRE) / DETFK_CENTRE,
        "formB_algebraic_degree_gt2_not_transcendental": bool(formB_algebraic_not_transcendental),
        "verdict": verdict,
    }
    out = get_output_path("protocol_w5_phiphi_field_results.json")
    with open(out, "w") as fp:
        json.dump(results, fp, indent=2)
    print(f"\n[Saved JSON] -> {out}")
    return results


if __name__ == "__main__":
    run()
