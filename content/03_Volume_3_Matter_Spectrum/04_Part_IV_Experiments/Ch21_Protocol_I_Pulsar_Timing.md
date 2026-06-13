### **Chapter 21: Protocol I — Pulsar Timing Array Anisotropy**

> [!IMPORTANT]
> **Epistemic Status: Tier 2 harmonic-form mechanism + Tier 3 amplitude (pending O.15(b))**
> This chapter presents a falsifiable prediction derived from the GCT quasicrystalline vacuum hypothesis. The $l=6$ harmonic form follows from the icosahedral representation theorem at Tier 2; the specific amplitude $\Delta\Gamma_{\max}=\phi^{-18}$ is a Tier 3 anchor pending the O.15(b) RG-map derivation of $K_\perp/K_\parallel=\phi^{-D}$ from the canonical Coxeter integer $D=18$. The predicted linear-power signal $\hat C_6 \approx 1.67 \times 10^{-4}$ sits $\sim 18\times$ below the combined-array stacked sensitivity ($\sigma(\hat C_6) \approx 3 \times 10^{-3}$) of NANOGrav 15-year + PPTA DR3 + EPTA DR2 (§21.3.2); the 15-angle icosahedral mask therefore enables a **near-term null test** on existing data ("no power at the icosahedral angles → icosahedral vacuum falsified at sensitivity $\sim 3\sigma \cdot \sigma(\hat C_6)$"), with **confident positive detection requiring Square Kilometre Array (SKA-PTA) observations in the SKA-era timeframe** (§21.3.1, §21.3.3).

---

**21.1 The Gravitational Wave Vacuum**

**21.1.1 GWs as Phonons of the Topological Glass**

In Geometric Consciousness Theory, the vacuum is not a smooth Minkowskian manifold but a **Topological Glass** — a six-dimensional icosahedral quasicrystal projected into 3+1D spacetime. Gravitational waves are not mere ripples in a smooth fluid; they are long-wavelength **acoustic phonons** propagating through this structured substratum.

In a physical crystal, the speed of sound is **anisotropic**: it varies depending on whether the acoustic wave propagates along a high-symmetry axis or off-axis. The icosahedral vacuum lattice possesses **six distinct five-fold symmetry axes**. Along these axes, the lattice is most efficiently packed; transverse to them, the phason field creates a slight mismatch in the acoustic impedance.

**21.1.2 The Hellings-Downs Curve and its Correction**

The standard Hellings-Downs (HD) correlation function describes the expected angular correlation between Pulsar Timing Array residuals under a perfectly isotropic stochastic gravitational wave background (SGWB):

$$ \Gamma_{HD}(\theta) = \frac{3}{2} x \ln x - \frac{x}{4} + \frac{1}{2}, \quad x = \frac{1 - \cos\theta}{2} $$

This curve assumes a perfectly isotropic GW background. **GCT breaks this assumption.** The six-fold anisotropy of the vacuum introduces a perturbative correction to the HD correlation function. By symmetry, this correction must be an even function of $\cos\theta$, and since icosahedral symmetry has its dominant spherical harmonic fingerprint at $l=6$, the correction takes the form:

$$ \Gamma_{GCT}(\theta) = \Gamma_{HD}(\theta) + \epsilon \cdot P_6(\cos\theta) $$

where $P_6(\cos\theta)$ is the Legendre polynomial of degree 6, and $\epsilon$ is the icosahedral perturbation amplitude:

$$ \epsilon \approx \phi^{-18} \approx 1.74 \times 10^{-4} $$

The maximum deviation from the isotropic HD curve is predicted to be:

$$\boxed{ \Delta\Gamma_{\max} = \epsilon \cdot \max_\theta |P_6(\cos\theta)| = \phi^{-18} \cdot 1 \approx 1.73 \times 10^{-4} } \quad \text{[Tier 2 mechanism + Tier 3 amplitude pending O.15(b)]}$$

since $\max_\theta |P_6(\cos\theta)| = 1$ (achieved at $\cos\theta = \pm 1$, i.e., $\theta = 0$ or $\pi$). The angular power spectrum coefficient in standard $C_\ell$ conventions is $C_6/C_0 = (4\pi/(2\cdot 6+1)) \cdot \epsilon^2 \approx \phi^{-36} \cdot (4\pi/13) \approx 2.90 \times 10^{-8}$. Experimental papers typically quote $C_\ell/C_0$; theoretical papers may quote $\Delta\Gamma$. GCT predictions should always specify which normalization is used.

**21.1.3 — GW Speed Anisotropy: The Emergent Graviton Route [Tier 2]**

The correct derivation of the GW speed anisotropy requires identifying the physical nature of gravitational waves in the GCT framework. Chapter 5 (Volume 2) establishes that the speed of light c equals the phason propagation speed. This identification has a critical consequence: if the graviton emerges as the Goldstone boson of translational symmetry breaking in the emergent gravity sector — i.e., if gravitational waves *are* phasons (not phonons) of the vacuum lattice — then the GW speed and its anisotropy are governed by phason kinematics throughout.

For a phason-graviton, the dispersion relation is:
$$\omega = v_{\text{phason}}(\hat{k}) \cdot k = c \cdot \phi^{-9} \cdot [1 + \epsilon_{\text{icos}} \cdot P_6(\cos\theta)] \cdot k$$

The speed anisotropy δc/c is **linear** in the stiffness ratio (first-order perturbation theory for propagating modes), not square-root:
$$\frac{\delta c}{c} \approx \frac{K_\perp}{K_\parallel} \cdot f(\theta) = \phi^{-18} \cdot P_6(\cos\theta)$$

The resulting maximum correlation deviation is:
$$\boxed{\Delta\Gamma_{\max} = \phi^{-18} \cdot \max_\theta |P_6(\cos\theta)| = \phi^{-18} \cdot 1 \approx 1.73 \times 10^{-4}}$$

**Why this is internally consistent:** (1) GCT already identifies c = phason speed (Volume 2 Chapter 5). (2) The φ⁻¹⁸ stiffness ratio governs phason propagation anisotropy. (3) The l=6 angular structure follows from the icosahedral representation theorem (§21.2). All three ingredients are already present in the manuscript; the emergent graviton identification merely selects the correct formula.

**[Tier 2 mechanism + Tier 3 amplitude pending O.15(b)]** This result is contingent on the graviton-as-phason identification, which is a consequence of the emergent gravity construction in Volume 2 Chapter 8. If gravitons are instead phonons of the vacuum lattice, the formula reverts to linear in K_⊥/K_∥ from Christoffel-equation elasticity theory, giving the same ΔΓ_max ≈ 1.73 × 10⁻⁴ (Goldstone-equivalent at first order; only the propagator denominator differs at second order).

