# PMNS θ₂₃ Lattice-Hamiltonian Resolution — Step 1

**Goal:** Derive, from the App_M microscopic 6D lattice Hamiltonian, the equation governing the phason field Φ⊥(**r**) sourced by a single pinned phonon-sector defect (e.g., an electron) at the origin. Solve it in closed form.

**Motivation:** This is the first step of the pre-registered lattice-Hamiltonian discriminant (Ch09 §9.4.2) for the 4.09σ PMNS θ₂₃ tension. Matter-averaging (Step 2) requires the single-defect Yukawa profile established here.

**Status:** Closed-form [Tier 1], conditional on App_M §M.2 and App_K §K.3–K.5. One geometric scalar (|b⊥|) still to be pinned in Step 1b.

---

## 1.1 Starting Point — Bare Vacuum Action

From App_M §M.2, the 6D microscopic Hamiltonian

$$H = \sum_{n \in \mathbb{Z}^6} \frac{\mathbf{p}_n^2}{2M} + \frac{\kappa}{2} \sum_{\langle n,m \rangle} (\mathbf{u}_n - \mathbf{u}_m)^2 + V_{lock}(\mathcal{P}_\perp \mathbf{u}_n)$$

admits a continuum limit (App_M §M.3) with decomposition **u** = **u**∥ + **u**⊥, **u**∥ ∈ E∥, **u**⊥ ∈ E⊥. The quadratic action is

$$S_{vac}[\mathbf{u}_\parallel, \mathbf{u}_\perp] = \int d^3x\, \left[ \frac{K_\parallel}{2} (\nabla \mathbf{u}_\parallel)^2 + \frac{K_\perp}{2} (\nabla \mathbf{u}_\perp)^2 + V_{lock}(\mathbf{u}_\perp) \right]$$

Expand V_lock around the ground state **u**⊥ = 0:

$$V_{lock}(\mathbf{u}_\perp) = V_{lock}(0) + \tfrac{1}{2} m_{lock}^2\, \mathbf{u}_\perp^2 + \mathcal{O}(\mathbf{u}_\perp^4)$$

Dropping the constant, define

$$m_{lock}^2 \equiv V''_{lock}(0)$$

This is the only coefficient of the confining potential that enters the linear response.

## 1.2 Identification of m_lock via the Healing Length

App_K §K.5 defines the healing length ξ by balancing elastic and locking energies at scale ξ:

$$K_\perp / \xi^2 \sim V''_{lock}(0) = m_{lock}^2 \quad \Longleftrightarrow \quad \boxed{\xi^2 = K_\perp / m_{lock}^2}$$

**Consequence:** m_lock is not a free parameter. It is fixed by K⊥ (App_K §K.4) and ξ (App_K §K.5, two-route derivation to machine precision, ξ ≈ 8.5 nm).

$$m_{lock}^2 = K_\perp / \xi^2 \quad [\text{Tier 1/2, inherited}]$$

## 1.3 Linearized Equation of Motion

Euler-Lagrange of the static action yields one equation per component of **u**⊥. Components decouple under the isotropy guaranteed by App_K §K.2 (the Gram matrix G⊥ is proportional to the identity on E⊥ for canonical AKN). Writing Φ⊥ for any one component:

$$-K_\perp \nabla^2 \Phi_\perp(\mathbf{r}) + m_{lock}^2\, \Phi_\perp(\mathbf{r}) = 0 \quad (\text{bare vacuum}) \quad [\text{Tier 1, direct linearization of App_M §M.2}]$$

## 1.4 Sourcing by a Pinned Phonon Defect

A "pinned knot" (the GCT picture of a charged lepton, Ch09 §9.4.1) is a localized topological defect carrying a 6D Burgers vector **b** ∈ Z⁶ — the winding of **u** around the defect core.

Under the canonical AKN projection,

$$\mathbf{b} = \mathbf{b}_\parallel + \mathbf{b}_\perp, \quad \mathbf{b}_\parallel = \mathcal{P}_\parallel \mathbf{b} \in E_\parallel, \quad \mathbf{b}_\perp = \mathcal{P}_\perp \mathbf{b} \in E_\perp$$

**Key observation [Tier 1].** Any nontrivial 6D Burgers vector necessarily projects onto both subspaces. A phonon-sector dislocation carrying a nonzero winding in **u**∥ therefore drags a matching perpendicular source **b**⊥ into the phason sector. This is not a coupling put in by hand — it is forced by the geometry of the 6D-to-3D projection (Socolar–Lubensky–Steinhardt dislocation theory for icosahedral quasicrystals, standard).

The Burgers singularity enters the phason EoM as a localized δ-source:

$$\boxed{\;-K_\perp \nabla^2 \Phi_\perp(\mathbf{r}) + m_{lock}^2\, \Phi_\perp(\mathbf{r}) = \mathcal{F}_\perp\, \delta^3(\mathbf{r})\;} \quad [\text{Tier 1}]$$

