"""
verify_proton_mass.py — Independent re-derivation of proton mass

App R §R.3 row 1:
 Formula: m_p = m_e · φ^(15 + φ^-1)
 App R: 938.417 MeV vs 938.272 → 155 ppm
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import CODATA, MATH, ppm_error
from report import make_result, write_result, print_summary

N_BARYON = 15
def main():
 phi = MATH.PHI
 m_e = CODATA.M_E_MEV
 exponent = N_BARYON + (phi ** -1)
 m_p_pred = m_e * (phi ** exponent)
 observed = CODATA.M_P_MEV
 ppm = ppm_error(m_p_pred, observed)

 result = make_result(
 name="proton_mass",
 app_r_label="Proton mass (m_p)",
 formula="m_p = m_e · φ^(15 + φ^-1)",
 predicted=m_p_pred,
 observed=observed,
 unit="MeV",
 app_r_predicted=938.417,
 app_r_precision_str="155 ppm (0.015%)",
 app_r_precision_ppm=155.0,
 tier="Tier 2 mechanism + Tier 3 sheet-exponent (155 ppm residual; closure pending AKN-action O.32)",
 status="TENSION",
 tolerance_ppm=300.0,
 extra={
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