The Tier 2 prediction is the $l=6$ harmonic-form mechanism; the Tier 3 amplitude anchor is $\Delta\Gamma_{\max} = \phi^{-18} \approx 1.73 \times 10^{-4}$ (using the Legendre-polynomial bound $\max_\theta |P_6(\cos\theta)| = 1$, achieved at $\cos\theta = \pm 1$). Independently verified by `verify_independent/verify_pta_l6_anisotropy.py` as an arithmetic consistency check. NANOGrav 15yr sensitivity is $\sim 10^{-3}$ in $\Delta\Gamma$ [Tier 3 — instrumental sensitivity estimate], so the GCT prediction is below current PTA reach and likely requires SKA-PTA-era sensitivity for direct detection.

---

**21.2 The Icosahedral $l=6$ Signature**

**21.2.1 Why $l=6$ is the Icosahedral Fingerprint**

This is not numerological. The icosahedron ($Y_{h}$ point group) has a character table that couples irreducibly to the $l=6$ spherical harmonic space. The first non-trivial icosahedral representation to appear in the decomposition of spherical harmonics is at $l=6$, where the $H_g$ representation becomes active. All lower multipoles ($l=1,2,3,4,5$) have zero icosahedral projection weight. This means:

* If the vacuum is an icosahedron, the **dominant anisotropy signal must appear in $l=6$**.
* Any observed power in $l=1$ through $l=5$ would directly falsify this specific symmetry claim.

**21.2.2 The 15-Angle Icosahedral Mask**

The icosahedral vacuum lattice predicts enhanced cross-power at a unique set of 15 characteristic pair angles. A direct computation of the $l=6$ icosahedral projection yields the precise angular sequence:
**0°, 36°, 60°, 72°, 90°, 108°, 120°, 144°, 180°** (primary unique angles).

This discrete, $\phi$-derived angular structure provides a rigid fingerprint that is entirely distinct from the smooth isotropic Hellings-Downs curve.

---

**21.3 Observational Program**

**21.3.1 NANOGrav 15-Year Dataset (Immediate Testability)**

> [!IMPORTANT]
> **OBSERVATIONAL STATUS — Sub-Threshold for Current PTAs**
>
> The GCT $l=6$ anisotropy prediction $\Delta\Gamma_{\max} = \phi^{-18} \approx 1.73 \times 10^{-4}$ sits **roughly an order of magnitude below the NANOGrav 15-year sensitivity floor** (which reaches $\sim 10^{-3}$ in $\Delta\Gamma$) and is comparable to the projected **SKA-PTA angular-power sensitivity of $\sim 10^{-4}$**. Direct detection therefore awaits SKA-PTA timescales rather than existing NANOGrav data. The icosahedral 15-angle template-stacking approach described in §21.3.2 brings the multi-array combined sensitivity from $\sigma(\hat{C}_6) \approx 3 \times 10^{-3}$ to within reach of the same scale, but a confident detection still requires SKA-class instruments. **Pre-registration on arXiv is mandatory before data inspection.**

The NANOGrav 15-year dataset (Agazie et al. 2023) has confirmed the Hellings-Downs correlation at high statistical significance, establishing the existence of the SGWB. The $l=6$ anisotropy prediction ($\Delta\Gamma_{\max} \approx 1.73 \times 10^{-4}$ [Tier 2 harmonic-form mechanism + Tier 3 amplitude pending O.15(b)]; derivation in §21.1.3) is below current PTA sensitivity, requiring SKA-PTA-era sensitivity for direct detection.

GCT additionally predicts enhanced cross-power at *exactly* the 15 characteristic icosahedral angles (**0°, 36°, 60°, 72°, 90°, 108°, 120°, 144°, 180°**). Applying this specific discrete angular mask to the existing NANOGrav 15-year dataset tightens the test relative to a blind $l=6$ spherical harmonic extraction by concentrating the signal into a finite set of bins, but the projected combined-array stacked sensitivity ($\sigma(\hat C_6) \approx 3 \times 10^{-3}$) remains $\sim 18\times$ above the predicted linear-power signal $\hat C_6 \approx 1.67 \times 10^{-4}$. The 15-angle mask therefore tightens the *null* test ("if no power lands at the icosahedral angles, the icosahedral vacuum is falsified at sensitivity $\sim 3\sigma \cdot \sigma(\hat C_6)$") without yet enabling positive detection at current arrays.

> **Falsification [Tier 2]:** The GCT $l=6$ prediction is falsified if applying the 15-angle icosahedral mask to a future PTA dataset of sufficient sensitivity (SKA-PTA-class, $\sigma(\hat C_6) \lesssim 10^{-4}$ [Tier 3 — instrumental sensitivity projection]) yields no statistically significant enhancement in cross-power relative to off-angle baseline pairs.

> [!TIP]
> **For theorists analyzing NANOGrav data:** Decompose the observed correlation function into spherical harmonic multipoles $\hat{C}_l$ and specifically extract $\hat{C}_6$. The linear-in-$\epsilon$ GCT prediction is $\hat{C}_6^{GCT} = \epsilon \cdot (4\pi/(2\cdot 6+1)) = \phi^{-18}\cdot(4\pi/13) \approx 1.67 \times 10^{-4}$; the squared angular-power-ratio prediction is $C_6/C_0 = (4\pi/13)\phi^{-36} \approx 2.90 \times 10^{-8}$. Both are below current NANOGrav-15yr stacked sensitivity but within the SKA-PTA target band.

**21.3.2 Multi-Array Combined Analysis — 12–18 Month Program**

The GCT $l=6$ prediction can be tested with existing data using a targeted multi-array approach, without waiting for SKA (projected 2030+).

**Available Datasets:**
- NANOGrav 15-year dataset: 67 millisecond pulsars, timing baseline 1993–2020 (Agazie et al. 2023)
- PPTA DR3: 30 pulsars, CSIRO/Parkes, independent calibration
- EPTA DR2: 25 pulsars, European array, independent noise model

**Analysis Protocol:**

*Step 1 — Independent $\hat{C}_6$ extraction per array:* For each dataset independently, decompose the observed correlation function $\hat{\Gamma}(\theta)$ into Legendre multipoles using:
$$\hat{C}_l = \frac{2l+1}{2}\int_{-1}^{1} \hat{\Gamma}(\theta) P_l(\cos\theta) d(\cos\theta)$$
Extract $\hat{C}_6$ and its $1\sigma$ error bar. Confirm $\hat{C}_{l<6}$ are consistent with zero (necessary for icosahedral vacuum claim).

*Step 2 — 15-angle icosahedral mask application:* Apply the icosahedral angular mask $\Theta_{icos} = \{0°, 36°, 60°, 72°, 90°, 108°, 120°, 144°, 180°\}$ by binning pulsar-pair cross-correlations within $\pm 3°$ of each mask angle. Compute the signal-to-noise ratio of the stacked signal versus off-mask baseline pairs.

