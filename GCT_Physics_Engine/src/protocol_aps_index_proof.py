#!/usr/bin/env python3
"""
protocol_aps_index_proof.py — Finite-Cage Spectral-Asymmetry Diagnostics
========================================================================
Computes two distinct finite-dimensional diagnostics on the canonical
I_h-closed icosahedral cage of a Z^6 vacancy:

1. the sign sum of the scalar weighted adjacency matrix A; and
2. the sign sum of the explicitly constructed 8N x 8N discrete Dirac matrix D.

The scalar sign sum divided by the spinor dimension is retained only as a
normalised graph diagnostic.  It is not the eta-invariant of D, an APS
boundary correction, or evidence for a bulk index.  In the present
construction the full discrete Dirac sign sum is zero.

Cage source: the canonical I_h-closed cage at perp_cutoff = 2.0 consists
of 5 full I_h orbits with sizes (12, 30, 20, 30, 60), totalling N = 152
nodes. The I_h closure is required for the App ULA Sec ULA.7 orthogonality
theorem on which the finite-N 1/(2N) correction depends. The cage is
constructed via `cage_builder.build_canonical_cage(size=152)`.

NO APS EVALUATION IS PERFORMED.  A qualifying APS calculation requires a
declared elliptic self-adjoint boundary operator, its Hilbert-space domain
and boundary conditions, the kernel term h, and a compatible bulk operator.
Those data and any graph-to-smooth comparison map remain Open Problem O.14c.
"""

import numpy as np
import sys
import json
from pathlib import Path

# Add GCT Physics Engine src to path
_SRC = Path(__file__).resolve().parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from gct_utils import get_output_path, GCTReporter, PHI
from cage_builder import build_canonical_cage

def get_gamma_6d():
    """Construct 8x8 Gamma matrices for Cl(6,0) using Kronecker products of Pauli matrices."""
    s_x = np.array([[0, 1], [1, 0]], dtype=complex)
    s_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    s_z = np.array([[1, 0], [0, -1]], dtype=complex)
    I2 = np.eye(2, dtype=complex)

    # Standard recursive construction for Cl(2n)
    gamma = []
    gamma.append(np.kron(s_x, np.kron(I2, I2)))
    gamma.append(np.kron(s_y, np.kron(I2, I2)))
    gamma.append(np.kron(s_z, np.kron(s_x, I2)))
    gamma.append(np.kron(s_z, np.kron(s_y, I2)))
    gamma.append(np.kron(s_z, np.kron(s_z, s_x)))
    gamma.append(np.kron(s_z, np.kron(s_z, s_y)))
    
    return np.array(gamma)

