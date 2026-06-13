# Appendix Q: The GCT Physics Engine

This appendix documents the **Geometric Consciousness Theory (GCT) Computational Verification Suite**. All source scripts reside in `GCT_Physics_Engine/src/` within the repository root. For computational verification (Law 1), readers are directed to the canonical source files at that path; the code is not reproduced inline here to avoid divergence between the appendix text and the source directory.

**Parity Status:** Synchronized with Repository at `GCT_Physics_Engine/src/`

> [!NOTE]
> **Analytical Limit Evaluation [Tier 3 Epistemic State]:**
> The computational verification suite operates in the analytical limit, employing registered analytical approximations (e.g., the ~21 ppm muon residual after the disclosed Tier 3 $+5\alpha$ pole-mass normalization and single-loop correction) as stand-ins for the underlying 6D spectral geometry. The complete non-perturbative lattice diagonalization (App Z) represents the full computational closure, which is deferred to future work pending advanced numerical methods. The present formulas are exact within their stated analytical approximations, not theorem-grade closures of every physical normalization.

---

## Q.1 Master Scripts

| File | Purpose |
|:---|:---|
| `GCT_Physics_Engine/verify_independent/run_all.py` | Master verification harness. Runs all independent verifier scripts (`verify_*.py`) under the CODATA-2022 anchor and emits per-script JSON + an aggregate scorecard at `verify_independent/results/scorecard.json`. |
| `GCT_Physics_Engine/config/falsification_thresholds.json` | Numerical-prediction tolerance registry for the LOCKED gauge+lepton subset consumed by the basic verifier wrappers (`verdict_rule` + `tolerance_ppm` format, ~30 predictions). Renamed from `falsification_registry.json` to disambiguate from the root-level `falsifiability_registry.json` (App FM matrix source) — the two files have distinct schemas and consumers. |
| `GCT_Physics_Engine/falsifiability_registry.json` | Full canonical falsifiability matrix — covering all ~60 manuscript predictions including PENDING, TENSION, MARGINAL, and Open Problem dispositions across cosmology, biophysics, and dark sector. Consumed by `build_falsifiability_matrix.py`. |
| `GCT_Physics_Engine/config/claim_registry.json` | Structured registry of all quantitative claims. |

### Q.1.1 Output directory convention

The engine writes results to three sibling directories under `GCT_Physics_Engine/`, each with a distinct role:

| Directory | Role | Written by |
|:---|:---|:---|
| `data/` | Per-protocol JSON results from the core `protocol_*.py` suite (the canonical engine outputs cross-referenced from App R / App H). Default write path for `gct_utils.get_output_path()` with a `.json` extension. | All `src/protocol_*.py` files that use the `gct_utils` output helper. |
| `outputs/` | Per-protocol JSON results from the H-series / Y-series / W-series / O-series protocols (newer additions tied to the App H Open Problem closures). Default write path for protocols that explicitly construct `Path(__file__).parent.parent / "outputs"`. | The H.1/H.2/H.4, Y.6, W.4, O.6/O.14/O.15/O.18/O.20/O.21/O.22 closure protocols. |
| `output/` | Figure PNG outputs and LaTeX-compiled PDFs from the build pipeline. | `build_scripts/compile_latex.py`, figure-rendering protocols, `generate_detailed_figures.py`. |
| `verify_independent/results/` | Per-verifier JSON results from the independent CODATA-anchored verifier harness. Distinct from `data/` because the verifiers re-derive from CODATA-2022 without importing the engine's `gct_constants.yaml`. | `verify_independent/verify_*.py` scripts via `verify_independent/report.py::write_result`. |

A fresh reader running an individual protocol via `python GCT_Physics_Engine/src/protocol_<name>.py` will find its JSON output in either `data/` or `outputs/` depending on the protocol generation; the App R / App H cross-references identify the canonical output path for each cited number.

---

## Q.2 Core Engine Libraries (`gct_*.py`)

These files constitute the fundamental mathematical and geometric objects of the GCT framework.

