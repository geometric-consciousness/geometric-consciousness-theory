### **Appendix TPR: Tier Promotion Roadmap**

### TPR.1 Purpose

Tier 0 contains only the first-person datum that experience is occurring, neither postulated nor derived. No other claim may enter Tier 0, and it is not a destination for tier promotion. Axiom 1 remains its stipulated universal Level I generalisation at Tier 1; no Level II substrate verdict follows.

The Epistemic Tier System in the Global Front Matter runs from Tier 0 to Tier 4; Tier 0 holds only the first-person datum, so every quantitative GCT claim falls in Tier 1 (axiomatic / mathematically forced) through Tier 4 (speculative extrapolation). Some Tier 2 or Tier 3 claims have bounded tests, but no finite computation by itself promotes a GCT identification to Tier 1. This appendix inventories candidate work and distinguishes standard mathematical subidentities from GCT-specific identifications, operator/domain construction, experimental validation, and open-ended theoretical closure.

This appendix is deliberately scoped: it enumerates *promotion candidates* and does not execute the promotions. Closure follows the priority ordering in §TPR.6.

### TPR.2 Classification Scheme

Each candidate is tagged on three axes:

- **Promotion** — current tier → target tier (e.g. T3 → T2, T2 → T1)
- **Closure type** — what kind of work would close the gap:
 - *Code-bounded* — a finite computation within the existing engine framework
 - *Math-bounded* — a bounded analytic step citing published literature
 - *Experiment-bounded* — requires laboratory data the manuscript cannot supply
 - *Open-research* — a major open conjecture in theoretical physics; closure is a research programme, not a bounded computation
- **Tractability** — high / medium / low, reflecting how completely the required step is specified by existing results

### TPR.3 Tier 3 → Tier 2 Promotion Candidates (Mixed Tractability)

This section contains five mixed-tractability entries: TP-B and TP-C are high-tractability; TP-D is a completed diagnostic whose closure is low-tractability (it lives upstream at $m_e$); TP-E is medium-tractability; and TP-A is a related negative result whose remaining closure path is long-horizon. The common placement keeps the gauge-flow analyses adjacent; it does not assign one tractability class to all five entries.

#### TP-A: $Z_3 = 7/10$ closed-form derivation — **NEGATIVE**

**Status.** The conjecture cannot be closed by character-theoretic work alone. The factor 10 in the denominator is a substrate count (the number of three-fold rotation axes of the rhombic triacontahedron, Tier 1 via V3 §3.1.2; its use as the SU(3) sector weight is a Tier 3 assignment, App GRF §GRF.2.3), but the factor 7 in the numerator is *imported* from the SM target $b_3^{\rm SM}({\rm full}) = -(11/3)C_2(\mathfrak{su}_3) + (4/3)n_f T_R = -11 + 4 = -7$ ($|b_3^{\rm SM}| = 7$). The number 7 has **no GCT-native origin in icosahedral group theory** — it is not a divisor of $|I_h|=120$, not a Coxeter degree of $H_3 \in \{2,6,10\}$ or $H_4 \in \{2,12,20,30\}$, not an irrep dimension or face/vertex/edge count of the RT, and does not appear as a natural quotient in any of the $H_4$-order families surveyed.

The "$Z_3 = 7/10$" form is therefore a **calibration**, not a closed-form prediction: it follows from imposing $b_3^{\rm GCT}(T_{\rm GUT}) = b_3^{\rm SM}({\rm full}) = -7$ and dividing by the geometric weight sum $\sum_\rho d_\rho^2 \cdot (10/120) = 10$. Promoting it to a substrate-derived Tier 2 result requires computing the phason loop contribution to $\alpha_s$ running directly — i.e., the QLQCD-2 program of App QLA.7.

**Disposition.** TP-A is long-horizon and bundled with App ORQ §ORQ.5 Open Problem O.5 (QLQCD-1L) and App QLA §QLA.7 (QLQCD-2). It remains adjacent to the gauge-flow candidates here, but is not one of the high-tractability entries. App GRF §GRF.3.1 gives the calibration-not-derivation reading.

**Where the analysis lives**: App GRF §GRF.3.1 ("Scope reading of $Z_3 = 7/10$") + §GRF.5.1 + §GRF.6 summary table.

#### TP-B: Finite-size scaling of the FK determinant for $m_d$ — **Tier 2 mechanism with primary $\phi^{\phi}$ output**

**Status.** Three independent findings emerge:

1. **FK definition.** The load-bearing quantity is the pseudo-determinant $\det_{FK}(A) = \exp\!\bigl((1/N)\sum_i \log|\lambda_i|\bigr)$ over the non-zero eigenvalues stated in V3 Ch10, not a spectral-gap ratio shortcut. Normalising by the number of non-zero eigenvalues is an ad hoc choice: Lück's (2002) von-Neumann-trace normalisation of the Fuglede–Kadison determinant gives ≈1.751 on the $R=2$ cage.

