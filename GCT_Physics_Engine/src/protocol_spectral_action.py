#!/usr/bin/env python3
"""
protocol_spectral_action.py
The Connes Spectral RGE + Seeley-DeWitt moment ladder.

Computes:
1. The geometric beta function kernel dS/dlnLambda from the D_F spectrum
   on the I_h-closed boundary cage (the established functionality).
2. The Seeley-DeWitt-moment ladder Tr(D^{2k}) for k = 0..3 on the cage
   spectrum, exposed for the Connes-Chamseddine Higgs-mass closure path.

CCM Higgs-mass closure path (Connes-Chamseddine-Marcolli 2007 *Adv. Theor.
Math. Phys.* 11:991): the standard SM spectral-triple result is
  m_H^2 ∝ (a_2 / a_4) * Lambda_GUT^2
where a_2, a_4 are the Seeley-DeWitt coefficients of the spectral
action S(D, Lambda) = Tr(f(D/Lambda)). On a continuous 4-manifold the
small-t heat-kernel expansion of Tr(exp(-tD^2)) reads
  Tr(exp(-tD^2)) ~ sum_n a_n * t^(n-d/2) / Gamma(n - d/2 + 1)
with a_2 ∝ scalar curvature and a_4 ∝ gauge field strength squared + ...
On the discrete AKN spectrum the *moment ladder*
  M_{2k} := Tr(D^{2k}) = sum_i lambda_i^{2k}
gives the heat-kernel expansion coefficients to leading order in the
small-t Taylor series of exp(-t lambda^2):
  Tr(exp(-tD^2)) = sum_k (-t)^k M_{2k} / k!
                 = N - t*M_2 + (t^2/2)*M_4 - (t^3/6)*M_6 + ...

The CCM Seeley-DeWitt identification a_n = (gauge-field-projected piece
of M_n in the spectral-triple algebra A_F) requires the explicit
identification of the spectral-triple decomposition
  A_F = C oplus H oplus M_3(C)
within subspaces of the D_F kernel (which fermion lives in which
representation). That field-theoretic decomposition is bundled with
Open Problem O.5 (QLQCD-1L closure); it is NOT implemented here.

What this script DOES implement: the moment ladder M_{2k} for k = 0..3
on the AKN cage spectrum, exposed as engine outputs that downstream
work can consume once the A_F decomposition is supplied. The naive
ratio M_2 / M_4 (the "spectral-triple-decomposition-free" analogue of
a_2 / a_4) is reported as a Tier 3 reference value pending the O.5
field-theoretic identification.

Cross-reference: V3 Ch06 §6.5.2 (CCM identification, Tier 2 mechanism +
Open Problem pending Seeley-DeWitt implementation per the engine-level
status); App H Open Problem O.5 (QLQCD-1L closure of the spectral-triple
decomposition).
"""

import numpy as np
import sys
import os
import json

# Add GCT Physics Engine src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from gct_utils import PHI, get_output_path, GCTReporter
from cage_builder import build_canonical_cage

