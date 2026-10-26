### **Chapter 2: The Rotation Sector (SU(2))**

While the $U(1)$ sector is modelled on the internal scalar phase of the vacuum condensate, the group $SU(2)$ enters two mathematically isomorphic but physically distinct roles. First, $SU(2)=\operatorname{Spin}(3)$ is the simply connected double cover of the spatial rotation group $SO(3)$ [Tier 1]. Second, the Standard Model uses an **internal** weak-isospin gauge group $SU(2)_L$, postulated to account for isospin and parity violation. The first fact does not derive the second. GCT proposes that an internal icosahedral frame bundle and a chiral connection realize the weak sector, but that physical identification requires a separately specified internal bundle, chiral representation and gauge dynamics [Tier 2 mechanism / Tier 3 realization]. Neither the Dirac belt trick nor the universal Solenoid forces weak isospin. This chapter keeps the $SU(2)$ group structure and the spatial double cover as mathematical inputs and separates them from the weak-isospin identification.

---

**2.1 The Two Bundles: Spin and Isospin**

**2.1.1 Isomorphism is not Identity**

Standard physics distinguishes **Spin** (transforming under spatial rotations) from **Weak Isospin** (transforming under internal gauge rotations), even though both use the $\mathfrak{su}(2)$ algebra. GCT proposes a common icosahedral origin while retaining two distinct fiber bundles; algebraic isomorphism is not physical identity.

1. **The spatial spin bundle ($E_\parallel$):** If the physical manifold admits the relevant spin structure, its oriented frame bundle lifts from $SO(3)$ to $\operatorname{Spin}(3)\cong SU(2)$. This is the standard home of **Space-Time Spin ($S$)**.
2. **The candidate internal gauge bundle ($E_\perp$):** The 3D internal manifold carries the same $H_3$ point-group symmetry, and GCT assigns the internal icosahedral-frame degrees of freedom to a distinct bundle. Identifying its continuum connection and chiral doublet representation with **Weak Isospin ($T$)** is a GCT physical bridge, not a consequence of the spatial spin lift.

**2.1.2 The Geometric Origin of $SU(2)_L$**

The exact mathematical input is $2I\subset SU(2)$ with 120 elements. GCT models internal-frame states by discrete hopping among those elements of the **Binary Icosahedral Group ($2I$)** and proposes a continuum $SU(2)$ connection in the long-wavelength limit. Deriving the Standard-Model $SU(2)_L$ gauge field still requires the continuum limit, kinetic term, fermion representation and a proof of left-handed coupling. The chiral ($\phi$-dependent) 6D projection motivates that identification but does not by itself establish it [Tier 2 structural candidate; Tier 3 physical gauge realization].

---

**2.2 The Spatial Double-Cover Control**

**2.2.1 Proposition 2.1 [Tier 1 double-cover topology + Tier 3 physical framed-bundle premise]**

**Proposition 2.1:** *If a physical framed-defect configuration realizes the non-trivial loop of $SO(3)$ and its quantum state is assigned the spinorial lift, then rotations act through $SU(2)$ and a $2\pi$ rotation acts by $-1$ in the fundamental representation.* This conditional statement is about spatial spin. Self-reference, an identity address and weak isospin do not follow from it.

**2.2.2 Proof: 360° rotation $\neq$ identity for ribbons**

As the standard control, model the physical object as a **framed ribbon** whose orientation is measured relative to an ambient frame. Applying this control to a GCT defect requires a separately derived physical framed-configuration bundle and connection. The universal Solenoid has $\pi_1(\Sigma_\infty)=0$ and supplies no rotation obstruction; mapping the physical state to a Solenoid address would be a separate bridge.
* A rotation of **$360^\circ$ ($2\pi$)** returns the knot to its original geometric position but introduces a phase factor of $e^{i\pi} = -1$ in the holonomy of the connection. Topologically, the ribbon accumulates a "twist" that cannot be removed by translation.
* A rotation of **$720^\circ$ ($4\pi$)** introduces a double-twist ($e^{i2\pi} = +1$). In 3D, a double-twist is contractible; it can be "looped" over the object to restore the system to its original state.

For the spinorial representation, the state vector returns after $720^\circ$ while rays are unchanged by the $360^\circ$ sign. Whether a particular GCT defect occupies that representation is the physical framed-bundle premise, not a conclusion about personal identity.

