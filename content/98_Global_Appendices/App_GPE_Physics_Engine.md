### **Appendix GPE: The GCT Physics Engine**

This appendix documents the **Geometric Consciousness Theory (GCT) Computational Verification Suite**. All source scripts reside in `GCT_Physics_Engine/src/` within the repository root. For computational verification, readers are directed to the canonical source files at that path; the code is not reproduced inline here to avoid divergence between the appendix text and the source directory.

**Parity Status:** The §GPE.2 class and function names are taken from the top-level `def`/`class` names in `GCT_Physics_Engine/src/gct_*.py`. Where this appendix and the source differ, the source files are canonical.

> [!NOTE]
> **Analytical Limit Evaluation [Tier 3 Epistemic State]:**
> The computational verification suite operates in the analytical limit, employing registered analytical approximations (e.g., the ~21 ppm muon residual, which needs both the Tier 3 $+5\alpha$ normalization and the H-EW-conditional second-order $\phi^8\alpha^2$ term; the first-order factor alone leaves about 2429 ppm) as stand-ins for the underlying 6D spectral geometry. The complete non-perturbative lattice diagonalization (App QLA) represents the full computational closure, which is deferred to future work pending advanced numerical methods. The present formulas are exact within their stated analytical approximations, not theorem-grade closures of every physical normalization.

---

## GPE.1 Master Scripts

| File | Purpose |
|:---|:---|
| `GCT_Physics_Engine/verify_independent/run_all.py` | Master verification harness. Runs all independent verifier scripts (`verify_*.py`) under the CODATA-2022 anchor and emits per-script JSON + an aggregate scorecard at `verify_independent/results/scorecard.json`. |
| `GCT_Physics_Engine/config/falsification_thresholds.json` | Numerical-prediction tolerance registry for the pre-committed gauge+lepton subset consumed by the basic verifier wrappers (`verdict_rule` + `tolerance_ppm` format, ~30 predictions). This registry is distinct from the root-level `falsifiability_registry.json` (App FSM matrix source) — the two files have distinct schemas and consumers. |
| `GCT_Physics_Engine/falsifiability_registry.json` | Full canonical falsifiability matrix — covering all registered manuscript predictions and postdictions, including PENDING, TENSION, MARGINAL, and Open Problem dispositions across cosmology, biophysics, and dark sector. Consumed by `build_falsifiability_matrix.py`. |
| `GCT_Physics_Engine/config/claim_registry.json` | Structured registry of all quantitative claims. |

### GPE.1.1 Output directory convention

The engine writes results to three sibling directories under `GCT_Physics_Engine/`, each with a distinct role:

| Directory | Role | Written by |
|:---|:---|:---|
| `data/` | Per-protocol JSON results from the core `protocol_*.py` suite (the canonical engine outputs cross-referenced from App PSC / App ORQ). Default write path for `gct_utils.get_output_path()` with a `.json` extension. | All `src/protocol_*.py` files that use the `gct_utils` output helper. |
| `outputs/` | Per-protocol JSON results from the H-series / Y-series / W-series / O-series protocols (tied to the App ORQ Open Problem programmes). Default write path for protocols that explicitly construct `Path(__file__).parent.parent / "outputs"`. | The H.1/H.2/H.4, Y.6, W.4, O.6/O.14/O.15/O.18/O.20/O.21/O.22 closure protocols. |
| `output/` | Figure PNG outputs and LaTeX-compiled PDFs from the build pipeline. | `build_scripts/compile_latex.py`, figure-rendering protocols, `generate_detailed_figures.py`. |
| `verify_independent/results/` | Per-verifier JSON results from the independent CODATA-anchored verifier harness. Distinct from `data/` because the verifiers re-derive from CODATA-2022 without importing the engine's `gct_constants.yaml`. | `verify_independent/verify_*.py` scripts via `verify_independent/report.py::write_result`. |