2. **Determinant evaluation.** The geometric mean over the non-zero eigenvalues gives a closed-form value at the $R=2$ cage. The 100 non-zero eigenvalues factor cleanly into icosahedral characters with multiplicities $\{\sqrt 2{:}6,\,\phi{:}24,\,\phi\sqrt 2{:}44,\,\phi\sqrt 3{:}8,\,2\phi{:}10,\,\phi^2\sqrt 2{:}6,\,\phi\sqrt 6{:}2\}$, and the geometric mean evaluates exactly to
$$\det_{FK}(D_F^{R=2}) = \phi \cdot 2^{39/100} \cdot 3^{5/100} = 2.239987\ldots$$
giving a finite-cage branch value $m_d = 4.849$ MeV. The primary output adopts the FK-determinant infinite-volume-limit closed form
$$m_d = m_u \phi^{\phi} = 4.716~{\rm MeV},$$
which is postdiction-consistent at $+0.33\%$ inside the registered 11% shell-resonance gate (Tier 4 as evidence: not distinguishable from numerology for strong effects; App PSC §PSC.9.6). On the $R=4$ lattice, $\det_{FK}$ oscillates across natural icosahedral shells at $N \in \{1416, 1626, 1686, 1866, 2046, 2178, 2418, 2988\}$ in the range $[2.105, 2.391]$ (envelope **$+11\%/-3\%$**, 1$\sigma$ band $\pm 5\%$) with median $\approx 2.18$ — within 1% of the Mixed-Harmonic Area Law heuristic $\phi^{\phi}=2.1785$. The $I_h$-closed orbit-union cage sequence in `protocol_md_fk_ih_closed_cages.py` gives the principled aggregate: deep-tail ($N \ge 2000$, 17 cages) mean signed error vs PDG = **$+0.09\%$**, with mean $\det_{FK}/\phi^{\phi}=0.9976$ and sample std $0.0253$.

2b. **Bellissard claim — clarification.** The FK output does *not* automatically lie in the Bellissard K-theoretic module $\mathbb{Z}[\phi]$, but the two relevant quantities fail to lie in it for *different* reasons. The exact finite-cage ($R{=}2$) branch value $\phi \cdot 2^{39/100} \cdot 3^{5/100}$ is **algebraic over $\mathbb{Q}$ of degree $200$**: the rational powers $2^{39/100}$ and $3^{1/20}$ are roots of $x^{100}-2^{39}$ and $x^{20}-3$ (irreducible by Capelli / Eisenstein), and the tower law over $\mathbb{Q}(\phi)$ gives degree $2 \times 100 = 200$, so it lies outside the degree-$2$ field $\mathbb{Z}[\phi]$ by its algebraic degree, **not** by transcendence. The asymptotic infinite-volume candidate $\phi^{\phi}$ *is* transcendental (Gelfond–Schneider: algebraic base $\phi \neq 0,1$, algebraic-irrational exponent), hence outside $\mathbb{Z}[\phi]$ — indeed outside every algebraic-number module. Neither lies in $\mathbb{Z}[\phi]$, but the finite-cage value is high-degree algebraic while the asymptotic value is transcendental. This does not falsify the numerical closure (which holds within PDG uncertainty) — it corrects *which kind of number* the FK determinant produces. Lück's FK determinant is a multiplicative spectral invariant distinct from the additive $K_0$-class of Bellissard gap labels (those apply to spectral *projections*, not full-spectrum determinants). The algebraic-field structure of the asymptotic $\det_{FK}$ is an Open Problem bundled with App ORQ O.5 (engine: `GCT_Physics_Engine/src/protocol_w5_phiphi_field.py`).

3. **Cage geometry status.** The "$N=144$ cage" is an artefact of the $R=2$, $\mathrm{perp\_cutoff}=2.0$ lattice truncation, not a closed icosahedral shell. On the $R=4$ lattice, the corresponding $|x_\perp| \le 0.46$ shell contains 634 nodes (only 54 of the 144 $R=2$ nodes overlap). The promotion is robust under this refinement at the sequence-mean level: the FK definition tracks the $m_d$ target across both cage geometries, while single-cage values continue to oscillate.

**Disposition.** $m_d$ is a **Tier 2 mechanism with a primary $\phi^{\phi}$ output**: the primary engine source adopts $m_d = m_u \phi^{\phi}$ as the FK-determinant infinite-volume-limit closed form. The row is postdiction-consistent at $+0.33\%$ conditional on O.5. On the $R=4$ lattice the value oscillates with median $\approx \phi^{\phi}$ and 1$\sigma$ band $\pm 5\%$; the $I_h$-closed deep-tail mean supports the $\phi^{\phi}$ candidate at the sequence-mean level, not as a uniform single-cage $\pm 3\%$ closure. The shell-resonance oscillation is a Tier 3 engine diagnostic of finite cages, not a physical prediction. The rigorous convergence proof and **algebraic-field identification** of $\det_{FK}$ in the continuum limit (whether it equals $\phi^{\phi}$ exactly or only its median tracks it; how this relates, if at all, to the Bellissard $\mathbb{Z}[\phi]$ gap-label module) remain **Tier 3 / Open** — bundled with App ORQ O.5. As evidence that φ or icosahedral structure is special, this match is **Tier 4**: the preregistered constant control test (v3, NEGATIVE-FRAGILE; App PSC §PSC.9.6) found φ's pattern of matches on 21 constants not distinguishable from that of random constants (58 of 300 random bases did at least as well). The test "excludes, at power ≥ 0.8, an effect in which φ hits at least 6 of the 8 informative rows through a real effect; weaker effects are not excluded." The number is kept as descriptive arithmetic.

