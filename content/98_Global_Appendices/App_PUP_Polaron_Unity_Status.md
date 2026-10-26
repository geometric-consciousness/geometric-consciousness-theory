### **Appendix PUP: Polaron Unity: Algebraic Status**

> **Cross-reference note:** This appendix records the mathematical status of Proposition 11.12.A (Polaron Unity), the disposition of which is referenced in V1 Ch11 §11.12.3, V1 Ch16 §16.2.7, App TCD §TCD.4 (Tier classification), App TAT §TAT.1 (Tier audit), and the Global Abstract. Background topology of $\Sigma_\infty$ lives in V1 Ch07 §7.2 and App TAS; the framed-ribbon knot $\mathcal{K}$ is defined in §PUP.2.3 (the former tethered-ribbon framework is retired; App CCD §CCD.4 now records only the standard $SU(2)$ rotation control).

> [!IMPORTANT]
> **Corrected disposition (v1.3.0).**
>
> 1. Knot-exterior topology gives a genuine finite-level free-indecomposability result (Lemma PUP.3.2: every knot group is freely indecomposable, by Kneser–Stallings; primeness is not used), conditional on the full-fibre support hypothesis $H_{PUP.1}^{\mathrm{fib}}$. It controls free products only.
> 2. The former Proposition PUP.1(ii), Hilbert-space non-factorizability, is **withdrawn**. Its load-bearing step, "a $\Gamma$-equivariant tensor factorization of the Hilbert space induces a direct-product factorization of $\Gamma$", is false, including for the regular/GNS representation. §PUP.4.2 gives an exact counterexample with the group $A_5$. The former open step (gap D) is therefore retired as false, not left open.
> 3. For the trefoil, the represented group of Definition PUP.2.5 is the knot group $\Gamma_\mathcal K=B_3$. Its centre $\langle\Delta^2\rangle\cong\mathbb Z$ is a nontrivial amenable normal subgroup, so O.35 (trivial amenable radical) is false as posed and the regular group von Neumann algebra $L(B_3)$ is not a factor (O.36). Both hold for the further central quotient $B_3/Z(B_3)\cong C_2*C_3$ [Tier 1 — standard]; whether any physical sector is that quotient's regular representation is open [Tier 3].
> 4. **Claim ceiling.** What survives is at most an *algebraic unity candidate*: a conditional statement about a specified observable algebra. It supplies no subject count, no owner, and no Level II verdict. Level II is open (Tier 3; V1 Ch16 §16.2.7, V1 Ch17 §17.1.3): no validated substrate criterion exists yet (it requires a typed, normalized, measured coupling, the Identity-Polaron construction and an independent phenomenal bridge; O.21/O.23/O.34, O.18).

---

#### PUP.1 Statement

Let $\Sigma_\infty = \varprojlim (S^1, z \mapsto z^n)$ denote the universal Adelic Solenoid (App TAS §TAS.1). By Pontryagin duality (App TAS §TAS.2),
$$\Sigma_\infty \;\cong\; (\mathbb{R} \times \hat{\mathbb{Z}})/\mathbb{Z}.$$
For each $n \geq 1$, let $X_n \cong S^1$ denote the $n$-th term in the inverse system, and let $p_n: \Sigma_\infty \to X_n$ be the canonical projection. For each $n$, the configuration space of an Identity Polaron at finite resolution $n$ is the product
$$M_n \;:=\; X_n \times E_\parallel \;\cong\; S^1 \times \mathbb{R}^3,$$
where $E_\parallel \cong \mathbb{R}^3$ is the physical projection slice of the adopted icosahedral cut-and-project ansatz (Parameter Ledger P1; App FTH §FTH.3; cf. Theorem FTH.1 for the conditional knot-dimension bound). Let $q_{nm}:M_m\to M_n$ be the ambient bonding maps and $\widetilde\Sigma_\infty:=\varprojlim_n(M_n,q_{nm})$. Projected knot cores and deleted supports are typed separately below.

Dimensional clarification: $M_n$ is a four-dimensional product. This appendix adopts one geometry consistently:
$$H_{PUP.1}^{\mathrm{fib}}:\quad \mathscr D_n:=X_n\times K_n\subset M_n,$$
where $K_n\subset E_\parallel$ is the projected framed-ribbon core and $\mathscr D_n$ is its full identity-fibre support. Consequently
$$M_n\setminus\mathscr D_n=X_n\times(E_\parallel\setminus K_n).$$
This **full-fibre complement hypothesis** is not the incompatible fixed-slice deletion $M_n\setminus(\{x_n^0\}\times K_n)$. The latter retains every point $(x,k)$ with $x\ne x_n^0$ and does not have the displayed product form. The formal proposition below is conditional on $H_{PUP.1}^{\mathrm{fib}}$; establishing that the physical Polaron carries full-fibre support, or replacing it with a genuine four-dimensional fixed-slice complement calculation, remains an O.18 modelling target.

Assume also $q_{nm}^{-1}(\mathscr D_n)=\mathscr D_m$. Then $q_{nm}$ restricts to the complements. Set
$$\mathscr D_\mathcal K:=\varprojlim_n\mathscr D_n,\qquad
\widetilde\Sigma_\infty\setminus\mathscr D_\mathcal K\cong\varprojlim_n(M_n\setminus\mathscr D_n).$$

> **Proposition PUP.1 (Polaron Unity Proposition, revised; conditional on O.18 and $H_{PUP.1}^{\mathrm{fib}}$) [Tier 3 conditional; part (ii) withdrawn].**
> *Let $\mathscr D_\mathcal K\subset\widetilde\Sigma_\infty$ be the inverse limit of complement-compatible full-fibre supports $\mathscr D_n=X_n\times K_n$. Then:*
>
> *(i) **Complement fundamental pro-group.** The inverse-limit topological group*
> $$\Pi_\mathcal K:=\varprojlim_n\pi_1(M_n\setminus\mathscr D_n),$$
> *is freely indecomposable: it admits no non-trivial free-product decomposition $G_1 * G_2$ with $G_1, G_2 \neq 1$.*
>
> *(ii) **Withdrawn.** The former claim that the canonical representation space $\mathcal H_\mathcal K$ of the represented quotient $\Gamma_\mathcal K$ admits no $\Gamma_\mathcal K$-equivariant tensor product decomposition is withdrawn. The bridge it relied on is false (§PUP.4.2, Counterexample PUP.4.2.B). No Hilbert-space non-factorizability statement is made in this appendix.*
>
> *(iii) **Uniqueness of the invariant normalized density (conditional lemma).** If $\mathcal M=\rho(\Gamma_\mathcal K)''$ is a finite factor with normalized trace $\tau$, a positive, unit-trace, Zeno-invariant density $R_{\rm inv}\in\mathcal M$ commuting with $\rho(\Gamma_\mathcal K)$ is uniquely $\mathbf1$. This is a density/state statement, not a uniqueness theorem for the canonical non-unitary Selection Operator $\mathcal F_{sel}=\mathcal P_{actualize}\circ\mathcal U_{steer}$. For the trefoil its hypothesis fails in the regular representation of $\Gamma_\mathcal K=B_3$, because $L(B_3)$ is not a factor (O.36, §PUP.6); (iii) therefore applies only to a factorial sector that has not been physically identified.*

