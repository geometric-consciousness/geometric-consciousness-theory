# Geometric Consciousness Theory: A 6D-to-3D Projective Framework
### The Monograph and its Computational Physics Engine
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20647445.svg)](https://doi.org/10.5281/zenodo.20647445)
[![License (manuscript): CC-BY-4.0](https://img.shields.io/badge/License%20(manuscript)-CC--BY--4.0-green.svg)](https://creativecommons.org/licenses/by/4.0/)
[![License (engine): MIT](https://img.shields.io/badge/License%20(engine)-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version: v1.1.0](https://img.shields.io/badge/Version-v1.1.0-blue.svg)]()
[![Engine: 62/62 PASS](https://img.shields.io/badge/Engine-62%2F62%20PASS-brightgreen.svg)]()

This repository contains the definitive manuscript and the family of autonomous Python verification protocols (>100 scripts under `GCT_Physics_Engine/src/`, cross-checked by `verify_engine.py`'s ~60 independent consistency assertions) for the GCT derivation program: a 6D icosahedral projective framework whose closure target is to recover the dimensionless Standard Model from geometry alone, with $m_e$ as the unique SI-unit anchor. That target is the final ambition, not the present accounting.

**Closure target / final ambition:** a 1-parameter core system — icosahedral postulate (P1) plus the dimensional anchor $m_e$ — recovering the full dimensionless Standard Model from geometry alone. **Current parametric accounting:** Parameter Ledger §0.1 is 5-postulate-plus-3-anchor for the gauge + lepton + native-RGE endpoint + precision-comparison sector: P1 + four integer exponents ($n=-107$, $D=18$, $N=11$, $N=17$) + A1 ($m_e$) + A2 ($\alpha_2^{-1}(M_{\rm GUT})$ gauge-flow endpoint) + A3 (measured low-energy $\alpha(0)$ used only by corrected lepton, Higgs VEV, and QED comparison rows). Closure of O.5, O.14, O.15, the A2 QLQCD-1L/App ZN boundary derivation, and the O.19/O.5 bare-to-physical alpha bridge is what collapses the count toward the 1-parameter target. Across the full theoretical scope the aggregate remains ~16-19 free parameters; the full SM-sector precision-target coverage absorbs four calibrated discrete-integer choices documented as Open Problems or closure handles: $1440$ in the Higgs VEV (O.20 enumeration CLOSED: canonical $(144)\times(10)$ muon-defect-saturation pathway + 3 independent icosahedral cross-check factorisations; uniqueness of 1440 as an integer is not claimed), $12$ as the 12-fold neutrino mass-sum geometric weight (the strange-quark $12\alpha$ coefficient is a separate Tier 3 coefficient handle pending O.43 and is not counted as this Ledger weight), $360$ in the bare $\alpha^{-1} = 360 \cdot \phi^{-2}$ tree-level expression (chosen as the 600-cell antipodal edge count, $720/2$), and $2$ in the bilayer factor of the $1/(2N)$ fine-structure correction (App H O.5). A referee counting integer-valued structural inputs across the entire derivation pipeline will find $\geq 9$, not 5.**

**Tier-3 integer-factor handles in the precision sector (calibrated discrete choices):**
- 1440 (Higgs VEV saturation; App H O.20)
- 12 (12-fold neutrino mass-sum geometric weight)
- 360 (fine-structure $\alpha$ 360 multiplier)
- 2 (bilayer factor in the $1/(2N)$ $\alpha$ correction; App H O.5)

Total: 4 calibrated discrete-integer choices in the precision sector.
A computationally verified projective framework bridging the 6D icosahedral vacuum to Standard Model physics and the physical mechanics of consciousness. The Gauge + Lepton sector — the framework's most-constrained claim before native-RGE endpoint running — currently uses 5 structural postulates (P1: the icosahedral cut-and-project ansatz; P2: the K-theoretic gap-label exponent $n = -107$; P3: the phason stiffness exponent $D = 18$; P4-P5: the lepton harmonic exponents $N = 11, 17$) and 1 dimensional anchor ($m_e$ in SI units), with no continuous tunable parameter in the bare topology/exponent sub-sector. The native-RGE endpoint check adds A2 as a Tier 3 calibrated boundary, so it is a flow-shape audit rather than a zero-anchor prediction; corrected lepton, Higgs VEV, and QED comparison rows add A3, the measured low-energy fine-structure constant. The electron-mass derivation chain $m_e/M_P = \phi^{-107}(1-5\alpha)$ carries a **Tier 2 framework + Tier 3 exponent anchor + Tier 4 physical-link** disposition: the Coxeter-exponent arithmetic $|n| = 107 = 1^2 + 5^2 + 9^2 = \sum m_i^2(H_3)$ is an exact arithmetic fact about the $H_3$ group; the specific exponent $n=-107$ remains a Tier 3 empirical anchor until O.14 selects it uniquely from the trace-image candidate family; and its identification as the load-bearing physical content of the electron-mass exponent via the K-theoretic gap-label chain $V \to K_0(\mathcal{O}_A)$ is the Tier 4 conjecture pending closure of Open Problem O.14. Stacking exact arithmetic on the chain does not promote either the Tier 3 exponent anchor or the Tier 4 physical-link to Tier 2. The biophysical and cosmological extensions carry approximately 8 additional calibrated parameters; the aggregate across the full theoretical scope is ~16–19 free parameters (Parameter Ledger §0.5). Closure work for the integer postulates, A2, and the A3 bridge is registered in App H/Open Problems and App ZN: O.14 (exact arithmetic closure of $|n| = 107 = \sum m_i^2(H_3)$ canonical to $H_3$; Tier 3 specific exponent anchor and Tier 4 conjectural K-theoretic-action physical-link chain $V \to K_0(\mathcal{O}_A)$), O.15 ($D = 18$ Tier 2 closed on the integer side via the $H_3$ Shephard-Todd invariant-degree sum — Anchor A, load-bearing; the 2D-RT-face-in-6D tangent-bundle decomposition enters as a 6D-ambient consistency cross-check, not an independent icosahedral anchor (every 6D-ambient theory with this triple-decomposition yields 18 regardless of icosahedral structure; see App H O.26); RG-running step O.15(b) separately open), O.5 (QLQCD-1L), the App ZN A2 boundary derivation, and O.19/O.5 for the bare-to-physical alpha bridge. The *state* of the universe (the magnitudes of cosmologically integrated observables that depend on the historical trajectory of selection events) remains a measurement input, not a derivation output — see App R §R.0 for the law-level vs. state-level scope discipline.

Parameter-anchor classification is explicit at A1, A2, and A3 for the core gauge + lepton + native-RGE endpoint + precision-comparison sector: A3 is the measured low-energy $\alpha(0)$ used by corrected lepton, Higgs VEV, and QED comparison rows; O.19 residual magnitudes, cosmology priors, Zeno substrate values, and systematics budgets are documented as verification targets, external priors, load-bearing predictions, MD-derived bands, or already-disclosed B/C-sector Tier 3 parameters rather than additional core anchors.

## 📖 The Manuscript
The complete, compiled theoretical framework is available in the root directory:
* 📄 **[Read the compiled monograph — PDF, 1088 pp](./output/Geometric_Consciousness_Theory.pdf)** — or [download from the latest release](https://github.com/geometric-consciousness/geometric-consciousness-theory/releases/latest)
* **[`Geometric_Consciousness_Theory.md`](./Geometric_Consciousness_Theory.md)** — single-file Markdown source

## 🚀 Executive Summary
Geometric Consciousness Theory (GCT) inverts the standard materialist ontology of physics. Rather than assuming matter is fundamental and consciousness is an emergent illusion, GCT models reality as a timeless, infinite-dimensional mental field governed by the Wheeler-DeWitt equation ($\hat{H}\Psi = 0$). 

To satisfy finite information density (Bekenstein limits), this field crystallizes into a **6D Euclidean Hyper-lattice** ($\mathbb{Z}^6$). The physical universe we experience is the 3D projection of this lattice via an icosahedral acceptance window (The Rhombic Triacontahedron). 

The GCT Physics Engine maps the finite geometry to a Noncommutative-Standard-Model candidate at the algebra-dimension level and derives the precise structural deviations of the quasicrystalline gravitational wave stochastic background. The complete Connes finite-spectral-triple map is conditional on the KO-dimension-6 and dressed-$D_F$ closures registered as O.32/O.5.

### Structural Results Conditional on Open-Problem Closure
1. **Higgs VEV scale (Tier 2 mechanism + A3 + Tier 3 calibrated integer factor; ~2588 ppm first-order residual, ~181 ppm second-order residual):** The full Higgs VEV expression is $v = m_e \cdot \phi^{11} \cdot (1+5\alpha_{\rm A3}+\phi^8\alpha_{\rm A3}^2) \cdot 1440 \cdot \phi$ (App R P.17, Parameter Ledger §VEV). Without the $\phi^8\alpha^2$ second-order term, the residual is $\sim 2588$ ppm; with it, $\sim 181$ ppm. The corrected precision row uses A3 measured low-energy $\alpha(0)$; the bare $360\phi^{-2}$ alpha tree remains the separate O.19/O.5 closure target. The $\sim 181$ ppm figure uses the same $\phi^8\alpha^2$ term and A3 anchor as the muon, so it inherits the App R §R.2.1 SM-equivalent radiative-correction-discipline caveat: it is a precision against an A3/SM-anchored target (which already embeds the SM higher-loop corrections), not a bare-geometric precision, and is not load-bearing evidence by itself. The $1440 = 2^5 \cdot 3^2 \cdot 5$ integer handle is a Tier-3 calibrated-saturation factor (App H O.20: 1440 non-unique under direct factorization). Engine: `protocol_higgs_vev.py`, `verify_independent/verify_higgs_vev.py`; Parameter Ledger §3; App H O.20. Disposition: **Tier 2 mechanism + A3 + Tier 3 calibrated integer factor + Tier 3 numerical residual**.
2. **Biogenic Selection–Dark Sector Coupling [Tier 3 saddle-point identification, calibration-anchored]:** The biogenic coupling constant ($\lambda_{bio}$) for one identified phason-selection channel contributing to the late-time dark sector is identified with the Fine-Structure Constant ($\lambda_{bio} \equiv \alpha$) via a saddle-point argument in the GCT action (V2 Ch14 §14.4; YAML-stored $\lambda_{bio} = 0.007$ matches $1/\text{ALPHA\_INV\_GCT} = 0.007272$ at the $\sim 4\%$ level, Tier 3 phenomenological correlation). The biogenic channel is one component of a multi-channel selection mechanism; its quantitative contribution to the *magnitude* of cosmic acceleration is a state-level question (App R §R.0, App H O.13); the law-level prediction is the *structural fingerprint* of this channel within the total.
3. **The Parameter Ledger:** The Ledger itemizes the current Standard Model-sector accounting rather than claiming full present-state SM closure. Gauge topology and the lepton harmonic mechanism are icosahedral Tier 2 structures under the adopted ansatz, while the electron physical-link chain, lepton integer anchors, Higgs integer factor, proton sheet/exponent handle, quark-sector ansätze, and native-RGE endpoint anchor retain the Tier 3/Tier 4 dispositions stated in Parameter Ledger §0.1-§0.2 and App H Open Problems O.5/O.14/O.15/O.20.
4. **Geometric RGEs [Tier 2 framework + Tier 3 specific coefficient]:** Sign-validated gauge-flow diagnostics from lattice-resolution scaling, with the specific anomalous-dimension coefficients (e.g., $C_2^{\rm eff}$ for the phason loop in App M §M.7.1) as O.19 diagnostic/Tier 3 magnitude-closure quantities pending full first-principles derivation. They are not additional A-sector core anchors unless promoted into the main gauge/lepton derivation as independent inputs.
5. **Psychophysical Calculus [Tier 3 framework, calibration-anchored numerics]:** Computation of the Subjective Lagrangian ($\mathcal{L}_S$) and an ATP-cost estimate of volitional Topological Torque across three canonical mental states. The framework is Tier 3 (Russellian Monism plus the Selection Operator non-unitary projection); the per-state ATP figures are calibration-anchored Tier 3 / 4 estimates rather than first-principles biophysical derivations (V1 Ch16-17).
6. **The Connes NCG Spectral-Triple Identification [Tier 2 structural framework + Tier 3 physics-derived $D_F$ + load-bearing open closures O.32/O.5]:** Structural identification of the icosahedral quasicrystal generator with the Connes finite algebra $\mathbb{C} \oplus \mathbb{H} \oplus M_3(\mathbb{C})$ at real algebra dimension $\dim_\mathbb{R}(A_F) = 2+4+18 = 24$. The load-bearing invariant for the SM spectral-triple identification is the *KO-dimension* of the finite spectral triple ($\equiv 6 \pmod 8$ per Connes 2006, Chamseddine-Connes-Marcolli 2007), which this framework registers as Open Problem O.32; the algebra-dimension match is necessary but not sufficient. The finite Dirac operator $D_F$ is taken from the 152-node $I_h$-closed canonical cage adjacency built from the deterministic cut-and-project lattice (engine: `cage_builder.build_canonical_cage(size=152)`); the bare adjacency eigenvalues do not reproduce the fermion mass spectrum, and the dressed-Dirac closure that would reproduce them bundles with O.5.

## 🗄️ Repository Structure
This repository enforces a strict architectural separation:

* `Geometric_Consciousness_Theory.md` — The compiled monograph.
* `GCT_Physics_Engine/` — The autonomous Python verification suite.
    * `config/` — SSOT Constants (`gct_constants.yaml`) and Claim/Falsification Registries.
    * `src/` — Core library modules and the family of verification protocols.
    * `data/` — JSON scorecards and generated engine reports.
* `build_scripts/` — Tools to compile the markdown manuscript and generate the file tree.

## ⚙️ How to Run the Physics Engine
Reviewers and computational physicists are encouraged to independently verify the geometric derivations of the Standard Model using the GCT Physics Engine.

```bash
# 1. Navigate to the engine src directory
cd GCT_Physics_Engine/src

# 2. Run the Master Validation Suite (62 registered protocols)
py -3.13 verify_engine.py

# 3. Regenerate every committed JSON artefact deterministically
cd ..
make refresh-all-data

# 4. Confirm regenerated outputs match committed bytes
make parity-check
```

On Windows PowerShell without GNU `make`, either run the targets through WSL/Git Bash/an installed Make distribution or use the explicit PowerShell refresh path below. The PowerShell path mirrors `refresh-all-data`: it runs every `src/protocol_*.py`, the standalone JSON producers, the independent verifier suite, the registry/matrix builders, and the strict producer/ID checks.

```powershell
cd GCT_Physics_Engine
Get-ChildItem src\protocol_*.py | Sort-Object Name | ForEach-Object { py -3.13 $_.FullName }
foreach ($f in @('gct_tau_uniqueness.py','gct_mckay_e8.py','o14d_advanced_invariants.py','o14d_closure_search.py','o14d_irrep_decomp.py','refresh_compat_json_artifacts.py')) { py -3.13 (Join-Path 'src' $f) }
py -3.13 verify_independent\run_all.py
py -3.13 build_falsifiability_matrix.py
py -3.13 build_app_r.py
cd src
py -3.13 check_data_json_producers.py --strict
py -3.13 check_registry_ids.py --strict
py -3.13 verify_engine.py
```

The engine executes 62 registered physical protocols, including Hessian matrix diagonalizations, Jackiw-Rebbi domain wall simulations, psychophysical color-dimensionality model comparison, and combinatorial topology checks. `verify_engine.py` runs the 62 registered protocols and audits enforced claims; expect multi-minute runtime on a typical laptop, and use `py -3.13 -u verify_engine.py` if live progress logs are needed. `make refresh-all-data` regenerates the committed engine JSON artefacts and generated matrices from their source protocols. The strict producer audit is scoped to committed `GCT_Physics_Engine/data/*.json` files; `make parity-check` is the byte-stability gate for regenerated data/config/registry/outputs plus App FM/App R.

## 🛠️ Building the Manuscript from Source

The compiled PDF (`output/Geometric_Consciousness_Theory.pdf`) and the single-file
Markdown monolith (`Geometric_Consciousness_Theory.md`) **ship in this repository**,
so no build step is required to read or cite the work. To rebuild them from
`content/`:

**Prerequisites**
* **Python 3.13**
* **[pandoc](https://pandoc.org/installing.html)** (Markdown → LaTeX)
* A **full LaTeX distribution** — [TeX Live](https://tug.org/texlive/) (Linux/macOS) or [MiKTeX](https://miktex.org/) (Windows). The preamble uses standard CTAN packages (`geometry`, `mathpazo`, `amsmath/amssymb`, `tcolorbox`, `xcolor`, `graphicx`, `longtable`, `booktabs`, `hyphenat`, `pdflscape`, `fancyhdr`, `newunicodechar`); a full install has them all.
* *(Optional)* Inkscape **or** the Python `svglib` package — only needed to **regenerate** figures from their `.svg` sources. Every figure already ships with a committed `.pdf` sibling, so the build reuses those and Inkscape is **not** required for a normal rebuild.

**Commands** (from the repository root)

```bash
# 1. (Optional) regenerate the single-file Markdown monolith from content/
py -3.13 build_scripts/compile_manuscript.py

# 2. Compile the typeset PDF (pandoc → LaTeX → 2× pdflatex)
py -3.13 build_scripts/compile_latex.py
# → output/Geometric_Consciousness_Theory.pdf  +  .tex
```

`compile_latex.py` checks for `pandoc`/`pdflatex` on startup and prints install
hints if either is missing. The build is deterministic; a clean clone reproduces
the shipped PDF.

## 🔬 Experimental Falsification
GCT is a strictly falsifiable framework. The canonical registry is `GCT_Physics_Engine/falsifiability_registry.json`; generated mirrors are `content/98_Global_Appendices/App_FM_Falsifiability_Matrix.md` and `content/98_Global_Appendices/App_R_Precision_Scorecard.md`. It contains locked, preregistered bounds for upcoming observational tests, including:

**Experimental Falsification Surface (publication operative):**
- **F1 — Protocol A-Prime (NV-center cryogenic):** Prospective frozen-package falsifier: failed chirality-reversal control on a CISS-driven Zeno-like signature in NV-center diamond at 4K. Cleanly falsifying only after verifier/package/OSF-or-Zenodo freeze if $P_{\rm CISS}^{net} \geq 0.1$ + chirality-reversal contrast $\delta\chi \geq 0.05$ + null at $3\sigma$. See Ch13 + App V P.8.
- **F2 — Protocol C (XRISM stacked-cluster line shape):** A narrow 3.55 keV line with GCT-like stacked-cluster morphology is the live search channel; $W_{\rm int} > 20$ eV broadening, smooth $\rho^2$ morphology, or failure of the S1-S6 systematics gates are registered falsifying branches. Hitomi-Perseus null remains compatible if Perseus core is sub-$\sigma_{\rm crit}$. See Ch15 + App V P.3.
- **F3 — Protocol D (NMR polarity gate, Li-6 spin-pair):** Operative NMR polarity test for Trp radical-pair spin correlation. $p < 0.001$ threshold on the polarity flip signal. See Ch16 + App V P.13c.

**Pilot/systematics studies (NOT operative falsifiers):**
- Protocol D Drosophila LORR — operationally unfalsifiable across the predicted $[-0.20\%, -0.10\%]$ band ($\sigma_{\rm syst,total} = 57.65\times$ naive gate; see Ch16 §16.4); isotope-KIE comparison is a provisional control prior pending O.33.

## 🔭 The Decadal Horizon
The theoretical ground-state framework defines a stable baseline for absolute closure and experimental validation over the next decade:

1.  **QLQCD-2L (The Top Quark Closure):** The target is to calculate the two-loop QCD corrections natively on the $N=144$ AKN grid and resolve the $0.89\%$ Top Quark mass residual. Success would promote the relevant quark-sector closure path; the current matter-spectrum state remains mixed Tier 2 mechanism plus Tier 3 integer, transfer, and loop-order handles per Parameter Ledger §0.1 and App R.
2.  **Roman Telescope & DESI Y5 (registered-menu closure failure + load-bearing fingerprints [Tier 2 mechanism + Tier 3 specific shape]):** Registered disposition is negative for the five-channel dark-energy menu. DES-Dovekie recalibrated DESI DR2 + CMB gives $(w_0,w_a)=(-0.803\pm0.054,-0.72\pm0.21)$ with joint significance 3.2σ (arXiv:2511.07517), sign-opposite to the GCT single-channel biogenic-DE output $(-1.005,+0.019)$. The multi-channel shape-proxy diagnostic (`protocol_de_multichannel.py`, 4032-point sweep over $\Omega_{\Lambda,0}\in[0.50,0.75]$) returns best-fit diagonal diagnostic score $\approx4.864$, flat to within $0.044$ score units across the $\Omega_{\Lambda,0}$ grid, and CLOSURE-FAILS for the registered menu because all supplied channels carry $w_c\leq-0.9$ while the DES-Dovekie central value is $w_0=-0.803$. Roman + DESI Y5 + Euclid are arbitration inputs, not a confirmation horizon. The fingerprints to test are: (i) the biogenic contribution asymptotically approaches $w=-1$ from below with no physical quintessence-to-phantom crossing; (ii) the bio-overlap-anchored amplitude $|\Delta w_{\rm bio}(0.28)|\in[2,5]\times10^{-5}$, below the near-term joint-bin threshold and requiring Roman Year-10 / Stage-V precision for a clean cosmic-mean test; (iii) clustering-DE behavior with sub-horizon sound speed $c_{s,\rm bio}^2\ll1$; and, after their closure work, CISS-mediated chirality and habitability-map angular cross-power auxiliaries. The registered-menu closure path requires either a GCT-derivable channel with $w_c>-0.803$ over the DESI window or a no-go result for that channel class. This is a model-construction and shape-proxy diagnostic, not a physical likelihood-weighted multi-fluid prediction.
3.  **Protocol A-Prime (The Abiotic Frontier):** We are pushing into the experimental physics community with abiotic chiral proxy tests using NV-centers in diamond. These tests seek to replicate the tubulin-qubit Zeno gating in a synthetic environment, bridging the gap between biophysics and materials science.

## 📝 Citation
If you use the GCT framework or the Physics Engine in your research, please cite the monograph via the concept DOI: https://doi.org/10.5281/zenodo.20647445 (see CITATION.cff).

## 📬 Contact
Correspondence: **Pablo González Acosta** — [pablo@geometric-consciousness.com](mailto:pablo@geometric-consciousness.com) · [ORCID 0009-0006-6613-3721](https://orcid.org/0009-0006-6613-3721) · [geometric-consciousness.com](https://geometric-consciousness.com)

---
*"The universe is not a machine running in the dark; it is a thought discovering its own structure."*