**2.2.3 Spinors and the need for $SU(2)$ ($4\pi$ symmetry)**

The universal cover of $SO(3)$ is the **Special Unitary group $SU(2)$**. Mathematically, $SU(2)$ is topologically equivalent to the 3-sphere ($S^3$), which is simply connected. Along the lifted one-parameter rotation path, $2\pi$ reaches the central element $-\mathbf{1}$ and $4\pi$ returns to $+\mathbf{1}$, matching the standard spinorial transport law.

**2.2.4 The Dirac Belt Trick as a Standard Framing Control**

The Dirac belt trick visualizes the non-trivial $\mathbb{Z}_2$ loop of $SO(3)$ for an object framed relative to its environment. It demonstrates the standard rotation topology [Tier 1], not that all matter is attached to the universal Solenoid and not that the weak gauge group is spatial rotation. The GCT claim that a defect realizes this physical framing remains a separate Tier 3 identification.

**2.2.5 Proof of the Double Cover Map (Quaternions) [Tier 1]**

Using the isomorphism between $SU(2)$ and the unit quaternions $\mathbb{H}_1$, a rotation $R \in SO(3)$ by angle $\theta_{rot}$ about axis $\hat{n}$ is mapped to $SU(2)$ elements $\pm q$, where $q = \cos(\theta_{rot}/2) + \hat{n}\sin(\theta_{rot}/2)$. The factor of $\theta_{rot}/2$ ensures that $\theta_{rot} = 2\pi$ yields $q = -1$, and $\theta_{rot} = 4\pi$ yields $q = +1$. This $2:1$ covering map rigorously defines the **spatial spin lift**. A weak-isospin bundle must be supplied independently.

---

**2.3 The Binary Icosahedral Candidate for the Internal Sector**

**2.3.1 $2I \subset SU(2)$ (120 Elements)**

While the hydrodynamic limit utilizes the continuous group $SU(2)$, the underlying hardware is a discrete lattice. The rotational symmetry of the 6D parent lattice projects to the **Binary Icosahedral Group**, denoted $2I$ (or $\tilde{I}$). This is a discrete subgroup of $SU(2)$ containing 120 elements.

**2.3.2 Lift of the Icosahedral Classes**

The 60 rotational symmetries of the icosahedron (group $I$) are "doubled" in $SU(2)$ to account for the spinor phase. The 120 elements of $2I$ correspond to the 120 vertices of the **600-Cell** (a regular 4-polytope) embedded in the $S^3$ manifold of the gauge group.

**2.3.3 Quaternion Representation (The 600-Cell) [Tier 1]**

The elements of the binary-icosahedral control set are:
* **8 units:** $(\pm 1, 0, 0, 0)$ and permutations.
* **16 vertices:** $\frac{1}{2}(\pm 1, \pm 1, \pm 1, \pm 1)$.
* **96 vertices:** even permutations of $\frac{1}{2}(0, \pm 1, \pm \phi, \pm \phi^{-1})$.

**2.3.4 Discrete Hopping of Internal Frames**

GCT hypothesizes that, because the lattice is discrete at the Planck scale, the microscopic internal frame of a particle hops among these 120 orientations and that a coarse-grained connection synchronizes neighboring cells. Identifying that connection with the physical weak force is Tier 3 until its continuum gauge action, matter representation and chiral couplings are derived.

---

**2.4 Chirality from Projection**

**2.4.1 The Primary Chiral Asymmetry (Geometric CP-Violation)**

Standard physics treats CP-violation (one of the Sakharov conditions for the matter–antimatter asymmetry, not the asymmetry itself) as a parameter in the CKM matrix. GCT proposes [Tier 3] that it is a **Structural Property of the Projection**.

**2.4.2 Chirality Witness: Jackiw-Rebbi Domain Wall [proposed mechanism, chirality audit open + Tier 3 numerical-control witness]**

Chirality has a computational check under the current model, but not a verification: the engine chirality audit finds a boundary zero mode that is generic rather than Fibonacci-specific, so the check stays open. The cut-and-project boundary of the quasicrystal acts as a topological domain wall, structurally analogous to the **Jackiw-Rebbi mechanism**. Computations on the 1D Fibonacci Chain equivalent yielded exactly 13 midgap states manifesting a net chirality of $+1$ (a left-handed surplus). This is consistent with, but not specific to, the proposed chiral-domain-wall mechanism (the chirality audit is open) and supplies a Tier 3 numerical-control witness for parity violation; theorem-grade uniqueness over the full gauge/classification setting remains an open App ORQ O.39 target.

