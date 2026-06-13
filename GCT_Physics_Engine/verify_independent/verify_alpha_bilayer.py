"""
verify_alpha_bilayer.py — α⁻¹_GCT = 360φ⁻² × (1 - 1/288) with bilayer correction.

V1 Ch13 §13.2.4 (Tier 2 Motivated Derivation):
 α⁻¹_GCT = α⁻¹_geom × η(144)
 = 137.5077 × (1 - 1/288)
 = 137.0303
 CODATA α⁻¹ = 137.035999
 Residual: 41.6 ppm

The bare 360φ⁻² baseline is already verified in verify_alpha.py (3442 ppm
residual). This verifier tests the BILAYER-CORRECTED prediction which
sharpens the residual to 41.6 ppm by importing the 1/(2N) = 1/288 potential-
theory correction (N = 144 cage nodes; bilayer = 2N = 288).

Tier 2 (Motivated Derivation) per Ch13 §13.2.4: the 1/(2N) correction is
not a free parameter (288 = 2×144 follows from N without additional choice)
but it is imported from potential theory rather than derived from GCT axioms
directly. The 41.6 ppm residual is the documented QLQCD-1L research debt
(O.5 / App Z.5-Z.6).
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import CODATA, MATH
from report import make_result, write_result, print_summary


def main():
 phi = MATH.PHI
 alpha_inv_CODATA = CODATA.ALPHA_INV # 137.035999...

 N_cage = 144 # cage node count (Tier 2 from Gauss-Bonnet + Fibonacci-square)
 bilayer = 2 * N_cage # = 288

 alpha_inv_bare = 360.0 * phi ** (-2) # = 137.5077 (Tier 2 bare)
 eta_bilayer = 1.0 - 1.0 / bilayer # = 1 - 1/288 = 0.996528
 alpha_inv_GCT_corr = alpha_inv_bare * eta_bilayer # = 137.0303

 err_bare_ppm = abs(alpha_inv_bare - alpha_inv_CODATA) / alpha_inv_CODATA * 1e6
 err_corr_ppm = abs(alpha_inv_GCT_corr - alpha_inv_CODATA) / alpha_inv_CODATA * 1e6
 improvement = err_bare_ppm / err_corr_ppm

 matches_stated_137_030 = abs(alpha_inv_GCT_corr - 137.0303) / 137.0303 < 1e-4
 internal_reproduction_status = matches_stated_137_030

 res = make_result(
 name="alpha_inverse_bilayer_corrected",
 app_r_label="Fine-structure α⁻¹ with bilayer 1/288 correction (Ch13 §13.2.4, Tier 2 Motivated)",
 formula="α⁻¹_GCT = 360φ⁻² × (1 - 1/288) = α⁻¹_bare × (1 - 1/(2N)), N=144",
 predicted=alpha_inv_GCT_corr,
 observed=alpha_inv_CODATA,
 unit="(dimensionless, α⁻¹)",
 app_r_predicted=137.0303,
 app_r_precision_str=(
 f"Bare 360·φ⁻² = {alpha_inv_bare:.6f} ({err_bare_ppm:.1f} ppm); "
 f"with bilayer factor (1-1/288) = {eta_bilayer:.6f}: "
 f"α⁻¹_GCT = {alpha_inv_GCT_corr:.6f} ({err_corr_ppm:.2f} ppm). "
 f"Precision improvement: {improvement:.0f}× (3442→41.6 ppm). "
 f"Matches Ch13 §13.2.4 stated 137.0303 ✓."
 ),
 app_r_precision_ppm=err_corr_ppm,
 tier="Tier 2 (Motivated Derivation; 1/(2N) correction imported from potential theory; full QLQCD-1L closure pending O.5)",
 status="OPEN_CONDITIONAL" if internal_reproduction_status else "TENSION",
 tolerance_ppm=None,
 extra={
 "phi": phi,
 "N_cage_nodes": N_cage,
 "bilayer_2N": bilayer,
 "alpha_inv_bare_360_phi_neg_2": alpha_inv_bare,
 "eta_bilayer_1_minus_1_over_288": eta_bilayer,
 "alpha_inv_GCT_corrected": alpha_inv_GCT_corr,
 "alpha_inv_CODATA": alpha_inv_CODATA,
 "alpha_inv_stated_in_Ch13_13_2_4": 137.0303,
 "residual_ppm_bare": err_bare_ppm,
 "residual_ppm_corrected": err_corr_ppm,
 "precision_improvement_factor": improvement,
 "matches_internal_137_0303_value": internal_reproduction_status,
 "closure_condition": (
 "This verifier reproduces the manuscript's bilayer-corrected arithmetic. "
 "It does not close the 1/(2N) bilayer correction or the residual 41.6 ppm "
 "as a first-principles alpha derivation; that remains O.5/O.19."
 ),
 "derivation_note": (
 "The bare 360φ⁻² formula yields 137.5077 (3442 ppm residual). "
 "The bilayer 1/(2N) = 1/288 correction (N=144 cage nodes; "
 "bilayer = 2N=288) tightens the prediction to 137.0303, "
 "reducing the residual to 41.6 ppm — an 83× precision "
 "improvement. The 1/(2N) factor is acknowledged in Ch13 "
 "§13.2.4 as imported from potential theory (Tier 2 Motivated) "
 "rather than derived from GCT axioms; the remaining 41.6 ppm "
 "is the documented QLQCD-1L research debt (Open Problem O.5)."
 ),
 },
 )
 print_summary(res); write_result(res)
 return res


if __name__ == "__main__":
 main()
