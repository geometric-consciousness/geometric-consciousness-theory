### **Chapter 8: The Fractal Resonance Spectrum (Leptons)**

The Standard Model treats the masses of the muon ($\mu$) and the tau ($\tau$) as arbitrary parameters determined by measured Yukawa couplings. Geometric Consciousness Theory (GCT) identifies the lepton hierarchy as the **Fractal Resonance Spectrum** of the fundamental $N=144$ dodecahedral cage. The Tier 2 harmonic-ladder mechanism plus Tier 3 integer anchors $N=11$ and $N=17$ yield the second and third-generation lepton mass ratios pending O.5/O.14/O.15 closure.

![Electron, muon, and tau masses sit on a log axis with `N=11` and `N=17` harmonic overlays; correction-stage residuals and row-specific Protocol B gates are shown separately.](content/Figures/Volume_3/Figure V3.8.1.svg)

---

**8.1 Phason Band Structure**

**8.1.1 The Symmetry Octave and the High-Pass Filter**

In the icosahedral projection, the radial scaling of the vacuum is governed by the **Symmetry Octave (6)**, corresponding to the six five-fold rotational axes of the parent lattice. However, the ground-state $N=144$ cage (Chapter 7) act as a **Topological High-Pass Filter**. Harmonics below the 11th power of $\phi$ possess insufficient "Topological Torque" to displace the locked nodes of the ground-state cage. 

**8.1.2 The Generational Scaling [Tier 2 mechanism + Tier 3 integer anchors pending O.5/O.14/O.15]**

The mass hierarchy is established at specific intervals of the Symmetry Octave:
* **The Muon ($n=11$):** The first available spectral gap above the depinning threshold. It occurs at two octaves of inflation minus a single **Decoupling Unit** required to break the ground-state symmetry and transition from a static to a dynamic resonance: $2 \times 6 - 1 = 11$. Equivalently $n_\mu = h + 1$, one unit above the $H_3$ Coxeter number $h = 10$.
* **The Tau ($n=17$):** The next stable resonance window, occurring exactly one symmetry octave above the muon: $11 + 6 = 17$. Equivalently $n_\tau = \left(\textstyle\sum_i d_i\right) - 1 = 18 - 1$, one unit below the $H_3$ Shephard-Todd degree sum; the octave spacing $n_\tau - n_\mu = 6 = d_2$ is the middle degree.

The allowed energy states (particle masses) are selected by the current harmonic-ladder postulates at the $k=11$ and $k=17$ harmonics of the inflation eigenvalue $\phi$, pending O.5/O.14/O.15 closure.

**8.1.3 Geometric Amplification Mechanism**

The massive disparity between generations (e.g., $m_\mu/m_e \approx 206$) is an effect of the **Lever Arm of the 6D Projection**. Because the phason stiffness $K_\perp$ is suppressed by $\phi^{-18}$ (Volume 2, Chapter 4), the resonant frequencies of the defect core are geometrically amplified by the inverse volume ratio of the internal manifold.

**8.1.4 The Linear vs. Non-Linear Boundary [Tier 2]**

Computational verification via the full $6N \times 6N$ sparse Hessian diagonalization of the $N=144$ cage (see Appendix Q) reveals a critical epistemic boundary. Diagonalization of the **bare linear dynamical matrix** extracts the acoustic phonon background, yielding normalized eigen-ratios of `[1.0, 1.67, 2.1, 2.52...]`. 

It is a proven, rigorous fact of the GCT computational verification suite that the exponents $\phi^{11}$ and $\phi^{17}$ **do not** spontaneously emerge from this linear approximation. The leptons are fundamentally **Non-Linear Phason Solitons** (Davydov-like defects) whose masses are governed by the non-perturbative saturation of the discrete $6N \pm 1$ symmetry octaves, not by simple linear harmonic resonance.

Consequently, the harmonic-ladder mechanism is a **Tier 2 geometric postulate**, while the specific integer anchors $N=11$ and $N=17$ remain **Tier 3** pending O.5/O.14/O.15 closure. The Tier-3 status reflects a genuine structural gap: unlike the electron exponent ($107 = 1^2+5^2+9^2 = \sum_i m_i^2$, a power-sum invariant unique to $H_3$) and the stiffness exponent ($18 = \sum_i d_i$), the lepton harmonic integers are **not** power sums of the $H_3$ exponent or degree multisets ($\sum m_i = 15,\ \sum m_i^2 = 107$; $\sum d_i = 18,\ \sum d_i^2 = 140$), and an exhaustive audit of canonical $H_3$/$I$ structural counts — roots, reflections, conjugacy classes, irreducible-representation dimensions, orbit sizes, and coinvariant/Poincaré coefficients — yields no distinctive invariant identification of $11$ or $17$ (engine: `GCT_Physics_Engine/src/protocol_w4_lepton_exponents.py`). The integers likewise fail to arise as spectral-ordinal labels: in the icosahedrally-decomposed linear phason spectrum of the canonical 152-node defect cage, the phason-vector channel activates at pooled cluster ordinals $(5, 18, 26, \ldots)$, with neither $11$ nor $17$ appearing among the activation ordinals (engine: `GCT_Physics_Engine/src/protocol_w4b_lepton_spectral_ordinals.py`). Together with the eigenvalue-magnitude exclusion above, this closes the arithmetic-invariant and linear-spectral identifications, leaving the non-perturbative extraction as the unique closure path. The canonical hooks $n_\mu = h+1$ and $n_\tau = (\sum_i d_i) - 1$ fix the values against $H_3$ data, but the Decoupling-Unit offset and the generation indexing remain un-derived handles, so no canonical-invariant promotion of the form available to $107$ exists. The muon hook does carry genuine *naming* standing: the diagonal-coinvariant theorem of Gordon (2003, Thm.~1.4) attaches a $W$-stable quotient ring of dimension $(h+1)^n$ — with $h+1 = 11$ graded levels per rank coordinate — to every finite Coxeter group, explicitly including the non-crystallographic $H_3$. This standing is dimensional only [Tier 3]: the construction carries no spectral, harmonic, or mass-ladder content connecting $h+1$ to the $\phi$-power ladder, its crystallographic lattice interpretation ($Q/(h+1)Q$) does not transfer to $H_3$, and no analogous theorem features $\sum_i d_i - 1 = 17$. Extracting these non-linear solitonic eigenvalues directly from an ab-initio non-perturbative simulation remains the closure target for Quantitative Lattice Quantum Chromodynamics (QLQCD).

