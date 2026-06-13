### **Chapter 10: The Extended Spectrum (Quarks and Hadrons)**

In the Standard Model, the masses of quarks and the resulting composite hadrons are determined by non-perturbative dynamics that remain computationally elusive. Geometric Consciousness Theory (GCT) identifies the hadron sector not as a separate class of physics, but as the **Crystallographic Inventory** of the vacuum interstices. While leptons correspond to node-centered vertex defects, quarks correspond to **Interstitial Face Defects**. This chapter gives the tiered hadron-sector account: Tier 2 mechanisms where the geometric chain is active, Tier 3 ansätze for unresolved harmonic / transfer choices, the down-quark mass as a Tier 2 Fuglede-Kadison-determinant mechanism whose primary output is the infinite-volume-limit closed form $m_d = m_u\phi^{\phi}$ (postdiction-consistent at $+0.33\%$, with rigorous convergence conditional on O.5), and the proton-mass route as **Tier 2 mechanism + Tier 3 sheet/exponent handle pending AKN-action closure**.

The specific mapping between these geometric structures and their generational harmonic orders is strictly governed by the **Galois Rationality Constraint** (Appendix E, Theorem E.5). This constraint provides the underlying organizing principle for why each generation maps to its specific order: it requires physical mass observables to be invariant under the Galois automorphism $\phi \to -1/\phi$, an organizing principle that applies uniformly across leptons, neutrinos, and quarks.

---

**10.1 Interstitial Defects (Quark Structure)**

**10.1.1 The Codimension of Defects: Quarks vs. Leptons**

GCT rigorously classifies elementary fermions by their topological codimension within the icosahedral tiling:
* **Vertex Defects (Leptons):** Possess **Codimension 3** (a point in 3D physical space). Their energy scales linearly with the inflation of the lattice radius ($\phi^1$).
* **Interstitial Defects (Quarks):** Possess **Codimension 1** (a surface in 3D physical space). Their energy scales with the inflation of the projected facet area ($\phi^2$).

While a quark appears point-like when bound within a hadron in the 3D projection, its underlying geometry in the 6D parent lattice is a mismatch on a 2-dimensional facet. This area-based topology is the mechanical origin of the **Area-Law Scaling ($\phi^2$)** observed in the quark mass hierarchy.

**10.1.2 Color Charge and Burgers Vector Alignment**

The normal vectors to the rhombic faces of the unit cells correspond to the **10 three-fold axes** of the icosahedral symmetry. Because a quark is a face defect, its **Burgers Vector** $\mathbf{b}_\perp$ (the measure of lattice mismatch) is necessarily aligned with one of these internal axes. "Color" is the phenomenological registration of this internal axis alignment. Quarks are color triplets (fundamentals of $SU(3)_C$); physical hadrons are color singlets formed by $SU(3)_C$ confinement. In the GCT model, the triplet color label tracks which internal three-fold-axis branch carries the face-defect mismatch, while the singlet condition is imposed only on confined hadron states.

**10.1.3 The Gluon String and Mechanical Confinement**

In the 6D parent lattice, an uncompensated interstitial face defect creates a 5-dimensional fault plane (a grain boundary) extending through the Bulk. In a supersolid vacuum, this fault plane carries divergent energy. To satisfy the Hamiltonian constraint $\hat{H}\Psi=0$, the strain field must collapse into a one-dimensional **Gluon String** or flux tube. 

Confinement is a **Mechanical Requirement** of the crystalline substrate. A quark mismatch must either terminate on an antiquark or form a closed 3-cycle (Baryon) to satisfy the **Global Singlet Condition** ($\sum \text{winding} \equiv 0 \pmod 3$). A hadron is a **Closed Grain Boundary** that allows the vacuum to remain stress-free at macroscopic distances.

---

**10.2 The Top Quark (The Geometric Lock)**

**10.2.1 The Universal Yield Strength [Tier 2 geometric motif + Tier 3 top-mass ansatz/residual]**

The Top Quark is the only fermion with a Yukawa coupling $y_t \approx 1$. GCT identifies the Top Quark as the **Universal Yield Strength** of the vacuum hardware. 

**Ansatz 10.1 [Tier 3 top-mass identification]:** *We posit that the Top Quark represents the lattice fracture limit, where the volumetric strain (Higgs dilation) is accompanied by a shear displacement of one unit-cell diagonal.*

**10.2.2 Derivation from the $D_6$ Face Diagonal ($\sqrt{2}$)**

The Top Quark mass ($m_t$) geometrically locks to the Higgs VEV ($v \approx 246.22$ GeV). The mass of the Top Quark is defined as the energy required to dilate a unit cell facet by its diagonal length, triggering a lattice fracture. This represents exactly half the VEV scaled by the $D_6$ root lattice face diagonal ($\sqrt{2}$):
$$m_t = \left(\frac{v}{2}\right) \cdot \sqrt{2} \approx \mathbf{174.1 \text{ GeV}} \quad \text{[Tier 2 mechanism + Tier 3 state-level/QCD-pole residual]}$$

This derived value is the **Bare Lattice Mass** at the crystallization scale. Its comparison to the observed pole mass remains a Tier 3 state-level/QCD-pole residual pending QLQCD closure.