def run_aps_proof():
    reporter = GCTReporter("O.14c: Finite-Cage Spectral-Asymmetry Diagnostics")

    reporter.section("Lattice Geometry")
    # Construct the canonical I_h-closed boundary cage surrounding the
    # vacancy at the origin. The 5-orbit composition (12+30+20+30+60)
    # totals N = 152 nodes and is the smallest I_h-closed orbit-union
    # at perp_cutoff = 2.0 that includes the outermost 60-orbit required
    # by the App ULA Sec ULA.7 orthogonality theorem.
    nodes_6d, nodes_perp = build_canonical_cage(size=152)
    nodes = nodes_6d.astype(np.int64)
    N = nodes.shape[0]
    dim_dirac = 8  # For Cl(6)

    # Recompute parallel-space coords + perp-space coords for downstream use
    x_eq = nodes
    norms = np.linalg.norm(nodes_perp, axis=1)
    indices = np.arange(N)
    x_perp = nodes_perp

    reporter.log_value("Nodes in Boundary Cage", N)
    reporter.log_value("Dirac Spinor Dimension", dim_dirac)
    reporter.log_value("Cage construction", "I_h-closed 5-orbit (12+30+20+30+60)")

    reporter.section("Dirac Operator Construction")
    gammas = get_gamma_6d()
    
    # 3. Build Adjacency with Golden-Weighted Phason Hopping
    # Reference: protocol_spectral_action.py
    # This incorporates perpendicular space distances, which breaks the standard 6D NN bipartite structure.
    
    # D of size (N*8) x (N*8)
    D = np.zeros((N * dim_dirac, N * dim_dirac), dtype=complex)
    
    edge_count = 0
    non_bipartite = False
    
    # To check bipartiteness, we need the adjacency graph
    adj_graph = [[] for _ in range(N)]
    
    for i in range(N):
        for j in range(i + 1, N):
            p_i = x_perp[indices[i]]
            p_j = x_perp[indices[j]]
            dist_perp = np.linalg.norm(p_i - p_j)
            
            # 6D Direction vector (for Gamma matrices)
            d = nodes[j] - nodes[i]
            
            weight = 0.0
            # Long bonds (length ~ 1 in E_perp)
            if abs(dist_perp - 1.0) < 0.05:
                weight = 1.0
            # Short bonds (length ~ 1/phi in E_perp)
            elif abs(dist_perp - (1.0 / PHI)) < 0.05:
                weight = PHI
            
            if weight > 0:
                edge_count += 1
                adj_graph[i].append(j)
                adj_graph[j].append(i)
                
                # Construct Dirac coupling: i * weight * (Gamma . d_unit)
                # Normalize d for the gamma projection
                d_norm = np.linalg.norm(d)
                if d_norm > 0:
                    d_hat = d / d_norm
                    gamma_n = np.zeros((dim_dirac, dim_dirac), dtype=complex)
                    for a in range(6):
                        gamma_n += d_hat[a] * gammas[a]
                    
                    term = 1j * weight * gamma_n
                    
                    row_i, col_i = i * dim_dirac, (i + 1) * dim_dirac
                    row_j, col_j = j * dim_dirac, (j + 1) * dim_dirac
                    
                    D[row_i:col_i, row_j:col_j] = term
                    D[row_j:col_j, row_i:col_i] = term.conj().T
                    
    reporter.log_value("Edges detected", edge_count)
    
    # Bipartite check (2-coloring)
    color = [-1] * N
    is_bipartite = True
    for start_node in range(N):
        if color[start_node] == -1:
            stack = [(start_node, 0)]
            while stack:
                u, c = stack.pop()
                if color[u] != -1:
                    if color[u] != c:
                        is_bipartite = False
                        break
                    continue
                color[u] = c
                for v in adj_graph[u]:
                    stack.append((v, 1 - c))
        if not is_bipartite:
            break
            
    reporter.log_value("Graph is Bipartite?", is_bipartite)
    if not is_bipartite:
        print("  [SUCCESS] Odd cycles detected in shell geometry! Breaking spectral symmetry.")
                
    # 3. Spectral Analysis
    reporter.section(f"Spectral Analysis: Scalar Adjacency ({N}x{N})")
    # Construct scalar adjacency matrix A
    A = np.zeros((N, N))
    for i in range(N):
        for j in range(i + 1, N):
            p_i = x_perp[indices[i]]
            p_j = x_perp[indices[j]]
            dist_perp = np.linalg.norm(p_i - p_j)
            if abs(dist_perp - 1.0) < 0.05:
                A[i, j] = A[j, i] = 1.0
            elif abs(dist_perp - (1.0 / PHI)) < 0.05:
                A[i, j] = A[j, i] = PHI

    lambdas_scalar = np.linalg.eigvalsh(A)
    signs_scalar = np.sign(lambdas_scalar)
    nonzero_scalar = signs_scalar[np.abs(lambdas_scalar) > 1e-12]
    scalar_adjacency_sign_sum = np.sum(nonzero_scalar)
    
    reporter.log_value("Scalar Zero Modes", N - len(nonzero_scalar))
    reporter.log_value("Scalar Sum of Signs", float(scalar_adjacency_sign_sum))

    reporter.section(f"Spectral Analysis: Dirac Operator ({N * dim_dirac}x{N * dim_dirac})")
    print("  Computing Dirac spectrum...")
    lambdas_dirac = np.linalg.eigvalsh(D)
    signs_dirac = np.sign(lambdas_dirac)
    nonzero_dirac = signs_dirac[np.abs(lambdas_dirac) > 1e-12]
    eta_dirac = np.sum(nonzero_dirac)
    
    reporter.log_value("Dirac Zero Modes", len(lambdas_dirac) - len(nonzero_dirac))
    reporter.log_value("Dirac Sum of Signs", float(eta_dirac))
    
    # Object/domain separation
    # ------------------------
    # A is a finite scalar weighted adjacency matrix on C^N.  D is a
    # distinct finite Hermitian matrix on C^N tensor C^8.  Dividing the
    # sign sum of A by 8 is only a normalised scalar-graph diagnostic; it
    # does not turn A into D and does not define an APS eta-invariant.
    dim_spinor = 8
    scalar_per_spinor_diagnostic = float(scalar_adjacency_sign_sum) / dim_spinor

    reporter.section("Object/Domain Audit (Diagnostic Only — see O.14c)")
    reporter.log_value("Scalar adjacency sign sum", float(scalar_adjacency_sign_sum))
    reporter.log_value("Spinor Normalization Factor", dim_spinor)
    reporter.log_value("Scalar adjacency / spinor-dimension diagnostic", scalar_per_spinor_diagnostic)
    reporter.log_value("Full discrete Dirac sign sum", float(eta_dirac))
    reporter.log_value("Qualifying APS boundary operator specified?", False)
    reporter.log_value("APS eta evaluated?", False)

    reason = (
        f"DIAGNOSTIC_ONLY: scalar adjacency sign sum={scalar_adjacency_sign_sum:.0f}; "
        f"scalar/8 diagnostic={scalar_per_spinor_diagnostic:.4f}; "
        f"full discrete Dirac sign sum={eta_dirac:.0f}. "
        "No qualifying APS boundary operator/domain, kernel term, bulk "
        "operator, or graph-to-smooth comparison is specified; therefore "
        "no APS eta-invariant or APS index is evaluated."
    )
    reporter.verdict(False, reason)

    results = {
        "N_nodes": int(N),
        "cage_construction": "I_h-closed 5-orbit (12+30+20+30+60)",
        "scalar_adjacency_operator": "A on C^N (finite weighted adjacency matrix)",
        "scalar_adjacency_sign_sum": float(scalar_adjacency_sign_sum),
        "spinor_dimension": dim_spinor,
        "scalar_adjacency_per_spinor_dimension_diagnostic": scalar_per_spinor_diagnostic,
        "discrete_dirac_operator": "D on C^N tensor C^8 (finite Hermitian matrix)",
        "discrete_dirac_sign_sum": float(eta_dirac),
        "aps_boundary_operator_specified": False,
        "aps_boundary_operator_domain_specified": False,
        "aps_kernel_term_computed": False,
        "aps_eta_evaluated": False,
        "aps_index_evaluated": False,
        "object_domain_status": "separate_finite_graph_diagnostics_only",
        "scalar_eigenvalues_summary": {
            "min": float(np.min(lambdas_scalar)),
            "max": float(np.max(lambdas_scalar)),
            "mean_abs": float(np.mean(np.abs(lambdas_scalar)))
        },
        "pass": False,
        "tier_status": "DIAGNOSTIC_ONLY — finite scalar-adjacency and discrete-Dirac sign sums computed; qualifying APS operator/domain absent"
    }
    
    out_path = get_output_path("protocol_aps_index_proof_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=4)
        
    return results

if __name__ == "__main__":
    run_aps_proof()
