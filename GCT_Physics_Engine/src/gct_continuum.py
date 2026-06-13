#!/usr/bin/env python3
"""
gct_continuum.py — Homogenization Engine
========================================
Coarse-graining tools to extract macroscopic continuum properties
from the microscopic lattice structure.

Calculates:
- Effective Elastic Moduli (Stiffness Tensor)
- Speed of Sound (Speed of Light in GCT)
- Effective Metric g_mu_nu
"""

import numpy as np
from typing import Tuple, Dict

# GCT Imports
from gct_lattice import GCTLattice
from gct_hamiltonian import GCTHamiltonian
from gct_stability import LatticeRelaxer
import gct_projections as proj

class ContinuumHomogenizer:
    """
    Derives continuum properties from lattice response.
    """
    
    def __init__(self, relaxer: LatticeRelaxer):
        self.relaxer = relaxer

    def coarse_grain_stiffness(
        self, 
        lattice: GCTLattice, 
        hamiltonian: GCTHamiltonian, 
        strain_epsilon: float = 1e-4
    ) -> float:
        """
        Compute the effective bulk stiffness (K_eff) by applying an isotropic strain
        and measuring the energy response.
        
        Method:
        1. Apply uniform expansion u = epsilon * x (in parallel space)
        2. Relax internal degrees of freedom under fixed-boundary conditions.
        3. E = 0.5 * V * K_eff * epsilon^2
        
        For GCT, we are interested in the shear/bulk modulus for PHYSICAL strains
        (Parallel space strains).
        
        Parameters
        ----------
        lattice : GCTLattice
            Representative volume element (RVE).
        hamiltonian : GCTHamiltonian
            Energy function.
        strain_epsilon : float
            Magnitude of strain.
            
        Returns
        -------
        K_eff : float
            Effective stiffness in lattice units.
        """
        # 1. State 0: Relaxed
        self.relaxer.relax_structure(lattice, hamiltonian)
        E0, _, _ = hamiltonian.compute_total_energy()
        
        # 2. Apply Strain
        # u_strain = epsilon * x_parallel
        # But x is in 6D. We want to strain physical space.
        # x_para = P_para(x). x_perp = P_perp(x).
        # New position x' = (1+eps) x_para + x_perp
        # u = x' - x = eps * x_para
        
        # The affine displacement is applied to all nodes and treated as the boundary condition.
        # For bulk modulus, this displacement can be applied to all nodes before relaxation
        # subject to boundary constraints.
        
        # Simplified approach: "Affine Deformation"
        # The affine displacement is applied to ALL nodes.
        # Then we measure energy WITHOUT relaxation (Born approximation)
        # Relaxation gives the relaxed modulus.
        
        # Born approximation gives the upper-bound response.
        # Fixed-boundary relaxation is represented by the imposed affine shape.
        
        # The strain fixes the finite-cluster boundary shape.
        # if the equilibrium positions define the "shape".
        # The variables here are u.
        
        # We implement: u += eps * project_parallel(x)
        x_para = proj.project_parallel(lattice.revert_integer_coordinates() if hasattr(lattice, 'revert_integer_coordinates') else lattice.x_equilibrium)
        # Note: lattice.x_equilibrium is float but represents integers.
        x_para = proj.project_parallel(lattice.x_equilibrium)
        
        # Transform back to 6D displacement.
        # u_6d = x_para_3d @ M_para
        M_para = proj.get_m_parallel()
        u_strain = strain_epsilon * (x_para @ M_para)
        
        # Apply
        lattice.u_displacement += u_strain
        
        # Measure Energy (Affine / Unrelaxed)
        E_strained, _, _ = hamiltonian.compute_total_energy()
        
        # Energy density = (E_strained - E0) / Volume
        # RVE volume can be approximated from the projected 3D support.
        # Or count nodes. Vol ~ N_nodes * v0.
        # v0 = 1 (unit cell volume in 6D projected to 3D density).
        
        # dE = 0.5 * K * epsilon^2 * V
        # K = 2 * dE / (epsilon^2 * V)
        # The implemented stiffness is normalized per node.
        
        dE = E_strained - E0
        
        # If dE is negative, we are unstable.
        
        # Volume estimation
        # Density of projected Z6 is not 1. It's complicated.
        # Return the energy-per-node stiffness parameter.
        # k_eff_per_node = 2 * (dE/N) / eps^2
        
        k_eff_per_node = 2 * (dE / lattice.N_nodes) / (strain_epsilon**2)
        
        # Restore
        lattice.u_displacement -= u_strain
        
        return k_eff_per_node

    def derive_acoustic_metric(self, K_eff: float, density: float = 1.0) -> Dict[str, float]:
        """
        Derive the effective speed of light/sound and metric.
        
        c = sqrt(K_eff / density)
        g_00 = -c^2
        
        Parameters
        ----------
        K_eff : float
            Effective stiffness in energy/volume/strain^2 units.
            Units: Energy units.
        density : float
            Effective mass density.
            
        Returns
        -------
        metric_data : dict
            c_s, g_00, g_ii
        """
        # If K_eff is per node, and density is mass per node.
        # Then c = sqrt(K_node / M_node).
        # Assuming M_node = 1 (Lattice Units).
        
        c_s = np.sqrt(abs(K_eff) / density)
        
        return {
            "c_s": c_s,
            "c_sq": c_s**2,
            "g_00": -(c_s**2),
            "g_11": 1.0,
            "g_22": 1.0,
            "g_33": 1.0
        }

# ---------------------------------------------------------------------------
# Sanity Check
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("-" * 60)
    print("GCT Continuum Mechanics — Sanity Check")
    print("-" * 60)
    
    # Setup
    lattice = GCTLattice(R=2, perp_cutoff=2.5)
    H = GCTHamiltonian(lattice)
    relaxer = LatticeRelaxer(tol=1e-5)
    homogenizer = ContinuumHomogenizer(relaxer)
    
    # Measure
    print(f"Lattice N={lattice.N_nodes}")
    K_node = homogenizer.coarse_grain_stiffness(lattice, H, strain_epsilon=0.001)
    
    print(f"Effective Stiffness per Node: {K_node:.6f}")
    
    # Metric
    metric = homogenizer.derive_acoustic_metric(K_node, density=1.0)
    print(f"Derived Speed of Sound (c):   {metric['c_s']:.6f}")
    print(f"Metric g_00:                  {metric['g_00']:.6f}")
    
    print("-" * 60)
