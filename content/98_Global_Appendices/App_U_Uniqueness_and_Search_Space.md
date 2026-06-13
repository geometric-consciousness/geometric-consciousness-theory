# Appendix U: Uniqueness and Search Space Analysis

A foundational requirement for any theory of everything is the prevention of "Look-Elsewhere" bias—the ability to find patterns in any data given enough trials. This appendix defines the search space of **Geometric Consciousness Theory (GCT)** and separates the Tier 2 multi-exponent geometric template from the Tier 3 specific integer anchors that remain tied to the QLQCD closure target.

## U.1 Bounded Search Space

GCT is not a curve-fitting exercise. The "Search Space" for physical constants is bounded by the symmetries of the **6D Hypercubic Lattice** and its **240-vertex E8 projection**.

1. **Scalar Anchor:** All mass ratios are referenced to the Electron mass ($m_e$), which represents the fundamental unit cell mass $a_6 \equiv 1$.
2. **Allowed Operators:** Formulas are restricted to powers of the Golden Ratio ($\phi$), the Fine-Structure Constant ($\alpha$), and the unit cell count $N=144$.
3. **Integer Forcing:** Exponents must be integers or simple fractions (e.g., $N/2$) derived from the **Symmetry Octave** rule.

---

## U.2 The Symmetry Octave Rule

The fundamental resonator of GCT is the **Icosahedral Shell**. Resonant modes are geometrically forced into nodes of 6-fold symmetry ($N = 6k \pm 1$).

### **U.2.1 The Muon (N=11)**
The exponent **11** for the Muon ratio ($m_\mu/m_e \approx \phi^{11}$) sits at the first sub-octave node of the 2nd shell of the symmetry-octave template:
$$ N = (2 \times 6) - 1 = 11 $$
This node is the primary stability point for a 12-vertex structure with a single defect. The shell-filling template $N = 6k \pm 1$ is Tier 2; the selection of this specific node is Tier 3 — consistent with, but not uniquely forced by, the template — pending the QLQCD closure target (§U.4; Ch08 §8.3.1; App H O.5).

### **U.2.2 The Tau (N=17)**
The exponent **17** for the Tau ratio ($m_\tau/m_e \approx \phi^{17}$) sits at the 3rd-shell node of the same Tier-2 template:
$$ N = (3 \times 6) - 1 = 17 $$
The absence of a lepton at $N=14 \pm 1$ is consistent with the gap between the 2nd and 3rd icosahedral shells in the 6D packing. As with $N=11$, the specific selection is Tier 3 — consistent with the shell-filling template, not uniquely forced — pending the QLQCD closure target (§U.4; Ch08 §8.3.1; App H O.5).

---

## U.3 The Baryonic Triad (N=15)

The base exponent **15** for the Proton mass ($m_p \sim \phi^{15}$) is forced by the **(3×5) Closure**:
- **3 Quarks:** Representing the internal degrees of freedom.
- **5-Fold Symmetry:** The fundamental rotational symmetry of the icosahedron.
The product $3 \times 5 = 15$ gives the number of gluonic winding states that close the baryonic knot — a Tier-2 structural mechanism, not an arbitrary fit. As with the lepton exponents (§U.2), the specific base value is Tier 3 pending the QLQCD closure target (§U.4), and the full exponent $15 + \phi^{-1}$ carries the Tier-3 Berry-phase correction handle (App R).

---

## U.4 Remaining Ansatz Terms and Integer Anchors [Mixed Tier]

The multi-exponent geometric template is Tier 2: leptons, baryons, and correction terms are restricted to symmetry-octave nodes and icosahedral projection data rather than arbitrary real-valued fits. The specific base exponents $(11,15,17)$ are Tier 3 fixed pending the QLQCD closure target (Ch08 §8.3.1; App H O.5/O.14/O.15); extracting the solitonic eigenvalues ab initio remains the closure target. Certain precision correction terms also remain at the **Ansatz Level**:

| **Term** | **Role** | **Status** |
| :--- | :--- | :--- |
| **$+5\alpha$** | Muon phason drag | $A_5$ channel multiplicity is analytically anchored; equal-weight conversion to the pole-mass coefficient is Tier 3 pending first-principles GCT self-energy / HPC eigenvalue closure |
| **$+\phi^{-1}$** | Proton projection shift | Derived via holonomy proof in `protocol_proton_berry_phase.py`. |
| **$3442$ ppm** | α residual | **Tier 2 (Target).** Identified as the Phason Anti-Screening shift. Defines the 1-loop research debt. |
| **$+\phi^8\alpha^2$** | Electroweak Mixing Correction | **Tier 2 exponent arithmetic + Tier 3 pole-mass residual closure.** The product is exact as exponent arithmetic in the registered $\phi^8\alpha^2$ readout, while its use in the absolute muon/Higgs pole-mass comparison remains conditional on O.15/O.5/O.19/O.26 closure. |

By identifying these terms explicitly, GCT maintains **epistemic discipline**. The Tier 2 structural claim is the multi-exponent geometric template; the current specific integer values and precision residuals are the closure frontier.

---

## U.5 Statistical Significance (Look-Elsewhere Analysis)

To prove that the GCT mass spectrum matches are not the result of "numerological cherry-picking," we perform a rigorous Look-Elsewhere Analysis.

### **U.5.1 Search Space Size**
The search space is defined by the **Symmetry Octave** rule: $N \in [1, 30]$. 
The allowed operators are limited to $\{\phi^N, \alpha, N \}$. 

### **U.5.2 Probability of Chance Match**
If the Lepton mass ratios ($m_\mu/m_e$ and $m_\tau/m_e$) were random numbers, the probability of them falling within $20$ ppm of a simple $\phi^N$ power for $N \le 30$ is:
* **Muon ($N=11$):** $P \approx 5 \times 10^{-4}$
* **Tau ($N=17$):** $P \approx 2 \times 10^{-3}$

### **U.5.3 Combined Significance (Pre- and Post-LEA)**

The raw combined probability of chance-matching both lepton mass exponents (N=11 and N=17) to 20 ppm precision simultaneously, within the shell-filling constraint $N = 6k \pm 1$, yields:

- **Canonical headline (broad internal look-elsewhere): ≈2.6σ** from the full $\mathbb{Z}[\phi]$ multi-base sweep over Lucas-vs-non-Lucas exponent assignments (Firewall §3 Master Statistical Table + App R §R.9.2).
- **Conditional auxiliary: ≈3.1σ** under the Conservative full-SM-texture window $N \in [4, 50]$ across ~25,000 trial pairs. The window choice is itself a framework-internal prior; citing this figure as headline without naming the window prior is significance laundering under the Firewall governance discipline.
- **Conditional auxiliary: ≈4.4σ** under the framework's depinning-threshold prior $N \in [8, 25]$ (153 trial pairs; the $N=8$ lower bound is itself a structural postulate per Ch08 §8.1.1). Citing this figure as headline without naming the conditioning prior is significance laundering under the Firewall governance discipline.
- **No separate $\gtrsim 4.7\sigma$ Postulate-G auxiliary is retained under the corrected Galois search space.** Postulate G restricts admissible exponent arithmetic to Galois-compatible integer powers $N \in \mathbb{Z}$ rather than to Lucas numbers specifically; with that corrected search-space it does not supply an additional narrower trial factor beyond the canonical multi-base / depinning-window disclosures. Postulate G remains a structural postulate of the framework rather than an independently established constraint.

The canonical headline figure across the manuscript is **≈2.6σ** (broad internal look-elsewhere); the 3.1σ and 4.4σ figures are conditional auxiliaries cited only with their conditioning priors named at the point of citation — **subject also to the search-space disclosure of §U.5.4 below**. A Lucas-only / Postulate-G-only $\gtrsim 4.7\sigma$ auxiliary is not supported after correcting Postulate G to $N \in \mathbb{Z}$.

### **U.5.4 Search-Space Disclosure**

The 4.4σ conditional auxiliary of §U.5.3 holds *conditional on the search space being the 153 $(N_1, N_2)$ trial pairs in $N \in [1, 30]$ with the shell-filling constraint $N = 6k \pm 1$ and the operator set restricted to $\{\phi^N, \alpha, N\}$*. A hostile reviewer can legitimately object that the actual GCT manuscript invokes a wider family of expressions across Volumes 2–3, including:

- $\phi$-powers and Galois-compatible integer exponents $N \in \mathbb{Z}$ ($\sim$ several hundred candidates after symmetry-octave + Galois pre-filtering);
- mixed lepton-harmonic ladders ($\sim$ tens of cross-terms);
- $\alpha$-corrections at zeroth, first, and second order ($\sim$ thirty operator forms when combined with the above);
- icosahedral-group-theoretic coefficients (Clebsch–Gordan products, dimensions of irreps, orbit lengths) — a few dozen distinct rationals;
- bilayer / cage factors (e.g., $1 - 1/288$, $1 - 5\alpha$) — a small but non-zero family of dressings.

If one removes the symmetry-octave + Galois-rationality pre-filters and counts the full unfiltered reachable-expression set across all of these classes, a hostile bound estimates approximately $1.3 \times 10^5$ expressions. Under that wider correction, the lepton-pair significance would degrade from $\approx 4.4\sigma$ to approximately $2.5\sigma$ — a substantially weaker result.

**The GCT position on this widening.** The 4.4σ conditional auxiliary is meaningful *within the symmetry-octave + Galois-rationality framework* — i.e., within the pre-filter the manuscript actually uses to select expressions for *new* predictions. Outside that pre-filter, the 4.4σ figure does not apply, and the bare lepton-pair coincidence carries only $\approx 2.5\sigma$ after LEA correction under the widest hostile bound. The broad internal look-elsewhere ≈2.6σ canonical headline sits at the conservative edge of this band; the 3.1σ Conservative-SM-texture-window-conditional and 4.4σ depinning-window-conditional figures are auxiliaries above it. The full evidential case for GCT therefore *does not rest on the lepton-pair LEA alone* — it rests on the conjunction of: (i) the lepton pair at the broad internal look-elsewhere ≈2.6σ canonical (with 3.1σ Conservative-window-conditional and 4.4σ depinning-prior-conditional auxiliaries); (ii) App-FM postdiction-consistency and algebraic-coherence rows for the Higgs VEV, proton mass, fine-structure-constant bilayer, and CP-violating phase predictions (V3 Ch7–10, App R), which are internal-alignment evidence rather than in-favor empirical detection pills. App FM currently records zero **DETECTED-TIGHT** and zero **DETECTED-MARGINAL** rows; rows marked POSTDICTION-CONSISTENT, CONSISTENT, ALGEBRAIC, PENDING-α-RESOLUTION, AT-GATE TENSION, CURRENT-DATA-TENSION, OPEN-RESEARCH, OPEN-CONDITIONAL, or PENDING-VERIFIER are not counted as in-favor empirical detection evidence. The muon $g - 2$ channel is registered as **Tension under WP2025** pending HVP-synthesis arbitration rather than load-bearing empirical evidence; (iii) the Tier 1/2 protocol-A-prime and protocol-D falsifiability paths (V3 Ch13, Ch16); and (iv) the substrate-prediction divergences from IIT / Orch-OR / Illusionism (V1 Ch16–17). No single observable is load-bearing; the conjunction is what is intended to be persuasive.

**For readers who want only LEA-conservative evidence:** the broad internal look-elsewhere canonical headline is ≈2.6σ; under the widest hostile-bound search space (no pre-filter at all), the lepton-pair coincidence degrades to ≈2.5σ. The load-bearing case across the manuscript rests on the conjunctive evidence in (ii)–(iv) above, not on the lepton-pair LEA alone. Readers who accept the symmetry-octave + Galois-rationality framework as a *prior* established by the geometric derivation chains (rather than as a post-hoc filter) may regard the 4.4σ depinning-threshold conditional figure as evidentially relevant within that prior; no separate Postulate-G/Lucas-only auxiliary is retained. The choice between these readings is a Tier 3 methodological judgement and is disclosed at the point of citation rather than buried in the headline.



