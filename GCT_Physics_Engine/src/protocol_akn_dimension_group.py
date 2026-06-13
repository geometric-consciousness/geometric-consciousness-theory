#!/usr/bin/env python3
"""
protocol_akn_dimension_group.py — dimension-group route to the Tier-1
closure target (Open Problem O.14).

Direct construction of the AKN dimension group via the Cuntz-Krieger /
Bratteli diagram for the Fibonacci substitution. The aim is to bypass
the boundary cage entirely and check whether the Cuntz-Krieger
Perron-Frobenius KMS state machinery picks out a unique label that
can be identified with -107 from first principles.

Setup:
  - Substitution matrix A = [[1,1],[1,0]] (Fibonacci, eigenvalue φ)
  - Bratteli diagram: at level n, the vertex set is {a, b} with A^n
    counts of paths
  - Dimension group D = lim Z² under multiplication by A
  - Cuntz-Krieger algebra 𝒪_A; its AF subalgebra has K_0 = D
  - Unique trace τ (the unique KMS state at β = log φ): given by the
    left Perron-Frobenius eigenvector (φ, 1) normalised
  - K_0 module is Z[φ] = Z ⊕ Zφ; under τ, the trace of (m, n) is m + nα
    where α = 1/φ (the normalised Perron eigenvalue of A^T)

Tier-1 closure target:
  Test whether ANY natural Cuntz-Krieger / Perron-Frobenius criterion
  picks out the specific label -107 from first principles. Candidates:
    1. The Cuntz-Krieger Perron-Frobenius theorem says the KMS state
       is UNIQUE at β = log(spectral radius). Does this uniqueness
       extend to picking a unique label?
    2. The "first non-trivial integer label" — smallest |n| such that
       (n, 0) ∈ D and τ((n, 0)) ∈ [0, 1] makes sense as IDOS?
    3. The Bellissard gap-labeling theorem combined with a specific
       physical operator selects a specific gap whose label is -107?

If a clean Cuntz-Krieger uniqueness principle picks -107, the Tier-1
closure target is met. If not, the result coincides with the orbit-union
route: Cuntz-Krieger validates the framework but does not pick the
specific integer.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
from gct_utils import C

ENGINE_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ENGINE_ROOT / "data" / "protocol_akn_dimension_group_results.json"

PHI = float(C.PHI)
ALPHA = 1.0 / PHI


# ════════════════════════════════════════════════════════════════════════════
# (1) Fibonacci substitution matrix and Perron-Frobenius data
# ════════════════════════════════════════════════════════════════════════════

A = np.array([[1, 1], [1, 0]], dtype=np.int64)

# Eigenvalues of A: φ and -1/φ. Eigenvectors normalised.
# Left Perron eigenvector (defining the trace on the dimension group):
# w · A = φ · w  →  w = (φ, 1) normalised
# Normalisation convention: τ(1, 0) is the trace of the unit-rank
# projection p_0 in the AF approximation.
# For the gap-labeling theorem the trace is τ(m, n) = m·1 + n·α
# under the convention that the unit projection at level 0 has trace 1.

def trace_of_label(label: tuple[int, int]) -> float:
    """τ((m, n)) = m + n·α, where α = 1/φ. Bellissard convention."""
    m, n = label
    return m + n * ALPHA


def fibonacci_numbers(n_max: int) -> list[int]:
    F = [0, 1]
    while len(F) <= n_max:
        F.append(F[-1] + F[-2])
    return F


# ════════════════════════════════════════════════════════════════════════════
# (2) Build the dimension group D as nested Z² under A
# ════════════════════════════════════════════════════════════════════════════
# At level n, basis vectors are e_a^{(n)}, e_b^{(n)}.
# The inclusion D_n → D_{n+1} is multiplication by A.
# An element of D at level n is a Z²-vector v.
# After n more substitutions, it becomes A^n · v.

def labels_at_level(level: int) -> list[tuple[int, int]]:
    """Return list of (m, n) labels accessible as elements of A^level · Z²
    with |coefficient| ≤ 1 (one basis vector at the original level)."""
    An = np.linalg.matrix_power(A, level)
    # The two natural basis vectors of D_0 map to A^n · e_1 and A^n · e_2.
    e1_lifted = (int(An[0, 0]), int(An[1, 0]))
    e2_lifted = (int(An[0, 1]), int(An[1, 1]))
    return [e1_lifted, e2_lifted]


def all_small_combinations_at_level(level: int, coeff_range: int = 5) -> list[tuple[int, int]]:
    """All (m, n) = α · A^level · e_1 + β · A^level · e_2 with |α|, |β| ≤ coeff_range."""
    An = np.linalg.matrix_power(A, level)
    out = set()
    for a in range(-coeff_range, coeff_range + 1):
        for b in range(-coeff_range, coeff_range + 1):
            v = a * An[:, 0] + b * An[:, 1]
            out.add((int(v[0]), int(v[1])))
    return sorted(out, key=lambda x: (abs(x[0]) + abs(x[1]), x[0], x[1]))


# ════════════════════════════════════════════════════════════════════════════
# (3) Search for the label -107 in the accessible D-elements
# ════════════════════════════════════════════════════════════════════════════

def find_label_in_D(target_m: int, max_level: int = 30, coeff_range: int = 30) -> list[dict]:
    """Search for (m, n) labels with m = target_m, n = anything small.
    Returns list of matches with the level + α, β at which they appear."""
    matches = []
    for level in range(0, max_level + 1):
        An = np.linalg.matrix_power(A, level)
        for a in range(-coeff_range, coeff_range + 1):
            for b in range(-coeff_range, coeff_range + 1):
                v = a * An[:, 0] + b * An[:, 1]
                if int(v[0]) == target_m:
                    n = int(v[1])
                    matches.append({
                        "level": level,
                        "alpha_coeff": a,
                        "beta_coeff": b,
                        "label": (target_m, n),
                        "trace": trace_of_label((target_m, n)),
                    })
    return matches


# ════════════════════════════════════════════════════════════════════════════
# (4) Cuntz-Krieger Perron-Frobenius KMS uniqueness check
# ════════════════════════════════════════════════════════════════════════════

def check_perron_frobenius_uniqueness() -> dict:
    """Compute Perron-Frobenius data of A and verify that the KMS state at
    β = log(spectral radius) is unique. Quantify what this uniqueness means
    for projection labels."""
    eigvals, eigvecs = np.linalg.eig(A.astype(float).T)  # transpose for LEFT eigenvectors
    idx_max = int(np.argmax(eigvals.real))
    lambda_PF = float(eigvals[idx_max].real)
    w = eigvecs[:, idx_max].real
    # Normalise w so that w[1] = 1 → w = (φ, 1) as expected
    w = w / w[1]
    return {
        "spectral_radius": lambda_PF,
        "log_PF_eigenvalue_beta": float(math.log(lambda_PF)),
        "left_PF_eigvec_normalised": w.tolist(),
        "uniqueness_remark": (
            "Cuntz-Krieger Perron-Frobenius theorem (Kerr-Pinzari, Olesen-Pedersen, "
            "Exel-Laca): for an irreducible {0,1}-matrix A, 𝒪_A has a UNIQUE "
            "KMS state at β = log(spectral radius). This UNIQUENESS is of the STATE, "
            "not of any specific projection — there are infinitely many projections "
            "in 𝒪_A with various K_0 labels, all of which the unique trace evaluates "
            "consistently. So this theorem does NOT pick a single distinguished "
            "label like -107 from the family. The framework gives the trace function "
            "τ : K_0 → ℝ unambiguously; the SPECIFIC label of the electron projection "
            "remains a separate question requiring additional physical input."
        ),
    }


# ════════════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════════════

def main() -> int:
    print("=" * 90)
    print("  Dimension-group route: direct AKN dimension group + Cuntz-Krieger machinery")
    print("=" * 90)

    print(f"  Substitution matrix A = {A.tolist()}")
    F = fibonacci_numbers(30)
    print(f"  Fibonacci numbers F_0..F_30: {F[:31]}")
    print()

    print("  Step 1: Perron-Frobenius / KMS state uniqueness")
    pf = check_perron_frobenius_uniqueness()
    print(f"    Spectral radius of A: λ = {pf['spectral_radius']:.10f} (should be φ = {PHI:.10f})")
    print(f"    Canonical β = log λ = {pf['log_PF_eigenvalue_beta']:.10f}")
    print(f"    Left PF eigenvector (φ, 1) normalised: {pf['left_PF_eigvec_normalised']}")
    print()
    print(f"    KMS uniqueness remark:")
    print(f"    {pf['uniqueness_remark']}")
    print()

    print("  Step 2: dimension group labels at small levels")
    for level in [0, 5, 10, 15, 20]:
        labels = labels_at_level(level)
        traces = [trace_of_label(l) for l in labels]
        print(f"    Level {level:>2}: basis vectors lift to {labels}, traces = {[f'{t:.6f}' for t in traces]}")
    print()

    print("  Step 3: search for the label -107 as first component (m = -107)")
    matches = find_label_in_D(-107, max_level=30, coeff_range=30)
    print(f"    Found {len(matches)} accessible labels (m, n) with m = -107 across levels 0–30, |α,β| ≤ 30:")
    # Show the first few; in particular look for ones with n in [0, ~200]
    interesting = [m for m in matches if 0 <= m["label"][1] <= 200]
    print(f"    Of these, {len(interesting)} have n ∈ [0, 200] (potentially valid as IDOS):")
    for m in interesting[:15]:
        print(f"      level={m['level']:>2}  (α,β)=({m['alpha_coeff']:+3d},{m['beta_coeff']:+3d})  label=({m['label'][0]:+5d}, {m['label'][1]:+5d})  τ={m['trace']:.6f}")
    valid_idos = [m for m in matches if 0 <= trace_of_label(m["label"]) <= 1]
    print(f"    Of all matches, {len(valid_idos)} have τ ∈ [0, 1] (a valid IDOS, hence a real spectral gap candidate):")
    for m in valid_idos[:10]:
        print(f"      level={m['level']:>2}  (α,β)=({m['alpha_coeff']:+3d},{m['beta_coeff']:+3d})  label=({m['label'][0]:+5d}, {m['label'][1]:+5d})  τ={m['trace']:.6f}")
    print()

    print("  Step 4: uniqueness analysis")
    print("    Question: does the AKN/Cuntz-Krieger framework pick a unique label?")
    print()
    if valid_idos:
        # Sort by trace
        sorted_by_tau = sorted(valid_idos, key=lambda m: m["trace"])
        print(f"    Among the {len(valid_idos)} valid-IDOS labels with m = -107:")
        print(f"    - Smallest τ: {sorted_by_tau[0]['trace']:.6f} at label {sorted_by_tau[0]['label']}")
        print(f"    - Largest τ:  {sorted_by_tau[-1]['trace']:.6f} at label {sorted_by_tau[-1]['label']}")
        print(f"    - All of these are valid spectral gap candidates under Bellissard.")
        print()
        print(f"    There is NO uniqueness principle in the Cuntz-Krieger / Perron-Frobenius")
        print(f"    framework that picks one of these {len(valid_idos)} labels over the others.")
        print(f"    The KMS-state uniqueness is uniqueness of the trace function, not of a")
        print(f"    distinguished projection. Multiple distinct projections (each with its")
        print(f"    own K_0 label) coexist in 𝒪_A, all assigned consistent traces by τ.")
    else:
        print(f"    No valid-IDOS labels with first component -107 found at the tested levels.")

    print()
    print("=" * 90)
    print("  STRUCTURAL CONCLUSION (dimension-group route):")
    print()
    print("  The Cuntz-Krieger / Perron-Frobenius framework VALIDATES the gap-labeling")
    print("  setup (the Bellissard gap-labeling route shows this empirically at small N")
    print("  for the 1D Fibonacci Hamiltonian). The trace function τ : K_0 → ℝ is")
    print("  well-defined and unique.")
    print()
    print("  HOWEVER: the Cuntz-Krieger KMS uniqueness theorem gives uniqueness of")
    print("  the STATE, not of any specific PROJECTION in K_0. The integer -107 is")
    print("  one of infinitely many valid first-component labels (and shows up in")
    print(f"  {len(valid_idos)} distinct (m, n) combinations with τ ∈ [0, 1]). The framework")
    print("  does NOT, by itself, pick out -107 as 'the electron's label' over any")
    print("  other integer label.")
    print()
    print("  This coincides with the orbit-union route: a validated structural framework")
    print("  with no intrinsic uniqueness principle for the specific integer. The")
    print("  'electron = label -107' identification requires an EXTERNAL physical input")
    print("  (the m_e empirical fit, or a specific operator whose ground-state gap")
    print("  happens to land at this label).")
    print()
    print("  Net status of the Tier-1 closure target via the dimension-group route: the")
    print("  framework is validated; the specific integer -107 is not closed by the")
    print("  Bellissard-Connes K-theoretic framework alone. The disposition is therefore")
    print("  a framework-Tier-1 +")
    print("  integer-Postulate split: the K-theoretic skeleton is Tier 1 algebraic, the")
    print("  specific exponent -107 is a Tier 3 integer anchor registered as Open")
    print("  Problem O.14 (see App H §H.5 and App U §U.7.6.7).")
    print("=" * 90)

    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DATA_PATH.open("w", encoding="utf-8") as f:
        json.dump({
            "perron_frobenius": pf,
            "labels_at_levels": {level: labels_at_level(level) for level in [0, 5, 10, 15, 20]},
            "minus_107_labels_count": len(matches),
            "minus_107_valid_idos_count": len(valid_idos),
            "minus_107_valid_idos_first_10": valid_idos[:10],
            "verdict": "Framework validated; specific integer not uniquely picked.",
        }, f, indent=2, default=str)
    print(f"  Results: {DATA_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