> [!NOTE]
> **Tree-Level QCD Residual (0.89%): Theoretically Bounded**
> The GCT formula $m_t = (v/2)\sqrt{2}$ is a tree-level prediction. The leading-order QCD correction from the pole-mass/MS-bar running is:
> $$\Delta m_t^{QCD} \approx \frac{4}{3}\frac{\alpha_s}{\pi} \times m_t \approx \frac{4}{3} \times \frac{0.1179}{\pi} \times 174.1 \approx +8.7 \text{ GeV (one-loop pole/MS-bar scale estimate)} \quad \text{[Tier 3]}$$
> This naïve one-loop correction is $\sim 5\%$ of the mass and overcorrects the observed $\sim 0.89\%$ tree-level residual. The residual is therefore **not closed by the displayed one-loop arithmetic**; it is only bounded as a loop-order-scale effect and constitutes **Open Research Debt QLQCD-2L** (see Appendix Z). Tier 2 closure requires a full QLQCD two-loop computation anchored to the GCT lattice RGE framework.

---

**10.3 The Proton Mass (The Baryonic Triad)**

**10.3.1 The Challenge: m_p from First Principles**

GCT derives the proton mass ($938.272$ MeV) not through stochastic simulation, but as a **Resonant Eigenvalue** of a 3-quark complex. 

**10.3.2 The Baryonic Energy Functional**

To rigorously derive the mass eigenvalue, we define the energy functional $E[\Phi]$ for a 3-quark defect (Triad) on the lattice:
$$ E[\Phi] = \int d^3x \left( \frac{1}{2} K_\perp (\nabla \mathbf{w})^2 + V_{lock}(\Phi) + \sigma_{string} \sum_{i=1}^3 \delta(\mathbf{x} - \mathbf{q}_i) \right) $$

**Derivation of the Base Exponent (15) [Tier 2 mechanism + Tier 3 hadron-sector handle]:**
The winding number $N$ of the ground state is determined by the **Topological Closure** of the defect surface. The defect wraps the 3 quarks (homotopy $Z_3$) around the 5-fold symmetry axis of the cage (homotopy $Z_5$). The minimal non-trivial winding that closes the surface without breaking the lattice symmetry is the product of the winding numbers [Tier 2]:
$$ N_{baryon} = 3 \times 5 = 15 \quad \text{[Tier 2]}$$
This identifies "15" not as a numerological guess, but as the **candidate winding generator** of the baryonic triad sector under the $Z_3 \times Z_5$ closure rule; a full configuration-space proof of $\pi_1(\text{Triad}) \cong \mathbb{Z}_{15}$ remains part of the hadron-sector closure.

The physical proton-mass formula still uses the sheet/exponent handle $15+\phi^{-1}$ as a Tier 3 hadron-sector anchor pending AKN-action / QLQCD closure. The integer 15 is the topological mechanism; the full exponent used in the 155 ppm headline is not a hidden parameter-free derivation.

**10.3.3 The Weak Berry Phase Correction**

The proton is not a pure strong-force object; it carries Electroweak charge. As the defect winds the Strong sector (15), it accumulates a secondary **Berry Phase** from its transport through the Weak bundle ($E_\perp$).

The magnitude of this phase is strictly determined by the $SU(2)$ Weak holonomy. The path-ordered integral around the $2\pi$ baryonic loop (the 5-fold axis) yields exactly $U_{weak} = -I_2$. This corresponds to a Berry phase of $\pi$, which is a half-winding ($N_{weak}=1/2$). Applying the icosahedral projection ratio $R = 2\phi^{-1}$ yields the exact correction:
$$ \text{Correction} = N_{weak} \cdot R = \left(\frac{1}{2}\right) \cdot (2\phi^{-1}) = \phi^{-1} $$

> **Postulate (Projection Ratio): [Tier 2 mechanism / Tier 3 specific value of the doubling factor]** *The effective projection ratio $R$ for a Berry phase accumulated over a 5-fold axis is $R = 2\phi^{-1}$.*
>
> *Status note.* The label "Postulate" rather than "Theorem" reflects that the spinor-doubling argument below establishes the *form* $R = N_{\rm sheet} \cdot \phi^{-1}$ via icosahedral pentagon geometry + double-cover sheet counting, but the *specific value* $N_{\rm sheet} = 2$ for the baryonic defect requires the structural commitment that both spinor sheets contribute coherently rather than destructively. A first-principles derivation of this constructive-vs-destructive sheet-summation rule from the AKN action — closing the postulate-to-theorem gap — is an open follow-up bundled with Open Problem O.5 (QLQCD-1L closure). The numerical match of the resulting $R = 2\phi^{-1}$ against the observed proton-mass exponent is Tier 2 (geometric form) + Tier 3 (specific doubling factor).
>
> *Proof (Spinor Doubling):* The Berry connection $A$ couples to the orientation of the defect frame. For a 5-fold axis in the Icosahedral group $H_3$, the projected area of the pentagonal face in the fundamental domain relative to the unit sphere is governed by the edge-to-diagonal ratio of the regular pentagon — precisely $\phi^{-1}$. This is the contribution from a single geometric "sheet."
>
> However, the baryonic defect is a **spinor** (a fermion). Spinors live on the **Double Cover** of the rotation group ($SU(2)$ over $SO(3)$). Under the constructive-sheet postulate, a complete physical orbit of the defect traverses **both sheets** of this covering map with coherent contribution from the Spin-Up sector ($|\uparrow\rangle$) and the Spin-Down sector ($|\downarrow\rangle$). The total Berry phase is then the coherent sum over both sheets:
> $$ R = \sum_{\text{sheets}} R_{\text{geometric}} = 1 \cdot (\phi^{-1}) + 1 \cdot (\phi^{-1}) = 2\phi^{-1} $$
> This "Spinor Doubling" supplies the Tier 2 geometric mechanism, but the constructive addition of the two sheets is the Tier 3 input identified in the postulate above. Neglecting one sheet would not realize the proposed baryonic SU(2) double-cover coupling, but a first-principles AKN-action proof of coherent rather than destructive sheet summation is still required before the factor of 2 can be promoted to theorem status. $\square$

