### **Chapter 6: Photon as Second Sound and the Maxwell Construction**

The identification of the vacuum as a supersolid quasicrystal proposes a material origin for the photon-as-second-sound ansatz. In standard Quantum Field Theory, the gauge potential $A_\mu$ is a fundamental vector field postulated as a background degree of freedom. In Geometric Consciousness Theory (GCT), this chapter sketches a **Lorenz-gauge Maxwell construction** on the phason sector. The sketch is a declared open programme, not a derivation (see the note below); full Maxwell+QED closure, including derivation of the gauge redundancy and radiative loop structure from tile dynamics, remains an Open Problem. Within the sketch, the speed of light enters as the phason phase velocity fixed by the elastic ratio $K_\perp/\rho_{eff}$.

**Declared open programme [Tier 3].** Postulate 6.1 proposes that the photon is the phason ("second-sound") mode and that Maxwell's equations follow. As written, this fails. (i) $A_i=(u_\perp)_i$ and $\mathbf B=\nabla\times\mathbf u_\perp$ pair $E_\parallel$ ($T_{1u}$) with $E_\perp$ ($T_{2u}$); $T_1\otimes T_2=G\oplus H$ has no vector part, so no $I_h$-equivariant map exists. (ii) With $\eta=\mathrm{diag}(+,-,-,-)$ the kinetic term gives $A_i$ the ghost sign, and $A_0=\theta$ (dimensionless) and $A_i=u_\perp$ (a length) mix dimensions. (iii) A 3D point defect has no $\pi_1$ winding, so winding cannot source $J_0$. (iv) The gauge redundancy is assumed, while $\theta$ is a physical global-$U(1)$ Goldstone mode. (v) $V_{lock}(\mathcal P_\perp\mathbf u)$ breaks the phason shift symmetry and gaps the mode ($\approx 17\,\mu$eV; $m_\gamma<10^{-18}$ eV). Closure needs a symmetry-breaking intertwiner, a ghost-free normalised action, a divergence-type charge, a derived gauge redundancy and a shift-symmetric locking term. The text below is the current sketch; nothing downstream uses it as support.

---

**6.1 The Identification of Light**

**6.1.1 Postulate 6.1: Photon as Second Sound**

In Chapter 5, within the supplied hydrodynamic ansatz, we obtained two distinct propagating branches in the vacuum condensate:
* **First Sound:** Corresponds to high-velocity phonon compressions in the physical manifold $E_\parallel$. Its velocity is determined by the bulk stiffness $K_\parallel$ and represents the **Bare Lattice Speed** ($v_{\text{bare}} \gg c$ under P3b), the speed of bulk stress. It is not a speed of entanglement correlations: such correlations carry no signal and are not accounted for by the supersolid pairing (Ch03 §3.1.2; §6.2.4).
* **Second Sound:** Corresponds to the low-velocity, out-of-phase oscillation of the lattice structure (phasons) and the superfluid phase.

**Postulate 6.1:** *The physical photon is the quantized excitation of the phason mode (Second Sound) within the vacuum supersolid.*

This identification proposes an ontological status for light [Tier 3, per §6.1.2]: on it, light is not an independent entity added to space but a wave of topological rearrangements propagating through the supersolid. If the phason stiffness $K_\perp$ is suppressed relative to the phonon bonds (the Tier 3 stiffness-map hypothesis P3b, §6.2.2), light travels at a speed that is macroscopic and finite. Reading this speed as the "refresh rate" of a causal simulation or of the emergence of structured experience is a Tier 4 interpretive gloss; it is not derived here.

**6.1.2 Photon as Second Sound from Gauge-Fixed Supersolid Hydrodynamics [Tier 3 open programme; defects (i)–(v) above unresolved]**

The proposed mapping from phason-sector hydrodynamics to Maxwell’s equations is sketched through four ingredients: (i) Euler–Lagrange wave equations from a stated gauge-fixed supersolid Lagrangian, (ii) Lorenz gauge fixing of the resulting four-potential dynamics, (iii) recovery of the homogeneous Maxwell pair as Bianchi identities of $F_{\mu\nu} = \partial_\mu A_\nu - \partial_\nu A_\mu$ and of the inhomogeneous pair from the Euler–Lagrange equations in Lorenz gauge, and (iv) Lorentz invariance of the action with the emergent speed $c^2 = K_\perp / \rho_{eff}$ identified as the phason phase velocity.

