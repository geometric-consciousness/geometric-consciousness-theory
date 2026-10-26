### **Appendix ULA: The Unified Lattice Action**

> **Epistemic Status:** [Tier 2 — framework derivation under the icosahedral substrate postulate; specific theorem statuses are noted per section. §ULA.7 phason α correction has template-direction compatibility only per App ORQ O.19, and neither its sign nor its magnitude is derived from the AKN action; §ULA.7.1 numerical magnitude inputs are Tier 3 pending O.19/O.5 AKN-loop closure, while O.15 governs the separate stiffness/RG exponent link]

This appendix provides the tiered **microscopic-action scaffold** for the GCT Effective Action. It removes circular definitions of $G$ and $\hbar$ by formulating the dynamics in lattice units and displaying the effective hierarchy induced by the projection geometry. The construction is a Tier 2 mechanism scaffold with Tier 3 numerical/continuum closure, not a theorem-grade microscopic derivation of the full continuum action; its photon-identification part is a Tier 3 declared open programme (V2 Ch06 §6.1).

---

## ULA.0 Epistemic Status (Tier Discipline)

- **Tier 2 mechanism + Tier 3 continuum-limit completion:** The 6D hypercubic lattice Hamiltonian is the explicit microscopic ansatz under the icosahedral substrate postulate. Its hydrodynamic limit supplies the effective-field scaffold used below, but a theorem-grade convergence proof from the discrete Hamiltonian to the displayed continuum action is not yet supplied.
- **Geometry-only non-identifiability + Tier 3 physical-link hypothesis:** The integer $D=18$ has Tier 2 support through the $H_3$ Shephard-Todd invariant-degree anchor. Point-group symmetry, however, permits independent quadratic coefficients on $E_\parallel$ and $E_\perp$, and the isotropic Hamiltonian of §ULA.2 sets them equal (§ULA.3); fixing the substitution/inflation map does not remove this freedom. The specific law $K_\perp/K_\parallel = \phi^{-18}$ is therefore the independent Tier 3 stiffness-map hypothesis P3b of the Parameter Ledger (O.15(b)), listed outside the parameter count exactly like H-EW; it requires a target-blind microscopic energy law plus a kinetic/mobility law, not geometry alone.

## ULA.1 Calibration Firewall (Single Anchor, SI mapping)

To ensure the technical rigor of Geometric Consciousness Theory and prevent the "Planck Loop" (where units are defined by the constants they seek to explain), we enforce a strict **Calibration Firewall**. 

### The Rules of the Firewall:
1. **Lattice Primacy:** All physical derivations must be performed in dimensionless lattice units ($a_6, t_6, \kappa$) first.
2. **Standardization:** Dimensional constants ($G, \hbar, c$) are treated as **Derived Conventions** used for human readability, not fundamental primitives. **Planck units are derived conventions, not primitives.**
3. **Single Anchor Mapping:** The conversion from lattice units to SI units (meters, seconds, kilograms) must be performed via a declared **Experimental Anchor** (typically $m_e$ or $E_{vac}$).

### Lattice Primitives (Dimensionless):
- **Lattice Spacing ($a_6$):** The minimum distance between nodes. $a_6 \equiv 1$.
- **Update Time ($t_6$):** The duration of one selection cycle. $t_6 \equiv 1$.
- **Bond Stiffness ($\kappa$):** The elastic restorative force. $\kappa \equiv 1$.
- **Node Mass ($M$):** The inertial weight of a lattice vertex. $M \equiv 1$.

In this system, dimensionless derived quantities and structural ratios are represented as **Structural Eigenvalues**. Dimensional constants such as the SI speed of light remain unit conventions; GCT uses only the dimensionless lattice ratio $\hat c = c/c_P$ (Parameter Ledger row $c$) as a structural object.

## ULA.2 Microscopic Hamiltonian on $\mathbb{Z}^6$

The fundamental dynamics are governed by a discrete sum over the 6D nodes:
$$ H = \sum_{n \in \mathbb{Z}^6} \frac{\mathbf{p}_n^2}{2M} + \frac{\kappa}{2} \sum_{\langle n,m \rangle} (\mathbf{u}_n - \mathbf{u}_m)^2 + V_{lock}(\mathcal{P}_\perp \mathbf{u}_n) $$

Where:
- $\mathbf{u}_n \in \mathbb{R}^6$ is the displacement vector of node $n$.
- $\langle n,m \rangle$ denotes summation over nearest neighbors in $\mathbb{Z}^6$.
- $V_{lock}$ is the periodic potential arising from the boundary of the Rhombic Triacontahedron window in $E_\perp$.

