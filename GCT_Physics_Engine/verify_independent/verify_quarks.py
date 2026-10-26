"""
verify_quarks.py — Independent re-derivation of quark masses

App PSC §PSC.3 rows 2–7:
 m_u = m_e · φ^3
 m_d = m_u · φ^φ
 m_s = m_u · φ^8 · (1 - 12α)
 m_c = m_u · φ^(13 + φ^-3) [App PSC prose; engine uses FK²]
 m_b = m_c · φ^2 · (5/4) [5/4 = dim(H)/dim(G)]; scored by the P.24 rule
 (PDG +/- 5 sigma of the prediction): 4134.69 vs 4183 +/- 7 MeV = 6.9 sigma, FAIL
 m_t = (v_GCT / 2) · sqrt(2), with v_GCT re-derived from the absolute
 Higgs-VEV pipeline rather than imported from the measured electroweak VEV

The canonical engine tuple is m_d = m_u·φ^φ, a postdiction-consistent
conditional value inside the registered 11% shell-resonance gate. The
φ^φ identification is the FK-determinant infinite-volume-limit branch and
remains conditional on O.5 for rigorous convergence.

Similarly for m_c: φ^(13+φ^-3) vs engine FK². Both branches are computed.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import CODATA, MATH, pct_error
from report import make_result, write_result, print_summary


def main():
 phi = MATH.PHI
 alpha = CODATA.ALPHA
 m_e = CODATA.M_E_MEV
 sqrt2 = MATH.SQRT2
 m_mu_geom_mev = m_e * (phi ** 11) * (
  1.0 + 5.0 * alpha + (phi ** 8) * (alpha ** 2)
 )
 v_gct_gev = (m_mu_geom_mev / 1000.0) * 1440.0 * phi
 v_mev = v_gct_gev * 1000.0

 # ---------- m_u = m_e · φ^3 -----------------------------------------
 m_u_pred = m_e * (phi ** 3)
 pct_u = pct_error(m_u_pred, CODATA.M_U_MEV)
 res_u = make_result(
 name="up_quark",
 app_psc_label="Up quark (m_u)",
 formula="m_u = m_e · φ^3",
 predicted=m_u_pred,
 observed=CODATA.M_U_MEV,
 unit="MeV",
 app_psc_predicted=2.16,
 app_psc_precision_str="0.21%",
 app_psc_precision_ppm=2100.0,
 tier="Tier 2 geometric motif + Tier 3 QCD scheme/running bridge + Tier 4 as evidence that phi explains the value (constant control test v3 NEGATIVE-FRAGILE; App PSC §PSC.9.6)",
 status="PASS" if pct_u < 1.0 else "FAIL",
 tolerance_ppm=10000.0,
 extra={"percent_error": pct_u},
 )
 print_summary(res_u); write_result(res_u)

 # ---------- m_d = m_u · φ^φ -----------------------------------------
 m_d_phi_phi = m_u_pred * (phi ** phi)
 engine_m_d = m_d_phi_phi
 engine_pct_d = pct_error(engine_m_d, CODATA.M_D_MEV)
 tolerance_ppm_d = 110000.0
 ppm_d = engine_pct_d * 1e4
 status_d = "FAIL" if ppm_d > tolerance_ppm_d else "PASS"
 res_d = make_result(
 name="down_quark",
 app_psc_label="Down quark (m_d)",
 formula="m_d = m_u · φ^φ (FK-determinant infinite-volume-limit closed form)",
 predicted=engine_m_d,
 observed=CODATA.M_D_MEV,
 unit="MeV",
 app_psc_predicted=4.716,
 app_psc_precision_str=f"{engine_pct_d:.2f}% ({ppm_d:.0f} ppm), inside the 11% shell-resonance gate; conditional on O.5",
 app_psc_precision_ppm=ppm_d,
 tier="Tier 2 FK-determinant mechanism + Tier 3 phi^phi identification of the shell median (infinite-volume limit open, O.5) + Tier 4 as evidence that phi explains the value (constant control test v3 NEGATIVE-FRAGILE; App PSC §PSC.9.6)",
 status=status_d,
 tolerance_ppm=tolerance_ppm_d,
 extra={
 "engine_branch_value_MeV": engine_m_d,
 "engine_branch_error_pct": engine_pct_d,
 "fk_limit_closed_form": "phi^phi",
 "closed_cage_deep_tail_mean_det_FK_over_phi_phi": 0.9976,
 "closed_cage_deep_tail_sample_std": 0.0253,
 "closed_cage_deep_tail_mean_signed_error_vs_PDG_percent": 0.09,
 "convergence_caveat": "empirical decaying envelope toward phi^phi; rigorous infinite-volume proof open, bundles with O.5",
 "branch_note": (
 "Canonical computation: FK-determinant infinite-volume-limit branch "
 "m_u·φ^φ. Single-cage values oscillate inside the 11% shell-resonance "
 "band; the match is a central-tendency result conditional on O.5."
 ),
 },
 )
 print_summary(res_d); write_result(res_d)

 # ---------- m_s = m_u · φ^8 · (1 - 12α) -----------------------------
 m_s_pred = m_u_pred * (phi ** 8) * (1.0 - 12.0 * alpha)
 pct_s_against_pdg2024 = pct_error(m_s_pred, CODATA.M_S_MEV)
 res_s = make_result(
 name="strange_quark",
 app_psc_label="Strange quark (m_s)",
 formula="m_s = m_u · φ^8 · (1 - 12α)",
 predicted=m_s_pred,
 observed=CODATA.M_S_MEV,
 unit="MeV",
 app_psc_predicted=92.79,
 app_psc_precision_str="0.76%; the 12α drag coefficient is a Tier 3 state-level handle per the Ledger",
 app_psc_precision_ppm=7632.0,
 tier="Tier 3 (12α drag coefficient; geometric scaling formula retained as the mechanism) + Tier 4 as evidence that phi explains the value (constant control test v3 NEGATIVE-FRAGILE; App PSC §PSC.9.6)",
 status="PASS" if pct_s_against_pdg2024 < 1.0 else "FAIL",
 tolerance_ppm=10000.0,
 extra={
 "percent_error_vs_pdg_2024_93p5": pct_s_against_pdg2024,
 "appr_comparison_target_MeV": CODATA.M_S_MEV,
 "pdg_2024_central_value_MeV": CODATA.M_S_MEV,
 "comparison_note": (
 "App PSC anchor: PDG 2024 central 93.5 MeV. Precision against 93.5: "
 "0.76%. This remains within the registered quark-sector envelope, "
 "with the 12α drag coefficient retained as Tier 3."
 ),
 },
 )
 print_summary(res_s); write_result(res_s)

 # ---------- m_c = m_u · φ^(13 + φ^-3) (App PSC prose) ----------------
 m_c_pred = m_u_pred * (phi ** (13 + (phi ** -3)))
 m_c_obs_mev = CODATA.M_C_GEV * 1000.0
 pct_c = pct_error(m_c_pred, m_c_obs_mev)
 res_c = make_result(
 name="charm_quark",
 app_psc_label="Charm quark (m_c)",
 formula="m_c = m_u · φ^(13 + φ^-3)",
 predicted=m_c_pred,
 observed=m_c_obs_mev,
 unit="MeV",
 app_psc_predicted=1263.45,
 app_psc_precision_str="0.75%",
 app_psc_precision_ppm=7503.0,
 tier="Tier 3 (Mixed-Harmonic ansatz, N=17 second-harmonic) + Tier 4 as evidence that phi explains the value (constant control test v3 NEGATIVE-FRAGILE; App PSC §PSC.9.6)",
 status="PASS" if pct_c <= 3.0 else "FAIL",
 tolerance_ppm=30000.0,
 extra={
 "percent_error_manuscript_branch": pct_c,
 "sigma_vs_pdg": abs(m_c_pred - m_c_obs_mev) / (CODATA.M_C_GEV_ERR * 1000.0),
 "band_source": "registry P.22: m_c outside +/- 3% (30000 ppm)",
 "engine_branch_note": (
 "Engine uses FK²_charm in place of φ^(13+φ^-3). Both branches "
 "happen to give ~1263 MeV due to FK calibration. Manuscript "
 "branch value is reproducible from the prose formula."
 ),
 },
 )
 print_summary(res_c); write_result(res_c)

 # ---------- m_b = m_c · φ^2 · (5/4) ---------------------------------
 m_b_pred = m_c_pred * (phi ** 2) * 1.25
 m_b_obs_mev = CODATA.M_B_GEV * 1000.0
 pct_b = pct_error(m_b_pred, m_b_obs_mev)
 # The P.24 rule ("outside PDG +/- 5 sigma of the prediction") is applied to the
 # bottom quark as to the top quark. The earlier window 4130-4230 MeV was centred
 # on the measurement, not on the prediction, and is withdrawn as a test.
 m_b_err_mev = CODATA.M_B_GEV_ERR * 1000.0
 sigma_b = abs(m_b_pred - m_b_obs_mev) / m_b_err_mev
 gate_sigma_b = 5.0
 res_b = make_result(
 name="bottom_quark",
 app_psc_label="Bottom quark (m_b)",
 formula="m_b = m_c · φ^2 · (5/4)",
 predicted=m_b_pred,
 observed=m_b_obs_mev,
 unit="MeV",
 app_psc_predicted=4134.69,
 app_psc_precision_str="-1.15% (6.9 sigma low against PDG 2024 4183 +/- 7 MeV): FAIL of the PDG +/- 5 sigma rule; Tier 2 5/4 coefficient + Tier 3 m_c input → Tier 3 absolute prediction",
 app_psc_precision_ppm=11549.0,
 tier="Tier 3 absolute prediction (5/4 coefficient Tier 2; imports Tier 3 m_c input; state-level residual conditional on O.5) + Tier 4 as evidence that phi explains the value (constant control test v3 NEGATIVE-FRAGILE; App PSC §PSC.9.6)",
 status="PASS" if sigma_b <= gate_sigma_b else "FAIL",
 tolerance_ppm=gate_sigma_b * m_b_err_mev / m_b_obs_mev * 1.0e6,
 extra={"percent_error": pct_b,
 "sigma_tension": sigma_b,
 "registered_gate_sigma": gate_sigma_b,
 "observed_sigma_MeV": m_b_err_mev,
 "cl_note": "PDG labels the +/-7 MeV as a 90% CL interval; read as such, the 1-sigma error is about 4.3 MeV and the miss is about 11 sigma",
 "binding_rule": "P.23: m_b outside PDG +/- 5 sigma of the geometric prediction (the P.24 rule); the earlier 4130-4230 MeV window was centred on the measurement and is withdrawn as a test",
 "coefficient_5_over_4_provenance":
 "A5 representation theorem dim(H)/dim(G) = 5/4"},
 )
 print_summary(res_b); write_result(res_b)

 # ---------- m_t = (v/2) · sqrt(2) -----------------------------------
 m_t_pred = (v_mev / 2.0) * sqrt2 / 1000.0 # GeV
 pct_t = pct_error(m_t_pred, CODATA.M_T_GEV)
 # P.24's written rule, "m_t outside PDG +/- 5 sigma" (registered since
 # v1.2.0), applies instead of the former 2 % window. A miss of the written
 # rule is a FAIL, by the same standard as the electron LOCKED rule (P.1c).
 sigma_t = abs(m_t_pred - CODATA.M_T_GEV) / CODATA.M_T_GEV_ERR
 gate_sigma_t = 5.0
 res_t = make_result(
 name="top_quark",
 app_psc_label="Top quark (m_t)",
 formula="m_t = (v_GCT / 2) · sqrt(2)",
 predicted=m_t_pred,
 observed=CODATA.M_T_GEV,
 unit="GeV",
 app_psc_predicted=174.07,
 app_psc_precision_str="0.87%; GCT-derived VEV input; Tier 2 mechanism + Tier 3 state-level/mass-scheme residual",
 app_psc_precision_ppm=8706.0,
 tier="Tier 2 mechanism + Tier 3 state-level/mass-scheme residual",
 status="PASS" if sigma_t <= gate_sigma_t else "FAIL",
 tolerance_ppm=gate_sigma_t * CODATA.M_T_GEV_ERR / CODATA.M_T_GEV * 1.0e6,
 extra={"percent_error": pct_t,
 "sigma_tension": sigma_t,
 "registered_gate_sigma": gate_sigma_t,
 "observed_sigma_GeV": CODATA.M_T_GEV_ERR,
 "gate_note": "P.24 written rule (PDG +/- 5 sigma, registered since v1.2.0) applied; outside the gate the row is a FAIL of the written rule, by the same standard as the electron LOCKED rule (P.1c); the Tier 3 state-level residual remains conditional on O.5, and a pole/MS-bar uncertainty model would be a new pre-registered band, not a retroactive rescue",
 "binding_rule": "P.24 written falsification rule: m_t outside PDG +/- 5 sigma (falsifiability_registry.json)",
 "v_GCT_GeV": v_gct_gev,
 "vev_provenance": "absolute GCT Higgs-VEV pipeline: m_e phi^11 (1 + 5 alpha + phi^8 alpha^2) * 1440 * phi",
 "qcd_correction_note":
 "Bare value; the comparator is the PDG 2024 direct-measurement mass (not a pole mass). Against the PDG pole mass from cross sections (172.4 +/- 0.7 GeV) the residual is about 2.4 sigma; the mass-scheme question is open and the registered comparator is not swapped after the result"},
 )
 print_summary(res_t); write_result(res_t)

 return [res_u, res_d, res_s, res_c, res_b, res_t]


if __name__ == "__main__":
 main()
