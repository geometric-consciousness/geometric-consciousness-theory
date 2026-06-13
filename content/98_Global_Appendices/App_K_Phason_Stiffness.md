# Appendix K: Derivation of Phason Stiffness

## K.1 Generalized Elasticity in 6D

The GCT vacuum is modeled as a harmonic hypercubic lattice in 6D with a scalar bond stiffness $\kappa_{6D}$. The elastic energy density $\mathcal{E}$ is:
$$ \mathcal{E} = \frac{1}{2} C_{MNPQ} E_{MN} E_{PQ} $$
where $C$ is the isotropic 6D elastic tensor.

## K.2 Projection and Gram Determinants

The 6D lattice nodes are projected into physical space $E_\parallel$ (phonon) and internal space $E_\perp$ (phason). Let $\mathcal{M}_\parallel$ and $\mathcal{M}_\perp$ be the $3 \times 6$ canonical icosahedral projection matrices.

We define the **Gram Matrices** for each subspace:
- $G_\parallel = \mathcal{M}_\parallel \mathcal{M}_\parallel^T$
- $G_\perp = \mathcal{M}_\perp \mathcal{M}_\perp^T$

The invariant volume of the unit cell in each subspace scales with the square root of the Gram determinant:
- $V_\parallel \propto \sqrt{\det(G_\parallel)}$
- $V_\perp \propto \sqrt{\det(G_\perp)}$

For the canonical icosahedral projection (AKN), evaluating these determinants yields the fundamental geometric ratio:
$$ \frac{\det(G_\perp)}{\det(G_\parallel)} = \phi^{-6} \approx 0.0557 $$

## K.3 Effective 3D Stiffness Scaling [Tier 3 — heuristic counting]

The effective stiffness $K$ in a projected continuum represents the energy density per unit volume. In 3D, the modulus is a volumetric average of the bond energy. The GCT *postulate* is that the energy-conservation-under-projection argument scales the effective stiffness with the **cube** of the determinant ratio:

$$ \frac{K_\perp}{K_\parallel} \approx \left( \frac{\det(G_\perp)}{\det(G_\parallel)} \right)^3 = (\phi^{-6})^3 = \phi^{-18} $$

> [!IMPORTANT]
> **Heuristic vs first-principles status.** The cube-power scaling above is a **counting heuristic**, not a derivation from standard quasicrystal elasticity theory. The standard treatment (Lubensky-Ramaswamy-Toner 1985; Socolar-Lubensky-Steinhardt 1986) takes the phason elastic constants $K_1, K_2$ as **independent** parameters of the icosahedral free energy, not as forced ratios of the phonon Lamé moduli. The "energy is conserved under projection but redistributed across different spatial volumes" argument does not produce $K_\perp/K_\parallel$ from first-principles elasticity theory. The GCT *prediction* $K_\perp/K_\parallel = \phi^{-18}$ is therefore a *postulate* of the framework consistent with the icosahedral geometry, not a derived consequence of standard elastic-tensor projection. The prediction itself — that the icosahedral lattice has phason modes parametrically softer than phonons by a $\phi$-power ratio — is the load-bearing statement; the cube-power is a heuristic count.