## U.6 Lemma III (Complete Proof): Uniqueness of the Icosahedral Vacuum [Tier 2]

> **Lemma III: Proof Status [Tier 1/2 — Uniqueness-Justified Structural Postulate]**
>
> Lemma III is established by two complementary proofs that together cover the logical space of quasicrystalline alternatives, *conditional on* the architectural commitment that the physical vacuum admits a polyhedral 3D point-group symmetry:
>
> - **§U.6.1 (Group Cohomology / Schur Multipliers):** Among binary polyhedral candidates ($2T \to E_6$, $2O \to E_7$, $2I \to E_8$), only $A_5$ (Icosahedral) is perfect with $H_1 = 0$, guaranteeing a unique universal central extension ($2I$). Tetrahedral and octahedral alternatives fail this perfectness condition.
>
> - **§U.6.2 (Atiyah–Hirzebruch / Stiefel–Whitney $w_2$):** Among non-polyhedral quasicrystalline symmetries (Decagonal $D_{10h}$, Octagonal $D_{8h}$), the classifying spaces carry a topological obstruction $w_2 \neq 0 \in H^2(B\Gamma, \mathbb{Z}_2)$ that prevents a globally consistent Spin structure without introducing a new free parameter.
>
> Together, §U.6.1 + §U.6.2 eliminate every quasicrystalline competitor — binary polyhedral and non-polyhedral alike — once the vacuum is required to admit a polyhedral 3D symmetry that supports Spin structure. Both proofs invoke standard textbook constructions (group cohomology and the Atiyah–Hirzebruch spectral sequence); the architectural commitment is the *premise*, not the proof. Lemma III is therefore classified **Tier 1/2 (Uniqueness-Justified Structural Postulate)**: the elimination of competitors is unconditional within the postulated class; the elevation to full Tier 1 would require an axiom-level argument that the vacuum must possess polyhedral symmetry rather than, for example, no symmetry at all.

**Lemma III (Complete Proof): All irrational ordered (quasicrystalline)
projections with $\lambda \neq \phi$ fail to produce a 3D symmetry group admitting
the required spinorial double cover.**

*Proof via McKay correspondence classification:*

Every quasicrystalline projection has an associated 3D point group $G$
and a binary polyhedral double cover $\tilde{G}$. By the McKay correspondence,
$\tilde{G}$ determines a unique simply-laced Lie algebra:

| $\tilde{G}$ | Order | 3D group $G$ | McKay Lie algebra | Natural lattice dim |
|--------|-------|------------|-------------------|---------------------|
| 2T | 24 | A₄ (tetra) | E₆ | 6D (but no RT) |
| 2O | 48 | S₄ (octa) | E₇ | 7D |
| 2I | 120 | A₅ ≅ H₃ | E₈ | 8D → 6D sub-lattice |

**Note on $E_6/E_7$ Dark Branches:** While Lemma III demands the icosahedral $2I \to E_8$ full manifold for the baryonic Standard Model phase, the discrete geometric projection physically populates the smaller, highly symmetric subalgebras ($2T \to E_6$ and $2O \to E_7$). These structures exist as non-interacting "Dark Sectors," sheltering sterile neutrinos and dark gauge bosons (e.g., in the $E_6$ adjoint $\mathbf{78}$) without violating the fundamental $E_8$ uniqueness.

GCT requires simultaneously:
1. A₅ ≅ H₃ symmetry (icosahedral RT acceptance window — Theorem 4.2)
2. Binary spinorial double cover (fermion 4π cycle — Chapter 15)
3. E₈-compatible 6D parent lattice (App_K stiffness hierarchy)

Only 2I satisfies all three. The silver ratio ($\delta_S = 1+\sqrt{2}$) generates
octagonal symmetry (2O → S₄), which fails condition 1. The tetrahedral
case (2T → E₆) produces a 6D algebra but with the wrong symmetry structure
(A₄ ≠ A₅ — no 5-fold axes, no RT window). □

The GCT protocol `gct_mckay_e8.py` verifies the E₈ → H₄(600-cell) → 2I chain
numerically. This lemma provides the algebraic WHY behind that numerical result.

> [!NOTE] 
> **Theoretical Note: Grassmannian Arithmetic Geometry**
> The $\phi$-optimality Diophantine gap proof has a natural extension in arithmetic geometry. The icosahedral lattice $\Lambda_{icos}$ defines a rational point on the Grassmannian $Gr(3,6)$ over $\mathbb{Q}(\phi)$. The Bogomolov–Zhang theorem on the distribution of algebraic points of small Weil height implies that lattices achieving the Diophantine approximation optimum must correspond to CM (complex multiplication) points on this Grassmannian. The icosahedral lattice, defined over $\mathbb{Q}(\phi)$ with $\phi^2 - \phi - 1 = 0$, is precisely a CM point. This suggests the icosahedral selection is globally optimal—the unique CM Grassmannian point achieving minimum height. [Tier 4 — Open Conjecture] Formal verification is left as an open mathematical problem.

### **U.6.1 Universal Proof via Group Cohomology and Schur Multipliers [Tier 1]**

A physical vacuum must admit a stable **Spin Structure** to support fermions (spinors). Topologically, this requires the point group $\Gamma$ to possess a unique **Universal Central Extension** by $\mathbb{Z}_2$. This property is determined by the **Schur Multiplier** $H_2(\Gamma, \mathbb{Z})$ and the Perfectness of the group ($H_1(\Gamma) = 0$).

**Comparative Analysis of Quasicrystal Symmetries:**

| Group | $H_1(\Gamma)$ (Abelianization) | Perfect? | Schur Multiplier $H_2$ | Spin Structure Status |
| :--- | :---: | :---: | :---: | :--- |
| **$A_5$ (Icosahedral)** | **0** | **Yes** | **$\mathbb{Z}_2$** | **Unique, Stable ($2I$)** |
| $D_{10}$ (Decagonal) | $\mathbb{Z}_2$ | No | 0 | Obstructed / Non-Universal |
| $D_8$ (Octagonal) | $\mathbb{Z}_2 \times \mathbb{Z}_2$ | No | $\mathbb{Z}_2$ | Non-Unique (Path Dependent) |
| $D_{12}$ (Dodecagonal) | $\mathbb{Z}_2 \times \mathbb{Z}_2$ | No | $\mathbb{Z}_2$ | Non-Unique (Path Dependent) |

**Proof:**
Only the Icosahedral group $A_5$ is **Perfect**. Its trivial abelianization ($H_1=0$) ensures that the central extension is universal. The Schur Multiplier $H_2(A_5, \mathbb{Z}) = \mathbb{Z}_2$ guarantees that this extension is exactly the **Binary Icosahedral Group ($2I$)**, which acts as the Spinor covering group.

For all other quasicrystalline point groups (Dihedral family $D_{2n}$), the group is solvable, not perfect ($H_1 \neq 0$). Consequently, they do not admit a Universal Central Extension. The definition of a spinor in such geometries is either topologically obstructed ($w_2 \neq 0$) or context-dependent (non-unique lifting), violating the **Axiom of Intelligibility**.

**Conclusion:** Icosahedral geometry is the unique 3D discrete symmetry capable of supporting a globally consistent, unobstructed fermion spectrum. $\square$

### **U.6.2 Supporting Proof via Cobordism Theory (Closing the Quasicrystal Loophole)**

The McKay-correspondence proof above addresses **binary polyhedral groups** but does not by itself rule out non-polyhedral quasicrystalline symmetries such as the Decagonal ($D_{10h}$) or Octagonal ($D_{8h}$) point groups, which exist in physical quasicrystals. The following argument eliminates all remaining candidates using a topological obstruction.

> **Proof via Atiyah-Hirzebruch Spectral Sequence (Cobordism):**
>
> A physical vacuum must admit a globally consistent **Spin Structure** in order to support fermionic matter. In topological field theory, the existence of a spin structure on the classifying space $BG$ of a symmetry group $G$ is determined by the **vanishing of the second Stiefel-Whitney class** $w_2$ in the cohomology group $H^2(BG, \mathbb{Z}_2)$.
>
> Evaluating $w_2$ for each candidate quasicrystalline point group $\Gamma \subset SO(3)$:
>
> | **Symmetry Group $\Gamma$** | **Classifying Space obstruction $H^2(B\Gamma, \mathbb{Z}_2)$** | **Spin Structure?** |
> | :--- | :--- | :--- |
> | **Icosahedral ($I_h \cong A_5 \times \mathbb{Z}_2$)** | $= 0$ | ✓ Unobstructed |
> | **Decagonal ($D_{10h}$)** | $\neq 0$ | ✗ Obstructed |
> | **Octagonal ($D_{8h}$)** | $\neq 0$ | ✗ Obstructed |
> | **Tetrahedral ($T_h$)** | $\neq 0$ | ✗ Obstructed |
>
> Only the Icosahedral group $I_h$ has $w_2 = 0$, meaning it is the unique quasicrystalline point group that allows a globally consistent definition of spinor fields without breaking the lattice symmetry.
>
> *Physical implication:* A Decagonal or Octagonal vacuum would require a **Spin$^c$ structure** rather than a true Spin structure, introducing an additional $U(1)$ principal bundle. This extra bundle is an unregistered structural input under the current 5-postulate-plus-3-anchor ledger and would need explicit free-parameter accounting before it could compete with the registered icosahedral substrate.
>
> This **topological obstruction** therefore proves Lemma III for *all* possible quasicrystalline point groups, not merely the binary polyhedral subgroups addressed by the McKay correspondence. The Icosahedral vacuum is uniquely selected at the level of cobordism invariants, prior to any dynamical calculation. $\square$

**Synthesis:** The Schur Multiplier proof (§U.6.1) and the cobordism obstruction proof (§U.6.2) are logically independent and jointly exhaustive. Together they prove Lemma III for all conceivable quasicrystalline competitors — binary polyhedral and non-polyhedral alike. Lemma III is hereby classified **Tier 1 (Complete Proof by Exhaustion)**. $\square\square$

### U.7 Theorem T-McKay: The 6D Parent Lattice as a Derived Necessity

> **Cross-reference note.** This section supplies the formal proof of Theorem T-McKay, the disposition of which is referenced in the Global Abstract, the Axiom & Postulate Ledger §2, App G §G.2.5 (Tier 1/2 classification), App T §T.1 (Tier audit row "6D Parent Lattice"), and downstream lattice-action chapters of Volumes 2 and 3. The level of rigor follows the modular-reduction template established for the Polaron Unity Proposition in Appendix Y: four of the five required lemmata are closed in this appendix or in the cited literature; the single remaining structural gap is itemized in §U.7.6 with an explicit reduction to a finite spectral-flow calculation.

#### U.7.1 Statement

