#!/usr/bin/env python3
"""
gct_geometry.py — Exact 6D Hypercube Projection Geometry
========================================================
Defines the Rhombic Triacontahedron (RT) as the perpendicular space 
projection of the 6D unit hypercube.

This module uses Scipy's ConvexHull to determine the exact boundaries 
of the acceptance window (atomic surface) for the quasicrystal.
"""

import numpy as np
import itertools
from scipy.spatial import ConvexHull
from typing import Tuple, Optional

# GCT Imports
import gct_projections as proj

class RhombicTriacontahedron:
    """
    Represents the exact acceptance window for the GCT lattice.
    Defined as the convex hull of the projected vertices of a 6D hypercube.
    
    The 6D hypercube is centered at origin with side length 1.
    Vertices are at (+/- 0.5, +/- 0.5, ...).
    """

    def __init__(self):
        """
        Initialize the geometry by computing the convex hull in 3D perp space.
        """
        # 1. Generate 6D Hypercube Vertices
        # 2^6 = 64 vertices at +/- 0.5
        vertices_6d = np.array(list(itertools.product([-0.5, 0.5], repeat=6)))
        
        # 2. Project to Perpendicular Space
        # (64, 6) -> (64, 3)
        self.vertices_perp = proj.project_perp(vertices_6d)
        
        # 3. Compute Convex Hull
        # This gives us the equations of the faces: n*x + d <= 0
        self.hull = ConvexHull(self.vertices_perp)
        
        # Extract equations: [normal_x, normal_y, normal_z, offset]
        # Equation: normal . x + offset <= 0
        # So normal . x <= -offset
        # Scipy returns equations such that n.x + d <= 0.
        # We want penetration distance p = n.x + d > 0 ? p : 0
        
        self.equations = self.hull.equations # (N_faces, 4)
        self.normals = self.equations[:, :3] # (N_faces, 3)
        self.offsets = self.equations[:, 3]  # (N_faces,)
        
        # For RT, we expect 30 faces.
        self.num_faces = len(self.equations)
        # print(f"Initialized RhombicTriacontahedron with {self.num_faces} faces.")

    def compute_penetration(self, points: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute how far points are *outside* the RT.
        
        Parameters
        ----------
        points : np.ndarray (N, 3)
            Points in perpendicular space.
            
        Returns
        -------
        penetration_depths : np.ndarray (N,)
            Distance outside the hull. 0.0 if inside.
        gradient_directions : np.ndarray (N, 3)
            Normalized direction of the penetration gradient (face normal).
            If inside, direction is zero vector (or undefined, but zero convenient).
        """
        # Convex Hull defined by intersection of half-spaces: n_i . x + d_i <= 0
        # If n_i . x + d_i > 0, the point is outside face i.
        # The penetration depth is max_i (n_i . x + d_i).
        # If all <= 0, max is <= 0, so clamp to 0.
        
        # Vectorized check against all faces
        # (N, 3) @ (3, F) + (F,) -> (N, F)
        distances_to_faces = points @ self.normals.T + self.offsets
        
        # Find max penetration for each point
        max_indices = np.argmax(distances_to_faces, axis=1) # (N,)
        # Use simple indexing to get the max values
        # Fancy indexing: range(N), max_indices
        max_dists = distances_to_faces[np.arange(len(points)), max_indices]
        
        # Filter: only positive distances matter
        outside_mask = max_dists > 0
        
        penetration = np.zeros(len(points))
        penetration[outside_mask] = max_dists[outside_mask]
        
        # Gradients
        # For points outside, the gradient of the distance function is the normal 
        # of the face they are penetrating most.
        gradients = np.zeros_like(points)
        
        # Only set gradients for outside points
        if np.any(outside_mask):
            relevant_indices = max_indices[outside_mask]
            gradients[outside_mask] = self.normals[relevant_indices]
            
        return penetration, gradients


# ---------------------------------------------------------------------------
# Sanity Check
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("-" * 60)
    print("GCT Geometry (Rhombic Triacontahedron) — Sanity Check")
    print("-" * 60)
    
    rt = RhombicTriacontahedron()
    print(f"Hull Vertices: {len(rt.hull.vertices)}") # Expected <= 64, with 32 RT outer vertices plus coplanar support points.
    # The RT has 32 vertices.
    # The 6D hypercube projected has interior vertices too. 
    # ConvexHull filters them.
    
    print(f"Hull Faces:    {rt.num_faces}") # Expected 30 for RT.
    
    # Check 1: origin inside with zero penetration.
    origin = np.zeros((1, 3))
    p, g = rt.compute_penetration(origin)
    print(f"Origin Penetration: {p[0]}")
    
    # Check 2: A point far away
    far_point = np.array([[10, 0, 0]])
    p_far, g_far = rt.compute_penetration(far_point)
    print(f"Far Point Penetration: {p_far[0]}")
    print(f"Far Point Normal: {g_far[0]}")
    
    # Check 3: Random points
    print("\nRandom Points Test:")
    rng = np.random.default_rng(42)
    test_points = rng.uniform(-5, 5, (5, 3))
    p_test, g_test = rt.compute_penetration(test_points)
    
    for i in range(5):
        status = "Outside" if p_test[i] > 0 else "Inside"
        print(f"  Point {test_points[i]} -> {status} (d={p_test[i]:.4f})")

    print("-" * 60)
