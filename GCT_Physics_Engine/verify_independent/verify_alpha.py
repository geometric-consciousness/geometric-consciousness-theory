"""
verify_alpha.py — Independent re-derivation of α^-1

App PSC §PSC.2 row 1:
 Formula: α^-1 = 360 · φ^-2
 App PSC: 137.5078 vs CODATA 137.035999177 -> 3443 ppm
 Tier: Tier 3 numerical relation (Tier 3 600-cell multiplier; mechanism open —
 the RT solid-angle construction is withdrawn, V1 §13.2.1–§13.2.2); O.19/O.5 pending

 The 0.5% band is the disclosed GCT phason anti-screening residual after
 ordinary sub-ppm QED precision is treated as an external Standard-Model
 bridge. It is not a precision validation of the bare 360*phi^-2 expression.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import CODATA, MATH, ppm_error
from report import make_result, write_result, print_summary, status_from_registered_band

ALPHA_FACTOR_360 = 360.0 # 600-cell edges / 2 = 720/2

def main():
 phi = MATH.PHI
 alpha_inv_pred = ALPHA_FACTOR_360 * (phi ** -2)
 observed = CODATA.ALPHA_INV
 ppm = ppm_error(alpha_inv_pred, observed)

 # Compute precision and let make_result/print_summary derive status
 # from (predicted, observed, tolerance) rather than hardcoding PASS.
 ppm_actual = abs(alpha_inv_pred - observed) / observed * 1e6
 tolerance = 5000.0 # documented anti-screening residual band
 derived_status = status_from_registered_band(
  ppm_actual, tolerance,
  inside_status="OPEN_CONDITIONAL", outside_status="FAIL",
 )

 result = make_result(
 name="alpha_inverse",
 app_psc_label="Fine-structure constant inverse (α^-1)",
 formula="α^-1 = 360 · φ^-2",
 predicted=alpha_inv_pred,
 observed=observed,
 unit="(dimensionless)",
 app_psc_predicted=137.5078,
 app_psc_precision_str="3443 ppm (Tree-Level Base)",
 app_psc_precision_ppm=3443.0,
 tier="Tier 3 numerical relation (Tier 3 600-cell multiplier; mechanism open — the RT solid-angle construction is withdrawn, V1 §13.2.1–§13.2.2); O.19/O.5 pending + Tier 4 as evidence that phi explains the value (constant control test v3 NEGATIVE-FRAGILE; App PSC §PSC.9.6)",
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