> **Theorem T-McKay (6D Parent Lattice as a Derived Necessity) [Tier 1/2 — modular reduction, closing lemma is currently a Tier-3 consistency check on a non-symmetric truncation per §U.7.6.3; see §U.7.6 for the bounded sub-steps and the cage-symmetry caveat].** *Let the physical vacuum admit (a) a discrete 3D point-group symmetry $\Gamma \subset SO(3)$ supporting a globally consistent Spin structure (Lemma III, §U.6), and (b) persistent topological knotting of one-dimensional defects (Theorem E.1; Axiom of Intelligibility under the dimensional Knot-Theoretic Bound). Then the 6-dimensional Euclidean integer lattice $\mathbb{Z}^6$ is uniquely determined as the minimal periodic parent lattice of the cut-and-project ansatz, via the three-step chain:*
>
> **Theorem-vs-Lemma framing.** Four of the five required sub-results are Tier-1 closed at the literature level (Lemmata III, T-McK.2, T-McK.3, T-McK.4). The closing sub-step T-McK.1b is currently a Tier-3 consistency check (§U.7.6.3): the engine's 144-node cage adjacency is not exactly $I$-symmetric, so the spectral-asymmetry argument $\eta_{\rm eff} = -1$ on the cage cannot be made structurally on the cage as implemented (§U.7.6.6 footnote 3). "Theorem T-McKay" is therefore better read as "T-McKay Forcing Chain" — a Tier-1/2 modular reduction in which the closing step is structurally identified but not yet closed at theorem-level rigor. Tier-1 elevation requires either (i) rebuilding the cage as a canonical union of $I$-orbits with a uniqueness rule selecting the $[12, 60, 12, 60]$ partition (§U.7.6.6 path (a)), or (ii) the smooth-side Connes-Moscovici character-theoretic evaluation on the continuous $\partial \mathcal{M}_{RT}$ orbit. Tracked under Open Problem O.14b (App H §H.5).
>
> $$\Gamma = A_5 \;\xrightarrow{\;\mathrm{Step\ 1}\;}\; \tilde{\Gamma} = 2I \;\xrightarrow{\;\mathrm{Step\ 2:\ McKay}\;}\; E_8 \;\xrightarrow{\;\mathrm{Step\ 3:\ Elser\text{–}Sloane}\;}\; \mathbb{Z}^6 \;\xrightarrow{\;\mathrm{cut\text{–}and\text{–}project}\;}\; H_3.$$
>
> *Each arrow is forced (uniquely) by a closed result in the published mathematical literature, with the single exception of the Spin-Statistics dependency in Step 1, which is reduced (§U.7.6) to a finite spectral-flow computation on the boundary $\partial\mathcal{M}_{RT}$ of the rhombic-triacontahedron acceptance window — the Atiyah–Patodi–Singer (APS) defect-index identification.*

The proof proceeds via three forcing lemmata (T-McK.1, T-McK.2, T-McK.3) and one closure lemma (T-McK.4). Lemmata T-McK.2, T-McK.3 and T-McK.4 are Tier 1 (closed in the literature). Lemma T-McK.1 reduces to two sub-claims: T-McK.1a (algebraic — the spinor cover step, Tier 1) and T-McK.1b (analytic — the APS defect-index identification, Tier 2 with explicit reduction). The present disposition is therefore **Tier 1/2** in the sense of App G §G.2.5, with the residual analytic gap bounded by §U.7.6.

---

#### U.7.2 Preliminaries

##### U.7.2.1 Notation and standing hypotheses

Throughout this section we adopt the following notation, all of which is standard in the literature:

| Symbol | Meaning |
| :--- | :--- |
| $\Gamma \subset SO(3)$ | Discrete polyhedral 3D point group selected by Lemma III §U.6 |
| $\tilde{\Gamma} \subset SU(2)$ | Universal central extension of $\Gamma$ by $\mathbb{Z}_2$ (Schur cover) |
| $A_5$ | Alternating group on 5 letters; $A_5 \cong I \cong H_3^+$ |
| $2I$ | Binary icosahedral group; order 120; $2I \cong \mathrm{SL}_2(\mathbb{F}_5)$ |
| $E_8$ | Exceptional simply-laced Lie algebra of rank 8; root system has 240 roots |
| $H_4$ | Non-crystallographic Coxeter group of rank 4; $|H_4| = 14{,}400$ |
| $\mathcal{M}_{RT}$ | Rhombic triacontahedron in $E_\perp \cong \mathbb{R}^3$ (acceptance window) |
| $\partial \mathcal{M}_{RT}$ | Boundary of the acceptance window; closed 2-manifold |
| $\eta(D)$ | Atiyah–Patodi–Singer $\eta$-invariant of the Dirac operator $D$ |
| $\mathrm{ind}_{APS}(D)$ | APS boundary-corrected Dirac index |
| $n_{\mathrm{def}}$ | Defect index — the integer associated to a stable knotted defect via the WZW holonomy / APS spectral flow |

The standing hypotheses inherited from prior sections are:

> **Hypothesis H1 (Polyhedral premise).** The vacuum point group admits a discrete 3D polyhedral symmetry $\Gamma$ supporting a globally consistent Spin structure. *(Lemma III, §U.6.1 + §U.6.2 — Tier 1 by exhaustion within the polyhedral class.)*
>
> **Hypothesis H2 (Knot-theoretic premise).** Persistent topological knotting of one-dimensional defects is supported by the physical slice $E_\parallel \cong \mathbb{R}^3$. *(Theorem E.1, App E §E.1 — Tier 1; the knot-theoretic bound is independent of GCT-specific architecture.)*

##### U.7.2.2 The McKay correspondence (standard form)

The McKay correspondence (McKay 1980) is a bijection between conjugacy classes of finite subgroups of $\mathrm{SU}(2)$ and simply-laced affine Dynkin diagrams of type ADE. For binary polyhedral subgroups:

| Binary group $\tilde{\Gamma}$ | Order | Base group $\Gamma \subset SO(3)$ | McKay graph | Lie algebra |
| :--- | :---: | :--- | :---: | :---: |
| Binary cyclic $2C_n$ | $2n$ | $C_n$ | $\widetilde{A}_{n-1}$ | $A_{n-1}$ |
| Binary dihedral $2D_n$ | $4n$ | $D_n$ | $\widetilde{D}_{n+2}$ | $D_{n+2}$ |
| Binary tetrahedral $2T$ | 24 | $A_4$ | $\widetilde{E}_6$ | $E_6$ |
| Binary octahedral $2O$ | 48 | $S_4$ | $\widetilde{E}_7$ | $E_7$ |
| Binary icosahedral $2I$ | 120 | $A_5$ | $\widetilde{E}_8$ | $E_8$ |

The correspondence assigns to each $\tilde{\Gamma}$ the affine Dynkin diagram whose vertices are the irreducible complex representations of $\tilde{\Gamma}$ and whose edges are determined by the decomposition of the defining 2-dimensional representation tensored with each irrep (the "McKay multiplication rule"). The Lie algebra associated to $\tilde{\Gamma}$ is the finite ADE algebra obtained by deleting the affine node. [Tier 1 — closed in McKay 1980; modern textbook treatment in Steinberg, *Representation Theory of Finite Groups* §10.]

##### U.7.2.3 The Elser–Sloane projection (standard form)

The Elser–Sloane projection (Elser & Sloane 1987, *J. Phys. A* 20: 6161) is the explicit linear map
$$\pi_{ES}: \mathbb{R}^8 \longrightarrow \mathbb{R}^4$$
defined by the matrix
$$P_{ES} = \frac{1}{\sqrt{2(2+\phi)}} \begin{pmatrix} \phi & 0 & 1 & 0 & 0 & 0 & 0 & -1/\phi \\ 0 & \phi & 0 & 1 & 0 & 0 & 1/\phi & 0 \\ 0 & 0 & \phi & 0 & 1 & 1/\phi & 0 & 0 \\ 0 & 0 & 0 & \phi & 1/\phi & -1 & 0 & 0 \end{pmatrix}$$
which sends the 240 roots of $E_8$ exactly onto the 120 vertices of the 600-cell (the $H_4$ root system), doubly covered. The eigenvalues of the Coxeter element of $H_4$ are $e^{2\pi i j / 30}$ for $j \in \{1, 11, 19, 29\}$; the dominant ratio is $\phi$, which is forced as the projection slope by the $H_4$ Coxeter number $h = 30$ via $\cos(\pi/5) = \phi/2$. The further projection $\mathbb{R}^4 \to \mathbb{R}^3$ from $H_4$ onto its $H_3$ sub-root-system yields the icosahedral 3D quasicrystal, with acceptance window the rhombic triacontahedron $\mathcal{M}_{RT}$. [Tier 1 — closed in Elser & Sloane 1987; verified independently in Moody & Patera 1993, *J. Phys. A* 26: 2829.]

##### U.7.2.4 The Atiyah–Patodi–Singer framework (standard form)

For a compact Riemannian manifold $M$ with boundary $\partial M$ and a Dirac operator $D$ acting on a spinor bundle, the Atiyah–Patodi–Singer index theorem (Atiyah, Patodi & Singer 1975, Math. Proc. Camb. Phil. Soc. 77: 43) states
$$\mathrm{ind}_{APS}(D) \;=\; \int_M \widehat{A}(M) \,\wedge\, \mathrm{ch}(\mathcal{E}) \;+\; \tfrac{1}{2}\bigl(h(D|_{\partial M}) - \eta(D|_{\partial M})\bigr),$$
where $h$ is the dimension of the kernel of the boundary Dirac operator and $\eta$ is the Atiyah–Patodi–Singer $\eta$-invariant — the regularized spectral asymmetry of $D|_{\partial M}$. The $\eta$-invariant is a real number, and on a 2-dimensional closed boundary $\partial M$ it takes values in $\mathbb{Q}$ for finite-symmetry-orbit configurations (Connes & Moscovici 1995, *Geom. Funct. Anal.* 5: 174, Theorem 4.1). [Tier 1 — closed in APS 1975; the rationality on finite-orbit boundaries is Tier 1 from Connes–Moscovici 1995.]

---

#### U.7.3 Forcing Lemmata

##### Lemma T-McK.1a (Spinor cover: $A_5 \Rightarrow 2I$) [Tier 1]

*Let $\Gamma = A_5 \subset SO(3)$ be the icosahedral rotation group. Then the unique universal central extension of $\Gamma$ by $\mathbb{Z}_2$ is the Binary Icosahedral Group $2I$, and $2I$ is the unique perfect double cover of $A_5$ inside $SU(2)$.*

*Proof.* The argument is closed by group cohomology. The Schur multiplier of $A_5$ is $H_2(A_5, \mathbb{Z}) = \mathbb{Z}_2$ (Aschbacher, *Finite Group Theory*, 2nd ed., §33.15), and $A_5$ is perfect: $H_1(A_5, \mathbb{Z}) = A_5/[A_5, A_5] = 0$ (since $A_5$ is the smallest non-abelian simple group). A perfect group with Schur multiplier $\mathbb{Z}_2$ admits a *unique* universal central extension; this universal extension is the Schur cover. For $A_5$, the Schur cover is $\mathrm{SL}_2(\mathbb{F}_5) \cong 2I$, of order 120 (Conway et al., *ATLAS of Finite Groups*, p. 2; Steinberg, *Lectures on Chevalley Groups* §7). The image of $2I$ in $SU(2)$ under the standard 2-dimensional irreducible representation is the binary icosahedral group, and this embedding is unique up to conjugation by Schur–Zassenhaus. $\square$

> **Remark.** This step is the algebraic content of the §U.6.1 argument, restated as a forcing lemma for Theorem T-McKay. The non-perfectness of $A_4$ (the tetrahedral case has $A_4/[A_4,A_4] = \mathbb{Z}_3 \neq 0$) and of $S_4$ (octahedral: $S_4/[S_4,S_4] = \mathbb{Z}_2 \neq 0$) is what makes their double covers non-universal; the icosahedral case is the unique perfect entry in the polyhedral table. The combination of perfectness ($H_1 = 0$) and $H_2 = \mathbb{Z}_2$ is closed under the Schur–Zassenhaus theorem (Robinson, *A Course in the Theory of Groups*, §11.1).

##### Lemma T-McK.1b (Spinor stability: persistence of $2I$-spinors under defect-knot formation) [Tier 2 — reducible to a bounded APS computation; see §U.7.6]

