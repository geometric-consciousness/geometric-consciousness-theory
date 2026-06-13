"""
verify_stiffness_ratio.py — Phason stiffness ratio η_stiff = K_⊥/K_∥ = φ⁻¹⁸.

INDEPENDENCE SCOPE: This verifier is NOT fully independent. Unlike the
CODATA/PDG-only scripts in this directory, it imports engine geometry
from src/ (`gct_projections` for the AKN projection matrices). Its
agreement with App K is therefore a CONSISTENCY CHECK against the engine's
own projection construction, not an independent corroboration of the
stiffness ratio. (See README "independence contract"; the fully
CODATA/PDG-anchored scripts in this directory carry the independence claim.)

App K §K.4 (Parameter Ledger §2):
 "K_⊥/K_∥ ≈ (det(G_⊥)/det(G_∥))³ = (φ⁻⁶)³ = φ⁻¹⁸"
 Tier 2: exponent D=18 = H_3 invariant-degree sum (Coxeter rep over Q(√5))
 Tier 2: identification of K with elastic phason stiffness sector

This verifier:
 (1) Computes det(G_⊥)/det(G_∥) from the canonical AKN projection
 matrices and verifies it equals φ⁻⁶ exactly.
 (2) Cubes the ratio and confirms K_⊥/K_∥ = φ⁻¹⁸ ≈ 1.731 × 10⁻⁴.
 (3) Confirms the lattice speed of light c = sqrt(K_⊥/K_∥) = φ⁻⁹.

This is structurally similar to the A.2 (Weinberg φ⁻³ uniqueness)
audit: the exponent follows from composition of independent geometric
inputs (Gram-determinant ratio + cube-power dimension argument), a Tier 2
geometric result.
"""

import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import MATH
from report import make_result, write_result, print_summary

import numpy as np


def main():
 phi = MATH.PHI

 # Step 1: Compute det(G_⊥)/det(G_∥) from the unnormalised projection matrices
 # (the chapter's claim uses the determinant RATIO, which is convention-independent)
 sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
 from gct_projections import get_m_parallel_unnormalized, get_m_perp_unnormalized
 M_para = get_m_parallel_unnormalized()
 M_perp = get_m_perp_unnormalized()
 G_para = M_para @ M_para.T
 G_perp = M_perp @ M_perp.T
 det_para = np.linalg.det(G_para)
 det_perp = np.linalg.det(G_perp)
 det_ratio = det_perp / det_para
 expected_det_ratio = phi ** (-6)
 det_ratio_match = abs(det_ratio - expected_det_ratio) / abs(expected_det_ratio)

 # Step 2: Cube the ratio → K_⊥/K_∥
 K_ratio = det_ratio ** 3
 expected_K_ratio = phi ** (-18)
 K_ratio_match = abs(K_ratio - expected_K_ratio) / abs(expected_K_ratio)

 # Step 3: Lattice speed of light c_lattice = sqrt(K_⊥/K_∥)
 c_lattice = math.sqrt(K_ratio)
 expected_c_lattice = phi ** (-9)
 c_lattice_match = abs(c_lattice - expected_c_lattice) / abs(expected_c_lattice)

 # All within machine precision
 all_match = (
 det_ratio_match < 1e-10
 and K_ratio_match < 1e-10
 and c_lattice_match < 1e-10
 )

 res = make_result(
 name="phason_stiffness_ratio",
 app_r_label="Phason stiffness ratio η_stiff = K_⊥/K_∥",
 formula="K_⊥/K_∥ = (det(G_⊥)/det(G_∥))³ = (φ⁻⁶)³ = φ⁻¹⁸",
 predicted=K_ratio,
 observed=expected_K_ratio,
 unit="(dimensionless)",
 app_r_predicted=phi ** (-18),
 app_r_precision_str=f"det ratio = {det_ratio:.10e} (expected φ⁻⁶ = {expected_det_ratio:.10e}); cubed = {K_ratio:.10e} (= φ⁻¹⁸); c_lattice = {c_lattice:.10e} (= φ⁻⁹)",
 app_r_precision_ppm=K_ratio_match * 1e6,
 tier="Tier 2 postulate + Tier 3 specific exponent (D=18)",
 status="PASS" if all_match else "FAIL",
 tolerance_ppm=1.0,
 extra={
 "det_G_para_raw": float(det_para),
 "det_G_perp_raw": float(det_perp),
 "det_ratio_computed": float(det_ratio),
 "det_ratio_expected_phi_minus_6": float(expected_det_ratio),
 "det_ratio_match_relative_error": float(det_ratio_match),
 "K_ratio_phi_minus_18": float(K_ratio),
 "K_ratio_expected": float(expected_K_ratio),
 "lattice_speed_of_light_phi_minus_9": float(c_lattice),
 "all_three_machine_precision_match": all_match,
 "derivation_note": (
 "The Gram-determinant ratio det(G_perp)/det(G_para) = phi^-6 "
 "is the algebraic identity following from the cut-and-project "
 "lattice basis. The cube relationship K ~ det^3 arises from "
 "the 3-dimensional projected continuum (elastic stiffness "
 "is energy density per unit volume in 3D). Composition gives "
 "K_perp/K_para = phi^-18 with no free parameters. The exponent "
 "18 is the H_3 invariant-degree sum (App K §K.4; real dimension "
 "of the Q(sqrt 5) representation = 18), a Tier 2 geometric "
 "input; the Tier 2 identification with the physical phason "
 "elastic sector is the substantive claim."
 ),
 },
 )
 print_summary(res); write_result(res)
 return res


if __name__ == "__main__":
 main()
