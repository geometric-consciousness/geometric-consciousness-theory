"""
verify_n144.py - N = 144 dodecahedral cage node count.

V3 Ch07 Sec 7.1.3 (Parameter Ledger Sec 2): "N = 12 x 12 = 144 = F_12 = 12^2".
Two structural derivations stated in Ch07:
    (a) Gauss-Bonnet closure: 12 outer dodecahedral faces x 12 inner
        vertex-star sub-nodes = 144.
    (b) Fibonacci resonance: 144 = F_12 (12th Fibonacci number) - the
        unique Fibonacci number that is also a perfect square in the
        range [55, 250].

This verifier confirms:
    (1) F_12 = 144 (Fibonacci identity).
    (2) 12^2 = 144 (perfect square).
    (3) No other Fibonacci number in [F_10, F_13] is a perfect square.
This makes 144 the UNIQUE intersection of "Fibonacci number" and
"perfect square" in the cage-size-relevant range.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from report import make_result, write_result, print_summary


def fibonacci(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def main():
    # (1) F_12 = 144
    f_12 = fibonacci(12)
    is_fibonacci_144 = (f_12 == 144)

    # (2) 12^2 = 144
    is_perfect_square_144 = (12 * 12 == 144)

    # (3) Uniqueness in cage-relevant range
    fib_in_range = [(k, fibonacci(k)) for k in range(10, 14)]
    perfect_square_fibs = [(k, f) for k, f in fib_in_range if int(f ** 0.5) ** 2 == f]

    matches = is_fibonacci_144 and is_perfect_square_144 and len(perfect_square_fibs) == 1

    res = make_result(
        name="cage_node_count_N144",
        app_r_label="Dodecahedral cage node count N = 144",
        formula="N = 12 x 12 = F_12 = 144 (Gauss-Bonnet closure + Fibonacci resonance)",
        predicted=144,
        observed=144,
        unit="(integer)",
        app_r_predicted=144,
        app_r_precision_str="exact integer identity (F_12 = 144 = 12^2; unique Fibonacci-square in [F_10, F_13])",
        app_r_precision_ppm=0.0,
        tier="Tier 2 (Gauss-Bonnet closure + Fibonacci resonance)",
        status="PASS" if matches else "FAIL",
        tolerance_ppm=0.0,
        extra={
            "F_12_computed": f_12,
            "F_12_equals_144": is_fibonacci_144,
            "144_equals_12_squared": is_perfect_square_144,
            "fibonacci_in_range_F10_to_F13": fib_in_range,
            "perfect_square_fibonacci_in_range": perfect_square_fibs,
            "uniqueness_holds": len(perfect_square_fibs) == 1,
            "derivation_note": (
                "Two independent structural anchors converge on 144: "
                "(a) Gauss-Bonnet closure with 5-fold angle deficits "
                "requires 12 outer faces x 12 inner sub-nodes per face = "
                "144 (Sub-Proof A); (b) the Fibonacci resonance condition "
                "for cage-size stability in a phi-based quasicrystal requires "
                "N to be both a Fibonacci number AND a perfect square; F_12 = "
                "144 = 12^2 is the unique such number in the cage-relevant "
                "range. The integer identity is trivially verifiable; the "
                "Tier 2 epistemic substance is in the two structural arguments "
                "themselves (Sub-Proofs A and B), which are mathematical "
                "consequences of the icosahedral cut-and-project setup."
            ),
        },
    )
    print_summary(res)
    write_result(res)
    return res


if __name__ == "__main__":
    main()