As written, $V_{lock}(\mathcal{P}_\perp \mathbf{u}_n)$ depends on the phason displacement itself, not on its gradient, so it breaks the uniform phason-shift symmetry that keeps phasons gapless and gives the phason a gap (§ULA.4.1 relates $m_{phason}$ to it). Postulate 6.1 (V2 Ch06) identifies the photon with this mode, which is one reason the photon-as-phason construction is a declared open programme (V2 Ch06 §6.1): a shift-symmetric locking term, or a derivation of which branch $V_{lock}$ gaps, is required [Tier 3 open].

## ULA.3 Projection and the Quadratic-Action No-Go

Let $P_\parallel$ and $P_\perp$ be the canonical complementary projectors of the lifted icosahedral action on $\mathbb{R}^6$. The representation decomposes into two inequivalent real three-dimensional irreducible components, so by Schur's lemma every invariant symmetric quadratic form is
$$ Q = aP_\parallel + bP_\perp . $$
Icosahedral symmetry removes the cross term but leaves two independent positive coefficients; it fixes neither coefficient nor the ratio $b/a$ (direct solution of $R_g^T Q R_g = Q$ gives a two-dimensional solution space, spanned by the two projectors) [Tier 1 representation theory].

The §ULA.2 nearest-neighbour Hamiltonian uses the isotropic Euclidean bond form $Q=\kappa I_6=\kappa(P_\parallel+P_\perp)$. With canonical row-isometric projection it therefore gives equal bare quadratic weights, $K_\perp/K_\parallel=1$, not $\phi^{-18}$. This is a **Tier 2 action-level no-go within the declared isotropic Hamiltonian**: it does not say that phasons cannot become softer, only that the softness is not generated by projection or symmetry alone. The obstruction survives a fixed substitution rule: for a sector-diagonal long-wavelength pencil with elastic weights $(a,b)$ and inertial weights $(\alpha,\beta)$, the generalized-eigenvalue ratio is $\lambda_\perp/\lambda_\parallel=b\alpha/(a\beta)$, which spans all positive reals while the point group and inflation map are unchanged. The internal locking potential $V_{lock}(\mathcal{P}_\perp\mathbf{u})$ can supply phason-specific mass and nonlinear vertices but does not, without an explicit coarse-graining calculation, assign the gradient-stiffness ratio; and the invariant degrees $\{2,6,10\}$ classify invariant polynomials without becoming an anomalous dimension by group theory alone.

The earlier display $K_\perp/K_\parallel=(\det G_\perp/\det G_\parallel)^3=\phi^{-18}$ is **retired**: it depends on the choice of row frame (a relative rescaling of the rows by $s$ changes it by $s^{18}$ while leaving the projectors unchanged), and it equals 1 for canonical projectors. GCT may still test the independent Tier 3 hypothesis P3b (O.15(b); listed outside the parameter count like H-EW, as in Appendix DPS):
$$ \frac{K_\perp}{K_\parallel} = \phi^{-D_{H3}} = \phi^{-18} \approx 1.731 \times 10^{-4} \qquad \text{[Tier 3 hypothesis]}, $$
under which a $\sim 10^{-4}$ suppression would make the phason sector the "soft" carrier relative to the "hard" phonon bonds. Closure requires additional physics: a target-blind microscopic energy law and a kinetic/inertial or mobility law, followed by the full dynamical pencil and an attractive, coordinate-invariant RG fixed ray.

### ULA.3.1 The Rhombohedral Shape Factor
The analytic derivation $\eta_{analytic} = 1 - 1/(2N)$ assumes a topologically perfect continuous distribution. However, evaluating the discrete Coulomb matrix directly on the AKN projected vertex coordinates reveals an $\eta_{computed}$ that slightly deviates, capturing the explicit rhombohedral non-sphericity of the physical defect cage. 

The reported 41.5 ppm residual in $\alpha^{-1}$ is therefore the post-bilayer O.19 target for the uncalculated 1-loop QLQCD correction. The $\eta_{computed}$ pipeline preserves the separate RT non-sphericity diagnostic without absorbing the residual into an adjustable shape factor.

## ULA.4 Continuum Limit (EFT) and Field Identification