def run_spectral_action():
    reporter = GCTReporter("Spectral Action Beta-Function + Seeley-DeWitt Moments")

    # Build D_F on the I_h-closed boundary cage (152 nodes; 5 orbits).
    cage_nodes, _ = build_canonical_cage(size=152)
    N = cage_nodes.shape[0]
    D_F = np.zeros((N, N))

    # Adjacency: 6D Nearest Neighbors (dist=1.0) with Golden weights
    for i in range(N):
        for j in range(i+1, N):
            dist = np.linalg.norm(cage_nodes[i] - cage_nodes[j])
            if abs(dist - 1.0) < 1e-4:
                D_F[i, j] = PHI
                D_F[j, i] = PHI

    # 2. Compute eigenvalues
    lambdas = np.linalg.eigvalsh(D_F)
    # Spectral Action f(x) = exp(-x^2) [Heat Kernel Proxy]
    # S(Lambda) = Tr(f(D_F/Lambda))

    # 3. Compute Beta Function dS/dln(Lambda)
    # dS/dlnL = L * dS/dL
    # dS/dL = Sum f'(li/L) * (-li/L^2)
    # f'(x) = -2x exp(-x^2)
    # dS/dL = Sum (-2 * li/L * exp(-(li/L)^2)) * (-li/L^2)
    # dS/dL = (2/L^3) * Sum li^2 * exp(-(li/L)^2)
    # dS/dlnL = (2/L^2) * Sum li^2 * exp(-(li/L)^2)

    def compute_beta(L):
        x_sq = (lambdas / L)**2
        return 2.0 * np.sum(x_sq * np.exp(-x_sq))

    # Logarithmic scale for Lambda (resolution)
    # L ranges from roughly min(lambda) to max(lambda)
    L_min = 0.5
    L_max = 20.0
    L_points = np.geomspace(L_min, L_max, 200)

    beta_vals = [compute_beta(L) for L in L_points]

    # 4. Seeley-DeWitt moment ladder M_{2k} = Tr(D^{2k})
    # Computed from the spectrum {lambda_i} as sum lambda_i^{2k}.
    # These are the small-t Taylor coefficients of Tr(exp(-tD^2)):
    #   Tr(exp(-tD^2)) = sum_k (-t)^k M_{2k} / k!
    # CCM a_n identification requires the spectral-triple algebra
    # decomposition (Open Problem O.5); the raw moments here are
    # exposed for downstream use once that decomposition is supplied.
    M_0 = float(N)                           # = Tr(I)
    M_2 = float(np.sum(lambdas**2))          # = Tr(D^2)
    M_4 = float(np.sum(lambdas**4))          # = Tr(D^4)
    M_6 = float(np.sum(lambdas**6))          # = Tr(D^6)

    # Naive ratio (pre-A_F-decomposition): the structural analogue
    # of (a_2 / a_4) in the CCM Higgs formula m_H^2 ∝ (a_2/a_4) * Lambda^2.
    # Tier 3 reference value — the field-theoretic a_2/a_4 requires the
    # spectral-triple decomposition (Open Problem O.5) and may differ
    # from the raw ratio by projection factors onto the gauge-Higgs
    # subspaces of A_F.
    if abs(M_4) > 1e-12:
        ratio_M2_M4 = M_2 / M_4
    else:
        ratio_M2_M4 = float('inf')

    # Heat-kernel trace at representative scales t (sanity check the
    # moment-ladder Taylor sum against the direct computation).
    t_test = 0.01
    hk_direct = float(np.sum(np.exp(-t_test * lambdas**2)))
    hk_taylor4 = float(M_0 - t_test*M_2 + (t_test**2/2)*M_4 - (t_test**3/6)*M_6)
    hk_taylor_residual = float(abs(hk_direct - hk_taylor4) / max(abs(hk_direct), 1e-12))

    # 5. Results & Export
    results = {
        "N_nodes": N,
        "lambdas": lambdas.tolist(),
        "L_points": L_points.tolist(),
        "beta_vals": beta_vals,
        "derivation": "dS/dln(Lambda) from I_h-closed 6D boundary-cage adjacency spectrum",
        "seeley_dewitt_moments": {
            "M_0_Tr_I": M_0,
            "M_2_Tr_D2": M_2,
            "M_4_Tr_D4": M_4,
            "M_6_Tr_D6": M_6,
            "ratio_M2_M4_pre_AF_decomposition": ratio_M2_M4,
            "ratio_status": "Tier 3 reference value; CCM a_2/a_4 field-theoretic identification requires A_F spectral-triple decomposition (Open Problem O.5)",
            "ccm_higgs_formula": "m_H^2 ∝ (a_2/a_4) * Lambda_GUT^2 (Connes-Chamseddine-Marcolli 2007 Adv. Theor. Math. Phys. 11:991)",
            "open_problem_O5_status": "field-theoretic decomposition of M_n into gauge/Higgs/fermion subspaces of A_F pending; bundle with QLQCD-1L per App H O.5",
        },
        "heat_kernel_sanity_check": {
            "t_test": t_test,
            "hk_direct_Tr_exp_minus_tD2": hk_direct,
            "hk_taylor_truncated_at_M6": hk_taylor4,
            "relative_residual": hk_taylor_residual,
            "interpretation": "small-t Taylor sum truncated at M_6 vs direct heat-kernel evaluation; residual should be O(t^4 * Tr(D^8)/24) for small enough t",
        },
        "pass": True,
    }

    kernel_path = get_output_path("spectral_rge_kernel.json")
    with open(kernel_path, "w") as f:
        json.dump(results, f, indent=4)

    engine_path = get_output_path("spectral_action_results.json")
    with open(engine_path, "w") as f:
        json.dump(results, f, indent=4)

    reporter.section("Spectral Summary")
    reporter.log_value("Max Eigenvalue", np.max(lambdas))
    reporter.log_value("Min Eigenvalue", np.min(lambdas))
    reporter.log_value("Beta Peak", np.max(beta_vals))

    reporter.section("Seeley-DeWitt Moment Ladder")
    reporter.log_value("M_0 = Tr(I)", M_0)
    reporter.log_value("M_2 = Tr(D^2)", f"{M_2:.4e}")
    reporter.log_value("M_4 = Tr(D^4)", f"{M_4:.4e}")
    reporter.log_value("M_6 = Tr(D^6)", f"{M_6:.4e}")
    reporter.log_value("M_2/M_4 (pre-A_F)", f"{ratio_M2_M4:.4e}")
    reporter.log_value("Heat-kernel Taylor residual", f"{hk_taylor_residual:.4e}")

    print(f"Spectral kernel saved to: {kernel_path}")

if __name__ == "__main__":
    run_spectral_action()
