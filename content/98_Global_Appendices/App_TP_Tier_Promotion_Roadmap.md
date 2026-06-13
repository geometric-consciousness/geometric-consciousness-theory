### **Appendix TP: Tier Promotion Roadmap**

### TP.1 Purpose

The Epistemic Tier System (Frontmatter §01) classifies every quantitative GCT claim into Tier 1 (axiomatic / mathematically forced) through Tier 4 (speculative extrapolation). Many claims currently labelled **Tier 2** or **Tier 3** are not promoted higher not because the structural argument is missing, but because a single bounded analytic step, a finite computation, or a small piece of code remains to be executed. This appendix inventories those promotion candidates and classifies each by the *type* of work required to close it — distinguishing items that can be closed with code and mathematics alone from items that require experimental validation or open-ended theoretical breakthroughs.

This appendix is deliberately scoped: it enumerates *promotion candidates* and does not execute the promotions. Closure follows the priority ordering in §TP.6.

### TP.2 Classification Scheme

Each candidate is tagged on three axes:

- **Promotion** — current tier → target tier (e.g. T3 → T2, T2 → T1)
- **Closure type** — what kind of work would close the gap:
 - *Code-bounded* — a finite computation in the existing GCT_Physics_Engine framework (hours to days of compute / engineering)
 - *Math-bounded* — a bounded analytic step citing published literature (days to weeks of focused mathematical work)
 - *Experiment-bounded* — requires laboratory data the manuscript cannot supply (months to years; collaboration-dependent)
 - *Open-research* — a major open conjecture in theoretical physics; closure is a research programme, not a bounded computation
- **Feasibility** — high / medium / low estimate of the probability that the work as scoped will land within ~2 weeks of focused effort

### TP.3 Tier 3 → Tier 2 Promotion Candidates (High Feasibility)

These are the candidates the math-closure pass identified or implied, where the path to Tier 2 is concretely specified and the work is bounded by either a finite computation or a single math step.

#### TP-A: $Z_3 = 7/10$ closed-form derivation — **NEGATIVE**

**Status.** The conjecture cannot be closed by character-theoretic work alone. The factor 10 in the denominator IS substrate-derived (the count of three-fold rotation axes of the rhombic triacontahedron, Tier 1 via V3 §3.1.2 + §3.2.1 Uniqueness Theorem), but the factor 7 in the numerator is *imported* from the SM target $|b_3^{\rm SM}({\rm full})| = -(11/3)C_2(\mathfrak{su}_3) + (4/3)n_f T_R = -11 + 4 = -7$. The number 7 has **no GCT-native origin in icosahedral group theory** — it is not a divisor of $|I_h|=120$, not a Coxeter degree of $H_3 \in \{2,6,10\}$ or $H_4 \in \{2,12,20,30\}$, not an irrep dimension or face/vertex/edge count of the RT, and does not appear as a natural quotient in any of the $H_4$-order families surveyed.

The "$Z_3 = 7/10$" form is therefore a **calibration**, not a closed-form prediction: it follows from imposing $b_3^{\rm GCT}(T_{\rm GUT}) = b_3^{\rm SM}({\rm full}) = -7$ and dividing by the geometric weight sum $\sum_\rho d_\rho^2 \cdot (10/120) = 10$. Promoting it to a substrate-derived Tier 2 result requires computing the phason loop contribution to $\alpha_s$ running directly — i.e., the QLQCD-2 program of App Z.7.

**Reclassification.** TP-A is moved from this high-feasibility section into §TP.6 long-horizon, bundled with App H §H.5 Open Problem O.5 (QLQCD-1L). App ZN §ZN.3.1 reflects the calibration-not-derivation reading.

**Where the analysis lives**: App ZN §ZN.3.1 ("Scope reading of $Z_3 = 7/10$") + §ZN.5.1 + §ZN.6 summary table.

#### TP-B: Finite-size scaling of the FK determinant for $m_d$ — **Tier 2 mechanism with primary $\phi^{\phi}$ output**

**Status.** Three independent findings emerge:

1. **FK definition.** The load-bearing invariant is the textbook Fuglede–Kadison determinant $\det_{FK}(A) = \exp\!\bigl((1/N)\sum_i \log|\lambda_i|\bigr)$ stated in V3 Ch10 and in Lück (2002) Def 3.11, not a spectral-gap ratio shortcut.

2. **Determinant evaluation.** The textbook geometric mean gives a closed-form value at the $R=2$ cage. The 100 non-zero eigenvalues factor cleanly into icosahedral characters with multiplicities $\{\sqrt 2{:}6,\,\phi{:}24,\,\phi\sqrt 2{:}44,\,\phi\sqrt 3{:}8,\,2\phi{:}10,\,\phi^2\sqrt 2{:}6,\,\phi\sqrt 6{:}2\}$, and the geometric mean evaluates exactly to
$$\det_{FK}(D_F^{R=2}) = \phi \cdot 2^{39/100} \cdot 3^{5/100} = 2.239987\ldots$$
giving a finite-cage branch value $m_d = 4.849$ MeV. The primary output adopts the FK-determinant infinite-volume-limit closed form
$$m_d = m_u \phi^{\phi} = 4.716~{\rm MeV},$$
which is postdiction-consistent at $+0.33\%$ inside the registered 11% shell-resonance gate. On the $R=4$ lattice, $\det_{FK}$ oscillates across natural icosahedral shells at $N \in \{1416, 1626, 1686, 1866, 2046, 2178, 2418, 2988\}$ in the range $[2.105, 2.391]$ (envelope **$+11\%/-3\%$**, 1$\sigma$ band $\pm 5\%$) with median $\approx 2.18$ — within 1% of the Mixed-Harmonic Area Law heuristic $\phi^{\phi}=2.1785$. The I_h-closed orbit-union cage sequence in `protocol_md_fk_ih_closed_cages.py` gives the principled aggregate: deep-tail ($N \ge 2000$, 17 cages) mean signed error vs PDG = **$+0.09\%$**, with mean $\det_{FK}/\phi^{\phi}=0.9976$ and sample std $0.0253$.

2b. **Bellissard claim — clarification.** The FK output does *not* automatically lie in the Bellissard K-theoretic module $\mathbb{Z}[\phi]$, but the two relevant quantities fail to lie in it for *different* reasons. The exact finite-cage ($R{=}2$) branch value $\phi \cdot 2^{39/100} \cdot 3^{5/100}$ is **algebraic over $\mathbb{Q}$ of degree $200$**: the rational powers $2^{39/100}$ and $3^{1/20}$ are roots of $x^{100}-2^{39}$ and $x^{20}-3$ (irreducible by Capelli / Eisenstein), and the tower law over $\mathbb{Q}(\phi)$ gives degree $2 \times 100 = 200$, so it lies outside the degree-$2$ field $\mathbb{Z}[\phi]$ by its algebraic degree, **not** by transcendence. The asymptotic infinite-volume candidate $\phi^{\phi}$ *is* transcendental (Gelfond–Schneider: algebraic base $\phi \neq 0,1$, algebraic-irrational exponent), hence outside $\mathbb{Z}[\phi]$ — indeed outside every algebraic-number module. Neither lies in $\mathbb{Z}[\phi]$, but the finite-cage value is high-degree algebraic while the asymptotic value is transcendental. This does not falsify the numerical closure (which holds within PDG uncertainty) — it corrects *which kind of number* the FK determinant produces. Lück's FK determinant is a multiplicative spectral invariant distinct from the additive $K_0$-class of Bellissard gap labels (those apply to spectral *projections*, not full-spectrum determinants). The algebraic-field structure of the asymptotic $\det_{FK}$ is an Open Problem bundled with App H O.5 (engine: `GCT_Physics_Engine/src/protocol_w5_phiphi_field.py`).

3. **Cage geometry status.** The "$N=144$ cage" is an artefact of the $R=2$, $\mathrm{perp\_cutoff}=2.0$ lattice truncation, not a closed icosahedral shell. On the $R=4$ lattice, the corresponding $|x_\perp| \le 0.46$ shell contains 634 nodes (only 54 of the 144 $R=2$ nodes overlap). The promotion is robust under this refinement at the sequence-mean level: the FK definition tracks the $m_d$ target across both cage geometries, while single-cage values continue to oscillate.

