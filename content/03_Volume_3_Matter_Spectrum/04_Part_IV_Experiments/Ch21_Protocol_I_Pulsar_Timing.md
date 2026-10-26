### **Chapter 21: Protocol I — The Icosahedral \(\ell=6\) Response Program**

> [!IMPORTANT]
> **Epistemic status.**
>
> - **Tier 1 mathematics:** for a scalar function invariant under the rotational icosahedral group, the first nonconstant invariant spherical harmonic occurs uniquely at $\ell=6$.
> - **Tier 2 within the declared GCT symmetry model:** if a physical scalar response preserves the vacuum's proposed $I_h$ symmetry, its leading *allowed* nonconstant component is that unique $A_g$ line.
> - **Tier 3/open physical bridge:** no current action calculation derives a nonzero PTA response, its frequency dependence, polarization content, orientation, or amplitude. P3b, $K_\perp/K_\parallel=\phi^{-18}$, does not by itself supply this detector response.
>
> A separation-only expression $\Gamma_{HD}(\zeta)+\epsilon P_6(\cos\zeta)$, a “15-angle mask,” and numerical conversions derived from them are not admissible icosahedral PTA observables: they erase the absolute sky orientation that an icosahedral signal must carry.

---

**21.1 Exact Icosahedral Harmonic Theorem**

For the rotational icosahedral group \(I\cong A_5\), with conjugacy classes

$$
(E,15C_2,20C_3,12C_5,12C_5^2),
$$

the restricted \(SO(3)\) representation has character

$$
\chi_\ell(\theta)=\frac{\sin[(\ell+\tfrac12)\theta]}{\sin(\theta/2)}.
$$

Exact character inner products give

| \(\ell\) | Restriction to \(I_h\) |
|---:|---|
| 0 | \(A_g\) |
| 1 | \(T_{1u}\) |
| 2 | \(H_g\) |
| 3 | \(T_{2u}\oplus G_u\) |
| 4 | \(G_g\oplus H_g\) |
| 5 | \(T_{1u}\oplus T_{2u}\oplus H_u\) |
| 6 | \(A_g\oplus T_{1g}\oplus G_g\oplus H_g\) |

Thus \(H_g\) already occurs at \(\ell=2\). What first appears at \(\ell=6\) is the nonconstant **trivial scalar representation** \(A_g\), with multiplicity one:

$$
\operatorname{rank}\!\left[\frac1{60}\sum_{g\in I}D^{(\ell)}(g)\right]
=0\quad(1\leq\ell\leq5),\qquad
\operatorname{rank}=1\quad(\ell=6).
$$

This theorem selects an allowed scalar shape. It does not require its coefficient to be nonzero.

**21.1.2 The unique six-axis invariant**

Choose one unit vector from each of the six unoriented five-fold axes,

$$
\mathbf a_i\in\frac1{\sqrt{\phi+2}}
\{(0,1,\phi),(0,-1,\phi),(1,\phi,0),(-1,\phi,0),(\phi,0,1),(\phi,0,-1)\}.
$$

The unique leading invariant can be written as the Reynolds sum

$$
H_6(\hat{\mathbf n})=\sum_{i=1}^{6}P_6(\mathbf a_i\!\cdot\!\hat{\mathbf n}),
\qquad
\int_{S^2}H_6^2\,d\Omega=\frac{1584\pi}{325}.
$$

Define the unit-norm template

$$
\mathcal A_6(\hat{\mathbf n})
=\frac{H_6(\hat{\mathbf n})}{\sqrt{1584\pi/325}}.
$$

In a frame whose \(z\)-axis is a five-fold axis, its normalized complex spherical-harmonic coefficients have support at \(m=0,\pm5\):

$$
a_{60}=\frac{\sqrt{11}}5,\qquad
\lvert a_{65}\rvert=\lvert a_{6,-5}\rvert=\frac{\sqrt7}{5}.
$$

with power fractions \(11/25,7/25,7/25\). A general orientation \(R\) rotates this coefficient vector with the Wigner matrix \(D^{(6)}(R)\), normally populating every \(m\). The nonzero \(m=\pm5\) terms prove that \(\mathcal A_6\) is not one zonal Legendre polynomial.

**21.1.3 Angles and axes are not a separation mask**

