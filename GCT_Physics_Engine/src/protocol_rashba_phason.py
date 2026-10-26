#!/usr/bin/env python3
"""
protocol_rashba_phason.py — Rashba-Phason Coupling Field-Typing Audit
=====================================================================
Representation-theory audit and energy-scale arithmetic for the candidate
Rashba-Phason coupling Hamiltonian of V1 Ch17 Eq. (17.3),

    H_RP = alpha_R * sum_j (d_j Phi_perp) * eps_jkl * k_k * sigma_l.

The audit computes, from the character table of the rotational icosahedral
group A5, the multiplicity of the trivial representation in the tensor
product that Eq. (17.3) contracts:

  * vector phason (E_perp ~ 3'): strain d_i u_perp^a lies in 3 (x) 3', and
    the cross product eps_jkl k_k sigma_l lies in Lambda^2(3) ~ 3. An
    A5-invariant coupling of this form exists iff mult_1[(3 (x) 3') (x) 3] > 0.
  * scalar phason (effective field model): the gradient lies in 3, and an
    invariant exists iff mult_1[3 (x) 3] > 0.

The computed multiplicities (0 for the vector phason, 1 for a scalar field)
reproduce the Tier 1 field-typing analysis of V1 Ch17 §17.1.3: Eq. (17.3) is not
an icosahedral scalar for the vector phason used elsewhere in GCT. The coupling
form, sign and magnitude are therefore Tier 3/open, and this protocol reports
a non-PASS verdict (COUPLING_FORM_NOT_A5_SCALAR) by design.

The energy-scale ratio E_RP / k_B T uses declared Tier 3 inputs (alpha_R,
k_F, phason gradient); it is arithmetic on assumed values, not a test.
"""

import json
import math
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from gct_utils import get_output_path, C

PHI = float(C.PHI)

# A5 conjugacy classes: identity, 15 double transpositions, 20 three-cycles,
# 12 five-cycles of type A, 12 five-cycles of type B (rotations by 2pi/5 and 4pi/5).
CLASS_SIZES = [1, 15, 20, 12, 12]
# Class of g^2 for each class (index map): e->e, (2,2)->e, 3->3, 5A->5B, 5B->5A.
SQUARE_CLASS = [0, 0, 2, 4, 3]
CHI = {
    "1": [1.0, 1.0, 1.0, 1.0, 1.0],
    "3": [3.0, -1.0, 0.0, PHI, 1.0 - PHI],
    "3p": [3.0, -1.0, 0.0, 1.0 - PHI, PHI],
}


def _lambda2(chi):
    """Character of the antisymmetric square: (chi(g)^2 - chi(g^2)) / 2."""
    return [(chi[c] ** 2 - chi[SQUARE_CLASS[c]]) / 2.0 for c in range(5)]


def _mult_trivial(*chis):
    """Multiplicity of the trivial representation in the tensor product."""
    order = sum(CLASS_SIZES)
    total = 0.0
    for c, size in enumerate(CLASS_SIZES):
        prod = 1.0
        for chi in chis:
            prod *= chi[c]
        total += size * prod
    return total / order


def field_typing_audit() -> dict:
    lam2_3 = _lambda2(CHI["3"])
    # Sanity: Lambda^2(3) is the 3 itself for SO(3)-type vectors.
    lam2_is_3 = all(abs(a - b) < 1e-12 for a, b in zip(lam2_3, CHI["3"]))
    mult_vector = _mult_trivial(CHI["3"], CHI["3p"], lam2_3)
    mult_scalar = _mult_trivial(CHI["3"], lam2_3)
    return {
        "lambda2_of_3_equals_3": lam2_is_3,
        "mult_trivial_vector_phason_(3x3')x3": round(mult_vector, 12) + 0.0,
        "mult_trivial_scalar_phason_3x3": round(mult_scalar, 12) + 0.0,
        "eq_17_3_is_A5_scalar_for_vector_phason": bool(round(mult_vector) > 0),
        "eq_17_3_is_A5_scalar_for_scalar_field": bool(round(mult_scalar) > 0),
    }


def energy_scale_arithmetic() -> dict:
    # Declared Tier 3 inputs (not measured for the Trp pocket).
    alpha_R_typ = 0.3    # eV*Ang (Rashba-scale placeholder)
    k_F = 1.0            # Ang^-1
    grad_Phi_bio = 1.0   # Ang^-1 (assumed phason gradient at molecular scale)
    E_RP = alpha_R_typ * k_F * grad_Phi_bio  # eV
    k_B_eV_per_K = 8.617333262145e-5
    T_body_K = 310.0
    kBT = k_B_eV_per_K * T_body_K
    return {
        "alpha_R_typical_eV_Ang": alpha_R_typ,
        "E_RP_eV": float(E_RP),
        "T_body_K": T_body_K,
        "kBT_310K_eV": float(kBT),
        "E_RP_over_kBT": float(E_RP / kBT),
        "status": "arithmetic on declared Tier 3 inputs; not a test",
    }


def run() -> dict:
    audit = field_typing_audit()
    scale = energy_scale_arithmetic()
    form_ok = audit["eq_17_3_is_A5_scalar_for_vector_phason"]
    verdict = "PASS" if form_ok else "COUPLING_FORM_NOT_A5_SCALAR"
    return {
        "protocol": "protocol_rashba_phason",
        "hamiltonian_form": "H_RP = alpha_R * sum_j (d_j Phi_perp) * eps_jkl * k_k * sigma_l",
        "field_typing_audit": audit,
        "energy_scale": scale,
        "pass": bool(form_ok),
        "verdict": verdict,
        "tier": "Tier 1 field-typing analysis (computed); coupling form, sign and magnitude Tier 3/open",
    }


def main() -> int:
    print("=" * 65)
    print("  GCT Protocol — Rashba-Phason Coupling Field-Typing Audit")
    print("=" * 65)
    results = run()
    a = results["field_typing_audit"]
    print(f"  Lambda^2(3) = 3                                : {a['lambda2_of_3_equals_3']}")
    print(f"  mult_1[(3 x 3') x 3]  (vector phason)          : {a['mult_trivial_vector_phason_(3x3\')x3']:.0f}")
    print(f"  mult_1[3 x 3]          (scalar field model)     : {a['mult_trivial_scalar_phason_3x3']:.0f}")
    s = results["energy_scale"]
    print(f"  E_RP / k_B T (declared Tier 3 inputs)          : {s['E_RP_over_kBT']:.2f}")
    out = get_output_path("protocol_rashba_phason_results.json")
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  VERDICT: {results['verdict']} (Eq. 17.3 is not an A5 scalar for the vector phason; coupling Tier 3/open)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
