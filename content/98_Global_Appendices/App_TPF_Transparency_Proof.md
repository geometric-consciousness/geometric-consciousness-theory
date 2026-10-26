### **Appendix TPF: The Transparency Proof**

**TPF.1 The Lattice Scattering Problem**

A fundamental objection to any discrete spacetime model is the potential violation of Lorentz Invariance (LIV). If space is a lattice with spacing $a \sim \ell_P$, high-energy particles with wavelengths $\lambda \sim a$ should undergo Bragg scattering or emit Vacuum Cherenkov radiation. This would result in a catastrophic energy loss for Ultra-High-Energy Cosmic Rays (UHECRs), imposing a GZK-like cutoff at the Planck scale. The observation of cosmic rays up to $10^{20}$ eV implies that the vacuum is transparent at least up to that energy, about $10^{-8}$ of the Planck energy; this does not by itself test Planck-scale transparency.

We model the scattering process using the Born Approximation. The scattering amplitude $A(\mathbf{q})$ for a momentum transfer $\mathbf{q}$ is proportional to the Fourier transform of the lattice potential $V(\mathbf{x})$.
$$ A(\mathbf{q}) \propto \tilde{V}(\mathbf{q}) = \sum_{\mathbf{G}} S(\mathbf{G}) \delta(\mathbf{q} - \mathbf{G}) $$
where $\mathbf{G}$ are the reciprocal lattice vectors and $S(\mathbf{G})$ is the Structure Factor. In a simple cubic lattice, $S(\mathbf{G})$ is constant, leading to strong scattering. In a quasicrystal, however, the structure factor is non-uniform.

**TPF.2 The Scattering Potential in Hyperspace**

In the Cut-and-Project formalism, the physical potential $V(\mathbf{x}_\parallel)$ is the projection of a hyper-periodic function in 6D. The structure factor $S(\mathbf{G}_\parallel)$ in physical space is determined by the **Fourier Transform of the Acceptance Window** $\tilde{W}(\mathbf{G}_\perp)$ in internal space.
$$ S(\mathbf{G}_\parallel) \propto \tilde{W}(\mathbf{G}_\perp) $$
For the Ammann-Kramer-Neri tiling, the window $W$ is a Rhombic Triacontahedron. Its Fourier transform decays as a rapid power law of the internal wavevector magnitude.
$$ |S(\mathbf{G})|^2 \sim \frac{1}{|\mathbf{G}_\perp|^{\nu_{RT}}} $$
where $\nu_{RT}$ denotes the power-law decay exponent of the Rhombic Triacontahedron window Fourier transform (distinct from the fine-structure constant $\alpha$). This decay is the key to transparency. A scattering event is only probable if the corresponding reciprocal lattice vector has a small perpendicular component $|\mathbf{G}_\perp| \approx 0$.

**TPF.3 Relativistic Kinematics and the Diophantine Gap**

