"""
verify_tau_mass.py — Independent re-derivation of m_tau

App R §R.1 row 3:
 Formula: m_tau = m_e · φ^17 · (1 - 3.6α)
 App R: 1776.84 MeV; Tier 2 mechanism + Tier 2 integer-pair
 (D=18, N=5) + Tier 3 combination rule; ~51 ppm against PDG 2024
 m_tau = 1776.93 MeV under SM-equivalent radiative-correction discipline.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import CODATA, MATH, ppm_error
from report import make_result, write_result, print_summary

N_TAU = 17 # 3·S_oct − 1
TAU_SCREEN_COEFF = -18.0 / 5.0 # = -3.6; headline coefficient is Tier 3 pending O.26b

def main():
 phi = MATH.PHI
 alpha = CODATA.ALPHA
 m_e = CODATA.M_E_MEV

 m_tau = m_e * (phi ** N_TAU) * (1.0 + TAU_SCREEN_COEFF * alpha)
 observed = CODATA.M_TAU_MEV
 ppm = ppm_error(m_tau, observed)

 result = make_result(
 name="tau_mass",
 app_r_label="Tau mass (m_tau)",
 formula="m_tau = m_e · φ^17 · (1 - 3.6α), -3.6 = -D/N = -18/5",
 predicted=m_tau,
 observed=observed,
 unit="MeV",
 app_r_predicted=1776.84,
 app_r_precision_str="~0.25% (Tier 2 bare) | ~51 ppm (Tier 2+3 corrected, vs PDG 2024)",
 app_r_precision_ppm=51.0,
 tier="Tier 2 mechanism + Tier 2 integer-pair (D=18, N=5) + Tier 3 combination rule c = -D/N pending O.26b; headline coefficient is Tier 3",
 status="PASS" if ppm <= 50.0 else "TENSION",
 tolerance_ppm=50.0,
 extra={
 "N_tau": N_TAU,
 "tau_screen_coeff": TAU_SCREEN_COEFF,
 "alpha_codata": alpha,
 },
 )
 print_summary(result)
 write_result(result)
 return result


if __name__ == "__main__":
 main()
