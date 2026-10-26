#!/usr/bin/env python3
"""Exact rotational-icosahedral l=6 invariant calculation.

This protocol verifies
the representation-theory theorem that the first nonconstant scalar invariant
of I ~= A5 occurs uniquely at l=6, constructs the six-axis Reynolds sum, and
records that no PTA amplitude or detector transfer follows from that theorem.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import sympy as sp

sys.path.append(str(Path(__file__).resolve().parent))
from gct_utils import get_output_path


def character_decomposition() -> list[dict[str, object]]:
    sqrt5 = sp.sqrt(5)
    phi = (1 + sqrt5) / 2
    sizes = [1, 15, 20, 12, 12]
    angles = [0, sp.pi, 2 * sp.pi / 3, 2 * sp.pi / 5, 4 * sp.pi / 5]
    irreps = {
        "A": [1, 1, 1, 1, 1],
        "T1": [3, -1, 0, phi, 1 - phi],
        "T2": [3, -1, 0, 1 - phi, phi],
        "G": [4, 0, 1, -1, -1],
        "H": [5, 1, -1, 0, 0],
    }

    rows: list[dict[str, object]] = []
    for ell in range(7):
        chi = []
        for theta in angles:
            value = 2 * ell + 1 if theta == 0 else 1 + 2 * sum(
                sp.cos(m * theta) for m in range(1, ell + 1)
            )
            chi.append(sp.simplify(value))

        mult: dict[str, int] = {}
        for name, irrep_chi in irreps.items():
            inner = sp.simplify(
                sum(s * a * b for s, a, b in zip(sizes, chi, irrep_chi)) / 60
            )
            assert inner.is_Integer and inner >= 0
            mult[name] = int(inner)

        parity = "g" if ell % 2 == 0 else "u"
        decomposition = " + ".join(
            f"{name}{parity}" for name, count in mult.items() for _ in range(count)
        )
        assert sum(mult[name] * int(irreps[name][0]) for name in irreps) == 2 * ell + 1
        rows.append(
            {
                "ell": ell,
                "decomposition_Ih": decomposition,
                "trivial_scalar_multiplicity": mult["A"],
            }
        )

    assert [row["decomposition_Ih"] for row in rows] == [
        "Ag", "T1u", "Hg", "T2u + Gu", "Gg + Hg", "T1u + T2u + Hu", "Ag + T1g + Gg + Hg",
    ]
    assert all(rows[ell]["trivial_scalar_multiplicity"] == 0 for ell in range(1, 6))
    assert rows[6]["trivial_scalar_multiplicity"] == 1
    return rows


def six_axis_invariant() -> dict[str, object]:
    x, y, z = sp.symbols("x y z", real=True)
    phi = (1 + sp.sqrt(5)) / 2
    axis_norm = sp.sqrt(phi + 2)
    raw_axes = [(0, 1, phi), (0, -1, phi), (1, phi, 0), (-1, phi, 0), (phi, 0, 1), (phi, 0, -1)]
    axes = [sp.Matrix(v) / axis_norm for v in raw_axes]
    vec = sp.Matrix([x, y, z])
    r2 = x**2 + y**2 + z**2

    def solid_p6(dot: sp.Expr) -> sp.Expr:
        return sp.Rational(1, 16) * (231 * dot**6 - 315 * dot**4 * r2 + 105 * dot**2 * r2**2 - 5 * r2**3)

    h6 = sp.expand(sum(solid_p6(axis.dot(vec)) for axis in axes))
    laplacian = sp.simplify(sum(sp.diff(h6, q, 2) for q in (x, y, z)))
    assert laplacian == 0
    assert sp.simplify(h6.subs({x: z, y: x, z: y}, simultaneous=True) - h6) == 0
    assert sp.simplify(h6.subs({x: x, y: -y, z: -z}, simultaneous=True) - h6) == 0

    dot_sq = {sp.simplify(axes[i].dot(axes[j]) ** 2) for i in range(6) for j in range(i + 1, 6)}
    assert dot_sq == {sp.Rational(1, 5)}
    p6_pair = sp.simplify(sp.legendre(6, 1 / sp.sqrt(5)))
    assert p6_pair == sp.Rational(41, 125)
    norm_sq = sp.simplify(4 * sp.pi / 13 * (6 + 30 * p6_pair))
    assert norm_sq == sp.Rational(1584, 325) * sp.pi

    return {
        "definition": "H6(n) = sum_{i=1}^6 P6(a_i dot n)",
        "L2_norm_squared": "1584*pi/325",
        "normalized_template": "A6 = H6/sqrt(1584*pi/325)",
        "fivefold_frame_power_fractions": {"m=0": "11/25", "m=+5": "7/25", "m=-5": "7/25"},
        "zonal_P6": False,
        "fivefold_axis_line_pair_angle_deg": 63.43494882292201,
        "orientation_space": "SO(3)/I",
    }


def main() -> dict[str, object]:
    rows = character_decomposition()
    invariant = six_axis_invariant()
    result = {
        "prediction_id": "GCT-IH-L6-STRUCTURAL",
        "protocol": "EXACT_ICOSAHEDRAL_SCALAR_INVARIANT",
        "status": "PASS_EXACT_L6_INVARIANT__PTA_SCALAR_SEPARATION_MAP_OBSTRUCTED",
        "pass": True,
        "tier": "Tier 1 exact mathematics; Tier 2 conditional symmetry application; Tier 3/open PTA transfer",
        "character_decomposition": rows,
        "invariant": invariant,
        "pta_bridge": {
            "separation_only_P6_template_valid": False,
            "fifteen_angle_mask_valid": False,
            "nonzero_response_derived": False,
            "amplitude_derived": False,
            "required_next_map": "action -> propagator -> polarization/source/pulsar transfer -> generalized ORFs",
        },
    }
    out = get_output_path("protocol_pta_l6_template_results.json")
    with open(out, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)
    print(json.dumps({"pass": True, "status": result["status"], "output": str(out)}, indent=2))
    return result


if __name__ == "__main__":
    main()
