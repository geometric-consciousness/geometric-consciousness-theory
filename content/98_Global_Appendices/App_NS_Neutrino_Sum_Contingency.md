### **Appendix NS: Neutrino Mass Sum Contingency**

### NS.1 Status and Scope

The Tier 2 mechanism plus Tier 3 absolute-scale prediction $\Sigma m_\nu = m_1 + m_2 + m_3 \approx 0.0853$ eV (V3 Ch09 Theorem 9.1, $m_1 = m_e \cdot \phi^{-36}$ floor; oscillation gaps from PDG) sits in $\sim 2\sigma$ tension with the Planck+DESI combined 95% CL upper bound $\Sigma m_\nu \lesssim 0.072$ eV under $\Lambda$CDM cosmology and the DESI DR2 $\Lambda$CDM-context bound $\Sigma m_\nu <0.064$ eV. V3 Ch22 §22.1.4 identifies this as an active near-term falsification risk. Euclid DR1-class weak-lensing/cosmology analyses are the registered next robustness check for whether the bound approaches the canonical exclusion band, $\Sigma m_\nu<0.075$ eV or $\Sigma m_\nu>0.15$ eV, under the joint P.4/P.6 likelihood discipline; the lower gate is deliberately above the normal-hierarchy oscillation floor near $0.059$ eV.

This appendix enumerates the three structurally distinct branches under which the prediction either survives, gets reframed, or falls; the contingency map fixes the adjudication branches so the falsification verdict has an unambiguous map.

The three branches are mutually exclusive in their outcome but jointly cover the parameter space:

- **NS.2 Branch 1 — Tightening.** Add a higher-order phason correction analogous to the muon's $\phi^8 \alpha^2$ self-energy and check whether it shifts the bare $\phi^{-36}$ result enough to escape the bound. **Result: structurally negative.**
- **NS.3 Branch 2 — Coupled prediction.** Re-derive the cosmological $\Sigma m_\nu$ bound under GCT's biogenic dark-energy $w(z)$ rather than $\Lambda$CDM's $w = -1$. **Result: native-likelihood calculation path, not a live rescue claim; the registered GCT $w(z)$ amplitude is expected to return a bound near $0.064$ eV, so it binds $\Sigma m_\nu$ jointly with the P.6 dark-energy arbitration gate while preserving the active tension.**
- **NS.4 Branch 3 — Falsification protocol.** Pre-registered list of what falls and what survives if Euclid DR1 confirms $\Sigma m_\nu < 0.075$ eV at definitive precision, or $\Sigma m_\nu >0.15$ eV, under the joint P.4/P.6 gate.

### NS.2 Branch 1 — Tightening via 2nd-order phason self-energy

**The structural question.** The muon mass benefits from a $\phi^8 \alpha^2$ 1-loop self-energy correction that tightens the bare $\phi^{11}$ prediction from $\sim 0.25\%$ to $21$ ppm (V3 Ch08 §8.2.3). The same kind of correction must exist in principle for the neutrino, since the second-order phason coupling that yields $\phi^{-36}$ is itself a tree-level result subject to higher-order graphs. The question: is the magnitude of this correction sufficient to shift $\Sigma m_\nu$ from $0.0853$ eV below the $0.072$ eV $\Lambda$CDM threshold (a $\sim 16\%$ downward shift)?

**Bare formula and the correction ansatz.** Theorem 9.1 reads $m_{\nu_1} = m_e \cdot \phi^{-36}$ [Tier 2]. The muon-analogue 1-loop correction would have the structural form

$$m_{\nu_1}^{\text{1-loop}} = m_e \cdot \phi^{-36} \cdot \left(1 + c \cdot \alpha^k \cdot \phi^X\right) \quad \text{[Tier 3 ansatz]},$$

where $c$ is an $O(1)$ icosahedral combinatorial factor, $k$ is the loop order, and $\phi^X$ is the phason-stiffness scaling of the loop integrand. The muon's instance has $c \approx 1$, $k = 2$, $X = 8$ — giving a relative shift $\Delta m_\mu / m_\mu \approx \phi^8 \alpha^2 \approx 0.0024$ (positive).