where F⊥ is the scalar point-force coefficient with SI dimensions of force. Step 1b §1.6 fixes its dimensional form as F⊥ = K⊥·|**b**⊥|·a₆. (Earlier drafts wrote the right-hand side as "b⊥ δ³(r)" treating b⊥ as a force coefficient — dimensionally the same but notationally misleading, since |**b**⊥| is a Burgers length. See §1b.6 for the cleaned-up form.)

## 1.5 Closed-Form Yukawa Solution

Rewrite using ξ² = K⊥ / m_lock²:

$$\left( -\nabla^2 + \frac{1}{\xi^2} \right) \Phi_\perp(\mathbf{r}) = \frac{b_\perp}{K_\perp}\, \delta^3(\mathbf{r})$$

The Green's function of the Helmholtz operator (−∇² + ξ⁻²) in 3D is G(r) = e^(−r/ξ) / (4π r). Therefore

$$\boxed{\;\Phi_\perp(\mathbf{r}) = \frac{b_\perp}{4\pi K_\perp} \cdot \frac{e^{-r/\xi}}{r}\;} \quad [\text{Tier 1}]$$

**Asymptotic behavior:**

| Regime | Profile | Physical picture |
|---|---|---|
| r ≪ ξ (≈ 8.5 nm) | Φ⊥ ≈ b⊥ / (4π K⊥ r) | Unscreened Coulomb-like phason tail |
| r ≫ ξ | Φ⊥ ∝ e^(−r/ξ)/r → 0 | Exponentially screened beyond healing length |

## 1.6 Integrated Strain Charge of One Defect

The total phason strain injected by a single pinned defect into the surrounding vacuum is

$$Q_\perp \equiv \int d^3r\; \Phi_\perp(\mathbf{r}) = \frac{b_\perp}{K_\perp} \int_0^\infty 4\pi r^2 \cdot \frac{e^{-r/\xi}}{4\pi r}\, dr = \frac{b_\perp}{K_\perp}\,\xi^2$$

$$\boxed{\;Q_\perp = \frac{b_\perp\, \xi^2}{K_\perp}\;} \quad [\text{Tier 1}]$$

This is the quantity that enters Step 2: matter density n (electrons per cm³) × Q⊥ gives the saturated background ⟨Φ⊥⟩ in the bulk.

## 1.7 Parameter Inventory — Zero Free Parameters

| Symbol | Value / Source | Tier |
|---|---|---|
| K⊥ | (E_P / ℓ_P³) · φ⁻¹⁸ | 1/2 (App_K §K.4) |
| ξ | 8.5 nm (two-route, 0 ppm convergence) | 2 (App_K §K.5) |
| m_lock² | K⊥ / ξ² | 1 (§1.2) |
| b⊥ | \|P⊥ b\|, b ∈ Z⁶ primitive knot winding | pending Step 1b |

**No phenomenological coupling has been introduced.** The only quantity not yet given a numerical value is |b⊥|, which is a mechanical computation from the canonical AKN projection matrices (App_K §K.2). That computation is Step 1b and does not require new physics — only the already-defined Gram matrices G∥, G⊥ and the primitive Z⁶ unit vectors.

## 1.8 What This Step Establishes

1. A single pinned defect creates a Yukawa-screened phason field extending over the healing length ξ.
2. The equation is forced by App_M's Hamiltonian + 6D Burgers vector geometry — no coupling constants inserted.
3. The integrated strain charge Q⊥ = b⊥ ξ² / K⊥ is the bridge to Step 2 (matter-averaged background).

## 1.9 Falsification Gates Already Active

- If Step 1b yields |b⊥| = 0 for the electron (i.e., the minimal knot has no phason component), the entire mechanism dies — there is no matter-induced phason background, and the 45° prediction must either survive on its own or be falsified.
- If ξ derived from App_K §K.5 were not the same as the ξ appearing in the Yukawa profile, the whole framework is internally inconsistent. (Check: they are identical by construction in §1.2.)

## 1.10 Dependencies for Step 2

Step 2 (matter-averaged ⟨Φ⊥⟩ through Earth crust) requires:

1. Numerical |b⊥| from Step 1b.
2. Observational input: n_e ≈ 1.3 × 10²⁴ /cm³ and n_nucleon ≈ 1.7 × 10²⁴ /cm³ in Earth crust (ρ ≈ 2.8 g/cm³).
3. Saturation check: n · ξ³ ≫ 1 (expected: ~10²⁴ × (8.5 × 10⁻⁷)³ ≈ 6 × 10⁴, so yes, bulk crust is deep in the phason-saturated regime).
4. Direction selection in E⊥: how the vectorial **b**⊥ averages over an isotropic distribution of pinned defects. (Naive expectation: scalar magnitude, random orientation → ⟨**b**⊥⟩ = 0 but ⟨**b**⊥ **b**⊥ᵀ⟩ ≠ 0 — i.e., no mean field but nonzero variance field. This is a critical subtlety for Step 2.)

---

**End of Step 1.** Step 1b (compute |b⊥| from canonical AKN projection matrices) is the next minimal unit of work.
