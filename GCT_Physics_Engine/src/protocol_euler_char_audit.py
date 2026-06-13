#!/usr/bin/env python3
"""
protocol_euler_char_audit.py — survey testing whether the value
'χ(Z⁶/H_3) = -107' in Ch07 §7.2.2 corresponds to a standard invariant.

The Tier-1 referent requires an explicit invariant definition. This script
enumerates the full
icosahedral group I_h (= H_3 Coxeter, order 120), lifts it to a 6-dim
linear action on R⁶ via three candidate representations consistent with
the cut-and-project setting, then computes EVERY natural "Euler-character-
like" invariant of the resulting Z⁶ action, looking for any that lands on
±107.

If exactly one candidate invariant hits ±107, that fixes the intended
meaning of "χ(Z⁶/H_3)" in the chapter, and the Tier 1 claim has a precise
referent. If no candidate matches, the value is not uniquely defined by this
construction: a precise definition for "χ" in this context, or an alternative
derivation of -107, remains the closure target.

Generators of the icosahedral rotation group I = A_5 used here come from
standard references (Coxeter, *Regular Polytopes*, §11.5). The two 3-dim
irreps T_1 and T_2 of I are Galois conjugates over Q(√5): T_2(g) is obtained
from T_1(g) by the field automorphism φ ↔ -1/φ = 1-φ.
"""

from __future__ import annotations

import math
import json
import sys
from pathlib import Path

import numpy as np
from gct_utils import C

ENGINE_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ENGINE_ROOT / "data" / "protocol_euler_char_audit_results.json"

PHI = float(C.PHI)
GAL = 1.0 - PHI                # Galois conjugate: φ̄ = 1 - φ = -1/φ


# ════════════════════════════════════════════════════════════════════════════
# Build icosahedral group I = A_5 as 60 rotation matrices in SO(3).
# ════════════════════════════════════════════════════════════════════════════
# Method: start with the 12 vertices of the icosahedron (unit vectors), find
# all rotations that permute them, deduplicate by matrix-near-equality.

def icosahedron_vertices() -> np.ndarray:
    """The 12 vertices of a regular icosahedron centered at origin, in a
    convention with two vertices on the z-axis."""
    return np.array([
        [ 0,  1,  PHI], [ 0, -1,  PHI], [ 0,  1, -PHI], [ 0, -1, -PHI],
        [ 1,  PHI, 0], [-1,  PHI, 0], [ 1, -PHI, 0], [-1, -PHI, 0],
        [ PHI, 0,  1], [ PHI, 0, -1], [-PHI, 0,  1], [-PHI, 0, -1],
    ]) / math.sqrt(1.0 + PHI**2)


def rotation_matrix_axis_angle(axis: np.ndarray, theta: float) -> np.ndarray:
    """Rodrigues' rotation formula."""
    axis = axis / np.linalg.norm(axis)
    K = np.array([[0, -axis[2], axis[1]],
                  [axis[2], 0, -axis[0]],
                  [-axis[1], axis[0], 0]])
    return np.eye(3) + math.sin(theta) * K + (1 - math.cos(theta)) * (K @ K)


def generate_icosahedral_rotations() -> list[np.ndarray]:
    """Generate all 60 rotations in I = A_5 by composing generators."""
    V = icosahedron_vertices()

    # Five-fold rotation about vertex 0 (axis = V[0])
    R5 = rotation_matrix_axis_angle(V[0], 2 * math.pi / 5)
    # Three-fold rotation about a face center (average of 3 adjacent vertices).
    # The triangle V[0], V[1], V[8] forms a face; its centroid is the 3-fold axis.
    face_center = (V[0] + V[1] + V[8]) / 3.0
    R3 = rotation_matrix_axis_angle(face_center, 2 * math.pi / 3)

    # BFS through compositions until we have all 60.
    elements: list[np.ndarray] = [np.eye(3)]
    queue = [np.eye(3)]
    while queue:
        g = queue.pop(0)
        for h in (R5, R3, R5.T, R3.T):
            new = g @ h
            duplicate = False
            for e in elements:
                if np.allclose(e, new, atol=1e-8):
                    duplicate = True
                    break
            if not duplicate:
                elements.append(new)
                queue.append(new)
                if len(elements) >= 60:
                    break
        if len(elements) >= 60:
            break
    assert len(elements) == 60, f"Expected 60, got {len(elements)}"
    return elements