The argument proceeds via four lemmata and one finite-level remark (§PUP.3). Lemmata PUP.3.2, PUP.3.4, and PUP.3.5 have the scopes stated below; Remark PUP.3.3 records finite-level evidence without pretending to prove an inverse-limit theorem. Lemma PUP.3.1 is conditional on the explicitly adopted full-fibre hypothesis $H_{PUP.1}^{\mathrm{fib}}$. Lemma PUP.3.4 — the identification of the abstract Gelfand–Naimark–Segal (GNS) representation associated with $\mathcal{K}$ with the *physical* phason Hilbert space — remains an open structural gap. Section PUP.4.2 records why the former direct-product/operator-factor step is false rather than open. O.35 (unique trace) and O.36 (factoriality of the regular algebra) fail as posed for the represented trefoil group $\Gamma_\mathcal K=B_3$ and hold for the further central quotient $B_3/Z(B_3)\cong C_2*C_3$ (§PUP.6). Together with the Anderson-Putnam extension to $S^3 \setminus K$ (Open Problem O.18) and the canonicity assignment $K \mapsto \mathcal{A}_K$, these items define the conditional structure on which parts (i) and (iii) rest.

> **Claim ceiling.** Even with every listed closure, the content of this appendix is at most an algebraic unity candidate. No theorem here identifies an Identity Polaron, an owner, one subject, any other subject count, or Level II Apperception; those require independent physical and phenomenal bridges (V1 Ch16 §16.2.7).

---

#### PUP.2 Preliminaries

##### PUP.2.1 The Adelic Solenoid revisited

The space $\Sigma_\infty$ is the inverse limit of the system $\{X_n, f_{nm}\}_{n \mid m}$ where $X_n \cong S^1$ and $f_{nm}(z) = z^{m/n}$. As a topological group,
$$\Sigma_\infty \;\cong\; (\mathbb{R} \times \hat{\mathbb{Z}})/\mathbb{Z},$$
with $\hat{\mathbb{Z}} = \varprojlim \mathbb{Z}/n\mathbb{Z}$ the profinite completion of the integers. The space is compact, connected, but not locally path-connected; locally, $\Sigma_\infty \cong \mathbb{R} \times \mathcal{C}$ where $\mathcal{C}$ is a Cantor set (App TAS §TAS.1).

The three inverse-limit objects used here must be kept distinct. The profinite group
$$\hat{\mathbb Z}=\varprojlim_n\mathbb Z/n\mathbb Z$$
is the totally disconnected fibre (address group) in the quotient presentation above. The Čech/shape fundamental invariant of $\Sigma_\infty$ is instead the pro-group represented by
$$\bigl\{\pi_1(X_n)\cong\mathbb Z,\ (f_{nm})_*=\times(m/n)\bigr\}_{n\mid m}.$$
It is this inverse system, rather than a single group isomorphic to $\hat{\mathbb Z}$, that shape theory assigns to the solenoid. Finally, the ordinary group inverse limit of this integer system is trivial: compatibility would require an integer divisible by every positive degree. These statements concern the solenoid itself and do not classify the later knot-complement pro-group. [Tier 1 — Standard inverse-limit and shape theory.]

##### PUP.2.2 The augmented configuration space

A Polaron at finite resolution $n$ is a framed ribbon embedded in the augmented configuration space
$$M_n \;=\; X_n \times E_\parallel \;\cong\; S^1 \times \mathbb{R}^3.$$
The $S^1$ factor records the identity-fiber coordinate at depth $n$; the $\mathbb{R}^3$ factor is the physical slice. The augmented inverse-limit space
$$\widetilde{\Sigma}_\infty \;:=\; \varprojlim_n M_n \;=\; \Sigma_\infty \times E_\parallel$$
is the proposed home of the Polaron knot, replacing the heuristic phrase "$\mathcal{K} \subset \Sigma_\infty$" that appears in the Chapter 11 statement. The replacement is motivated, not forced: knotting of one-dimensional defects needs a three-dimensional ambient slice (cf. Theorem FTH.1), and the bare solenoid $\Sigma_\infty$ has local Lebesgue dimension one, so a knot cannot sit in $\Sigma_\infty$ itself. The physical slice $E_\parallel \cong \mathbb{R}^3$ supplies the three transverse dimensions, while the solenoid fiber records the identity address. That a physical Polaron is confined to such a slice, with the support required by $H_{PUP.1}^{\mathrm{fib}}$, is a Tier 3 modelling hypothesis under O.18; the Chapter 11 Polaron ansatz does not establish it. A single fixed-slice copy of the knot does not give the product complement (§PUP.1). Within the model, this is the sense in which the Polaron is a knot "in the solenoid": it is a knot in the augmented total space whose ambient projection onto the identity factor recovers the address path of Chapter 7 §7.4.

##### PUP.2.3 Definition of the Polaron knot $\mathcal{K}$

> **Definition PUP.2.3 (Polaron knot and full-fibre support).** A Polaron knot is an inverse system $\mathcal{K}=(K_n,\iota_{nm})$ where:
> 1. For each $n$, $K_n\subset E_\parallel$ is the core $\kappa_n(S^1\times\{\tfrac12\})$ of a smoothly embedded framed ribbon $\kappa_n:S^1\times[0,1]\hookrightarrow E_\parallel$ and is a tame prime knot in the standard three-dimensional sense (Burde–Zieschang, *Knots*, §3).
> 2. The bonding maps $\iota_{nm}:K_m\to K_n$ form a coherent system induced by the declared finite-resolution construction.
> 3. Under $H_{PUP.1}^{\mathrm{fib}}$, the corresponding deleted defect support in $M_n$ is $\mathscr D_n=X_n\times K_n$. This full-fibre support, rather than a single-slice copy $\{x_n^0\}\times K_n$, is the object whose complement is used below.
> 3a. Ambient bonding maps satisfy $q_{nm}^{-1}(\mathscr D_n)=\mathscr D_m$, hence restrict to maps of supports and complements.
> 4. The framing is non-trivial: the linking number of the two ribbon edges $\kappa_n(S^1 \times \{0\})$ and $\kappa_n(S^1 \times \{1\})$ (with $\kappa_n$ the ribbon embedding of item 1) equals $N$, the braid index of the underlying Polaron condensate.

The condition that the projected core be prime at each finite level is the rigorous translation of the Chapter 11 §11.12.2 phrase "the link reduces to an irreducible knot whose peripheral structure is trivial only for the full $N$-component system." Primeness is asserted for $K_n\subset E_\parallel$, while the complement calculation is asserted for its full-fibre support $\mathscr D_n\subset M_n$; the two object types are not conflated. Primeness of a knot is not the same as irreducibility of its exterior (§PUP.3, scope note after Lemma PUP.3.2); the free-indecomposability step uses only the latter, which holds for prime and composite knots alike.

##### PUP.2.4 The Wirtinger pro-system

For each $n$, $H_{PUP.1}^{\mathrm{fib}}$ gives the product complement exactly:
$$M_n\setminus\mathscr D_n=X_n\times(E_\parallel\setminus K_n).$$
Its knot-group factor admits a **Wirtinger presentation**
$$G(K_n)=\pi_1(E_\parallel\setminus K_n)=\langle x_1,\ldots,x_{k_n}\mid r_1^{(n)},\ldots,r_{k_n-1}^{(n)}\rangle,$$
where the $x_i$ are meridians of $K_n$ and the $r_j^{(n)}$ are the crossing relations (Burde–Zieschang §3.B). The bonding maps induce group homomorphisms
$$\varphi_{nm}:\pi_1(M_m\setminus\mathscr D_m)\to\pi_1(M_n\setminus\mathscr D_n).$$
Define the complement fundamental pro-group
$$\Pi_\mathcal K:=\varprojlim_n\pi_1(M_n\setminus\mathscr D_n).$$
The finite-level knot groups are generally infinite, so this inverse limit is not called profinite. A profinite group would require a separately constructed inverse system of finite quotients or completions. [Tier 3 conditional; inverse-limit free indecomposability remains open.]

##### PUP.2.5 The canonical phason representation $\mathcal{H}_\mathcal{K}$

