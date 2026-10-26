### **Appendix NSM: Neutrino Mass Sum Contingency**

### NSM.1 Status and Scope

The conditional absolute-scale target $\Sigma m_\nu = m_1 + m_2 + m_3 \approx 0.0853$ eV (V3 Ch09 Theorem 9.1, $m_1 = m_e \cdot \phi^{-36}$ floor; oscillation gaps from PDG) is **Tier 3 and P3b-conditioned**, not a Tier 2 prediction: $\phi^{-36} = (\phi^{-18})^2$ enters as the square of the registered Tier 3 stiffness-map hypothesis P3b (App DPS §DPS.3; only the integer $D = 18$ is Tier 2). It lies above both the Planck+DESI 2024 combined 95% CL upper bound $\Sigma m_\nu \lesssim 0.072$ eV under $\Lambda$CDM cosmology and the tighter DESI DR2 + CMB $\Lambda$CDM bound $\Sigma m_\nu <0.064$ eV (95%); no single σ figure is quoted, since a "~2σ" label would understate the DR2 tension. V3 Ch22 §22.1.4 identifies this as an active near-term falsification risk. Euclid DR1-class weak-lensing/cosmology analyses are the registered next robustness check for whether the bound approaches the canonical exclusion band, $\Sigma m_\nu<0.075$ eV or $\Sigma m_\nu>0.15$ eV. P.4 and P.6 remain independent template/model-comparison evidence: no neutrino outcome activates or confirms a causal biogenic channel. The lower P.4 gate is deliberately above the normal-hierarchy oscillation floor near $0.059$ eV.

This appendix enumerates the three structurally distinct branches under which the P.4 template is retained, reframed, or excluded; the contingency map fixes the adjudication branches so the falsification verdict has an unambiguous map.

The three branches are mutually exclusive in their outcome but jointly cover the parameter space:

- **NSM.2 Branch 1 — Tightening.** Add a higher-order phason correction analogous to the muon's $\phi^8 \alpha^2$ self-energy and check whether it shifts the bare $\phi^{-36}$ result enough to escape the bound. **Result: structurally negative.**
- **NSM.3 Branch 2 — Conditional model comparison.** Re-evaluate the cosmological $\Sigma m_\nu$ bound under the registered conditional $w(z)$ template rather than $\Lambda$CDM's $w=-1$. **Result: an independent likelihood-comparison path, not a live rescue or causal-channel activation claim; the small registered template is expected to leave the bound near $0.064$ eV.**
- **NSM.4 Branch 3 — Falsification protocol.** Pre-registered list of what falls and what survives if Euclid DR1 establishes $\Sigma m_\nu < 0.075$ eV at definitive precision, or $\Sigma m_\nu >0.15$ eV. P.4 is adjudicated independently of P.6.

### NSM.2 Branch 1 — Tightening via 2nd-order phason self-energy

**The structural question.** The muon mass benefits from a $\phi^8 \alpha^2$ 1-loop self-energy correction that tightens the first-order $\phi^{11}(1+5\alpha)$ prediction from $\approx 0.24\%$ to $21$ ppm (V3 Ch08 §8.2.3). The same kind of correction must exist in principle for the neutrino, since the second-order phason coupling that yields $\phi^{-36}$ is itself a tree-level result subject to higher-order graphs. The question: is the magnitude of this correction sufficient to shift $\Sigma m_\nu$ from $0.0853$ eV below the DESI DR2 $\Lambda$CDM bound of $0.064$ eV, or even below the looser $0.072$ eV Planck+DESI 2024 bound? The correction acts on $m_{\nu_1}$ only; $m_2$ and $m_3$ follow from the oscillation gaps, so $\Sigma(m_1)=m_1+\sqrt{m_1^2+\Delta m^2_{21}}+\sqrt{m_1^2+\Delta m^2_{31}}$ with $d\Sigma/dm_1\approx2.2$ at the floor and a normal-ordering minimum $\Sigma(0)\approx0.059$ eV. Reaching $0.072$ eV needs $m_1\approx0.0088$ eV (a ~43% drop from $0.0153$ eV); reaching $0.064$ eV needs $m_1\approx0.0041$ eV (a ~73% drop).