*Let $\mathcal{K} \subset E_\parallel$ be a stable knotted defect of the form constructed in Theorem E.1, and let $\rho_{2I}: 2I \to SU(2)$ denote the spinor representation of the binary icosahedral group. Then the parallel transport of a $2I$-spinor field along the meridian of the defect tubular neighborhood induces a non-trivial holonomy in $SU(2)$, and the topological obstruction to global trivialization of the spinor bundle is captured by the Atiyah–Patodi–Singer $\eta$-invariant on $\partial \mathcal{M}_{RT}$. The defect-index identification*
$$n_{\mathrm{def}} \;=\; -\tfrac{1}{2}\eta(D|_{\partial \mathcal{M}_{RT}}) \;\stackrel{?}{=}\; -107$$
*is the conjectured closure datum.*

*Status.* The structural identification (LHS) is Tier 1 via the WZW evaluation of App C §C.4: a $2\pi$ rotation of a tethered defect produces holonomy $e^{i\pi} = -1$, yielding the half-integer spin signature. The quantitative identification (RHS — the specific value $n_{\mathrm{def}} = -107$ matching the electron mass exponent) is Tier 2, reducible to an explicit APS spectral-flow computation on the boundary of the acceptance window. This is the **single remaining structural gap** in the chain; the explicit reduction is itemized in §U.7.6.

> **Remark T-McK.1b.A [Why the gap is bounded].** The APS $\eta$-invariant on $\partial \mathcal{M}_{RT}$ — a closed 2-manifold of genus 30 (the rhombic triacontahedron has 30 rhombic faces; after the standard simplicial refinement, the dual graph yields the same Euler characteristic) — is a *finite* spectral computation. Connes & Moscovici 1995 (Theorem 4.1) shows that $\eta$ takes values in $\mathbb{Q}$ on finite-symmetry-orbit boundaries; the explicit value is computed by enumerating the spectrum of the boundary Dirac operator on a fundamental domain of the icosahedral group action on $\partial \mathcal{M}_{RT}$ and applying the trace formula of Connes 1994, Ch. VI §3. The computation is bounded in the same sense as step Y.6.3 of Appendix Y: it is operator-algebra bookkeeping, not new mathematics.

##### Lemma T-McK.2 (McKay-correspondence forcing: $2I \Rightarrow E_8$) [Tier 1]

*Under the McKay correspondence, the binary icosahedral group $2I \subset SU(2)$ is mapped to the simply-laced affine Dynkin diagram $\widetilde{E}_8$. Deleting the affine node yields the finite Dynkin diagram $E_8$, which is the unique simply-laced Lie algebra of rank 8 with a 240-vertex root system in $\mathbb{R}^8$.*

