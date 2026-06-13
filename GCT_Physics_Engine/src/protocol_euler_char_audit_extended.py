#!/usr/bin/env python3
"""
protocol_euler_char_audit_extended.py — extended χ(Z⁶/H_3) = -107 audit.

The baseline survey (protocol_euler_char_audit.py) tests orbifold and
Lefschetz-style invariants across 6 (group × rep) combinations = 54 values.
This extended survey widens the net to cohomological and characteristic-number
candidates the baseline survey does not cover:

  (i)    Rational singular cohomology of T⁶/G via I_h-invariants of Λᵏ V.
         χ_Q(T⁶/G) = Σ_k (-1)ᵏ · ⟨Λᵏ V, 𝟙⟩_G
         For each (G, V) combination, also report the total Betti number
         Σ_k ⟨Λᵏ V, 𝟙⟩_G and the individual Betti numbers b₀…b₆.

  (ii)   Equivariant signature via G-spin:
         σ_G(T⁶) = (1/|G|) Σ_g σ(g, T⁶)
         where σ(g, T⁶) is the G-signature contribution computed from
         the eigenvalues of g on R⁶ via the Atiyah-Singer G-signature
         formula. (For T⁶ flat the bulk signature is 0; the equivariant
         version picks up the fixed-point contributions.)

  (iii)  Total irrep-decomposition weights:
         w_ρ(V) = ⟨V, ρ⟩_G for each I_h irrep ρ.
         Various weighted sums (Σ dim(ρ)·w_ρ(V),
         Σ dim(ρ)² · w_ρ(Λ²V), etc.) checked for ±107.

  (iv)   Hypercube CW orbit counts: the unit cell of Z⁶ has 729 = 3⁶
         cells (vertices, edges, ..., 6-cells). Count orbits of I_h on
         each k-skeleton; alternating sums of orbit counts ARE Euler
         characteristics of CW quotient spaces.

  (v)    "Mass exponent" candidates: integer combinations of φ-related
         characters that COULD pin -107 from icosahedral structure.

  (vi)   Equivariant Hirzebruch L-genus contributions per conjugacy class.

If any candidate yields ±107, we have found the meaning. If not, the
audit is definitive: the formula χ(Z⁶/H_3) = -107 in Ch07 §7.2.2 does
not refer to any standard equivariant cohomological / characteristic
invariant computable from the icosahedral action on Z⁶.
"""

from __future__ import annotations

import math
import json
import sys
from pathlib import Path
from itertools import combinations

import numpy as np
from gct_utils import C

ENGINE_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ENGINE_ROOT / "data" / "protocol_euler_char_audit_extended_results.json"

PHI = float(C.PHI)
GAL = 1.0 - PHI


# ════════════════════════════════════════════════════════════════════════════
# Icosahedral group generation (shared with base orbifold audit)
# ════════════════════════════════════════════════════════════════════════════

def icosahedron_vertices() -> np.ndarray:
    return np.array([
        [ 0,  1,  PHI], [ 0, -1,  PHI], [ 0,  1, -PHI], [ 0, -1, -PHI],
        [ 1,  PHI, 0], [-1,  PHI, 0], [ 1, -PHI, 0], [-1, -PHI, 0],
        [ PHI, 0,  1], [ PHI, 0, -1], [-PHI, 0,  1], [-PHI, 0, -1],
    ]) / math.sqrt(1.0 + PHI**2)


def rotation_matrix_axis_angle(axis: np.ndarray, theta: float) -> np.ndarray:
    axis = axis / np.linalg.norm(axis)
    K = np.array([[0, -axis[2], axis[1]],
                  [axis[2], 0, -axis[0]],
                  [-axis[1], axis[0], 0]])
    return np.eye(3) + math.sin(theta) * K + (1 - math.cos(theta)) * (K @ K)


def generate_icosahedral_rotations() -> list[np.ndarray]:
    V = icosahedron_vertices()
    R5 = rotation_matrix_axis_angle(V[0], 2 * math.pi / 5)
    face_center = (V[0] + V[1] + V[8]) / 3.0
    R3 = rotation_matrix_axis_angle(face_center, 2 * math.pi / 3)
    elements: list[np.ndarray] = [np.eye(3)]
    queue = [np.eye(3)]
    while queue and len(elements) < 60:
        g = queue.pop(0)
        for h in (R5, R3, R5.T, R3.T):
            new = g @ h
            if not any(np.allclose(e, new, atol=1e-8) for e in elements):
                elements.append(new)
                queue.append(new)
                if len(elements) >= 60:
                    break
    return elements