In the hydrodynamic limit ($a_6 \to 0$), the coarse-grained phonon field $\mathbf{u}_\parallel$ and phason field $\mathbf{w}_\perp$ generate the candidate emergent fields:
- **Acoustic Metric:** Condensate fluctuations produce an effective Lorentzian metric $g_{\mu\nu}$ for the waves they carry [Tier 3]. Whether the gravitational carrier is the phonon or the phason sector is open (V2 Ch04_00 §4.B.1); a phonon carrier at the bare speed ($\approx 76c$ under P3b) is incompatible with GW170817 unless a mechanism bringing its speed to $c$ is derived.
- **Maxwell Gauge Potential:** Conditional on a derived gapped physical eigenstate bundle over the phason collective-coordinate manifold, adiabatic phason motion may define a $U(1)$ Berry connection $A_\mu$ [Tier 3, declared open programme, V2 Ch06 §6.1]. Periodicity of $V_{lock}$ supplies neither a field quotient nor that eigenstate bundle, and a finite point-group quotient does not by itself force Berry curvature. The first-principles tile-dynamics derivation of the antisymmetric $F_{\mu\nu}F^{\mu\nu}$ kinetic term and the two-polarization gauge-redundancy structure is the Ch06/App ORQ O.15 closure target.

Under the continuum-limit ansatz used in this appendix, the discrete Hamiltonian is represented by the **GCT Master Action**:
$$ S = \int d^4x \left[ \mathcal{L}_{metric}(g_{\mu\nu}) + \mathcal{L}_{gauge}(A_\mu) + \mathcal{L}_{interaction} \right] $$

Here $\mathcal{L}_{interaction}$ is a placeholder, not a microscopic vertex. It does not derive the spinorial matter sector, normalize chirality, derive the deformation/spin-orbit vertices, or fix the spin-phason coefficient; consistent with the field-typing analysis of V1 Ch17 §17.1.3, no Level-II verdict follows from it.

### ULA.4.1 The Phason Condensate and Dark Energy Density

In a separately specified broken-vacuum completion, a frozen phason condensate may acquire a vacuum expectation value $\langle\Phi_\perp\rangle$. The literal §ULA.2 Hamiltonian and $H_3$ symmetry alone do not select the quadratic sign, vacuum radius, direction, or a non-zero target, so the condensate amplitude is treated as conditional rather than as an output already set by $V_{lock}$. The associated conditional vacuum energy density is the massive scalar condensate formula:
$$\boxed{\rho_\Lambda = \frac{1}{2} m_{phason}^2 \langle\Phi_\perp\rangle^2} \quad \text{[Tier 3 — pending Tier 2 elevation upon derivation of } \langle\Phi_\perp\rangle \text{ from } V_{lock}\text{]}$$

This formula is cited in V2 Ch14 §14.1.3 as the "App ULA Lagrangian condensate formula." The condensate amplitude $\langle\Phi_\perp\rangle$ is related to the phason locking potential via the saddle-point condition $V_{lock}'(\langle\Phi_\perp\rangle) = m_{phason}^2 \langle\Phi_\perp\rangle$. Until $\langle\Phi_\perp\rangle$ is derived from first principles, $m_{phason}$ remains an Open Parameter (see Parameter Ledger §4 and Open Problem O.1). As written, that condition is the stationarity condition of $V_{lock} - \tfrac12 m_{phason}^2\Phi_\perp^2$, whose value at the stationary point is not $+\tfrac12 m_{phason}^2\langle\Phi_\perp\rangle^2$, and $\Phi_\perp$ (a displacement) needs a stiffness normalisation before $m^2\Phi^2$ is an energy density; the total potential and the field normalisation are open [Tier 3].

The alternative holographic/Friedmann consistency form (V2 Ch14 §14.1.5, Ryu-Takayanagi + Friedmann) is the Ch14 canonical expression:
$$\rho_\Lambda = \frac{3\Omega_\Lambda}{8\pi}\frac{\hbar H_0^2}{c\ell_P^2} \quad \text{[Tier 1 rewriting of the Friedmann identity + Tier 3 area-law reading and numerical evaluation]}$$
With $G = \ell_P^2c^3/\hbar$ this expression is identically $\Omega_\Lambda\rho_{crit}c^2$, i.e. the definition of $\Omega_\Lambda$; it gives $\rho_\Lambda \approx 0.0818\cdot\hbar H_0^2/(c\cdot\ell_P^2)$ at $\Omega_\Lambda = 0.685$ (Planck 2018). Its area-law susceptibility reading is a Tier 3 interpretation; the absolute value imports $H_0$ and $\Omega_\Lambda$ pending O.1/O.4 closure. These two expressions become mutually constraining only after $\langle\Phi_\perp\rangle$ is derived from $V_{lock}$; they are not independent Tier 2 magnitude derivations.

