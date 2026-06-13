"""
App Y Sec Y.6.3b General-Prime Polaron Unity Extension via Anderson-Putnam Primitivity
========================================================================================

Audits the matrix-theoretic input in the App Y Sec Y.6.3b general-prime
extension of Proposition Y.1 (Polaron Unity). The protocol verifies the
primitive-matrix Perron-Frobenius ingredient needed for the AF-core
dimension-group trace step; it does not construct the knot-complement
C*-algebra, prove canonicity of K |-> A_K, or supply a universal
finite-quotient meridian trace.

What this protocol closes
==========================

App Y Sec Y.6.3b reduces the general-prime extension to three inputs:
(A) an Anderson-Putnam-style substitution C*-algebra for S^3 \ K;
(B) canonicity of the assignment K |-> A_K; and (C) a meridian
finite-quotient trace construction for the relevant knot-complement
representation. Given a primitive non-permutation matrix A_K, the
Cuntz-Krieger algebra O_{A_K} is non-tracial; the trace data used by
Lemma Y.3.4 live on the gauge-fixed AF core F_{A_K}=O_{A_K}^T and on
the finite-dimensional meridian quotient, as in the trefoil case.

Conditional structural chain (Tier 3 extension scaffold)
========================================================

  (1) K is a prime knot in S^3.
      Premise from App Y Sec Y.3 (Kneser-Stallings: prime knot groups
      are freely indecomposable; Lemma Y.3.2).

  (2) ==> If a prime-knot complement supplies an AKN-style substitution
      model rho_K with an irreducible substitution matrix A_K, then the
      Perron-Frobenius consequences below apply. This protocol does not
      prove that every prime knot complement supplies such a substitution;
      it audits the primitive-matrix consequence when the substitution
      model is supplied.

  (3) ==> A_K has unique Perron-Frobenius eigenvalue lambda_PF(A_K)
      > 0 with all other eigenvalues strictly smaller in modulus.
      Perron-Frobenius theorem for primitive non-negative matrices
      (Horn-Johnson 1985 Thm 8.5.1).

  (4) ==> lambda_PF(A_K) is algebraic. It is irrational only after
      excluding integer-Perron degeneracies and other rational-root
      cases; primitive non-permutation integer matrices can have rational
      Perron eigenvalues (for example [[1,1],[1,1]] has lambda_PF=2).
      Lind-Marcus 1995 "An Introduction to Symbolic Dynamics and
      Coding" Sec 11.1: for an irreducible non-negative integer
      matrix of size >= 2 with primitive substitution rule, the
      Perron eigenvalue is a Perron number (algebraic integer with
      all conjugates strictly smaller in modulus). The representative
      non-degenerate samples below have algebraic-irrational Perron
      eigenvalues; this is not a universal theorem for every primitive
      non-permutation integer matrix.

  (5) ==> The AF core F_{A_K}=O_{A_K}^T carries the ordered
      dimension-group state paired with the Perron-Frobenius
      eigenvector. For primitive irreducible non-permutation A_K,
      O_{A_K} itself is purely-infinite simple and non-tracial
      (Cuntz-Krieger 1980 Thm 2.14 + Cor 2.15).

  (6) ==> The Zeno conditional expectation E_Zeno : B_K -> B_K^diag
      on the meridian subalgebra B_K must be compared in a finite
      meridian quotient or other trace-bearing representation. The
      trefoil calculation currently uses an M_2(C) finite-matrix
      surrogate; a unitary finite-dimensional faithful quotient of the
      meridian C*-subalgebra remains an open construction. No trace is
      extended to O_{A_K}.

The closure chain is structurally complete *given* (A) the
Anderson-Putnam-style C*-algebra extension from R^n tile spaces
to substitution structures on S^3 \ K, (B) canonicity of the
assignment K |-> A_K across choice of substitution presentation,
(C) a finite-quotient meridian trace construction, (D) KO-dim-6 sign
verification (O.32), (E) the BKKO trivial-amenable-radical hypothesis
(O.35), and (F) the primary-representation hypothesis (O.36). Under
(A) + (B) + (C) + (D) + (E) + (F) and the fixed-slice finite-level
complement reduction H_Y.1, Lemma Y.3.4 extends from the trefoil to
any prime knot K. Proposition Y.1 (Polaron Unity) is Tier 3 conditional
for the trefoil case and Tier 3 conditional on those general-prime
inputs.

What this protocol DOES NOT do
================================

  - Construct the explicit AKN substitution matrix A_K for each
    specific prime knot K. This is a candidate construction pending
    Anderson-Putnam-to-knot-complement extension (O.18 gap A); its
    explicit form depends on the knot's tile-decomposition and is not
    needed for the matrix-theoretic audit.
  - Provide a fully rigorous derivation of Anderson-Putnam Theorem
    4.6 from first principles. The theorem is taken as a literature
    citation (Anderson-Putnam 1998).

What this protocol DOES provide
================================

  - Explicit verification of step (4) for representative non-degenerate
    prime-knot candidate substitution matrices, demonstrating algebraic-
    irrational Perron values under the expected sample structure.
  - Numerical verification of the trefoil case as a reference check
    (Fibonacci matrix [[1,1],[1,0]] with Perron eigenvalue phi,
    confirming the structural chain).
  - A structural audit of the primitive-matrix input in Sec Y.6.3b.

Sample verification: Perron eigenvalues for canonical primitive
non-negative integer matrices of small size
============================================================

For each candidate matrix A below (representative of the AKN substitution
structure for various prime knot complexities), we verify:
  - A is primitive (A^n strictly positive for some n)
  - the Perron eigenvalue is classified exactly; irrationality is a
    non-degenerate sample property, not a consequence of primitivity alone

The candidate matrices are constructed via the Wirtinger-relation
abelianization: for a knot with k crossings, the AKN substitution
matrix is roughly (k-1) x (k-1) with entries derived from the
crossing structure. We also include a primitive rational-Perron
counterexample to prevent the false primitivity-implies-irrational step.

Cross-reference: App Y Sec Y.6.3a (trefoil case explicit closure);
Sec Y.6.3b (general-prime extension); App H §O.18 (Lemma Y.3.4);
Anderson-Putnam 1998 (Ergodic Theory & Dynamical Systems 18:509);
Putnam 2000 (Comm. Math. Phys. 213:493); Horn-Johnson 1985 Sec 8.5;
Lind-Marcus 1995 Sec 11.1.
"""

