"""
verify_dm_line_centroid_postdiction_check.py — Independent centroid check for 3.55 keV DM line

Manuscript: E_vac = m_e c² / 144 = m_e (in eV) / 144
gct_constants.yaml derived value: 3.5486 keV
Observed (Bulbul et al. 2014, Perseus): 3.55 ± 0.03 keV
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import CODATA
from report import make_result, write_result, print_summary

N_CAGE = 144

def main():
 m_e_keV = CODATA.M_E_MEV * 1000.0
 E_vac_keV = m_e_keV / N_CAGE
 observed_keV = CODATA.E_DM_LINE_KEV
 sig_keV = CODATA.E_DM_LINE_SIG_KEV

 diff = abs(E_vac_keV - observed_keV)
 sigma_dist = diff / sig_keV
 ppm = diff / observed_keV * 1e6

 tolerance_ppm = 1000.0
 status = "PASS" if ppm <= tolerance_ppm else ("TENSION" if sigma_dist <= 2.0 else "FAIL")

 res = make_result(
 name="dm_line_3p55keV",
 app_r_label="3.55 keV X-ray line (E_vac)",
 formula="E_vac = m_e · c² / 144 (N=144 cage saturation)",
 predicted=E_vac_keV,
 observed=observed_keV,
 unit="keV",
 app_r_predicted=3.5486,
 app_r_precision_str=f"{ppm:.0f} ppm (within {sigma_dist:.2f}σ of observed line centroid)",
 app_r_precision_ppm=ppm,
 tier="Tier 3 postdiction-context centroid; operative P.3 falsifier is dm_line_width_morphology",
 status=status,
 tolerance_ppm=tolerance_ppm,
 extra={
 "centroid_separation_keV": diff,
 "sigma_distance_from_centroid": sigma_dist,
 "xrism_status_note": (
 "XRISM (3.75 Ms on 10 clusters) has not yet resolved the line. "
 "Upper limit 5× weaker than required to confirm/refute. App R "
 "lists status as Under Test — Data Inconclusive."
 ),
 },
 )
 print_summary(res); write_result(res)
 return res


if __name__ == "__main__":
 main()
