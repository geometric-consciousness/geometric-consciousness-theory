#!/usr/bin/env python3
"""
gct_lorentz.py — Lorentz Symmetry Analyzer
====================================================
Tools to verify the emergence of Lorentz symmetry (Isotropy)
by analyzing the phonon/phason dispersion relations.

Distinguishes between:
1. Phonon Branch (Bulk/Gravity): High velocity, Parallel polarized.
2. Phason Branch (Light/Info): Low velocity, Perpendicular polarized.

Identifies the GCT Speed of Light c = Phi^-9 from the Phason branch.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List, Dict

# GCT Imports
from gct_lattice import GCTLattice
from gct_hamiltonian import GCTHamiltonian
from gct_stability import LatticeRelaxer
import gct_projections as proj

class DispersionAnalyzer:
    """
    Computes dispersion relations via Full Hessian Diagonalization.
    """
    
    def __init__(self, relaxer: LatticeRelaxer):
        self.relaxer = relaxer

    def project_wavevector(
        self, 
        eigenvector: np.ndarray, 
        lattice: GCTLattice,
        direction: np.ndarray
    ) -> Tuple[float, float]:
        """
        Assign an effective wavevector k (scalar magnitude along direction)
        to a given eigenvector by spatial Fourier Transform.
        
        S(k) = | sum_j u_j * exp(i k * x_j_para . direction) |^2
        
        We scan k to find the peak.
        
        Parameters
        ----------
        eigenvector : (N*6,) flattened mode shape.
        lattice : GCT Lattice.
        direction : (3,) unit vector in Parallel Space.
        
        Returns
        -------
        k_peak : float
        spectral_weight : float (0 to 1) quality of the k-assignment.
        """
        # Reshape to (N, 6)
        u_mode = eigenvector.reshape((lattice.N_nodes, 6))
        
        # Project displacement to 3D Parallel space for Phonon analysis
        # For Phasons, the "wave" is also in the tiling, but usually 
        # parameterized by physical space coordinate x_para.
        # i.e. u_perp(x_para) ~ exp(i k x_para).
        
        # We want the modulation wavevector in PHYSICAL space.
        
        # Get x_para
        x_para = proj.project_parallel(lattice.x_equilibrium) # (N, 3)
        
        # Project x onto direction
        x_proj = x_para @ direction # (N,) scalar positions along line
        
        # Compute the spatial modulation through the complex Fourier transform.
        
        # u_mode is a 6D displacement field.
        # We want to detect the spatial modulation.
        # Sum the 6D displacement vectors directly.
        # F(k) = sum_j u_j * exp(-i * k * x_j_proj)  -> Vector result
        # Power(k) = |F(k)|^2
        
        # Scan k from 0 to Pi (approx).
        k_scan = np.linspace(0.0, 3.14, 50)
        powers = []
        
        # Vectorized Fourier transform.
        # exp_factors: (N, n_k)
        phases = np.outer(x_proj, k_scan) # (N, K)
        exp_factors = np.exp(-1j * phases) # (N, K)
        
        # F_k: (K, 6)
        # sum_j u_j (1, 6) * exp (1)
        # u_mode: (N, 6)
        
        # Einsum: n=nodes, d=dim(6), k=k_points
        F_k = np.einsum('nd,nk->kd', u_mode, exp_factors)
        
        # Power
        P_k = np.sum(np.abs(F_k)**2, axis=1) # (K,)
        
        best_idx = np.argmax(P_k)
        k_peak = k_scan[best_idx]
        max_power = P_k[best_idx]
        
        # Normalize against the mode power when needed.
        total_power = np.sum(np.abs(u_mode)**2) * lattice.N_nodes # Approximate Parseval normalization.
        # Parseval... return the P_k peak relative to total norm
        
        norm_factor = np.sum(np.abs(F_k)**2) # Aggregate scanned-k power.
        # Return k_peak.
        
        return k_peak, max_power

    def analyze_spectrum(
        self, 
        lattice: GCTLattice, 
        hamiltonian: GCTHamiltonian,
        direction: np.ndarray
    ) -> Dict[str, List[float]]:
        """
        Full spectral analysis.
        
        1. Compute Hessian & Diagonalize -> Eigenvalues (w^2) and Eigenvectors.
        2. For each mode:
            a. Classify Phonon vs Phason (Parallel vs Perp Energy).
            b. Assign effective k (Fourier peak).
        3. Collect data points (k, w) for both branches.
        """
        print("Computing Hessian...")
        hessian = self.relaxer.compute_hessian(lattice, hamiltonian, eps=1e-4)
        
        print("Diagonalizing...")
        try:
            # eigh for symmetric
            evals, evecs = np.linalg.eigh(hessian)
        except np.linalg.LinAlgError:
            print("Diagonalization failed!")
            return {}
            
        # evecs is (6N, 6N), columns are eigenvectors
        
        phonon_data = {"k": [], "w": []}
        phason_data = {"k": [], "w": []}
        
        # M_para, M_perp for classification
        M_para = proj.get_m_parallel()
        M_perp = proj.get_m_perp()
        
        N_nodes = lattice.N_nodes
        direction = direction / np.linalg.norm(direction)
        
        print(f"Analyzing {len(evals)} modes...")
        
        for i in range(len(evals)):
            w_sq = evals[i]
            
            # Skip translational zero modes (and negatives/instabilities)
            if w_sq < 1e-8:
                continue
                
            w = np.sqrt(w_sq)
            v = evecs[:, i] # (6N,)
            v_reshaped = v.reshape((N_nodes, 6))
            
            # 1. Classification
            # Project ALL displacements to Para and Perp and compare norms
            # v_reshaped is projected through the parallel/perpendicular maps.
            # v_reshaped is (N, 6).
            # We want component in E_para.
            # P_para project operator is (6,6).
            # But we have proj.project_parallel(v) -> (N,3)
            
            u_p = proj.project_parallel(v_reshaped) # (N,3)
            u_perp = proj.project_perp(v_reshaped)  # (N,3)
            
            power_para = np.sum(u_p**2)
            power_perp = np.sum(u_perp**2)
            
            ratio = power_para / (power_para + power_perp + 1e-12)
            
            # 2. k-vector
            # Analyze all modes that pass the k-window filter.
            k, quality = self.project_wavevector(v, lattice, direction)
            
            # Filter to the low-k acoustic regime.
            if k > 2.0:
                continue
                
            if ratio > 0.8:
                # Phonon
                phonon_data["k"].append(k)
                phonon_data["w"].append(w)
            elif ratio < 0.2:
                # Phason
                phason_data["k"].append(k)
                phason_data["w"].append(w)
            else:
                # Mixed mode
                pass
                
        return {"phonon": phonon_data, "phason": phason_data}

    def plot_dual_dispersion(
        self, 
        data: Dict, 
        filename: str = "dual_dispersion.png",
        target_c: float = 0.01315
    ):
        """Plot Phonon and Phason branches."""
        try:
            plt.figure(figsize=(12, 7))
            
            # Plot Phonons
            pk = np.array(data["phonon"]["k"])
            pw = np.array(data["phonon"]["w"])
            if len(pk) > 0:
                plt.scatter(pk, pw, c='r', alpha=0.5, s=10, label='Phonons (Bulk)')
                # Fit
                if len(pk) > 5:
                    mask = (pk > 0.1) & (pk < 1.5)
                    if np.sum(mask) > 2:
                        s, _ = np.polyfit(pk[mask], pw[mask], 1)
                        plt.plot(pk, s*pk, 'r--', alpha=0.5, label=f'c_phonon = {s:.3f}')
            
            # Plot Phasons
            phk = np.array(data["phason"]["k"])
            phw = np.array(data["phason"]["w"])
            c_phason = 0.0
            
            if len(phk) > 0:
                plt.scatter(phk, phw, c='b', alpha=0.5, s=10, label='Phasons (Holographic)')
                
                # Filter for the linear acoustic regime of gapless Goldstone phasons.
                mask = (phk > 0.1) & (phk < 1.5)
                if np.sum(mask) > 2:
                    c_phason, _ = np.polyfit(phk[mask], phw[mask], 1)
                    plt.plot(phk, c_phason*phk, 'b--', alpha=0.8, lw=2, label=f'c_phason = {c_phason:.3f}')

            plt.xlabel("Wavevector |k| (1/L)", fontsize=12)
            plt.ylabel("Frequency ω", fontsize=12)
            
            err = abs(c_phason - target_c) / target_c * 100 if c_phason > 0 else 100
            
            plt.title(f"GCT Dual-Branch Dispersion\nPhason Speed c = {c_phason:.5f} (Target $\Phi^{{-9}}={target_c:.5f}$, Err={err:.1f}%)", fontsize=14)
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.savefig(filename)
            print(f"Plot saved to {filename}")
            
            return c_phason
            
        except Exception as e:
            print(f"Plotting failed: {e}")
            return 0.0

# ---------------------------------------------------------------------------
# Sanity Check
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("-" * 60)
    print("GCT Lorentz Analyzer — Sanity Check")
    print("-" * 60)
    
    # R=1, cutoff=1.5 gives an approximately 60-100 node test lattice.
    lattice = GCTLattice(R=1, perp_cutoff=1.5)
    print(f"Nodes: {lattice.N_nodes} (Matrix size: {6*lattice.N_nodes})")
    
    H = GCTHamiltonian(lattice)
    relaxer = LatticeRelaxer(tol=1e-4) # Fast relax
    analyzer = DispersionAnalyzer(relaxer) # Pass relaxer for Hessian
    
    # Analyze
    direction = np.array([1, 0, 0])
    data = analyzer.analyze_spectrum(lattice, H, direction)
    
    # Check data content
    n_ph = len(data.get("phonon", {}).get("k", []))
    n_pha = len(data.get("phason", {}).get("k", []))
    print(f"Identified Modes: {n_ph} Phonons, {n_pha} Phasons")
    
    if n_pha > 0:
        k = data['phason']['k'][0]
        w = data['phason']['w'][0]
        print(f"Sample Phason: k={k:.3f}, w={w:.3f}")
        
    print("-" * 60)