def add_reflections(rotations: list[np.ndarray]) -> list[np.ndarray]:
    """I_h = I ∪ (-I × I) where -I is inversion. Yields 120 elements."""
    inv = -np.eye(3)
    return rotations + [inv @ R for R in rotations]


# ════════════════════════════════════════════════════════════════════════════
# Three 6-dim representations of I (and I_h)
# ════════════════════════════════════════════════════════════════════════════

def lift_T1_T1(g3: np.ndarray) -> np.ndarray:
    """Two copies of the standard T_1 (defining) rep: R⁶ = R³ ⊕ R³."""
    M = np.zeros((6, 6))
    M[:3, :3] = g3
    M[3:, 3:] = g3
    return M


def galois_conjugate_matrix(g3: np.ndarray) -> np.ndarray:
    """Apply the field automorphism φ ↔ 1-φ entry-wise. For a matrix whose
    entries are linear combinations of 1 and φ, swap the φ coefficient with
    (1-φ) coefficient. We detect the φ-coefficient by exhaustive numerical
    matching."""
    out = np.zeros_like(g3)
    for i in range(3):
        for j in range(3):
            x = g3[i, j]
            # Express x = a + b·φ with a, b rational (small integer denoms).
            # Try denominators 1, 2, 4, sqrt(...) — but for icosahedral matrices
            # entries are in Z[φ]/k for small k. Use a search.
            best_a, best_b = None, None
            best_err = float('inf')
            for denom in (1, 2, 4):
                for a_num in range(-12*denom, 12*denom + 1):
                    for b_num in range(-12*denom, 12*denom + 1):
                        a, b = a_num / denom, b_num / denom
                        err = abs(x - (a + b * PHI))
                        if err < best_err:
                            best_err = err
                            best_a, best_b = a, b
                if best_err < 1e-7:
                    break
            if best_err > 1e-5:
                # Fall back to numerical conjugation: x has only rational part
                out[i, j] = x
            else:
                out[i, j] = best_a + best_b * GAL
    return out


def lift_T1_T2(g3: np.ndarray) -> np.ndarray:
    """T_1 ⊕ T_2: defining rep plus its Galois conjugate. This is the
    'standard cut-and-project' 6-dim rep used for icosahedral quasicrystals."""
    M = np.zeros((6, 6))
    M[:3, :3] = g3
    M[3:, 3:] = galois_conjugate_matrix(g3)
    return M


def lift_T1_T1_with_inversion(g3: np.ndarray, det_sign: float) -> np.ndarray:
    """T_1g ⊕ T_1u: both copies of T_1 but second copy multiplied by det(g)
    (so the second copy is ungerade under inversion)."""
    M = np.zeros((6, 6))
    M[:3, :3] = g3
    M[3:, 3:] = det_sign * g3
    return M


# ════════════════════════════════════════════════════════════════════════════
# Candidate "Euler-characteristic-like" invariants of the Z⁶ action
# ════════════════════════════════════════════════════════════════════════════

def fixed_torus_dim(M: np.ndarray) -> int:
    """Dimension of the +1 eigenspace of M (= dim of Fix(g) on T⁶)."""
    eigvals = np.linalg.eigvals(M)
    return int(np.sum(np.abs(eigvals - 1.0) < 1e-6))


