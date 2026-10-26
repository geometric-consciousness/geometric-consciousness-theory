#!/usr/bin/env python3
"""
protocol_mixing_geometry.py — Geometric Evaluator for CKM and PMNS Mixing
==============================================================
Objective: Evaluate the mixing parameters (CKM, PMNS, CP Phase) from the
Mixed-Harmonic Law and topological tunneling geometry. Coverage is partial:
theta12, theta13, and delta_CP are evaluated from the Tier 3 geometric ansaetze.
The bare theta23 = 45 deg lies inside the NuFIT 6.0 3-sigma ranges with and
without SK atmospheric data (octant unresolved); the registered tension of this
protocol is the CKM s12 row (corrected Cabibbo formula, ~3.6 sigma against PDG
2024). The headline mixing angles carry Tier 3 status; see the in-body verdict.
Expected outcome re-registered (config/expected_outcomes.json; CHANGELOG
v1.3.0): after the theta23 comparator was corrected to NuFIT 6.0, theta23 is
no longer a tension, and the registered tension is carried by CKM s12 (3.60
sigma). The closure class (tension) is unchanged.
"""

import sys
import json
import math
from pathlib import Path
from gct_utils import C, resolve_a3

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
        ALPHA_OBS = 1.0 / 137.035999177

def main():
    phi = float(C.PHI)
    alpha, _ = resolve_a3(C)
    
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
    s12_ckm_targ = float(C.S12_CKM)   # PDG 2024 eq. 12.28, from the SSOT
    s12_ckm_sigma = 0.00068           # PDG 2024 global-fit lambda (s12) uncertainty (eq. 12.28)
    s23_ckm_targ = float(C.S23_CKM)
    s13_ckm_targ = float(C.S13_CKM)
    
    # Jarlskog Invariant
    # J = s12 * s23 * s13 * c12 * c23 * c13^2 * sin(delta)
    # Tier 3 ansatz (O.7 open): J_ckm ~ phi^-22
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
            print(f"    {angle.upper()} (Jarlskog): Ansatz value = {pred:.3e}")
            continue
        targ = ckm_targs[angle]
        err = abs(pred - targ) / targ * 100.0
        print(f"    {angle.upper()}: Ansatz value = {pred:.5f}, Target = {targ:.5f}, Error = {err:.2f}%")

    # -----------------------------------------------------------------
    # PMNS Matrix (Unpinned Axis Sliding)
    # -----------------------------------------------------------------
    theta12_pmns_pred = math.degrees(math.atan(1.0 / phi)) + (8.3893 / 5.0)
    theta23_pmns_pred = 45.0
    theta13_pmns_pred = math.degrees(math.asin(phi ** -4))
    
    # CP Violating Phase
    delta_cp_pred = 360.0 * (phi ** -1)
    
    # NuFIT 6.0 PMNS targets (Esteban et al., JHEP 12 (2024) 216, arXiv:2410.05380,
    # Table 1, normal ordering, IC24 with SK atmospheric data).
    t12_pmns_targ = 33.68
    t23_pmns_targ = 43.3      # with SK; without SK the best fit is 48.5 deg
    t13_pmns_targ = 8.56
    dcp_targ = 212.0
    # Delta chi^2 at theta23 = 45 deg, from the NuFIT 6.0 one-dimensional
    # sin^2(theta23) projections (v60.release-TByes-NO / -TBoff-NO), measured
    # from the global minimum. A two-octant likelihood: no Gaussian sigma.
    t23_dchi2_45_with_sk = 2.02
    t23_dchi2_45_without_sk = 4.20
    t23_3sigma_with_sk = (41.3, 49.9)
    t23_3sigma_without_sk = (41.0, 50.5)

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

    # θ₂₃: 45 deg against the NuFIT 6.0 3-sigma ranges and Delta chi^2 values.
    theta23_inside_3sigma = (
        t23_3sigma_with_sk[0] <= theta23_pmns_pred <= t23_3sigma_with_sk[1]
        and t23_3sigma_without_sk[0] <= theta23_pmns_pred <= t23_3sigma_without_sk[1]
    )
    theta23_equiv_sigma_with_sk = math.sqrt(t23_dchi2_45_with_sk)
    theta23_equiv_sigma_without_sk = math.sqrt(t23_dchi2_45_without_sk)

    # CKM s12 (corrected Cabibbo formula) against PDG 2024: the protocol's tension row.
    s12_tension_sigma = abs(s12_ckm_pred - s12_ckm_targ) / s12_ckm_sigma
    s12_status = "TENSION" if s12_tension_sigma >= 3.0 else "WITHIN_3SIGMA"

    print("\n  [ PMNS Parameters (Neutrinos) ]")
    for angle, pred in pmns_preds.items():
        targ = pmns_targs[angle]
        err = abs(pred - targ) / targ * 100.0
        tag = ""
        if angle == "theta23":
            tag = (f"   [Tier 3 - inside NuFIT 6.0 3-sigma ranges; Delta chi2(45) = "
                   f"{t23_dchi2_45_with_sk} with SK / {t23_dchi2_45_without_sk} without]")
        print(f"    {angle.upper()}: Ansatz value = {pred:.2f} deg, Target = {targ:.2f} deg, Error = {err:.2f}%{tag}")

    theta23_status = "WITHIN_3SIGMA_OCTANT_UNRESOLVED" if theta23_inside_3sigma else "OUTSIDE_3SIGMA"
    print("\n" + "=" * 70)
    print(f"  VERDICT: TENSION - CKM s12 (corrected Cabibbo formula) at {s12_tension_sigma:.2f} sigma;")
    print(f"           theta12, theta13, delta_CP are Tier 3 ansatz values;")
    print(f"           theta23 = 45 deg is inside the NuFIT 6.0 3-sigma ranges (octant unresolved).")
    print(f"           Status: {theta23_status}. DUNE / Hyper-K octant data are the decisive test.")
    print("=" * 70)
    
    # -----------------------------------------------------------------
    # CP Violation Phase Extractor
    # -----------------------------------------------------------------
    cp_derivation = derive_delta_cp()
    
    output = {
        "pass": s12_status != "TENSION" and theta23_inside_3sigma,
        "ckm": {
            "predictions": ckm_preds,
            "targets": ckm_targs,
            "s12_pdg_sigma": s12_ckm_sigma,
            "s12_tension_sigma": s12_tension_sigma,
            "expected_outcome_note": "Expected outcome re-registered after the theta23 comparator correction; the registered tension is now carried by CKM s12.",
            "s12_status": s12_status
        },
        "pmns": {
            "predictions": pmns_preds,
            "targets": pmns_targs,
            "targets_source": "NuFIT 6.0 (arXiv:2410.05380) Table 1, normal ordering, IC24 with SK atmospheric data",
            "theta23_best_fit_without_sk_deg": 48.5,
            "theta23_3sigma_with_sk_deg": list(t23_3sigma_with_sk),
            "theta23_3sigma_without_sk_deg": list(t23_3sigma_without_sk),
            "theta23_dchi2_at_45_with_sk": t23_dchi2_45_with_sk,
            "theta23_dchi2_at_45_without_sk": t23_dchi2_45_without_sk,
            "theta23_equiv_sigma_with_sk": theta23_equiv_sigma_with_sk,
            "theta23_equiv_sigma_without_sk": theta23_equiv_sigma_without_sk,
            "theta23_inside_both_3sigma_ranges": theta23_inside_3sigma,
            "theta23_status": theta23_status,
            "theta23_tier": "Tier 3 (octant unresolved)",
            "theta23_note": "The earlier 4.09-sigma figure, a one-octant Gaussian on 49.5 +/- 1.1 deg, is withdrawn.",
            "resolution_path": "DUNE / Hyper-K octant data; lattice-Hamiltonian derivation of neutrino propagation through discrete icosahedral vacuum (Ch09 §9.4.2 pre-registered discriminant)"
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
    alpha, _ = resolve_a3(C)
    
    # CKM mixing sines from Ch10 Mixed-Harmonic Law
    s12 = PHI**-3 * (1 - 5*alpha)
    s23 = PHI**(-(6 + 1/PHI))
    s13 = PHI**(-(11 + 1/PHI))
    
    c12 = np.sqrt(1 - s12**2)
    c23 = np.sqrt(1 - s23**2)
    c13 = np.sqrt(1 - s13**2)
    
    # GCT Jarlskog candidate J ~ phi^-22 (Tier 3 ansatz; Open Problem O.7)
    J_gct = PHI**-22
    
    # Extract delta_CP
    denominator = s12 * c12 * s23 * c23 * s13 * (c13**2)
    sin_delta = J_gct / denominator
    
    if abs(sin_delta) > 1:
        delta_cp_deg = None
        status = "UNPHYSICAL - sin(delta) > 1"
    else:
        delta_cp_rad = np.arcsin(sin_delta)
        # sin(delta) fixes delta only up to delta <-> 180 - delta; the
        # second-quadrant branch is reported. This is a CKM phase from the
        # Tier 3 J ansatz and is not compared with the PMNS delta_CP.
        delta_cp_deg = float(180 - np.degrees(delta_cp_rad))
        status = "PHYSICAL"
        
    # PMNS delta_CP ansatz 360/PHI (a different matrix; not a comparator here)
    delta_cp_pmns_ansatz = 360 / PHI
    
    return {
        "s12": s12, "s23": s23, "s13": s13,
        "J_gct_phi_22": J_gct,
        "sin_delta_cp": sin_delta,
        "delta_cp_deg_derived": delta_cp_deg,
        "pmns_delta_cp_ansatz_deg_not_comparable": delta_cp_pmns_ansatz,
        "status": status,
        "note": "CKM phase from the Tier 3 J ansatz (phi^-22; O.7 open); not comparable with the PMNS delta_CP = 360/phi, so no match precision is reported. A CKM comparator would be the PDG unitarity-triangle angle gamma.",
    }

if __name__ == "__main__":
    sys.exit(main())
