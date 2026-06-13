"""
verify_pmns.py - Independent re-derivation of PMNS angles

App R Sec R.4 rows 4-7:
    theta_12 = arctan(1/phi) + (theta_13/5)           -> 33.40 deg vs 33.40 deg (0.01%)
    theta_23 = 45 deg                                  -> 45.00 deg vs 49.5 deg (>4 sigma tension)
    theta_13 = arcsin(phi^-4)                          -> 8.39 deg vs 8.58 deg (2.22%)
    delta_CP = 2 pi * phi^-1 (in degrees: 360/phi)     -> 222.5 deg vs 232.0 deg (4.10%)
"""

import sys
import math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import CODATA, MATH, pct_error
from report import make_result, write_result, print_summary


def main():
    phi = MATH.PHI

    theta13_rad = math.asin(phi ** -4)
    theta13_deg = math.degrees(theta13_rad)

    theta12_deg = math.degrees(math.atan(1.0 / phi)) + theta13_deg / 5.0
    theta23_deg = 45.0
    delta_cp_deg = 360.0 * (phi ** -1)

    targets = {
        "theta12": CODATA.THETA12_DEG,
        "theta23": CODATA.THETA23_DEG,
        "theta13": CODATA.THETA13_DEG,
        "delta_cp": CODATA.DELTA_CP_DEG,
    }
    preds = {
        "theta12": theta12_deg,
        "theta23": theta23_deg,
        "theta13": theta13_deg,
        "delta_cp": delta_cp_deg,
    }
    app_r_pred = {
        "theta12": 33.40, "theta23": 45.00, "theta13": 8.39, "delta_cp": 222.5,
    }
    app_r_str = {
        "theta12": "0.01%",
        "theta23": "4.5 deg (>4 sigma tension)",
        "theta13": "2.22%",
        "delta_cp": "4.10%",
    }
    formulas = {
        "theta12": "theta_12 = arctan(1/phi) + theta_13/5",
        "theta23": "theta_23 = 45 deg (bare prediction; Tier 3 due to tension)",
        "theta13": "theta_13 = arcsin(phi^-4)",
        "delta_cp": "delta_CP = 2 pi * phi^-1 (= 360 deg / phi)",
    }
    tiers = {
        "theta12": "Tier 3",
        "theta23": "Tier 3 (Tension)",
        "theta13": "Tier 3",
        "delta_cp": "Tier 2 parametric phase mechanism + Tier 3 PMNS-sector magnitude/disposition pending O.7 and theta_23 tension resolution",
    }
    # PDG/NuFit-scale one-sigma tolerances used for verifier status.
    # PASS means within 1 sigma; TENSION means outside 1 sigma but not
    # a hard verifier failure. This is stricter than the loose <5% gate.
    tolerances_deg = {
        "theta12": 0.80,
        "theta23": CODATA.THETA23_DEG_ERR,
        "theta13": 0.12,
        "delta_cp": 35.0,
    }

    results = []
    for k in ("theta12", "theta23", "theta13", "delta_cp"):
        pct = pct_error(preds[k], targets[k])
        gap_deg = abs(preds[k] - targets[k])
        tol_deg = tolerances_deg[k]
        sigma = gap_deg / tol_deg if tol_deg else math.inf
        status = "PASS" if sigma <= 1.0 else "TENSION"
        if k == "delta_cp" and status == "PASS":
            status = "OPEN_CONDITIONAL"
        extra = {
            "percent_error": pct,
            "gap_deg": gap_deg,
            "pdg_tolerance_deg": tol_deg,
            "sigma_vs_pdg_tolerance": sigma,
            "status_rule": "PASS if within 1 sigma PDG/NuFit-scale tolerance; otherwise TENSION; delta_CP is downgraded to OPEN_CONDITIONAL because the phase mechanism is Tier 2 but PMNS-sector magnitude/disposition remains Tier 3 pending O.7 and theta_23 tension resolution",
        }
        if k == "theta23":
            extra["note"] = (
                "Bare prediction 45 deg is in >4 sigma tension with the "
                "49.5 deg +/- 1.1 deg anchor. App R Sec R.4 downgrades to "
                "Tier 3 pending geometric derivation of the deviation."
            )

        res = make_result(
            name=f"pmns_{k}",
            app_r_label=f"PMNS {k}",
            formula=formulas[k],
            predicted=preds[k],
            observed=targets[k],
            unit="degrees",
            app_r_predicted=app_r_pred[k],
            app_r_precision_str=app_r_str[k],
            app_r_precision_ppm=None,
            tier=tiers[k],
            status=status,
            tolerance_ppm=None,
            extra=extra,
        )
        print_summary(res)
        write_result(res)
        results.append(res)
    return results


if __name__ == "__main__":
    main()
