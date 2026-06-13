#!/usr/bin/env python3
"""
gct_projections.py - Canonical 6D -> 3D Icosahedral Projection Matrices
========================================================================

Canonical Projection Convention.

Mathematical Summary
--------------------
The GCT lattice is a Z^6 hypercubic lattice projected onto physical 3-space
(E_parallel) via the icosahedral cut-and-project method. The projection
decomposes R^6 = E_parallel (+) E_perp, where both subspaces are 3-dimensional.

The canonical AKN (Ammann-Kramer-Neri) basis uses the 6 icosahedral vertex
directions as column vectors. In the standard orientation, the unnormalized
row matrices are:

    M_para_raw[i,j] in {0, +/-1, +/-phi}
    M_perp_raw[i,j] in {0, +/-1, +/-phi'} where phi' = -1/phi (Galois conjugate)

Normalization Convention
------------------------
A single scalar N = 1/sqrt(2(2+phi)) makes M_para an isometry (G_para = I_3),
but does NOT satisfy the completeness relation
M_para^T M_para + M_perp^T M_perp = I_6, because the two subspaces have
different intrinsic scales.

The correct canonical form requires TWO normalizations:

    N_para = 1 / sqrt(2(2+phi))   ~ 0.37175
    N_perp = 1 / sqrt(2(2+phi'))  ~ 0.60150 where phi' = -1/phi

With these:
    (1) Orthogonality:  M_para @ M_perp^T = 0_{3x3}                  [machine precision]
    (2) Completeness:   M_para^T M_para + M_perp^T M_perp = I_6      [machine precision]
    (3) Both Gram matrices are identity: G_para = G_perp = I_3

The phi^{-6} Gram determinant ratio is a property of the UNNORMALIZED matrices:

    det(G_perp_raw) / det(G_para_raw) = phi^{-6}

This is the geometric invariant that drives the stiffness hierarchy. The
phi^{-18} stiffness ratio follows from the 3D volume scaling:

    eta = (det_ratio_raw)^3 = (phi^{-6})^3 = phi^{-18}

This is consistent with the physical argument: the phason stiffness
suppression comes from the ratio of the intrinsic scales of the two
subspaces, not from the normalized projection matrices (which are both
isometries by construction).

Normalization Disambiguation
-----------------------------
- V2 Ch2.1.1 uses N = 1/sqrt(2(2+phi)) - this is N_para, the physical-space isometry.
- Appendix J's N = 1/sqrt(5) is a single-normalization approximation
  (1/sqrt(5) ~ 0.4472 vs N_perp ~ 0.6015), distinct from the two-
  normalization convention adopted here.
- The canonical convention defined here (two-normalization form) is the
  unique choice that simultaneously satisfies orthogonality AND completeness.

Usage
-----
    from gct_projections import get_m_parallel, get_m_perp, verify_properties
    M_para = get_m_parallel()  # shape (3, 6), normalized
    M_perp = get_m_perp()      # shape (3, 6), normalized
    verify_properties()        # asserts all geometric identities
"""

import numpy as np
import sys
import os

from gct_utils import C

# Derived normalization constants (computed once at module load)
# N_para: makes G_para = M_para M_para^T = I_3 (isometry on E_parallel)
# k_para = 2*(2 + phi)  [eigenvalue of M_para_raw @ M_para_raw^T]
PHI_VAL: float = float(C.PHI)
_K_PARA: float = 2.0 * (2.0 + PHI_VAL)
N_PARA: float = 1.0 / np.sqrt(_K_PARA)

# N_perp: makes G_perp = M_perp M_perp^T = I_3 (isometry on E_perp)
# k_perp = 2*(2 + phi')  where phi' = -1/phi is the Galois conjugate
# i.e. k_perp = 2*(2 - 1/phi) [eigenvalue of M_perp_raw @ M_perp_raw^T]
_PHI_CONJ: float = -1.0 / PHI_VAL
_K_PERP: float = 2.0 * (2.0 + _PHI_CONJ)
N_PERP: float = 1.0 / np.sqrt(_K_PERP)


def get_m_parallel() -> np.ndarray:
    """Return the canonical normalized parallel projection matrix M_para (3x6).

    The rows span E_parallel (physical 3-space). With normalization N_para,
    the Gram matrix G_para = M_para @ M_para^T = I_3 exactly.
    """
    p = PHI_VAL
    raw = np.array([
        [ 1,  p,  0, -1,  p,  0],
        [ p,  0,  1,  p,  0, -1],
        [ 0,  1,  p,  0, -1,  p],
    ], dtype=np.float64)
    return N_PARA * raw