**Reclassification.** $m_d$ is a **Tier 2 mechanism with a primary $\phi^{\phi}$ output**: the primary engine source adopts $m_d = m_u \phi^{\phi}$ as the FK-determinant infinite-volume-limit closed form. The row is postdiction-consistent at $+0.33\%$ conditional on O.5. On the $R=4$ lattice the value oscillates with median $\approx \phi^{\phi}$ and 1$\sigma$ band $\pm 5\%$; the I_h-closed deep-tail mean supports the $\phi^{\phi}$ candidate at the sequence-mean level, not as a uniform single-cage $\pm 3\%$ closure. The shell-resonance signature is itself a Tier 2 prediction. The rigorous convergence proof and **algebraic-field identification** of $\det_{FK}$ in the continuum limit (whether it equals $\phi^{\phi}$ exactly or only its median tracks it; how this relates, if at all, to the Bellissard $\mathbb{Z}[\phi]$ gap-label module) remain **Tier 3 / Open** — bundled with App H O.5.

**Separate finding (not closure).** The charm-quark line `m_c = m_u * fk_det_charm**2`, with `fk_det_charm = fk_det * (target_charm_sqrt / fk_det)`, algebraically forces `fk_det_charm = target_charm_sqrt`. This is a heuristic $\phi^{13+\phi^{-3}}$ target rather than a K-theoretic gap-label derivation. Per Ch10's $N=17$ second-harmonic framing, $m_c$ requires a separate gap-label analysis (App H Open Problem O.5; bundled with §TP-F). **$m_c$ stays Tier 3**.

**Falsification.** If a re-derivation of the FK determinant under the Connes–Bellissard noncommutative-integration formalism returns a value outside $[\phi^{\phi/2},\, \phi^{2\phi/2}] \approx [1.48,\, 3.20]$ in the continuum limit of the icosahedral cage, the structural identification $m_d = m_u \cdot \det_{FK}$ is falsified. The shell-resonance signature ($\pm 3\%$ oscillation about the mean across $N \gtrsim 1600$) is also experimentally observable in principle through quark-mass spread under lattice-QCD finite-volume scaling.

- **Disposition**: down-quark mass Tier 2 mechanism with primary output $m_d = m_u \phi^{\phi}$; postdiction-consistent at $+0.33\%$ conditional on O.5, with shell-resonance oscillation disclosure retained.
- **What stayed open**: charm-quark mass (Tier 3, awaiting K-theoretic gap label for $N=17$ mode — bundled with §TP-F + App H O.5).
- **Where it lives**: `GCT_Physics_Engine/src/gct_spectrum.py` (FK determinant definition), `protocol_quark_mismatch.py` (primary consumer), `protocol_quark_mismatch_scaling.py` (finite-size scaling), `protocol_md_fk_ih_closed_cages.py` (I_h-closed orbit-union cage sequence), `data/fk_scaling.json` (scaling table), `data/protocol_md_fk_ih_closed_cages_results.json` (closed-cage sequence table), V3 Ch10 §10.X (FK definition and $m_c$ status).

#### TP-C: $\alpha_s$ bare prefactor 10 trace — **PER-FACTOR TRACE CLOSED; PRODUCT REMAINS TIER 3 HANDLE**

**Audit result.** The factorisation $\alpha_s^{-1}({\rm bare}) = 10\phi^2$ is now fully traced through the manuscript at the per-factor level. The factors have geometric anchors, but the product is not promoted to a Tier 2 physical prediction: the area-law multiplication and the strong-sector matching to a bare SU(3) boundary remain a Tier 3 calibrated handle pending O.42 / QLQCD-2 closure.

