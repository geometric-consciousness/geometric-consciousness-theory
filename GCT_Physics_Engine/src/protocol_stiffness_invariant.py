#!/usr/bin/env python3
"""
protocol_stiffness_invariant.py
===============================
Compute the G_par and G_perp Gram eigenvalues of the unnormalized (raw-frame)
AKN projection matrices and check that their mean ratio is phi^-2.

Scope: this is raw-frame coordinate arithmetic, not a stiffness derivation.
The ratio depends on the frame (it scales as s^2 under an internal rescaling,
and the canonical isometric projectors give 1), so it does not fix
K_perp/K_parallel (App DPS §DPS.2-§DPS.3). Only the integer D = 18 is Tier 2
(H3 invariant-degree sum); the stiffness map K_perp/K_parallel = phi^-18 is the
Tier 3 P3b hypothesis (O.15(b)), registered outside the count (Parameter
Ledger §0.1). The JSON key names are kept for compatibility.
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
        "stiffness_ratio": float(ratio),
        "scope": "raw-frame Gram-eigenvalue identity (frame-dependent; canonical projectors give 1); not a stiffness derivation. D = 18 Tier 2; phi^-18 map Tier 3 P3b (O.15(b))."
    }

    out_path = get_output_path("protocol_stiffness_invariant_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=4)
    print(f"Results written to {out_path}")

if __name__ == "__main__":
    main()
