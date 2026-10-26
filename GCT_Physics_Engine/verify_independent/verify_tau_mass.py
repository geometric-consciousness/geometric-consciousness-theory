"""
verify_tau_mass.py — Independent re-derivation of m_tau

App PSC §PSC.1 row 3:
 Formula: m_tau = m_e · φ^17 · (1 - 3.6α)
 App PSC: 1776.84 MeV; Tier 2 mechanism + Tier 2 integer D=18 + N=5 A5 irrep count
 (Tier 3 as a channel number) + Tier 3 combination rule; ~51 ppm against PDG 2024
 m_tau = 1776.93 MeV; a Tier 3 formula residual (no theory-error model).
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import CODATA, MATH, ppm_error
from report import make_result, write_result, print_summary

N_TAU = 17 # 3·S_oct − 1
TAU_SCREEN_COEFF = -18.0 / 5.0 # = -3.6; headline coefficient is Tier 3 pending O.26b
REGISTERED_TOLERANCE_PPM = 50.0 # registered tolerance; not a derived theory floor
HARD_FAIL_PPM = 55.0


def evaluate_registered_tolerance_status(ppm: float) -> str:
 """Classify the registered 50/55 ppm tri-state tolerance (not a derived theory floor)."""
 value = abs(ppm)
 if value <= REGISTERED_TOLERANCE_PPM:
  return "PASS"
 if value < HARD_FAIL_PPM:
  return "AT_GATE_TENSION"
 return "HARD_FAIL"

def main():
 phi = MATH.PHI
 alpha = CODATA.ALPHA
 m_e = CODATA.M_E_MEV

 m_tau = m_e * (phi ** N_TAU) * (1.0 + TAU_SCREEN_COEFF * alpha)
 observed = CODATA.M_TAU_MEV
 ppm = ppm_error(m_tau, observed)
 tolerance_status = evaluate_registered_tolerance_status(ppm)

 result = make_result(
 name="tau_mass",
 app_psc_label="Tau mass (m_tau)",
 formula="m_tau = m_e · φ^17 · (1 - 3.6α), -3.6 = -D/N = -18/5",
 predicted=m_tau,
 observed=observed,
 unit="MeV",
 app_psc_predicted=1776.84,
 app_psc_precision_str="+2.69% (bare phi^17) | ~-51 ppm (first-order formula, Tier 2+3, vs PDG 2024)",
 app_psc_precision_ppm=51.0,
 tier="Tier 2 mechanism + Tier 2 integer D=18 + N=5 A5 irrep count (Tier 3 as a channel number) + Tier 3 combination rule c = -D/N pending O.26b; headline coefficient is Tier 3 + Tier 4 as evidence that phi explains the value (constant control test v3 NEGATIVE-FRAGILE; App PSC §PSC.9.6)",
 status={"PASS": "PASS", "AT_GATE_TENSION": "TENSION", "HARD_FAIL": "FAIL"}[tolerance_status],
 tolerance_ppm=50.0,
 extra={
 "N_tau": N_TAU,
 "tau_screen_coeff": TAU_SCREEN_COEFF,
 "alpha_codata": alpha,
 "registered_tolerance_ppm": [REGISTERED_TOLERANCE_PPM, HARD_FAIL_PPM],
 "registered_tolerance_status": tolerance_status,
 "theory_floor_note": "The earlier 10-50 ppm SM-correction theory floor is withdrawn; 50/55 ppm is a registered tolerance, not a derived floor, and no decision uses a theory floor.",
 "hard_fail_ppm": HARD_FAIL_PPM,
 },
 )
 print_summary(result)
 write_result(result)
 return result


if __name__ == "__main__":
 main()