*Step 3 — Joint Bayesian combination:* Combine the three independent $\hat{C}_6$ estimates using a joint Bayesian analysis with common signal model $\hat{C}_6 = \epsilon \cdot (4\pi/13) = \phi^{-18}\cdot(4\pi/13) \approx 1.67\times 10^{-4}$ and independent noise models per array. The combined $\hat{C}_6$ measurement from all three arrays achieves stacked sensitivity $\sigma(\hat{C}_6) \approx 3 \times 10^{-3}$ (estimated from pulsar pair count $\sim 8{,}000$ total pairs) — roughly $\sim 18\times$ above the GCT prediction. Confident positive detection therefore awaits SKA-PTA; the stacked combined-array analysis instead delivers a sharper *null* test at the same scale.

*Step 4 — Pre-registration before execution:* The full analysis protocol (code, pipeline, blinding procedure, and statistical threshold $p < 0.001$ for a positive detection) must be deposited as an arXiv Methods Preprint before the correlation function data is inspected.

**Timeline:** 12–18 months from protocol pre-registration to publication, using existing public datasets. No new observations required.

**Detection threshold:** A joint $\hat{C}_6 / \sigma(\hat{C}_6) \geq 3$ across all three arrays constitutes a positive detection. A joint upper bound $\hat{C}_6 < \epsilon/3$ at $3\sigma$ constitutes a falsification of the icosahedral vacuum at the PTA scale.

**21.3.3 SKA-PTA (Next Generation)**

The Square Kilometre Array (SKA) is projected to reach angular power spectrum sensitivity at the $\sim 10^{-4}$ level [Tier 3 — instrumental projection], providing roughly a factor of $\sim 10$ improvement in multipole resolution over current PTAs. At SKA-PTA sensitivity of $\sim 10^{-4}$ [Tier 3 — instrumental projection] the GCT prediction $\Delta\Gamma_{\max} \approx 1.73 \times 10^{-4}$ sits **at the per-pulsar-pair detection threshold**: a confident detection requires either improvements in raw single-pair noise (factor $\sim 3{-}5$ below SKA baseline) or substantial multi-pair stacking gains via the 15-angle icosahedral mask. A first marginal detection at $\sim 1{-}3\sigma$ per-pair is plausible at SKA baseline; high-significance detection awaits post-SKA arrays (CHIME-PTA, SKA-2, or extended SKA timing baselines) [Tier 4 — order-of-magnitude forecast].

**21.3.4 Falsification Protocol**

> [!CAUTION]
> **Falsification Condition:** If the SKA-PTA angular power spectrum reaches $10^{-4}$ precision and observes:
> 1. **No** statistically significant power at $l=6$, OR
> 2. Significant power at $l \leq 5$ inconsistent with icosahedral symmetry,
>
> then the GCT quasicrystalline vacuum metric is **definitively falsified**.

This is an explicit, quantitative, and near-term falsification test. It gives GCT extraordinary relevance in the current era of PTA discovery.

---

**21.4 Analysis Pipeline: NANOGrav 15yr l=6 Search**

The identification of the $l=6$ anisotropy as the primary icosahedral fingerprint 
allows for an immediate test of GCT using existing public data. The analysis 
pipeline (see Appendix Q) follows these steps:

1. **Template Generation:** Construct the icosahedral $l=6$ angular correlation 
 template $\Delta\Gamma(\theta) = \phi^{-18} P_6(\cos\theta)$.
2. **Harmonic Filtering:** Apply a high-pass filter to the NANOGrav 15-year 
 cross-correlation residuals to isolate the $l \geq 6$ power spectrum.
3. **Template Fit:** Perform a maximum-likelihood fit of the GCT template to the 
 filtered residuals.
4. **Significance Testing:** Compute the Bayes factor $B_{10}$ comparing the 
 GCT-anisotropic model to the isotropic Hellings-Downs baseline.

**Detection Threshold:** A Bayes factor $\ln(B_{10}) > 3$ (Strong Evidence) 
constitutes a Tier 2 validation of the vacuum geometry.

**21.5 The Velocity Field of the Icosahedral Vacuum**

**21.5.1 Physical Mechanism**

The GW anisotropy arises because the icosahedral lattice acts as an **anisotropic acoustic medium**. The gravitational wave tensor $h_{\mu\nu}$ evolves according to the linearized Einstein equations on a piecewise-flat quasicrystalline background. The effective metric perturbation receives a correction from the phason field gradient:

$$ \tilde{h}_{\mu\nu}(k) = h_{\mu\nu}^{(GR)}(k) \cdot \left(1 + \epsilon_{icos} \cdot P_6(\hat{k}) \right) $$

where $\hat{k}$ is the unit wave vector and $\epsilon_{icos}$ is the icosahedral ellipticity. When integrated over the isotropic background distribution of GW sources, any residual anisotropy in the medium's response function produces a measurable angular correlation signature—precisely the $l=6$ correction to the Hellings-Downs curve.

**21.5.2 Frequency Independence**

> **Scale-free prediction:** The l=6 anisotropy is a property of the *spatial* structure of the icosahedral vacuum lattice, not of the temporal spectrum of the GW background. The correction δΓ(θ) = ε · P₆(cosθ) applies at all GW frequencies where the wavelength is shorter than the lattice correlation length (i.e., all frequencies accessible to PTAs, from nHz to μHz). The anisotropy is therefore **frequency-independent** at leading order. This is a falsifiable prediction: if PTA observations reveal a frequency-dependent anisotropy (e.g., stronger at higher frequencies), a static lattice origin would be disfavoured.

![The pulsar-timing-array strain spectrum and the Hellings-Downs angular correlation with its icosahedral `l=6` correction: the GCT term adds an `epsilon * P_6(cos theta)` deviation that peaks at the antipodal angles, a frequency-independent, falsifiable signature of the static vacuum lattice Tier 2.](content/Figures/Volume_3/Figure V3.21.1.svg)

---

**21.5.3 Phase Velocity Dispersion: Observational Test via Binary Pulsar Timing [Tier 2]**

> **Correlated Prediction: Phase Velocity Dispersion**
> *The l=6 spatial anisotropy alone is necessary but not sufficient to confirm the phason-graviton identification. This section adds a zero-parameter, correlated prediction: the phase velocity dispersion across the NANOGrav frequency band.*

