### **Appendix GRF: GCT-Native Renormalization Group Flow**

> **Status:** Candidate native flow for the Open Research Debt flagged in V3 Ch22 §22.8. The $\beta$-function *shape* for U(1)$_Y$ and SU(2)$_L$ follows from a Tier 3 icosahedral $I_h$ irrep-activation ansatz whose activation schedule and sign assignments are Tier 3 model inputs (no continuous shape parameter is fitted); absolute magnitudes use three calibrated normalisations $\{Z_1, Z_2, Z_3\}$, and the $\sin^2\theta_W(M_Z)$ run from the H-EW boundary uses the imported A2 benchmark $\alpha_2^{-1}(M_{\rm GUT})\approx24$-$25$ (the MSSM unified coupling; §GRF.4.3) and lands 26.7% low. A pre-registered audit with Standard-Model β-functions (§GRF.4.3) records the gauge-running check from the declared inputs as **FAILED**. SU(3)$_C$ running remains Tier 3, deferred to QLQCD-2 (App QLA.7). Numerical verification: `GCT_Physics_Engine/src/protocol_rge_native.py`.

---

## GRF.1 Background — Why SM RGEs Work, What GCT Needs to Replace

The Standard Model gauge couplings $\{g_1, g_2, g_3\}$ run with energy scale $\mu$ according to the Renormalization Group Equations (RGEs):

$$\frac{d\,\alpha_i^{-1}}{d t} \;=\; -\frac{b_i(\mu)}{2\pi}, \qquad t \equiv \ln(\mu/M_Z),$$

with one-loop coefficients (full SM content above the top threshold):
$$b_1 = +\tfrac{41}{6},\qquad b_2 = -\tfrac{19}{6},\qquad b_3 = -7.$$

In SM, these rationals arise from the **virtual-particle loop content** — fermion and gauge-boson loops at each mass threshold. The coefficients themselves are derived from the particle Lagrangian, gauge-group Casimir invariants $C_2(G_i)$, and the multiplicity $T_R$ of each representation. The one-loop equations above provide the transparent comparator used here; precision phenomenology additionally requires a declared renormalisation scheme, threshold matching and higher-loop terms. Direct coupling measurements (LEP/SLD, Tevatron, LHC) reach only the TeV scale; running toward $M_{\rm GUT}$ is an extrapolation of the SM equations, not a measured flow.

For Chapter 4 of Volume 3 (Electroweak Unification), Standard-Model running uses the measured value $\sin^2\theta_W(M_Z)=0.23122\pm0.00006$ (PDG 2026 $\overline{\rm MS}$ $\hat s^2_Z(M_Z)$, EW review Table 10.2; the effective leptonic angle 0.23154 is a different quantity) only as a comparison target or as part of the low-energy coupling normalization. The raw Galois-frame ratio $\rho_{\rm raw}=\phi^{-2}$ (normalized share $0.27639$) is a coordinate identity, and the bare boundary $\phi^{-3}$ is the Tier 3 hypothesis H-EW (V3 Ch04 §4.1–§4.3). Importing SM RGE coefficients to flow such a boundary down to $M_Z$ is flagged in V3 Ch22 §22.8 as **Open Research Debt**, because it imports machinery (virtual-particle loop counting) that does not belong to the GCT substrate ontology. GCT's substrate is the supersolid icosahedral quasicrystal; there are no virtual particles, only phason hydrodynamics and topological defects.

The open target motivating this appendix (which supplies only a Tier 3 activation ansatz toward it) is therefore: **derive the $b_i$-coefficients and the flow shape from the GCT substrate alone — phonon/phason stiffness, icosahedral group invariants, canonical cut-and-project projector shares — without importing virtual-particle loop content.**

The native phason-RGE flow (`GCT_Physics_Engine/src/protocol_rge_native.py`) is a calibrated Tier 3 ansatz. Its three normalisations $Z_i$ are chosen so that the saturated coefficients equal the Standard-Model one-loop coefficients, so it does not predict their magnitudes, and its activation schedule and sign assignments are Tier 3 model inputs. The imported A2 benchmark $\alpha_2^{-1}(M_{\rm GUT}) = 24.0$ is not an endpoint calibration for this kernel; from the H-EW boundary the kernel lands 26.7% below the Z-pole value (V3 Ch04 §4.5.1). The pre-registered gauge-running check from the H-EW boundary is FAILED (§GRF.4.3). Deriving the normalisation constants, the activation schedule and A2 from a normalized action remains the open target.

---

## GRF.2 The Hydrodynamic-Relaxation-Tensor Formulation

### GRF.2.1 The substrate ingredients (tiers as stated per item)

Three families of invariants drive the construction. Each is established elsewhere in the manuscript and is reproduced verbatim here for reference:

**(i) Phonon/phason stiffness ratio** (App DPS.4) [Tier 3 physical-link input pending O.15(b); Parameter Ledger §0.1 P3]:
$$\frac{K_\perp}{K_\parallel} \;=\; \phi^{-18} \;\approx\; 1.731 \times 10^{-4}.$$