Consider a relativistic particle with momentum $\mathbf{p}$. For large angle scattering, the required momentum transfer is $\mathbf{G}_\parallel \approx 2\mathbf{p}$.
The reciprocal lattice vectors $\mathbf{G}$ are integer combinations of the basis vectors $\mathbf{e}_i^*$.
$$ \mathbf{G} = \sum_{i=1}^6 n_i \mathbf{e}_i^* $$
The parallel and perpendicular components are coupled. Because the projection involves the Golden Ratio $\phi$, which is the **"Most Irrational"** number (Hurwitz's Theorem), there is a **Diophantine Gap** between the parallel and perpendicular components.

For a generic large $\mathbf{G}_\parallel$ (high energy), the corresponding $\mathbf{G}_\perp$ cannot be arbitrarily small.
Specifically, for $\mathbf{G}_\parallel \sim p$, the minimum possible $\mathbf{G}_\perp$ scales as $p^{-1}$ only for specific Fibonacci-resonant indices. For generic high-energy states (random directions), $|\mathbf{G}_\perp|$ grows with $p$. Since the potential amplitude decays with $|\mathbf{G}_\perp|$, the effective potential barrier for generic high-momentum scattering **vanishes**.

**TPF.4 The Transparency Theorem**

**Theorem TPF.1 (Asymptotic Transparency) [Tier 3 — heuristic Born-level scaling argument; steps 4–5 below are assumptions, not derived; the physical application to the vacuum is conditional]:** 
Within the Born-approximation scattering model above, and granting the assumed scalings of steps 4–5, the scattering cross-section of a relativistic particle with the quasicrystal vacuum is suppressed by the **Diophantine Gap** of the Golden Ratio. 

The effective dispersion relation is then modelled (not derived) as:
$$E^2 = p^2 c^2 \left( 1 - \xi \left(\frac{p}{M_{Planck}}\right)^2 \right)$$
For UHECRs with $p \ll M_{Planck}$, the correction term is negligible, preserving Lorentz Invariance. However, at $p \sim M_{Planck}$, the term becomes significant. A speculative extension reads this as an **Anisotropic GZK Recovery** (Protocol H) [Tier 4; no derived LIV coefficient, threshold modification or direction map].

**Proof sketch (heuristic):**
1. The cross-section is the integral of the structure factor over the kinematically allowed momentum transfers.
2. $\sigma(E) \propto \int |S(\mathbf{G})|^2 \delta(E - E') d^3\mathbf{G}$.
3. Due to the Diophantine scaling, the density of lattice points with significant weight ($|\mathbf{G}_\perp| < \epsilon$) decreases as $|\mathbf{G}_\parallel|$ increases.
4. *Assumption (not derived):* the effective spectral weight of the potential scales as $V_{eff} \sim E^{-1}$.
5. *Assumption-dependent consequence:* with step 4 and Born scaling $\sigma\propto|V_{eff}|^2$, $\sigma(E) \propto E^{-2}$.

Under these assumptions the cross-section vanishes as $E \to \infty$ and the lattice becomes effectively transparent: the universe would appear discrete at low energies but approximately continuous at high energies. This would supply a candidate mechanism for "Lorentz Safety" for UHECRs; it does not ensure it, since steps 4–5 and the dispersion form above are not derived from the lattice action [Tier 3].

**TPF.5 The Center-Inversion Argument: Cancellation of the Inversion-Odd Linear LIV Term [Tier 1 within the model; general $n=1$ exclusion Tier 3]**

Theorem TPF.1 sketches asymptotic Diophantine suppression ($\sigma \propto E^{-2}$) for generic scattering, on the assumptions of its steps 4–5 [Tier 3]. This section shows a narrower result within the same scattering model: **the inversion-odd structure-factor contribution to the linear ($n=1$) LIV coefficient cancels**. Inversion symmetry alone does not forbid every $n=1$ term: a rotation-invariant correction proportional to $|\mathbf{p}|$ is inversion-even, and in effective field theory the rotation-invariant $n=1$ photon terms are CPT-odd and helicity-dependent. Excluding them requires the CPT and helicity structure of the emergent electromagnetic action, which has not been derived [Tier 3 assumption].

**The RT Center-Inversion Symmetry.** The Rhombic Triacontahedron (RT) acceptance window $W \subset E_\perp$ possesses full icosahedral point-group symmetry $I_h$. Crucially, $I_h$ contains the **center-inversion operation** $\mathbf{r} \to -\mathbf{r}$:
$$\mathbf{r} \in W \implies -\mathbf{r} \in W$$
This is a standard property of the RT: all 30 rhombic faces come in antipodal pairs, so $W = -W$.

**The n=1 LIV coefficient.** The first-order Lorentz-violating correction to the photon dispersion relation takes the general form:
$$E = pc\left(1 + \xi_1 \frac{p}{M_{Planck}} + \xi_2 \left(\frac{p}{M_{Planck}}\right)^2 + \cdots\right)$$
The coefficient $\xi_1$ (the linear correction) is determined by the antisymmetric part of the structure factor sum over the reciprocal lattice:
$$\xi_1 \propto \sum_{\mathbf{G}} (\hat{\mathbf{p}} \cdot \mathbf{G}_\parallel)\, |S(\mathbf{G})|^2$$
where $\hat{\mathbf{p}}$ is the propagation direction and $\mathbf{G}_\parallel$ is the parallel component of the reciprocal vector.

**Cancellation by inversion symmetry.** The structure factor satisfies $S(\mathbf{G}) = \tilde{W}(\mathbf{G}_\perp)$, the Fourier transform of the window function. Under the center-inversion $\mathbf{G} \to -\mathbf{G}$, we have:
- $\mathbf{G}_\parallel \to -\mathbf{G}_\parallel$ (the parallel component changes sign)
- $|S(\mathbf{G})|^2 = |\tilde{W}(\mathbf{G}_\perp)|^2 \to |\tilde{W}(-\mathbf{G}_\perp)|^2 = |\tilde{W}(\mathbf{G}_\perp)|^2$ (invariant, since $|W|^2$ is even)

Therefore the summand $(\hat{\mathbf{p}} \cdot \mathbf{G}_\parallel)|S(\mathbf{G})|^2$ is **odd** under $\mathbf{G} \to -\mathbf{G}$. Because the reciprocal module is a group, it is symmetric under $\mathbf{G} \to -\mathbf{G}$, and the sum of an odd function over a symmetric domain is exactly zero:
$$\xi_1 = \sum_{\mathbf{G}} (\hat{\mathbf{p}} \cdot \mathbf{G}_\parallel)\, |S(\mathbf{G})|^2 = 0$$

**Scope of the cancellation.** This cancellation is generic, not a consequence of the RT center-inversion. Every reciprocal lattice or module is closed under $\mathbf{G}\to-\mathbf{G}$, and for any real-valued potential Friedel's law gives $S(-\mathbf{G})=S(\mathbf{G})^*$, hence $|S(-\mathbf{G})|^2=|S(\mathbf{G})|^2$, whether or not the window satisfies $W=-W$. The same structure-factor sum therefore vanishes for any real periodic or cut-and-project potential in this Born-level model. The RT inversion symmetry is consistent with the result but is not needed for it, and the cancellation is not an icosahedral signature.

**Theorem TPF.2 (Linear LIV Cancellation within the TPF Model) [Tier 1 within the model; general $n=1$ exclusion Tier 3]:** *For any propagation direction $\hat{\mathbf{p}}$, the structure-factor sum defining $\xi_1$ in the App TPF scattering model vanishes by the $\mathbf{G}\to-\mathbf{G}$ symmetry of the reciprocal module together with Friedel's law for a real potential (generic to any real periodic or cut-and-project potential; the RT center-inversion is consistent with, but not required for, the cancellation). If, in addition, the CPT and helicity structure of the emergent electromagnetic action excludes the inversion-even rotation-invariant $n=1$ terms (Tier 3 assumption), the leading LIV correction is quadratic ($n=2$) with coefficient $\xi_2 \sim \mathcal{O}(1)$.*

**Physical consequence.** Two kinds of astrophysical bound apply to linear LIV. Time-of-flight data from GRB 090510 give $E_{QG,1} > 1.2\,E_{\rm Planck}$, i.e. $|\xi_1| \lesssim 1$ (Abdo et al. 2009); GRB polarimetry constrains helicity-dependent (birefringent) $n=1$ terms at roughly the $10^{-16}$ level. Within the TPF model both are satisfied only under the Tier 3 CPT/helicity assumption: the structure-factor cancellation removes only the inversion-odd part, and an inversion-even rotation-invariant $|\mathbf{p}|$ term (not excluded by the model) is exactly what time-of-flight bounds constrain. The conditional model expectation is zero linear LIV and a non-zero quadratic correction at Planck-scale energies; the anisotropic pattern reflecting the icosahedral symmetry is a Tier 4 extension (see V3 Ch20, Protocol H). $\square$
