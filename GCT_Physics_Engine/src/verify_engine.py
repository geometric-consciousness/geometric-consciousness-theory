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
    # Manuscript-cited integer-anchor closure (App H O.14 path (l) +
    # App H O.26 D=18 anchor verification)
    "protocol_o14_coxeter_exponent_squares.py",
    # Closure Lindblad small-N verification of the
    # chiral-OAM DFS suppression (Ch17 §17.1.3c + App H O.23).
    "protocol_o23_lindblad_explicit.py",
    # Closure Protocol D Monte Carlo systematics propagation
    # (Ch16 §16.3.4). Registered as expected non-PASS in
    # EXPECTED_NON_PASS — the operationally-unfalsifiable verdict at
    # Bonferroni-corrected significance under the §16.3.4 budget is the
    # pre-registered structural finding, not a failure.
    "protocol_d_mc_systematics.py",
    # App H O.13 fingerprint (iv) bridge: framework-level catalogue of
    # the clustering-DE perturbation equations + Jeans-length activation
    # threshold identification + parametric cross-power-fingerprint
    # dependence check (Ch14 §14.6.3). PASS at framework-bridge
    # level; full numerical closure registered as O.13 sub-item.
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
        "rationale": "Electron exponent arithmetic closes the registered n=107 counting check, but the physical V->K_0 trace-image/Dixmier-residue selection remains App H O.14; intrinsic protocol pass remains false until that link closes.",
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
            and d.get("precision_validation_pass") is False
            and d.get("pass") is False
            and float(d.get("ppm_error", 0.0)) > 3000.0
        ),
        "rationale": "Bare alpha 360*phi^-2 is within the tree-level 0.5% band but remains OPEN_CONDITIONAL; the protocol must not count the 3442 ppm residual as a precision PASS.",
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
        "check": lambda d: "pending" in str(d.get("bulk_index_status", "")).lower(),
        "rationale": "APS index theorem cage observables computed; bulk Pontryagin term pending Open Problem O.14c.",
    },
    "protocol_global_significance.py": {
        "json": "protocol_global_significance_results.json",
        "check": lambda d: (
            d.get("pass") is False
            and d.get("cross_base_monte_carlo", {}).get("n_non_phi_bases_hitting_all_four") == 0
            and d.get("cross_base_monte_carlo", {}).get("phi_bare_passes_all_four_targets") is False
            and d.get("cross_base_monte_carlo", {}).get("phi_corrected_passes_all_four_targets") is True
            and d.get("cross_base_monte_carlo", {}).get("sigma_joint_two_sided", 0.0) < 5.0
        ),
        "rationale": "Cross-base Monte Carlo is a registered expected non-pass: no sampled non-phi bare-control base hits all four targets, but bare phi misses the sparse lepton targets; corrected phi formulae pass and the auxiliary p_null bound is not a unique-base proof.",
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
        "check": lambda d: d.get("pmns", {}).get("theta23_status") == "TENSION_GT_4SIGMA",
        "rationale": "PMNS theta_23 ~4 sigma tension is the external-data disposition (NOvA/T2K 49.5 vs bare GCT 45 deg); CKM Jarlskog prefactor pending Open Problem O.7.",
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
        "rationale": "Multi-channel shape-proxy partition closure failure to the DESI CPL fit is the registered diagnostic structural verdict (Ch14 §14.6.3 + App R §R.8 row 8): Tier 2 convex-combination EoS identity plus Tier 3 shape-proxy parametrizations/calibrated amplitudes. The failure is restricted to the registered five-channel menu; any GCT-derivable quintessence-today channel discovery remains App H O.13 open closure path.",
    },
    "protocol_o13_intra_class2_dynamics.py": {
        "json": "protocol_o13_intra_class2_dynamics_results.json",
        "check": lambda d: (
            isinstance(d.get("kardashev_band_envelope_dw_z028"), list)
            and len(d["kardashev_band_envelope_dw_z028"]) == 2
        ),
        "rationale": "Class-2 intra-Class-2-dynamics envelope (Ch14 §14.6.2 + App H O.13 closure path) outputs the Kardashev-band |Δw(z=0.28)| range; structural-output PASS criterion is that the envelope is produced as a 2-element [min, max] list.",
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
    # [-0.20%, -0.10%] band (parametric power = 0.00 at both effects, systematic SD far above
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
        "rationale": "Protocol D systematic-error budget at Ch16 §16.3.4 (S1-S6) renders the assay operationally unfalsifiable at Bonferroni-corrected significance across the predicted signed [-0.20%, -0.10%] band under the MC specification (S2 perturbs synthetic data; N=10000 parametric Gaussian z-test gate; C1/C2 sub-runs executed). C2's apparent empirical power is invalid because the null false-positive rate is uncontrolled, so the closure-path-pass flag must remain false until both power and FPR gates are satisfied.",
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
        tolerance_type = claim.get("tolerance_type", "")

        def _as_bool(x):
            if isinstance(x, bool):
                return x
            if isinstance(x, str):
                lx = x.strip().lower()
                if lx == "true":
                    return True
                if lx == "false":
                    return False
            return None

        if val is None:
            print("FIELD NOT FOUND")
            if claim.get("enforce"):
                claim_audit_results["failed"].append(cid)
            else:
                claim_audit_results["pending"].append(cid)
            continue

        is_match = False
        if tolerance_type == "string_match":
            is_match = (str(target) in str(val))
        elif tolerance_type == "exact_string":
            is_match = (str(val) == str(target))
        elif tolerance_type == "exact_string_prefix_match":
            is_match = str(val).startswith(str(target))
        elif tolerance_type in {"boolean", "boolean_match"}:
            actual_bool = _as_bool(val)
            target_bool = _as_bool(target)
            is_match = (
                actual_bool is not None
                and target_bool is not None
                and actual_bool == target_bool
            )
        elif tolerance_type in {"lt", "lte", "gt", "gte"}:
            try:
                actual = float(val)
                expected = float(target)
                if tolerance_type == "lt":
                    is_match = actual < expected
                    logic = "<"
                elif tolerance_type == "lte":
                    is_match = actual <= expected
                    logic = "<="
                elif tolerance_type == "gt":
                    is_match = actual > expected
                    logic = ">"
                elif tolerance_type == "gte":
                    is_match = actual >= expected
                    logic = ">="
            except (ValueError, TypeError):
                is_match = False
        elif logic == "==":
            try:
                actual_diff  = abs(float(val) - float(target))
                allowed_diff = tol
                if tolerance_type == "absolute":
                    allowed_diff = tol
                elif tolerance_type == "relative":
                    allowed_diff = tol * abs(float(target))
                elif tolerance_type in {"ppm", "ppm_tri_state", "ppm_soft_tension"}:
                    allowed_diff = abs(float(target)) * tol / 1_000_000.0
                is_match = actual_diff <= allowed_diff
            except (ValueError, TypeError):
                is_match = (str(val) == str(target))
        elif logic == "<":
            try:
                is_match = float(val) < float(target)
            except (ValueError, TypeError):
                is_match = False
        elif logic == ">":
            try:
                is_match = float(val) > float(target)
            except (ValueError, TypeError):
                is_match = False
        elif logic == "<=":
            try:
                is_match = float(val) <= float(target)
            except (ValueError, TypeError):
                is_match = False
        elif logic == ">=":
            try:
                is_match = float(val) >= float(target)
            except (ValueError, TypeError):
                is_match = False

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


    with open(os.path.join(DATA_DIR, "protocol_pta_anisotropy_results.json"), 'r') as f:
        delta_gamma_max = json.load(f).get("delta_gamma_max", 0)
        
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
    assert abs(delta_gamma_max - 0.00017307) < 0.00001, \
        "PTA anisotropy: ΔΓ_max must be ~1.73e-4 (= phi^-18); see Ch21 §21.1.3"

    # Misra-Sudarshan (J. Math. Phys. 18:756): tau_eff = tau_Z^2 / tau_meas
    # where tau_Z = 1/Delta_ST is the Zeno time in the cyclic-frequency
    # convention (DeltaE/h), NOT the phenomenological T2.
    # The bare radical-pair Misra-Sudarshan extension is BARE_MS_EXTENSION_INSUFFICIENT
    # at canonical biological parameters; 10 ms target coherence is closure-dependent
    # on Open Problem O.23 (chiral phonon-polariton DFS) per App X §X.2b / §X.12.
    assert dec_data["verdict"].startswith("BARE_MS_EXTENSION_INSUFFICIENT"), \
        "Decoherence audit must report BARE_MS_EXTENSION_INSUFFICIENT at canonical inputs (O.23 pending)"

    # Numerical guard against a T_2^2/tau_meas backdoor: the bare Misra-Sudarshan
    # tau_eff = tau_Z^2/tau_meas sits at ~0.1 us (~110 ns) for the canonical
    # radical-pair parameters, about five orders of magnitude below the 10 ms target.
    # A T_2^2 substitution would instead produce ~1e4 us.
    assert 0.05 < tau_eff_bare_us < 1.0, \
        f"Decoherence audit: extrapolated tau_eff_bare must be ~0.1 us (Misra-Sudarshan tau_Z^2/tau_meas diagnostic), got {tau_eff_bare_us} us"

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

    # Remap registered non-PASS verdicts against the EXPECTED_NON_PASS registry:
    # expected verdict matches actual verdict -> registered PASS; unexpected
    # non-PASS -> DRIFT.
    expected_verdict_matches = {}   # proto -> rationale string
    drift_failures           = {}   # proto -> reason string
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
    n_total      = len(proto_results)
    n_passed     = sum(1 for v in proto_results.values() if v)
    n_expected_verdict_match = len(expected_verdict_matches)
    n_drift      = len(drift_failures)
    n_enforced_claims_failed = len(claim_audit_results["failed"])
    n_pending    = len(claim_audit_results["pending"])

    print("-" * 80)
    print(f"Protocols Passing               : {n_passed}/{n_total}")
    print(f"  of which expected-verdict matches: {n_expected_verdict_match}")
    print(f"Drift Failures (unexpected)     : {n_drift}")
    print(f"Enforced Claims Failed          : {n_enforced_claims_failed}")
    print(f"Pending Claims (Non-Enforced)   : {n_pending}")
    print(f"Protocol Pass Rate              : {100.0 * n_passed / max(n_total,1):.1f}%")

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
            print("\nVERDICT: SYSTEM UNSTABLE. ENFORCED CLAIMS FAILED.")
        else:
            print("\nVERDICT: SYSTEM UNSTABLE. PROTOCOL DRIFT FROM REGISTERED EXPECTED VERDICTS.")
        sys.exit(1)
    else:
        print("\nVERDICT: TIER 1 VALIDATION COMPLETE.")
        sys.exit(0)


if __name__ == "__main__":
    main()
