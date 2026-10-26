### **Appendix IVH: Independent Verification Harness**

This appendix documents the parallel verification stack that re-evaluates the numerical claims in **Appendix PSC** from an independent codebase — narrowing the epistemic-circularity gap that would otherwise leave App PSC's precision figures vulnerable to the criticism *"the precision is computed by the same engine that generates the prediction."* It re-evaluates stated formulas; it does not test their geometric derivation or their tiers (§IVH.6), and four engine-dependent scripts are excluded from the independence claim (§IVH.1).

The harness lives at:

```
GCT_Physics_Engine/verify_independent/
|-- constants.py # CODATA 2022 + PDG 2024, hardcoded with citations
|-- report.py # shared reporting + discrepancy flagging
|-- verify_<claim>.py # one per registered claim or consistency check
|-- run_all.py # master scorecard aggregator
`-- results/<claim>.json # per-claim machine-readable output + scorecard.json
```

---

## IVH.1 Purpose and Method

**Purpose.** App PSC's precision figures are produced by `GCT_Physics_Engine/src/`. If a reader doubts the engine, they cannot independently audit App PSC without rebuilding the engine — a circular trust loop. The verification harness removes that numerical loop by re-evaluating each App PSC number from the manuscript-stated formula in a separate codebase that imports nothing from the engine (it does not remove the dependence on the formulas themselves). Four scripts are explicit exceptions and do not carry the independence claim — see the **Independence-scope exceptions** note below.

**Method.** For each row of App PSC §§PSC.1–PSC.6:

1. Read the GCT formula directly from the manuscript prose (App PSC, the relevant chapter, and the formula citation).
2. Re-implement it in `verify_<name>.py` using only the mathematical primitives ($\phi$, $\pi$, $\sqrt{2}$, $\sqrt{5}$) and CODATA 2022 / PDG 2024 empirical anchors hardcoded in `constants.py`.
3. Compute the prediction, compare to the observed value, and emit ppm precision.
4. Compare independent precision against the precision App PSC claims. Flag any discrepancy.
5. Emit a JSON result. `run_all.py` aggregates into a master scorecard.

**What is NOT imported.** The independent scripts never import from `gct_utils.C`, `gct_constants.yaml`, or any module in `GCT_Physics_Engine/src/`. The constants in `verify_independent/constants.py` are sourced directly from CODATA 2022 (May 2024 release) and PDG 2024, with the source noted next to each value.

**Independence and reference-class boundary.** The historical `verify_independent/` directory contains three declared result classes: external `EMPIRICAL_ANCHOR` comparisons, internal `MANUSCRIPT_STATED` arithmetic checks, and `PURE_MATHEMATICAL` identity checks. Only the first class is an empirical re-derivation, and class membership is emitted in every result JSON. Four top-level scripts are explicitly engine-dependent and do not carry the independence claim: `verify_g2_muon.py` imports `gct_utils.C`; `verify_stiffness_ratio.py` imports `gct_projections`; `verify_p13c_nmr_polarity.py` imports `nmr_polarity_power`; and `verify_protocol_d_mc_systematics.py` reads the engine-produced Protocol-D MC artifact. Their rows are **engine-consistency checks**, not independent corroboration. Checks under `verify_independent/self_consistency/` are excluded from the master scorecard. Thus the operative criterion is source and reference provenance, not merely the absence of an import from `src/`.

**Discrepancy-reporting rule.** Where independent re-derivation disagrees with App PSC or with the engine, the harness reports the disagreement. It does NOT modify App PSC or the engine to suppress the disagreement. Discrepancies are listed in §IVH.4.

---

## IVH.2 Independent-Codebase Architecture

### Hardcoded empirical anchors (`constants.py`)

| Quantity | Value | Units | Source |
| :--- | :--- | :--- | :--- |
| $m_e$ | $0.51099895069$ | MeV/$c^2$ | CODATA 2022 |
| $m_e$ | $9.1093837139 \times 10^{-31}$ | kg | CODATA 2022 |
| $m_p$ | $938.27208816$ | MeV/$c^2$ | CODATA 2022 |
| $m_\mu$ | $105.6583755$ | MeV/$c^2$ | PDG 2024 |
| $m_\tau$ | $1776.93$ | MeV/$c^2$ | PDG 2024 |
| $\alpha$ | $7.2973525643 \times 10^{-3}$ | — | CODATA 2022 |
| $\alpha^{-1}$ | $137.035999177$ | — | CODATA 2022 |
| $G$ | $6.67430 \times 10^{-11}$ | m$^3$kg$^{-1}$s$^{-2}$ | CODATA 2022 |
| $c$ | $299\,792\,458$ | m/s | SI exact |
| $\hbar$ | $1.054571817 \times 10^{-34}$ | J·s | CODATA 2022 |
| $v_{EW}$ | $246.21965$ | GeV | PDG 2024 |
| $m_u, m_d, m_s$ | $2.16, 4.70, 93.5$ | MeV/$c^2$ | PDG 2024 (MSbar at 2 GeV) |
| $m_c, m_b, m_t$ | $1.2730 \pm 0.0046,\ 4.183 \pm 0.007,\ 172.57 \pm 0.29$ | GeV/$c^2$ | PDG 2024 ($m_t$: direct-measurement mass, not a pole mass) |
| CKM $s_{12}, s_{23}, s_{13}$ | $0.2250, 0.0418, 0.003732$ | — | PDG 2024 (Wolfenstein/global fit) |
| PMNS $\theta_{12}$ | $33.68^{+0.73}_{-0.70}$° | — | NuFIT 6.0 (normal ordering) |
| PMNS $\theta_{23}$ | $43.3^{+1.0}_{-0.8}$° with SK (3σ 41.3°–49.9°); $48.5^{+0.7}_{-0.9}$° without (3σ 41.0°–50.5°); $\Delta\chi^2(45°) = 2.02 / 4.20$ | — | NuFIT 6.0 (normal ordering; $\Delta\chi^2$ from the published 1-D projections) |
| PMNS $\theta_{13}$ | $8.56 \pm 0.11$° with SK ($8.52 \pm 0.11$° without) | — | NuFIT 6.0 |
| PMNS $\delta_{CP}$ | $212^{+26}_{-41}$° with SK ($177^{+19}_{-20}$° without) | — | NuFIT 6.0 |
| $\Delta m^2_{21}$ | $7.49 \times 10^{-5}$ | eV$^2$ | NuFIT 6.0 |
| $\Delta m^2_{31}$ | $2.513 \times 10^{-3}$ | eV$^2$ | NuFIT 6.0 (with SK) |
| $\sum m_\nu$ DESI DR2 bound (registered comparator) | $0.064$ | eV | DESI DR2 BAO + CMB, ΛCDM (95%) |
| $\sum m_\nu$ earlier bounds (context only) | $0.12$ / $0.072$ | eV | Planck 2018 / Planck + DESI 2024 (95%) |
| $a_e$ | $1.159\,652\,180\,59(13) \times 10^{-3}$ | — | Fan et al. 2023 |
| $\alpha^{-1}$ (Cs / Rb) | $137.035\,999\,046(27)$ / $137.035\,999\,206(11)$ | — | Parker 2018 / Morel 2020 |
| 3.55 keV X-ray line | $3.55 \pm 0.03$ | keV | Bulbul et al. 2014 |

Mathematical primitives: $\phi = (1+\sqrt{5})/2$ computed exactly from `math.sqrt(5)`; $\pi$ from `math.pi`. No GCT-provided constant flows into the independent scripts (the four engine-dependent exceptions of §IVH.1 aside).

### Per-claim formula provenance

Each `verify_<name>.py` script states the formula it re-implements, cites the manuscript section (App PSC row, plus the originating chapter — e.g. Ch08 §8.4 for $m_\mu$), and declares the integer / structural inputs explicitly (e.g. `N_MU = 11`, `N_GEOM = -107`, `SATURATION = 1440`). These structural inputs are taken from the manuscript prose, not from `gct_constants.yaml`.

---

## IVH.3 Per-Claim Verification Status

Run output `run_all.py` (re-runnable; see §IVH.5). Independent ppm = $|\text{pred} - \text{obs}|/\text{obs}$ where the prediction is the harness's re-derivation and `obs` is CODATA 2022 / PDG 2024.

The executable scorecard records three independent fields: `reference_class`,
`band_outcome`, and `derivational_closure`. A row may lie inside its empirical
band while retaining an open derivational bridge; that combination is not a
contradiction and is not collapsed into a single monotone status ladder. The
registered-band ordering applies only within a shared empirical reference class
and shared numeric band.

| Claim | App PSC ppm | Independent ppm | Match | Status |
| :--- | :---: | :---: | :---: | :--- |
| **R.1 Leptons** | | | | |
| Electron mass ($m_e$) | 1006 | 1006.17 | ✓ | **FAIL** of the LOCKED 1000 ppm pre-commitment (missed by 6 ppm; registry P.1c). The later 1500 ppm band is not applied retroactively. |
| Muon mass ($m_\mu$) | 21 | 21.09 | ✓ | **PASS** |
| Tau mass ($m_\tau$) | 51 | 50.85 | ⚠ | **AT-GATE TENSION** |
| **R.2 Couplings** | | | | |
| $\alpha^{-1}$ | 3443 | 3442.64 | ⚠ | **OPEN_CONDITIONAL** (Tier 3 numerical relation; Tier 3 600-cell multiplier; mechanism open — the RT solid-angle construction is withdrawn, V1 §13.2.1–§13.2.2; precision closure pending O.19/O.5) |
| Muon g-2 ($\Delta a_\mu$) | 3.3σ | above WP2025 SM total | ⚠ | **TENSION UNDER WP2025** (Tier 3 fitted/equal-weight $1/5$ coefficient + A3 on top of a geometric mechanism class; no robust confirmation) |
| Raw Galois-frame ratio $\rho_{\rm raw}$ ($\phi^{-2}$) | Tier 1 exact (coordinate arithmetic) | $0.38197$ | ✓ | **TIER1_EXACT** — a coordinate identity, not a physical Weinberg boundary |
| $\sin^2\theta_W$ bare ($\phi^{-3}$; Tier 3 hypothesis H-EW) | 21000 (2.1%) | 20967 | ○ | **OPEN_RESEARCH** — the bare angle is the undecided Tier 3 hypothesis H-EW (P.14 registered as open research). The value lies inside the registered 5% band, but that is a cross-scale numerical alignment, not RGE support or a derivation; the one-loop comparator from this boundary is 40.87% low at $M_Z$ (V3 Ch04 §4.3.3), and the pre-registered gauge-running check from it is FAILED (App GRF §GRF.4.3). The 2.1% alignment is **Tier 4 as evidence** (φ-formula match; App PSC §PSC.9.6). |
| Cabibbo angle | 11058 (1.11%) | 11058 | ✓ | **TENSION** — the residual exceeds the 0.5% CKM precision gate shared with CKM $s_{12}$ (same observable, same formula); it lies inside the 5% (50,000 ppm) P.18 falsification band, so nothing is falsified. Observed angle taken as $\arcsin\lambda$ from the PDG mixing anchor. |
| Newton $G$ | 2273.725 (display 2274) | 2273.725 | ✓ | **FAIL** inherited from the electron row (registry P.16): $G \propto m_e^{-2}$, so the residual is the electron Planck-link residual doubled; the P.1c LOCKED 1000 ppm rule is 2001 ppm on $G$, and both branches (2273.725 ppm; all-CODATA-$\alpha$ 2013.345 ppm) miss it. Not independent evidence (see §IVH.4) |
| Higgs VEV | 179 | 179.15 | ✓ | **OPEN_CONDITIONAL** (residual well inside gate; conditional on the A3 measured-$\alpha$ input and a Tier 3 calibrated handle) |
| **R.3 Hadrons** | | | | |
| Proton ($m_p$) | 155 | 154.93 | ✓ | **OPEN_CONDITIONAL** (residual inside gate; sheet exponent $15+\phi^{-1}$ is a Tier 3 anchor pending AKN-action closure under O.5) |
| Up quark | 2100 (0.21%) | 2142 | ✓ | **PASS** |
| Down quark | 3308 (0.33%) | 3307.77 | ✓ | **PASS** — POSTDICTION-CONSISTENT empirical-band outcome; derivational closure remains conditional on O.5 for the FK-determinant infinite-volume limit (see §IVH.4). |
| Strange quark | 7632 (0.76%) | 7632 | ✓ | **PASS** (the verifier uses `constants.py`; the engine protocol reads `M_S_OBS` from YAML; see §IVH.4) |
| Charm quark | 7503 (0.75%) | 7503 | ✓ | **PASS** (2.1σ below PDG; inside the registered ±3% band) |
| Bottom quark | 11549 (1.15%) | 11549 | ✓ | **FAIL** of the PDG $\pm5\sigma$ rule applied to the top quark: 6.9σ low against $4183\pm7$ MeV. The earlier 4130–4230 MeV window was centred on the measurement and is withdrawn as a test (registry P.23). |
| Top quark | 8706 (0.87%) | 8706 | ✓ | **FAIL** of the written P.24 rule (PDG $\pm5\sigma$, registered since v1.2.0): 5.18σ against PDG 2024 ($172.57\pm0.29$ GeV). The same standard as the electron row applies; the residual is a Tier 3 state-level residual conditional on O.5, and a pole/MS-bar uncertainty model would be a new pre-registered band, not a retroactive rescue. Both paths use the GCT-derived $v=246.1755$ GeV, not the measured electroweak VEV. |
| **R.4 Mixing matrices** | | | | |
| CKM $s_{12}$ | 10900 (1.09%) | 10864.50 | ✓ | **TENSION** (residual exceeds the 0.5% gate) |
| CKM $s_{23}$ | 9800 (0.98%) | 9769 | ✓ | **TENSION** (residual exceeds the 0.5% gate) |
| CKM $s_{13}$ | 76 (0.01%) | 76 | ✓ | **PASS** |
| PMNS $\theta_{12}$ | (−0.85%) | 8452 | ✓ | **PASS** (0.4σ against NuFIT 6.0) |
| PMNS $\theta_{23}$ | inside both 3σ ranges | $\Delta\chi^2(45°)=2.02$ with SK / 4.20 without | ✓ | **OPEN_CONDITIONAL** (octant unresolved; the earlier one-octant 4.09σ Gaussian is withdrawn) |
| PMNS $\theta_{13}$ | (−2.0%) | 19943 | ✓ | **TENSION** (1.5σ against NuFIT 6.0 with SK; 1.2σ without) |
| PMNS $\delta_{CP}$ | (+0.4σ / +2.4σ) | 49492 | ✓ | **OPEN_CONDITIONAL** (phase not independently fixed; +0.4σ against NuFIT 6.0 with SK, +2.4σ without) |
| **R.5 Neutrino** | | | | |
| $m_1$ floor | < KATRIN 0.45 eV (90% CL, 2025) | $0.01531$ eV | ✓ | **OPEN_CONDITIONAL** — the conditional value respects the KATRIN upper bound, but no $m_1$ observation exists (registry P.4b) |
| $\sum m_\nu$ | < 0.064 (DESI DR2 + CMB, ΛCDM) | $0.08530$ eV | partial | **TENSION** vs DESI DR2; the bound lies below the 0.075 eV P.4 gate but is model-dependent (acknowledged in App PSC) |
| **R.6 DM** | | | | |
| 3.55 keV X-ray line (centroid) | 0.04% | 393 ppm | ✓ | **OPEN_CONDITIONAL** — context only: the line is unconfirmed by the blinded width and morphology gates, so centroid agreement is never counted as a PASS |

**Aggregate result.** The canonical scorecard contains 54 claim-result JSON rows emitted by the harness's allowlisted verifier invocation: 7 empirical-anchor PASS rows, 9 internal-arithmetic rows, 8 Tier-1-exact pure-mathematical rows (algebraic identities, including the CKM/PMNS unitarity bookkeeping rows, are not counted as empirical anchors), 26 tension/open/pending rows comprising 7 TENSION, 16 OPEN_CONDITIONAL, 2 OPEN_RESEARCH, and 1 PENDING-α-RESOLUTION, and 4 registered FAIL rows (the electron row, which misses its LOCKED 1000 ppm pre-commitment at 1006 ppm; the Newton-$G$ row, which inherits that failure; the bottom-quark row, which misses the PDG $\pm5\sigma$ rule at 6.9σ; and the top-quark row, which misses its written P.24 $\pm5\sigma$ rule at 5.18σ). The 7 empirical-anchor PASS rows are settled-data postdictions (muon, up, down, strange and charm masses, CKM $s_{13}$, PMNS $\theta_{12}$); several of them rest on exponents found by postdictive search with no trial factor, and none is counted as evidence on its own strength. PASS means only that the value lies inside its registered band (descriptive arithmetic); as evidence that φ or icosahedral structure is special, the φ-formula rows of this table are **Tier 4** (constant control test v3, NEGATIVE-FRAGILE; App PSC §PSC.9.6). Self-consistency IMP01 is excluded, and each unique result name occupies one row. The single discrepancy-bearing item, `cage_node_count_N144`, compares the adopted manuscript datum 144 to 144; it is not an empirical cage-size observation. Four registered FAIL rows (electron, P.1c; Newton $G$, P.16; bottom quark, P.23; top quark, P.24) and zero unexpected FAIL rows are present.

---

## IVH.4 Independent-Verification Cross-Checks

The independent harness reports source-level disagreements as verification outputs and leaves the manuscript/engine comparison explicit. Three cross-check classes are tracked here.

### Newton's $G$ Precision

The independent Newton-$G$ verifier evaluates two explicitly separated branches. The model-authoritative branch uses $\alpha_{\rm GCT}=\phi^2/360$ with CODATA-2022 $m_e$ and exact SI $h,c$; it gives $G=6.689475523\times10^{-11}$ and **2273.725 ppm (displayed as 2274 ppm, 0.23%)**. The all-CODATA-$\alpha$ sensitivity branch gives $G=6.687737668\times10^{-11}$ and 2013.345 ppm. Thus 2274 ppm is a mixed model/empirical-input postdiction, not an all-CODATA-input evaluation; the 260.380 ppm branch difference comes from the $\alpha$ substitution. The comparison concerns the Jacobson Route 1 expression only, which reduces to the Planck identity $G=\hbar c/M_P^2$ through the electron-mass anchor in $a_6$; it does not validate the phason-elasticity Routes 2/3, whose dimensionally completed form differs from $G$ by a calibration-dependent factor that is never 1 ($\phi^{18}/(32\pi)\approx57$ in the Parameter Ledger convention $c=\phi^{-9}c_P$; $\phi^{-18}/(32\pi)\approx1.72\times10^{-6}$ only if $c_P=c$; App DPS §DPS.7). App PSC §PSC.2, V2 Ch09 §9.1.4, App ULA §ULA.8, App DPS §DPS.7, V3 Ch22, and the Parameter Ledger use the model-authoritative figure. The $G$ row is not independent of the electron row: $G \propto m_e^{-2}$ through $a_6$, so 2013.345 ppm $=(1+1006.17\ \text{ppm})^2-1$ and 2273.725 ppm $=(1+1136.22\ \text{ppm})^2-1$. It therefore carries the P.1c LOCKED 1000 ppm rule (2001 ppm on $G$), inherits P.1c's FAIL, and is not counted as a pass.

### Down-Quark Fuglede-Kadison Determinant

The down-quark route uses the Fuglede-Kadison determinant infinite-volume-limit branch as the primary source: $m_d = m_u \phi^{\phi} = 4.716$ MeV, a $+0.33\%$ residual against the PDG comparison value and inside the registered 11% shell-resonance gate. App TPR §TP-B records the finite-size scaling support: the FK-type geometric-mean determinant $\exp((1/N)\sum \log |\lambda_i|)$, with $N$ the number of non-zero eigenvalues (an ad hoc normalisation, not Lück's von-Neumann-trace normalisation; App GPE §GPE.4), on larger natural icosahedral shells centers on $\phi^\phi$, with the $I_h$-closed deep-tail mean $\det_{FK}/\phi^\phi=0.9976$ (sample std $0.0253$) and sequence-mean signed error vs PDG $+0.09\%$. Single-cage values oscillate within the 11% band with empirical decaying envelope; rigorous convergence proof and algebraic-field identification remain O.5. The charm-quark `fk_det_charm` entry remains Tier 3 heuristic pending K-theoretic gap-label closure (App ORQ O.5 / TP-F). The closed-cage sequence is recorded through `protocol_md_fk_ih_closed_cages.py`.

### Strange-Quark Target Import Path

The strange-quark comparison target is sourced from YAML through `protocol_quark_mismatch.py`, which reads `float(C.M_S_OBS)` for the `s` target. This keeps the script and configuration on a single source of truth. App PSC §PSC.3 reports the engine convention and its corresponding precision against the configured comparison value.

### Tensions (acknowledged in App PSC; not discrepancies in the verification sense)

- **PMNS $\theta_{23}$**: no longer a tension. The bare 45° lies inside the NuFIT 6.0 3σ ranges with and without SK atmospheric data ($\Delta\chi^2(45°)\approx2.0$ and $4.2$); the earlier one-octant 4.09σ figure is withdrawn and the octant is unresolved pending DUNE / Hyper-K.
- **$\sum m_\nu$**: 0.0853 eV vs DESI DR2 + CMB < 0.064 eV (ΛCDM, 95%) → active tension. App PRG/Falsifiability Matrix P.4 uses the registered exclusion band $\sum m_\nu < 0.075$ eV or $\sum m_\nu > 0.15$ eV at definitive precision; the DR2 bound already lies below the 0.075 eV gate, and the row remains a tension rather than a gate crossing only because the bound is ΛCDM-model-dependent.

These are tensions between the theory and the data, not between sub-parts of GCT's own documentation, so the verification harness records them as TENSION rather than DISCREPANCY.

---

## IVH.5 How to Re-Run the Verification

```bash
cd GCT_Physics_Engine/verify_independent
py -3.13 run_all.py # full harness
py -3.13 verify_muon_mass.py # single claim
```

**Expected outputs:**
- `results/<claim>.json` — one per verification script (overwritten on each run)
- `results/scorecard.json` — aggregated master scorecard with summary buckets

**Pytest mode:** the verification scripts also work as pytest functions. The `main` entry points return result dicts; add `assert result["status"] in ("PASS", "TIER1_EXACT", "TENSION")` in a thin pytest wrapper if integrating into CI.

**Python version:** Python 3.13 (matches the repo's pinned version). No third-party dependencies — only the standard library (`math`, `json`, `pathlib`, `typing`).

**Maintenance rule.** When any App PSC numerical claim changes, the corresponding `verify_<name>.py` script must be updated to match. The harness is intended to be ADJACENT to App PSC, not derivative of it. If a discrepancy is identified by the harness, the resolution path is to fix App PSC prose, fix the engine, or document the difference here in §IVH.4 — never to silently align the harness to suppress the disagreement.

---

## IVH.6 What This Harness Verifies and Doesn't Verify

**Verifies:**
- The canonical scorecard aggregate in §IVH.3 records the 54 allowlisted claim-result rows and their 7 empirical-anchor PASS, 9 internal-arithmetic, 8 Tier-1-exact, 26 tension/open/pending dispositions and 4 registered FAIL rows (electron, LOCKED 1000 ppm rule missed at 1006 ppm; Newton $G$, inheriting that failure; bottom quark, PDG $\pm5\sigma$ rule missed at 6.9σ; top quark, written P.24 $\pm5\sigma$ rule missed at 5.18σ), with zero unexpected FAIL. Its single discrepancy-bearing item, `cage_node_count_N144`, tests the adopted manuscript datum 144 against 144 rather than an empirical cage-size observation.
- Newton-G, down-quark, and strange-quark documentation mismatches are resolved into explicit tier/status dispositions: Newton-G is a 2273.725 ppm mixed model/anchor postdiction (display 2274 ppm) on $\alpha_{\rm GCT}=\phi^2/360$, derived from the electron row and carrying its FAIL; the all-CODATA-$\alpha$ branch is a separately labelled 2013.345 ppm sensitivity check. The down-quark route is postdiction-consistent conditional on O.5 through the primary $\phi^\phi$ FK limit; the strange-quark target imports the YAML/engine comparison value consistently.

**Doesn't verify:**
- The harness does NOT test the geometric derivation of the formulas themselves. It tests the *numerical evaluation* of those formulas given CODATA / PDG anchors. The geometric provenance (why $\phi^{-107}$ for the electron, why $\phi^{15+\phi^{-1}}$ for the proton, etc.) remains the responsibility of the manuscript prose and `App GPE (Physics Engine)`.
- The harness does NOT test consistency of formulas across chapters (e.g. that the proton-mass formula in Ch10 matches the one in App PSC). Cross-document formula parity is maintained by the canonical-source rule of App TAT §TAT.2, not by this harness.
- The harness does NOT validate Tier classifications. Each claim's tier label is inherited from App PSC.

**END OF APPENDIX IVH**