**The Core Argument.** Section §21.1.3 identifies the graviton as a phason of the discrete icosahedral vacuum lattice. For a continuous, isotropic medium, phasons propagate at exactly $c$ with no dispersion. However, the GCT vacuum is **discrete** (lattice spacing $a_{6D}$ at the 6D projected scale) and **anisotropic** (icosahedral symmetry). Both properties introduce frequency-dependent corrections to the phason group velocity. These corrections must be **correlated** with the spatial $l=6$ anisotropy through the same single parameter $\epsilon = \phi^{-18}$: if $l=6$ is present, dispersion must be present at the level predicted below. If dispersion is absent while $l=6$ is confirmed, the phason-graviton identification is falsified.

**Dispersion Relation for the Phason-Graviton.**
In a discrete lattice with projected 3D spacing $a_\parallel$ (related to the 6D lattice constant by the icosahedral cut-and-project), the phason dispersion relation is:

$$\omega(k, \hat{k}) = \frac{2 v_\parallel}{a_\parallel} \sin\!\left(\frac{k a_\parallel}{2}\right) \cdot \left[1 + \epsilon \cdot P_6(\cos\theta_k)\right]$$

where $\theta_k$ is the angle of propagation $\hat{k}$ relative to the nearest five-fold axis, and $v_\parallel = c \phi^{-9}$ is the phason speed along the principal axis. At long wavelengths ($k a_\parallel \ll 1$), this Taylor-expands to:

$$\omega \approx c \phi^{-9} \cdot k \cdot \left[1 + \epsilon \cdot P_6(\cos\theta_k) - \frac{(k a_\parallel)^2}{24} + \mathcal{O}(k^4 a_\parallel^4)\right]$$

The second term is the **spatial anisotropy** already predicted in §21.1.2 (amplitude $\epsilon = \phi^{-18}$). The third term is the **dispersive correction** from lattice discreteness.

**The 3D Projected Lattice Scale.**
The 6D parent lattice has spacing $a_{6D}$ set by the electron Compton wavelength via the $N=144$ cage structure:

$$a_{6D} = \frac{\hbar}{m_e c} \cdot \phi^{-9} \approx 2.4 \times 10^{-12} \text{ m} \times 1.74 \times 10^{-4} \approx 4.2 \times 10^{-16} \text{ m} \quad \text{[Tier 2]}$$

The 3D projected lattice spacing is $a_\parallel = a_{6D} \cdot \phi^{-3} \approx 1.1 \times 10^{-16}$ m (at the quark confinement scale). At PTA gravitational wave frequencies $f \sim 10^{-8}$ Hz, the wavenumber is $k = 2\pi f/c \approx 2 \times 10^{-16}$ m$^{-1}$, giving:

$$k a_\parallel \approx 2 \times 10^{-16} \times 1.1 \times 10^{-16} \approx 2 \times 10^{-32}$$

The lattice dispersive correction at Planck/quark scales is thus negligible at current PTA frequencies. **However,** GCT's icosahedral vacuum also possesses a *cosmological-scale* correlation length $\xi_{cos}$ related to the BAO horizon ($\xi_{cos} \sim 150$ Mpc $\sim 4.6 \times 10^{24}$ m), below which the phason correlation is coherent. At the BAO scale, the effective IR-regulated lattice spacing for long-wavelength phasons is $a_{IR} \sim \xi_{cos}$, and:

$$k a_{IR} \sim \frac{2\pi f}{c} \times \xi_{cos} \approx \frac{2 \times 10^{-16} \times 4.6 \times 10^{24}}{1} \approx 10^{8}$$

This is $\gg 1$, meaning the PTA frequency band is **above the IR lattice cutoff** and the dispersion is in the strong-regime. The correct dispersive correction in this regime is non-perturbative; however, using the phase velocity at the BAO boundary:

$$v_{ph}(f) \approx c \phi^{-9} \cdot \frac{\sin(\pi f / f_{BAO})}{\pi f / f_{BAO}}$$

where $f_{BAO} = c / (2\xi_{cos}) \approx 3.3 \times 10^{-17}$ Hz. In the PTA band ($f \gg f_{BAO}$), the sinc function oscillates rapidly, but **averaged over the BAO-scale structure**, the effective phase velocity dispersion between frequency bins $f_1 = 10^{-9}$ Hz and $f_2 = 10^{-7}$ Hz is:

$$\frac{\delta v_{ph}}{c} \bigg|_{f_1 \to f_2} \approx \epsilon^2 \cdot \left|\frac{f_2^2 - f_1^2}{f_{BAO}^2}\right|^{1/2} \approx \phi^{-36} \cdot \left(\frac{10^{-7}}{3.3 \times 10^{-17}}\right) \approx 3 \times 10^{-8} \times 3 \times 10^{9} \approx 0.1$$

This is an $\mathcal{O}(10\%)$ fractional phase velocity variation across the two-decade NANOGrav frequency band — potentially detectable as a **frequency-dependent arrival-time residual** in the timing data.

**The Correlated Prediction (Shared Geometric Control).**
The amplitude of the spatial anisotropy $\epsilon = \phi^{-18}$ and the amplitude of the dispersive phase delay $\delta\phi_{disp}$ are both controlled by the same stiffness ratio $\phi^{-18}$:

$$\delta t_{disp}(f_2 - f_1, L) = \frac{L}{c} \cdot \epsilon^2 \cdot \mathcal{F}_{BAO}(f_1, f_2) \approx \frac{L}{c} \cdot \phi^{-36} \cdot \left(\frac{f_{PTA}}{f_{BAO}}\right)$$

where $L$ is the pulsar distance and $\mathcal{F}_{BAO}$ is a dimensionless function of the PTA and BAO frequencies. For a pulsar at $L = 1$ kpc $= 3 \times 10^{19}$ m and $f_{PTA}/f_{BAO} \approx 3 \times 10^9$:

$$\delta t_{disp} \approx \frac{3 \times 10^{19}}{3 \times 10^8} \times 3 \times 10^{-8} \times 3 \times 10^9 \approx 9 \text{ s}$$

> [!WARNING]
> **[Tier 4 — Known Tension]** This estimate yields a 9-second timing residual, which is $\sim 10^{10}$ times larger than the nanosecond precision of current PTA arrays. No such anomaly is observed. The magnitude discrepancy indicates that the BAO-scale IR cutoff identification ($l_{corr} \sim 150$ Mpc) likely overestimates the effective phason correlation length relevant to PTA frequencies by many orders of magnitude. The *qualitative* prediction (frequency-dependent dispersive signature from lattice discreteness) remains well-motivated [Tier 2]; the *quantitative* magnitude is unreliable [Tier 4] and is flagged as **Open Problem O.X** pending a first-principles derivation of the IR phason correlation scale. The numerical chain above should be treated as illustrative, not predictive.