| File | Purpose | Key Functions |
|:---|:---|:---|
| `gct_algebra_consistency.py` | Verifies algebraic identities and Lie algebra relations for the GCT gauge sector. | `verify_algebra_closure` |
| `gct_alpha.py` | Derives the bare fine-structure constant from 600-cell geometry. Key formula: `alpha_bare^-1 = 360 * phi^-2`. | `compute_alpha_bare` |
| `gct_chirality.py` | Checks chiral anomaly cancellation conditions for the quasicrystalline fermion spectrum. | `check_anomaly_cancellation` |
| `gct_continuum.py` | Validates the continuum limit of the discrete lattice action. | `validate_continuum_limit` |
| `gct_defects.py` | Computes topological defect properties (kinks, vortices) in the phason field. | `compute_defect_energy` |
| `gct_gauge.py` | Derives gauge group structure from icosahedral symmetry via Berry connections. | `derive_gauge_groups` |
| `gct_geometry.py` | Implements the Rhombic Triacontahedron via convex hull of 6D hypercube projection. | `RhombicTriacontahedron`, `project_6d_to_3d` |
| `gct_hamiltonian.py` | Constructs the GCT Hamiltonian operator for the N=144 defect cage. | `build_hamiltonian` |
| `gct_lattice.py` | Generates Z^6 integer lattice points filtered by perp-space acceptance window cutoff. | `GCTLattice`, `generate_akn_tiling` |
| `gct_lorentz.py` | Checks Lorentz symmetry emergence from phason stiffness ratio. | `verify_lorentz_invariance` |
| `gct_mass.py` | Computes mass spectrum via Peierls-Nabarro barrier scan. | `compute_peierls_nabarro_barrier`, `compute_mass_spectrum` |
| `gct_mckay_e8.py` | Implements McKay correspondence for E8 root lattice identification. | `mckay_correspondence` |
| `gct_precision_qed.py` | Computes QED corrections to the bare GCT coupling constants. | `compute_qed_corrections` |
| `gct_projections.py` | Implements the cut-and-project scheme from Z^6 to AKN tiling. | `cut_and_project`, `compute_acceptance_window` |
| `gct_quantum_control.py` | Models quantum Zeno effect and phason steering for Protocol A. | `compute_zeno_frequency` |
| `gct_redundancy.py` | Checks for redundant degrees of freedom in the phason field expansion. | `check_redundancy` |
| `gct_representations.py` | Computes icosahedral group (A5/H3) representations and character tables. | `compute_A5_representations` |
| `gct_spectrum.py` | Computes harmonic spectrum and Fuglede–Kadison determinant. The FK routine evaluates $\det_{FK}(D_F) = \exp((1/N)\sum_i \log|\lambda_i|)$ over the non-zero spectrum of the cage adjacency $D_F$ (Lück 2002 Def 3.11), per the V3 Ch10 Mixed-Harmonic Area Law. The down-quark primary `protocol_quark_mismatch.py` row uses $m_d = m_u \phi^{\phi} = 4.716$ MeV as the FK-determinant infinite-volume-limit closed form, postdiction-consistent at $+0.33\%$ inside the registered 11% shell-resonance band. The I_h-closed sequence in `protocol_md_fk_ih_closed_cages.py` gives deep-tail mean $\det_{FK}/\phi^{\phi}=0.9976$ (sample std $0.0253$), with sequence-mean signed error vs PDG $+0.09\%$; rigorous convergence proof remains O.5. The charm-quark gap label at the $N=17$ second-harmonic mode is not yet derived from the cage spectrum; the $m_c$ value uses the heuristic Mixed-Harmonic exponent $\phi^{13+\phi^{-3}}$ pending QLQCD-1L closure (Open Problem O.5; tracked in App TP §TP-B / §TP-F). | `compute_harmonic_spectrum`, `compute_fuglede_kadison_determinant` |
| `gct_stability.py` | Verifies stability of the icosahedral ground state against perturbations. | `check_ground_state_stability` |
| `gct_tau_uniqueness.py` | Checks uniqueness of the tau lepton exponent via representation theory. | `prove_tau_uniqueness` |
| `gct_utils.py` | Shared utilities: GCT constants (φ, α, m_e, etc.), unit conversions, logging. | `Constants`, `GCTConstants` |

---

## Q.3 Experimental Protocols (`protocol_*.py`)

These scripts execute the specific derivations, proofs, and phenomenological checks for GCT parameters.