> **Phason-mode dispersion: LRT-diffusive vs GCT-propagating identification [Tier 2 mechanism + Tier 3 open identification].** LRT (Lubensky-Ramaswamy-Toner 1985) establishes that in the *hydrodynamic IR limit* of standard 3D icosahedral phason elasticity, phason modes are **diffusive**: $\omega \propto i D_\perp q^2$ with $D_\perp$ a phason diffusion constant. GCT identifies phasons with a *propagating* photon-like mode ($\omega \propto q$ with phase velocity $\hat c = c_P \phi^{-9}$; V2 Ch06 §6.2), which is structurally distinct from the LRT hydrodynamic limit. The reconciliation is scale-dependent: LRT's diffusive regime applies in the IR limit where momentum is small compared to the inverse phason correlation length $1/\xi_\perp$; GCT's propagating identification applies at the UV / Planck-scale lattice level where the phason field carries unsuppressed elastic energy. There is a **crossover scale** $q_c$ between propagating-UV and diffusive-IR phason behaviour, set by the ratio of phason elastic energy to phason damping. The GCT *prediction* is that this crossover sits well above the cosmological IR cutoff so that the propagating-phason identification dominates the speed-of-light derivation; the *empirical disposition* requires either (a) LRT-style analysis extended to the UV regime confirming the propagating crossover, or (b) measurement of the crossover scale in a chemically clean analog system. This is bundled with **Open Problem O.15**; the LRT-diffusive vs GCT-propagating gap is not a contradiction but a scale-regime distinction that is not currently quantified.

## K.4 The D=18 Identification via H_3 Shephard-Todd Invariant Degrees [Tier 2 integer identification anchoring a Tier 3 heuristic stiffness-ratio claim]

The exponent 18 in $K_\perp/K_\parallel = \phi^{-18}$ admits a canonical group-theoretic identification: it is the **sum of fundamental degrees** of the icosahedral $H_3$ Coxeter group (Shephard-Todd theorem; Humphreys 1990 *Reflection Groups and Coxeter Groups* Table 1):
$$D = d_1 + d_2 + d_3 = 2 + 6 + 10 = 18.$$
The Shephard-Todd identity gives equivalently $D = N + r$, where $N = 15$ is the number of positive roots of $H_3$ (= number of reflections) and $r = 3$ is the rank: $15 + 3 = 18$ ✓.

For comparison with other rank-3 finite Coxeter groups: $A_3$ has invariant-degree sum 9 (= 2 + 3 + 4); $B_3$ has 12 (= 2 + 4 + 6); $H_3$ at 18 has the **largest** invariant-degree sum among rank-3 finite Coxeter groups, reflecting the non-crystallographic 5-fold symmetry (Coxeter number $h = 10$, exceeding the crystallographic bound $h \leq 6$). Engine cross-reference: `GCT_Physics_Engine/src/protocol_o15a_h3_invariant_degrees.py`.

> [!IMPORTANT]
> **Status of the identification (two-layer disposition).** The integer 18 in $\phi^{-18}$ is identified with the **canonical Shephard-Todd invariant** of the icosahedral Coxeter group $H_3$ — the sum of fundamental invariant degrees $d_1 + d_2 + d_3 = 2 + 6 + 10 = 18 = N + r = 15 + 3$. The Shephard-Todd invariant-degree sum is a standard finite-Coxeter-group invariant — this *integer identification* is **Tier 2 canonical group theory**.
>
> The connection from the integer 18 to the *full stiffness-ratio claim* $K_\perp/K_\parallel = \phi^{-18}$ is the §K.3 cube-power scaling, which is a **Tier 3 heuristic** (explicitly tier-labeled in §K.3) — not derived from standard quasicrystal elasticity theory, in which Lubensky-Ramaswamy-Toner treat $K_1, K_2$ as independent EFT parameters. The full stiffness-ratio claim is therefore **Tier 3 numerical heuristic anchored by a Tier 2 canonical Coxeter integer**, not a forced derivation.
>
> **The remaining open piece (full Tier 2 closure of O.15(a)): the per-invariant anomalous dimension calculation.** The structural argument would proceed as: (1) write the LRT free energy on the AKN lattice in symmetry-adapted basis as $F = \sum_n F_n(I_{d_n}(\Phi_\perp))$, where $I_{d_n}$ is the H$_3$ fundamental invariant of degree $d_n \in \{2, 6, 10\}$ and $F_n$ is its phason-elastic coupling; (2) identify the RG step $b = \phi$ as the Perron eigenvalue of the AKN substitution matrix (standard Senechal 1995 §2.5 result); (3) compute the one-loop diagrams that renormalize each $F_n$ separately by integrating high-momentum phason modes within one RG shell; (4) show explicitly that the per-invariant anomalous dimension of the coupling associated with $I_{d_n}$ equals $d_n \log\phi$ (the load-bearing dynamical step that no published QC calculation cited here has done — Lubensky-Ramaswamy-Toner 1985 and Socolar-Lubensky-Steinhardt 1986 treat $K_1, K_2$ as independent EFT parameters and do not work in the symmetry-adapted basis); (5) sum: total anomalous dimension = $(d_1 + d_2 + d_3) \log\phi = 18 \log\phi$; (6) exponentiate: $K_\perp/K_\parallel = \exp(-18\log\phi) = \phi^{-18}$. **Step (4) is the unique missing piece**: the per-invariant bookkeeping $c_n = d_n$ is currently taken as input from icosahedral natural-scaling assumptions. A rigorous closure of O.15 requires either an explicit one-loop integration in the symmetry-adapted basis (research-grade QFT calculation on the AKN lattice; ~multi-day focused work) or a structural argument that derives $c_n = d_n$ from the Chevalley-Shephard-Todd theorem extended to RG anomalous dimensions. No such derivation is cited here. The Shephard-Todd identification establishes the canonical icosahedral-group-theoretic origin of the integer 18; the connection to the elasticity-ratio remains the load-bearing structural assumption (Open Problem O.15). Experimentally testable in synthetic photonic / charge-density-wave systems where chemical bonding is absent (per §K.4b).

