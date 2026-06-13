# Consciousness Engine Index

This index binds the consciousness-chapter claims to existing engine protocols. It also records which claims remain open-problem targets rather than missing files.

| Manuscript locus | Claim surface | Engine binding |
|---|---|---|
| V1 Ch16 §16.2.2c / §16.4 | Quality Space irrep decomposition and phenomenal-coordinate scaffold | Analytic 21-DOF bookkeeping is carried in the manuscript as a Tier 2 irrep-count claim with Tier 3 modality/color mapping. No current engine PASS verdict is assigned to the full stress-tensor-to-$I_h$ decomposition. Supporting group-theory checks live in the cage/irrep protocols listed below; a source-bound computation such as `src/protocol_quality_space_irreps.py` remains the promotion target. |
| V1 Ch17 §17.1.2 | Tubulin-Trp radical-pair substrate and bound-water fraction | `src/protocol_zeno_energy_budget.py`, `verify_independent/verify_fbound.py`, `src/protocol_o21_beta_tubulin_trp_pdb.py`, `src/protocol_polaron_Ncoh_derivation.py`. |
| V1 Ch17 §17.1.3 / App H O.23 | Chiral phonon-polariton protected subspace and DFS lifetime scaling | `src/protocol_decoherence_audit.py`, `src/protocol_o23_dfs_collective_dressing.py`, `src/protocol_o23_lindblad_explicit.py`, `src/protocol_eta_zeno.py`. |
| V1 Ch17 §17.5.1 | Graph-theoretic necessary-condition witness for IIT-style integration on the Identity Polaron | `src/protocol_iit_phi.py` (min-cut, balanced cut, spectral gap). |
| V1 Ch17 §17.5 | Canonical IIT 3.0 Phi on tractable induced sub-graphs | `src/protocol_iit_phi_pyphi.py` for k=2..5 sub-graphs; full k=12 remains Open Problem O.28. |
| V1 Ch16 §16.4 / App H O.29 | Stoddard/avian color-dimensionality challenge and sensor-vs-substrate decomposition | `src/protocol_psychophysics_color_dim.py` ingests the Stoddard 2020 hummingbird color table, verifies 4-cone sensor catches compress to the 3-D avian tetrahedral chromaticity simplex after intensity normalization, and tests whether categorical nonspectral/axis labels add explanatory power beyond receptor-space distance in a binomial choice model. Engine status: `COMPATIBLE_O29_STODDARD_MODEL_COMPARISON`; this is behavioral compatibility only, not a 4D-vs-3D perceptual-manifold adjudication. Anatomical compression locus remains empirical. |
| V3 Ch13 Protocol A-Prime | NV-centre chiral surrogate, Anti-Zeno feature, and LGI coherence gate | `src/protocol_zeno_energy_budget.py`, `src/protocol_decoherence_audit.py`, `src/protocol_o12_nu_zeno_renormalization.py`, `src/protocol_preregistration.py`, `falsifiability_registry.json` rows P.8/P.8c/P.44. |

## Open Engine Binding

**O.29 binding:** `protocol_psychophysics_color_dim.py` is the executable Stoddard 2020 color-dimensionality model comparison. It binds the behavioral branch of the sensor-vs-substrate distinction while leaving the avian anatomical compression locus empirical.

Psychophysics-facing claims are split across IIT/Phi, Quality Space, O.23 protected-subspace, and the O.29 sensor-vs-substrate model-comparison surface implemented by the protocol.