**Bare formula and the correction ansatz.** Theorem 9.1 reads $m_{\nu_1} = m_e \cdot \phi^{-36}$ only after the Tier 3 P3b amplitude and the electron anchor are supplied [Tier 3, P3b-conditioned]. The muon-analogue 1-loop correction would have the structural form

$$m_{\nu_1}^{\text{1-loop}} = m_e \cdot \phi^{-36} \cdot \left(1 + c \cdot \alpha^k \cdot \phi^X\right) \quad \text{[Tier 3 ansatz]},$$

where $c$ is an $O(1)$ icosahedral combinatorial factor, $k$ is the loop order, and $\phi^X$ is the phason-stiffness scaling of the loop integrand. The muon's instance has $c \approx 1$, $k = 2$, $X = 8$ — giving a relative shift $\Delta m_\mu / m_\mu \approx \phi^8 \alpha^2 \approx 0.0025$ (positive).

**Order-of-magnitude bound.** For the neutrino, the natural loop order is also $k = 2$ (the second-order phason coupling is already the leading-order tree). The geometric exponent $X$ on the loop term is bounded above by the bare exponent itself: a loop correction cannot scale faster than the tree-level kernel it dresses. Therefore $|\phi^X| \lesssim \phi^{36}$ at most, and more plausibly $|\phi^X| \sim \phi^{18}$ (the single $K_\perp / K_\parallel$ factor), giving a relative shift

$$\left| \frac{\Delta m_{\nu_1}}{m_{\nu_1}} \right| \lesssim \alpha^2 \cdot \phi^{18} \approx 5.3 \times 10^{-5} \cdot 5.78 \times 10^3 \approx 0.31 \quad \text{[Tier 3 upper bound]}.$$

This is the loosest possible bound — and even at this loose bound, the sign of the correction is the open question. Without an explicit derivation of $c$ from the icosahedral self-energy graph topology, the sign is undetermined; without sign, "Branch 1 saves the prediction" is not falsifiable.

**Two more conservative estimates.**

- *Conservative bound: $X = 8$ (the muon's exponent).* Relative shift of $m_1$ $\lesssim \phi^8 \alpha^2 \approx 0.0025$. This shifts $\Sigma m_\nu$ by at most $\approx 8\times10^{-5}$ eV — about 160 times too small to reach $0.072$ eV and about 260 times too small to reach $0.064$ eV.
- *Conservative bound: $X = 0$ (no phason enhancement, pure $\alpha^2$).* Relative shift of $m_1$ $\lesssim \alpha^2 \approx 5 \times 10^{-5}$. Shift of $\Sigma m_\nu$ $\lesssim 2 \times 10^{-6}$ eV — nearly four orders of magnitude too small.

The loose bound $\phi^{18} \alpha^2 \approx 0.31$ is structurally implausible (it would represent a 31% correction to a tree-level result, the opposite of how loop expansions usually behave), and even it lowers $\Sigma m_\nu$ only to $\approx0.0755$ eV, still above both bounds. The realistic regime $\phi^{8} \alpha^2 \to \alpha^2$ changes $m_1$ by at most $\approx 0.25\%$ to $\approx 5 \times 10^{-3}\%$, against the ~43% (to $0.072$ eV) or ~73% (to $0.064$ eV) needed.

**Branch 1 conclusion [conditional negative, Tier 3].** Within the declared muon-analogue correction family, a 2nd-order phason self-energy is too small to lower the P3b-conditioned $\Sigma m_\nu$ below either $\Lambda$CDM bound: its natural magnitude is two to four orders of magnitude too small, and even the implausible loose bound falls short. This closes that correction ansatz as a non-viable direction; it does not close the first-principles neutrino scale.

The value $\Sigma m_\nu = 0.0853$ eV therefore remains a sharp **conditional** target rather than a fittable one: excluding it rejects the P3b-to-neutrino absolute-scale map (Branch 3), while leaving the Tier 2 integer $D_{H_3} = 18$ and unrelated sectors untouched.

### NSM.3 Branch 2 — Joint model-comparison under the conditional GCT dark-energy coordinate

**The structural claim.** The Planck+DESI 2024 $\Sigma m_\nu \lesssim 0.072$ eV bound is derived under the cosmological model $w(z) = -1$ exactly at all redshifts ($\Lambda$CDM). The GCT single-channel curve is phantom across all scanned redshifts ($w(z) \leq -1$ for all $z$ in the scan window). DESI 2024/DR2 CPL fits prefer the sign-opposite quadrant $(w_0 > -1, w_a < 0)$ — quintessence today with a more-phantom-in-the-past trajectory. The DESI-preferred dynamical-DE direction is therefore not a data driver for the conditional GCT template; it is an external tension registered as Open Problem O.13 closure-path C1, requiring a CMB+BAO+LSS likelihood to compare the independently adjudicated P.4 and P.6 templates under the same cosmology. Generic $w_0w_a$ neutrino-mass-bound relaxation cannot be imported without that likelihood; the $\Sigma m_\nu$ result remains independent P.4 model-comparison evidence and cannot activate P.6.

**The well-known degeneracy.** In the linear regime, the CMB constrains the integrated late-time geometry through the angular acoustic scale $\theta_*$ and the BAO scale $r_d D_V(z)$. Both depend on $\int_0^z dz' / H(z')$, which in turn depends on the dark-energy equation of state. A more negative $w$ at low $z$ accelerates the expansion, lowering $H_0$-equivalent late-time distances; the data can absorb a higher $\Sigma m_\nu$ as compensation. Quantitatively, the $\Sigma m_\nu$ posterior under standard CPL parameterisation $w(a) = w_0 + w_a(1-a)$ widens by a factor of $\sim 1.5$–$2$ relative to $\Lambda$CDM in Planck + BAO + SN fits when $w_0$ and $w_a$ are jointly free (DESI Y1 2024; Chen+ 2025; Planck 2018 §6) [Tier 3 — citation chain to cosmology literature, not GCT-internal].