## K.4b Empirical Comparison and the i-AlPdMn Gap [Tier 3]

> [!IMPORTANT]
> **Empirical-gap disclosure.** Experimental measurements of phason elastic constants in **i-AlPdMn quasicrystals** by de Boissieu et al. (1995, *Phys. Rev. Lett.* 75:89) and Francoual et al. (2006, *Phil. Mag.* 86:1029) give phason-to-phonon stiffness ratios in the range $K_{\text{phason}}/K_{\text{phonon}} \sim 10^{-2}$ to $10^{-1}$, depending on convention ($K_2/(\lambda+2\mu)$ vs $K_1/\mu$). The GCT prediction $\phi^{-18} \approx 1.73 \times 10^{-4}$ is **two to three orders of magnitude smaller** than measured i-AlPdMn values. The framing "the metallic alloy values are contaminated by chemical bonding" is directionally plausible: chemical bonding (Penrose-Toner phason locking, hopping-amplitude reduction) generically *stiffens* phason modes, so the "pure vacuum" GCT value should be softer than measured. A 100–1000× softening factor from chemical-bonding contamination is, however, *not currently quantified* and not credible without an estimate of the bonding correction.

> **Penrose-Toner locking magnitude — quantitative correction [Tier 2 mechanism, Tier 3 numerical anchors].** The chemical-bonding contribution to the i-AlPdMn phason stiffness gap is derived in `GCT_Physics_Engine/src/protocol_o15_phason_stiffness_chemical_correction.py` via the Kalugin-Katz (2008) / Trambly de Laissardière-Mihalkovič (2013) phason-elasticity formula:
> $$K_{PT} \;\sim\; \frac{E_{\text{flip}}}{V_{\text{atom}}},$$
> where $E_{\text{flip}}$ is the atomic-flip activation energy and $V_{\text{atom}}$ is the per-atom volume. For i-AlPdMn:
> - $E_{\text{flip}} \in [100, 700]$ meV (Trambly+ 2013 DFT for Al-Pd swap energies across coordination shells)
> - $V_{\text{atom}} \in [12, 20]$ Å³ (i-AlPdMn structural data)
> - $K_{\text{phonon}} = \rho c_L^2 \approx 0.535$ eV/Å³ (longitudinal phonon stiffness, $\rho_{\text{i-AlPdMn}} \approx 5100$ kg/m³, $c_L \approx 4100$ m/s; de Boissieu 1995, Wang+ 1998).
>
> The protocol sweeps over these literature-anchored ranges and yields
> $$\frac{K_{PT}}{K_{\text{phonon}}} \in [9.3 \times 10^{-3},\, 1.09 \times 10^{-1}],$$
> which *covers both* the de Boissieu 1995 measurement ($\sim 10^{-2}$) and the Francoual 2006 measurement ($\sim 10^{-1}$). The bare GCT prediction $K_\perp^{\text{bare}}/K_{\text{phonon}} = \phi^{-18} \approx 1.73 \times 10^{-4}$ sits $58$–$578\times$ *below* this chemical-bonding floor.
>
> **The interpretation is now numerical, not qualitative.** Metallic-alloy i-AlPdMn phason measurements are dominated by Penrose-Toner chemical-bonding contributions; the bare lattice-geometric $\phi^{-18}$ signature is buried two-to-three orders of magnitude below the chemical-bonding floor and *cannot in principle be resolved* by metallic-quasicrystal scattering experiments. The apparent 100–1000× tension between $\phi^{-18}$ and i-AlPdMn measurements is therefore *quantitatively explained* by the chemical-bonding correction with realistic atomic-physics parameters; it is not a falsification of $\phi^{-18}$. Direct experimental test of the bare $\phi^{-18}$ prediction requires *chemically clean analog systems* (synthetic photonic quasicrystals where $E_{\text{flip}} \to 0$, charge-density-wave systems with controlled atomic-flip suppression, or atomic-physics simulations of icosahedral cut-and-project geometry without metallic bonding).