from __future__ import annotations

import math
import json
from pathlib import Path

import numpy as np


def is_primitive(A: np.ndarray, max_power: int = 20) -> tuple[bool, int]:
    """Check whether A is primitive: some A^n is strictly positive."""
    if (A > 0).all():
        return True, 1
    A_power = A.astype(float).copy()
    for n in range(2, max_power + 1):
        A_power = A_power @ A.astype(float)
        if (A_power > 0).all():
            return True, n
    return False, -1


def perron_eigenvalue(A: np.ndarray) -> float:
    """Return the Perron eigenvalue (largest real positive eigenvalue)."""
    eigs = np.linalg.eigvals(A.astype(float))
    real_eigs = [e.real for e in eigs if abs(e.imag) < 1e-10 and e.real > 0]
    return float(max(real_eigs)) if real_eigs else float(max(np.abs(eigs)))


def is_algebraic_irrational(A: np.ndarray) -> dict:
    """Inspect whether the Perron eigenvalue is algebraic-irrational.

    For an integer matrix, the characteristic polynomial has integer
    coefficients. A rational algebraic-integer eigenvalue must be an
    integer root. If the constant term is zero, factor out powers of x
    before applying the rational-root theorem so integer nonzero roots
    such as lambda=2 for x^2-2x are not missed.
    """
    lambda_PF = perron_eigenvalue(A)
    # Get integer characteristic polynomial coefficients
    char_poly = np.poly(A.astype(float))  # leading coeff first
    # Round to nearest integer for integer-matrix invariants.
    char_poly_int = [int(round(c)) for c in char_poly]
    reduced_poly_int = list(char_poly_int)
    factored_zero_roots = 0
    while len(reduced_poly_int) > 1 and reduced_poly_int[-1] == 0:
        reduced_poly_int.pop()
        factored_zero_roots += 1
    reduced_constant_term = reduced_poly_int[-1]

    # Rational root candidates: zero roots plus integer divisors of the
    # reduced constant term.
    divisors = []
    if factored_zero_roots:
        divisors.append(0)
    if reduced_constant_term != 0:
        for d in range(1, abs(reduced_constant_term) + 1):
            if reduced_constant_term % d == 0:
                divisors.extend([d, -d])

    # Check if any integer divisor is the Perron eigenvalue
    is_integer_eig = any(abs(lambda_PF - d) < 1e-9 for d in divisors)

    return {
        "perron_eigenvalue": lambda_PF,
        "char_poly_int_coeffs": char_poly_int,
        "constant_term": char_poly_int[-1],
        "reduced_constant_term_after_zero_factor": reduced_constant_term,
        "factored_zero_roots": factored_zero_roots,
        "integer_root_candidates": divisors,
        "perron_is_integer_root": is_integer_eig,
        "perron_is_algebraic_irrational": (not is_integer_eig),
    }