## ULA.5 Dimensionless Constants (Lattice Units)

We define the following system parameters entirely in lattice units:
- **Lattice Speed of Light ($\hat{c}$):** $\hat{c} = \sqrt{K_\perp / \rho_{eff}}$ is the structural wave-speed relation. The numerical export $\hat{c} \approx \phi^{-9}$ is Tier 3, conditional on the P3b stiffness-map hypothesis (§ULA.3) and on the corresponding density normalization.
- **Lattice Action Quantum ($\hat{\hbar}$):** Derived from the minimal action per update ($\hat{\hbar} \equiv 1$).
- **Lattice Gravity ($\hat{G}$):** Defined by the area of the unit cell ($\hat{G} \equiv 1$). This is a labelling convention: evaluating $G = c^3a_6^2/(4\hbar)$ in lattice units does not give 1 under the speed convention of §ULA.6, and the reconciliation is open.

## ULA.6 SI Mapping (Experimental Anchors)

To map the lattice eigenvalues to the SI system, we select the **Electron Mass ($m_e$)** as the primary anchor (the vacuum scale $E_{vac}$ is a separate quantity). 

- **Physical Anchor:** $m_e \approx 0.511$ MeV.
- **Conversion Rule:** One lattice mass unit $M$ is defined such that the ground-state defect resonance matches $m_e$.

Once anchored, the traditional Planck units emerge as **derived length/time scales**:

| SI Convention | GCT Status | Derivation / Mapping |
| :--- | :--- | :--- |
| **Planck Length ($\ell_P$)** | Derived Scale | Half the lattice spacing, $\ell_P = a_6/2 \approx 1.6 \times 10^{-35}$ m. |
| **Planck Time ($t_P$)** | Open calibration | $t_P = \ell_P/c \approx 5.4 \times 10^{-44}$ s. In the Parameter Ledger convention ($c = \phi^{-9}c_P$, with $c_P = a_6/t_6$ the bare lattice speed) and $a_6 = 2\ell_P$, the update time would be $t_6 = 2\phi^{-9}t_P \approx 1.4\times10^{-45}$ s, not $t_P$. The earlier identification $t_6 = t_P$ gives $a_6/t_6 = 2c$ and is inconsistent with that convention; the time calibration is open (O.15(b)). |
| **Lattice light ratio ($\hat c = c/c_P$)** | Geometric Ratio | $c/c_P = \sqrt{K_\perp/K_\parallel}$ with $c_P = a_6/t_6$ (common inertial normalization assumed); the SI value of $c$ is a convention, while the stiffness-ratio link $\phi^{-9}$ remains Tier 3 pending O.15(b). |
| **Gravity ($\hat{G}$, lattice units)** | Labelling convention (open) | $\hat{G} \equiv 1$ by convention. Evaluating $G = c^3a_6^2/(4\hbar)$ in lattice units ($\hat a_6 = \hat\hbar = 1$, $\hat c = \phi^{-9}$ under the Ledger speed convention) gives $\phi^{-27}/4 \approx 5.7\times10^{-7}$, not 1; the reconciliation is open (§ULA.5). The SI value of Newton's $G$ is postdicted in §ULA.8 via the Jacobson thermodynamic chain as $G = c^3 a_6^2 / (4\hbar)$ ([L$^3$ M$^{-1}$ T$^{-2}$]), with O.14 Planck-link and dimensional-anchor qualifications; the ULA.6 row reports the lattice-unit convention and is not itself an SI expression for $G$. |
| **Action ($\hbar$)** | Lattice-unit convention | $\hat{\hbar} \equiv 1$ (Action per lattice cell). |

> [!IMPORTANT]
> **Warning on Circularity:** In GCT, it is incorrect to say "$G$ is derived from the Planck length." It is correct to say: "The Planck length is the human mapping of the fundamental lattice spacing $a_6$, and $G$ is the area-equivalent of that spacing."

## ULA.7 Finite-N Vacuum Polarization and the 1/(2N) Correction [Tier 2 single-shell trace + Tier 3 bilayer integer-factor handle; rigorous geometric closure pending O.5]

**Setup.** In the finite-N lattice regularization, the one-loop vacuum
polarization $\Pi(0)$ receives a finite-size correction from the discrete
trace over the $N=144$ cage nodes (Tier 3 cage posit per V3 Ch07 §7.1.3,
pending the O.38 minimization). Continuum limit: $\Pi(0)|_\infty$ as $N \to \infty$.

