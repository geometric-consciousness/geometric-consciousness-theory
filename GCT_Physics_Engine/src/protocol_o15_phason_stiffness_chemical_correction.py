#!/usr/bin/env python3
"""
protocol_o15_phason_stiffness_chemical_correction.py
====================================================

QUARANTINED dimensional-sweep audit. This script is NOT evidence for the
Tier 3 P3b stiffness map K_perp/K_parallel = phi^(-18), does NOT close Open
Problem O.15 path (b), and always reports pass = false.

History. Earlier editions used this sweep to claim that a Penrose-Toner
"chemical-bonding floor" quantitatively explained a 100-1000x gap between
phi^(-18) and i-AlPdMn measurements. That claim is withdrawn
(App DPS §DPS.4b; App ORQ O.15, O.41) for three reasons:

  (i)   K_PT ~ E_flip / V_atom has the dimensions of an energy density, but an
        equilibrium phason elastic constant is a second derivative of the
        free-energy density with respect to phason strain, while an activation
        barrier controls kinetics. Converting one into the other needs a
        specified microscopic Hamiltonian or partition function, flip density,
        strain increment, degeneracies, temperature and relaxation prescription;
        none is supplied, and the unit coefficient was implicit.
  (ii)  The DFT source formerly cited for the 100-700 meV Al-Pd swap energies
        ("Phys. Rev. B 88:144102", 2013) is wrong: DOI
        10.1103/PhysRevB.88.144102 is Xiao, Cheng, Zhou, Goodenough and
        Henkelman (2013), "Mechanism of the CaIrO3 post-perovskite phase
        transition under pressure", unrelated to quasicrystals. The swap-energy
        band is therefore an unsourced input.
  (iii) The former "observational anchors" are not the registered ratio
        (the cited papers have not been re-read against this specific
        claim):
        de Boissieu et al. (1995) infer the phason elastic anisotropy K_2/K_1
        and Francoual et al. (2006) report phason relaxation kinetics. Neither
        observable is K_perp/K_parallel, so the former 1e-2 .. 1e-1 "band"
        compared unlike quantities.

What remains is arithmetic: the script sweeps E_flip / V_atom over the
historical input box and reports the resulting dimensionless numbers, so the
retired claim stays reproducible and auditable. Only the integer D = 18 is
Tier 2; the phi^(-18) map is the Tier 3 P3b hypothesis, registered outside the
count (Parameter Ledger §0.1).
"""

import json
import math
import numpy as np
from pathlib import Path

try:
    from gct_utils import get_output_path, C
    OUTPUT_DIR_AVAILABLE = True
except ImportError:
    OUTPUT_DIR_AVAILABLE = False

# Golden ratio and bare GCT prediction
PHI = float(C.PHI)
PHI_NEG_18 = PHI ** (-18)  # = 1.7307e-4

# i-AlPdMn material parameters (Tier 3 literature anchors)
RHO_IAPDMN = 5100.0       # kg/m^3 (de Boissieu+ 1995)
C_L_IAPDMN = 4100.0       # m/s longitudinal sound speed (Wang+ 1998)
K_PHONON_IAPDMN_PA = RHO_IAPDMN * C_L_IAPDMN ** 2  # in Pa

# Unit conversion: 1 Pa = 1 J/m^3 = (6.241509e18 eV)/(1e30 A^3) = 6.241509e-12 eV/A^3.
PA_TO_EV_PER_A3 = 6.241509e-12

K_PHONON_IAPDMN_EV_PER_A3 = K_PHONON_IAPDMN_PA * PA_TO_EV_PER_A3

# Withdrawn comparison values (not K_perp/K_parallel; see docstring (iii)).
K_PHASON_OVER_PHONON_DE_BOISSIEU_1995 = 1e-2
K_PHASON_OVER_PHONON_FRANCOUAL_2006 = 1e-1

# Historical, unsourced input box (see docstring (ii)); kept only so the
# retired sweep remains reproducible.
E_FLIP_RANGE_MEV = (100.0, 700.0)
V_ATOM_RANGE_A3 = (12.0, 20.0)       # per-atom volume in i-AlPdMn


def k_phason_pt(e_flip_mev, v_atom_a3):
    """Penrose-Toner phason stiffness contribution in eV/A^3.

    K_PT ~ E_flip / V_atom
    E_flip in meV, V_atom in cubic angstroms.
    """
    e_flip_ev = e_flip_mev * 1e-3
    return e_flip_ev / v_atom_a3


