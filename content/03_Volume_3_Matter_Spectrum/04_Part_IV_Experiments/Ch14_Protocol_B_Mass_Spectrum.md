### **Chapter 14: Protocol B (Mass Spectrum Computation)**

The derivation of the lepton mass hierarchy in Chapter 8 identifies the muon and tau as the 11th and 17th harmonics of the electron's dodecahedral cage. To audit these results against the engine ledger, we employ **Protocol B**: a deterministic verification of the projected lattice geometry. This protocol computes the charged-lepton mass ratios from the Tier 2 harmonic-ladder mechanism plus the Tier 3 integer anchors $N=11$ and $N=17$ per Parameter Ledger §0.1; first-principles unique-eigenvalue extraction remains open under O.5/O.14/O.15.

---

**14.1 Methodology**

**14.1.1 Algorithm: Projected Lattice Dynamics**

The analysis models the vacuum as an Ammann-Kramer-Neri (AKN) tiling, generated via the Cut-and-Project method from the 6-dimensional hyper-lattice $\mathbb{Z}^6$. We construct the **Geometric Resonance Matrix ($\mathbf{G}$)**, which represents the coupled harmonic structure of the $N=144$ dodecahedral cage.

Unlike standard molecular dynamics, which operate in 3D Euclidean space, the GCT algorithm operates on **Projected Degrees of Freedom**. Each node $i$ in the 6D parent lattice possesses a 6D displacement vector $\mathbf{U}_i$. Upon projection into the physical manifold, this vector is partitioned into physical ($\mathbf{u}_\parallel$) and internal ($\mathbf{u}_\perp$) components. The interaction energy of a bond between nodes $i$ and $j$ is defined by the stiffness hierarchy derived in Volume 2:
$$V_{ij} = \frac{1}{2} K_\parallel (\Delta \mathbf{u}_\parallel \cdot \hat{\mathbf{n}}_\parallel)^2 + \frac{1}{2} K_\perp (\Delta \mathbf{u}_\perp \cdot \hat{\mathbf{n}}_\perp)^2$$
The analysis solves for the **Node-Centric Eigenvalues** (eigenstates of the center-of-mass motion), distinguishing these from the interface stress energies (surface area mismatches) utilized for the hadron spectrum.

**14.1.2 Parameters: The Phason Stiffness Ansatz ($D=18$) [Tier 2 integer identification (D=18) + Tier 3 heuristic stiffness-ratio map — Parameter Ledger §0.1 P3; Open Problem O.15]**

The analysis requires exactly one material input: the ratio of phason stiffness to phonon stiffness.

No tree-level stiffness ratio follows from the projection geometry. The earlier "theorem" that the Gram eigenvalue ratio of the 6D$\to$3D projection gives $\eta_0 = \phi^{-2}$ is withdrawn: $\phi^{-2}$ is a raw-frame (legacy single-chart) Gram ratio, which changes under row rescaling and equals 1 for the canonical row-isometric projectors (App DPS §DPS.2–3; V3 Ch04 §4.1.2), so it is a normalization convention and not a physical stiffness. The picture in which phonon-phason coupling suppresses $K_\perp$ under RG flow at the relevant physical scale is a GCT conjecture [Tier 3], not a result taken from the quasicrystal hydrodynamics literature (Lubensky, Ramaswamy and Toner 1985 treat the phason elastic constants as independent effective-theory parameters).

We set $n=18$ as a **Tier 2 integer identification (D=18) + Tier 3 heuristic stiffness-ratio map** (Parameter Ledger §0.1 P3 canonical disposition; first-principles RG closure tracked under Open Problem O.15). The two layers are kept separate: $D_{H_3}=2+6+10=18$ is the Tier 2 Coxeter integer, while the physical map $K_\perp/K_\parallel=\phi^{-18}$ is the independent Tier 3 hypothesis P3b (Parameter Ledger §0.1; O.15). Like H-EW, P3b is a registered Tier 3 hypothesis listed outside the core-input count; only the integer $D=18$ is Tier 2, and P3b is a bare stipulation. Arithmetic rewritings of $\phi^{-18}$ (for example as $(\phi^{-2})^9$ over nine phonon-phason channels, or the $H_3$-Coxeter rank × Galois × dimension count of App DPS §DPS.4) are not derivations and give it no support. The former cube-of-Gram-determinant route (App DPS §DPS.3) is retired: the Gram-determinant ratio depends on the coordinate frame (a row rescaling changes it by $s^{18}$, and canonical row-isometric projectors give 1). Icosahedral $H_3/I_h$ symmetry permits a quadratic stiffness form $Q=aP_\parallel+bP_\perp$ with $b/a$ free, and the isotropic parent action gives $b/a=1$, so symmetry alone does not fix $\phi^{-18}$ [Tier 1 representation theory]. The earlier claim of empirical support from a $10^{-2}$–$10^{-1}$ i-AlMnSi / i-AlPdMn phason/phonon band, and of a quantitatively derived chemical-bonding floor, is also retired: the quasicrystal measurements cited for it concern $K_2/K_1$ phason elastic anisotropy and diffusive relaxation kinetics rather than a phason/phonon stiffness ratio, and the DFT reference cited for the floor (DOI 10.1103/PhysRevB.88.144102) is Xiao et al. (2013) on the CaIrO$_3$ post-perovskite transition, not i-AlPdMn. Every numerical use of $\phi^{-18}$ below is therefore conditional on P3b; first-principles microscopic, action-level or RG closure remains Open Problem O.15.