**Order-of-magnitude bound.** For the neutrino, the natural loop order is also $k = 2$ (the second-order phason coupling is already the leading-order tree). The geometric exponent $X$ on the loop term is bounded above by the bare exponent itself: a loop correction cannot scale faster than the tree-level kernel it dresses. Therefore $|\phi^X| \lesssim \phi^{36}$ at most, and more plausibly $|\phi^X| \sim \phi^{18}$ (the single $K_\perp / K_\parallel$ factor), giving a relative shift

$$\left| \frac{\Delta m_{\nu_1}}{m_{\nu_1}} \right| \lesssim \alpha^2 \cdot \phi^{18} \approx 5 \times 10^{-5} \cdot 5.78 \times 10^3 \approx 0.29 \quad \text{[Tier 3 upper bound]}.$$

This is the loosest possible bound — and even at this loose bound, the sign of the correction is the open question. Without an explicit derivation of $c$ from the icosahedral self-energy graph topology, the sign is undetermined; without sign, "Branch 1 saves the prediction" is not falsifiable.

**Two more conservative estimates.**

- *Conservative bound: $X = 8$ (the muon's exponent).* Relative shift $\lesssim \phi^8 \alpha^2 \approx 0.0024$. This shifts $\Sigma m_\nu$ by at most $0.0002$ eV — insufficient by a factor of $\sim 50$ to close the gap to $0.072$ eV.
- *Conservative bound: $X = 0$ (no phason enhancement, pure $\alpha^2$).* Relative shift $\lesssim \alpha^2 \approx 5 \times 10^{-5}$. Shift $\lesssim 4 \times 10^{-6}$ eV — three orders of magnitude too small.

The loose bound $\phi^{18} \alpha^2 \approx 0.29$ is structurally implausible (it would represent a 29% correction to a tree-level result, the opposite of how loop expansions usually behave). The realistic regime $\phi^{8} \alpha^2 \to \alpha^2$ closes the gap by at most $0.5\%$ to $5 \times 10^{-3}\%$.

**Branch 1 conclusion [structurally negative, Tier 2].** A muon-analogue 2nd-order phason self-energy is structurally insufficient to lower $\Sigma m_\nu$ below the $\Lambda$CDM threshold. The mechanism's natural magnitude is two to three orders of magnitude too small. The bare $\phi^{-36}$ prediction is rigid; any survival path must come from elsewhere. Branch 1 is therefore documented and closed as a non-viable closure direction.

The rigidity itself is informative: it means $\Sigma m_\nu = 0.0853$ eV is a load-bearing prediction of the icosahedral mass spectrum, not a fittable target. Either the data accommodates it (via Branch 2) or the theory falls on this point (Branch 3).

### NS.3 Branch 2 — Coupled prediction under GCT biogenic dark-energy cosmology

**The structural claim.** The Planck+DESI 2024 $\Sigma m_\nu \lesssim 0.072$ eV bound is derived under the cosmological model $w(z) = -1$ exactly at all redshifts ($\Lambda$CDM). The GCT single-channel curve is phantom across all scanned redshifts ($w(z) \leq -1$ for all $z$ in the scan window). DESI 2024/DR2 CPL fits prefer the sign-opposite quadrant $(w_0 > -1, w_a < 0)$ — quintessence today with a more-phantom-in-the-past trajectory. The DESI-preferred dynamical-DE direction is therefore not a data driver for the GCT phantom branch; it is an external tension registered as Open Problem O.13 closure-path C1, requiring a GCT-native CMB+BAO+LSS likelihood to determine whether any multi-channel reweighting can fit the DESI quadrant. Generic $w_0w_a$ neutrino-mass-bound relaxation cannot be imported into the GCT prior without that native likelihood; the $\Sigma m_\nu$ tension is therefore an active tension, not a "currently consistent" survival branch.

**The well-known degeneracy.** In the linear regime, the CMB constrains the integrated late-time geometry through the angular acoustic scale $\theta_*$ and the BAO scale $r_d D_V(z)$. Both depend on $\int_0^z dz' / H(z')$, which in turn depends on the dark-energy equation of state. A more negative $w$ at low $z$ accelerates the expansion, lowering $H_0$-equivalent late-time distances; the data can absorb a higher $\Sigma m_\nu$ as compensation. Quantitatively, the Σm_ν posterior under standard CPL parameterisation $w(a) = w_0 + w_a(1-a)$ widens by a factor of $\sim 1.5$–$2$ relative to $\Lambda$CDM in Planck + BAO + SN fits when $w_0$ and $w_a$ are jointly free (DESI Y1 2024; Chen+ 2025; Planck 2018 §6) [Tier 3 — citation chain to cosmology literature, not GCT-internal].

