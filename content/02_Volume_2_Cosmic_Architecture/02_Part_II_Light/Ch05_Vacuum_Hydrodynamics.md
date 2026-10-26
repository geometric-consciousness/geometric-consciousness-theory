### **Chapter 5: Vacuum Hydrodynamics**

The static geometry and elastic degrees of freedom of the vacuum supply the crystallographic scaffold. Because the vacuum is a **Supersolid**, it does not merely possess a static shape; it possesses a macroscopic state of motion. To understand how light, gravity, and information propagate through the substrate, we must transition from crystallography to hydrodynamics. This chapter states the model equations of motion for the vacuum condensate, treating the supersolid quasicrystal as a complex, multi-component fluid.

---

**5.1 The Hydrodynamic Variables**

To describe the low-energy behavior of the vacuum, we define the variables that characterize the state of the condensate at every point in the physical manifold $E_\parallel$. These variables correspond to the Goldstone modes of the broken symmetries derived in Chapter 3.

**5.1.1 Superfluid Velocity ($\mathbf{v}_s$)**

The primary degree of freedom arising from the spontaneous breaking of the $U(1)$ global phase symmetry is the **Superfluid Velocity**. 

**Definition 5.1:**
$$\mathbf{v}_s = \frac{\hbar}{m}\nabla\theta$$
where $\theta$ is the superfluid phase and $m$ is the effective mass of the lattice constituents. 

Unlike a classical fluid, the superfluid velocity in the vacuum is **Irrotational** ($\nabla \times \mathbf{v}_s = 0$) in all simply connected regions. Vorticity can only exist at the core of topological singularities (vortex lines). In the proposed GCT mapping of electrodynamics, $\mathbf{v}_s$ represents the longitudinal flow of the probability current. Under Postulate 6.1, Chapter 6 maps the phase $\theta$ itself (not its spatial gradient, which is a vector) to the scalar potential $A_0$ (Ch06 §6.1.2) [Tier 3; part of the declared open programme of Ch06 §6.1].

**5.1.2 Phason Displacement and Strain ($w_{ij}$)**

The second fundamental variable arises from the breaking of translational symmetry in the 6-dimensional parent space. This is described by the phason displacement vector $\mathbf{u}_\perp$ in the internal space $E_\perp$.

**Definition 5.2:**
The **Phason Strain** $w_{ij}$ is the spatial gradient of the internal displacement:
$$w_{ij} = \partial_i u_{\perp j}$$
where $i$ is a coordinate index in physical space ($E_\parallel$) and $j$ is an index in internal space ($E_\perp$). 

The phason strain represents the local geometric "tilt" of the acceptance window. Unlike the irrotational $\mathbf{v}_s$, the phason displacement field supports **Transverse Modes** ($\nabla \times \mathbf{u}_\perp \neq 0$). Chapter 6 proposes identifying these rearrangements with the **Vector Potential** ($\mathbf{A}$) [Tier 3, declared open programme]: as written, $\nabla\times\mathbf u_\perp$ contracts an $E_\parallel$ derivative with an $E_\perp$ index, and no $I_h$-equivariant map relates the two (Ch06 §6.1). Matter defects act as sources of phason strain, and the phason field, in turn, exerts a force on matter; this is a candidate, not derived, material origin of the gauge interactions.

---

**5.2 The Phason-Superfluid Coupling**

**5.2.1 The Free Energy Functional**

To describe the energy of the moving supersolid, we utilize the hydrodynamic formalism for icosahedral quasicrystals. To satisfy **Translational Invariance**, the energy density must depend only on the gradients of the displacement fields (strains), not the absolute positions. The total free energy $F$ is defined as:

$$F = \int d^3x \left[\frac{1}{2}\rho_s \mathbf{v}_s^2 + \frac{1}{2}K_\parallel \varepsilon_{ij}^2 + \frac{1}{2}K_\perp w_{ij}^2 + C_{ijkl}^{mix} \varepsilon_{ij} w_{kl} \right]$$

where $\rho_s$ is the superfluid density, $\varepsilon_{ij}$ is the phonon strain, and $w_{kl}$ is the phason strain. 

**5.2.2 The Coupling Tensor ($C_{ijkl}^{mix}$)**

The interaction between the physical and internal manifolds is governed by the **Phason-Phonon Coupling Tensor**. This is a **Fourth-Rank Tensor** that respects the icosahedral point-group symmetry. 

