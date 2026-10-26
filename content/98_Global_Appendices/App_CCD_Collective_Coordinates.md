### **Appendix CCD: The Collective Coordinate Derivation**

**CCD.1 The Ansatz: Soliton Decomposition**

To bridge the non-linear dynamics of the Supersolid Quasicrystal with the linear formalism of Quantum Field Theory, we utilize the **Collective Coordinate Method (CCM)**. We assume the existence of a stable, static topological defect $\Phi_0(x)$ that satisfies the vacuum field equations (e.g., the dodecahedral electron cage).

Given a chosen time parameter and moving-defect solution, the collective-coordinate method represents the profile by a trajectory $X(t)$. Calling this an appearance "to the Selection Operator" is an optional Agent-frame interpretation; no physical Selection Operator is required or derived by the decomposition. We introduce the time-dependent decomposition:
$$\Psi(x, t) = \Phi_0(x - X(t)) + \delta\Psi(x, t)$$
Where:
* $X(t)$ are the **Collective Coordinates** (or Moduli) representing the center-of-mass and internal orientation of the knot.
* $\Phi_0(x - X(t))$ represents the **Rigid Profile** of the defect being translated through the lattice.
* $\delta\Psi(x, t)$ represents the **Fluctuation Field** (phonons and phasons) representing the "wake" or self-interaction of the moving defect.

**CCD.2 The Zero-Mode Projection**

The translation of a defect in a uniform medium is a **Zero-Mode** of the system; because the coarse-grained medium is translation invariant, the energy of the defect is independent of its absolute position $X$ (up to Peierls–Nabarro and phason-locking corrections of the underlying quasilattice). To promote $X(t)$ to a dynamical variable, we must ensure that the fluctuations $\delta\Psi$ do not contain any component that corresponds to a simple translation. 

We impose the **Orthogonality Condition**:
$$\int_{\mathbb{R}^3} \text{Re} \left[ \delta\Psi(x, t) \cdot \frac{\partial \Phi_0^*(x - X(t))}{\partial X} \right] d^3x = 0$$
At linear order this projection assigns the translational zero-mode motion to the collective coordinate $X(t)$, while $\delta\Psi$ carries the remaining "wave-like" radiative corrections and phason drag. This standard collective-coordinate step [Tier 1 method] is the device used by the **Soliton-Field Duality** proposed in V1 Ch14 §14.1; it does not by itself establish that proposal.

**CCD.3 The Effective Action and Stiffness Hierarchy [Tier 1 method; Tier 2/3 GCT realization]**

We substitute the decomposition ansatz into the Field action. The resulting schematic effective particle Lagrangian $\mathcal{L}_{eff}$ is used, within the GCT realization [Tier 2/3], to model mass as **Lattice Impedance**; this is a modelling reading, not a derivation of the origin of mass:
$$\mathcal{L}_{eff}(X, \dot{X}) = \frac{1}{2} M_{bare} \dot{X}^2 - V(X) + \mathcal{L}_{int}(X, \delta\Psi)$$
In the collective-coordinate method the inertia is set by the kinetic coefficient, $M = \int \rho\,(\partial\Phi_0)^2$, i.e. the static energy carried by a field divided by the square of that field's speed; stiffness sets the static energy. The partition below is therefore a heuristic. A defect whose energy sat mainly in the phonon sector would inherit the phonon branch's limiting speed rather than $c$, an open multiple-limiting-speed issue (V2 Ch06 §6.3.2). In the GCT supersolid vacuum, the **Bare Mass** ($M_{bare}$) is heuristically partitioned according to the stiffness hierarchy:
1. **Inertia ($K_\parallel$):** The primary mass component is determined by the "Hard" phonon bonds of the 6D lattice. This provides the resistance to acceleration.
2. **Maneuverability ($K_\perp$):** The coupling to the "Soft" phason field determines the radiative corrections ($\delta m$) and the phason drag coefficients.

Within the declared defect action, the physical mass $m_{phys} = M_{bare} + \delta m$ is modeled by the integrated strain energy of the knot across both subspaces. The collective-coordinate method itself is standard Tier 1 machinery. Obtaining a Schrödinger equation for the center-of-mass coordinate would additionally require a derived moduli-space metric, canonical quantization, a Hamiltonian and a controlled nonrelativistic limit; the schematic Lagrangian above does not prove that result. The identification of inertia with the "weight" of the $6D$ lattice bonds the defect must displace remains a Tier 2/3 GCT interpretation.

