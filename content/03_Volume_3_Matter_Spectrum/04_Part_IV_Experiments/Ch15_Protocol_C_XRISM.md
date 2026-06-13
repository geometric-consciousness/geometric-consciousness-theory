### **Chapter 15: Protocol C (XRISM Preregistration)**

The 3.55 keV X-ray anomaly, identified in Chapter 11 as the monochromatic signature of vacuum lattice fracture, provides the most direct observational link to GCT. **Protocol C** defines the formal preregistration for the XRISM line-shape audit.

---

**15.1 Formal Decision Framework**

To ensure scientific reproducibility and avoid outcome-contingent curve fitting, GCT preregisters the following hypothesis test for the XRISM stacked-cluster stress-aperture survey.

**15.1.1 The Null Hypothesis ($H_0$)**
The Dark Matter signal at 3.55 keV originates from a particulate gas (e.g., sterile neutrinos) or standard atomic multiplets (K XVIII).
- **Signature:** Instrumental profile convolved with cluster-virial broadening and background-line modeling uncertainties ($\sigma_v \approx 1300$ km/s for the Perseus reference) [Tier 3 — cluster virial measurement].
- **Expected FWHM:** $\approx 37$ eV for the broad thermal/virialized reference at $E=3.55$ keV [Tier 3 — broadening calculation]. This width is a diagnostic axis, not a standalone sterile-neutrino verdict; morphology, flux floor, and background model are load-bearing.
- **Recoil:** Standard Loss ($0.88$ eV) [Tier 3 — atomic recoil calculation].

**15.1.2 The GCT Hypothesis ($H_1$)**
The Dark Matter signal originates from a macroscopic, coherent topological glass (supersolid vacuum).
- **Signature:** Recoil-free, monochromatic emission (GCT Mössbauer Effect).
- **Expected FWHM (observed; bulk-turbulence broadened Voigt):** $\sim 9.8$ eV at 3.55 keV — quadrature combination of the XRISM Resolve instrumental Gaussian $\sigma_{\rm inst} = 5\,{\rm eV}/2.355 \approx 2.12$ eV (operational analysis freeze uses the then-current XRISM POG plus RMF/ARF calibration files as primary response inputs; the 5–7 eV mission-spec band and Ishisaki et al. 2022 *Proc. SPIE* 12181:121811S (DOI 10.1117/12.2630654) are retained as pre-flight/historical scale anchors) and the bulk-cluster-turbulence Gaussian $\sigma_{\rm kin} \approx E_{\rm line} (v_{\rm turb}/c) \approx 3.55$ eV at $v_{\rm turb} \approx 300$ km/s for typical cluster-core turbulence. Engine-canonical value: `expected_fwhm_ev = 9.7458` per `GCT_Physics_Engine/data/protocol_dm_line_forward_model_results.json` at $\text{XRISM\_FWHM\_EV} = 5.0$. **Sensitivity sweep:** at the conservative mission-spec upper bound $\text{XRISM\_FWHM\_EV} = 7.0$, $\sigma_{\rm inst} = 2.97$ eV, the quadrature $\sigma_{\rm inst,eff} = \sqrt{2.97^2 + 3.55^2} \approx 4.63$ eV, and the predicted observed Voigt FWHM rises to $\sim 10.9$ eV — the §15.2 spectral-compatible band lower edge shifts accordingly. The **deconvolved intrinsic line-width residual** $W_{\rm int} \lesssim 5$ eV (instrument and registered kinematic/turbulence model removed; unmodeled astrophysical and natural broadening remain) is what the §15.2 decision rule operates on — distinct from the observed FWHM that an external observer would measure on the plotted line; both numbers must be reported jointly to avoid the "observer sees ~9 eV → GCT falsified" misreading. [Tier 3 — observed FWHM follows from the Voigt convolution of three Tier 1 / Tier 3 inputs; the W_int decision rule is the falsification gate.]
- **Recoil:** Zero Loss ($< 0.1$ eV) [Tier 2 Prediction — Mössbauer suppression].
- **Acoustic Phonon Signature:** Temporal and spatial cross-correlation with a burst of High-Frequency Gravitational Waves (HFGWs) in the 1-100 MHz band (vacuum fracture acoustic emission).