**Specifically for GCT's $w(z)$.** GCT does not predict a free $(w_0, w_a)$ — it predicts a specific continuous-phantom trajectory with $w(z) \leq -1$ across the low-redshift scan window, asymptoting to $-1$ from below, and with the principled Class-2 envelope $|\Delta w(z=0.28)| \in [2,5]\times10^{-5}$ under the current Ch14/O.13 closure discipline. Plugging this $w(z)$ into a CMB+BAO+SN+LSS likelihood (rather than CPL) should give a $\Sigma m_\nu$ posterior close to the DESI DR2 $\Lambda$CDM-context value, approximately $0.064$ eV, because the registered GCT dark-energy amplitude is too small and sign-opposite to import the generic CPL relaxation. The exact posterior is not available until the native likelihood is run.

**Quantitative status [Tier 3 — pending full likelihood re-run].** A generic $w_0w_a$ relaxation cannot be imported as a GCT-native posterior because the GCT biogenic $w(z)$ prior is sign-opposite to the DESI-preferred dynamical-DE quadrant. The 0.0853 eV floor therefore remains in tension with the DESI DR2 $\Lambda$CDM bound, and the GCT-native likelihood path is expected to return $\approx0.064$ eV rather than $0.0853$ eV. A first-principles assessment still requires implementing GCT's $w(z)$ in a modified Boltzmann code (CLASS or CAMB extension) and re-running the full CMB+BAO+SN+LSS likelihood. This is the explicit research debt of Branch 2 / O.13c.

**The coupling — what it means for falsification.** Under Branch 2, $\Sigma m_\nu = 0.0853$ eV does **not** stand alone. It is bound jointly with the P.6 dark-energy arbitration gate (continuous phantom-phase signature with the Class-2 envelope near $z \approx 0.28$, V3 Ch12). The joint binary gate becomes:

| Euclid DR1 + DESI Y3 finds … | Verdict |
| :--- | :--- |
| $0.10 \leq \Sigma m_\nu \leq 0.15$ eV at $3\sigma$ AND $w < -1$ at low $z$ at $> 3\sigma$ | Both P.4 and P.6 supported; biogenic DE mechanism strongly supported. |
| $\Sigma m_\nu < 0.075$ eV at definitive precision AND $w = -1$ at all $z < 0.5$ at $> 3\sigma$ | Both P.4 and P.6 falsified; jump to Branch 3 falsification protocol. |
| $\Sigma m_\nu < 0.075$ eV at definitive precision AND $w < -1$ at low $z$ at $> 3\sigma$ | Mixed: the phantom-phase signature supports biogenic DE, but $\Sigma m_\nu$ falls. Either (a) the $\phi^{-36}$ suppression mechanism is wrong, or (b) the coupling between $w(z)$ and $\Sigma m_\nu$ is not as the Branch 2 estimate above. Requires structural rework of Ch09. |
| $0.10 \leq \Sigma m_\nu \leq 0.15$ eV at $3\sigma$ AND $w = -1$ at all $z < 0.5$ at $> 3\sigma$ | $\Sigma m_\nu$ survives but biogenic DE is falsified. The Cosmological Entanglement Theorem (Ch09 §9.3.4) loses its central premise; that section requires rework but the prediction itself stands. |
| $\Sigma m_\nu >0.15$ eV at definitive precision | P.4 upper exclusion fires; the registered absolute-scale floor is wrong on the high-mass side and Ch09 must be reopened independently of any survival of the dark-energy channel. |

This is the explicit statement of the Cosmological Entanglement Theorem (§9.3.4), made falsifiable: the discrete mass spectrum and the dynamic vacuum are *jointly* the GCT cosmological claim, and they live or die together in the (++) and (--) cells of this table.

**Branch 2 status [Tier 3].** The coupled prediction is an active tension pending a GCT-native cosmology likelihood. Published generic CPL-prior relaxations are not imported as GCT support because the DESI-preferred quadrant is sign-opposite to the GCT single-channel branch. Branch 2 is a calculation path, not current survival evidence: the registered GCT $w(z)$ amplitude points toward a native bound near $0.064$ eV. It does not dissolve the falsification risk; it defines the calculation required to adjudicate it.