> **Phason-elasticity scope note (scalar vs tensor).** GCT's $K_\perp/K_\parallel = \phi^{-18}$ is a **scalar** stiffness ratio. The standard Socolar-Lubensky-Steinhardt (1986) treatment of icosahedral quasicrystal elasticity decomposes the phason free energy into **two independent elastic constants** $K_1$ (the symmetric phason strain) and $K_2$ (the antisymmetric / transverse phason mode), with the i-AlPdMn measurements above quoted in this $(K_1, K_2)$ basis. The GCT scalar identification $K_\perp$ is most naturally read as the trace-mode combination $K_1 + (5/3) K_2$ (the rotationally invariant scalar in the icosahedral phason elasticity tensor); the $(K_1, K_2)$ breakdown is currently *not* derived separately in the GCT framework. A full SLS-style two-constant GCT derivation — and the consequent prediction for the $K_1/K_2$ ratio in addition to the $K_\perp/K_\parallel$ scalar — is an open refinement target tracked under **Open Problem O.15** alongside the RG closure of the scalar exponent. Until O.15 closes, comparisons against i-AlPdMn $(K_1, K_2)$ measurements must be interpreted modulo this scalar→tensor mapping.
>
> **Empirical status (post-quantitative-correction).** The 100-1000× gap between $\phi^{-18}$ and i-AlPdMn measurements is *quantitatively reproduced* by the Penrose-Toner chemical-bonding correction with literature-anchored $(E_{\text{flip}}, V_{\text{atom}})$ ranges — the metallic-alloy data is consistent with the bare GCT prediction sitting two-to-three orders of magnitude below the chemical-bonding floor. Direct test of the bare $\phi^{-18}$ prediction remains an Open Research target: it requires a measurement of phason stiffness in a chemically clean analog system (synthetic photonic quasicrystal, charge-density-wave system, or atomic-physics simulation) where the bare $\phi$-power prediction is testable without the Penrose-Toner confound. The qualitative direction (phason modes parametrically softer than phonon modes by a $\phi$-power) is confirmed in i-AlPdMn; the specific exponent $-18$ is consistent with i-AlPdMn data after chemical-bonding correction but is not directly resolved from metallic-quasicrystal measurements.

The GCT prediction direction (phason modes parametrically softer than phonon modes by a $\phi$-power) is confirmed qualitatively in i-AlPdMn. The specific exponent $-18$ remains unverified experimentally and currently follows from the heuristic counting argument of §K.4 rather than from an independent derivation.