def get_m_perp() -> np.ndarray:
    """Return the canonical normalized perpendicular projection matrix M_perp (3x6).

    The rows span E_perp (internal/phason space). The entries use the Galois
    conjugate slope phi' = -1/phi. With normalization N_perp, the Gram matrix
    G_perp = M_perp @ M_perp^T = I_3 exactly.
    """
    ip = _PHI_CONJ
    raw = np.array([
        [ 1, ip,  0, -1, ip,  0],
        [ip,  0,  1, ip,  0, -1],
        [ 0,  1, ip,  0, -1, ip],
    ], dtype=np.float64)
    return N_PERP * raw


def get_m_parallel_unnormalized() -> np.ndarray:
    """Return the unnormalized parallel projection matrix (3x6).

    Use this when computing the Gram determinant ratio phi^{-6} or the
    stiffness ratio phi^{-18}, which are properties of the unnormalized basis.
    """
    p = PHI_VAL
    return np.array([
        [ 1,  p,  0, -1,  p,  0],
        [ p,  0,  1,  p,  0, -1],
        [ 0,  1,  p,  0, -1,  p],
    ], dtype=np.float64)


def get_m_perp_unnormalized() -> np.ndarray:
    """Return the unnormalized perpendicular projection matrix (3x6).

    Use this when computing the Gram determinant ratio phi^{-6} or the
    stiffness ratio phi^{-18}, which are properties of the unnormalized basis.
    """
    ip = _PHI_CONJ
    return np.array([
        [ 1, ip,  0, -1, ip,  0],
        [ip,  0,  1, ip,  0, -1],
        [ 0,  1, ip,  0, -1, ip],
    ], dtype=np.float64)


def get_projector_parallel() -> np.ndarray:
    """P_para = M_para^T M_para, orthogonal projector onto E_parallel.

    Shape (6, 6). Satisfies P_para^2 = P_para, rank = 3.
    """
    M = get_m_parallel()
    return M.T @ M


def get_projector_perp() -> np.ndarray:
    """P_perp = M_perp^T M_perp, orthogonal projector onto E_perp.

    Shape (6, 6). Satisfies P_perp^2 = P_perp, rank = 3.
    """
    M = get_m_perp()
    return M.T @ M


def compute_stiffness_ratio() -> dict:
    """Compute the Gram determinant ratio and stiffness suppression factor.

    The physical stiffness ratio eta = K_perp / K_para is derived from the
    UNNORMALIZED Gram matrices, where the intrinsic scale difference between
    E_parallel and E_perp is preserved.
    """
    M_para_raw = get_m_parallel_unnormalized()
    M_perp_raw = get_m_perp_unnormalized()

    G_para = M_para_raw @ M_para_raw.T
    G_perp = M_perp_raw @ M_perp_raw.T

    det_para = float(np.linalg.det(G_para))
    det_perp = float(np.linalg.det(G_perp))
    det_ratio = det_perp / det_para
    stiffness = det_ratio ** 3

    phi_m6 = PHI_VAL ** (-6)
    phi_m18 = PHI_VAL ** (-18)

    return {
        "det_para_raw": det_para,
        "det_perp_raw": det_perp,
        "det_ratio": det_ratio,
        "stiffness_ratio": stiffness,
        "phi_pow_m6": phi_m6,
        "phi_pow_m18": phi_m18,
        "det_ratio_match": bool(np.isclose(det_ratio, phi_m6, rtol=1e-9)),
        "stiffness_match": bool(np.isclose(stiffness, phi_m18, rtol=1e-9)),
    }


