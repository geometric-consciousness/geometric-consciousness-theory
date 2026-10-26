"""
verify_newton_g.py — Independent Newton-G consistency check via Jacobson chain

App PSC §PSC.2 row 7 (canonical figure):
 Formula chain (per protocol_absolute_scale.py prose):
 a_6 = (2 ħ / (m_e c)) · φ^-107 · (1 - 5α)
 G = c^3 · a_6^2 / (4 ħ)
 Model-authoritative branch (GCT bare alpha; CODATA m_e; exact SI h,c):
 6.689475523e-11, +2273.725 ppm against CODATA G.
 App PSC / Ledger / Ch09 / App ULA / App DPS / Ch22 all report 2274 ppm (0.23%)
 canonically. See App IVH §IVH.4 for the input-set reconciliation.

Not independent of the electron row: G ∝ m_e^-2 through a_6, so the G residual
is the electron Planck-link residual doubled ((1 + 1006.17 ppm)^2 - 1 = 2013.3 ppm
on the all-CODATA-alpha branch). The row therefore carries the P.1c LOCKED
1000 ppm electron rule, (1.001)^2 - 1 = 2001 ppm on G, and inherits P.1c's FAIL;
it is not counted as an independent pass (registry P.16).
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import CODATA, MATH, ppm_error
from report import make_result, write_result, print_summary

N_GEOM = -107
N_PHASON = 5
# P.1c LOCKED 1000 ppm electron rule carried through G ∝ m_e^-2.
INHERITED_ELECTRON_RULE_PPM = ((1.0 + 1000.0e-6) ** 2 - 1.0) * 1.0e6

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
 # Branch A: model-authoritative GCT-bare α with CODATA m_e and exact SI hbar, c.
 alpha_gct = (MATH.PHI ** 2) / 360.0
 A = G_from_chain(alpha_gct)
 # Branch B: CODATA α with CODATA m_e, hbar, c
 alpha_codata = CODATA.ALPHA
 B = G_from_chain(alpha_codata)

 G_obs = CODATA.G_SI # 6.67430e-11 (CODATA 2022)
 ppm_A = ppm_error(A["G_pred"], G_obs) # GCT-bare α, CODATA anchors
 ppm_B = ppm_error(B["G_pred"], G_obs) # CODATA-α throughout
 electron_equiv_A_ppm = ((A["G_pred"] / G_obs) ** 0.5 - 1.0) * 1.0e6
 electron_equiv_B_ppm = ((B["G_pred"] / G_obs) ** 0.5 - 1.0) * 1.0e6

 # The canonical scorecard claim comes from Branch A. It is a mixed model/anchor
 # evaluation, not an all-CODATA-alpha branch.
 result = make_result(
 name="newton_g",
 app_psc_label="Newton's G (Jacobson horizon chain)",
 formula="a_6 = (2 ħ / (m_e c)) · φ^-107 · (1 - 5α_GCT), α_GCT=φ^2/360; G = c^3 a_6^2 / (4 ħ)",
 predicted=A["G_pred"],
 observed=G_obs,
 unit="m^3 kg^-1 s^-2",
 app_psc_predicted=A["G_pred"],
 app_psc_precision_str="2273.725 ppm (display 2274 ppm) on model-authoritative alpha_GCT=phi^2/360 with CODATA m_e and exact SI h,c; Tier 2 thermodynamic mechanism + Tier 4 Planck-link conjecture (inherits O.14) + Tier 3 dimensional anchor",
 app_psc_precision_ppm=ppm_A,
 tier="Tier 2 thermodynamic mechanism + Tier 4 Planck-link conjecture (inherits O.14) + Tier 3 dimensional anchor + Tier 4 as evidence that phi explains the value (constant control test v3 NEGATIVE-FRAGILE; App PSC §PSC.9.6)",
 status="PASS" if ppm_A <= INHERITED_ELECTRON_RULE_PPM else "FAIL",
 tolerance_ppm=INHERITED_ELECTRON_RULE_PPM,
 extra={
 "branch_A_alpha_gct_codata_anchors": {
 "alpha": alpha_gct,
 "a_6_m": A["a_6_m"],
 "G_pred": A["G_pred"],
 "ppm_vs_CODATA_G": ppm_A,
 "same_branch_electron_equivalent_ppm": electron_equiv_A_ppm,
 "note": ("Model-authoritative GCT-bare α with CODATA-2022 m_e "
 "and exact SI hbar, c."),
 },
 "branch_B_alpha_codata_codata_anchors": {
 "alpha": alpha_codata,
 "a_6_m": B["a_6_m"],
 "G_pred": B["G_pred"],
 "ppm_vs_CODATA_G": ppm_B,
 "same_branch_electron_equivalent_ppm": electron_equiv_B_ppm,
 "note": "All-CODATA-α sensitivity branch; not the model-authoritative output.",
 },
 "inherited_rule": "P.1c LOCKED 1000 ppm electron rule -> (1.001)^2 - 1 = 2001 ppm on G; both branches miss it, so the row inherits P.1c's FAIL and is not an independent pass",
 "sigma_vs_CODATA_G_uncertainty_branch_A": ppm_A / 22.0,
 "sigma_vs_CODATA_G_uncertainty_branch_B": ppm_B / 22.0,
 "cascade_invariant": (
 "G/G_CODATA = (1 + electron_equivalent_residual)^2; "
 "branch A: 1136.217001 ppm -> 2273.724992 ppm; "
 "branch B: 1006.166275 ppm -> 2013.344921 ppm."
 ),
 },
 )

 # YAML carries the CODATA/SI anchors (G_SI, m_e, hbar, c); alpha_GCT is the
 # model input. The difference from Branch B is an alpha substitution, not
 # finite precision or measurement uncertainty in hbar/c.
 # App PSC / Ledger / Ch09 / App ULA / App DPS / Ch22 all report the
 # model-authoritative 2273.725 ppm value (display 2274 ppm).

 print_summary(result)
 write_result(result)
 return result


if __name__ == "__main__":
 main()