### NS.4 Branch 3 — Falsification Protocol (Pre-registered)

If Euclid DR1-class cosmology confirms $\Sigma m_\nu < 0.075$ eV at definitive precision AND DESI Y3 separately confirms $w = -1$ at all $z < 0.5$ at $> 3\sigma$ — the (-/-) cell of the NS.3 table — the following sections of the manuscript are **falsified** and must be retracted:

**Falsified results:**

- **V3 Ch09 §9.3.1 Theorem 9.1** — the $\phi^{-36}$ second-order phason coupling mechanism. The specific mass floor $m_{\nu_1} = m_e \cdot \phi^{-36} = 0.0153$ eV does not survive.
- **V3 Ch09 §9.3.4 Cosmological Entanglement Theorem** — the "tension is a foundational confirmation" framing collapses. The discrete mass spectrum and dynamic vacuum stand or fall independently under the contingency data.
- **V3 Ch09 §9.6.1 "$0.015$ eV Floor"** prediction for next-stage KATRIN operations / Project 8.
- **V3 Ch09 §9.6.2 "$\Sigma m_\nu \approx 0.0853$ eV"** primary falsification vector — falsified by definition.
- **App V row P.4** — neutrino floor prediction.
- **V3 Ch19 Protocol G** — the mechanical proof programme for the $\phi^{-36}$ eigenvalue becomes a forensic post-mortem of why the suppression mechanism failed.

**Sections requiring partial rework:**

- **V3 Ch09 §9.2.2 Geometric See-Saw** — the identification of "squared phason stiffness" with the neutrino-mass mechanism is what fails. The mathematical mechanism may survive with a different exponent (not $\phi^{-36}$) if a structural re-derivation lands on a different suppression power.
- **V3 Ch09 §9.2.3 $E_6$ Geometric See-Saw** — Theorem 9.2 numerics (consistent with Theorem 9.1) become inconsistent and must be redone.
- **V2 Ch14 §14.2 Biogenic Dark Energy** — only IF DESI Y3 also rejects the phantom-phase signature (cell --, the joint-falsification case). If $w < -1$ is confirmed but $\Sigma m_\nu$ falls, biogenic DE survives the cosmology test but loses its V3 Ch09 anchor.

**Results that survive unaffected (orthogonal mechanisms):**

- **Lepton mass ratios** $m_\mu/m_e = \phi^{11} \cdot (1 + \phi^8 \alpha^2)$, $m_\tau/m_e = \phi^{17} \cdot (1 - 3.6\alpha)$ — independent of the neutrino mechanism. The 21 ppm (Muon, PDG 2024) / 51 ppm (Tau, PDG 2024) precision stands.
- **Fine-structure constant** $\alpha^{-1} = 360 \phi^{-2}$ — gauge sector, no overlap.
- **Weinberg angle** $\sin^2 \theta_W^{bare} = \phi^{-3}$ — electroweak gauge sector.
- **Quark masses** $m_u, m_s, m_b, m_t$ at Tier 2 — strong sector, orthogonal.
- **Down-quark Fuglede–Kadison mechanism** (current $R=2$ baseline tension; $R=4$ primary-output update path via App TP §TP-B) — orthogonal.
- **Proton mass** $m_p = m_e \phi^{15+\phi^{-1}}$ at $\sim0.015\%$ — hadron sector, orthogonal.
- **Newton's $G$** via Jacobson chain (2274 ppm) — gravity sector, cascades from $m_e$ not from neutrino mechanism.
- **$\alpha_s$ bare $= 10\phi^2$** (TP-C per-factor trace documented; product remains a Tier 3 calibrated handle pending O.42 / QLQCD-2) — strong coupling, orthogonal.
- **$\sin^2 \theta_W(M_{GUT}) = \phi^{-2}$** (TIER1_EXACT via Gram Projection Theorem) — unconditionally exact.
- **All Tier 1 structural results** — Wheeler-DeWitt nullity, photon masslessness via Maxwell/residual-$U(1)$ gauge protection, dimensionality $D=3,D=6$ from knot stability — these are axiom-level or theorem-level and do not touch the neutrino mechanism; the Standard-Model spectral-triple identification remains conditional on O.32.
- **CP-violating phase $\delta_{CP} = 360^\circ \cdot \phi^{-1}$** — derived from the Jarlskog volume; independent of $\Sigma m_\nu$.
- **Electron EDM prediction** $d_e \lesssim 10^{-29} e \cdot \text{cm}$ (Ch09 §9.6.3) — derived from $\delta_{CP}$ and the 2-loop electroweak structure, not from $\phi^{-36}$. Survives.