Icosahedral rotation-class angles are \(0^\circ,72^\circ,120^\circ,144^\circ,180^\circ\). The group has six five-fold, ten three-fold and fifteen two-fold unoriented axes. These are different objects. Every pair of distinct five-fold axis lines meets at

$$
\arccos(1/\sqrt5)=63.4349488^\circ.
$$

The list \(\{0,36,60,72,90,108,120,144,180\}^\circ\) is neither a fifteen-element set nor the set of five-fold-axis pair angles. Binning only by pulsar-pair separation also discards the absolute orientation required by \(\mathcal A_6(R^{-1}\hat n)\).

---

**21.2 The Correct PTA Observable**

**21.2.1 Why a separation-only correction cannot work**

The Hellings--Downs curve \(\Gamma_{HD}(\zeta)\) is a function only of angular separation \(\zeta\). Under a simultaneous rotation \(Q\),

$$
(Q\hat p_a)\cdot(Q\hat p_b)=\hat p_a\cdot\hat p_b.
$$

Therefore any term \(P_6(\hat p_a\cdot\hat p_b)\) remains fully \(SO(3)\)-invariant. It contains no icosahedral frame, no six axes and no orientation that another messenger could share.

**21.2.2 Generalized overlap-reduction functions**

For an anisotropic, unpolarized stochastic-background **sky-power** model, expand

$$
P(\hat\Omega)=\sum_{\ell m}c_{\ell m}Y_{\ell m}(\hat\Omega).
$$

The PTA covariance is then

$$
\Gamma_{ab}(f)=\sum_{\ell m}c_{\ell m}\Gamma^{ab}_{\ell m}(f),
$$

where the generalized overlap-reduction functions depend on individual pulsar directions, detector antenna patterns and pulsar terms. This is the primary formalism of Mingarelli et al. (2013) and Gair et al. (2014), not a one-dimensional Legendre correction.

A minimal, explicitly conditional icosahedral sky-power ansatz is

$$
P(\hat\Omega;R)=1+\eta\,\mathcal A_6(R^{-1}\hat\Omega),
$$

$$
\Gamma_{ab}(f;R)=\Gamma^{HD}_{ab}(f)
+\eta\sum_{m=-6}^{6}a_{6m}(R)\Gamma^{ab}_{6m}(f).
$$

Here \(R\in SO(3)/I\) is the physical icosahedral orientation and \(\eta\) is an undetermined response coefficient. Unless another measurement fixes \(R\), the fit carries three continuous orientation parameters modulo the sixty rotational symmetries.

**21.2.3 Sky anisotropy is not propagation anisotropy**

The ansatz above describes anisotropic source power on the sky. GCT's proposed mechanism instead concerns anisotropic propagation through a structured vacuum. That requires a separate derivation beginning with a directional response kernel,

$$
K_{IJ}(\omega,\mathbf k;R)
=K^{(0)}_{IJ}(\omega,k)
+\eta\,\mathcal A_6(R^{-1}\hat k)\,\Delta K_{IJ}(\omega,k)+\cdots,
$$

and continuing through the modified Green function, polarization content, source-to-Earth transfer, pulsar term and timing-residual covariance. Only then can the generalized-ORF template and its coefficient be fixed.

This bridge is presently open. The exact harmonic theorem does not choose \(\eta\). P3b chooses neither \(\Delta K_{IJ}\) nor the map from a stiffness ratio to a timing covariance.

---

**21.3 Normalization Calculation**

A separation-only normalization would define

$$
\widehat C_\ell=\frac{2\ell+1}{2}\int_{-1}^{1}
\widehat\Gamma(x)P_\ell(x)\,dx
$$

while injecting \(\delta\Gamma=\epsilon P_6\). Orthogonality gives \(\delta\widehat C_6=\epsilon\), not \((4\pi/13)\epsilon\). For the standard scalar sky-map convention, the ratio depends on the declared normalization of the angular template. It is not universally \((4\pi/13)\epsilon^2\). The numerical quantities \(1.67\times10^{-4}\) and \(2.90\times10^{-8}\) are therefore not defined PTA conversions without a specified observable, normalization, and transfer function.

---

**21.4 Dispersion and Frequency Dependence**