### 15.1.3 Addressing Known Non-Detections

Multiple independent analyses have reported non-detections of the 3.55 keV 
line in environments where dark matter density alone would predict a strong 
sterile-neutrino signal. GCT does not contest these results; they are
consistent with the stress-gating hypothesis, while their status remains
retrospective until frozen stress-aperture maps and masks are applied
cluster-by-cluster before residual unblinding.

**Malyshev et al. (2014)** performed a stacked XMM-Newton analysis of 
dwarf spheroidal galaxies (dSphs) and blank-sky fields, finding no 3.55 keV 
emission. Under the sterile neutrino hypothesis, this is anomalous given the 
high dark matter columns. Under GCT's **Stress-Gating Hypothesis** 
(§11.1.3), this is the expected result: dSphs possess virial velocities 
of $\sigma_v \sim 5$–$10$ km/s, yielding gravitational shear stresses 
$\sigma_{vir} \ll \sigma_{crit} = K_\perp \cdot \phi^{-5}$ (Appendix K). 
The vacuum lattice in these environments is in the elastic glass phase — 
below the yield threshold — and emits no radiation.

**Riemer-Sørensen (2016)** analyzed Chandra observations of the Milky Way
halo and found no significant excess at 3.55 keV. This is likewise compatible
with a null result in diffuse, low-shear halo environments: the smooth gravitational
potential of the Milky Way halo generates insufficient shear to fracture the
supersolid vacuum lattice. Emission is concentrated in high-stress fracture
zones (cluster outskirts, merger shocks, and high-shear ICM), not in relaxed stellar halos.

**Quantitative GCT Resolution:** 
The stress-gating threshold is numerically frozen as
$$\sigma_{crit}\equiv \sqrt{P_{\rm Perseus-core}P_{\rm Bullet-shock,central}}=\sqrt{(0.07)(4.0)}=0.529\ {\rm keV\,cm^{-3}}\approx0.53\ {\rm keV\,cm^{-3}},$$
using the Perseus-core pressure anchor and the central Bullet-shock pressure estimate cited in Ch11. This remains Tier 3 because the threshold is observation-bracketed, not first-principles derived. Above threshold, emission is mandatory; below, suppressed. **Protocol C's frozen stress-aperture rule:** the operative falsification aperture is the mass-weighted set of cells whose pre-line thermal-pressure/shear proxy satisfies $P_{\rm proxy}\ge0.53\ {\rm keV\,cm^{-3}}$ within the XRISM stacked-cluster sample. The Perseus core is sub-$\sigma_{crit}$ and is not a falsification point; the Hitomi-Perseus null is consistent with this gate.

**Frozen target-cell list.** Before inspecting any 3.55 keV residuals, the analysis locks the following cell classes from pressure/shear maps: (i) Bullet Cluster bow-shock wedge and Mach-cone shell; (ii) Coma merger / radio-relic pressure shells; (iii) A2142 cold-front / merger shell; (iv) A3667, A2256, and A2319 radio-relic or merger-shock shells; (v) any Perseus, A2029, or A1795 off-core annulus only where the same pre-line proxy exceeds $0.53\ {\rm keV\,cm^{-3}}$. Relaxed cool cores, including Perseus $r\lesssim100$ kpc and the A2029/A1795 cores, are locked as sub-threshold calibrators unless their pre-line maps exceed the numeric cut. This freezes the aperture before residual unblinding; residual-selected cell admission is prohibited.

This converts the non-detections from anomalies into stress-gating consistency checks rather than prior successful predictions.
The preregistration in §15.1 should be understood in this context: H1 predicts a strong narrow signal in **non-core** stress-gated cluster regions ABOVE $\sigma_{crit}=0.53\ {\rm keV\,cm^{-3}}$ (cluster outskirts, merger shocks, high-shear ICM); Perseus core is sub-$\sigma_{crit}$ under the frozen numeric stress threshold, explaining Hitomi-Perseus null compatibility. GCT registers a low-shear null branch for dSphs and smooth halos. Both types of measurement are falsification-relevant — a detection in a dSph would falsify the low-shear null branch, while a registered above-$\sigma_{crit}$ stacked-cluster null falsifies only after the preregistered sensitivity and stress-aperture spatial-map requirements are met. **Operational stress-aperture rule:** the primary cluster test is run on the frozen target-cell list above, with aperture weights committed before unblinding from X-ray line residuals.