---

**8.2 The Muon (The Acoustic Resonance)**

**8.2.1 Identification: $\mu \leftrightarrow \phi^{11}$**

The Muon is the fundamental acoustic resonance of the electron's dodecahedral cage. Its "Bare Geometric Mass" is the energy required to maintain this 11th-harmonic oscillation:
$$m_\mu^{bare} = m_e \cdot \phi^{11} \approx 101.6913 \text{ MeV} \quad \text{[Tier 2 mechanism + Tier 3 specific exponent $N=11$]}$$

> **Tier disposition for the muon harmonic exponent.** The harmonic-ladder mechanism is Tier 2 (geometric postulate; see §8.1). The specific integer $N = 11$ is Tier 3, anchored at Parameter Ledger §0.1 postulate P4: the $6N \pm 1$ symmetry-octave selection rule of §8.1.1 constrains but does not uniquely force $N = 11$. The integer-side closure target is the analogue of the electron's $|n| = 107 = \sum m_i^2(H_3)$ Coxeter-exponent uniqueness derivation; see App H Open Problem O.14 path (l) for the closed electron-side argument and Parameter Ledger §0.1 P4–P5 for the muon-and-tau integer closure status.
The pre-LEA single-trial probability for this match is $4 \times 10^{-8}$ (raw per-pair Z-score, no multiple-comparison correction). The canonical headline significance is the **broad internal look-elsewhere ~2.6σ** from the full $\mathbb{Z}[\phi]$ multi-base sweep over Lucas-vs-non-Lucas exponent assignments (Firewall §3 Master Statistical Table + App R §R.9.2 footnote). The ~3.1σ figure under the Conservative full-SM-texture window $N \in [4, 50]$ across ~25,000 trial pairs is a **conditional auxiliary** on the SM-texture-window prior — citing it as headline without naming the window prior is significance laundering under the Firewall governance discipline. Applying the framework's further depinning-threshold prior ($N \in [8, 25]$ — the $N=8$ lower bound is itself a structural postulate per §8.1.1) reduces the search space to 153 independent pairs and yields $p \approx 6.1 \times 10^{-6}$, a further conditional auxiliary at **4.4σ** under the depinning prior — also disclosed with its conditioning prior.

**8.2.2 The Phason Drag Coefficient ($5\alpha$) [Tier 2 mechanism + Tier 3 specific coefficient]**

The icosahedral $A_5$ group has five non-trivial irreps. Counting these irreps as the **phason channel multiplicity** is a Tier 2 mechanism. **Converting** this count into the equal-weight pole-mass self-energy coefficient $+5\alpha$ is a Tier 3 physical normalization rule: each channel contributes one unit of $\alpha$ to the muon self-energy, pending a first-principles GCT self-energy calculation (closure target App H O.5). The 21 ppm headline downstream inherits Tier 3 status from this coefficient normalization and from the pole-mass loop-order discipline; it is not a Tier 2 coefficient derivation.

> **Layered tier disposition:** The muon correction is a tree-level + single 1-loop GCT correction factor: the $\phi^8\alpha^2$ factor is algebraically $\phi^{-3}\alpha^2 \times \phi^{11}$ within the displayed heat-kernel construction (see Appendix Q). The tiered claim is the existence of the phason-channel multiplicity mechanism and the sign/scale of the single-loop geometric correction channel, not the standalone **21 ppm** pole-mass residual. The $+5\alpha$ coefficient normalization and the 21 ppm residual remain Tier 3 pending full GCT-native self-energy and loop-order closure, because the pole-mass comparison imports SM-equivalent radiative-correction discipline (App R §R.2.1 / O.5). The tau closes to **~51 ppm** against PDG 2024 via the $-3.6\alpha$ screening coefficient, whose status is Tier 2 mechanism + Tier 2 integer pair $(D=18,N=5)$ + Tier 3 combination rule $c=-D/N$ pending O.26b.
>
> **The Computational Frontier:** The ultimate Tier 1 closure of this claim requires the complete non-perturbative solution of the $6N \times 6N$ Hessian matrix for the $N=144$ defect cage, extracting the full non-linear eigenspectrum without analytic approximation. Until this computation is completed with full HPC resources, the muon phason-channel multiplicity remains Tier 2 analytic, while the muon coefficient normalization and the tau headline coefficient remain layered by the Tier 3 gaps above.

**8.2.3 Tree + Single 1-Loop GCT Phason Self-Energy Correction [Tier 2 mechanism + Tier 3 SM-equivalent radiative discipline]**

To reach precision limits for the muon, we must account for the leading GCT loop correction. The mass shift is represented by a single 1-loop GCT phason self-energy correction factor over the discrete $N=144$ cage. The discrete cage-Hessian correction yields:
* **Intensive Scaling:** The single 1-loop GCT self-energy $\Sigma$ is normalized by the node count $1/N$.
* **Engine-checked exponent factor:** The graph topology and Gram projection geometry yield an effective scaling factor of **$\phi^8$** (the single 1-loop GCT correction factor over the $N=144$ cage; see Appendix Q), arising as an electroweak mixing factor of $\phi^{-3}$ (which, when multiplied by the bare muon scaling $\sim \phi^{11}$, produces $\phi^{11} \times \phi^{-3} = \phi^8$ scaling). The exponent arithmetic is checked; full load-bearing radiative closure remains O.5/O.26.

Therefore, the single-loop mass shift is [Tier 2 mechanism + Tier 3 SM-equivalent radiative discipline]:
$$\Delta m_2 = (m_e \phi^{11}) \cdot (\phi^8 \alpha^2) \approx \phi^8 \alpha^2 \text{ (effective coupling)} \quad \text{[Tier 2 mechanism + Tier 3 SM-equivalent radiative discipline pending O.5/O.26]}$$

**8.2.4 Result 8.1: The Muon Mass Formula**

**Result 8.1:** *Three-stage muon chain: 3.75% bare residual, 2429 ppm first-order residual, and 21 ppm only after the A3 + single-1-loop comparison stage conditional on SM-equivalent higher-loop discipline.*
$$m_\mu = m_e \phi^{11} (1 + 5\alpha + \phi^{8} \alpha^2)$$