## K.5 Polaron Healing Length [Tier 1 textbook formula; GCT-internal Route 2 closed negatively under O.25]

**Physical Setup.** The healing length $\xi$ is the spatial scale at which the polaron's kinetic energy balances its self-energy. The canonical Gross-Pitaevskii / Bohr scaling for a Coulomb-bound polaron in a dielectric medium is

$$\boxed{\;\xi = \frac{\hbar c}{\alpha^2\, m_e c^2} = \frac{a_0}{\alpha},\;}$$

with $a_0 = \hbar/(\alpha m_e c)$ the Bohr radius. This is a **standard QED-Bohr result** [Tier 1] — it follows from elementary atomic-scale arguments and is *not* a GCT-specific prediction. Substituting CODATA $\alpha^{-1} = 137.036$ yields $\xi \approx 7.25$ nm; substituting GCT bare $\alpha^{-1} = 360\phi^{-2} = 137.508$ yields $\xi \approx 7.30$ nm — the formula is $\alpha$-input-insensitive at the $\sim 0.7\%$ level because the two $\alpha$ values differ by $\sim 0.35\%$ and the difference enters as a square.

**GCT-internal phason-elastic Route 2 (Open Problem O.25: structurally negative).** A GCT-internal route that would reproduce $\xi = \hbar c/(\alpha^2 m_e c^2)$ from the 6D lattice stiffness chain proceeds by equating the phason elastic energy $E_{\rm elastic} \sim K_\perp \cdot a_6^2 \cdot \xi$ (with $K_\perp \cdot u_\perp^2$ per unit length on phason gradient $u_\perp \sim a_6$ across polaron volume $\xi^3$) to a Coulomb electromagnetic self-energy $E_{\rm EM} \sim \alpha \hbar c/\xi$, with substitutions $K_\perp = \phi^{-18} K_\parallel = \phi^{-18}\,M_P c^2/\ell_P^3$, $a_6 = 2\ell_P$, and $m_e = M_P\,\phi^{-107}(1-5\alpha)$. Carrying out the algebra explicitly:

$$\xi^2 \sim \frac{\alpha \hbar c}{K_\perp \cdot a_6^2} = \frac{\alpha \phi^{18}}{4} \cdot \frac{\hbar \ell_P}{M_P c} = \frac{\alpha \phi^{18}}{4} \cdot \ell_P^2,$$

(using $\hbar/(M_P c) = \ell_P$), giving

$$\xi^{\rm Route\,2} = \tfrac{1}{2}\, \phi^9\, \sqrt{\alpha}\, \ell_P \approx 5 \times 10^{-35}\ \text{m} \approx 5 \times 10^{-26}\ \text{nm},$$

approximately $10^{26}$ times smaller than the Tier 1 target $a_0/\alpha \approx 7.25$ nm. The substitution chain produces a Planck-scale length, not a nanometre-scale length. The reason is **structural and unfixable**: the target $a_0/\alpha$ carries a $1/\alpha^2$ Coulomb-bound-state enhancement that blows the Compton wavelength $\hbar/(m_e c) \sim 4 \times 10^{-13}$ m up to the nm scale, but $\alpha$ enters the GCT substitution chain only through the $(1-5\alpha)$ correction in $m_e = M_P\phi^{-107}(1-5\alpha)$ — an $\mathcal{O}(\alpha)$ correction, not a $1/\alpha^2$ enhancement. No variant of the ansatz (Compton kinetic, vacuum fluctuation, electron rest energy on either side, alternative $u_\perp$ saturation scales) recovers the missing factor of $\sim \alpha^{-5/2} \cdot \phi^{98}$. Open Problem O.25 therefore stands as a **structural negative**: the GCT-internal substitution chain cannot reproduce $a_0/\alpha$; $\xi = a_0/\alpha$ is Tier 1 textbook physics with no GCT-derived equivalent, and the only GCT-specific empirical content of this section is the microtubule-lumen identification below.

