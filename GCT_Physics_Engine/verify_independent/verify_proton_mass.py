"""
verify_proton_mass.py — Independent recomputation of the proton-mass formula

App PSC §PSC.3 row 1:
 Formula: m_p = m_e · φ^(15 + φ^-1)
 App PSC: 938.417 MeV vs 938.272 → 155 ppm
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import CODATA, MATH, ppm_error
from report import make_result, write_result, print_summary, status_from_registered_band

N_BARYON = 15
def main():
 phi = MATH.PHI
 m_e = CODATA.M_E_MEV
 exponent = N_BARYON + (phi ** -1)
 m_p_pred = m_e * (phi ** exponent)
 observed = CODATA.M_P_MEV
 ppm = ppm_error(m_p_pred, observed)

 tolerance = 500.0
 result = make_result(
 name="proton_mass",
 app_psc_label="Proton mass (m_p)",
 formula="m_p = m_e · φ^(15 + φ^-1)",
 predicted=m_p_pred,
 observed=observed,
 unit="MeV",
 app_psc_predicted=938.417,
 app_psc_precision_str="155 ppm (0.015%)",
 app_psc_precision_ppm=155.0,
 tier="Tier 2 mechanism + Tier 3 sheet-exponent (155 ppm residual; closure pending AKN-action O.5) + Tier 4 as evidence that phi explains the value (constant control test v3 NEGATIVE-FRAGILE; App PSC §PSC.9.6)",
 status=status_from_registered_band(
  ppm, tolerance, inside_status="OPEN_CONDITIONAL", outside_status="TENSION"
 ),
 tolerance_ppm=tolerance,
 extra={
  "status_rule": (
   "The residual sits inside the registered 500 ppm gate, so the arithmetic does not "
   "carry a tension. The sheet exponent 15 + phi^-1 is a Tier 3 anchor whose "
   "derivation remains pending AKN-action closure under O.5, so the row is "
   "OPEN_CONDITIONAL rather than PASS."
  ),
 "exponent_15_plus_phi_inv": exponent,
 "ratio_m_p_over_m_e_pred": phi ** exponent,
 "ratio_m_p_over_m_e_observed": observed / m_e,
 },
 )
 print_summary(result)
 write_result(result)
 return result


if __name__ == "__main__":
 main()