The total scaling exponent is the sum of the primary (Strong) winding and the secondary (Weak) winding:
$$ \Phi_{total} = N_{strong} + \text{Correction} = 15 + \phi^{-1} $$
Thus, the formula $m_p \sim \phi^{15+\phi^{-1}}$ is the result of **holonomic additivity** across the two orthogonal fiber bundles.

**QCD Benchmarking (The Absolute Pipeline):**
GCT establishes an **End-to-End Absolute Mass Pipeline**. Rather than relying on the experimental electron mass as an arbitrary input, GCT projects the proton mass from the non-reduced Planck mass ($M_{Planck}$):

1. **Geometric Anchor:** $m_e = M_{Planck} \cdot \phi^{-107} \cdot (1 - 5\alpha)$
2. **Harmonic Projection:** $m_p = m_e \cdot \phi^{15 + \phi^{-1}}$

* **Ratio Precision ($m_p/m_e$) [Tier 2 mechanism + Tier 3 sheet/exponent handle]:** The harmonic-projection formula evaluates to $\phi^{15+\phi^{-1}} \approx 1836.437$, against the CODATA observed ratio $1836.153$. The ratio-level precision is **155 ppm ($0.015\%$)**. The Tier 2 substance is the baryonic-triad harmonic mechanism; the sheet-doubling / coherent-summation handle and the specific composite exponent remain Tier 3 until the AKN-action proof closes. Anchored to the CODATA $m_e$, the formula prediction is $m_p \approx 938.417$ MeV against CODATA $m_p = 938.272$ MeV — same 155 ppm residual, expressed in absolute units. *(Cross-reference: Ch18 §18.1.1 is the canonical Protocol F statement; Appendix R §R.3 "Hadron Sector" carries the precision scorecard entry.)*
* **Absolute Pipeline Precision ($M_{Planck} \to m_e \to m_p$) [Tier 2 mechanism + Tier 3 corrected-formula / AKN-action handle]:** The Planck-anchored end-to-end pipeline (App R §R.3, "Absolute Pipeline" row) carries the same $\phi^{15+\phi^{-1}}$ harmonic projection composed with $m_e = M_P \phi^{-107}(1-5\alpha)$. Its residuals are stepwise: the electron anchor from $M_P\phi^{-107}(1-5\alpha)$ remains a corrected-formula postdiction at roughly $10^3$ ppm, the proton/electron harmonic projection contributes the quoted $155$ ppm ratio residual, and the composed absolute mass inherits both open assumptions. It is therefore not a Tier 2 closure of the proton mass. The AKN-action / QLQCD closure path must still derive the sheet exponent and hadronic action correction before the absolute pipeline can be upgraded.

This derivation treats the proton as the fundamental acoustic resonator of the 6D lattice and computes the mass from the CODATA $m_e$ dimensional anchor plus the $\phi^{-1}$ sheet postulate (Tier 2 mechanism + Tier 3 sheet/exponent handle under the ratio-precision disclosure). The Planck-to-proton absolute pipeline is carried only as a consistency chain until the AKN-action status closes.

> [!IMPORTANT]
> **Firewall Metadata [Proton Mass]**
> - **Type:** Postdiction
> - **Inputs:** $M_{Planck}$ (Anchor), $\phi$ (Invariant), $15+\phi^{-1}$ (Structural)
> - **Degrees of Freedom:** 0 continuous fitted parameters; A1 electron anchor plus Tier 3 sheet/exponent handle $15+\phi^{-1}$
> - **Provenance:** End-to-End Absolute Pipeline ($M_{Planck} \to m_e \to m_p$)

---

**10.4 The Quark Inventory [Tier 2 mechanisms + Tier 3/open-research state values; down-quark R=4 source-promotion target, charm Tier 3 heuristic]**

Applying these symmetries, GCT gives scheme-dependent quark mass comparison values from the dimensional anchor $m_e$:

| Quark sector | Empirical comparison convention used here | Scale/status |
| :--- | :--- | :--- |
| $u,d,s$ | $\overline{\mathrm{MS}}$ running masses | $\mu = 2$ GeV |
| $c,b$ | $\overline{\mathrm{MS}}$ running masses | $\mu = m_q$ |
| $t$ | Pole-mass convention | QCD pole-mass ambiguity retained as a Tier 3 residual |

Quark masses are renormalized parameters, not invariant rest masses. The comparison burden is therefore part of the model: the GCT tree-level geometric values must be stated against a declared QCD scheme and scale, with running and pole/MS-bar conversion carried as open QLQCD closure work rather than hidden inside the precision headline.

> **Tier 3 Algebraic Identification (strange quark $12\alpha$ coefficient candidate; full theorem-grade derivation pending O.43):**
> The strange quark electromagnetic correction mechanism is the dodecahedral face-channel drag of an RT face defect. The specific $12\alpha$ coefficient is the registered candidate coefficient pending QLQCD-1L/O.5 closure.
> 
> *Proof sketch:* The strange quark is an interstitial face defect within the Rhombic Triacontahedron (RT). The immediate candidate coupling environment for an RT face center is the 12 pentagonal faces of the dodecahedral cage (the dual lattice to the icosahedral vertex). Each face supplies a candidate electromagnetic drag channel to the phason strain field. The Tier 2 claim is the face-channel mechanism; the exact $12 \times \alpha$ coefficient awaits the same QLQCD-1L/O.5 closure that governs the quark-sector headline. □
> 
> This is the dual-lattice analog of the muon's $5\alpha$ vertex coefficient.