In the model, each meridian generator $x_i$ is posited to act on phason modes of the lattice as a holonomy of a phason gauge connection around the knot core, and the action is posited to be unitary for the phason inner product. Both are Tier 3 modelling hypotheses: no phason gauge connection around a knot core has been derived, and no engine calculation establishes this holonomy representation. Let
$$\rho:\Gamma_\mathcal K\to\mathcal U(\mathcal H_\mathcal K)$$
denote this posited unitary representation, where $\mathcal{H}_\mathcal{K}$ is constructed as follows.

> **Definition PUP.2.5 (Canonical phason Hilbert space).** Let $\mathcal{A}_\mathcal{K} := C^*_r(\Gamma_\mathcal{K})$ denote the reduced group C\*-algebra of the represented discrete knot group after the central $\mathbb{Z}$ factor supplied by the full-fibre product complement has been quotiented out. For the trefoil this group is the knot group $\Gamma_\mathcal K=B_3$ itself, whose own centre $\langle\Delta^2\rangle\cong\mathbb Z$ is nontrivial. The Zeno boundary condition (§PUP.2.6) was intended to select a distinguished tracial state $\tau$ on $\mathcal{A}_\mathcal{K}$ through the unique-trace hypothesis registered as O.35; for $B_3$ that hypothesis fails (§PUP.2.6, §PUP.6), so $\tau$ below denotes the canonical regular trace, chosen rather than selected. The canonical phason Hilbert space $\mathcal{H}_\mathcal{K}$ is the GNS Hilbert space of $(\mathcal{A}_\mathcal{K}, \tau)$.

This construction is standard in operator-algebraic representation theory (Brown–Ozawa, *C\*-algebras and Finite-Dimensional Approximations*, §1.5).

##### PUP.2.6 The Zeno boundary condition

The hypothesised Zeno Drive of Chapter 17 §17.1.2 (Tier 3) is modelled as imposing a continuous projective measurement of the singlet state of the Trp radical pair network. The picture uses the historical 100 MHz material-scan scenario (the imported $\sim10^8$ s${}^{-1}$ spin-selective recombination timescale of the radical-pair scenario) as a placeholder only; it is not an operating Zeno cadence, and no Zeno measurement rate is derived (V1 Ch17 §17.1.3; V3 Ch13 §13.4.7). Mathematically, the model treats the boundary as a conditional expectation onto the represented trace-bearing algebra:
$$\mathbb{E}_{Zeno}: \mathcal{A}_\mathcal{K} \to \mathcal{Z}(\mathcal{A}_\mathcal{K}).$$
That the physical Zeno map equals such a trace-preserving conditional expectation is itself a Tier 3 hypothesis.

> **Definition PUP.2.6 (Zeno Boundary) [Tier 3 modelling hypothesis; its physical Zeno-Drive realization is Tier 3].** The Zeno boundary is proposed to select a distinguished faithful normalized trace on $\mathcal{A}_\mathcal{K}=C^*_r(\Gamma_\mathcal{K})$, the reduced group C\*-algebra of the represented discrete quotient introduced in Definition PUP.2.5 after quotienting the full-fibre product's central $\mathbb{Z}$ factor. That trace would be *the* unique one only if condition (a) below held; for the trefoil group $B_3$ condition (a) fails, so no unique trace exists and the selection is hypothetical. The pro-group $\Pi_\mathcal K$ supplies inverse-system control data; the BKKO theorem is invoked only for $\Gamma_\mathcal K$, and would require:
> (a) $\Gamma_\mathcal{K}$ has the unique-trace property, equivalently trivial amenable radical in the Breuillard-Kalantar-Kennedy-Ozawa theorem (2017, Theorem 1.3, arXiv:1410.2518). C\*-simplicity is a stronger separate condition and is not asserted here; and
> (b) the central $\mathbb{Z}$ factor introduced by the full-fibre product split in Lemma PUP.3.1 is explicitly quotiented out before the trace is taken.
>
> Residual finiteness is not required to define the displayed pro-system or to invoke the BKKO unique-trace criterion for the represented discrete quotient. It becomes relevant only for an optional route through separating finite quotients or a separately constructed profinite completion, and it is not sufficient for trace uniqueness. Trivial amenable radical in the sense of BKKO is the operative condition, registered as Open Problem **O.35**. For the trefoil the represented group is $B_3$, whose centre $\langle\Delta^2\rangle\cong\mathbb Z$ is a nontrivial amenable normal subgroup. Its amenable radical is therefore nontrivial, condition (a) fails, and $C^*_r(B_3)$ does not have a unique trace. O.35 as posed thereby fails for the represented group $B_3$ [Tier 1 — standard]. A further quotient by the knot group's own centre is a possible repair route: for $B_3/Z(B_3)\cong C_2*C_3$ the amenable radical is trivial, so O.35/O.36 hold there [Tier 1 — standard]. That route is not developed in this edition, and whether any physical sector is that quotient's regular representation is open [Tier 3].

> **Definition PUP.2.6b (Invariant normalized density).** Let $R_{\rm inv}\in L(\Gamma_\mathcal K)$ be the density, relative to $\tau$, of a normal state that is:
> (a) positive,
> (b) of unit trace under $\tau$,
> (c) invariant under the Zeno conditional expectation $\mathbb{E}_{Zeno}$, and
> (d) invariant for the represented knot-group action: $[R_{\rm inv},\rho(g)]=0$ for every $g\in\Gamma_\mathcal K$.

Proposition PUP.1(iii) says these conditions determine $R_{\rm inv}$ whenever the represented algebra is a finite factor; for the trefoil regular representation it is not (§PUP.6). The canonical Selection Operator is instead the non-unitary branch-selecting process $\mathcal F_{sel}=\mathcal P_{actualize}\circ\mathcal U_{steer}$ (Ch06 §6.4.1; Ch10 §10.4.1); it is not a normalized density and is not proved equal to the identity here.

---

#### PUP.3 Lemmata

##### Lemma PUP.3.1 (Wirtinger presentation at each finite level) [Tier 3 conditional on $H_{PUP.1}^{\mathrm{fib}}$]

*For each $n \geq 1$, if the defect support satisfies $H_{PUP.1}^{\mathrm{fib}}$, the group $\pi_1(M_n \setminus \mathscr D_n)$ is
$$\pi_1(M_n \setminus \mathscr D_n)\cong\mathbb Z\times G(K_n),$$
where $G(K_n)$ has the finite Wirtinger presentation
$$G(K_n)=\langle x_1, \ldots, x_{k_n} \mid w_i x_{\sigma(i)} w_i^{-1} = x_{\tau(i)},\; i = 1, \ldots, k_n - 1 \rangle.$$
The $x_i$ are meridians and the relations are determined by crossings of a planar projection of the projected knot core $K_n\subset E_\parallel$.*

*Proof.* By $H_{PUP.1}^{\mathrm{fib}}$, $\mathscr D_n=X_n\times K_n$ and hence
$$M_n\setminus\mathscr D_n=X_n\times(E_\parallel\setminus K_n).$$
With $\pi_1(X_n)\cong\mathbb Z$, the product theorem gives the displayed $\mathbb Z\times G(K_n)$ split. The $X_n$ generator commutes with every meridian, and the presentation of $G(K_n)$ is the classical Wirtinger presentation (Burde–Zieschang §3.B). No product claim is made for deletion of a single fixed-slice ribbon or for an arbitrary four-dimensional ribbon embedding. $\square$

A useful conditional corollary: after quotienting the central $\mathbb{Z}$ generator under $H_{PUP.1}^{\mathrm{fib}}$, the finite-level group is the classical knot group $G(K_n)$. We use this corollary only with that hypothesis in force.

