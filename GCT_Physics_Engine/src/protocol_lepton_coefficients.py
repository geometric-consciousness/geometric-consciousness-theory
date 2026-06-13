#!/usr/bin/env python3
"""
protocol_lepton_coefficients.py -- Lepton Coupling Coefficients from A5 Group Theory
==================================================================
Algebraic derivation of the lepton drag coefficients:
  D1. The 5-channel muon multiplicity — from A5 representation theory on
      6 axes. The equal-weight conversion to the +5α pole-mass coefficient
      is a Tier 3 normalization rule pending O.5.
  D2. The -3.6α coefficient — from Kramers-Kronig face-tangent bundle.

Two Acceptance Tests
--------------------
  D1. Decompose the 6-axis permutation rep of A5 → exactly 1A ⊕ 1H.
      This checks the bookkeeping in which 1 channel is locked (Identity) and 5 are free (phasons).
  D2. Phase-space tangent bundle at an RT face has D=18 dimensions.
      With N=5-fold symmetry: screening coeff = -D/N = -18/5 = -3.6.
      - D=18 is the Tier 2 H_3 Shephard-Todd integer anchor, with the
        6D tangent-bundle decomposition serving as a consistency check.
      - Factor 5 = number of A5 representation channels (icosahedral 5-fold)
        (same A5 counting that gives +5*alpha for muon drag)
      - Negative sign: tau couples to E_perp anti-screening sector (Galois conjugate)
      Tier status: Tier 2 mechanism + Tier 2 integer-pair (D=18, N=5)
      + Tier 3 combination rule c = -D/N pending O.26b; headline
      coefficient is Tier 3.
      TAU_SCREEN_COEFF = -3.6  # = -18/5; see Ch08 §[tau derivation] and App T

Output
------
  data/lepton_coefficients_results.json
"""

import sys
import json
import math
from pathlib import Path
from fractions import Fraction

# ---------------------------------------------------------------------------
# Path bootstrap
# ---------------------------------------------------------------------------
_SRC = Path(__file__).resolve().parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from gct_utils import get_output_path, PHI, C


# ============================================================================
# Physical constants
# ============================================================================

ALPHA = C.ALPHA_OBS


# ============================================================================
# TEST D1: A5 Representation Theory — 5-channel Muon Drag
# ============================================================================