The input parameter for the phason stiffness is set, conditional on the Tier 3 hypothesis P3b, as:
$$\frac{K_\perp}{K_\parallel} = \phi^{-18} \approx 1.7307 \times 10^{-4}$$

**14.1.3 Computational Setup: Harmonic Ansatz Evaluation**

The $6N \times 6N$ geometric projection matrix is analyzed to extract the spectrum of eigenfrequencies $\{\omega_k\}$. Because quasicrystalline spectra can be **singular continuous** (proven for one-dimensional Fibonacci-type models; not established for 3D icosahedral operators), eigenvalues are expected to cluster in a complex hierarchy. Protocol B utilizes a **Harmonic Ansatz Evaluation** to target the specific pseudo-gaps ($\phi^{11}$ and $\phi^{17}$) without the algorithm becoming lost in the dense background of uncoupled phason modes.

The evaluation identifies the fundamental breathing mode resonance ($\omega_0$), which represents the electron's mass-energy.

**14.1.4 Numerical Convergence and the Local Isomorphism Shield**

Stability is probed by increasing the cluster size from the $N=144$ core toward an $N=2000$ node neighborhood. The dodecahedral cage satisfies the local matching rules of the icosahedral projection, so by local isomorphism every finite patch recurs throughout the tiling; local isomorphism concerns patch recurrence and implies no spectral protection by itself. The picture of the aperiodic background as a **Topological Shield**, in which the $N=144$ symmetry acts as a resonant cavity that filters out local fluctuations and would yield a mass eigenvalue protected against local environmental disorder, is a Tier 3 heuristic; no such eigenvalue has yet been extracted (§14.2). A specific numerical convergence rate is not asserted here: the finite-$N$ discretization artifact present in the direct graph extraction (§14.2; `protocol_lepton_spectrum.py`) is why first-principles non-perturbative eigenvalue closure remains open (O.5/O.14/O.15).

---

**14.2 Validation and Results**

