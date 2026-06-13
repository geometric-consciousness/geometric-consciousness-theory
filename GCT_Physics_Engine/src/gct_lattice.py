#!/usr/bin/env python3
"""
gct_lattice.py — 6D Hypercubic Lattice Data Structure
=====================================================
Defines the `GCTLattice` class representing the vacuum substrate
as a Z^6 hypercubic lattice projected onto R^3.

Features:
- Generates Z^6 integer points within a 6D bounding box.
- Filters points based on perpendicular space confinement (RT radius).
- Manages state variables: x_equilibrium, u_displacement, velocities.
- Pre-computes neighbor lists for 6D connectivity.
"""

import numpy as np
import itertools
from dataclasses import dataclass
from typing import Tuple, List, Optional
import sys

# GCT Imports
from gct_utils import C
import gct_projections as proj

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DIMENSION = 6

# Approximate radius of Rhombic Triacontahedron in perp space units
# Cutoff radius sufficient to generate the test cluster (not derived from the
# lattice constants). An unscaled RT has outer radius sqrt(5+2sqrt(5)) ~= 3.078.
# We'll use a standard "safe" cutoff for unit lattice.
RT_RADIUS_APPROX = 2.5 

class GCTLattice:
    """
    Represents the 6D hypercubic lattice subset (quasicrystal approximant/patch).
    
    Attributes
    ----------
    dimension : int
        Fixed at 6.
    N_nodes : int
        Number of active nodes in the simulation.
    x_equilibrium : np.ndarray (N_nodes, 6)
        Integer coordinates of the equilibrium positions in Z^6.
    u_displacement : np.ndarray (N_nodes, 6)
        Dynamic displacement vectors from equilibrium.
    velocities : np.ndarray (N_nodes, 6)
        Velocity vectors (du/dt).
    """

    def __init__(self, R: int, perp_cutoff: float = RT_RADIUS_APPROX):
        """
        Initialize the lattice by generating Z^6 points within radius R
        and filtering by perp-space confinement.

        Parameters
        ----------
        R : int
            Chebyshev radius in 6D integer space (max coordinate value).
            Warning: The number of candidate points grows as (2R+1)^6.
            Keep R small (<= 4) for testing.
        perp_cutoff : float
            Maximum allowed norm in perpendicular space |x_perp|.
        """
        self.dimension = DIMENSION
        self.perp_cutoff = perp_cutoff
        
        print(f"Initializing GCT Lattice (R={R}, Cutoff={perp_cutoff})...")
        
        # 1. Generate candidate points in Z^6
        # Using a generator to avoid massive memory usage before filtering if R is large
        # For R=2, (2*2+1)^6 = 15625, fitting easily in memory.
        
        range_vals = range(-R, R + 1)
        candidates_list = []
        
        # Iterating product. 
        # Cluster initialization uses a vectorized meshgrid: fast at R=2, with
        # memory growing at R=3-4.

        ranges = [np.arange(-R, R + 1)] * DIMENSION
        candidate_grid = np.array(np.meshgrid(*ranges)).T.reshape(-1, DIMENSION)
        
        # 2. Filter by Perp Space Cutoff
        # We need to project ALL candidates to check their perp norm.
        # This is the "Cut" in "Cut-and-Project".
        
        x_perp = proj.project_perp(candidate_grid) # (N, 3)
        norms = np.linalg.norm(x_perp, axis=1)
        
        mask = norms <= perp_cutoff
        self.x_equilibrium = candidate_grid[mask].astype(np.float64) # Keep as float for physics ops
        self.N_nodes = len(self.x_equilibrium)
        
        print(f"  Candidates: {len(candidate_grid)}")
        print(f"  Accepted:   {self.N_nodes} ({(self.N_nodes/len(candidate_grid))*100:.1f}%)")
        
        # 3. Initialize State Variables
        self.u_displacement = np.zeros_like(self.x_equilibrium)
        self.velocities     = np.zeros_like(self.x_equilibrium)
        
        # 4. Precompute Neighbors
        self.neighbor_indices = self.get_neighbors()

    def get_neighbors(self) -> List[np.ndarray]:
        """
        Compute adjacency list for 12 nearest neighbors in 6D.
        
        In Z^6, NN are points with distance 1 (changing one coordinate by +/- 1).
        There are 2*6 = 12 neighbors.
        
        Returns
        -------
        neighbors : List[np.ndarray]
            A list where index i contains an array of indices j that are neighbors of node i.
            (Returned as a list of arrays; a sparse matrix is an equivalent representation.)
        """
        # Brute force distance matrix is O(N^2).
        # For N=1000, N^2 = 1,000,000 floats (8MB) -> Fast.
        # For N=10,000, N^2 = 100,000,000 floats (800MB) -> Manageable.
        # For N > 20,000, need KDTree.
        
        if self.N_nodes > 15000:
            print("Warning: Large N, brute force neighbor search might be slow.")
            # Fallback to CKDTree if scipy is available, else brute force
            try:
                from scipy.spatial import cKDTree
                tree = cKDTree(self.x_equilibrium)
                # Query nearest neighbors within distance 1.1 (allowing for float error)
                # k=13 because the point itself is included
                dists, network = tree.query(self.x_equilibrium, k=13, distance_upper_bound=1.1)
                
                neighbor_list = []
                for i, row in enumerate(network):
                    # Filter out the point itself (dist ~ 0) and infinite sentinels.
                    valid_neighbors = []
                    for j, idx in enumerate(row):
                         if idx != i and idx < self.N_nodes and dists[i,j] <= 1.1:
                             valid_neighbors.append(idx)
                    neighbor_list.append(np.array(valid_neighbors, dtype=int))
                return neighbor_list

            except ImportError:
                pass # Fall through to broadcasting

        # Vectorized Brute Force for moderate N
        # We are looking for exactly distance 1 in Integer grid Z^6.
        # But x_equilibrium is float.
        # Use squared Euclidean distance.
        
        # This requires calculating pairwise distances. 
        # To avoid N^2 memory for large N, we can iterate or use a spatially hashed approach.
        # For the sanity-check regime (N < 2000), broadcasting is fine.
        
        # Optimization: We know neighbors must be in the list.
        # We can build a lookup map from tuple(coords) -> index.
        
        coord_map = {tuple(row): i for i, row in enumerate(self.x_equilibrium)}
        neighbor_list = []
        
        # The 12 standard basis vectors +/- e_k
        basis_vectors = np.eye(DIMENSION, dtype=int)
        directions = np.vstack([basis_vectors, -basis_vectors]) # (12, 6)
        
        for i in range(self.N_nodes):
            current_pos = self.x_equilibrium[i]
            neighs = []
            for d in directions:
                target = tuple(current_pos + d)
                if target in coord_map:
                    neighs.append(coord_map[target])
            neighbor_list.append(np.array(neighs, dtype=int))
            
        return neighbor_list


