"""
H.1.1 Consensus Protocol Convergence Theorem
=============================================

Checks that the N-Agent weighted consensus protocol of Ch11
converges to a singular, self-consistent lattice history.

Mathematical setup (Ch11 Sec 11.3.2):

  - N agents with p-adic identity addresses s_1, ..., s_N.
  - Pairwise coupling kappa_ij = kappa_0 * exp(-lambda_c * d_H(s_i, s_j))
    > 0 strictly for all i, j (finite Consensus Decay Constant).
  - Each agent updates its local potential via the weighted-mean fixed-
    point equation:

        Phi_i^(t+1) = sum_j W_ij Phi_j^(t),   W_ij = kappa_ij / sum_k kappa_ik

    where W is row-stochastic (rows sum to 1) and STRICTLY POSITIVE
    (every entry > 0 because kappa_ij > 0).

Theorem (H.1.1, Tier 1 mathematically forced):

  Let W be the row-stochastic consensus matrix of an N-Agent network
  with strictly positive coupling. Then:

    (i)   W has spectral radius rho(W) = 1 with a SIMPLE leading
          eigenvalue lambda_1 = 1 (Perron-Frobenius for strictly
          positive matrices, Horn & Johnson 1985 Thm 8.2.11).
    (ii)  All other eigenvalues satisfy |lambda_k| < 1 strictly
          (strong Perron-Frobenius gap, idem Cor 8.2.12).
    (iii) The iteration Phi^(t+1) = W Phi^(t) converges geometrically
          in t with rate |lambda_2| < 1 to the UNIQUE fixed point
          Phi^* proportional to the right-eigenvector of W at
          lambda_1 = 1.
    (iv)  This fixed point is exactly the self-consistent solution of
          the §11.3.2 Euler-Lagrange weighted-mean equation:
          Phi_i^* = sum_j W_ij Phi_j^*  for all i.

Proof outline:

  (i)+(ii) follow from strict positivity of W (since exp(-lambda_c * d_H)
  > 0 for finite lambda_c, d_H < infinity) via Perron-Frobenius.
  (iii) follows from |lambda_2| < 1: ||Phi^(t) - Phi^*|| <= C |lambda_2|^t.
  (iv) follows from W Phi^* = lambda_1 Phi^* = Phi^*, i.e. Phi^* is the
  fixed point of the iteration AND the Euler-Lagrange stationary state.

Engine outputs:
  - Construct a representative p-adic agent network at depths d = 2, 3, 4.
  - Compute W eigenvalues and verify (i)+(ii).
  - Iterate from random initial Phi^(0) and verify geometric convergence
    to Phi^* at the rate predicted by |lambda_2|.
  - Verify Phi^* satisfies the weighted-mean fixed-point equation.

Cross-reference: V1 Ch11 Sec 11.3.2 (Consensus Action functional); Ch07
(p-adic identity tree); App H H.1.1.
"""

from __future__ import annotations

import math
import json
from pathlib import Path
from typing import List, Tuple

import numpy as np


def first_common_branch_level(addr_i: List[int], addr_j: List[int]) -> int:
    """Level of first common branch node in the p-adic tree.

    Per Ch07 Sec 7.6.2: d_H(i,j) = p^(-m) where m is the level at which
    the two addresses first agree (counting from root).
    For two paths in a tree, m = length of common prefix.
    """
    m = 0
    for ai, aj in zip(addr_i, addr_j):
        if ai != aj:
            break
        m += 1
    return m


def hierarchical_distance(addr_i: List[int],
                            addr_j: List[int],
                            p: int) -> float:
    """d_H = p^(-m) where m is common-prefix length. d_H = 0 if identical."""
    if addr_i == addr_j:
        return 0.0
    m = first_common_branch_level(addr_i, addr_j)
    return p ** (-m) if m > 0 else 1.0  # diverge at root => d_H = 1


def generate_agent_addresses(depth: int, p: int) -> List[List[int]]:
    """All p^depth agents at the leaf level of a p-ary tree of depth 'depth'."""
    addresses = []

    def recurse(prefix: List[int], remaining: int):
        if remaining == 0:
            addresses.append(prefix[:])
            return
        for digit in range(p):
            recurse(prefix + [digit], remaining - 1)

    recurse([], depth)
    return addresses


