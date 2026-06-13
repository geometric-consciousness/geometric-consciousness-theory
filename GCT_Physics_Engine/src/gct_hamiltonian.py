#!/usr/bin/env python3
"""
gct_hamiltonian.py — 6D Microscopic Action
==========================================
Implements the Hamiltonian mechanics for the GCT vacuum.
Reference: Appendix M (Master Action)

Hamiltonian Structure:
----------------------
H = H_phonon + H_lock

1. H_phonon (Parallel Space Elasticity):
   Energy cost of distorting the lattice in physical space.
   E_ph = (1/2) * K_para * sum_{<i,j>} |u_i - u_j|^2

2. H_lock (Perpendicular Space Confinement):
   Energy cost of atom surfaces leaving the locking window (Protocol B).
   E_lock = (1/2) * K_perp * |P_perp(x_i + u_i)|^2
   
   Note: K_perp is suppressed by eta = PHI^-18 relative to K_para.
"""

import numpy as np
from typing import Tuple

# GCT Imports
from gct_utils import C
import gct_projections as proj
from gct_lattice import GCTLattice


from gct_geometry import RhombicTriacontahedron

class GCTHamiltonian:
    """
    Computes energy and forces for a GCTLattice state.
    Uses exact Rhombic Triacontahedron geometry for confinement.
    """
    
    def __init__(self, lattice: GCTLattice):
        """
        Initialize the Hamiltonian for a specific lattice instance.
        
        Parameters
        ----------
        lattice : GCTLattice
            The lattice object containing state variables (u, x, etc).
        """
        self.lattice = lattice
        
        # Physics Parameters (Lattice Units)
        self.K_PARALLEL = 1.0
        
        # Stiffness Ratio from SSOT
        try:
            self.K_PERP = self.K_PARALLEL * float(C.ETA_STIFFNESS)
        except (AttributeError, NameError):
             self.K_PERP = self.K_PARALLEL * (float(C.PHI)**-18)

        # Geometry for Locking Term
        self.geometry = RhombicTriacontahedron()
        
        # Cache for neighbor edges
        self._edge_indices = None

    def invalidate_cache(self):
        """
        Invalidate cached edge indices.
        Call this if the lattice topology changes (nodes added/removed).
        """
        self._edge_indices = None

    def _get_edges(self):
        """Helper to get cached edge indices."""
        if self._edge_indices is None:
            edges = []
            for i, neighbors in enumerate(self.lattice.neighbor_indices):
                for j in neighbors:
                    if i < j:
                        edges.append((i, j))
            self._edge_indices = np.array(edges, dtype=int)
        return self._edge_indices

    def compute_total_energy(self) -> Tuple[float, float, float]:
        """
        Compute the total potential energy of the current lattice state.
        
        Returns
        -------
        (E_total, E_phonon, E_lock) : Tuple[float, float, float]
        """
        u = self.lattice.u_displacement
        x = self.lattice.x_equilibrium
        
        # 1. Phonon Energy (Pairwise)
        E_phonon = 0.0
        edges = self._get_edges()
        if len(edges) > 0:
            idx_i = edges[:, 0]
            idx_j = edges[:, 1]
            diff = u[idx_i] - u[idx_j]
            dist_sq = np.sum(diff**2, axis=1)
            E_phonon = 0.5 * self.K_PARALLEL * np.sum(dist_sq)

        # 2. Locking Energy (Exact Geometry)
        # E_lock = 0.5 * K_perp * sum(penetration_distance^2)
        
        pos_total = x + u
        x_perp = proj.project_perp(pos_total)
        
        # Compute penetration
        dists, _ = self.geometry.compute_penetration(x_perp)
        
        # Only points outside the RT contribute
        E_lock = 0.5 * self.K_PERP * np.sum(dists**2)
        
        return E_phonon + E_lock, E_phonon, E_lock

    def compute_forces(self) -> np.ndarray:
        """
        Compute forces on all nodes. F = -Grad(H)
        
        Returns
        -------
        forces : np.ndarray (N, 6)
        """
        u = self.lattice.u_displacement
        x = self.lattice.x_equilibrium
        N = self.lattice.N_nodes
        
        forces = np.zeros((N, 6), dtype=np.float64)
        
        # 1. Phonon Forces
        edges = self._get_edges()
        if len(edges) > 0:
            idx_i = edges[:, 0]
            idx_j = edges[:, 1]
            
            diff = u[idx_i] - u[idx_j]
            
            # F_i += -K * (u_i - u_j)
            force_contribution = -self.K_PARALLEL * diff
            
            np.add.at(forces, idx_i, force_contribution)
            np.add.at(forces, idx_j, -force_contribution)

        # 2. Locking Forces
        # E = 0.5 * K * (n.x_perp - offset)^2
        # F_perp = -K * distance * normal
        # F_6D   = F_perp @ M_perp
        
        pos_total = x + u
        x_perp = proj.project_perp(pos_total)
        
        dists, gradients = self.geometry.compute_penetration(x_perp)
        
        # Lock force in perp space (N, 3)
        # Only for points with dist > 0
        mask = dists > 0
        
        if np.any(mask):
            # F_perp = -K * d * n
            # gradients contains normals for violated faces
            f_perp = -self.K_PERP * (dists[mask][:, np.newaxis] * gradients[mask])
            
            # Map back to 6D
            # f_6d = f_perp @ M_perp
            # M_perp is (3, 6). f_perp is (N_active, 3).
            # Result (N_active, 6)
            M_perp = proj.get_m_perp()
            f_lock_6d = f_perp @ M_perp
            
            forces[mask] += f_lock_6d
        
        return forces

# ---------------------------------------------------------------------------
# Sanity Check
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("-" * 60)
    print("GCT Hamiltonian — Sanity Check")
    print("-" * 60)
    
    # 1. Setup minimal lattice
    lattice = GCTLattice(R=2)
    H = GCTHamiltonian(lattice)
    
    print(f"Lattice Nodes: {lattice.N_nodes}")
    print(f"Eta Stiffness: {H.K_PERP:.4e}")
    
    # 2. Check Initial Energy (Equilibrium)
    # At u=0, phonon energy is zero.
    # Lock energy remains tiny but non-zero from confinement of equilibrium points.
    # In the cut-and-project construction, accepted points lie within RT radius.
    # They therefore have non-zero x_perp and E_lock(u=0) > 0.
    
    E_tot, E_ph, E_lk = H.compute_total_energy()
    print(f"\nInitial Energy (u=0):")
    print(f"  Total:  {E_tot:.6f}")
    print(f"  Phonon: {E_ph:.6f}")
    print(f"  Lock:   {E_lk:.6f}")
    
    # 3. Apply a perturbation
    # Displace one node
    idx = 0
    lattice.u_displacement[idx] = np.array([0.1, 0, 0, 0, 0, 0])
    
    E_tot_new, E_ph_new, E_lk_new = H.compute_total_energy()
    print(f"\nPerturbed Energy (Node 0 dx=0.1):")
    print(f"  Total:  {E_tot_new:.6f}")
    print(f"  Phonon: {E_ph_new:.6f}")
    print(f"  Lock:   {E_lk_new:.6f}")
    
    # 4. Check Forces
    forces = H.compute_forces()
    f_node = forces[idx]
    print(f"\nForce on perturbed node:")
    print(f"  F vector: {np.round(f_node, 4)}")
    print(f"  Norm:     {np.linalg.norm(f_node):.4f}")
    
    # Expect restoring force
    # Phonon force: neighbors pull back
    # Lock force: perp confinement pulls back
    
    print("-" * 60)