def k_perp_bare_ev_per_a3():
    """Bare GCT prediction K_perp = phi^(-18) * K_phonon in eV/A^3."""
    return PHI_NEG_18 * K_PHONON_IAPDMN_EV_PER_A3


def run_sweep():
    """Sweep (E_flip, V_atom) over the literature-anchored ranges and
    report the predicted K_phason/K_phonon envelope."""
    e_flip_grid = np.linspace(E_FLIP_RANGE_MEV[0], E_FLIP_RANGE_MEV[1], 6)
    v_atom_grid = np.linspace(V_ATOM_RANGE_A3[0], V_ATOM_RANGE_A3[1], 5)

    k_perp_bare = k_perp_bare_ev_per_a3()
    k_phonon = K_PHONON_IAPDMN_EV_PER_A3

    rows = []
    for e_flip in e_flip_grid:
        for v_atom in v_atom_grid:
            k_pt = k_phason_pt(e_flip, v_atom)
            k_phason_total = k_perp_bare + k_pt
            ratio_pt_over_phonon = k_pt / k_phonon
            ratio_total_over_phonon = k_phason_total / k_phonon
            rows.append({
                "E_flip_meV": float(e_flip),
                "V_atom_A3": float(v_atom),
                "K_PT_eV_per_A3": float(k_pt),
                "K_perp_bare_eV_per_A3": float(k_perp_bare),
                "K_phason_total_eV_per_A3": float(k_phason_total),
                "K_PT_over_K_phonon": float(ratio_pt_over_phonon),
                "K_phason_total_over_K_phonon": float(ratio_total_over_phonon),
            })

    return rows, k_perp_bare, k_phonon


def verdict(rows):
    """Determine whether sweep reproduces observed K_phason/K_phonon range."""
    pt_over_phonon = [r["K_PT_over_K_phonon"] for r in rows]
    total_over_phonon = [r["K_phason_total_over_K_phonon"] for r in rows]

    pt_min, pt_max = min(pt_over_phonon), max(pt_over_phonon)
    total_min, total_max = min(total_over_phonon), max(total_over_phonon)

    obs_lo = K_PHASON_OVER_PHONON_DE_BOISSIEU_1995
    obs_hi = K_PHASON_OVER_PHONON_FRANCOUAL_2006

    # Check that the sweep covers the observed range.
    covers_de_boissieu = pt_min <= obs_lo <= pt_max
    covers_francoual = pt_min <= obs_hi <= pt_max
    covers_full_obs_range = pt_min <= obs_lo and pt_max >= obs_hi

    # Quarantined: the coverage booleans are arithmetic on a withdrawn
    # comparison and carry no evidential weight in either direction.
    direction = (
        "QUARANTINED: dimensional sweep only. No O.15(b) closure and no "
        "chemical-bonding floor are claimed (App DPS §DPS.4b)."
    )

    framing = (
        f"Quarantined arithmetic: E_flip/V_atom over the historical, unsourced "
        f"box E_flip in [{E_FLIP_RANGE_MEV[0]}, {E_FLIP_RANGE_MEV[1]}] meV and "
        f"V_atom in [{V_ATOM_RANGE_A3[0]}, {V_ATOM_RANGE_A3[1]}] A^3 gives "
        f"dimensionless numbers in [{pt_min:.3e}, {pt_max:.3e}]. The quotient is "
        f"not a phason elastic constant, the formerly cited DFT source (DOI "
        f"10.1103/PhysRevB.88.144102) is a CaIrO3 study, and the de Boissieu 1995 "
        f"/ Francoual 2006 values are K_2/K_1 anisotropy and relaxation kinetics, "
        f"not K_perp/K_parallel. Nothing here supports or tests the Tier 3 P3b "
        f"map phi^(-18) = {PHI_NEG_18:.3e}; reconciliation with alloy data "
        f"first needs the O.41 observable map."
    )

    return {
        "status": "QUARANTINED_NOT_EVIDENCE",
        "direction": direction,
        "framing": framing,
        "K_PT_over_K_phonon_range": [pt_min, pt_max],
        "K_phason_total_over_K_phonon_range": [total_min, total_max],
        "observation_de_boissieu_1995": obs_lo,
        "observation_francoual_2006": obs_hi,
        "covers_de_boissieu": covers_de_boissieu,
        "covers_francoual": covers_francoual,
        "covers_full_observed_range": covers_full_obs_range,
        "bare_phi_18_over_de_boissieu": PHI_NEG_18 / obs_lo,
        "bare_phi_18_over_francoual": PHI_NEG_18 / obs_hi,
    }