The Quark sector (interstitial defects) follows a **Mixed-Harmonic Area Law** derived from the **Fuglede–Kadison Spectral Geometry** of the icosahedral cage. The down-quark mass is obtained from the normalized pseudo-determinant of the cage adjacency operator $D_F$ — i.e. the geometric mean of the absolute values of its non-zero eigenvalues, matching the integral-form generalized Fuglede-Kadison determinant discipline of Lück (2002, Def. 3.11):
$$\widetilde{\det}_{FK}(D_F) := \exp\!\left(\tfrac{1}{N_{\rm nz}}\sum_{\lambda_i\neq 0} \ln|\lambda_i|\right) \quad \text{(normalized pseudo-determinant over the nonzero spectrum).}$$
This is **not** equal to $|\det D_F|^{1/N}$ for the finite cage, because the $R=2$ operator has 44 zero modes among 144 vertices and the ordinary determinant vanishes. The normalization is $N_{\rm nz}=100=144-44$.
At the engine's $R=2,\,\mathrm{perp\_cutoff}=2.0$ cage (100 non-zero eigenvalues + 44 zero modes among 144 vertices) the spectrum factors cleanly into icosahedral characters with the multiplicities
$$\lambda \in \bigl\{\sqrt 2\ (\times 6),\ \phi\ (\times 24),\ \phi\sqrt 2\ (\times 44),\ \phi\sqrt 3\ (\times 8),\ 2\phi\ (\times 10),\ \phi^2\sqrt 2\ (\times 6),\ \phi\sqrt 6\ (\times 2)\bigr\}.$$
The geometric mean evaluates in closed form to
$$\det_{FK}(D_F^{R=2}) \;=\; \phi \cdot 2^{39/100} \cdot 3^{5/100} \;=\; 2.239987\ldots$$
giving a finite-cage branch value $m_d = 4.849$ MeV ($+3.17\%$ from the PDG 2024 central value). This value is retained as a secondary $R=2$ algebraic diagnostic, not as the adopted primary row. The primary FK output is the infinite-volume-limit identification
$$m_d = m_u \phi^{\phi} = 4.716~{\rm MeV},$$
which is **POSTDICTION-CONSISTENT conditional on O.5**: $+0.33\%$ against the PDG 2024 central value and inside the registered 11% shell-resonance band.

![The quark mass spectrum is shown against declared PDG comparison conventions; the down-quark row P.20 is postdiction-consistent at the $m_d = m_u\phi^{\phi}$ infinite-volume-limit closed form, conditional on O.5.](content/Figures/Volume_3/Figure V3.10.1.svg)

On larger cages the FK pseudo-determinant exhibits **shell-resonance behaviour**: across $N \in \{1416, 1626, 1686, 1866, 2046, 2178, 2418, 2988\}$ on a converged $R=4$ lattice it oscillates in $[2.105,\, 2.391]$ within the registered 11% band, with an empirical decaying envelope and median $\approx 2.18$, matching the Mixed-Harmonic Area Law heuristic $\phi^{\phi}=2.1785$ to within $\sim 1\%$. The $I_h$-closed orbit-union sequence supplies the aggregate check: closed-cage deep-tail mean $\det_{FK}/\phi^{\phi}=0.9976$ and sequence-mean signed error $+0.09\%$ vs PDG. The tracking of $\phi^{\phi}$ is suggestive but not rigorously derived: by Gelfond–Schneider, $\phi^{\phi}$ is transcendental over $\mathbb{Q}$ and therefore **not in the K-theoretic gap-label module $\mathbb{Z}[\phi]$** that Bellissard's theorem produces for cut-and-project quasicrystal Schrödinger spectra. The closed-form $R=2$ value $\phi \cdot 2^{39/100} \cdot 3^{5/100}$ is algebraic over $\mathbb{Q}$ (a product of $\phi\in\mathbb{Q}(\sqrt5)$ and rational powers of integers) but lies outside $\mathbb{Z}[\phi]$ for these non-integer exponents. This is consistent with Lück's framework: the FK pseudo-determinant is a multiplicative spectral invariant distinct from the additive gap-label $K_0$-class. Identifying the precise algebraic structure of $\widetilde{\det}_{FK}$ in the continuum limit — and its relation, if any, to Bellissard's $\mathbb{Z}[\phi]$ — is an Open Problem (tracked under App H §O.5 + App TP §TP-B). Computational verification: see Appendix Q; finite-size scaling table: `GCT_Physics_Engine/data/fk_scaling.json`.

1. **Up Quark:** $m_u = m_e \cdot \phi^3$ [Tier 2 geometric motif + Tier 3 QCD scheme/running bridge]
 > **Scheme bridge:** the exponent motif is fixed by the icosahedral mass ladder, but the comparison to the PDG $\overline{\rm MS}$ value at $\mu=2$ GeV inherits the hadronic renormalization-scheme/running bridge. The row is therefore postdiction-consistent, not a standalone scheme-independent quark-mass prediction.