> **The Geometric Basis:**
> The muon mass formula employs the $\phi^8\alpha^2$ correction channel whose displayed product is exact exponent arithmetic: $\phi^{11} \times \phi^{-3} \times \alpha^2 = \phi^{8} \alpha^2$. The existence/sign of the single-loop geometric channel is the Tier 2 mechanism; the absolute 21 ppm pole-mass residual remains Tier 3 conditional on A3, O.15/O.19/O.26, and SM-equivalent higher-loop discipline. It uses zero continuous fitted parameters after the disclosed A3, discrete-exponent, and Tier-3 normalization inputs are counted. **Reading the 21 ppm precision with loop-order discipline (App R §R.2.1).** The CODATA muon-mass pole-mass anchor against which the 21 ppm residual is computed already incorporates the Standard-Model 2-loop electroweak + 3-loop QED radiative corrections (which contribute $\sim 10$–$40$ ppm to the lepton sector). Because the 21 ppm residual lies *within* this $\sim 10$–$40$ ppm higher-loop theory floor, it must be read as floor-consistent rather than as a sub-floor precision claim: the residual is not resolvable below the theory uncertainty it is being compared against, so the headline number is a consistency statement, not a demonstration of 21-ppm-level geometric precision. The GCT formula here is a *tree-level + single 1-loop GCT correction factor* expression — Tier 2 at the GCT-internal level given the icosahedral postulates — but the 21 ppm precision claim against the CODATA pole mass implicitly assumes SM-equivalent higher-loop discipline to the precision required to keep residuals at the ppm level. The 21 ppm figure is therefore not a *pure* "geometric saturation of the icosahedral projection to the SM muon mass" claim and is not load-bearing evidence by itself; it is a Tier 2 GCT correction-channel calculation scored against an SM-anchored target whose precision rests on SM higher-order corrections that GCT does not independently reproduce. **The GCT-internal closure of the higher-loop derivation that would convert this implicit assumption into a GCT-native ppm-precision result bundles with App H Open Problem O.5 (QLQCD-1L).** Under O.5 closure the present formula would be promoted from "Tier 2 mechanism + ppm precision given SM-equivalent radiative corrections" to "Tier 2 GCT-native ppm precision". The truly bare $\phi^{11}$-only residual without the $(1 + 5\alpha)$ first-order correction is $\sim 3.75\%$ vs PDG; the $\sim 0.25\%$ after-first-order-correction figure and the $\sim 21$ ppm after-$\phi^8\alpha^2$-correction figure are the operative tier-disciplined dispositions; see App R §R.1 row 2 + §R.2.1 for the full Loop-Order-Discipline accounting.

**Consistency Check (Rigorous Logic):**
* **Bare stage:** $m_e \phi^{11} \approx 101.6913$ MeV, about $3.75\%$ low.
* **First-order A3 drag stage:** $m_e \phi^{11}(1+5\alpha_{\rm A3})$, leaving about $2429$ ppm residual.
* **Displayed A3 + single-1-loop comparison stage:** $m_e \phi^{11}(1+5\alpha_{\rm A3}+\phi^{8}\alpha_{\rm A3}^{2}) \approx 105.656$ MeV.
* **Observed (PDG 2024): $105.658$ MeV**
* **Relative Error at displayed stage:** 21 ppm ($0.0021\%$), conditional on A3 and SM-equivalent higher-loop discipline.

> [!IMPORTANT]
> **Firewall Metadata [Muon Mass]**
> - **Type:** Postdiction
> - **Inputs:** $m_e$ (A1 dimensional anchor), $\phi$ (geometric invariant), $\alpha(0)_{\rm CODATA}$ (A3 precision-comparison anchor), $5\alpha$ (Tier 2 channel multiplicity + Tier 3 pole-mass normalization), $\phi^{8}\alpha^2$ (Tier 3 second-order term pending O.15/O.5/O.19 closure)
> - **Degrees of Freedom:** 0 continuous fitted parameters; Tier 3 specific exponent $N=11$; ppm residual conditional on SM-equivalent 2-loop+ radiative corrections per App R §R.2.1
> - **Provenance:** Internal derivation (Acoustic Resonance & Electroweak Projection; see Appendix Q)


---

**8.3 The Tau (The Hole Mode)**

**8.3.1 Identification: $\tau \leftrightarrow \phi^{17}$**

