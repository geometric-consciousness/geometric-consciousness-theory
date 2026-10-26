"""
verify_stiffness_ratio.py — Phason stiffness ratio η_stiff = K_⊥/K_∥ = φ⁻¹⁸.

INDEPENDENCE SCOPE: This verifier is NOT fully independent. Unlike the
CODATA/PDG-only scripts in this directory, it imports engine geometry
from src/ (`gct_projections` for the AKN projection matrices). Its
agreement with App DPS is therefore a CONSISTENCY CHECK against the engine's
own projection construction, not an independent corroboration of the
stiffness ratio. (See README "independence contract"; the fully
CODATA/PDG-anchored scripts in this directory carry the independence claim.)

App DPS §DPS.2-§DPS.4 (Parameter Ledger §0.1 P3):
 Tier 2: exponent D=18 = H_3 invariant-degree sum (integer identification)
 Tier 3: the stiffness map K_⊥/K_∥ = φ⁻¹⁸ (registered hypothesis P3b, O.15(b),
         listed outside the count)
 Retired as a derivation: "K_⊥/K_∥ ≈ (det(G_⊥)/det(G_∥))³". The raw-frame
 Gram ratio φ⁻⁶ scales as s⁶ under internal rescaling (its cube as s¹⁸), and
 the canonical isometric projectors give 1 (App DPS §DPS.3).

This verifier checks raw-frame coordinate arithmetic only (TIER1_EXACT means
the arithmetic identities hold, not that a stiffness ratio is derived):
 (1) Computes det(G_⊥)/det(G_∥) from the unnormalized AKN projection
 matrices and verifies it equals φ⁻⁶ exactly.
 (2) Cubes the ratio: (φ⁻⁶)³ = φ⁻¹⁸ ≈ 1.731 × 10⁻⁴.
 (3) Takes the square root: φ⁻⁹ (the value the Tier 3 P3b reading uses for
 the lattice speed).

This is structurally similar to the raw-frame Weinberg volume identity
($n=-3$ and V_perp,0/V_parallel,0 = phi^-3 as Tier 1 coordinate arithmetic,
with the physical bare angle remaining the Tier 3 hypothesis H-EW)
audit: the exponent follows from composition of independent geometric
inputs (Gram-determinant ratio + cube-power dimension argument); the
raw-frame ratio is Tier 1 coordinate arithmetic and the cube-power map to the
physical stiffness ratio is a Tier 3 heuristic (App DPS §DPS.3; O.15(b)).
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
 app_psc_label="Phason stiffness ratio η_stiff = K_⊥/K_∥",
 formula="K_⊥/K_∥ = (det(G_⊥)/det(G_∥))³ = (φ⁻⁶)³ = φ⁻¹⁸",
 predicted=K_ratio,
 observed=expected_K_ratio,
 unit="(dimensionless)",
 app_psc_predicted=phi ** (-18),
 app_psc_precision_str=f"det ratio = {det_ratio:.10e} (expected φ⁻⁶ = {expected_det_ratio:.10e}); cubed = {K_ratio:.10e} (= φ⁻¹⁸); c_lattice = {c_lattice:.10e} (= φ⁻⁹)",
 app_psc_precision_ppm=K_ratio_match * 1e6,
 tier="Tier 2 integer identification (D=18) + Tier 3 heuristic stiffness-ratio map",
 status="TIER1_EXACT" if all_match else "FAIL",
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
 "is a raw-frame (coordinate-dependent) algebraic identity of the cut-and-project "
 "lattice basis: it scales as s^6 under an internal rescaling and the canonical "
 "isometric projectors give 1, so its cube does not derive a stiffness ratio "
 "(the former Gram-cube route is retired, App DPS §DPS.3). The exponent "
 "18 is the H_3 invariant-degree sum (App DPS §DPS.4), the Tier 2 integer "
 "identification; the map K_perp/K_para = phi^-18 is the Tier 3 P3b "
 "hypothesis (O.15(b)), registered outside the count."
 ),
 },
 )
 print_summary(res); write_result(res)
 return res


if __name__ == "__main__":
 main()