def main():
    print("=" * 76)
    print("O.15 QUARANTINED AUDIT: retired Penrose-Toner 'chemical floor' sweep (not evidence)")
    print("=" * 76)

    print(f"\nTier 3 P3b map value (not derived; registered hypothesis):")
    print(f"  phi^(-18)                                 : {PHI_NEG_18:.4e}")

    print(f"\ni-AlPdMn material parameters:")
    print(f"  rho                                       : {RHO_IAPDMN} kg/m^3")
    print(f"  c_L (longitudinal)                        : {C_L_IAPDMN} m/s")
    print(f"  K_phonon = rho c_L^2                      : {K_PHONON_IAPDMN_PA:.3e} Pa")
    print(f"  K_phonon                                  : {K_PHONON_IAPDMN_EV_PER_A3:.3f} eV/A^3")
    print(f"  K_perp_bare = phi^(-18) * K_phonon        : {k_perp_bare_ev_per_a3():.3e} eV/A^3")

    print(f"\nPenrose-Toner sweep:")
    print(f"  E_flip range (historical, unsourced)      : [{E_FLIP_RANGE_MEV[0]}, "
          f"{E_FLIP_RANGE_MEV[1]}] meV")
    print(f"  V_atom range (i-AlPdMn)                   : [{V_ATOM_RANGE_A3[0]}, "
          f"{V_ATOM_RANGE_A3[1]}] A^3")

    rows, k_perp_bare, k_phonon = run_sweep()
    print(f"\n  {'E_flip [meV]':>13}  {'V_atom [A^3]':>13}  {'K_PT/K_phonon':>15}  "
          f"{'K_total/K_phonon':>17}")
    for r in rows:
        print(f"  {r['E_flip_meV']:>13.0f}  {r['V_atom_A3']:>13.1f}  "
              f"{r['K_PT_over_K_phonon']:>15.3e}  "
              f"{r['K_phason_total_over_K_phonon']:>17.3e}")

    v = verdict(rows)
    print(f"\n" + "=" * 76)
    print("QUARANTINED: NO VERDICT FOR O.15 PATH (b)")
    print("=" * 76)
    print(f"  Direction: {v['direction']}")
    print(f"")
    print(f"  E_flip/V_atom quotient range (arithmetic) : "
          f"[{v['K_PT_over_K_phonon_range'][0]:.3e}, "
          f"{v['K_PT_over_K_phonon_range'][1]:.3e}]")
    print("  Comparison with the de Boissieu 1995 / Francoual 2006 values is withdrawn:")
    print("  they are not K_perp/K_parallel (docstring (iii)); no coverage verdict is drawn.")
    print(f"")
    print(f"  Framing: {v['framing']}")
    print("=" * 76)

    output = {
        "protocol": "protocol_o15_phason_stiffness_chemical_correction.py",
        "pass": False,
        "quarantined": True,
        "status": "QUARANTINED_NOT_EVIDENCE",
        "quarantine_reason": (
            "Dimensional sweep only: E_flip/V_atom is not a phason elastic constant; "
            "the cited DFT DOI 10.1103/PhysRevB.88.144102 is Xiao et al. 2013 (CaIrO3); "
            "the i-AlPdMn values are K_2/K_1 anisotropy and relaxation kinetics, not "
            "K_perp/K_parallel. No O.15(b) closure, no chemical floor (App DPS §DPS.4b)."
        ),
        "bare_gct_phi_neg_18": PHI_NEG_18,
        "K_phonon_iAlPdMn_Pa": K_PHONON_IAPDMN_PA,
        "K_phonon_iAlPdMn_eV_per_A3": K_PHONON_IAPDMN_EV_PER_A3,
        "K_perp_bare_eV_per_A3": k_perp_bare,
        "E_flip_range_meV": list(E_FLIP_RANGE_MEV),
        "V_atom_range_A3": list(V_ATOM_RANGE_A3),
        "observation_de_boissieu_1995": K_PHASON_OVER_PHONON_DE_BOISSIEU_1995,
        "observation_francoual_2006": K_PHASON_OVER_PHONON_FRANCOUAL_2006,
        "sweep": rows,
        "verdict": v,
    }
    if OUTPUT_DIR_AVAILABLE:
        out_path = get_output_path("protocol_o15_phason_stiffness_chemical_correction_results.json")
    else:
        out_path = Path(__file__).resolve().parent.parent / "data" / "protocol_o15_phason_stiffness_chemical_correction_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to: {out_path}")
    print("=" * 76)


if __name__ == "__main__":
    main()
