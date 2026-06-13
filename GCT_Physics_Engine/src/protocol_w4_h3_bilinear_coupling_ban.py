"""
App W Sec W.4 No-Signalling Theorem — H_3 character-theoretic selection rules
=============================================================================

Computes the two selection rules that govern phonon–phason couplings in the
icosahedral H_3 effective theory of E_parallel (phonon u_||) + E_perp (phason
u_perp) fields. The phonon displacement transforms as the vector irrep T_1 and
the phason displacement as the Galois-conjugate irrep T_2 (these are the two
inequivalent 3-dimensional irreps of I, related by the Q(sqrt(5)) automorphism
phi -> 1 - phi; standard quasicrystal identification — Senechal 1995 §2.5,
Janssen et al. 2018 §6.3).

Two distinct bilinear couplings exist a priori:

  (i) Displacement-level mixing  M_ij u_||^i u_perp^j
      --> coupling tensor lives in (T_1 (x) T_2)
      --> exists iff n_A(T_1 (x) T_2) > 0.

  (ii) Strain-level mixing  C_ijkl epsilon_ij w_kl,
       with epsilon_ij = ∂_i u_||^j  in T_1 (x) T_1,
            w_kl       = ∂_k u_perp^l in T_1 (x) T_2,
       --> coupling tensor lives in (T_1 (x) T_1) (x) (T_1 (x) T_2)
       --> exists iff n_A((T_1 (x) T_1) (x) (T_1 (x) T_2)) > 0.

The two selection rules answer DIFFERENT physical questions: (i) bans a
mass-like algebraic mixing of phonon and phason amplitudes; (ii) governs the
standard SLS / LRT strain-strain coupling K_3 of icosahedral quasicrystal
elasticity (Socolar, Lubensky & Steinhardt 1986; Lubensky, Ramaswamy & Toner
1985), which is the same C^{mix}_ijkl term that appears in App M Sec M.4.

This protocol computes both multiplicities, identifies which sub-product of
the rank-4 decomposition carries the strain-strain invariant, and reports the
explicit selection-rule structure that the no-signalling argument in App W Sec
W.4 rests on. The closure of Theorem W.1 then proceeds:

  - Step 1: only the strain-strain K_3 coupling survives; the displacement-
            level coupling is forbidden by the displacement-level selection
            rule  n_A(T_1 (x) T_2) = 0.
  - Step 2: a phason source drives the phonon equation through the K_3 term;
            the resulting signal in E_|| propagates at phonon speed v <= c
            (Lorentz invariance of the long-wavelength effective theory).
  - Step 3: p-adic proximity is not E_|| proximity (Realization Operator).

Theorem W.1 (No Superluminal Signalling via p-adic Proximity) therefore
operates at Tier 2: Step 1 is Tier 1 (group-theoretic), Step 2 is Tier 2
(standard relativistic field-theory fact), Step 3 is Tier 1 (cut-and-project).
The load-bearing physical input is Step 2's subluminal phonon propagation.

Character table of I (Hamermesh 1962 Table III.1):

  Rep    | E   | 12C_5     | 12C_5^2    | 20C_3 | 15C_2 |
  -------|-----|-----------|------------|-------|-------|
  A      |  1  |  1        |  1         |  1    |  1    |
  T_1    |  3  |  phi      |  1 - phi   |  0    | -1    |  (vector rep)
  T_2    |  3  |  1 - phi  |  phi       |  0    | -1    |  (Galois conjugate)
  G      |  4  | -1        | -1         |  1    |  0    |
  H      |  5  |  0        |  0         | -1    |  1    |

Standard decompositions (consistency-checked numerically below):
  T_1 (x) T_1 = A + T_1 + H
  T_2 (x) T_2 = A + T_2 + H
  T_1 (x) T_2 = G + H        (no A --> displacement coupling forbidden)
  (T_1 (x) T_1) (x) (T_1 (x) T_2) contains A with multiplicity 1
                                (from the H (x) H sub-product --> K_3 allowed)

Cross-reference: App W Sec W.4 (No-Signalling Theorem);
App M Sec M.4 (phonon-phason coupling structure); App E Sec E.4
(no-signalling proposition at the foundational-theorems level).
"""

from __future__ import annotations

import math
import json
from pathlib import Path
try:
    from gct_utils import C
    _PHI_FROM_SSOT = float(C.PHI)
except ImportError:
    _PHI_FROM_SSOT = (1.0 + math.sqrt(5.0)) / 2.0


