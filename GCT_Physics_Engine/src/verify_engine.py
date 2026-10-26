#!/usr/bin/env python3
"""
GCT Master Verification Suite
Filename: verify_engine.py

- Step 0: Constants Integrity Check (gct_constants.validate()) before any protocol runs.
  If the SSOT YAML is malformed or missing constants, the suite aborts immediately.
- Core verification logic retained except for explicitly registered expected-nonpass dispositions.
"""

import sys
import io
import os
import subprocess
import json
import time
import math

from check_expected_outcomes import check_expected_outcomes

# Force UTF-8 output so protocol Unicode chars (≈ τ ξ → etc.) print cleanly on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Directory Constants (Relative to GCT_Physics_Engine/src/)
SRC_DIR  = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(SRC_DIR), "data")
CONFIG_DIR = os.path.join(os.path.dirname(SRC_DIR), "config")

# Ensure src directory is in path for subprocesses
src_path = os.path.abspath(SRC_DIR)
env_base = os.environ.copy()
env_base["PYTHONPATH"] = src_path + os.pathsep + env_base.get("PYTHONPATH", "")


def _as_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized == "true":
            return True
        if normalized == "false":
            return False
    return None


def evaluate_registered_claim_value(value, claim):
    """Evaluate one registry comparison without implying evidential scope.

    Scientific claims may target an external empirical value, while internal
    regressions belong to protocol/expected-outcome checks.  The caller uses
    ``verification_scope`` for reporting; this function only evaluates the
    declared comparison.
    """
    target = claim.get("target_value", claim.get("target"))
    tolerance = claim.get("tolerance", 1e-9)
    logic = claim.get("logic", "==")
    tolerance_type = claim.get("tolerance_type", "")

    if value is None:
        return False, logic
    if tolerance_type == "string_match":
        return str(target) in str(value), logic
    if tolerance_type == "exact_string":
        return str(value) == str(target), logic
    if tolerance_type == "exact_string_prefix_match":
        return str(value).startswith(str(target)), logic
    if tolerance_type in {"boolean", "boolean_match"}:
        actual_bool = _as_bool(value)
        target_bool = _as_bool(target)
        return (
            actual_bool is not None
            and target_bool is not None
            and actual_bool == target_bool
        ), logic
    if tolerance_type in {"lt", "lte", "gt", "gte"}:
        try:
            actual = float(value)
            expected = float(target)
            comparator = {
                "lt": (actual < expected, "<"),
                "lte": (actual <= expected, "<="),
                "gt": (actual > expected, ">"),
                "gte": (actual >= expected, ">="),
            }
            return comparator[tolerance_type]
        except (ValueError, TypeError):
            return False, logic
    if logic == "==":
        try:
            actual_diff = abs(float(value) - float(target))
            allowed_diff = tolerance
            if tolerance_type == "relative":
                allowed_diff = tolerance * abs(float(target))
            elif tolerance_type in {"ppm", "ppm_tri_state", "ppm_soft_tension"}:
                allowed_diff = abs(float(target)) * tolerance / 1_000_000.0
            return actual_diff <= allowed_diff, logic
        except (ValueError, TypeError):
            return str(value) == str(target), logic
    try:
        actual = float(value)
        expected = float(target)
        comparisons = {
            "<": actual < expected,
            ">": actual > expected,
            "<=": actual <= expected,
            ">=": actual >= expected,
        }
        return comparisons.get(logic, False), logic
    except (ValueError, TypeError):
        return False, logic


def validate_fine_structure_claim_contract(claim):
    """Fail closed if C_FINE_STRUCTURE stops being the external CODATA claim."""
    if claim.get("claim_id") != "C_FINE_STRUCTURE":
        raise ValueError("fine-structure contract validator received the wrong claim")

    errors = []
    if claim.get("json_field") != "alpha_bare_inv":
        errors.append("json_field must be alpha_bare_inv")
    if not math.isclose(
        float(claim.get("target_value", float("nan"))),
        137.035999177,
        rel_tol=0.0,
        abs_tol=1e-12,
    ):
        errors.append("target_value must be the CODATA 2022 alpha inverse")
    if claim.get("tolerance") != 5000 or claim.get("tolerance_type") != "ppm":
        errors.append("external comparison must use the registered 5000-ppm band")
    if claim.get("verification_scope") != "external_empirical_comparison":
        errors.append("verification_scope must remain external_empirical_comparison")
    if claim.get("claim_type") != "external_postdiction":
        errors.append("claim_type must remain external_postdiction")
    if "10.1103/RevModPhys.97.025002" not in claim.get("target_provenance", ""):
        errors.append("CODATA 2022 provenance DOI is missing")
    if errors:
        raise ValueError("C_FINE_STRUCTURE registry contract invalid: " + "; ".join(errors))
    return True

PROTOCOLS = [
    # 1. Core Hardware
    "protocol_absolute_scale.py",
    "protocol_phi_selection.py",
    "protocol_stiffness_ratio.py",
    "protocol_cage_minimization.py",
    "protocol_continuum_validation.py",

    # 2. Gauge Symmetries
    "protocol_gauge_uniqueness.py",
    "protocol_su3_proof_complete.py",
    "protocol_su3_complexification.py",
    "protocol_chirality_audit.py",
    "protocol_anomaly_check.py",
    "protocol_connes_isomorphism.py",

    # 3. Mass Spectrum
    "protocol_alpha_derivation.py",
    "protocol_hadron_topology.py",
    "protocol_exponent_derivation.py",
    "protocol_lepton_coefficients.py",
    "protocol_lepton_spectrum.py",
    "protocol_mass_corrections.py",
    "protocol_healing_length.py",
    "protocol_proton_berry_phase.py",
    "protocol_proton_mass.py",
    "protocol_quark_mismatch.py",
    "protocol_higgs_vev.py",

    # 4. Interactions & Mixing
    "protocol_electroweak.py",
    "protocol_mixing_geometry.py",
    "protocol_qed_audit.py",
    "protocol_fermion_audit.py",
    "protocol_geometric_rge.py",

    # 5. Astrophysics & Cosmology
    "protocol_core_cosmology_compat.py",
    "protocol_dark_energy.py",
    "protocol_dark_matter_fracture.py",
    "protocol_dm_line_forward_model.py",
    "protocol_lorentz_violation.py",
    "protocol_pta_anisotropy.py",
    "protocol_pta_l6_template.py",
    "protocol_sdss_l6.py",
    "protocol_ta_hotspot.py",
    "protocol_neutrino_precision.py",
    # Manuscript-cited standalones included in the in-suite cross-claim
    # audit to guard against silent drift in checked outputs.
    "protocol_imp01_pipeline.py",          # Ch14 §14.5 IMP-01 biogenic-DE pipeline
    "protocol_de_multichannel.py",          # Ch14 §14.6.3 4032-point multi-channel sweep
    "protocol_o13_intra_class2_dynamics.py", # Ch14 §14.6.2 Class-2 envelope

    # 6. Biophysics & Awareness
    "protocol_zeno_energy_budget.py",
    "protocol_decoherence_audit.py",
    "protocol_isotope_experiment.py",
    "protocol_subjective_lagrangian.py",
    "protocol_iit_phi_pyphi.py",
    "protocol_psychophysics_color_dim.py",
    "protocol_rashba_phason.py",

    # 7. System Integrity
    "protocol_microscopic_consistency_audit.py",
    "protocol_alpha_1loop.py",
    "protocol_cft_boundary.py",
    "protocol_ledger_closeout.py",
    "protocol_preregistration.py",
    "protocol_ncg_spectral_geometry.py",
    "protocol_lee_extended.py",
    "protocol_spectral_action.py",
    "gct_mckay_e8.py",
    "protocol_mckay_tier1.py",
    "protocol_aps_index_proof.py",
    # Manuscript-cited integer-anchor closure (App ORQ O.14 path (l) +
    # App ORQ O.26 D=18 anchor verification)
    "protocol_o14_coxeter_exponent_squares.py",
    # Closure Lindblad small-N verification of the
    # chiral-OAM DFS suppression (Ch17 §17.1.3c + App ORQ O.23).
    "protocol_o23_lindblad_explicit.py",
    # Closure Protocol D Monte Carlo systematics propagation
    # (Ch16 §16.3.4). Registered as expected non-PASS in
    # EXPECTED_NON_PASS — the operationally-unfalsifiable verdict at
    # Bonferroni-corrected significance under the §16.3.4 budget is the
    # pre-registered structural finding, not a failure.
    "protocol_d_mc_systematics.py",
    # App ORQ O.13 fingerprint (iv): conditional catalogue of standard
    # clustering-DE equations and stipulated template arithmetic. Physical
    # source mapping remains open, so the registered outcome is non-PASS.
    "protocol_clustering_de_framework.py"
]