**Single-Shell Finite-N Trace.**
For $N$ nodes on a single $I_h$-symmetric icosahedral shell, the one-loop
self-energy admits the structural decomposition
$$\Pi(0)|_N = \sum_{i=1}^{N} G_{ii}^2 + \sum_{i \neq j} G_{ij}^2$$
where $G_{ij}$ is the lattice Green's function at zero momentum. The
off-diagonal term is a sum of squares and does **not** vanish; the rigorous
finite-$N$ structure is supplied instead by vertex-transitivity. For an
$I_h$-equivariant Green's function on a vertex-transitive shell the diagonal is
constant, $G_{ii} = c$, so the diagonal self-energy carries the exact normalized
weight
$$\frac{\sum_{i} G_{ii}^2}{(\operatorname{Tr} G)^2} = \frac{N c^2}{(N c)^2} = \frac{1}{N}
\qquad \text{(single }I_h\text{-symmetric shell of }N\text{ nodes),}$$
an identity that holds across the icosahedral, dodecahedral, and
icosidodecahedral shells under both Laplacian-resolvent and adjacency-resolvent
conventions (engine: `GCT_Physics_Engine/src/protocol_m7_bilayer_orthogonality.py`).
Identifying this normalized diagonal weight with the physical finite-$N$
correction $\Delta\Pi_1/\Pi_\infty = 1/N$ is the geometric step that — together
with the factor-of-2 promotion below — bundles with O.5.

**Two-Level Cage Structure and the Factor of 2.**
The cage commitment of V3 Ch07 §7.1.3 is the *two-level* structure $N = 12_{\text{outer}} \times 12_{\text{inner}} = 144$: 12 outer dodecahedral face directions, each carrying a 12-fold inner vertex sub-shell. Under the bilayer tensor trace $G^{(2L)} = G^{(\text{outer})} \otimes G^{(\text{inner})}$ the normalized diagonal weight factorizes,
$$\frac{\sum_d (G^{(2L)}_{dd})^2}{(\operatorname{Tr} G^{(2L)})^2} = \left[\frac{\sum_i G_{ii}^2}{(\operatorname{Tr} G)^2}\right]\left[\frac{\sum_j g_{jj}^2}{(\operatorname{Tr} g)^2}\right] = \frac{1}{12}\cdot\frac{1}{12} = \frac{1}{144} = \frac{1}{N},$$
so the tensor construction alone reproduces the single-shell $1/N$ — **not** $1/(2N)$ (verified in the engine protocol above; this follows from $\operatorname{Tr}(A\otimes B) = \operatorname{Tr}A\,\operatorname{Tr}B$ and $\operatorname{diag}(A\otimes B) = \operatorname{diag}(A)\otimes\operatorname{diag}(B)$). Obtaining the empirically required
$$\frac{\Delta\Pi}{\Pi_\infty} = \frac{1}{2N} = \frac{1}{288}$$
requires an additional within-level / across-level projection beyond the stated tensor product — a structural input the bilayer counting motivates but does not derive.
The "factor of 2" reflects the bilayer-pairing ansatz and remains a Tier 3 discrete integer-factor handle selected to land near $\alpha$ alongside the 360 multiplier; the *full* closure of the within-level vs. across-level cancellation balance is the geometric step bundled with O.5.

The factor of 2 is the load-bearing Tier 3 integer-factor handle that moves the bare
$\alpha^{-1} = 360\phi^{-2} \approx 137.508$ prediction to the bilayer-
corrected $\alpha^{-1}_{\text{GCT}} = 360\phi^{-2}(1 - 1/288) \approx 137.030$,
which lands 41.5 ppm from CODATA (V1 Ch13 §13.2.4). This is a calibrated postdiction until O.5 derives the bilayer pairing factor from the AKN bubble integral rather than selecting it over the $1/N$ alternative. As evidence that φ or icosahedral structure is special, this match is **Tier 4**: the preregistered constant control test (v3, NEGATIVE-FRAGILE; App PSC §PSC.9.6) found φ's pattern of matches on 21 constants not distinguishable from that of random constants (58 of 300 random bases did at least as well). The test "excludes, at power ≥ 0.8, an effect in which φ hits at least 6 of the 8 informative rows through a real effect; weaker effects are not excluded." The number is kept as descriptive arithmetic.

