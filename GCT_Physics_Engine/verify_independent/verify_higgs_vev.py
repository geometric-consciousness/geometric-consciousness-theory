"""
verify_higgs_vev.py — Independent re-derivation of Higgs VEV (absolute pipeline)

App PSC §PSC.2 row 8:
 Formula: v = m_e · φ^11 · (1 + 5α_A3 + φ^8 α_A3^2) · 1440 · φ
 = m_mu · 1440 · φ
 App PSC: 246.1755 GeV (engine full precision) vs PDG 246.21965 → ~179 ppm

The registered factor 1440 = N_cage (=144) × N_RT_3foldAxes (=10) is exact
arithmetic conditional on the Tier 3 O.38 N_cage posit. O.20 enumerates the
factorisations but does not select this physical branch.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import CODATA, MATH, ppm_error
from report import make_result, write_result, print_summary, status_from_registered_band

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

 tolerance = 5000.0
 result = make_result(
 name="higgs_vev",
 app_psc_label="Higgs VEV (v)",
 formula="v = m_e · φ^11 · (1 + 5α_A3 + φ^8 α_A3^2) · 1440 · φ",
 predicted=v_gev,
 observed=observed,
 unit="GeV",
 app_psc_predicted=246.1755,
 app_psc_precision_str="179 ppm",
 app_psc_precision_ppm=179.0,
 tier=("OPEN-CONDITIONAL: Tier 2 product/mechanism arithmetic conditional "
       "on the Tier 3 O.38 N_cage=144 posit + A3 measured alpha input + "
       "Tier 3 calibrated-handle residual + Tier 4 as evidence that phi explains the value (constant control test v3 NEGATIVE-FRAGILE; App PSC §PSC.9.6)"),
 status=status_from_registered_band(
  ppm, tolerance, inside_status="OPEN_CONDITIONAL", outside_status="FAIL"
 ),
 tolerance_ppm=tolerance,
 extra={
 "m_mu_intermediate_MeV": m_mu,
 "alpha_codata_A3": alpha,
 "alpha_anchor": "A3 measured low-energy alpha (CODATA 2022) inherited from the muon precision-comparison row.",
 "saturation_factor_1440": SATURATION,
 "saturation_provenance": (
     "144 × 10 is exact arithmetic conditional on the Tier 3 O.38 "
     "N_cage=144 posit; O.20 enumeration does not select the branch."
 ),
 "o38_dependency": "OPEN: full lattice minimization has not selected N_cage=144.",
 },
 )
 print_summary(result)
 write_result(result)
 return result


if __name__ == "__main__":
 main()