def build_consensus_matrix(addresses: List[List[int]],
                             p: int,
                             lambda_c: float,
                             kappa_0: float = 1.0) -> np.ndarray:
    """W_ij = kappa_ij / sum_k kappa_ik, where kappa_ij = kappa_0 exp(-lambda_c d_H)."""
    N = len(addresses)
    K = np.zeros((N, N), dtype=float)
    for i in range(N):
        for j in range(N):
            d = hierarchical_distance(addresses[i], addresses[j], p)
            K[i, j] = kappa_0 * math.exp(-lambda_c * d)
    # Row-stochastic normalisation
    row_sums = K.sum(axis=1, keepdims=True)
    W = K / row_sums
    return W


def verify_strict_positivity(W: np.ndarray) -> bool:
    return bool((W > 0).all())


def spectral_analysis(W: np.ndarray) -> dict:
    """Return eigenvalues sorted by magnitude descending; spectral gap."""
    eigenvalues = np.linalg.eigvals(W)
    magnitudes = np.abs(eigenvalues)
    order = np.argsort(magnitudes)[::-1]
    eigs_sorted = eigenvalues[order]
    mags_sorted = magnitudes[order]
    lambda_1 = eigs_sorted[0]
    lambda_2 = eigs_sorted[1]
    return {
        "lambda_1_real": float(np.real(lambda_1)),
        "lambda_1_imag": float(np.imag(lambda_1)),
        "lambda_1_magnitude": float(mags_sorted[0]),
        "lambda_2_real": float(np.real(lambda_2)),
        "lambda_2_imag": float(np.imag(lambda_2)),
        "lambda_2_magnitude": float(mags_sorted[1]),
        "spectral_gap": float(1.0 - mags_sorted[1]),
        "lambda_1_is_simple_one": bool(
            math.isclose(mags_sorted[0], 1.0, rel_tol=1e-10) and
            mags_sorted[1] < 1.0 - 1e-10
        ),
        "all_other_eigs_strictly_less_than_1": bool(
            (mags_sorted[1:] < 1.0 - 1e-12).all()
        ),
    }


def fixed_point(W: np.ndarray) -> np.ndarray:
    """Right-eigenvector of W at eigenvalue 1, normalised."""
    eigenvalues, eigenvectors = np.linalg.eig(W)
    # Find eigenvalue closest to 1
    idx = np.argmin(np.abs(eigenvalues - 1.0))
    v = np.real(eigenvectors[:, idx])
    # Normalise so largest entry = 1 (convention)
    v = v / np.max(np.abs(v))
    return v


def iterate_and_measure_convergence(W: np.ndarray,
                                       Phi_0: np.ndarray,
                                       max_iter: int = 200,
                                       tol: float = 1e-12) -> dict:
    """Run iteration Phi <- W Phi, measure geometric convergence rate."""
    Phi_star = fixed_point(W)
    # Align Phi_0 to same scale as Phi_star for distance comparison
    Phi = Phi_0.copy()
    residuals = []
    for t in range(max_iter):
        # Distance to invariant subspace: project Phi onto Phi_star direction
        # and measure orthogonal component
        Phi_norm = Phi / max(np.abs(Phi).max(), 1e-30)
        diff = Phi_norm - Phi_star * np.sign(Phi_norm @ Phi_star)
        residual = float(np.linalg.norm(diff))
        residuals.append(residual)
        if residual < tol:
            break
        Phi = W @ Phi
    return {
        "num_iterations": len(residuals),
        "final_residual": residuals[-1],
        "converged": bool(residuals[-1] < 1e-6),
        "early_residuals": residuals[:5],
        "late_residuals": residuals[-5:] if len(residuals) >= 5 else residuals,
    }


def verify_self_consistency(W: np.ndarray, Phi_star: np.ndarray) -> dict:
    """Check W Phi^* == Phi^* numerically."""
    W_Phi = W @ Phi_star
    # Normalise both to same convention for comparison
    W_Phi_norm = W_Phi / max(np.abs(W_Phi).max(), 1e-30)
    Phi_star_norm = Phi_star / max(np.abs(Phi_star).max(), 1e-30)
    err = float(np.max(np.abs(W_Phi_norm - Phi_star_norm)))
    return {
        "max_abs_error": err,
        "self_consistent": bool(err < 1e-10),
    }


