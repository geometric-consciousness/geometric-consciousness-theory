#!/usr/bin/env python3
"""
GCT Protocol: Phason Stiffness Ratio
Filename: protocol_stiffness_ratio.py

This protocol checks two things:

  1. The integer anchor D = 18, computed from Coxeter matrices and
     Coxeter-element eigenphases (H3 degrees 2 + 6 + 10). H3 is unique among
     finite irreducible rank-three Coxeter systems with this sum; the reducible
     A1 x I2(14) also gives 18. This is the Tier 2 integer identification and
     the part of the check that could fail.
  2. The raw-frame Gram-determinant ratio det(G_perp)/det(G_para) = phi^-6 and
     its cube phi^-18. This is coordinate arithmetic in the unnormalized frame:
     it scales as s^18 under an internal rescaling, and the canonical isometric
     projectors (and the isotropic action) give 1. It is therefore NOT a
     derivation of the phason-to-phonon stiffness ratio; the former Gram-cube
     route is retired (App DPS §DPS.3).

The physical map K_perp/K_parallel = phi^-18 is the Tier 3 P3b hypothesis
(O.15(b)), registered outside the count like H-EW (Parameter Ledger §0.1).
"""

import numpy as np
import json
import os
from gct_utils import GCTReporter, PHI, get_output_path


def coxeter_matrix(edge_labels):
    """Return the Coxeter matrix for a linear diagram with given edge labels."""
    rank = len(edge_labels) + 1
    matrix = np.full((rank, rank), 2, dtype=int)
    np.fill_diagonal(matrix, 1)
    for i, label in enumerate(edge_labels):
        matrix[i, i + 1] = label
        matrix[i + 1, i] = label
    return matrix


def invariant_degrees_from_coxeter_matrix(matrix):
    """Compute invariant degrees as Coxeter-element exponents plus one.

    The geometric representation uses the simple-root Gram matrix
    ``B_ij = -cos(pi/m_ij)``.  The order and eigenphases of the product of
    simple reflections determine the Coxeter number and exponents.  No
    invariant degree is supplied as input.
    """
    rank = matrix.shape[0]
    gram = np.eye(rank)
    for i in range(rank):
        for j in range(i + 1, rank):
            gram[i, j] = gram[j, i] = -np.cos(np.pi / matrix[i, j])

    reflections = []
    for i in range(rank):
        reflection = np.eye(rank)
        reflection[i, :] -= 2.0 * gram[i, :]
        reflections.append(reflection)

    element = np.eye(rank)
    for reflection in reflections:
        element = element @ reflection

    power = np.eye(rank)
    coxeter_number = None
    for candidate_order in range(1, 1001):
        power = power @ element
        if np.allclose(power, np.eye(rank), atol=1e-9, rtol=0.0):
            coxeter_number = candidate_order
            break
    if coxeter_number is None:
        raise ValueError("Coxeter element order exceeds the finite-search bound")

    phases = np.mod(np.angle(np.linalg.eigvals(element)), 2.0 * np.pi)
    exponents = sorted(
        int(round(phase * coxeter_number / (2.0 * np.pi))) % coxeter_number
        for phase in phases
    )
    if 0 in exponents:
        raise ValueError("Unexpected zero exponent in a finite irreducible component")
    return tuple(exponent + 1 for exponent in exponents), coxeter_number


