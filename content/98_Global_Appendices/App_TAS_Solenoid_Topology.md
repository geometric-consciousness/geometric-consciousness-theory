### **Appendix TAS: Topology of the Adelic Solenoid**

> **Cross-reference note:** The Pontryagin duality proof in this appendix provides additional detail for the construction presented inline in V1 Chapter 7 §7.2.2 (where it is cited via Hewitt & Ross). A proof sketch of $\Sigma_\infty \cong (\mathbb{R} \times \hat{\mathbb{Z}})/\mathbb{Z}$ is given in §TAS.2 below; the full argument is in Hewitt & Ross. No-signalling does not follow from the address topology of $\Sigma_\infty$: shared cylinders establish no correlation, common state or channel. The separate conditional field-readout bound (subluminal only on an extra $v_{\rm phonon}\leq c$ premise) is in Appendix FTH Proposition FTH.4 and Appendix SNE §SNE.4; the icosahedral selection input is developed in Appendix USS §USS.6.

**TAS.1 Inverse Limit Spectra and the 5-adic specification**

The identity space $\Sigma_\infty$ is the **Inverse Limit** of a system of circle wrappings $\{X_n, f_{nm}\}$ where each $X_n \cong S^1$ and $f_{nm}: X_m \to X_n$ is the bonding map $z \mapsto z^{m/n}$ for $n|m$.

**Definition:**
$$\Sigma_\infty = \varprojlim (S^1, f_{nm}) = \left\{ (z_n) \in \prod S^1 : z_n = (z_m)^{m/n} \right\}$$
Dualizing the circle system gives the direct limit $\varinjlim\mathbb{Z}\cong\mathbb{Q}$, and the profinite transversal is $\hat{\mathbb{Z}}=\varprojlim_n\mathbb{Z}/n\mathbb{Z}\cong\prod_p\mathbb{Z}_p$, which contains every prime factor [Tier 1]. GCT proposes the **5-adic factor** ($\mathbb{Z}_5$) as the primary structure of the identity bundle [Tier 3]. This choice is motivated by the adopted icosahedral point-group structure (App USS records $A_5$ as the Tier 1/2 architectural premise H1 and derives conditional consequences; it does not prove point-group uniqueness), but the icosahedral occurrence of order five does not force an infinite $5^k$ refinement tower. A selected $\mathbb{Z}_5$ factor becomes physically privileged only if a compatible fivefold subdivision/RG mechanism is independently derived [Tier 3/open]. A pure degree-five circle tower is not the universal Solenoid; its dual is $\mathbb{Z}[1/5]$.

**TAS.2 Pontryagin Duality: Proof Sketch**

We sketch the local product structure of $\Sigma_\infty$ via the **Pontryagin Duality Theorem**, establishing a bijection between locally compact abelian groups and their character groups.
1. The dual of the discrete group of rationals $\mathbb{Q}$ is the inverse limit of the system $(S^1, z^n)$.
2. Therefore, $\Sigma_\infty \cong \text{Char}(\mathbb{Q})$.
3. By the structure theorem for solenoids, we obtain the canonical decomposition:
$$\Sigma_\infty \cong (\mathbb{R} \times \hat{\mathbb{Z}}) / \mathbb{Z}$$
This is a suspension/local-product presentation (equivalently $\Sigma_\infty\cong\mathbb{A}_{\mathbb{Q}}/\mathbb{Q}$), not a literal global product: the path components are dense real leaves, and the transversal $\hat{\mathbb{Z}}$ is profinite (a product over all primes, not a single $p$-adic factor) [Tier 1]. GCT reads these two roles as a continuous **Stream** (the path-component of the identity) and a totally disconnected **Fractal Fiber** (the address); identifying them with experiential flow and identity address is a Tier 3 GCT bridge, not a consequence of the duality.

**TAS.3 The First Čech Cohomology Group**

Because $\Sigma_\infty$ is not locally contractible, we utilize **Čech Cohomology** to measure its informational capacity. The first Čech cohomology group is:
$$\check{H}^1(\Sigma_\infty; \mathbb{Z}) \cong \varinjlim \check{H}^1(S^1; \mathbb{Z}) \cong \mathbb{Q}$$
This invariant must be kept distinct from the homotopy invariants: $\pi_1(\Sigma_\infty)=0$ and, under the standard first-shape-group convention, $\check\pi_1(\Sigma_\infty)=0$, while the pro-group $\operatorname{pro}\pi_1$ is the inverse system $(\mathbb{Z}\xleftarrow{\times d_1}\mathbb{Z}\xleftarrow{\times d_2}\cdots)$ and $\hat{\mathbb{Z}}$ is the separate profinite deck/transversal group [Tier 1]. The isomorphism $\check{H}^1 \cong \mathbb{Q}$ classifies integral Čech-cohomology classes of the solenoid; it does not assign an Agent an ordinary winding number. It does not by itself identify those classes with Agent states, quark charges, or physical memories. Any such interpretation requires an explicit comparison map from the relevant physical state space to $\check H^1$ and a dynamical preservation theorem. [Tier 1 — cohomology calculation; Tier 3 — physical interpretation open.]

**TAS.4 The Ultrametric Inequality and Resonance**

The hierarchical distance $d_H$ between two identity addresses $s_i, s_j$ in a selected 5-adic factor is defined by the 5-adic norm:
$$d_H(s_i, s_j) = 5^{-m}$$
where $m$ is the level of the first common branch node. More generally, a chosen divisibility chain $1=N_0\mid N_1\mid\cdots$ defines clopen cylinders $C_{k,a}=a+N_k\hat{\mathbb{Z}}$ and a compatible ultrametric $d_c(x,y)=c^{-r(x,y)}$ with $r(x,y)=\sup\{k:x\equiv y \pmod{N_k}\}$. The chain and the scale $c$ are chosen; the formula $5^{-m}$ applies to a selected $\mathbb{Z}_5$ factor or chosen filtration, not intrinsically to all of $\hat{\mathbb{Z}}$. The root is the whole level-zero transversal cylinder, not the connected Solenoid or a primordial subject, and extracting the transversal coordinate of a full Solenoid point requires a selected base fiber or local chart [Tier 1 given the choices].

**Properties:**
1. **Non-Archimedean:** $d_H(x, z) \le \max(d_H(x, y), d_H(y, z))$. This ensures that identity "clusters" (cylinders) are either nested or disjoint, rather than partially overlapping.
2. **Observer and memory ceiling:** Nested cylinders model shared coarse membership: distinct "finger" ends may belong to one "hand" cylinder at a declared resolution, and distinct ends remain distinct points even when they share a coarse cylinder. This does not establish that the cylinder is a Level II subject, that one end accesses every sibling state, or that ultrametric proximity transmits information. A single qualified **Identity Polaron** with several apertures is a Tier 3 default. Parent-level experience, cross-life recall, post-mortem recoupling and related survival interpretations are not derived by this topology; they remain Tier 4 speculation unless a physical projection/coupling and an ownership mechanism are derived.
