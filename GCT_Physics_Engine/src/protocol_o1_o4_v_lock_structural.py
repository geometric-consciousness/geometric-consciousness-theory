#!/usr/bin/env python3
"""
protocol_o1_o4_v_lock_structural.py
====================================

Structural identification of the icosahedral lock potential V_lock as
a polynomial in the H_3 fundamental Coxeter invariants. Partial closure
of Open Problem O.1/O.4.

CONTEXT (App H O.1, O.4; V2 Ch14 Sec 14.2)

O.1: Derive the operative phason mass gap m_phason_operative from the non-linear dynamics
     of the icosahedral locking potential V_lock without numerical
     coincidences.
O.4: Derive H_0 from GCT geometry. H_0 is coupled to the dark-energy density
     scale but is not directly identical to m_phason_operative.

ORIGINAL OPEN QUESTION

What is the explicit non-linear V_lock, and what mass-gap does it
predict?

STRUCTURAL IDENTIFICATION

By the Chevalley-Shephard-Todd theorem (Humphreys 1990 Sec 3.5), any
H_3-invariant polynomial of the icosahedral phason field Phi can be
written as a polynomial in the three fundamental invariants of H_3:

  I_2(Phi)  - degree 2 (the metric / quadratic)
  I_6(Phi)  - degree 6 (the icosahedral cubic invariant)
  I_10(Phi) - degree 10 (the higher icosahedral invariant)

The canonical V_lock for an icosahedral phason field then takes the
form

  V_lock(Phi) = -mu^2 * I_2(Phi) + (g_6 / 6) * I_6(Phi) + (g_10 / 10) * I_10(Phi)
                + (higher invariant polynomials in {I_2, I_6, I_10})

The first three terms are the *minimal* non-trivial icosahedral-
invariant potential consistent with the H_3 Coxeter symmetry. Higher
terms (polynomials in I_2, I_6, I_10 of total degree > 10) provide
corrections but are subdominant in the small-Phi expansion.

MASS GAP FROM SPONTANEOUS SYMMETRY BREAKING

The minimum of V_lock (at <Phi> != 0 with H_3 broken to a subgroup)
gives:
  - Goldstone modes (massless phasons) in the directions tangent to
    the H_3 orbit of <Phi>
  - A radial mass m_phason in the direction normal to the orbit

For the simplest Mexican-hat case (g_10 = 0, only I_2 and I_6):
  V_lock = -mu^2 |Phi|^2 + (g_6/6) I_6(Phi)
The mass gap is m_phason^2 ~ mu^2 with a numerical prefactor depending
on the specific H_3-orbit structure at the minimum.

TIER-3 WEINBERG ANSATZ (registered as O.37)

The Weinberg coincidence suggests an alternative scalar scale candidate
  m_Weinberg = M_P phi^(-147) ~ 2.2 meV.
This candidate does not match the operative biogenic-DE quartic mass
  m_phason_operative = 1.7e-5 eV.
The Hubble energy hbar H_0 is a third distinct scale tied to the dark-energy
density, not a direct phason mass constraint.

PARTIAL CLOSURE STATUS

V_lock has canonical Chevalley-Shephard-Todd form as a polynomial in the
H_3 fundamental invariants {I_2, I_6, I_10} of degrees {2, 6, 10}. This is
a Tier 2 STRUCTURAL identification. (App H O.1 leaves V_lock as an
unspecified non-linear icosahedral potential and m_phason undetermined.)

Remaining open: the specific coupling constants (mu^2, g_6, g_10) are
                NOT derivable in-session; they require coupling to the
                cut-and-project lattice constants via the cosmological
                susceptibility chi. The operative mass scale remains
                m_phason_operative = 1.7e-5 eV; the 2.2 meV Weinberg candidate
                is a Tier-3 ansatz pending O.37 reconcile-or-discard.

The structural identification (V_lock = polynomial in H_3 fundamental
invariants) is the canonical icosahedral-symmetry framework; what is
NOT closed is the derivation of the specific coupling constants that
fix m_phason numerically.
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
EV_TO_KG = 1.78266e-36     # 1 eV / c^2

M_P = math.sqrt(HBAR * C_LIGHT / G_NEWTON)
ELL_P = math.sqrt(HBAR * G_NEWTON / C_LIGHT ** 3)

# Cosmological inputs (Planck 2018)
H0_KM_S_MPC = 67.4
H0_SI = (H0_KM_S_MPC * 1000.0) / 3.0857e22

# H_3 fundamental degrees
H3_DEGREES = (2, 6, 10)
H3_DEGREE_SUM = sum(H3_DEGREES)  # = 18 (per O.15(a) sharpening)

# Cosmological constant from Friedmann
OMEGA_LAMBDA = 0.685
RHO_LAMBDA_SI = OMEGA_LAMBDA * 3 * H0_SI ** 2 * C_LIGHT ** 2 / (8 * math.pi * G_NEWTON)


def m_weinberg_candidate_from_quartic_density():
    """Quartic-density scalar candidate: m = (rho_Lambda * hbar^3 / c^5)^(1/4)."""
    return (RHO_LAMBDA_SI * HBAR ** 3 / C_LIGHT ** 5) ** 0.25


def mass_energy_in_eV(m_kg):
    """Convert mass in kg to energy in eV (rest energy)."""
    return m_kg * C_LIGHT ** 2 / 1.602e-19


def phi_power_exponent(M_ref, m_target):
    """x such that m_target = M_ref * phi^(-x)."""
    return -math.log(m_target / M_ref) / math.log(PHI)


def find_nearby_icosahedral_integers(x, max_search=300):
    """Suggest icosahedral integers near x."""
    candidates = {
        "N_cage = 144": 144,
        "h * N = 10 * 15 = 150": 150,
        "h * (N + 1) = 10 * 16 = 160": 160,
        "|I_h|: 120": 120,
        "|I_h| + N: 120+15=135": 135,
        "(h-1) * N = 9*15 = 135": 135,
        "rank * N * 2 = 90": 90,
        "h * Coxeter_h = 100": 100,
        "h * dihedral_D5 = 100": 100,
        "h * sum_degrees = 10*18 = 180": 180,
    }
    nearby = sorted([(name, val, abs(val - x)) for name, val in candidates.items()],
                     key=lambda t: t[2])
    return nearby[:5]


def main():
    print("=" * 76)
    print("O.1/O.4 PROTOCOL: V_lock structural identification + phason-scale scope")
    print("=" * 76)

    print(f"\nH_3 Coxeter group fundamental invariants (Chevalley-Shephard-Todd):")
    print(f"  Fundamental degrees: {H3_DEGREES}")
    print(f"  Sum of degrees     : {H3_DEGREE_SUM}  (matches O.15(a) sharpening)")
    print(f"")
    print(f"  Canonical V_lock structural form:")
    print(f"    V_lock(Phi) = -mu^2 I_2(Phi) + (g_6/6) I_6(Phi) + (g_10/10) I_10(Phi) + ...")
    print(f"  where I_2, I_6, I_10 are the fundamental H_3-invariant polynomials")
    print(f"  of degrees 2, 6, 10. Higher-order corrections are polynomials in")
    print(f"  {{I_2, I_6, I_10}} of total degree > 10.")

    print(f"\nMass gap from spontaneous H_3 symmetry breaking:")
    print(f"  At <Phi> != 0, V_lock has a radial-mode mass m_phason_operative^2 ~ mu^2 * f(g_6, g_10)")
    print(f"  Goldstone modes (massless phasons) tangent to the H_3 orbit.")
    print(f"  Specific m_phason_operative value requires (mu, g_6, g_10) coupling-constant inputs.")

    print(f"\nTier-3 Weinberg ansatz (O.37; not operative m_phason):")
    print(f"  rho_Lambda = Omega_L * 3 H_0^2 c^2 / (8 pi G_N) = {RHO_LAMBDA_SI:.3e} J/m^3")
    print(f"  m_Weinberg = (rho_Lambda * hbar^3 / c^5)^(1/4)")

    m_weinberg_kg = m_weinberg_candidate_from_quartic_density()
    m_weinberg_meV = mass_energy_in_eV(m_weinberg_kg) * 1000.0
    print(f"  m_Weinberg candidate: {m_weinberg_kg:.3e} kg = {m_weinberg_meV:.3f} meV")
    print(f"  m_phason_operative retained in Ledger/Ch14/engine: 1.700e-05 eV")

    exponent_x = phi_power_exponent(M_P, m_weinberg_kg)
    print(f"\n  phi-power identification: m_Weinberg = M_P * phi^(-{exponent_x:.1f})")
    print(f"  M_P / m_Weinberg = {M_P / m_weinberg_kg:.3e}")

    # Nearby icosahedral integers
    print(f"\n  Nearby icosahedral combinatorial integers:")
    for name, val, dist in find_nearby_icosahedral_integers(exponent_x):
        print(f"    {name:>35}: |distance| = {dist:.1f}")

    print(f"\n" + "=" * 76)
    print("VERDICT FOR O.1/O.4 (structural identification only)")
    print("=" * 76)
    print(f"  STRUCTURAL CLOSURE (Tier 2):")
    print(f"    V_lock is the canonical polynomial in H_3 fundamental invariants")
    print(f"    {{I_2, I_6, I_10}} of degrees {{2, 6, 10}} per Chevalley-Shephard-Todd.")
    print(f"    The sum of degrees (18) is the same Coxeter invariant that fixes")
    print(f"    K_perp/K_parallel = phi^(-18) per O.15(a).")
    print(f"")
    print(f"  EMPIRICAL ANCHOR (Tier 3 numerical):")
    print(f"    Weinberg coincidence gives m_Weinberg ~ {m_weinberg_meV:.1f} meV")
    print(f"    -> m_Weinberg = M_P * phi^(-{exponent_x:.0f})")
    print(f"    This does not match m_phason_operative = 1.7e-5 eV and is O.37.")
    print(f"    The exponent {exponent_x:.0f} does not match any single canonical")
    print(f"    icosahedral integer cleanly (closest: N_cage=144, h*N=150).")
    print(f"")
    print(f"  NOT CLOSED (remains research-level open):")
    print(f"    - First-principles derivation of the coupling constants")
    print(f"      (mu^2, g_6, g_10) in V_lock from the cut-and-project lattice")
    print(f"      structure")
    print(f"    - Identification of the phi-power exponent (~146) with a")
    print(f"      canonical icosahedral group-theoretic integer")
    print(f"    - Mexican-hat-style explicit symmetry-breaking analysis on the")
    print(f"      icosahedral coset H_3 / stabilizer")
    print(f"")
    print(f"  STATUS: Structural identification of V_lock = canonical H_3-invariant")
    print(f"  polynomial (Tier 2). m_phason_operative remains 1.7e-5 eV; the")
    print(f"  Weinberg candidate is Tier 3 pending O.37 reconcile-or-discard.")
    print(f"  First-principles derivation of coupling constants remains open.")
    print("=" * 76)

    out = {
        "H_3_fundamental_degrees": list(H3_DEGREES),
        "H_3_degree_sum_per_O15a": H3_DEGREE_SUM,
        "V_lock_canonical_form": "polynomial in {I_2, I_6, I_10} per Chevalley-Shephard-Todd",
        "H0_SI": H0_SI,
        "Omega_Lambda": OMEGA_LAMBDA,
        "rho_Lambda_SI_J_per_m3": RHO_LAMBDA_SI,
        "m_phason_operative_eV": 1.7e-5,
        "m_weinberg_candidate_kg": m_weinberg_kg,
        "m_weinberg_candidate_meV": m_weinberg_meV,
        "M_P_SI_kg": M_P,
        "phi_power_exponent": exponent_x,
        "nearest_icosahedral_integers": [
            {"name": n, "value": v, "distance": d}
            for n, v, d in find_nearby_icosahedral_integers(exponent_x)
        ],
        "status": "Structural identification of V_lock (Tier 2); m_phason_operative retained at 1.7e-5 eV; Weinberg candidate 2.2 meV is Tier 3 O.37 ansatz; coupling constants REMAIN OPEN",
        "remaining_open_research_level": [
            "First-principles derivation of (mu^2, g_6, g_10) coupling constants",
            "O.37 reconcile-or-discard of phi^(-~146) Weinberg candidate",
            "Explicit Mexican-hat symmetry-breaking on H_3 / stabilizer coset",
        ],
    }
    if OUTPUT_DIR_AVAILABLE:
        out_path = get_output_path("protocol_o1_o4_v_lock_structural_results.json")
    else:
        out_path = Path(__file__).resolve().parent.parent / "data" / "protocol_o1_o4_v_lock_structural_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nResults saved to: {out_path}")
    print("=" * 76)


if __name__ == "__main__":
    main()