def rank_three_coxeter_enumeration(target_value):
    """Enumerate the complete finite real Coxeter classification at rank three.

    The irreducible systems are A3, B3 and H3.  The reducible systems are
    A1^3 and the infinite family A1 x I2(m), m >= 3.  For the family, the
    component degree sum is 2 + (2 + m) = m + 4, so its target-value member
    is solved exactly rather than selected by a finite ad hoc cutoff.
    """
    component_matrices = {
        "A1": coxeter_matrix(()),
        "A3": coxeter_matrix((3, 3)),
        "B3": coxeter_matrix((4, 3)),
        "H3": coxeter_matrix((5, 3)),
    }
    component_data = {
        name: invariant_degrees_from_coxeter_matrix(matrix)
        for name, matrix in component_matrices.items()
    }

    irreducible = {
        name: component_data[name][0] for name in ("A3", "B3", "H3")
    }
    reducible = {
        "A1 x A1 x A1": component_data["A1"][0] * 3,
    }

    family_parameter = target_value - 4
    if family_parameter >= 3:
        i2_matrix = coxeter_matrix((family_parameter,))
        i2_degrees, _ = invariant_degrees_from_coxeter_matrix(i2_matrix)
        reducible[f"A1 x I2({family_parameter})"] = tuple(
            sorted(component_data["A1"][0] + i2_degrees)
        )

    degree_sums = {
        name: sum(degrees) for name, degrees in {**irreducible, **reducible}.items()
    }
    return {
        "irreducible": irreducible,
        "reducible": reducible,
        "degree_sums": degree_sums,
        "component_coxeter_numbers": {
            name: component_data[name][1] for name in component_data
        },
        "reducible_family": "A1 x I2(m), m >= 3, degrees (2, 2, m), sum m + 4",
    }


def verify_d18_integer_anchor(reporter):
    """
    Compute the H3 invariant-degree sum and delimit its uniqueness correctly.

    H3 is the unique finite irreducible rank-three Coxeter system with degree
    sum 18.  It is not unique among all finite rank-three Coxeter systems:
    A1 x I2(14) has degrees (2, 2, 14) and the same sum.  The degrees below are
    computed from Coxeter matrices and Coxeter-element eigenphases.
    """
    reporter.section("D=18 Coxeter Integer Anchor Check")

    target_value = 18
    enumeration = rank_three_coxeter_enumeration(target_value)
    invariant_degrees = {
        **enumeration["irreducible"], **enumeration["reducible"]
    }
    degree_sums = enumeration["degree_sums"]
    for group, degrees in invariant_degrees.items():
        reporter.log_value(
            f"{group} invariant degrees {degrees} sum", degree_sums[group]
        )

    d_representation = degree_sums["H3"]
    reporter.log_comparison("Expected D=18", d_representation, target_value)

    irreducible_attaining = [
        group for group in enumeration["irreducible"]
        if degree_sums[group] == target_value
    ]
    all_attaining = [
        group for group, total in degree_sums.items() if total == target_value
    ]
    irreducible_unique = irreducible_attaining == ["H3"]
    reducible_counterexample_present = "A1 x I2(14)" in all_attaining
    reporter.log_value(
        "Finite irreducible systems attaining 18", ", ".join(irreducible_attaining)
    )
    reporter.log_value(
        "All finite rank-three systems attaining 18", ", ".join(all_attaining)
    )
    reporter.log_value("Reducible family", enumeration["reducible_family"])

    # Consistency mnemonic only; not the verification.
    mnemonic = 3 * 2 * 3
    reporter.log_value("rank x Galois degree x generators (mnemonic)", mnemonic)

    phi_18 = PHI**(-18)
    reporter.log_value("phi^-18 numeric value", phi_18)

    d18_pass = (
        d_representation == target_value
        and irreducible_unique
        and reducible_counterexample_present
    )
    if d18_pass:
        print(
            "D=18 anchor verified: H3 invariant degrees 2+6+10 = 18, unique among "
            "finite irreducible rank-three Coxeter systems (A3 = 9, B3 = 12). "
            "The numerical sum is not unique among all finite rank-three systems: "
            "A1 x I2(14) also gives 2+2+14 = 18. The H3 identification is Tier 2 "
            "conditional on the irreducible icosahedral premise; the phason-elastic "
            "RG-map link remains Tier 3 / O.15."
        )

    return d18_pass, d_representation, enumeration, all_attaining