**CCD.4 The $SU(2)$ / WZW Rotation Control [Tier 1 mathematics; Tier 3 physical framed-defect premise]**

**What this section evaluates and what it does not.** This section evaluates only the standard rotation control: the double cover $SU(2)\to SO(3)$ and the spinorial sign of a $2\pi$ rotation [Tier 1]. It does **not** evaluate a WZW term on the configuration space of any specific GCT defect, it does not compute a tether contribution, it does not supply an APS boundary operator, domain or index, and it does not derive Fermi–Dirac or Bose–Einstein statistics. Cross-references elsewhere in the manuscript to a WZW "evaluation" in this section should be read in this restricted sense.

**The standard rotation control [Tier 1].** The control is independent of the universal Solenoid. One has
$$\pi_1(SO(3))\cong\mathbb{Z}_2,\qquad SU(2)\longrightarrow SO(3)$$
as the simply connected double cover. A non-trivial $2\pi$ loop in $SO(3)$ lifts to a path from $\mathbf{1}$ to $-\mathbf{1}$ in $SU(2)\cong S^3$, and the spin-$\tfrac12$ representation therefore sends a $2\pi$ rotation to $-1$ and a $4\pi$ rotation to $+1$. The normalized WZW form
$$\Omega_{WZW}=\frac{1}{24\pi^2}\operatorname{tr}\!\left[(g^{-1}dg)^3\right],\qquad [\Omega_{WZW}]\in H^3(SU(2);\mathbb{Z}),\qquad \int_{S^3}\Omega_{WZW}=1,$$
is a compatible standard description of the integer extension class once the boundary data and the extension are specified. The earlier "hemisphere" step, which integrated $\Omega_{WZW}$ over half of $S^3$ to obtain $W=\tfrac12$, is withdrawn: a path from $\mathbf{1}$ to $-\mathbf{1}$ does not sweep a distinguished 3-ball, and the integral of the volume form over a chosen half of $S^3$ is not a topological invariant. The sign $-1$ comes from the double-cover lift itself.

**Physical framed-defect premise [Tier 3].** The non-triviality of the loop in $SO(3)$ does not by itself show that its image is non-trivial in a defect's configuration space. To apply the control to a GCT defect, the physical configuration space must independently provide a framed-defect bundle or connection whose rotation loop maps to the non-trivial class in $SO(3)$ and whose quantum state uses the spinorial lift (for example, a Finkelstein–Rubinstein sign on a configuration space with the appropriate non-trivial fundamental group and a chosen character). That framing is not supplied by the inverse-limit address topology: the universal Solenoid has $\pi_1(\Sigma_\infty)=0$, so it furnishes no rotation homotopy obstruction, and the Identity Tether route therefore does not supply the spinorial sign. Mapping a framed physical state to a Solenoid address is a separate Tier 3 bridge.

**Conditional conclusion.** If the physical framed-defect premise is derived from the defect action, the standard $SU(2)$ control gives the $2\pi\mapsto-1$ transport law. It does **not** by itself show that every GCT knot realizes the spin-$\tfrac12$ representation, that an "untethered" excitation is bosonic, or that the spin–statistics connection follows from a Solenoid tether. Fermi/Bose statistics additionally invoke the usual locality, covariance, positive-energy and field-representation hypotheses (or a separately derived lattice analogue). The former "Theorem CCD.1 (Tether-Induced Half-Integer Spin)" is therefore retired; the surviving result is the Tier 1 rotation control plus a Tier 3 physical framed-defect identification.

> **Note on Tier classification:** The double-cover sign and the normalization of the generator of $H^3(SU(2);\mathbb{Z})$ are Tier 1 results in algebraic topology, independent of any GCT-specific architecture. The identification of physical GCT defects with framed configurations carrying the spinorial lift is a Tier 3 premise, open until a defect action supplies the bundle. O.14 is a separate conditional APS programme: a qualifying boundary operator, domain, and index problem have not yet been specified and evaluated, so the finite weighted-adjacency sign counts do not supply an APS $\eta$-invariant or promote the GCT identification.