> [!IMPORTANT]
> **Status of the factor of 2 (Tier 3 discrete integer-factor handle).**
> The $1/N$ single-shell trace is rigorous for any $I_h$-symmetric shell via
> the vertex-transitivity identity $\sum_i G_{ii}^2/(\operatorname{Tr} G)^2 = 1/N$.
> The factor of 2 promoting $1/N \to 1/(2N)$ requires an additional
> structural input beyond the single-shell vertex-transitivity identity; in the
> present manuscript this input is imported from the two-level $12 \times 12$
> cage commitment (V3 Ch07 §7.1.3) as a *motivated* counting argument rather
> than a single-axiom derivation. A first-principles derivation of the
> factor of 2 from the $N = 144$ cage geometry — explicit construction of
> an $I_h$-closed two-level decomposition such that the off-diagonal cross-
> level Green's-function contribution vanishes by orthogonality and the
> diagonal correction integrates to $1/(2N)$ rather than $1/N$ — is bundled
> with Open Problem **O.5** (QLQCD-1L closure; App ORQ §ORQ.5). A closure of O.5
> would allow the factor of 2 to be reassessed as a derived rather than selected
> input; no promotion is automatic. Until then the $1/(2N)$ correction is a
> calibrated selection: it is preferred over the $1/N$ alternative only because
> the latter would shift $\alpha^{-1}_{\text{GCT}}$ from 137.030 to 136.553
> ($\sim 3500$ ppm off CODATA), and the V1 Ch13
> §13.2.4 prediction stands as a Tier 3 numerical relation (Tier 3 600-cell multiplier; mechanism open — the RT solid-angle construction is withdrawn, V1 §13.2.1–§13.2.2) plus Tier 3 bilayer integer-factor handle rather than a Tier 1 derived correction.

### ULA.7.1 Topological Origin of Phason Anti-Screening

The GCT tree-level relation for the Fine-Structure Constant ($\alpha^{-1} = 360\phi^{-2}$) yields a value 3443 ppm larger than observed. The bilayer handle $1/(2N)=1/288$ reduces this bare residual to the 41.5 ppm post-bilayer residual. That remaining 41.5 ppm identifies the required direction and magnitude target of a candidate **Phason Anti-Screening shift**; neither is yet derived from the AKN action, and the exact magnitude remains a QLQCD-1L/O.19 closure target. Calling a phason mode bosonic does not by itself supply the continuous non-Abelian gauge structure, physical eigenbundle, vertices or loop measure needed to infer anti-screening (fermionic electron loops screen in standard QED).

The analytical task for QLQCD remains the rigorous integration of the phason loop on the Ammann-Kramer-Neri (AKN) grid. The bare 0.34% mismatch fixes the correction direction required by the data but does not establish its mechanism or sign; the 41.5 ppm post-bilayer residual is the numerical target that a source-derived discrete AKN bubble integral would have to reproduce.

The 0.34% bare residual and the 41.5 ppm post-bilayer residual are not adjustable constants. The loop calculation targets the 41.5 ppm residual only; any coefficient extracted by matching that residual to a continuous-running formula is therefore an O.19 diagnostic quantity until derived from the icosahedral AKN bubble integral.