**15.1.4 Engagement with Dessert-Rodd-Safdi 2020 and the Boyarsky et al. response.**
Dessert, Rodd & Safdi (2020) *Science* 367:1465 used more than 30 Ms of XMM-Newton blank-sky observations to test the Milky-Way-halo flux expected from decaying-dark-matter explanations of the reported 3.5 keV line, finding no evidence for the line and setting decay-rate limits inconsistent with that interpretation. Boyarsky, Malyshev, Ruchayskiy & Savchenko (2020) contested the strength of that limit, arguing that background-line modeling can weaken the bound by more than an order of magnitude and leave a dark-matter interpretation viable; Dessert/Rodd/Safdi's reply held that even conservative additional-line modeling still strongly disfavors decaying dark matter. The literature null is therefore not simply "broad instrumental continuum versus narrow Lorentzian"; it is a coupled blank-sky halo-flux and background-modeling dispute over whether a decaying-DM line should already have appeared in Milky-Way halo data.

**GCT discriminator:** GCT does not use the decaying-DM halo-flux null as its primary model. It predicts stress-gated cluster emission: a Lorentzian-narrow monochromatic line at $E_{vac} = m_e c^2 / 144 \approx 3.5486$ keV (matching the §15.2 decision-rule centroid $E_c = 3.548 \pm 0.005$ keV and the engine output `verify_dm_line_centroid_postdiction_check.py::predicted = 3.5486038 keV` to the displayed precision) whose spatial morphology tracks high-shear fracture boundaries rather than the smooth Milky-Way-halo column. Dessert's blank-sky null remains load-bearing as a warning that background modeling can erase the claimed signal; Boyarsky's response remains load-bearing as a warning that over-aggressive background modeling can over-tighten the bound. The XRISM/Athena test must therefore adjudicate three axes at once: intrinsic width, centroid, and stress-correlated morphology. **Operational consequence:** a resolved $W_{\rm int}<1$ eV line is not a linewidth discriminator by itself, because sterile-neutrino decay can also be intrinsically narrow before cluster kinematics and instrumental convolution; Milky-Way halo blank-sky nulls impose an independent flux constraint. A null result in the registered high-shear cluster sample at the required sensitivity falsifies or demotes the GCT stress-gating threshold; it should not be reported merely as "Dessert vindicated" unless the analysis also reproduces the blank-sky halo-flux assumptions of Dessert et al.

> [!IMPORTANT]
> **Falsification Condition (Non-Detection Branch):** A confirmed detection 
> of 3.55 keV emission at $>3\sigma$ significance in a dSph system with 
> virial velocity $\sigma_v < 15$ km/s would falsify the stress-gating 
> hypothesis, as this implies $\sigma_{vir} < \sigma_{crit}$ by the 
> geometric yield criterion.
> Candidate low-shear targets are Draco, Ursa Minor, Sculptor, Fornax,
> Sextans, and Carina. The dSph branch is decisive only for a blinded
> line search with centroid $E_c = 3.548 \pm 0.005$ keV, deconvolved
> $W_{\rm int}\leq5$ eV, background-line subtraction inside the S1-S6
> budget, and a stack reaching a line-flux sensitivity at least as deep
> as the terminal Bulbul-level Protocol C floor when expressed in the same
> decay-rate-normalized convention ($\Gamma \lesssim 2.0\times10^{-28}\,
> \mathrm{s}^{-1}$ at 94 Ms equivalent). Shallower dSph stacks are sensitivity-limited
> constraints rather than stress-gating falsifiers.

---

**15.2 Quantitative Decision Rule**