# Some scripts write output to a non-standard filename (i.e. not the default
# <scriptname_without_py>_results.json). Map them here.
JSON_OVERRIDE = {
    "protocol_su3_proof_complete.py": "protocol_su3_proof_complete_results.json",
    "protocol_fermion_audit.py": "protocol_fermion_audit_results.json",
    "protocol_zeno_energy_budget.py": "protocol_zeno_energy_budget_results.json",
    "protocol_spectral_action.py": "spectral_action_results.json",
    "gct_mckay_e8.py": "mckay_e8_report.json",
    "protocol_mckay_tier1.py": "protocol_mckay_tier1_results.json"
}

# Protocols whose intrinsic verdict is non-PASS by design (an open closure
# under a registered Open Problem, or a registered external-data tension).
# For these, the canonical PASS criterion is that the actual verdict
# matches the registered expected verdict — drift to a different verdict
# (or an unexpected positive closure) is the genuine failure mode.
#
# This realises the pre-registration pattern at the protocol-PASS layer:
# "expected to fail in a specific way" -> PASS-expected-verdict-match;
# "fails in an unexpected way" -> DRIFT (alarming). Each protocol's JSON
# output preserves its native `pass` field (which reflects the protocol's
# own intrinsic closure status); verify_engine's verdict layer interprets
# the expected non-PASS protocols against their registered expected verdict.
EXPECTED_NON_PASS = {
    "protocol_electroweak.py": {
        "json": "protocol_electroweak_results.json",
        "check": lambda d: (
            d.get("pass") is False
            and d.get("status") == "FAILED_CHECK__H_EW_HYPOTHESIS_OPEN"
            and d.get("physical_boundary_derived") is False
            and d.get("physical_endpoint_predicted_autonomously") is False
            and d.get("projector_audit", {}).get("machine_pass") is True
            and d.get("projector_audit", {}).get("raw_ratio_coordinate_invariant") is False
            and d.get("rge_convention", {}).get("sm_coefficient_audit_pass") is True
            and abs(float(d.get("sin2_red", 0.0)) - 0.1367253) < 1e-5
            and float(d.get("error_red", 0.0)) > 0.40
        ),
        "rationale": "Canonical projectors give a 1/2+1/2 split and the bare angle phi^-3 is the Tier 3 hypothesis H-EW. With full-SM one-loop coefficients the one-coupling-conditioned reduced-scale comparator gives about 0.136725 (roughly 41% low); no RGE support for H-EW.",
    },
    "protocol_quark_mismatch.py": {
        "json": "protocol_quark_mismatch_results.json",
        "check": lambda d: (
            d.get("pass") is False
            and d.get("verdict") == "REGISTERED_GATE_FAIL_B_T__D_FK_GATE_PASS"
            and d.get("d_gate_pass") is True
            and d.get("per_quark_status", {}).get("t") == "FAIL"
            and d.get("per_quark_status", {}).get("b") == "FAIL"
        ),
        "rationale": "Top (P.24) and bottom (P.23) are scored against their registered PDG +/-5 sigma rules and FAIL (5.18 sigma, 6.90 sigma), as in App FSM/PSC and V3 Ch10; the down-quark FK gate (P.20) still passes and is asserted separately.",
    },
    "protocol_absolute_scale.py": {
        "json": "protocol_absolute_scale_results.json",
        "check": lambda d: (
            d.get("pass") is False
            and d.get("verdict") == "FAIL_INHERITED_P1C_2001PPM_RULE__UPSTREAM_CASCADED"
            and d.get("band_status") == "OUTSIDE_REGISTERED_BAND"
            and 2273.7 < float(d.get("ppm_error", 0.0)) < 2273.8
        ),
        "rationale": "Newton-G absolute scale misses the inherited 2001 ppm rule at 2273.725 ppm (App FSM P.16, OUTSIDE_REGISTERED_BAND); the residual is upstream-cascaded and the failed elasticity route adds no closure (V2 Ch09, App TPR).",
    },
    "protocol_geometric_rge.py": {
        "json": "protocol_geometric_rge_results.json",
        "check": lambda d: (
            d.get("pass") is False
            and d.get("status") == "QUARANTINED_ENDPOINT_BY_CONSTRUCTION"
            and d.get("h_ew_boundary", {}).get("derived_from_kernel") is False
            and d.get("target_normalized_integrator_check", {}).get("observed_endpoint_used_as_input") is True
            and d.get("target_normalized_integrator_check", {}).get("integrator_pass") is True
            and d.get("target_normalized_integrator_check", {}).get("physical_prediction") is False
            and d.get("sin2_w_predicted") is None
        ),
        "rationale": "The spectral-kernel endpoint match is target-normalised and therefore only an integrator check; the H-EW boundary is a Tier 3 hypothesis and no physical endpoint is predicted.",
    },
    "protocol_gauge_uniqueness.py": {
        "json": "protocol_gauge_uniqueness_results.json",
        "check": lambda d: (
            d.get("pass") is False
            and d.get("verdict") == "OPEN_CANDIDATE_SPECIFICITY_NOT_ESTABLISHED"
            and d.get("rt_candidate_witness") is True
            and d.get("RhombicTriacontahedron", {}).get("gram_rank") == 6
            and d.get("MatchedAxis_Control", {}).get("discriminates_rt") is False
            and d.get("MonteCarlo_Control", {}).get("reached_algebra_test") == 0
        ),
        "rationale": "The RT ten-axis inventory gives Gram rank 6 and an 8-dimensional closure with an A2 Cartan matrix, but generic matched ten-axis sets do the same and no random polyhedron reaches the algebra test; RT specificity is not established and the SU(3) identification is an open Tier 3 candidate (O.39).",
    },
    "protocol_cage_minimization.py": {
        "json": "protocol_cage_minimization_results.json",
        "check": lambda d: (
            d.get("status") == "ASSUMED_NOT_COMPUTED"
            and d.get("pass") is False
            and d.get("optimal_N_assumed") == 144
            and "O.38" in str(d.get("tier", ""))
        ),
        "rationale": "Cage minimization carries a conservative Tier 3 disposition: N=144 is an analytic-branch Tier 3 structural posit until the full R>=10 lattice scan closes O.38.",
    },
    "protocol_dixmier_trace_scaling.py": {
        "json": "protocol_dixmier_trace_scaling_results.json",
        "check": lambda d: (
            d.get("type_check_pass") is True
            and d.get("dixmier_trace_pass") is False
            and d.get("status") == "open_problem_O.14"
        ),
        "rationale": "Dixmier trace scaling currently type-checks the finite Dirac operator but does not close the Connes-Moscovici residue computation; intrinsic pass remains false until O.14 closes.",
    },
    "protocol_exponent_derivation.py": {
        "json": "protocol_exponent_derivation_results.json",
        "check": lambda d: (
            d.get("arithmetic_consistency_pass") is True
            and d.get("o14_physical_link_closed") is False
            and d.get("status") == "open_problem_O.14"
            and d.get("pass") is False
            and d.get("verdict") == "ARITHMETIC_PASS__O14_PHYSICAL_LINK_OPEN"
        ),
        "rationale": "Electron exponent arithmetic closes the registered n=107 counting check, but the physical V->K_0 trace-image/Dixmier-residue selection remains App ORQ O.14; intrinsic protocol pass remains false until that link closes.",
    },
    "protocol_connes_isomorphism.py": {
        "json": "protocol_connes_isomorphism_results.json",
        "check": lambda d: (
            d.get("necessary_condition_pass") is True
            and d.get("spectral_triple_identification_pass") is False
            and d.get("verdict") == "NECESSARY_CONDITION_PASS__FULL_SPECTRAL_TRIPLE_OPEN"
        ),
        "rationale": "Connes-isomorphism protocol currently closes only the 24-dimensional algebra-count necessary condition; full spectral-triple identification remains pending O.32 full closure, first-order/order-zero conditions, and dressed-Dirac checks.",
    },
    "protocol_rashba_phason.py": {
        "json": "protocol_rashba_phason_results.json",
        "check": lambda d: str(d.get("verdict", "")).startswith("COUPLING_FORM_NOT_A5_SCALAR"),
        "rationale": "A5 character computation: mult_1[(3x3')x3] = 0, so the Eq. 17.3 cross-product coupling is not an icosahedral scalar for the vector phason; coupling form, sign and magnitude remain Tier 3/open (V1 Ch17 §17.1.3).",
    },
    "protocol_decoherence_audit.py": {
        "json": "protocol_decoherence_audit_results.json",
        "check": lambda d: str(d.get("verdict", "")).startswith("BARE_MS_EXTENSION_INSUFFICIENT"),
        "rationale": "Bare Misra-Sudarshan extension correctly reports INSUFFICIENT; closure pending Open Problem O.23 (chiral phonon-polariton DFS).",
    },
    "protocol_alpha_derivation.py": {
        "json": "protocol_alpha_derivation_results.json",
        "check": lambda d: (
            d.get("status") == "OPEN_CONDITIONAL"
            and d.get("tree_level_within_0p5pct_band") is True
            and d.get("external_comparison_pass") is True
            and d.get("formula_regression_pass") is True
            and d.get("precision_validation_pass") is False
            and d.get("pass") is False
            and float(d.get("ppm_error", 0.0)) > 3000.0
        ),
        "rationale": "Bare alpha 360*phi^-2 is within the tree-level 0.5% band but remains OPEN_CONDITIONAL; the protocol must not count the 3443 ppm residual as a precision PASS.",
    },
    "protocol_alpha_1loop.py": {
        "json": "protocol_alpha_1loop_results.json",
        "check": lambda d: (
            d.get("sign_topology_consistency_pass") is True
            and d.get("magnitude_closure_pass") is False
            and d.get("pass") is False
            and int(d.get("tier_C_ico_value", 0)) == 3
        ),
        "rationale": "Alpha one-loop audit records sign/topology consistency separately while keeping magnitude closure as an expected non-PASS until O.19/O.5 closes.",
    },
    "protocol_qed_audit.py": {
        "json": "protocol_qed_audit_results.json",
        "check": lambda d: (
            d.get("muon_g2", {}).get("verdict") == "TENSION"
            and abs(float(d.get("muon_g2", {}).get("sigma_after", 0.0))) > 0.6
            and not bool(d.get("pass_compatible"))
        ),
        "rationale": "QED audit reports the muon g-2 channel as TENSION under the WP2025 lattice-dominant HVP synthesis: Tier 2 mechanism + Tier 3 1/5 coefficient + A3 + Tier 4 calibration-survival conjecture; falsification conditional on long-term HVP-synthesis arbitration.",
    },
    "protocol_aps_index_proof.py": {
        "json": "protocol_aps_index_proof_results.json",
        "check": lambda d: (
            d.get("aps_eta_evaluated") is False
            and d.get("aps_index_evaluated") is False
            and d.get("aps_boundary_operator_domain_specified") is False
            and float(d.get("scalar_adjacency_sign_sum", 0.0)) == -14.0
            and float(d.get("discrete_dirac_sign_sum", 1.0)) == 0.0
            and d.get("pass") is False
        ),
        "rationale": "Finite-cage diagnostic reports the scalar-adjacency sign sum (-14) and the distinct full discrete-Dirac sign sum (0); no qualifying APS operator/domain, eta-invariant, or index is evaluated.",
    },
    "protocol_global_significance.py": {
        "json": "protocol_global_significance_results.json",
        "check": lambda d: (
            d.get("pass") is False
            and d.get("cross_base_monte_carlo", {}).get("n_non_phi_bases_hitting_all_four") == 0
            and d.get("cross_base_monte_carlo", {}).get("phi_bare_passes_all_four_targets") is False
            and d.get("cross_base_monte_carlo", {}).get("phi_corrected_passes_all_four_targets") is True
            and d.get("cross_base_monte_carlo", {}).get("status") == "WITHDRAWN_NON_INFORMATIVE"
            and d.get("cross_base_monte_carlo", {}).get("alpha_interval_inside_exclusion_window") is True
            and "sigma_joint_two_sided" not in d.get("cross_base_monte_carlo", {})
            and d.get("lepton_lea", {}).get("lepton_exponent_pair", {}).get("status") == "WITHDRAWN_NON_INFORMATIVE"
            and d.get("lepton_lea", {}).get("lepton_exponent_pair", {}).get("canonical") is False
            and "lea_corrected_sigma" not in d.get("lepton_lea", {}).get("lepton_exponent_pair", {})
            and d.get("canonical_sigma") is None
        ),
        "rationale": "Cross-base Monte Carlo and expanded lepton grid are registered expected non-passes with status WITHDRAWN_NON_INFORMATIVE: the alpha condition admits only bases inside the excluded phi window, so no non-phi base can pass by construction; the lepton grid evaluates phi only with a post hoc 21 ppm window and a covering (C1, C2) grid. Neither emits a sigma; no global significance is claimed.",
    },
    "protocol_microscopic_consistency_audit.py": {
        "json": "protocol_microscopic_consistency_audit_results.json",
        "check": lambda d: (
            d.get("defect_verdict") == "ASSUMED_NOT_COMPUTED_O38_PENDING"
            and int(d.get("N_optimal_assumed", 0)) == 144
            and d.get("cage_status") == "ASSUMED_NOT_COMPUTED"
            and d.get("pass") is False
        ),
        "rationale": "Microscopic cage audit inherits the O.38 demotion: N=144 is an analytic-branch Tier 3 structural posit until FULL_LATTICE_MODE completes the R>=10 minimization.",
    },
    "protocol_mixing_geometry.py": {
        "json": "protocol_mixing_geometry_results.json",
        "check": lambda d: (
            d.get("pass") is False
            and d.get("ckm", {}).get("s12_status") == "TENSION"
            and d.get("pmns", {}).get("theta23_status") == "WITHIN_3SIGMA_OCTANT_UNRESOLVED"
        ),
        "rationale": "The registered tension is CKM s12 (corrected Cabibbo formula, ~3.6 sigma against PDG 2024). PMNS theta_23 = 45 deg lies inside the NuFIT 6.0 3-sigma ranges with and without SK atmospheric data (octant unresolved; the earlier 4.09-sigma one-octant Gaussian is withdrawn); CKM Jarlskog prefactor pending Open Problem O.7.",
    },
    "protocol_lepton_spectrum.py": {
        "json": "protocol_lepton_spectrum_results.json",
        "check": lambda d: (
            d.get("verdict") == "ANALYTIC_PASS_GRAPH_TENSION"
            and d.get("graph_passed") is False
            and abs(float(d.get("muon_error_graph_ppm", 0.0))) > float(d.get("graph_pass_tolerance_ppm", 1000.0))
            and bool(d.get("muon_second_order", {}).get("error_ppm", 1e9) < 2500.0)
        ),
        "rationale": "Lepton analytic limit remains the registered mass formula check, while the finite-N graph extraction gates on mass residuals. The current graph branch is a disclosed TENSION because the muon graph residual is far above the 1000 ppm graph tolerance.",
    },
    "protocol_zeno_energy_budget.py": {
        "json": "protocol_zeno_energy_budget_results.json",
        "check": lambda d: (
            d.get("verdict") == "CENTRAL_N_RP_ZERO_O21_PENDING_WITH_SENSITIVITY_BRANCH"
            and d.get("B2_cooperativity", {}).get("verdict") is False
            and d.get("B2_cooperativity", {}).get("N_bio_central") == 0.0
            and d.get("B2_cooperativity", {}).get("sensitivity_branch", {}).get("verdict") is True
            and d.get("B3_energy_balance", {}).get("check1_spins_sufficient") is False
            and d.get("B5_chiral_polariton_dfs", {}).get("reaches_operative_target_100us") is True
            and d.get("B5_chiral_polariton_dfs", {}).get("reaches_selection_target_10ms") is False
            and d.get("B2_cooperativity", {}).get("N_bio_basis", "").startswith("central beta-tubulin branch n_rp=0")
            and "Posner" in d.get("disposition_text", "")
        ),
        "rationale": "Zeno energy-budget audit uses the central beta-tubulin n_rp=0 baseline pending O.21 and reports the n_rp=1 beta-Trp inventory only as a sensitivity branch. The sensitivity branch preserves the arithmetic cooperativity ratio, but it is not the live central verdict; O.23 DFS dressing reaches the 100 us floor but remains below the 10 ms target; the Posner concentration estimate is retained only as a secondary proxy, not load-bearing closure.",
    },
    # Manuscript-cited standalones promoted into the in-suite cross-claim
    # audit. These protocols output structural-data dictionaries rather than
    # top-level pass: True/False fields; their canonical PASS criterion is
    # that the output dictionary carries the expected structural verdict.
    "protocol_imp01_pipeline.py": {
        "json": "protocol_imp01_pipeline_results.json",
        "check": lambda d: (
            isinstance(d.get("headline_run"), dict)
            and "w0_CPL_fit" in d["headline_run"]
            and "wa_CPL_fit" in d["headline_run"]
            and d["headline_run"]["w0_CPL_fit"] < -1.0   # asymptote-from-below shape
        ),
        "rationale": "IMP-01 biogenic-DE pipeline (Ch14 §14.5) headline run produces the CPL fit on the asymptote-from-below w(z) curve; structural-output PASS criterion is that the headline_run dict carries the CPL coefficients with the phantom-direction shape w0 < -1.",
    },
    "protocol_de_multichannel.py": {
        "json": "protocol_de_multichannel_results.json",
        "check": lambda d: d.get("closure_verdict") == "CLOSURE-FAILS",
        "rationale": "Multi-channel shape-proxy partition closure failure to the DESI CPL fit is the registered diagnostic structural verdict (Ch14 §14.6.3 + App PSC §PSC.8 row 8): Tier 2 convex-combination EoS identity plus Tier 3 shape-proxy parametrizations/calibrated amplitudes. The failure is restricted to the registered five-channel menu; any GCT-derivable quintessence-today channel discovery remains App ORQ O.13 open closure path.",
    },
    "protocol_o13_intra_class2_dynamics.py": {
        "json": "protocol_o13_intra_class2_dynamics_results.json",
        "check": lambda d: (
            isinstance(d.get("kardashev_band_envelope_dw_z028"), list)
            and len(d["kardashev_band_envelope_dw_z028"]) == 2
        ),
        "rationale": "Class-2 intra-Class-2-dynamics envelope (Ch14 §14.6.2 + App ORQ O.13 closure path) outputs the Kardashev-band |Δw(z=0.28)| range; structural-output PASS criterion is that the envelope is produced as a 2-element [min, max] list.",
    },
    # protocol_o14_coxeter_exponent_squares writes a top-level pass: True
    # field directly (see the protocol main()); it's a positive Tier 2
    # closure (uniqueness match for H_3 ↔ 107) rather than an expected
    # non-pass disclosure, so it does NOT need to be in EXPECTED_NON_PASS —
    # run_protocol handles it natively now that pass: True is written.
    # Protocol D MC systematics: pre-registered structural verdict
    # (S2 now perturbs synthetic
    # data, N=10000 trials, parametric Gaussian z-test gate, C1/C2
    # closure-path sub-runs executed): the §16.3.4 registered systematic-
    # error budget renders the assay operationally unfalsifiable at
    # Bonferroni-corrected significance across the predicted signed
    # n_rp=1 sensitivity band, simulated at 0.10%/0.20% (parametric power = 0.00 at both effects, systematic SD far above
    # the 0.10% gate). Closure path C2 (widen gate to
    # 0.20%) reports empirical power at the 0.20% effect under the
    # registered budget, but its null false-positive rate remains
    # uncontrolled; C1 alone gives only 1.20x SD reduction (not the
    # 2.5x target under the registered assay-budget interpretation).
    "protocol_d_mc_systematics.py": {
        "json": "protocol_d_mc_systematics_results.json",
        "check": lambda d: d.get("verdict_status", "").startswith("BELOW_TARGET_POWER_AT_010_PCT_EFFECT")
                            and not bool(d.get("closure_path_pass_at_least_one_of_C1_C2", True))
                            and not bool(d.get("closure_path_C2_widen_gate_to_020_pct", {}).get("target_met_at_0p20pct_effect_with_false_positive_gate", True)),
        "rationale": "Protocol D systematic-error budget at Ch16 §16.3.4 (S1-S6) renders the assay operationally unfalsifiable at Bonferroni-corrected significance across the n_rp=1 sensitivity band [-0.22%, -0.11%] (the MC simulates 0.10% and 0.20% effects) under the MC specification (S2 perturbs synthetic data; N=10000 parametric Gaussian z-test gate; C1/C2 sub-runs executed). C2's apparent empirical power is invalid because the null false-positive rate is uncontrolled, so the closure-path-pass flag must remain false until both power and FPR gates are satisfied.",
    },
    "protocol_clustering_de_framework.py": {
        "json": "protocol_clustering_de_framework_results.json",
        "check": lambda d: (
            d.get("pass") is False
            and d.get("verdict_status")
            == "CONDITIONAL_FRAMEWORK_CATALOGUED__PHYSICAL_SOURCE_MAP_OPEN"
        ),
        "rationale": "The protocol catalogues standard clustering-DE equations and conditional source-proxy template arithmetic only. It does not derive a canonical GCT channel; typed coupling, normalized source map, second-order/windowed statistic, causal identification, and covariance-aware likelihood remain open.",
    },
    # Lindblad explicit (closure-path-(a) numerical verification
    # of the O.23 DFS suppression under chiral OAM bath vs symmetric bath
    # collective-coupling discrimination), using sigma_- collapse operators
    # per canonical Tavis-Cummings DFS algebra, symmetric collective bath
    # as proper control (not bath absence), and strict monotonic-increasing
    # predicate + magnitude threshold:
    # the chiral OAM-l=1 collective sigma_- bath gives strictly larger T_2
    # than the symmetric OAM-l=0 collective sigma_- bath (DFS direction
    # confirmed), but the small-N tractable end (N=2-5) sits below the
    # asymptotic sqrt(N) enhancement regime. DFS ratio decreases from
    # ~1.96 (N=2) to ~1.61 (N=5) under the residual per-dimer
    # dephasing/emission channels. The pre-registered structural verdict
    # is DFS_SUPPRESSION_NOT_DEMONSTRATED at the small-N tractable end;
    # the analytic sqrt(N) extrapolation to the microtubule-bundle
    # N ~ 10^3 regime remains the operative framework-level closure
    # (companion protocol protocol_o23_dfs_collective_dressing.py).
    "protocol_o23_lindblad_explicit.py": {
        "json": "protocol_o23_lindblad_explicit_results.json",
        "check": lambda d: d.get("verdict_status", "") == "DFS_SUPPRESSION_NOT_DEMONSTRATED",
        "rationale": "Lindblad small-N test (N=2..5) confirms DFS direction (chiral OAM-l=1 bath gives larger T_2 than symmetric OAM-l=0 bath) but does not reach the strict 2x magnitude threshold at the tractable small-N end. The asymptotic sqrt(N) collective-dressing enhancement applies at N ~ 10^3 microtubule-bundle scale, not at N = 2..5; the small-N regime is below the asymptotic dark-state limit because per-dimer dephasing/emission channels (sigma_z + sigma_- on individual sites) leak the |W> coherence at small rate.",
    },
    "protocol_iit_phi_pyphi.py": {
        "json": "protocol_iit_phi_pyphi_results.json",
        "check": lambda d: (
            isinstance(d.get("subsystem_phi"), list)
            and bool(d["subsystem_phi"])
            and (
                (
                    str(d.get("pyphi_dependency_status", "")).startswith("unavailable")
                    and d.get("status") == "NEEDS_PYPHI"
                    and d.get("pass") is False
                )
                or (
                    d.get("pyphi_dependency_status") == "available"
                    and d.get("status") == "SELECTED_SUBGRAPH_POSITIVE__O28_PENDING"
                    and d.get("phi_selected_subgraph_positive_k2_to_k5") is True
                    and d.get("phi_selected_subgraph_witness_k2_to_k5_positive") is True
                    and all(float(r.get("phi", 0.0)) > 0.0 for r in d["subsystem_phi"])
                )
            )
        ),
        "rationale": "IIT Phi audit records PyPhi dependency status explicitly. Dependency-unavailable runs must report NEEDS_PYPHI without passing cached references as evidence, while environments with PyPhi installed must produce positive tractable sub-graph Phi values; the k=12 numerical Phi target remains Open Problem O.28.",
    },
    "protocol_mass_corrections.py": {
        "json": "protocol_mass_corrections_results.json",
        "check": lambda d: d.get("pass") is False and d.get("verdict") == "R1_MUON_DEGENERACY_OR_TAU_SCREENING_NOT_REPRODUCED",
        "rationale": "Hard-coded/tautological PASS retired. The R=1 Hessian check now applies the stated criteria (4..6 modes near phi^11; Re chi(phi^17) < 0) instead of a literal muon pass and the cannot-fail Im chi < 0 test; both fail at R=1 and no R>=2 run is registered (open).",
    },
    "protocol_continuum_validation.py": {
        "json": "protocol_continuum_validation_results.json",
        "check": lambda d: d.get("pass") is False and d.get("verdict") == "R1_PHASON_SPEED_NOT_CONVERGED_TO_PHI_M9",
        "rationale": "Hard-coded/tautological PASS retired. The R=1 run now uses the same 10% tolerance as the full mode instead of 2500%; c_meas misses phi^-9 by about 18x and no R>=10 run is registered (open).",
    },
    "protocol_ncg_spectral_geometry.py": {
        "json": "protocol_ncg_spectral_geometry_results.json",
        "check": lambda d: d.get("pass") is False and str(d.get("verdict", "")).startswith("GAPS_11_17_NOT_SIGNIFICANT"),
        "rationale": "Hard-coded/tautological PASS retired. pass is now spectral_closure_pass (both gaps > 2 sigma) instead of an execution check that could not fail; the gaps sit at about 0.69 and 0.23 sigma (open).",
    },
    "protocol_sdss_l6.py": {
        "json": "protocol_sdss_l6_results.json",
        "check": lambda d: d.get("pass") is False and d.get("verdict") == "NO_GCT_TEST_TEMPLATE_ONLY_PHYSICAL_TRANSFER_OPEN",
        "rationale": "Hard-coded/tautological PASS retired. The literal pass is removed: no amplitude is predicted (predicted_c6_c0 is null) and no data are compared; this is a template design only (open).",
    },
    "protocol_ledger_closeout.py": {
        "json": "protocol_ledger_closeout_results.json",
        "check": lambda d: d.get("pass") is False and d.get("verdict") == "BOOKKEEPING_ONLY_STATUS_DECLARATIONS_NO_COMPUTATION",
        "rationale": "Hard-coded/tautological PASS retired. The literal pass is removed: the script records two status declarations (Born rule Tier 3 conditional, HVP Tier 4 under WP2025 tension) and computes nothing (open).",
    },
    "protocol_cft_boundary.py": {
        "json": "protocol_cft_boundary_results.json",
        "check": lambda d: d.get("pass") is False and d.get("verdict") == "FIT_BY_CONSTRUCTION_DIAGNOSTIC_EXTRACTION",
        "rationale": "Hard-coded/tautological PASS retired. The literal pass is removed: C_ico is back-solved from CODATA alpha, so agreement is a fit by construction (open, pending O.19).",
    },
    "protocol_lee_extended.py": {
        "json": "protocol_lee_extended_results.json",
        "check": lambda d: d.get("pass") is False and str(d.get("verdict", "")).startswith("GCT_OUTSIDE_20PPM_WINDOW_LEE_PREMISE_FAILS"),
        "rationale": "Hard-coded/tautological PASS retired. The literal pass is replaced by the premise the p-value needs: GCT mu and tau ratios within 20 ppm with the engine formulas. They sit at about -21 and -51 ppm, so the global p-value does not apply (open).",
    },
    "protocol_spectral_action.py": {
        "json": "spectral_action_results.json",
        "check": lambda d: d.get("pass") is False and d.get("verdict") == "BOOKKEEPING_MOMENTS_ONLY_CCM_IDENTIFICATION_OPEN_O5",
        "rationale": "Hard-coded/tautological PASS retired. The literal pass is removed: the Seeley-DeWitt moment ladder is bookkeeping and the CCM a_2/a_4 identification is Open Problem O.5; only the heat-kernel numerics check is kept as a named field (open).",
    },
    "protocol_isotope_experiment.py": {
        "json": "protocol_isotope_experiment_results.json",
        "check": lambda d: d.get("pass") is False and d.get("verdict") == "NO_GCT_TEST_DESIGN_ONLY_CENTRAL_N_RP_ZERO_O21_PENDING",
        "rationale": "Hard-coded/tautological PASS retired. The former pass was three identities on typed design inputs; this is an experimental design with no data and a zero central effect (n_rp = 0 pending O.21) (conditional).",
    },
    "protocol_subjective_lagrangian.py": {
        "json": "protocol_subjective_lagrangian_results.json",
        "check": lambda d: d.get("pass") is False and d.get("verdict") == "STATE_C_EXCEEDS_1NW_NEURON_BUDGET",
        "rationale": "Hard-coded/tautological PASS retired. The OR-fallback that compared single-spin power with the whole-neuron 1 nW ceiling is removed; State C draws about 3e8 times the ceiling on the n_rp=1 branch (tension).",
    },
    "protocol_chirality_audit.py": {
        "json": "protocol_chirality_audit_results.json",
        "check": lambda d: d.get("pass") is False and d.get("verdict") == "CHIRAL_ZERO_MODE_GENERIC_NOT_FIBONACCI_SPECIFIC",
        "rationale": "Hard-coded/tautological PASS retired. Sign-of-noise L/R labels are replaced by a count of genuine chiral zero modes (|E| < 1e-8, |<C>| > 0.5) against a random-bond control; every control chain gives the same count, so the effect is generic to odd bipartite chains (open).",
    },
    "protocol_ta_hotspot.py": {
        "json": "protocol_ta_hotspot_results.json",
        "check": lambda d: d.get("pass") is False and str(d.get("verdict", "")).startswith("ALIGNMENT_NOT_SIGNIFICANT"),
        "rationale": "Hard-coded/tautological PASS retired. The fitted-azimuth match is now tested against isotropic random directions with the same psi fit; about 64% of random directions also fall within 20 degrees (open).",
    },
    "protocol_hadron_topology.py": {
        "json": "protocol_hadron_topology_results.json",
        "check": lambda d: d.get("pass") is False and str(d.get("verdict", "")).startswith("CKM_S23_EXPONENT_OUTSIDE_0P5PCT_GATE"),
        "rationale": "Check II gates on the verifier's 0.5% CKM band with the PDG 2024 targets from the SSOT. s13 lies inside it (about 76 ppm); s23 misses GCT's own 0.5% gate at about 0.98% (1.05% against the unrounded 0.04183), about 0.6 sigma from PDG, so this is a miss of the registered precision gate, not a clash with data (tension).",
    },
    "protocol_healing_length.py": {
        "json": "protocol_healing_length_results.json",
        "check": lambda d: d.get("pass") is False and d.get("verdict") == "STANDARD_PHYSICS_ARITHMETIC_GCT_ROUTE2_CLOSES_NEGATIVELY_O25",
        "rationale": "Hard-coded/tautological PASS retired. The target 7.25 nm is a_0/alpha itself, so the former PASS compared the formula with its own output; the GCT Route 2 derivation closes negatively (O.25) (open).",
    },
    "protocol_core_cosmology_compat.py": {
        "json": "protocol_core_cosmology_compat_results.json",
        "check": lambda d: d.get("pass") is False and d.get("verdict") == "STANDARD_PHYSICS_ARITHMETIC_NO_GCT_INPUT",
        "rationale": "Hard-coded/tautological PASS retired. log10(t_H/t_P) in (60, 62) uses observed G, hbar and H0 only; no GCT input enters, so the check cannot test GCT (open).",
    },
    "protocol_neutrino_precision.py": {
        "json": "protocol_neutrino_precision_results.json",
        "check": lambda d: d.get("pass") is False and d.get("verdict") == "TENSION_SIGMA_MNU_ABOVE_DESI_DR2_0P0642_EV_LCDM",
        "rationale": "Hard-coded/tautological PASS retired. The gate is the DESI DR2 BAO + CMB LambdaCDM bound (0.0642 eV, arXiv:2503.14738; < 0.16 eV under w0wa) instead of Planck 2018 (0.12 eV); Sigma m_nu = 0.0853 eV exceeds it, and also the Planck+DESI 2024 0.072 eV bound used by verify_neutrino.py (tension).",
    },
    "protocol_anomaly_check.py": {
        "json": "protocol_anomaly_check_results.json",
        "check": lambda d: d.get("pass") is False and d.get("verdict") == "SM_HYPERCHARGE_ANOMALY_IDENTITY_NO_GCT_INPUT" and d.get("identity_holds") is True,
        "rationale": "The charges are the typed Standard Model hypercharges, so anomaly cancellation is a textbook SM identity with no GCT input (open).",
    },
    "protocol_proton_berry_phase.py": {
        "json": "protocol_proton_berry_phase_results.json",
        "check": lambda d: d.get("pass") is False and d.get("verdict") == "SU2_HOLONOMY_IDENTITY_NO_GCT_INPUT_PHI_INV_INPUT" and d.get("identity_holds") is True,
        "rationale": "exp(i*pi*sigma_z) = -I_2 and the (-1)^n parity sweep are SU(2) identities with no GCT input; phi^-1 is an input (open).",
    },
    "protocol_dm_line_forward_model.py": {
        "json": "protocol_dm_line_forward_model_results.json",
        "check": lambda d: d.get("pass") is False and d.get("verdict") == "DESIGN_DISTINGUISHABLE_TYPED_VELOCITIES_NO_DATA" and d.get("design_distinguishable") is True,
        "rationale": "Two Doppler widths from typed velocities (1300 vs 300 km/s) differ by more than 5 eV; a design-feasibility check with no data, like isotope_experiment (conditional).",
    },
    "protocol_fermion_audit.py": {
        "json": "protocol_fermion_audit_results.json",
        "check": lambda d: d.get("pass") is False and d.get("verdict") == "OPEN_INVENTORY_CHECKS_HOLD_BY_CONSTRUCTION" and d.get("checks_consistent") is True,
        "rationale": "The three checks cannot fail. The vertex orbit is 1 because the rotation axis is defined through the vertex, any off-axis point has orbit 3 under an order-3 rotation, and the gauge scan rotates a zero displacement field (delta_E = 0 for any generator). Recorded as consistent; open.",
    },
}


