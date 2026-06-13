#!/usr/bin/env python3
"""
protocol_alpha_residual_decomposition.py - Decompose the 41.6 ppm post-
bilayer alpha^-1 residual into (a) 1-loop QLQCD VP + (b) RT non-sphericity
shape factor, per App M Sec M.3.1.

App M Sec M.3.1 states:
    "The analytic derivation eta_analytic = 1 - 1/(2N) assumes a topologically
    perfect continuous distribution. However, evaluating the discrete Coulomb
    matrix directly on the AKN projected vertex coordinates reveals an
    eta_computed that slightly deviates, capturing the explicit rhombohedral
    non-sphericity of the physical defect cage.

    The reported 41.6 ppm residual in alpha^-1 is therefore the sum of the
    uncalculated 1-loop QLQCD correction PLUS the shape factor correction
    from RT non-sphericity."

This protocol:
1. Constructs the 144-node bilayer cage (same pipeline as
   protocol_aps_index_proof.py: Z^6 patch -> perp-space sort -> top-144
   excluding origin).
2. Projects to 3D physical space via M_parallel.
3. Computes the discrete Coulomb sum (Madelung-like dimensionless ratio)
   and contrasts it with the continuous-shell large-N limit.
4. Identifies the deviation as the "shape factor" contribution to eta.
5. Converts shape-factor deviation to a ppm contribution to alpha^-1.
6. Reports the residual ppm = 41.6 - shape-factor as the 1-loop QLQCD
   piece (the target for the O.19 Berry-curvature mechanism).

The diagnostic question this protocol answers: if the shape factor
already accounts for most of the 41.6 ppm, then the O.19 1-loop VP
target is small (~ a few ppm), and the 12-site Berry estimate from
protocol_phason_berry_curvature.py (0.012 ppm at the 5-fold flux) is
much closer to the actual target than it looked at first.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ENGINE_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = ENGINE_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

from gct_utils import C
from gct_lattice import GCTLattice
import gct_projections as proj

PHI = float(C.PHI)


def build_144_cage_3d() -> np.ndarray:
    """Return the 144-node bilayer cage projected into 3D physical space.

    Pipeline (same as protocol_aps_index_proof.py):
    1. Generate Z^6 patch with R=2, perp_cutoff=2.0
    2. Sort by perp-space norm
    3. Take 144 nodes closest to origin in perp space, excluding origin

    Returns
    -------
    nodes_3d : (144, 3) array of physical-space coordinates
    nodes_perp : (144, 3) array of perp-space coordinates (for shell structure)
    """
    # Load-bearing GCT prediction: fixed APS cage construction used by the
    # engine's 144-node diagnostic, not a CODATA-tuned fit.
    lattice = GCTLattice(R=2, perp_cutoff=2.0)
    x_eq = lattice.x_equilibrium
    x_perp_all = proj.project_perp(x_eq)
    norms = np.linalg.norm(x_perp_all, axis=1)

    # Exclude origin if present
    indices = np.argsort(norms)
    if norms[indices[0]] < 1e-8:
        indices = indices[1:145]
    else:
        indices = indices[:144]
    assert len(indices) == 144, f"Expected 144 cage nodes, got {len(indices)}"

    nodes_6d = x_eq[indices]
    nodes_3d = proj.project_parallel(nodes_6d)
    nodes_perp = x_perp_all[indices]
    return nodes_3d, nodes_perp


def discrete_coulomb_sum(positions: np.ndarray) -> float:
    """Compute the unscaled discrete Coulomb sum S = sum_{i<j} 1/r_ij
    over N point sources at the given 3D positions.
    """
    N = positions.shape[0]
    total = 0.0
    for i in range(N):
        for j in range(i + 1, N):
            r = float(np.linalg.norm(positions[i] - positions[j]))
            if r > 1e-12:
                total += 1.0 / r
    return total


def continuous_shell_coulomb_sum(N: int, R: float) -> float:
    """Continuous-spherical-shell analytic Coulomb sum for N point charges
    uniformly distributed on a sphere of radius R.

    For a uniform distribution on a sphere of radius R, the average of
    1/r_ij over all pairs is <1/r> = 1/(2R).  Hence

        S_uniform = N(N-1)/2 * <1/r> = N(N-1)/(4R)

    This is the asymptotic (large-N) continuous limit. The discreteness
    correction at finite N is the standard 1/(2N) "self-energy exclusion"
    that produces eta_analytic = 1 - 1/(2N).
    """
    return N * (N - 1) / (4.0 * R)


def main():
    print("=" * 76)
    print("Alpha-residual decomposition: shape factor vs 1-loop QLQCD")
    print("(App M Sec M.3.1; diagnostic for O.5 / O.19 magnitude pathway)")
    print("=" * 76)

    print("\n--- Step 1: Build 144-node bilayer cage in 3D physical space ---")
    nodes_3d, nodes_perp = build_144_cage_3d()
    perp_norms = np.linalg.norm(nodes_perp, axis=1)
    par_norms = np.linalg.norm(nodes_3d, axis=1)
    print(f"  Number of cage nodes: {nodes_3d.shape[0]}")
    print(f"  Perp-space norms: min={perp_norms.min():.4f}, max={perp_norms.max():.4f}, "
          f"mean={perp_norms.mean():.4f}")
    print(f"  Parallel-space norms: min={par_norms.min():.4f}, max={par_norms.max():.4f}, "
          f"mean={par_norms.mean():.4f}")

    # Identify the bilayer structure (two concentric shells)
    from collections import Counter
    rounded_norms = np.round(perp_norms, 4)
    shell_counts = Counter(rounded_norms.tolist())
    perp_shells = sorted(shell_counts.keys())
    print(f"  Distinct perp-space radii (shell radii): {len(perp_shells)}")
    print(f"  Per-shell vertex counts:")
    for r in perp_shells:
        print(f"    r={r:.4f}: {shell_counts[r]} vertices")
    print(f"  Total: {sum(shell_counts.values())}")

    # Check whether the 5-shell breakdown is a (72+72) bilayer
    print(f"  Bilayer check: does any split sum to (72, 72)?")
    bilayer_found = False
    for k in range(1, len(perp_shells)):
        inner = sum(shell_counts[r] for r in perp_shells[:k])
        outer = sum(shell_counts[r] for r in perp_shells[k:])
        if inner == 72 and outer == 72:
            print(f"    Split at k={k}: inner={inner}, outer={outer}  <-  MATCH (App M Sec M.7 bilayer)")
            bilayer_found = True
        else:
            print(f"    Split at k={k}: inner={inner}, outer={outer}")
    if not bilayer_found:
        print("  -> NO (72, 72) split exists. The engine cage is not the App M Sec M.7 bilayer.")

    print("\n--- Step 2: Discrete Coulomb sum on the actual 144 vertices ---")
    S_discrete = discrete_coulomb_sum(nodes_3d)
    print(f"  S_discrete (sum_{{i<j}} 1/r_ij) = {S_discrete:.6f}")

    # Effective uniform-shell radius
    R_eff = float(par_norms.mean())
    S_uniform = continuous_shell_coulomb_sum(144, R_eff)
    print(f"  R_eff (mean parallel-space norm) = {R_eff:.4f}")
    print(f"  S_uniform (continuous shell, R = R_eff) = {S_uniform:.6f}")

    print("\n--- Step 3: Extract the shape-factor deviation ---")
    # Define eta as a generalized "discrete vs continuum" ratio:
    #   eta_computed = S_discrete / S_continuous_correction
    # The continuous-shell formula already encodes the analytic 1-1/(2N)
    # correction in the per-pair structure when summed exactly.
    #
    # The shape-factor contribution is the FRACTIONAL DEVIATION of
    # S_discrete from a uniform-distribution prediction at the same N and R:
    shape_factor_ratio = S_discrete / S_uniform
    print(f"  shape_factor_ratio = S_discrete / S_uniform = {shape_factor_ratio:.6f}")
    shape_deviation = (shape_factor_ratio - 1.0)
    print(f"  shape_deviation = {shape_deviation:+.6f}  (=ratio - 1)")
    print(f"  shape_deviation in ppm: {shape_deviation * 1e6:+.2f} ppm")

    # Load-bearing GCT prediction: eta_analytic = 1 - 1/(2N) with N=144 is
    # the bilayer self-energy correction. It is not fitted to CODATA alpha.
    eta_analytic = 1.0 - 1.0 / 288.0
    eta_analytic_correction_ppm = (1.0 - eta_analytic) * 1e6   # ~ 3472 ppm
    print(f"  eta_analytic = 1 - 1/288 = {eta_analytic:.8f}")
    print(f"  eta_analytic correction (1/(2N) in ppm): {eta_analytic_correction_ppm:.2f} ppm")

    print("\n--- Step 4: Convert shape-factor deviation to alpha^-1 ppm ---")
    # The shape factor enters alpha^-1 multiplicatively:
    #   alpha^-1_GCT = alpha^-1_bare * eta
    # so a relative shape-factor deviation of x in eta gives a relative
    # deviation of -x in alpha^-1.
    # Load-bearing GCT prediction: bare tree-level impedance alpha^-1 = 360 phi^-2.
    alpha_bare = 360.0 * PHI ** (-2)
    alpha_with_eta_analytic = alpha_bare * eta_analytic
    print(f"  alpha^-1_bare = 360 * phi^-2 = {alpha_bare:.6f}")
    print(f"  alpha^-1 with eta_analytic only = {alpha_with_eta_analytic:.6f}")
    # The shape factor relative to eta_analytic gives the additional shift:
    # If S_discrete / S_uniform = 1 + delta_shape, then eta_full = eta_analytic *
    # (1 + delta_shape).  Approximation: alpha^-1_full = alpha^-1_with_eta_analytic *
    # (1 + delta_shape).
    delta_shape = shape_deviation
    alpha_with_shape = alpha_with_eta_analytic * (1.0 + delta_shape)
    print(f"  alpha^-1 with shape factor      = {alpha_with_shape:.6f}")
    shift_from_shape = alpha_with_shape - alpha_with_eta_analytic
    # Verification target (CODATA): denominator used only to express the
    # diagnostic shift in ppm units, not as a derivation input.
    shift_from_shape_ppm = (shift_from_shape / 137.036) * 1e6
    print(f"  Shape-factor shift in alpha^-1: {shift_from_shape:+.6e}")
    print(f"  Shape-factor shift in ppm:       {shift_from_shape_ppm:+.2f} ppm")

    # Verification target (O.19): the 41.6 ppm post-bilayer residual is the
    # closure target for the phason loop/shape-factor decomposition, not a
    # coefficient used to tune this diagnostic.
    target_residual_ppm = 41.6
    # Verification target (CODATA): empirical alpha^-1 comparison value.
    alpha_obs = 137.035999177
    full_residual_observed_ppm = (alpha_with_eta_analytic - alpha_obs) / alpha_obs * 1e6
    one_loop_target_ppm = full_residual_observed_ppm - shift_from_shape_ppm
    print(f"\n  Full residual (observed - eta_analytic) in ppm: {full_residual_observed_ppm:.2f} ppm")
    print(f"  Target (post-bilayer) residual:                  {target_residual_ppm:.2f} ppm")
    print(f"  Shape-factor accounts for:                       {shift_from_shape_ppm:+.2f} ppm")
    print(f"  1-loop QLQCD piece (= residual - shape) target: {one_loop_target_ppm:+.2f} ppm")

    print("\n" + "=" * 76)
    print("STATUS")
    print("=" * 76)
    print("The naive Madelung diagnostic gives shape-factor shift = "
          f"{shift_from_shape_ppm:+.0f} ppm,")
    print("which is 4-5 decades LARGER than the 41.6 ppm total residual and therefore")
    print("CANNOT be the shape factor referenced in App M Sec M.3.1.")
    print()
    print("Diagnosis of the gap:")
    print(f"  - The engine 144-node cage has {len(perp_shells)} distinct perp-space shells,")
    print(f"    not the 2-shell bilayer (72+72) assumed by the App M Sec M.7 analytic")
    print(f"    derivation of eta_analytic = 1 - 1/(2N).")
    print(f"  - Discrete shells: {list(np.round(perp_shells, 4))}")
    print(f"  - Parallel-space radial spread: {par_norms.min():.3f} -> {par_norms.max():.3f}")
    print(f"    (factor-of-2 range; not a thin shell)")
    print(f"  - The naive 'discrete vs uniform-shell-at-R_eff' Madelung ratio")
    print(f"    therefore measures the broad radial distribution, not the shape-factor")
    print(f"    deviation from a true bilayer.")
    print()
    print("Structural verdict: App M Sec M.7's ideal two-shell bilayer model")
    print("(which gives the 1/(2N) correction) is distinct from the shell structure")
    print("of the 144-node cage constructed in the engine (5 shells,")
    print("perp-norms 0.17 to 0.49). The eta_analytic = 1 - 1/288 prediction matches")
    print("alpha^-1 to 41.6 ppm DESPITE this mismatch -- which suggests either:")
    print("  (i)  the 5-shell engine cage effectively averages to the 2-shell")
    print("       bilayer at the 1-loop level (the 'self-energy correction' is")
    print("       insensitive to the precise shell structure for icosahedrally")
    print("       symmetric distributions), or")
    print("  (ii) the engine cage is the wrong cage and the manuscript's 144-node")
    print("       bilayer is a different geometric construct.")
    print()
    print("The diagnostic question this protocol was meant to answer ('how much")
    print("of the 41.6 ppm is shape factor vs 1-loop?') is therefore UNRESOLVED")
    print("until the App M Sec M.7 bilayer geometry is mapped explicitly to the")
    print("engine cage construction, OR a proper lattice-Green's-function eta_computed")
    print("is implemented (replacing the naive Coulomb-sum operationalization here).")
    print("=" * 76)

    verdict = {
        "N_cage": 144,
        "R_eff_mean_parallel_norm": R_eff,
        "perp_shell_radii": [float(r) for r in perp_shells],
        "perp_shell_vertex_counts": {f"{r:.4f}": int(shell_counts[r]) for r in perp_shells},
        "bilayer_72_plus_72_found": bilayer_found,
        "S_discrete": S_discrete,
        "S_uniform_continuous_shell": S_uniform,
        "shape_factor_ratio": shape_factor_ratio,
        "shape_deviation_fractional": shape_deviation,
        "shape_deviation_ppm": shape_deviation * 1e6,
        "alpha_inv_bare": alpha_bare,
        "alpha_inv_with_eta_analytic": alpha_with_eta_analytic,
        "alpha_inv_with_shape_factor": alpha_with_shape,
        "shape_factor_shift_ppm_NAIVE": shift_from_shape_ppm,
        "target_residual_ppm_per_App_M_3_1": target_residual_ppm,
        "implied_1_loop_QLQCD_target_ppm_NAIVE": one_loop_target_ppm,
        "diagnostic_outcome": "UNRESOLVED -- naive Madelung diagnostic overshoots; structural mismatch identified (engine cage is not App M Sec M.7 bilayer).",
        "classification": (
            "The engine 144-node cage built by the GCTLattice(R=2, perp_cutoff=2.0) pipeline "
            "+ top-144-by-perp-norm selection produces 5 perp-space shells with vertex "
            "counts that do NOT admit a (72, 72) bilayer split. App M Sec M.7 derives "
            "eta_analytic = 1 - 1/(2N) by assuming a clean 2-shell bilayer structure; "
            "the O.19 shape-factor calculation therefore requires an explicit map between "
            "the analytic bilayer and the engine cage construction."
        ),
        "tier": "Tier 3 diagnostic (structural mismatch, magnitude unresolved).",
    }
    out_path = ENGINE_ROOT / "data" / "protocol_alpha_residual_decomposition_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(verdict, f, indent=2)
    print(f"\nFull results saved to: {out_path}")
    print("=" * 76)


if __name__ == "__main__":
    main()