**(ii) Cut-and-project projector weights** (V3 Ch04 §4.1) [Tier 1]:
$$\|\Pi_\parallel \mathbf{E}_i\|^2 = \|\Pi_\perp \mathbf{E}_i\|^2 = \tfrac{1}{2} \quad \text{(canonical row-isometric projectors)},$$ while the declared raw Galois frames give the coordinate-dependent ratio $\rho_{\rm raw} = \phi^{-2}$, which is not a physical sector weight.

**(iii) Icosahedral irrep content of $I_h$** (group theory). The full icosahedral point group $I_h$ has 10 inequivalent irreducible representations:

| Irrep | $d_\rho$ | Parity | Role / transformation content |
|-------|---------|--------|-------------|
| $A_g$ | 1 | $+$ | vacuum scalar |
| $T_{1g}$ | 3 | $+$ | axial vector (pseudovector; rotation generators) |
| $T_{2g}$ | 3 | $+$ | Galois-conjugate partner of $T_{1g}$ (not a vector) |
| $G_g$ | 4 | $+$ | mixed quadruplet |
| $H_g$ | 5 | $+$ | quadrupolar tensor |
| $A_u$ | 1 | $-$ | pseudoscalar |
| $T_{1u}$ | 3 | $-$ | polar vector ($E_\parallel$; phonon displacement) |
| $T_{2u}$ | 3 | $-$ | Galois-conjugate polar triplet ($E_\perp$; phason displacement) |
| $G_u$ | 4 | $-$ | mixed quadruplet |
| $H_u$ | 5 | $-$ | quadrupolar tensor |

Burnside identity: $\sum_\rho d_\rho^2 = 120 = |I_h|$, with the dimension sums split as $16+16$ between the gerade and ungerade towers and the $d^2$ contributions split as $60+60$ [Tier 1 group theory]. The earlier identification of $16+16=32$ with "32 vertex stars" of the AKN tiling is retired: the equality is only the parity-split sum of irrep dimensions. Vertex-star counts depend on the enumeration convention — 24 (historical count, App CXL §CXL.3), 9 (bare edge-incidence stars, App QLA §QLA.3) and 101 (radius-two decorated stars, App QLA §QLA.3) — and none of them is 32.

### GRF.2.2 The activation schedule (Tier 3 ansatz)

In a hydrodynamic picture, the contribution of phason mode $\rho$ to the running of a gauge coupling at scale $\mu$ is governed by whether the probe wavelength $\lambda = \hbar c/\mu$ can resolve mode $\rho$. The natural geometric scaling is:

$$t_\rho \;=\; T_\text{GUT}\cdot \frac{d_\rho}{d_\text{max}}, \qquad d_\text{max} = 5,$$

where $t_\rho$ is the resolution depth (in units of $\ln \mu/M_Z$) at which irrep $\rho$ activates. Ansatz reading: irreps of larger representation dimension are taken to require a deeper probe to be resolved. Representation dimension does not by itself derive a physical threshold, and no substrate action currently yields this map; the choice $d_\text{max} = 5$ (the largest irrep dimension) places the upper edge of the activation tower at $M_\text{GUT}$ by construction.

The schedule is monotonic: $A_g$ ($d=1$) activates first (at $t = T_\text{GUT}/5 \approx 6.7$), $T$-irreps ($d=3$) activate at $t = 3T_\text{GUT}/5 \approx 20.1$, $G$-irreps ($d=4$) at $t = 4T_\text{GUT}/5 \approx 26.8$, $H$-irreps ($d=5$) at $t = T_\text{GUT} \approx 33.5$.

**Zero-measure $d=5$ defect.** Because the $H_g, H_u$ irreps activate exactly at $t = T_\text{GUT}$, they have an activation interval of measure zero inside $[0, T_\text{GUT}]$ and contribute nothing to the flow from $M_Z$ to $M_\text{GUT}$. They are nevertheless included in the sums used to calibrate the saturated $Z_i$ (§GRF.3.1), and a numerical integrator that samples the step at the endpoint can give them a step-size-dependent contribution. That leakage is a quadrature artefact, not substrate physics; a revised schedule must remove the defect.