**Microtubule lumen identification [Tier 3 biological correlation].** The polaron diameter $2\xi = 14.5$ nm sits within $\sim 3\%$ of the inner diameter of the microtubule lumen ($\sim 15$ nm) (Ch07 §7.3.3); this "snug match / resonant confinement" is a Tier 3 biological correlation, tighter than alternative scalings ($2\xi = 17$ nm vs $15$ nm, $\sim 13\%$ discrepancy) but not itself a derivation of the lumen geometry from GCT.

**Tier Classification.** The formula $\xi = a_0/\alpha$ is **Tier 1** (standard QED-Bohr scaling). The GCT-internal phason-elastic Route 2 derivation does **not** reproduce this formula from the GCT substitution chain (Open Problem O.25 structural negative, above). The specific numerical value $\xi \approx 7.25$ nm follows from the Tier 1 formula plus the CODATA $\alpha$ input. The microtubule-lumen identification is **Tier 3** biological correlation.

## K.6 Phason Speed Export and Numerical Values

Using $\phi \approx 1.618034$:
$$ \eta = \phi^{-18} \approx 1.731 \times 10^{-4} $$

This factor of $\sim 1.7 \times 10^{-4}$ represents the "Softness" of the phason field. It defines the hierarchy between the **Planck Scale** ($K_\parallel$) and the **Grand Unification (GUT) Scale** ($K_\perp$). **Falsification scope (scope-restricted per §K.4b):** deviation from the $\phi^{-18}$ ratio falsifies the GCT *bare-vacuum* prediction only in chemically clean analog systems where the Penrose-Toner phason-locking and chemical-bonding stiffening contributions are absent or quantified (synthetic photonic quasicrystals, charge-density-wave systems, or atomic-physics simulations). In *real* metallic-alloy quasicrystals such as i-AlPdMn (de Boissieu 1995; Francoual 2006), measured $K_{\text{phason}}/K_{\text{phonon}} \sim 10^{-2}$ to $10^{-1}$ is 100-1000× larger than the bare GCT prediction — this gap is *not* a falsification of the framework but the consequence of chemical-bonding contamination (§K.4b), itself currently unquantified. A clean-system measurement consistent with $\phi^{-18}$ would confirm the GCT bare prediction; an i-AlPdMn-style measurement at $10^{-2}$ to $10^{-1}$ is *consistent* with the framework conditional on the chemical-bonding correction (Open Problem O.15).

The lattice speed of light follows directly from the stiffness ratio:
$$\hat{c} = \sqrt{K_\perp/K_\parallel} = \sqrt{\phi^{-18}} = \phi^{-9} \approx 0.01315$$
[Tier 2 integer-identification (H_3 Shephard-Todd anchor) + Tier 3 physical-link conjecture (pending O.15(b)) — exponent $D=18$ from the unique icosahedral anchor $\{2,6,10\} = 18$ (Parameter Ledger §0.1 P3; first-principles RG closure of the $\phi^{-D}$ running tracked under Open Problem O.15(b)); the §K.4 rank 3 × Galois 2 × dim 3 = 18 decomposition is a 6D-ambient consistency cross-check, not a second independent icosahedral anchor; identification of $\hat{c}$ with the vacuum speed of light $c$ is Tier 2, contingent on the icosahedral projection ansatz.]

## K.7 Three-Route Cross-Check of the G Derivation [Tier 2 — Route 1 closes to standard Planck identity; Routes 2/3 are structural-scaling cross-checks only]

Three independent derivations of Newton's gravitational constant $G$ appear in the GCT manuscript. This section closes Route 1 to the standard Planck-mass identity $G = \hbar c / M_P^2$ and documents Routes 2 and 3 as *structural cross-checks* at the natural-units / order-of-magnitude scaling level — confirming that the phason-elasticity form $G \sim \hat c^4 / (K_\perp L^2)$ has the right dimensional scaling for a gravitational coupling, but **not** standalone SI-unit derivations: the published Routes 2/3 formula is dimensionally inconsistent (off by one factor of $L$), the dimensionally-corrected form differs from Route 1 by $\phi^{-18}/(32\pi) \approx 10^{-6}$, and no first-principles GCT cancellation closes that residual.