##### Lemma PUP.3.2 (Kneser–Stallings: knot groups are freely indecomposable) [Tier 1]

*Let $K \subset S^3$ (equivalently $\mathbb{R}^3$) be a knot (prime or composite). Then the knot group $G(K) = \pi_1(\mathbb{R}^3 \setminus K)$ is **freely indecomposable**: there exist no non-trivial subgroups $H_1, H_2 < G(K)$ such that $G(K) = H_1 * H_2$.*

*Proof.* This is a classical theorem of 3-manifold topology, resting on Kneser's conjecture, proved by Stallings (1959; see also Stallings 1971) with the boundary case by Heil (1972): a free-product decomposition of the fundamental group of a compact 3-manifold is realized geometrically by an essential embedded 2-sphere or properly embedded disc. Stallings' proof uses the Papakyriakopoulos sphere/loop-theorem machinery (Loop Theorem: Papakyriakopoulos 1957, generalized by Stallings 1960), but the step used here is Kneser's conjecture, not the Loop Theorem itself. The argument: the exterior $X_K = S^3 \setminus N(K)$ (where $N(K)$ is an open tubular neighborhood) is irreducible (Hatcher, *Notes on Basic 3-Manifold Topology*, §1.2), which rules out an essential 2-sphere. For a non-trivial knot its torus boundary is incompressible, which rules out an essential disc; for the unknot $G(K)\cong\mathbb Z$, which is freely indecomposable directly. Hence $G(K)$ is freely indecomposable. $\square$

> **Scope of the hypothesis.** Irreducibility of the exterior is not equivalent to primeness of $K$: exteriors of composite knots are irreducible as well, and a connected sum is detected in the exterior by an essential decomposing annulus rather than by a 2-sphere. Kneser–Milnor decomposes 3-manifolds along spheres and does not supply that equivalence. Free indecomposability above follows from irreducibility of the exterior (with boundary incompressibility for a non-trivial knot, or $G(K)\cong\mathbb Z$ for the unknot), not from primeness; where primeness itself is needed it is taken through the annular criterion, not inferred from irreducibility.

This is the deepest classical ingredient. The proof rests on Kneser's conjecture (Stallings' theorem, whose proof uses the Papakyriakopoulos–Stallings loop/sphere-theorem machinery) together with irreducibility and boundary-incompressibility of knot exteriors, all foundational results in three-manifold topology.

##### Remark PUP.3.3 (Finite-resolution free-indecomposability control; no inverse-limit theorem) [Tier 1 finite-level fact; inverse-limit closure open under O.18]

For the registered inverse system $\{G_n,\varphi_{nm}\}$, Lemma PUP.3.2 proves free indecomposability separately for each finite-resolution knot group $G_n$. This sentence is only a record of those finite-level facts; it is not an implication about $\widehat G=\varprojlim_nG_n$. Whether $\widehat G$ is freely indecomposable requires an additional inverse-limit theorem for this actual pro-system and remains an O.18 closure target.

> **Remark PUP.3.3.A [Tier classification].** Finite-level Kneser–Stallings control is Tier 1. Inverse-limit promotion is Tier 3/O.18 and requires a theorem for the actual pro-system $\Pi_\mathcal K$. Profinite Bass–Serre results do not apply unless finite completions are separately constructed.

##### Lemma PUP.3.4 (Identification of canonical and physical phason representations) [Tier 3 conditional pending O.18 full-fibre-support closure + finite quotient trace + O.32; O.35/O.36 fail as posed for the trefoil, §PUP.6]

*Let $\mathcal{H}_\mathcal{K}^{phys}$ denote the proposed physical phason Hilbert space of a future realized Polaron branch, conditional on the full coupling and structural closure program. Let $\mathcal{H}_\mathcal{K}^{can}$ denote the canonical GNS Hilbert space of Definition PUP.2.5. Then there exists a $\Gamma_\mathcal K$-equivariant unitary isomorphism
$$U: \mathcal{H}_\mathcal{K}^{phys} \;\xrightarrow{\sim}\; \mathcal{H}_\mathcal{K}^{can}$$
intertwining the physical phason holonomy action with the canonical regular representation.*

*Status.* The Lemma is the structural bridge from operator-algebraic representation theory (where Lemmata PUP.3.1–PUP.3.3 and Lemma PUP.3.5 below operate) to the *physical* Hilbert space of the Polaron condensate (where Proposition 11.12.A is to be applied). It is the analogue, for the Polaron knot, of the proposed Connes–Chamseddine spectral-triple identification of the GCT vacuum (V3 Ch06 §6.5, Tier 3; its KO-dimension-6 verification is App ORQ O.32) — and it would reduce to that identification if the spectral-triple identification were granted.

*What is reduced.* Granting the spectral-triple identification of V3 Ch06 §6.5 (Tier 3 conditional on O.32/O.5), the physical phason Hilbert space at a fixed lattice configuration is modeled by the finite-subshift analogue of the AKN tiling algebra. The full AKN tiling algebra is governed by tiling-groupoid / substitution machinery rather than being canonically identical to a Cuntz–Krieger algebra of one finite adjacency matrix (cf. Putnam, *C\*-algebras from substitution tilings*). The Polaron knot defines a specific representation of $\Pi_\mathcal K$ inside this finite-subshift analogue — namely, the holonomy representation around the meridians of $\mathcal{K}$. The required equivariance $U$ is then the GNS realization of the holonomy state.

*What is open.* The remaining gap, marked Tier 3 conditional until the registered closure stack is supplied, is the following structural verification:

> **Open structural step (the L4 gap).** Work throughout on the declared reduced group algebra $\mathcal A_\mathcal K=C_r^*(\Gamma_\mathcal K)$ and its finitely generated meridian C\*-subalgebra $B_\mathcal K=C^*(\rho(x_1),\ldots,\rho(x_k))\subset\mathcal A_\mathcal K$. First verify that the physical holonomy/Zeno state restricted to $B_\mathcal K$ equals $\tau|_{B_\mathcal K}$. If an expectation-level comparison is also required, define both conditional expectations with the same domain and codomain and prove their equality separately. Equality of restricted states and equality of conditional expectations are not equivalent statements, and neither has yet been derived from the other.

Finite generation by the $k_n$ meridian unitaries does not make $B_\mathcal K$ finite-dimensional. The trefoil $M_2(\mathbb C)$ calculation is therefore a finite-matrix surrogate only. Closing the lemma requires a faithful represented model or a controlled family of finite representations, together with convergence and trace-descent results connecting that model to $B_\mathcal K\subset\mathcal A_\mathcal K$. Until those results are supplied, the Lemma inherits the Tier 3 conditional disposition from §PUP.6.3a/b. $\square$

##### Lemma PUP.3.5 (Factoriality / central-decomposition control) [Tier 1 standard fact under its hypothesis; the hypothesis fails for the trefoil regular representation]

*Suppose $\rho$ is a primary representation of $G$ on $\mathcal{H}$. Then $\rho(G)''$ is a factor, so the represented sector has trivial center and no non-trivial direct-integral/central decomposition. This controls central decomposition; it does not by itself exclude every $G$-equivariant tensor-product factorization.*

*Remark.* The factorial-representation hypothesis is essential: a non-primary representation can have absence of tensor decomposition without $\rho(G)''$ being a factor. For example, take $G=\mathbb{Z}/2$ acting on $\mathbb{C}^2$ by $\mathrm{diag}(1,-1)$. Then $\rho(G)''=\mathbb{C}\oplus\mathbb{C}$ is not a factor, but no tensor decomposition with both factors of dimension at least $2$ exists. For the represented knot group at hand, primary-representation status was registered as the closure target of **O.36**. For the trefoil, the regular representation of $\Gamma_\mathcal K=B_3$ is not primary: the infinite centre $\langle\Delta^2\rangle$ generates a diffuse centre of $L(B_3)$, so $L(B_3)$ is not a factor [Tier 1 — standard].

