"""
verify_alpha.py — Independent re-derivation of α^-1

App R §R.2 row 1:
 Formula: α^-1 = 360 · φ^-2
 App R: 137.5077 vs CODATA 137.035999 -> 3442 ppm
 Tier: Tier 2 mechanism + Tier 3 specific 600-cell multiplier pending O.19/O.5

 The 0.5% band is the disclosed GCT phason anti-screening residual after
 ordinary sub-ppm QED precision is treated as an external Standard-Model
 bridge. It is not a precision validation of the bare 360*phi^-2 expression.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import CODATA, MATH, ppm_error
from report import make_result, write_result, print_summary

ALPHA_FACTOR_360 = 360.0 # 600-cell edges / 2 = 720/2

def main():
 phi = MATH.PHI
 alpha_inv_pred = ALPHA_FACTOR_360 * (phi ** -2)
 observed = CODATA.ALPHA_INV
 ppm = ppm_error(alpha_inv_pred, observed)

 # Compute precision and let make_result/print_summary derive status
 # from (predicted, observed, tolerance) rather than hardcoding PASS.
 ppm_actual = abs(alpha_inv_pred - observed) / observed * 1e6
 tolerance = 5000.0 # documented anti-screening residual band (Tier 2 tree-level)
 derived_status = "OPEN_CONDITIONAL" if ppm_actual <= tolerance else "FAIL"

 result = make_result(
 name="alpha_inverse",
 app_r_label="Fine-structure constant inverse (α^-1)",
 formula="α^-1 = 360 · φ^-2",
 predicted=alpha_inv_pred,
 observed=observed,
 unit="(dimensionless)",
 app_r_predicted=137.5077,
 app_r_precision_str="3442 ppm (Tree-Level Base)",
 app_r_precision_ppm=3442.0,
 tier="Tier 2 mechanism + Tier 3 specific multiplier (O.19/O.5 pending)",
 status=derived_status,
 tolerance_ppm=tolerance,
 extra={
 "phi_squared_inv": phi ** -2,
 "alpha_factor_360_provenance": "600-cell antipodal edge-count selection; Tier 3 specific multiplier pending O.19/O.5",
 "actual_ppm_residual": ppm_actual,
 "status_note": (
 "Tree-level residual 3442.6 ppm; Tier 3 numerical residual pending O.5 "
 "(1/(2N) integer-factor closure) and O.19 (phason 1-loop magnitude "
 "closure). Within 0.5% tolerance band but NOT a precision validation."
 ),
 },
 )
 print_summary(result)
 write_result(result)
 return result


if __name__ == "__main__":
 main()