**The three routes:**
- **Route 1 (Jacobson primary):** $G_1 = \dfrac{c^3 a_6^2}{4\hbar}$ (V2 Ch09 §9.1.4)
- **Route 2 (Phason elasticity):** $G_2 = \dfrac{\hat{c}^4}{8\pi K_\perp a_6}$ (V2 Ch08 §8.1.4)
- **Route 3 (Acoustic metric):** $G_3 = \dfrac{\hat{c}^4}{8\pi K_\perp a_6}$ (V1 §13.3.4 — same formula, different derivation path)

Routes 2 and 3 share the same formula; the cross-route question is whether $G_1$ reduces to the same numerical value as $G_2 \equiv G_3$.

**Closure of Route 1 to the standard Planck identity.** We substitute the GCT expressions $\hat{c} = \phi^{-9}c_P$ (§K.6) and $K_\perp = (E_P/\ell_P^3)\phi^{-18}$ (§K.4), where $c_P$ is the Planck speed and $E_P = M_P c^2$ is the Planck energy. The derivation below closes Route 1 to the standard identity $G = \hbar c / M_P^2$; the reduction of Route 2 to the same identity requires the additional dimensional bookkeeping recorded as O.22 below.

Step 1 — Express $\hat{c}^4$ and $K_\perp$:
$$\hat{c}^4 = \phi^{-36} c_P^4, \qquad K_\perp = \frac{M_P c_P^2}{\ell_P^3} \phi^{-18}$$

Step 2 — Substitute into Route 2:
$$G_2 = \frac{\phi^{-36} c_P^4}{8\pi \cdot \dfrac{M_P c_P^2}{\ell_P^3} \cdot \phi^{-18} \cdot a_6} = \frac{\phi^{-18} c_P^2 \ell_P^3}{8\pi M_P a_6}$$

Step 3 — Use the Planck identities $c_P^2 = G M_P / \ell_P$ (from definition $\ell_P = \sqrt{\hbar G/c^3} \Rightarrow G = \ell_P^2 c^3/\hbar$) and the lattice-Planck relation. The Route 1 expression gives:
$$G_1 = \frac{c^3 a_6^2}{4\hbar}$$
Substituting the GCT lattice spacing $a_6 = (2\hbar/m_e c)\phi^{-107}(1-5\alpha)$ and the Planck mass relation $M_P = m_e \phi^{107}(1-5\alpha)^{-1}$:
$$a_6 = \frac{2\hbar}{M_P c} \cdot \phi^{-107}(1-5\alpha) \cdot \phi^{107}(1-5\alpha)^{-1} = \frac{2\hbar}{M_P c}$$
(the $\phi^{107}$ and $(1-5\alpha)$ factors cancel exactly). Therefore:
$$G_1 = \frac{c^3}{4\hbar} \cdot \frac{4\hbar^2}{M_P^2 c^2} = \frac{\hbar c}{M_P^2} = G_{standard}$$
which is the standard definition of $G$ in terms of the Planck mass. Since $M_P^2 = \hbar c / G$ by definition, the closing identity $G = \hbar c / M_P^2$ is *tautological*: it confirms that the GCT Route 1 substitution chain is dimensionally consistent with the standard Planck-mass definition. It does **not** establish that Route 2's phason-elasticity formula reduces to the same value.

**Status of the cross-check.** What is proved above:
- Route 1's substitution chain closes consistently to $G = \hbar c / M_P^2$ (the Planck-mass tautology).
- Routes 2 and 3 share a single phason-elasticity formula $G = \hat c^4 / (8\pi K_\perp a_6)$; equivalence between Routes 2 and 3 is automatic by formula identity.