**Ingredient I — Euler–Lagrange equations from the supersolid Lagrangian.** The sketch assigns the phason sector the Lagrangian density [Tier 3 open programme]:
$$\mathcal{L}_{phason} = \frac{\rho_{eff}}{2} \, (\partial_t A_\mu)(\partial_t A^\mu) \; - \; \frac{K_\perp}{2} \, (\partial_i A_\mu)(\partial_i A^\mu) \; + \; J_\mu A^\mu, \qquad \eta_{\mu\nu} = \text{diag}(+1, -1, -1, -1),$$
with the proposed four-potential identification $A_0 = \theta$ (superfluid phase, scalar potential) and $A_i = (u_\perp)_i$ (transverse phason displacement, vector potential), and the matter current $J_\mu$ arising from the topological coupling described below. As written, with this metric the spatial components $A_i$ carry negative kinetic energy, and $A_0$ and $A_i$ have different dimensions (defects (ii) above). The display is intended as the Lorenz/Feynman-gauge (gauge-fixed) form of the Maxwell action — positing it in this form builds the $U(1)$ gauge structure into the starting point. §6.1.2 is therefore at most a **Tier 3 open sketch**: it shows what a gauge-fixed Maxwell action would give if the phason sector realised it, but the phason realisation itself is not established (defects (i)–(v)). The first-principles target remains the derivation of the gauge redundancy itself — the antisymmetric $-\tfrac14 F_{\mu\nu}F^{\mu\nu}$ kinetic term, with two propagating polarizations rather than four — from the supersolid tile dynamics, rather than assuming it via the gauge-fixed Lagrangian. The Euler–Lagrange equations give the second-order wave equation:
$$\rho_{eff} \, \partial_t^2 A_\mu - K_\perp \, \nabla^2 A_\mu = J_\mu.$$
[Tier 3 open programme; algebra of the assumed gauge-fixed form only]
The current $J_\mu$ is meant to encode a **topological coupling** between matter and the lattice: a matter defect (Volume 3) creates a localized jump in the phason strain. The sketch took a phase winding $\oint \nabla \theta = 2\pi n$ around the defect core as the source $J_0$ and the defect velocity as the source $J_i$. That step fails for point defects: a loop around a point in 3D is contractible, so the winding vanishes, and a non-zero winding requires a vortex line, which sources vorticity rather than a Coulomb divergence (defect (iii)). $J_0$ is therefore an assumed source, and charge conservation $\partial_\mu J^\mu = 0$ is imposed, not derived [Tier 3 open].

**Ingredient II — Lorenz gauge fixing.** Imposing the Lorenz condition
$$\partial_t A_0 + \frac{K_\perp}{\rho_{eff}} \, \nabla \cdot \mathbf{A} = 0$$
(consistent with current conservation $\partial_\mu J^\mu = 0$ and propagated by the EOM) and dividing the wave equation by $K_\perp$ gives the covariant form:
$$\Box_c A_\mu = \frac{1}{K_\perp} J_\mu, \qquad \Box_c \equiv \frac{1}{c^2} \partial_t^2 - \nabla^2$$
with $c^2 = K_\perp / \rho_{eff}$ identified in Ingredient IV [Tier 3 open programme; algebra of the assumed gauge-fixed form only].

**Ingredient III — Maxwell pair.** From the field identifications $E_i = -\partial_i A_0 - \partial_t A_i$ and $B_i = \epsilon_{ijk} \partial_j A_k$ (formalized in §6.1.3), the homogeneous pair follows as Bianchi identities of the field-strength tensor $F_{\mu\nu}$, independent of the EOM:
$$\nabla \cdot \mathbf{B} = 0, \qquad \nabla \times \mathbf{E} + \partial_t \mathbf{B} = 0 \quad \text{[Tier 1 — algebraic identity]}.$$
Substituting the field definitions into the Lorenz-gauge wave equation and using the Lorenz constraint to eliminate $\nabla(\nabla \cdot \mathbf{A})$ and $\partial_t (\nabla \cdot \mathbf{A})$ yields the inhomogeneous pair:
$$\nabla \cdot \mathbf{E} = \frac{J_0}{K_\perp}, \qquad \nabla \times \mathbf{B} - \frac{1}{c^2} \partial_t \mathbf{E} = \frac{1}{K_\perp} \mathbf{J}.$$
[Tier 3 open programme; algebra of the assumed gauge-fixed form only]
The phason stiffness $K_\perp$ plays the role of the vacuum permittivity $\epsilon_0$ in lattice units; the SI conversion is fixed by the anchoring of App ULA §ULA.6.

