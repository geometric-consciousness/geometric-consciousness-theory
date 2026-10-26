"""
verify_alpha_s_bare.py — Strong coupling α_s⁻¹(bare) = 10 φ² ≈ 26.18 (Tier 3 handle).

V3 Ch04 §4.5.5 / App TAT §TAT.3 / App GRF §GRF.5 / App TPR §TPR.3:
 α_s⁻¹(bare) = 10 φ² [Tier 3 calibrated handle pending O.42 / QLQCD-2]
 where 10 = count of three-fold rotation axes of the RT (Tier 1 given P1)
 and φ² = standard icosahedral inflation factor (Tier 1 given P1)
 → α_s⁻¹(bare) ≈ 26.18 → α_s(bare) ≈ 0.0382

This is a BARE TREE-LEVEL handle at M_GUT, not the running PDG value at M_Z.
PDG 2024 α_s(M_Z) = 0.1180 ± 0.0009 (α_s⁻¹ = 8.475 at the central
value). The manuscript states (App GRF §GRF.5)
that the bare value is "too small (α_s too large) to be carried by 33.5 e-folds
of asymptotic-free running down to PDG value"; QLQCD-2 non-perturbative
confinement corrections are the canonical path to closure (Open Problem in App
QLA.7).

This verifier:
 (1) Computes α_s⁻¹(bare) = 10 φ² and confirms the literal formula gives
 26.18 from manuscript-internal inputs.
 (2) Reports the inverse-space residual with the observed inverse coupling as
 denominator: [α_s⁻¹(bare) - α_s⁻¹(M_Z)] / α_s⁻¹(M_Z) = +208.9%.
 The separately labelled direct-space comparison places the M_Z coupling
 67.63% above the bare coupling when normalized to α_s(M_Z). Both compare a
 GUT-scale handle with an M_Z value and so mix scales; the native run from
 the handle gives α_s(M_Z) ≈ 0.052, 55.9% low (Ch04 §4.5.5).
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import MATH, ALPHA_S_MZ_PDG_2024, ALPHA_S_MZ_PDG_2024_ERR
from report import make_result, write_result, print_summary


def main():
 phi = MATH.PHI

 # GCT bare formula
 alpha_s_inv_bare = 10.0 * phi ** 2
 alpha_s_bare = 1.0 / alpha_s_inv_bare

 # Manuscript stated
 stated_inv = 26.18
 err_pct = abs(alpha_s_inv_bare - stated_inv) / stated_inv * 100.0
 formula_OK = err_pct < 0.1 # the formula 10·φ² is exact; we just check rounding

 # Gap to PDG α_s(M_Z) — DOCUMENTED IN APP GRF §GRF.5 as the QLQCD-2 debt
 alpha_s_PDG_MZ = ALPHA_S_MZ_PDG_2024
 alpha_s_inv_PDG_MZ = 1.0 / alpha_s_PDG_MZ
 bare_vs_PDG_gap_pct = (alpha_s_inv_bare - alpha_s_inv_PDG_MZ) / alpha_s_inv_PDG_MZ * 100.0
 direct_space_gap_pct = (alpha_s_PDG_MZ - alpha_s_bare) / alpha_s_PDG_MZ * 100.0

 res = make_result(
 name="alpha_s_inv_bare",
 app_psc_label="Strong coupling α_s⁻¹(bare) = 10 φ² (Tier 3 calibrated handle)",
 formula="α_s⁻¹(bare) = 10 · φ² (10 = RT three-fold axes; φ² = icosahedral inflation)",
 predicted=alpha_s_inv_bare,
 observed=stated_inv,
 reference_class="MANUSCRIPT_STATED",
 unit="(dimensionless)",
 app_psc_predicted=stated_inv,
 app_psc_precision_str=(
 f"Tier 3 calibrated-handle evaluation: 10 · φ² = {alpha_s_inv_bare:.4f} "
 f"vs stated 26.18 ({err_pct:+.4f}%). Gap to PDG α_s⁻¹(M_Z) = "
 f"{alpha_s_inv_PDG_MZ:.4f} is {bare_vs_PDG_gap_pct:+.1f}% under the "
 f"(bare⁻¹ - M_Z⁻¹)/M_Z⁻¹ convention; in direct-coupling space, "
 f"α_s(M_Z) exceeds α_s(bare) by {direct_space_gap_pct:.2f}% when normalized "
 f"to α_s(M_Z). This is the open debt of App GRF §GRF.5 / Ch04 §4.5.5 "
 f"(QLQCD-2 non-perturbative confinement correction, App QLA.7 open problem)."
 ),
 app_psc_precision_ppm=err_pct * 1e4,
 tier="Tier 3 calibrated handle (10 integer + φ² geometric factor); O.42 / QLQCD-2 open + Tier 4 as evidence that phi explains the value (constant control test v3 NEGATIVE-FRAGILE; App PSC §PSC.9.6)",
 status="INTERNAL_ARITHMETIC_PASS" if formula_OK else "FAIL",
 tolerance_ppm=None,
 extra={
 "phi": phi,
 "alpha_s_inv_bare_GCT_formula": alpha_s_inv_bare,
 "alpha_s_bare_GCT": alpha_s_bare,
 "alpha_s_inv_stated_in_manuscript": stated_inv,
 "formula_rounding_error_pct": err_pct,
 "alpha_s_PDG_MZ": alpha_s_PDG_MZ,
 "alpha_s_PDG_MZ_uncertainty": ALPHA_S_MZ_PDG_2024_ERR,
 "alpha_s_inv_PDG_MZ": alpha_s_inv_PDG_MZ,
 "bare_vs_PDG_gap_pct": bare_vs_PDG_gap_pct,
 "inverse_space_residual_convention": "(alpha_s_inv_bare - alpha_s_inv_PDG_MZ) / alpha_s_inv_PDG_MZ",
 "direct_space_gap_pct": direct_space_gap_pct,
 "direct_space_gap_convention": "(alpha_s_PDG_MZ - alpha_s_bare) / alpha_s_PDG_MZ",
 "derivation_note": (
 "α_s⁻¹(bare) = 10 φ² combines two geometric substrate inputs: "
 "(a) the count of three-fold rotation axes of the rhombic "
 "triacontahedron = 10, and (b) the icosahedral inflation "
 "factor φ². The TREE-LEVEL bare value 26.18 is a calibrated handle "
 "at M_GUT; the inverse-space +208.9% residual to PDG 2024 "
 "α_s⁻¹(M_Z) = 8.475 uses the observed inverse coupling as denominator. "
 "The direct-space 67.63% comparison is separately labelled. Both compare a "
 "GUT-scale handle with an M_Z value and so mix scales; the native run gives "
 "α_s(M_Z) ≈ 0.052 (55.9% low). The gap is the open "
 "QLQCD-2 non-perturbative confinement debt (App QLA.7), "
 "explicitly acknowledged in App GRF §GRF.5 and Ch04 §4.5.5. "
 "Non-perturbative closure remains pending."
 ),
 },
 )
 print_summary(res); write_result(res)
 return res


if __name__ == "__main__":
 main()