| Factor | Origin | Tier | Anchor |
| :--- | :--- | :--- | :--- |
| **10** | Count of three-fold rotation axes of the rhombic triacontahedron (RT) acceptance window. Conditional on the RT/AKN substrate, this is the Tier 1 axis inventory used in the two-step color construction: Gram-image reduction to an 8-dimensional operator span, followed by a Tier 3 $A_2$ / $\mathfrak{su}(3)$ candidate-identification check. Monte Carlo controls over 1 000 random polyhedra produce zero alternatives for the same finite witness, but theorem-grade compact-Lie uniqueness remains O.39. | **Tier 1 inventory; Tier 3 identification context** | V3 §3.1.2 + §3.2.1 |
| **$\phi^2$** | Square of the dominant $H_4$ Coxeter projection eigenvalue $\bigl\|2\cos(\pi/5)\bigr\| = \phi$, forced by the Lie-algebraic structure of $E_8$ and the $H_4$ Coxeter degrees $\{2,12,20,30\}$ (Humphreys §3.7). | **Tier 1** | App U §U.7.3 Lemma T-McK.4 |
| **product $10\phi^2$** | Area-law combination: bare inverse coupling = (count of axes) × (area-scaling eigenvalue). | **Tier 3 calibrated handle** | V3 §4.5.2 + O.42 / QLQCD-2 closure target |

This per-factor decomposition is a substantive tightening of the prior shorthand: $\alpha_s^{-1}({\rm bare}) = 10\phi^2$ is not a single monolithic prediction. The factors are geometrically motivated (10 = three-fold rotation axis count of the RT acceptance window; $\phi^2$ = squared dominant $H_4$ Coxeter projection eigenvalue), while the product-level strong-coupling claim remains Tier 3 until the area-law product and native strong running are derived without the calibrated handle.

- **What closed**: the per-factor trace for $\alpha_s^{-1}({\rm bare})$. The remaining 67.6% running gap to PDG $\alpha_s(M_Z)$ is QLQCD-2 territory (App Z.7), and the product-level status is the registered Tier 3 calibrated handle.
- **Where it lives**: V3 Ch04 §4.5.5 (expanded with the explicit factor-by-factor derivation chain) + App U §U.7.3 (Lemma T-McK.4) + V3 §3.1.2 + §3.2.1 (10-axis Uniqueness Theorem).
- **Falsification**: see V3 Ch04 §4.5.5 — note that falsification of the empirical 67.6% running gap by QLQCD-2 corrections would NOT falsify the geometric factor anchors; it would falsify the Tier 3 calibrated strong-sector handle / area-law combination rule of §4.5.2.

#### TP-D: Newton's $G$ residual structure — **DIAGNOSTIC COMPLETE / UPSTREAM-CASCADED**

**Cascade structure.** The 2274 ppm $G$ residual is the upstream-cascaded image of the 1006 ppm electron mass residual (since $a_6 \propto 1/m_e$ and $G \propto a_6^2$, fractional error doubles). $2 \cdot 1006 \approx 2012$ ppm accounts for $\approx 88\%$ of the $G$ residual; the remainder is from cross-terms with $\hbar/c$ at full CODATA-2022 precision and the $\alpha$ APS-residual (3442 ppm) partially propagating through $(1-5\alpha)$.

**Muon-analogue 2nd-order pathway is structurally insufficient.** Adding the muon-analogue 2nd-order $\alpha^2$ correction to the electron mass formula yields a negligible contribution: per V3 §8.2.3, the muon's coefficient $\phi^8 = \phi^{-3}_{\text{ewk-mix}} \times \phi^{11}_{\text{bare-muon-exp}}$. Substituting the electron's bare exponent ($-107$) into the same combination rule gives $\phi^{-3} \times \phi^{-107} = \phi^{-110} \approx 6.7 \times 10^{-23}$, contributing $\phi^{-110} \cdot \alpha^2 \approx 3.6 \times 10^{-27}$ to $m_e$ — **totally negligible** relative to the 1006 ppm residual. The 2nd-order phason self-energy by the muon-analogue mechanism therefore does NOT close the electron / $G$ residuals.

**Real closure paths (none high-feasibility).** The 1006 ppm electron residual most plausibly closes through:

1. **APS $\eta$-invariant computation on $\partial\mathcal{M}_{\text{RT}}$** that closes $\alpha$'s 3442 ppm gap — this is Lemma T-McK.1b (App U §U.7.6.3), tracked on the TP-I/J closure list as a bounded analytic computation.
2. **Higher-order non-perturbative corrections** to the discrete RT lattice mass formula beyond tree-level $(1-5\alpha)$ — would require a dedicated 1-loop computation of the electron mass on the cage (analogous to the muon's §8.2.3 but for the ground-state defect rather than the 11th harmonic).
3. **Refinement of the Tier 3 $M_P$ convention** — V3 §7.2.2 flags the $\sqrt{\hbar c / G_N}$ vs $\sqrt{\hbar c / 8\pi G_N}$ choice as a Tier 3 phenomenological selection. A first-principles derivation here would change the absolute scale.

**Status.** The $G$ residual is upstream-cascaded from the electron mass residual; a tighter $G$ requires upstream work on $m_e$, not direct work on the gravitational derivation chain. The diagnostic chain is complete.

- **Where it lives**: V2 Ch09 §9.1.5 (cascade structure callout) + App R §R.1 row 1 (electron) + this entry.
- **Closure path**: bundled with TP-I/J (Lemma T-McK.1b APS spectral-flow), tracked on the future closure list per §TP.6.

#### TP-E: Higgs VEV 1.6% radiative-correction closure [Closure: math-bounded + code-bounded; Feasibility: medium]

App R §R.2 row Higgs VEV reports $v_{\rm pred} = 246.18$ GeV vs 246.22 GeV measured, with 181 ppm residual on the *absolute* derivation but a 1.6% gap in the bare Higgs mass $m_H^{\rm bare}$ (123.11 GeV vs 125.1 GeV measured). The latter is attributed to "radiative corrections" in App R footnotes. A 1-loop computation of the radiative correction in the GCT spectral framework would either close the 1.6% (promoting $m_H$ to Tier 2 with quantitative validation) or surface a structural issue.

- **What closes**: $m_H^{\rm bare}$ Tier 3 → Tier 2 (or reveals a structural revision)
- **Where it lives**: V3 Ch04 Higgs sector + new section under `protocol_higgs_vev.py`
- **Effort estimate**: 3–5 days of 1-loop spectral-action analytic work + engine integration

### TP.4 Tier 3 → Tier 2 Promotion Candidates (Medium Feasibility)

These candidates have a clear closure path but require either substantial mathematical machinery or are harder than the §TP.3 items.

#### TP-F: CKM $s_{23}, s_{13}$ from K-theoretic gap labels [Closure: gap-label route ruled out as a standalone path; residual bundles with O.5]

V3 Ch10 carries the four irrational-exponent quark formulas ($m_d, m_c, s_{23}, s_{13}$) as Tier 3 ansätze; the down-quark and charm-quark routes are addressed by TP-B (finite-size FK scaling). For the CKM angles $s_{23} = \phi^{-(6 + \phi^{-1})}$ and $s_{13} = \phi^{-(11 + \phi^{-1})}$, the K-theoretic gap-label audit (engine: `GCT_Physics_Engine/src/protocol_tpf_ckm_gap_labels.py`) enumerates the Bellissard $\mathbb{Z}[\phi]$ trace-image labels $L(p,q) = (p\,\phi^{-1} + q)\bmod 1$ (App U §U.7.6) against the observed magnitudes and establishes that this route does not close them: (i) neither observed value lies on an integer-power label $\phi^{-n}$ — both fall strictly between consecutive powers ($n_{\rm obs} \approx 6.60$ for $s_{23}$, $11.62$ for $s_{13}$, each $\gtrsim 17\%$ from the nearer power); (ii) a general $\mathbb{Z}[\phi]$ label matches the observed magnitudes only at $|p| \approx 42$ ($s_{23}$) and $|p| \approx 466$ ($s_{13}$), far beyond the validated/accessible range ($|p| \le 7$ at the 1D Fibonacci scale $F_{15} = 610$), and — because $\{p\,\phi^{-1}\bmod 1\}$ is equidistributed — multiple labels co-fit at that scale with no selection rule, the same under-determination as the open $-107$ uniqueness (O.14a); and (iii) the literal ansätze carry irrational algebraic exponents, so by the Gelfond-Schneider theorem they are transcendental and lie outside $\mathbb{Z}[\phi]$ — indeed outside any algebraic-number K-theory trace module, a convention-independent exclusion. A richer 6D AKN $K_0$ trace image than the validated $\mathbb{Z}[\phi]$ core is not excluded in principle, but no such module is supplied, and none can host the transcendental ansätze. The standalone gap-label closure is therefore ruled out; the residual derivation of $s_{23}, s_{13}$ remains with the QLQCD dressed-Dirac extraction (App H Open Problem O.5), where gap labels can at most serve as a downstream consistency check.

- **What closes**: removes the gap-label route as a standalone TP-F closure; sharpens the $s_{23}, s_{13}$ residual to the O.5 dressed-Dirac extraction
- **Where it lives**: V3 Ch10 §10.6 + App H O.5; engine `protocol_tpf_ckm_gap_labels.py`
- **Effort estimate**: standalone gap-label enumeration complete (negative result); full closure bounded by App H O.5 status

#### TP-G: Weinberg angle uniqueness via $H_4$ [Closure: math-bounded; Feasibility: medium]

App R §R.2 reports $\sin^2\theta_W^{\rm bare} = \phi^{-3} = 0.23607$ with 2.1% error against $\sin^2\theta_W^{\rm Z\text{-}pole} = 0.23122$. Currently Tier 2 ("Geometric BC"). Promotion to Tier 1 ("uniquely forced by $I_h$") would require an App Y-style uniqueness argument: prove that $\phi^{-3}$ is the *unique* volumetric scaling consistent with the $I_h$ symmetry of the cut-and-project Gram weights, no other rational power of $\phi$ admitted. The argument structure mirrors App Y's Polaron Unity Proposition and App U §U.7's T-McKay rigor.

- **What closes**: $\sin^2\theta_W^{\rm bare}$ Tier 2 → Tier 1 (uniqueness theorem)
- **Where it lives**: V2 Ch07 Electroweak + new uniqueness theorem in App U or App Y
- **Effort estimate**: 1 week of focused modular-reduction work

#### TP-H: Inattentional blindness quantitative loading [Closure: experiment-bounded; Feasibility: low]

V1 §16.6 derives the inattentional-blindness phenomenon as attention-vector misalignment with the information gradient. The qualitative derivation is Tier 2; the quantitative loading (specific psychophysical thresholds reproduced from the GCT formula $I(X) = \int |F_{\rm sel} \cdot \hat{\bf i}|\, d^3r$) is Tier 3 pending experimental validation. App H Open Problem O.3 already lists this as an open research direction. The promotion path requires psychophysics collaboration — not code-only.

- **What closes**: §16.6 quantitative claim Tier 3 → Tier 2 (subject to experimental validation)
- **Where it lives**: V1 §16.6 + App H O.3 (already a public Open Problem)
- **Effort estimate**: experiment-bounded; cannot be closed in-manuscript

### TP.5 Tier 2 → Tier 1 Promotion Candidates

These are claims already at Tier 2 under the explicit structural-anchor accounting of the Parameter Ledger that would, if a single bounded analytic step closes, promote to Tier 1 (axiomatic / mathematically forced).

#### TP-I: T-McKay → Tier 1 via T-McK.1b APS spectral-flow [Closure: math-bounded; Feasibility: medium]

App U §U.7 establishes T-McKay at Tier 1/2 with four of five forcing lemmata closed at Tier 1 in published literature. The single remaining bounded gap is **Lemma T-McK.1b**: a finite spectral-flow computation of the icosahedral $\eta$-invariant on the boundary $\partial \mathcal{M}_{RT}$ of the rhombic-triacontahedron acceptance window, via Connes-Moscovici 1995 Thm 4.1 + APS 1975 Thm 3.10.

- **What closes**: T-McKay → Tier 1 unconditional (under H1 + H2)
- **Where it lives**: App U §U.7.6.3 (already specified)
- **Effort estimate**: 1 week of operator-algebra work; finite-dimensional bookkeeping

#### TP-J: Spin-Statistics §15.3.2 → Tier 1 via the same T-McK.1b [Closure: math-bounded; Feasibility: medium — bundled with TP-I]

V1 Ch15 §15.3.2 carries the Tier label "modular reduction; Tier 1 elevation reduces to the bounded analytic step of Lemma T-McK.1b" (per Item 2 commit). Closure of T-McK.1b promotes both T-McKay and Spin-Statistics simultaneously. This is a free bundling — the same single computation lifts two theorems.

- **What closes**: V1 Ch15 §15.3.2 Spin-Statistics Theorem → Tier 1
- **Where it lives**: V1 Ch15 §15.3.2 (cross-ref) + App U §U.7.6.3 (the actual computation)
- **Effort estimate**: zero additional beyond TP-I

#### TP-K: Polaron Unity Proposition (App Y) Y.3.4 closure [Closure: math-bounded; Feasibility: medium-low]

App Y carries Polaron Unity as Tier 3 conditional for the trefoil-knot case and for the general prime-knot extension under a modular reduction. The bounded trefoil trace computation in §Y.6.3a is a finite-matrix meridian-trace surrogate, but the finite-level ambient space is $M_n \cong S^1 \times \mathbb{R}^3$, the classical knot-complement product split requires a fixed-slice reduction $H_{Y.1}$ not yet proved by the Ch11 ansatz, and the trefoil trace step still requires a unitary finite-dimensional faithful quotient. Promotion of the Polaron Unity claim from Proposition to Theorem requires closure of that O.18 subproblem plus the Anderson-Putnam-to-$S^3 \setminus K$ extension (gap A), canonicity of $K \mapsto \mathcal{A}_K$ (gap B), and a finite-quotient meridian trace construction for the general case.

- **What closes**: App Y Polaron Unity Proposition → Tier 1/2 (depending on H1 + H2 of App Y's premise structure), at which point the Proposition would be promoted to Theorem
- **Where it lives**: App Y §Y.3.4 + bibliography §IX (Knot Theory & Operator Algebras)
- **Effort estimate**: 1–2 weeks of focused operator-algebra work, contingent on literature access

### TP.6 Promotion Sequencing Recommendation (for the next closure pass and beyond)

Bundled by closure type, ordered by feasibility × impact:

**Closure-status pass (status of the four "high-feasibility" items):**

1. **TP-D** Newton's $G$ residual structure — **DIAGNOSTIC COMPLETE.** The 2274 ppm $G$ residual is upstream-cascaded from the 1006 ppm electron mass residual ($G \propto a_6^2 \propto m_e^{-2}$ doubles the fractional error). The muon-analogue 2nd-order $\alpha^2$ correction gives a $\phi^{-110}$-suppressed shift to $m_e$ — totally negligible. Real closure paths run through Lemma T-McK.1b (APS spectral-flow on $\alpha$, bundled with TP-I/J) or a dedicated electron 1-loop computation. See §TP.3 entry.
2. **TP-C** $\alpha_s$ bare prefactor 10 trace — **PER-FACTOR TRACE CLOSED; PRODUCT TIER 3.** The 10 axis count and $\phi^2$ factor are geometrically traced, but the area-law product remains the registered Tier 3 calibrated strong-sector handle pending O.42 / QLQCD-2. See §TP.3 entry.
3. **TP-B** FK finite-size scaling for $m_d$ — **Tier 2 mechanism; primary $\phi^{\phi}$ output.** The primary engine source adopts $m_d = m_u \phi^{\phi}$ as the FK-determinant infinite-volume-limit closed form, postdiction-consistent at $+0.33\%$ conditional on O.5. The enlarged $R=4$ lattice oscillates around $\phi^{\phi}$ with a decaying envelope. The I_h-closed orbit-union cage sequence in `protocol_md_fk_ih_closed_cages.py` gives deep-tail ($N \ge 2000$, 17 cages) mean $\det_{FK}/\phi^{\phi}=0.9976$ (sample std $0.0253$) and mean signed error vs PDG $+0.09\%$; the closed-cage tail error range is $[-7.20\%, +10.12\%]$, all tail values sit inside the 11% shell-resonance band, and excursions persist at $N=1746$ ($+5.6\%$), $N=1866$ ($+10.1\%$), and $N=2688$ ($+5.4\%$). Rigorous convergence proof and algebraic-field identification of $\det_{FK}$ in the continuum limit remain Tier 3/Open, bundled with O.5. The charm-quark hard-coded heuristic is exposed as Tier 3 awaiting QLQCD-1L gap-label analysis. See §TP.3 entry.
4. **TP-A** $Z_3 = 7/10$ closed-form derivation — **NEGATIVE — long-horizon (QLQCD-2 dependent).** See §TP.3 entry for the analysis: the 7 in the numerator has no GCT-native origin in icosahedral group theory; the form is calibration, not closed-form derivation.

**Net summary:** of the four high-feasibility items, TP-B supplies the primary $\phi^{\phi}$ output for $m_d$ conditional on O.5, TP-C closes only the per-factor trace while retaining Tier 3 product status, TP-A resolves to long-horizon QLQCD-2-dependent work, and TP-D is upstream-cascaded to the electron mass residual (residual lives at $m_e$, not at $G$). TP-B is particularly substantive: $m_d$ matches the Mixed-Harmonic Area Law heuristic $\phi^{\phi}$ at $+0.33\%$ through the primary engine source, anchored on the textbook Fuglede-Kadison determinant $\exp((1/N)\sum\log|\lambda_i|)$ rather than a gap-ratio shortcut.

**Recommended future closure pass (medium-feasibility, higher mathematical investment):**

5. **TP-I + TP-J** Joint T-McK.1b APS spectral-flow computation — 1 week, medium feasibility, very high impact (simultaneously promotes T-McKay and Spin-Statistics to Tier 1)
6. **TP-G** Weinberg angle $\phi^{-3}$ uniqueness theorem — 1 week, medium feasibility, medium-high impact
7. **TP-E** Higgs VEV radiative-correction 1-loop closure — 3–5 days, medium feasibility, medium impact

**Long-horizon (not bounded-pass material; programmatic):**

8. **TP-A** $Z_3$ from first principles — bundled with App H O.5 + App Z.7 QLQCD-2 (the 7 in the numerator requires direct phason-loop computation; closed-form from icosahedral group theory alone is ruled out by the §TP.3 audit)
9. **TP-F** CKM $s_{23}, s_{13}$ via K-theoretic gap labels — bundled with App H O.5 (QLQCD-1L)
10. **TP-K** Polaron Unity Y.3.4 closure — bundled with App Y revision pass
11. **TP-H** Inattentional blindness experimental validation — App H O.3 (experiment-bounded)

### TP.7 What This Roadmap Does NOT Include

To preserve the boundary between (i) candidates with clear math/code paths and (ii) genuine open research, the following are *excluded* from this roadmap and remain in the **Open Problems** inventory of App H §H.5:

- **O.1 / O.4** Phason mass gap & $H_0$ from lattice dynamics — these are equivalent open problems and constitute the framework's primary cosmological frontier. Closure is a research programme, not a bounded computation.
- **O.5** QLQCD-1L closure — a multi-month lattice-computation programme; TP-F above is a sub-component contribution.
- **O.6** dS/CFT boundary state for $\chi$ — a famous open conjecture in holographic gravity (Strominger 2001 / Maldacena 2003 territory); no tractable closure path.
- **O.2** Mechanical proof of neutrino eigenvalues (Protocol G) — 6D lattice simulation; bounded but compute-intensive and dependent on simulation framework readiness.

### TP.8 Process Note

This roadmap is a working document. Promotion candidates are added or removed as the math-closure pass continues. The expected cadence is one pass per minor version closing the top 3–5 candidates by feasibility × impact, with the remaining candidates rolling forward. The discipline is the same as the rest of the manuscript: tier labels move only when the work is done, not on intention.
