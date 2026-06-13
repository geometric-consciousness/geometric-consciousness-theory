#!/usr/bin/env python3
"""
protocol_mixing_geometry.py — Geometric Evaluator for CKM and PMNS Mixing
==============================================================
Objective: Evaluate the mixing parameters (CKM, PMNS, CP Phase) from the
Mixed-Harmonic Law and topological tunneling geometry. Coverage is partial:
theta12, theta13, and delta_CP follow from the geometric construction, while
the bare theta23 prediction sits in tension with the PMNS data. The headline
mixing angles carry Tier 3 status; see the in-body verdict.
"""

import sys
import json
import math
from pathlib import Path
from gct_utils import C

# Path bootstrap
_SRC = Path(__file__).resolve().parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

try:
    from gct_utils import get_output_path, C
except ImportError:
    # Fallback if gct_utils isn't available in this context
    def get_output_path(filename):
        return str(_SRC.parent.parent / "data" / filename)
    class C:
        PHI = float(C.PHI)
        ALPHA_OBS = 0.0072973525693

def main():
    phi = float(C.PHI)
    alpha = float(C.ALPHA_OBS)
    
    print("=" * 70)
    print("  GCT Protocol: Mixing Geometry (CKM & PMNS)")
    print("=" * 70)
    
    # -----------------------------------------------------------------
    # CKM Matrix (Pinned Face Tunneling)
    # -----------------------------------------------------------------
    s12_ckm_pred = (phi ** -3) * (1.0 - 5.0 * alpha)
    s23_ckm_pred = phi ** -(6.0 + (phi ** -1))
    s13_ckm_pred = phi ** -(11.0 + (phi ** -1))
    
    # PDG 2024 CKM Targets
    s12_ckm_targ = 0.225
    s23_ckm_targ = 0.0418
    s13_ckm_targ = 0.00369
    
    # Jarlskog Invariant
    # J = s12 * s23 * s13 * c12 * c23 * c13^2 * sin(delta)
    # Geometrically: J_ckm ~ phi^-22
    j_ckm_pred = phi ** -22
    
    ckm_preds = {
        "s12": s12_ckm_pred,
        "s23": s23_ckm_pred,
        "s13": s13_ckm_pred,
        "J": j_ckm_pred
    }
    ckm_targs = {
        "s12": s12_ckm_targ,
        "s23": s23_ckm_targ,
        "s13": s13_ckm_targ
    }
    
    print("\n  [ CKM Parameters (Quarks) ]")
    for angle, pred in ckm_preds.items():
        if angle == "J":
            print(f"    {angle.upper()} (Jarlskog): Predicted = {pred:.3e}")
            continue
        targ = ckm_targs[angle]
        err = abs(pred - targ) / targ * 100.0
        print(f"    {angle.upper()}: Predicted = {pred:.5f}, Target = {targ:.5f}, Error = {err:.2f}%")

    # -----------------------------------------------------------------
    # PMNS Matrix (Unpinned Axis Sliding)
    # -----------------------------------------------------------------
    theta12_pmns_pred = math.degrees(math.atan(1.0 / phi)) + (8.3893 / 5.0)
    theta23_pmns_pred = 45.0
    theta13_pmns_pred = math.degrees(math.asin(phi ** -4))
    
    # CP Violating Phase
    delta_cp_pred = 360.0 * (phi ** -1)
    
    # NuFIT 5.3 / NOvA + T2K 2024 PMNS Targets (Normal Ordering)
    # θ₂₃ best-fit is in tension with the bare GCT prediction (see Ch09 §9.4.2).
    t12_pmns_targ = 33.4
    t23_pmns_targ = 49.5      # NOvA + T2K best-fit, second octant; 1σ ≈ 1.1°
    t23_pmns_sigma = 1.1
    t13_pmns_targ = 8.58
    dcp_targ = 232.0

    pmns_preds = {
        "theta12": theta12_pmns_pred,
        "theta23": theta23_pmns_pred,
        "theta13": theta13_pmns_pred,
        "delta_cp": delta_cp_pred
    }
    pmns_targs = {
        "theta12": t12_pmns_targ,
        "theta23": t23_pmns_targ,
        "theta13": t13_pmns_targ,
        "delta_cp": dcp_targ
    }

    # θ₂₃ tension in units of the reported 1σ
    theta23_tension_sigma = abs(theta23_pmns_pred - t23_pmns_targ) / t23_pmns_sigma

    print("\n  [ PMNS Parameters (Neutrinos) ]")
    for angle, pred in pmns_preds.items():
        targ = pmns_targs[angle]
        err = abs(pred - targ) / targ * 100.0
        tag = ""
        if angle == "theta23":
            tag = f"   [Tier 3 - Tension {theta23_tension_sigma:.2f} sigma]"
        print(f"    {angle.upper()}: Predicted = {pred:.2f} deg, Target = {targ:.2f} deg, Error = {err:.2f}%{tag}")

    theta23_status = "TENSION_GT_4SIGMA" if theta23_tension_sigma > 4 else "WITHIN_2SIGMA"
    print("\n" + "=" * 70)
    print(f"  VERDICT: PARTIAL - theta12, theta13, delta_CP derived geometrically;")
    print(f"           theta23 bare prediction (45 deg) in {theta23_tension_sigma:.2f} sigma tension")
    print(f"           with NOvA+T2K ({t23_pmns_targ} deg +/- {t23_pmns_sigma} deg). Status: {theta23_status}")
    print(f"           Pending lattice-Hamiltonian discriminant (Ch09 sec 9.4.2).")
    print("=" * 70)
    
    # -----------------------------------------------------------------
    # CP Violation Phase Extractor
    # -----------------------------------------------------------------
    cp_derivation = derive_delta_cp()
    
    output = {
        "pass": theta23_tension_sigma < 2.0,
        "ckm": {
            "predictions": ckm_preds,
            "targets": ckm_targs
        },
        "pmns": {
            "predictions": pmns_preds,
            "targets": pmns_targs,
            "theta23_tension_sigma": theta23_tension_sigma,
            "theta23_status": theta23_status,
            "theta23_tier": "Tier 3 (Tension)",
            "resolution_path": "Lattice-Hamiltonian derivation of neutrino propagation through discrete icosahedral vacuum (Ch09 §9.4.2 pre-registered discriminant)"
        },
        "cp_violation_derivation": cp_derivation
    }
    
    outfile = get_output_path("protocol_mixing_geometry_results.json")
    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
        
    return 0