# ---------------------------------------------------------------------------
# Sanity Check
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("-" * 60)
    print("GCT Lattice Module — Sanity Check")
    print("-" * 60)
    
    # Check 1: Small Lattice
    R_test = 2
    lattice = GCTLattice(R=R_test)
    
    print(f"\nCreated Lattice with R={R_test}")
    print(f"Nodes: {lattice.N_nodes}")
    print(f"Dimensions: {lattice.x_equilibrium.shape}")
    
    # Check 2: Neighbor count statistics
    neighbors = lattice.neighbor_indices
    counts = [len(n) for n in neighbors]
    avg_neighbors = np.mean(counts)
    
    print(f"\nNeighbor Statistics:")
    print(f"  Avg Coordination: {avg_neighbors:.2f}")
    print(f"  Max Coordination: {np.max(counts)}")
    print(f"  Min Coordination: {np.min(counts)} (Surface nodes)")
    
    # Check 3: zero-point energy is 0 for centered u=0.
    # Just checking internal consistency of state
    total_kinetic = 0.5 * np.sum(lattice.velocities**2)
    print(f"\nInitial Kinetic Energy: {total_kinetic}")
    
    # Check 4: Projection of Center Node
    center_idx = -1
    # Find origin if exists
    origin = np.zeros(6)
    dists = np.linalg.norm(lattice.x_equilibrium, axis=1)
    min_dist_idx = np.argmin(dists)
    
    if dists[min_dist_idx] < 1e-6:
        print(f"\nOrigin Node Detected at Index {min_dist_idx}")
        p_para = proj.project_parallel(lattice.x_equilibrium[min_dist_idx])
        p_perp = proj.project_perp(lattice.x_equilibrium[min_dist_idx])
        print(f"  Projected Parallel: {p_para}")
        print(f"  Projected Perp:     {p_perp}")
    
    print("-" * 60)
    print("Sanity Check Complete.")
    print("-" * 60)