*Proof sketch.* For primary representations, factoriality is exactly the trivial-center condition for $\rho(G)''$ (Takesaki, *Theory of Operator Algebras I*, §V.1). A non-trivial central decomposition of a primary representation would contradict the primary hypothesis. Excluding tensor-product factorizations would require additional hypotheses on commuting subfactor pairs or on the represented tensor factors; no such exclusion follows from group-level indecomposability, because the former PUP.4.2 bridge is false (Counterexample PUP.4.2.B). The lemma is therefore a central-decomposition statement inside a represented primary sector, not a tensor-prime theorem for arbitrary unitary representations. $\square$

*Caveat on type.* This Lemma asserts factoriality, not a Murray–von Neumann type. A profinite completion of the complement pro-group has not been constructed. The represented countable discrete quotient $\Gamma_\mathcal K$ has a Type II$_1$ regular algebra only if it is i.c.c.; the trefoil group $B_3$ is not i.c.c., since its central elements have one-element conjugacy classes. At finite resolution the algebra is generally $\bigoplus_jM_{d_{n,j}}(\mathbb C)$ and is one factor only in a primary sector. Invariance places $R_{\rm inv}$ in the center; this statement does not constrain $\mathcal F_{sel}$.

---

#### PUP.4 Argument for Proposition PUP.1

We treat the three parts in sequence, citing the Lemmata. Part (ii) is withdrawn; §PUP.4.2 records why.

##### PUP.4.1 Proof of (i) — Free indecomposability of $\Pi_\mathcal K$

Let $\mathcal{K}$ be a Polaron knot in the sense of Definition PUP.2.3 and assume $H_{PUP.1}^{\mathrm{fib}}$. By Lemma PUP.3.1, for each finite resolution $n$, $\pi_1(M_n \setminus \mathscr D_n) \cong \mathbb{Z} \times G(K_n)$. The projected core $K_n\subset E_\parallel$ is a knot, so after quotienting the central $\mathbb Z$ factor, $G(K_n)$ is freely indecomposable by Lemma PUP.3.2 (primeness, assumed in Definition PUP.2.3, is not used in this step).

Remark PUP.3.3 records finite-level controls but no inverse-limit implication. Promotion to $\Pi_\mathcal K$ remains O.18. $\square$

##### PUP.4.2 Status of (ii) — withdrawn: the tensor-factor bridge is false

The former argument for (ii) granted Lemma PUP.3.4, so that the physical phason Hilbert space $\mathcal{H}_\mathcal{K}^{phys}$ would be canonically isomorphic to the GNS Hilbert space $\mathcal{H}_\mathcal{K}^{can}$ of the represented discrete quotient $\Gamma_\mathcal K$, and then sought to exclude every $\Gamma_\mathcal K$-equivariant tensor decomposition of that space.

Two steps were needed. First, Lemma PUP.3.2 establishes **free** indecomposability of the finite-level knot groups; it does not establish **direct-product** indecomposability. A freely indecomposable group can still split as a direct product (abelian groups supply elementary examples). Second, and decisively, the former closure target assumed that an equivariant tensor decomposition of the representation space would induce a direct-product decomposition of the group. That implication is false.

An equivariant tensor presentation means
$$U\rho(g)U^*=\rho_A(g)\otimes\rho_B(g)\qquad(g\in\Gamma),$$
with the same group acting diagonally on both factors. It does not require the group itself to decompose.

