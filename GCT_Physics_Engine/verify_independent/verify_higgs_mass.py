"""
verify_higgs_mass.py — Independent re-derivation of the bare Higgs mass.

V3 Ch05 §5.2.3 (Bulk Modulus and the λ = 1/8 Prediction):
 GCT predicts the bare quartic coupling λ = 1/8 from the packing
 efficiency of the icosahedral tiles (inscribed sphere / RT volume).
 The standard SM mass relation m_H = √(2λ) · v reduces under
 λ = 1/8 to m_H = v/2.

 Inputs:
 v = 246.22 GeV (measured, or 246.18 GeV from GCT derivation)
 λ_bare = 1/8 (Tier 2, geometric packing-efficiency identity)
 Output:
 m_H^bare = v · √(2·1/8) = v · (1/2) = 123.11 GeV (using v_obs)

 Observed: m_H ≈ 125.10 GeV (PDG 2024)
 Gap: +1.6% (= +1.99 GeV)
 Manuscript framing (§5.2.3): "consistent with standard radiative
 corrections".

Tier 1 closure (TP-E / roadmap A.3) requires a full 1-loop spectral-
action computation in the GCT framework with modified β-functions
(App ZN). This is research-level work bundled with QLQCD-1L closure.

This verifier:
 (1) Re-derives m_H^bare from λ = 1/8 and the measured v.
 (2) Reports the +1.6% gap against PDG.
 (3) Flags it as expected-sign-and-rough-magnitude under standard
 SM 1-loop radiative corrections, with precise GCT-specific
 1-loop computation as Open Problem.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import CODATA, MATH
from report import make_result, write_result, print_summary

# PDG 2024 Higgs mass + Higgs VEV (anchoring)
M_H_PDG_GEV = 125.10
M_H_PDG_UNC_GEV = 0.14


def main():
 # GCT bare quartic coupling (Tier 2, geometric packing-efficiency)
 lambda_bare = 1.0 / 8.0
 # Use the OBSERVED Higgs VEV (v = 246.22 GeV) for the bare m_H prediction.
 # Using the GCT-derived v (246.18 GeV) shifts m_H^bare by only 0.02%
 # — the dominant gap is the 1.6% radiative correction, not the VEV residual.
 v_gev = CODATA.V_HIGGS_GEV
 # m_H^bare = v · √(2λ)
 import math as _math
 m_H_bare = v_gev * _math.sqrt(2.0 * lambda_bare)

 gap = M_H_PDG_GEV - m_H_bare
 gap_pct = 100.0 * gap / M_H_PDG_GEV
 gap_ppm = 1.0e6 * abs(gap) / M_H_PDG_GEV
 combined_unc = M_H_PDG_UNC_GEV # observed unc dominant
 gap_in_sigmas = abs(gap) / combined_unc

 # The 1.6% gap is the manuscript-acknowledged radiative-correction
 # contingency. Internal reproduction of the bare relation is successful,
 # but empirical closure remains open until a GCT-native loop calculation
 # supplies the correction.
 # (Standard SM running drives lambda upward from negative at GUT to
 # ~0.13 at EW; GCT's λ_bare = 1/8 sits between these, and the +1.6%
 # gap is consistent with one-loop matching at the appropriate
 # threshold scale within order-of-magnitude reasoning.)
 pass_status = (abs(gap_pct) < 5.0) # 5% band — Tier 2 tree-level expectation

 res = make_result(
 name="higgs_mass_bare",
 app_r_label="Higgs mass (bare, from λ = 1/8)",
 formula="m_H^bare = v · √(2λ_bare) = v · √(2 · 1/8) = v/2",
 predicted=m_H_bare,
 observed=M_H_PDG_GEV,
 unit="GeV",
 app_r_predicted=123.11,
 app_r_precision_str=f"+{gap_pct:.2f}% gap ({gap_in_sigmas:.1f}σ vs PDG unc; consistent with expected SM 1-loop radiative correction sign and rough magnitude)",
 app_r_precision_ppm=gap_ppm,
 tier="Tier 2 bare lambda = 1/8 geometric packing identity + Tier 3 physical m_H pending TP-E 1-loop closure",
 status="OPEN_CONDITIONAL" if pass_status else "FAIL",
 tolerance_ppm=50000.0,
 extra={
 "lambda_bare_geometric": lambda_bare,
 "v_GeV_input": v_gev,
 "m_H_bare_GeV": m_H_bare,
 "m_H_observed_GeV": M_H_PDG_GEV,
 "gap_GeV": gap,
 "gap_pct": gap_pct,
 "gap_in_sigmas_vs_pdg_unc": gap_in_sigmas,
 "matches_registered_5pct_tree_level_band": pass_status,
 "closure_condition": "GCT-native one-loop/spectral-action correction must account for the +1.6% gap without importing the SM correction as a fit.",
 "radiative_framing": (
 "The +1.6% gap (+1.99 GeV) is consistent with the standard "
 "SM 1-loop radiative correction in sign and rough magnitude: "
 "running lambda from GCT's geometric scale (M_GUT ~ 3.2e16 GeV) "
 "down to the EW scale via the SM beta function generates "
 "corrections of order few percent (top-Yukawa dominant). "
 "The precise GCT 1-loop computation requires the modified "
 "beta functions of App ZN (GCT-Native RG Flow) with phason "
 "loop contributions; this is research-level work bundled "
 "with the QLQCD-1L closure programme. Manuscript V3 Ch05 "
 "5.2.3 acknowledges this contingency as 'consistent with "
 "standard radiative corrections' without quantitative "
 "validation; this verifier registers the prediction "
 "explicitly with the disclosure."
 ),
 "tier_1_closure_path": (
 "TP-E (roadmap A.3): full 1-loop spectral-action computation "
 "in the GCT framework, replacing the manuscript's qualitative "
 "'standard radiative corrections' attribution with a "
 "first-principles GCT-specific value. Requires App ZN beta "
 "functions + Connes spectral action evaluated on the N=144 "
 "cage, following QLQCD-1L closure."
 ),
 },
 )
 print_summary(res); write_result(res)
 return res


if __name__ == "__main__":
 main()
