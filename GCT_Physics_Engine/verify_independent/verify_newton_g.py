"""
verify_newton_g.py — Independent Newton-G consistency check via Jacobson chain

App R §R.2 row 7 (canonical figure):
 Formula chain (per protocol_absolute_scale.py prose):
 a_6 = (2 ħ / (m_e c)) · φ^-107 · (1 - 5α)
 G = c^3 · a_6^2 / (4 ħ)
 Engine predicted (CODATA-2022 inputs): 6.68948e-11
 App R / Ledger / Ch09 / App M / App K / Ch22 all report 2274 ppm (0.23%)
 canonically. See App R2 §R2.4 for the input-set reconciliation.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import CODATA, MATH, ppm_error
from report import make_result, write_result, print_summary

N_GEOM = -107
N_PHASON = 5

def G_from_chain(alpha: float, m_e_kg: float = None, hbar: float = None,
 c: float = None) -> dict:
 phi = MATH.PHI
 if m_e_kg is None: m_e_kg = CODATA.M_E_KG
 if hbar is None: hbar = CODATA.HBAR
 if c is None: c = CODATA.C_LIGHT
 drag = 1.0 - N_PHASON * alpha
 a_6 = (2.0 * hbar / (m_e_kg * c)) * (phi ** N_GEOM) * drag
 G_pred = (c ** 3) * (a_6 ** 2) / (4.0 * hbar)
 return {"alpha": alpha, "a_6_m": a_6, "G_pred": G_pred, "drag": drag}

def main():
 # Branch A: GCT-bare α with CODATA m_e, hbar, c (true independent re-derivation)
 alpha_gct = (MATH.PHI ** 2) / 360.0
 A = G_from_chain(alpha_gct)
 # Branch B: CODATA α with CODATA m_e, hbar, c
 alpha_codata = CODATA.ALPHA
 B = G_from_chain(alpha_codata)

 G_obs = CODATA.G_SI # 6.67430e-11 (CODATA 2022)
 ppm_A = ppm_error(A["G_pred"], G_obs) # GCT-bare α, CODATA anchors
 ppm_B = ppm_error(B["G_pred"], G_obs) # CODATA-α throughout

 # The canonical scorecard claim comes from Branch A (true independent re-derivation
 # using GCT-bare α and CODATA-2022 m_e, hbar, c).
 result = make_result(
 name="newton_g",
 app_r_label="Newton's G (Jacobson horizon chain)",
 formula="a_6 = (2 ħ / (m_e c)) · φ^-107 · (1 - 5α); G = c^3 a_6^2 / (4 ħ)",
 predicted=A["G_pred"],
 observed=G_obs,
 unit="m^3 kg^-1 s^-2",
 app_r_predicted=6.68948e-11,
 app_r_precision_str="2274 ppm postdiction; Tier 2 thermodynamic mechanism + Tier 4 Planck-link conjecture (inherits O.14) + Tier 3 dimensional anchor",
 app_r_precision_ppm=2274.0,
 tier="Tier 2 thermodynamic mechanism + Tier 4 Planck-link conjecture (inherits O.14) + Tier 3 dimensional anchor",
 status="PASS" if ppm_A < 5000.0 else "FAIL",
 tolerance_ppm=5000.0,
 extra={
 "branch_A_alpha_gct_codata_anchors": {
 "alpha": alpha_gct,
 "a_6_m": A["a_6_m"],
 "G_pred": A["G_pred"],
 "ppm_vs_CODATA_G": ppm_A,
 "note": ("GCT-bare α with CODATA-2022 m_e, hbar, c. True "
 "independent re-derivation."),
 },
 "branch_B_alpha_codata_codata_anchors": {
 "alpha": alpha_codata,
 "a_6_m": B["a_6_m"],
 "G_pred": B["G_pred"],
 "ppm_vs_CODATA_G": ppm_B,
 "note": "CODATA α throughout — alt branch for sensitivity to α.",
 },
 },
 )

 # YAML carries full CODATA-2022 inputs
 # precision (G_SI 6.67430e-11, HBAR 1.054571817e-34, EV_TO_J 1.602176634e-19).
 # App R / Ledger / Ch09 / App M / App K / Ch22 all report 2274 ppm canonically.

 print_summary(result)
 write_result(result)
 return result


if __name__ == "__main__":
 main()