def verify_knot_substitution_matrix(
    label: str, A: np.ndarray, expected_perron: float | None = None
) -> dict:
    """Run full verification on a candidate knot substitution matrix."""
    primitive, n_to_positive = is_primitive(A)
    irrationality = is_algebraic_irrational(A)
    matches = None
    if expected_perron is not None:
        matches = abs(irrationality["perron_eigenvalue"] - expected_perron) < 1e-9
    return {
        "label": label,
        "matrix": A.tolist(),
        "size": A.shape[0],
        "primitive": primitive,
        "n_to_strictly_positive": n_to_positive,
        "perron_eigenvalue": irrationality["perron_eigenvalue"],
        "characteristic_polynomial": irrationality["char_poly_int_coeffs"],
        "perron_is_algebraic_irrational": irrationality["perron_is_algebraic_irrational"],
        "matches_expected_perron": matches,
        "passes_matrix_theoretic_ingredient": (
            primitive and irrationality["perron_is_algebraic_irrational"]),
    }


def compute() -> dict:
    try:
        from gct_utils import C
        _PHI_FROM_SSOT = float(C.PHI)
    except ImportError:
        _PHI_FROM_SSOT = (1.0 + math.sqrt(5.0)) / 2.0

    PHI = _PHI_FROM_SSOT
    # ===============================================================
    #
    # IMPORTANT: these are NOT the actual AKN substitution matrices
    # for each knot. The Anderson-Putnam construction for a specific
    # knot K depends on the explicit tile-decomposition of the knot
    # complement and is research-level for general K. The samples
    # below are chosen to demonstrate the STRUCTURAL PATTERN: the
    # representative non-degenerate primitive non-negative integer
    # matrices have algebraic-irrational Perron eigenvalues.
    #
    # The load-bearing case is the trefoil (Fibonacci), which is the
    # specific AKN matrix verified in App Y Sec Y.6.3a. The remaining
    # samples are PATTERN-DEMONSTRATIONS, not knot-specific verifications.

    # Trefoil case (Fibonacci): the canonical AKN matrix from
    # App Y Sec Y.6.3a. Perron = phi.
    trefoil_A = np.array([[1, 1], [1, 0]])

    # Pattern demonstration: 2x2 primitive matrices with irrational Perron
    pattern_2x2_a = np.array([[2, 1], [1, 1]])  # Perron = 1+sqrt(2)
    pattern_2x2_b = np.array([[1, 2], [1, 1]])  # Perron = 1+sqrt(2)
    pattern_2x2_c = np.array([[3, 1], [1, 2]])  # Perron = (5+sqrt(5))/2

    # Pattern demonstration: 3x3 primitive matrices with irrational Perron
    pattern_3x3_a = np.array([[2, 1, 0], [1, 1, 1], [0, 1, 1]])  # primitive
    pattern_3x3_b = np.array([[1, 1, 1], [1, 1, 0], [0, 1, 1]])  # primitive

    # Pattern demonstration: 4x4 primitive matrix with irrational Perron
    # (more generic structure to avoid the cyclic-degenerate case)
    pattern_4x4 = np.array([
        [2, 1, 0, 0],
        [1, 1, 1, 0],
        [0, 1, 1, 1],
        [0, 0, 1, 1],
    ])

    rational_perron_counterexample = np.array([[1, 1], [1, 1]])

    verifications = []
    verifications.append(verify_knot_substitution_matrix(
        "Trefoil AKN (Fibonacci, App Y Sec Y.6.3a) -- ACTUAL knot AKN matrix",
        trefoil_A,
        expected_perron=PHI,
    ))
    verifications.append(verify_knot_substitution_matrix(
        "Pattern 2x2 example A (size-2 primitive demo)",
        pattern_2x2_a,
    ))
    verifications.append(verify_knot_substitution_matrix(
        "Pattern 2x2 example B (size-2 primitive demo)",
        pattern_2x2_b,
    ))
    verifications.append(verify_knot_substitution_matrix(
        "Pattern 2x2 example C (size-2 primitive demo)",
        pattern_2x2_c,
    ))
    verifications.append(verify_knot_substitution_matrix(
        "Pattern 3x3 example A (size-3 primitive demo)",
        pattern_3x3_a,
    ))
    verifications.append(verify_knot_substitution_matrix(
        "Pattern 3x3 example B (size-3 primitive demo)",
        pattern_3x3_b,
    ))
    verifications.append(verify_knot_substitution_matrix(
        "Pattern 4x4 example (size-4 primitive demo)",
        pattern_4x4,
    ))
    rational_counterexample = verify_knot_substitution_matrix(
        "Positive rank-one primitive rational-Perron control [[1,1],[1,1]]",
        rational_perron_counterexample,
        expected_perron=2.0,
    )

    all_pass = all(v["passes_matrix_theoretic_ingredient"] for v in verifications)

    return {
        "structural_chain_summary": [
            "(1) K prime in S^3 [Kneser-Stallings, Lemma Y.3.2]",
            "(2) AKN tile-substitution rho_K primitive [unproved extension; Anderson-Putnam 1998 supplies substitution-tiling machinery, not S^3 \\ K construction]",
            "(3) Perron-Frobenius: A_K has unique max-modulus eigenvalue [HJ85 Thm 8.5.1]",
            "(4) Perron eigenvalue is algebraic; irrationality requires excluding rational-root degeneracies [Lind-Marcus 1995 Sec 11.1]",
            "(5) AF core F_{A_K}=O_{A_K}^T carries dimension-group state; O_{A_K} is non-tracial",
            "(6) meridian trace identity requires a unitary finite-dimensional faithful trace-bearing quotient [trefoil currently: M_2(C) surrogate]",
        ],
        "closure_status": (
            "Structural extension of Y.6.3a to general prime knots is "
            "complete *given* (A) the Anderson-Putnam-style C*-algebra "
            "extension from R^n tile spaces to substitution structures on "
            "S^3 \\ K, (B) canonicity of K |-> A_K, and (C) a finite-quotient "
            "meridian trace construction (Open Problem O.18), and the "
            "fixed-slice finite-level complement reduction H_Y.1. Trefoil-case "
            "Polaron Unity is Tier 3 conditional pending resolution of the "
            "App Y finite-level 4-manifold knot-complement clarification "
            "(registered as a sub-closure of Open Problem O.18); the "
            "general-prime extension remains Tier 3 conditional on "
            "Anderson-Putnam-to-knot-complement extension, canonicity of "
            "K -> A_K, finite-quotient meridian trace construction, and "
            "KO-dim-6 sign verification (O.32), together with O.35 "
            "(BKKO trivial-amenable-radical hypothesis) and O.36 "
            "(primary-representation hypothesis)."),
        "sample_verifications": verifications,
        "rational_perron_counterexample": rational_counterexample,
        "all_samples_pass_matrix_theoretic_ingredient": {
            "matrix_theoretic_input_pass": bool(all_pass),
            "anderson_putnam_extension_supplied": False,
            "general_prime_closure": "tier_3_conditional",
            "open_gaps": ["A", "B", "C", "D", "O.35", "O.36"],
        },
        "remaining_open": (
            "The AKN tile-substitution rho_K primitive remains an unproved "
            "extension: Anderson-Putnam 1998 supplies substitution-tiling "
            "machinery, not the S^3 \\ K construction. A fully self-contained "
            "GCT-internal derivation would require constructing the AKN "
            "substitution, proving primitivity, and proving recognizability "
            "inside this protocol."),
    }