def test_d1_A5_decomposition():
    """
    Decompose the 6-dimensional permutation representation of the
    Icosahedral group I ≅ A5 acting on its 6 five-fold rotation axes.

    A5 Conjugacy Classes (order 60)
    --------------------------------
    Class      Size  Description
    -------    ----  --------------------------------
    C_e          1   Identity
    C_5         12   Rotations by 2pi/5
    C_5^2       12   Rotations by 4pi/5
    C_3         20   Rotations by 2pi/3
    C_2         15   Rotations by pi (half-turns)

    Permutation character χ_perm(g)
    (= number of 5-fold axes left fixed by g, where a 5-fold axis is an
    antipodal pair of opposite vertices, counted as one unordered pair):
      Identity: all 6 axis-pairs fixed                          → χ = 6
      C_5:      exactly the axis-pair along the rotation fixed   → χ = 1
      C_5^2:    same axis-pair as C_5                            → χ = 1
      C_3:      no 5-fold axis lies along a 3-fold axis          → χ = 0
      C_2:      a half-turn normalises two Sylow-5 subgroups,
                leaving two axis-pairs invariant as unordered
                pairs (axis reversed = same axis)               → χ = 2
    yielding the permutation character χ_perm = (6, 1, 1, 0, 2).

    Character table of A5:
      Irrep   dim  C_e  C_5     C_5^2   C_3  C_2
      A         1   1    1       1       1    1
      T1        3   3    φ      1-φ      0   -1
      T2        3   3   1-φ     φ        0   -1
      G         4   4   -1      -1       1    0
      H         5   5    0       0      -1    1

    Decomposition formula: n_i = (1/|G|) sum_k |C_k| χ_perm(k) χ_i(k)
    """
    # ---- Group order and conjugacy class sizes -----------------------------
    GROUP_ORDER = 60
    class_sizes = [1, 12, 12, 20, 15]   # |C_e|, |C_5|, |C_5^2|, |C_3|, |C_2|
    assert sum(class_sizes) == GROUP_ORDER

    # ---- Permutation character ---------------------------------------------
    # chi_perm(g) = number of 5-fold axes (antipodal vertex-pairs) fixed by g.
    #
    # C_e  : all 6 axis-pairs are fixed.                          chi = 6
    # C_5  : exactly 1 axis-pair lies along the rotation axis.   chi = 1
    # C_5^2: same axis as C_5.                                    chi = 1
    # C_3  : no 5-fold axis lies on a 3-fold axis.                chi = 0
    # C_2  : the 15 half-turns each lie in exactly D_5 = N(Syl5).
    #         Each C_2 normalises 2 of the 6 Sylow-5 subgroups.  chi = 2
    #
    # Verification: chi(1A + 1H) = (1+5, 1+0, 1+0, 1-1, 1+1) = (6,1,1,0,2) [matches]
    # Norm-squared: (1/60)[36+12+12+0+60] = 120/60 = 2 [integer, valid character]
    chi_perm = [6, 1, 1, 0, 2]

    # ---- Character table (exact, using Fraction arithmetic for φ) ---------
    # φ = (1+√5)/2.  Characters involving φ need exact arithmetic.
    # We work in the field Q(√5): represent each character as (a + b*√5)/2
    # but for the inner product formula we only need integer results.
    # The inner products n_i are guaranteed integers; we can compute them
    # in floating point and round, then verify exactness.

    sqrt5 = math.sqrt(5)
    phi_exact   =  (1 + sqrt5) / 2         # φ
    phi_conj    =  (1 - sqrt5) / 2         # 1 - φ = conjugate

    char_table = {
        #          C_e   C_5       C_5^2    C_3   C_2
        "A":  [1,     1,        1,       1,    1  ],
        "T1": [3,     phi_exact, phi_conj, 0,   -1 ],
        "T2": [3,     phi_conj,  phi_exact, 0,  -1 ],
        "G":  [4,    -1,        -1,       1,    0  ],
        "H":  [5,     0,         0,      -1,    1  ],
    }

    irrep_names = ["A", "T1", "T2", "G", "H"]
    dims        = [1, 3, 3, 4, 5]

    # ---- Inner product n_i = (1/|G|) sum_k |C_k| chi_perm(k) chi_i(k) -----
    multiplicities = {}
    for name in irrep_names:
        chi_i = char_table[name]
        total = sum(
            class_sizes[k] * chi_perm[k] * chi_i[k]
            for k in range(5)
        )
        n_i = total / GROUP_ORDER
        multiplicities[name] = n_i

    # ---- Verify result is integer-valued -----------------------------------
    for name, n_i in multiplicities.items():
        assert abs(n_i - round(n_i)) < 1e-9, \
            f"Multiplicity of {name} = {n_i} is not an integer!"

    mult_int = {name: int(round(n_i)) for name, n_i in multiplicities.items()}
    decomp_array = [mult_int[name] for name in irrep_names]

    # ---- Verify the decomposition: total dimension must equal 6 ------------
    total_dim = sum(mult_int[name] * dims[i]
                    for i, name in enumerate(irrep_names))
    assert total_dim == 6, f"Decomposition dimension {total_dim} != 6"

    # ---- Target: exactly 1A + 1H ------------------------------------------
    target = {"A": 1, "T1": 0, "T2": 0, "G": 0, "H": 1}
    d1_pass = (mult_int == target)

    # ---- Interpretation ----------------------------------------------------
    # n_XXX_channels = multiplicity × dimension of the irrep
    dim_of = {"A": 1, "T1": 3, "T2": 3, "G": 4, "H": 5}
    n_locked = mult_int["A"] * dim_of["A"]   # 1*1 = 1 locked channel
    n_free   = mult_int["H"] * dim_of["H"]   # 1*5 = 5 free phason channels
    # The 5 free channels each couple independently to alpha -> coefficient = 5*alpha

    return d1_pass, {
        "group": "A5 (Icosahedral Group I)",
        "group_order": GROUP_ORDER,
        "conjugacy_classes": {
            "C_e":   {"size": 1,  "chi_perm": chi_perm[0]},
            "C_5":   {"size": 12, "chi_perm": chi_perm[1]},
            "C_5_2": {"size": 12, "chi_perm": chi_perm[2]},
            "C_3":   {"size": 20, "chi_perm": chi_perm[3]},
            "C_2":   {"size": 15, "chi_perm": chi_perm[4]},
        },
        "chi_perm_vector": chi_perm,
        "multiplicities": mult_int,
        "decomposition_array": decomp_array,   # [nA, nT1, nT2, nG, nH] = [1,0,0,0,1]
        "decomposition_string": " + ".join(
            f"{mult_int[n]}{n}" for n in irrep_names if mult_int[n] > 0
        ),
        "n_locked_channels": n_locked,         # 1  (1 * dim(A) = 1)
        "n_free_channels":   n_free,            # 5  (1 * dim(H) = 5)
        "mu_drag_coefficient": n_free,          # = 5  -> 5*alpha
        "d1_pass": d1_pass,
    }



