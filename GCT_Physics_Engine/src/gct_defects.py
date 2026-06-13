#!/usr/bin/env python3
"""
gct_defects.py — Lattice Surgery Tools
======================================
Utilities for creating defects (vacancies, interstitials, clusters)
in the GCT vacuum structure.

"Surgical" modification of the 6D lattice integers.
"""

import numpy as np
from typing import Optional, List

# GCT Imports
from gct_lattice import GCTLattice
from gct_hamiltonian import GCTHamiltonian

class DefectBuilder:
    """
    Static utility class for modifying lattice topology.
    """
    
    @staticmethod
    def remove_node(lattice: GCTLattice, index: int, hamiltonian: Optional[GCTHamiltonian] = None):
        """
        Remove a single node from the lattice by index.
        
        Parameters
        ----------
        lattice : GCTLattice
            The lattice to modify in-place.
        index : int
            Index of the node to remove.
        hamiltonian : Optional[GCTHamiltonian]
            If provided, its cache will be invalidated.
        """
        if index < 0 or index >= lattice.N_nodes:
            raise IndexError(f"Node index {index} out of bounds (N={lattice.N_nodes})")
        
        # 1. Delete rows from state arrays
        # Create mask to keep everything except index
        mask = np.ones(lattice.N_nodes, dtype=bool)
        mask[index] = False
        
        lattice.x_equilibrium = lattice.x_equilibrium[mask]
        lattice.u_displacement = lattice.u_displacement[mask]
        lattice.velocities = lattice.velocities[mask]
        
        # 2. Update count
        lattice.N_nodes -= 1
        
        # 3. Update connectivity
        # Indices have shifted! Recomputing neighbors is the safest robust way.
        # This is O(N) or O(N log N) depending on implementation.
        # For N ~ 200, it's instant.
        lattice.neighbor_indices = lattice.get_neighbors()
        
        # 4. Invalidate Hamiltonian Cache if linked
        if hamiltonian:
            hamiltonian.invalidate_cache()

    @staticmethod
    def create_central_hole(lattice: GCTLattice, radius_sq: float, hamiltonian: Optional[GCTHamiltonian] = None):
        """
        Remove all nodes within a certain squared distance from the origin (0,0,0,0,0,0).
        
        Parameters
        ----------
        radius_sq : float
            Squared Euclidean distance in 6D integer space.
        """
        # Calculate distances
        dists_sq = np.sum(lattice.x_equilibrium**2, axis=1)
        
        # Keep nodes OUTSIDE the hole
        mask = dists_sq >= radius_sq
        
        # Apply mask
        lattice.x_equilibrium = lattice.x_equilibrium[mask]
        lattice.u_displacement = lattice.u_displacement[mask]
        lattice.velocities = lattice.velocities[mask]
        
        lattice.N_nodes = len(lattice.x_equilibrium)
        
        # Recompute
        lattice.neighbor_indices = lattice.get_neighbors()
        
        if hamiltonian:
            hamiltonian.invalidate_cache()
            
    @staticmethod
    def build_cage(lattice: GCTLattice, N_target: int, hamiltonian: Optional[GCTHamiltonian] = None):
        """
        Create a cluster of exactly N_target nodes closest to the origin,
        removing the origin itself (creating a vacancy).
        
        This builds the "Cage" for the N-scan.
        
        Parameters
        ----------
        N_target : int
            Number of nodes to keep (excluding origin).
        """
        # 1. Calculate distances from origin (6D Euclidean)
        # Note: 6D integers.
        dists_sq = np.sum(lattice.x_equilibrium**2, axis=1)
        
        # 2. Sort indices by distance
        sorted_indices = np.argsort(dists_sq)
        
        # 3. Select nodes
        # We want the closest nodes, BUT we want to EXCLUDE the origin (dist=0).
        # Assuming origin exists at index 0 of sorted list if dist=0.
        
        keep_indices = []
        count = 0
        
        for idx in sorted_indices:
            if dists_sq[idx] < 1e-6:
                continue # Skip origin (Vacancy)
            
            keep_indices.append(idx)
            count += 1
            if count == N_target:
                break
                
        if count < N_target:
            raise ValueError(f"Lattice too small (R={lattice.x_equilibrium.max()}) to extract {N_target} nodes.")
            
        keep_indices = np.array(keep_indices)
        
        # 4. Slice
        lattice.x_equilibrium = lattice.x_equilibrium[keep_indices]
        # Reset U and V for fresh relaxation
        lattice.u_displacement = np.zeros_like(lattice.x_equilibrium)
        lattice.velocities = np.zeros_like(lattice.x_equilibrium)
        
        lattice.N_nodes = len(lattice.x_equilibrium)
        
        # 5. Recompute
        lattice.neighbor_indices = lattice.get_neighbors()
        
        if hamiltonian:
            # Important: The Hamiltonian passed might reference the OLD lattice arrays if not careful.
            # But Hamiltonian holds reference to `lattice` object, and we updated attributes in-place.
            # So checks out.
            hamiltonian.invalidate_cache()

# ---------------------------------------------------------------------------
# Sanity Check
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("-" * 60)
    print("GCT Defect Builder — Sanity Check")
    print("-" * 60)
    
    # Setup
    lattice = GCTLattice(R=2)
    H = GCTHamiltonian(lattice)
    initial_N = lattice.N_nodes
    print(f"Initial Lattice: N={initial_N}")
    
    # 1. Test Single Removal
    print("\nRemoving node 0...")
    DefectBuilder.remove_node(lattice, 0, H)
    print(f"New N: {lattice.N_nodes}")
    assert lattice.N_nodes == initial_N - 1
    
    # Check H works
    E_tot, _, _ = H.compute_total_energy()
    print(f"Energy after removal: {E_tot:.4f}")
    
    # 2. Test Cage Build
    print("\nBuilding Cage N=20...")
    # Need fresh lattice or large enough
    lattice = GCTLattice(R=2)
    H = GCTHamiltonian(lattice) # Re-bind
    
    DefectBuilder.build_cage(lattice, 20, H)
    print(f"Cage N: {lattice.N_nodes}")
    assert lattice.N_nodes == 20
    
    # Check origin is gone
    dists = np.linalg.norm(lattice.x_equilibrium, axis=1)
    min_dist = np.min(dists)
    print(f"Min dist from origin: {min_dist:.4f} (Should be > 0)")
    assert min_dist > 0.1
    
    print("-" * 60)