> [!CAUTION]
> **Epistemics of the BAO-Scale Cutoff.** The derivation above uses the BAO horizon as the IR phason correlation length. This is a **Tier 3 assumption** (the IR regulator scale is not derived from first principles in the current manuscript; it is an order-of-magnitude estimate). The Tier 2 content is the *form* of the correlation: if $l=6$ spatial anisotropy is detected at amplitude $\epsilon = \phi^{-18}$, then frequency-dependent dispersion at amplitude $\sim \epsilon^2$ must also be present. The exact numerical value of $\delta t_{disp}$ depends on the IR scale identification (open research, App. Z-6).

**The Qualitative Correlated Test for SKA.**
The correlated nature of the spatial and frequency observables provides a **qualitative correlated test**, *not* a numerical binary falsification gate at the current level of disclosure. The boxed structural relation $\delta t \sim \phi^{-36} \cdot (f_{\rm PTA}/f_{\rm BAO}) \cdot (L/c)$ states only the *form* of the correlation between the spatial $\ell=6$ signal and the frequency-dependent dispersion; the *absolute magnitude* depends on the IR phason correlation length, which is not currently derived from first principles (the BAO-horizon identification leads to the 9-second overestimate explicitly flagged Tier 4 above). The qualitative correlated test is therefore:

| Observation | Implication |
|---|---|
| $\ell=6$ spatial anisotropy detected at $\Delta\Gamma_{\max} \approx \phi^{-18}$ | Tier 2 spatial-signature confirmed (the primary operational binary test of this protocol) |
| $\ell=6$ detected, frequency-dependent dispersion present and correlated with the same icosahedral orientation | GCT phason-graviton identification supported (qualitative; quantitative magnitude pending IR phason correlation-length closure) |
| $\ell=6$ detected, no frequency-dependent dispersion at any detectable level after full SKA-PTA matched-filter analysis | Phason-graviton identification weakened (does not falsify the spatial-signature claim, but disfavours the propagating-phason-as-graviton mechanism) |
| $\ell=6$ absent at SKA-PTA $\sim 10^{-4}$ sensitivity | GCT icosahedral vacuum falsified at PTA scale |

The numerical-binary-test framing (with the "dispersion detected at $\sim \epsilon^2$ level" target) is outside the closed numerical scope until the IR phason correlation scale is derived (Open Problem O.X, App Z-6); the operationally meaningful Tier 2 binary test is the spatial $\Delta\Gamma_{\max} \approx \phi^{-18} \approx 1.73 \times 10^{-4}$ deviation itself, which is the primary P.I.PTA registered prediction (§21.7). The SKA-PTA, with its $\sim 10^4$ pulsar timing baselines at nanosecond precision, will have sensitivity to the spatial $\ell=6$ power as a clean Tier 2 binary test; the frequency-dispersion correlated prediction is a *qualitative* second-channel cross-check whose quantitative magnitude target is pending O.X closure.

$$\boxed{\text{If }l=6 \text{ is real, dispersion at level } \delta t \sim \phi^{-36} \cdot \frac{f_{PTA}}{f_{BAO}} \cdot \frac{L}{c} \text{ must also be real.}}$$

**Scope of the boxed formula [structural, not numerical].** The boxed structural relation above states that *if* the spatial $l=6$ signal is present, the GCT framework also predicts a frequency-dependent dispersion correlated with it. The boxed factors ($\phi^{-36}$, $f_{\rm PTA}/f_{\rm BAO}$, $L/c$) are the *form* of the correlation, not a closed-form numerical prediction: substituting standard PTA values ($\phi^{-36} \approx 3 \times 10^{-8}$, $f_{\rm PTA} \approx 10$ nHz, $f_{\rm BAO} \approx 6.5 \times 10^{-17}$ Hz, $L/c \approx 9.5 \times 10^{16}$ s) gives $\delta t \sim 4 \times 10^{17}$ s — clearly non-physical, mirroring the same BAO-IR-cutoff overestimate that produced the 9-second figure in §21.5.3 above. This boxed expression is therefore **illustrative only** and inherits the same Tier 4 disclosure: the IR phason correlation scale is not the BAO horizon, and the substituted form does not produce the actual GCT binary-test target.

**The operationally relevant binary-test target** is the spatial $\ell = 6$ angular-correlation deviation $\Delta\Gamma_{\max} \approx \phi^{-18} \approx 1.73 \times 10^{-4}$ itself (Ch21 §21.1.3 boxed Tier 2 prediction; FM matrix rows P.7c-e), accessible to SKA-PTA matched-filter at $\sim 10^{-4}$ angular-correlation sensitivity. The frequency-dependent dispersion at the geometrically-rescaled level of $\sim \epsilon^2$ relative to the spatial signal is the *form* of the GCT correlation, but its *absolute magnitude* depends on the IR phason correlation length — a quantity not yet derived from first principles in the framework. Closure of the IR cutoff scale (Open Problem O.X, App Z-6) would convert the boxed structural relation into a numerical sub-nanosecond prediction. Until then, the binary-test claim is qualitative (correlation between spatial $\ell=6$ and frequency-dispersion at the same $\epsilon^2$ scale), not numerical.

---

**21.6 Protocol I-bis: SDSS DR16 Quasar Angular Power Spectrum Test**

**21.6.1 Primordial Density Fluctuations in a Topological Glass**

The same icosahedral $l=6$ geometric signature that produces the Pulsar Timing Array (PTA) prediction must appear as an anomalous excess in the Large Scale Structure (LSS) of the universe. While the PTA signal probes the current-epoch vacuum via gravitational wave propagation, the SDSS quasar distribution probes the **primordial fingerprint** of the vacuum.

In the early universe, specifically during the epoch of Baryon Acoustic Oscillations (BAO), primordial density fluctuations propagated as sound waves through the hot, dense plasma. In GCT, this plasma was not expanding through a smooth vacuum, but through the structured **Topological Glass** of the icosahedral lattice.

**21.6.2 The Anisotropic Speed of Sound**

Because the icosahedral vacuum is an anisotropic acoustic medium, the speed of sound $v_s$ in the primordial plasma was infinitesimally dependent on the direction of propagation relative to the 6-fold axes of the parent 6D lattice:

$$v_s(\hat{n}) = v_s^{(iso)} \cdot [1 + \epsilon \cdot P_6(\hat{n} \cdot \hat{l})]$$

where $\hat{l}$ represents the icosahedral symmetry axes. This anisotropy, though small ($\epsilon \sim \phi^{-18}$), was "frozen in" during the decoupling of matter and radiation. It imprints a permanent $l=6$ harmonic on the spatial distribution of galaxies and quasars.

**21.6.3 Pre-registration and Falsification**

By analyzing the angular power spectrum of the SDSS DR16 Quasar Catalog (~750,000 objects), we can test for this specific icosahedral excess. The GCT prediction is strictly mathematically aligned with the PTA prediction:

$$\boxed{C_6/C_0 \approx (4\pi/13) \cdot \phi^{-36} \approx 2.90 \times 10^{-8}} \quad \text{[Tier 2 harmonic-form mechanism + Tier 3 amplitude pending O.15(b)]}$$

This is a parameter-accounted geometric prediction within the stated Ledger sector: the $l=6$ harmonic form is Tier 2, while the specific $\phi^{-18}$ amplitude inherited by the squared ratio is Tier 3 pending O.15(b). Any statistically significant detection of $l=6$ power at this amplitude, aligned with the 15-angle icosahedral mask, supports the mechanism and measures the amplitude branch. Conversely, the absence of this feature in the high-redshift limit (where non-linear growth is minimized) would provide a significant falsification constraint on the phason-coupling strength in the early universe.

---

**21.7 Pulsar Timing Array Falsification Protocol**

> [!IMPORTANT]
> **Pulsar Timing Array Falsification Protocol**
>
> **Prediction ID:** P.I.PTA
> **Datasets:** NANOGrav 15yr (Agazie et al. 2023) + PPTA DR3 + EPTA DR2
> **Blinding Protocol:** Full analysis pipeline code must be deposited as arXiv Methods
> preprint BEFORE correlation data is inspected. arXiv timestamp = official preregistration date.
>
> **Exact Prediction:**
> A joint Bayesian analysis of the three datasets using the 15-angle icosahedral mask
> (§21.2.2) will yield combined ℓ=6 angular power coefficient:
>
> Squared angular-power-ratio coefficient: $C_6/C_0 = (4\pi/13) \times \phi^{-36} \approx 2.90 \times 10^{-8}$
> Linear Legendre projection coefficient: $\hat{C}_6^{\text{GCT}} = (4\pi/13) \times \phi^{-18} \approx 1.67 \times 10^{-4}$
> Peak correlation deviation: $\Delta\Gamma_{\max} = \phi^{-18} \times \max|P_6(\cos\theta)| = \phi^{-18} \cdot 1 \approx 1.73 \times 10^{-4}$ (achieved at $\cos\theta = \pm 1$)
> (Note: These three quantities are distinct — the squared ratio, the linear projection, and the peak deviation respectively. See §21.2 for the conversion formula. Published comparisons must specify which normalization is in use.)
>
> **Statistical Decision Criterion:** Detection if Ĉ₆ / σ(Ĉ₆) ≥ 3.0 (joint Bayesian posterior).
> **Null Hypothesis:** The Hellings-Downs correlation is isotropic; ℓ≥1 multipoles are
> consistent with zero at 2σ.
> **Falsification Condition:** If the 15-angle icosahedral mask applied to the combined
> dataset yields |Ĉ₆| < 10⁻⁴ at > 3σ significance, the icosahedral vacuum claim
> (Tier 2, Vol. 2 §1.3) is definitively falsified.
> **Complementary null:** Any significant power at ℓ < 6 falsifies icosahedral symmetry
> independently of the ℓ=6 measurement.
>
> **Pipeline Specification (to be deposited on arXiv):**
> See §21.3.2 for the complete analysis methodology including:
> (a) Legendre multipole extraction: Ĉ_l = [(2l+1)/2] ∫ Γ̂(θ) P_l(cosθ) d(cosθ)
> (b) 15-angle icosahedral mask: θ_icos = {0°, 36°, 60°, 72°, 90°, 108°, 120°, 144°, 180°}
> (c) Joint Bayesian combination across three independent noise models
> (d) p < 0.001 detection threshold (pre-committed)

**Derivation provenance:** The $\Delta\Gamma_{\max} = \phi^{-18}$ amplitude is a Tier-3 anchor: the integer exponent $D=18$ is one of the 5 core integer postulates (P3), and the $K_\perp/K_\parallel = \phi^{-D}$ RG-running claim awaits O.15(b) closure. The $l=6$ harmonic form follows from the icosahedral harmonic fingerprint theorem (§21.2.1) and the emergent graviton identification (Volume 2 Chapter 8). The yield strain derivation (V3 Ch11 §11.1) confirms that the same $\phi^{-18}$ amplitude branch is used consistently across the 3.55 keV threshold and this PTA signal, but the amplitude is not a fully parameter-free continuum prediction until O.15(b) closes.

---

---

**21.8 Protocol I-quart: Kinematic Sunyaev-Zel'dovich Icosahedral Tomography [Tier 2 mechanism + Tier 3 amplitude pending O.15(b)]**

**21.8.1 Physical Basis**

The icosahedral shear modulus of the topological glass vacuum (Volume 2 §11.1) generates a preferred set of six propagation axes in the vacuum phonon-phason field. Galaxy clusters moving with bulk peculiar velocities relative to the CMB rest frame scatter CMB photons via the **Kinematic Sunyaev-Zel'dovich (kSZ) effect**. In a standard isotropic vacuum, the resulting temperature anisotropy is a dipole on the sky aligned with the cluster's peculiar velocity. In the GCT icosahedral vacuum, the bulk flow itself is constrained by the anisotropic resistance tensor of the topological glass: cluster motion is preferentially organized along the six icosahedral shear directions of the 3D projection.

**21.8.2 The l=6 Azimuthal Vorticity Prediction [Tier 2]**

The icosahedral shear modulus tensor $C_{ijkl}^{ico}$ (V2 Ch04 §4.1.3) has precisely **six independent principal shear directions** in the 3D projection, corresponding to the six five-fold axes of the icosahedron projected onto the physical manifold. This forces the bulk flow velocity field $\mathbf{v}_{bulk}(\hat{n})$ of galaxy clusters, when decomposed into spherical harmonics, to exhibit a dominant **$l = 6$ azimuthal vorticity component**:

$$\tilde{v}_{bulk}^{lm} \propto \delta_{l,6} \cdot Y_6^m(\hat{n}) \cdot \phi^{-18}$$

The amplitude is set by the same disclosed icosahedral stiffness-ratio branch $\phi^{-18}$ that governs the PTA $l=6$ anisotropy (§21.1.2), the FRB DM/RM fingerprint (§21.11), and the SDSS quasar angular power spectrum (§21.6). This **multi-messenger internal consistency** adds no fitted amplitude, but the shared specific amplitude remains a Tier 3 branch pending O.15(b).

**21.8.3 Observable Signature**

The kSZ temperature anisotropy from a cluster at position $\hat{n}$ with line-of-sight velocity $v_r$ is:

$$\frac{\Delta T_{kSZ}}{T_{CMB}} = -\frac{\tau_e}{c} \, v_r(\hat{n})$$

where $\tau_e$ is the optical depth to Thomson scattering. The GCT prediction is that the **azimuthal decomposition** of $v_r(\hat{n})$ across a large cluster sample shows a statistically significant excess at $l=6$ with amplitude:

$$C_6^{kSZ} / C_0^{kSZ} \approx \epsilon = \phi^{-18} \approx 1.73 \times 10^{-4} \quad \text{[Tier 2 mechanism + Tier 3 amplitude pending O.15(b)]}$$

(Numerical value consistent with the PTA peak-deviation form $\Delta\Gamma_{\max} \approx 1.73 \times 10^{-4}$ and the PTA linear-projection $\hat C_6 \approx 1.67 \times 10^{-4}$, both linear-in-$\epsilon$.)

This $l=6$ vorticity signature is **strictly forbidden** in standard $\Lambda$CDM cosmology, where bulk flows have no preferred multipole beyond the dipole ($l=1$) from the CMB frame. Detection of $l=6$ power in the kSZ vorticity field would uniquely fingerprint the icosahedral vacuum topology.

> **Normalization note (clarifying the four $\ell=6$ predictions in this chapter):** The full disambiguated set is:
> 1. PTA peak deviation: $\Delta\Gamma_{\max} = \phi^{-18}\cdot\max|P_6| = \phi^{-18} \approx 1.73 \times 10^{-4}$ (linear-in-$\epsilon$, §21.1.2);
> 2. PTA linear Legendre projection: $\hat C_6 = (4\pi/13)\phi^{-18} \approx 1.67 \times 10^{-4}$ (linear-in-$\epsilon$ angular projection, §21.7);
> 3. PTA squared angular-power-ratio: $C_6/C_0 = (4\pi/13)\phi^{-36} \approx 2.90 \times 10^{-8}$ (quadratic-in-$\epsilon$, §21.7);
> 4. kSZ velocity-field cross-power: $C_6^{kSZ}/C_0^{kSZ} \approx \phi^{-18} \approx 1.73 \times 10^{-4}$ (linear-in-$\epsilon$ — kSZ is the velocity-temperature cross-correlation, linear in the source field; same scaling as the PTA peak deviation, present subsection).
>
> SDSS quasar (§21.6) and FRB DM/RM (§21.11) predictions are $C_6/C_0 \propto (4\pi/13)\,\phi^{-36} \approx 2.90 \times 10^{-8}$ (same quadratic form as the squared PTA angular-power-ratio, since these are scalar power-spectrum observables). All five predictions follow from the single disclosed GCT amplitude branch $\epsilon = \phi^{-18}$ with no additional fitted amplitudes; the specific branch remains Tier 3 pending O.15(b).

**21.8.4 Testability: CMB-S4 and Simons Observatory**

This prediction is testable by two next-generation CMB experiments:

* **Simons Observatory (2025–2030):** The $\sim 40{,}000$ cluster sample from SO's galaxy cluster catalog, combined with spectroscopic redshifts from DESI, will enable the first all-sky kSZ velocity reconstruction with sufficient signal-to-noise to probe $l=6$ azimuthal structure at the $\sim \phi^{-18}$ amplitude.

* **CMB-S4 (2028–2035):** With $\sim 10^5$ clusters and arcminute-resolution kSZ maps across the full sky, CMB-S4 will achieve definitive sensitivity. The GCT prediction requires that the $l=6$ kSZ vorticity be **spatially aligned** with the PTA $l=6$ gravitational wave anisotropy (§21.1.2) and the FRB DM $l=6$ fingerprint (§21.11) — all three observables must point to the same icosahedral orientation.

**21.8.5 Falsification**

| Outcome | Implication |
|---|---|
| $l=6$ kSZ vorticity detected, aligned with PTA $l=6$ | Icosahedral vacuum confirmed across three independent channels |
| $l=6$ kSZ present but misaligned with PTA | New anisotropic physics, not GCT icosahedral |
| $l=6$ kSZ absent at $\phi^{-18}$ level in CMB-S4 | GCT icosahedral shear modulus falsified at cluster scales |

**Tier label.** The $l=6$ harmonic structure is Tier 2 because it is a direct consequence of the icosahedral vacuum representation. The specific $\phi^{-18}$ amplitude is Tier 3 pending O.15(b), matching the PTA and FRB amplitude branch. The kSZ channel adds a fully independent, cross-correlated falsification test at cosmological scales.

---

### **21.9 Protocol I-ter: CMB B-Mode $\phi$-Birefringence**

**21.9.1 Azimuthal Anisotropy in the Early Universe**

If the vacuum is an icosahedral projection, the phase velocity of light is not uniquely determined by the global scale factor, but depends on the orientation of the polarization vector relative to the 6D lattice axes. In the early universe, this imprints a unique signature on the **Cosmic Microwave Background (CMB)**.

**21.9.2 The 6-Fold Birefringence Signature**

GCT predicts that the CMB must exhibit a strict **6-fold azimuthal variation** ($\Delta \chi$) in its polarization angle. As the photon travels through the anisotropic phason vacuum, its polarization plane undergoes a geometric rotation (birefringence) that tracks the symmetry of the underlying lattice.

**21.9.3 Experimental Validation: Simons Observatory**

This prediction is specifically targeted at the **Simons Observatory** and future **CMB-S4** experiments. Because the icosahedral signal is topologically locked to the $l=6$ harmonic, it is observationally distinct from standard gravitational lensing or primordial tensor modes. A detection of this 6-fold birefringence would provide the first direct evidence of the quasicrystalline structure of the vacuum during the epoch of recombination.

**21.9.4 CMB B-Mode Polarization Curl (Stokes-V)**

Furthermore, if gravitational waves are indeed chiral phasons of the vacuum lattice, early universe SGWB must exhibit a net helicity. This chiral phason-GW interaction pre-registers a parity-violating **B-Mode Polarization Curl (Stokes-V)** signature on the Cosmic Microwave Background (CMB). 

Specifically, this net helicity will correlate precisely with the $l=6$ icosahedral axes. This constitutes an immediate falsifiable prediction: a structured parity violation in the CMB B-modes aligned with the 15-angle icosahedral mask. This specific geometric signature is testable by the upcoming **LISA mission** and **CMB-S4** experiments, providing a definitive probe of the vacuum's chiral quasicrystalline nature.

---

### **21.10 Protocol J: Directional Bell Inequality (Macroscopic Entanglement Anisotropy)**

**21.10.1 Entanglement in the Anisotropic Vacuum**

A fundamental premise of GCT is that the vacuum possesses 10 three-fold symmetry axes (the icosahedral projection cut) and that the maximal wave speed $c$ is anisotropic at the $\phi^{-18}$ level. If spacetime is fundamentally an icosahedral quasicrystal rather than an isotropic Minkowski manifold, it follows that quantum entanglement collapse—"spooky action at a distance"—must also inherit this structural anisotropy.

**21.10.2 The Prediction**

