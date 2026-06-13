#!/usr/bin/env python3
"""
protocol_stiffness_invariant.py
===============================
Compute G_par and G_perp eigenvalues from the canonical
AKN projection matrices to verify the phi^-2 stiffness ratio tree-level foundation.
"""

import numpy as np
import json
import os
from gct_utils import C
from gct_projections import get_m_parallel_unnormalized, get_m_perp_unnormalized

def get_output_path(filename):
    out_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    return os.path.join(out_dir, filename)

def main():
    phi = float(C.PHI)

    # Use the same unnormalized AKN projection matrices that define the
    # shipped stiffness-ratio audit JSON.
    M_para_raw = get_m_parallel_unnormalized()
    M_perp_raw = get_m_perp_unnormalized()

    G_para = M_para_raw @ M_para_raw.T
    G_perp = M_perp_raw @ M_perp_raw.T

    eig_para = np.linalg.eigvalsh(G_para)
    eig_perp = np.linalg.eigvalsh(G_perp)

    val_g_par = np.mean(eig_para)
    val_g_perp = np.mean(eig_perp)
    ratio = val_g_perp / val_g_par
    target = phi**-2
    pass_check = bool(abs(ratio - target) <= 1e-12)

    results = {
        "pass": pass_check,
        "eig_para_mean": float(val_g_par),
        "eig_perp_mean": float(val_g_perp),
        "eigenvalue_ratio": float(ratio),
        "target_eta_0": float(target),
        "stiffness_ratio": float(ratio)
    }

    out_path = get_output_path("protocol_stiffness_invariant_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=4)
    print(f"Results written to {out_path}")

if __name__ == "__main__":
    main()
