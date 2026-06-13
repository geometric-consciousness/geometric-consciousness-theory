"""
verify_higgs_vev.py — Independent re-derivation of Higgs VEV (absolute pipeline)

App R §R.2 row 8:
 Formula: v = m_e · φ^11 · (1 + 5α_A3 + φ^8 α_A3^2) · 1440 · φ
 = m_mu · 1440 · φ
 App R: 246.1754 GeV (engine full precision) vs PDG 246.22 → ~181 ppm
 (engine residual_error_ppm = 180.67 from `protocol_higgs_vev_results.json`;
 independent PDG-anchor check reports 179.15 ppm)

The 1440 saturation factor = N_cage (=144, F_12) × N_RT_3foldAxes(=10).
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import CODATA, MATH, ppm_error
from report import make_result, write_result, print_summary

N_CAGE = 144
N_RT_AXES_HALF = 10
SATURATION = N_CAGE * N_RT_AXES_HALF # = 1440
N_MU = 11
N_PHASON = 5
PHI_POWER_2 = 8

def main():
 phi = MATH.PHI
 # A3 disclosure: the canonical VEV precision row inherits the corrected
 # muon formula and therefore the measured low-energy alpha input.
 alpha = CODATA.ALPHA
 m_e_mev = CODATA.M_E_MEV

 m_mu = m_e_mev * (phi ** N_MU) * (
 1.0 + N_PHASON * alpha + (phi ** PHI_POWER_2) * alpha**2
 ) # MeV
 v_mev = m_mu * SATURATION * phi
 v_gev = v_mev / 1000.0

 observed = CODATA.V_HIGGS_GEV
 ppm = ppm_error(v_gev, observed)

 result = make_result(
 name="higgs_vev",
 app_r_label="Higgs VEV (v)",
 formula="v = m_e · φ^11 · (1 + 5α_A3 + φ^8 α_A3^2) · 1440 · φ",
 predicted=v_gev,
 observed=observed,
 unit="GeV",
 app_r_predicted=246.1754,
 app_r_precision_str="181 ppm",
 app_r_precision_ppm=181.0,
 tier="Tier 2 mechanism + A3 measured alpha input + Tier 3 calibrated-handle residual",
 status="OPEN_CONDITIONAL" if ppm < 500.0 else "FAIL",
 tolerance_ppm=500.0,
 extra={
 "m_mu_intermediate_MeV": m_mu,
 "alpha_codata_A3": alpha,
 "alpha_anchor": "A3 measured low-energy alpha inherited from the muon precision-comparison row.",
 "saturation_factor_1440": SATURATION,
 "saturation_provenance": "144 (F_12 Fibonacci cage) × 10 (RT 3-fold axes)",
 },
 )
 print_summary(result)
 write_result(result)
 return result


if __name__ == "__main__":
 main()