def run_constants_integrity_check():
    """
    Step 0: Validate the SSOT YAML before running any protocols.
    Imports gct_constants from src/ and calls validate().
    Returns True if all constants are well-formed, False otherwise.
    """
    print("\n" + "="*80)
    print("STEP 0: CONSTANTS INTEGRITY CHECK (SSOT Validation)")
    print("="*80)

    # Run gct_utils self-test as a subprocess so PYTHONPATH is correct
    result = subprocess.run(
        [sys.executable, os.path.join(SRC_DIR, "gct_utils.py")],
        capture_output=True, text=True, env=env_base
    )
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)

    passed = result.returncode == 0
    if passed:
        print("  [PASS] SSOT constants are well-formed. Proceeding with protocol suite.\n")
    else:
        print("  [FAIL] SSOT constants validation FAILED. Aborting suite.\n")
    return passed


def run_protocol(filename):
    print(f"\n>>> EXECUTING: {filename}")

    script_path = os.path.join(SRC_DIR, filename)

    if not os.path.exists(script_path):
        print(f"  [ERROR] File not found: {script_path}")
        return False

    start = time.time()
    try:
        env = env_base.copy()
        env["PYTHONUTF8"] = "1"   # Python 3.7+ UTF-8 mode; avoids cp1252 on Windows
        result = subprocess.run(
            [sys.executable, "-X", "utf8", script_path],
            capture_output=True, text=True, encoding="utf-8", errors="replace", env=env
        )
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

        # STRICT CHECK: Must read JSON result from data/ directory
        # Use override filename if present, otherwise derive from script name
        json_filename = JSON_OVERRIDE.get(filename, filename.replace(".py", "_results.json"))
        json_path     = os.path.join(DATA_DIR, json_filename)

        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                data = json.load(f)
                return data.get("pass", False)
        else:
            print(f"  [WARNING] No result JSON found at {json_path}")
            return False

    except Exception as e:
        print(f"  [EXCEPTION] {e}")
        return False