def main():
    results = compute()
    out_dir = Path(__file__).parent.parent / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "y6_3b_polaron_unity_general_prime.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"App Y Sec Y.6.3b General-Prime Polaron Unity Extension")
    print(f"=" * 65)
    print(f"Structural chain:")
    for step in results["structural_chain_summary"]:
        print(f"  {step}")
    print()
    print(f"Sample knot substitution-matrix verifications:")
    for v in results["sample_verifications"]:
        print(f"  {v['label']}:")
        print(f"    matrix size = {v['size']}")
        print(f"    primitive: {v['primitive']} (positive at n = {v['n_to_strictly_positive']})")
        print(f"    Perron eigenvalue = {v['perron_eigenvalue']:.6f}")
        if v["matches_expected_perron"] is not None:
            print(f"    matches expected: {v['matches_expected_perron']}")
        print(f"    algebraic-irrational: {v['perron_is_algebraic_irrational']}")
        print(f"    passes matrix-theoretic ingredient: {v['passes_matrix_theoretic_ingredient']}")
    print()
    print(
        "Matrix-theoretic sample input pass: "
        f"{results['all_samples_pass_matrix_theoretic_ingredient']['matrix_theoretic_input_pass']}"
    )
    print(f"Closure: {results['closure_status'][:80]}...")
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
