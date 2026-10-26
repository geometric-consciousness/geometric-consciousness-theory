### **Chapter 4: Electroweak Unification**

In the standard Glashow-Weinberg-Salam (GWS) model, the unification of the electromagnetic and weak interactions uses the symmetry group $SU(2)_L \times U(1)_Y$ and an empirically fixed weak mixing angle, $\theta_W$. GCT proposes that the electroweak sectors inherit structure from the $E_\parallel \oplus E_\perp$ decomposition of the 6-dimensional parent lattice. The canonical projector fixes the sector geometry but does not, by itself, fix the relative gauge-kinetic normalization of the two sectors. This chapter therefore separates exact projection identities from the conditional bare-angle hypothesis and from the renormalization-group (RGE) audits, none of which currently closes on the observed Z-pole value.

---

**4.1 The Canonical Projector Result**

**4.1.1 Projected Basis-Vector Norms [Tier 1]**

As established in Volume 2, the basis $\{\mathbf{E}_1, \dots, \mathbf{E}_6\}$ of $\mathbb{Z}^6$ is resolved into two orthogonal three-dimensional subspaces, the parallel space ($E_\parallel$, physical) and the perpendicular space ($E_\perp$, internal). With the canonical row-isometric maps $\widehat M_\parallel, \widehat M_\perp$, define
$$\Pi_\parallel = \widehat M_\parallel^{T} \widehat M_\parallel, \qquad \Pi_\perp = \widehat M_\perp^{T} \widehat M_\perp .$$
They satisfy $\Pi_\parallel + \Pi_\perp = I_6$. Icosahedral symmetry acts transitively on the six basis axes, so the six diagonal entries of each projector are equal, and the rank-three trace gives
$$\|\Pi_\parallel \mathbf{E}_i\|^2 = \|\Pi_\perp \mathbf{E}_i\|^2 = \tfrac{1}{2} \qquad (i = 1, \dots, 6).$$

**4.1.2 Raw Galois-Frame Identity [Tier 1 arithmetic; coordinate-dependent]**

Before row normalization, the Galois-conjugate matrices obey
$$A_0 A_0^{T} = 2(2+\phi) I_3, \qquad B_0 B_0^{T} = 2(3-\phi) I_3,$$
so their raw squared-scale ratio is
$$\rho_{\rm raw} = \frac{2(3-\phi)}{2(2+\phi)} = \frac{3-\phi}{2+\phi} = \phi^{-2},$$
using $\phi^2 = \phi + 1$, and the raw linear-scale ratio is $\phi^{-1}$. This exact identity belongs to the declared raw frame. Under $B_0 \mapsto s B_0$ the row space and the proper projector $B_0^{T}(B_0 B_0^{T})^{-1} B_0$ are unchanged while $\rho_{\rm raw} \mapsto s^2 \rho_{\rm raw}$, so $\rho_{\rm raw}$ is not a substrate-invariant physical length ratio. The relative electroweak coupling must come from a canonically normalized action or trace, not from the coordinate lengths of two raw row frames. This does not predict equal electroweak couplings either.

---

**4.2 The Definition of Hypercharge**

**4.2.1 Hypercharge as Internal $U(1)$ Generator**

GCT assigns the two sectors of the electroweak force to internal degrees of freedom [Tier 3 placement; V3 Ch02 §2.1.1, V3 Ch06 §6.1.2]:
* **Weak Isospin ($T_3$):** Corresponds to rotations of the candidate internal icosahedral-frame ($2I \subset SU(2)$) bundle, placed on the internal ($E_\perp$) side. It is not the gauge field of the spatial frame: the spatial double cover $\operatorname{Spin}(3)$ of rotations in $E_\parallel$ is a separate Tier 1 control (V3 Ch02 §2.2).
* **Weak Hypercharge ($Y$):** Corresponds to phase rotations within the **Internal Space** ($E_\perp$). 

**4.2.2 The Charge Formula and the 1/2 Factor [Tier 1 normalization convention + Tier 3 GCT interpretation]**

The electric charge $Q$ is the generator of the symmetry that remains unbroken after crystallization. The Gell-Mann-Nishijima formula ($Q = T_3 + Y/2$) is standard; GCT offers a Tier 3 reading of it as a normalization aligning the weak-frame and internal-phase sectors (below). 