def verify_properties(tol: float = 1e-12, verbose: bool = True) -> bool:
    """Assert all geometric properties of the canonical projection matrices."""
    M_para = get_m_parallel()
    M_perp = get_m_perp()
    P_para = get_projector_parallel()
    P_perp = get_projector_perp()
    I3 = np.eye(3)
    I6 = np.eye(6)

    checks = {}

    checks["shape_para"] = M_para.shape == (3, 6)
    checks["shape_perp"] = M_perp.shape == (3, 6)

    G_para = M_para @ M_para.T
    G_perp = M_perp @ M_perp.T
    checks["gram_para_is_I3"] = bool(np.allclose(G_para, I3, atol=tol))
    checks["gram_perp_is_I3"] = bool(np.allclose(G_perp, I3, atol=tol))

    orth = M_para @ M_perp.T
    checks["orthogonality"] = bool(np.allclose(orth, np.zeros((3, 3)), atol=tol))

    comp = M_para.T @ M_para + M_perp.T @ M_perp
    checks["completeness"] = bool(np.allclose(comp, I6, atol=tol))

    checks["projector_para_idem"] = bool(np.allclose(P_para @ P_para, P_para, atol=tol))
    checks["projector_perp_idem"] = bool(np.allclose(P_perp @ P_perp, P_perp, atol=tol))

    checks["projector_complement"] = bool(np.allclose(P_para + P_perp, I6, atol=tol))

    sr = compute_stiffness_ratio()
    checks["det_ratio_phi_m6"] = sr["det_ratio_match"]
    checks["stiffness_phi_m18"] = sr["stiffness_match"]

    all_passed = all(checks.values())

    if verbose:
        print("\n" + "=" * 60)
        print("  GCT CANONICAL PROJECTION VERIFICATION")
        print(f"  N_para = 1/sqrt(2*(2+phi))  = {N_PARA:.10f}")
        print(f"  N_perp = 1/sqrt(2*(2+phi')) = {N_PERP:.10f}  (phi'=-1/phi)")
        print("=" * 60)

        labels = {
            "shape_para": "M_para shape = (3,6)",
            "shape_perp": "M_perp shape = (3,6)",
            "gram_para_is_I3": "G_para = M_para M_para^T = I_3",
            "gram_perp_is_I3": "G_perp = M_perp M_perp^T = I_3",
            "orthogonality": "M_para M_perp^T = 0_{3x3}",
            "completeness": "M_para^T M_para + M_perp^T M_perp = I_6",
            "projector_para_idem": "P_para^2 = P_para",
            "projector_perp_idem": "P_perp^2 = P_perp",
            "projector_complement": "P_para + P_perp = I_6",
            "det_ratio_phi_m6": f"det(G_perp_raw)/det(G_para_raw) = phi^-6 = {PHI_VAL ** -6:.8f}",
            "stiffness_phi_m18": f"det_ratio^3 = phi^-18 = {PHI_VAL ** -18:.4e}",
        }

        for key, label in labels.items():
            status = "PASS" if checks[key] else "FAIL"
            print(f"  [{status}] {label}")

        print()
        print(f"  Gram errors (max abs):")
        print(f"    G_para - I_3:        {np.max(np.abs(G_para - I3)):.2e}")
        print(f"    G_perp - I_3:        {np.max(np.abs(G_perp - I3)):.2e}")
        print(f"    Orthogonality error: {np.max(np.abs(orth)):.2e}")
        print(f"    Completeness error:  {np.max(np.abs(comp - I6)):.2e}")
        print()
        print(f"  Stiffness ratio (unnorm):")
        print(f"    det(G_para_raw) = {sr['det_para_raw']:.6f}")
        print(f"    det(G_perp_raw) = {sr['det_perp_raw']:.6f}")
        print(f"    det ratio       = {sr['det_ratio']:.10f}")
        print(f"    phi^-6          = {sr['phi_pow_m6']:.10f}")
        print(f"    stiffness eta   = {sr['stiffness_ratio']:.6e}")
        print(f"    phi^-18         = {sr['phi_pow_m18']:.6e}")
        print()

        if all_passed:
            print("  RESULT: ALL PROPERTIES VERIFIED")
        else:
            failed = [k for k, v in checks.items() if not v]
            print(f"  RESULT: FAILED -- {failed}")
        print("=" * 60 + "\n")

    return all_passed


def project_parallel(v: np.ndarray) -> np.ndarray:
    """Project a 6D lattice vector v into E_parallel (physical space)."""
    M = get_m_parallel()
    return v @ M.T


def project_perp(v: np.ndarray) -> np.ndarray:
    """Project a 6D lattice vector v into E_perp (internal/phason space)."""
    M = get_m_perp()
    return v @ M.T


def get_gram_determinants() -> dict:
    """Alias for compute_stiffness_ratio to satisfy Protocol interface."""
    return compute_stiffness_ratio()


if __name__ == "__main__":
    ok = verify_properties(tol=1e-12, verbose=True)

    sr = compute_stiffness_ratio()
    print("Stiffness Ratio Summary:")
    for k, v in sr.items():
        print(f"  {k:<25} = {v}")

    print("\nExample projections (standard basis vectors of Z^6):")
    M_para = get_m_parallel()
    M_perp = get_m_perp()
    for i in range(6):
        e = np.zeros(6)
        e[i] = 1.0
        para = M_para @ e
        perp = M_perp @ e
        print(f"  e_{i + 1} -> E_para: {np.round(para, 4)} | E_perp: {np.round(perp, 4)}")

    sys.exit(0 if ok else 1)