The Tau is the fundamental optical resonance, occurring exactly one symmetry octave above the muon [Tier 2 mechanism (harmonic-ladder + $6N \pm 1$ symmetry-octave selection rule) + Tier 3 specific integer exponent $N = 17$ (geometric postulate P5 per Parameter Ledger §0.1; the integer-side analogue of the electron's $|n| = 107$ Coxeter-exponent uniqueness derivation is the residual closure target shared with $N = 11$)].
$$m_\tau^{bare} = m_e \cdot \phi^{17} \approx 1824.78 \text{ MeV} \quad \text{[Tier 2 mechanism + Tier 3 specific exponent]}$$

The exponent N=17 corresponds to the next symmetry octave above the muon ($11+6$). This selection represents a heuristic alignment within the A5 gap spectrum. Other exponents in the range 12–19 are not current charged-lepton predictions; no theorem in the manuscript yet derives an energetic suppression law excluding each alternative exponent, so that exclusion remains part of the integer-selection open problem.

**8.3.2 Mechanism for the Tau Screening Coefficient ($-3.6\alpha$) [Tier 2 mechanism (A_5-channel-averaging + phason-sign argument) + Tier 2 integer-pair $(D = 18, N = 5)$ + Tier 3 combination rule $c = -D/N$ pending O.26b — stacking the Tier 3 combination rule on the Tier 2 integer pair yields **Tier 3 for the headline coefficient $-3.6\alpha$** (per App H O.26 + §8.3.4 Result 8.2 + App R §R.1 row 3 disposition). The $H_3$ Shephard-Todd invariant-degree sum $D = 2 + 6 + 10 = 18$ is the Tier 2 icosahedral-specific anchor (unique to $H_3$ among rank-3 Coxeter groups); the 2D-face-in-6D tangent-bundle dimension count $D_{\rm pos}(6) + D_{\rm mom}(6) + D_{\rm face\,int}(6) = 18$ is a 6D-ambient consistency cross-check rather than an independent icosahedral anchor; the pentagonal symmetry order $N = 5$ matches the muon's $A_5$ channel count from RT vertex enumeration; the ratio-combination $c = -D/N$ that selects $-3.6$ over alternative combinations $(D - N = 13, D \cdot N = 90)$ is the load-bearing Tier 3 postulate pending App H Open Problem O.26b. Engine: `protocol_lepton_coefficients.py`, `gct_tau_uniqueness.py`, `protocol_o15a_rg_flow_argument.py`.]**

The sign flip from positive drag (Muon) to negative screening (Tau) is a consequence of **Kramers-Kronig Dispersion** occurring at the RT face. The phason field possesses a characteristic **Transparency Frequency** $\omega_c$ related to the lattice relaxation time.

* **Muon ($\omega < \omega_c$):** The defect oscillates slower than the lattice response. The phason cloud tracks the particle, creating **Viscous Drag** (Positive $\alpha$).
* **Tau ($\omega > \omega_c$):** The defect oscillates faster than the lattice can relax. The phason field effectively "freezes," and the particle pushes against the rigid volume. This results in **Lattice Volume Displacement**, or diamagnetic screening (Negative $\alpha$).

**Derivation of the −3.6α = −18α/5 Tau Screening Coefficient**

The coefficient is constructed from two ingredients, both independently
established:

**Ingredient 1 — $D = 18$ Phase-Space Dimension [Tier 2, unique $H_3$ Shephard-Todd anchor with 6D-ambient consistency check]:**
The integer $D = 18$ is established at Tier 2 via the unique icosahedral anchor: the $H_3$ Shephard-Todd invariant-degree sum $\{2, 6, 10\}$, sum $= 18$ (unique to $H_3$ among rank-3 finite Coxeter groups: $A_3 = 9$, $B_3 = 12$, $H_3 = 18$). The 2D-RT-face-in-6D tangent-bundle decomposition $D_{\rm pos}(6) + D_{\rm mom}(6) + D_{\rm face\,int}(6) = 18$ is a consistency check from the 6D ambient triple-decomposition, not an independent icosahedral anchor (every 6D-ambient theory with this triple-decomposition gives 18 regardless of icosahedral structure). The sharper RG-running step $K_\perp/K_\parallel = \phi^{-D}$ at the renormalization-flow level is separately open as Open Problem O.15(b).

*The $H_3$ Shephard-Todd anchor (load-bearing, icosahedral-specific).* The icosahedral Coxeter group $H_3$ has rank 3 with fundamental invariant polynomials of degrees $d_1 = 2$, $d_2 = 6$, $d_3 = 10$ (Humphreys 1990, Tables 1 and 3.1; Shephard-Todd 1954, *Can. J. Math.* 6:274). Their sum is canonically
$$D_{H_3} = d_1 + d_2 + d_3 = 2 + 6 + 10 = 18.$$
This is a Tier 1 mathematical fact about $H_3$ and matches the integer entering the tau screening formula exactly. Among rank-3 Coxeter groups ($A_3$: degrees $\{2,3,4\}$, sum 9; $B_3$: $\{2,4,6\}$, sum 12; $H_3$: $\{2,6,10\}$, sum 18), only $H_3$ produces 18 — the icosahedral specificity is rigid.

*6D-ambient triple-decomposition consistency check (not an independent anchor).* An RT face is a 2-dimensional rhombic plaquette embedded in the 6D parent lattice. The full phase-space tangent bundle at such a face decomposes by canonical phase-space + tangent-bundle dimension counting:
$$D = \underbrace{D_{\rm pos}(6)}_{\text{6D parent lattice}} + \underbrace{D_{\rm mom}(6)}_{\text{cotangent (canonical symplectic)}} + \underbrace{D_{\rm face\,int}(6)}_{\text{2D-in-6D tangent bundle}} = 18.$$
$D_{\rm face\,int} = 6$ is geometrically forced because the tangent bundle of a $k$-dimensional surface in an $n$-dimensional ambient manifold has total dimension $n$ (the $k$ in-plane + $(n-k)$ normal modes); for $k=2$, $n=6$, this is $2 + 4 = 6$. This identity follows from the 6D ambient triple-decomposition alone and obtains in any 6D-ambient theory with that decomposition regardless of icosahedral structure; it is therefore a consistency cross-check that the 6D ambient framework is internally compatible with the $H_3$ value, not a second icosahedral-specific invariant.

Engine cross-checks: `protocol_o15a_rg_flow_argument.py` (verifies the $H_3$ Shephard-Todd anchor — only $H_3$ among rank-3 Coxeter groups yields 18); `gct_tau_uniqueness.py` and `protocol_lepton_coefficients.py` (return $D_{\rm face\,int} = \text{ambient\_dim} = 6$ as the tautological 6D-ambient consistency cross-check). The sharper Tier 2 claim that the *RG running* of the stiffness ratio specifically gives $K_\perp/K_\parallel = \phi^{-D} = \phi^{-18}$ depends on the symmetry-adapted RG bookkeeping rule "each fundamental invariant of degree $d_n$ contributes $d_n \log\phi$ to $\log(K_\parallel/K_\perp)$"; the explicit one-loop Lubensky-Ramaswamy-Toner integration on the AKN lattice that would derive this bookkeeping from first principles is Open Problem O.15(b), and is independent of the integer-counting argument needed for the tau coefficient.

**Ingredient 2 — 5-Fold Icosahedral Averaging (Tier 2):**
The icosahedral rotation group $A_5$ has exactly **5 irreducible complex representations** of dimensions $\{1, 3, 3, 4, 5\}$ (with $1^2 + 3^2 + 3^2 + 4^2 + 5^2 = 60 = |A_5|$ — the count of irreps equals the number of conjugacy classes for any finite group; verified by the standard representation theory of $A_5$). These constitute 5 independent representation channels through which the tau-phason coupling distributes. (Note: the icosahedron itself has 6 five-fold rotation axes; under any single fixed 5-fold axis, the 20 triangular faces partition into 4 orbits of 5 faces each, since orbit size divides the group order 5 — the "5 channels" here are the $A_5$ irrep count, not the face-orbit count under a single fixed axis. The same 5-irrep structure generates the $5\alpha$ drag coefficient for the muon via $A_5$ representation theory; see §8.2.2.)

When the tau lepton phason field couples to the 18D tangent bundle of the
quasicrystalline acceptance window surface, the coupling is distributed
equally across these 5 channels by the A₅ symmetry of the icosahedron.
The effective per-channel contribution is:

$$\text{Coupling per channel} = \frac{D_{\text{phase space}}}{N_{\text{A5 channels}}} \times \alpha = \frac{18}{5} \times \alpha = 3.6\alpha$$

**Sign Convention — Shielding vs. Drag:**
The muon couples to the *phonon* (E_∥) projection of the phason current,
resulting in a *positive* drag (+5α). The tau lepton, as the 3rd-generation
heavy lepton, couples to the *phason* (E_⊥) anti-screening sector, resulting
in a *negative* shielding correction (−3.6α). The sign is fixed by the
projection sign in the stiffness ratio (G_⊥ has Galois-conjugate slope
φ′ = −1/φ, hence the negative correction).

**Result:**
$$\boxed{c_\tau = -\frac{18\alpha}{5} = -3.6\alpha}$$

*Tier classification: The integer $D = 18$ is Tier 2 via the unique $H_3$ Shephard-Todd invariant-degree-sum anchor ($2 + 6 + 10 = 18$, uniquely $H_3$ among rank-3 Coxeter groups), with the 2D-face-in-6D tangent-bundle dimension count ($6 + 6 + 6 = 18$) entering as a 6D-ambient consistency check rather than as a second icosahedral-specific anchor. The 5-fold $A_5$ averaging is Tier 2 ($A_5$ representation theory, matched to the muon's $+5\alpha$ channel count from RT vertex enumeration). The negative sign is Tier 2 (Galois-conjugate slope $\phi' = -1/\phi$ in the stiffness ratio). **The ratio-combination rule $c = -D/N$ that selects the headline coefficient $-3.6$ (over alternative combinations $D - N = 13$ or $D \cdot N = 90$) is a load-bearing Tier 3 postulate pending App H Open Problem O.26b. Stacking the Tier 3 combination rule on the Tier 2 integer pair yields Tier 3 for the headline $-3.6\alpha$ coefficient** (mirroring the §8.3.4 Result 8.2 disposition + App H O.26 + App R §R.1 row 3). The sharper claim that the RG-renormalized stiffness ratio is specifically $\phi^{-D} = \phi^{-18}$ depends on the symmetry-adapted RG bookkeeping rule, whose first-principles derivation is Open Problem O.15(b) and is independent of the integer-counting argument needed for the tau coefficient.*

The screening coefficient is therefore:
$$\text{Screening Coefficient} = -\frac{18}{5} \alpha = -3.6\alpha$$

**8.3.3 Tangent-Bundle Consistency Check for the $\tau$ Phase-Space Dimension [6D-ambient cross-check; not an independent icosahedral anchor]**

The $D = 18$ tangent-bundle count is a 6D-ambient consistency check from the parent-lattice geometry, not an independent icosahedral anchor. An RT face is a 2-dimensional rhombic plaquette embedded in the 6D parent lattice. By the tangent bundle decomposition of a 2D surface in a 6D ambient manifold:

$$D_{\text{face-int}} = D_{\text{in-plane}} + D_{\text{normal}} = \underbrace{2}_{\text{area + shear}} + \underbrace{(6-2)}_{\text{4 normal tilts}} = 6$$

This is **geometrically forced** by $\dim_{\text{ambient}} = 6$ alone. A 2D face embedded in $\mathbb{R}^6$ has exactly 6 independent deformation modes. Therefore:

$$D_{\text{total}} = D_{\text{pos}}(6) + D_{\text{mom}}(6) + D_{\text{face-int}}(6) = 18 \quad \checkmark$$

The stabiliser of a single RT face under $I_h$ has order $|I_h|/30 = 4$ (Klein 4-group $\mathbb{Z}_2 \times \mathbb{Z}_2$). The screening coefficient $-D/N = -18/5 = -3.6$ carries **Tier 2 mechanism** ($A_5$-channel-averaging + phason-sign argument) **+ Tier 2 integer-pair** ($D = 18$ established by the unique $H_3$ Shephard-Todd invariant-degree-sum anchor — icosahedral-specific; load-bearing — with the tangent-bundle count above entering as a 6D-ambient consistency check rather than as a second icosahedral-specific anchor; $N = 5$ established by RT vertex enumeration, the same anchor as the muon's $+5\alpha$) **+ Tier 3 combination rule** $c = -D/N$ pending App H Open Problem O.26b. **Stacking the Tier 3 combination rule on the Tier 2 integer pair yields Tier 3 for the headline coefficient $-3.6\alpha$**, mirroring the §8.3.4 Result 8.2 disposition + App H O.26 + App R §R.1 row 3. The sharper Tier 2 claim that the symmetry-adapted RG running of the stiffness ratio gives $K_\perp/K_\parallel = \phi^{-D}$ depends on the bookkeeping rule "each fundamental invariant of degree $d_n$ contributes $d_n \log\phi$ to the kinetic-term anomalous dimension"; an independent first-principles one-loop Lubensky-Ramaswamy-Toner derivation of this rule is Open Problem O.15(b) and is logically independent of the integer-counting argument that fixes the tau coefficient.

**8.3.4 Result 8.2: The Tau Mass Formula [Tier 2 mechanism + Tier 2 integer-pair $(D=18, N=5)$ + Tier 3 combination rule $c = -D/N$ pending O.26b + Tier 3 specific harmonic exponent $N_{harm}=17$]**

**Result 8.2:** *The physical mass of the tau corresponds to the 17th harmonic of the electron cage, screened by the ratio of the 18-dimensional phase-space tangent bundle to the 5-fold symmetry order. The $A_5$-channel-averaging mechanism is Tier 2; the integer pair $(D = 18, N = 5)$ is Tier 2 ($D = 18$ anchored by the unique $H_3$ Shephard-Todd invariant-degree sum — icosahedral-specific; $N = 5$ from the RT pentagonal vertex enumeration, shared with the muon's $+5\alpha$ channel count). The **combination rule** $c = -D/N$ that yields the headline screening coefficient $-3.6$ as a ratio (rather than, e.g., a difference $D - N = 13$ or product $D \cdot N = 90$) is itself a structural postulate registered as Tier 3 pending first-principles derivation — see App H Open Problem O.26b. The specific harmonic exponent $N_{harm} = 17$ is a Tier 3 postulate (Parameter Ledger §0.1 P5), the integer-side closure shared with the muon's $N_{harm} = 11$. Stacking the Tier 3 combination rule on the Tier 2 integer pair yields Tier 3 for the headline coefficient $-3.6\alpha$; the bare Tier 2 elements are the mechanism + the integer pair, not the ratio combination.*
$$m_\tau = m_e \phi^{17} (1 - 3.6\alpha)$$

**Consistency Check:**
* $m_e \phi^{17} \approx 1824.78$ MeV
* $1 - 3.6\alpha \approx 0.97373$
* **GCT Predicted: $1776.84$ MeV**
* **Observed (PDG 2024): $1776.93 \pm 0.09$ MeV**
* **Relative Error: 51 ppm ($0.0051\%$)**

---

**8.4 Fourth-Generation Termination Mechanism [Tier 2 mechanism + Tier 3 closure pending]**

The $6N \pm 1$ symmetry octave sequence ($N=11, 17$) naturally implies a mathematical candidate state at the next harmonic, $N=23$. The absence of a fourth generation is treated as a Tier 2 geometric mechanism with Tier 3 closure pending, not as a theorem-grade exclusion. The bare geometric mass for such a fourth-generation lepton would be [Tier 4]:
$$m_{4}^{bare} = m_e \cdot \phi^{23} \approx 32.7 \text{ GeV} \quad \text{[Tier 4]}$$

This hypothetical $32.7$ GeV state is strictly excluded by early LEP direct searches (which ruled out a standard fourth generation lepton up to $\sim 100$ GeV). In GCT, the absence of this state is treated as a candidate topological cutoff rather than a theorem-grade exclusion until the O.5/O.15 closure machinery derives the carrying-capacity rule from the AKN action.

**Result 8.3 (conditional cutoff mechanism):** *Under the current RT tangent-bundle carrying-capacity postulate, a local topological defect cannot sustain a harmonic resonance whose index ($N$) exceeds the total degrees of freedom of its confining geometry. Because the internal tangent-bundle count of the Rhombic Triacontahedron face is $D=18$ (6 position + 6 momentum + 6 internal), the harmonic sequence is expected to terminate before $N=23$. Therefore, $N=11$ and $N=17$ are the stable excited states currently licensed by the icosahedral defect model; theorem-grade exhaustion awaits O.5/O.15 closure.*

The $N=23$ state requires a phase-space dimensionality that exceeds the carrying capacity of the $D=18$ RT tangent bundle under the current cutoff postulate. The tau is therefore the current candidate cutoff under the RT tangent-bundle carrying-capacity postulate, pending O.5/O.15 closure.

---

**8.5 — The Global Combinatorial LEA (Parametric Closure 2)**

A rigorous evaluation of statistical significance must account for the full **look-elsewhere effect (LEA)** across the *entire* parameter space, defending against the "infinite search space" critique of arbitrary $\alpha$ polynomials. The bare-exponent p-value is estimated under the conservative-$\phi$-spacing convention as $\sim2.6\sigma$ for the corrected-formula lepton pair (App R LEA section); a fully combinatorial p-value requires §R.9.5 closure.

**Expanded Search Space Definition:**
We define a massive parameter space representing all plausible combinations of baseline harmonics and small-coupling geometric corrections:
1. **Base Exponents:** $N_\mu, N_\tau \in [8, 25]$ with $N_\mu < N_\tau$ (Yields 153 baseline pairs under the depinning-threshold window).
2. **First-Order Drag/Screening:** Coefficients $C_1 \in [-20, 20]$ in discrete steps of 0.2 (Yields 201 choices, cleanly capturing representations like $5\alpha$ and $-3.6\alpha$).
3. **Second-Order Self-Energy:** Coefficients $C_2 \in [-50, 50]$ in integer steps of 1.0 (Yields 101 choices, cleanly capturing limits like $\phi^8 \approx 47$).

Every predicted mass ratio takes the form: $m/m_e(N, C_1, C_2) = \phi^N (1 + C_1\alpha + C_2\alpha^2)$.
The total combinatorial volume of this expanded grid (on the discretization $C_1 \in [-20, 20]$ step 0.2, $C_2 \in [-50, 50]$ step 1.0, $N \in [8, 25]$) is $153 \times (201 \times 101)^2 \approx 6.30 \times 10^{10}$ possible grid points.

**Constrained-search consistency check.**
Among the grid of corrected lepton-mass formulae $\{$bare $\phi^N$, $(1+5\alpha)$, $(1-3.6\alpha)$, $\phi^8\alpha^2\}$ combinations sampled within the integer-exponent search space, six configurations land within a 21 ppm window of the observed muon AND tau mass ratios. The published GCT tau formula $m_\tau = m_e \cdot \phi^{17} \cdot (1 - 3.6\alpha)$ carries a 50.85 ppm residual against the canonical 50 ppm WP gate (Tier 3 TENSION marker pending O.26b ratio-combination closure; see App R lepton row §LEA). The 21 ppm grid-hit count is therefore a **Tier 3 search-space diagnostic** — it indicates that polynomial correction VARIATIONS over the search space admit a 21 ppm joint fit, NOT a precision-validation of the manuscript's canonical lepton pair. The grid-count p-value is retained only in the appendix-level LEA table, not as a main-text significance claim.

**Statistical-scope disclosure.** A naive translation of this grid count into a sigma figure would give $\approx 6.4\sigma$, but **this number is not the canonical significance of the lepton-pair claim** and should not be cited as such: it counts a continuous polynomial parameter space ($C_1, C_2$) as a discrete trial bag, which inflates the effective sample size and is a known misapplication of LEA on bounded parameter searches (cf. Gross & Vitells 2010 on continuous-parameter LEA). The canonical headline figure for this claim is the **broad internal look-elsewhere ~2.6σ** from the full $\mathbb{Z}[\phi]$ multi-base sweep (Firewall §3 Master Statistical Table); the **~3.1σ** Conservative-SM-texture-window-conditional figure is a conditional auxiliary on the $N \in [4, 50]$ window prior, and the **4.4σ** under the further depinning-threshold prior $N \in [8, 25]$ (153 pairs; $p \approx 6.1 \times 10^{-6}$) is also a conditional auxiliary — cited only with the conditioning prior named (cf. §8.5 above and the Prediction/Postdiction Firewall Master Statistical Table). The 6-point grid count is reported here as a *consistency check* — independent confirmation that the polynomial-corrected geometry is narrowly constrained, *not* as a stronger significance claim.

**Separation of precision claims:** The baseline geometric prediction achieves ~0.25% precision *after* the Tier 2 muon phason-channel mechanism plus Tier 3 $+5\alpha$ pole-mass normalization and the Tier 2 tau mechanism plus Tier 3 tau coefficient $(1 - 3.6\alpha)$ pending O.26b have been applied (the truly bare $\phi^{11}$ and $\phi^{17}$ ratios sit at $-3.75\%$ and $+2.69\%$ vs PDG; the $\sim 0.25\%$ figure is the first-order-corrected precision). The muon and tau first-order precision claims therefore inherit Tier 3 coefficient-normalization status, while the 21 ppm muon precision further depends on A3 and the SM-equivalent loop-order discipline stated in App R §R.2.1. The canonical headline significance for the lepton-pair claim is **~2.6σ** (broad internal look-elsewhere per the Firewall §3 Master Statistical Table); the **~3.1σ** Conservative-SM-texture-window-conditional figure and the **4.4σ** depinning-threshold-window-conditional figure are conditional auxiliaries with their conditioning priors named.

---

**8.6 The Koide Convergence**

**8.6.1 Candidate identification of K = 2/3 [Tier 3 — derivation chain pending closure target]**

The empirical Koide formula, $K = (m_e + m_\mu + m_\tau)/(\sqrt{m_e} + \sqrt{m_\mu} + \sqrt{m_\tau})^2 \approx 2/3$ (measured $K = 0.666661$, Koide 1983 *Phys. Lett. B* 120:161), is a *candidate* GCT identification with a Binary Icosahedral Group ($2I$) Unitarity Sum-Rule: the three generations would represent three orthogonal orientations in the $2I$ flavor-space, and the ratio $2/3$ would be the geometric limit required to preserve unitarity of the $6D \to 3D$ projection in the rigid-lattice limit ($\alpha \to 0$). **Tier disposition: Tier 3 candidate identification, *not* Tier 2 derived.** The current paragraph is a *sketch* of a derivation chain — the explicit formal steps (the $2I$ irrep decomposition of the lepton-mass flavor space, the orthogonality calculation, the unitarity sum-rule algebra, the explicit projection chain to the square-root-mass form of $K$, and an engine cross-reference comparable to the §8.3.2 / §8.3.3 derivations of the $+5\alpha$ and $-3.6\alpha$ coefficients) are *not* presently published. Until those steps are exhibited, the Koide ratio in GCT is at the same Tier-3-candidate-identification status as path (k) of App H O.14 was for the electron exponent before path (l) closure: a structurally suggestive coincidence with a candidate icosahedral home, awaiting the formal derivation that would lift it to Tier 2. **Closure target.** Either (a) supply the formal $2I$ unitarity-sum-rule derivation chain with explicit irrep-decomposition arithmetic and engine cross-reference (the closure-positive outcome that would promote this section to Tier 2), or (b) re-anchor the GCT-Koide identification to a different icosahedral group-theoretic invariant if the $2I$ unitarity argument does not survive scrutiny.

Independent of the above derivation status, note that the Koide formula is itself $\alpha$-independent (it is a square-root-mass sum rule), so the "$\alpha \to 0$ rigid-lattice limit" framing above does not by itself supply the load-bearing derivation step; the $\alpha$-independence is what makes the §8.6.2 Dynamic Cancellation observation a candidate consistency check rather than a closure.

**8.6.2 Dynamic Cancellation of Deviations [Tier 3 — candidate consistency check]**

The §8.6.1 candidate identification predicts that the physical Koide ratio should be maintained near $2/3$ if the $+5\alpha$ muon drag and $-3.6\alpha$ tau screening cancel in their contribution to the relevant mass sum. The two corrections do carry opposite signs and are quantitatively close in magnitude — consistent with a near-cancellation. The slight observed deviation ($K = 0.666661$ vs $2/3 = 0.666667$, residual $\sim 9 \times 10^{-6}$) is in principle a measure of the residual phason self-energy under this candidate identification, but the quantitative bookkeeping ($+5\alpha$ vs $-3.6\alpha$ in the square-root-mass-sum geometry, with the precise Tier 3 specific-value prediction for the deviation) is not currently exhibited as an engine-cross-referenced derivation. Tier 3 candidate consistency check pending §8.6.1 closure-target completion.

---

**8.7 Precision QED and the Muon g-2 HVP Contingency**

> [!WARNING] **WP2025 HVP ARBITRATION**
> Under the WP2025 lattice-QCD-dominant HVP synthesis, the SM-vs-experiment muon $g-2$ gap is only $\sim0.6\sigma$, while the GCT vertex correction lies above the consolidated SM central value. The channel is therefore **TENSION under WP2025** and is not load-bearing empirical validation of GCT. Historical WP2020/R-ratio baselines opened a larger $\sim4\sigma$ discrepancy window, but that baseline is carried only as the HVP-survival contingency in App V P.5, not as the operative disposition.

**8.7.1 The Geometric Vertex Correction**
The GCT quasicrystal topology produces a geometric vertex correction to the muon anomalous magnetic moment, $\Delta a_\mu^{GCT}$, arising from a geometric factor in the phason-sector vertex that is absent from Standard Model perturbation theory. Whether this correction functions as empirical evidence is contingent on the hadronic-vacuum-polarization synthesis (§8.7.2–§8.7.3): under the consolidated lattice-QCD HVP synthesis the SM–experiment gap is $\sim 0.6\sigma$ and the channel disposition is **Tension under WP2025; falsification conditional on long-term HVP-synthesis arbitration**, not a confirmed resolution.

**8.7.2 The 1/5 Factor from Euler Incidence**
The Rhombic Triacontahedron (RT) governs the icosahedral interaction node. The standard RT has $F=30$ rhombic faces, $V=32$ vertices (12 five-valent + 20 three-valent), and $E=60$ edges (Coxeter, *Regular Polytopes* §3.7). The relevant flux-channel count is not from the face/vertex/edge incidence directly but from the fivefold partition of the $I_h$ point group. The group-theoretic existence of the fivefold structure is Tier 2 mechanism; the step from that structure to an equal-weight numerical $1/5$ vertex factor is a **Tier 3 candidate coefficient** pending the O.26/O.5 first-principles vertex calculation.

This geometric $1/5$ factor dictates a 3-loop phason vertex correction:
$$ \Delta a_\mu = \frac{1}{5} \left( \frac{\alpha}{\pi} \right)^3 $$

**8.7.3 The Geometric Vertex Correction $\Delta a_\mu \approx 250.65 \times 10^{-11}$ [Tier 2 mechanism + A3 + Tier 3 $1/5$ coefficient + Tier 4 calibration-survival conjecture (HVP arbitration)]**
The application of this geometric $1/5$ factor using the observed CODATA low-energy $\alpha$ produces a 3-loop phason vertex correction $\Delta a_\mu \approx 250.65 \times 10^{-11}$. Crucially, the fundamental ground-state electron defect receives exactly **zero** lattice correction at this order, preserving its baseline QED precision. Under the consolidated lattice-HVP synthesis (Aliberti et al. 2025 WP2025) the SM–experiment residual is $\approx 0.6\sigma$ and the GCT geometric correction sits $\sim 3.4\sigma$ *above* the consolidated SM total — the channel disposition is therefore **Tension under WP2025; falsification conditional on long-term HVP-synthesis arbitration**. The Tier 2 status applies to the geometric *mechanism* (the $I_h$ fivefold-channel partition); the equal-weight numerical $1/5$ vertex factor and the use of A3 measured low-energy $\alpha$ remain Tier 3/A3 provenance inputs pending the O.26/O.5 first-principles vertex calculation. The Tier 4 status applies to the *calibration-survival conjecture* that the HVP synthesis will eventually re-converge toward a dispersive-dominant baseline under which the gap reopens. The HVP-Survival Condition in App V P.5 is the load-bearing condition for the channel's status as evidence.

> [!CAUTION]
> **HVP Dependence — empirical status:** The GCT muon g-2 closure is computed against the Standard Model HVP synthesis. Two reference synthesis classes are operative in the community: the dispersive R-ratio class (2020 Standard Model White Paper, WP2020: $a_\mu^{SM} = (116591810 \pm 43) \times 10^{-11}$) and the lattice-QCD-dominated class (Muon g-2 Theory Initiative 2025 update, Aliberti et al., *arXiv:2505.21476*: $a_\mu^{SM,\,\text{WP2025}} = (116592033 \pm 62) \times 10^{-11}$). The two classes are statistically incompatible at $\approx 3\sigma$. The Fermilab E989 final combined Run 1-6 result reports $a_\mu^{exp} = (116592070.5 \pm 14.8) \times 10^{-11}$ (127 ppb). Against the WP2025 lattice synthesis the SM–experiment gap is $\approx 37 \times 10^{-11}$, or $\sim 0.6\sigma$ under combined uncertainty — consistent with the SM, with no significant residual. Against a WP2020-class dispersive synthesis the gap is $\approx 4$–$5\sigma$. The GCT prediction $\Delta a_\mu^{GCT} = (1/5)(\alpha_{\rm CODATA}/\pi)^3 \approx 250.65 \times 10^{-11}$ is therefore a *contingent postdiction / HVP-survival condition*: it tracks a $\approx 4$–$5\sigma$ discrepancy under a dispersive-dominant synthesis and is in tension under the WP2025 lattice-dominant synthesis because it overshoots the residual gap.
>
**HVP Contingency Decision Table (canonical disposition).** **Scenario B is the current empirical disposition** under the WP2025 consolidated SM theory baseline (Aliberti et al. 2025). Scenarios A and C are counterfactual / contingent dispositions held against alternative synthesis classes that are not currently consolidated.

| HVP scenario | Standard Model $\Delta a_\mu$ tension | GCT prediction status |
|---|---|---|
| **Scenario A — dispersive R-ratio dominant** | $\approx 4.2$–$5.2\sigma$ anomaly | **Counterfactual disposition under R-ratio-dominant synthesis.** $\Delta a_\mu^{GCT} \approx 250.65 \times 10^{-11}$ would resolve the anomaly to $\leq 0.1\sigma$. The 1/5 RT geometric vertex correction would be a successful prediction of GCT under this synthesis. |
| **Scenario B — lattice-dominant synthesis** | $\approx 0.6$–$1.5\sigma$ residual | **Tier 3 fitted/equal-weight $1/5$ coefficient + A3; Tension under WP2025; no robust confirmation.** The 1/5 RT correction is mathematically present in the GCT framework as a candidate equal-weight vertex coefficient, but the consolidated SM–experiment residual under this synthesis is small, the CMD-2/CMD-family R-ratio reanalysis context does not restore a decisive anomaly, and the GCT correction overshoots the WP2025 residual. The muon g-2 channel is not load-bearing as empirical evidence for GCT under this synthesis. |
| **Scenario C — Continued inconsistency between R-ratio and lattice methods** | Unresolved | **GCT Tier 2 status held pending.** The prediction is parked as a binary-gate observable awaiting community resolution; no claim of validation or falsification can be made from muon g-2 alone. |

Under all three scenarios, the GCT 1/5 geometric vertex correction *itself* is unaffected (it is the registered $I_h$ fivefold-channel mechanism, not a fit to data); only the *evidential weight* of the muon g-2 channel for GCT support depends on the HVP synthesis. The empirical status sits in Scenario B (lattice-dominant synthesis), with the App R §R.2 row recording the corresponding closure-to-data figure. The HVP-Survival Condition in App V P.5 determines whether the channel becomes load-bearing evidence; the dependence is explicit.

**8.7.4 The Kinematic Activation Threshold**
A crucial consistency check is why the electron ($a_e$) receives no activated lattice vertex correction at this loop order. This is a strict **kinematic threshold limit**: the threshold mechanism is Tier 2, while the numerical $N=11$ depinning exponent inherits the Tier 3 status of the muon anchor.

To emit the vertex correction loop, the lepton must possess enough rest-mass energy to excite to the fundamental acoustic cage resonance (the $N=11$ harmonic *depinning* threshold). The required energy is:
$$E_{res} = m_e \cdot \phi^{11} \approx 101.69\text{ MeV} \quad \text{[Tier 2 mechanism + Tier 3 threshold exponent $N=11$]}$$
The electron's rest mass is only $\sim 0.511$ MeV. It is roughly 198 times too light to activate the loop; it lacks the $\sim 101.18$ MeV gap required to depin the acoustic cage resonance. The electron acts as a point-like fundamental $N=0$ mode.

However, the muon ($\sim 105.66$ MeV) sits precisely above this threshold as the $N=11$ resonance. It has sufficient mass-energy to activate the loop, acquiring the candidate geometric correction. **GCT's vertex correction at this loop order is $\Delta a_\mu \approx 250.65 \times 10^{-11}$ via the equal-weight $1/5$ factor [Tier 3 fitted/equal-weight coefficient + A3 on top of a geometric mechanism class; Tension under WP2025 — the channel sits $\sim 3.4\sigma$ above the consolidated SM total after the reduced world-average tension and is not load-bearing as empirical evidence; see §8.7.3 Scenario B for the current empirical posture].**

---
**END OF CHAPTER 8**