The test is adjudicated based on $W_{int}$ and stress-aperture spatial tracking. Here $W_{int}$ means the deconvolved **intrinsic line-width residual** after removing the instrumental response and the registered cluster kinematic/turbulence model; unmodeled astrophysical and natural broadening remain in $W_{int}$. The separately reported convolved observed FWHM includes instrument + turbulence and is expected to be $\sim9.8$ eV for the GCT forward model. The spectral centroid $E_c$ is reported as postdiction-status context for any detected line, not as an operative P.3 falsifier. The HFGW cross-correlation is a separate Tier 4 mechanism-context row outside the P.3 gate. The $W_{int}$ axis is calibrated against two distinct discriminators: the XRISM Resolve instrumental FWHM floor at $\sim 5$ eV (Ishisaki et al. 2022, *Proc. SPIE* 12181:121811S (DOI 10.1117/12.2630654)) and the Dessert-Rodd-Safdi 2020 instrumental-systematic floor for the 3.55 keV band (§15.1.4). The decision rule separates these into four explicit bands:

| $W_{int}$ | Status | Conclusion |
| :--- | :--- | :--- |
| $< 1$ eV | **Narrow line** | Narrow line; not a linewidth discriminator by itself because sterile-neutrino decay can also be intrinsically narrow before cluster kinematics and instrumental convolution. Combined with $E_c = 3.548 \pm 0.005$ keV [centroid postdiction-status alignment; forward Tier 2 gate is $W_{int}$ + morphology] and flux tracking $\nabla \sigma_{vir}$, this is a stress-gated-line outcome; HFGW co-detection (1-100 MHz band) would constitute the additional confirmation row P.7-equivalent for the vacuum-fracture mechanism, but requires HFGW detection sensitivity that does not currently exist at cluster distances (see scope note below). |
| $1$–$5$ eV | **Spectral-compatible (morphology + flux floor pending)** | $W_{int}$ is the **deconvolved intrinsic line-width residual** after instrument and registered kinematic/turbulence deconvolution and lies at a scale that is statistically difficult to separate from the XRISM response floor once response-matrix, background, and turbulence uncertainties are propagated. The current XRISM POG/RMF/ARF response files are the operative calibration source; Ishisaki et al. 2022 is retained as mission-design context. GCT is spectrally compatible with the data but not discriminated against the Dessert instrumental-systematic-floor interpretation; final discrimination requires the registered stress-aperture morphology and flux-floor conditions, with Athena X-IFU follow-up at 2.5 eV FWHM as the cleaner linewidth test. |
| $5$–$20$ eV | **Statistical Tie** | Broader than the instrument FWHM floor but narrower than the thermal/atomic-plasma falsification threshold. GCT compatible but the sterile-neutrino virial-broadening interpretation cannot be excluded; potential inhomogeneous broadening or source confusion. |
| $> 20$ eV OR Flux follows $\rho^2$ | **GCT Falsification** | Thermal/atomic-plasma virial broadening inconsistent with the solid-state Mössbauer-narrowed emission GCT predicts. **H1 Falsified.** Theory requires macroscopic coherence and stress-dependent fracture. Resolved thermal motion or smooth density tracking invalidates the topological glass model. |

