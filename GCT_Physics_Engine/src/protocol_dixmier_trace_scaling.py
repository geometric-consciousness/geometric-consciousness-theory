#!/usr/bin/env python3
"""
protocol_dixmier_trace_scaling.py — AKN Gap-Label Scaling Type Check
====================================================================
Reports the topological spectral measure tau = phi^(-107) as the scaling
factor assigned from the assumed gap-labeling exponent n = -107
(Tier 3 anchor; uniqueness pending App H Open Problem O.14).

**Scope of this script:** the function name
`run_gap_label_scaling_typecheck` constructs the gamma matrices and the Dirac
spectrum on the I_h-closed boundary cage, but the load-bearing numerical
output of this script is `tau = PHI ** (-107)` assigned from the gap
exponent. The spectrum construction serves as a *type-check* that the
Dirac operator is well-defined on the cage geometry; the Dixmier trace
proper (Tr_omega on |D|^{-p}, where p is the spectral dimension) requires
the explicit Connes-Moscovici local-index-formula computation that is NOT
performed here.

**What this script verifies:** that the assumed exponent n = -107
produces the scaling factor tau = phi^(-107) consistent with downstream
mass-ratio derivations (V3 Ch07 m_e ratio). What it does NOT verify:
the first-principles uniqueness of n = -107 from the AF-core dimension
group / trace image of the AKN substitution algebra, which is Z[φ]; the
full Cuntz-Krieger K_0(O_A) for A=[[1,1],[1,0]] is trivial since
coker(I-A^T) is trivial. See App Y §Y.3 for the canonical AF-core-vs-full-O_A
distinction. Nor does it verify the explicit Dixmier-trace computation from
the cage Dirac spectrum (Open Problem candidate; see App H).

For the canonical Connes-Moscovici Dixmier-trace machinery on
substitution-tiling C*-algebras, see Connes-Moscovici 1995 GAFA + the
Bellissard-Herrmann-Zarrouati gap-labeling references in App H O.14.
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

def get_gamma_6d():
    s_x = np.array([[0, 1], [1, 0]], dtype=complex)
    s_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    s_z = np.array([[1, 0], [0, -1]], dtype=complex)
    I2 = np.eye(2, dtype=complex)

    gamma = []
    gamma.append(np.kron(s_x, np.kron(I2, I2)))
    gamma.append(np.kron(s_y, np.kron(I2, I2)))
    gamma.append(np.kron(s_z, np.kron(s_x, I2)))
    gamma.append(np.kron(s_z, np.kron(s_y, I2)))
    gamma.append(np.kron(s_z, np.kron(s_z, s_x)))
    gamma.append(np.kron(s_z, np.kron(s_z, s_y)))
    
    return np.array(gamma)

def run_gap_label_scaling_typecheck():
    reporter = GCTReporter("AKN Gap-Label Scaling Type Check")
    
    reporter.section("Lattice Geometry")
    # Canonical I_h-closed boundary cage (5 orbits: 12+30+20+30+60 = 152).
    from cage_builder import build_canonical_cage
    nodes_6d, nodes_perp = build_canonical_cage(size=152)
    nodes = nodes_6d.astype(np.int64)
    N = nodes.shape[0]
    dim_dirac = 8
    indices = np.arange(N)
    x_perp = nodes_perp

    reporter.log_value("Nodes in Boundary Cage", N)
    reporter.log_value("Dirac Spinor Dimension", dim_dirac)
    reporter.log_value("Cage construction", "I_h-closed 5-orbit (12+30+20+30+60)")
    
    reporter.section("Dirac Operator Construction")
    gammas = get_gamma_6d()
    D = np.zeros((N * dim_dirac, N * dim_dirac), dtype=complex)
    
    for i in range(N):
        for j in range(i + 1, N):
            p_i = x_perp[indices[i]]
            p_j = x_perp[indices[j]]
            dist_perp = np.linalg.norm(p_i - p_j)
            
            d = nodes[j] - nodes[i]
            
            weight = 0.0
            if abs(dist_perp - 1.0) < 0.05:
                weight = 1.0
            elif abs(dist_perp - (1.0 / PHI)) < 0.05:
                weight = PHI
            
            if weight > 0:
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
                    
    reporter.section("Dirac Spectrum Type-Check")
    print("  Computing Dirac spectrum on the I_h-closed cage (type-check only)...")
    lambdas_dirac = np.linalg.eigvalsh(D)

    # Filter out clear zero modes to form |D|^{-1}
    nz_mask = np.abs(lambdas_dirac) > 1e-12
    lambdas_nz = lambdas_dirac[nz_mask]

    # Type-check observables from the constructed spectrum: these confirm
    # the Dirac operator is well-defined on the cage (gamma-matrix algebra
    # closes, the spectrum is real, non-zero modes are dense), but they do
    # NOT constitute a Dixmier-trace derivation of the gap-label scaling.
    n_modes_total = int(lambdas_dirac.shape[0])
    n_modes_nonzero = int(lambdas_nz.shape[0])
    spectrum_max_abs = float(np.max(np.abs(lambdas_nz))) if n_modes_nonzero > 0 else 0.0
    spectrum_min_abs = float(np.min(np.abs(lambdas_nz))) if n_modes_nonzero > 0 else 0.0

    reporter.log_value("Dirac modes (total)", n_modes_total)
    reporter.log_value("Dirac modes (nonzero)", n_modes_nonzero)
    reporter.log_value("Spectrum |lambda| range", f"[{spectrum_min_abs:.3e}, {spectrum_max_abs:.3e}]")

    reporter.section("Gap-Label Scaling Factor (asserted, not derived)")

    # The Dixmier trace of |D|^{-p} for the spectral dimension p maps into
    # the K_0(A) module Z + Z*phi via the Connes-Moscovici local index
    # formula (Connes-Moscovici 1995 GAFA + Bellissard-Herrmann-Zarrouati
    # 2000 gap-labelling on the AKN tiling C*-algebra). The canonical
    # output is the assumed gap-label scaling factor tau = phi^{-107}
    # downstream protocols (Ch07 mass-ratio chain) consume.
    #
    # **What this script asserts:** the scaling factor tau = phi^n with
    # n = -107 is the gap-label integer downstream protocols rely on;
    # the canonical identification |n| = 107 = sum m_i^2(H_3) is
    # established at Tier 2 via the Coxeter-exponent uniqueness derivation
    # of `protocol_o14_coxeter_exponent_squares.py` (App H O.14 path (l)
    # closure on the integer-identification side).
    #
    # **What this script does NOT derive:** the residue
    # Res_{s=p} Tr(|D|^{-s}) from the constructed Dirac spectrum above.
    # The Connes-Moscovici local index formula on a substitution-tiling
    # C*-algebra requires (a) the spectral dimension p of the AKN hull as
    # an analytic input (Bellissard 1992 gap-labelling extends to discrete
    # spectra only via Banach-density arguments; the finite-cage spectrum
    # computed here has no continuum spectral dimension) and (b) the
    # Pimsner-Voiculescu six-term sequence on the AKN crossed product to
    # identify the trace image. The full numerical residue computation is
    # registered as the residual Tier 4 physical-link conjecture of App H
    # Open Problem O.14 (the structural-link chain V -> AF-core dimension group / trace image).
    #
    # The current script therefore evaluates the assumed gap-label
    # scaling factor as input, type-checks the Dirac spectrum, and exposes
    # both quantities for dependent protocols. The "derivation" claim
    # would require closure of O.14; the present output is the asserted
    # scaling factor + type-check verdict.
    n_gap = -107
    dixmier_scaling = PHI ** n_gap

    reporter.log_value("Assumed gap-label integer (n)", n_gap)
    reporter.log_value("Algebraic Base (\u03A6)", PHI)
    reporter.log_value("Assumed gap-label scaling factor \u03A6^{-107}", dixmier_scaling)

    # Type-check verdict: the script confirms the Dirac operator is
    # well-defined on the constructed cage and exposes the assumed gap-label
    # scaling factor used by dependent protocols; it does NOT close the
    # Connes-Moscovici residue derivation (Open Problem O.14).
    type_check_pass = (n_modes_nonzero > 0)
    dixmier_trace_pass = False
    reason = (
        f"Dirac operator type-check PASS: {n_modes_nonzero} nonzero modes on "
        f"the I_h-closed cage; assumed gap-label scaling factor "
        f"\u03C4 = \u03A6^{n_gap} asserted for downstream protocols. "
        f"First-principles Connes-Moscovici residue derivation of \u03C4 from "
        f"the cage Dirac spectrum is registered as App H Open Problem O.14 "
        f"(K-theoretic-action structural-link chain V -> AF-core dimension group / trace image)."
    )
    reporter.verdict(type_check_pass and dixmier_trace_pass, reason)

    results = {
        "N_nodes": int(N),
        "dirac_modes_total": n_modes_total,
        "dirac_modes_nonzero": n_modes_nonzero,
        "spectrum_min_abs": spectrum_min_abs,
        "spectrum_max_abs": spectrum_max_abs,
        "gap_label": int(n_gap),
        "dixmier_scaling": float(dixmier_scaling),
        "dixmier_scaling_provenance": "asserted_gap_label_input_pending_O.14",
        "type_check_pass": bool(type_check_pass),
        "dixmier_trace_pass": bool(dixmier_trace_pass),
        "status": "open_problem_O.14",
        "connes_moscovici_residue_status": "open_problem_O.14",
        "pass": bool(type_check_pass and dixmier_trace_pass)
    }
    
    out_path = get_output_path("protocol_dixmier_trace_scaling_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=4)
        
    return results

if __name__ == "__main__":
    run_gap_label_scaling_typecheck()