| File | Purpose |
|:---|:---|
| `protocol_absolute_scale.py` | Derives absolute mass scale from m_e anchor. |
| `protocol_alpha_derivation.py` | Full derivation of α^-1 = 360φ^-2 from 600-cell geometry. |
| `protocol_alpha_1loop.py` | One-loop phason anti-screening correction to bare α. |
| `protocol_anomaly_check.py` | Gauge anomaly cancellation verification. |
| `protocol_aps_index_proof.py` | APS Index Theorem scaffold for exponent 107 on the I_h-closed boundary cage; reports the discrete boundary asymmetry $\eta_{\mathrm{eff}}$ and the bulk integer required to recover $n=107$ (pending O.14c Pontryagin-class closure). |
| `protocol_cage_minimization.py` | N=144 analytic-branch structural posit; full lattice minimization pending O.38. |
| `protocol_cft_boundary.py` | CFT boundary conditions for the AKN quasicrystal. |
| `protocol_chirality_audit.py` | Chirality audit for fermion spectrum. |
| `protocol_ciss_parity_audit.py` | CISS literature-band audit: protein/peptide default band, DNA stress edge, and no tubulin-specific promotion without direct measurement. |
| `protocol_connes_isomorphism.py` | Necessary algebra-dimension check for the Connes spectral-triple correspondence; KO-dimension sign verification and first-order-condition closure remain pending. |
| `protocol_continuum_validation.py` | Continuum limit validation for the lattice action. |
| `protocol_core_cosmology_compat.py` | Core cosmology compatibility checks (ΛCDM comparison). |
| `protocol_dark_energy.py` | Holographic $\rho_\Lambda=(3\Omega_\Lambda/8\pi)\hbar H_0^2/(c\ell_P^2)$ consistency check plus Tier 3 biogenic-channel coupling $\lambda_{\rm bio}\equiv\alpha$. |
| `protocol_de_multichannel.py` | Multi-channel dark-energy **shape-proxy** diagnostic; not a physical multi-fluid density-evolution model or covariance-aware likelihood. |
| `protocol_dark_matter_fracture.py` | Dark matter fracture toy diagnostic (constructive mechanism check, not standalone falsification or evidence). |
| `protocol_decoherence_audit.py` | Decoherence time scale audit for biophysics protocols. |
| `protocol_dixmier_trace_scaling.py` | Gap-label scaling type check for the spectral zeta scaffold; Dixmier trace closure remains pending. |
| `protocol_dm_line_forward_model.py` | Forward model for 3.55 keV dark matter line prediction. |
| `protocol_electroweak.py` | Electroweak unification and Weinberg angle derivation. |
| `protocol_exponent_derivation.py` | Arithmetic check for candidate electron exponent bookkeeping (`n=107`) with O.14 physical-link closure explicitly open; not a derivation of lepton harmonic exponents. |
| `protocol_fermion_audit.py` | Full fermion spectrum audit across all three generations. |
| `protocol_gauge_uniqueness.py` | Numerical control for the SU(3) candidate generated by the RT-icosahedral substrate; theorem-grade Cartan-Killing uniqueness remains App H O.39. |
| `protocol_geometric_rge.py` | Geometric RGE flow from GUT scale to Z-pole. |
| `protocol_global_significance.py` | Global significance calculation. **Canonical headline ~2.6σ** (broad internal look-elsewhere, full $\mathbb{Z}[\phi]$ multi-base sweep in App R §R.9.2 + Firewall §3 Master Statistical Table). Conditional auxiliaries: 3.1σ under the Conservative full-SM-texture window $N \in [4, 50]$, 4.4σ under the framework's depinning-threshold prior $N \in [8, 25]$ — cited only with the conditioning prior named under the Firewall governance discipline. |
| `protocol_hadron_topology.py` | Hadronic topology and baryonic triad geometry. |
| `protocol_healing_length.py` | Verification of polaron healing length ξ as the Tier 1 textbook Bohr-Compton scale plus Tier 3 lumen-scale match. |
| `protocol_higgs_vev.py` | Higgs VEV formula-evaluation check: v = m_μ × 1440 × φ, with OPEN_CONDITIONAL precision status inherited from muon closure and the Tier 3 1440 handle. |
| `protocol_iit_phi.py` | Graph-theoretic necessary-condition witness (min-cut + spectral gap); full IIT Φ via `protocol_iit_phi_pyphi.py` for k=2..5 sub-graphs; k=12 deferred to O.28. |
| `protocol_isotope_experiment.py` | Protocol D H2^16O vs H2^17O LORR endpoint plus ^17O NMR quadrupole polarity gate. |
| `protocol_kie_audit.py` | Protocol D solvent-KIE audit: the registered KIE bound is a Tier 3 literature-prior control, not a direct H2^16O/H2^17O radical-pair verifier. |
| `protocol_binet_identity_arithmetic_check.py` | Binet identity arithmetic check for the assumed electron exponent `n = -107` in `Z[phi]`; not a K-theoretic derivation (O.14 remains open). |
| `protocol_ledger_closeout.py` | Parameter Ledger closure verification (all Tier 2 parameters confirmed). |
| `protocol_lee_extended.py` | Extended Lee model for phason-mediated interactions. |
| `protocol_lepton_coefficients.py` | Phason-channel multiplicity and lepton-coefficient audit: the muon channel count is Tier 2, while the equal-weight $+5\alpha$ pole-mass normalization and the tau ratio-combination rule remain Tier 3 closure targets. |
| `protocol_lepton_spectrum.py` | Full lepton mass spectrum: electron, muon (21 ppm against PDG 2024), tau (51 ppm against PDG 2024). |
| `protocol_lorentz_violation.py` | Lorentz violation bounds from phason dispersion. |
| `protocol_mass_corrections.py` | Higher-order mass corrections from phason self-energy. |
| `protocol_mckay_tier1.py` | McKay correspondence Tier 1 proof. |
| `protocol_mixing_geometry.py` | CKM and PMNS mixing angle geometry. |
| `protocol_ncg_spectral_geometry.py` | Bare finite-$D_F$ spectral-gap diagnostic on the canonical cage; not a completed Connes spectral-triple construction. |
| `protocol_neutrino_precision.py` | Neutrino mass and PMNS angles (Tier 3 Tension: 4.09σ, documented). |
| `protocol_microscopic_consistency_audit.py` | Microscopic consistency audit: c_phonon/c_phason stiffness hierarchy + 144-cell defect-size check against the (c_phonon/c_phason)² = Φ¹⁸ master identity. |
| `protocol_phi_selection.py` | Proof that φ is the unique quasicrystal slope satisfying all constraints. |
| `protocol_preregistration.py` | Pre-registered predictions for experimental falsification. |
| `protocol_proton_berry_phase.py` | Proton mass from baryonic triad Berry phase. |
| `protocol_proton_mass.py` | Proton mass derivation: m_p = m_e · φ^(15 + φ^-1) (~0.015%). |
| `protocol_subjective_lagrangian.py` | Subjective Lagrangian computation across three canonical mental states (state A / B / C ATP budget, Vibrational Stark Effect, Whispering-Gallery Mode resonance, ATP-to-CI-channel coupling κ). |
| `protocol_pta_anisotropy.py` | PTA gravitational wave anisotropy prediction. |
| `protocol_pta_l6_template.py` | PTA L=6 multipole template for phason GW background. |
| `protocol_qed_audit.py` | QED perturbative correction audit. |
| `protocol_quark_mismatch.py` | Quark mass mismatch analysis (irrational exponent formulas). |
| `protocol_rashba_phason.py` | Rashba-type phason spin-orbit coupling. |
| `protocol_sdss_l6.py` | SDSS large-scale structure L=6 icosahedral anisotropy. |
| `protocol_spectral_action.py` | Connes spectral action principle verification. |
| `protocol_stiffness_invariant.py` | Stiffness ratio invariant K_⊥/K_∥ = φ^-18 proof. |
| `protocol_stiffness_ratio.py` | Numerical verification of stiffness ratio. |
| `protocol_su3_complexification.py` | SU(3) complexification from icosahedral color triplets. |
| `protocol_su3_proof_complete.py` | RT 10-axis generator-inventory audit plus $A_2$ root-system candidate identification for the SU(3) sector; theorem-grade uniqueness remains App H O.39. |
| `protocol_ta_hotspot.py` | Telescope Array cosmic ray hotspot icosahedral alignment. |
| `protocol_zeno_energy_budget.py` | Zeno effect energy budget vs. ATP (Protocol A biophysics). |

