# Appendix D: Born-Rule Compatibility from the Selection Operator [Tier 3 Conditional]

## D.0 Scope and Status

This appendix presents the Born rule as a conditional compatibility result rather than an unconditional geometric derivation. The precise claim is a **Tier 3 conditional compatibility theorem**: if the GCT Selection Operator supplies a countably additive, noncontextual probability measure on the projection lattice of the phason Hilbert space, then the usual Born representation follows by the projection-measure representation theorem. The missing internal proofs are registered as Open Problem O.40a (countable additivity) and Open Problem O.40b (noncontextuality).

| Proof Requirement | Current Disposition |
|-----|------------|
| KL-divergence / metabolic argument | Motivational only; not used as a proof |
| Metabolic energy bound | Not required by Gleason; not a probability-measure proof |
| Non-quadratic Born rules | Excluded by Gleason only after the frame-function hypotheses are independently satisfied |
| Projection-lattice frame-function role for the Selection Operator | Conditional on O.40a and O.40b |
| D=3 -> dim(H) >= 3 bridge | Made explicit in §D.1 |
| Tier classification | Tier 3 conditional compatibility pending O.40a/O.40b |

## D.1 Setup: The GCT Lattice Hilbert Space

The GCT vacuum is modeled by a 6D hypercubic lattice with an icosahedral acceptance-window measure. The phason Hilbert space is

$$
\mathcal{H}=L^2(\mathbb{Z}^6,d\mu_{RT}),
$$

where $d\mu_{RT}$ encodes the icosahedral cut-and-project structure. The lattice Hilbert space is separable and infinite-dimensional, so $\dim(\mathcal{H})\ge 3$, the dimensional hypothesis required by Gleason's theorem.

An Agent at address $|S\rangle\in\mathcal{H}$ is represented by a normalized pure-state candidate. Branch projections are denoted by $P\in\mathcal{P}(\mathcal{H})$. The Selection Operator is required to supply a probability assignment

$$
\mu_S:\mathcal{P}(\mathcal{H})\to[0,1].
$$

The important point is type-discipline: $\mu_S$ must be defined as a probability measure on projections before Gleason is invoked. It cannot be defined by $\mu_S(P_\phi)=|\langle S|\phi\rangle|^2$ and then used to derive the same quadratic formula.

## D.2 Frame-Function Hypotheses Required Before Gleason

**Hypothesis D.2-A: Countable additivity [open, O.40a].** For every countable orthogonal family of projections $\{P_i\}$ with strong-operator sum $P=\sum_i P_i$, the Selection Operator measure must satisfy

$$
\mu_S(P)=\sum_i\mu_S(P_i).
$$

GCT has a candidate source for this property: the inverse-limit Hilbert-space construction and the additivity of orthogonal phason sectors. What is not yet supplied is a proof that the Selection Operator's independently defined geometric overlap functional descends to a countably additive measure on the full projection lattice. That proof is Open Problem O.40a.

**Hypothesis D.2-B: Noncontextuality [open, O.40b].** The assigned value $\mu_S(P)$ must depend only on the projection $P$, not on the orthonormal basis or measurement context in which $P$ is embedded.

GCT has a candidate source for this property: the icosahedral acceptance-window measure is basis-free at the geometric level. What is not yet supplied is a Kochen-Specker-safe proof that the Selection Operator's probability assignment is independent of the chosen projection decomposition for every admissible phason observable. That proof is Open Problem O.40b.

**Normalization and non-negativity.** A probability measure on projections must satisfy $\mu_S(P)\ge 0$ and $\mu_S(I)=1$. These are part of the measure structure required for the Gleason step. They are not established by writing the Born quadratic in advance.

## D.3 Application of Gleason's Theorem

**Gleason's theorem.** If $\mathcal{H}$ is a separable Hilbert space with $\dim(\mathcal{H})\ge 3$, and $\mu:\mathcal{P}(\mathcal{H})\to[0,1]$ is a countably additive, normalized, noncontextual probability measure on projections, then there exists a unique density operator $\rho$ such that

$$
\mu(P)=\mathrm{Tr}(\rho P)
$$

for every projection $P\in\mathcal{P}(\mathcal{H})$.

Under O.40a and O.40b closure, the GCT Selection Operator measure $\mu_S$ therefore has a density-operator representation:

$$
\mu_S(P)=\mathrm{Tr}(\rho_S P).
$$

The additional GCT identification $\rho_S=|S\rangle\langle S|$ is a Selection-Operator construction claim: the Agent address must define a pure-state density operator rather than a mixed state or context-dependent ensemble. With that identification, rank-one branch projections $P_\phi=|\phi\rangle\langle\phi|$ satisfy

$$
\mu_S(P_\phi)=\mathrm{Tr}(|S\rangle\langle S|\,|\phi\rangle\langle\phi|)
=|\langle S|\phi\rangle|^2.
$$

## D.4 Conditional Compatibility Theorem

**THEOREM D.1 [Tier 3 conditional]: Born-rule compatibility of the GCT Selection Operator**

If the GCT probability assignment is a normalized, countably additive, noncontextual measure on the phason projection lattice (O.40a and O.40b), and if the Agent address construction identifies $\rho_S=|S\rangle\langle S|$, then Gleason's theorem represents the branch probabilities by

$$
P(\phi|S)=|\langle S|\phi\rangle|^2.
$$

This is a compatibility theorem, not a standalone derivation of the Born rule from the existing GCT geometric axioms alone. The theorem-grade ambition is preserved as a closure target: prove O.40a and O.40b from the inverse-limit Hilbert-space construction and the icosahedral acceptance-window geometry, then the Born representation follows by Gleason without circularly assuming the quadratic form.

## D.5 Diagnosis of the Earlier Thermodynamic Argument

The KL-divergence / metabolic-survival argument is physically suggestive but not a proof of the Born rule. It may motivate why biological agents couple to stable branches, but it does not by itself establish countable additivity or noncontextuality on the projection lattice. It is therefore retained only as interpretive commentary.

## D.6 Busch and Dimension-Two Objections

Gleason's original theorem does not apply to an isolated two-dimensional Hilbert space. GCT's relevant phason Hilbert space is the infinite-dimensional lattice Hilbert space in §D.1; qubit-scale models are subspace or coarse-grained descriptions inside that larger structure. A complete response still depends on O.40a/O.40b, because the Selection Operator measure must be defined on the global projection lattice before low-dimensional effective systems inherit the Born representation.