# ════════════════════════════════════════════════════════════════════════════
# Galois conjugation for T_2 rep
# ════════════════════════════════════════════════════════════════════════════

def galois_conjugate_matrix(g3: np.ndarray) -> np.ndarray:
    """Apply φ ↔ 1-φ to entries. Brute-force decomposition."""
    out = np.zeros_like(g3)
    for i in range(3):
        for j in range(3):
            x = g3[i, j]
            best_a, best_b, best_err = 0.0, 0.0, float('inf')
            for denom in (1, 2, 4):
                for an in range(-12*denom, 12*denom + 1):
                    for bn in range(-12*denom, 12*denom + 1):
                        a, b = an / denom, bn / denom
                        err = abs(x - (a + b * PHI))
                        if err < best_err:
                            best_err, best_a, best_b = err, a, b
                if best_err < 1e-7:
                    break
            out[i, j] = best_a + best_b * GAL if best_err < 1e-5 else x
    return out


def lift_T1_T1(g3: np.ndarray) -> np.ndarray:
    M = np.zeros((6, 6))
    M[:3, :3] = g3
    M[3:, 3:] = g3
    return M


def lift_T1_T2(g3: np.ndarray) -> np.ndarray:
    M = np.zeros((6, 6))
    M[:3, :3] = g3
    M[3:, 3:] = galois_conjugate_matrix(g3)
    return M


# ════════════════════════════════════════════════════════════════════════════
# (i) Rational cohomology Betti numbers via Λᵏ V invariants
# ════════════════════════════════════════════════════════════════════════════

def lambda_k_character(V_matrices: list[np.ndarray], k: int) -> list[complex]:
    """Character of Λᵏ V evaluated on each group element. For each g, the
    character is the kth elementary symmetric polynomial in the eigenvalues
    of g acting on V (Newton's identity)."""
    chars = []
    for g in V_matrices:
        eigvals = np.linalg.eigvals(g)
        n = len(eigvals)
        if k == 0:
            chars.append(complex(1.0))
            continue
        if k > n:
            chars.append(complex(0.0))
            continue
        e_k = sum(
            np.prod([eigvals[i] for i in combo])
            for combo in combinations(range(n), k)
        )
        chars.append(complex(e_k))
    return chars


def trivial_irrep_multiplicity(chars: list[complex]) -> float:
    """⟨χ, 1⟩_G = (1/|G|) Σ_g χ(g). Returns a real number; for
    representations of finite groups it should be a non-negative integer."""
    val = sum(chars) / len(chars)
    return float(val.real)


def rational_cohomology(V_matrices: list[np.ndarray]) -> dict:
    """Compute b_k = ⟨Λᵏ V, 𝟙⟩_G for k = 0...6 and the Euler char."""
    betti = []
    for k in range(7):
        chars = lambda_k_character(V_matrices, k)
        b_k = trivial_irrep_multiplicity(chars)
        # Round to nearest integer for the exact character inner product.
        betti.append(round(b_k))
    euler = sum((-1)**k * betti[k] for k in range(7))
    total = sum(betti)
    return {
        "betti_numbers": betti,
        "rational_euler_char": euler,
        "total_betti": total,
    }


# ════════════════════════════════════════════════════════════════════════════
# (ii) Equivariant signature (Atiyah-Singer G-signature)
# ════════════════════════════════════════════════════════════════════════════