**Specifically for the registered GCT coordinate.** The Tier 3 ansatz stipulates a continuous-phantom trajectory with $w(z) \leq -1$ across the low-redshift scan window and a Class-2-allocated envelope $|\Delta w(z=0.28)| \in [2,5]\times10^{-5}$. These are conditional model coordinates, not a derived biogenic mechanism; the phantom direction is stipulated and is Tier 4 as a physical claim, because the written dark-energy action cannot produce $w<-1$ without a ghost (V2 Ch14 §14.3.1). Plugging this $w(z)$ into a CMB+BAO+SN+LSS likelihood should give a $\Sigma m_\nu$ posterior close to the DESI DR2 $\Lambda$CDM-context value, approximately $0.064$ eV; the exact posterior is unavailable until the native likelihood is run. The typed coupling, normalized source history, and information-to-metric causal map remain open.

**Quantitative status [Tier 3 — pending full likelihood re-run].** A generic $w_0w_a$ relaxation cannot be imported as a GCT-native posterior because the GCT biogenic $w(z)$ prior is sign-opposite to the DESI-preferred dynamical-DE quadrant. The 0.0853 eV floor therefore remains in tension with the DESI DR2 $\Lambda$CDM bound, and the GCT-native likelihood path is expected to return $\approx0.064$ eV rather than $0.0853$ eV. A first-principles assessment still requires implementing GCT's $w(z)$ in a modified Boltzmann code (CLASS or CAMB extension) and re-running the full CMB+BAO+SN+LSS likelihood. This is the explicit research debt of Branch 2 / O.13c.

**Joint reporting — what it means for model adjudication.** P.4 and the conditional P.6 coordinate are displayed together because the inferred neutrino posterior depends on the adopted cosmology. This decision matrix is not a physical coupling or theorem; each template receives its own disposition. The registered P.6 multi-channel menu is already falsified at branch level under its >3σ rule (App FSM P.6); "the dark-energy template" in this table and in NSM.5 means the separate single-channel phantom template only:

| Euclid DR1 + DESI Y3 finds … | Verdict |
| :--- | :--- |
| $0.10 \leq \Sigma m_\nu \leq 0.15$ eV at $3\sigma$ AND $w < -1$ at low $z$ at $> 3\sigma$ | Both registered numerical templates are supported; no biogenic causal mechanism is thereby confirmed. |
| $\Sigma m_\nu < 0.075$ eV at definitive precision AND $w = -1$ at all $z < 0.5$ at $> 3\sigma$ | Both templates are excluded and their respective sectors are reopened. |
| $\Sigma m_\nu < 0.075$ eV at definitive precision AND $w < -1$ at low $z$ at $> 3\sigma$ | Mixed: the neutrino floor is excluded while the conditional dark-energy template remains compatible; rework Ch09 independently. |
| $0.10 \leq \Sigma m_\nu \leq 0.15$ eV at $3\sigma$ AND $w = -1$ at all $z < 0.5$ at $> 3\sigma$ | Mixed: the neutrino template remains compatible while the registered dark-energy coordinate is excluded. |
| $\Sigma m_\nu >0.15$ eV at definitive precision | P.4 upper exclusion fires; the registered absolute-scale floor is wrong on the high-mass side and Ch09 must be reopened independently of any survival of the dark-energy channel. |

This joint contingency table preserves the cosmology dependence of the inferred neutrino posterior without asserting a theorem or physical link between the two sectors.

**Branch 2 status [Tier 3].** This is an independent model-comparison calculation pending a likelihood that evaluates P.4 and P.6 under the same cosmology. Published generic CPL-prior relaxations are not imported as GCT support because the DESI-preferred quadrant is sign-opposite to the conditional single-channel template. The registered $w(z)$ amplitude points toward a bound near $0.064$ eV. The calculation neither activates P.6 nor supplies causal-channel evidence; it preserves separate dispositions for both templates.

### NSM.4 Branch 3 — Falsification Protocol (Pre-registered)

If Euclid DR1-class cosmology confirms $\Sigma m_\nu < 0.075$ eV at definitive precision AND DESI Y3 separately confirms $w = -1$ at all $z < 0.5$ at $> 3\sigma$ — the (-/-) cell of the NSM.3 table — the following sections of the manuscript are **falsified** and must be retracted:

**Falsified results:**

- **V3 Ch09 §9.3.1 Theorem 9.1** — the P3b-conditioned $\phi^{-36}$ second-order phason coupling mechanism (the P3b-to-neutrino absolute-scale map). The specific mass floor $m_{\nu_1} = m_e \cdot \phi^{-36} = 0.0153$ eV does not survive.
- **V3 Ch09 §9.3.4 joint contingency framing** — update the model-comparison record; the discrete mass spectrum and conditional dark-energy coordinate stand or fall independently.
- **V3 Ch09 §9.6.1 "$0.015$ eV Floor"** prediction (not KATRIN-falsifiable: current KATRIN limit $0.45$ eV vs $m_\beta \sim 0.018$ eV for normal ordering with NuFIT 6.0 splittings; tested via the cosmological $\Sigma m_\nu$ gate P.4, Project 8 long-horizon; Tier 3 conditional on P3b + A1).
- **V3 Ch09 §9.6.2 "$\Sigma m_\nu \approx 0.0853$ eV"** primary falsification vector — falsified by definition.
- **App PRG row P.4** — neutrino floor prediction.
- **V3 Ch19 Protocol G** — the derivation programme for the $\phi^{-36}$ eigenvalue becomes a forensic post-mortem of why the suppression mechanism failed.

**Sections requiring partial rework:**

- **V3 Ch09 §9.2.2 Geometric See-Saw** — the identification of "squared phason stiffness" with the neutrino-mass mechanism is what fails. The mathematical mechanism may survive with a different exponent (not $\phi^{-36}$) if a structural re-derivation lands on a different suppression power.
- **V3 Ch09 §9.2.3 $E_6$ Geometric See-Saw** — Theorem 9.2 numerics (consistent with Theorem 9.1) become inconsistent and must be redone.
- **V2 Ch14 §14.2 conditional dark-energy coordinate** — only if the registered phantom template is independently excluded. If $w < -1$ remains compatible while $\Sigma m_\nu$ falls, the conditional coordinate retains that compatibility but gains no causal-mechanism confirmation.