> [!CAUTION]
> **The Linear Boundary Constraint — read this before the precision tables below.** Extensive HPC analysis of the full sparse Hessian (see Appendix GPE) confirms that the bare linear dynamical matrix yields normalized eigen-ratios of `[1.0, 1.67, 2.1, 2.52...]`. Neither $\phi^{11}$ nor $\phi^{17}$ emerge spontaneously from linear diagonalization. 
> 
> The leptons are non-linear phason solitons whose exact mass scaling is governed by the $6N \pm 1$ symmetry saturation, not linear oscillatory modes. The $\phi^{11}$ and $\phi^{17}$ gap alignments are therefore **Tier 2 Geometric Postulates** (the harmonic-ladder structure committed to in Parameter Ledger §0.1 P4/P5) plus the **Tier 3 specific integer choices** $N=11$ (muon) and $N=17$ (tau). The non-perturbative computational extraction of these solitonic eigenvalues from first principles remains an open goal for the GCT framework. The bare $\phi^{11}$ / $\phi^{17}$ residuals are $-3.75\%$ / $+2.69\%$; after the Tier 3 first-order coefficients the muon reaches ~0.24% (the tau's first-order formula is its full formula, −51 ppm), and the ppm-level figures in §14.2.3 below are Tier 3 formula residuals against measured masses (the muon mass is measured to 22 ppb, CODATA 2022), not precision claims.

**14.2.1 The Harmonic Ansatz and the Linear/Non-Linear Boundary [Tier 2 Postulate]**

The primary non-linear pseudo-gaps of the dodecahedral cage correspond to the 11th and 17th harmonics of the inflation operator. Under the **Geometric Harmonic Ansatz**:
* **Muon Target:** $\phi^{11} \approx 199.005$ [Tier 2 Postulate]
* **Tau Target:** $\phi^{17} = L_{17}+\phi^{-17} \approx 3571.0003$ [Tier 2 Postulate] ($L_{17}=3571$ is the Lucas number)

**14.2.2 Precision Mass Audit**

We apply the phason drag corrections derived in Chapter 8 to the geometric eigenvalues. For the Muon, we include the **Second-Order Phi-Alpha Correction** ($\phi^8\alpha^2=\phi^{-3}\times\phi^{11}\alpha^2$: Tier 2 exponent arithmetic, verified computationally, see Appendix GPE; reading its $\phi^{-3}$ factor as an electroweak mixing projection rests on the Tier 3 hypothesis H-EW, V3 Ch04 §4.3.2). The residual error of **−21 ppm ($-0.0021\%$)** for the Muon (lepton-spectrum protocol; App PSC §PSC.1) is about $10^3\sigma$ against the 22 ppb CODATA 2022 measurement uncertainty, so the formula does not reproduce $m_\mu$ at measurement precision; it is a Tier 3 formula residual. (The earlier reading of it as inside a "$\sim$10–40 ppm higher-loop theory floor" is withdrawn: Standard-Model radiative corrections are not an uncertainty on a measured mass.) The next geometric correction enters at third order carrying a $\phi$-power coefficient comparable to the $\phi^8$ second-order term — $\phi^8\alpha^3 \approx 1.8 \times 10^{-5}$ [Tier 3 — order-of-magnitude estimate by analogy to the second-order coefficient], the same size as the residual, so the row tests nothing beyond first order — whereas the bare uncoefficiented **Third-Order Radiative Correction** $\alpha^3 \sim 3.9 \times 10^{-7}$ [Tier 1 — QED perturbation theory] alone is two orders smaller. Native first-principles loop closure remains open under O.5/O.14/O.15.

**14.2.3 Final Lepton Mass Table vs. PDG**

| **Particle** | **Geometric Exponent** | **GCT formula value (postdiction; MeV)** | **Observed (MeV)** | **Relative Error** |
| :--- | :---: | :--- | :--- | :--- |
| **Electron** | $0$ | **0.5109989** (input, anchor A1) | $0.5109989$ | **Base Scale** |
| **Muon** | $11$ | **105.656** [Tier 2 mechanism (harmonic ladder, conditional on the Tier 3 $\phi$-step, V3 Ch08 §8.1.2) + Tier 3 specific exponent N=11 per Ledger §0.1 P4] | $105.6583755(23)$ (CODATA 2022) | **~−21 ppm (Tier 3 formula residual)** |
| **Tau** | $17$ | **1776.84** [Tier 2 mechanism (harmonic ladder, conditional on the Tier 3 $\phi$-step, V3 Ch08 §8.1.2) + Tier 3 specific exponent N=17 per Ledger §0.1 P5] | $1776.93 \pm 0.09$ (PDG 2024) | **~−51 ppm (−0.0051%)** |

**14.2.4 The Tau Comparison**

For the tau, the GCT value $1776.84$ MeV lies $0.09$ MeV ($\sim$51 ppm, about $1\sigma$) below the PDG 2024 value $1776.93 \pm 0.09$ MeV ($\sim$0.005%). The GCT number carries no propagated theoretical uncertainty: the Tier 3 exponent $N=17$, the inserted Tier 3 tau correction rule and the unpropagated next-order term are not converted into an error bar. The number of displayed digits is therefore not a precision claim, and the formula is not more precise than experiment. Future high-luminosity lepton-collider and tau-threshold measurements would tighten this postdiction comparison; it is not a prediction.

**Conclusion:**
Protocol B treats the charged lepton mass hierarchy as a **deterministic spectral fingerprint** candidate of the 6D hyper-lattice. The match across multiple generations using the icosahedral geometric framework (parameterised by $\phi$ as the structural constant, plus the integer-valued harmonic exponents $N = 11, 17$ which enter as Tier 3 specific values per Parameter Ledger §0.1 P4/P5 — not as additional fitted parameters but as structural commitments of the framework) is consistent with the harmonic-ladder mechanism, but no global significance is claimed for it (V3 Ch08 §8.5). As evidence that φ or icosahedral structure is special, this match is **Tier 4**: the preregistered constant control test (v3, NEGATIVE-FRAGILE; App PSC §PSC.9.6) found φ's pattern of matches on 21 constants not distinguishable from that of random constants (58 of 300 random bases did at least as well). The test "excludes, at power ≥ 0.8, an effect in which φ hits at least 6 of the 8 informative rows through a real effect; weaker effects are not excluded." The numbers are kept as descriptive arithmetic, while first-principles unique-eigenvalue extraction remains open under O.5/O.14/O.15. References to $\phi$ as the structural constant are structural-constants-only language; the 5-postulate-plus-1-anchor bare lepton-ratio sub-sector (the bare $\alpha$ relation $360\phi^{-2}$ is a separate Tier 3 numerical relation, mechanism open; the corrected lepton rows also need A3, H-EW and the Tier 3 coefficient rules), with the native-RGE endpoint and precision-comparison rows adding anchors A2–A6 (Parameter Ledger §0.1), is the load-bearing tier discipline.

**END OF CHAPTER 14**