> **Counterexample PUP.4.2.B (equivariant tensor factorization without group factorization) [Tier 1].** Order the conjugacy classes of the alternating group $A_5$ (order 60) as $1A, 2A, 3A, 5A, 5B$, and write $\bar\phi=(1-\sqrt5)/2$. Among its irreducible characters are
> $$\chi_3=(3,-1,0,\phi,\bar\phi),\quad \chi_{3'}=(3,-1,0,\bar\phi,\phi),\quad \chi_4=(4,0,1,-1,-1),\quad \chi_5=(5,1,-1,0,0).$$
> Let $W=V_3\oplus V_{3'}\oplus V_4\oplus 2V_5$, so that $\chi_W=(20,0,-1,0,0)$ (using $\phi+\bar\phi=1$). Then
> $$\chi_{V_3\otimes W}=\chi_3\,\chi_W=(60,0,0,0,0)=\chi_{\rm reg}.$$
> Since a finite-group representation is determined by its character, $\ell^2(A_5)\cong V_3\otimes W$ as $A_5$-representations, with both factors non-trivial. This holds in particular for the canonical regular/GNS Hilbert space of $(C^*_r(A_5),\tau_{\rm reg})$. Yet $A_5$ is a nonabelian simple group and has no non-trivial direct-product decomposition. Hence
> $$\text{equivariant Hilbert-space tensor factorization}\;\not\Rightarrow\;\text{direct-product group factorization}.$$

The former "PUP.4.2 direct-product/operator-factor gap" (gap D of §PUP.6.3b) is therefore retired as false, not left open. Part (ii) of Proposition PUP.1 is withdrawn. Because regular representations of indecomposable groups can carry such equivariant tensor coordinates, their absence is not the right invariant for a unity claim.

> **Remark PUP.4.2.A (What a correct target would look like).** Free indecomposability remains useful because it blocks one class of fragmentation of the Polaron complement. A meaningful unity statement would instead have to concern an *observable algebra*: first produce commuting, state-compatible observable subalgebras corresponding to an independently defined physical bipartition, then show that the represented von Neumann algebra admits no decomposition into two diffuse factors along it. Such an algebraic primeness statement, even if proved, would bound only the algebra. It would not forbid arbitrary Hilbert-space tensor coordinates, and it would not supply an owner, a subject count or Level II. No construction of this kind is developed in this edition.

##### PUP.4.3 Proof of (iii) — Uniqueness of $R_{\rm inv}$ (conditional lemma)

We work in the finite von Neumann algebra $\mathcal M=\rho(\Gamma_\mathcal K)''$ acting on $\mathcal H_\mathcal K^{can}$, where $\Gamma_\mathcal K$ is the countable discrete group arising from the inverse-system control data, and we *assume* that $\mathcal M$ is a factor. O.35 and O.36 were meant to supply the distinguished trace and that factoriality. For the trefoil, neither holds in the regular representation $L(B_3)$ (§PUP.2.6, Lemma PUP.3.5), so the argument below applies only to a factorial sector whose physical identification is open [Tier 3].

**Uniqueness step.** Condition (d) in Definition PUP.2.6b gives
$$R_{\rm inv}\in\rho(\Gamma_\mathcal K)' .$$
Because $R_{\rm inv}\in\mathcal M$, it follows that $R_{\rm inv}\in Z(\mathcal M)$. If $\mathcal M$ is a factor, $R_{\rm inv}=c\mathbf1$; positivity and normalized unit trace give $c=1$. Thus $R_{\rm inv}=\mathbf1$ uniquely. This density/state proof is not a proof that $\mathcal F_{sel}=\mathbf1$.

If $\Gamma_\mathcal K$ is additionally i.c.c., its regular group von Neumann algebra is Type II$_1$ (Murray–von Neumann 1943; Takesaki §V.7.1). That type classification is separate from the uniqueness proof. At finite resolution the represented algebra is generally a direct sum of matrix blocks and is a factor only after restricting to a primary sector.

The conclusion is only that the invariant normalized density is unique. The canonical Selection Operator remains the non-unitary branch selector $\mathcal F_{sel}=\mathcal P_{actualize}\circ\mathcal U_{steer}$. $\square$

> **Remark PUP.4.3.A (Finite-resolution sanity check).** At finite resolution,
> $$L_n:=\rho_n(G(K_n))''\cong\bigoplus_jM_{d_{n,j}}(\mathbb C).$$
> It is one matrix factor only in a primary sector. Without that restriction, an equivariant density lies in the blockwise center and normalization alone need not fix all block weights, so winner-specific uniqueness is not automatic. In a primary sector, the same commutation-plus-factoriality argument gives $R_{{\rm inv},n}=\mathbf1$. It does not constrain the canonical non-unitary $\mathcal F_{sel}$. A classical knot group may remain infinite even though its represented algebra is finite dimensional; no finite-group or i.c.c. claim is inferred from the truncation.

---

#### PUP.5 Interpretation and remarks

##### PUP.5.1 Proposed phenomenal interpretation

> **Corollary PUP.5.1 (Proposed phenomenal interpretation) [Tier 3; no subject count, owner or Level II].** With part (ii) of Proposition PUP.1 withdrawn, no non-factorizability result is available to support phenomenal unity. What remains is a conditional algebraic statement — (i), and (iii) for a factorial sector — which a separately stated phenomenal bridge might interpret as an algebraic unity candidate. The uniqueness of $R_{\rm inv}$ in (iii) is a density statement only; it does not prove uniqueness of the non-unitary Selection Operator.

Any such interpretation inherits the full closure stack: physical justification of $H_{PUP.1}^{\mathrm{fib}}$, inverse-limit promotion, a faithful represented meridian model or controlled finite-representation family with convergence and trace descent, the Anderson-Putnam extension, identification of a physical factorial sector (O.35/O.36 fail as posed for the trefoil regular representation), O.32, and the Tier 3 phenomenal-identification bridge. Even if all of these closed, the result would be at most an algebraic unity candidate: it would not by itself identify an Identity Polaron, an owner, one subject or Level II.

##### PUP.5.2 Candidate controls do not define the Aggregate–Polaron boundary

> **Remark PUP.5.2 (Finite-level knot type is discrete) [Tier 1 finite-level fact; no physical phase-boundary claim].** *Knot type is a topological invariant with values in a discrete set, so at each finite resolution a change in the prime-decomposition type of the projected core $K_n$ is a discrete change.*

This remark does not formalize a physical Aggregate–Polaron phase boundary, and it does not make that boundary sharp. Whether any physical transition tracks knot type depends on the inverse-limit, physical-realization and coupling questions above, all of which are open; the candidate material controls (nuclear spin, chirality) do not define a binary boundary (V1 Ch16 §16.2.6).

##### PUP.5.3 Split links (illustration only)

> **Remark PUP.5.3 (Split-link illustration) [Tier 3 illustration; not a substrate verdict].** *If a configuration projected at every finite resolution to a split link $\mathcal{L}_n = \mathcal{K}_n^{(1)} \sqcup \mathcal{K}_n^{(2)} \sqcup \cdots$, the fundamental group of its complement would be a non-trivial free product of the component knot groups (van Kampen's theorem applied to the disjoint complements), and part (i) would not apply to it.* Failure of primeness does not by itself give split-link topology — a connected sum of two trefoils is non-prime yet is a single-component knot — and no derivation shows that a thermally decohered Class 0 configuration (V1 Ch11 §11.4.1) projects to a split link [Tier 3 premise].

This remark is not a formulation of "a rock has no unity". A free-product group says nothing, by itself, about Hilbert-space factorization (§PUP.4.2), and nothing here shows that any Class 0 system lacks unity, phenomenal character or Level II. The Level II status of every substrate is open (Tier 3; V1 Ch16 §16.2.7). The remark makes no existence or uniqueness claim about the canonical non-unitary $\mathcal F_{sel}$.

---

#### PUP.6 Remaining gap (Lemma PUP.3.4) — modular reduction list

The argument above closes Lemma PUP.3.2 at each finite level; Remark PUP.3.3 explicitly leaves inverse-limit promotion open. Lemma PUP.3.5 applies only to a primary representation, which the trefoil regular representation is not. Lemma PUP.3.1 is exact under the declared full-fibre support hypothesis $H_{PUP.1}^{\mathrm{fib}}$; physical justification of that support model remains an O.18 target. The remaining open gap is **Lemma PUP.3.4**: identifying the physical phason Hilbert space with a canonical GNS Hilbert space.

**O.35/O.36 status [Tier 1 — standard; physical identification Tier 3].** O.35/O.36 fail as posed for the represented trefoil group $B_3$ (its centre $\langle\Delta^2\rangle$ makes the amenable radical nontrivial and $L(B_3)$ non-factorial) and hold for the further central quotient $B_3/Z(B_3)\cong C_2*C_3$ [Tier 1 — standard]; whether any physical sector is that quotient's regular representation is open [Tier 3]. Concretely, O.35 (trivial amenable radical, hence unique trace) is false as posed for $\Gamma_\mathcal K=B_3$ of Definition PUP.2.5, and O.36 fails for its regular/GNS representation.

The Lemma PUP.3.4 gap is not reducible to a single finite-dimensional verification. The finite-matrix calculation is diagnostic; convergence, faithful representation, and trace descent to the declared meridian subalgebra remain open:

| Step | Required | Status |
|---|---|---|
| PUP.6.0 | Full-fibre support $H_{PUP.1}^{\mathrm{fib}}$: $\mathscr D_n=X_n\times K_n$. | The complement identity $M_n\setminus\mathscr D_n=X_n\times(E_\parallel\setminus K_n)$ is exact. Physical justification of this support model, or a separate four-dimensional fixed-slice calculation, remains open under O.18. |
| PUP.6.1 | Existence of the holonomy representation of $\Pi_\mathcal K$ on phason modes around meridians of $\mathcal{K}_n$ at each level $n$. | Tier 3/open. It would follow from a phason gauge connection around the knot core, which has not been derived; no engine calculation establishes the representation. |
| PUP.6.2 | The holonomy representation is unitary with respect to the phason inner product induced by the lattice action. | Tier 3/open. Unitarity is posited together with PUP.6.1, not derived. |
| PUP.6.3 | A Zeno-induced trace agrees with the canonical regular trace on the represented discrete quotient after quotienting the full-fibre product's central $\mathbb Z$ factor. | For the trefoil the regular trace on $C^*_r(B_3)$ is not the unique trace (O.35 fails as posed), so a trace identification would need an additional physical selection rule. The trefoil computation is a finite-matrix surrogate only. |
| PUP.6.4 | The GNS Hilbert space of the regular trace is equivariantly isomorphic to the physical phason Hilbert space of the condensate. | Tier 3/open; under the spectral-triple identification tracked in App ORQ O.32 and V3 Ch06 §6.5 it reduces to PUP.6.3 and inherits its status. |

Part (i) of the proposition is Tier 3 conditional on physical justification of $H_{PUP.1}^{\mathrm{fib}}$ and inverse-limit promotion. Part (iii) is a conditional lemma that applies only to a factorial sector, whose physical identification is open. Part (ii) is withdrawn. The general-prime extension additionally requires Anderson-Putnam-to-knot-complement extension, canonicity of $K\mapsto A_K$, and O.32.

> [!IMPORTANT]
> **Formal disposition.** Lemma PUP.3.1 is exact under declared full-fibre support $H_{PUP.1}^{\mathrm{fib}}$; physical adoption of that support remains open. Remark PUP.3.3 leaves inverse-limit promotion open. The former §PUP.4.2 direct-product/operator-factor step is false (Counterexample PUP.4.2.B), so Proposition PUP.1(ii) is withdrawn. O.35 and O.36 fail as posed for the represented trefoil group $B_3$ and hold for the further central quotient $B_3/Z(B_3)\cong C_2*C_3$; whether any physical sector is that quotient's regular representation is open. The general-prime case additionally carries gaps (A) Anderson-Putnam extension, (B) canonicity and (C) support realization; former gap (D) is retired as false.
>
> - **Proposition 11.12.A (Polaron Unity):** reduced to an algebraic unity candidate. Part (i) is Tier 3 conditional on physical justification of $H_{PUP.1}^{\mathrm{fib}}$ and inverse-limit promotion; part (iii) holds only in a factorial sector whose physical identification is Tier 3; no Hilbert-space non-factorizability claim survives.
> - **Proposition 11.12.A — general prime case:** additionally conditional on (A) + (B) + (C).
> - **Corollary PUP.5.1 (proposed phenomenal interpretation):** Tier 3; no subject count, owner or Level II follows.
>
> **Effective load-bearing claim.** At most an algebraic unity candidate. Identifying any part of it with a physical Identity Polaron or with phenomenal unity requires the separately open coupling and phenomenal bridges; no substrate prediction rests on this appendix.

> [!NOTE]
> **Scope of the structural closure.** The finite-level van Kampen/Wirtinger step is exact under $H_{PUP.1}^{\mathrm{fib}}$; physical adoption of that support remains open. The remaining open items are inverse-limit promotion, the meridian trace/GNS bridge, identification of a physical factorial sector, and the additional general-prime inputs.

##### PUP.6.3a Superseded surrogate: the Fibonacci substitution model (not a derivation)

Earlier versions proposed to reduce the trefoil trace step PUP.6.3 to the uniqueness of the canonical trace on the AF core of a Cuntz–Krieger algebra $\mathcal{O}_A$, with $A$ taken to be the Fibonacci substitution matrix
$$
A =
\begin{pmatrix}
1 & 1\\
1 & 0
\end{pmatrix},
$$
whose Perron–Frobenius eigenvalue is $\phi = (1+\sqrt{5})/2$. **This route is retired as a derivation.** No construction in the manuscript links the trefoil knot group to this matrix: the identification "trefoil $=$ Fibonacci substitution" was a modelling choice, not a result. The trace it produces also lives on a different object. $\mathcal{O}_A$ is simple and purely infinite (Cuntz–Krieger 1980, Thm 2.14 and Cor 2.15), so it has no tracial state; the unique trace sits on its AF core $\mathcal{F}_A = \mathcal{O}_A^{\mathbb{T}}$, with $K_0(\mathcal{F}_A) \cong \mathbb{Z}[\phi]$ (Putnam 2000 §5). A trace on $\mathcal{F}_A$ is not a trace on $C^*_r(\Gamma_\mathcal K)$, and for the trefoil the latter has no unique trace at all (O.35 fails as posed, §PUP.6). These Tier 1 facts about $\mathcal{O}_A$ are recorded only to document the superseded surrogate; they supply no trace identification for the Polaron.

Let $B_\mathcal K\subset\mathcal A_\mathcal K=C_r^*(\Gamma_\mathcal K)$ denote the meridian sub-C\*-algebra generated by the represented Wirtinger unitaries $\rho(m_1),\rho(m_2),\rho(m_3)$ of the trefoil and the unit $\mathbf{1}$. The trace step needed here is a represented-algebra statement on this declared domain: construct either (i) a faithful trace-bearing representation of $B_\mathcal K$, or (ii) a controlled finite-representation family whose normalized traces converge to $\tau|_{B_\mathcal K}$ and for which the physical state descends compatibly. A single finite-dimensional representation cannot be faithful to an infinite source algebra; the standard $SL(2,\mathbb{Z})$ matrices used for the trefoil group relation therefore supply only a finite-matrix surrogate, not the required convergence or trace-descent proof. The AF-core state from the substitution model is a separate object, and no comparison map to $B_\mathcal K$ has been constructed.

**Conditional claim.** If such a finite-level unitary representation/trace model is supplied, with $\mathbb{E}_{\text{Zeno}}$ the Zeno conditional expectation of Definition PUP.2.6, $\pi_n:B_\mathcal K\to M_n(\mathbb C)$ the finite-level unitary representation of the meridian relation set supplied by that model, and $\tau_n=\mathrm{Tr}/n$ the normalised matrix trace on the represented finite algebra, then $\tau_n\circ\pi_n\circ\mathbb{E}_{\text{Zeno}}=\tau_n\circ\pi_n$ on the represented relation set provided the expectation is trace-preserving on the represented diagonal subalgebra. This is an elementary finite-dimensional trace statement once the finite-level model exists; the existence of that model is the load-bearing open construction. Promotion beyond the surrogate cannot rest on unique-trace control for $\Gamma_\mathcal K=B_3$, which fails (O.35, §PUP.6); it would need a physical rule selecting the trace.

Numerical verification in `GCT_Physics_Engine/src/protocol_o18_trefoil_meridian_trace.py` checks a 2-dimensional finite-matrix surrogate at $<10^{-12}$ precision. It does not close the unitary trace model, physical full-fibre-support adoption, inverse-limit promotion, or any trace identification.

##### PUP.6.3b Conditional extension to general prime Polaron knots [Tier 3 conditional on Anderson-Putnam-to-knot-complement extension]

The trefoil surrogate of §PUP.6.3a supplies no trace identification (the Fibonacci-matrix link is not derived, and the AF-core trace lives on a different algebra). A trefoil-specific trace closure would require a finite-level unitary representation/trace model for the meridian relation set; the finite $M_2(\mathbb{C})$ surrogate is not enough. Extension to general prime Polaron knots would require constructing an Anderson-Putnam-style substitution C\*-algebra from the knot complement $S^3 \setminus K$, not from a tiling of $\mathbb{R}^n$. Anderson-Putnam (1998) construct substitution C\*-algebras from **substitution tilings of $\mathbb{R}^n$**; the extension of their machinery to substitution structures on a 3-manifold-with-boundary (specifically, a knot complement in $S^3$) has no published precedent we can cite. Three open gaps, and one retired step, separate the trefoil surrogate from a general-prime statement:

(A) **Construction gap.** An Anderson-Putnam-style C\*-algebra on the knot complement $S^3 \setminus K$ — analogous to the Anderson-Putnam C\*-algebra on $\mathbb{R}^n$ tile spaces but for compact 3-manifolds with toroidal boundary — has not been constructed in published literature. Whether such a construction exists, and whether it would carry any trace structure relevant to $C^*_r(\Gamma_\mathcal K)$, is an open extension of Anderson-Putnam 1998 from $\mathbb{R}^n$ to $S^3 \setminus K$ tile spaces.

(B) **Canonicity gap.** Even assuming (A) is supplied, the assignment $K \mapsto A_K$ across choice of substitution presentation is the residual canonicity sub-question registered as Open Problem O.18.

(C) **Support-realization gap.** Under $H_{PUP.1}^{\mathrm{fib}}$, Lemma PUP.3.1 uses the exact product complement $M_n\setminus\mathscr D_n=X_n\times(E_\parallel\setminus K_n)$. Physical justification of full-fibre support remains open; deletion in one fixed slice would instead require a genuine four-dimensional complement calculation. This is registered under O.18.

(D) **Retired: direct-product/operator-factor step.** This step asked for a theorem that any non-trivial equivariant tensor factor of the represented phason Hilbert space would induce a direct-product factor of the represented group. That implication is false (Counterexample PUP.4.2.B), so (D) is not an open gap; it is withdrawn together with Proposition PUP.1(ii).

The former structural chain *"prime knot $\to$ primitive AKN $\to$ Perron-Frobenius dimension-group state on the AF core $\to$ controlled meridian trace identity $\to$ direct-product/operator-factor theorem"* is therefore broken at two links: the AF-core state is not a trace on $C^*_r(\Gamma_\mathcal K)$, and the last step is false. Engine note: `GCT_Physics_Engine/src/protocol_y6_3b_polaron_unity_general_prime.py` confirms only the primitive-matrix input of that former chain, on representative primitive non-negative integer matrices of sizes 2–4. It does **not** implement a per-knot matrix construction (gap A), the canonicity argument (gap B), a meridian convergence/trace-descent construction, or any unity theorem; it verifies a matrix-theoretic fact *given* a primitive matrix.

**Tier disposition.** Trefoil-case Polaron Unity is reduced to an algebraic unity candidate: part (i) is Tier 3 conditional on the physical full-fibre-support/complement-map closure and inverse-limit promotion (sub-closures of Open Problem O.18); part (iii) applies only to a factorial sector whose physical identification is Tier 3; part (ii) is withdrawn. The general-prime extension additionally requires Anderson-Putnam-to-knot-complement extension, canonicity of $K \to A_K$, a controlled meridian representation with convergence and trace descent, and KO-dim-6 sign verification (O.32). Corollary PUP.5.1 inherits this disposition and supplies no subject count, owner or Level II.

**Effective scope of the Polaron Unity Proposition in this manuscript.** The finite-level product complement is exact under declared full-fibre support; physical adoption of that support remains open. The trefoil trace remains a surrogate, inverse-limit promotion remains open, and no Hilbert-space non-factorizability claim survives. The general-prime claim additionally depends on (A) + (B) + (C).

##### PUP.6.5 Background references for the superseded substitution surrogate

The substitution surrogate of §PUP.6.3a drew on the following published results. They are independently established, but none of them supplies a trace on $C^*_r(\Gamma_\mathcal K)$ or links a knot group to a substitution matrix:

1. Cuntz, J. & Krieger, W., "A class of C\*-algebras and topological Markov chains," *Invent. Math.* 56 (1980), 251–268 — supplies the finite-subshift/topological-Markov-chain analogue for C\*-algebraic trace bookkeeping. The AKN icosahedral tiling algebra is treated through tiling groupoid/substitution machinery rather than as a canonical Cuntz-Krieger algebra.
2. Putnam, I. F., "C\*-algebras from substitution tilings," in *Integers, Polynomials and Quivers*, Adv. Stud. Pure Math. 26, 2000 — provides the GNS construction of the canonical trace on substitution-tiling C\*-algebras.
3. Anderson, J. E. & Putnam, I. F., "Topological invariants for substitution tilings and their associated C\*-algebras," *Ergod. Th. Dynam. Sys.* 18 (1998), 509–537 — provides substitution-tiling C\*-algebra and K-theory tools, not the GCT meridian trace or physical full-fibre-support construction tracked under O.18.
4. Ribes, L. & Zalesskii, P., *Profinite Groups*, 2nd ed., Springer 2010 — background for a possible future finite-completion route; it is not applied to $\Pi_\mathcal K$ as currently defined.

The complement step is exact under $H_{PUP.1}^{\mathrm{fib}}$, whose physical adoption remains O.18; the general-prime extension additionally requires gaps (A)–(C) of §PUP.6.3b.

---

#### PUP.7 Summary of Tier dispositions

| Lemma / Theorem | Tier | Justification |
|---|---|---|
| Lemma PUP.3.1 (Wirtinger at each level) | Tier 3 conditional on $H_{PUP.1}^{\mathrm{fib}}$ | Exact product complement under declared full-fibre support; physical adoption remains O.18. |
| Lemma PUP.3.2 (Kneser–Stallings) | Tier 1 | Classical 3-manifold theorem (Kneser's conjecture: Kneser 1929, Stallings 1959/1971, Heil 1972; irreducibility of knot exteriors). |
| Remark PUP.3.3 (finite-resolution control; no inverse-limit theorem) | Tier 1 finite-level / Tier 3 inverse-limit target | Finite knot groups are controlled by Lemma PUP.3.2; inverse-limit promotion remains open. |
| Lemma PUP.3.4 (canonical = physical phason representation) | **Tier 3 conditional** on $H_{PUP.1}^{\mathrm{fib}}$, physical adoption, finite-level trace/GNS bridge, and §PUP.6.3b inputs | The finite matrix is a surrogate, not a trace-descent proof. |
| Sub-step §PUP.6.3 (trace identity) | **Tier 3/open** | The engine check is a surrogate consistency check; the Fibonacci substitution route is superseded (§PUP.6.3a), and $C^*_r(B_3)$ has no unique trace. |
| Counterexample PUP.4.2.B ($A_5$: $\chi_3\chi_W=\chi_{\rm reg}$) | **Tier 1** | Equivariant Hilbert-space tensor factorization does not imply direct-product group factorization. |
| Former open step PUP.4.2 / gap (D) (direct-product/operator-factor bridge) | **Retired as false** | Refuted by Counterexample PUP.4.2.B. |
| O.35 / O.36 for the represented trefoil group $\Gamma_\mathcal K=B_3$ | **Fail as posed for $B_3$; hold for $B_3/Z(B_3)\cong C_2*C_3$ [Tier 1 — standard]; physical identification Tier 3** | The nontrivial amenable centre $\langle\Delta^2\rangle$ makes the amenable radical nontrivial (no unique trace) and $L(B_3)$ non-factorial; whether any physical sector is the regular representation of $B_3/Z(B_3)$ is open. |
| Lemma PUP.3.5 (factoriality / central decomposition under primary representation) | Tier 1 standard fact under its hypothesis | Takesaki §V.1. The hypothesis fails for the trefoil regular representation; the lemma excludes no tensor factorization. |
| **Proposition PUP.1(i) — trefoil** | **Tier 3 conditional on $H_{PUP.1}^{\mathrm{fib}}$ + physical adoption + inverse-limit promotion** | Finite-level free indecomposability is Tier 1; promotion is open. |
| **Proposition PUP.1(ii)** | **Withdrawn** | Its bridge is false (§PUP.4.2). |
| **Proposition PUP.1(iii)** | Tier 1 conditional lemma; physical use Tier 3 | Holds in any finite factor; for the trefoil it needs a factorial sector whose physical identification is open. No uniqueness theorem for $\mathcal F_{sel}$ is claimed. |
| **Proposition PUP.1 — general prime** | **Tier 3 conditional on (A)–(C), $H_{PUP.1}^{\mathrm{fib}}$ and physical adoption** | Inherits every trefoil limitation plus the Anderson-Putnam/canonicity inputs. |
| **Corollary PUP.5.1 (proposed phenomenal interpretation)** | **Tier 3** | At most an algebraic unity candidate; requires independent physical-coupling and phenomenal bridges. No subject count, owner, Level II or substrate verdict follows. |
| Remarks PUP.5.2 / PUP.5.3 | Tier 1 finite-level fact / Tier 3 illustration | No physical phase-boundary claim and no substrate verdict. |

Trefoil-case Polaron Unity is, at most, an algebraic unity candidate. Part (i) is Tier 3 conditional on the physical full-fibre-support/complement-map closure and inverse-limit promotion (sub-closures of Open Problem O.18); part (ii) is withdrawn; part (iii) applies only to a physically unidentified factorial sector, because O.35 and O.36 fail as posed for $B_3$. The general-prime extension additionally requires Anderson-Putnam-to-knot-complement extension, canonicity of $K \to A_K$, a controlled meridian representation with convergence and trace descent, and KO-dim-6 sign verification (O.32). None of this supplies a subject count, an owner or a Level II verdict.