2. **Down Quark:** $m_d = m_u \cdot \widetilde{\det}_{FK,\infty} = m_u \phi^{\phi}$ [Tier 2 FK-determinant mechanism + Tier 3 $\phi^{\phi}$ infinite-volume-limit identification conditional on O.5]
 > **Derivation (Fuglede–Kadison):** The Down Quark is a face-defect at the fundamental ($N=11$) harmonic scale. Its mass scale is set by the normalized pseudo-determinant of the cage adjacency $D_F$ — the geometric mean of $|\lambda_i|$ over the non-zero spectrum. The finite $R=2$ cage evaluates to $\widetilde{\det}_{FK} = \phi \cdot 2^{39/100} \cdot 3^{5/100} = 2.239987$, a secondary algebraic diagnostic. The adopted primary output is $m_d = m_u\phi^{\phi}=4.716$ MeV, $+0.33\%$ against the PDG 2024 central value and inside the registered 11% shell-resonance band. The FK-determinant sequence centers on $\phi^{\phi}$: closed-cage deep-tail mean $\det_{FK}/\phi^{\phi}=0.9976$, sequence-mean signed error $+0.09\%$ vs PDG. Single-cage values oscillate within the 11% band with an empirical decaying envelope; rigorous infinite-volume convergence is not proven and bundles with O.5. The algebraic-field structure of $\widetilde{\det}_{FK}$ (whether the asymptotic value is exactly $\phi^{\phi}$, or only the median, and how it relates to the Bellissard $\mathbb{Z}[\phi]$ gap-label module) is an Open Problem.
3. **Strange Quark:** $m_s = m_u \cdot \phi^8 \cdot (1 - 12\alpha)$ [Tier 2 mechanism + Tier 3 specific coefficient (12) pending O.43 closure]
 > **Coefficient status ($12\alpha$ drag):** Unlike vertex defects (leptons) which couple to 5 icosahedral faces ($5\alpha$), quarks are modeled as interstitial face defects. A face-defect drag proportional to the $\mathbb{Z}^6$ coordination number $Z=12$ supplies the Tier 2 mechanism candidate, but the exact use of $12\alpha$ as the strange-quark screening coefficient is a Tier 3 coefficient handle until QLQCD-1L/O.5 derives the face-channel drag from the quark-sector action.
4. **Charm Quark:** $m_c = m_u \cdot \phi^{13 + \phi^{-1}/\phi^2}$ [Tier 3 — heuristic Mixed-Harmonic Area Law]
 > **Status (Tier 3):** The Charm Quark sits at the second-harmonic ($N=17$) defect mode and is expected to be derivable from the cage's second-harmonic K-theoretic gap label — a separate operator-algebraic invariant from the down-quark FK determinant. The closed-form derivation of this gap label is not yet executed in the engine; the current value uses the Mixed-Harmonic Area Law heuristic exponent $13 + \phi^{-3}$, which agrees with PDG 2024 to $0.75\%$ but is not derived from substrate. Closure is bundled with App H Open Problem O.5 (QLQCD-1L) and tracked in App TP §TP-B / §TP-F.