**Results that survive unaffected (orthogonal mechanisms):**

- **Lepton mass ratios** $m_\mu/m_e = \phi^{11} \cdot (1 + 5\alpha + \phi^8 \alpha^2)$, $m_\tau/m_e = \phi^{17} \cdot (1 - 3.6\alpha)$ — independent of the neutrino mechanism. Their postdiction residuals (muon −21 ppm, tau −51 ppm against PDG 2024; Tier 3 formula residuals conditional on A3, H-EW and the Tier 3 coefficient rules; Tier 4 as evidence, App PSC §PSC.9.6) are unaffected.
- **Fine-structure constant** $\alpha^{-1} = 360 \phi^{-2}$ — gauge sector, no overlap.
- **Electroweak boundary hypothesis** $\sin^2 \theta_W^{bare} = \phi^{-3}$ (Tier 3, H-EW; V3 Ch04 §4.3) — its open status is independent of the neutrino mechanism. The pre-registered gauge-running audit is a FAILED check (App GRF §GRF.4.3), so H-EW stands as a Tier 3 hypothesis at an unspecified scale.
- **Quark masses** $m_u, m_s, m_b, m_t$ (Tier 2 scaling mechanisms where registered; Tier 3 absolute values, App TAT) — strong sector, orthogonal. Each keeps its own registered disposition, including the P.24 top-quark FAIL of the written PDG $\pm5\sigma$ rule (174.07 GeV vs $172.57\pm0.29$ GeV, $5.18\sigma$) and the P.23 bottom-quark FAIL of the same rule (4134.69 MeV vs $4183\pm7$ MeV, $6.9\sigma$).
- **Down-quark Fuglede–Kadison mechanism** (primary output $m_d = m_u\phi^{\phi} = 4.716$ MeV, $+0.33\%$, POSTDICTION-CONSISTENT conditional on O.5; the exact $R=2$ finite-cage branch is a secondary value; App PSC, App TAT) — orthogonal.
- **Proton mass** $m_p = m_e \phi^{15+\phi^{-1}}$ (formula output $1836.437\,m_e$ vs $1836.153\,m_e$, +155 ppm, inside the 500 ppm postdiction band; Tier 4 as evidence, App PSC §PSC.9.6) — hadron sector, orthogonal.
- **Newton's $G$** via Jacobson chain (2274 ppm, model-authoritative $\alpha_{\rm GCT}$ branch) — independent of the neutrino mechanism; it is the electron Planck-link row inverted, so it is not independent evidence and is not counted as a pass while the electron row fails its LOCKED rule.
- **$\alpha_s$ bare $= 10\phi^2$** (TP-C per-factor trace documented; product remains a Tier 3 calibrated handle pending O.42 / QLQCD-2) — strong coupling, orthogonal.
- **Canonical electroweak projector split $1/2+1/2$** (Tier 1 exact projector identity; the bare angle $\phi^{-3}$ is a separate Tier 3 hypothesis, V3 Ch04 §4.3) — independent of the neutrino mechanism.
- **Structural results outside the neutrino mechanism** — unaffected: the Tier 1 photon-masslessness control (unbroken local $U(1)$ gauge invariance and the Ward identity), the Tier 3 Wheeler–DeWitt adoption, the conditional $D=3$ knot argument (Tier 1 knot mathematics plus a Tier 3 premise; App TCD §TCD.2) and the Tier 1/2 rank-six architectural choice. None of these touches the neutrino mechanism; the Standard-Model spectral-triple identification remains conditional on O.32.
- **CP-violating phase $\delta_{CP} = 360^\circ \cdot \phi^{-1}$** — a Tier 3 phase ansatz (App FSM P.12b/P.31), independent of the Jarlskog magnitude (O.7) and of $\Sigma m_\nu$.
- **Electron EDM estimate** $d_e \sim 3 \times 10^{-31}\, e \cdot \text{cm}$ at the candidate $J_{\rm CKM}^{\rm GCT} \sim \phi^{-22}$ scale under a reference normalization (Ch09 §9.6.3) — a Tier 3 estimate inheriting the open CKM invariant (O.7) and a beyond-Standard-Model loop structure, not $\phi^{-36}$. Survives.