A fresh reader running an individual protocol via `python GCT_Physics_Engine/src/protocol_<name>.py` will find its JSON output in either `data/` or `outputs/` depending on the protocol generation; the App PSC / App ORQ cross-references identify the canonical output path for each cited number.

---

## GPE.2 Core Engine Libraries (`gct_*.py`)

These files constitute the fundamental mathematical and geometric objects of the GCT framework.

| File | Purpose | Key classes / functions |
|:---|:---|:---|
| `gct_algebra_consistency.py` | Assigns candidate hypercharges from topological winding weights (Tier 3: Proposal 1.2 and the face-defect quark assignment) and checks the four anomaly-cancellation sums; with Standard Model hypercharges the cancellation is a Standard Model identity. | `ConsistencyChecker` (`derive_hypercharge`, `verify_rh_hypercharges`, `check_anomaly_cancellation`) |
| `gct_alpha.py` | Evaluates the bare tree-level formula $\alpha_{\rm bare}^{-1} = 360\,\phi^{-2}$ (Tier 3 numerical relation; Tier 3 600-cell multiplier; mechanism open — the RT solid-angle construction is withdrawn, V1 §13.2.1–§13.2.2) and reports the 3443 ppm residual to CODATA as the O.19 target. | `AlphaCalculator` (`compute_600cell_factor`, `compute_geometric_impedance`, `compute_alpha`) |
| `gct_chirality.py` | 1D Fibonacci tight-binding model of a Jackiw–Rebbi-type domain-wall zero mode; the zero mode is generic rather than Fibonacci-specific (see `protocol_chirality_audit.py`). | `fibonacci_word`, `ChiralityProver` (`build_hamiltonian`, `solve_1D_model`) |
| `gct_constants.py` | Named module-level facade over the SSOT constants (`gct_constants.yaml`) for protocols whose ledger anchors must be visible to static audits. | `validate` |
| `gct_continuum.py` | Coarse-graining helpers that extract effective elastic moduli and an effective acoustic metric from the lattice response; the acoustic-metric route to $G$ is retired (App DPS §DPS.7). | `ContinuumHomogenizer` (`coarse_grain_stiffness`, `derive_acoustic_metric`) |
| `gct_defects.py` | Lattice-surgery utilities: node removal (vacancies), central holes and cage construction. | `DefectBuilder` (`remove_node`, `create_central_hole`, `build_cage`) |
| `gct_gauge.py` | Builds a finite RT-axis / traceless-matrix commutator-closure control (Tier 1 matrix algebra). Its eight-dimensional output is a candidate algebraic match for the open Tier 3 SU(3) identification, not a Berry eigenbundle, a physical Standard Model field or action, or a uniqueness theorem (O.39). | `GaugeGenerator` (`identify_3fold_axes`, `generate_algebra`) |
| `gct_geometry.py` | Rhombic Triacontahedron acceptance window as the convex hull of the projected 6D unit hypercube. | `RhombicTriacontahedron` (`compute_penetration`) |
| `gct_hamiltonian.py` | Energy and forces for a lattice state: phonon elasticity plus a perpendicular-space locking term, with $K_\perp/K_\parallel=\phi^{-18}$ inserted as the Tier 3 P3b input. | `GCTHamiltonian` (`compute_total_energy`, `compute_forces`) |
| `gct_lattice.py` | $\mathbb Z^6$ lattice patch filtered by a perpendicular-space cutoff, with displacement/velocity state and neighbour lists. | `GCTLattice` (`get_neighbors`) |
| `gct_lorentz.py` | Phonon/phason dispersion relations by Hessian diagonalization. Reading the phason-branch speed as $c=\phi^{-9}$ is the Tier 3 P3b-conditioned identification; at small patch sizes it is not reproduced (`protocol_continuum_validation.py`). | `DispersionAnalyzer` (`project_wavevector`, `analyze_spectrum`) |
| `gct_mass.py` | Peierls–Nabarro barrier scan for a toy defect (a vacancy in a small patch): rigid shift, relaxation, barrier height. It does not compute a particle mass spectrum and does not evaluate $m_e$ (§GPE.4 item 2). | `MassCalculator` (`compute_peierls_nabarro_barrier`) |
| `gct_mckay_e8.py` | Binary icosahedral group $2I$, its character-fusion (McKay) graph against affine $\widetilde E_8$ [Tier 1], and the Elser–Sloane two-shell $E_8\to H_4$ check; it does not identify the root system with the physical parent lattice. | `verify_binary_icosahedral_mckay`, `verify_e8_as_two_h4_shells`, `run_mckay_e8_audit` |
| `gct_precision_qed.py` | Anomalous-moment and Lamb-shift arithmetic. The muon $g-2$ term $(1/5)(\alpha_{A3}/\pi)^3$ uses a Tier 3 equal-weight channel coefficient and the measured A3 $\alpha$ (tension under WP2025); the Lamb-shift lattice correction is negligible. | `compute_anomalous_moment`, `compute_lamb_shift_correction` |
| `gct_projections.py` | Canonical normalized and raw $3\times6$ icosahedral projection matrices and projectors. The raw-frame Gram ratio it reports is frame-dependent (App DPS §DPS.2–§DPS.3). | `get_m_parallel`, `get_m_perp`, `get_projector_parallel`, `get_projector_perp`, `compute_stiffness_ratio`, `verify_properties` |
| `gct_quantum_control.py` | Landauer-bound energy-budget arithmetic for the historical Zeno-feedback scenario of Protocol A (qubits supportable within a neuronal ATP budget at a declared measurement rate). It does not implement phason steering, a Selection clock, or Level II (V1 Ch17 §17.1.3). | `compute_zeno_thermodynamics` |
| `gct_redundancy.py` | Checks invariance of the lattice Hamiltonian under local rotations of the three internal components of $u_\perp$; this is the invariance condition a local gauge symmetry would need, not a derived gauge field. | `GaugeRedundancyVerifier` (`verify_gauge_invariance`, `scan_all_sites`) |
| `gct_representations.py` | Classifies lattice defects into candidate representation labels (vertex defects as singlets, face defects as triplets; open Tier 3 identification) and computes a defect Berry phase. | `RepresentationAnalyzer` (`classify_defect_topology`, `compute_berry_phase`) |
| `gct_spectrum.py` | Eigenmodes of defect cages and the Fuglede–Kadison determinant. The FK routine evaluates $\det_{FK}(D_F) = \exp((1/N)\sum_i \log|\lambda_i|)$ over the non-zero spectrum of the cage adjacency $D_F$ (an ad hoc normalisation by the number of non-zero eigenvalues; Lück's 2002 von-Neumann-trace normalisation gives ≈1.751 on the $R=2$ cage), per the V3 Ch10 Mixed-Harmonic Area Law. The down-quark primary `protocol_quark_mismatch.py` row uses $m_d = m_u \phi^{\phi} = 4.716$ MeV as the FK-determinant infinite-volume-limit closed form, postdiction-consistent at $+0.33\%$ inside the registered 11% shell-resonance band (Tier 4 as evidence: not distinguishable from numerology for strong effects; App PSC §PSC.9.6). The $I_h$-closed sequence in `protocol_md_fk_ih_closed_cages.py` gives deep-tail mean $\det_{FK}/\phi^{\phi}=0.9976$ (sample std $0.0253$), with sequence-mean signed error vs PDG $+0.09\%$; rigorous convergence proof remains O.5. The muon five-fold degeneracy and tau screening sign are not reproduced at small patch size (`protocol_mass_corrections.py`). The charm-quark gap label at the $N=17$ second-harmonic mode is not yet derived from the cage spectrum; the $m_c$ value uses the heuristic Mixed-Harmonic exponent $\phi^{13+\phi^{-3}}$ pending QLQCD-1L closure (Open Problem O.5; tracked in App TPR §TP-B / §TP-F). | `SpectrumAnalyzer` (`compute_defect_spectrum`, `analyze_mode_degeneracy`, `build_144_cage_adjacency_matrix`, `compute_fuglede_kadison_determinant`) |
| `gct_stability.py` | L-BFGS-B relaxation of a lattice configuration and Hessian (dynamical-matrix) spectrum analysis. | `LatticeRelaxer` (`relax_structure`, `compute_hessian`, `analyze_spectrum`) |
| `gct_tau_uniqueness.py` | Records the $D=18$ integer anchor ($H_3$ invariant-degree sum) and the 5-fold factor used in the tau screening coefficient, with the RT-face tangent-bundle count as a 6D consistency check (Tier 2 integer anchor + Tier 3 combination rule; not a uniqueness proof despite the file name). | `run_tau_uniqueness_proof`, `compute_permutation_character_RT`, `decompose_representation` |
| `gct_utils.py` | SSOT interface: dot-accessible constants loaded from `gct_constants.yaml`, A3 resolution, output paths and a small audit reporter. | `C`, `resolve_a3`, `get_output_path`, `GCTReporter` |

---

## GPE.3 Experimental Protocols (`protocol_*.py`)

These scripts execute derivations where the required inputs are closed, plus conditional proofs, finite controls, formula evaluations and phenomenological checks whose physical bridges remain explicitly tiered. A script name containing "derivation" or "proof" does not by itself promote the tier of the claim it evaluates.

| File | Purpose |
|:---|:---|
| `protocol_absolute_scale.py` | Derives absolute mass scale from $m_e$ anchor. |
| `protocol_alpha_derivation.py` | Evaluates the bare formula $\alpha^{-1} = 360\phi^{-2}$ (Tier 3 numerical relation (Tier 3 600-cell multiplier; mechanism open — the RT solid-angle construction is withdrawn, V1 §13.2.1–§13.2.2)) and reports its 0.34% residual to CODATA; a formula evaluation, not a full derivation (O.19/O.5 open). |
| `protocol_alpha_1loop.py` | Inserted one-loop-template direction diagnostic for the bare-$\alpha$ residual on the 30 RT face normals; no native phason gauge action, coupling, sign or magnitude is derived ("phason anti-screening" is a Tier 3 candidate convention). |
| `protocol_anomaly_check.py` | Gauge-anomaly traces for the registered charge assignment; the charges are the Standard Model hypercharges, so cancellation is a Standard Model identity (registered as open). |
| `protocol_aps_index_proof.py` | Finite weighted-adjacency diagnostic for the O.14 APS programme. It reports a scalar sign count and the full discrete-Dirac sign sum, but specifies no qualifying APS boundary operator/domain and evaluates no APS $\eta$-invariant or index. |
| `protocol_cage_minimization.py` | N=144 analytic-branch structural posit; full lattice minimization pending O.38. |
| `protocol_cft_boundary.py` | Back-solved CFT boundary coefficient (a fit by construction; diagnostic extraction, registered open). |
| `protocol_chirality_audit.py` | Chiral zero-mode count on a 1D Fibonacci chain against 200 random-bond controls; the zero mode is generic, not Fibonacci-specific (registered open). |
| `protocol_ciss_parity_audit.py` | CISS literature-band audit: protein/peptide default band, DNA stress edge, and no tubulin-specific promotion without direct measurement. |
| `protocol_connes_isomorphism.py` | Necessary algebra-dimension check for the Connes spectral-triple correspondence; KO-dimension sign verification and first-order-condition closure remain pending. |
| `protocol_continuum_validation.py` | Continuum-limit check of the phason speed against $\phi^{-9}$ at a 10% tolerance; at R=1 the measured speed misses by ~18× (not converged; registered open). |
| `protocol_core_cosmology_compat.py` | Standard large-number arithmetic $t_H/t_P$ with no GCT input (registered open). |
| `protocol_dark_energy.py` | Holographic $\rho_\Lambda=(3\Omega_\Lambda/8\pi)\hbar H_0^2/(c\ell_P^2)$ consistency check plus Tier 3 biogenic-channel coupling $\lambda_{\rm bio}\equiv\alpha$. |
| `protocol_de_multichannel.py` | Multi-channel dark-energy **shape-proxy** diagnostic; not a physical multi-fluid density-evolution model or covariance-aware likelihood. |
| `protocol_dark_matter_fracture.py` | Dark matter fracture toy diagnostic (constructive mechanism check, not standalone falsification or evidence). |
| `protocol_decoherence_audit.py` | Decoherence time scale audit for biophysics protocols. |
| `protocol_dixmier_trace_scaling.py` | Gap-label scaling type check for the spectral zeta scaffold; Dixmier trace closure remains pending. |
| `protocol_dm_line_forward_model.py` | Forward model for the 3.55 keV line width; a design-feasibility comparison of two typed velocity dispersions, with no data (registered as conditional). |
| `protocol_electroweak.py` | Electroweak boundary audit: canonical projector shares, raw-frame ratios, and one-loop runs from the Tier 3 hypothesis H-EW. |
| `protocol_exponent_derivation.py` | Arithmetic check for candidate electron exponent bookkeeping ($n=107$) with O.14 physical-link closure explicitly open; not a derivation of lepton harmonic exponents. |
| `protocol_fermion_audit.py` | Particle-inventory consistency checks for the Tier 3 lepton, quark and gluon candidate readings. The orbit sizes and the gauge scan hold by construction, so the result is registered as open, not confirmed. |
| `protocol_gauge_uniqueness.py` | Numerical control for the SU(3) candidate built on the RT-icosahedral axis set (closure is not specific to the RT window); theorem-grade Cartan-Killing uniqueness remains App ORQ O.39. |
| `protocol_geometric_rge.py` | Target-normalized geometric RGE integrator (implementation check; the endpoint is imposed by construction). |
| `protocol_global_significance.py` | Look-elsewhere and cross-base diagnostics for the lepton exponent pair; no significance figure from it is cited. Earlier global-significance figures for the numerical matches are withdrawn: the cross-base comparison could not, by construction, credit any base other than $\phi$, and the trial counts behind the quoted σ values were asserted rather than enumerated. The preregistered constant control test that compares $\phi$ against other constants under identical formula freedom has reported: v3 is NEGATIVE-FRAGILE (58 of 300 random bases do at least as well as $\phi$ on 21 constants; $p_0 = 0.196$; non-confirmatory). The test "excludes, at power ≥ 0.8, an effect in which φ hits at least 6 of the 8 informative rows through a real effect; weaker effects are not excluded." The $\phi$-formula matches are therefore Tier 4 as evidence (App PSC §PSC.9.6); no global significance is claimed for them, and no individual match is cited as evidence on its own strength. |
| `protocol_hadron_topology.py` | Hadron-sector arithmetic checks. The CKM $s_{23}$ exponent misses GCT's own 0.5% precision gate (0.98%, about 0.6σ from the PDG 2024 value, so a gate miss rather than a clash with data); $s_{13}$ lies within it (76 ppm). Registered tension. |
| `protocol_healing_length.py` | Arithmetic $\xi = a_0/\alpha \approx 7.25$ nm [Tier 1 arithmetic; its identification as the vacuum/polaron healing length is Tier 3]; the GCT phason-stiffness route closes negatively (O.25; registered open). |
| `protocol_higgs_vev.py` | Higgs VEV formula-evaluation check: $v = m_\mu \times 1440 \times \phi$, with OPEN_CONDITIONAL precision status inherited from muon closure and the Tier 3 1440 handle. |
| `protocol_iit_phi.py` | Graph-theoretic necessary-condition witness (min-cut + spectral gap); full IIT Φ via `protocol_iit_phi_pyphi.py` for k=2..5 sub-graphs; k=12 deferred to O.28. |
| `protocol_isotope_experiment.py` | Protocol D H$_2{}^{16}$O vs H$_2{}^{17}$O LORR endpoint plus $^{17}$O NMR quadrupole polarity gate. |
| `protocol_kie_audit.py` | Protocol D solvent-KIE audit: the registered KIE bound is a Tier 3 literature-prior control, not a direct H$_2{}^{16}$O/H$_2{}^{17}$O radical-pair verifier. |
| `protocol_binet_identity_arithmetic_check.py` | Binet identity arithmetic check for the assumed electron exponent $n = -107$ in $\mathbb{Z}[\phi]$; not a K-theoretic derivation (O.14 remains open). |
| `protocol_ledger_closeout.py` | Status declarations for the Parameter Ledger closeout (Born rule Tier 3 conditional, HVP stance); bookkeeping only, no computation (registered open). |
| `protocol_lee_extended.py` | Look-elsewhere estimate for the mass formulae; its premise (μ and τ within 20 ppm) fails for τ at −50.9 ppm (registered open). |
| `protocol_lepton_coefficients.py` | Phason-channel multiplicity and lepton-coefficient audit: the muon channel count (five $A_5$ irreps, trivial included) is a Tier 3 counting convention, while the equal-weight $+5\alpha$ pole-mass normalization and the tau ratio-combination rule remain Tier 3 closure targets. |
| `protocol_lepton_spectrum.py` | Full lepton mass spectrum: electron, muon (21 ppm against PDG 2024), tau (51 ppm against PDG 2024). |
| `protocol_lorentz_violation.py` | Lorentz violation bounds from phason dispersion. |
| `protocol_mass_corrections.py` | Phason self-energy mode checks; at R=1 the claimed 5-fold muon degeneracy and the tau screening sign are not reproduced (registered open). |
| `protocol_mckay_tier1.py` | Checks the binary-icosahedral character-fusion (McKay) correspondence $2I \leftrightarrow \widetilde E_8$ [Tier 1 finite-group mathematics]; it does not identify that root system with the physical parent lattice. |
| `protocol_mixing_geometry.py` | CKM and PMNS mixing angle geometry. |
| `protocol_ncg_spectral_geometry.py` | Bare finite-$D_F$ spectral-gap diagnostic on the canonical cage; not a completed Connes spectral-triple construction. |
| `protocol_neutrino_precision.py` | Neutrino mass sum against the DESI DR2 + CMB bound $\Sigma m_\nu < 0.0642$ eV (95%, ΛCDM; $< 0.16$ eV under $w_0w_a$); $\Sigma m_\nu = 0.0853$ eV, registered tension. PMNS angles: the bare $\theta_{23}=45^\circ$ lies inside the NuFIT 6.0 normal-ordering $3\sigma$ range with and without Super-Kamiokande data; the earlier 4.09σ figure is withdrawn and the octant is unresolved. |
| `protocol_microscopic_consistency_audit.py` | Microscopic consistency audit: $c_{\rm phonon}/c_{\rm phason}$ stiffness hierarchy + 144-cell defect-size check against the relation $(c_{\rm phonon}/c_{\rm phason})^2 = \phi^{18}$, which is the Tier 3 stiffness-map hypothesis P3b, not an identity. |
| `protocol_phi_selection.py` | Finite-height Diophantine-gap scan $J_R$ (bounded lattice radius) comparing candidate slopes. Because the unbounded gap vanishes for every irrational slope, this is a bounded-radius comparison, not a proof that $\phi$ is the unique quasicrystal slope. |
| `protocol_preregistration.py` | Writes the pre-registered experimental thresholds (registration bookkeeping, not a test; registered open). |
| `protocol_proton_berry_phase.py` | SU(2) holonomy identity $U = -I_2$ (Berry phase $\pi$) and the integer-parity sweep $U_n = (-1)^n I_2$; the $\phi^{-1}$ correction and the proton-mass exponent $15 + \phi^{-1}$ are inputs, not computed. |
| `protocol_proton_mass.py` | Proton mass formula (Tier 2 mechanism + Tier 3 sheet/exponent handle): $m_p = m_e \cdot \phi^{15 + \phi^{-1}}$ (~0.015%). |
| `protocol_subjective_lagrangian.py` | Historical Tier 3/4 surrogate arithmetic across three labeled states A / B / C (conditional ATP ledger, Vibrational Stark input arithmetic, Whispering-Gallery Mode scenario, and the Stark/CI energy-scale ratio κ). A pass is arithmetic replay only; no volition, phason, Selection-Operator or Level-II inference follows. |
| `protocol_pta_anisotropy.py` | Compatibility wrapper recording the withdrawn numerical PTA response; physical transfer and amplitude remain open. |
| `protocol_pta_l6_template.py` | Exact oriented rotational-icosahedral scalar invariant; no physical PTA response or amplitude is derived. |
| `protocol_qed_audit.py` | QED perturbative correction audit. |
| `protocol_quark_mismatch.py` | Quark mass mismatch analysis (irrational exponent formulas). |
| `protocol_rashba_phason.py` | A5 character audit of the Rashba-phason coupling (Eq. 17.3 is not an icosahedral scalar for the vector phason; coupling Tier 3/open) and energy-scale arithmetic on declared inputs. |
| `protocol_sdss_l6.py` | SDSS $l=6$ template with no predicted amplitude (no GCT test; physical transfer open). |
| `protocol_spectral_action.py` | Spectral-action moment bookkeeping and heat-kernel numerics; the CCM $a_2/a_4$ identification is open (O.5; registered open). |
| `protocol_stiffness_invariant.py` | Historical coordinate-normalization diagnostic (Gram eigenvalues of the raw projection frames); it does not prove a physical stiffness invariant. The Gram-determinant ratio is frame-dependent (App DPS §DPS.2–§DPS.3). |
| `protocol_stiffness_ratio.py` | Computes the $H_3$ invariant-degree sum $D=18$ from Coxeter data (the Tier 2 integer identification; the part of the check that can fail) and the raw-frame Gram cube, which equals $\phi^{-18}$ only in the unnormalized frame. The stiffness map $K_\perp/K_\parallel = \phi^{-18}$ is the Tier 3 P3b hypothesis (O.15(b)); the protocol does not derive it. |
| `protocol_su3_complexification.py` | Tier 3 candidate SU(3) complexification from proposed icosahedral color triplets (the Hermitian real-form choice is an input, not derived). |
| `protocol_su3_proof_complete.py` | RT 10-axis generator-inventory audit plus $A_2$ root-system candidate identification for the SU(3) sector; theorem-grade uniqueness remains App ORQ O.39. |
| `protocol_ta_hotspot.py` | Telescope Array hotspot alignment with a fitted azimuth; a Monte Carlo over random directions gives p ≈ 0.64 (not significant; registered open). |
| `protocol_zeno_energy_budget.py` | Conditional Tavis-Cummings / ATP energy-budget arithmetic for declared external-rate scenarios (Protocol A material proxy). It does not derive an ATP-to-phason transducer, a Zeno Drive, a Selection Operator, an Identity Polaron, or a Level-II gate. |

---

## GPE.4 Known Limitations of the Computational Verification Suite

The following items mark the boundaries of the present computational verification and the analytic results that lie beyond it:

1. **Fuglede–Kadison determinant in `gct_spectrum.py`:** the FK-type determinant routine is evaluated directly from the cage spectrum with an ad hoc normalisation by the number of non-zero eigenvalues (Lück's 2002 von-Neumann-trace normalisation gives ≈1.751 on the $R=2$ cage), with finite-size scaling on the enlarged lattice and the $I_h$-closed orbit-union sequence. The down-quark primary `protocol_quark_mismatch.py` output is $m_d = m_u \phi^{\phi}$, the FK-determinant infinite-volume-limit closed form, postdiction-consistent at $+0.33\%$ and conditional on O.5 for rigorous convergence. The charm-quark gap label at the $N=17$ second-harmonic mode is not yet derived from the spectrum (Open Problem O.5; $m_c$ uses the heuristic Mixed-Harmonic exponent $\phi^{13+\phi^{-3}}$).

2. **Analytical $m_e$ formula and `gct_mass.py`:** `gct_mass.py` computes a Peierls–Nabarro barrier for a toy defect; it does not evaluate or derive $m_e = M_P\phi^{-107}(1-5\alpha)$. That formula is a Tier 3 anchor-normalised Planck-link check ($m_e$ is the A1 anchor; O.14), evaluated arithmetically by `verify_independent/verify_electron_mass.py`; its 1006 ppm residual misses the pre-committed 1000 ppm rule by 6 ppm, a FAIL of that rule (App FSM P.1c).

3. **`protocol_subjective_lagrangian.py` scope:** The protocol replays supplied state labels, an ATP ledger, Vibrational-Stark arithmetic, and the dimensionless Stark-energy/CI-gap ratio κ. That ratio is not a transition probability, and the protocol supplies no ATP-to-phason transducer, Berry steering, polariton-production result, Selection Operator, or phenomenal inference. It also does *not* compute psychophysical scaling laws or $T_2$ ($E_\perp$)-irrep color-discrimination metrics. The Chapter 16 §16.4 Quality Space irrep decomposition is an analytic group-theory result (verifiable by hand against the $I_h$ character table) and the §17.5 IIT Φ values are computed in `protocol_iit_phi.py` and `protocol_iit_phi_pyphi.py`. The color-dimensionality audit is bound separately by `protocol_psychophysics_color_dim.py`, which ingests the Stoddard 2020 hummingbird table, verifies 4-cone to 3-D chromaticity compression, and tests whether categorical nonspectral/axis labels add explanatory power beyond receptor-space distance in a binomial choice model.

## GPE.5 Engine Verification Controls

Four engine-verification control classes bound what the physics engine does and does not certify. They are non-claim-bearing engineering controls: the claim verdicts above depend on the protocol outputs and registry thresholds, while these controls define the audit surface around those outputs.

**Dimensional-analysis control.** The `gct_constants.yaml` SSOT documents units as commentary fields. The engine's dimensional consistency is therefore a documented contract rather than a runtime-enforced type system. The critical SI / natural / Planck-unit mixing surfaces are cosmology (`protocol_dark_energy.py`, `protocol_imp01_pipeline.py`) and spectral-action code (`protocol_alpha_1loop.py`).

**Physics-validity control.** The verifier harness tests formula evaluation: whether the stated expression computes the registered value to machine precision. Physics-validity claims, such as whether $K_\perp/K_\parallel = \phi^{-18}$ matches Lubensky-Ramaswamy-Toner / Socolar-Lubensky-Steinhardt elasticity expectations or any measured material observable, are tiered separately in the manuscript text and registry notes. In particular, the former i-AlPdMn "chemical-bonding floor" comparison is withdrawn (App DPS §DPS.4b): the output of `protocol_o15_phason_stiffness_chemical_correction.py` is not evidence for P3b or for a material floor, and the script is quarantined as a dimensional-sweep check that reports a failed check and is not evidence.

**Falsifiability-registry cross-check.** The `falsifiability_registry.json` binds manuscript rows to verifier names, falsification bands, experiments, and timeframes. `build_falsifiability_matrix.py` consumes the registry together with `verify_independent/results/scorecard.json`; registry edits therefore propagate to App FSM through regeneration rather than hand edits.

**Closed-claim traceability.** The stable traceability surface is the pair `(claim_registry.json, falsifiability_registry.json)` plus the generated protocol JSON. A claim is auditable when its manuscript row, registry entry, verifier script, and JSON output all point to the same formula, tier, threshold, and disposition.

These controls define the engine-verification boundary for the manuscript: formula evaluation, claim-tier disposition, empirical falsification bands, and registry-to-output synchronization remain distinct checks.

---

*For questions regarding the physics engine, run `python GCT_Physics_Engine/verify_independent/run_all.py` from the repository root to execute the full independent-verifier scorecard.*
