import numpy as np
import json
import os
from gct_utils import C, get_output_path

def run_protocol():
    """
    Diagnostic extraction of the coefficient that would map the bare
    3443 ppm alpha residual onto a one-loop boundary-vacuum-polarization form.
    The CODATA value is an empirical comparison target, not a derivation input.
    """
    print("Executing: protocol_cft_boundary.py")

    # 1. Constants
    # Bare alpha from Tier 2 derivation: 360 / phi^2
    alpha_bare_inv = 360.0 / (C.PHI**2)
    alpha_bare = 1.0 / alpha_bare_inv
    
    # Verification target (CODATA): empirical alpha^-1 used only to measure
    # the residual and back-solve the diagnostic C_ico coefficient.
    from gct_utils import resolve_a3
    alpha_obs, alpha_obs_inv = resolve_a3(C)
    
    # 2. Fractional shift required
    # delta_alpha / alpha_obs
    delta_alpha_over_alpha = (alpha_bare - alpha_obs) / alpha_obs
    
    # 3. Logarithmic span from me to Mp
    # Tier 2 GCT: me / Mp = phi^-107
    # ln(Mp^2 / me^2) = -2 * ln(me / Mp) = -2 * ln(phi^-107) = 214 * ln(phi)
    log_span = 214.0 * np.log(float(C.PHI))
    
    # 4. Diagnostic extraction of C_ico (topological winding coefficient).
    # Equation: delta_alpha / alpha = (alpha_obs / (3 * pi)) * C_ico * ln(Mp^2 / me^2)
    # C_ico = (delta_alpha / alpha) * (3 * pi) / (alpha_obs * log_span)
    # Tier 3 diagnostic status: this extraction is not used downstream as a
    # free GCT input; O.19 remains the first-principles magnitude task.
    
    c_ico = (delta_alpha_over_alpha * 3.0 * np.pi) / (alpha_obs * log_span)
    
    results = {
        "alpha_bare_inv": float(alpha_bare_inv),
        "alpha_obs_inv": float(alpha_obs_inv),
        "residual_ppm": float(delta_alpha_over_alpha * 1e6),
        "log_span": float(log_span),
        "C_ico_extracted": float(c_ico),
        # The former literal pass=True is retired. C_ico is
        # back-solved so that the bare alpha reproduces CODATA; the agreement
        # is a fit by construction and tests nothing.
        "verdict": "FIT_BY_CONSTRUCTION_DIAGNOSTIC_EXTRACTION",
        "pass": False,
        "classification": (
            "Verification target (CODATA) plus diagnostic back-solved "
            "coefficient; not a core parameter anchor"
        )
    }

    print(f"  Residual Gap: {results['residual_ppm']:.4f} ppm")
    print(f"  Extracted C_ico: {results['C_ico_extracted']:.10f} (back-solved from CODATA; fit by construction)")
    
    # Save results
    output_path = get_output_path("protocol_cft_boundary_results.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=4)
        
    print(f"  Results saved to {output_path}")
    return True

if __name__ == "__main__":
    run_protocol()
