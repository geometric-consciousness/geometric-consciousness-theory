"""
verify_ckm.py - Independent recomputation of the CKM angle formulas

App PSC Sec PSC.4 rows 1-3:
    s12 = phi^-3 (1 - 5 alpha)                    -> 0.2275 vs 0.2250 (1.09%)
    s23 = phi^-(6 + phi^-1)                       -> 0.0414 vs 0.0418 (0.98%)
    s13 = phi^-(11 + phi^-1)                      -> 0.00373 vs 0.003732 (0.01%)

The executable precision gate is 0.5%; misses above that gate are reported
as TENSION rather than PASS.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import CODATA, MATH, pct_error
from report import make_result, write_result, print_summary


def main():
    phi = MATH.PHI
    alpha = CODATA.ALPHA

    s12 = (phi ** -3) * (1.0 - 5.0 * alpha)
    s23 = phi ** -(6 + phi ** -1)
    s13 = phi ** -(11 + phi ** -1)

    targets = {"s12": CODATA.S12_CKM, "s23": CODATA.S23_CKM, "s13": CODATA.S13_CKM}
    preds = {"s12": s12, "s23": s23, "s13": s13}
    app_psc_pred = {"s12": 0.2275, "s23": 0.0414, "s13": 0.00373}
    app_psc_pct = {"s12": 1.09, "s23": 0.98, "s13": 0.0076}
    formulas = {
        "s12": "s12 = phi^-3 * (1 - 5 alpha)",
        "s23": "s23 = phi^-(6 + phi^-1)",
        "s13": "s13 = phi^-(11 + phi^-1)",
    }

    # Tier dispositions per Ch10 §10.5.1 / App PSC §PSC.4:
    # s_12 has a Tier 3 bare φ^-3 identification plus a Tier 3
    # lepton-to-hadron transfer correction; s_23 and s_13 remain
    # Tier 3 ansatze pending QLQCD-1L.
    tier_per_angle = {
        "s12": "Tier 3 bare identification (raw-frame phi^-3) + Tier 3 lepton-to-hadron transfer correction pending O.5 + Tier 4 as evidence that phi explains the value (constant control test v3 NEGATIVE-FRAGILE; App PSC §PSC.9.6)",
        "s23": "Tier 3 (ansatz; the standalone K-theoretic gap-label route is ruled out, App TPR §TP-F; the residual bundles with O.5) + Tier 4 as evidence that phi explains the value (constant control test v3 NEGATIVE-FRAGILE; App PSC §PSC.9.6)",
        "s13": "Tier 3 (ansatz; the standalone K-theoretic gap-label route is ruled out, App TPR §TP-F; the residual bundles with O.5) + Tier 4 as evidence that phi explains the value (constant control test v3 NEGATIVE-FRAGILE; App PSC §PSC.9.6)",
    }
    results = []
    for k in ("s12", "s23", "s13"):
        pct = pct_error(preds[k], targets[k])
        res = make_result(
            name=f"ckm_{k}",
            app_psc_label=f"CKM {k}",
            formula=formulas[k],
            predicted=preds[k],
            observed=targets[k],
            unit="(dimensionless)",
            app_psc_predicted=app_psc_pred[k],
            app_psc_precision_str=f"{app_psc_pct[k]:.2f}%",
            app_psc_precision_ppm=app_psc_pct[k] * 1e4,
            tier=tier_per_angle[k],
            status="PASS" if pct < 0.5 else "TENSION",
            tolerance_ppm=5000.0,
            extra={"percent_error": pct, "precision_gate_percent": 0.5},
        )
        print_summary(res)
        write_result(res)
        results.append(res)
    return results


if __name__ == "__main__":
    main()