**2.4.3 Candidate Chiral Representation [Tier 2 mechanism / Tier 3 physical assignment]**

The weak-sector task is to derive an **internal** representation in which the candidate $SU(2)_L$ connection acts on left-chiral fermion fields while right-chiral Standard-Model fields are $SU(2)_L$ singlets. Spatial handedness, spatial spin and weak isospin are distinct notions. The oriented 6D$\to$3D projection and the domain-wall index of §2.4.2 can motivate a chiral asymmetry, but neither the Selection Operator nor an Agent address selects the Standard-Model representation by itself. A complete derivation requires the internal gauge bundle, its Dirac operator, the chiral matter representation and anomaly cancellation.

As a candidate parent branching, one may write
$$\mathbf{4} \to (\mathbf{2}, \mathbf{1}) \oplus (\mathbf{1}, \mathbf{2})$$
under a declared $SU(2)_L\times SU(2)_R$ parent symmetry. Here both factors are internal representation labels in this weak-sector ansatz:
* **$(\mathbf{2}, \mathbf{1})$:** Candidate left-chiral doublet under the factor proposed for gauging as $SU(2)_L$.
* **$(\mathbf{1}, \mathbf{2})$:** Candidate right-chiral partner under the second factor, which must be reduced or otherwise mapped to the observed $SU(2)_L$-singlet spectrum.

This branching is not a physical-versus-internal rotation split and is not yet a derivation of the Standard-Model fermion content.

**2.4.4 Left-Handed Coupling to the Weak Force**

GCT proposes the physical weak bosons as the connection modes of the candidate internal $SU(2)_L$ bundle. Conditional on the chiral representation bridge above, left-chiral doublets couple to $W^a_\mu$ through the standard covariant derivative. The icosahedral projection supplies a proposed geometric origin for that bridge; it does not replace the required gauge connection, kinetic term or representation derivation [Tier 3 physical realization].

**2.4.5 Right-Handed Singlets and the Neutrino Candidate**

In the Standard Model, right-handed charged fermions are singlets of $SU(2)_L$ but still carry hypercharge, so they are not generically sterile [Tier 1]. A right-handed neutrino, if present, is the special gauge-singlet candidate. Mapping such a component to an $E_\perp$-dominated defect mode may motivate the second-order neutrino suppression in **Chapter 9**, but that mapping and the resulting mass operator remain Tier 3 until the internal representation and couplings are derived.

---

**2.5 Physical Interpretation**

**2.5.1 Three Generators: $W^+, W^-, W^3$ (Before Mixing)**

The $SU(2)_L$ algebra is generated by three operators. $W^\pm$ act as raising/lowering operators within a weak-isospin doublet (for example, the neutrino/electron components), while $W^3$ is the pre-mixing neutral generator that later combines with the Hypercharge field $B$ (Chapter 4) to form the physical $Z$ and $\gamma$. These operations change internal weak-isospin state; they do not rotate or rewrite a Solenoid identity address.

**2.5.2 Weak Isospin $T_3$ as Lattice Orientation**

The quantum number $T_3 = \pm 1/2$ labels the two components of the candidate internal weak doublet relative to the declared local internal frame [Tier 3 assignment]. It is not a personal-identity bit or an identity-address coordinate.

**2.5.3 Parity Violation as a Geometric Candidate**

GCT proposes that the oriented 6D$\to$3D cut-and-project construction, with its irrational $\phi$-slope, supplies a geometric source for chirality. That orientation is a Tier 3/open candidate: the cut-and-project set is centrosymmetric, so an independently defined chirality-breaking operator would be needed (App USS §USS.7, Remark T-McK.1b.A; V2 Ch02 §2.1.3); deriving the observed weak parity violation still requires the internal $SU(2)_L$ bundle, chiral Dirac spectrum and matter couplings identified above [Tier 3 realization]. It is therefore an evidence target and an architecture, not a proof obtained from the spatial double cover or from agency.

![Standard spatial-rotation control: the SU(2) double cover sends a $2\pi$ rotation to the central element $-1$, while a $4\pi$ rotation returns to $+1$. Applying this control to a GCT defect requires its physical framed bundle; the internal weak-isospin bundle is separate.](content/Figures/Volume_3/Figure V3.2.1.svg)