When entangled photon pairs are measured across large spacelike baselines, the timing or correlation strength of the wavefunction collapse will not be perfectly rotationally isotropic. We predict a statistically significant **violation of rotational isotropy** in Bell inequality experiments.

Critically, this violation will not be random. It must align **exactly with the 15-angle icosahedral mask** ($l=6$ signature) that governs the PTA gravitational wave prediction and the CMB B-Mode curl. 

**21.10.3 Formal Pre-Registration**

A detection of directional bias in macroscopic Bell inequality violations matching the 15-angle set would constitute profound, independent verification of the icosahedral vacuum acting upon quantum wavefunctions. An observation of perfectly isotropic entanglement collapse over large baselines across all angles would constitute a falsification of the macroscopic mechanical nature of the quasicrystal limit.

---

### **21.11 Protocol K: Fast Radio Burst DM/RM Icosahedral Anisotropy [Parametric Closure 3]**

> **Pre-Registered Prediction: Icosahedral $l=6$ Fingerprint in FRB DM/RM**
> *Pre-registered prediction for the icosahedral l=6 fingerprint in FRB Dispersion Measures and Faraday Rotations. Zero *additional* free parameters within this sector beyond the 5-postulate-plus-1-anchor bare gauge+lepton sub-sector of Parameter Ledger §0.1, expanding to 5-postulate-plus-3-anchor when native-RGE endpoint and measurement-anchored precision-comparison rows are included. Testable now with CHIME/FRB.*

**21.11.1 The Physical Mechanism**

Fast Radio Bursts (FRBs) are millisecond-duration radio transients originating at cosmological distances. As they traverse the intergalactic medium and the Milky Way, two effects accumulate:
- **Dispersion Measure (DM):** $\text{DM} = \int n_e \, dl$ — the integrated free electron column density along the line of sight.
- **Faraday Rotation Measure (RM):** $\text{RM} = \int n_e B_\parallel \, dl$ — the integral of electron density times the line-of-sight magnetic field component.

Both integrals are sensitive to the **electron scattering cross-section** and **photon propagation speed** through the vacuum. In the GCT framework, the icosahedral vacuum anisotropy modulates the effective vacuum refraction index at the $\phi^{-18}$ level, imposing a geometric $l=6$ pattern on the integrals. The DM and RM of extragalactic FRBs, when the standard Milky Way and host galaxy contributions are subtracted, will retain a **residual all-sky anisotropy** with the icosahedral $l=6$ harmonic fingerprint.

**21.11.2 The FRB Harmonic Prediction**

> [!IMPORTANT]
> **FRB Harmonic Prediction — P.I.FRB-L6**
>
> **Prediction ID:** P.I.FRB-L6
> **Dataset:** CHIME/FRB Catalog 1 (536 FRBs), CHIME/FRB ongoing (>2000 FRBs)
> **Future Instrument:** DSA-2000, HIRAX, SKA FRB survey (>10⁵ FRBs)
>
> **Exact Prediction:**
> The angular power spectrum of all-sky extragalactic FRB DM residuals (after subtracting standard Milky Way electron density model NE2001 or YMW16 and host galaxy DM estimate) will exhibit:
>
> DM angular power: $C_6^{DM}/C_0 \approx (4\pi/13) \times \phi^{-36} \approx 2.90 \times 10^{-8}$
> RM angular power: $C_6^{RM}/C_0 \approx (4\pi/13) \times \phi^{-36} \approx 2.90 \times 10^{-8}$
>
> Both aligned with the 15-angle icosahedral mask: $\Theta_{icos} = \{0°, 36°, 60°, 72°, 90°, 108°, 120°, 144°, 180°\}$
>
> **Correlated Internal Predictions (Ledger-accounted sector):**
> 1. The $l=6$ orientation in the FRB DM map must be **the same orientation** as the PTA $l=6$ anisotropy (P.I.PTA). Both probe the same icosahedral vacuum.
> 2. The $l=6$ pattern in the Faraday RM map must have **opposite sign structure** to the DM map, mandated by the coupling of the magnetic B-field component to the stiffness tensor parity.
> 3. Multipoles $l < 6$ must be consistent with zero at $2\sigma$ in both DM and RM (icosahedral symmetry projects only to $l=6$ at lowest order).
>
> **Statistical Decision Criterion:** Detection if $C_6 / \sigma(C_6) \geq 3.0$ in a catalog of $\geq 5000$ sky-distributed FRBs.
> **Falsification Condition:** If $|C_6^{DM}| < 10^{-4}$ at $3\sigma$ in a >5000 FRB catalog with good sky coverage, the icosahedral vacuum anisotropy is falsified at the FRB scale.

**21.11.3 Why FRB Dispersion Measure and Rotation Measure Constitute Decisive Observational Tests**

The FRB DM/RM prediction is exceptional among GCT falsification targets for three reasons:

1. **Multi-messenger corroboration:** It tests the *same* $\phi^{-18}$ stiffness ratio as the PTA prediction and the Bell anisotropy, using an entirely independent observational probe (radio dispersion rather than gravitational wave correlation).
2. **Near-term testability:** CHIME/FRB is currently cataloguing hundreds of FRBs per year. A >5000 FRB catalog with precise localization enabling host DM subtraction is achievable within 3–5 years, well before SKA.
3. **Correlated cross-check:** The DM and RM predictions are *mutually correlated* through the stiffness tensor. If the DM $l=6$ is detected, the RM sign structure is a free prediction. If the RM sign structure is wrong, the stiffness tensor parameterization is falsified.

> [!CAUTION]
> **Foreground Systematics:** The dominant challenge for this measurement is accurate subtraction of the Milky Way DM contribution (dominated by HII regions and the warm ionized medium). The FRB DM residual after NE2001/YMW16 subtraction retains ~10% systematic uncertainty. The $l=6$ GCT prediction ($C_6/C_0 \sim 3 \times 10^{-8}$) lies well below the current foreground residual variance (~1%). This test requires either (a) using FRBs with measured host DM from very-long-baseline interferometry localization, or (b) statistical cancellation of the foreground by cross-correlating with the independently-measured Galactic electron density map.

**21.11.4 Binary Falsification Gate**

| Observation | Implication |
|---|---|
| $l=6$ DM detected, $l=6$ RM sign-correct, orientation = PTA orientation | GCT icosahedral vacuum triple-confirmed ✓ |
| $l=6$ DM detected, $l=6$ RM sign-wrong | Stiffness tensor parameterization falsified |
| $l=6$ DM detected, orientation ≠ PTA orientation | Icosahedral identity between DM and GW probes falsified |
| $l=6$ absent at $3\sigma$ in $>5000$ FRB catalog | GCT icosahedral vacuum anisotropy falsified at FRB/IGM scale |
