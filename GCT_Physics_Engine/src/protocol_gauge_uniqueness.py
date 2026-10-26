#!/usr/bin/env python3
"""
protocol_gauge_uniqueness.py — SU(3) Candidate Numerical Control
=================================================================
This protocol tests whether the eight-dimensional su(3) candidate built from
the ten three-fold axes of the RT acceptance window is specific to that
geometry.  It is not a theorem-grade classification proof over all compact
Lie groups.

Controls:
- Cube face axes / octahedron (3 axes) -> abelian closure
- Rhombic Triacontahedron (10 three-fold axes) -> 8-dimensional closure
- Matched-axis control: ten random unit axes, same closure and a
  tolerance-based A2 Cartan comparison
- Monte Carlo over random convex polyhedra (first gate: exactly ten
  three-fold axes)

The quadrupole Gram matrix G_ij = (a_i . a_j)^2 has rank <= 6 for any ten
real axes (Frobenius Gram matrix in Sym^2(R^3)); the RT value is rank 6 with
a four-dimensional null space.  The eight-dimensional closure is a separate
calculation.  Generic matched ten-axis sets also close to dimension 8 with an
A2 Cartan matrix, so the registered controls do not establish RT specificity;
the color identification remains an open Tier 3 candidate (O.39).
"""

import numpy as np
import json
from gct_utils import get_output_path
from scipy.spatial import ConvexHull

# GCT Imports
from gct_geometry import RhombicTriacontahedron
from gct_gauge import GaugeGenerator
from protocol_su3_proof_complete import build_su3_basis, compute_structure_constants, compute_cartan_matrix, _build_rt_axes

# ============================================================================
# MONTE CARLO CONTROL
# ============================================================================

def _random_spherical_points(rng: np.random.Generator, n_points: int) -> np.ndarray:
    pts = rng.standard_normal((n_points, 3))
    return pts / np.linalg.norm(pts, axis=1, keepdims=True)


def run_monte_carlo_control(n_trials: int = 1000, n_points_per_polyhedron: int = 32) -> dict:
    """
    Monte Carlo Control: Random Convex Polyhedra vs. SU(3).

    For each trial, sample random spherical points, form the convex hull, and
    test whether the resulting random convex polyhedron produces:
      (a) the 10 three-fold axes required by the RT witness,
      (a) An 8-dimensional Lie algebra, AND
      (b) An exact A2 Cartan matrix [[2,-1],[-1,2]] without floating point noise.

    Success Criterion: ZERO trials must satisfy both criteria.
    """
    print("\n" + "="*60)
    print("MONTE CARLO CONTROL: Random Convex Polyhedra vs SU(3)")
    print(f"  n_trials = {n_trials}, n_points_per_polyhedron = {n_points_per_polyhedron}")
    print("  sampling = random spherical points -> ConvexHull -> 3-fold-axis extraction")
    print(f"  Cartan check: np.array_equal (exact integer match)")
    print("="*60)

    target_cm = np.array([[2, -1], [-1, 2]])

    n_10_axes   = 0  # hulls with the RT-compatible 10 three-fold axes
    n_dim8      = 0  # trials producing an 8-dimensional algebra
    n_success   = 0  # trials passing the full RT witness

    rng = np.random.default_rng(seed=0)

    for trial in range(n_trials):
        points = _random_spherical_points(rng, n_points_per_polyhedron)
        try:
            hull = ConvexHull(points)
            axes = GaugeGenerator.identify_3fold_axes(hull)
        except Exception:
            continue

        if len(axes) != 10:
            continue
        n_10_axes += 1

        try:
            dim, _ = GaugeGenerator.generate_algebra(axes)
        except Exception:
            continue

        if dim == 8:
            n_dim8 += 1
            # 3. Compute Cartan Matrix and 4. Count Successes
            try:
                basis = build_su3_basis(axes)
                f     = compute_structure_constants(basis)
                cm, _ = compute_cartan_matrix(basis, f)
                # Strict Cartan Equality Check: exact integer A2 match (not by itself a specificity test).
                # Random vectors produce floating-point noise and fail np.array_equal.
                if np.array_equal(cm, target_cm):
                    n_success += 1
            except Exception:
                pass

    evaluated = n_10_axes > 0
    mc_pass = bool(evaluated and n_success == 0)
    if not evaluated:
        verdict = "NOT_EVALUATED"
    else:
        verdict = "PASS" if mc_pass else "FAIL"

    print(f"  Trials with 10 3-fold axes : {n_10_axes} / {n_trials}")
    print(f"  Trials with dim-8 algebra  : {n_dim8} / {n_trials}")
    print(f"  Trials with full RT witness: {n_success} / {n_trials}")
    print(f"  Monte Carlo verdict        : [{verdict}]")

    return {
        "n_trials": n_trials,
        "n_alternatives_tested": n_10_axes,
        "n_polyhedra_sampled": n_trials,
        "sampling": "random spherical points -> ConvexHull -> 3-fold-axis extraction",
        "n_points_per_polyhedron": n_points_per_polyhedron,
        "n_trials_with_10_threefold_axes": n_10_axes,
        "n_trials_with_dim8_algebra": n_dim8,
        "n_trials_with_exact_A2_cartan": n_success,
        "n_trials_with_full_rt_witness": n_success,
        "n_alternatives_with_full_rt_witness": n_success,
        "monte_carlo_success_rate": 0.0 if n_success == 0 else float(n_success / n_trials),
        "success_criterion": "n_trials_with_10_threefold_axes > 0 and n_trials_with_full_rt_witness == 0",
        "edge_case_policy": "If no trial reaches the algebra test (no ten-axis hull), the control is NOT_EVALUATED with pass false, not PASS by vacuous truth",
        "pass": mc_pass,
        "verdict": verdict,
    }

