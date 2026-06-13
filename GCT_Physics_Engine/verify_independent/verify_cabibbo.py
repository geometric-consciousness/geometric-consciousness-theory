"""
verify_cabibbo.py — Independent re-derivation of Cabibbo angle

 App R §R.4 row:
 Formula: θ_C ≡ arcsin(s12_CKM) with s12 = φ^-3 (1 - 5α)
 Tier: Tier 2 bare prediction (φ^-3) + Tier 3 lepton-to-hadron transfer correction pending O.5
 App R: 13.147° vs observed 13.040° → 0.82%
 Executable precision gate: 0.5%; misses above that gate are TENSION.
"""

import sys
import math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import CODATA, MATH, pct_error
from report import make_result, write_result, print_summary


def main():
 phi = MATH.PHI
 alpha = CODATA.ALPHA

 s12 = (phi ** -3) * (1.0 - 5.0 * alpha)
 theta_c_deg = math.degrees(math.asin(s12))
 observed = CODATA.THETA_C_DEG
 pct = pct_error(theta_c_deg, observed)

 result = make_result(
	 name="cabibbo_angle",
	 app_r_label="Cabibbo angle (θ_C)",
	 formula="sin(θ_C) = φ^-3 · (1 - 5α); θ_C = arcsin(·)",
	 predicted=theta_c_deg,
	 observed=observed,
	 unit="degrees",
	 app_r_predicted=13.147,
	 app_r_precision_str="0.82%",
	 app_r_precision_ppm=8200.0,
	 tier="Tier 2 bare + Tier 3 lepton-to-hadron transfer correction pending O.5",
	 status="PASS" if pct < 0.5 else "TENSION",
	 tolerance_ppm=5000.0,
	 extra={"sin_theta_C_pred": s12, "percent_error": pct, "precision_gate_percent": 0.5},
 )
 print_summary(result)
 write_result(result)
 return result


if __name__ == "__main__":
 main()