> [!IMPORTANT]
> **Status of the sign and magnitude.** The required shift direction is compatible with a separately supplied non-Abelian bosonic anti-screening / asymptotic-freedom template: $\alpha^{-1}_{bare} > \alpha^{-1}_{obs}$ can be read as $\alpha^{-1}(\text{UV}) > \alpha^{-1}(\text{IR})$ when "bare" is assigned to the icosahedral/Planck-scale reference and "observed" to the IR Thomson-limit value. This applies to the bare-to-observed shift only: the bilayer term overshoots the observed value, so the remaining 41.5 ppm residual runs in the opposite direction and is not accounted for by the same convention. `GCT_Physics_Engine/src/protocol_phason_oneloop_AKN.py` checks that convention-level direction only; it does not derive a native AKN phason loop. The opposite sign of fermion-loop QED screening does not establish that the phason sector supplies the desired sign, and the algebraic Galois map $\phi\mapsto-1/\phi$ fixes no physical sign.
>
> The *magnitude* target for O.19 is the 41.5 ppm post-bilayer residual, not the full +3443 ppm bare residual. A one-loop NAGT-style running formula $\Delta \alpha^{-1} = (b_{phason}/2\pi) \ln(\Lambda_{UV}/\Lambda_{IR})$ applied to a continuous-gauge phason structure is therefore only a diagnostic template for that residual. Taking $\Lambda_{UV} = M_{Planck}$ as the icosahedral cutoff and $\Lambda_{IR} = m_e$ as the Thomson reference gives $\ln(\Lambda_{UV}/\Lambda_{IR}) \approx 51.5$; targeting the 41.5 ppm residual gives a back-solved $b_{phason}$ of order $7\times10^{-4}$ and a corresponding finite-group class-sum coefficient of order $2\times10^{-4}$ (reported only as an order-of-magnitude diagnostic; the magnitude itself is not closed, see the two structural caveats below). **Status of this framing: template-direction compatibility only.** Two structural caveats preclude promotion to a native mechanism or magnitude closure: (a) the NAGT $(11/3) C_2$ beta function presupposes a continuous propagating gauge boson plus ghost cancellation, while the icosahedral $I_h$ symmetry of the AKN substrate is a discrete reflection group that does not admit a quadratic Casimir in the standard Lie-algebraic sense; (b) a broad icosahedral `class_sum_eff` bracket permits diagnostic retuning rather than a structural derivation. Engine: `GCT_Physics_Engine/src/protocol_o19_phason_alpha_magnitude.py` evaluates a continuous-gauge template, not an AKN derivation; the convention-level direction check is `protocol_phason_oneloop_AKN.py`. **Open Problem O.19** therefore stands at template-direction compatibility only, not a sign-validated native mechanism or a magnitude closure. The remaining open closure paths are (a) a discrete-lattice analogue of the continuous-gauge running (Kotani-Sunada operator algebra on AKN, or a finite-group Bost-Connes-type analysis) and (b) a first-principles derivation of `class_sum_eff` from explicit icosahedral irrep theory plus the AKN bubble integral with a tight range; closure of (a) or (b) bundles with O.5 (QLQCD-1L non-perturbative quark-mass closure).

*The bare value $\alpha^{-1} = 360\phi^{-2}$ is the model's tree-level reference [Tier 3 numerical relation (Tier 3 600-cell multiplier; mechanism open — the RT solid-angle construction is withdrawn, V1 §13.2.1–§13.2.2)]. It does not supersede the $1/288$ bilayer term, which remains the separate Tier 3 integer-factor handle of §ULA.7 used to reach the 137.030 postdiction.*

> [!IMPORTANT]
> **Firewall Metadata [Lattice Vacuum Polarization]**
> - **Type:** Calibrated-Postdiction (Tier 3 integer-factor handle pending O.5)
> - **Inputs:** $N=144$ (Bilayer cage nodes), 1-loop Finite-N Trace
> - **Degrees of Freedom:** Tier 3 discrete integer-factor handle $1/(2N)$ selected to land near $\alpha$ alongside the 360 multiplier; the magnitude anchor is the SI-unit reference [Tier 1 anchor], not a continuous fitted parameter
> - **Provenance:** Tier-3 calibrated integer-factor handle ($1/(2N)$ selected vs $1/N$ which misses CODATA by $\sim3500$ ppm; O.5 closure target)

## ULA.8 The Jacobson Entropy Chain — From Phason Fluid to G [Tier 2 thermodynamic mechanism + Tier 4 Planck-link conjecture + Tier 3 dimensional/SI anchor]

This derivation establishes the thermodynamic mechanism for $G$ through the Jacobson (1995) horizon-entropy chain, but the numerical Planck-link inherits O.14 and the $m_e$ SI dimensional anchor. The current disposition is **Tier 2 thermodynamic mechanism + Tier 4 Planck-link conjecture (inherits O.14) + Tier 3 dimensional/SI anchor — 2273.725 ppm postdiction (display 2274 ppm), NOT a Tier 2 prediction**. The numerical branch uses model-authoritative $\alpha_{\rm GCT}=\phi^2/360$, CODATA $m_e$, and exact SI $h,c$. We apply the Jacobson argument to the local Rindler horizon of an accelerated worldline, as in Jacobson (1995). Reading that horizon as the causal horizon of an Agent or Selection Operator is a separate Tier 4 interpretation; it is not used in, and is not supported by, the thermodynamic mechanism.

**Step 1: Anchor to the Electron Mass**
The electron, as the primary topological defect, dictates the size of the unit lattice spacing $a_6$. Instead of defining mass from the Planck length, we define the lattice spacing from the electron:
$$m_e = M_{Planck} \cdot \phi^{-107} \cdot (1 - 5\alpha_{\rm GCT}), \qquad \alpha_{\rm GCT}=\phi^2/360$$
Because $M_{Planck} = \frac{2\hbar}{c \cdot a_6}$ in the discrete lattice (free of continuum $8\pi$ artifacts), we invert this to isolate $a_6$:
$$a_6 = \frac{2\hbar}{m_e c} \cdot \phi^{-107} \cdot (1 - 5\alpha_{\rm GCT})$$

