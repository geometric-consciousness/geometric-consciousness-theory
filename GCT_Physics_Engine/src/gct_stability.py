#!/usr/bin/env python3
"""
gct_stability.py — Vibrational Stability Analysis
=================================================
Tools for finding the ground state configuration and analyzing 
the phonon/phason spectrum of the GCT lattice.

Features:
- LatticeRelaxer: Minimizes Hamiltonian energy using L-BFGS-B.
- Hessian Analysis: Computes the dynamical matrix (Force Hessian)
  and its eigen-spectrum to identify stable/unstable modes.
"""

import numpy as np
from scipy.optimize import minimize
from typing import Tuple, List

# GCT Imports
from gct_lattice import GCTLattice
from gct_hamiltonian import GCTHamiltonian

class LatticeRelaxer:
    """
    Minimizes the energy of a GCT lattice configuration.
    """

    def __init__(self, tol: float = 1e-6):
        """
        Initialize the relaxer.
        
        Parameters
        ----------
        tol : float
            Tolerance for convergence (force norm).
        """
        self.tol = tol

    def relax_structure(self, lattice: GCTLattice, hamiltonian: GCTHamiltonian) -> float:
        """
        Relax the current lattice configuration to a local minimum.
        Updates lattice.u_displacement in-place.
        
        Returns
        -------
        final_energy : float
            The minimized total energy.
        """
        N = lattice.N_nodes
        x0 = lattice.u_displacement.ravel() # Flatten for optimizer
        
        # Define Objective Function for Scipy
        def objective(u_flat):
            # Reshape
            u_current = u_flat.reshape((N, 6))
            
            # Temporarily update lattice state
            # Note: The Hamiltonian reads from lattice.u_displacement
            lattice.u_displacement = u_current
            
            # Compute E and Forces
            E_tot, _, _ = hamiltonian.compute_total_energy()
            forces = hamiltonian.compute_forces()
            
            # Gradients for minimize are -forces
            grads = -forces.ravel()
            
            return E_tot, grads
            
        print(f"Relaxing lattice with {N} nodes...")
        
        # Run Optimization
        res = minimize(
            objective, 
            x0, 
            method='L-BFGS-B', 
            jac=True, 
            options={'ftol': self.tol, 'gtol': self.tol, 'disp': False}
        )
        
        # Update lattice with final result
        lattice.u_displacement = res.x.reshape((N, 6))
        
        print(f"Relaxation Complete. Status: {res.message}")
        print(f"Final Energy: {res.fun:.6e}")
        
        return res.fun

    def compute_hessian(self, lattice: GCTLattice, hamiltonian: GCTHamiltonian, eps: float = 1e-5) -> np.ndarray:
        """
        Compute the Hessian matrix (6N x 6N) via finite differences of forces.
        H_ij = - dF_i / du_j
        
        Parameters
        ----------
        eps : float
            Finite difference step size.
            
        Returns
        -------
        hessian : np.ndarray (6N, 6N)
        """
        N = lattice.N_nodes
        dim = 6
        num_dof = N * dim
        
        print(f"Computing Hessian ({num_dof} x {num_dof})...")
        
        hessian = np.zeros((num_dof, num_dof))
        
        # Base forces at current configuration
        # Make sure lattice state is consistent
        f0 = hamiltonian.compute_forces().ravel()
        u0 = lattice.u_displacement.copy()
        
        # Iterate over all degrees of freedom
        # For small N this is fine. For N=1000, 6000 evals is okay.
        
        if N > 200:
            print("  Progress:", end=" ", flush=True)
            
        for i in range(num_dof):
            # Perturb DOF i
            u_perturb = u0.ravel()
            u_perturb[i] += eps
            lattice.u_displacement = u_perturb.reshape((N, dim))
            
            # Get perturbed force
            f_plus = hamiltonian.compute_forces().ravel()
            
            # Finite difference
            # H_ij = - (F_i(u+eps) - F_i(u)) / eps
            # Force is negative gradient, so Hessian is Jacobian of -Force = Jacobian of Gradient
            # d(Grad E)/du = - dF/du
            
            # Perturbing coordinate u_i yields the force-gradient column dF_j / du_i.
            
            # Hessian H_ij = d^2E / (du_i du_j)
            # F_j = - dE / du_j
            # So H_ij = - dF_j / du_i
            # We are perturbing u_i. We see change in all F_j.
            # So this gives us the i-th COLUMN of the Hessian (or row due to symmetry).
            
            col_i = -(f_plus - f0) / eps
            hessian[:, i] = col_i
            
            if N > 200 and i % (num_dof // 10) == 0:
                print(f"{int(i/num_dof*100)}%...", end=" ", flush=True)
        
        if N > 200:
            print("Done.")
            
        # Symmetrize to reduce noise
        hessian = 0.5 * (hessian + hessian.T)
        
        # Restore lattice state
        lattice.u_displacement = u0
        
        return hessian

    def compute_sparse_hessian(self, lattice: GCTLattice, hamiltonian: GCTHamiltonian) -> 'scipy.sparse.csc_matrix':
        """
        Build the 6N x 6N Hessian matrix as a sparse matrix directly from the analytic forces.
        """
        import scipy.sparse as sp
        N = lattice.N_nodes
        dim = 6
        num_dof = N * dim
        row = []
        col = []
        data = []

        import gct_projections as proj
        
        # 1. Phonon Hessian (Parallel Space)
        edges = hamiltonian._get_edges()
        degrees = np.zeros(N)
        if len(edges) > 0:
            for i, j in edges:
                degrees[i] += 1
                degrees[j] += 1
                for d in range(dim):
                    # Off-diagonal
                    row.extend([i*dim + d, j*dim + d])
                    col.extend([j*dim + d, i*dim + d])
                    data.extend([-hamiltonian.K_PARALLEL, -hamiltonian.K_PARALLEL])

        # Diagonal phonon terms
        for i in range(N):
            for d in range(dim):
                row.append(i*dim + d)
                col.append(i*dim + d)
                data.append(hamiltonian.K_PARALLEL * degrees[i])

        # 2. Lock Hessian (Perpendicular Space)
        pos_total = lattice.x_equilibrium + lattice.u_displacement
        x_perp = proj.project_perp(pos_total)
        dists, gradients = hamiltonian.geometry.compute_penetration(x_perp)

        mask = dists > 0
        if np.any(mask):
            M_perp = proj.get_m_perp()  # (3, 6)
            for i in range(N):
                if mask[i]:
                    n = gradients[i]  # normal vector shape (3,)
                    # H_6D = K_perp * M^T (n * n^T) M
                    H_6D = hamiltonian.K_PERP * (M_perp.T @ np.outer(n, n) @ M_perp)
                    for d1 in range(dim):
                        for d2 in range(dim):
                            row.append(i*dim + d1)
                            col.append(i*dim + d2)
                            data.append(H_6D[d1, d2])

        hessian_sparse = sp.csc_matrix((data, (row, col)), shape=(num_dof, num_dof))
        return hessian_sparse

    def analyze_spectrum(self, hessian: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute eigenvalues of the Hessian.
        
        Returns
        -------
        frequencies_sq : np.ndarray (6N,)
            Squared frequencies (eigenvalues).
        eigenvectors : np.ndarray (6N, 6N)
            Eigenvectors (columns).
        """
        print("Diagonalizing Hessian...")
        w2, v = np.linalg.eigh(hessian)
        
        # Sort
        idx = np.argsort(w2)
        w2 = w2[idx]
        v = v[:, idx]
        
        return w2, v


# ---------------------------------------------------------------------------
# Sanity Check
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("-" * 60)
    print("GCT Stability Analysis — Sanity Check")
    print("-" * 60)
    
    # 1. Setup small lattice
    from gct_geometry import RhombicTriacontahedron
    
    # Use a smaller cutoff to get a tiny cluster for quick testing
    # R=1 gives 729 candidates. With cutoff=1.0, we get ~60 nodes.
    lattice = GCTLattice(R=1, perp_cutoff=1.0) 
    hamiltonian = GCTHamiltonian(lattice) # Using currently installed Hamiltonian
    
    print(f"Test Lattice Nodes: {lattice.N_nodes}")
    
    relaxer = LatticeRelaxer(tol=1e-5)
    
    # 2. Perturb and Relax
    print("\nPerturbing lattice...")
    rng = np.random.default_rng(42)
    lattice.u_displacement += rng.uniform(-0.1, 0.1, lattice.u_displacement.shape)
    
    E_initial, _, _ = hamiltonian.compute_total_energy()
    print(f"Initial Energy: {E_initial:.6e}")
    
    E_final = relaxer.relax_structure(lattice, hamiltonian)
    
    # 3. Spectrum
    hess = relaxer.compute_hessian(lattice, hamiltonian)
    w2, v = relaxer.analyze_spectrum(hess)
    
    print(f"\nSpectrum (First 10 modes):")
    print(np.round(w2[:10], 5))
    
    if np.any(w2 < -1e-4):
        print("  WARNING: Unstable modes detected (Negative w^2)")
    else:
        print("  Stability: Stable (No significant negative eigenvalues)")
        
    print("-" * 60)