**Separate finding (not closure).** The charm-quark line `m_c = m_u * fk_det_charm**2`, with `fk_det_charm = fk_det * (target_charm_sqrt / fk_det)`, algebraically forces `fk_det_charm = target_charm_sqrt`. This is a heuristic $\phi^{13+\phi^{-3}}$ target rather than a K-theoretic gap-label derivation. Per Ch10's $N=17$ second-harmonic framing, $m_c$ requires a separate gap-label analysis (App ORQ Open Problem O.5; bundled with §TP-F). **$m_c$ stays Tier 3**.

**Falsification.** If a re-derivation of the FK determinant under the Connes–Bellissard noncommutative-integration formalism returns a value outside $[\phi^{\phi/2},\, \phi^{3\phi/2}] \approx [1.48,\, 3.22]$ in the continuum limit of the icosahedral cage, the structural identification $m_d = m_u \cdot \det_{FK}$ is falsified. The finite-cage oscillation (envelope $+11\%/-3\%$, 1$\sigma$ band $\pm5\%$ across $N \gtrsim 1400$) is a property of the engine's cage sequence; it has no established counterpart in lattice-QCD finite-volume effects.

- **Disposition**: down-quark mass Tier 2 mechanism with primary output $m_d = m_u \phi^{\phi}$; postdiction-consistent at $+0.33\%$ conditional on O.5 (**Tier 4 as evidence**; App PSC §PSC.9.6), with shell-resonance oscillation disclosure retained.
- **Open dependency**: charm-quark mass (Tier 3, awaiting K-theoretic gap label for $N=17$ mode — bundled with §TP-F + App ORQ O.5).
- **Where it lives**: `GCT_Physics_Engine/src/gct_spectrum.py` (FK determinant definition), `protocol_quark_mismatch.py` (primary consumer), `protocol_quark_mismatch_scaling.py` (finite-size scaling), `protocol_md_fk_ih_closed_cages.py` ($I_h$-closed orbit-union cage sequence), `data/fk_scaling.json` (scaling table), `data/protocol_md_fk_ih_closed_cages_results.json` (closed-cage sequence table), V3 Ch10 §10.4 (FK definition and $m_c$ status).

#### TP-C: $\alpha_s$ bare prefactor 10 trace — **PER-FACTOR TRACE CLOSED; PRODUCT REMAINS TIER 3 HANDLE**

**Factor status.** The factorisation $\alpha_s^{-1}({\rm bare}) = 10\phi^2$ has per-factor anchors through the manuscript at the per-factor level. The factors have geometric anchors, but the product is not promoted to a Tier 2 physical prediction: the area-law multiplication and the strong-sector matching to a bare SU(3) boundary remain a Tier 3 calibrated handle pending O.42 / QLQCD-2 closure.

| Factor | Origin | Tier | Anchor |
| :--- | :--- | :--- | :--- |
| **10** | Count of three-fold rotation axes of the rhombic triacontahedron (RT) acceptance window. Conditional on the RT/AKN substrate, this is the Tier 1 axis inventory used in the color construction: the traceless seeds span five dimensions and close to an eight-dimensional algebra with an $A_2$ fingerprint. Generic ten-axis sets close the same way, so the construction supports only an open Tier 3 $\mathfrak{su}(3)$ candidate; compact-Lie uniqueness remains O.39. | **Tier 1 inventory; Tier 3 open identification** | V3 §3.1.2 + §3.2.1 |
| **$\phi^2$** | Square of the $H_4$ Cartan/root-metric slope $\phi=2\cos(\pi/5)$, fixed by the pentagonal Cartan entry $-\phi$ and the Lie-algebraic structure of $E_8$ (Humphreys §3.7). The Coxeter-element eigenvalues are unit-modulus roots of unity, not quantities with modulus $\phi$. | **Tier 1** | App USS §USS.7.3 Lemma T-McK.4 |
| **product $10\phi^2$** | Area-law combination: bare inverse coupling = (count of axes) × (area-scaling eigenvalue). | **Tier 3 calibrated handle** + **Tier 4 as evidence** (φ-formula match; App PSC §PSC.9.6) | V3 §4.5.2 + O.42 / QLQCD-2 closure target |