PHI = _PHI_FROM_SSOT
# Columns indexed by conjugacy classes: [E, 12C_5, 12C_5^2, 20C_3, 15C_2].
CLASS_SIZES = [1, 12, 12, 20, 15]
GROUP_ORDER = sum(CLASS_SIZES)  # = 60

CHARACTER_TABLE = {
    "A":   [1.0, 1.0,        1.0,        1.0,  1.0],
    "T_1": [3.0, PHI,        1.0 - PHI,  0.0, -1.0],
    "T_2": [3.0, 1.0 - PHI,  PHI,        0.0, -1.0],
    "G":   [4.0, -1.0,       -1.0,       1.0,  0.0],
    "H":   [5.0, 0.0,        0.0,       -1.0,  1.0],
}

REP_DIMENSIONS = {name: chars[0] for name, chars in CHARACTER_TABLE.items()}


def tensor_product_character(chi_a, chi_b):
    return [a * b for a, b in zip(chi_a, chi_b)]


def inner_product_with_irrep(chi_product, chi_irrep):
    return sum(c * x_r * x_p for c, x_r, x_p
               in zip(CLASS_SIZES, chi_irrep, chi_product)) / GROUP_ORDER


def decompose(chi_product):
    return {name: round(inner_product_with_irrep(chi_product, chi), 12)
            for name, chi in CHARACTER_TABLE.items()}


def dimension_check(decomposition, expected):
    total = sum(decomposition[name] * REP_DIMENSIONS[name]
                for name in decomposition)
    return {
        "expected_dimension": expected,
        "sum_of_multiplicities_times_dims": total,
        "matches": abs(total - expected) < 1e-10,
    }


def compute():
    chi_T1 = CHARACTER_TABLE["T_1"]
    chi_T2 = CHARACTER_TABLE["T_2"]
    chi_T1xT1 = tensor_product_character(chi_T1, chi_T1)
    chi_T2xT2 = tensor_product_character(chi_T2, chi_T2)
    chi_T1xT2 = tensor_product_character(chi_T1, chi_T2)
    chi_strain_strain = tensor_product_character(chi_T1xT1, chi_T1xT2)

    decomp_T1xT1 = decompose(chi_T1xT1)
    decomp_T2xT2 = decompose(chi_T2xT2)
    decomp_T1xT2 = decompose(chi_T1xT2)
    decomp_strain_strain = decompose(chi_strain_strain)

    # Displacement-level selection rule (rank-2 tensor).
    n_A_displacement = decomp_T1xT2["A"]

    # Strain-level selection rule (rank-4 tensor).
    n_A_strain_strain = decomp_strain_strain["A"]

    # Identify which sub-product of (T_1 (x) T_1) carries the strain-strain
    # invariant. Using T_1 (x) T_1 = A + T_1 + H and T_1 (x) T_2 = G + H, the
    # only A-containing tensor product of the irrep summands is H (x) H, since
    # H (x) H contains A with multiplicity 1.
    chi_HxH = tensor_product_character(CHARACTER_TABLE["H"], CHARACTER_TABLE["H"])
    n_A_HxH = round(inner_product_with_irrep(chi_HxH, CHARACTER_TABLE["A"]), 12)

    return {
        "group": "I (icosahedral proper rotation, |I|=60)",
        "character_table_source": "Hamermesh 1962 Table III.1",
        "phi_value": PHI,
        "phonon_rep": "T_1 (vector representation, 3D)",
        "phason_rep": "T_2 (Galois conjugate of T_1, 3D)",

        "displacement_level_selection_rule": {
            "coupling_form": "M_ij u_parallel^i u_perp^j",
            "coupling_tensor_lives_in": "T_1 (x) T_2",
            "character_of_T1_x_T2": chi_T1xT2,
            "decomposition_T1_x_T2": decomp_T1xT2,
            "n_A": n_A_displacement,
            "coupling_allowed": (abs(n_A_displacement) > 1e-10),
            "interpretation": (
                "No H_3-invariant displacement-displacement coupling "
                "exists. A mass-like algebraic mixing of phonon and "
                "phason amplitudes is forbidden by icosahedral symmetry."),
        },

        "strain_level_selection_rule": {
            "coupling_form": (
                "C^{mix}_ijkl epsilon_ij w_kl, with "
                "epsilon_ij = ∂_i u_parallel^j (in T_1 (x) T_1) and "
                "w_kl = ∂_k u_perp^l (in T_1 (x) T_2)"),
            "coupling_tensor_lives_in": "(T_1 (x) T_1) (x) (T_1 (x) T_2)",
            "T_1_x_T_1_decomposition": decomp_T1xT1,
            "T_1_x_T_2_decomposition": decomp_T1xT2,
            "character_of_full_product": chi_strain_strain,
            "decomposition_full_product": decomp_strain_strain,
            "n_A": n_A_strain_strain,
            "coupling_allowed": (abs(n_A_strain_strain) > 1e-10),
            "carrying_sub_product": "H (x) H",
            "n_A_in_H_x_H": n_A_HxH,
            "physical_identification": (
                "This is the standard Socolar-Lubensky-Steinhardt / "
                "Lubensky-Ramaswamy-Toner K_3 coupling of icosahedral "
                "quasicrystal elasticity, identical to the C^{mix}_ijkl "
                "term of App M Sec M.4."),
            "interpretation": (
                "Exactly one H_3-invariant strain-strain coupling exists. "
                "A phason source drives the phonon equation through "
                "this K_3 term; the induced disturbance propagates at "
                "phonon speed and is therefore subluminal."),
        },

        "self_coupling_consistency_checks": {
            "T_1_x_T_1_decomposition": decomp_T1xT1,
            "T_2_x_T_2_decomposition": decomp_T2xT2,
            "T_1_x_T_1_contains_A": (abs(decomp_T1xT1["A"]) > 1e-10),
            "T_2_x_T_2_contains_A": (abs(decomp_T2xT2["A"]) > 1e-10),
            "interpretation": (
                "Self-products T_1 (x) T_1 = A + T_1 + H and "
                "T_2 (x) T_2 = A + T_2 + H each contain A with "
                "multiplicity 1 — phonon-phonon and phason-phason "
                "self-couplings are allowed at linear order."),
        },

        "dimension_consistency_checks": {
            "T_1_x_T_2_dim": dimension_check(decomp_T1xT2, 9.0),
            "T_1_x_T_1_dim": dimension_check(decomp_T1xT1, 9.0),
            "T_2_x_T_2_dim": dimension_check(decomp_T2xT2, 9.0),
            "strain_strain_dim": dimension_check(decomp_strain_strain, 81.0),
        },

        "no_signalling_closure": {
            "tier": "Tier 2",
            "step_1_tier": "Tier 1 (group-theoretic; both selection rules above)",
            "step_2_tier": (
                "Tier 2 (standard relativistic field-theory fact: phonon "
                "sound speed is bounded above by c via Lorentz invariance "
                "of the long-wavelength effective theory)"),
            "step_3_tier": "Tier 1 (Realization Operator projection)",
            "load_bearing_step": (
                "Step 2 (subluminality of the phonon sector). Step 1 "
                "establishes the selection-rule structure of the coupling "
                "and identifies the K_3 strain-strain term as the unique "
                "channel through which a phason source can drive E_||; "
                "Step 2 then closes the no-signalling argument by bounding "
                "the propagation speed of that channel."),
        },
    }


