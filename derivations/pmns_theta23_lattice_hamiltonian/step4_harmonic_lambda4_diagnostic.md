# PMNS θ₂₃ Lattice-Hamiltonian Resolution — Step 4 (Diagnostic)

**Goal:** Evaluate whether harmonic-order-dependent λ₄(n_α) — the most promising sub-leading escape route in the Step 3 §3.7 scorecard — can produce a flavor-selective shift in θ₂₃.

**Status:** **Negative result [Tier 1].** Harmonic-dependent λ₄(n_α) produces a matter correction that is diagonal in the mass basis of the vacuum Hamiltonian. By the basis-commutativity theorem for 3-flavor oscillations, this does **not** shift mixing angles. Step 3 §3.7 scorecard error identified and corrected.

---

## 4.1 The Basis-Commutativity Theorem

The 3-flavor oscillation Hamiltonian in vacuum (at energy E) is

$$H_{\text{vac}} = \frac{M^2_{\text{vac}}}{2E}$$

where M²_vac is the mass-squared matrix, diagonal in the **mass basis** by definition. In matter,

$$H_{\text{matter}} = \frac{M^2_{\text{vac}}}{2E} + V_{\text{matter}}$$

Oscillation probabilities are determined by the eigenvectors of H_matter, not of H_vac. The key question: do the eigenvectors differ?

**Theorem.** If [V_matter, M²_vac] = 0, then V_matter and M²_vac share a common eigenbasis, which is the mass basis. The eigenvectors of H_matter are the same as the eigenvectors of M²_vac. The PMNS matrix (flavor ↔ mass rotation) is unchanged by matter. **All mixing angles are equal to their vacuum values.**

**Corollary.** Any V_matter that is **diagonal in the mass basis** (even with unequal diagonal entries) commutes with M²_vac trivially and leaves mixing angles unchanged.

**Standard MSW escape:** V_MSW = √2 G_F n_e · diag(1, 0, 0) is diagonal in the **flavor basis**, which is NOT the same basis in which M²_vac is diagonal. Therefore [V_MSW, M²_vac] ≠ 0, and mixing angles shift.

**Two bases are involved.** For V_matter to shift mixing angles, it must be diagonal (or close to diagonal) in a basis *different* from the mass basis. The natural candidate is the **flavor basis** — diagonality there gives CC-like behavior analogous to MSW.

## 4.2 Harmonic-Dependent λ₄(n_α) in the Mass Basis

Recall the leading-order result from Step 3 §3.2:

$$\Delta M^2_{\text{matter}} = \tfrac{5\lambda_4}{6}\,\Sigma\,\mathbf{I}_{E_\perp}$$

For **harmonic-dependent** λ₄(n_α) — where each mass eigenstate ν_α couples to V_lock with an effective quartic coefficient determined by its characteristic Φ excursion — this generalizes to

$$\Delta M^2_{\alpha\beta}\Big|_{\text{matter, sub-leading}} = \tfrac{5\lambda_4(n_\alpha)}{6}\,\Sigma\,\delta_{\alpha\beta}$$

The δ_{αβ} structure is inherited from the icosahedral A_g → A_g theorem of Step 3 §3.6. What changes is the α-dependence of the diagonal entries:

$$\Delta M^2_{\text{sub-leading}} = \text{diag}(C_1, C_2, C_3), \qquad C_\alpha = \tfrac{5\lambda_4(n_\alpha)}{6}\,\Sigma$$

**In the mass basis.** The matrix is diagonal in the same basis as M²_vac. Therefore [V_matter, M²_vac] = 0 and, by §4.1, mixing angles are unchanged.

$$\boxed{\;\theta_{23}^{\text{matter (harmonic-}\lambda_4\text{)}} = \theta_{23}^{\text{vac}} = 45^\circ\;} \quad [\text{Tier 1}]$$

## 4.3 Correction to Step 3 §3.7 Scorecard

The Step 3 §3.7 row for "Harmonic-dependent λ₄(n_α)" previously read:

> Harmonic-dependent λ₄(n_α) | Yes (marginal) | ~(Δn/n) × leading ≈ few % | Tier 2/3

This is **wrong**. The mechanism is mass-basis-diagonal, hence invisible to mixing angles by §4.1. The corrected entry:

> Harmonic-dependent λ₄(n_α) | **No** — mass-basis diagonal | shifts absolute masses, not mixing | Tier 1 (negative)

The Step 3 scorecard will be updated to reflect this.

## 4.4 Generalized Basis Analysis — Which Mechanisms Survive?

Extending the basis-commutativity test to every mechanism in the Step 3 §3.7 scorecard:

| Mechanism | Basis structure | Commutes with M²_vac? | Shifts θ₂₃? |
|---|---|---|---|
| Leading (λ₄ Φ² δΦ²) | C · I in any basis | Yes (trivially) | No |
| Harmonic-dependent λ₄(n_α) | diag(C_α) in mass basis | **Yes** (by §4.2) | **No** — corrected from Step 3 |
| Anisotropic crust (H_g content in ⟨Φ⊗Φ⟩) | Non-diagonal in mass basis if matter orientation aligns with a non-mass axis in E_⊥ | **No** (if alignment direction is not a mass eigenvector) | **Yes, in principle** |
| Gradient coupling ⟨∇Φ⟩² | Isotropic under I_h → diag in mass basis | Yes | No |
| Higher-order (λ₆, λ₈, …) | All preserve I_h A_g → A_g diagonal structure | Yes | No |

**Only the anisotropic-crust mechanism survives the basis-commutativity test.** Every phason-strain mechanism that respects macroscopic icosahedral symmetry produces a mass-basis-diagonal correction and leaves mixing angles unchanged.

## 4.5 What This Means for the 45° Prediction

Combining Steps 1–4, within the framework of the phason-strain Yukawa-sum picture:

1. **Leading-order matter correction is flavor-blind (A_g → A_g theorem).** [Step 3, Tier 1]
2. **Harmonic-dependent sub-leading correction is mass-basis-diagonal, doesn't shift mixing angles.** [Step 4, Tier 1]
3. **All I_h-symmetric higher-order corrections share the same mass-basis-diagonal structure.** [Step 4, Tier 1]

**Therefore, within the Steps 1–2 phason-strain framework, NO mechanism that respects macroscopic icosahedral symmetry can shift θ₂₃.**

The only remaining channels within this framework:

- **(a) Anisotropic matter** (violates Step 2 A2). Earth crust is macroscopically isotropic on NOvA/T2K baselines at the polycrystalline-averaging scale. Plausible contributions from crustal stratification or mantle transitions are geometrically small and would need specific Tier 3 analysis.
- **(b) Direct charged-lepton CC coupling** (outside the phason-strain framework). This would be the GCT analog of electroweak CC scattering — a ν_flavor / charged-lepton vertex sourced by the 6D lattice structure but with the PMNS flavor index carried through specifically. Computing it requires integrating Vol 3 Part I (Product Structure / Electron Knot / Gauge Group) with Step 1's Yukawa picture. This is substantial new work.

Neither (a) nor (b) is accessible via straightforward extension of Steps 1–3.

## 4.6 Updated Status of the 45° Bare Prediction

After Step 4, the epistemic picture sharpens further:

- **Tier 3 (Tension) status retained.** The 4.09σ gap with NOvA/T2K data remains unresolved.
- **Two sub-leading escape routes in Step 3 §3.7 are now closed by §4.1 basis-commutativity:** harmonic-dependent λ₄, higher-order I_h-symmetric couplings.
- **One speculative escape route remains (anisotropic matter).** Requires careful Tier 3 modeling of Earth-crust orientational correlations.
- **One research-grade escape route remains (direct CC coupling).** Requires V3 Part I integration — substantial.

The 45° prediction is now more exposed than after Step 3. The space of "simple" lattice-Hamiltonian resolutions has been nearly exhausted by symmetry arguments.

## 4.7 What to Do with This Result

Two paths:

**Path A' (honest / conservative).** Update Ch9 §9.4.2 with the full derivation-chain conclusion: the leading-order and next-to-leading-order lattice-Hamiltonian corrections under macroscopic icosahedral symmetry both give zero θ₂₃ shift. The 45° prediction is therefore promoted to a **strong pre-registered falsification test**: if further research into anisotropic matter or direct CC coupling also fails to close the gap, the 45° prediction is empirically falsified.

**Path B' (substantial / research-grade).** Attempt the direct CC coupling derivation by integrating Vol 3 Part I with the phason-strain picture. This is on the order of weeks of work, not hours or sessions.

**Path C' (creative / speculative).** Investigate whether Earth-matter anisotropies at the geologically-plausible scale (mantle-crust boundary, stratified deposits, etc.) could contribute a non-zero H_g component to ⟨Φ_bg ⊗ Φ_bg⟩. Would require coupling GCT phason model to specific geological datasets.

Recommendation: **Path A'** is the honest scientific update. Paths B' and C' can be pursued separately but should not block the manuscript correction.

## 4.8 Step 4 Summary

| Statement | Tier |
|---|---|
| Mass-basis-diagonal V_matter does not shift mixing angles | 1 (basis-commutativity theorem) |
| Harmonic-dependent λ₄(n_α) is mass-basis-diagonal | 1 (corollary of Step 3 A_g→A_g theorem) |
| Therefore harmonic-dependent λ₄ does not shift θ₂₃ | 1 |
| All I_h-symmetric phason-strain corrections are mass-basis-diagonal | 1 |
| Step 3 §3.7 scorecard corrected: harmonic-dependent λ₄ is NOT a rescue | 1 |
| Only anisotropic matter (Tier 3) or direct CC coupling (unworked) remain | — |

---

**End of Step 4.** Two scorecard channels closed. The 45° prediction faces increased falsification pressure.