The factor of **1/2** is a normalization convention of the Standard Model charge formula: the alternative $Q = T_3 + Y$, with $Y$ halved, is equally common (V3 Ch01 §1.3.3). GCT offers a Tier 3 interpretation of it, the **Topological Covering Difference** of the two manifolds. $T_3$ acts in the doublet representation of the binary (double-cover) frame group $2I \subset SU(2)$ of the internal weak bundle (where a full $2\pi$ frame rotation acts by $-1$ and the identity returns at $4\pi$), with eigenvalues $\pm 1/2$; these values come from the doublet representation, and this is not the spatial spin double cover. $Y$ acts on the **Scalar Single-Cover** of the internal phase (where a full rotation is $2\pi$). In this book's convention $Y$ takes the values $+1/3$, $-1$, $+4/3$, $-2/3$ and $-2$ (§4.2.3, V3 Ch01 §1.3.3), which are not integers, so the covering difference does not fix the factor 1/2. The reading that the $U(1)$ hypercharge is "halved" relative to the $SU(2)$ isospin so that a unit lattice step acts consistently on both sectors is a Tier 3 interpretation of a convention, not a derivation.

---

**4.2.3 Derivation of Right-Handed Hypercharges [Tier 1 algebraic identity + Tier 2 mechanism / Tier 3 physical singlet assignment]**

> **Theorem 4.2 — Right-Handed Hypercharges [Tier 1 algebraic identity + Tier 2 mechanism / Tier 3 physical singlet assignment]**
>
> *Statement:* For any right-handed fermion state in GCT — defined as a
> singlet of the candidate internal weak bundle ($T_3 = 0$; the singlet
> assignment is the Tier 3 chiral-representation assignment of V3 Ch02 §2.4.3) —
> the Weak Hypercharge is exactly:
> $$Y_R = 2Q$$
> where $Q$ is the conserved electric charge, taken as given; its values and the defect-topology-to-charge mapping via AKN lattice winding are Tier 3 (Proposal 1.2, V3 Ch01 §1.3.2).
>
> *Derivation:* Set $T_3 = 0$ in $Q = T_3 + Y/2$. Solve for $Y$.
>
> *Results:*
> | State | $Q$ | $Y_R = 2Q$ |
> |:---:|:---:|:---:|
> | $u_R$ | $+2/3$ | $+4/3$ |
> | $d_R$ | $-1/3$ | $-2/3$ |
> | $e_R$ | $-1$ | $-2$ |
>
> *Tier: Tier 1 algebraic identity (anomaly cancellation given the standard SM hypercharge assignment is a textbook result, Bilal 2008 §7.3) + Tier 2 GCT-specific L/R-asymmetric assignment mechanism, whose physical realization (right-handed states as singlets of the internal weak bundle) is the Tier 3 assignment of V3 Ch02 §2.4.3. The hypercharge assignment adds no continuous parameter to the 5-postulate-plus-6-anchor accounting of Parameter Ledger §0.1; the bare electroweak angle is the separate Tier 3 hypothesis H-EW, registered outside that count (Parameter Ledger §0.1; §4.3.2). Computational verification: see Appendix GPE; executable verifier: `GCT_Physics_Engine/verify_independent/verify_hypercharges.py`.*

---

**4.3 The Weinberg Angle: Open Boundary Problem**

> [!NOTE]
> **Status of the electroweak boundary**
>
> Three statements are kept separate:
>
> 1. **Canonical projector geometry [Tier 1]:** $\|\Pi_\parallel \mathbf{E}_i\|^2 = \|\Pi_\perp \mathbf{E}_i\|^2 = 1/2$, an exact statement about two complementary rank-three subspaces.
> 2. **Raw Galois-frame arithmetic [Tier 1, coordinate-dependent]:** the declared unnormalized row frames give a squared-scale ratio $\rho_{\rm raw} = \phi^{-2}$ and a raw three-volume ratio $\phi^{-3}$.
> 3. **Bare electroweak boundary [Tier 3 hypothesis, H-EW]:** $\sin^2\theta_W^{\rm bare} = \phi^{-3}$, retained only as a proposed relation between canonically normalized gauge-kinetic coefficients.
>
> Neither item 1 nor item 2 derives item 3. In particular, the canonical $1/2 + 1/2$ projector split is not a prediction that the physical Weinberg angle equals $1/2$.