For an analytic inversion-symmetric microscopic response, a generic branch can be expanded as

$$
\omega^2(k,\hat k)=c^2k^2\left[
1+\eta(\omega,k)\mathcal A_6(R^{-1}\hat k)
+\gamma_2(\hat k)(ka_6)^2+\mathcal O((ka_6)^4)
\right].
$$

The anisotropic response \(\eta\) and dispersive coefficient \(\gamma_2\) are independent effective-action data. Neither is fixed by the integer \(D_{H_3}=18\) or P3b alone. At the canonical microscopic scale \(a_6=2\ell_P\approx3.23\times10^{-35}\) m and \(f=10^{-8}\) Hz, \(ka_6\approx6.8\times10^{-51}\), so microscopic nearest-neighbour lattice dispersion is irrelevant at PTA frequencies. Detectable collective infrared dispersion remains an open hypothesis requiring a derived nonlocal kernel.

---

**21.5 Revised Analysis Program**

The analysis is not ready for data preregistration. The next required work is theoretical:

1. Derive a GW response kernel from the GCT action, including inertia/dissipation and polarization structure.
2. Establish whether the response has a nonzero scalar \(A_g\) coefficient at \(\ell=6\).
3. Derive the frequency-dependent transfer into PTA residuals and generalized overlap-reduction functions.
4. Freeze normalization, orientation treatment and nuisance/foreground model.
5. Only then preregister a blind joint analysis of PTA datasets.

If an independently motivated sky-power model is studied before the propagation calculation, it must be labelled a phenomenological \(I_h\) template search, not a GCT prediction. The fit must use the full \(m\)-resolved vector \(a_{6m}(R)\); a separation-only stack or “15-angle mask” is inadmissible.

---

**21.6 Tier-Separated Decision Rules**

| Question | Current status | What would decide it |
|---|---|---|
| Does scalar \(I_h\) invariance first allow a nonconstant harmonic at \(\ell=6\)? | Exact Tier 1 theorem | Character/Reynolds calculation, already verified |
| Does the GCT vacuum generate a nonzero scalar \(\ell=6\) GW response? | Tier 3/open | Action \(\to\) propagator calculation |
| Is the response a sky-power anisotropy or a propagation anisotropy? | Open | Source/medium transfer derivation |
| What is its PTA coefficient and frequency law? | Open | Generalized-ORF observable map |
| Does P3b imply the observable amplitude? | No current derivation | Independent stiffness-to-response transfer law |
| Can a null PTA result falsify the angular theorem now? | No | A nonzero response floor must first be derived |

An empirically established vacuum-attributable scalar anisotropy below \(\ell=6\) would reject the application of exact \(I_h\) scalar symmetry to that channel. Absence of \(\ell=6\) does not reject the group theorem because the allowed coefficient may vanish. Once a nonzero action-level coefficient and sensitivity floor are derived, a preregistered upper limit can falsify that specific physical response map.

---

**21.7 Cross-Messenger Scope**

The same exact invariant \(\mathcal A_6(R^{-1}\hat n)\) can serve as a common *conditional* template for other directional observables, but symmetry does not make their transfer functions or amplitudes equal. Large-scale structure, CMB birefringence, directional Bell tests, and FRB DM/RM each require their own response and survey-selection kernels. If two independently derived channels couple to one fixed vacuum tensor, shared orientation means the same fitted \(R\in SO(3)/I\) or the same rotated coefficient vector \(a_{6m}(R)\), never the same pulsar-pair separation bins.

---

**21.8 Reproducibility and Canonical Disposition**

The exact harmonic calculation is implemented in `GCT_Physics_Engine/src/protocol_pta_l6_template.py`. It verifies the character decomposition, invariant-projector rank, six-axis harmonic, norm, \(m\)-weights, pair-angle calculation and normalization obstruction. The expected result is that the exact $\ell=6$ invariant is confirmed while the separation-only PTA map is obstructed.

**Conclusion.** Exact icosahedral scalar symmetry selects a unique leading allowed harmonic at \(\ell=6\). The physical map from the GCT action to a nonzero, oriented PTA covariance remains open at Tier 3. The required calculation is action \(\to\) propagator \(\to\) generalized overlap-reduction function, not a \(P_6\) separation-bin search.