def main():
    print("="*80)
    print("GCT Master Verification Suite")
    print("="*80)

    # -------------------------------------------------------------------------
    # STEP 0: Constants Integrity Check
    # -------------------------------------------------------------------------
    if not run_constants_integrity_check():
        print("\nABORTED: Fix gct_constants.yaml / gct_constants.py before running protocols.")
        sys.exit(2)

    # -------------------------------------------------------------------------
    # 1. Load Claim Registry
    # -------------------------------------------------------------------------
    registry_candidates = [
        os.path.join(CONFIG_DIR, "claim_registry.json"),
        os.path.join(os.path.dirname(SRC_DIR), "claim_registry.json"),
        os.path.join(os.getcwd(), "claim_registry.json"),
        os.path.join(os.getcwd(), "GCT_Physics_Engine", "claim_registry.json"),
        os.path.join(DATA_DIR, "claim_registry.json"),
    ]

    registry_path = None
    for cand in registry_candidates:
        if os.path.exists(cand):
            registry_path = cand
            break

    registry = []
    if registry_path:
        with open(registry_path, 'r') as f:
            registry = json.load(f)
        fine_structure_claim = next(
            (claim for claim in registry if claim.get("claim_id") == "C_FINE_STRUCTURE"),
            None,
        )
        if fine_structure_claim is None:
            raise ValueError("claim_registry.json is missing C_FINE_STRUCTURE")
        validate_fine_structure_claim_contract(fine_structure_claim)
        print(f"Loaded {len(registry)} claims from registry: {registry_path}")
    else:
        print("[WARNING] claim_registry.json not found. Proceeding with protocol-only audit.")

    # -------------------------------------------------------------------------
    # 2. Execute all protocols to refresh data
    # -------------------------------------------------------------------------
    print("\nRefreshing Physics Engine Data...")
    proto_results = {}
    for proto in PROTOCOLS:
        passed = run_protocol(proto)
        proto_results[proto] = passed

    # -------------------------------------------------------------------------
    # 3. Claim Registry Audit
    # -------------------------------------------------------------------------
    print("\n" + "="*80)
    print("CLAIM REGISTRY AUDIT")
    print("="*80)

    claim_audit_results = {"passed": [], "failed": [], "pending": []}

    for claim in registry:
        cid          = claim.get("claim_id", "UNK")
        protocol_json = claim.get("protocol_output_json")

        if claim.get("retired") is True:
            print(f"Checking Claim [{cid}]: RETIRED")
            continue

        print(f"Checking Claim [{cid}]:", end=" ")

        if not protocol_json:
            print("MISSING PROTOCOL JSON FIELD")
            if claim.get("enforce"):
                claim_audit_results["failed"].append(cid)
            else:
                claim_audit_results["pending"].append(cid)
            continue

        json_path    = os.path.join(DATA_DIR, os.path.basename(protocol_json))

        if not os.path.exists(json_path):
            print("MISSING DATA")
            if claim.get("enforce"):
                claim_audit_results["failed"].append(cid)
            else:
                claim_audit_results["pending"].append(cid)
            continue

        with open(json_path, 'r') as f:
            data = json.load(f)

        field_path = claim.get("json_field", "")
        val = data
        for k in field_path.split("."):
            if isinstance(val, dict):
                val = val.get(k)
            else:
                val = None
                break

        target = claim.get("target_value", claim.get("target"))
        tol    = claim.get("tolerance", 1e-9)
        logic  = claim.get("logic", "==")

        if val is None:
            print("FIELD NOT FOUND")
            if claim.get("enforce"):
                claim_audit_results["failed"].append(cid)
            else:
                claim_audit_results["pending"].append(cid)
            continue

        is_match, logic = evaluate_registered_claim_value(val, claim)

        if is_match:
            try:
                print(f"MATCH (val: {float(val):.4f} {logic} target: {float(target):.4f})")
            except:
                print(f"MATCH (val: {val} {logic} target: {target})")
            claim_audit_results["passed"].append(cid)
        else:
            if claim.get("enforce"):
                try:
                    print(f"FAIL (val: {float(val):.4f}, target: {float(target):.4f}, tol: {tol})")
                except:
                    print(f"FAIL (val: {val}, target: {target}, tol: {tol})")
                claim_audit_results["failed"].append(cid)
            else:
                try:
                    print(f"PENDING (val: {float(val):.4f}, target: {float(target):.4f}, tol: {tol})")
                except:
                    print(f"PENDING (val: {val}, target: {target}, tol: {tol})")
                claim_audit_results["pending"].append(cid)

    # -------------------------------------------------------------------------
    # 3.5 Cross-claim consistency assertions
    # -------------------------------------------------------------------------
    print("\n" + "="*80)
    print("CROSS-CLAIM CONSISTENCY AUDIT")
    print("="*80)


    with open(os.path.join(DATA_DIR, "protocol_pta_l6_template_results.json"), 'r') as f:
        pta_l6_data = json.load(f)
        
    with open(os.path.join(DATA_DIR, "protocol_decoherence_audit_results.json"), 'r') as f:
        dec_data = json.load(f)
        T2 = dec_data.get("T2_native_s", 0)
        tau_zeno = dec_data.get("tau_zeno_s", dec_data.get("tau_recomb_s", dec_data.get("tau_recombination_s", dec_data.get("tau_rec_s", 1))))
        tau_eff_bare_us = dec_data.get(
            "tau_eff_bare_us_extrapolated_outside_quadratic_regime",
            dec_data.get("tau_eff_bare_us", 0),
        )
        bare_tau_regime_validity = dec_data.get("bare_tau_regime_validity", "")
        
    with open(os.path.join(DATA_DIR, "protocol_zeno_energy_budget_results.json"), 'r') as f:
        note = json.load(f).get("correction_note", "")
        tau_raw_baseline = "T2" if "FAD" in note or "Trp" in note else "bulk water 1e-13s"
        
    with open(os.path.join(DATA_DIR, "protocol_quark_mismatch_results.json"), 'r') as f:
        # Check for b_quark_coefficient_tier in the data
        b_quark_coefficient_tier = json.load(f).get("b_quark_coefficient_tier", 3)
        
    # Dark Energy dispositions from source registries
    lambda_bio_tier = 3
    for claim in registry:
        if claim.get("claim_id") == "C_DARK_ENERGY_CROSSING":
            lambda_bio_tier = claim.get("tier", 3)

    chi_disposition_text = None
    falsifiability_registry_path = os.path.join(os.path.dirname(SRC_DIR), "falsifiability_registry.json")
    with open(falsifiability_registry_path, "r", encoding="utf-8") as f:
        falsifiability_registry = json.load(f)
    for entry in falsifiability_registry.get("entries", []):
        if entry.get("verifier_name") == "chi_holographic_susceptibility":
            chi_disposition_text = entry.get("disposition_text")
            break

    # Cross-claim consistency assertions
    assert pta_l6_data.get("pass") is True and pta_l6_data.get("pta_bridge", {}).get("nonzero_response_derived") is False, \
        "PTA scalar theorem must retain an exact l=6 invariant while the physical response remains open; see Ch21"

    # Short-time Misra-Sudarshan diagnostic: tau_eff = tau_Z^2 / tau_meas,
    # where tau_Z = hbar/sigma_H. The variance input is quoted as sigma_H/h
    # in cyclic Hz; tau_Z is not 1/(sigma_H/h) and is not the phenomenological T2.
    # The bare radical-pair Misra-Sudarshan extension is BARE_MS_EXTENSION_INSUFFICIENT
    # at canonical biological parameters; 10 ms target coherence is closure-dependent
    # on Open Problem O.23 (chiral phonon-polariton DFS) per App BEB §BEB.2b / §BEB.12.
    assert dec_data["verdict"].startswith("BARE_MS_EXTENSION_INSUFFICIENT"), \
        "Decoherence audit must report BARE_MS_EXTENSION_INSUFFICIENT at canonical inputs (O.23 pending)"

    # Numerical guard against a T_2^2/tau_meas backdoor: the bare Misra-Sudarshan
    # tau_eff = tau_Z^2/tau_meas sits at about 0.0028 us (2.8 ns) for the
    # canonical radical-pair parameters, more than six orders below the 10 ms target.
    # A T_2^2 substitution would instead produce ~1e4 us.
    assert 0.0027 < tau_eff_bare_us < 0.0029, \
        f"Decoherence audit: extrapolated tau_eff_bare must be about 0.0028 us (tau_Z=hbar/sigma_H), got {tau_eff_bare_us} us"

    assert bare_tau_regime_validity == "outside_quadratic_regime", \
        "Decoherence audit must label the canonical 10 ns drive interval as outside the bare quadratic Misra-Sudarshan regime"

    # assert tau_raw_baseline == "T2", \
    #    "Zeno baseline: must be T2 (FAD/Trp radical pair), not bulk water 1e-13s"

    assert b_quark_coefficient_tier == 2, \
        "Bottom quark 5/4: must be Tier 2 (A5 theorem)"

    assert lambda_bio_tier == 3, \
        "lambda_bio: must be Tier 3 (post-hoc fit)"

    assert chi_disposition_text and "chi = pi (c/H_0 ell_P)^2" in chi_disposition_text, \
        "chi: falsifiability disposition_text must be present in falsifiability_registry.json"

    print("All cross-claim consistency assertions verified. ✓")

    # -------------------------------------------------------------------------
    # 4. Final System Status
    # -------------------------------------------------------------------------
    print("\n" + "="*80)
    print("FINAL SYSTEM STATUS")
    print("="*80)

    # The committed manifest is the suite-integrity preregistration. It covers
    # every protocol, including positive, open, conditional, and tension
    # outcomes, and fails closed if the suite membership or result status drifts.
    expected_outcome_report = check_expected_outcomes(PROTOCOLS)

    # Retain the deeper cross-field guards for registered non-PASS outcomes.
    # The manifest is authoritative for the registered status; these checks
    # additionally verify the internal fields that support that status.
    # expected verdict matches actual verdict -> registered PASS; unexpected
    # non-PASS -> DRIFT.
    expected_verdict_matches = {}   # proto -> rationale string
    drift_failures           = {}   # proto -> reason string
    for proto, reasons in expected_outcome_report["failures"].items():
        drift_failures[proto] = "; ".join(reasons)
    for proto, passed in list(proto_results.items()):
        if passed or proto not in EXPECTED_NON_PASS:
            continue
        spec = EXPECTED_NON_PASS[proto]
        json_path = os.path.join(DATA_DIR, spec["json"])
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                d = json.load(f)
        except Exception as e:
            drift_failures[proto] = f"could not read {spec['json']}: {e}"
            continue
        if spec["check"](d):
            expected_verdict_matches[proto] = spec["rationale"]
            proto_results[proto] = True  # remap to PASS (expected verdict verified)
        else:
            drift_failures[proto] = "registered as expected non-pass but actual verdict differs from expected"

    # Any remaining FAIL that is NOT in EXPECTED_NON_PASS is also drift
    # (unexpected non-pass on a protocol whose closure was registered as
    # positive).
    for proto, passed in proto_results.items():
        if not passed and proto not in EXPECTED_NON_PASS:
            drift_failures.setdefault(proto, "unexpected non-pass; not registered in EXPECTED_NON_PASS")

    for proto, passed in proto_results.items():
        if proto in expected_verdict_matches:
            tag = "PASS (expected-verdict match)"
        elif passed:
            tag = "PASS"
        else:
            tag = "FAIL (drift)"
        print(f"Protocol {proto:<35} : {tag}")

    # ── Layered score computation (pre-registration pattern) ─────────────────
    n_total      = expected_outcome_report["total"]
    n_passed     = expected_outcome_report["matched"]
    n_expected_verdict_match = len(expected_verdict_matches)
    n_drift      = len(drift_failures)
    n_enforced_claims_failed = len(claim_audit_results["failed"])
    n_pending    = len(claim_audit_results["pending"])

    print("-" * 80)
    closure = expected_outcome_report["scientific_closure"]
    print(f"Suite Integrity                 : {n_passed}/{n_total} expected results")
    print(
        "Scientific Closure              : "
        f"{closure['confirmed']} confirmed · {closure['open']} open · "
        f"{closure['conditional']} conditional · {closure['tension']} tension"
    )
    print(f"  registered non-PASS deep checks: {n_expected_verdict_match}")
    print(f"Drift Failures (unexpected)     : {n_drift}")
    print(f"Enforced Registry Comparisons Failed: {n_enforced_claims_failed}")
    print(f"Pending Claims (Non-Enforced)   : {n_pending}")
    print(f"Suite Integrity Rate            : {100.0 * n_passed / max(n_total,1):.1f}%")

    if expected_verdict_matches:
        print("\nExpected-verdict matches (registered expected non-PASS verdicts, verified):")
        for proto, rationale in expected_verdict_matches.items():
            print(f"  - {proto}: {rationale}")

    if drift_failures:
        print("\nDRIFT FAILURES (unexpected non-PASS or registered verdict differs):")
        for proto, reason in drift_failures.items():
            print(f"  - {proto}: {reason}")

    if n_enforced_claims_failed > 0 or n_drift > 0:
        if n_enforced_claims_failed > 0:
            print("\nVERDICT: SYSTEM UNSTABLE. ENFORCED REGISTRY COMPARISONS FAILED.")
        else:
            print("\nVERDICT: SYSTEM UNSTABLE. PROTOCOL DRIFT FROM REGISTERED EXPECTED VERDICTS.")
        sys.exit(1)
    else:
        print("\nVERDICT: SUITE INTEGRITY COMPLETE; SEE SCIENTIFIC-CLOSURE BREAKDOWN.")
        sys.exit(0)


if __name__ == "__main__":
    main()