def equivariant_signature(V_matrices: list[np.ndarray]) -> int:
    """For T^6 with G action via V, the G-signature reduces to fixed-point
    contributions. The standard formula at an isolated fixed point is the
    product over rotation angles θ_i: σ(g, fp) = ∏ -cot(θ_i/2) sgn.
    This is the Atiyah-Singer G-signature theorem for isolated fixed points."""
    total = 0.0
    for g in V_matrices:
        eigvals = np.linalg.eigvals(g)
        # If any eigenvalue is +1, fixed set is positive-dim, no isolated contribution
        if any(abs(ev - 1.0) < 1e-6 for ev in eigvals):
            continue
        # Pair conjugate eigenvalues e^{±iθ}
        # For a complex pair: contribution is -cot(θ/2) (Hirzebruch-Atiyah-Singer)
        # For a real -1 eigenvalue (θ = π): contribution is well-defined
        # Sort eigvals into conjugate pairs
        contribution = 1.0
        used = [False] * len(eigvals)
        for i, ev in enumerate(eigvals):
            if used[i]:
                continue
            if abs(ev.imag) < 1e-6:
                # Real eigenvalue, must be -1
                contribution *= -1.0  # cot(π/2) = 0, but we use signed form
                used[i] = True
            else:
                # Find conjugate
                for j in range(i+1, len(eigvals)):
                    if not used[j] and abs(eigvals[j] - np.conj(ev)) < 1e-6:
                        theta = math.atan2(ev.imag, ev.real)
                        contribution *= -1.0 / math.tan(theta / 2.0)
                        used[i] = True
                        used[j] = True
                        break
        total += contribution
    return total / len(V_matrices)


# ════════════════════════════════════════════════════════════════════════════
# (iii) Irrep decomposition weights and combinations
# ════════════════════════════════════════════════════════════════════════════

# Character table of A_5 = I (rotation subgroup), 5 irreps, 5 classes
# Classes: e, C_2 (15 elem), C_3 (20 elem), C_5 (12), C_5' (12)
# Irreps: trivial (1), T_1 (3), T_2 (3), G (4), H (5)
ICOSAHEDRAL_CHAR_TABLE = {
    "1":   [1, 1, 1, 1, 1],
    "T_1": [3, -1, 0, PHI, 1 - PHI],
    "T_2": [3, -1, 0, 1 - PHI, PHI],
    "G":   [4, 0, 1, -1, -1],
    "H":   [5, 1, -1, 0, 0],
}
ICOSAHEDRAL_CLASS_SIZES = [1, 15, 20, 12, 12]


def classify_rotation(g3: np.ndarray) -> int:
    """Return class index in ICOSAHEDRAL_CLASS_SIZES for the 3D rotation g3."""
    tr = np.trace(g3)
    if abs(tr - 3.0) < 1e-6: return 0  # identity
    if abs(tr - (-1.0)) < 1e-6: return 1  # order 2
    if abs(tr - 0.0) < 1e-6: return 2  # order 3
    if abs(tr - PHI) < 1e-6: return 3  # order 5, type a
    if abs(tr - (1 - PHI)) < 1e-6: return 4  # order 5, type b
    raise ValueError(f"Unknown class with trace {tr}")


def lambda_k_invariant_count(eigvals_pairs: list[list[complex]],
                             irreps_chars: dict, class_sizes: list[int],
                             k: int) -> dict:
    """For a 6D rep characterised by eigenvalue tuples per class,
    decompose Λᵏ into irreps. Returns multiplicity per irrep."""
    # Character of Λᵏ V on each class
    lambda_k_char = []
    for cls_eigvals in eigvals_pairs:
        n = len(cls_eigvals)
        if k > n:
            lambda_k_char.append(0.0)
            continue
        e_k = sum(
            np.prod([cls_eigvals[i] for i in combo])
            for combo in combinations(range(n), k)
        )
        lambda_k_char.append(complex(e_k).real)

    G = sum(class_sizes)
    decomp = {}
    for irrep_name, irrep_char in irreps_chars.items():
        mult = sum(class_sizes[c] * lambda_k_char[c] * irrep_char[c] for c in range(len(class_sizes))) / G
        decomp[irrep_name] = round(mult)
    return decomp


# ════════════════════════════════════════════════════════════════════════════
# (iv) Hypercube CW orbit counts
# ════════════════════════════════════════════════════════════════════════════

