# GCT Codebase Structure

is collapsed into a single placeholder line so the published tree shows only publication-relevant artefacts.

```text
Geometric Consciousness Theory
├── .github
│   └── workflows
├── .gitignore
├── CODEBASE_STRUCTURE.md
├── GCT - The Architecture of Reality
│   ├── GCT_ La Arquitectura de la Realidad.md
│   ├── GCT_ La Arquitectura de la Realidad.pdf
│   ├── GCT_ The Architecture of Reality.md
│   └── GCT_ The Architecture of Reality.pdf
├── GCT_Physics_Engine
│   ├── Makefile
│   ├── README.md
│   ├── build_falsifiability_matrix.py
│   ├── config
│   │   ├── claim_registry.json
│   │   ├── falsification_thresholds.json
│   │   └── gct_constants.yaml
│   ├── data
│   │   ├── aps_index_proof_results.json
│   │   ├── fk_scaling.json
│   │   ├── mckay_e8_report.json
│   │   ├── o14d_advanced_invariants_results.json
│   │   ├── o14d_closure_search_results.json
│   │   ├── o14d_irrep_decomp_results.json
│   │   ├── pdb
│   │   │   ├── pdb1jff.ent
│   │   │   └── pdb6dpu.ent
│   │   ├── protocol_absolute_scale_results.json
│   │   ├── protocol_akn_dimension_group_results.json
│   │   ├── protocol_akn_vertex_stars_results.json
│   │   ├── protocol_alpha_1loop_results.json
│   │   ├── protocol_alpha_derivation_results.json
│   │   ├── protocol_alpha_residual_decomposition_results.json
│   │   ├── protocol_anomaly_check_results.json
│   │   ├── protocol_aps_cage_search_results.json
│   │   ├── protocol_aps_candidates_final_results.json
│   │   ├── protocol_aps_index_proof_results.json
│   │   ├── protocol_bellissard_gap_labels_results.json
│   │   ├── protocol_cage_blast_radius_results.json
│   │   ├── protocol_cage_discovery_results.json
│   │   ├── protocol_cage_minimization_results.json
│   │   ├── protocol_cage_orbit_structure_results.json
│   │   ├── protocol_cage_repair_results.json
│   │   ├── protocol_cage_spectral_decomp_results.json
│   │   ├── protocol_cft_boundary_results.json
│   │   ├── protocol_ch06_maxwell_emergence_results.json
│   │   ├── protocol_chirality_audit_results.json
│   │   ├── protocol_connes_isomorphism_results.json
│   │   ├── protocol_continuum_validation_results.json
│   │   ├── protocol_core_cosmology_compat_results.json
│   │   ├── protocol_d_mc_systematics_results.json
│   │   ├── protocol_dark_energy_results.json
│   │   ├── protocol_dark_matter_fracture_results.json
│   │   ├── protocol_de_multichannel_results.json
│   │   ├── protocol_decoherence_audit_results.json
│   │   ├── protocol_dixmier_trace_scaling_results.json
│   │   ├── protocol_dm_line_forward_model_results.json
│   │   ├── protocol_electroweak_results.json
│   │   ├── protocol_eta_continuum_results.json
│   │   ├── protocol_eta_zeno_results.json
│   │   ├── protocol_euler_char_audit_results.json
│   │   ├── protocol_exponent_derivation_results.json
│   │   ├── protocol_fbio_kk_reduction_results.json
│   │   ├── protocol_fermion_audit_results.json
│   │   ├── protocol_fuglede_kadison_me_results.json
│   │   ├── protocol_gauge_uniqueness_results.json
│   │   ├── protocol_geometric_rge_results.json
│   │   ├── protocol_global_significance_results.json
│   │   ├── protocol_hadron_topology_results.json
│   │   ├── protocol_healing_length_results.json
│   │   ├── protocol_higgs_vev_results.json
│   │   ├── protocol_iit_phi_pyphi_results.json
│   │   ├── protocol_iit_phi_results.json
│   │   ├── protocol_imp01_pipeline_results.json
│   │   ├── protocol_isotope_experiment_results.json
│   │   ├── protocol_jarlskog_formula_search_results.json
│   │   ├── protocol_k_theory_mass_results.json
│   │   ├── protocol_ledger_closeout_results.json
│   │   ├── protocol_lee_extended_results.json
│   │   ├── protocol_lepton_coefficients_results.json
│   │   ├── protocol_lepton_spectrum_results.json
│   │   ├── protocol_lorentz_violation_results.json
│   │   ├── protocol_mass_corrections_results.json
│   │   ├── protocol_mckay_tier1_results.json
│   │   ├── protocol_mckay_tier1_summary.json
│   │   ├── protocol_microscopic_consistency_audit_results.json
│   │   ├── protocol_mixing_geometry_results.json
│   │   ├── protocol_n132_investigation_results.json
│   │   ├── protocol_n132_nullspace_results.json
│   │   ├── protocol_ncg_spectral_geometry_results.json
│   │   ├── protocol_neutrino_precision_results.json
│   │   ├── protocol_o12_nu_zeno_renormalization_results.json
│   │   ├── protocol_o13_closure_class2_strict_results.json
│   │   ├── protocol_o13_intra_class2_dynamics_results.json
│   │   ├── protocol_o14_coxeter_exponent_squares_results.json
│   │   ├── protocol_o14_n107_combinatorial_enum_results.json
│   │   ├── protocol_o15_phason_stiffness_chemical_correction_results.json
│   │   ├── protocol_o15a_h3_invariant_degrees_results.json
│   │   ├── protocol_o16_n_coh_verification_results.json
│   │   ├── protocol_o17_delta_h_local_results.json
│   │   ├── protocol_o17p_isw_amplitude_results.json
│   │   ├── protocol_o18_trefoil_meridian_trace_results.json
│   │   ├── protocol_o19_phason_alpha_magnitude_results.json
│   │   ├── protocol_o1_o4_v_lock_structural_results.json
│   │   ├── protocol_o20_icosahedral_1440_factorisations_results.json
│   │   ├── protocol_o21_beta_tubulin_trp_pdb_results.json
│   │   ├── protocol_o22_newton_g_dimensional_full_results.json
│   │   ├── protocol_o22_newton_g_dimensional_results.json
│   │   ├── protocol_o23_dfs_collective_dressing_results.json
│   │   ├── protocol_o23_lindblad_explicit_results.json
│   │   ├── protocol_o6_dscft_hartle_hawking_results.json
│   │   ├── protocol_o6_dscft_operator_matching_results.json
│   │   ├── protocol_o7_jarlskog_phi22_results.json
│   │   ├── protocol_orbit_union_search_results.json
│   │   ├── protocol_p_evolve_first_principles_results.json
│   │   ├── protocol_p_evolve_stage_hierarchy_results.json
│   │   ├── protocol_phason_berry_curvature_results.json
│   │   ├── protocol_phason_oneloop_AKN_results.json
│   │   ├── protocol_phi_selection_results.json
│   │   ├── protocol_polaron_Ncoh_derivation_results.json
│   │   ├── protocol_preregistration_results.json
│   │   ├── protocol_proton_berry_phase_results.json
│   │   ├── protocol_proton_mass_results.json
│   │   ├── protocol_pta_anisotropy_results.json
│   │   ├── protocol_pta_l6_results.json
│   │   ├── protocol_pta_l6_template_results.json
│   │   ├── protocol_qed_audit_results.json
│   │   ├── protocol_quark_mismatch_results.json
│   │   ├── protocol_rashba_phason_results.json
│   │   ├── protocol_rge_native_results.json
│   │   ├── protocol_rt_eta_invariant_results.json
│   │   ├── protocol_sdss_l6_results.json
│   │   ├── protocol_stiffness_invariant_results.json
│   │   ├── protocol_stiffness_ratio_results.json
│   │   ├── protocol_su3_complexification_results.json
│   │   ├── protocol_su3_proof_complete_results.json
│   │   ├── protocol_subjective_lagrangian_results.json
│   │   ├── protocol_ta_hotspot_results.json
│   │   ├── protocol_tau_uniqueness_results.json
│   │   ├── protocol_uniqueness_criterion_results.json
│   │   ├── protocol_uniqueness_final_push_results.json
│   │   ├── protocol_uniqueness_sophisticated_results.json
│   │   ├── protocol_wavefunction_overlap_results.json
│   │   ├── protocol_weinberg_uniqueness_results.json
│   │   ├── protocol_zeno_energy_budget_results.json
│   │   ├── pta_preregistration_package.json
│   │   ├── spectral_action_results.json
│   │   └── spectral_rge_kernel.json
│   ├── falsifiability_registry.json
│   ├── outputs
│   │   ├── h1_1_consensus_convergence.json
│   │   ├── h1_1b_krein_rutman_profinite.json
│   │   ├── h2_1_phason_dressing.json
│   │   ├── h2_3_neutrino_phi36_lattice.json
│   │   ├── h4_1_topological_limit.json
│   │   ├── h4_2_initial_address.json
│   │   ├── h4_3_branch_switching.json
│   │   ├── h4_4_integration_window.json
│   │   ├── h4_5_iit_phi_phase_transition.json
│   │   ├── o14_coxeter_exponent_squares.json
│   │   ├── o15a_rg_flow_argument.json
│   │   ├── w4_h3_bilinear_coupling_ban.json
│   │   └── y6_3b_polaron_unity_general_prime.json
│   ├── pyphi.log
│   ├── pyproject.toml
│   ├── reproduce_standard_model.py
│   ├── requirements.txt
│   ├── scripts
│   │   └── check_phi_ssot.py
│   ├── src
│   │   ├── cage_builder.py
│   │   ├── gct_algebra_consistency.py
│   │   ├── gct_alpha.py
│   │   ├── gct_chirality.py
│   │   ├── gct_continuum.py
│   │   ├── gct_defects.py
│   │   ├── gct_gauge.py
│   │   ├── gct_geometry.py
│   │   ├── gct_hamiltonian.py
│   │   ├── gct_lattice.py
│   │   ├── gct_lorentz.py
│   │   ├── gct_mass.py
│   │   ├── gct_mckay_e8.py
│   │   ├── gct_precision_qed.py
│   │   ├── gct_projections.py
│   │   ├── gct_quantum_control.py
│   │   ├── gct_redundancy.py
│   │   ├── gct_representations.py
│   │   ├── gct_spectrum.py
│   │   ├── gct_stability.py
│   │   ├── gct_tau_uniqueness.py
│   │   ├── gct_utils.py
│   │   ├── o14d_advanced_invariants.py
│   │   ├── o14d_closure_search.py
│   │   ├── o14d_irrep_decomp.py
│   │   ├── protocol_absolute_scale.py
│   │   ├── protocol_akn_dimension_group.py
│   │   ├── protocol_akn_vertex_stars.py
│   │   ├── protocol_alpha_1loop.py
│   │   ├── protocol_alpha_derivation.py
│   │   ├── protocol_alpha_residual_decomposition.py
│   │   ├── protocol_anomaly_check.py
│   │   ├── protocol_aps_cage_search.py
│   │   ├── protocol_aps_candidates_final.py
│   │   ├── protocol_aps_index_proof.py
│   │   ├── protocol_bellissard_gap_labels.py
│   │   ├── protocol_cage_blast_radius.py
│   │   ├── protocol_cage_minimization.py
│   │   ├── protocol_cage_orbit_structure.py
│   │   ├── protocol_cage_repair.py
│   │   ├── protocol_cage_spectral_decomp.py
│   │   ├── protocol_cft_boundary.py
│   │   ├── protocol_ch06_maxwell_emergence.py
│   │   ├── protocol_chirality_audit.py
│   │   ├── protocol_connes_isomorphism.py
│   │   ├── protocol_continuum_validation.py
│   │   ├── protocol_core_cosmology_compat.py
│   │   ├── protocol_d_mc_systematics.py
│   │   ├── protocol_dark_energy.py
│   │   ├── protocol_dark_matter_fracture.py
│   │   ├── protocol_de_multichannel.py
│   │   ├── protocol_decoherence_audit.py
│   │   ├── protocol_dixmier_trace_scaling.py
│   │   ├── protocol_dm_line_forward_model.py
│   │   ├── protocol_electroweak.py
│   │   ├── protocol_eta_continuum.py
│   │   ├── protocol_eta_zeno.py
│   │   ├── protocol_euler_char_audit.py
│   │   ├── protocol_euler_char_audit_extended.py
│   │   ├── protocol_exponent_derivation.py
│   │   ├── protocol_fermion_audit.py
│   │   ├── protocol_gauge_uniqueness.py
│   │   ├── protocol_geometric_rge.py
│   │   ├── protocol_global_significance.py
│   │   ├── protocol_h1_1_consensus_convergence.py
│   │   ├── protocol_h1_1b_krein_rutman_profinite.py
│   │   ├── protocol_h2_1_phason_dressing.py
│   │   ├── protocol_h2_3_neutrino_phi36_lattice.py
│   │   ├── protocol_h4_1_topological_limit.py
│   │   ├── protocol_h4_2_initial_address.py
│   │   ├── protocol_h4_3_branch_switching.py
│   │   ├── protocol_h4_4_integration_window.py
│   │   ├── protocol_h4_5_iit_phi_phase_transition.py
│   │   ├── protocol_hadron_topology.py
│   │   ├── protocol_healing_length.py
│   │   ├── protocol_higgs_vev.py
│   │   ├── protocol_iit_phi.py
│   │   ├── protocol_iit_phi_pyphi.py
│   │   ├── protocol_imp01_pipeline.py
│   │   ├── protocol_isotope_experiment.py
│   │   ├── protocol_jarlskog_formula_search.py
│   │   ├── protocol_k_theory_mass.py
│   │   ├── protocol_ledger_closeout.py
│   │   ├── protocol_lee_extended.py
│   │   ├── protocol_lepton_coefficients.py
│   │   ├── protocol_lepton_spectrum.py
│   │   ├── protocol_lorentz_violation.py
│   │   ├── protocol_mass_corrections.py
│   │   ├── protocol_mckay_tier1.py
│   │   ├── protocol_microscopic_consistency_audit.py
│   │   ├── protocol_mixing_geometry.py
│   │   ├── protocol_n132_investigation.py
│   │   ├── protocol_n132_nullspace.py
│   │   ├── protocol_ncg_spectral_geometry.py
│   │   ├── protocol_neutrino_precision.py
│   │   ├── protocol_o12_nu_zeno_renormalization.py
│   │   ├── protocol_o13_closure_class2_strict.py
│   │   ├── protocol_o13_intra_class2_dynamics.py
│   │   ├── protocol_o14_coxeter_exponent_squares.py
│   │   ├── protocol_o14_n107_combinatorial_enum.py
│   │   ├── protocol_o15_phason_stiffness_chemical_correction.py
│   │   ├── protocol_o15a_h3_invariant_degrees.py
│   │   ├── protocol_o15a_rg_flow_argument.py
│   │   ├── protocol_o16_n_coh_verification.py
│   │   ├── protocol_o17_delta_h_local.py
│   │   ├── protocol_o17p_isw_amplitude.py
│   │   ├── protocol_o18_trefoil_meridian_trace.py
│   │   ├── protocol_o19_phason_alpha_magnitude.py
│   │   ├── protocol_o1_o4_v_lock_structural.py
│   │   ├── protocol_o20_icosahedral_1440_factorisations.py
│   │   ├── protocol_o21_beta_tubulin_trp_pdb.py
│   │   ├── protocol_o22_newton_g_dimensional.py
│   │   ├── protocol_o22_newton_g_dimensional_full.py
│   │   ├── protocol_o23_dfs_collective_dressing.py
│   │   ├── protocol_o23_lindblad_explicit.py
│   │   ├── protocol_o6_dscft_hartle_hawking.py
│   │   ├── protocol_o6_dscft_operator_matching.py
│   │   ├── protocol_o7_jarlskog_phi22.py
│   │   ├── protocol_orbit_union_search.py
│   │   ├── protocol_p_evolve_first_principles.py
│   │   ├── protocol_p_evolve_stage_hierarchy.py
│   │   ├── protocol_phason_berry_curvature.py
│   │   ├── protocol_phason_oneloop_AKN.py
│   │   ├── protocol_phi_selection.py
│   │   ├── protocol_polaron_Ncoh_derivation.py
│   │   ├── protocol_preregistration.py
│   │   ├── protocol_proton_berry_phase.py
│   │   ├── protocol_proton_mass.py
│   │   ├── protocol_pta_anisotropy.py
│   │   ├── protocol_pta_l6_template.py
│   │   ├── protocol_qed_audit.py
│   │   ├── protocol_quark_mismatch.py
│   │   ├── protocol_quark_mismatch_scaling.py
│   │   ├── protocol_rashba_phason.py
│   │   ├── protocol_rge_native.py
│   │   ├── protocol_rt_eta_invariant.py
│   │   ├── protocol_sdss_l6.py
│   │   ├── protocol_spectral_action.py
│   │   ├── protocol_stiffness_invariant.py
│   │   ├── protocol_stiffness_ratio.py
│   │   ├── protocol_su3_complexification.py
│   │   ├── protocol_su3_proof_complete.py
│   │   ├── protocol_subjective_lagrangian.py
│   │   ├── protocol_ta_hotspot.py
│   │   ├── protocol_uniqueness_criterion.py
│   │   ├── protocol_uniqueness_final_push.py
│   │   ├── protocol_uniqueness_sophisticated.py
│   │   ├── protocol_w4_h3_bilinear_coupling_ban.py
│   │   ├── protocol_weinberg_uniqueness.py
│   │   ├── protocol_y6_3b_polaron_unity_general_prime.py
│   │   ├── protocol_zeno_energy_budget.py
│   │   ├── pyphi.log
│   │   └── verify_engine.py
│   └── verify_independent
│       ├── constants.py
│       ├── report.py
│       ├── results
│       │   ├── E_perp_E_para_amplitudes.json
│       │   ├── alpha_inverse.json
│       │   ├── alpha_inverse_bilayer_corrected.json
│       │   ├── alpha_s_inv_bare.json
│       │   ├── anti_zeno_upper_crossover.json
│       │   ├── bottom_quark.json
│       │   ├── cabibbo_angle.json
│       │   ├── cage_node_count_N144.json
│       │   ├── ch20_liv_delay_and_rm_coefficient.json
│       │   ├── charm_quark.json
│       │   ├── chi_holographic_susceptibility.json
│       │   ├── ckm_jarlskog.json
│       │   ├── ckm_s12.json
│       │   ├── ckm_s13.json
│       │   ├── ckm_s23.json
│       │   ├── ckm_unitarity_3x3.json
│       │   ├── dm_line_3p55keV.json
│       │   ├── down_quark.json
│       │   ├── electron_mass.json
│       │   ├── f_bound_NOE_geometric.json
│       │   ├── fbio_jacobian.json
│       │   ├── g2_electron.json
│       │   ├── g2_muon.json
│       │   ├── higgs_mass_bare.json
│       │   ├── higgs_vev.json
│       │   ├── hypercharges_and_anomaly_cancellation.json
│       │   ├── imp01_biogenic_DE_pipeline.json
│       │   ├── muon_mass.json
│       │   ├── neutrino_m1_floor.json
│       │   ├── neutrino_sum.json
│       │   ├── newton_g.json
│       │   ├── nu_zeno_van_Hove.json
│       │   ├── phason_stiffness_ratio.json
│       │   ├── pmns_delta_cp.json
│       │   ├── pmns_theta12.json
│       │   ├── pmns_theta13.json
│       │   ├── pmns_theta23.json
│       │   ├── pmns_unitarity_3x3.json
│       │   ├── polaron_healing_length.json
│       │   ├── proton_mass.json
│       │   ├── pta_l6_linear_legendre.json
│       │   ├── pta_l6_peak_deviation.json
│       │   ├── pta_l6_squared_power_ratio.json
│       │   ├── scorecard.json
│       │   ├── strange_quark.json
│       │   ├── strong_cp_theta_bar.json
│       │   ├── tau_mass.json
│       │   ├── top_quark.json
│       │   ├── up_quark.json
│       │   ├── w_z_phantom_crossing_z028.json
│       │   ├── weinberg_bare.json
│       │   ├── weinberg_gut.json
│       │   └── yield_strain_epsilon_y.json
│       ├── run_all.py
│       ├── self_consistency
│       │   └── check_imp01_pipeline.py
│       ├── verify_E_amplitudes.py
│       ├── verify_alpha.py
│       ├── verify_alpha_bilayer.py
│       ├── verify_alpha_s_bare.py
│       ├── verify_anti_zeno_upper_crossover.py
│       ├── verify_cabibbo.py
│       ├── verify_ch20_liv_and_rm.py
│       ├── verify_chi_holographic.py
│       ├── verify_ckm.py
│       ├── verify_dm_line.py
│       ├── verify_electron_mass.py
│       ├── verify_epsilon_y.py
│       ├── verify_fbio_jacobian.py
│       ├── verify_fbound.py
│       ├── verify_g2_electron.py
│       ├── verify_g2_muon.py
│       ├── verify_healing_length.py
│       ├── verify_higgs_mass.py
│       ├── verify_higgs_vev.py
│       ├── verify_hypercharges.py
│       ├── verify_jarlskog.py
│       ├── verify_mixing_unitarity.py
│       ├── verify_muon_mass.py
│       ├── verify_n144.py
│       ├── verify_neutrino.py
│       ├── verify_newton_g.py
│       ├── verify_nu_zeno.py
│       ├── verify_phantom_crossing.py
│       ├── verify_pmns.py
│       ├── verify_proton_mass.py
│       ├── verify_pta_l6_anisotropy.py
│       ├── verify_quarks.py
│       ├── verify_stiffness_ratio.py
│       ├── verify_strong_cp.py
│       ├── verify_tau_mass.py
│       └── verify_weinberg.py
├── GCT_Physics_Engine_Reference.md
├── GCT_Review_Reference.md
├── GCT_V1_Part1_Review.md
├── GCT_V1_Score_Report.md
├── Geometric_Consciousness_Theory.md
├── LICENSE
├── LICENSE-CONTENT
├── NOTICE.md
├── README.md
├── build_scripts
│   ├── _common.py
│   ├── compile_latex.py
│   ├── compile_manuscript.py
│   ├── export_engine.py
│   ├── generate_index.py
│   ├── manage_figures.py
│   ├── metadata.json
│   └── scan_unicode.py
├── content
│   ├── 00_Global_Frontmatter
│   │   ├── 00_Global_Abstract.md
│   │   ├── 01_Epistemic_Tier_System.md
│   │   ├── 02_Axiom_and_Postulate_Ledger.md
│   │   ├── 03_Parameter_Ledger.md
│   │   └── 04_Prediction_Postdiction_Firewall.md
│   ├── 01_Volume_1_Operating_System
│   │   ├── 00_Frontmatter
│   │   │   ├── 00_Abstract.md
│   │   │   ├── 01_Preface.md
│   │   │   └── 02_Notation.md
│   │   ├── 01_Part_I_Logic_of_Being
│   │   │   ├── Ch01_Staircase_of_Certainty.md
│   │   │   ├── Ch02_Axiomatic_Foundation.md
│   │   │   ├── Ch03_Ontological_Fork.md
│   │   │   ├── Ch04_Discrete_Geometry.md
│   │   │   └── Ch05_Cosmology_of_Zero.md
│   │   ├── 02_Part_II_Identity
│   │   │   ├── Ch06_Tripartite_Ontology.md
│   │   │   └── Ch07_Universal_Tree_Bundle.md
│   │   ├── 03_Part_III_Rendering
│   │   │   ├── Ch08_Simultaneous_Time.md
│   │   │   ├── Ch09_Rendering_Engine.md
│   │   │   ├── Ch10_Russellian_Causation.md
│   │   │   └── Ch11_Consensus_Protocol.md
│   │   ├── 04_Part_IV_Physics_Bridge
│   │   │   ├── Ch12_Fundamental_Constraint.md
│   │   │   ├── Ch13_Geometric_Constants.md
│   │   │   ├── Ch14_Topology_to_Fields.md
│   │   │   └── Ch15_Spin_Statistics.md
│   │   ├── 05_Part_V_Experience
│   │   │   ├── Ch16_Time_and_Qualia.md
│   │   │   └── Ch17_Physical_Substrate.md
│   │   ├── 06_Part_VI_Applications_and_Extensions
│   │   │   ├── 00_Part_VI_Introduction.md
│   │   │   ├── Ch20_Social_Systems.md
│   │   │   ├── Ch21_Aesthetics.md
│   │   │   ├── Ch22_Contemplative_Practice.md
│   │   │   ├── Ch23_Theology.md
│   │   │   ├── Ch24_Strange_Loops.md
│   │   │   └── Ch25_Philosophy_of_Science.md
│   │   └── 99_Backmatter
│   │       ├── 01_Glossary.md
│   │       ├── 02_Notation_Ref.md
│   │       ├── 03_Bibliography.md
│   │       └── 04_Index.md
│   ├── 02_Volume_2_Cosmic_Architecture
│   │   ├── 00_Frontmatter
│   │   │   ├── 00_Abstract.md
│   │   │   ├── 01_Preface.md
│   │   │   └── 02_Notation.md
│   │   ├── 01_Part_I_Crystallography
│   │   │   ├── Ch01_6D_Parent_Lattice.md
│   │   │   ├── Ch02_Projective_Geometry.md
│   │   │   └── Ch03_Supersolid_Transition.md
│   │   ├── 02_Part_II_Light
│   │   │   ├── Ch04_00_Effective_Action_Bridge.md
│   │   │   ├── Ch04_Lattice_Dynamics.md
│   │   │   ├── Ch05_Vacuum_Hydrodynamics.md
│   │   │   ├── Ch06_Electrodynamics_Derivation.md
│   │   │   └── Ch07_Thermodynamics_of_Creation.md
│   │   ├── 03_Part_III_Gravity
│   │   │   ├── Ch08_Acoustic_Metric.md
│   │   │   ├── Ch09_Entropic_Gravity.md
│   │   │   └── Ch10_Singularities_Gravastars.md
│   │   ├── 04_Part_IV_Dark_Sector
│   │   │   ├── Ch11_Dark_Matter_I_Glass.md
│   │   │   ├── Ch12_Dark_Matter_II_Galactic.md
│   │   │   ├── Ch13_Dark_Matter_III_Clusters.md
│   │   │   └── Ch14_Dark_Energy_Lagrangian.md
│   │   └── 99_Backmatter
│   │       ├── 01_Glossary.md
│   │       ├── 02_Notation_Ref.md
│   │       ├── 03_Bibliography.md
│   │       └── 04_Index.md
│   ├── 03_Volume_3_Matter_Spectrum
│   │   ├── 00_Frontmatter
│   │   │   ├── 00_Abstract.md
│   │   │   ├── 01_Preface.md
│   │   │   └── 02_Notation.md
│   │   ├── 01_Part_I_Forces
│   │   │   ├── Ch01_Phase_Sector_U1.md
│   │   │   ├── Ch02_Rotation_Sector_SU2.md
│   │   │   ├── Ch03_Color_Force_SU3.md
│   │   │   ├── Ch04_Electroweak_Unification.md
│   │   │   ├── Ch05_Higgs_Mechanism.md
│   │   │   └── Ch06_Product_Structure.md
│   │   ├── 02_Part_II_Matter
│   │   │   ├── Ch07_Fundamental_Knot_Electron.md
│   │   │   ├── Ch08_Fractal_Resonance_Leptons.md
│   │   │   ├── Ch09_Neutrinos_Ghostly_Resonances.md
│   │   │   └── Ch10_Extended_Spectrum_Quarks.md
│   │   ├── 03_Part_III_Astrophysics
│   │   │   ├── Ch11_355keV_Anomaly.md
│   │   │   └── Ch12_Dynamic_Dark_Energy.md
│   │   ├── 04_Part_IV_Experiments
│   │   │   ├── Ch13_Protocol_A_Zeno_Drive.md
│   │   │   ├── Ch14_Protocol_B_Mass_Spectrum.md
│   │   │   ├── Ch15_Protocol_C_XRISM.md
│   │   │   ├── Ch16_Protocol_D_Isotope.md
│   │   │   ├── Ch17_Protocol_E_Quark_Mismatch.md
│   │   │   ├── Ch18_Protocol_F_Proton_Mass.md
│   │   │   ├── Ch19_Protocol_G_Neutrinos.md
│   │   │   ├── Ch20_Protocol_H_Lattice_Fracture.md
│   │   │   ├── Ch21_Protocol_I_Pulsar_Timing.md
│   │   │   └── Ch22_Conclusion_Roadmap.md
│   │   └── 99_Backmatter
│   │       ├── 01_Glossary.md
│   │       ├── 02_Notation_Ref.md
│   │       ├── 03_Bibliography.md
│   │       └── 04_Index.md
│   ├── 98_Global_Appendices
│   │   ├── App_A_Measure_Theory.md
│   │   ├── App_B_Solenoid_Topology.md
│   │   ├── App_C_Collective_Coordinates.md
│   │   ├── App_D_Born_Rule.md
│   │   ├── App_E_Foundational_Theorems.md
│   │   ├── App_FM_Falsifiability_Matrix.md
│   │   ├── App_F_Nuclear_Spin.md
│   │   ├── App_G_Tier_Classification.md
│   │   ├── App_H_Research_Questions.md
│   │   ├── App_I_Ontology_Block_Universe.md
│   │   ├── App_J_Crystallography.md
│   │   ├── App_K_Phason_Stiffness.md
│   │   ├── App_L_Thermodynamics.md
│   │   ├── App_M_The_Unified_Action.md
│   │   ├── App_NS_Neutrino_Sum_Contingency.md
│   │   ├── App_N_Transparency_Proof.md
│   │   ├── App_O_Math_Foundations.md
│   │   ├── App_P_Quasicrystal_Theory.md
│   │   ├── App_Q_Physics_Engine.md
│   │   ├── App_R2_Independent_Verification.md
│   │   ├── App_R_Precision_Scorecard.md
│   │   ├── App_S_Engine_Reports.md
│   │   ├── App_TP_Tier_Promotion_Roadmap.md
│   │   ├── App_T_Tier_Audit.md
│   │   ├── App_U_Uniqueness_and_Search_Space.md
│   │   ├── App_V_Prediction_Registry.md
│   │   ├── App_W_Selection_NoSignalling_Energy.md
│   │   ├── App_X_Decoherence_and_Energy.md
│   │   ├── App_Y_Polaron_Unity_Proof.md
│   │   ├── App_ZN_Native_RG_Flow.md
│   │   └── App_Z_QLQCD_Algorithm.md
│   ├── 99_Global_Backmatter
│   │   ├── 01_Master_Glossary.md
│   │   ├── 02_Master_Bibliography.md
│   │   ├── 03_Master_Index.md
│   │   ├── 04_Acknowledgments.md
│   │   └── 05_Colophon.md
│   └── Figures
│       ├── GCT_Figures_Catalog_DETAILED.md
│       ├── Volume_1
│       │   ├── Figure V1.1.1.pdf
│       │   ├── Figure V1.1.1.svg
│       │   ├── Figure V1.12.1.png
│       │   ├── Figure V1.4.1.png
│       │   ├── Figure V1.5.1.png
│       │   ├── Figure V1.5.2.png
│       │   ├── Figure V1.7.1.png
│       │   └── Figure V1.8.1.png
│       ├── Volume_2
│       │   ├── Figure V2.1.1.png
│       │   ├── Figure V2.1.2.pdf
│       │   ├── Figure V2.1.2.svg
│       │   ├── Figure V2.12.1.png
│       │   ├── Figure V2.14.1.png
│       │   └── Figure V2.8.1.png
│       └── Volume_3
│           ├── Figure V3.1.1.png
│           ├── Figure V3.1.2.png
│           ├── Figure V3.10.1.png
│           ├── Figure V3.11.1.png
│           ├── Figure V3.13.1.png
│           ├── Figure V3.2.1.png
│           ├── Figure V3.21.1.png
│           ├── Figure V3.22.1.svg
│           ├── Figure V3.4.1.png
│           ├── Figure V3.5.1.png
│           ├── Figure V3.8.1.pdf
│           ├── Figure V3.8.1.png
│           ├── fig_v3_8_1_lepton_spectrum.pdf
│           ├── fig_v3_8_1_lepton_spectrum.png
│           └── figure_v3_8_1.py
├── extract_figures.sh
├── fig_v3_8_1_lepton_spectrum.pdf
├── fig_v3_8_1_lepton_spectrum.png
├── generate_detailed_figures.py
└── pyphi.log
```