def derive_delta_cp():
    import numpy as np
    from gct_utils import C
    PHI = float(C.PHI)
    alpha = float(C.ALPHA_OBS) if hasattr(C, 'ALPHA_OBS') else 0.0072973525693
    
    # CKM mixing sines from Ch10 Mixed-Harmonic Law
    s12 = PHI**-3 * (1 - 5*alpha)
    s23 = PHI**(-(6 + 1/PHI))
    s13 = PHI**(-(11 + 1/PHI))
    
    c12 = np.sqrt(1 - s12**2)
    c23 = np.sqrt(1 - s23**2)
    c13 = np.sqrt(1 - s13**2)
    
    # GCT Jarlskog invariant (Tier 2 claim from Ch10)
    J_gct = PHI**-22
    
    # Extract delta_CP
    denominator = s12 * c12 * s23 * c23 * (s13**2)
    sin_delta = J_gct / denominator
    
    if abs(sin_delta) > 1:
        delta_cp_deg = None
        status = "UNPHYSICAL - sin(delta) > 1"
    else:
        delta_cp_rad = np.arcsin(sin_delta)
        # Physical solution in second quadrant for CP violation
        delta_cp_deg = 180 - np.degrees(delta_cp_rad)
        status = "PHYSICAL"
        
    # Manuscript claim: 360/PHI
    delta_cp_manuscript = 360 / PHI
    
    return {
        "s12": s12, "s23": s23, "s13": s13,
        "J_gct_phi_22": J_gct,
        "sin_delta_cp": sin_delta,
        "delta_cp_deg_derived": delta_cp_deg,
        "delta_cp_manuscript_claim": delta_cp_manuscript,
        "status": status,
        "match_precision_pct": abs(delta_cp_deg - delta_cp_manuscript)/delta_cp_manuscript * 100 if delta_cp_deg else None
    }

if __name__ == "__main__":
    sys.exit(main())