This per-factor decomposition is a substantive tightening of the prior shorthand: $\alpha_s^{-1}({\rm bare}) = 10\phi^2$ is not a single monolithic prediction. The factors are geometrically motivated (10 = three-fold rotation axis count of the RT acceptance window; $\phi^2$ = squared $H_4$ Cartan/root-metric slope factor), while the product-level strong-coupling claim remains Tier 3 until the area-law product and native strong running are derived without the calibrated handle.

- **What closed**: the per-factor trace for $\alpha_s^{-1}({\rm bare})$. The remaining 55.9% endpoint gap of the native run to PDG $\alpha_s(M_Z)$ is QLQCD-2 territory (App QLA.7), and the product-level status is the registered Tier 3 calibrated handle. In the pre-registered gauge-running audit (App GRF §GRF.4.3), run top-down with SM β-functions together with A2 and H-EW, $\alpha_3^{-1}=10\phi^2$ reaches zero at $2$–$6\times10^6$ GeV, so $\alpha_s(M_Z)$ is undefined (non-perturbative); the audit is a **FAILED check** (App GRF §GRF.4.3).
- **Where it lives**: V3 Ch04 §4.5.5 (expanded with the explicit factor-by-factor derivation chain) + App USS §USS.7.3 (Lemma T-McK.4) + V3 §3.1.2 (axis inventory) + §3.2.1.
- **Falsification**: see V3 Ch04 §4.5.5 — note that failure of QLQCD-2 corrections to close the 55.9% endpoint gap would NOT falsify the geometric factor anchors; it would falsify the Tier 3 calibrated strong-sector handle / area-law combination rule of §4.5.2.

#### TP-D: Newton's $G$ residual structure — **DIAGNOSTIC COMPLETE / UPSTREAM-CASCADED**

**Cascade structure.** The model-authoritative branch uses $\alpha_{\rm GCT}=\phi^2/360$ with CODATA $m_e$ and exact SI $h,c$, giving $G=6.689475523\times10^{-11}$ and a 2273.725 ppm residual (display 2274 ppm). The separate all-CODATA-$\alpha$ sensitivity branch gives 2013.345 ppm, consistent with mapping the 1006.166 ppm electron residual through $G\propto m_e^{-2}$ (2012.332 ppm at leading order plus the quadratic term). The $G$ row is therefore the electron Planck-link row inverted: it is not independent evidence and is not counted as a pass while the electron row fails its pre-committed 1000 ppm rule; like the electron row it is Tier 4 as evidence (App PSC §PSC.9.6). The 260.380 ppm difference between branches is caused by $\alpha_{\rm CODATA}\to\alpha_{\rm GCT}$ in $(1-5\alpha)^2$; there are no finite-precision uncertainty terms from $\hbar$ or $c$ because $h$ and $c$ are exact in the post-2019 SI.

**Muon-analogue 2nd-order pathway is structurally insufficient.** Adding the muon-analogue 2nd-order $\alpha^2$ correction to the electron mass formula yields a negligible contribution: per V3 §8.2.3, the muon's coefficient $\phi^8 = \phi^{-3} \times \phi^{11}_{\text{bare-muon-exp}}$. Substituting the electron's bare exponent ($-107$) into the same combination rule gives $\phi^{-3} \times \phi^{-107} = \phi^{-110} \approx 1.0 \times 10^{-23}$, contributing $\phi^{-110} \cdot \alpha^2 \approx 5.5 \times 10^{-28}$ to $m_e$ — **totally negligible** relative to the 1006 ppm residual. The 2nd-order phason self-energy by the muon-analogue mechanism therefore does NOT close the electron / $G$ residuals.

**Closure paths.** None is high-tractability. The 1006 ppm electron residual most plausibly closes through:

1. **Conditional APS programme on $\partial\mathcal{M}_{\text{RT}}$** — first specify a qualifying boundary operator and domain, then evaluate the corresponding APS invariant/index. The existing weighted-adjacency sign count is only a finite diagnostic and does not close $\alpha$'s residual.
2. **Higher-order non-perturbative corrections** to the discrete RT lattice mass formula beyond tree-level $(1-5\alpha)$ — would require a dedicated 1-loop computation of the electron mass on the cage (analogous to the muon's §8.2.3 but for the ground-state defect rather than the 11th harmonic).
3. **Refinement of the Tier 3 $M_P$ convention** — V3 §7.2.2 flags the $\sqrt{\hbar c / G_N}$ vs $\sqrt{\hbar c / 8\pi G_N}$ choice as a Tier 3 phenomenological selection. A first-principles derivation here would change the absolute scale.

**Status.** The $G$ residual is upstream-cascaded from the electron mass residual; a tighter $G$ requires upstream work on $m_e$, not direct work on the gravitational derivation chain. The diagnostic chain is complete.

- **Where it lives**: V2 Ch09 §9.1.5 (cascade structure callout) + App PSC §PSC.1 row 1 (electron) + this entry.
- **Closure path**: a separate O.14 operator/domain/index construction, followed by any justified connection to the mass normalization; no promotion follows from the present finite diagnostic.

#### TP-E: Higgs VEV 1.6% radiative-correction closure [Closure: math-bounded + code-bounded; Tractability: medium]

App PSC §PSC.2 reports an **OPEN-CONDITIONAL** Higgs VEV evaluation $v_{\rm pred}=246.1755$ GeV versus the sole declared PDG-2024 anchor $v=246.21965$ GeV. Its Tier 2 product arithmetic applies only after supplying the Tier 3 O.38 $N_{\rm cage}=144$ posit; O.20 enumerates but does not select the $144\times10$ branch. The approximately 179 ppm comparison is conditional, not an absolute or geometric closure (Tier 4 as evidence: not distinguishable from numerology for strong effects; App PSC §PSC.9.6). Separately, the bare Higgs mass $m_H^{\rm bare}=v_{\rm GCT}/2=123.09$ GeV (123.11 GeV with the measured $v$) lies 1.69% below the PDG 2024 value $125.20\pm0.11$ GeV; a 1-loop GCT spectral computation would test that distinct radiative-correction closure.

- **What closes**: $m_H^{\rm bare}$ Tier 3 → Tier 2 (or reveals a structural revision)
- **Where it lives**: V3 Ch04 Higgs sector + new section under `protocol_higgs_vev.py`

### TPR.4 Tier 3 → Tier 2 Promotion Candidates (Medium Tractability)

These candidates have a clear closure path but require either substantial mathematical machinery or are harder than the §TPR.3 items.

#### TP-F: CKM $s_{23}, s_{13}$ from K-theoretic gap labels [Closure: gap-label route ruled out as a standalone path; residual bundles with O.5]

V3 Ch10 carries the four irrational-exponent quark formulas ($m_d, m_c, s_{23}, s_{13}$) as Tier 3 ansätze; the down-quark and charm-quark routes are addressed by TP-B (finite-size FK scaling). For the CKM angles $s_{23} = \phi^{-(6 + \phi^{-1})}$ and $s_{13} = \phi^{-(11 + \phi^{-1})}$, the K-theoretic gap-label audit (engine: `GCT_Physics_Engine/src/protocol_tpf_ckm_gap_labels.py`) enumerates the Bellissard $\mathbb{Z}[\phi]$ trace-image labels $L(p,q) = (p\,\phi^{-1} + q)\bmod 1$ (App USS §USS.7.6) against the observed magnitudes and establishes that this route does not close them: (i) neither observed value lies on an integer-power label $\phi^{-n}$ — both fall strictly between consecutive powers ($n_{\rm obs} \approx 6.60$ for $s_{23}$, $11.62$ for $s_{13}$, each $\gtrsim 17\%$ from the nearer power); (ii) a general $\mathbb{Z}[\phi]$ label matches the observed magnitudes only at $|p| \approx 42$ ($s_{23}$) and $|p| \approx 466$ ($s_{13}$), far beyond the validated/accessible range ($|p| \le 7$ at the 1D Fibonacci scale $F_{15} = 610$), and — because $\{p\,\phi^{-1}\bmod 1\}$ is equidistributed — multiple labels co-fit at that scale with no selection rule, the same under-determination as the open $-107$ uniqueness (O.14a); and (iii) the literal ansätze carry irrational algebraic exponents, so by the Gelfond-Schneider theorem they are transcendental and lie outside $\mathbb{Z}[\phi]$ — indeed outside any algebraic-number K-theory trace module, a convention-independent exclusion. A richer 6D AKN $K_0$ trace image than the validated $\mathbb{Z}[\phi]$ core is not excluded in principle, but no such module is supplied, and none can host the transcendental ansätze. The standalone gap-label closure is therefore ruled out; the residual derivation of $s_{23}, s_{13}$ remains with the QLQCD dressed-Dirac extraction (App ORQ Open Problem O.5), where gap labels can at most serve as a downstream consistency check.

- **What closes**: removes the gap-label route as a standalone TP-F closure; sharpens the $s_{23}, s_{13}$ residual to the O.5 dressed-Dirac extraction
- **Where it lives**: V3 Ch10 §10.6 + App ORQ O.5; engine `protocol_tpf_ckm_gap_labels.py`
- **Scope**: standalone gap-label enumeration complete (negative result); full closure bounded by App ORQ O.5 status

#### TP-G: Weinberg raw-frame identity and physical boundary [Closure: raw-frame arithmetic closed; physical boundary open]

App PSC §PSC.2 lists $\sin^2\theta_W^{\rm bare}=\phi^{-3}=0.23607$, 2.1% from $\sin^2\theta_W^{\rm Z\text{-}pole}=0.23122$ (PDG 2026 $\overline{\rm MS}$), as a cross-scale numerical alignment (Tier 4 as evidence: not distinguishable from numerology for strong effects; App PSC §PSC.9.6). App USS §USS.9 gives the exact raw-frame identity $V_{\perp,0}/V_{\parallel,0}=\phi^{-3}$, which is coordinate arithmetic: it changes under row rescaling while the canonical projectors (shares $1/2+1/2$) do not. The physical bare angle is the Tier 3 gauge-kinetic hypothesis H-EW (V3 Ch04 §4.3.2), and the conditioned one-loop comparator from that boundary misses the Z pole by 40.87% (V3 Ch04 §4.3.3). The pre-registered gauge-running audit (App GRF §GRF.4.3) is a **FAILED check**: top-down from {A2 = 24–25, H-EW, $\alpha_3^{-1}=10\phi^2$, $M_{\rm GUT}=3.2\times10^{16}$ GeV} with SM β-functions (1-loop, 2-loop, top-decoupled) it gives $\sin^2\theta_W(M_Z)=0.058$–$0.067$, the best case ($0.0673$) at $-52\sigma$ against $0.23122\pm0.00006$, and $\alpha_s(M_Z)$ undefined; bottom-up, $\sin^2\theta_W$ equals $\phi^{-3}$ only at 243 GeV, and placing H-EW there would be endpoint fitting. Since any matter content containing the SM has $b_Y\ge41/6$, A2 and H-EW cannot both hold for any SM extension (App GRF §GRF.4.3). H-EW remains a Tier 3 hypothesis at an unspecified scale.

- **What closes**: the raw-frame integer-exponent identity only; no physical promotion of H-EW
- **Promotion path**: derive the relative $SU(2)$/$U(1)$ gauge-kinetic coefficients from a normalized 6D action (V3 Ch04 §4.5.4)
- **Where it lives**: V3 Ch04 §4.1–§4.3 + App USS §USS.9

#### TP-H: Inattentional blindness surrogate [Closure: experiment-bounded; Tractability: low]

V1 §16.6 uses attention-vector misalignment with the information gradient as an analogy for inattentional blindness. It is not identical to, or a mechanism for, the empirical phenomenon, so the reading is Tier 4 (it could reach Tier 3 only as an ordinary empirical model). The open question is whether the surrogate $I(X) = \int |F_{\rm sel} \cdot \hat{\bf i}|\, d^3r$ predicts psychophysical thresholds at all. App ORQ Open Problem O.3 lists this as an open research direction. The test requires psychophysics collaboration — not code-only.

- **What closes**: a test of whether the §16.6 surrogate predicts thresholds (Tier 4 → Tier 3 only as an ordinary empirical model)
- **Where it lives**: V1 §16.6 + App ORQ O.3 (already a public Open Problem)
- **Scope**: experiment-bounded; cannot be closed in-manuscript

### TPR.5 Analytic promotion candidates and conditional consistency programmes

This section separates genuine analytic-promotion candidates from downstream consistency programmes. Each entry states whether closure changes an epistemic tier; a successful conditional consistency calculation does not automatically promote the architecture or physical identification that supplies its domain.

#### TP-I: T-McKay downstream operator-consistency programme [Closure: open construction; Tractability: open; Promotion: none automatic]

App USS §USS.7 separates the closed representation-theoretic arrows of the conditional T-McKay architecture from Program T-McK.1b. TP-I is the downstream operator-consistency programme only. No qualifying smooth bulk/boundary operator pair, Hilbert-space domain, boundary conditions, kernel term, reduced invariant, relative-invariant construction, spectral-flow control, or graph-to-smooth comparison theorem is specified. The finite scalar-adjacency and discrete-Dirac sign sums are diagnostics on distinct finite spaces and do not reduce this construction problem.

- **What closes**: a specified smooth Fredholm problem; its boundary operator and domain; kernel and reduced invariant $\xi=\tfrac12(h+\eta)$; any required relative $\rho$-invariant; compatible bulk pairing; spectral-flow/local-variation control; and a proved comparison, if claimed, to the finite graph diagnostics
- **What does not close automatically**: selection of $n=-107$, the cage-selection rule, the 6D parent architecture, or the GCT spin-statistics identification; each requires an independent bridge
- **Where it lives**: App USS §USS.7.6.1–4, with the physical comparison target in V1 Ch15 §15.3.2
- **Scope/status**: open infinite-dimensional operator/domain and comparison construction; successful closure would establish a conditional consistency result on the adopted architecture, not Tier-1 promotion

#### TP-J: Spin-statistics operator/domain comparison programme [Closure: open construction; Tractability: open]

V1 Ch15 §15.3.2 separates the Tier 1 conditional mathematics (the standard $SU(2)$ double-cover rotation control; App CCD §CCD.4) from the GCT spin-statistics identification, which is Tier 3/open (the physical framed-defect premise of App CCD §CCD.4 is not derived). TP-J asks for an independently specified operator, domain, index problem, and comparison map; even a successful result would be a distinct conditional consistency statement rather than an automatic tier promotion.

- **What closes**: a separately stated APS operator/index claim; no automatic Tier 1 promotion of the GCT spin-statistics identification
- **Where it lives**: V1 Ch15 §15.3.2 (cross-reference) + App USS §USS.7.6.1–4 (the open construction programme)
- **Scope**: distinct operator/domain/comparison work; not bundled closure

#### TP-K: Polaron Unity (App PUP) algebraic-status programme [Closure: open construction (physical identification); Tractability: low without substrate data; Promotion: none automatic]

App PUP now records Polaron Unity at its **algebraic status**: Proposition PUP.1(ii) (Hilbert-space non-factorizability) is withdrawn because its tensor-factor-to-direct-product bridge is false; for the trefoil, $\Gamma_\mathcal K=B_3$ has a nontrivial amenable centre, so O.35 is false as posed and the regular $L(B_3)$ is not a factor (O.35/O.36 fail as posed for the represented trefoil group $B_3$ (its centre $\langle\Delta^2\rangle$ makes the amenable radical nontrivial and $L(B_3)$ non-factorial) and hold for the further central quotient $B_3/Z(B_3)\cong C_2*C_3$ [Tier 1 — standard]; whether any physical sector is that quotient's regular representation is open [Tier 3]). What survives is at most an algebraic unity candidate, with no subject count, owner or Level II verdict. The former non-factorizability closure route is retired, and no mathematical result in this entry can promote a unity, subject-count or Level-II claim to Tier 1/2. The remaining work is a physical identification stack, not one more abstract lemma. The superseded trefoil trace computation of §PUP.6.3a is a finite-matrix surrogate only; moreover the finite-level ambient space is $M_n \cong S^1 \times \mathbb{R}^3$, the classical knot-complement product split requires full-fibre supports $\mathscr D_n=X_n\times K_n$ and complement-compatible ambient bonding maps not yet physically derived by the Ch11 ansatz, and the trefoil trace step still requires a faithful represented meridian model or a controlled finite-representation family with convergence and trace descent. The inverse limit of the generally infinite complement groups is a pro-group, not a profinite group absent separately constructed finite completions. Proposition PUP.1(iii) gives a conditional invariant-density statement for $R_{\rm inv}$ only in a factorial sector, whose physical identification is open; it does not make the canonical non-unitary $\mathcal F_{sel}$ unique. The surviving items are the O.18 sub-problems (physical full-fibre support, inverse-limit promotion, the meridian trace/GNS bridge of Lemma PUP.3.4, identification of a physical factorial sector) plus, for the general case, the Anderson-Putnam-to-$S^3 \setminus K$ extension (gap A), canonicity of $K \mapsto \mathcal{A}_K$ (gap B) and support realization (gap C).

- **What closes**: at most the algebraic-unity-candidate statement of App PUP on a physically identified sector; no outcome promotes a Level II, owner or subject-count claim to Tier 1/2, and no Proposition-to-Theorem promotion is scheduled
- **Where it lives**: App PUP Lemma PUP.3.4 (§PUP.3) and §PUP.6 + bibliography §IX (Knot Theory & Operator Algebras)
- **Scope**: open physical-identification construction; low feasibility without substrate data, since the decisive steps are a derived physical sector, representation and coupling rather than a bounded operator-algebra computation

### TPR.6 Promotion Ordering

Bundled by closure type, ordered by tractability and impact:

**Status of the TP-A–TP-D subset of §TPR.3 (two high-tractability, one completed diagnostic and one long-horizon):**

1. **TP-D** Newton's $G$ residual structure — **DIAGNOSTIC COMPLETE.** The all-CODATA-$\alpha$ sensitivity branch carries the doubled 1006.166 ppm electron-anchor residual into 2013.345 ppm in $G$; the model-authoritative $\alpha_{\rm GCT}=\phi^2/360$ branch is 2273.725 ppm, with the additional 260.380 ppm arising from the $\alpha$ substitution. The muon-analogue 2nd-order $\alpha^2$ correction gives a $\phi^{-110}$-suppressed shift to $m_e$ — totally negligible. A dedicated electron 1-loop computation is a direct closure route; the separate O.14 APS programme presently lacks a qualifying operator/domain/index and supplies no residual correction. See §TPR.3 entry.
2. **TP-C** $\alpha_s$ bare prefactor 10 trace — **PER-FACTOR TRACE CLOSED; PRODUCT TIER 3.** The 10 axis count and $\phi^2$ factor are geometrically traced, but the area-law product remains the registered Tier 3 calibrated strong-sector handle pending O.42 / QLQCD-2. See §TPR.3 entry.
3. **TP-B** FK finite-size scaling for $m_d$ — **Tier 2 mechanism; primary $\phi^{\phi}$ output.** The primary engine source adopts $m_d = m_u \phi^{\phi}$ as the FK-determinant infinite-volume-limit closed form, postdiction-consistent at $+0.33\%$ conditional on O.5 (Tier 4 as evidence; App PSC §PSC.9.6). The enlarged $R=4$ lattice oscillates around $\phi^{\phi}$. The $I_h$-closed orbit-union cage sequence in `protocol_md_fk_ih_closed_cages.py` gives deep-tail ($N \ge 2000$, 17 cages) mean $\det_{FK}/\phi^{\phi}=0.9976$ (sample std $0.0253$) and mean signed error vs PDG $+0.09\%$; the closed-cage tail error range is $[-7.20\%, +10.12\%]$, all tail values sit inside the 11% shell-resonance band, and excursions persist at $N=1746$ ($+5.6\%$), $N=1866$ ($+10.1\%$), and $N=2688$ ($+5.4\%$). Rigorous convergence proof and algebraic-field identification of $\det_{FK}$ in the continuum limit remain Tier 3/Open, bundled with O.5. The charm-quark hard-coded heuristic is exposed as Tier 3 awaiting QLQCD-1L gap-label analysis. See §TPR.3 entry.
4. **TP-A** $Z_3 = 7/10$ closed-form derivation — **NEGATIVE — long-horizon (QLQCD-2 dependent).** See §TPR.3 entry for the analysis: the 7 in the numerator has no GCT-native origin in icosahedral group theory; the form is calibration, not closed-form derivation.

**Net summary:** within the four-row TP-A–TP-D subset, TP-B and TP-C are high-tractability and TP-D is a completed diagnostic: TP-B supplies the primary $\phi^{\phi}$ output for $m_d$ conditional on O.5, TP-C closes only the per-factor trace while retaining Tier 3 product status, and TP-D is upstream-cascaded to the electron mass residual (residual lives at $m_e$, not at $G$). TP-A is the subset's long-horizon, QLQCD-2-dependent entry. TP-E, the fifth entry in §TPR.3, is separately classified as medium-tractability. TP-B is particularly substantive as mechanism bookkeeping: $m_d$ matches the Mixed-Harmonic Area Law heuristic $\phi^{\phi}$ at $+0.33\%$ through the primary engine source (a match that is Tier 4 as evidence; App PSC §PSC.9.6), anchored on the pseudo-determinant $\exp((1/N)\sum\log|\lambda_i|)$ over non-zero eigenvalues (an ad hoc normalisation; Lück's von-Neumann-trace normalisation gives ≈1.751 on the $R=2$ cage) rather than a gap-ratio shortcut.

**Candidates requiring a larger mathematical investment:**

5. **TP-I + TP-J** Conditional APS programme — requires a chirality-breaking boundary operator, domain, and justified index problem (App USS §USS.7.6.3); any bearing on T-McKay or spin statistics must then be proved separately
6. **TP-G** Weinberg raw-frame identity — arithmetic closed but coordinate-dependent; the bare angle remains the Tier 3 gauge-kinetic hypothesis H-EW at an unspecified scale (the gauge-running audit is a FAILED check, App GRF §GRF.4.3) and the Z-pole value a Tier 3 comparison target
7. **TP-E** Higgs VEV radiative-correction 1-loop closure — closes on an explicit one-loop evaluation of the registered correction

**Long-horizon (not bounded-pass material; programmatic):**

8. **TP-A** $Z_3$ from first principles — bundled with App ORQ O.5 + App QLA.7 QLQCD-2 (the 7 in the numerator requires direct phason-loop computation; closed-form from icosahedral group theory alone is ruled out by the §TPR.3 audit)
9. **TP-F** CKM $s_{23}, s_{13}$ via K-theoretic gap labels — bundled with App ORQ O.5 (QLQCD-1L)
10. **TP-K** Polaron Unity algebraic-status programme — open physical-identification construction (physical sector, representation and coupling); the abstract programme reaches only the algebraic-unity-candidate ceiling, and the Level II status is open (Tier 3): no validated substrate criterion exists yet (it requires a typed, normalized, measured coupling, the Identity-Polaron construction and an independent phenomenal bridge; O.21/O.23/O.34, O.18)
11. **TP-H** Inattentional-blindness surrogate (Tier 4 analogy) — App ORQ O.3 (experiment-bounded)

### TPR.7 What This Roadmap Does NOT Include

To preserve the boundary between (i) candidates with clear math/code paths and (ii) genuine open research, the following are *excluded* from this roadmap and remain in the **Open Problems** inventory of App ORQ §ORQ.5:

- **O.1 / O.4** Phason mass gap & $H_0$ from lattice dynamics — these are equivalent open problems and constitute the framework's primary cosmological frontier. Closure is a research programme, not a bounded computation.
- **O.5** QLQCD-1L closure — a multi-month lattice-computation programme; TP-F above is a sub-component contribution.
- **O.6** dS/CFT boundary state for $\chi$ — a famous open conjecture in holographic gravity (Strominger 2001 / Maldacena 2003 territory); no tractable closure path.
- **O.2** Mechanical proof of neutrino eigenvalues (Protocol G) — 6D lattice simulation; bounded but compute-intensive and dependent on simulation framework readiness.

### TPR.8 Standard of Promotion

This appendix records what each promotion requires, not a schedule for supplying it. A tier label moves only when the stated work is complete, never on the strength of an intention to do it; a candidate that is not closed is carried at its current tier with the missing step named.