def main():
    results = compute()
    out_dir = Path(__file__).parent.parent / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "w4_h3_bilinear_coupling_ban.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    disp = results["displacement_level_selection_rule"]
    strain = results["strain_level_selection_rule"]
    closure = results["no_signalling_closure"]

    print("App W Sec W.4 H_3 selection rules for phonon-phason couplings")
    print("=" * 65)
    print(f"Group: {results['group']}")
    print(f"phi = {results['phi_value']:.10f}")
    print()
    print("Displacement-level coupling  M_ij u_||^i u_perp^j:")
    print(f"  coupling tensor in {disp['coupling_tensor_lives_in']}")
    print(f"  T_1 (x) T_2 decomposition: {disp['decomposition_T1_x_T2']}")
    print(f"  n_A = {disp['n_A']}  -->  coupling allowed: {disp['coupling_allowed']}")
    print()
    print("Strain-level coupling  C^{mix}_ijkl eps_ij w_kl:")
    print(f"  coupling tensor in {strain['coupling_tensor_lives_in']}")
    print(f"  T_1 (x) T_1 = {strain['T_1_x_T_1_decomposition']}")
    print(f"  T_1 (x) T_2 = {strain['T_1_x_T_2_decomposition']}")
    print(f"  n_A = {strain['n_A']}  -->  coupling allowed: {strain['coupling_allowed']}")
    print(f"  carrying sub-product: {strain['carrying_sub_product']}")
    print(f"  --> identification: K_3 SLS / LRT strain-strain coupling")
    print()
    print(f"No-signalling theorem tier: {closure['tier']}")
    print(f"  Step 1 (selection rules)       : {closure['step_1_tier']}")
    print(f"  Step 2 (subluminal propagation): {closure['step_2_tier']}")
    print(f"  Step 3 (R-Operator projection) : {closure['step_3_tier']}")
    print()
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
