"""
verify_n144.py - N = 144 dodecahedral cage node count.

V3 Ch07 Sec 7.1.3: "N = 12 x 12 = 144 = F_12 = 12^2" is an adopted
Tier-3 two-shell cage posit pending O.38, not a Gauss--Bonnet derivation.

This verifier confirms:
    (1) the icosahedron defect is pi/3 and its 12-vertex total is 4pi;
    (2) the dodecahedron defect is pi/5 and its 20-vertex total is 4pi;
    (3) F_12 = 144 = 12^2, with no other square Fibonacci number in the
        local [F_10, F_13] range.
These are exact consistency checks. They do not select N=144 physically.
"""

import math
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
    # Exact polyhedral Gauss--Bonnet totals.
    ico_defect = 2 * math.pi - 5 * (math.pi / 3)
    ico_total = 12 * ico_defect
    dodeca_defect = 2 * math.pi - 3 * (3 * math.pi / 5)
    dodeca_total = 20 * dodeca_defect
    gauss_bonnet_checks = (
        math.isclose(ico_defect, math.pi / 3)
        and math.isclose(ico_total, 4 * math.pi)
        and math.isclose(dodeca_defect, math.pi / 5)
        and math.isclose(dodeca_total, 4 * math.pi)
    )

    # Conditional two-shell arithmetic.
    f_12 = fibonacci(12)
    is_fibonacci_144 = (f_12 == 144)

    # (2) 12^2 = 144
    is_perfect_square_144 = (12 * 12 == 144)

    # (3) Uniqueness in cage-relevant range
    fib_in_range = [(k, fibonacci(k)) for k in range(10, 14)]
    perfect_square_fibs = [(k, f) for k, f in fib_in_range if int(f ** 0.5) ** 2 == f]

    matches = (
        gauss_bonnet_checks
        and is_fibonacci_144
        and is_perfect_square_144
        and len(perfect_square_fibs) == 1
    )

    res = make_result(
        name="cage_node_count_N144",
        app_psc_label="Dodecahedral cage node count N = 144",
        formula="adopted N = 12 x 12 = F_12 = 144; GB: 12(pi/3) = 20(pi/5) = 4pi",
        predicted=144,
        observed=144,
        unit="(integer)",
        app_psc_predicted=144,
        app_psc_precision_str="exact conditional arithmetic; physical cage selection NOT_EVALUATED pending O.38",
        app_psc_precision_ppm=None,
        tier="Tier 3 N=144 cage posit + Tier 1 polyhedral/arithmetic checks (O.38 open)",
        status="INTERNAL_ARITHMETIC_PASS" if matches else "FAIL",
        derivational_closure="OPEN_CONDITIONAL",
        tolerance_ppm=None,
        discrepancy_notes=[
            "The 144-to-144 comparison checks the adopted manuscript datum only; "
            "it is not an empirical observation or a physical cage-size test."
        ],
        extra={
            "F_12_computed": f_12,
            "F_12_equals_144": is_fibonacci_144,
            "144_equals_12_squared": is_perfect_square_144,
            "fibonacci_in_range_F10_to_F13": fib_in_range,
            "perfect_square_fibonacci_in_range": perfect_square_fibs,
            "uniqueness_holds": len(perfect_square_fibs) == 1,
            "icosahedron_vertex_defect_rad": ico_defect,
            "icosahedron_vertex_count": 12,
            "icosahedron_total_defect_rad": ico_total,
            "dodecahedron_vertex_defect_rad": dodeca_defect,
            "dodecahedron_vertex_count": 20,
            "dodecahedron_total_defect_rad": dodeca_total,
            "gauss_bonnet_checks_pass": gauss_bonnet_checks,
            "n144_derived_by_gauss_bonnet": False,
            "z12_role": "geometry-specific consistency check only; not a forcing input",
            "open_problem": "O.38 full lattice minimization",
            "derivation_note": (
                "Discrete Gauss--Bonnet closes exactly on the regular "
                "icosahedron (vertex defect pi/3, 12 vertices) and regular "
                "dodecahedron (vertex defect pi/5, 20 vertices), each totaling "
                "4pi. It does not determine 12 sub-nodes per face or N=144. "
                "The exact F_12=144=12^2 identity checks the adopted two-shell "
                "ansatz; physical cage-size selection remains a Tier-3 posit "
                "pending O.38."
            ),
        },
    )
    print_summary(res)
    write_result(res)
    return res


if __name__ == "__main__":
    main()