---

## Q.4 Known Limitations of the Computational Verification Suite

The following items mark the boundaries of the present computational verification (Law 1) and the analytic results that lie beyond it:

1. **Fuglede–Kadison determinant in `gct_spectrum.py`:** the FK determinant routine is evaluated directly from the cage spectrum per Lück (2002) Def 3.11, with finite-size scaling on the enlarged lattice and the I_h-closed orbit-union sequence. The down-quark primary `protocol_quark_mismatch.py` output is $m_d = m_u \phi^{\phi}$, the FK-determinant infinite-volume-limit closed form, postdiction-consistent at $+0.33\%$ and conditional on O.5 for rigorous convergence. The charm-quark gap label at the $N=17$ second-harmonic mode is not yet derived from the spectrum (Open Problem O.5; $m_c$ uses the heuristic Mixed-Harmonic exponent $\phi^{13+\phi^{-3}}$).

2. **Analytical `m_e` formula and `gct_mass.py`:** The manuscript states `m_e = M_P × φ^{-107} × (1-5α)`. The engine derives the mass from a numerical Peierls-Nabarro barrier scan rather than by evaluating the symbolic expression directly. Both approaches are equivalent — the algebraic formula is the analytic closed form of the barrier minimum — and a dedicated symbolic-formula verification function is a natural addition.

