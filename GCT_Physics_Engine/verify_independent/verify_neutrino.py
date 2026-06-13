"""
verify_neutrino.py — Independent re-derivation of neutrino floor + sum

App R §R.5:
 m_1 = m_e · φ^-36 → 0.0153 eV (KATRIN < 0.8 eV → consistent)
 Σm_ν = sqrt(m_1² + Δm²_21) + sqrt(m_1² + Δm²_31) + m_1
 → 0.0853 eV vs Planck < 0.12 (consistency)
 vs DESI 2024 < 0.072 (~2σ tension)
"""

import sys
import math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import CODATA, MATH, pct_error
from report import make_result, write_result, print_summary


def main():
 phi = MATH.PHI
 m_e_eV = CODATA.M_E_MEV * 1.0e6 # 5.110e5 eV

 # ---------- m_1 floor ----------
 m1_eV = m_e_eV * (phi ** -36)
 KATRIN_BOUND_eV = 0.8
 m1_below_bound = m1_eV < KATRIN_BOUND_eV
 status_m1 = "PASS" if m1_below_bound else "FAIL"
 res_m1 = make_result(
 name="neutrino_m1_floor",
 app_r_label="Neutrino m_1 floor",
 formula="m_1 = m_e · φ^-36",
 predicted=m1_eV,
 observed=None, # KATRIN is an upper bound, not a measurement
 unit="eV",
 app_r_predicted=0.0153,
 app_r_precision_str=f"m_1 = {m1_eV:.4e} eV; KATRIN upper bound {KATRIN_BOUND_eV} eV → {'within bound' if m1_below_bound else 'OUTSIDE BOUND'}",
 app_r_precision_ppm=None,
 tier="Tier 2",
 status=status_m1,
 tolerance_ppm=None,
 extra={
 "katrin_upper_bound_eV": KATRIN_BOUND_eV,
 "predicted_is_below_bound": m1_below_bound,
 },
 )
 print_summary(res_m1); write_result(res_m1)

 # ---------- Σm_ν (Normal Ordering) ----------
 m2_eV = math.sqrt(m1_eV ** 2 + CODATA.DELTA_M2_21)
 m3_eV = math.sqrt(m1_eV ** 2 + CODATA.DELTA_M2_31)
 sigma_m_eV = m1_eV + m2_eV + m3_eV

 planck_bound = CODATA.SIGMA_MNU_PLANCK_BOUND_EV # 0.12
 desi_bound = CODATA.SIGMA_MNU_DESI_2024_EV # 0.072

 # Tension vs DESI: Σm > bound
 desi_excess = sigma_m_eV - desi_bound

 res_sum = make_result(
 name="neutrino_sum",
 app_r_label="Σ m_ν (NO)",
 formula="Σm_ν = m_1 + sqrt(m_1² + Δm²_21) + sqrt(m_1² + Δm²_31)",
 predicted=sigma_m_eV,
 observed=None, # bound, not measurement
 unit="eV",
 app_r_predicted=0.0853,
 app_r_precision_str=(
 "< 0.12 (Planck 2018) CONSISTENT; "
 "< 0.072 (Planck+DESI 2024) ~2σ TENSION"
 ),
 app_r_precision_ppm=None,
 tier="Tier 2 / Tier 3 (consistency check)",
 status="TENSION" if desi_excess > 0 else "PASS",
 tolerance_ppm=None,
 extra={
 "m1_eV": m1_eV, "m2_eV": m2_eV, "m3_eV": m3_eV,
 "planck_2018_bound_eV": planck_bound,
 "planck_2018_status": "PASS (Σ < 0.12)" if sigma_m_eV < planck_bound else "FAIL",
 "desi_2024_bound_eV": desi_bound,
 "desi_2024_status": "TENSION (Σ > 0.072)" if sigma_m_eV > desi_bound else "PASS",
 "desi_excess_eV": desi_excess,
 "note": (
 "Σm_ν > 0.072 eV puts GCT in 2σ tension with Planck+DESI 2024. "
 "App R notes this is the most urgent active falsification risk."
 ),
 },
 )
 print_summary(res_sum); write_result(res_sum)
 return [res_m1, res_sum]


if __name__ == "__main__":
 main()