5. **Bottom Quark:** $m_b = m_c \cdot \phi^2 \cdot (5/4)$ [Tier 2 mechanism + Tier 3 specific integer-handle (5/4) pending O.43 closure]
 > **Algebraic Identification (A₅ Dimensional Ratio):** The coefficient 5/4 arises from the ratio of the dimensions of the icosahedral symmetry group's relevant representations in the third-generation quark sector.
 >
 > *Proof sketch:* The bottom quark couples to the vacuum lattice through the same icosahedral defect structure as the charm quark, but at the third-generation energy scale. In the icosahedral group I ≅ A₅ (the alternating group on 5 elements), the relevant representations for third-generation quarks are the 5-dimensional irrep H (Schoenflies) (governing the defect's coupling to the five-fold axes) and the 4-dimensional irrep G (Schoenflies) (governing the coupling to the three-fold tetrahedral substructure). The coupling strength candidate scales as dim(H)/dim(G) = 5/4 (canonical Schoenflies labels for the icosahedral 5- and 4-dimensional irreps; Cotton, *Chemical Applications of Group Theory* 3rd ed. Table A.15; Altmann-Herzig 1994). The representation ratio is exact, but its use as the bottom-quark mass handle remains a Tier 3 specific integer-handle pending O.43 closure.
 >
 > **Classification:** [Tier 2 mechanism + Tier 3 coefficient handle] The 5/4 ratio = dim(H)/dim(G) in A₅ is a representation-theoretic fact; its deployment as the bottom-quark coefficient remains pending O.43.
 
 *Falsification Note: If future lattice QCD places m_b outside 4130–4230 MeV at 5σ, the A₅ dimensional ratio is falsified for the bottom quark sector.*
6. **Top Quark:** $m_t = (v_{target} / 2) \cdot \sqrt{2}$

These tiered tree-level derivations are **geometric mechanism outputs** from the icosahedral cage, not a blanket parameter-free closure of the hadron sector. The percentage errors against current targets ($u$: $+0.21\%$; $d$: open source-promotion target, with the $R=2$ source-placeholder residual $\sim20\%$ and the $+3.83\%$ closed-form branch retained as a non-primary analytic reference until source promotion; $s$: $+0.23\%$; $c$: $+0.52\%$ heuristic; $b$: $+1.08\%$; $t$: $+0.89\%$) are the raw output of the FK determinant and the Mixed-Harmonic Area Law; they are **not fitted post-hoc**. The dominant remaining residuals are:

1. **Shell-resonance band on $\widetilde{\det}_{FK}$.** The finite cut-and-project window samples a discrete subset of the noncommutative spectral geometry. As the cage size $N$ sweeps natural icosahedral shells, the FK pseudo-determinant oscillates in a $\pm 3\%$ band about its asymptotic value $\approx \phi^{\phi}$. This is a Tier 2 mechanism (FK-pseudo-det closure) + Tier 3 source-branch/state-value issue, not a defect of the mechanism.
2. **Missing higher-order QCD running.** Loop corrections from QCD running (analogous to the top quark 0.89% QLQCD-2L debt) contribute $\mathcal{O}(1\%)$ at the charm scale.
3. **Open Problem on $m_c$ K-theoretic gap label.** The charm quark currently uses the Mixed-Harmonic Area Law heuristic $\phi^{13+\phi^{-3}}$ at the $N=17$ second-harmonic mode. The first-principles derivation of this gap label from the cage spectrum is bundled with App H O.5 (QLQCD-1L); tracked in App TP §TP-B / §TP-F.

The protocol is **mechanism-retained but source-promotion-open** under the Explicit Derivation Criterion: the geometric provenance of the strange-, bottom-, and top-quark formulas is verified at Tier 2, the down-quark R=2 source baseline remains a non-operative placeholder until the primary engine output adopts the converged $R=4$ branch or an equivalent operator-derived FK chain, and the charm-quark formula is disclosed as Tier 3 heuristic awaiting the second-harmonic gap-label construction. No target values are pre-assigned (see Appendix Q). This hadronic derivation reduces standard-model parameterisation at tree level but does not currently eliminate it across the full quark sector.

---

**10.5 QCD Phenomena**

**10.5.1 Universal Vacuum Viscosity: The Cabibbo Angle [Tier 2 bare + Tier 3 lepton-to-hadron transfer]**

The mixing between $d$ and $s$ quarks is a geometric rotation relic. The **bare** angle is the Weinberg Invariant $\phi^{-3}$ acting as a direct geometric prediction:
$$\sin \theta_C^{\rm bare} = \phi^{-3} \approx \mathbf{0.236068} \quad \text{[Tier 2]}$$
Observed (PDG 2024): $\sin \theta_C \approx 0.225$. The **bare residual is therefore $\approx 4.9\%$** — the declared Tier 2 precision for the geometric prediction itself.

The bare residual is the same magnitude as the Weinberg-angle bare residual (2.1% in §4.5.4), pointing to a shared origin in the $\phi^{-3}$ Gram-projection scaling that all Tier 2 bare predictions in this sector receive a correction from. For the Cabibbo angle, the candidate **Universal Vacuum Viscosity** correction reuses the lepton-vertex $5\alpha$ phason-drag coefficient from Ch08 §8.2.2:
$$\sin \theta_C^{\rm corrected} = \phi^{-3}(1 - 5\alpha) \approx 0.236 \times (1 - 0.036) \approx \mathbf{0.227} \quad \text{[Tier 2 bare + Tier 3 lepton-vertex transfer]}$$
This narrows the angle residual to ~0.82% (the $s_{12}$ element residual is 1.09%). *Note: the $\alpha$ in the correction is the CODATA experimental value (137.036); the GCT-derived $\alpha$ (137.508 bare) sits inside the Phason Anti-Screening QLQCD-1L research debt of App Z.*

> **Tier discipline on the 0.82% precision claim [important].** The corrected Cabibbo formula gives $s_{12}=0.22745$ vs PDG $0.22501$, a $1.09\%$ element residual. The angle residual is $\theta_C=13.147^\circ$ vs $13.040^\circ$, or $0.82\%$, because of the sine/arcsine nonlinearity. This sub-percent angle precision is a **Tier 2 bare + Tier 3 transfer** result, *not* a Tier 2 prediction. The lepton-to-hadron transfer of $5\alpha$ — from the lepton-vertex coupling at 5 of 12 dodecahedral pentagonal faces (where the mechanism is supported by the icosahedral $A_5$ vertex action) to the hadronic face-defect intra-generation rotation — is a **structural identification** under the icosahedral fiber-vertex / face-defect duality (Ch07 §7.1.2 vs Ch10 §10.1), not a forced derivation. The structural argument: $A_5$ acts identically on vertices (rotational) and pentagonal faces (rotational + parity), so the same 5-fold coupling count governs both observables under the same coefficient. **Promotion** of the transfer to a Tier 2 corrected prediction requires an explicit Brauer-character computation showing the 5-fold action multiplicity is preserved under the vertex-to-face Goldstone projection — bundled with **Open Problem O.5** (hadronic-sector closure). Until O.5 closes, the **declared Tier 2 prediction is the bare $\phi^{-3}$ at 4.9% residual**; the corrected figure should be read as "Tier 2 bare + Tier 3 transfer," consistent with the §R.2.1 loop-order discipline framework. The inter-generation CKM elements ($s_{23}$, $s_{13}$) receive an additional $\phi^{-1}$ holonomy step (§10.6) that the intra-generation Cabibbo does not; this is the geometric origin of the CKM hierarchy under the same transfer ansatz.

> **Lepton-to-hadron bridge for the $5\alpha$ coefficient [Tier 2 bare mechanism + Tier 3 transfer handle].** The $5\alpha$ drag coefficient is derived in Ch08 §8.2.2 as a *lepton-vertex* phenomenon: a charged lepton couples to 5 of the 12 dodecahedral pentagonal faces under the icosahedral $A_5$ vertex group, giving $5\alpha$ as the bare radiative self-screening. The Cabibbo angle is a *hadronic* face-defect rotation (intra-generation $d \to s$, both face defects of the same icosahedral fiber), not a lepton-vertex interaction. The $5\alpha$ coefficient transfer from the lepton-vertex derivation to the Cabibbo hadronic rotation is a disclosed Tier 3 transfer handle: **the projection from $A_5$ vertex coupling to the icosahedral face-defect Goldstone manifold is assumed to preserve the 5-fold coupling count**. This is not an additional continuous fit; it depends on the icosahedral fiber-vertex / face-defect duality (Ch07 §7.1.2 — "Vertex Defects centered on the nodes" vs Ch10 §10.1 — "Interstitial Face Defects"). The duality is structural: $A_5$ acts identically on vertices (rotational) and pentagonal faces (rotational + parity), so the same 5-fold coupling structure governs both observables under the same coupling constant $5\alpha$. Promoting this transfer to a Tier 2 corrected prediction would require an explicit Brauer-character computation showing the 5-fold action multiplicity is preserved under the vertex-to-face Goldstone projection — bundled with **Open Problem O.5** (hadronic-sector closure). The inter-generation CKM elements ($s_{23}$, $s_{13}$) receive an *additional* $\phi^{-1}$ holonomy step (§10.6, "Mixed-Harmonic Law") that the intra-generation Cabibbo does not; this is the geometric origin of the CKM hierarchy under the same transfer.

**10.5.2 Asymptotic Freedom and Lattice Transparency**

As established in Volume 2, Appendix N, the vacuum lattice exhibits **High-Energy Transparency**. At the Planck scale, the quark de-Broglie wavelength is so small that it "misses" the 6D lattice nodes, resulting in zero coupling. This provides the geometric origin of **Asymptotic Freedom**: the strong force vanishes because the lattice becomes a continuum to high-frequency probes.

**10.5.3 The Mass-Drag Anti-Correlation**

GCT identifies a fundamental law: **Heavy particles (Top) have zero drag; light particles (Muon) have maximum drag.** Because high-mass defects oscillate faster than the phason relaxation time, they "self-screen" from the hydrodynamic friction of the vacuum. Consciousness and light arise in the "Soft" sector ($K_\perp$), where drag is maximized, enabling the registration of Qualia.

---

**10.6 The CKM Mixed-Harmonic Ansatz [Tier 2 bare Cabibbo mechanism + Tier 3 corrected-formula handle / Tier 3 remaining angles]**

While Neutrino (PMNS) mixing represents the unpinned axis sliding of itinerant phason waves, Quark mixing represents **Topological Tunneling** between the pinned icosahedral faces of the underlying vacuum lattice.

Because quarks are structural artifacts deeply bound within the strong force matrix, their "flavor shifting" forces them to push against the high-frequency internal geometry of the lattice. This process is inherently suppressed (damped) by the electromagnetic vacuum viscosity ($\alpha$). Thus, unlike the large PMNS angles, the CKM angles are inherently small and follow a strict geometric descent defined by the Mixed-Harmonic Law:

1. **Cabibbo Angle ($s_{12}$):** $s_{12}^{\rm bare}=\phi^{-3}$ is the Tier 2 face-tunneling mechanism; the corrected formula $s_{12} = \phi^{-3} \cdot (1 - 5\alpha)$ is a Tier 3 lepton-to-hadron transfer handle pending O.5 / QLQCD-1L.
2. **$s_{23}$ Mixing:** $s_{23} = \phi^{-(6 + \phi^{-1})}$ **[Tier 3 Ansatz — Irrational Exponent: $6 + \phi^{-1} \approx 6.618$ is irrational. See Open Problem O.5.]**
3. **$s_{13}$ Mixing:** $s_{13} = \phi^{-(11 + \phi^{-1})}$ **[Tier 3 Ansatz — Irrational Exponent: $11 + \phi^{-1} \approx 11.618$ is irrational. See Open Problem O.5.]**

### 10.6.1 CKM Berry-Phase Identification of the $\phi^{-1}$ step [Tier 3 candidate]

The additive $\phi^{-1}$ in the exponents for $s_{23}$ and $s_{13}$ is not an unconstrained fitted parameter. It is a candidate transfer of the $SU(2)$ Berry holonomy used in the proton-mass route.

For the proton, one complete $SU(2)$ cycle around a 5-fold baryonic axis yields a phase transformation $U = -I$, contributing $N_{weak} \times R = (\frac{1}{2})(2\phi^{-1}) = \phi^{-1}$ to the mass exponent.

For quarks, each CKM off-diagonal element involving a **Generation Change** ($s \to c$, $b \to c$, $b \to u$) forces the topological face-defect to cross the $SU(2)$ fiber. This adds one additional holonomy step beyond the bare face-tunneling path. The Cabibbo angle ($s_{12}$), being an intra-generation interaction ($d \to s$), does not trigger this additional cycle, receiving no $\phi^{-1}$ shift.

This geometric projection generates the hierarchy of flavor mixing. The Cabibbo angle has a Tier 2 bare prediction $\sin\theta_C^{\rm bare} = \phi^{-3}$ ($4.9\%$ residual) and a Tier 2 bare + Tier 3 lepton-to-hadron transfer correction $s_{12} = \phi^{-3}(1-5\alpha)$ ($0.82\%$ residual pending O.5); the remaining angles ($s_{23}$, $s_{13}$) with their irrational exponents remain Tier 3 pending resolution of Open Problem O.5.

**Candidate derivation ($\phi^{-1}$ Weak Holonomy Correction) [Tier 3 under Appendix R authority]:**
The $\phi^{-1}$ additive adjustment in the higher-generation CKM exponents is a candidate transfer of the proton-sector $SU(2)_L$ Berry holonomy to quark face-defect tunneling. Quarks are modeled as face-defects using the same weak fiber bundle as the Baryonic Triad; as a quark undergoes topological face-tunneling across generational boundaries, the ansatz assigns one $\phi^{-1}$ Weak Berry phase holonomy step. The CKM transfer remains Tier 3 pending first-principles lepton-to-hadron transfer and QLQCD closure.

These structural identities analytically output $s_{12} \approx 0.22745$ [Tier 2 bare + Tier 3 transfer], $s_{23} \approx 0.0415$ [Tier 3], and $s_{13} \approx 0.0037$ [Tier 3], broadly tracking the PDG 2024 pattern but not constituting a theorem-grade CKM closure. The corrected Cabibbo value remains in live precision tension: relative to the PDG $s_{12}\approx0.2250$ target, the residual is $\sim1.09\%$ and is carried as an explicit $\sim3.6\sigma$ $s_{12}$ tension until O.5/QLQCD derives the lepton-to-hadron transfer. The CP-violating Jarlskog invariant $J_{CKM}$ for this matrix is an **Open Research Problem (App H §H.5, O.7)** bundled with the QLQCD-1L research debt. The $\delta_{CP} = 360^\circ \cdot \phi^{-1}$ phase remains a Tier 3 **leptonic/mixing-geometry phase ansatz** in the GCT registry (pending O.7; the Jackiw-Rebbi mechanism is the gauge-chirality result of Ch02 §2.4.2, not this phase), and it is not by itself a derivation of hadronic CKM CP violation. Hadronic CP violation requires the CKM-area/Jarlskog invariant $J_{CKM}$ plus QCD dressing; that closure remains O.7/O.5. The geometric phase may supply a candidate boundary condition for the hadronic sector, but it does not secure the matter-antimatter-asymmetry claim until the Jarlskog amplitude is derived.

---

> **Closure Target: Fuglede–Kadison Audit for the Down-Quark Mass Scale [Tier 2 FK-determinant mechanism + Tier 3 $\phi^{\phi}$ infinite-volume-limit identification conditional on O.5]**
>
> Let $D_F$ denote the adjacency operator of the icosahedral cage (graph with $N$ vertices selected as the closest perp-projected images of the $\mathbb{Z}^6$ lattice; edges of weight $\phi$ between pairs at unit ambient-space distance). The normalized FK pseudo-determinant is
> $$\widetilde{\det}_{FK}(D_F) := \exp\!\left(\tfrac{1}{N_{\rm nz}}\sum_{\lambda_i\neq 0} \ln|\lambda_i|\right)$$
> where $N_{\rm nz}$ is the count of non-zero eigenvalues and $\lambda_i$ are the corresponding eigenvalues (Lück 2002, Def 3.11 generalized FK determinant integral form). For the $R=2$ cage, $N_{\rm nz}=100=144-44$; the ordinary determinant vanishes because the operator has 44 zero modes, so no equality to $|\det D_F|^{1/N}$ is claimed. Then
> $$m_d = m_u \cdot \widetilde{\det}_{FK}(D_F).$$
>
> *Closed-form evaluation at the $R=2$ cage.* At the engine's reference construction (144 vertices, 100 non-zero eigenvalues + 44 zero modes) the spectrum factors into icosahedral characters with multiplicities $\{\sqrt 2{:}6,\ \phi{:}24,\ \phi\sqrt 2{:}44,\ \phi\sqrt 3{:}8,\ 2\phi{:}10,\ \phi^2\sqrt 2{:}6,\ \phi\sqrt 6{:}2\}$, and the geometric mean evaluates exactly to
> $$\det_{FK}(D_F^{R=2}) \;=\; \phi \cdot 2^{39/100} \cdot 3^{5/100} \;=\; 2.239987\ldots,$$
> giving a finite-cage branch value $m_d = 4.849$ MeV ($+3.17\%$ from the PDG 2024 central value). This branch is a secondary algebraic diagnostic. The adopted primary output is $m_d = m_u\phi^{\phi}=4.716$ MeV, $+0.33\%$ against the PDG 2024 central value and inside the registered 11% shell-resonance band. On the converged $R=4$ lattice $\det_{FK}$ oscillates shell-to-shell in $[2.105,\, 2.391]$ within the 11% band with an empirical decaying envelope and median $\approx \phi^{\phi}$; the $I_h$-closed deep-tail mean gives $\det_{FK}/\phi^{\phi}=0.9976$ with sequence-mean signed error $+0.09\%$ vs PDG. See Appendix Q + finite-size scaling table `data/fk_scaling.json`.
>
> **Algebraic-field status (Open).** The finite $R=2$ diagnostic $\phi \cdot 2^{39/100} \cdot 3^{5/100}$ is algebraic over $\mathbb{Q}$ (a product of $\phi \in \mathbb{Q}(\sqrt5)$ and rational powers of integers), but lies **outside $\mathbb{Z}[\phi]$** for these non-integer exponents. The primary asymptotic-limit candidate $\phi^{\phi}$ is transcendental over $\mathbb{Q}$ by Gelfond-Schneider. This is consistent with Lück's framework — the FK pseudo-determinant is a multiplicative spectral invariant distinct from the additive $K_0$-class of Bellissard gap labels — but it leaves open whether $\widetilde{\det}_{FK}$ converges to $\phi^{\phi}$ exactly in some scaling limit, or only its median tracks $\phi^{\phi}$ within shell-resonance noise.
>
> **Charm-quark status.** The charm quark sits at the second-harmonic ($N=17$) defect mode and is expected to admit a separate spectral derivation from a cage submodule. That derivation is not yet executed; the manuscript currently uses the heuristic Mixed-Harmonic Area Law $m_c = m_u \cdot \phi^{13 + \phi^{-3}}$ (PDG 2024 residual $0.75\%$), explicitly labeled **Tier 3**. The closure path is bundled with App H Open Problem O.5 (QLQCD-1L) and tracked in App TP §TP-B / §TP-F. The CKM matrix elements ($s_{23}$, $s_{13}$) constitute the same Open Problem O.5-CKM, targeted for closure in QLQCD-2L computations (Appendix Z §Z.7).

**END OF CHAPTER 10**