Within the supplied hydrodynamic ansatz, a nonzero $C_{ijkl}^{mix}$ permits a phonon–phason "Dragging" effect: a flow of the superfluid through the lattice may induce phason strain, and phason motion (a topological rearrangement of the tiles) may source a phase gradient, so that the "solid" and "fluid" aspects of the vacuum form a coupled dynamical system. Symmetry allowance does not fix the coefficient or establish a biological source. Identifying this cross-coupling with a Selection Operator (Volume 1) exerting topological torque on the physical world requires an independently derived Agent/source/transducer map and remains Tier 3/open.

**5.2.3 Transformation of Modes: The Second Sound Theorem [Tier 3 open programme; see the note below]**

A normal solid has only acoustic phonon branches (and, in special conditions, phonon second sound). In the supplied supersolid-quasicrystal ansatz, the lattice and the phase are proposed to support two distinct branches.

**Theorem 5.1 (The Second Sound Theorem) [label kept for reference stability; a Tier 3 posit of the supplied hydrodynamic ansatz, with the stiffness hierarchy conditional on P3b — not a theorem]:**
*The ansatz posits two propagating wave solutions of the phason-superfluid system, categorized by the stiffness hierarchy:*

1. **First Sound (Phonons):** A high-velocity mode dominated by the Planck-scale stiffness $K_\parallel$. This wave corresponds to bulk lattice compression. 
2. **Second Sound (Phasons):** A low-velocity mode dominated by the suppressed stiffness $K_\perp$. This wave involves the synchronized, out-of-phase oscillation of the internal lattice structure and the superfluid phase. 

**Declared open programme [Tier 3].** Postulate 6.1 (Ch06) identifies the second-sound branch with the photon and $c$ with its speed. No equations are diagonalised here: the displayed $F$ has no $\theta$–$\mathbf u_\perp$ bilinear coupling ($\nabla\theta$ is $T_1$, the phason strain is $G\oplus H$) and no compressibility term, and the phason inertia $\rho_{eff}$ is posited (§5.3), so the two branches and the identification are assumptions of the ansatz. "Second sound" names the phason branch here, not the two-fluid entropy wave. A closing derivation needs the coupled equations of motion and the repairs listed in Ch06 §6.1; the faster first-sound branch also needs a shown mechanism that keeps it informationally inert (Ch06 §6.2.4). Nothing downstream uses this identification as support.

---

**5.3 The Hydrodynamic Equations**

The evolution of the vacuum state is modelled by three equations (two conservation laws and a phason wave equation). Crucially, GCT posits that the phason field in the vacuum possesses **Effective Inertia** due to its entrainment with the superfluid density.

**5.3.1 Continuity Equation [Tier 1, given the model]**
$$\frac{\partial\rho}{\partial t} + \nabla \cdot (\rho \mathbf{v}_s) = 0$$
This ensures the conservation of the total probability measure of the condensate. Reading it as a conservation of "Presence" (Axiom 1) is a Tier 4 interpretive bridge, not part of the equation.

**5.3.2 Euler Equation (Vacuum Momentum) [Tier 2]**
$$\rho \left[ \frac{\partial\mathbf{v}_s}{\partial t} + (\mathbf{v}_s \cdot \nabla)\mathbf{v}_s \right] = -\nabla P + \mathbf{f}_{ext}$$
The force term $\mathbf{f}_{ext}$ includes the stress exerted by the phason strain field. In the hydrodynamic limit, this equation governs the refraction of waves by vacuum gradients, giving rise to the **Acoustic Metric** of Chapter 8 (whose role as gravity is Tier 3; carrier open, Ch04 §4.1.1).

**5.3.3 Phason Wave Equation [Tier 3 open programme; photon identification Ch06 §6.1]**
$$\rho_{eff} \frac{\partial^2 \mathbf{u}_\perp}{\partial t^2} = K_\perp \nabla^2 \mathbf{u}_\perp + \mathbf{S}_{coupling}$$
Unlike metallic quasicrystals where phasons are diffusive, the vacuum phasons are taken to be **Propagating Modes** [Tier 3 — conditional on the Tier 3 supersolid premise and on the posited inertia $\rho_{eff}$; in metallic quasicrystals this mode is diffusive]. The second-order time derivative represents the posited effective inertia of the topological structure. The source term $\mathbf{S}_{coupling}$ accounts for the interaction with the phonon manifold. Componentwise this is a wave equation of the same form as the Lorenz-gauge Maxwell wave equation; identifying it with electrodynamics is the declared open programme of Chapter 6 (§6.1), not a result.