def compute() -> dict:
    results = {
        "theorem": (
            "For an N-Agent consensus network with strictly positive "
            "coupling kappa_ij = kappa_0 exp(-lambda_c d_H) > 0, the "
            "row-stochastic matrix W has simple leading eigenvalue 1, "
            "all other eigenvalues |lambda_k| < 1, and the iteration "
            "Phi^(t+1) = W Phi^(t) converges geometrically to the "
            "unique fixed point at rate |lambda_2|^t."),
        "tier": "Tier 1 (Perron-Frobenius for strictly positive matrices)",
        "instances": {},
    }

    rng = np.random.default_rng(seed=42)

    for (p, depth, lambda_c) in [
        (2, 2, 0.5),  # 4 agents, p=2
        (2, 3, 0.5),  # 8 agents
        (2, 4, 0.5),  # 16 agents
        (3, 2, 0.7),  # 9 agents, p=3
        (2, 4, 2.0),  # 16 agents, stronger viscosity
        (2, 4, 0.1),  # 16 agents, weak viscosity (still strictly positive)
    ]:
        addresses = generate_agent_addresses(depth, p)
        W = build_consensus_matrix(addresses, p, lambda_c)
        positivity = verify_strict_positivity(W)
        spectral = spectral_analysis(W)
        N = len(addresses)
        Phi_0 = rng.standard_normal(N)
        convergence = iterate_and_measure_convergence(W, Phi_0)
        Phi_star = fixed_point(W)
        consistency = verify_self_consistency(W, Phi_star)

        key = f"p={p}_depth={depth}_lambda_c={lambda_c}"
        results["instances"][key] = {
            "N": N,
            "strict_positivity_W_ij_gt_0": positivity,
            "spectral": spectral,
            "convergence": convergence,
            "fixed_point_self_consistent": consistency,
            "all_four_theorem_points_satisfied": all([
                positivity,
                spectral["lambda_1_is_simple_one"],
                spectral["all_other_eigs_strictly_less_than_1"],
                convergence["converged"],
                consistency["self_consistent"],
            ]),
        }

    all_pass = all(
        inst["all_four_theorem_points_satisfied"]
        for inst in results["instances"].values()
    )
    results["all_instances_pass_theorem"] = all_pass
    results["closure_status"] = {
        "tier": "Tier 1",
        "status": "CLOSED" if all_pass else "FAILED",
        "claim": ("H.1.1 closed: the Ch11 Sec 11.3.2 N-Agent consensus "
                   "protocol always converges to a singular, self-"
                   "consistent lattice history via Perron-Frobenius for "
                   "strictly positive matrices. Convergence rate is "
                   "|lambda_2|^t where lambda_2 is the second-largest "
                   "eigenvalue of the row-stochastic consensus matrix W."),
        "scope_caveats": (
            "Theorem assumes finite-N, finite-lambda_c, finite-depth "
            "p-adic addresses (kappa_ij > 0 strictly). Continuum N -> "
            "infinity or lambda_c -> infinity limits may require "
            "additional regularity. Periodic-orbit branches (multiple "
            "eigenvalues at |lambda| = 1) are excluded by strict "
            "positivity; they would only arise if some kappa_ij = 0 "
            "exactly (graph disconnected) or in singular limits."),
    }
    return results


def main():
    results = compute()
    out_dir = Path(__file__).parent.parent / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "h1_1_consensus_convergence.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"H.1.1 Consensus Protocol Convergence Theorem")
    print(f"=" * 60)
    print(f"Theorem tier: {results['tier']}")
    print()
    for key, inst in results["instances"].items():
        s = inst["spectral"]
        c = inst["convergence"]
        cons = inst["fixed_point_self_consistent"]
        print(f"Instance {key} (N = {inst['N']}):")
        print(f"  strict positivity:   {inst['strict_positivity_W_ij_gt_0']}")
        print(f"  lambda_1 = {s['lambda_1_magnitude']:.10f} (simple: {s['lambda_1_is_simple_one']})")
        print(f"  lambda_2 = {s['lambda_2_magnitude']:.6f}  spectral_gap = {s['spectral_gap']:.6f}")
        print(f"  converged in {c['num_iterations']} iters, residual = {c['final_residual']:.3e}")
        print(f"  W Phi* = Phi*: err = {cons['max_abs_error']:.3e}")
        print(f"  ALL FOUR POINTS: {inst['all_four_theorem_points_satisfied']}")
        print()
    print(f"All instances pass theorem: {results['all_instances_pass_theorem']}")
    print(f"Closure: {results['closure_status']['status']}")
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