**Post-falsification structural story.** If Branch 3 fires, GCT retains the bare fine-structure relation $\alpha^{-1}=360\phi^{-2}$ (Tier 3; mechanism open) and the charged-lepton ratios as Tier 3 formula residuals conditional on A3, H-EW and the Tier 3 coefficient rules (see the lepton bullet above), with the native-RGE endpoint and precision-comparison rows adding anchors A2–A6 (Parameter Ledger §0.1), plus a Tier 2 area-law mechanism for the cosmological-constant sector whose absolute magnitude remains Tier 3/calibration-imported (V2 Ch14 §14.1.5). The neutrino *absolute* scale becomes a Tier 3 Open Problem alongside the Higgs absolute scale and the dark-energy dynamics. As evidence that φ is special, these retained φ-formula matches are Tier 4 whatever Branch 3 does (Tier 4 as evidence: not distinguishable from numerology for strong effects; App PSC §PSC.9.6). The parameter accounting itself (11 declared core inputs; P3b outside the count) is unchanged: the neutrino floor was never part of a closed dimensional system, since it rests on P3b.

The retraction text for §9.3.1 / §9.3.4 / §9.6.2 is specified by this appendix's decision matrix; no additional narrative discretion is intended at adjudication time.

### NSM.5 Decision matrix

| Outcome (Euclid DR1 + DESI Y3) | Action |
| :--- | :--- |
| $0.10 \leq \Sigma m_\nu \leq 0.15$ eV & $w < -1$ at low $z$ ($> 3\sigma$ each) | Both registered numerical templates supported; retain their existing tier split. This does not promote or empirically validate a biogenic causal mechanism. |
| $0.05 \leq \Sigma m_\nu < 0.10$ eV at definitive precision | NSM.5 boundary outcome: values below $0.075$ eV fire the lower P.4 exclusion boundary; values in $[0.075,0.10)$ are inside the P.4 window and consistent with the registered 0.0853 eV floor; support requires O.13b (the common-cosmology likelihood) plus the Ch09/App PRG disposition update before any independent P.4 support claim. No result activates P.6. |
| $\Sigma m_\nu < 0.075$ eV at definitive precision & $w = -1$ at all $z < 0.5$ ($> 3\sigma$) | NSM.4 fires. Execute Branch 3 retraction protocol. |
| $\Sigma m_\nu < 0.075$ eV at definitive precision & $w < -1$ at low $z$ ($> 3\sigma$) | Mixed; reopen the neutrino floor while the conditional dark-energy template remains compatible. No causal-mechanism inference follows. |
| $0.10 \leq \Sigma m_\nu \leq 0.15$ eV & $w = -1$ at all $z < 0.5$ ($> 3\sigma$) | Mixed; retain the neutrino result and exclude the registered conditional dark-energy template independently. |
| $\Sigma m_\nu >0.15$ eV at definitive precision | Upper-band P.4 exclusion; reopen the absolute neutrino-scale mechanism regardless of the P.6 verdict. |
| Neither bound nor crossing established at decisive precision | Prediction remains active in tension; await the registered cosmology and direct-mass programs. |

### NSM.6 Cross-references and registry updates

This appendix:

- *consumes* V3 Ch09 (Theorems 9.1, 9.2 and §9.3.4), V2 Ch14 (§14.1, §14.2), V3 Ch12 (Dynamic Dark Energy), V3 Ch19 (Protocol G), V3 Ch22 §22.1.4 (binary gates).
- *updates* App PRG rows P.4 and P.6 to make their independent template/model-comparison roles explicit; neither can activate a causal biogenic channel.
- *informs* the App FSM Falsifiability Matrix row for P.4, whose roadmap link points to this appendix.
- states the explicit NSM.3 conditional that governs the V3 Ch09 §9.3.4 discussion, which cross-references this appendix for the falsifiability protocol.

**End of Appendix NSM.**