A2_TARGET = np.array([[2, -1], [-1, 2]])
A2_ATOL = 1e-6


def _a2_within_tolerance(axes) -> bool:
    basis = build_su3_basis(axes)
    f = compute_structure_constants(basis)
    cm, _ = compute_cartan_matrix(basis, f)
    return bool(np.allclose(np.asarray(cm, dtype=float), A2_TARGET, atol=A2_ATOL))


def run_matched_axis_control(n_trials: int = 200, seed: int = 1) -> dict:
    """Ten random unit axes per trial: closure dimension and tolerance A2 check."""
    rng = np.random.default_rng(seed)
    n_dim8 = 0
    n_a2 = 0
    for _ in range(n_trials):
        axes = [v / np.linalg.norm(v) for v in rng.standard_normal((10, 3))]
        dim, _ = GaugeGenerator.generate_algebra(axes)
        if dim == 8:
            n_dim8 += 1
            try:
                if _a2_within_tolerance(axes):
                    n_a2 += 1
            except Exception:
                pass
    print(f"  Matched-axis control: {n_dim8}/{n_trials} dim-8 closures, "
          f"{n_a2}/{n_trials} A2 within atol={A2_ATOL}")
    return {
        "n_trials": n_trials,
        "seed": seed,
        "axes_per_trial": 10,
        "n_dim8_closure": n_dim8,
        "n_A2_within_tolerance": n_a2,
        "a2_tolerance_atol": A2_ATOL,
        "discriminates_rt": bool(n_a2 == 0),
    }