def fixed_set_euler(M: np.ndarray) -> int:
    """Euler char of Fix(g, T⁶): 0 if positive-dim, else det_Z(I - M) lattice
    points (= 1 if no eigenvalue equals 1)."""
    d = fixed_torus_dim(M)
    if d > 0:
        return 0
    # All eigenvalues ≠ 1, so Fix(g, T⁶) is finitely many points.
    # Count = |det(I - M)|.
    return int(round(abs(np.linalg.det(np.eye(6) - M))))


def det_sign(M: np.ndarray) -> int:
    """+1 (proper rotation in O(6)) or -1 (improper) — Reflections."""
    return int(round(np.sign(np.linalg.det(M))))


def reflection_count_3d(g3: np.ndarray) -> int:
    """+1 if g3 ∈ SO(3) (proper rotation), -1 if reflection (det = -1)."""
    return int(round(np.sign(np.linalg.det(g3))))


# ════════════════════════════════════════════════════════════════════════════
# MAIN: enumerate, lift, compute all candidate Euler-char-like sums
# ════════════════════════════════════════════════════════════════════════════

def compute_invariants(rotations_3d: list[np.ndarray],
                       include_reflections: bool,
                       lift_name: str,
                       lift_fn) -> dict:
    """For a fixed 6D rep, compute an array of Euler-char-like candidates."""
    if include_reflections:
        elements_3d = add_reflections(rotations_3d)
    else:
        elements_3d = list(rotations_3d)
    G = len(elements_3d)

    invariants = {
        "orbifold_chi":        0.0,   # (1/|G|) Σ χ(Fix(g, T⁶))
        "signed_orbifold_chi": 0.0,   # (1/|G|) Σ det(g)·χ(Fix(g, T⁶))
        "lefschetz_avg":       0.0,   # (1/|G|) Σ det(I - M)
        "signed_lefschetz":    0.0,   # (1/|G|) Σ det(g)·det(I - M)
        "fixed_point_count":   0,     # # elements with isolated fixed set on T⁶
        "improper_count":      0,     # # elements with det = -1 (reflections)
        "lefschetz_sum":       0.0,   # plain Σ det(I - M) — Atiyah-Bott style
        "signed_lef_sum":      0.0,   # Σ det(g) · det(I - M)
        "alt_signature_sum":   0.0,   # Σ (-1)^d_fix · det(I - M) for non-zero
    }

    for g3 in elements_3d:
        # Build the 6D matrix using the chosen lift
        if lift_name == "T1_T1_signed":
            M = lift_fn(g3, reflection_count_3d(g3))
        else:
            M = lift_fn(g3)

        d_fix = fixed_torus_dim(M)
        chi_fix = fixed_set_euler(M)
        det6 = det_sign(M)
        lefschetz = np.linalg.det(np.eye(6) - M)
        # Round to nearest integer when very close (Lefschetz integer for unit lattice)
        lefschetz_int = lefschetz if abs(lefschetz - round(lefschetz)) > 0.01 else round(lefschetz)

        invariants["orbifold_chi"] += chi_fix
        invariants["signed_orbifold_chi"] += det6 * chi_fix
        invariants["lefschetz_avg"] += lefschetz_int
        invariants["signed_lefschetz"] += det6 * lefschetz_int
        invariants["lefschetz_sum"] += lefschetz_int
        invariants["signed_lef_sum"] += det6 * lefschetz_int
        if chi_fix > 0:
            invariants["fixed_point_count"] += 1
            invariants["alt_signature_sum"] += ((-1) ** d_fix) * chi_fix
        if det6 < 0:
            invariants["improper_count"] += 1

    # Normalize the averages
    invariants["orbifold_chi"]        /= G
    invariants["signed_orbifold_chi"] /= G
    invariants["lefschetz_avg"]       /= G
    invariants["signed_lefschetz"]    /= G

    invariants["G"] = G
    return invariants