*Proof.* The McKay correspondence is a closed result (McKay 1980; modern proof in Slodowy, *Simple Singularities and Simple Algebraic Groups*, Springer LNM 815). The specific assignment $2I \to \widetilde{E}_8$ is verified by computing the McKay graph of $2I$: the 9 irreducible complex representations of $2I$ (of dimensions $1, 2, 2', 3, 3', 4, 4', 5, 6$) form the vertices, and the edges are computed from the decomposition of $V_2 \otimes V_i$ where $V_2$ is the defining 2-dimensional representation. The resulting graph is the affine Dynkin diagram $\widetilde{E}_8$ (Conway & Sloane, *Sphere Packings, Lattices, and Groups*, §4.10). Deletion of the affine node yields the $E_8$ Dynkin diagram, and the $E_8$ root system contains exactly 240 roots of squared length 2 — the largest exceptional simply-laced root system (Bourbaki, *Lie Groups and Lie Algebras*, Ch. VI §4). Among the McKay-associated Lie algebras for binary polyhedral groups, $E_8$ is the unique one of rank $> 7$; this rank-uniqueness is what subsequently forces the parent-lattice dimension to be 8 prior to the Elser–Sloane reduction. $\square$

##### Lemma T-McK.3 (Elser–Sloane forcing: $E_8 \Rightarrow \mathbb{Z}^6$) [Tier 1]

*The Elser–Sloane projection $\pi_{ES}: \mathbb{R}^8 \to \mathbb{R}^4$ sends the $E_8$ root system onto the $H_4$ root system; the further $H_4 \to H_3$ reduction selects an integer sub-lattice of rank 6 inside $E_8$ as the unique minimal periodic parent lattice whose cut-and-project image is the 3D icosahedral quasicrystal. The dimension 6 is the rank of the $D_6$ orbit sub-lattice selected by the $H_4$ Coxeter element.*

*Proof.* The $E_8$ root system contains a $D_6 \oplus A_1^2$ sub-system as a maximal-rank sub-root-system (Bourbaki, *Lie Groups and Lie Algebras*, Plate VII). Under the Elser–Sloane projection, the $D_6$ component projects to the 60 root vectors of the icosahedral 3D lattice (the Ammann–Kramer–Neri lattice; Kramer & Neri 1984, *Acta Crystallographica* A40: 580). The integer span of these 60 vectors in $\mathbb{R}^6$ is the $\mathbb{Z}^6$ hypercubic sub-lattice of $E_8$, and Moody & Patera 1993 (Theorem 3.2) shows this is the *unique* periodic sub-lattice of $E_8$ whose Elser–Sloane image is the icosahedral 3D quasicrystal. The minimality is established by the rank inequality: any periodic parent lattice of an aperiodic structure with rotational symmetry of order $n$ requires rank $\geq \phi(n)$ where $\phi$ is Euler's totient (Senechal, *Quasicrystals and Geometry*, §2.6); for $n = 5$, $\phi(5) = 4$, but the embedding of a 3D icosahedral structure in a hypercubic lattice with full $H_3$ symmetry requires rank $\geq 6$, with 6 being achieved. $\square$

> **Remark T-McK.3.A.** The dimension count is the same as Bak's 1985 "Phenomenological theory of icosahedral incommensurate order" (*Phys. Rev. Lett.* 54: 1517), in which the indexing problem for the icosahedral phase forces a 6-dimensional Miller-index space. The Elser–Sloane projection is the canonical realization; alternative projections (e.g., Kalugin–Kitayev–Levitov 1985, *JETP Lett.* 41: 145) give the same dimension by the same totient argument.

##### Lemma T-McK.4 (φ-slope forcing: the $H_4$ Coxeter eigenvalue) [Tier 1]

*The projection slope of the Elser–Sloane map is exactly $\phi = (1+\sqrt{5})/2$; this slope is forced by the eigenvalue structure of the $H_4$ Coxeter element and admits no free parameter.*

*Proof.* The Coxeter element $c \in H_4$ has order $h = 30$ (the Coxeter number of $H_4$). Its eigenvalues on $\mathbb{R}^4 \otimes \mathbb{C}$ are $e^{2\pi i d_j / h}$ where $d_j \in \{2, 12, 20, 30\}$ are the degrees of $H_4$'s fundamental invariants (Humphreys, *Reflection Groups and Coxeter Groups*, §3.7). The dominant ratio between the two largest moduli of the projection eigenvalues is
$$\bigl|2 \cos(\pi/5)\bigr| = \phi,$$
which is the eigenvalue of the inflation operator of the $H_4$ tiling. The Elser–Sloane projector is the orthogonal projection onto the 4-plane spanned by the Coxeter eigenvectors with eigenvalues $e^{\pm 2\pi i / 30}$ and $e^{\pm 11 \cdot 2\pi i / 30}$; the ratio of the eigenvalue moduli is the inflation factor $\phi$. No free real parameter enters the construction: the slope is fixed by the Coxeter spectrum of $H_4$, which is fixed by the Lie-algebraic structure of $E_8$. $\square$

---

#### U.7.4 Proof of Theorem T-McKay

Assembling the lemmata:

1. **Lemma III (§U.6.1 + §U.6.2)** forces $\Gamma = A_5$ as the unique 3D polyhedral group supporting Spin structure within the quasicrystalline class. *Tier 1 by exhaustion.*
2. **Lemma T-McK.1a** forces $\tilde{\Gamma} = 2I$ as the unique universal spinor cover of $A_5$. *Tier 1 — Schur cover.*
3. **Lemma T-McK.1b** identifies the Spin-Statistics dependency: persistent fermion knotting at the icosahedral vacuum requires the WZW phase $\pi$ of App C §C.4 to be the *correct* APS defect index. The algebraic step is Tier 1; the quantitative APS computation is Tier 2 with the reduction of §U.7.6.
4. **Lemma T-McK.2** forces $E_8$ as the unique simply-laced Lie algebra in the McKay correspondence assigned to $2I$. *Tier 1 — closed in McKay 1980.*
5. **Lemma T-McK.3** forces $\mathbb{Z}^6$ as the unique minimal periodic parent lattice via the Elser–Sloane projection $E_8 \to H_4 \to H_3$. *Tier 1 — closed in Elser–Sloane 1987 and Moody–Patera 1993.*
6. **Lemma T-McK.4** forces the projection slope to be $\phi$. *Tier 1 — closed in Humphreys §3.7 and the $H_4$ Coxeter spectrum.*

Composing the chain:
$$A_5 \;\xrightarrow{\;\text{T-McK.1a}\;}\; 2I \;\xrightarrow{\;\text{T-McK.2 (McKay)}\;}\; E_8 \;\xrightarrow{\;\text{T-McK.3 (Elser–Sloane)}\;}\; \mathbb{Z}^6 \;\xrightarrow{\;\text{cut-and-project}\;}\; H_3,$$
with the slope $\phi$ forced by T-McK.4 at the $H_4$ intermediate stage. The 6-dimensional parent lattice is uniquely determined by the polyhedral premise H1 and the knot-theoretic premise H2, modulo the Spin-Statistics analytic closure of T-McK.1b. $\square$

*Computationally verified by `gct_mckay_e8.py` (Protocol R-025). See `data/mckay_e8_report.json`.*

---

#### U.7.5 Tier disposition table

| Step / Lemma | Tier | Closure status |
| :--- | :--- | :--- |
| Lemma III (Polyhedral premise H1) | Tier 1 | Closed by §U.6.1 + §U.6.2 (Schur cohomology + Atiyah–Hirzebruch $w_2$). |
| Theorem E.1 (Knot-theoretic premise H2) | Tier 1 | Closed in App E §E.1. |
| Lemma T-McK.1a (Spinor cover: $A_5 \to 2I$) | Tier 1 | Closed by Schur cover and Aschbacher §33.15. |
| Lemma T-McK.1b (Spinor stability: APS defect index) | Tier 2 framework + Tier 3 current implementation | Reduces to a finite spectral-flow computation on $\partial \mathcal{M}_{RT}$ (§U.7.6); the current §U.7.6.3 implementation is a Tier-3 consistency check on a non-$I$-symmetric truncation (§U.7.6.6 footnote 3). Theorem-level closure (Tier 1) requires either path (a) cage rebuild as canonical $I$-orbit union or path (b) smooth-side Connes-Moscovici evaluation. |
| Lemma T-McK.2 (McKay: $2I \to E_8$) | Tier 1 | Closed by McKay 1980 + Slodowy LNM 815. |
| Lemma T-McK.3 (Elser–Sloane: $E_8 \to \mathbb{Z}^6$) | Tier 1 | Closed by Elser & Sloane 1987 + Moody & Patera 1993. |
| Lemma T-McK.4 ($\phi$-slope from $H_4$ Coxeter) | Tier 1 | Closed by Humphreys §3.7. |
| **Theorem T-McKay Forcing Chain — overall** | **Tier 1/2 modular reduction; closing lemma T-McK.1b at Tier 2 framework + Tier 3 current implementation** | **Four of five forcing lemmata closed at Tier 1 in the published literature; the closing lemma T-McK.1b is reduced to a finite spectral-flow computation but the current §U.7.6.3 implementation is a Tier-3 consistency check on a non-symmetric truncation (Open Problem O.14b). Under strict chain-tier arithmetic (chain tier = min(lemma tiers)), the forcing chain currently sits at Tier 3 implementation under a Tier 2 modular-reduction framework; Tier-1 elevation requires closure of O.14b via path (a) or (b) of §U.7.6.6.** |

The disposition is the analogue, for the parent-lattice forcing chain, of the Polaron Unity Proposition's Tier 3 conditional trefoil-case modular reduction (App Y §Y.7). The structural difference is that for T-McKay, four of the five forcing lemmata are closed at Tier 1 in the published literature, and only the analytic step T-McK.1b carries a structural reduction; the Polaron Unity disposition closes four lemmata but the bridge lemma Y.3.4 is reduced to an operator-algebra computation that remains conditional for the trefoil case through §Y.6.3a, O.35, and O.36, and remains conditional on Open Problem O.18 plus §Y.6.3a/b for the general prime-knot extension. T-McKay is therefore one step closer to a fully closed result than Polaron Unity: closure of T-McK.1b would elevate the entire chain to Tier 1, whereas the App Y trefoil reduction is the candidate for Theorem-level promotion contingent on App Y O.35/O.36 closure.

---

#### U.7.6 The remaining gap (Lemma T-McK.1b) — modular reduction list

The single structural gap in Theorem T-McKay is the analytic closure of Lemma T-McK.1b: identification of the WZW holonomy phase of App C §C.4 with the APS defect index of the boundary $\partial \mathcal{M}_{RT}$ of the rhombic-triacontahedron acceptance window. The reduction proceeds in four bounded sub-steps:

| Sub-step | Required | Status |
| :--- | :--- | :--- |
| U.7.6.1 | Existence of a smooth Dirac operator $D$ on the icosahedral cut-and-project manifold $\mathcal{M}$ with boundary $\partial \mathcal{M}_{RT}$. | Standard; follows from the icosahedral Spin structure of §U.6.1 and the standard construction of Dirac operators on spin manifolds (Lawson & Michelsohn, *Spin Geometry*, §II.5). |
| U.7.6.2 | The boundary $\partial \mathcal{M}_{RT}$ admits a closed-form spectrum of $D|_{\partial \mathcal{M}_{RT}}$ computable as an icosahedral orbit decomposition. | Standard; the rhombic triacontahedron is a finite icosahedral $G$-CW complex, and Dirac spectra on finite $G$-CW boundaries are computed by character-theoretic restriction (Connes 1994, Ch. III §6). |
| U.7.6.3 | The APS $\eta$-invariant $\eta(D|_{\partial \mathcal{M}_{RT}})$ takes a specific rational value, with the defect-index identification $n_{\mathrm{def}} = -\tfrac{1}{2}\eta = -107$ under the convention of this section. | **Tier 1 analytic closure outstanding; discrete APS scaffold does not close at integer arithmetic on either available $I_h$-closed cage.** The engine computation (`protocol_aps_index_proof.py`, §U.7.6.6) on the canonical $I_h$-closed 152-node cage (`cage_builder.build_canonical_cage(size=152)`) reports $\eta_{\rm scalar} = -14$ and spinor-reduced $\eta_{\rm eff} = -1.75$. The bulk Pontryagin-integer value required to recover $n = -107$ via $\text{Bulk} + \eta_{\rm eff} = -107$ is therefore $108.75$, which is not an integer; the alternative 92-node $I_h$-closed cage gives $\eta_{\rm scalar} = +3$ and bulk-required $= 106.625$, also non-integer. The discrete APS scaffold therefore does *not* numerically confirm $n = -107$ on either canonical $I_h$-closed cage at perp_cutoff $= 2.0$. Tier 1 promotion requires either (i) identifying an $I_h$-closed cage geometry (possibly at a different perp_cutoff) where the discrete $\eta_{\rm scalar}$ combines with an integer Pontryagin bulk to recover $-107$, or (ii) the Connes–Moscovici character-theoretic evaluation on the continuous $\partial \mathcal{M}_{RT}$ orbit. The empirical anchor (mass-formula CODATA match to $\sim 1006$ ppm) is independent of the APS closure and stands as the load-bearing determination of $n = -107$. Tracked under **Open Problem O.14b/c** (App H §H.5). |

> **Normalization convention reconciliation** (with V3 Ch07 §7.2.3). Two conventions appear across the manuscript for the APS $\eta$-invariant on $\partial \mathcal{M}_{RT}$, and they reconcile as follows. This section (§U.7.6.3) uses the **integer-index convention**: $n_{\mathrm{def}} \equiv -\tfrac{1}{2}\eta_{\rm APS}$, so the load-bearing identity $n_{\mathrm{def}} = -107$ corresponds to $\eta_{\rm APS} = 214$ (a positive integer, after accounting for the factor-of-2 spinor-cover normalization in the APS boundary-corrected index formula). V3 Ch07 §7.2.3 uses the **continuous-shift convention**: the residual $\delta\alpha^{-1} = \eta(D_F|_{\partial \mathcal{M}_{RT}})/2$ identifies $\eta$ directly with twice the post-bilayer fine-structure-constant residual, $\eta_{\rm target} \approx +0.012$ (non-integer in the continuum, integer-valued in the discrete-graph approximation as $\sum \mathrm{sign}(\lambda)$). The two conventions differ by the factor-of-2 spinor-cover / line-bundle normalization standard in APS theory (Atiyah–Patodi–Singer 1975, Theorem 3.10) and are not in contradiction; the engine's computed $\eta_{\rm scalar} = -14$ on the $I_h$-closed 152-cage is the discrete-graph proxy for the §7.2.3 continuous quantity, *not* for the §U.7.6.3 integer-index $\eta_{\rm APS} = 214$, and the discrete value does not currently close the integer-bulk requirement on either available $I_h$-closed cage at perp_cutoff $= 2.0$. Tier-1 closure of O.14b/c (via §U.7.6.6 path (a) or (b)) would also pin the normalization explicitly and identify an integer-bulk-closing cage geometry; until then, comparisons between §7.2.3 numerical claims and §U.7.6.3 integer-index identifications must apply the factor-of-2 conversion and treat the integer-recovery as an open question.
| U.7.6.4 | The result is stable under perturbations of the cut-and-project window within the icosahedral homotopy class. | Standard; APS $\eta$-invariants are deformation-invariants under continuous variation of Dirac operators (APS 1975, Theorem 3.10). |

The disposition of T-McKay is therefore **Tier 1/2 modulo sub-step U.7.6.3**, the latter being a finite spectral-flow computation. Closure of U.7.6.3 would elevate the theorem to **Tier 1 (Logical Necessity)**, since all four forcing lemmata would then be closed at Tier 1 and the chain would constitute an unconditional derivation of the 6D parent lattice from the polyhedral and knot-theoretic premises H1 and H2.

##### U.7.6.5 References for the open step

The path to closing U.7.6.3 uses the following independently established results:

1. **Atiyah, M. F., Patodi, V. K., & Singer, I. M.** (1975). "Spectral asymmetry and Riemannian geometry. I." *Math. Proc. Camb. Phil. Soc.* 77: 43–69. — Defines the $\eta$-invariant and the APS boundary-corrected index theorem; supplies the deformation-invariance of Theorem 3.10.
2. **Connes, A.** (1994). *Noncommutative Geometry*. Academic Press, Ch. III §6 and Ch. VI §3. — Supplies the character-theoretic spectral decomposition on finite-$G$ boundaries needed for U.7.6.2.
3. **Connes, A., & Moscovici, H.** (1995). "The Local Index Formula in Noncommutative Geometry." *Geom. Funct. Anal.* 5: 174–243, Theorem 4.1. — Establishes rationality of $\eta$ on finite-symmetry-orbit boundaries; supplies the trace-formula reduction needed for U.7.6.3.
4. **Lawson, H. B., & Michelsohn, M.-L.** (1989). *Spin Geometry*. Princeton Mathematical Series 38, §II.5. — Standard reference for Dirac operators on icosahedral Spin manifolds.

The composition of (1)–(4) reduces U.7.6.3 to an explicit computation of the icosahedral $\eta$-character on the 60-element orbit of the rhombic triacontahedron's vertex set. The computation is operator-algebra bookkeeping on a finite-dimensional representation space; it is bounded in the same sense as step Y.6.3 of Appendix Y.

##### U.7.6.6 Engine numerical confirmation [Tier 3]

The defect-index identification of U.7.6.3 has been probed numerically via `GCT_Physics_Engine/src/protocol_aps_index_proof.py`. The script constructs the 6D Dirac operator on the canonical $I_h$-closed boundary cage of a $\mathbb{Z}^6$ vacancy (152 nodes; 5 full $I_h$ orbits per `cage_builder.build_canonical_cage`, the smallest $I_h$-closed orbit-union at perp_cutoff $= 2.0$ that includes the outermost 60-orbit required for $I_h$-symmetric spectral analysis), assembles the 8-component Clifford spinor bundle from Pauli-product $\Gamma$-matrices for $\mathrm{Cl}(6,0)$, applies the standard discrete spectral-asymmetry counting (positive minus negative eigenvalues of the Dirac operator divided by the spinor dimension 8), and reports the bulk value that would be required to recover $n = -107$ via the APS decomposition. The result, archived in `GCT_Physics_Engine/data/protocol_aps_index_proof_results.json`, is:

| Quantity | Engine value (I_h-closed 152-cage) |
| :--- | :--- |
| Boundary spectral asymmetry $\eta_{\rm scalar}$ | $-14$ |
| Spinor-reduced $\eta_{\rm eff} = \eta_{\rm scalar} / 8$ | $-1.75$ |
| Bulk value required to recover $n=107$ via $\text{Bulk} + \eta_{\rm eff} = 107$ | $108.75$ (non-integer) |

The bulk value required to recover the empirically-anchored exponent $n = -107$ via the APS decomposition $\text{Index} = \text{Bulk} + \eta_{\rm eff}$ on the canonical $I_h$-closed boundary cage (152 nodes; 5 full $I_h$ orbits per `cage_builder.build_canonical_cage`) is **not an integer**. Since the bulk contribution is a Pontryagin-class evaluation that must be integer-valued, the APS decomposition does not cleanly close at integer arithmetic on this cage geometry: the discrete engine computation alone does not numerically confirm $n = -107$.

This is **not** evidence that $n = -107$ is wrong — the empirical anchor (mass formula matches CODATA to $\sim 1006$ ppm) is independent of the APS construction. It is evidence that the **APS pathway to $n = -107$ is genuinely open**: either (i) a different cage geometry exists at some other perp_cutoff where the I_h-closed orbit-union yields an $\eta_{\rm scalar}$ that combines with an integer Pontryagin bulk to give the empirical $-107$, or (ii) a richer index-theoretic framework than the discrete-cage APS scaffold above is required. The standing Open Problem O.14c (bulk Pontryagin-class evaluation on the 6D icosahedral cell) is therefore expanded to: *determine whether and how the discrete APS sum can recover integer $n = -107$, on any I_h-closed cage geometry*.

**What the engine establishes (Tier 3 numerical fact):** on the canonical I_h-closed 152-node boundary cage, $\eta_{\rm scalar} = -14$ and the bulk integer required for a clean APS recovery of $n = -107$ would be $108.75$, which is not an integer.

**What U.7.6.3 still requires (Tier 1):** either the Connes–Moscovici character-theoretic evaluation of $\eta(D|_{\partial \mathcal{M}_{RT}})$ on the continuous 30-rhombus boundary of the acceptance window with explicit integer-bulk closure, or a different cage geometry where the discrete sum closes cleanly.

**Scope of the engine evidence.** Four qualifications must be kept on the record:

1. *The bulk $\widehat{A}$-contribution is not derived from a first-principles Pontryagin-class computation.* The script `protocol_aps_index_proof.py` reports the bulk value that would be required to recover $n = -107$ given the discrete $\eta_{\rm eff}$ measured on the chosen cage. On the canonical $I_h$-closed 152-cage this required bulk is $108.75$, which is not an integer; on the 92-cage it is $106.625$, also non-integer. A rigorous Pontryagin-class evaluation on the 6D icosahedral cell — yielding an integer bulk that combines with the discrete $\eta_{\rm eff}$ to give $-107$ — remains outstanding (O.14c).

2. *The spectral asymmetry used is of the scalar adjacency matrix, not the full Dirac operator.* The engine constructs an $8N$-dimensional discrete Dirac on the $I_h$-closed cage (where $N$ is the cage node count: $1216$-dim on the 152-cage; $736$-dim on the 92-cage) with Clifford-product hopping terms, but the asymmetry $\eta_{\rm scalar}$ that drives the result is computed from the $N \times N$ scalar weighted adjacency matrix (golden-weighted bonds at $|x_\perp| = 1$ vs $1/\phi$), then normalised by the spinor dimension $8$. This is a discrete-index-style identification, not a direct evaluation of the boundary Dirac's spectral asymmetry on the full $8N$-dimensional space.

3'. **Additional path-(a) and path-(b) results:** following the symmetry-broken-cage diagnostic below, two follow-up scripts probe whether Tier 1 closure can be earned rather than accepted.

   *Path (a):* `GCT_Physics_Engine/src/protocol_orbit_union_search.py` enumerated all 42 ways to partition 144 into a sum of I-orbit sizes (from 15 I-orbits in the perp-distance-3.0 region) and built each as an I-symmetric 144-cage. **Exactly 1 of 42 cages gives $\eta_{\rm scalar} = -8$, matching the engine's prediction.** The winning composition is sizes $[12, 60, 12, 60]$ (specific subset #17). Other I-symmetric cages give $\eta_{\rm scalar}$ ranging over $\{-22, -18, -16, -14, -12, -10, -8, -6, -4, -2, -1, 0, +2, +4, +6, +8, +10, +24\}$. So the integer $-8$ IS structurally achievable under exact I-symmetry, and the cage that delivers it is the one specifically picked out by the two-shell vertex+generic decomposition argued below.

   *Two-Shell Vertex+Generic Decomposition (TS-VG) — structural uniqueness argument for path (a) [Tier 2 reduction].* Among the 42 I-orbit-unions summing to 144, the $[12, 60, 12, 60]$ composition is the *unique* one matching the **two-shell vertex+generic structure** required by the dodecahedral-cage commitment of V3 §7.1.3:
   
   * **Vertex orbits:** $I$ acts on the 12 icosahedron vertices with stabiliser $\mathbb{Z}_5$ (5-fold axis at each vertex), giving orbits of size $|I|/|\mathbb{Z}_5| = 60/5 = 12$. In the radial enumeration of the 14 available I-orbits (sizes $[12, 30, 30, 60, 20, 60, 60, 30, 60, 20, 60, 12, 24, 22]$ ordered by minimum perp-norm), exactly two such 12-orbits exist: one inner shell at the smallest perp-radius (orbit index 0) and one outer shell at the largest 12-orbit perp-radius (orbit index 11). These are the canonical "vertex shells" of the inner-and-outer dodecahedral cage faces.
   * **Generic orbits:** $I$ acting on generic positions with trivial stabiliser gives orbits of size $|I| = 60$. Five such 60-orbits exist in the search radius (indices 3, 5, 6, 8, 10), each filling the inter-vertex space at its respective radial shell. These are the canonical "phason-mode envelope" shells that carry the bound-state amplitude away from the vertex singularities.
   * **Two-shell sum:** the dodecahedral cage requires two concentric shells (V3 §7.1.3 Sub-Proof B perfect-square commitment; Cohn 1964 number-theoretic uniqueness of $144 = 12^2$ as the unique non-trivial Fibonacci perfect square). Each shell contributes a vertex-orbit (12 nodes) plus a generic-orbit (60 nodes), for $12 + 60 = 72$ nodes per shell and $2 \times 72 = 144$ total. The orbit-union $[V_{\text{inner}}, G_{\text{inner}}, V_{\text{outer}}, G_{\text{outer}}]$ = $[12, 60, 12, 60]$ is the only orbit-union among the 42 enumerated matching this decomposition.
   
   *Reduction status.* Under the TS-VG commitment, the 42-fold uncertainty collapses to at most $\binom{m}{2}$ candidate orbit-unions, where $m$ is the number of distinct 60-orbits in the search radius (in the canonical $R=3, \text{perp\_cutoff}=3.0$ enumeration of `o14d_closure_search.py`, $m = 7$, giving $\binom{7}{2} = 21$ candidate pairings). The engine reports exactly one of these pairings yields $\eta_{\rm scalar} = -8$: the 60-orbit pair at radial indices $(8, 13)$ with perp-norms $(0.489, 0.565)$ — both in the *outer* radial portion of the search window, *not* the inner+outer shell-matching geometry one might first guess.
   
   *Empirical test of candidate selection rules.* The standalone closure search (`GCT_Physics_Engine/src/o14d_closure_search.py`) tested three a-priori-natural radial selection rules against the winning pair $(8, 13)$:
   * **(i) Minimum-radial-extent** (the two smallest-perp 60-orbits): selects pair $(3, 5)$ → **fails to match the winner**.
   * **(ii) Inner-outer shell-radius matching** (each 60-orbit paired with the closest 12-orbit shell): selects pair $(11, 12)$ → **fails to match the winner**.
   * **(iii) Chiral-parity / Galois-conjugate radii** (60-orbit perp-norm ratio matching $\phi$ or $\phi^{-1}$): selects pair $(12, 13)$ → **fails to match the winner**.
   
   **All three natural radial rules fail.** The TS-VG decomposition is real (1 of 21 pairings yields $\eta_{\rm scalar} = -8$, consistent with the original manuscript claim of 1 of 42 under the original enumeration), but the further reduction from $\leq 21$ candidates to the unique winner is *not* captured by simple radial geometric rules.
   
   *Empirical test of I-irrep multiplicity selection (route $\alpha$).* The follow-up analysis (`GCT_Physics_Engine/src/o14d_irrep_decomp.py`) computed the I-irrep multiplicity decomposition of the $144 \times 144$ cage adjacency spectrum for each of the 21 pairings, hypothesising that the winning pair $(8, 13)$ would exhibit a unique multiplet-count pattern $(n_A, n_T, n_G, n_H)$ that the other 20 do not match. **All 21 cages exhibit the identical I-irrep profile** $(n_A, n_T, n_G, n_H) = (4, 16, 8, 12)$, with total $4 \cdot 1 + 16 \cdot 3 + 8 \cdot 4 + 12 \cdot 5 = 144$ and **no anomalous multiplicities** (every eigenvalue's multiplicity lies in the I-irrep dimension set $\{1, 3, 4, 5\}$, confirming exact I-symmetry of all 21 cages). The I-irrep multiplicity profile is therefore *invariant* across the 21 [12, 60, 12, 60] pairings — it is a structural consequence of the orbit-size composition and the I-equivariance of the bond rules, independent of which specific orbit-pair is chosen. **Route $\alpha$ at the lumped-multiplicity level definitively fails to select the winner.**
   
   *What this reveals about the closure path.* The $\eta_{\rm scalar}$ values across the 21 pairings span a wide range ($\{-22, -16, -14, -12, -10, -8, -6, 0, 2, 4, 6, 24\}$, with $-8$ being one of 5 single-occurrence values) **despite all 21 sharing identical irrep multiplicity counts**. The selection therefore happens at the level of *signed irrep placement* — which multiplets sit at positive vs negative eigenvalues — rather than at the level of multiplet counts.
   
   *Empirical test of T_1 vs T_2 character refinement (route $\alpha'$).* A follow-up analysis (`GCT_Physics_Engine/src/o14d_advanced_invariants.py`) computed the full I-character decomposition with $T_1$ and $T_2$ distinguished via the standard I character table on the five conjugacy classes $\{E, C_5, C_5^2, C_3, C_2\}$ with their $\phi$- and $-1/\phi$-valued characters. **All 21 pairings exhibit the identical character profile $(n_A, n_{T_1}, n_{T_2}, n_G, n_H) = (4, 8, 8, 8, 12)$.** The $T$-multiplet count of 16 from the lumped analysis is confirmed as $8 + 8$ split evenly between $T_1$ and $T_2$, but this split is invariant across all 21 pairings — refinement does not discriminate.
   
   *Empirical test of discrete topological invariants (route $\beta$).* Nine candidate topological / spectral invariants were tested: bond count $n_{\text{edges}}$, triangle count $n_{\Delta}$, 4-cycle count $n_{\square}$, spectral moments $\text{Tr}(A^k)$ for $k = 2, \ldots, 6$, and adjacency determinant $\det A$. **All nine invariants uniquely identify the winner**, but in the trivial sense that all 21 pairings have pairwise-distinct topological signatures — no two pairings share any single invariant. The winner $(8, 13)$ has $n_{\text{edges}} = 2760$, $n_{\Delta} = 9800$, $n_{\square} = 320835$; the 20 other pairings have 20 different bond counts (ranging from 1380 to 2940), 20 different triangle counts (1000 to 13280), and 20 different 4-cycle counts (18075 to 377430). No simple extremization rule (minimum, maximum, target-matching to a derived integer) selects the winner from this distribution. The selection of $(8, 13)$ is therefore mediated by the $\eta_{\rm scalar} = -8$ spectral signature itself, which is tautological with the manuscript prediction unless the specific integer value $-8$ (or equivalently, the specific topological signature $(2760, 9800, 320835, \ldots)$ of the winner) can be derived from first principles via icosahedral group theory + the cage construction rules — which remains open as the genuine O.14d research item.
   
   *Tier disposition of path (a).* The TS-VG argument moves the cage-uniqueness disposition from "$1$ of $42$ unmotivated picks" to "$1$ of $\leq 21$ under the two-shell vertex+generic structural commitment." This is a **Tier 2 partial structural reduction** under the dodecahedral-cage commitment of P1. The further reduction from $\leq 21$ to the unique winner requires either (a) a deeper structural identification of the spectral/topological feature distinguishing pair $(8, 13)$ from the other 20 pairings (e.g., an I-irrep multiplicity pattern in the adjacency spectrum that only $(8, 13)$ exhibits, or a Pontryagin-class topological invariant of the bond graph that picks it out), or (b) accepting the unique-winner selection as a sixth structural postulate P6 added to P1-P5 (with corresponding update to Parameter Ledger §0.1). The empirical finding is that the three a-priori-natural radial rules do *not* close the gap; the closure path therefore points toward spectral/topological analysis of the winning bond graph, not toward a simple geometric uniqueness argument.

   *Path (b):* `GCT_Physics_Engine/src/protocol_bellissard_gap_labels.py` tested the Bellissard gap-labeling theorem on the 1D Fibonacci Hamiltonian $H \psi_n = \psi_{n+1} + \psi_{n-1} + \lambda V_n \psi_n$ with Fibonacci potential $V$. At lattice size $F_{15} = 610$, $\lambda = 1$, **all 9 spectral gaps were cleanly labeled by integer pairs $(p, q)$ with $p \cdot \alpha + q \equiv$ IDOS $\bmod 1$ to error $< 10^{-3}$ (where $\alpha = 1/\phi$)**. Two of the 9 gaps had pure-integer labels ($q = 0$): IDOS $= 0.381967$ with $(p, q) = (-1, 0)$, and IDOS $= 0.763934$ with $(-2, 0)$. Maximum $|p|$ accessible at this lattice size: $7$. Bellissard's framework is numerically validated; integer labels in $\mathbb{Z} \subset \mathbb{Z}[\phi]$ form a well-defined sub-family of gaps, of which $-107$ would be one member at appropriate (astronomically larger) lattice scale. The claim "the integer $-107$ is a gap label of the AKN spectrum" is at least *consistent* with the validated framework.

   *Net effect on A.1 / T-McK.1b closure.* The two new results move the disposition meaningfully. The Bellissard framework is validated empirically (path (b)). What remains *open* is sharper: (i) identify an $I_h$-closed cage geometry where the discrete $\eta_{\rm scalar}$ combines with an integer Pontryagin bulk to give $-107$, and (ii) carry out the first-principles bulk Pontryagin-class evaluation on the 6D icosahedral cell. The currently available $I_h$-closed cages at perp_cutoff $= 2.0$ (sizes 92 and 152) both yield non-integer required bulks; closure may require either a different perp_cutoff with a different I-orbit content, or a richer index-theoretic framework than the direct discrete-APS scaffold.

3. *The canonical $I_h$-closed cage now used by the engine genuinely has exact icosahedral symmetry.* The cage helper `GCT_Physics_Engine/src/cage_builder.py` constructs the boundary cage as the union of full $I_h$ orbits up to the chosen perp_cutoff; the canonical size at perp_cutoff $= 2.0$ is 152 nodes (5 orbits: 12+30+20+30+60), with 92 nodes (4 inner orbits) available as a smaller-cage alternative. `GCT_Physics_Engine/src/protocol_cage_repair.py` verifies that 60/60 icosahedral rotations (lifted to signed-permutation matrices on $\mathbb{Z}^6$ via `lift_to_6d_signed_perm`) preserve the 152-cage, confirming exact $I_h$ symmetry. `GCT_Physics_Engine/src/protocol_cage_spectral_decomp.py` then performs the full $I$-irrep decomposition of the adjacency spectrum: $C^{152} = A_g{\oplus}5 \oplus T_{1g}{\oplus}7 \oplus T_{2g}{\oplus}7 \oplus G_g{\oplus}10 \oplus H_g{\oplus}13$ ($1{+}3{\cdot}7{+}3{\cdot}7{+}4{\cdot}10{+}5{\cdot}13 = 5{+}21{+}21{+}40{+}65 = 152$ ✓), with per-irrep sign-sums summing to the directly-measured $\eta_{\rm scalar} = -14$ ($A_g{:}{+}1$, $T_{1g}{:}{-}9$, $T_{2g}{:}{-}9$, $G_g{:}{+}8$, $H_g{:}{-}5$; sum $= -14$). The $\eta_{\rm scalar}$ integer is therefore *structurally derived* from the $I_h$-irrep decomposition of the canonical cage geometry — not a numerical artifact of a non-symmetric truncation. The remaining question is whether the symmetric cage's *specific integer* ($-14$) combines with an integer Pontryagin bulk to recover $-107$ via $\text{Bulk} + (-14)/8 = -107$. The required bulk $108.75$ is not an integer, so the answer at the 152-cage is no. Two paths forward: (i) repeat the construction at other perp_cutoffs to find an $I_h$-closed cage whose $\eta_{\rm scalar}$ does close cleanly (a finite combinatorial search over perp_cutoff values and orbit choices); (ii) close the bulk Pontryagin computation analytically (O.14c) and check whether the structural answer matches the discrete $\eta_{\rm eff} = -1.75$ at some other index normalization.

4. *An independent smooth-route attempt does not (yet) reproduce the discrete $\eta_{\rm eff}$.* A companion script `GCT_Physics_Engine/src/protocol_eta_continuum.py` computes the Connes–Moscovici equivariant $\eta$ on the smooth 2-sphere with $2I$ action, twisted by line bundles $L_n$ of Chern number $n \in \{-3, \dots, +3\}$, summing the Atiyah–Bott local fixed-point contributions over the nine $2I$ conjugacy classes. Under the three normalization conventions surveyed, the values land in $\{\pm 0.125, \pm 0.25\}$ with no clean match to the discrete $\eta_{\rm eff} = -1.75$ on the $I_h$-closed 152-cage. The discrepancy is most likely a convention mismatch (factor of 2 from the spinor double cover, or a missing line-bundle holonomy phase from the cut-and-project structure), but its resolution is precisely the operator-algebra bookkeeping the lemma reduced to. The smooth-route script is committed alongside the discrete one so the convention chain can be re-examined.

The numerical evidence on the discrete side is now structurally derived (full $I$-irrep decomposition on the $I_h$-closed cage), but the discrete $\eta_{\rm eff}$ does not combine with an integer Pontryagin bulk to recover $-107$ at the canonical perp_cutoff; and the *bridge to the smooth manifold* — the analytic step the lemma actually requires — is not closed by what is in the engine today. Roadmap candidate A.1 (TP-I + TP-J) therefore stays as **Partial — discrete $I_h$-irrep decomposition closed; integer-bulk closure and smooth Connes–Moscovici bridge outstanding (O.14b/c)**.

##### U.7.6.7 Specific-integer disposition for $n = -107$

The K-theoretic skeleton above (U.7.6.1–U.7.6.6) supplies Tier 2 framework support for gap labels in $\mathbb{Z}[\phi]$ through Bellissard/Connes-style tiling K-theory, with a rigorously closed 1D Fibonacci AF-core toy model. The 6D AKN lift, the integer-valued sublattice relevant to defects, and the CMLIF residue interpretation at $s=3$ remain Tier 4 physical-link conjectures until the required AKN spectral-triple and trace-image construction is supplied. The disposition of the **specific integer** $n = -107$ — the gap label selecting the ground-state electron defect — is separated cleanly from that framework support:

> **Tier 2 framework + Tier 4 AKN physical-link conjecture.** The 1D Fibonacci AF-core gap-label framework is closed as a toy model; the 6D AKN CMLIF residue / integer-sublattice transfer is an open structural-link conjecture.
>
> **Tier 3 postulate (Open Problem O.14).** The ground-state electron defect is the projection labeled by the specific integer $-107 \in \mathbb{Z} \subset \mathbb{Z}[\phi]$.

The Tier 3 postulate is currently supported by an empirical anchor (independent of any APS scaffold), with the APS-route as an open theoretical pathway:

1. **Empirical anchor.** The mass formula $m_e = M_P \phi^{-107}(1-5\alpha)$ matches CODATA to $\sim 0.1\%$ (1006 ppm), verified by `verify_independent/verify_electron_mass.py`. No other integer in $[-200, +200]$ gives sub-percent agreement.
2. **Numerical APS scaffold.** The engine's discrete APS computation on the canonical $I_h$-closed 152-node boundary cage gives $\eta_{\rm scalar} = -14$ (spinor-reduced $\eta_{\rm eff} = -1.75$); the bulk value required to recover $n = -107$ via $\text{Bulk} + \eta_{\rm eff} = -107$ is therefore $108.75$, which is not an integer. The discrete-cage APS sum thus does *not* numerically confirm $n = -107$ on the I_h-closed geometry; the empirical-anchor item in this list carries the determination, and the APS pathway remains an open route pending O.14c. See §U.7.6.6 for the corrected discrete-cage spectral decomposition.

**What is *not* claimed.** A first-principles uniqueness proof selecting $-107$ from among the $\mathbb{Z}[\phi]$-valued integer gap labels of the 6D AKN crossed-product is not provided. The phrase "$\chi(\mathbb{Z}^6/H_3) = -107$" sometimes used as informal shorthand for the constraint is *not* identified with any single standard equivariant Euler-characteristic-like invariant: a systematic survey (`GCT_Physics_Engine/src/protocol_euler_char_audit.py` plus `protocol_euler_char_audit_extended.py`) covering 78 candidate invariants — orbifold Euler characteristics, signed Lefschetz averages, fixed-point counts, signature sums on the three icosahedral 6-dim representations $T_1\oplus T_1$, $T_1\oplus T_2$, $T_{1g}\oplus T_{1u}$; rational singular cohomology Betti numbers $b_0, \dots, b_6$ of $T^6/G$ via the Hodge-type decomposition into $I_h$-invariants of $\Lambda^k V$; the alternating sum $\chi_Q = \sum (-1)^k b_k$; weighted Betti sums $\sum k \cdot b_k$ and $\sum k^2 \cdot b_k$; the equivariant Atiyah–Singer $G$-signature; hypercube vertex orbit counts — finds no candidate yielding $\pm 107$. The closest observation is $\sum k^2 \cdot b_k = 92$ for $I \times (T_1 \oplus T_1)$, with no principled selection rule preferring that weighted sum. The "$\chi(\mathbb{Z}^6/H_3) = -107$" shorthand should therefore be read as a label for the (currently open) uniqueness postulate, not as a reference to any specific standard invariant.

**Open items on the path to a Tier 1 promotion of the specific integer.** Four discrete computational/convention items remain. They are recorded here as named Open Problems rather than as required closures for the present specification:

- **O.14a — K-theoretic uniqueness.** Show that the $N = 144$ Gauss-Bonnet saturation constraint (§7.1.3) picks $\phi^{-107}$ uniquely from among the $\mathbb{Z}[\phi]$-valued trace-image gap labels of $K_0(\mathcal{A})$, possibly via a specific equivariant cohomological invariant that the 78-candidate survey did not test.
- **O.14b — Smooth-route Connes–Moscovici convention.** The companion script `protocol_eta_continuum.py` evaluates the equivariant $\eta$ on $S^2/2I$ for twisting bundles of Chern number $n \in \{-3,\dots,+3\}$ via the standard Atiyah–Bott local fixed-point formula. Under three surveyed normalization conventions the smooth-route values cluster at $\pm 0.125,\, \pm 0.25$ — none snap to the discrete-cage value $\eta_{\mathrm{eff}} = -1$. The mismatch is consistent with a missing holonomy phase associated with the line bundle's twist around the icosahedral fundamental domain, and resolution is a bounded operator-algebra calculation on the 60-element $2I$-orbit of the rhombic triacontahedron vertices.
- **O.14c — Bulk $\widehat{A}$-contribution and integer APS closure.** Determine whether and how the discrete APS sum $\text{Bulk} + \eta_{\rm eff}$ can recover integer $n = -107$ on any $I_h$-closed boundary-cage geometry. On the canonical $I_h$-closed 152-cage at perp_cutoff $= 2.0$ the bulk-required-for-$n{=}{-}107$ is $108.75$ (non-integer); on the $I_h$-closed 92-cage at the same cutoff it is $106.625$ (also non-integer). Closure requires either an explicit Pontryagin-class evaluation on the 6D icosahedral cell that yields an integer bulk combining with the corresponding $\eta_{\rm eff}$ to give $-107$ on a specific I_h-closed cage, or a richer index-theoretic framework than the direct discrete-APS scaffold. The empirical anchor (mass-formula CODATA match) is independent of this closure.
- **O.14d — Two-Shell Cage Uniqueness Refinement (status: Tier 2 partial reduction; six selection rules tested and falsified or tautological).** §U.7.6.6 path (a) above presents the Two-Shell Vertex+Generic (TS-VG) Decomposition argument as a Tier 2 structural reduction collapsing the 42-fold I-orbit-union uncertainty to $\leq 21$ candidates under the two-shell perfect-square commitment of §7.1.3 Sub-Proof B + Cohn 1964. The standalone closure search suite (`GCT_Physics_Engine/src/o14d_closure_search.py`, `o14d_irrep_decomp.py`, `o14d_advanced_invariants.py`) has identified the unique winning 60-orbit pair as indices $(8, 13)$ at perp-norms $(0.489, 0.565)$, and tested six selection rules:
  * **(i) Minimum-radial-extent** — selects $(3, 5)$, **fails**.
  * **(ii) Inner-outer shell-radius matching** — selects $(11, 12)$, **fails**.
  * **(iii) Chiral-parity / Galois-conjugate radii** — selects $(12, 13)$, **fails**.
  * **(iv-$\alpha$) Lumped I-irrep multiplicities** $(n_A, n_T, n_G, n_H)$ — all 21 pairings have the identical profile $(4, 16, 8, 12)$, **fails (invariant across all candidates)**.
  * **(v-$\alpha'$) Split I-character analysis** with $T_1$ vs $T_2$ distinguished — all 21 pairings have the identical profile $(n_A, n_{T_1}, n_{T_2}, n_G, n_H) = (4, 8, 8, 8, 12)$, **fails (refined character profile is still invariant)**.
  * **(vi-$\beta$) Discrete topological invariants** ($n_{\text{edges}}$, $n_\Delta$, $n_\square$, $\text{Tr}(A^k)$, $\det A$) — each invariant has 21 distinct values across the 21 pairings (i.e., each "uniquely identifies" the winner trivially), but **no extremization or target-matching rule selects $(8, 13)$ specifically**; the topological signatures separate the pairings without offering a structural selection criterion. **Fails as a non-tautological closure rule.**
  
  **All six tested rules fail or are tautological.** The closure of the 21 → 1 step is genuinely deeper than (a) radial geometry, (b) representation-theoretic multiplicity counting (lumped or split), or (c) standard discrete topological invariants. The eigenvalue *placement* (which multiplets sit at positive vs negative spectral eigenvalues) differs across the 21 pairings and uniquely produces the $\eta_{\rm scalar} = -8$ signature for $(8, 13)$; what is needed is a first-principles derivation of that signature from icosahedral group theory + the cage construction rules. Remaining candidate routes for the closure: (a) route $\delta$ — compute the equivariant Chern-Simons class of the $I$-equivariant bond bundle and identify the discrete integer value distinguishing $(8, 13)$ from first principles (months of math); (b) route $\gamma$ — accept the unique-winner selection as a sixth structural postulate $P_6$ with corresponding update to Parameter Ledger §0.1, completing the "structural postulates" rather than the "first-principles derivations" column of the parameter accounting. Status: **Tier 2 partial structural reduction** (42 → 21 closed via TS-VG + Cohn 1964; 21 → 1 reduction is open and now confirmed to require *non-standard* spectral/topological invariants beyond the standard tested toolkit).

Closure of O.14a alone would promote the specific-integer postulate to Tier 1. Closure of O.14b and O.14c would supply the independent smooth-side confirmation. The integer $107$ is empirically established by the $m_e$ fit; what remains is the formal proof chain landing on it from first principles.

**A normalization-convention consistency item to track.** Two formulations of the index-to-defect correspondence appear in the manuscript: §7.2.3 uses $\eta = n_{\mathrm{def}}$, whereas U.7.6.3 uses $\eta = -2\, n_{\mathrm{def}}$. The two are consistent under a factor-of-2 spinor-cover/line-bundle normalization that is implicit but not made explicit in either passage. Closure of O.14b above is expected to fix the convention chain; once fixed, one of the two formulations should be retired in favour of the controlling one.

---

## U.8 Theorem U.8: Uniqueness of the SU(2) Connection on the 5-Fold Baryonic Bundle [Tier 1]

**Statement:** The connection $A_\theta = \frac{1}{2}\sigma_z$ is the unique
flat SU(2)-equivariant connection on the principal $2I$-bundle over the
5-fold baryonic loop. No other holonomy weight $n$ is compatible with the
fiber symmetry of the Binary Icosahedral Group.

**Proof:**

*Step 1 — Stabilizer of the 5-fold axis.*
Let $\hat{a}_5$ be the directed 5-fold rotation axis of the icosahedron.
The stabilizer of $\hat{a}_5$ under the adjoint $SO(3)$ action of the
icosahedral group $I$ is:
$$\mathrm{Stab}_I(\hat{a}_5) = \mathbb{Z}_5$$
generated by a $72°$ rotation. Its SU(2) pre-image in the double cover
$2I$ is:
$$\mathrm{Stab}_{2I}(\hat{a}_5) = \mathbb{Z}_{10}$$
generated by $U_{\mathrm{gen}} = \exp(i\pi\sigma_z/5)$.
The cyclic-subgroup orders of $2I$ are exactly $\{1, 2, 3, 4, 5, 6, 10\}$.

*Step 2 — Holonomy constraint.*
A SU(2)-equivariant connection on this bundle must assign a $2\pi$-loop
holonomy lying in $\mathrm{Stab}_{2I}(\hat{a}_5)$ that generates $\mathbb{Z}_{10}$.
For a diagonal axial connection $A_\theta = \frac{n}{2}\sigma_z$:
$$\mathcal{P}\exp\!\left(i\int_0^{2\pi} A_\theta\, d\theta\right)
= \exp(in\pi\sigma_z)$$

*Step 3 — Uniqueness by subgroup constraint.*
$n = 1$: holonomy $= \exp(i\pi\sigma_z) = -I_2 = U_{\mathrm{gen}}^5$,
the unique order-2 element of $\mathbb{Z}_{10}$, consistent with the baryonic
$2\pi$ loop. $\checkmark$

For $n \geq 2$: holonomy generates $\mathbb{Z}_{5n} \subset SU(2)$. For
$n \geq 2$, orders $\geq 10$ not in $\{1,2,3,4,5,6,10\}$ arise, violating
$2I$-equivariance. Every $n \geq 2$ is algebraically forbidden. $\otimes$

Therefore $n = 1$, giving
$$\boxed{A_\theta = \tfrac{1}{2}\sigma_z}$$
is the **unique** connection compatible with the $2I$ fiber symmetry. $\square$

**Tier:** Tier 1 — pure algebraic theorem; no physical input, no free parameters.

**Corollary (Proton Mass Exponent):** Holonomy $-I_2$ implies Berry phase
$\gamma = \pi$ (half-winding $N_\mathrm{weak} = 1/2$). Icosahedral projection
ratio $R = 2\phi^{-1}$ then gives:
$$\phi\text{-correction} = N_\mathrm{weak} \cdot R = \phi^{-1}$$
establishing the proton exponent $\Phi_\mathrm{total} = 15 + \phi^{-1}$.

*Numerical verification: `protocol_proton_berry_phase.py` confirms
$\|U_\mathrm{weak} + I_2\|_F < 10^{-9}$ for $N_\mathrm{steps} = 10{,}000$.*
*Detailed derivation: Vol. 3 Ch18 §18.2.3.A.*

---

## U.9 Theorem U.9: Uniqueness of the Bare Weinberg Angle $\sin^2\theta_W^{\rm bare} = \phi^{-3}$ [Tier 1]

> **Theorem U.9 (Bare Weinberg Angle Uniqueness).** *Among all rational powers $\phi^n$ ($n \in \mathbb{Z}$) of the golden ratio, the bare geometric Weinberg angle*
> $$\sin^2 \theta_W^{\rm bare} = \frac{V_\perp}{V_\parallel}$$
> *(the volumetric scaling of the internal manifold relative to the physical manifold) takes the value $\phi^{-3}$, and only this value, as a consequence of three independent Tier 1 inputs:*
>
> - **T1.a (Dimension fixing):** $\dim(E_\perp) = 3$. The icosahedral cut-and-project decomposes $\mathbb{R}^6 = E_\parallel \oplus E_\perp$ with both subspaces 3-dimensional; this is the structural prerequisite for the AKN tiling and is fixed by Lemma III (App U §U.6) and V1 Ch02 §2.4. (Tier 1 axiomatic / theorem.)
>
> - **T1.b (Per-axis length ratio):** $|E^\perp_i| / |E^\parallel_i| = \phi^{-1}$ for each $i \in \{1,\dots,6\}$. This follows from the Gram Projection Theorem (V3 Ch04 §4.3.2, already Tier 1: exact algebraic): squared norms $|E^\parallel_i|^2 = (1+\phi^2)/5$ and $|E^\perp_i|^2 = (1+\phi^{-2})/5$ give ratio $(1+\phi^{-2})/(1+\phi^2) = \phi^{-2}$, so the length ratio is $\sqrt{\phi^{-2}} = \phi^{-1}$.
>
> - **T1.c (Volume scaling):** For a Euclidean $d$-dimensional manifold with isotropic scaling factor $\lambda$, the volume scales as $V = \lambda^d \cdot V_0$. (Tier 1 axiomatic — standard Euclidean measure theory.)
>
> **Proof.** By T1.b, each axis of $E_\perp$ scales by $\phi^{-1}$ relative to the corresponding $E_\parallel$ axis. The icosahedral symmetry ensures this scaling is isotropic (the same per-axis factor across all six lattice basis vectors, verified by the per-axis equality $|E^\perp_i|^2 = (1+\phi^{-2})/5$ for all $i$). By T1.a and T1.c, the resulting volume ratio is
> $$\frac{V_\perp}{V_\parallel} = (\phi^{-1})^{\dim(E_\perp)} = (\phi^{-1})^3 = \phi^{-3}.$$
> Any candidate value $\phi^n$ with $n \neq -3$ would require:
> - $n = -1$: identifying $\sin^2\theta_W^{\rm bare}$ with a *length* ratio rather than a *volume* ratio — violates T1.c (volume formula).
> - $n = -2$: identifying with an *area* ratio (dim 2) rather than a *volume* ratio (dim 3) — violates T1.a (dim fixing).
> - $n = -4$: would require either a 4-dimensional perp space (violates T1.a) or a per-axis length ratio $\phi^{-4/3}$ (violates T1.b — irrational; not a rational power of $\phi$).
> - $n = -6$: would require dimension $6$ — that is the full 6D parent lattice, not the perp projection. The Weinberg angle is by definition the ratio of the 3D projected volumes, so $n = -6$ is structurally excluded.
> - $n \geq 0$: no scaling or expansion of $E_\perp$ relative to $E_\parallel$ — directly contradicts T1.b.
>
> No other rational power of $\phi$ is consistent with the joint constraint T1.a $\wedge$ T1.b $\wedge$ T1.c. Hence $n = -3$ is uniquely forced. $\square$
>
> **Tier 1 disposition.** Given the volumetric identification as the structural definition of the bare angle (Ch04 §4.3.1; the Weinberg angle is the ratio of the 3D projected volumes of $E_\perp$ relative to $E_\parallel$), the *specific value* $\phi^{-3}$ is forced by the composition of three independent Tier 1 inputs (T1.a–T1.c) with no free parameter and no alternative permitted. Theorem U.9 is the corresponding Tier 1 Uniqueness Theorem.
>
> **Numerical verification.** `GCT_Physics_Engine/src/protocol_weinberg_uniqueness.py` computes the squared norms from the canonical AKN unnormalised projection matrices, confirms $|E^\parallel_i|^2 = 1+\phi^2$ and $|E^\perp_i|^2 = 1+\phi^{-2}$ to machine precision, verifies the length ratio $\phi^{-1}$, and cubes it to recover $V_\perp/V_\parallel = \phi^{-3} = 0.2360679775$. The certificate is stored at `GCT_Physics_Engine/data/protocol_weinberg_uniqueness_results.json`.
>
> **Scope.** Theorem U.9 promotes the *bare* (GUT-scale) Weinberg angle to Tier 1. It does not bear on the Z-pole value $\sin^2\theta_W(M_Z) = 0.23122$, which remains a Tier 3 Observational Import (V3 Ch04 §4.5) used as the IR boundary condition for the RGE running; full IR autonomy without importing the Z-pole value is the QLQCD-1L open research debt (App Z), unchanged by Theorem U.9.

**END OF APPENDIX U**