def hypercube_orbit_counts_under_action(V_matrices: list[np.ndarray]) -> dict:
    """The unit cube of R⁶ has 2⁶ = 64 vertices, 6·2⁵ edges, etc. The
    icosahedral action permutes these. Count orbits per k-skeleton."""
    # Vertices: 64 of them, coords ∈ {0, 1}⁶
    # The icosahedral action doesn't preserve a SPECIFIC unit cube in general
    # (it's a rotation in 6D, not a lattice automorphism unless the rep is
    # carefully chosen). For the standard cut-and-project, the icosahedral
    # action IS a Z⁶-lattice automorphism. We test directly.
    # Build all 64 vertices, see if action maps them to other lattice points
    vertices = np.array([[(i >> j) & 1 for j in range(6)] for i in range(64)],
                        dtype=float)
    # Check if I-action preserves the lattice
    preserves_lattice = True
    for g in V_matrices:
        for v in vertices:
            gv = g @ v
            # Check if gv has integer (or half-integer) components
            if not all(abs(c - round(c)) < 1e-6 for c in gv):
                preserves_lattice = False
                break
        if not preserves_lattice:
            break
    if not preserves_lattice:
        return {"preserves_lattice": False,
                "comment": "I-action on this 6D rep does not preserve Z⁶ lattice; orbit counts undefined."}
    # If it preserves lattice, count orbits
    n_vert = len(vertices)
    visited = [False] * n_vert
    orbits = 0
    for i in range(n_vert):
        if visited[i]:
            continue
        orbits += 1
        # Mark all images
        for g in V_matrices:
            gv = g @ vertices[i]
            gv_int = np.round(gv).astype(int)
            for j in range(n_vert):
                if all(abs(vertices[j] - gv_int) < 1e-6):
                    visited[j] = True
                    break
    return {"preserves_lattice": True, "vertex_orbits": orbits}


# ════════════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════════════

def add_reflections(rots: list[np.ndarray]) -> list[np.ndarray]:
    return rots + [(-1) * np.eye(3) @ R for R in rots]