def main() -> int:
    print("=" * 90)
    print("  Invariant survey: χ(Z⁶/H_3) = -107  [Ch07 §7.2.2]")
    print("=" * 90)
    print("  Building I = A_5 (60 rotations) by Coxeter generators...")
    I_rots = generate_icosahedral_rotations()
    print(f"  ✓ |I| = {len(I_rots)}")

    print()
    print("  Testing whether ANY natural Euler-char-like invariant of the")
    print("  icosahedral action on Z⁶ lands on ±107 under three candidate")
    print("  6-dim representations:")
    print()

    results = {}
    for group_name, include_refl in [("I  (60 rotations)", False),
                                      ("I_h (120 incl. reflections)", True)]:
        for lift_name, lift_fn in [("T1 ⊕ T1", lift_T1_T1),
                                    ("T1 ⊕ T2 (Galois)", lift_T1_T2),
                                    ("T1g ⊕ T1u (signed)", lift_T1_T1_with_inversion)]:
            key = f"{group_name} | {lift_name}"
            print(f"  ── {key} ─" + "─" * max(0, 60 - len(key)))
            try:
                inv = compute_invariants(I_rots, include_refl, lift_name.replace("T1g ⊕ T1u (signed)", "T1_T1_signed"), lift_fn)
            except Exception as e:
                print(f"    [ERROR] {type(e).__name__}: {e}")
                continue
            results[key] = inv
            for name, val in inv.items():
                marker = "  *** MATCHES -107 ***" if isinstance(val, (int, float)) and abs(val + 107) < 0.5 else \
                         ("  *** MATCHES +107 ***" if isinstance(val, (int, float)) and abs(val - 107) < 0.5 else "")
                if isinstance(val, (int, float)):
                    print(f"    {name:<28} = {val:>14.4f}{marker}")
                else:
                    print(f"    {name:<28} = {val}")
            print()

    print("=" * 90)
    # Report whether any candidate matched +/-107.
    any_match = False
    for k, inv in results.items():
        for name, val in inv.items():
            if isinstance(val, (int, float)) and abs(abs(val) - 107) < 0.5:
                print(f"  MATCH: {k} : {name} = {val}")
                any_match = True

    if not any_match:
        print("  NO MATCH found among the candidate Euler-char-like invariants.")
        print()
        print("  CONCLUSION: 'χ(Z⁶/H_3) = -107' as asserted in Ch07 §7.2.2 does")
        print("  NOT correspond to any standard orbifold / equivariant /")
        print("  Lefschetz-style Euler-characteristic invariant of the icosahedral")
        print("  action on Z⁶ under any of the three natural 6-dim representations")
        print("  surveyed. The chapter cites this Euler characteristic as one of")
        print("  the two constraints determining the K-theoretic gap label -107,")
        print("  but the invariant it refers to is not specified and not")
        print("  recoverable from the candidates tested here.")
        print()
        print("  CLOSURE TARGET: the Tier-1 referent of χ(Z⁶/H_3) requires either")
        print("  (a) an explicit definition of χ(Z⁶/H_3) together with a separate")
        print("  derivation showing it equals -107; or (b) the independent")
        print("  Bellissard gap-labeling argument (which uses CMLIF + KMS state,")
        print("  not Euler characteristic), under which the -107 label is carried")
        print("  by the gap-labeling constraint rather than the Euler-char step.")
    print("=" * 90)

    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DATA_PATH.open("w", encoding="utf-8") as f:
        json.dump({
            "claim": "χ(Z⁶/H_3) = -107 in Ch07 §7.2.2",
            "candidates_surveyed": list(results.keys()),
            "invariants_per_candidate": {k: {kk: float(vv) if isinstance(vv, (int, float)) else vv for kk, vv in v.items()}
                                         for k, v in results.items()},
            "any_match_to_pm_107": any_match,
            "conclusion": (
                "No candidate Euler-char-like invariant matches ±107"
                if not any_match else
                "Match(es) found — see invariants_per_candidate"
            ),
        }, f, indent=2)
    print(f"  Results: {DATA_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
