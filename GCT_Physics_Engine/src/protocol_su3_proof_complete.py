#!/usr/bin/env python3
"""
protocol_su3_proof_complete.py — SU(3) Candidate Identification from RT Geometry
================================================================
Algebraic candidate-identification audit for the Rhombic
Triacontahedron (RT) acceptance window's 3-fold axes.

The protocol separates two claims:
  1. The RT ten-axis inventory closes to an 8-dimensional operator span.
  2. That span has the A2 fingerprint expected of su(3): 2 Cartan
     generators + 6 roots, with the canonical A2 Cartan matrix.

This is a Tier 3 representation-theoretic candidate identification until
the O.39 gauge-uniqueness theorem excludes all compact-Lie alternatives.

[PASS] A1. Structure constants & Jacobi identity verification
[PASS] A2. Cartan matrix computation (target: [[2,-1],[-1,2]])
[PASS] A3. Killing form (all eigenvalues negative => compact su(3))

Output
------
  data/su3_proof_complete_results.json
"""

import sys
import json
import numpy as np
from itertools import combinations
from pathlib import Path

# ---------------------------------------------------------------------------
# Path bootstrap — ensure src/ is importable when run from any cwd
# ---------------------------------------------------------------------------
_SRC = Path(__file__).resolve().parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from gct_utils import get_output_path


