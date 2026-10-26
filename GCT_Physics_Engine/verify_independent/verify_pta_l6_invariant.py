r"""Independent checks for the icosahedral \ell=6 PTA boundary.

The group-theory result is exact: the rotational icosahedral action has no
nonconstant scalar harmonic below \ell=6 and one at \ell=6.  A sky response,
its normalization, and a generalized pulsar-timing overlap reduction function
require additional physical maps and remain open.
"""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))

from report import make_result, print_summary, write_result


def _trivial_multiplicities() -> list[int]:
    """Compute multiplicities of the trivial A5 irrep in spherical harmonics."""
    sizes = [1, 15, 20, 12, 12]
    angles = [0, sp.pi, 2 * sp.pi / 3, 2 * sp.pi / 5, 4 * sp.pi / 5]
    multiplicities: list[int] = []
    for ell in range(7):
        character = [
            2 * ell + 1 if theta == 0 else 1 + 2 * sum(
                sp.cos(m * theta) for m in range(1, ell + 1)
            )
            for theta in angles
        ]
        multiplicity = sp.simplify(
            sp.Rational(sum(size * value for size, value in zip(sizes, character)), 60)
        )
        assert multiplicity.is_integer and multiplicity >= 0
        multiplicities.append(int(multiplicity))
    return multiplicities


def main() -> list[dict]:
    multiplicities = _trivial_multiplicities()
    first_nonconstant = next(ell for ell, count in enumerate(multiplicities) if ell > 0 and count)
    exact_l6 = multiplicities[1:6] == [0, 0, 0, 0, 0] and multiplicities[6] == 1

    invariant = make_result(
        name="pta_l6_first_scalar_invariant",
        app_psc_label="First nonconstant rotational-icosahedral scalar harmonic",
        formula="mult_A(H_l)=0 for 1<=l<6; mult_A(H_6)=1",
        predicted=float(first_nonconstant),
        observed=6.0,
        reference_class="PURE_MATHEMATICAL",
        unit="multipole index",
        tier="Tier 1 exact representation theory",
        status="TIER1_EXACT" if exact_l6 else "FAIL",
        tolerance_ppm=None,
        extra={"trivial_scalar_multiplicities_l0_to_l6": multiplicities},
    )
    orientation = make_result(
        name="pta_l6_orientation_requirement",
        app_psc_label=r"Icosahedral \ell=6 orientation requirement",
        formula="A_6(R n) with R in SO(3)/I; a separation-only zonal P_6(cos zeta) is not the oriented invariant",
        predicted=1.0,
        observed=1.0,
        reference_class="PURE_MATHEMATICAL",
        unit="boolean exact statement",
        tier="Tier 1 exact symmetry statement",
        status="TIER1_EXACT" if exact_l6 else "FAIL",
        tolerance_ppm=None,
        extra={
            "orientation_space": "SO(3)/I",
            "separation_only_zonal_template_is_derived": False,
            "finite_angle_mask_is_derived": False,
        },
    )
    transfer = make_result(
        name="pta_l6_transfer_open",
        app_psc_label="PTA physical transfer map",
        formula="action -> propagator -> polarization/source/pulsar transfer -> generalized ORFs",
        predicted=0.0,
        observed=0.0,
        reference_class="MANUSCRIPT_STATED",
        unit="closure state",
        tier="Tier 3 physical response program",
        status="OPEN_CONDITIONAL",
        derivational_closure="OPEN_RESEARCH",
        tolerance_ppm=None,
        extra={
            "nonzero_response_derived": False,
            "amplitude_derived": False,
            "frequency_law_derived": False,
            "sky_orientation_derived": False,
        },
    )
    results = [invariant, orientation, transfer]
    for result in results:
        write_result(result)
        print_summary(result)
    return results


if __name__ == "__main__":
    main()