3. **`protocol_subjective_lagrangian.py` scope:** The Subjective-Lagrangian protocol computes the per-state ATP budget, the Vibrational Stark Effect, and the ATP-to-CI-channel coupling κ; it does *not* compute psychophysical scaling laws or $T_2$ ($E_\perp$)-irrep color-discrimination metrics. The Chapter 16 §16.4 Quality Space irrep decomposition is an analytic group-theory result (verifiable by hand against the $I_h$ character table) and the §17.5 IIT Φ values are computed in `protocol_iit_phi.py` and `protocol_iit_phi_pyphi.py`. The color-dimensionality audit is bound separately by `protocol_psychophysics_color_dim.py`, which ingests the Stoddard 2020 hummingbird table, verifies 4-cone to 3-D chromaticity compression, and tests whether categorical nonspectral/axis labels add explanatory power beyond receptor-space distance in a binomial choice model.

## Q.5 Engine Verification Controls

Four engine-verification control classes bound what the physics engine does and does not certify. They are non-claim-bearing engineering controls: the claim verdicts above depend on the protocol outputs and registry thresholds, while these controls define the audit surface around those outputs.

**Dimensional-analysis control.** The `gct_constants.yaml` SSOT documents units as commentary fields. The engine's dimensional consistency is therefore a documented contract rather than a runtime-enforced type system. The critical SI / natural / Planck-unit mixing surfaces are cosmology (`protocol_dark_energy.py`, `protocol_imp01_pipeline.py`) and spectral-action code (`protocol_alpha_1loop.py`).

**Physics-validity control.** The verifier harness tests formula evaluation: whether the stated expression computes the registered value to machine precision. Physics-validity claims, such as whether $K_\perp/K_\parallel = \phi^{-18}$ matches Lubensky-Ramaswamy-Toner / Socolar-Lubensky-Steinhardt elasticity expectations or the i-AlPdMn empirical range, are tiered separately in the manuscript text and registry notes.

**Falsifiability-registry cross-check.** The `falsifiability_registry.json` binds manuscript rows to verifier names, falsification bands, experiments, and timeframes. `build_falsifiability_matrix.py` consumes the registry together with `verify_independent/results/scorecard.json`; registry edits therefore propagate to App FM through regeneration rather than hand edits.

**Closed-claim traceability.** The stable traceability surface is the pair `(claim_registry.json, falsifiability_registry.json)` plus the generated protocol JSON. A claim is auditable when its manuscript row, registry entry, verifier script, and JSON output all point to the same formula, tier, threshold, and disposition.

These controls define the engine-verification boundary for the manuscript: formula evaluation, claim-tier disposition, empirical falsification bands, and registry-to-output synchronization remain distinct checks.

---

*For questions regarding the physics engine, run `python GCT_Physics_Engine/verify_independent/run_all.py` from the repository root to execute the full independent-verifier scorecard.*