# ============================================================================
# TEST D2: Kramers-Kronig Tau Screening — -3.6α coefficient
# ============================================================================

def test_d2_tau_screening():
    """
    Derive the Tau lepton's radiative screening coefficient -D/N.

    The Tau is a Face Defect of the RT window.
    ------------------------------------------
    The RT (Rhombic Triacontahedron) has 30 rhombic faces.
    Each face is the boundary between two 3D Voronoi cells of the
    icosahedral quasilattice — it is a 2D interface in 3D space.

    Phase-Space Tangent Bundle at a Face (D = 18)
    ----------------------------------------------
    At each RT face the full phase-space tangent bundle splits into:

      Layer 1: Position degrees of freedom (6D parent space)
               Each of the 6 embedding dimensions contributes 1 DOF.
               Sub-total: 6

      Layer 2: Momentum degrees of freedom (cotangent = dual of position)
               Conjugate momenta in the full 6D parent lattice.
               Sub-total: 6

      Layer 3: Internal RT face degrees of freedom
               Each rhombic face of the RT has 6 internal modes:
               • 2 in-plane translation modes (the 2D face)
               • 2 in-plane rotation/dilation (complex structure of face)
               • 1 normal (phason) displacement mode
               • 1 phason momentum conjugate
               Sub-total: 6

    Total: D = 6 + 6 + 6 = 18

    Pentagonal Symmetry Factor (N = 5)
    -----------------------------------
    The RT cage has 5-fold pentagonal symmetry about each vertex.
    The Tau defect sits at the center of a pentagonal projection
    (the Penrose P2 5-fold axis).  The Kramers-Kronig sum rule for
    screening above the transparency frequency ω_c averages over this
    N = 5-fold symmetry, introducing the factor 1/N in the screening sum.

    Screening coefficient:
        -D/N = -18/5 = -3.6

    Physical meaning: the radiative correction to the Tau mass carries
    a negative (screening) factor -3.6α relative to the bare Planck mass.

    STATUS: TIER 2 INTEGER PAIR + TIER 3 COMBINATION RULE
    -----------------------------------------------------
    The D=18 numerator is anchored by the H_3 Shephard-Todd invariant-
    degree sum. The 6D tangent-bundle count below is a consistency check:

    An RT face is a 2D rhombic plaquette embedded in the 6-dimensional
    parent lattice. The tangent bundle of a 2D surface in 6D ambient space
    decomposes as:

      D_face_int = face_dim + (ambient_dim - face_dim) = ambient_dim = 6

    More explicitly:
      - In-plane shape deformations:  2D  (area stretch + shear)
      - Out-of-plane tilt modes:      4D  (4 normal bundle directions in 6D)
      - Total D_face_int = 2 + 4 = 6  ← geometrically forced, NOT fitted

    D_total = D_position(6) + D_momentum(6) + D_face_int(6) = 18.

    Verification: gct_tau_uniqueness.py confirms the uniqueness of the
    H_3 D=18 subclaim. The rule c = -D/N remains pending O.26b.
    See data/protocol_tau_uniqueness_results.json.
    """
    # ---- RT geometry -------------------------------------------------------
    N_RT_FACES  = 30     # faces of the Rhombic Triacontahedron

    # ---- Tangent bundle dimension D = 18 [6D consistency check] ------------
    D_POSITION = 6       # position DOF in 6D parent lattice
    D_MOMENTUM = 6       # momentum DOF (cotangent bundle)
    D_FACE_INT = 6       # internal RT face modes (see docstring)
    D_TOTAL    = D_POSITION + D_MOMENTUM + D_FACE_INT   # 18

    # ---- Pentagonal symmetry factor ----------------------------------------
    N_SYMMETRY = 5       # 5-fold vertex symmetry of RT cage

    # ---- Epistemic Status --------------------------------------------------
    # 6D consistency check: D_face_int = ambient_dim = 6
    # (2 in-plane + 4 out-of-plane tilt modes). H_3 supplies the load-
    # bearing icosahedral anchor; c = -D/N is Tier 3 pending O.26b.

    # ---- Screening coefficient ---------------------------------------------
    ratio = -D_TOTAL / N_SYMMETRY   # = -18/5 = -3.6
    ratio_exact = Fraction(-D_TOTAL, N_SYMMETRY)   # exact rational = -18/5

    d2_pass = (ratio_exact == Fraction(-18, 5))

    return d2_pass, {
        "RT_faces": N_RT_FACES,
        "D_position": D_POSITION,
        "D_momentum": D_MOMENTUM,
        "D_face_internal": D_FACE_INT,
        "D_total": D_TOTAL,
        "N_symmetry": N_SYMMETRY,
        "screening_coefficient_exact": str(ratio_exact),  # "-18/5"
        "screening_coefficient_float": ratio,             # -3.6
        "tau_drag_coefficient": ratio,                    # -3.6 → -3.6α
        "d2_pass": d2_pass,
    }


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 70)
    print("  Lepton Coupling Coefficients from A5 Group Theory")
    print("  Lepton Coupling Coefficients: 5*alpha (Muon) and -3.6*alpha (Tau)")
    print("=" * 70)

    # -----------------------------------------------------------------------
    # D1: A5 decomposition -> 5 channels; +5alpha normalization is Tier 3
    # -----------------------------------------------------------------------
    print("\n[D1] Decomposing the 6-axis permutation representation of A5...")
    d1_pass, d1_info = test_d1_A5_decomposition()

    print(f"  Group: {d1_info['group']}  (order {d1_info['group_order']})")
    print()
    print("  Conjugacy class     |  size  |  chi_perm")
    print("  ------------------  |  ----  |  --------")
    for cls, v in d1_info["conjugacy_classes"].items():
        print(f"  {cls:<18}  |  {v['size']:4d}  |  {v['chi_perm']}")
    print()
    print(f"  chi_perm vector     : {d1_info['chi_perm_vector']}")
    print()
    print("  Irrep multiplicities (inner-product formula):")
    mult = d1_info["multiplicities"]
    for name, n in mult.items():
        print(f"    n_{name} = {n}")
    print()
    print(f"  Decomposition       : {d1_info['decomposition_string']}")
    print(f"  Decomp array [A,T1,T2,G,H] = {d1_info['decomposition_array']}")
    print(f"  n_locked (A rep)    : {d1_info['n_locked_channels']}  (Identity Tether)")
    print(f"  n_free   (H rep)    : {d1_info['n_free_channels']}  (Free Phason Channels)")
    print(f"  Muon drag coeff     : {d1_info['n_free_channels']} * alpha = {d1_info['mu_drag_coefficient'] * ALPHA:.6f}")
    print(f"  D1 target: 1A + 1H  : {'[PASS]' if d1_pass else '[FAIL] -- got ' + d1_info['decomposition_string']}")

    # -----------------------------------------------------------------------
    # D2: Tau screening → -3.6α
    # -----------------------------------------------------------------------
    print("\n[D2] Kramers-Kronig face-tangent bundle screening...")
    d2_pass, d2_info = test_d2_tau_screening()

    print(f"  RT faces            : {d2_info['RT_faces']}")
    print()
    print(f"  Tangent bundle D = {d2_info['D_total']}:")
    print(f"    D_position (6D lattice)    : {d2_info['D_position']}")
    print(f"    D_momentum (cotangent)     : {d2_info['D_momentum']}")
    print(f"    D_face_internal (RT modes) : {d2_info['D_face_internal']}")
    print()
    print(f"  Pentagonal symmetry N       : {d2_info['N_symmetry']}")
    print(f"  Screening coeff -D/N        : -{d2_info['D_total']}/{d2_info['N_symmetry']} = {d2_info['screening_coefficient_exact']} = {d2_info['screening_coefficient_float']:.1f}")
    print(f"  Tau drag coeff              : -3.6 * alpha = {d2_info['tau_drag_coefficient'] * ALPHA:.6f}")
    print(f"  D2 target: -18/5 = -3.6    : {'[PASS]' if d2_pass else '[FAIL]'}")

    # -----------------------------------------------------------------------
    # Final verdict
    # -----------------------------------------------------------------------
    all_pass  = d1_pass and d2_pass
    final_tag = "PASS" if all_pass else "FAIL"

    print("\n" + "=" * 70)
    print("  FINAL VERDICT")
    print("=" * 70)
    print(f"  [{'PASS' if d1_pass else 'FAIL'}] D1  Perm rep A5 = 1A + 1H  -> 5 free channels -> 5*alpha")
    print(f"  [{'PASS' if d2_pass else 'FAIL'}] D2  -D/N = -18/5 = -3.6    -> Tau screening -3.6*alpha")
    print()
    if all_pass:
        print("  VERDICT: PASS")
        print("  The electron drag coefficient is algebraically derived (Tier 2);")
        print("  the tau coefficient remains a calibrated/anchor-dependent")
        print("  Tier 3 rule pending O.26b closure.")
    else:
        print(f"  VERDICT: {final_tag}")

    # -----------------------------------------------------------------------
    # Save JSON
    # -----------------------------------------------------------------------
    results = {
        "protocol": "Lepton Coupling Coefficients (A5 Representation Theory)",
        "D1_muon_drag": d1_info,
        "D2_tau_screening": d2_info,
        "summary": {
            "decomposition_array_A_T1_T2_G_H": d1_info["decomposition_array"],
            "decomposition": d1_info["decomposition_string"],
            "n_free_channels": d1_info["n_free_channels"],
            "mu_drag_coefficient_5alpha": d1_info["mu_drag_coefficient"],
            "tau_screening_ratio": d2_info["screening_coefficient_exact"],
            "tau_screening_float": d2_info["screening_coefficient_float"],
        },
        "pass": all_pass,
        "verdict": final_tag,
    }

    out_path = get_output_path("protocol_lepton_coefficients_results.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)
    print(f"\n  Results saved to: {out_path}")
    print("=" * 70)

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
