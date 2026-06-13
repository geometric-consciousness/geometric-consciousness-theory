"""
verify_g2_muon.py — Cross-check of GCT contribution to muon g-2

INDEPENDENCE SCOPE: This verifier is NOT fully independent. Unlike the
CODATA/PDG-only scripts in this directory, it imports engine constants
from src/ (`gct_utils.C` for the geometric constants and the WP2025 SM
SSOT values). Its agreement with App R is therefore a CONSISTENCY CHECK
against the engine, not an independent corroboration of the muon g-2
result. (See README "independence contract"; the fully CODATA/PDG-anchored
scripts in this directory carry the independence claim.)

App R §R.2 row 2:
 Δa_μ (GCT) = (1/5) · (α_CODATA/π)^3 → ~250.65 × 10^-11
 WP2025 SM prediction: a_μ^SM = (116592033 ± 62) × 10^-11
   (Aliberti et al. arXiv:2505.21476, May 2025 Muon g-2 Theory Initiative
    White Paper; lattice-QCD-dominated HVP synthesis)
 Fermilab E989 Run 1-6 combined: a_μ^exp = (116592070.5 ± 14.8) × 10^-11
 WP2025 gap: a_μ^exp − a_μ^SM ≈ 37.5 × 10^-11 ; combined σ ≈ 63 × 10^-11
   → ~0.59σ, no significant anomaly under WP2025 synthesis.
 GCT prediction 250.65 × 10^-11 overshoots the gap by ~6.7×, sits at
   ~3.4σ above WP2025 SM. Channel disposition: Tier 2 mechanism + Tier 3
   1/5 coefficient + A3 + Tier 4 calibration-survival conjecture (HVP arbitration); Tension under WP2025,
   falsification conditional on long-term HVP-synthesis arbitration
   (Ch08 §8.7.3 / App G / App R §R.2).
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from constants import CODATA, MATH
from gct_utils import C
from report import make_result, write_result, print_summary


def main():
 alpha = CODATA.ALPHA
 pi = MATH.PI

 delta_a_mu_pred = (1.0 / 5.0) * (alpha / pi) ** 3

 # WP2025 (Aliberti et al. arXiv:2505.21476), imported from SSOT.
 a_mu_sm_wp2025 = float(C.MUON_G2_SM_WP2025)
 a_mu_sm_wp2025_sigma = float(C.MUON_G2_SM_WP2025_UNCERT)
 # Fermilab E989 Run 1-6 combined
 a_mu_exp = 116592070.5e-11
 a_mu_exp_sigma = 14.8e-11

 wp2025_gap = a_mu_exp - a_mu_sm_wp2025
 wp2025_gap_sigma = (a_mu_sm_wp2025_sigma ** 2 + a_mu_exp_sigma ** 2) ** 0.5
 wp2025_gap_in_sigmas = wp2025_gap / wp2025_gap_sigma

 # GCT prediction compared against the WP2025 SM-vs-experiment gap.
 sigma_tension_vs_wp2025_gap = abs(
 delta_a_mu_pred - wp2025_gap
 ) / wp2025_gap_sigma

 # Under WP2025, no significant SM-vs-experiment anomaly remains
 # (~0.6σ gap), and the GCT 250.65e-11 prediction is ~3.4σ above the
 # SM under the same lattice-QCD synthesis. Channel disposition:
 # Tier 2 mechanism + Tier 3 1/5 coefficient + A3 + Tier 4
 # calibration-survival conjecture (HVP arbitration); Tension under WP2025,
 # falsification conditional on long-term HVP-synthesis arbitration
 # (Ch08 §8.7.3 / App G).
 derived_status = "TENSION" # WP2025 synthesis: no anomaly for GCT to explain

 res = make_result(
 name="g2_muon",
 app_r_label="Muon g-2 GCT contribution",
 formula="Δa_μ = (1/5) · (α_CODATA/π)^3",
 predicted=delta_a_mu_pred,
 observed=wp2025_gap,
 unit="(dimensionless)",
 app_r_predicted=250.65e-11,
 app_r_precision_str=(
 f"WP2025 gap (a_exp − a_SM) = {wp2025_gap*1e11:+.1f}×10⁻¹¹ "
 f"at {wp2025_gap_in_sigmas:.2f}σ (no significant anomaly); "
 f"GCT prediction overshoots the gap by ~{delta_a_mu_pred/abs(wp2025_gap):.1f}× "
 f"and sits {sigma_tension_vs_wp2025_gap:.2f}σ above SM under lattice-QCD HVP. "
 f"Channel disposition: Tension under WP2025; falsification conditional on long-term "
 f"HVP-synthesis arbitration (Ch08 §8.7.3 / App G / App R §R.2)."
 ),
 app_r_precision_ppm=None,
 tier="Tier 2 mechanism + Tier 3 1/5 coefficient + A3 + Tier 4 calibration-survival conjecture (HVP arbitration); Tension under WP2025; falsification conditional on long-term HVP-synthesis arbitration",
 status=derived_status,
 tolerance_ppm=None,
 extra={
 "delta_a_mu_GCT_x_10_11": delta_a_mu_pred * 1e11,
 "a_mu_sm_wp2025_x_10_11": a_mu_sm_wp2025 * 1e11,
 "a_mu_sm_wp2025_sigma_x_10_11": a_mu_sm_wp2025_sigma * 1e11,
 "a_mu_exp_fermilab_final_x_10_11": a_mu_exp * 1e11,
 "a_mu_exp_sigma_x_10_11": a_mu_exp_sigma * 1e11,
 "wp2025_gap_x_10_11": wp2025_gap * 1e11,
 "wp2025_gap_sigma_x_10_11": wp2025_gap_sigma * 1e11,
 "wp2025_gap_in_sigmas": wp2025_gap_in_sigmas,
 "gct_prediction_in_sigmas_above_wp2025_sm": sigma_tension_vs_wp2025_gap,
 "hvp_synthesis": (
 "WP2025 (Aliberti et al. arXiv:2505.21476) adopts the "
 "lattice-QCD-dominated HVP average. Under this synthesis the "
 "SM-vs-experiment gap is ~0.6σ — no significant anomaly. "
 "The GCT 250.65×10⁻¹¹ phason-loop correction sits ~3.4σ above "
 "the WP2025 SM central value under the lattice synthesis. "
 "Channel disposition: Tension under WP2025; falsification "
 "conditional on long-term HVP-synthesis arbitration "
 "— validated-postdiction status is conditional on the HVP-Survival "
 "Condition (App V row P.5) holding under future R-ratio resolution."
 ),
 },
 )
 print_summary(res); write_result(res)
 return res


if __name__ == "__main__":
 main()
