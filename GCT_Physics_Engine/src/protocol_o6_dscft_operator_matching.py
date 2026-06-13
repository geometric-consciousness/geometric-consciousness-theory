#!/usr/bin/env python3
"""
protocol_o6_dscft_operator_matching.py
=======================================

Symmetry-level dS_4/CFT_3 operator matching extension of the Hartle-
Hawking semi-classical closure. Tier 1 partial closure refinement of
Open Problem O.6.

CONTEXT

The Hartle-Hawking closure (protocol_o6_dscft_hartle_hawking.py)
established Tier 1 partial: the semi-classical boundary state on
Euclidean S^4 gives S_HH = S_GH = chi via replica-trick entanglement
entropy. The remaining open piece is the FULL dS_4/CFT_3 operator
dictionary (Strominger 2001 JHEP 10:034; Maldacena 2003 JHEP 05:013;
Anninos-Hartman-Strominger 2017 Class. Quant. Grav. 34:015009).

This protocol provides the SYMMETRY-LEVEL extension:
  - matching the dS_4 isometry group SO(4,1) to the CFT_3 conformal
    group SO(4,1), with spin cover Spin(4,1) ~= USp(2,2)
  - identifying scalar bulk-boundary operator dimensions via the
    mass-dimension relation as written in the manuscript,
    Delta(Delta - d) = m^2 L^2
  - documenting the unitarity caveat (non-normalizable bulk states in
    dS) as the remaining open piece

THIS IS NOT A FULL CLOSURE of the operator dictionary -- the unitary
completion of the Hilbert-space structure at the dS side is genuinely
open in theoretical physics. The symmetry-level matching is a
structural extension that sharpens the Tier 1 partial status without
claiming Hilbert-space-level completion.

SETUP

dS_4 in global coordinates: ds^2 = L^2 (-dt^2 + cosh^2(t) dOmega_3^2)
where L = c / H_0 is the dS radius.

The isometry group is SO(4,1) (de Sitter group). On the future
conformal boundary I^+ (S^3 at t -> +infinity), SO(4,1) acts as the
conformal group of S^3, which is also SO(4,1) (Strominger 2001 Sec 2).
Its spin cover is Spin(4,1), isomorphic to USp(2,2). SL(2,C) is the
spin cover of SO^+(3,1), not the dS_4/CFT_3 conformal-group cover.

For a scalar field phi of mass m in dS_4, the asymptotic behavior near
I^+ is:
  phi(t, Omega) ~ e^(-Delta_+ t) phi_+(Omega) + e^(-Delta_- t) phi_-(Omega)
where Delta_+ + Delta_- = d = 3 (boundary dimension) and, under the
equation Delta(Delta - d) = m^2 L^2, Delta_+ Delta_- = -m^2 L^2.

Solving:
  Delta_+/- = (d/2) +/- sqrt((d/2)^2 + m^2 L^2)
           = (3/2) +/- sqrt(9/4 + m^2 L^2)

Three regimes:
  - m^2 L^2 > 0 : Delta_+ > d and Delta_- < 0 under this equation
  - m^2 L^2 = 0 : Delta_+ = d and Delta_- = 0
  - the complementary-series formula with sqrt(d^2/4 - m^2 L^2) belongs
    to the alternate dS-sign convention Delta(d - Delta) = m^2 L^2, not
    to Delta(Delta - d) = m^2 L^2

CFT_3 OPERATOR DICTIONARY

In the bulk-boundary correspondence (analogous to AdS/CFT but with
dS-specific subtleties):
  - The slower-falloff mode (Delta_-) sources the boundary operator
  - The faster-falloff mode (Delta_+) is the VEV / expectation value
  - The CFT_3 operator dimension is Delta_+

For the Tier-3 Weinberg-candidate scalar (O.37), with
  m_Weinberg ~ 2.2 meV ~ M_P phi^(-147),
we evaluate the toy operator-matching point m^2 L^2 ~ 1. This candidate is
not m_phason_operative = 1.7e-5 eV and not the Hubble energy hbar H_0.
It is an alternative scale ansatz pending reconcile-or-discard under O.37.

For m^2 L^2 = 1, Delta_+/- = 3/2 +/- sqrt(9/4 + 1) = (3 +/- sqrt(13))/2
  Delta_+ = (3 + sqrt(13))/2 ~ 3.303
  Delta_- = (3 - sqrt(13))/2 ~ -0.303

NO phi-POWER DIMENSION CLAIM UNDER THE WRITTEN EQUATION

For the Weinberg-candidate scalar at m^2 L^2 ~ 1,
the boundary CFT_3 operator dimensions are not golden-ratio squares under
Delta(Delta - d) = m^2 L^2. A phi^(+/-2) identification follows
only if the relation is instead written with the dS complementary-series
sign Delta(d - Delta) = m^2 L^2. That alternate-sign observation is not
claimed here as an O.6 closure.

SYMMETRY-LEVEL MATCHING

  Bulk isometry group:          SO(4,1)
  Boundary conformal group:     SO(4,1) (== conformal group of S^3)
  Spin cover:                   Spin(4,1) ~= USp(2,2)
  Non-cover note:               SL(2,C) covers SO^+(3,1), not SO(4,1)
  Casimir eigenvalues:          parametrize unitary irreps
  Principal series:             continuous parameter, complex Delta
  Complementary series:         real Delta in (0, d)
  Discrete series:              at specific integer Delta

The Weinberg-candidate scalar at m^2 L^2 ~ 1 sits outside the simple
complementary-series interval under the written equation: Delta_+ > 3 and
Delta_- < 0.

REMAINING OPEN (genuinely conjectural in theoretical physics)

The HILBERT-SPACE-LEVEL UNITARITY of dS/CFT is open:
  - dS has non-normalizable mode expansions (Maldacena 2003)
  - The Bunch-Davies vacuum is non-Hermitian under standard inner product
  - Anninos-Hartman-Strominger 2017 propose higher-spin dictionary with
    explicit unitary structure for specific cases
  - Full proof of unitarity for general matter content remains open

This is a problem in theoretical physics, NOT a problem specific to GCT.
GCT inherits the symmetry-level matching cleanly; the Hilbert-space
unitarity question is independent of GCT's specific implementation.

STATUS

  Current standing:    Tier 1 partial (semi-classical boundary state via
                       S^4 path integral) plus a symmetry-algebra
                       consistency audit. Under the written equation
                       Delta(Delta - d) = m^2 L^2 the phi^(+/-2) numerical
                       identification is an alternate-sign diagnostic, not
                       a closure.
  Full closure (open): Hilbert-space unitarity + complete operator-algebra
                       dictionary (genuinely open in theoretical physics)
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


def conformal_dimensions(m_squared_L_squared, d=3):
    """Delta_+/- for scalar mass m under Delta(Delta - d) = m^2 L^2.

    Delta(Delta - d) = m^2 L^2
    Delta_+/- = (d/2) +/- sqrt((d/2)^2 + m^2 L^2)
    """
    half_d = d / 2.0
    discriminant = half_d ** 2 + m_squared_L_squared
    if discriminant >= 0:
        sqrt_d = math.sqrt(discriminant)
        return (half_d + sqrt_d, half_d - sqrt_d, "real")
    else:
        sqrt_d = math.sqrt(-discriminant)
        # Delta = d/2 +/- i sqrt(...)
        return (complex(half_d, sqrt_d), complex(half_d, -sqrt_d), "complex (principal series)")


def classify_series(delta_plus_minus, series_type):
    """Classify the SO(4,1) representation series."""
    if series_type == "complex (principal series)":
        return "principal series"
    delta_plus, delta_minus = delta_plus_minus[0], delta_plus_minus[1]
    if 0 < delta_minus < 3 and 0 < delta_plus < 3:
        return "complementary series"
    elif delta_minus == 0 or delta_plus == 3 or delta_minus == 3 or delta_plus == 0:
        return "discrete series boundary"
    else:
        return "outside standard series classification"


def main():
    print("=" * 76)
    print("O.6 PROTOCOL EXTENSION: dS_4/CFT_3 symmetry-level operator matching")
    print("=" * 76)

    print(f"\nDeSitter scalar bulk-boundary correspondence:")
    print(f"  Bulk: dS_4 of radius L = c/H_0")
    print(f"  Boundary: future infinity I^+ ~ S^3")
    print(f"  Both isometry/conformal group: SO(4,1)")
    print(f"  Scalar of mass m: Delta(Delta - 3) = m^2 L^2")
    print(f"  Delta_+/- = 3/2 +/- sqrt(9/4 + m^2 L^2)")

    print(f"\nSeries classification by m^2 L^2:")
    for m2L2, label in [(0.0, "massless"),
                         (0.5, "light"),
                         (1.0, "Weinberg-candidate ansatz (O.37; m^2 L^2 ~ 1)"),
                         (2.0, "moderate"),
                         (9.0 / 4.0, "conformally coupled"),
                         (3.0, "heavy"),
                         (10.0, "very heavy")]:
        d_p, d_m, series_type = conformal_dimensions(m2L2)
        cls = classify_series((d_p, d_m), series_type)
        if isinstance(d_p, complex):
            print(f"  m^2 L^2 = {m2L2:>6.3f} ({label:<35}): Delta_+/- = {d_p:.3f}, {d_m:.3f}  -- {cls}")
        else:
            print(f"  m^2 L^2 = {m2L2:>6.3f} ({label:<35}): Delta_+ = {d_p:.4f}, Delta_- = {d_m:.4f}  -- {cls}")

    print(f"\n--- Weinberg-candidate scalar ansatz (O.37; m^2 L^2 ~ 1) ---")
    delta_p, delta_m, series_type = conformal_dimensions(1.0)
    cls = classify_series((delta_p, delta_m), series_type)
    print(f"  Delta_+ = (3 + sqrt(13))/2 = {delta_p:.6f}")
    print(f"  phi^2   = phi + 1          = {PHI ** 2:.6f}  (diagnostic only)")
    print(f"  Match: {math.isclose(delta_p, PHI ** 2, rel_tol=1e-10)}")
    print(f"")
    print(f"  Delta_- = (3 - sqrt(13))/2 = {delta_m:.6f}")
    print(f"  1/phi^2 = 2 - phi          = {1.0 / PHI ** 2:.6f}  (diagnostic only)")
    print(f"  Match: {math.isclose(delta_m, 1.0 / PHI ** 2, rel_tol=1e-10)}")

    print(f"\n  CFT_3 BOUNDARY OPERATOR DIMENSIONS:")
    print(f"  --> Delta_+ = (3 + sqrt(13))/2")
    print(f"  --> Delta_- = (3 - sqrt(13))/2")
    print(f"  --> No phi^(+/-2) identification follows from the written equation.")
    print(f"")
    print(f"  Series:    {cls}")
    print(f"  Sum check: Delta_+ + Delta_- = {delta_p + delta_m:.6f} = d = 3  (boundary dim)")
    print(f"  Product:   Delta_+ * Delta_- = {delta_p * delta_m:.6f} = -m^2 L^2 = -1")

    print(f"\nSO(4,1) Casimir eigenvalues:")
    print(f"  C_2 = Delta(Delta - 3) = m^2 L^2 = 1 (the eigenvalue is the bulk mass^2)")

    print(f"\n" + "=" * 76)
    print("VERDICT FOR O.6 EXTENSION")
    print("=" * 76)
    print(f"  STRUCTURAL CLAIM (Tier 1 partial extension):")
    print(f"")
    print(f"    The Tier-3 Weinberg-candidate scalar (m_Weinberg ~ M_P phi^(-147),")
    print(f"    not m_phason_operative and not hbar H_0) gives CFT_3 boundary dimensions")
    print(f"        Delta_+ = (3 + sqrt(13))/2 ~ 3.303")
    print(f"        Delta_- = (3 - sqrt(13))/2 ~ -0.303")
    print(f"    from Delta(Delta - d) = m^2 L^2.")
    print(f"")
    print(f"    The phi^(+/-2) value belongs to the alternate-sign diagnostic")
    print(f"    Delta(d - Delta) = m^2 L^2 and is not claimed as a closure here.")
    print(f"")
    print(f"  STATUS:")
    print(f"    Tier 1 partial (Hartle-Hawking semi-classical boundary state)")
    print(f"    plus a sign-corrected symmetry-level free-scalar diagnostic")
    print(f"")
    print(f"    REMAINING OPEN (genuinely conjectural in theoretical physics, not")
    print(f"    GCT-specific):")
    print(f"      - Hilbert-space unitarity for general matter content in dS")
    print(f"      - Bunch-Davies vacuum non-Hermitian inner-product structure")
    print(f"        (Maldacena 2003 JHEP 05:013)")
    print(f"      - Complete operator-algebra dictionary beyond free-scalar mode")
    print(f"        (Anninos-Hartman-Strominger 2017 higher-spin partial)")
    print(f"")
    print(f"    These are open dS/CFT research questions, NOT GCT-specific gaps.")
    print(f"    GCT inherits the symmetry-level matching cleanly; the unitarity")
    print(f"    completion is upstream of any framework using dS_4.")
    print("=" * 76)

    out = {
        "phi": PHI,
        "phi_squared": PHI ** 2,
        "phi_neg_2": 1.0 / PHI ** 2,
        "bulk_isometry_group": "SO(4,1)",
        "boundary_conformal_group": "SO(4,1)",
        "spin_cover": "Spin(4,1) ~= USp(2,2)",
        "non_cover_note": "SL(2,C) covers SO^+(3,1), not SO(4,1).",
        "m_phason_operative_eV": 1.7e-5,
        "m_weinberg_candidate_m2L2": 1.0,
        "Delta_plus_weinberg_candidate": delta_p,
        "Delta_minus_weinberg_candidate": delta_m,
        "Delta_plus_equals_phi_squared": bool(math.isclose(delta_p, PHI ** 2, rel_tol=1e-10)),
        "Delta_minus_equals_phi_neg_2": bool(math.isclose(delta_m, 1.0 / PHI ** 2, rel_tol=1e-10)),
        "mass_dimension_relation_used": "Delta(Delta - d) = m^2 L^2",
        "root_formula": "Delta = (d +/- sqrt(d^2 + 4 m^2 L^2)) / 2",
        "phi_power_identification_diagnostic_only": True,
        "alternate_sign_diagnostic": "Delta(d - Delta) = m^2 L^2 gives phi^(+/-2) at m^2L^2=1, but that is not the written relation.",
        "series_classification": cls,
        "remaining_open_in_theoretical_physics": [
            "Hilbert-space unitarity for general matter in dS",
            "Bunch-Davies vacuum non-Hermitian inner-product structure (Maldacena 2003)",
            "Complete operator-algebra dictionary beyond free-scalar mode (Anninos-Hartman-Strominger 2017 higher-spin partial)",
        ],
        "status": "Tier 1 partial + sign-corrected symmetry-level diagnostic; phi^(+/-2) identification is an alternate-sign diagnostic under Delta(d - Delta) = m^2 L^2, not the written relation; Hilbert-space unitarity remains conjectural at the theoretical-physics level (NOT GCT-specific)",
    }
    if OUTPUT_DIR_AVAILABLE:
        out_path = get_output_path("protocol_o6_dscft_operator_matching_results.json")
    else:
        out_path = Path(__file__).resolve().parent.parent / "data" / "protocol_o6_dscft_operator_matching_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nResults saved to: {out_path}")
    print("=" * 76)


if __name__ == "__main__":
    main()