def compute_stiffness_ratio():
    reporter = GCTReporter("Phason Stiffness Ratio Verification")
    
    # 1. Define Projection Matrices (AKN Canonical 3x6)
    # These are the canonical projection vectors (unnormalized)
    # satisfying det(G_perp)/det(G_para) = phi^-6
    p = PHI
    
    # M_parallel
    m_para = np.array([
        [1, p, 0, -1, p, 0],
        [p, 0, 1, p, 0, -1],
        [0, 1, p, 0, -1, p]
    ])
    
    # M_perp (Galois conjugate p' = -1/p)
    ip = -1.0 / p
    m_perp = np.array([
        [1, ip, 0, -1, ip, 0],
        [ip, 0, 1, ip, 0, -1],
        [0, 1, ip, 0, -1, ip]
    ])

    reporter.section("Matrix Verification")
    reporter.log_value("M_parallel Shape", m_para.shape)
    reporter.log_value("M_perp Shape", m_perp.shape)
    
    # 2. Compute Gram Matrices
    g_para = m_para @ m_para.T
    g_perp = m_perp @ m_perp.T
    
    det_para = np.linalg.det(g_para)
    det_perp = np.linalg.det(g_perp)
    
    reporter.log_value("det(G_parallel)", det_para)
    reporter.log_value("det(G_perp)", det_perp)
    
    # 3. Ratio Analysis
    det_ratio = det_perp / det_para
    predicted_det_ratio = PHI**(-6)
    
    reporter.section("Determinant Ratio Verification")
    reporter.log_comparison("det(G_perp)/det(G_para)", det_ratio, predicted_det_ratio)
    
    # 4. Final Stiffness Suppression (3D Volume Scaling)
    stiffness_ratio = det_ratio**3
    target_ratio = PHI**(-18)
    
    reporter.section("Raw-frame Gram cube (frame-dependent; not a stiffness derivation)")
    reporter.log_comparison("(det G_perp / det G_para)^3", stiffness_ratio, target_ratio)
    
    # 5. D=18 integer-anchor verification
    d18_pass, d_val, coxeter_enumeration, d18_attaining = verify_d18_integer_anchor(
        reporter
    )
    
    # Verdict
    is_passed = abs(stiffness_ratio - target_ratio) < 1e-10 and d18_pass
    reporter.verdict(
        is_passed,
        "D=18 is a Tier 2 H3 integer identification conditional on the "
        "irreducible icosahedral premise; the raw-frame Gram cube equals "
        "phi^-18 only in the unnormalized frame and derives no stiffness; the "
        "phi^-18 stiffness map is the Tier 3 P3b hypothesis (O.15(b))."
    )
    
    # Output JSON
    output = {
        "protocol": "protocol_stiffness_ratio.py",
        "pass": bool(is_passed),
        "tier_discipline": "Tier 2 H3 integer identification conditional on the irreducible icosahedral premise + Tier 3 P3b stiffness map pending O.15(b); the raw-frame Gram ratio is frame-dependent coordinate arithmetic, not a stiffness derivation",
        "tier_2_integer_anchor_check": "PASS" if d18_pass else "FAIL",
        "d18_rg_counting": int(d_val),
        "rank_three_coxeter_enumeration": {
            "irreducible": {
                name: list(degrees)
                for name, degrees in coxeter_enumeration["irreducible"].items()
            },
            "reducible_cases_checked": {
                name: list(degrees)
                for name, degrees in coxeter_enumeration["reducible"].items()
            },
            "reducible_family": coxeter_enumeration["reducible_family"],
            "systems_attaining_d18": d18_attaining,
            "uniqueness_scope": "H3 is unique only within finite irreducible rank-three Coxeter systems",
        },
        "det_ratio": float(det_ratio),
        "stiffness_ratio": float(stiffness_ratio),
        "target_ratio": float(target_ratio),
        "phi": float(PHI)
    }
    
    output_path = get_output_path("protocol_stiffness_ratio_results.json")
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)
    
    return is_passed

if __name__ == "__main__":
    compute_stiffness_ratio()