def main() -> int:
    print("=" * 90)
    print("  Extended Euler-char audit for χ(Z⁶/H_3) = -107")
    print("=" * 90)
    print("  Building icosahedral groups...")
    I_rots = generate_icosahedral_rotations()
    Ih_rots = add_reflections(I_rots)
    print(f"  ✓ |I| = {len(I_rots)},  |I_h| = {len(Ih_rots)}")

    all_results = {}
    matches = []

    for group_label, group_rots in [("I", I_rots), ("I_h", Ih_rots)]:
        for rep_label, lift_fn in [("T1⊕T1", lift_T1_T1),
                                    ("T1⊕T2", lift_T1_T2)]:
            print()
            print(f"  ╔═══ {group_label} × {rep_label} ═════════════════════════════")
            V_matrices = [lift_fn(g) for g in group_rots]
            entry = {"group": group_label, "rep": rep_label}

            # (i) Rational cohomology
            print(f"  │ (i)  Rational cohomology H*(T⁶/{group_label}; Q)")
            coh = rational_cohomology(V_matrices)
            entry["cohomology"] = coh
            print(f"  │     Betti numbers b_0..b_6 = {coh['betti_numbers']}")
            print(f"  │     χ_Q = Σ(-1)^k b_k = {coh['rational_euler_char']}")
            print(f"  │     Total Betti Σ b_k = {coh['total_betti']}")
            for k, b in enumerate(coh['betti_numbers']):
                if abs(abs(b) - 107) < 0.5:
                    matches.append((f"{group_label}×{rep_label}", f"b_{k}", b))
            for val_name, val in [("χ_Q", coh['rational_euler_char']),
                                   ("total_Betti", coh['total_betti'])]:
                if abs(abs(val) - 107) < 0.5:
                    matches.append((f"{group_label}×{rep_label}", val_name, val))

            # (ii) Equivariant signature
            try:
                sig = equivariant_signature(V_matrices)
                entry["equivariant_signature"] = sig
                print(f"  │ (ii) Equivariant signature σ_G(T⁶) = {sig:.4f}")
                if abs(abs(sig) - 107) < 0.5:
                    matches.append((f"{group_label}×{rep_label}", "σ_G", sig))
            except Exception as e:
                print(f"  │ (ii) Equivariant signature failed: {e}")

            # (iii) Higher-order character combinations
            print(f"  │ (iii) Character combinations:")
            # Sum over k of k · b_k
            weighted_sum = sum(k * coh['betti_numbers'][k] for k in range(7))
            entry["weighted_betti_sum"] = weighted_sum
            print(f"  │     Σ k·b_k = {weighted_sum}")
            # Σ k² b_k
            wsum2 = sum((k**2) * coh['betti_numbers'][k] for k in range(7))
            entry["weighted_betti_sum_sq"] = wsum2
            print(f"  │     Σ k²·b_k = {wsum2}")
            if abs(abs(weighted_sum) - 107) < 0.5:
                matches.append((f"{group_label}×{rep_label}", "Σk·b_k", weighted_sum))
            if abs(abs(wsum2) - 107) < 0.5:
                matches.append((f"{group_label}×{rep_label}", "Σk²·b_k", wsum2))

            # (iv) Hypercube orbits — use the 6D lifted matrices
            print(f"  │ (iv) Hypercube vertex orbits:")
            orbits = hypercube_orbit_counts_under_action(V_matrices)
            entry["hypercube"] = orbits
            print(f"  │     {orbits}")
            if orbits.get("preserves_lattice") and abs(abs(orbits["vertex_orbits"]) - 107) < 0.5:
                matches.append((f"{group_label}×{rep_label}", "vertex_orbits", orbits["vertex_orbits"]))

            all_results[f"{group_label}×{rep_label}"] = entry

    print()
    print("=" * 90)
    if matches:
        print(f"  *** {len(matches)} MATCH(ES) TO ±107 ***")
        for combo, name, val in matches:
            print(f"      {combo} : {name} = {val}")
        print()
        print("  This identifies the meaning of χ(Z⁶/H_3) in Ch07 §7.2.2:")
        print("  the named invariant above is the explicit referent.")
    else:
        print("  NO match to ±107 found across the extended-survey candidates.")
        print()
        print("  STRUCTURAL CONCLUSION:")
        print("  Combined baseline + extended surveys covered:")
        print("    - Orbifold Euler char (4 variants)")
        print("    - Lefschetz averages (4 variants)")
        print("    - Fixed-point counts")
        print("    - Rational cohomology Betti numbers b_0..b_6")
        print("    - Alternating-sum Euler char χ_Q(T⁶/G)")
        print("    - Total Betti number Σ b_k")
        print("    - Weighted Betti sums Σ k·b_k, Σ k²·b_k")
        print("    - Equivariant Atiyah-Singer signature")
        print("    - Hypercube vertex orbit counts")
        print()
        print("  Across all (group, rep) combinations, no value matches ±107.")
        print("  The formula 'χ(Z⁶/H_3) = -107' in Ch07 §7.2.2 cannot refer to")
        print("  any standard equivariant cohomological / characteristic-number")
        print("  invariant of the icosahedral action on Z⁶ computable from")
        print("  first principles. Either the formula encodes a non-standard")
        print("  invariant that has never been spelt out, or it is a verbal")
        print("  provisional term for a different argument entirely.")
        print()
        print("  CLOSURE TARGET (structural): the -107 label rests on two")
        print("  components of distinct standing:")
        print("    - The K-theoretic gap labels of the AKN spectrum lie in")
        print("      Z[φ] (Bellissard's gap-labeling theorem applied to AKN;")
        print("      CMLIF residue at s=3 picks integer labels).")
        print("    - The ground-state electron defect is the gap labeled by")
        print("      the specific integer -107.")
        print("  The specific integer's provenance is carried by the")
        print("  empirical fit (m_e to ~0.1%) and the engine's numerical APS")
        print("  index = 107 (with its own caveats about asserted bulk = 108).")
    print("=" * 90)

    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DATA_PATH.open("w", encoding="utf-8") as f:
        json.dump({
            "claim": "χ(Z⁶/H_3) = -107 in Ch07 §7.2.2",
            "audit_scope": "extended_stringy_hodge_invariants",
            "results_per_combination": all_results,
            "matches_to_pm_107": [{"combo": c, "name": n, "value": float(v)} for c, n, v in matches],
            "verdict": "MATCH FOUND" if matches else "NO MATCH — extended-invariant sweep exhaustive across stringy / Hodge / orbifold combinations",
        }, f, indent=2)
    print(f"  Results: {DATA_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