def run_uniqueness_proof():
    print("="*60)
    print("GCT Protocol: Gauge Candidate Numerical Control")
    print("="*60)
    
    results = {}
    
    # 1. The Cube (Control Group A)
    # Use face-normal axes (3 Cartesian directions) — these project to DIAGONAL
    # traceless matrices that commute with each other, spanning only the
    # Cartan sub-algebra (dim = 2).  This is the correct result for a simple
    # cubic embedding: the cube has NO off-diagonal generators from face normals.
    print("\n1. Testing The Cube face axes (Control Group A)...")
    cube_axes = [
        np.array([1.0, 0.0, 0.0]),
        np.array([0.0, 1.0, 0.0]),
        np.array([0.0, 0.0, 1.0]),
    ]
    print(f"  Using {len(cube_axes)} face-normal axes (Cartesian basis).")

    cube_dim, _ = GaugeGenerator.generate_algebra(cube_axes)
    print(f"  Generated Algebra Dimension: {cube_dim}")
    print(f"  Target: <=2  (Cartan / Abelian sub-algebra of SU(3))")

    results["Cube"] = {
        "axes": len(cube_axes),
        "dimension": cube_dim,
        "target": 2,
        "match": (cube_dim <= 2),
        "note": "Cartesian face normals span only the Cartan subalgebra (dim=2)."
    }
    
    # 2. The Octahedron (Control)
    print("\n2. Testing The Octahedron (Control Group B)...")
    # Vertices: (+-1, 0, 0), ...
    oct_points = [
        [1,0,0], [-1,0,0],
        [0,1,0], [0,-1,0],
        [0,0,1], [0,0,-1]
    ]
    oct_points = np.array(oct_points)
    oct_hull = ConvexHull(oct_points)
    
    # Octahedron has 3-fold symmetry on FACES (8 faces -> 4 axes).
    # Vertices are 4-fold and faces are 3-fold.
    # Our `identify_3fold_axes` looks for VERTICES with 3 faces meeting.
    # In the octahedron, four faces meet at each vertex; this method therefore finds 0 axes.
    # The geometric generator rule is "vertices with 3 incident faces".
    # This is topological.
    
    oct_axes = GaugeGenerator.identify_3fold_axes(oct_hull)
    print(f"  Identified {len(oct_axes)} axes of 3-fold symmetry (Vertex-based).")
    
    oct_dim, _ = GaugeGenerator.generate_algebra(oct_axes)
    print(f"  Generated Algebra Dimension: {oct_dim}")
    
    results["Octahedron"] = {
        "axes": len(oct_axes),
        "dimension": oct_dim,
        "note": "Vertices are 4-fold, expecting 0 axes."
    }

    # 3. The Rhombic Triacontahedron (The Vacuum)
    print("\n3. Testing Rhombic Triacontahedron (GCT Vacuum)...")
    # Generate Polyhedron
    rt = RhombicTriacontahedron()
    # Need points for hull. RT vertices are convex hull of... 
    # RT object has `hull` attribute!
    
    rt_hull = rt.hull
    rt_axes = _build_rt_axes()
    
    print(f"  Identified {len(rt_axes)} axes of 3-fold symmetry.")
    # RT has 12 5-fold vertices (icosahedral) and 20 3-fold vertices (dodecahedral).
    # 20 vertices -> 10 axes.
    # We expect 10.
    
    print("  Generating Lie Algebra closure (this may take a moment)...")
    rt_dim, _ = GaugeGenerator.generate_algebra(rt_axes)
    print(f"  Generated Algebra Dimension: {rt_dim}")
    print(f"  Target: 8 (SU(3))")
    
    results["RhombicTriacontahedron"] = {
        "axes": len(rt_axes),
        "dimension": rt_dim,
        "target": 8,
        "match": (rt_dim == 8)
    }
    
    print("  === Null Vector Extraction ===")
    G = np.zeros((10, 10))
    for i in range(10):
        for j in range(10):
            G[i, j] = (np.dot(rt_axes[i], rt_axes[j]))**2
    
    U, S, Vh = np.linalg.svd(G)
    null_indices = np.where(S < 1e-9)[0]
    null_vectors = Vh[null_indices]
    
    print(f"  SVD Singular values of Gram matrix: {S}")
    print(f"  Found {len(null_indices)} null vectors.")
    if len(null_indices) == 4:
        print("  [PASS] Null space dimension is exactly 4.")
        gram_nullity_status = "PASS"
    else:
        print("  [FAIL] Null space dimension is NOT 4.")
        gram_nullity_status = "FAIL"
        
    for idx, nv in enumerate(null_vectors):
        print(f"    n_{idx+1} = {nv}")
        
    results["RhombicTriacontahedron"]["gram_null_vectors"] = null_vectors.tolist()
    results["RhombicTriacontahedron"]["gram_rank"] = int(10 - len(null_indices))
    results["RhombicTriacontahedron"]["gram_rank_upper_bound_any_ten_axes"] = 6
    results["RhombicTriacontahedron"]["gram_nullity_check"] = gram_nullity_status
    try:
        results["RhombicTriacontahedron"]["cartan_A2_within_tolerance"] = _a2_within_tolerance(rt_axes)
    except Exception:
        results["RhombicTriacontahedron"]["cartan_A2_within_tolerance"] = False
    
    # 4. Control C (Cuboctahedron)
    print("\n4. Testing Cuboctahedron (Control Group C)...")
    cuboc_axes = [
        np.array([1.0, 1.0, 1.0]) / np.sqrt(3),
        np.array([-1.0, 1.0, 1.0]) / np.sqrt(3),
        np.array([1.0, -1.0, 1.0]) / np.sqrt(3),
        np.array([-1.0, -1.0, 1.0]) / np.sqrt(3)
    ]
    cuboc_dim, _ = GaugeGenerator.generate_algebra(cuboc_axes)
    print(f"  Generated Algebra Dimension: {cuboc_dim}")
    
    cuboc_cartan_a2_match = False
    cuboc_su3_match = False
    if cuboc_dim == 8:
        try:
            basis_c = build_su3_basis(cuboc_axes)
            f_c = compute_structure_constants(basis_c)
            cm_c, _ = compute_cartan_matrix(basis_c, f_c)
            target_cm = np.array([[2, -1], [-1, 2]])
            # A2 Cartan agreement alone is not the full RT uniqueness witness.
            # The control is rejected unless it also has the 10-axis RT orbit
            # and the Gram-nullity check.
            if np.array_equal(cm_c, target_cm):
                cuboc_cartan_a2_match = True
                cuboc_su3_match = (len(cuboc_axes) == len(rt_axes))
        except Exception:
            pass

    results["Cuboctahedron"] = {
        "axes": len(cuboc_axes),
        "dimension": cuboc_dim,
        "match": not cuboc_su3_match,
        "cartan_A2_match": cuboc_cartan_a2_match,
        "note": "Rejected as a full RT witness: lacks the 10-axis RT orbit and its Gram-nullity check."
    }

    # 5. Control D (Perturbed RT)
    print("\n5. Testing Perturbed RT (Control Group D)...")
    np.random.seed(42)  # Deterministic test
    perturbed_axes = []
    for ax in rt_axes:
        noise = (np.random.rand(3) - 0.5) * 2.0 * 0.01
        p_ax = ax + noise
        p_ax /= np.linalg.norm(p_ax)
        perturbed_axes.append(p_ax)
        
    print(f"  Added uniform noise (eps=0.01) to the 10 RT axes.")
    pert_dim, _ = GaugeGenerator.generate_algebra(perturbed_axes)
    print(f"  Generated Algebra Dimension: {pert_dim}")

    pert_su3_match = False
    if pert_dim == 8:
        try:
            basis_p = build_su3_basis(perturbed_axes)
            f_p = compute_structure_constants(basis_p)
            cm_p, _ = compute_cartan_matrix(basis_p, f_p)
            target_cm = np.array([[2, -1], [-1, 2]])
            # Strict tolerance check: must NOT have floating point noise
            if np.array_equal(cm_p, target_cm):
                pert_su3_match = True
        except Exception:
            pass
            
    try:
        pert_a2_tol = _a2_within_tolerance(perturbed_axes) if pert_dim == 8 else False
    except Exception:
        pert_a2_tol = False
    results["PerturbedRT"] = {
        "axes": len(perturbed_axes),
        "dimension": pert_dim,
        "match": not pert_su3_match,
        "cartan_A2_within_tolerance": pert_a2_tol,
        "note": ("Exact float equality of the Cartan matrix is not a discriminating test; "
                 "the tolerance-based comparison is recorded separately."),
    }
    
    # 6. Monte Carlo Control
    mc_results = run_monte_carlo_control(n_trials=1000)
    mc_results["reached_algebra_test"] = int(mc_results["n_trials_with_10_threefold_axes"])
    mc_results["discriminating"] = bool(mc_results["n_trials_with_10_threefold_axes"] > 0)
    results["MonteCarlo_Control"] = mc_results

    # 6b. Matched-axis control
    print("\n6b. Matched-axis control (ten random unit axes)...")
    matched = run_matched_axis_control()
    results["MatchedAxis_Control"] = matched

    # 7. Save and Verify
    rt_witness = (
        rt_dim == 8
        and results["RhombicTriacontahedron"].get("gram_nullity_check") == "PASS"
        and results["RhombicTriacontahedron"].get("cartan_A2_within_tolerance") is True
    )
    uniqueness_passed = (
        rt_witness
        and cube_dim <= 2
        and matched["discriminates_rt"]
        and mc_results["discriminating"]
        and mc_results["pass"]
    )
    results["rt_candidate_witness"] = bool(rt_witness)
    results["specificity_established"] = bool(uniqueness_passed)
    results["pass"] = bool(uniqueness_passed)
    results["verdict"] = (
        "PASS_NUMERICAL_CONTROL" if uniqueness_passed
        else "OPEN_CANDIDATE_SPECIFICITY_NOT_ESTABLISHED"
    )
    results["framing"] = (
        "PASS (numerical control): matched controls fail the RT witness; "
        "theorem-grade uniqueness remains O.39."
        if uniqueness_passed
        else ("OPEN: the RT inventory closes to an 8-dimensional algebra with an A2 "
              "Cartan matrix, but generic matched ten-axis sets do the same and no "
              "random polyhedron reached the algebra test. RT specificity is not "
              "established; the color identification is an open Tier 3 candidate (O.39).")
    )
    
    outfile = get_output_path("protocol_gauge_uniqueness_results.json")
    with open(outfile, "w") as f:
        json.dump(results, f, indent=2)

    print("\n" + "="*60)
    print(results["framing"])
    print(f"  RT dim={rt_dim}, Gram rank={results['RhombicTriacontahedron']['gram_rank']}, "
          f"Cube dim={cube_dim}, Cuboctahedron dim={cuboc_dim}, Perturbed RT dim={pert_dim}.")
    print(f"  Matched-axis control: {matched['n_A2_within_tolerance']}/{matched['n_trials']} A2 within tolerance.")
    print(f"  Monte Carlo: {mc_results['reached_algebra_test']}/{mc_results['n_trials']} trials reached the algebra test.")
    print("="*60)

if __name__ == "__main__":
    run_uniqueness_proof()