At $t \le 0$ (the regime $\mu \le M_Z$), only the $d=1$ irreps are taken to contribute. This special IR convention is also a model input (the ansatz's stand-in for "all SM fields are above threshold at $M_Z$").

### GRF.2.3 The gauge-sector coupling weights (Tier 1 projector shares; Tier 3 sector assignment)

Each gauge sector $G_i \in \{U(1)_Y, SU(2)_L, SU(3)_C\}$ couples to a specific subset of phason irreps weighted by a canonical projector share or by the icosahedral axis count:

- **$U(1)_Y$:** couples to all irreps (gerade or ungerade) through the perpendicular projection: $w_1(\rho) = \|\Pi_\perp \mathbf{E}_i\|^2 = 1/2$ for every $\rho$. Ansatz reading: the hypercharge field is taken to couple to every phason mode.
- **$SU(2)_L$:** couples only to the $T_1$ pair $T_{1g}$ (axial vector) and $T_{1u}$ (polar vector) — the two $I_h$ irreps that restrict to the $\ell=1$ (spin-1) irrep $T_1$ of the rotation subgroup $I$ — with the parallel projector share: $w_2(\rho) = \|\Pi_\parallel \mathbf{E}_i\|^2 = 1/2$ for $\rho \in \{T_{1g}, T_{1u}\}$, zero otherwise. Ansatz reading: the weak-isospin field is taken to couple to the vector sector only (cf. the strain-level phonon–phason coupling $C^{mix}_{ijkl}$ of App SNE §SNE.4(ii)).
- **$SU(3)_C$:** couples to all irreps via the 10 three-fold rotation axes of the rhombic triacontahedron: $w_3(\rho) = 10/120$. Ansatz reading: the exact count of 10 three-fold axes (V3 Ch04 §4.5.5), divided by the group order $|I_h| = 120$, is converted into a colour-sector weight; that conversion is an ansatz.

### GRF.2.4 Sign assignments (Tier 3 model inputs)

The sign of each $b_i$ — whether the coupling screens (Landau pole in the UV) or anti-screens (asymptotic freedom) — is assigned from the parity of the dominant irrep coupling to each sector; these assignments are Tier 3 model inputs, not derivations. Parity alone does not force screening for U(1) or anti-screening for SU(2)/SU(3), and no action-level calculation currently fixes these signs; the readings below are motivating narratives only:

- $\text{sign}(b_1) = +1$ (screening): U(1) couples to the gerade-dominant phason content; gerade modes redshift the coupling at high energy (positive $\beta$).
- $\text{sign}(b_2) = -1$ (anti-screening): SU(2) couples only to vector irreps $T_{1g}, T_{1u}$; the ungerade $T_{1u}$ component dominates the loop contribution and gives asymptotic freedom.
- $\text{sign}(b_3) = -1$ (anti-screening): SU(3) couples to the three-fold axis structure; the sign is assigned negative by analogy with non-Abelian gauge boson loops in the SM (a Tier 3 model choice).

---

## GRF.3 The β-Function Construction per Coupling (Tier 3 ansatz)

### GRF.3.1 The native β-function

$$b_i^\text{GCT}(t) \;=\; (\text{sign}_i)\cdot Z_i \cdot \sum_{\rho \,:\, t \ge t_\rho} d_\rho^2 \cdot w_i(\rho).$$

The summation is over all icosahedral irreps active at resolution depth $t$. Three remarks:

1. **The sum is finite.** Once $t \ge T_\text{GUT}$ all 10 irreps are active and $b_i^\text{GCT}$ saturates at a constant value. Within the ansatz this plays the role of "no further SM fields above $M_\text{GUT}$".
2. **The shape is fixed by the disclosed sector choices.** Given the icosahedral group, the projector shares, and the sector coupling assignments above, $b_i^\text{GCT}(t)/Z_i$ is a definite step function within that accounting. Those choices are Tier 3 inputs, so the mathematical definiteness of the curve does not make it a Tier 2 physical derivation.
3. **The $Z_i$ normalise the magnitude.** They play the same role for the gauge-sector β-coefficient magnitudes that $m_e$ plays for the lepton sector (one anchor per independent sector). We fix $Z_i$ by demanding $b_i^\text{GCT}(T_\text{GUT}) = b_i^\text{SM}(\text{full content})$:

$$Z_1 = \frac{41/6}{\sum_\rho d_\rho^2 \cdot w_1} = \frac{41/6}{120 \cdot (1/2)} = \frac{41}{360} \approx 0.1139,$$
$$Z_2 = \frac{19/6}{\sum_{\rho \in \{T_{1g},T_{1u}\}} d_\rho^2 \cdot w_2} = \frac{19/6}{18 \cdot (1/2)} = \frac{19}{54} \approx 0.3519,$$
$$Z_3 = \frac{7}{\sum_\rho d_\rho^2 \cdot (10/120)} = \frac{7}{120 \cdot (10/120)} = \frac{7}{10} = 0.7.$$

The canonical projector shares $w_1 = w_2 = 1/2$ are used because they are the row-rescaling-invariant projector shares (V3 Ch04 §4.1.1; their use as sector weights is the Tier 3 assignment of §GRF.2.3); the raw-frame values $(1+\phi^{\pm2})/5$ change under row rescaling. Only the products $Z_i w_i$ enter the flow, so the saturated coefficients below do not depend on this choice. For the same reason, a common change in a sector weight is absorbed by its $Z_i$, and the calibrated saturation values cannot validate the projector weights or the gauge embedding. The denominators above include the $d=5$ irreps, which have zero activation measure below $T_\text{GUT}$ (§GRF.2.2).

**Scope reading of $Z_3 = 7/10$ [Tier 3 calibration, NOT closed-form derivation; as shown in App TPR §TP-A].** The ratio $7/10$ is *not* a closed-form prediction from substrate alone — it is a calibration. The denominator (10) is a genuine substrate count (the number of three-fold rotation axes of the rhombic triacontahedron, Tier 1 via V3 Ch03 §3.1.2); its use as the SU(3) sector weight is the Tier 3 assignment of §GRF.2.3. The numerator (7), however, is *imported* from the SM target $|b_3^{\rm SM}({\rm full})| = 7$ — itself the result of the SM virtual-particle loop sum $-(11/3) C_2(\mathfrak{su}_3) + (4/3) n_f T_R = -11 + 4 = -7$. The factor 7 has no GCT-native origin in icosahedral group theory: it is not a divisor of $|I_h|=120$, not a Coxeter degree of $H_3 \in \{2,6,10\}$ or $H_4 \in \{2,12,20,30\}$, not an irrep dimension or vertex/face/edge count of the RT. The "7/10" form is therefore the *consequence* of the matching condition $b_3^{\rm GCT}(T_{\rm GUT}) = b_3^{\rm SM}({\rm full}) = -7$, not an independent prediction.

The reading of $Z_3 = 7/10$ as a QLQCD derivation target remains a research route (§GRF.5.3; a target-blind derivation would be testable, §GRF.6) — but the tier label on this calibration is **Tier 3 (anchor)**, not Tier 2. A genuine first-principles derivation of $Z_3$ requires the QLQCD-2 path of App QLA.7: computing the phason loop contribution to $\alpha_s$ running directly, without using SM coefficients as inputs. Until that work lands, $Z_3$ remains on the same Tier-3 footing as $Z_1$ and $Z_2$ in this appendix.

### GRF.3.2 Verification at saturation

At $t = T_\text{GUT}$ (full activation), the calculation produces:

| Sector | $b_i^\text{GCT}(T_\text{GUT})$ | $b_i^\text{SM}(\text{full})$ | Match |
|--------|-------------------------------|------------------------------|-------|
| U(1)$_Y$ | $+6.833$ | $+41/6 = +6.833$ | exact (by $Z_1$ construction) |
| SU(2)$_L$ | $-3.167$ | $-19/6 = -3.167$ | exact (by $Z_2$ construction) |
| SU(3)$_C$ | $-7.000$ | $-7.000$ | exact (by $Z_3$ construction) |

At $t = 0$ (only $d=1$ irreps active):

| Sector | $b_i^\text{GCT}(0)$ | $b_i^\text{SM}(M_Z)$ | Comment |
|--------|---------------------|----------------------|---------|
| U(1)$_Y$ | $+0.114$ | $\approx +5.9$ (top decoupled; $+41/6$ with full content) | GCT activation slower than SM mass thresholds |
| SU(2)$_L$ | $-0.000$ | $\sim -3.0$ | GCT: no vector irreps active below $M_Z$ |
| SU(3)$_C$ | $-0.117$ | $-23/3 \approx -7.67$ (5 flavours) | GCT: only the $d=1$ irreps contribute, so SU(3) running below $M_Z$ is almost absent ($\lvert b_3\rvert\approx0.12$) |

The IR-side discrepancy is a known limitation of the Tier 3 activation ansatz, not evidence for it: the icosahedral irrep activation schedule has *one* dimensional gradient (set by $d_\rho/d_\text{max}$) rather than the *multiple* mass thresholds of SM particle content. It marks the difference between the ansatz flow and a particle-counting flow.

---

## GRF.4 Numerical Comparison with PDG Running Data

Running the GCT-native flow against PDG benchmarks (see `protocol_rge_native.py` for the full numerical analysis):

| Quantity | GCT-native | SM 1-loop | PDG observed | $\|\Delta\|_\text{GCT-PDG}$ |
|----------|-----------|-----------|--------------|------------------------------|
| $\alpha^{-1}(M_Z)$ (from $M_e$) | $136.82$ | $126.69$ | $127.94$ | $6.9\%$ |
| $\sin^2\theta_W(M_Z)$ (from $M_\text{GUT}$, Tier 3 BC $= \phi^{-3}$) | $0.170$ | $0.059$ † | $0.231$ | $26.7\%$ |
| $\alpha_s(M_Z)$ (from $M_\text{GUT}$, BC $= (10\phi^2)^{-1}$) | $0.052$ | — | $0.118$ | $55.9\%$ |

† Both columns use the disclosed Parameter Ledger A2 UV endpoint anchor $\alpha_2^{-1}(M_\text{GUT}) \approx 24$-$25$ and the Tier 3 H-EW boundary. Both outputs land **low**: the GCT-native kernel by 26.7% and this A2-conditioned full-content SM one-loop run by 74.6% (0.0587 vs 0.23122; comparison only, not fitted to the measured endpoint). This A2-conditioned run is distinct from the canonical one-coupling-conditioned SM comparator of V3 Ch04 §4.3.3, which gives 0.1367 (40.87% low). Misses of this size are not loop-order effects; they show that this boundary/A2 combination does not reproduce the Z-pole value under either kernel. The pre-registered audit of §GRF.4.3 confirms this at two loops and with thresholds (best case 0.0673, −52σ) and records the check as **FAILED**.

**Precision assessment:**

- For $\alpha(\mu)$: the GCT ansatz output $\alpha^{-1}(M_Z) = 136.8168$ sits between the unrun CODATA A3 value 137.035999177 and the PDG value 127.94, but it recovers only $(137.0360 - 136.8168)/(137.0360 - 127.94) \approx 2.4\%$ of the running, leaving a signed residual of $+6.94\%$ against 127.94 [Tier 3 calibrated/postdictive flow]. This is far worse than the SM one-loop comparator ($126.69$, $-0.98\%$). The discrepancy is dominated by the IR end of the flow ($M_e \to M_Z$), where the GCT irrep activation schedule has only $d=1$ irreps active, while in the SM the three charged leptons and the five lighter quark flavours contribute.

- For $\sin^2\theta_W$: from the Tier 3 H-EW boundary $\phi^{-3}$ the native kernel lands $26.7\%$ low. The imported A2 value is not an endpoint calibration for this kernel: reproducing the measured $\alpha_2(M_Z)$ would require $\alpha_2^{-1}(M_\text{GUT}) \approx 36.3$, and no single A2 lets H-EW and this kernel match both low-energy couplings. Re-anchoring to the PDG endpoint would be the "fit the IR" move that V3 Ch22 §22.8 flags as Tier-3 import. A2 remains listed in Parameter Ledger §0.1 as a calibrated gauge-flow anchor, not hidden inside the protocol. A2 is the MSSM unified coupling, not a Standard-Model value, and together with H-EW it is inconsistent with any matter content containing the Standard Model (no-go of §GRF.4.3); whether to retire it is an open v1.4.0 decision.

- For $\alpha_s$: the GCT-native flow does **not** recover the PDG value; it lands $55.9\%$ low (V3 Ch04 §4.5.5), i.e. $\alpha_s(M_Z)\approx0.052$ is too weak. Over the 33.5 e-folds the native kernel lowers $\alpha_s^{-1}$ by only about 7, so reaching $\alpha_s(M_Z)=0.118$ would need $\alpha_s^{-1}(M_\text{GUT})\approx15$–16: the bare handle $10\phi^2 \approx 26.18$ is too *large* for this kernel. Under SM one-loop running ($b_3=-7$) the required value is $\approx46$; starting from 26.18, $\alpha_3^{-1}$ reaches zero at $2$–$6\times10^6$ GeV (1-loop to 2-loop, §GRF.4.3), far above $M_Z$, so $\alpha_s(M_Z)$ is undefined (non-perturbative) from the declared handle under SM running. The handle therefore fails in opposite directions under the two kernels; QLQCD-2 (App QLA.7) would have to derive both the handle and the running.

### GRF.4.1 What the GCT-native ansatz encodes

The following features of the ansatz are listed with their status:

1. **The sign hierarchy** $b_1 > 0 > b_2 > b_3$ follows from the Tier 3 sign assignments of §GRF.2.4; it is built into the ansatz rather than derived.
2. **The numerical ordering** $|b_3| > |b_1| > |b_2|$ at saturation is imposed by the $Z_i$ calibration to the Standard-Model coefficients.
3. **The Weinberg-angle UV boundary data** separate the Tier 1 raw-frame coordinate ratio $\rho_{\rm raw}=\phi^{-2}$ (not a physical invariant) from the Tier 3 gauge-kinetic hypothesis $\sin^2\theta_W^{\rm bare}=\phi^{-3}$ (H-EW; V3 Ch04 §4.3).
4. **The bare strong-coupling handle** $\alpha_s^{-1}(\text{bare}) = 10\phi^2$ is Tier 3: the 10 integer and $\phi^2$ factor are geometrically traced, but the product rule and native strong-sector closure remain O.42 / QLQCD-2 work (V3 Ch04 §4.5.5).
5. **The flow saturates above $M_\text{GUT}$** because the icosahedral irrep tower is finite — see §GRF.4.2.

### GRF.4.2 The UV fixed-point question — comparison with Asymptotic Safety

Asymptotic Safety (Weinberg 1976, Reuter 1998) proposes a non-Gaussian UV fixed point: couplings $g_i^* \ne 0$ at which the beta functions vanish, $\beta_i(g^*) = 0$, and which the dimensionless couplings approach as $\mu \to \infty$. The calibrated GCT-native ansatz behaves differently:

- For $t > T_\text{GUT}$: all 10 irreps are already active, so $b_i^\text{GCT}(t) = b_i^\text{GCT}(T_\text{GUT}) = \text{const} \ne 0$. Constant nonzero $b_i$ continue to run the inverse couplings linearly in $t$; this is **not** a fixed point, Gaussian or non-Gaussian.
- The saturation is a mathematical consequence of the finite $I_h$ irrep list ($\sum d_\rho^2 = 120$) plus the chosen activation rule. It does not by itself establish a combinatorial UV cutoff or a UV completion.
- A possible physical reading (Tier 3, conditional on the $M_\text{GUT}$ scale assignment and O.15): above $M_\text{GUT}$ the probe wavelength would approach the lattice scale and a continuum flow would cease to apply, with discrete lattice physics (App QLA) taking over. No discrete-substrate UV theory has been constructed to support this reading.

The ansatz therefore neither predicts nor excludes a Weinberg-Reuter fixed point; the stronger claim that the substrate itself is the UV completion requires an action-level derivation beyond this appendix.

### GRF.4.3 Pre-registered SM-kernel audit and no-go

A pre-registered gauge-running audit ran the declared ultraviolet data $\{A2=24$–$25,\ \sin^2\theta_W(M_{\rm GUT})=\phi^{-3}\ (\text{H-EW}),\ \alpha_3^{-1}(M_{\rm GUT})=10\phi^2,\ M_{\rm GUT}=M_{\rm red}\phi^{-9}=3.2\times10^{16}\,{\rm GeV}\}$ down to $M_Z$ with Standard-Model β-functions and with the native kernel of §GRF.3, and found that no declared-input configuration reproduces the low-energy gauge couplings. The numbers below are standard Standard-Model running (imported Tier 1 machinery) evaluated on the declared inputs. The comparators were fixed before any script existed: $\hat s^2_Z=0.23122\pm0.00006$ (PDG 2026 $\overline{\rm MS}$, EW review Table 10.2), $\alpha_s(M_Z)=0.1180\pm0.0009$ (PDG 2026 QCD review) and $\hat\alpha^{(5)}(M_Z)^{-1}=127.930\pm0.008$ (PDG 2024). Pulls use $\sqrt{\sigma_{\rm exp}^2+\sigma_{\rm th}^2}$, where, as pre-registered, $\sigma_{\rm th}$ is the declared theory uncertainty or the spread across the SM kernels, whichever is larger. A separately written blind re-implementation agreed on all 25 compared numbers.

**Top-down runs (declared inputs at $M_{\rm GUT}$ → $M_Z$).**

| Route | $\sin^2\theta_W(M_Z)$ | $\alpha_{em}^{-1}(M_Z)$ | $\alpha_s(M_Z)$ |
|---|---|---|---|
| SM 1-loop, A2 = 24 / 25 | 0.0587 / 0.0647 | 121.21 / 125.45 | undefined: $\alpha_3^{-1}\to0$ at $2.0\times10^6$ GeV |
| SM 1-loop, top decoupled, A2 = 24 / 25 | 0.0584 / 0.0644 | 121.06 / 125.30 | undefined (same) |
| SM 2-loop\*, A2 = 24 / 25 | 0.0615 / 0.0673 | 122.02 / 126.24 | undefined: $\alpha_3^{-1}\to0$ at $\approx6\times10^6$ GeV |
| native kernel (A4–A6), A2 = 24 | 0.16957 (−62σ) | 101.71 (−261σ) | 0.05204 (−30σ) |

\* The 2-loop top-down run is defined only with the measured $\alpha_s$ inside its 2-loop terms, because $\alpha_3$ blows up above $M_Z$. The $\alpha_{em}^{-1}$ column is the top-down value from the H-EW/A2 boundary; it is a different route from the $M_e\to M_Z$ entry of the §GRF.4 table.

The best case for $\sin^2\theta_W(M_Z)$ is 0.0673 (2-loop, A2 = 25), **−52σ** against 0.23122. With SM β-functions $\alpha_3^{-1}$ reaches zero at $2$–$6\times10^6$ GeV, so **$\alpha_s(M_Z)$ is undefined (non-perturbative)** from the declared handle; the native kernel gives 0.05204 (−30σ).

**Bottom-up run (2-loop, PDG values → $M_{\rm GUT}$).** $\alpha_Y^{-1}=61.57$, $\alpha_2^{-1}=46.18$, $\alpha_3^{-1}=46.25$ and $\sin^2\theta_W(M_{\rm GUT})=0.4286$, against the declared $\alpha_2^{-1}=24$–25, $\sin^2\theta_W=\phi^{-3}=0.2361$ and $\alpha_3^{-1}=26.18$. The running $\sin^2\theta_W$ equals $\phi^{-3}$ only at **243 GeV**; placing H-EW at 243 GeV would be endpoint fitting.

**The miss is not an artefact.** The audit checked the usual suspects one by one:
- *Code:* all four engine numbers (native 0.16957, SM same-A2 0.0587, the conditioned 0.136725 of V3 Ch04 §4.3.3, native $\alpha_s$ 0.05204) were reproduced; there is no code bug in the engine.
- *Normalisation (D2):* the engine is internally consistent in physical hypercharge ($b_Y=41/6$). Reading H-EW in SU(5) normalisation makes the miss worse ($\sin^2\theta_W(M_Z)=0.040$), and no declared GCT embedding supplies the factor 5/3.
- *Loop order (D3):* going from one to two loops shifts $\sin^2\theta_W(M_Z)$ by +0.0027, about 2% of the miss.
- *Thresholds (D4):* decoupling the top shifts it by at most 0.0004.
- *Comparator (D5):* the verdict is the same (−52σ) with the superseded PDG 2024 value 0.23129.

**No-go [Tier 1 arithmetic with the imported SM β-functions; exact at one loop, checked at two].** Any matter content that contains the Standard Model has $b_Y\ge41/6$, so $\alpha_Y^{-1}(M_{\rm GUT})\le61.6$. With A2 = 24–25 this forces $\sin^2\theta_W(M_{\rm GUT})\ge0.280$–$0.288$, above $\phi^{-3}=0.236$: **A2 and H-EW cannot both hold for any SM extension.** For the native kernel the declared sign $b_2\le0$ (§GRF.2.4) forces $\alpha_2^{-1}(M_Z)\le A2\le25$, against 29.58 measured, for every $Z_2$ and every activation schedule.

**A2 provenance.** A2, $\alpha_2^{-1}(M_{\rm GUT})\approx24$–25, is the **MSSM** unified coupling: Langacker & Polonsky, Phys. Rev. D 47, 4028 (1993), give $\alpha_G^{-1}\approx23$–24.5 at $M_G\approx2.5\times10^{16}$ GeV for the MSSM, and in the Standard Model the couplings do not unify. With SM running $\alpha_2^{-1}(3.2\times10^{16}\,{\rm GeV})=46.2$ at two loops ($\approx46.5$ at one loop). A2 is therefore not a Standard-Model-equivalent benchmark. The strong handle $10\phi^2=26.18$ also sits in the MSSM range (SM: $\alpha_3^{-1}(M_{\rm GUT})=46.2$).

**The $\alpha_{em}$ borderline is not counted.** An $\alpha_{em}^{-1}(M_Z)$ value of 126.24 (−1.8σ) appears only in the 2-loop run that imports the measured $\alpha_s$, at the edge of the A2 range (matching needs A2 = 25.4), and only as a compensating sum: $\alpha_{em}^{-1}=\alpha_Y^{-1}+\alpha_2^{-1}$ with $\alpha_2^{-1}=8.5$ (measured 29.6) and $\alpha_Y^{-1}=117.7$ (measured 98.4). With declared-input kernels only, the best case is 125.45, at −17σ. The value is flagged and **not counted**; this judgement was made after the result was seen and is recorded as such.

**What a repair would need (described, not adopted).** Dropping A2 while keeping H-EW at $M_{\rm GUT}$ and $10\phi^2$ would require, with hypercharge held at its SM running, $\alpha_2^{-1}(M_{\rm GUT})\le19.0$ and an average $b_3\approx-3.3$: roughly four hypercharge-neutral SU(2)-triplet and two colour-octet Weyl fermions near the weak scale, with no new hypercharged matter. This appendix, V3 Ch04 and the Parameter Ledger derive no such states, and choosing their number and mass to hit two numbers would be a fit.

**Status: FAILED check.** "**FAILED check**: no declared-input configuration reproduces $\sin^2\theta_W(M_Z)$, $\alpha_s(M_Z)$ or $\alpha_{em}(M_Z)$ (one borderline two-loop $\alpha_{\rm em}$ value, which imports the measured $\alpha_s$, is excluded by a post hoc judgement; App GRF §GRF.4.3)." H-EW remains a Tier 3 hypothesis at an unspecified scale; the audit tests the declared combination (H-EW at $M_{\rm GUT}$ with A2, $10\phi^2$ and the stated kernels), not every possible placement of the boundary. Whether to retire A2 and A4–A6 ($Z_1$–$Z_3$) is an open v1.4.0 decision: (i) keep all inputs and record the check as FAILED; (ii) retire A2 for its MSSM provenance and its contradiction with H-EW; (iii) also retire A4–A6, which restate the SM one-loop coefficients, and use the SM β-functions as imported Tier 1 machinery, at the cost of the native-RGE scope. v1.3.0 retires nothing and keeps the counts (11 declared core inputs; 24 numbered Ledger inputs).

---

## GRF.5 Open Issues

### GRF.5.1 QLQCD ab-initio derivation of $\{Z_1, Z_2, Z_3\}$ and A2

The three icosahedral normalisations are currently anchored to SM full-content values via construction, and the endpoint check imports A2, $\alpha_2^{-1}(M_{\rm GUT})\approx24$-$25$, the MSSM unified coupling (Langacker & Polonsky 1993; §GRF.4.3); SM running from $M_Z$ gives $\alpha_2^{-1}(3.2\times10^{16}\,{\rm GeV})=46.2$ at two loops ($\approx46.5$ at one loop) instead. With H-EW at $M_{\rm GUT}$, A2 is inconsistent with any SM extension (§GRF.4.3), so an ab-initio A2 that reproduced 24–25 would not rescue the running check; whether to retire A2 and A4–A6 is an open v1.4.0 decision. A full Tier-2 derivation would compute these quantities ab initio from:

- $Z_1$: spectral-action expansion (App GPE) restricted to the U(1) sector with the icosahedral Dirac operator.
- $Z_2$: phonon–phason coupling tensor $C_{ijkl}^\text{mix}$ (App SNE §SNE.4(ii)) evaluated on the vector sector.
- $Z_3$: QLQCD-2 non-perturbative confinement computation (App QLA.7). $Z_3 = 7/10$ is a calibration using the SM target $|b_3^{\rm SM}| = 7$ as the numerator; first-principles closure requires computing the GCT phason-loop contribution to $\alpha_s$ running directly — that is the QLQCD-2 task (App QLA.7).
- A2: the SU(2) boundary value from the icosahedral irrep activation schedule and a normalized gauge-kinetic action that decides the bare boundary, without tuning to $\sin^2\theta_W(M_Z)$.

Each of these is a discrete open research target with its own difficulty class. $Z_3$ is the highest priority because it also closes the bare $\alpha_s$ magnitude gap.

### GRF.5.2 The IR-side activation schedule

The icosahedral activation schedule has only $d=1$ irreps active for $t \le 0$ (the regime $\mu \le M_Z$), which produces a much shallower running than SM in the low-energy regime. A revised schedule must remove the $d=5$ zero-measure defect (§GRF.2.2), state how the special $t \le 0$ convention arises and specify physical threshold matching. Incorporating the **mass thresholds of the lepton sector** as additional activation depths is one possible extension, but it would be another model choice unless the mapping from particle thresholds to irreps is derived independently.

### GRF.5.3 SU(3) strong-coupling closure

The bare Tier 3 handle $\alpha_s^{-1}(\text{GUT}) = 10\phi^2 \approx 26.18$ does not recover the PDG endpoint: it is too large for the native kernel (which would need $\approx15$–16) and too small for SM one-loop running (which would need $\approx46$; §GRF.4). Two routes are open:

- **QLQCD-2 confinement corrections** (App QLA.7): non-perturbative phason-axis interactions on the AKN lattice may change the bare value and the running. For the native kernel the bare inverse coupling would have to move down; an upward shift would worsen the native miss. Highest priority because it would simultaneously close the bare-magnitude gap and the running.
- **Multi-axis topological gluing** of three-fold and five-fold axes (a speculative route not yet developed in any chapter): the discrete topology of the icosahedral lattice may contribute an additional $\beta$-shift not captured by the irrep-counting decomposition used in §GRF.3.

### GRF.5.4 Two-loop and Yukawa back-reaction

The GCT-native β-function as constructed here is a 1-loop ansatz. The Standard-Model comparator of V3 Ch04 §4.3.3 uses one-loop full-content coefficients and does not reproduce the Z pole from the H-EW boundary either; the pre-registered audit of §GRF.4.3 shows that the SM two-loop terms shift $\sin^2\theta_W(M_Z)$ by only +0.0027. The GCT 1-loop construction does not include 2-loop phason-phason interactions or Yukawa back-reaction; these may eventually define higher-order corrections (cf. the phonon–phason coupling $C^{mix}_{ijkl}$ of App SNE §SNE.4(ii) at second order), but they are not a precision refinement of an already successful one-loop result and cannot by themselves supply the missing gauge-kinetic normalization. The 26.7% and 40.87% electroweak residuals, the target-calibrated $Z_i$ and the activation defect must be resolved first.

---

## GRF.6 Summary

| Coupling | Shape (Tier) | Magnitude (Tier) | Open work |
|----------|-------------|------------------|-----------|
| $\alpha(\mu)$ | Tier 3 (irrep-activation ansatz) | Tier 3 (anchor $Z_1$) | Spectral $Z_1$ derivation |
| $\sin^2\theta_W(\mu)$ | Tier 3 (irrep-activation ansatz) | Tier 3 (anchors $Z_2$ + imported A2 benchmark $\alpha_2^{-1}(M_{\rm GUT})$); 26.7% low from the H-EW boundary; running check **FAILED** (§GRF.4.3) | Phason-phonon $Z_2$ derivation + A2 boundary derivation + gauge-kinetic decision on H-EW |
| $\alpha_s(\mu)$ bare | **Tier 3 calibrated handle** ($10\phi^2$, V3 Ch04 §4.5.5; see App TPR §TP-C / §TPR.3 — factor trace documented, product closure pending) | Tier 3 (10 integer + $\phi^2$ geometric factor; O.42 / QLQCD-2 pending) | O.42 / QLQCD-2 |
| $\alpha_s(\mu)$ running | Tier 3 ($Z_3$ anchor calibrated against $|b_3^{\rm SM}| = 7$ SM target; first-principles closure at QLQCD-2 per App QLA.7) | Tier 3 (incomplete) | QLQCD-2 (App QLA.7) |

The structural claim of V3 Ch22 §22.8's roadmap is **not closed**: the SM β-function *structure* (signs, sector hierarchy) is modeled by the Tier 3 irrep-activation ansatz with canonical projector shares, and the saturated values are imposed by the $Z_i$ calibration. The remaining work is to derive the three $Z_i$ normalisations, the A2 boundary and the activation schedule ab initio from a normalized action. Until then, the gauge-flow sector retains the three Tier-3 magnitude anchors $Z_1$, $Z_2$ and $Z_3$ plus the A2 endpoint anchor; these are carried as rows A4-A6 and A2 in Parameter Ledger §0.1 rather than counted as a closed prediction from the current postulate set. Whether to retire A2 and A4–A6 after the FAILED running check of §GRF.4.3 is an open v1.4.0 decision; v1.3.0 retires nothing (11 declared core inputs; 24 numbered Ledger inputs).

The full numerical analysis, including the finite-tower UV behaviour discussed in §GRF.4.2, lives in `GCT_Physics_Engine/src/protocol_rge_native.py` and writes its results to `GCT_Physics_Engine/data/protocol_rge_native_results.json`.

**Branch-level falsification status: FAILED check.** The present H-EW + A2 + calibrated-$Z_i$ activation branch fails as an autonomous electroweak flow model: it lands 26.7% below $\sin^2\theta_W(M_Z) = 0.23122$ (−62σ), and the pre-registered audit of §GRF.4.3 shows that Standard-Model β-functions do no better (best case −52σ; $\alpha_s(M_Z)$ undefined) and that A2 and H-EW at $M_{\rm GUT}$ cannot both hold for any SM extension. No declared-input configuration reproduces $\sin^2\theta_W(M_Z)$, $\alpha_s(M_Z)$ or $\alpha_{em}(M_Z)$. H-EW itself remains a Tier 3 hypothesis at an unspecified scale. The $Z_i$ values themselves are not independent falsifiable predictions, because they are definitions tied to the SM targets. A future action-derived calculation (for example a QLQCD-2 derivation of $Z_3$ that does not use $|b_3^{\rm SM}| = 7$) can be tested without those calibrations; disagreement would falsify that proposed native mechanism, while agreement would count as new evidence only if the target values were not used in its construction.
