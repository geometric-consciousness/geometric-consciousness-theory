# PMNS θ₂₃ Lattice-Hamiltonian Resolution — Step 3

**Goal:** Derive the modification to neutrino dispersion induced by the matter-averaged variance field ⟨**Φ**⊥ ⊗ **Φ**⊥⟩ (Step 2), project it onto the neutrino flavor basis, and extract the predicted shift in θ₂₃.

**Status:** Closed-form at leading order [Tier 1]. The leading-order result is **NEGATIVE** — i.e., at leading order, matter does NOT shift θ₂₃. This has direct implications for the Ch09 §9.4.2 pre-registered discriminant.

---

## 3.1 Setup — the Neutrino Phason Mode in a Background

A neutrino is an itinerant phason wave (Ch09 §9.4.1). Writing the total phason field as **Φ**⊥ = **Φ**⊥^{bg} + **δΦ**⊥ — background (matter-averaged) + fluctuation (the ν mode) — the relevant part of the action is the locking potential:

$$V_{lock}(\mathbf{\Phi}_\perp^{bg} + \boldsymbol{\delta\Phi}_\perp) = V_{lock}(\mathbf{\Phi}_\perp^{bg}) + V'_{lock}\cdot\boldsymbol{\delta\Phi} + \tfrac{1}{2}\boldsymbol{\delta\Phi}\cdot V''_{lock}(\mathbf{\Phi}_\perp^{bg})\cdot \boldsymbol{\delta\Phi} + O(\delta\Phi^3)$$

Expand V''_lock around the ground state:

$$V''_{lock}(\mathbf{\Phi}^{bg}) = V''_{lock}(0) + V'''_{lock}(0)\cdot\mathbf{\Phi}^{bg} + \tfrac{1}{2} V^{(4)}_{lock}(0)\cdot(\mathbf{\Phi}^{bg} \otimes \mathbf{\Phi}^{bg}) + O((\Phi^{bg})^3)$$

Average over the matter-induced background distribution (Step 2: ⟨**Φ**^{bg}⟩ = 0, ⟨**Φ**^{bg} ⊗ **Φ**^{bg}⟩ = Σ **I**_{E⊥}, where Σ ≡ n ξ a₆⁴(3−φ)/(24π)):

$$\langle V''_{lock} \rangle_{bg} = V''_{lock}(0) + \tfrac{1}{2}\,V^{(4)}_{lock}(0) : (\Sigma\,\mathbf{I}_{E\perp}) + O(\Sigma^2)$$

The linear term drops out because ⟨**Φ**^{bg}⟩ = 0.

## 3.2 Effective Mass-Squared Correction — Tensor Structure

For an approximately isotropic RT window (icosahedral symmetry is stronger than full O(3), but for averaged bulk matter the leading contribution reduces to the isotropic invariant — see §3.6 for the caveat), the fourth derivative tensor has the form

$$V^{(4),\,abcd}_{lock}(0) = \tfrac{\lambda_4}{3}\,(\delta^{ab}\delta^{cd} + \delta^{ac}\delta^{bd} + \delta^{ad}\delta^{bc})$$

where λ₄ ≡ V^{(4)}_{lock}(0)_{aaaa} (scalar invariant). Contracting with the isotropic variance Σ δ^{cd}:

$$V^{(4),\,abcd}_{lock} \cdot (\Sigma\,\delta^{cd}) = \tfrac{\lambda_4}{3}\,(3 \delta^{ab}\Sigma + \Sigma\,\delta^{ab} + \Sigma\,\delta^{ab}) = \tfrac{5\lambda_4}{3}\,\Sigma\,\delta^{ab}$$

So

$$\langle V''_{lock} \rangle_{bg} = m_{lock}^2\,\mathbf{I}_{E\perp} + \tfrac{5\lambda_4}{6}\,\Sigma\,\mathbf{I}_{E\perp} + O(\Sigma^2)$$

**Key result:** the leading-order matter-induced correction to the effective mass-squared operator for phason fluctuations is **proportional to the identity on E_⊥**.

$$\boxed{\;\Delta M^2_{\text{matter}} = \tfrac{5\lambda_4}{6}\,\Sigma\,\mathbf{I}_{E_\perp} \quad [\text{Tier 1 | isotropic RT window assumption}]\;}$$

## 3.3 Projection onto the Neutrino Flavor Basis

Three neutrino flavors correspond to three harmonic modes in E_⊥ (Ch09 §9.4). Whether they are taken as (a) directions in E_⊥ spanning an orthonormal basis, or (b) orthogonal harmonic-order modes at fixed Φ geometry, the conclusion is the same:

$$\langle \nu_\alpha | \Delta M^2_{\text{matter}} | \nu_\beta \rangle = \tfrac{5\lambda_4}{6}\,\Sigma\,\langle \nu_\alpha | \nu_\beta \rangle = \tfrac{5\lambda_4}{6}\,\Sigma\,\delta_{\alpha\beta}$$

The matter correction in the flavor basis is proportional to δ_{αβ} — **flavor-blind**.

## 3.4 Consequence: Zero θ₂₃ Shift at Leading Order

The matter-modified mass-squared matrix is

$$M^2_{\text{eff}} = M^2_{\text{vac}} + C\,\mathbf{I}_{\text{flavor}}, \qquad C \equiv \tfrac{5\lambda_4}{6}\,\Sigma$$

Adding C · **I** to a diagonal matrix shifts all eigenvalues by the same amount C, leaving mass-squared differences unchanged:

$$\Delta m^2_{\alpha\beta}|_{\text{matter}} = \Delta m^2_{\alpha\beta}|_{\text{vac}} \qquad [\text{Tier 1}]$$

Mixing angles depend only on mass-squared differences. Therefore

$$\boxed{\;\theta_{23}^{\text{matter-leading}} = \theta_{23}^{\text{vac}} = 45^\circ \qquad [\text{Tier 1}]\;}$$

**The leading-order lattice-Hamiltonian matter correction does not shift θ₂₃ at all.**

Identically, θ₁₂ and θ₁₃ receive zero matter-induced correction at this order. The CP phase δ_CP is also unchanged.

## 3.5 Implications for the Ch09 §9.4.2 Pre-Registered Discriminant

Ch9 §9.4.2 states (post-fix by this project):

> "if the lattice derivation recovers the standard MSW result, the bare 45° prediction is falsified; if it departs from MSW consistent with the 4.5° shift, the prediction elevates to Tier 2."

The leading-order lattice-Hamiltonian derivation gives:
- **Different** from standard MSW. Standard MSW produces ~0.00004° shift in θ₂₃ through flavor-selective (ν_e-only) CC scattering. The lattice-Hamiltonian derivation gives exactly zero shift through flavor-blind quadratic phason coupling. Two different mechanisms, two different predictions.
- **Does not reconcile** the 4.5° gap. The mechanism as constructed cannot produce the observed 49.5°.

This triggers a third outcome the discriminant did not anticipate: **the lattice-Hamiltonian mechanism is distinct from MSW, but also does not reconcile with observation.**

**Current status of the 45° bare prediction after Step 3:**
- Remains at Tier 3 (Tension), 4.09σ.
- The "lattice-Hamiltonian resolution" hypothesis no longer provides a free pass — it has been calculated and does not close the gap.
- Either a sub-leading mechanism rescues the prediction (candidates in §3.7) or the 45° prediction faces an increased falsification pressure.

## 3.6 Why the Leading Order is Flavor-Blind — Icosahedral Symmetry Theorem

The flavor-blindness result is not an approximation — it follows rigorously from the icosahedral symmetry of the RT window.

**Symmetry theorem.** Under the icosahedral point group I_h, rank-2 symmetric tensors on E_⊥ decompose as

$$(\mathbf{E}_\perp \otimes \mathbf{E}_\perp)_{\text{sym}} \;=\; A_g \oplus H_g$$

where A_g is the 1-dimensional scalar (trace) representation and H_g is the 5-dimensional traceless rank-2 representation.

- The matter-averaged source ⟨Φ_bg ⊗ Φ_bg⟩ = Σ × I_{E⊥} has only **A_g content** (Step 2 result under A2).
- V^{(4)}_{lock} preserves I_h symmetry. Its action on A_g rank-2 sources produces A_g rank-2 output.
- A_g rank-2 = scalar times I_{E⊥}. Projected onto any flavor basis (orthonormal, spanning E_⊥, or 3 Galois-conjugate axes within E_⊥), this is proportional to δ_{αβ}.

**Conclusion [Tier 1, symmetry-protected].** Zero θ₂₃ shift at leading order is forbidden to fail unless one of the following channels opens:

1. **Anisotropic source (H_g content in ⟨Φ_bg ⊗ Φ_bg⟩).** Requires Step 2 Assumption A2 to be violated — i.e., macroscopically oriented matter where polycrystalline averaging does not complete. Implausible for isotropic Earth crust over NOvA/T2K baselines, but not impossible.

2. **Operators that mix A_g and H_g channels.** Forbidden at the V^(4) quadratic-coupling level by I_h symmetry. Allowed at higher orders (V^(6) etc.) only via the rank-6 icosahedral invariants that couple A_g source to H_g output through anomalous operators. Highly suppressed.

3. **Flavor-dependent effective λ₄.** If the three ν flavors sit at three distinct harmonic orders n_α of the phason mode, the effective quartic coupling λ₄(n_α) may differ per flavor because each harmonic probes V_lock at a different Φ amplitude. This is genuinely sub-leading (geometric effect, not symmetry-forbidden). Magnitude depends on Δλ₄(n_α)/λ₄, which requires explicit computation.

The isotropic leading-order result (§3.2) is **symmetry-theorem robust** against channels (1) and (2) above the forbidden thresholds. (3) is the only genuine escape route and is genuinely sub-leading.

## 3.7 Sub-Leading Mechanisms — Scorecard

**Note:** Entries below have been updated after Step 4's basis-commutativity analysis. See `step4_harmonic_lambda4_diagnostic.md` for details.

| Mechanism | Basis structure | Shifts θ₂₃? | Tier |
|---|---|---|---|
| Leading (λ₄ Φ² δΦ²) | C · I — mass-basis diagonal | **No** — flavor-blind | 1 — computed (Step 3) |
| Harmonic-dependent λ₄(n_α) | diag(C_α) — mass-basis diagonal | **No** — commutes with M²_vac | 1 — computed (Step 4) |
| Anisotropic crust (H_g content in ⟨Φ⊗Φ⟩) | Non-diagonal in mass basis if crust orientation ≠ mass-axis | **Yes in principle** | 3 — not yet derived |
| Gradient coupling ⟨∇Φ⟩² | Isotropic under I_h → mass-basis diag | **No** | 1 — ruled out by same A_g theorem |
| Higher-order (λ₆, λ₈, …) | All preserve I_h A_g → A_g → mass-basis diag | **No** | 1 — ruled out |
| Direct CC-like coupling to charged leptons | Flavor-basis diagonal → non-mass-diagonal | **Yes in principle** | unworked — requires V3 Part I |

**Most promising remaining:** direct CC-like coupling from the electroweak sector (requires substantial new derivation), or anisotropic matter (speculative). Most simple phason-strain sub-leading mechanisms are ruled out by the basis-commutativity argument of Step 4 §4.1.

## 3.8 Order-of-Magnitude Estimate for the Leading-Order Coefficient C

For completeness, the magnitude of the flavor-blind shift C = (5λ₄/6) Σ, even though it does not affect mixing:

- λ₄ ~ K⊥/ξ⁴ (harmonic-confinement estimate; actual value depends on RT window shape, could be substantially smaller if V_lock is near hard-wall)
- Σ = n ξ a₆⁴(3−φ)/(24π) ≈ 1.43 × 10⁻¹¹⁸ m²
- C ~ (5/6) × (K⊥/ξ⁴) × Σ = (5/6) × K⊥ × Σ/ξ⁴

In natural units (ℏ = c = 1): K⊥ ≈ 3.8 × 10¹⁰⁸ eV⁴, Σ/ξ⁴ dimensionless ≈ 2.8 × 10⁻¹⁰² (= Σ/(ξ² × ξ²), with Σ/ξ² ≈ 2 × 10⁻¹⁰² and another 1/ξ² factor).

Wait — Σ/ξ⁴ has dimension [m²/m⁴] = 1/m². In natural units this is eV², not dimensionless. Let me redo.

[C] = [K⊥][Σ]/[ξ⁴] = (eV⁴)(eV⁻²)/(eV⁻⁴) = eV⁶. That's wrong dimension for a mass-squared shift.

**Dimensional reconciliation required.** The correct dimensional form of (λ₄/6) Σ must have dim eV² (mass-squared). If λ₄ has dim eV⁸ (as a V^(4) with Φ in units of length = eV⁻¹, so Φ⁴ has dim eV⁻⁴, and V needs dim eV⁴, giving [V^(4)] = eV⁸), then λ₄ × ⟨Φ²⟩ has dim eV⁸ × eV⁻² = eV⁶. Still not eV².

The missing factor: the δΦ² term has dim eV⁻². When we identify δΦ with the canonical ν field, we normalize such that the kinetic term has coefficient 1/2. This normalization divides by K⊥ × (length)² or similar factors.

Clean conclusion: the dimensional coefficient requires careful canonical-field normalization that was not done cleanly in the schematic derivation above. The overall MAGNITUDE of C is uncertain, potentially from 0 (hard-wall V_lock) to order-of-magnitude estimates requiring careful canonical normalization.

**But the FLAVOR STRUCTURE is independent of this magnitude uncertainty** — the (5λ₄/6) Σ I result is exactly flavor-blind whatever the prefactor, because of the isotropy of ⟨Φ_bg ⊗ Φ_bg⟩ and the symmetric rank-4 structure of V^{(4)}_{lock} in the icosahedral window. The Step 3 conclusion (zero θ₂₃ shift at leading order) stands without requiring the magnitude to be computed.

[Tier 1 for flavor structure, Tier 3 for magnitude — pending canonical normalization work.]

## 3.9 Summary — What Step 3 Establishes

1. **The matter-induced phason perturbation couples to neutrino dispersion at quadratic order in Φ_bg** via the V⁽⁴⁾_lock term of the locking potential. [Tier 1]

2. **With isotropic ⟨Φ_bg ⊗ Φ_bg⟩ (Step 2 result, Tier 1 | Tier 2 modeling) and icosahedral-symmetric RT window, the correction is proportional to I_{E_⊥}** — flavor-blind. [Tier 1]

3. **Therefore all three mass-squared eigenvalues shift by the same amount C**, and mass-squared differences — the only observables entering oscillation — are unchanged. [Tier 1]

4. **θ₂₃, θ₁₂, θ₁₃, and δ_CP receive zero correction from matter at leading order.** [Tier 1]

5. **The observed 4.09σ tension in θ₂₃ is NOT resolved by the leading-order lattice-Hamiltonian matter effect.** The Ch09 §9.4.2 pre-registered discriminant produces a third outcome (lattice-Hamiltonian distinct from MSW, but also not reconciling the data). The 45° prediction retains Tier 3 (Tension) status. [Tier 1]

## 3.10 What Step 3 Does NOT Do

- **Does not rule out sub-leading mechanisms.** Harmonic-dependent λ₄(n_α), anisotropic matter, and higher-order couplings remain as potential resolutions. §3.7 scorecard lists candidates with tentative tier classifications.
- **Does not compute the magnitude of C.** The dimensional coefficient requires canonical field normalization and a detailed RT window curvature calculation not performed here. But the flavor structure is independent of C's magnitude.
- **Does not falsify the 45° prediction.** It increases falsification pressure by removing one of the main "lattice-Hamiltonian resolution" hypothesized rescues, but the prediction could still be rescued by sub-leading effects or by revised matter modeling.

## 3.11 Next-Step Candidates (Step 4+)

**Update after Step 4.** Path B (harmonic-dependent λ₄) has been investigated and ruled out by the basis-commutativity argument — a mass-basis-diagonal correction does not shift mixing angles. See `step4_harmonic_lambda4_diagnostic.md`.

Paths that remain open after Step 4:

**Path A' (Honest / conservative).** Update Ch09 §9.4.2 to reflect the full Steps 1–4 chain: leading and simple sub-leading corrections under I_h symmetry are ruled out. The 45° prediction becomes a strong pre-registered falsification test.

**Path B' (Research-grade).** Direct CC-like coupling derived from V3 Part I electroweak structure. Weeks of work.

**Path C' (Speculative).** Anisotropic-matter modeling using geophysical datasets. Not yet scoped.

---

**End of Step 3.** The leading-order result is established. The 45° prediction faces increased empirical pressure. See Step 4 for the elimination of the first sub-leading rescue.