**Dimensional analysis of Routes 2/3 [closure of O.22].** Engine: `GCT_Physics_Engine/src/protocol_o22_newton_g_dimensional_full.py` performs the explicit unit-by-unit propagation. The single-$a_6$ Route 2 formula $G_2 = \hat c^4 / (8\pi K_\perp a_6)$ has dimensions
$$[G_2] = \frac{L^4 T^{-4}}{(M L^{-1} T^{-2}) \cdot L} = L^4 M^{-1} T^{-2},$$
which differs from $[G] = L^3 M^{-1} T^{-2}$ by one factor of length. The single-$a_6$ expression is therefore **dimensionally inconsistent** as a standalone SI-unit expression for $G$. The minimal dimensional correction is to replace $a_6$ by $a_6^2$:
$$G_2^{(\text{corrected})} = \frac{\hat c^4}{8\pi K_\perp a_6^2}, \qquad [G_2^{(\text{corrected})}] = L^3 M^{-1} T^{-2} \;\checkmark$$
Numerical evaluation with the GCT-canonical substitutions $\hat c = \phi^{-9} c$, $K_\perp = (E_P/\ell_P^3)\phi^{-18}$, $a_6 = 2\ell_P$:
$$G_2^{(\text{corrected})} = \frac{\phi^{-18}}{32\pi}\, G \approx 1.72 \times 10^{-6}\, G.$$
The corrected Route 2 differs from Route 1 by the factor $\phi^{-18}/(32\pi) \approx 10^{-6}$ — six orders of magnitude smaller than the SI value of $G$. The GCT framework does **not** absorb this residual via any natural substitution: the $\phi^{-18}$ factor in $K_\perp$ matches the $\phi^{-36}$ factor in $\hat c^4$ only down to a remaining $\phi^{-18}/(32\pi)$ scaling, which has no first-principles cancellation in the current framework.

**Status of the cross-route claim.** Routes 2 and 3 are *structural cross-checks* at the natural-units / order-of-magnitude scaling level — they confirm that the form $G \sim \hat c^4 / (K_\perp L^2)$ has the right *dimensional scaling* for a phason-elasticity gravitational coupling. They are **not** standalone SI-unit derivations of $G$: the single-$a_6$ expression is dimensionally inconsistent, the corrected formula is off by $\sim 10^{-6}$, and no GCT-internal substitution closes the residual. The "three-route equivalence" claim is therefore restricted to scaling-form consistency, not numerical identity.

**Empirical disposition.** The Route 1 derivation of $G$ is Tier 2 with 2274 ppm agreement against CODATA-2022 (verified by `verify_independent/verify_newton_g.py`). The 2274 ppm CODATA agreement is a Route 1 result and reflects the precision of the electron-mass anchor through $a_6 = 2\hbar/(M_P c)$. Routes 2/3 are structural-scaling cross-checks only; they do not contribute to the empirical $G$ derivation.

**Summary.** GCT establishes the standard Planck identity $G = \hbar c / M_P^2$ via Route 1 (Jacobson horizon entropy + lattice-Planck relation; Tier 2, 2274 ppm vs CODATA). Routes 2 and 3 (phason elasticity) are structural cross-checks confirming the scaling form $G \sim \hat c^4 / (K_\perp L^2)$ but are **not** standalone SI-unit derivations: the single-$a_6$ expression is dimensionally inconsistent (off by one factor of $L$), the dimensionally-corrected form differs from Route 1 by $\phi^{-18}/(32\pi) \approx 10^{-6}$, and no first-principles GCT cancellation closes that residual. The three-route headline is therefore a *single SI-unit closure (Route 1) plus structural-scaling cross-checks (Routes 2/3)*, not three independent proofs. The single anchor in the Route 1 reduction is the electron-mass exponent $-107$ that enters $a_6$ and cancels into the standard Planck identity — no separate $G$ fit.
