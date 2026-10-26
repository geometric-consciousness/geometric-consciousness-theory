"""
verify_cabibbo.py — Independent recomputation of the Cabibbo-angle formula

 App PSC §PSC.4 row:
 Formula: θ_C ≡ arcsin(s12_CKM) with s12 = φ^-3 (1 - 5α)
 Tier: Tier 3 bare identification (raw-frame φ^-3) + Tier 3 lepton-to-hadron transfer correction pending O.5
 App PSC: 13.1473° vs observed 13.0035° → 1.11%
 Executable precision gate: 0.5% (5,000 ppm), the same CKM precision gate that
 verify_ckm.py applies to ckm_s12 (sin θ_C = s12, same formula). One observable
 carries one precision gate, so the 1.11 %
 residual is a TENSION. The registered P.18 band of 5% (50,000 ppm) is kept only
 as the falsification band: a 1.11 % miss falsifies nothing and retires nothing.
"""

import sys
import math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import CODATA, MATH, pct_error
from report import make_result, write_result, print_summary, status_from_registered_band


def main():
 phi = MATH.PHI
 alpha = CODATA.ALPHA

 s12 = (phi ** -3) * (1.0 - 5.0 * alpha)
 theta_c_deg = math.degrees(math.asin(s12))
 observed = CODATA.THETA_C_DEG
 pct = pct_error(theta_c_deg, observed)
 ppm = pct * 1.0e4
 precision_gate_ppm = 5000.0          # shared CKM precision gate (= ckm_s12)
 falsification_band_ppm = 50000.0     # registered P.18 falsification band
 falsification_band_outcome = (
     "INSIDE_REGISTERED_FALSIFICATION_BAND" if abs(ppm) <= falsification_band_ppm
     else "OUTSIDE_REGISTERED_FALSIFICATION_BAND"
 )

 result = make_result(
     name="cabibbo_angle",
     app_psc_label="Cabibbo angle (θ_C)",
     formula="sin(θ_C) = φ^-3 · (1 - 5α); θ_C = arcsin(·)",
     predicted=theta_c_deg,
     observed=observed,
     reference_class="EMPIRICAL_ANCHOR",
     derivational_closure="OPEN_O.5_LEPTON_TO_HADRON_TRANSFER",
     unit="degrees",
     app_psc_predicted=13.1473,
     app_psc_precision_str="1.11%",
     app_psc_precision_ppm=11058.0,
     tier="Tier 3 bare identification (raw-frame phi^-3) + Tier 3 lepton-to-hadron transfer correction pending O.5 + Tier 4 as evidence that phi explains the value (constant control test v3 NEGATIVE-FRAGILE; App PSC §PSC.9.6)",
     status=status_from_registered_band(ppm, precision_gate_ppm),
     tolerance_ppm=precision_gate_ppm,
     extra={
         "sin_theta_C_pred": s12,
         "percent_error": pct,
         "precision_gate_percent": 0.5,
         "registered_falsification_band_percent": 5.0,
         "falsification_band_outcome": falsification_band_outcome,
     },
 )
 print_summary(result)
 write_result(result)
 return result


if __name__ == "__main__":
 main()
