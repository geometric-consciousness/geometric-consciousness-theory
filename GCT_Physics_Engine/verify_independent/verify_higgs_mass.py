"""
verify_higgs_mass.py — Independent re-derivation of the bare Higgs mass.

V3 Ch05 §5.2.3 (Bulk Modulus and the λ = 1/8 Ansatz):
 GCT registers the bare quartic coupling λ = 1/8 as a Tier 3 packing
 ansatz on an added broken-vacuum completion. No geometric quantity is
 currently known to fix it (the earlier inscribed-sphere / RT-volume
 motivation is withdrawn: that ratio is ≈ 0.887, not 1/8), and the
 H3-invariant lattice action does not select this normalization.
 The standard SM mass relation m_H = √(2λ) · v reduces under
 λ = 1/8 to m_H = v/2.

 Inputs:
 v_GCT = 246.1755 GeV (the conditional GCT VEV evaluation, the convention of the top-quark row;
 with the measured v = 246.21965 GeV the result would be 123.11 GeV)
 λ_bare = 1/8 (Tier 3 bare packing ansatz)
 Output:
 m_H^bare = v · √(2·1/8) = v · (1/2) = 123.09 GeV (using v_GCT)

 Observed: m_H = 125.20 ± 0.11 GeV (PDG 2024 weighted average)
 Gap (prediction − observation): −1.69% (= −2.11 GeV; 19 sigma against
 the PDG uncertainty). The gap is not attributed to a computed correction
 (V3 Ch05 §5.2.3): λ = 1/8 lies near the SM MS-bar λ(m_t) ≈ 0.126, and the
 scale at which 1/8 applies is not derived.

Tier 1 closure (TP-E / roadmap A.3) requires a full 1-loop spectral-
action computation in the GCT framework with modified β-functions
(App GRF). This is research-level work bundled with QLQCD-1L closure.

This verifier:
 (1) Re-derives m_H^bare from λ = 1/8 and v_GCT.
 (2) Reports the −1.69% gap against PDG.
 (3) Attributes the gap to no computed correction and registers no
 prediction of its sign or size; a GCT-specific 1-loop computation
 (TP-E) is the open closure target.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import CODATA, MATH
from report import make_result, write_result, print_summary, status_from_registered_band

# PDG 2024 Higgs mass + Higgs VEV (anchoring)
M_H_PDG_GEV = 125.20
M_H_PDG_UNC_GEV = 0.11


def main():
 # GCT bare quartic coupling (Tier 3 packing ansatz)
 lambda_bare = 1.0 / 8.0
 # Use the GCT-derived VEV (the same convention as the top-quark row), re-derived
 # here from the absolute pipeline m_e phi^11 (1 + 5 alpha + phi^8 alpha^2) * 1440 * phi.
 # Using the measured v (246.21965 GeV) instead would give 123.11 GeV (0.02% higher).
 phi = MATH.PHI
 alpha = CODATA.ALPHA
 m_mu_geom_mev = CODATA.M_E_MEV * (phi ** 11) * (1.0 + 5.0 * alpha + (phi ** 8) * (alpha ** 2))
 v_gev = (m_mu_geom_mev / 1000.0) * 1440.0 * phi
 # m_H^bare = v · √(2λ)
 import math as _math
 m_H_bare = v_gev * _math.sqrt(2.0 * lambda_bare)

 gap = M_H_PDG_GEV - m_H_bare
 gap_pct = 100.0 * gap / M_H_PDG_GEV
 gap_ppm = 1.0e6 * abs(gap) / M_H_PDG_GEV
 combined_unc = M_H_PDG_UNC_GEV # observed unc dominant
 gap_in_sigmas = abs(gap) / combined_unc

 # The −1.69% gap (pred − obs, v_GCT) is not attributed to a computed
 # correction. Internal reproduction of the bare relation is successful,
 # but empirical closure remains open until a GCT-native loop calculation
 # supplies a correction. gap_GeV / gap_pct below are obs − pred (positive).
 # (λ_bare = 1/8 lies close to the SM MS-bar value λ(μ ≈ m_t) ≈ 0.126;
 # the scale at which it applies is not derived, and that proximity is
 # what makes the 1.69% gap look small.)
 tolerance = 50000.0
 derived_status = status_from_registered_band(
  gap_ppm, tolerance,
  inside_status="OPEN_CONDITIONAL", outside_status="FAIL",
 )

 res = make_result(
 name="higgs_mass_bare",
 app_psc_label="Higgs mass (bare, from λ = 1/8)",
 formula="m_H^bare = v · √(2λ_bare) = v · √(2 · 1/8) = v/2",
 predicted=m_H_bare,
 observed=M_H_PDG_GEV,
 unit="GeV",
 app_psc_predicted=123.09,
 app_psc_precision_str=f"−{gap_pct:.2f}% gap (pred − obs; {gap_in_sigmas:.1f}σ vs PDG unc; not attributed to a computed correction)",
 app_psc_precision_ppm=gap_ppm,
 tier="Tier 3 bare lambda = 1/8 packing ansatz on an added broken-vacuum completion + Tier 3 physical m_H pending TP-E 1-loop closure",
 status=derived_status,
 tolerance_ppm=tolerance,
 extra={
 "lambda_bare_geometric": lambda_bare,
 "v_GeV_input": v_gev,
 "v_convention": "v_GCT from the absolute Higgs-VEV pipeline (top-quark-row convention); measured v would give 123.11 GeV",
 "m_H_bare_GeV": m_H_bare,
 "m_H_observed_GeV": M_H_PDG_GEV,
 "gap_GeV": gap,
 "gap_pct": gap_pct,
 "gap_in_sigmas_vs_pdg_unc": gap_in_sigmas,
 "matches_registered_5pct_tree_level_band": derived_status == "OPEN_CONDITIONAL",
 "closure_condition": "GCT-native one-loop/spectral-action correction must account for the −1.69% (pred − obs) gap without importing the SM correction as a fit.",
 "radiative_framing": (
 "The −1.69% gap (pred − obs = −2.11 GeV) is not attributed to a computed "
 "correction. lambda_bare = 1/8 lies near the SM MS-bar value "
 "lambda(m_t) ~ 0.126, not near the value the SM runs to at "
 "M_GUT, and the scale at which 1/8 applies is not derived "
 "(V3 Ch05 5.2.3). A GCT-native 1-loop calculation (modified "
 "beta functions of App GRF with phason loop contributions, "
 "bundled with the QLQCD-1L closure programme) is the closure "
 "target. This verifier records the bare relation; it "
 "registers no prediction."
 ),
 "tier_1_closure_path": (
 "TP-E (roadmap A.3): full 1-loop spectral-action computation "
 "in the GCT framework, replacing the unattributed gap with a "
 "first-principles GCT-specific value. Requires App GRF beta "
 "functions + Connes spectral action evaluated on the N=144 "
 "cage, following QLQCD-1L closure."
 ),
 },
 )
 print_summary(res); write_result(res)
 return res


if __name__ == "__main__":
 main()