**4.3.1 The raw volume ratio is not an invariant [Tier 1]**

For the declared raw Galois frames the relative linear scale is $\phi^{-1}$, hence the raw three-volume ratio is
$$\frac{V_{\perp,0}}{V_{\parallel,0}} = \phi^{-3}.$$
The coordinate change $B_0 \mapsto s B_0$ leaves the internal row space and its proper projector unchanged while multiplying the raw volume ratio by $s^3$; if the acceptance window is rescaled with the coordinates, the cut-and-project model set is unchanged as well. The integer-exponent identity of App USS §USS.9 is therefore an exact statement about the declared raw frames, not a physical length or volume ratio, and it does not by itself fix a coupling. The surviving exact result is the row-isometric projector decomposition of §4.1; a physical mixing angle depends on how the two gauge sectors are normalized in the action.

**4.3.2 The physical gauge-kinetic question [Tier 3 open hypothesis]**

With canonically normalized field strengths, write the ultraviolet kinetic terms schematically as
$$\mathcal{L}_{\rm kin} = -\frac{1}{4g^2}\,{\rm Tr}(W_{\mu\nu}W^{\mu\nu}) - \frac{1}{4g'^2} B_{\mu\nu}B^{\mu\nu}, \qquad \sin^2\theta_W = \frac{g'^2}{g^2 + g'^2}.$$
GCT does not yet derive the relative coefficients $g^{-2}$ and $g'^{-2}$ from a normalization-invariant microscopic trace. The candidate boundary condition
$$\boxed{\sin^2\theta_W^{\rm bare} = \phi^{-3} \approx 0.236068}$$
is therefore a **Tier 3 gauge-kinetic hypothesis**, labelled **H-EW**, not a consequence of the cut-and-project matrices alone. H-EW is an open hypothesis registered outside the five counted postulates P1–P5 and the anchors A1–A6 (Parameter Ledger §0.1). Closing this branch requires deriving the two coefficients from the 6D action, including generator normalization and the measure on the acceptance-window and internal degrees of freedom. Its 2.1% direct proximity to the Z-pole value $0.23122 \pm 0.00006$ (PDG 2026 $\overline{\rm MS}$ $\hat s^2_Z(M_Z)$; the effective leptonic angle 0.23154 is a different quantity) compares quantities at different scales and is a numerical alignment, not RGE support. As evidence that φ or icosahedral structure is special, this alignment is **Tier 4**: the preregistered constant control test (v3, NEGATIVE-FRAGILE; App PSC §PSC.9.6) found φ's pattern of matches on 21 constants not distinguishable from that of random constants (58 of 300 random bases did at least as well), and it scored the $\sin^2\theta_W$ row as one of φ's three misses. The test "excludes, at power ≥ 0.8, an effect in which φ hits at least 6 of the 8 informative rows through a real effect; weaker effects are not excluded." The number is kept as descriptive arithmetic.

---

**4.3.3 Conditional scale and RGE audits [Tier 1 SM equations + Tier 3 GCT inputs]**

A further assumption enters before the candidate boundary can be compared with the Z-pole. The scale assignment
$$M_{\rm GUT} = M_{\rm red}\,\phi^{-9} = \left(\frac{M_{\rm Planck}}{\sqrt{8\pi}}\right)\phi^{-9} \approx 3.2 \times 10^{16}\ \text{GeV}$$
inherits the Tier 3 stiffness/action-RG hypothesis of Open Problem O.15; it is not fixed by the normalized projector. Three numerically distinct calculations are reported:

1. **Physical-hypercharge one-loop comparator [Tier 1 SM equations + Tier 3 GCT boundary and scale].** With $\alpha_Y = g'^2/(4\pi)$, $\alpha_2 = g^2/(4\pi)$, $\sin^2\theta_W = \alpha_Y/(\alpha_Y + \alpha_2)$ and the full-Standard-Model one-loop coefficients $b_Y = 41/6$, $b_2 = -19/6$, running from the H-EW boundary at $M_{\rm red}\phi^{-9}$ returns
   $$\sin^2\theta_W(M_Z) \approx 0.136725,$$
   about **40.87% below** $0.23122$. This route imports the measured $\alpha_{\rm em}(M_Z)$ and $\alpha_2(M_Z)$ normalization, so it is a one-coupling-conditioned consistency test, not an autonomous prediction. The same flow run upward from the measured endpoint implies $\sin^2\theta_W \approx 0.4286$ at $M_{\rm red}\phi^{-9}$ (two-loop value, App GRF §GRF.4.3), and it reaches $\phi^{-3}$ at 243 GeV (two loops, App GRF §GRF.4.3), only about $2.7\,M_Z$; selecting that scale after observing the crossing would be endpoint fitting. Using the raw-frame value $\phi^{-2}$ as if it were the physical boundary gives $0.20953$ (9.38% low); that counterfactual is a coordinate diagnostic, not a physical boundary.

2. **Native irrep-activation kernel [Tier 3 calibrated ansatz].** With the imported A2 ultraviolet benchmark $\alpha_2^{-1}(M_{\rm GUT}) = 24.0$ (the **MSSM** unified coupling: Langacker & Polonsky, Phys. Rev. D 47, 4028 (1993), give $\alpha_G^{-1} \approx 23$–$24.5$ at $M_G \approx 2.5\times10^{16}$ GeV for the MSSM, while in the Standard Model the couplings do not unify; Standard-Model running with the inputs of route 1 gives $\alpha_2^{-1} = 46.2$ at $M_{\rm red}\phi^{-9}$ at two loops, $\approx 46.5$ at one loop, so A2 is incompatible with the Standard-Model running of route 1), three sector factors $Z_i$ chosen so that the saturated coefficients equal the Standard-Model one-loop coefficients, and the declared $I_h$ activation schedule, the engine returns
   $$\sin^2\theta_W(M_Z) \approx 0.16957,$$
   about **26.66% below** observation. A2 is not an endpoint fit, but neither the $Z_i$ factors nor the activation schedule is derived from the 6D action.

3. **Target-normalized geometric integrator [implementation check only].** A normalized kernel whose amplitude is solved from the observed endpoint reaches that endpoint to machine precision by construction. It tests the integrator, not H-EW or an RGE law.

There is therefore **no current numerical RGE support for H-EW**.

The pre-registered gauge-running audit (App GRF §GRF.4.3), run at one and two loops with thresholds, confirms that the miss is not a loop-order, threshold, normalisation or comparator effect: H-EW at $M_{\rm GUT}$ is incompatible with Standard-Model running, and with A2 it is incompatible with any SM extension. From the declared inputs the best Standard-Model case is $\sin^2\theta_W(M_Z) = 0.0673$ (2-loop, A2 = 25), −52σ, and run upward at two loops the measured value reaches $\phi^{-3}$ only at 243 GeV; placing H-EW at 243 GeV would be endpoint fitting. The check is recorded as **FAILED**: no declared-input configuration reproduces $\sin^2\theta_W(M_Z)$, $\alpha_s(M_Z)$ or $\alpha_{em}(M_Z)$ (one borderline two-loop $\alpha_{\rm em}$ value, which imports the measured $\alpha_s$, is excluded by a post hoc judgement; App GRF §GRF.4.3). Whether to retire A2 and A4–A6 is an open v1.4.0 decision; v1.3.0 retires nothing.

![The electroweak boundary problem: the Tier 3 H-EW boundary is separated from the measured Z-pole value, and the two current flow routes miss the endpoint.](content/Figures/Volume_3/Figure V3.4.1.svg)

> [!IMPORTANT]
> **Firewall Metadata [Weinberg angle]**
>
> - **Canonical projector:** $1/2 + 1/2$ sector shares; Tier 1 geometry; not an electroweak-angle prediction.
> - **Raw frame values:** $\rho_{\rm raw} = \phi^{-2}$ and $V_{\perp,0}/V_{\parallel,0} = \phi^{-3}$; Tier 1 coordinate arithmetic; not physical invariants.
> - **Bare angle:** $\sin^2\theta_W^{\rm bare} = \phi^{-3}$; Tier 3 gauge-kinetic hypothesis (H-EW); one unresolved physical-map assumption.
> - **GUT scale:** $M_{\rm red}\phi^{-9}$; Tier 3, conditional on O.15.
> - **Z-pole audits:** the physical-hypercharge comparator gives $0.136725$ (40.87% low); the native kernel with the imported A2 benchmark gives $0.16957$ (26.66% low). Both are Tier 3 negative consistency results; the pre-registered 2-loop audit (App GRF §GRF.4.3) records the running check as **FAILED** (best Standard-Model case −52σ).
> - **Closure:** the target-normalized route is an implementation check only; ultraviolet and infrared action-level closure remain open.

**4.3.4 Conditional coupling ratio [Tier 1 algebra conditional on a Tier 3 premise]**

Assuming the Tier 3 boundary hypothesis $\sin^2\theta_W^{\rm bare} = \phi^{-3}$, the corresponding ratio of the weak ($g$) and hypercharge ($g'$) couplings follows from the exact identity **$\phi^3 - 1 = 2\phi$**.
*Proof:* $\phi^3 = \phi \cdot \phi^2 = \phi(\phi+1) = \phi^2 + \phi = (\phi+1) + \phi = 2\phi + 1$. Thus, $\phi^3 - 1 = 2\phi$.

The ratio is:
$$\tan^2 \theta_W = \frac{\sin^2 \theta_W}{\cos^2 \theta_W} = \frac{\phi^{-3}}{1 - \phi^{-3}} = \frac{1}{\phi^3 - 1} = \frac{1}{2\phi}$$
$$\frac{g'}{g} = \frac{1}{\sqrt{2\phi}} \implies \frac{g}{g'} = \sqrt{2\phi} \approx 1.79891$$
The algebra is exact, but its physical status inherits the unresolved Tier 3 gauge-kinetic premise. It does not independently derive the relative force strengths.

---

**4.4 Physical Interpretation**

**4.4.1 Electromagnetic Field as Rotated W³ + B**

GCT reads the mixing of the pre-mixed gauge fields ($W^3_\mu$ and $B_\mu$) as a **Coordinate Transformation** [Tier 3 interpretation] between the "Lattice Basis" (aligned with projection axes) and the "Propagation Basis" (aligned with phason eigenmodes).
* **The Photon ($\gamma$):** The mode that aligns with the **flat direction** of the vacuum potential, remaining massless.
* **The Z Boson:** The mode that aligns with the **stiff direction** of the lattice dilation, acquiring mass via the Higgs mechanism.

**4.4.2 $W^\pm, Z$ masses from the candidate boundary [Tier 3 conditional]**

At tree level the mass ratio is a consequence of the mixing angle. Under the Tier 3 candidate boundary:
$$\frac{M_W}{M_Z} = \cos \theta_W = \sqrt{1 - \phi^{-3}} \approx 0.8740$$
The PDG ratio $M_W/M_Z = 0.88136 \pm 0.00015$ leaves a 0.83% residual, about $49\sigma$ on the direct ratio. This is not a precision agreement and cannot promote the boundary hypothesis: it is a conditional tree-level consequence that lacks the required radiative treatment (Open Problems O.19 and O.5).

**4.4.3 Geometric interpretation [Tier 3 conjecture]**

GCT may interpret an eventual gauge-kinetic ratio as a measure of how a normalized excitation couples to the hypercharge and isospin channels. The projector calculation alone does not establish that interpretation, and it does not show that 23.6% of a fluctuation is geometrically sequestered in $E_\perp$. That stronger reading remains conditional on an action-level derivation of the gauge coefficients.

---

**4.5 RGE Audit: Three Non-Closing Routes**

> [!IMPORTANT]
> **Epistemic status: Tier 3 negative consistency result.**
>
> The exact $I_h$ irrep inventory is group theory, but its use as a scale-activation schedule is a Tier 3 ansatz. The native kernel calibrates three $Z_i$ factors to the Standard-Model beta coefficients. The physical-hypercharge comparator and the native kernel both miss the Z-pole (running check **FAILED**, App GRF §GRF.4.3), while the target-normalized route reaches it only because the endpoint is supplied as an input. None establishes an autonomous boundary or flow law.

*[Tier 1 Standard-Model RGE algebra and finite group inventory; Tier 3 GCT boundary, scale, activation and physical-flow inferences — computational audits in Appendix GPE and App GRF.]*

**4.5.1 Native irrep-activation ansatz**

The native ansatz activates the finite $I_h$ irreps according to their dimensions and uses equal canonical projector shares. That supplies a disclosed candidate curve, not a beta-function derivation. Three independent normalization factors $Z_i$ are defined so that the saturated coefficients equal the three Standard-Model one-loop coefficients exactly; the $Z_i$ therefore carry the absolute coefficient information and the ansatz does not predict it. In its present step schedule the highest-dimensional irreps activate only at the ultraviolet endpoint and contribute on a zero-measure interval. The schedule, the signs of the three beta functions and their coupling to the gauge sectors all remain Tier 3 model inputs.

The imported benchmark $\alpha_2^{-1}(M_{\rm GUT}) = 24.0$ is Parameter Ledger anchor A2, the MSSM unified coupling (§4.3.3). It is not chosen to reproduce the infrared endpoint, and the kernel does not transport it successfully: the H-EW boundary gives $\sin^2\theta_W(M_Z) \approx 0.16957$, 26.66% low. The native route is a failing calibrated ansatz, not a successful interpolation.

**4.5.2 Resolution depth as a candidate mechanism [Tier 3]**

GCT proposes that scale dependence may be represented by the depth at which a probe resolves the 3D quasicrystal and its 6D parent description:

- **Low energy** ($\mu \sim M_Z$, large $\lambda$): the probe is represented by a coarse-grained 3D quasicrystal description. The value $\sin^2\theta_W(M_Z) = 0.23122$ is an external observational comparator and, in conditioned calculations, part of the low-energy coupling normalization.

- **High energy** ($\mu \sim M_{\rm GUT}$, small $\lambda$): the probe is represented as resolving more of the 6D parent structure. The value $\phi^{-3}$ is a Tier 3 gauge-kinetic boundary hypothesis, not exposed by the canonical projector.

A per-axis measure argument cannot connect these regimes: its $\phi^{-1}$ linear factor and $\phi^{-6}$ determinant ratio belong to a raw, non-isometric frame and change under row rescaling, while the proper projectors do not. A physical flow must instead be derived from a normalized scale-dependent effective action. The resolution-depth picture is thus a candidate mechanism, not a replacement derivation of the Standard Model beta functions; its physical content begins only when a coarse-graining map acts on a normalized microscopic action and predicts more than the endpoints used to define it.

**4.5.3 Target-normalized kernel [implementation check]**

Define the **resolution depth** $t = \ln(\mu/M_Z)$, so $t = 0$ at the Z-pole and $t = T_{\rm GUT} = \ln(M_{\rm GUT}/M_Z)$ at the candidate ultraviolet boundary. A phenomenological lattice-resolution function interpolates an effective dimension $D_{\rm eff} \in [3, 6]$:

$$F(t) = 3 + \frac{3}{1 + e^{-(t - T_{GUT}/2)/\sigma}}, \quad \sigma = \frac{T_{GUT}}{2\ln\phi}$$

with the phenomenological phason de-resolution kernel

$$\beta_{geo}(t) = \frac{e^{-t^2/(2\sigma^2)}}{\int_0^{T_{GUT}} e^{-t'^2/(2\sigma^2)} dt'}, \quad \frac{d\sin^2\theta_W}{dt} = +\Delta \cdot \beta_{geo}(t)$$

where $\Delta$ is fixed by the two declared boundary values

$$\sin^2\theta_W(M_{\rm GUT}) = \phi^{-3}_{\text{(Tier 3 hypothesis)}}, \quad \sin^2\theta_W(M_Z) = 0.23122_{\text{(observed)}}.$$

Because $\beta_{\rm geo}$ is normalized and $\Delta$ is solved from those same endpoints, integrating the equation reaches the endpoint by construction. A 5,000-step RK4 integration recovers the imposed endpoint to machine precision, which verifies only the sign, integration direction and numerical normalization of the kernel. The endpoint agreement is not empirical support for H-EW, the Gaussian shape or the resolution-depth interpretation, and the route is excluded from the prediction ledger.

**4.5.4 What the negative result establishes**

The convention-correct one-loop comparator and the native irrep kernel produce large adverse residuals, so there is no numerical evidence for H-EW at present. Neither failed flow is derived from the GCT microscopic action, so the audit does not by itself falsify H-EW at an unspecified scale.

The pre-registered gauge-running audit (App GRF §GRF.4.3) confirms that the miss is not a loop-order, threshold, normalisation or comparator effect: H-EW at $M_{\rm GUT}$ is incompatible with Standard-Model running, and with A2 it is incompatible with any SM extension (since $b_Y \ge 41/6$ for any content containing the Standard Model, A2 = 24–25 forces $\sin^2\theta_W(M_{\rm GUT}) \ge 0.280$–$0.288 > \phi^{-3}$). The check is recorded as **FAILED**. Run upward at two loops, the measured value reaches $\phi^{-3}$ only at 243 GeV; placing H-EW at 243 GeV would be endpoint fitting. Whether to retire A2 and A4–A6 ($Z_1$–$Z_3$) is an open v1.4.0 decision; v1.3.0 keeps the counts (11 declared core inputs; 24 numbered Ledger inputs). The surviving research content is narrower but testable:

1. derive a normalized 6D gauge action and the relative $SU(2)$/$U(1)$ generator traces, thereby deciding H-EW independently of the projector frame;
2. derive the coarse-graining map, beta functions and threshold matching from that action, including the two independent phason elastic constants rather than a single scalar surrogate;
3. derive or retire the O.15 scale assignment instead of inserting it;
4. predict at least two low-energy gauge observables from a common ultraviolet state without using either observable to set the flow amplitude.

Until those conditions are met, no partial theoretical autonomy is claimed for the electroweak boundary or endpoint. O.15 supplies the action/RG bridge; QLQCD-1L (Appendix QLA) and Open Problem O.5 remain linked non-perturbative closure targets.

> [!IMPORTANT]
> **Firewall Metadata [Weinberg Z-pole]**
> - **Type:** RGE audit / negative consistency result
> - **Inputs:** Tier 3 $\phi^{-3}$ boundary hypothesis; Tier 3 O.15 $M_{\rm GUT}$ assignment; route-specific use of A2 or of the measured low-energy coupling normalization
> - **Physical-hypercharge comparator:** $0.136725$; 40.87% low
> - **Native calibrated kernel:** $0.16957$; 26.66% low
> - **Target-normalized integrator:** endpoint imposed; no physical residual
> - **Pre-registered SM-kernel audit (App GRF §GRF.4.3):** best case $0.0673$ (2-loop, A2 = 25), −52σ; A2 + H-EW no-go for any SM extension; running check **FAILED**
> - **Status:** Tier 3 open boundary; current implementations do not close; physical action/RG closure open

### 4.5.5 Extension to the Strong Coupling — bare handle and open running gap

*[Tier 3 bare-handle and running branch. **Headline disclosure**: the proposed bare handle $\alpha_s(\text{bare}) \approx 0.0382$ is not a same-scale prediction for $\alpha_s(M_Z)$. Evolving it with the $Z_3$-calibrated native kernel gives $\alpha_s(M_Z) \approx 0.05204$, about 55.9% below the observed $0.118$. This adverse result is the load-bearing QLQCD-2 research debt (App QLA.7).]*

The candidate Geometric RGE framework models running through lattice resolution depth rather than deriving it from virtual-particle loop counting. The same proposed principle is applied here to the strong coupling $\alpha_s$; the current endpoint audit shows that the principle is not yet a closed dynamics.

**Tier 3 calibrated handle (10 integer + $\phi^2$ geometric factor; closure pending O.42):**

The bare value is written as the product of two geometric numbers; each number is Tier 1 given P1, while its role in $\alpha_s$ is a Tier 3 reading:

$$\alpha_s^{-1}(\text{bare}) \;=\; \underbrace{10}_{\text{RT 3-fold axis count}} \;\cdot\; \underbrace{\phi^2}_{H_4\text{ Cartan/root-metric slope factor, squared}} \;\approx\; 26.18.$$

**Factor 1 — The integer 10 [Tier 1 given P1].** The rhombic triacontahedron (RT) acceptance window possesses exactly *ten* three-fold rotational axes, corresponding to the 20 three-fold vertices of the RT grouped in antipodal pairs (V3 §3.1.2). This count is fixed by **Postulate P1** (Parameter Ledger §0.1 — the icosahedral cut-and-project ansatz). The axis count is the Tier 1 content used here; the separate V3 §3.2.1 matrix construction (traceless seeds spanning five dimensions, an eight-dimensional closure and an $A_2$ fingerprint) is not specific to the RT inventory and supports only an open Tier 3 $\mathfrak{su}(3)$ candidate, with uniqueness under App ORQ O.39. The integer 10 is therefore a Tier 1 substrate invariant *conditional on P1* — the count follows from the icosahedral selection, while the icosahedral choice itself is the structural postulate P1, not a Tier 1 deduction.

**Factor 2 — The slope factor $\phi^2$ [Tier 1 number given P1; Tier 3 role].** The proposal is that the bare $\alpha_s$ is set by the *square* of the area-scaling factor on the icosahedral lattice. By Lemma T-McK.4 (App USS §USS.7.3), the golden factor entering the projection is exactly
$$\bigl|2\cos(\pi/5)\bigr| = \phi = \tfrac{1}{2}(1+\sqrt{5}),$$
forced by the Lie-algebraic structure of $E_8$ through the $H_4$ Cartan entry $-\phi$, the golden-ratio root metric, and the cut-and-project slope (Humphreys, *Reflection Groups and Coxeter Groups*, §3.7). The Coxeter-element eigenvalues remain roots of unity on the unit circle; $\phi$ is not their magnitude. The number $\phi^2 \approx 2.618$ is Tier 1 *given* the icosahedral / $H_4$ / $E_8$ ambient choice fixed by Postulate P1. Reading it as the "area" scaling factor that sets the bare $\alpha_s$ (one factor of $\phi$ per linear lattice dimension, two of them spanned by the 3-fold axis pair in $E_\perp$) is a Tier 3 heuristic, not a consequence of the Coxeter structure.

**Combination — area-law product [Tier 3 calibrated handle pending O.42].** The combination $\alpha_s^{-1}(\text{bare}) = N_{\text{axes}} \cdot \phi^{2}$ is proposed as an *area-law product*: the bare inverse coupling counts independent topological sources (the 10 axes) weighted by the substrate's natural area-scaling factor ($\phi^2$ from the $H_4$ Cartan/root-metric slope). The two factors are separately geometric, but the strong-sector product is not promoted to Tier 2 closure until the native strong-running / QLQCD boundary map derives the $10\phi^2$ handle from the hadronic action rather than selecting it as the calibrated bare handle.
$$\alpha_s(\text{bare}) \;=\; \frac{1}{10\phi^2} \;\approx\; 0.0382.$$
This is a proposed ultraviolet handle, so directly comparing it with the observed $\alpha_s(M_Z) \approx 0.118$ would mix scales. The relevant audit evolves the handle from $M_{\rm GUT}$ to $M_Z$ with the same Tier 3 native resolution-depth ansatz used above (Appendix GPE, App GRF §GRF.4). It returns $\alpha_s(M_Z) \approx 0.05204$, a **55.9% low** endpoint. Because $Z_3$ is calibrated to the Standard-Model one-loop coefficient, this is a calibrated consistency failure, not a first-principles GCT prediction. QLQCD-2 (App QLA.7) must derive both the ultraviolet handle and the non-perturbative running. With Standard-Model β-functions instead, $\alpha_3^{-1}$ starting from $10\phi^2$ reaches zero at $2$–$6\times10^6$ GeV (one to two loops; App GRF §GRF.4.3), far above $M_Z$, so $\alpha_s(M_Z)$ is undefined (non-perturbative) from the declared handle; $10\phi^2 = 26.18$ also sits in the MSSM range, not the Standard-Model value $\alpha_3^{-1}(M_{\rm GUT}) = 46.2$.

**Status:** BARE HANDLE COMPUTED; PHYSICAL BRIDGE OPEN. The factorisation $\alpha_s^{-1}(\text{bare}) = 10\phi^2$ uses two geometric numbers, each Tier 1 *conditional on Postulate P1*, whose role in $\alpha_s$ is a Tier 3 reading; their product as a gauge-kinetic coefficient is a Tier 3 calibrated handle until O.42 / QLQCD-2 derives it from the hadronic action. The current native running leaves a 55.9% endpoint gap.

**Falsification Condition:** If the full non-perturbative QLQCD-2 corrections to the 
10-axis SU(3) boundary condition cannot close the current 55.9% endpoint gap to reproduce 
$\alpha_s(M_Z) = 0.1180 \pm 0.0009$ (PDG 2026 QCD review), the $10\phi^2$ handle is refuted as the bare strong coupling. The numbers 10 and $\phi^2$ would remain arithmetic facts given P1; what fails is their Tier 3 use, individually and in the area-law product, as the source of $\alpha_s$.