**Step 2: Phason Horizon Entropy**
For a uniformly accelerated worldline in the phason medium (no Agent is required), the local causal boundary is a Rindler horizon radiating at the Unruh temperature:
$$T_U = \frac{\hbar a}{2\pi c k_B}$$
Following the macroscopic thermodynamic identity $\delta Q = T dS$, the heat flux across the Unruh boundary must be proportional to the lattice entropy of the horizon area, taken as one $k_B$ (one nat) per $a_6^2$ plaquette; one bit per plaquette would divide $G$ below by $\ln 2$. 

**Step 3: Newton's G postdiction**
Applying the Jacobson identity linking horizon area variations to the emergent field equations yields the exact macroscopic gravitational coupling:
$$G_{predicted} = \frac{c^3 a_6^2}{4\hbar}$$
This postdicts Newton's Constant from $m_e$, the model invariant $\alpha_{\rm GCT}=\phi^2/360$, $\phi$, and the exact SI conversions $\hbar,c$, with the numerical Planck-link inheriting O.14 and the $m_e$ SI anchor. The evaluated postdiction $6.689475523 \times 10^{-11}$ differs from the CODATA 2022 $G_N$ measurement by **2273.725 ppm (display 2274 ppm)**; since it is the electron row inverted, it is not independent evidence (Tier 4 as evidence: not distinguishable from numerology for strong effects; App PSC §PSC.9.6). The all-CODATA-$\alpha$ value is a separate 2013.345 ppm sensitivity branch; see V2 Ch09 §9.1.4.

## ULA.9 The Jacobian of Screening (Planck-to-Biology Scale Ratio) [Tier 1 algebraic identity + Tier 3/Tier 4 inputs; the $F_{bio}$ application is a quarantined scenario]

The historical biophysical transduction scenario used a dimensionless scale factor $(\ell_P/\xi)^3$ to bridge Planck-scale vacuum stiffness to the biological scale. That $F_{bio}$ expression is **quarantined as an unadopted dimensional ansatz** (V3 Ch13 §13.1.2; App BEB): no normalized mode, interaction coefficient or executable provenance makes it a force law, and no biological force, rate or voltage is derived from it. The ratio below is retained only as an algebraic identity and for traceability; it is not a derived suppression of a physical force, and its use as a "Planck-to-biology bridge" is a withdrawn scenario rather than a live derivation.

**Algebraic identity (displayed for traceability):**

By definition: $\ell_P \equiv \sqrt{\hbar G/c^3}$ and the polaron healing length $\xi \equiv \hbar c / (\alpha^2 m_e c^2)$.

The linear ratio is therefore:
$$\frac{\ell_P}{\xi} = \alpha^2 \frac{m_e}{M_{Planck}}$$

Substituting the electron-mass relation $m_e / M_{Planck} = \phi^{-107}(1-5\alpha)$ — a Tier 3 anchor-normalised Planck-link check ($m_e$ is the A1 anchor; O.14), whose 1006 ppm residual misses the pre-committed 1000 ppm rule by 6 ppm (App FSM P.1c reports a FAIL of that rule):
$$\text{Jacobian} = \left(\frac{\ell_P}{\xi}\right)^3 = \left[\alpha^2 \cdot \phi^{-107}(1-5\alpha)\right]^3 \approx 1.1 \times 10^{-80}$$

Every symbol is either a universal constant ($\alpha, \hbar, G, c$) or a fixed GCT input in the electron-mass chain ($\phi^{-107}$, $5\alpha$). Given those Tier 3/Tier 4 inputs, the substitution introduces no additional fitted coefficient; this is arithmetic on $\xi = a_0/\alpha \approx 7.25$ nm [Tier 1 arithmetic; its identification as the vacuum/polaron healing length is Tier 3], not a derivation of a physical scale bridge. The algebraic substitution yields $\approx 1.11 \times 10^{-80}$, consistent with the Parameter Ledger §2 Jacobian entry and Ch18 §18.2.1 entry with $\xi = 7.25$ nm; `verify_independent/verify_fbio_jacobian.py` checks that arithmetic only. No "80-order-of-magnitude suppression of a Planck-scale vacuum force" follows, because the force law it would multiply is quarantined.

*Cross-reference: Vol. 3 Ch. 13 §13.1.2 (the quarantined $F_{bio}$ scenario, displayed there for traceability only).*