**Post-falsification structural story.** If Branch 3 fires, GCT remains a 5-postulate-plus-1-anchor bare gauge+charged-lepton-ratio sub-sector, expanding to 5-postulate-plus-3-anchor when native-RGE endpoint and measurement-anchored precision-comparison rows are included, plus a Tier 2 area-law mechanism for the cosmological-constant sector whose absolute magnitude remains Tier 3/calibration-imported (V2 Ch14 §14.1.5). The neutrino *absolute* scale becomes a Tier 3 Open Problem alongside the Higgs absolute scale and the dark-energy dynamics. The framework's overall epistemic posture downgrades from "1-DOF closure of the dimensional mass scale" to "1-DOF closure of the charged-lepton dimensional mass scale" — a real loss, but not a structural collapse.

The retraction text for §9.3.1 / §9.3.4 / §9.6.2 is specified by this appendix's decision matrix; no additional narrative discretion is intended at adjudication time.

### NS.5 Decision matrix

| Outcome (Euclid DR1 + DESI Y3) | Action |
| :--- | :--- |
| $0.10 \leq \Sigma m_\nu \leq 0.15$ eV & $w < -1$ at low $z$ ($> 3\sigma$ each) | NS.3 supported. Promote $\Sigma m_\nu$ from Tier 2 to Tier 2-Validated; promote the phantom-phase signature from Tier 3 to Tier 2-Validated; promote Cosmological Entanglement Theorem from "framework hypothesis" to "empirical validation." |
| $0.05 \leq \Sigma m_\nu < 0.10$ eV at definitive precision | NS.5 boundary outcome: values below $0.075$ eV fire the lower P.4 exclusion boundary; values in $[0.075,0.10)$ leave P.4 in severe tension but below the survival-promotion band, requiring the GCT-native likelihood and Ch09/App V disposition update before any support claim. |
| $\Sigma m_\nu < 0.075$ eV at definitive precision & $w = -1$ at all $z < 0.5$ ($> 3\sigma$) | NS.4 fires. Execute Branch 3 retraction protocol. |
| $\Sigma m_\nu < 0.075$ eV at definitive precision & $w < -1$ at low $z$ ($> 3\sigma$) | Mixed; structural rework of Ch09 + retention of Ch14 biogenic DE. $\Sigma m_\nu$ mechanism reopened; cosmological mechanism stands. |
| $0.10 \leq \Sigma m_\nu \leq 0.15$ eV & $w = -1$ at all $z < 0.5$ ($> 3\sigma$) | Mixed; $\Sigma m_\nu$ survives, Ch14 §14.2 biogenic DE falsified. The Cosmological Entanglement Theorem (§9.3.4) loses its physical anchor and is retracted; the $\phi^{-36}$ mechanism stands on its own without the cosmological framing. |
| $\Sigma m_\nu >0.15$ eV at definitive precision | Upper-band P.4 exclusion; reopen the absolute neutrino-scale mechanism regardless of the P.6 verdict. |
| Neither bound nor crossing established at decisive precision | Prediction remains active in tension; await the registered cosmology and direct-mass programs. |

### NS.6 Cross-references and registry updates

This appendix:

- *consumes* V3 Ch09 (Theorems 9.1, 9.2 and §9.3.4), V2 Ch14 (§14.1, §14.2), V3 Ch12 (Dynamic Dark Energy), V3 Ch19 (Protocol G), V3 Ch22 §22.1.4 (binary gates).
- *updates* App V row P.4 (cross-reference to NS.5 decision matrix) and App V row P.6 (coupling to P.4 made explicit).
- *informs* the App FM Falsifiability Matrix row for P.4 (the `linked_roadmap_id: E.1` entry now resolves to this appendix).
- *replaces* the implicit Ch09 §9.3.4 framing ("not a tension, but a foundational confirmation") with the explicit NS.3 conditional. The §9.3.4 wording remains in V3 Ch09 but cross-references NS for the falsifiability protocol.

**End of Appendix NS.**