**Static Coulomb limit.** The static electromagnetic case is not a separate assumption; it is the $J_i=0$, $\partial_t A_\mu=0$ limit of the same inhomogeneous pair. The temporal EOM reduces to
$$-K_\perp\nabla^2 A_0(\mathbf{x}) = J_0(\mathbf{x}),$$
while the field identification gives $\mathbf{E}=-\nabla A_0$ and $\mathbf{B}=0$. Therefore
$$\nabla\cdot\mathbf{E}=-\nabla^2 A_0=\frac{J_0}{K_\perp}, \qquad A_0(\mathbf{x})=\frac{1}{4\pi K_\perp}\int\frac{J_0(\mathbf{x}')}{|\mathbf{x}-\mathbf{x}'|}\,d^3x'.$$
This is the Coulomb Green function in lattice units. The scalar phase component $A_0=\theta$ is then a longitudinal constraint field fixed instantaneously by the (assumed) conserved charge density; it is not a third propagating photon polarization. Thus, granted the assumed gauge-fixed action, the same Lorenz/Coulomb-gauge reduction that leaves two transverse propagating modes also recovers static electrostatics; the source $J_0$ is assumed (defect (iii)).

**Ingredient IV — Lorentz invariance and the emergent speed $c$.** After imposing the metric/current transformation rules, the gauge-fixed Lagrangian inherits Lorentz covariance from the assumed Maxwell action; the underlying $F_{\mu\nu}F^{\mu\nu}$ kinetic term is not derived here (open: see the declared-open-programme note above). Isotropic propagation would further require the phason anisotropy $K_2$ and the phonon–phason coupling $K_3$ allowed by icosahedral elasticity (Ch04 §4.1.3) to vanish or decouple in this sector; that is an open constraint, not a result. The dimensionless lattice value $\hat{c} = \sqrt{K_\perp / K_\parallel} = \phi^{-9}$ (§6.2.2) [Tier 2 integer-identification conditional on the irreducible $H_3$ premise + Tier 3 physical-link conjecture pending Open Problem O.15(b), per Parameter Ledger §0.1 P3].

The symbolic verification of all four ingredients — including the U(1) gauge invariance of $\mathbf{E}$ and $\mathbf{B}$ under $A_0 \to A_0 - \partial_t \Lambda$, $A_i \to A_i + \partial_i \Lambda$, and a sensitivity sweep of the structural closure across the defensible range of the stiffness exponent $D \in \{14, 16, 18, 20, 22\}$ — is implemented in `GCT_Physics_Engine/src/protocol_ch06_maxwell_emergence.py`. The sympy residuals check algebraic identities of the assumed Maxwell form only; they cannot fail and do not test the phason realisation, and the $D$ sweep is uninformative because $D$ enters only through $c^2$.

**6.1.2b Polarization-count reconciliation [Tier 3 open programme; the reduction is assumed, not derived].**
The Lorenz-gauge Lagrangian of Ingredient I carries four components $A_\mu = (A_0, A_i)$, but the physical photon has only **two transverse polarizations**. The gauge-fixed-vs-physical reconciliation operates as follows:

* **Field-component to phason-mode identification.** Per the §6.1.3 mapping below, the four $A_\mu$ components correspond to two physically distinct phason hydrodynamic modes: $A_0 = \theta$ is the **superfluid phase** of the condensate (a *longitudinal scalar* mode tracking the local condensate orientation), and $A_i = (u_\perp)_i$ are the **transverse phason displacements** (three vector components in the internal $E_\perp$ tangent space). Calling two of them "transverse to the propagation direction" presupposes an $E_\perp\to E_\parallel$ identification; the wavevector lies in $E_\parallel$, and no $I_h$-equivariant identification exists (defect (i)), so the transverse/longitudinal split is part of the open programme.

* **Why the longitudinal sector does not propagate as a physical particle.** Under the Lorenz constraint $\partial_t A_0 + (K_\perp/\rho_{eff}) \nabla \cdot \mathbf{A} = 0$ (Ingredient II), the scalar component $A_0$ and the longitudinal vector component $\nabla \cdot \mathbf{A}$ are **dynamically linked**: their independent oscillations are forbidden by the gauge constraint. Taking the static Coulomb-limit gauge choice makes this explicit: the scalar potential becomes an instantaneous response to the charge density (Poisson equation, not a propagating wave), and the longitudinal vector component is eliminated by $\nabla \cdot \mathbf{A}=0$. In the assumed Maxwell form, the remaining two transverse vector components of $\mathbf{A}$ are the physical polarizations. In the Ch05 supersolid ansatz, however, $\theta$ (the Goldstone mode of a *global* $U(1)$) and the longitudinal phason are physical propagating modes, and the shift $A_i\to A_i+\partial_i\Lambda$ changes the Ch05 free energy, so it is not a symmetry of that ansatz (defect (iv)). Reducing the 1 + 3 supersolid modes to two polarizations would need a mechanism (gapping or decoupling) that is not derived [Tier 3 open].

* **Photon masslessness and Anderson-Higgs scope for §6.3.1.** Photon masslessness is inherited from the ungauge-fixed Maxwell action / residual gauge structure and the absence of a mass term; the gauge-fixed expression alone does not prove gauge invariance. The alternative Anderson-Higgs mechanism applies to broken gauged U(1) and gives massive vectors, not photons. In the assumed Maxwell form, the exact statement is the two-physical-polarization Coulomb-gauge reduction above plus the assumed U(1) gauge redundancy (defect (iv)).

* **IR/UV scale separation against the operative biogenic-DE quartic mass scale $m_{phason} \approx 1.7 \times 10^{-5}$ eV (Parameter Ledger §4) [Tier 3 open; the separation is asserted, not derived].** As written, $V_{lock}(\mathcal P_\perp\mathbf u)$ in App ULA §ULA.2 acts on $\mathbf u_\perp$ itself, breaks the phason shift symmetry and would gap the very mode Postulate 6.1 identifies with the photon; $1.7\times10^{-5}$ eV exceeds the photon-mass bound $m_\gamma<1\times10^{-18}$ eV (PDG) by about $10^{13}$ (defect (v)). Which branch $V_{lock}$ gaps has not been derived. The separation below is the programme's intended reading, not a result. Within the assumed gauge-fixed action, the static Coulomb derivation above fixes the longitudinal Maxwell constraint sector: $A_0$ solves a Poisson equation sourced by the assumed charge and does not inherit a Yukawa mass term from the cold-dark-sector phason gap. On the intended reading, the $m_{phason}$ value belongs to the cosmological frozen-phason scalar branch (App ORQ O.1 / O.4), not to the $U(1)$ Maxwell constraint field after the Lorenz/Coulomb reduction, and for transverse propagating electromagnetic waves the photon-as-phason identification would be the massless long-wavelength gauge mode with two physical polarizations, with any residual dark-sector dressing a separate mixing correction bounded by the App ORQ O.1/O.4 closure programme. On that reading, Coulomb-law tests would constrain the Maxwell constraint sector recovered above, while the 17 $\mu$eV phason gap constrains the dark-sector scalar branch. The two sectors share the supersolid substrate but are not the same observable degree of freedom.

**6.1.3 The Electromagnetic Field Identification [Tier 3 open programme; not $I_h$-equivariant as written, defect (i)]**

We formally map the hydrodynamic variables of the vacuum to the observable electromagnetic fields:
* **Vector Potential ($\mathbf{A}$):** Identified with the transverse phason displacement vector $\mathbf{u}_\perp$.
* **Scalar Potential ($A_0$):** Identified with the superfluid phase $\theta$ of the condensate.
* **Electric Field ($\mathbf{E}$):** The force exerted on a defect to maintain coherence, defined as:
 $$\mathbf{E} \propto -\nabla \theta - \frac{\partial \mathbf{u}_\perp}{\partial t}$$
 [Tier 3 open programme; not $I_h$-equivariant as written, defect (i)]
 This would unify the electrostatic force (phase gradient) with the inductive force (velocity of tile rearrangements).
* **Magnetic Field ($\mathbf{B}$):** Identified with the curl of the phason displacement:
 $$\mathbf{B} \propto \nabla \times \mathbf{u}_\perp$$
 [Tier 3 open programme; not $I_h$-equivariant as written, defect (i)]
 On this mapping, the magnetic field would be the local vorticity or "topological twist" of the phason field.

On this mapping (Tier 3, conditional on the assumed gauge-fixed action), Electromagnetism would be the **Kinematics of Tile Rearrangements** within the vacuum. The phase $\theta$ carries a global $U(1)$; the $U(1)$ gauge redundancy is assumed (§6.1.2), not derived from it.

---

**6.2 The Speed of Light as Phason Phase Velocity**

**6.2.1 The Material Origin of Causal Refresh**

Under Postulate 6.1, the speed of light $c$ is modelled as the propagation velocity of "second sound" in the vacuum supersolid. It is determined by the ratio of the phason restoring force to the internal inertial density of the acceptance window.

**6.2.2 Continuum Homogenization and the Conditional Speed Relation [Tier 2 integer identification (D=18) + Tier 3 heuristic stiffness-ratio map + kinetic assumption]**

The dimensionless lattice speed of light $\hat{c}$ is obtained from the **Continuum Homogenization** of the lattice. We analyze the $6N \times 6N$ dynamical Hessian matrix of the quasicrystal under the postulated stiffness ratio.

The homogenization procedure decouples the matrix into acoustic branches. We distinguish between:
* **The Phonon Branch:** The high-velocity eigenvalues representing bulk strain ($K_\parallel$).
* **The Phason Branch (proposed electrodynamics, open programme §6.1):** The low-velocity eigenvalues representing internal topological rearrangements ($K_\perp$).

Which branch carries gravity is open: some passages place it on the phonon branch, others on phason-density gradients (Ch04_00 §4.B.1; Ch08). A phonon carrier at the bare speed ($\approx 76c$ under P3b) is incompatible with GW170817, which bounds $-3\times10^{-15}<\Delta c/c<7\times10^{-16}$ for gravitational waves, unless a mechanism is derived that brings its speed to $c$.

Under the postulated phason-stiffness scaling $K_\perp/K_\parallel = \phi^{-18}$ (Tier 2 integer-identification conditional on the irreducible $H_3$ premise + Tier 3 physical-link conjecture pending Open Problem O.15(b), per Parameter Ledger §0.1 P3 and App DPS §DPS.4), the eigenvalue problem for the homogenized phason branch in the long-wavelength limit ($k \to 0$) gives a dimensionless ratio $\hat c^2 = K_\perp/K_\parallel = \phi^{-18}$. Therefore, the lattice speed of light emerges as:
$$ \hat{c} = \sqrt{\phi^{-18}} = \phi^{-9} \approx 0.01316 \quad \text{[Tier 2 integer identification (D=18) + Tier 3 heuristic stiffness-ratio map]} $$

The dimensionless ratio $\hat c^2$ here is the postulated stiffness ratio $K_\perp/K_\parallel$ (cf. App ULA §ULA.6 for the calibration to SI $c$); the dimensional speed $c$ requires the SI mapping fixed via the lattice spacing $a_6$.

**Status of the stiffness map.** Only the integer $D = 18$ is Tier 2. The physical map $K_\perp/K_\parallel = \phi^{-18}$ is the registered Tier 3 stiffness-map hypothesis P3b (Parameter Ledger §0.1; Open Problem O.15(b)), listed outside the parameter count in the same way as the electroweak hypothesis H-EW. The long-wavelength homogenized branch gives the conditional identity $\hat c^2 = K_\perp/K_\parallel$; the numerical value $\phi^{-9}$ is a descendant of P3b, not a consequence of $D_{H_3} = 18$ alone. The relation also assumes that the phonon and phason sectors share one inertial normalization. Icosahedral symmetry leaves the quadratic form $Q=aP_\parallel+bP_\perp$ with $b/a$ free, and positive rescalings of the elastic and inertial sector coefficients preserve the point group and inflation map while spanning every positive speed ratio (universality-boundary statement, §4.2.2). The speed export is therefore a conditional relation, not a projection theorem (cf. the conditional speed relation of V1 Ch13 §13.3.4).

**6.2.3 Physical Implications: The 1/76 Scale**

Conditional on P3b, $\hat c = \phi^{-9} \approx 1/76.01$ makes the phason branch roughly two orders of magnitude slower than the bare lattice bonds.

* **Dependency Chain:** This numerical value inherits the entire **Tier 3 P3b / O.15(b) physical-map hypothesis** (Parameter Ledger §0.1). The Hessian propagates a supplied ratio; it does not derive that ratio from $D_{H_3} = 18$.
* **SI Mapping:** The Parameter Ledger convention (row $c$) is $c = \phi^{-9}c_P$, with $c$ the observed speed of light ($2.99 \times 10^8$ m/s) and $c_P$ the bare lattice speed; App ULA §ULA.6 relates this to the lattice spacing $a_6$ [Tier 3, conditional on P3b; the lattice update time $t_6$ is then not the Planck time, see App ULA §ULA.6].

> [!NOTE]
> **Theorem Box — Phason Speed Export (Cross-Volume Reference) [label kept for reference stability; content is a Tier 3 conditional relation under P3b, not a theorem]**
> The conditional lattice speed $\hat c = \sqrt{K_\perp/K_\parallel} = \phi^{-9}$ — the phason (second-sound) group velocity in units of the bare lattice speed — appears in multiple GCT contexts. It is one shared Tier 3 P3b / O.15(b) input, conditional also on a shared inertial normalization (§6.2.2), not a separately derived fact in each context:
> - **Volume 1 §13.3.4 (former gravity route):** Used as $\hat{c} = \phi^{-9}$ in the former elasticity expression $G = \hat{c}^4 / (8\pi K_\perp a_6)$. That expression is dimensionally inconsistent by one length and is retired as a derivation or check of $G$ (V2 Ch08 §8.1.4).
> - **Volume 3 §13.1.2 (historical biophysical scenario):** The same supplied ratio was inserted into a biophysical coupling formula that is no longer adopted. The field-typing analysis (V1 Ch17 §17.1.3) found no action-normalized material–phason coupling or rate, so this use is retained only as provenance and not as a Zeno-Drive derivation.
> The shared symbol does **not** close either physical application. It is the same Tier 3 conditional ratio referenced by both contexts; see App DPS §DPS.6.



**6.2.4 Asymptotic Causality: The Speed of Causal Organization**

In the relativistic effective theory, the light cone is the causal boundary for signals carried by the Maxwell sector. Calling $c$ the **Maximum Speed of Organization** is an interpretive gloss. The manuscript has not shown that all tiling rearrangements are limited by this mode, that faster phonon-like modes are informationally inert, or that the light cone is a Selection Operator's causal boundary. Any Selection-Operator link is Tier 3/open and does not enter the electrodynamics derivation.

---

**6.3 Background Speed vs. Particle Drag**

**6.3.1 Photon Masslessness [Tier 1 gauge limit; GCT phason realisation Tier 3 open]**

The bare photon is exactly massless in the gauge-invariant Maxwell limit ($m_\gamma = 0$) [Tier 1 gauge-invariance statement]. The GCT chain that identifies this Maxwell field with the phason-sector second-sound mode is the declared open programme of §6.1: the gauge redundancy is assumed, and as written the locking potential would gap the identified mode (defects (iv)–(v)); the stiffness and residual-gap story also depends on the exponent-selection layer tracked in Parameter Ledger §0.1 and App ORQ O.1/O.4/O.15. The result is therefore read as: gauge masslessness is Tier 1, while the GCT phason realisation of that massless photon is Tier 3 and open.

**6.3.2 Massive Particle Propagation and the Relativistic Limit**

Within the declared supersolid ansatz, a fermion is modeled as a **topological defect** *within* the lattice (unlike the photon, which is modeled as a wave *of* the lattice structure), and a moving defect may be assigned a material drag term. Identifying that term with **phason drag** in the physical vacuum is a Tier 3 constitutive hypothesis. Identifying it further with qualia or an Agent's subjective registration (V1 Ch16) requires an unclosed Selection carrier, owner and phenomenal bridge, and is not part of the electrodynamics derivation.

As a defect approaches $c$, the phason field cannot rearrange fast enough to accommodate the displacement, leading to a divergent energy requirement. By integrating the work done against this phason drag, we recover the standard **Relativistic Energy-Momentum Relation** [Tier 3 conjectural consistency sketch]:
$$E^2 = p^2c^2 + m^2c^4$$
This is a consistency sketch, not a closed derivation. A full Lorentz-invariant point-particle action and stress-energy derivation from the supersolid hydrodynamic action remain open (closure target: O.34b in App ORQ). Spacetime curvature is modeled as the elastic strain of the vacuum. Standard time dilation follows from the physical metric; calling it a slowing of an Agent's selection index ($dn$) due to informational resistance is a Tier 3/4 metaphor, not a derived clock or phenomenal law.