> **HFGW co-detection scope note (Tier 4 conditional).** The Protocol C falsification rule states that HFGW co-detection is outside the operative P.3 gate. A "NO HFGW burst detected" clause would be **currently unfalsifiable** because no instrument has 1-100 MHz HFGW sensitivity at extragalactic cluster distances (the published HFGW detector concepts — Gertsenshtein-Zeldovich inverse-mechanism, optical-resonance cavities, levitated-sensor arrays — sit ~$10^{20}$ orders of magnitude short of cluster-scale GW strain at MHz frequencies; Aggarwal, Aguiar, Bauswein et al. 2021 *Living Rev. Relativ.* 24:4 review the field's sensitivity gap). The HFGW co-detection prediction is therefore **Tier 4 (currently unfalsifiable on operational grounds)** until detector technology closes the sensitivity gap; it is *not* part of the operational P.3 falsification gate above. The genuine Tier 2 P.3 falsification gate is the spectral $W_{int}$ + Protocol C stress-aperture spatial-tracking row; centroid agreement is postdiction-status context reported separately.

**Executable-readiness qualifier.** Protocol C is a conditional decision design, not a completed OSF-grade executable preregistration until the per-cell ARF/RMF/background/effective-mass table is frozen and deposited with the target-cell mask, response files, background model, and synthetic-line checks. The nominal 94 Ms exposure is therefore necessary but not sufficient for a decisive no-line branch.

**Conditional preregistration design.** Registry mirror (App V P.3 / App FM P.3): GCT is falsified at decisive sensitivity if any registered branch holds: (a) NO 3.55 keV line detected at the terminal no-line floor $\Gamma \lesssim 2.0\times10^{-28}\ \mathrm{s}^{-1}$ in $\geq94$ Ms equivalent stacked exposure, OR (b) detected line has $W_{\rm int}>20$ eV FWHM after instrument and registered kinematic/turbulence deconvolution, OR (c) detected-line morphology does NOT follow the stress-gated $\rho_{\rm above\,\sigma_{crit}}^2$ template by $\Delta\chi^2\ge9$ versus both smooth $\rho$ and smooth $\rho^2$ templates. The 26 Ms / $\Gamma \lesssim 3.8\times10^{-28}\ \mathrm{s}^{-1}$ value obtained by scaling the XRISM 3.75 Ms ten-cluster reference stack is a sensitivity milestone and morphology/linewidth constraint point, not a terminal no-line falsifier of a Bulbul-normalized $\Gamma\sim2\times10^{-28}\ \mathrm{s}^{-1}$ signal. The terminal no-line floor is the same scaling continued to the Bulbul-level normalization: $1.0\times10^{-27}\sqrt{3.75/94}\approx2.0\times10^{-28}\ \mathrm{s}^{-1}$. Aperture: mass-weighted stress-gated regions with $P_{\rm proxy}\ge\sigma_{\rm crit}=0.53\ {\rm keV\,cm^{-3}}$ under the Protocol C stress-aperture rule (§15.1.4). Sample-size/integration rule: the primary above-$\sigma_{crit}$ stacked-cluster no-line decision requires an exposure stack reaching the terminal floor at 3.55 keV after background modelling; shallower stacks are sensitivity-limited and reported as constraints, not decisive nulls. The nominal 94 Ms equivalent exposure is insufficient by itself: the preregistration must include a per-cell ARF/RMF/background/effective-mass exposure table demonstrating that each frozen stress-aperture cell contributes to the terminal flux/decay-rate floor after real response, masking, continuum, and cluster-stacking losses before the terminal no-line branch is executable as a completed decisive falsifier.

**Executable-gate status.** Until the per-cell ARF/RMF/background/effective-mass table is frozen, the terminal no-line branch is preregistered but not executable as a decisive falsifier; the current package supports sensitivity-limited constraints and morphology/linewidth milestones.

**Public preregistration freeze.** Before unblinding line residuals, the Protocol C package is deposited in a timestamped public archive (OSF/Zenodo or mission-collaboration equivalent) containing the target-cell list and exclusion rules, RMF/ARF/gain-response files, synthetic-line injections at the registered flux/width/morphology levels, K-XVIII/background model priors, analysis code hash, randomization/blinding seed protocol, S1-S6 systematic budget, and amendment ledger. Any post-freeze change is recorded as a numbered amendment with timestamp, rationale, and the blinded/unblinded state of the affected data.

**Operational count/background power model:** For XRISM Resolve at 5 eV-class instrument resolution, a 20 eV line window, effective area $A_{\rm eff}=200\ \mathrm{cm^2}$, and background $6.6\times10^{-4}\ \mathrm{cnt/s/keV}$ per the HEASARC XRISM Resolve POG residual-background line, the idealized background rate in the line window is $1.32\times10^{-5}\ \mathrm{cnt/s}$. At 3.75 Ms, $B\approx49.5$ counts, so $3\sqrt{B}\approx21.1$ source counts and $F_{3\sigma}\approx2.8\times10^{-8}\ \mathrm{ph/cm^2/s}$. At 26 Ms, $B\approx343$ counts, so $3\sqrt{B}\approx55.6$ source counts and the background-limited theoretical floor is $F_{3\sigma}\approx1.1\times10^{-8}\ \mathrm{ph/cm^2/s}$, corresponding in the prior-normalization convention to $\Gamma\lesssim1.2\times10^{-30}\ \mathrm{s}^{-1}$. At 94 Ms, the empirical-derived no-line floor reaches the Bulbul-level $\Gamma\lesssim2.0\times10^{-28}\ \mathrm{s}^{-1}$ under the same reference-stack scaling. The background-limited theoretical floor is not the operative falsification gate. Real-stack penalties from aperture overlap, continuum subtraction uncertainty, line-model degeneracy with adjacent thermal lines such as K-XVIII at 3.5 keV, and cluster-stacking S/N efficiency typically degrade the limit by 100-1000×. **Terminal no-line falsification operates on the Bulbul-level empirical-derived floor**, not the background-limited theoretical floor.

Analysis blinding: the primary linewidth fit is run blinded to the GCT/sterile-neutrino labels, using fixed windows around 3.548 keV and sideband-derived background terms; centroid is carried as context after the spectral fit is frozen. An unblinded secondary analysis may inspect stress-map alignment only after the spectral fit is frozen. **Morphology decision statistic and power:** after unblinding, the Protocol C stress-weighted aperture template from the frozen target cells is compared against smooth $\rho$ and $\rho^2$ templates with the same exposure/background mask. Before the line fit is inspected, the frozen mask must pass the template-separation diagnostic $D_{\rm sep}=\min(1-\mathrm{corr}(S,\rho),\,1-\mathrm{corr}(S,\rho^2))\ge0.25$ using unit-normalized, exposure-weighted templates under the same mask. At the registered 26 Ms morphology milestone, the count model gives $B\approx343$ background counts in the 20 eV line window and $3\sqrt{B}\approx55.6$ source counts; for one registered morphology degree of freedom this is powered to $\Delta\chi^2\ge9$ only when the $D_{\rm sep}$ diagnostic passes. A stress-gated morphology is required to improve the line-flux fit by $\Delta\chi^2\ge9$ (3σ for one registered morphology degree of freedom) over both smooth templates; a smooth-template preference of $\Delta\chi^2\ge9$ at decisive spectral sensitivity falsifies the stress-morphology branch. If the frozen mask fails the pre-line template-separation diagnostic, the morphology branch is reported as underpowered rather than used as a falsifier; the terminal spectral non-detection branch remains tied to $\Gamma\lesssim2.0\times10^{-28}\ \mathrm{s}^{-1}$ at $\ge94$ Ms equivalent, while linewidth/morphology constraints may be reported at the 26 Ms milestone. Partial-detection rule: (a) line in band with $W_{int}<5$ eV but no stress map is "spectral-compatible / morphology-pending"; (b) stress-aperture alignment without a resolved line is "morphology-compatible / spectral-pending"; (c) line absent only at the 26 Ms milestone is sensitivity-limited; line absent at the terminal Bulbul-level floor across the stacked above-$\sigma_{crit}$ apertures is a substantive stress-gating failure; (d) any $W_{int}>20$ eV or smooth $\rho^2$ density tracking at decisive sensitivity falsifies the Protocol C GCT branch.

**Preregistered systematic-error budget (frozen before unblinding).** The P.3 linewidth decision must report all six systematics before assigning a pass/fail label:

| Systematic | Registered tolerance | Mitigation / reporting rule |
| :--- | :--- | :--- |
| S1 RMF/ARF residuals | $<2\%$ per channel | Resolve response matrix and energy-dependent redistribution propagated into the deconvolution prior. |
| S2 K-XVIII subtraction uncertainty | $<1\times10^{-5}\ {\rm s}^{-1}$ contamination | Local sideband slope, cluster-continuum curvature, and K-XVIII/Ar/Ca line complex fitted jointly, with K-XVIII subtraction reported explicitly. |
| S3 gain drift | $<0.3$ eV cumulative | Gain drift and pointing-dependent response checked against calibration lines. |
| S4 split-stack scatter | $\sigma_{\rm stack}<0.5$ eV | Split-stack linewidth and centroid stability across exposure partitions. |
| S5 cluster kinematic / ICM-substructure deconvolution | residual $<1$ eV after velocity-field and shear-map priors | Perseus primary stack repeated on the registered high-shear cluster ensemble with cluster-level random effects; high-shear apertures require pre-line velocity/shear-map priors, and any aperture whose thermal-substructure or Doppler-shear budget cannot be bounded below 1 eV is reported as systematics-limited rather than decisive. |
| S6 calibration consistency | $<2\%$ systematic across exposures | Cross-exposure calibration consistency reported before unblinding. |

A null or linewidth excess is decisive only if the S1-S6 budget remains inside its preregistered tolerance; otherwise the outcome is "systematics-limited" rather than a P.3 falsification.

---

**15.3 Forward Model Implementation**

The GCT Physics Engine generates the expected observational signature by convolving the lattice-predicted delta function with the XRISM Resolve redistribution matrix:

```python
# GCT Forward Model (Simplified Logic)
sigma_inst = instrument_fwhm / 2.355
sigma_eff = sqrt(sigma_inst**2 + sigma_turb**2)
fwhm_total = 2.355 * sigma_eff  # GCT predicts intrinsic_width ~ 0
```
Detailed simulation code is provided in **Appendix Q**.

**15.4 Falsification Commitment**

If XRISM Resolve definitively measures the 3.55 keV line in the stacked above-$\sigma_{crit}$ cluster apertures with a deconvolved intrinsic width $W_{int} > 20$ eV (the §15.2 decision-rule falsification threshold), GCT is **falsified**. A null is decisive only when the exposure stack reaches the preregistered sensitivity floor and the mass-weighted stress-gated aperture map is included. The Perseus core alone remains sub-threshold and is not a falsification point. The universe either exhibits bulk vacuum coherence under the registered stress-gating conditions or it does not.

> [!NOTE]
> The deep-survey exposure at the requisite sensitivity is the registered Protocol C exposure class (XRISM Science Working Group, JAXA/NASA Mission Operations Plan; cf. Tashiro et al. 2018 *Proc. SPIE* 10699:1069922 for the XRISM mission concept). Stacks that do not reach the terminal Bulbul-level empirical-derived $\Gamma \lesssim 2.0 \times 10^{-28}\,\mathrm{s}^{-1}$ sensitivity floor are reported as sensitivity-limited constraints rather than decisive nulls; the 26 Ms / $\Gamma \lesssim 3.8 \times 10^{-28}\,\mathrm{s}^{-1}$ point remains the morphology-linewidth milestone, and the background-limited $\Gamma \lesssim 1.2 \times 10^{-30}\,\mathrm{s}^{-1}$ calculation is a theoretical ceiling, not the operational gate.

---

**15.5 XRISM Stacked-Cluster Constraint: Line-Shape Verdict**

The Protocol C constraint table distinguishes sensitivity-limited cluster stacks from decisive line-shape tests. Reference stack:

| Item | Result |
| :--- | :--- |
| Exposure | 3.75 Ms (10 clusters stacked) |
| 3.55 keV Line Detection | **Not detected** in the reference stack |
| Decay Rate Upper Limit | $\Gamma \lesssim 1.0 \times 10^{-27}\ \mathrm{s}^{-1}$ (3$\sigma$ upper limit; XRISM Collaboration 2025, arXiv:2510.24560) [Tier 3 — observational upper bound] |
| Sensitivity vs. Bulbul et al. | **5× weaker** than original XMM-Newton detection rate |
| Physical Conclusion | **Sensitivity-limited** — insufficient depth to confirm or rule out |
| GCT Prediction Status | **Stress-gated branch not adjudicated.** Deeper above-$\sigma_{crit}$ survey required. |

Protocol C becomes decisive only for the mass-weighted above-$\sigma_{crit}$ stacked-cluster aperture that reaches the preregistered sensitivity floor and reports the frozen linewidth and stress-map decision rule, with centroid carried as postdiction-status context. Shallower stacks and Perseus-core-only nulls remain constraints on the line-flux normalization rather than falsifications of the stress-gated branch.

---

**END OF CHAPTER 15**
