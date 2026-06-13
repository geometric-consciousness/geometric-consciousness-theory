#!/usr/bin/env python3
"""
gct_redundancy.py — Gauge Redundancy Verifier 
==========================================================
Checks that the GCT Hamiltonian is invariant under LOCAL SU(3) rotations
of the internal phason displacement field u_perp.

Physical Interpretation:
    The phason displacement u_perp of a site lives in E_perp (3D internal space).
    A local SU(3) rotation mixes the three "color components" of u_perp at a 
    single site without changing the physical energy.
    This is EXACTLY the definition of a local gauge symmetry.
    => Gluons are the "gauge bosons" of these local phason rearrangements.
"""

import numpy as np
from typing import Tuple, Dict

# GCT Imports
from gct_lattice import GCTLattice
from gct_hamiltonian import GCTHamiltonian
import gct_projections as proj


class GaugeRedundancyVerifier:
    """
    Tests local SU(3) gauge invariance of the Hamiltonian.
    """

    @staticmethod
    def apply_local_su3_rotation(
        lattice: GCTLattice,
        site_idx: int,
        generator: np.ndarray
    ) -> None:
        """
        Apply a local SU(3) rotation to the phason displacement of ONE site.

        The 6D displacement u[site] = (u_para, u_perp) decomposes into
        a physical part (u_para in E_parallel) and internal part (u_perp in E_perp).
        We rotate ONLY the u_perp component.

        Parameters
        ----------
        lattice   : GCTLattice (modified IN PLACE)
        site_idx  : Index of site to rotate
        generator : (3, 3) Hermitian traceless matrix (SU(3) generator)
        """
        M_perp = proj.get_m_perp()   # (3, 6)
        M_para = proj.get_m_parallel()  # (3, 6)

        u_site = lattice.u_displacement[site_idx]  # (6,)

        # Decompose into perp component
        u_perp_3d = M_perp @ u_site   # (3,)
        u_para_3d = M_para @ u_site   # (3,)

        # Apply infinitesimal SU(3) rotation: u_perp -> exp(i eps G) u_perp
        # For small eps, exp(i eps G) ≈ I + i*eps*G
        eps = 0.05  # Small angle
        # G is Hermitian, so R = exp(i*eps*G) is unitary.
        # For real displacement: use real part of rotation.
        # G is real symmetric (our generators from gct_gauge are real sym).
        # exp(i*eps*G) for real symmetric G has Re(R) = cos(eps*G-eigenvals).
        # Easier: just apply rotation matrix R = expm(eps*G) treated as 3x3 real
        # since our generators Q = v*v^T - I/3 are real.

        # Compute matrix exponential via eigendecomposition
        evals, evecs = np.linalg.eigh(generator.real)
        R = evecs @ np.diag(np.cos(eps * evals)) @ evecs.T  # Real rotation

        # Rotate u_perp
        u_perp_rotated = R @ u_perp_3d   # (3,)

        # Recompose 6D displacement:
        # u = M_para^T u_para + M_perp^T u_perp  (pseudo-inverse reconstruction)
        # Since M_para, M_perp are isometries: M^T @ M @ u = component in subspace
        # Full reconstruction: u_new = M_para^T @ u_para_3d + M_perp^T @ u_perp_rotated
        u_new = M_para.T @ u_para_3d + M_perp.T @ u_perp_rotated  # (6,)
        lattice.u_displacement[site_idx] = u_new

    @staticmethod
    def verify_gauge_invariance(
        lattice: GCTLattice,
        hamiltonian: GCTHamiltonian,
        generator: np.ndarray,
        site_idx: int = 0,
        tol: float = 1e-6
    ) -> Dict:
        """
        Test: Apply local SU(3) rotation to one site. Check if energy changes.

        Returns
        -------
        dict with:
            E_before, E_after, delta_E, is_invariant (bool)
        """
        # Measure energy before
        E_before, _, _ = hamiltonian.compute_total_energy()

        # Save state
        u_saved = lattice.u_displacement.copy()

        # Apply rotation to chosen site
        GaugeRedundancyVerifier.apply_local_su3_rotation(lattice, site_idx, generator)

        # Measure energy after
        E_after, _, _ = hamiltonian.compute_total_energy()

        # Restore state
        lattice.u_displacement = u_saved

        delta_E = abs(E_after - E_before)
        is_invariant = delta_E < tol

        return {
            "E_before": float(E_before),
            "E_after": float(E_after),
            "delta_E": float(delta_E),
            "is_invariant": is_invariant,
            "tolerance": tol
        }

    @staticmethod
    def scan_all_sites(
        lattice: GCTLattice,
        hamiltonian: GCTHamiltonian,
        generator: np.ndarray,
        max_sites: int = 10,
        tol: float = 1e-4
    ) -> Dict:
        """
        Verify gauge invariance across multiple sites.
        Returns summary statistics.
        """
        results = []
        n_sites = min(max_sites, lattice.N_nodes)

        for i in range(n_sites):
            r = GaugeRedundancyVerifier.verify_gauge_invariance(
                lattice, hamiltonian, generator, site_idx=i, tol=tol
            )
            results.append(r)

        delta_Es = [r["delta_E"] for r in results]
        n_invariant = sum(1 for r in results if r["is_invariant"])

        return {
            "n_sites_tested": n_sites,
            "n_invariant": n_invariant,
            "max_delta_E": float(max(delta_Es)),
            "mean_delta_E": float(np.mean(delta_Es)),
            "all_invariant": (n_invariant == n_sites)
        }


# ---------------------------------------------------------------------------
# Sanity Check
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    from gct_lattice import GCTLattice
    from gct_hamiltonian import GCTHamiltonian
    import numpy as np

    print("-" * 60)
    print("GCT Redundancy Verifier — Sanity Check")
    print("-" * 60)

    # Small lattice
    lattice = GCTLattice(R=1, perp_cutoff=1.5)
    H = GCTHamiltonian(lattice)

    print(f"Lattice Nodes: {lattice.N_nodes}")

    # Use a simple generator: the diagonal SU(3) generator lambda_3
    # lambda_3 = diag(1, -1, 0) (traceless)
    gen = np.array([
        [1,  0,  0],
        [0, -1,  0],
        [0,  0,  0]
    ], dtype=float)

    print("Testing gauge invariance (local SU(3) rotation)...")
    result = GaugeRedundancyVerifier.verify_gauge_invariance(lattice, H, gen)

    print(f"  E_before:     {result['E_before']:.8f}")
    print(f"  E_after:      {result['E_after']:.8f}")
    print(f"  delta_E:      {result['delta_E']:.2e}")
    print(f"  Is Invariant: {result['is_invariant']}")

    print("-" * 60)
