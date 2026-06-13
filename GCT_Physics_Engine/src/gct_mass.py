#!/usr/bin/env python3
"""
gct_mass.py — Inertial Mass Calculation
=======================================
Calculates the effective mass of defects (phantoms) by measuring
the energy barrier for translation (Peierls-Nabarro potential).
"""

import numpy as np
from typing import Tuple, List

# GCT Imports
from gct_lattice import GCTLattice
from gct_hamiltonian import GCTHamiltonian
from gct_stability import LatticeRelaxer
import gct_defects as defects

class MassCalculator:
    """
    Tools for computing effective mass from energy landscapes.
    """
    
    def __init__(self, relaxer: LatticeRelaxer):
        self.relaxer = relaxer

    def compute_peierls_nabarro_barrier(
        self, 
        lattice: GCTLattice, 
        hamiltonian: GCTHamiltonian, 
        direction_6d: np.ndarray, 
        steps: int = 10
    ) -> Tuple[np.ndarray, np.ndarray, float]:
        """
        Estimate the PN barrier by shifting the lattice relative to the locking potential.
        
        The physical interpretation is moving the phason/defect.
        Technically, we shift the *displacement field* u by a fraction of a lattice period.
        
        Parameters
        ----------
        lattice : GCTLattice
            The base configuration (presumed relaxed).
        hamiltonian : GCTHamiltonian
            The energy function.
        direction_6d : np.ndarray
            Direction vector in 6D integer space (e.g. [1,0,0,0,0,0]).
        steps : int
            Number of steps to scan across one unit period.
            
        Returns
        -------
        shifts : np.ndarray
            Fraction of lattice constant shifted.
        energies : np.ndarray
            Relaxed energy at each step.
        barrier_height : float
            Max energy - Min energy.
        """
        # Normalize direction to unit length in integer space.
        # Usually we scan from alpha=0 to 1 along a basis vector.
        
        shifts = np.linspace(0, 1.0, steps)
        energies = []
        
        # Save initial state
        initial_u = lattice.u_displacement.copy()
        initial_x = lattice.x_equilibrium.copy() # Should not change
        
        print(f"Scanning PN Barrier ({steps} steps)...")
        
        for alpha in shifts:
            # Shift Logic:
            # We want to translate the "defect center".
            # For a vacancy, the "center" is void.
            # If we shift the underlying grid (x_equilibrium), we change the discrete structure.
            # If we shift u, we are just straining it.
            
            # Correct approach for PN barrier in discrete systems:
            # Constrain the "center of mass" or a specific coordinate, and relax others.
            # Or, apply a global shift to the locking potential reference.
            
            # Since our locking potential is P_perp(x+u), shifting u by `d` is equivalent 
            # to shifting the atomic surface window.
            
            # Rigid shift ansatz:
            shift_vector = alpha * direction_6d
            
            # Peierls-Nabarro migration scan: seed the lattice with a rigid
            # displacement of the defect by `alpha` along the 6D direction, then
            # relax. The relaxed energy E(alpha) traces the migration landscape,
            # whose saddle (the PN barrier) sits near alpha = 0.5. The relaxation
            # is seeded rather than reaction-coordinate-constrained, so a low or
            # zero-mode barrier lets the defect slide toward an integer ground
            # state, while a high barrier holds it in the metastable well near alpha.
            lattice.u_displacement = initial_u + shift_vector
            e_final = self.relaxer.relax_structure(lattice, hamiltonian)
            energies.append(e_final)
            
        energies = np.array(energies)
        barrier = np.max(energies) - np.min(energies)
        
        # Restore
        lattice.u_displacement = initial_u
        
        return shifts, energies, barrier

# ---------------------------------------------------------------------------
# Sanity Check
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("-" * 60)
    print("GCT Mass Calculator — Sanity Check")
    print("-" * 60)
    
    # 1. Setup small lattice
    lattice = GCTLattice(R=1, perp_cutoff=1.0) # Tiny N=33
    hamiltonian = GCTHamiltonian(lattice)
    relaxer = LatticeRelaxer(tol=1e-4) # Loose tol for speed
    mass_calc = MassCalculator(relaxer)
    
    # 2. Create a vacancy
    print(f"Original N: {lattice.N_nodes}")
    # Remove center (closest to origin)
    dists = np.sum(lattice.x_equilibrium**2, axis=1)
    center_idx = np.argmin(dists)
    defects.DefectBuilder.remove_node(lattice, center_idx, hamiltonian)
    print(f"Defect N:   {lattice.N_nodes}")
    
    # 3. Compute Barrier along direction [1,0,0,0,0,0]
    direction = np.array([1, 0, 0, 0, 0, 0], dtype=float)
    
    shifts, E, barrier = mass_calc.compute_peierls_nabarro_barrier(
        lattice, hamiltonian, direction, steps=5
    )
    
    print("\nPN Barrier Scan:")
    for s, e_val in zip(shifts, E):
        print(f"  Shift {s:.2f}: E = {e_val:.6f}")
        
    print(f"\nBarrier Height: {barrier:.6e}")
    
    # Mass approx ~ Barrier / (lattice_const)^2... 
    # Just checking functional execution.
    
    print("-" * 60)