class _NumpyEncoder(json.JSONEncoder):
    """Serialise numpy scalar types that standard json cannot handle."""
    def default(self, obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, (np.bool_,)):
            return bool(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

# ============================================================================
# SECTION 1: RT Geometry — 10 three-fold axes
# ============================================================================
# The Rhombic Triacontahedron has 20 vertices, grouped into 10 antipodal
# pairs. Each vertex is a meeting point of exactly 3 rhombic faces, making
# it a 3-fold symmetry axis.
#
# We enumerate them using the golden ratio φ = (1+√5)/2.
# The 20 vertices of the RT fall into two shells:
#   Type A (12 vertices): permutations of (±1, ±φ, 0) / ||
#   Type B ( 8 vertices): (±1, ±1, ±1)  scaled by φ / (√5)  (approx)
#
# However, the most direct way (matching gct_gauge.py's identify_3fold_axes)
# is to hard-code the 10 canonical axis directions used throughout the GCT
# codebase — these are the icosahedral 3-fold axes normalised to unit length.
# ---------------------------------------------------------------------------

def _build_rt_axes() -> list[np.ndarray]:
    """
    Return the 10 unique 3-fold axis directions of the Rhombic Triacontahedron.

    The RT is dual to the icosidodecahedron. Its 3-fold axes coincide with the
    20 vertex directions of the regular icosahedron (10 antipodal pairs).

    Icosahedron vertex coordinates (un-normalised):
        (0, ±1, ±φ),  (±1, ±φ, 0),  (±φ, 0, ±1)   with φ = (1+√5)/2
    """
    phi = (1.0 + np.sqrt(5.0)) / 2.0

    raw = [
        [0,  1,  phi],
        [0,  1, -phi],
        [0, -1,  phi],
        [1,  phi, 0],
        [1, -phi, 0],
        [-1,  phi, 0],
        [phi, 0,  1],
        [phi, 0, -1],
        [-phi, 0,  1],
        [0, -1, -phi],
    ]

    axes = []
    for r in raw:
        v = np.array(r, dtype=float)
        axes.append(v / np.linalg.norm(v))
    return axes


# ============================================================================
# SECTION 2: Build orthonormal 8D candidate basis via Gram-Schmidt
# ============================================================================

def _frobenius_ip(A: np.ndarray, B: np.ndarray) -> complex:
    """Frobenius inner product:  Tr(A† B)."""
    return np.trace(A.conj().T @ B)


def _gram_schmidt_ortho(matrices: list[np.ndarray]) -> list[np.ndarray]:
    """
    Gram-Schmidt orthonormalisation under the Frobenius inner product.
    Returns a list of matrices satisfying Tr(Bi† Bj) = δᵢⱼ.
    """
    basis: list[np.ndarray] = []
    for M in matrices:
        v = M.copy().astype(complex)
        for b in basis:
            v = v - _frobenius_ip(b, v) * b
        norm = np.sqrt(_frobenius_ip(v, v).real)
        if norm > 1e-10:
            basis.append(v / norm)
    return basis


def build_su3_basis(axes: list[np.ndarray]) -> list[np.ndarray]:
    """
    Construct an orthonormal 8-dimensional candidate basis from RT axes.

    Steps
    -----
    1. Form traceless Hermitian seed operators Qk = |vk><vk| - I/3.
    2. Close the algebra under commutators i[A,B] until no new directions appear.
    3. Orthonormalise under Frobenius: Tr(Bi Bj) = δᵢⱼ.
       (Since the Bi are Hermitian: Bi† = Bi, so Tr(Bi† Bj) = Tr(Bi Bj).)
    """
    seeds = []
    for v in axes:
        v = v.reshape(3, 1)
        P = (v @ v.T).astype(complex)
        Q = P - np.eye(3, dtype=complex) / 3.0
        seeds.append(Q)

    # Closure under commutators
    candidates = list(seeds)
    for _ in range(30):          # iterate until stable
        n_before = len(candidates)
        for i in range(n_before):
            for j in range(i + 1, n_before):
                comm = candidates[i] @ candidates[j] - candidates[j] @ candidates[i]
                C = 1j * comm   # keep Hermitian
                candidates.append(C)
        # Prune to independent set via GS
        candidates = _gram_schmidt_ortho(candidates)
        if len(candidates) == n_before:
            break  # converged

    basis = _gram_schmidt_ortho(candidates)
    return basis[:8]   # candidate su(3) span dimension


# ============================================================================
# SECTION 3: Structure Constants
# ============================================================================

def compute_structure_constants(basis: list[np.ndarray]) -> np.ndarray:
    """
    Compute f^{ijk} from [Bi, Bj] = i Σk f^{ijk} Bk.

    Using the identity:  f^{ijk} = -i Tr([Bi, Bj] Bk).
    Since basis is o.n. under Frobenius (Tr(Bi Bj) = δij for Hermitian Bi),
    this is exact.
    """
    n = len(basis)
    f = np.zeros((n, n, n), dtype=complex)
    for i in range(n):
        for j in range(n):
            comm = basis[i] @ basis[j] - basis[j] @ basis[i]
            for k in range(n):
                f[i, j, k] = -1j * np.trace(comm @ basis[k])
    return f.real   # f^{ijk} are purely real for su(N)


def verify_jacobi(f: np.ndarray) -> float:
    """
    Verify the Jacobi identity: Σm (f^{ijm} f^{mkl} + f^{jkm} f^{mil} + f^{kim} f^{mjl}) = 0
    for all (i,j,k,l).

    Returns the maximum absolute violation.
    """
    n = f.shape[0]
    max_viol = 0.0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    # Jacobi via structure constants
                    val = (
                        np.einsum('m,m->', f[i, j, :], f[:, k, l]) +
                        np.einsum('m,m->', f[j, k, :], f[:, i, l]) +
                        np.einsum('m,m->', f[k, i, :], f[:, j, l])
                    )
                    max_viol = max(max_viol, abs(val))
    return max_viol


# ============================================================================
# SECTION 4: Cartan Matrix — Weight-Space Approach
# ============================================================================

def compute_cartan_matrix(
    basis: list[np.ndarray],
    f: np.ndarray
) -> tuple[np.ndarray, dict]:
    """
    Compute the Cartan matrix of su(3) via the fundamental-representation root analysis.

    Correct approach:
    -----------------
    The algebraic structure is most cleanly revealed by working in the 3D fundamental
    representation (the 3x3 matrices themselves), not in the 8D adjoint representation.

    1. Find two commuting 3x3 Hermitian matrices H1, H2 (the CSA generators).
    2. Simultaneously diagonalize H1, H2 in C^3 to get 3 weight vectors:
           mu_i = (eigenvalue of H1 on weight i, eigenvalue of H2 on weight i)
    3. The 6 roots of su(3) are the pairwise differences:
           alpha_{ij} = mu_i - mu_j  for i != j
    4. Identify 3 positive roots (e.g. first component positive).
       For su(3): alpha12, alpha13, alpha23 where alpha13 = alpha12 + alpha23.
    5. The 2 simple roots are the indecomposable positive roots.
    6. Compute the Cartan matrix A_ij = 2<alpha_i, alpha_j> / <alpha_j, alpha_j>.

    This avoids the nilpotency problem of the adjoint approach in this specific basis.
    """
    n = len(basis)

    # --- 4a. Find commuting pair H1,H2 in the 3x3 representation -----------
    csa_indices = []
    min_comm_norm = np.inf
    best_pair = (0, 1)

    for i in range(n):
        for j in range(i + 1, n):
            comm = basis[i] @ basis[j] - basis[j] @ basis[i]
            cnorm = float(np.linalg.norm(comm))
            if cnorm < min_comm_norm:
                min_comm_norm = cnorm
                best_pair = (i, j)
            if cnorm < 1e-9:
                csa_indices.append((i, j))

    if not csa_indices:
        csa_indices = [best_pair]

    h1_idx, h2_idx = csa_indices[0]
    H1 = basis[h1_idx]
    H2 = basis[h2_idx]

    # --- 4b. Simultaneously diagonalize H1 and H2 in C^3 --------------------
    # H1 and H2 are 3x3 Hermitian matrices. Diagonalize H1 first, then use
    # the same eigenvectors for H2 (valid since [H1,H2] = 0).
    eps = 1.0 / np.sqrt(137.036)   # irrational for lifting degeneracies
    M3 = H1 + eps * H2

    evals3, evecs3 = np.linalg.eigh(M3)  # H1+eps*H2 is still Hermitian
    # evals3 sorted ascending. The correct eigenvecs of H1+eps*H2 diagonalize both.

    # Extract the *separate* eigenvalues of H1 and H2 on these eigenvectors:
    weights = np.zeros((3, 2))   # weights[i] = (mu_H1, mu_H2) for the i-th weight
    for i in range(3):
        v = evecs3[:, i]
        denom = float(np.dot(v.conj(), v).real)
        if denom > 1e-12:
            weights[i, 0] = float(np.dot(v.conj(), H1 @ v).real / denom)
            weights[i, 1] = float(np.dot(v.conj(), H2 @ v).real / denom)

    # --- 4c. Compute all 6 roots as differences of weights ------------------
    # Root alpha_{ij} = mu_i - mu_j  for i != j
    roots_signed = []
    for i in range(3):
        for j in range(3):
            if i != j:
                roots_signed.append(weights[i] - weights[j])

    roots_signed = np.array(roots_signed)   # shape (6, 2)

    # --- 4d. Identify 3 positive roots -------------------------------------
    def _is_positive(r: np.ndarray) -> bool:
        for x in r:
            if abs(x) > 1e-7:
                return bool(x > 0)
        return False

    positive_roots = [r for r in roots_signed if _is_positive(r)]

    # --- 4e. Find simple roots (indecomposable positive roots) -------------
    tol_cluster = 1e-5

    def _is_simple(root: np.ndarray, positives: list) -> bool:
        for r1 in positives:
            for r2 in positives:
                if np.linalg.norm(r1) < 1e-9 or np.linalg.norm(r2) < 1e-9:
                    continue
                if np.linalg.norm(root - r1 - r2) < tol_cluster:
                    return False   # root = r1 + r2 => not simple
        return True

    simple_roots = [r for r in positive_roots if _is_simple(r, positive_roots)]

    # Fallback: use the 2 smallest positive roots
    if len(simple_roots) < 2:
        norms = [np.linalg.norm(r) for r in positive_roots]
        simple_roots = [positive_roots[i] for i in np.argsort(norms)[:2]]

    if len(simple_roots) < 2:
        # Emergency fallback
        simple_roots = list(roots_signed[:2])

    # --- 4f. Compute Cartan Matrix ------------------------------------------
    a1, a2 = simple_roots[0], simple_roots[1]
    d11 = float(np.dot(a1, a1))
    d22 = float(np.dot(a2, a2))

    cartan = np.array([
        [2.0,
         2.0 * float(np.dot(a1, a2)) / d22 if d22 > 1e-10 else np.nan],
        [2.0 * float(np.dot(a2, a1)) / d11 if d11 > 1e-10 else np.nan,
         2.0],
    ])

    info = {
        "csa_indices": [int(h1_idx), int(h2_idx)],
        "fundamental_weights": weights.round(6).tolist(),
        "n_positive_roots": len(positive_roots),
        "n_nonzero_roots": len(roots_signed),
        "simple_root_1": a1.tolist(),
        "simple_root_2": a2.tolist(),
    }

    return cartan, info


# ============================================================================
# SECTION 5: Killing Form
# ============================================================================

def compute_killing_form(f: np.ndarray) -> np.ndarray:
    """
    Compute the Killing form matrix: κᵢⱼ = Tr(ad(Bi) ∘ ad(Bj)).

    κᵢⱼ = Σ_{m,n} f^{imn} f^{jmn}   (using antisymmetry of f)
    """
    n = f.shape[0]
    kappa = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            # ad(Bi)_mn = f^{imn}  (using the convention adH = -i f, but here
            # we want the real adjoint: [ad(Bi)]_mn = f^{i}_{mn})
            adBi = f[i, :, :]    # shape (n,n)
            adBj = f[j, :, :]
            kappa[i, j] = np.trace(adBi @ adBj)
    return kappa


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 70)
    print("  SU(3) Candidate-Identification Audit")
    print("  RT 10-axis span + A2 root-system fingerprint")
    print("=" * 70)

    # ------------------------------------------------------------------
    # Step 1: Build orthonormal basis
    # ------------------------------------------------------------------
    print("\n[Step 1] Building orthonormal 8D candidate basis from RT 3-fold axes...")
    axes = _build_rt_axes()
    print(f"  RT 3-fold axes found : {len(axes)}")

    basis = build_su3_basis(axes)
    print(f"  Basis dimension      : {len(basis)}")

    if len(basis) != 8:
        print(f"  WARNING: Expected 8-dimensional algebra, got {len(basis)}.")
        print("  Aborting audit — geometric seed may be insufficient.")
        sys.exit(1)

    # Quick orthonormality check
    gram = np.zeros((8, 8), dtype=complex)
    for i in range(8):
        for j in range(8):
            gram[i, j] = np.trace(basis[i] @ basis[j])
    max_off_diag = np.max(np.abs(gram - np.eye(8)))
    print(f"  Gram matrix max off-diag error: {max_off_diag:.2e}  (target <1e-10)")

    # ------------------------------------------------------------------
    # Step 2: Acceptance Test A1 — Structure Constants & Jacobi
    # ------------------------------------------------------------------
    print("\n[A1] Computing structure constants f^{ijk}...")
    f = compute_structure_constants(basis)
    print(f"  f tensor shape: {f.shape}   (totally antisymmetric)")

    # Antisymmetry check
    asym_err = np.max(np.abs(f + np.transpose(f, (1, 0, 2))))
    print(f"  Antisymmetry error f^{{ijk}} + f^{{jik}}: {asym_err:.2e}  (target 0)")

    print("  Verifying Jacobi identity (all n^4 = 4096 triplets)...")
    jacobi_max = verify_jacobi(f)
    jacobi_pass = jacobi_max < 1e-10
    print(f"  Jacobi max violation : {jacobi_max:.4e}   {'[PASS]' if jacobi_pass else '[FAIL]'}")

    # ------------------------------------------------------------------
    # Step 3: Acceptance Test A2 -- Cartan Matrix
    # ------------------------------------------------------------------
    print("\n[A2] Computing Cartan matrix...")
    cartan, cinfo = compute_cartan_matrix(basis, f)

    target_cartan = np.array([[2, -1], [-1, 2]], dtype=float)
    # Handle NaN in cartan when rounding
    cartan_for_json = np.where(np.isnan(cartan), -999, np.round(cartan)).astype(int)

    print(f"  Simple root a1 : {np.array(cinfo['simple_root_1']).round(4)}")
    print(f"  Simple root a2 : {np.array(cinfo['simple_root_2']).round(4)}")
    print(f"  Non-zero roots found: {cinfo['n_nonzero_roots']}  (target: 6)")
    print()
    print("  Extracted Cartan Matrix:")
    print("  +-------------+")
    for row in cartan.round(3):
        print(f"  |  {row[0]:+6.3f}  {row[1]:+6.3f}  |")
    print("  +-------------+")
    print()
    print("  Rounded Cartan Matrix:")
    print(f"    {cartan_for_json.tolist()}")

    cartan_diff = np.max(np.abs(cartan - target_cartan))
    cartan_pass = cartan_diff < 1e-9     # strict equality check
    print(f"  Max deviation from [[2,-1],[-1,2]]: {cartan_diff:.4f}   {'[PASS]' if cartan_pass else '[FAIL]'}")

    # ------------------------------------------------------------------
    # Step 4: Acceptance Test A3 -- Killing Form
    # ------------------------------------------------------------------
    print("\n[A3] Computing Killing form = Tr(ad(Bi) ad(Bj))...")
    kappa = compute_killing_form(f)
    killing_evals = np.linalg.eigvalsh(kappa)
    all_negative = bool(np.all(killing_evals < 0))

    print(f"  Killing eigenvalues: {np.round(killing_evals, 4).tolist()}")
    print(f"  All negative        : {all_negative}   {'[PASS] compact real su(3)' if all_negative else '[FAIL]'}")

    # ------------------------------------------------------------------
    # Final Verdict
    # ------------------------------------------------------------------
    all_pass = jacobi_pass and cartan_pass and all_negative
    verdict = "su3_candidate_identified" if all_pass else "su3_candidate_FAILED"

    print("\n" + "=" * 70)
    print("  FINAL VERDICT")
    print("=" * 70)
    if all_pass:
        print("  [PASS] A1 (Jacobi Identity)  : PASS")
        print("  [PASS] A2 (Cartan Matrix)    : PASS  -> [[2,-1],[-1,2]] matches su(3) A2")
        print("  [PASS] A3 (Killing Form)     : PASS  -> compact real algebra confirmed")
        print()
        print("  VERDICT: su3_candidate_identified")
        print("  The RT acceptance window generates the registered su(3) candidate.")
        print("  Theorem-grade uniqueness remains O.39.")
    else:
        print(f"  A1: {'PASS' if jacobi_pass else 'FAIL'}  "
              f"A2: {'PASS' if cartan_pass else 'FAIL'}  "
              f"A3: {'PASS' if all_negative else 'FAIL'}")
        print(f"  VERDICT: {verdict}")

    # ------------------------------------------------------------------
    # Save JSON
    # ------------------------------------------------------------------
    results = {
        "jacobi_max_violation": float(jacobi_max),
        "jacobi_pass": jacobi_pass,
        "cartan_matrix": cartan_for_json.tolist(),
        "cartan_matrix_raw": cartan.round(6).tolist(),
        "cartan_pass": cartan_pass,
        "killing_eigenvalues": [float(x) for x in killing_evals],
        "killing_all_negative": all_negative,
        "csa_info": cinfo,
        "basis_dimension": len(basis),
        "gram_max_off_diag": float(max_off_diag),
        "identification_status": (
            "Tier 2 generator inventory plus Tier 3 A2/su(3) candidate "
            "identification pending O.39 gauge-uniqueness theorem"
        ),
        "verdict": verdict,
        "pass": bool(all_pass),
    }

    out_path = get_output_path("protocol_su3_proof_complete_results.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2, cls=_NumpyEncoder)
    print(f"\n  Results saved to: {out_path}")
    print("=" * 70)

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
