"""
verify_pmns.py - Independent recomputation of the PMNS angle formulas

App PSC Sec PSC.4 rows 4-7 (comparators: NuFIT 6.0, normal ordering, with SK
atmospheric data unless noted; arXiv:2410.05380 Table 1):
    theta_12 = arctan(1/phi) + (theta_13/5)  -> 33.40 deg vs 33.68 (+0.73/-0.70) deg (-0.85%, 0.4 sigma)
    theta_23 = 45 deg                         -> inside the 3-sigma range with SK (41.3-49.9 deg) and
                                                 without SK (41.0-50.5 deg); Delta chi^2(45 deg) = 2.02 / 4.20;
                                                 octant unresolved (the earlier one-octant 4.09-sigma
                                                 Gaussian is withdrawn)
    theta_13 = arcsin(phi^-4)                 -> 8.39 deg vs 8.56 +/- 0.11 deg (-2.0%, 1.5 sigma; 1.2 sigma without SK)
    delta_CP = 2 pi * phi^-1 (360/phi deg)    -> 222.5 deg vs 212 (+26/-41) deg (+0.4 sigma; +2.4 sigma vs 177 without SK)
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
    app_psc_pred = {
        "theta12": 33.40, "theta23": 45.00, "theta13": 8.39, "delta_cp": 222.5,
    }
    app_psc_str = {
        "theta12": "-0.85% (0.4 sigma vs NuFIT 6.0)",
        "theta23": "inside both NuFIT 6.0 3-sigma ranges; Delta chi^2(45 deg) = 2.0 with SK / 4.2 without; octant unresolved",
        "theta13": "-2.0% (1.5 sigma vs NuFIT 6.0 with SK; 1.2 sigma without)",
        "delta_cp": "+0.4 sigma with SK; +2.4 sigma without SK",
    }
    formulas = {
        "theta12": "theta_12 = arctan(1/phi) + theta_13/5",
        "theta23": "theta_23 = 45 deg (bare prediction; Tier 3, octant unresolved)",
        "theta13": "theta_13 = arcsin(phi^-4)",
        "delta_cp": "delta_CP = 2 pi * phi^-1 (= 360 deg / phi)",
    }
    tiers = {
        "theta12": "Tier 3 + Tier 4 as evidence that phi explains the value (constant control test v3 NEGATIVE-FRAGILE; App PSC §PSC.9.6)",
        "theta23": "Tier 3 (octant unresolved)",
        "theta13": "Tier 3 (postdiction; theta_13 measured in 2012) + Tier 4 as evidence that phi explains the value (constant control test v3 NEGATIVE-FRAGILE; App PSC §PSC.9.6)",
        "delta_cp": "Tier 3 phase ansatz (2 pi phi^-1) + Tier 3 PMNS-sector magnitude/disposition pending O.7 and the theta_23 octant + Tier 4 as evidence that phi explains the value (constant control test v3 NEGATIVE-FRAGILE; App PSC §PSC.9.6)",
    }
    # One-sigma tolerances on the side of the prediction (NuFIT 6.0 errors are
    # asymmetric). PASS means within 1 sigma; TENSION means outside 1 sigma but
    # not a hard verifier failure. theta_23 is judged on the two-octant
    # Delta chi^2 / 3-sigma ranges instead of a Gaussian.
    tolerances_deg = {
        "theta12": CODATA.THETA12_DEG_ERR_MINUS if theta12_deg < CODATA.THETA12_DEG else CODATA.THETA12_DEG_ERR_PLUS,
        "theta23": None,
        "theta13": CODATA.THETA13_DEG_ERR,
        "delta_cp": CODATA.DELTA_CP_DEG_ERR_PLUS,
    }

    results = []
    for k in ("theta12", "theta23", "theta13", "delta_cp"):
        pct = pct_error(preds[k], targets[k])
        gap_deg = abs(preds[k] - targets[k])
        tol_deg = tolerances_deg[k]
        extra = {
            "percent_error": pct,
            "gap_deg": gap_deg,
            "comparator_source": "NuFIT 6.0 (arXiv:2410.05380) Table 1, normal ordering, IC24 with SK atmospheric data",
        }
        if k == "theta23":
            lo_sk, hi_sk = CODATA.THETA23_3SIGMA_WITH_SK
            lo_nosk, hi_nosk = CODATA.THETA23_3SIGMA_WITHOUT_SK
            inside = lo_sk <= preds[k] <= hi_sk and lo_nosk <= preds[k] <= hi_nosk
            status = "OPEN_CONDITIONAL" if inside else "TENSION"
            extra.update({
                "best_fit_with_sk_deg": CODATA.THETA23_DEG,
                "best_fit_without_sk_deg": CODATA.THETA23_DEG_WITHOUT_SK,
                "three_sigma_with_sk_deg": [lo_sk, hi_sk],
                "three_sigma_without_sk_deg": [lo_nosk, hi_nosk],
                "dchi2_at_45_with_sk": CODATA.THETA23_DCHI2_45_WITH_SK,
                "dchi2_at_45_without_sk": CODATA.THETA23_DCHI2_45_WITHOUT_SK,
                "equivalent_sigma_with_sk": math.sqrt(CODATA.THETA23_DCHI2_45_WITH_SK),
                "equivalent_sigma_without_sk": math.sqrt(CODATA.THETA23_DCHI2_45_WITHOUT_SK),
                "inside_both_3sigma_ranges": inside,
                "status_rule": "OPEN_CONDITIONAL while 45 deg lies inside both NuFIT 6.0 3-sigma ranges and the octant is unresolved (DUNE / Hyper-K decisive); TENSION otherwise",
                "note": (
                    "The bare 45 deg prediction lies inside the NuFIT 6.0 3-sigma ranges with and without "
                    "SK atmospheric data. The earlier 4.09-sigma figure, a one-octant Gaussian on "
                    "49.5 +/- 1.1 deg, is withdrawn: 45 deg is not in >3-sigma tension and the octant is unresolved."
                ),
            })
        else:
            sigma = gap_deg / tol_deg
            status = "PASS" if sigma <= 1.0 else "TENSION"
            if k == "delta_cp" and status == "PASS":
                status = "OPEN_CONDITIONAL"
            extra.update({
                "nufit_tolerance_deg": tol_deg,
                "sigma_vs_nufit_tolerance": sigma,
                "status_rule": "PASS if within the 1-sigma NuFIT 6.0 error on the prediction's side; otherwise TENSION; delta_CP is downgraded to OPEN_CONDITIONAL because the 2 pi phi^-1 phase is a Tier 3 ansatz and the PMNS-sector magnitude/disposition remains Tier 3 pending O.7 and the theta_23 octant",
            })
            if k == "theta13":
                extra["without_sk_deg"] = CODATA.THETA13_DEG_WITHOUT_SK
                extra["sigma_vs_without_sk"] = abs(preds[k] - CODATA.THETA13_DEG_WITHOUT_SK) / CODATA.THETA13_DEG_ERR
            if k == "delta_cp":
                extra["without_sk_deg"] = CODATA.DELTA_CP_DEG_WITHOUT_SK
                extra["sigma_vs_without_sk"] = abs(preds[k] - CODATA.DELTA_CP_DEG_WITHOUT_SK) / CODATA.DELTA_CP_DEG_WITHOUT_SK_ERR_PLUS
                extra["error_note"] = "NuFIT 6.0 delta_CP errors are non-Gaussian; the sigma values are indicative."

        res = make_result(
            name=f"pmns_{k}",
            app_psc_label=f"PMNS {k}",
            formula=formulas[k],
            predicted=preds[k],
            observed=targets[k],
            unit="degrees",
            app_psc_predicted=app_psc_pred[k],
            app_psc_precision_str=app_psc_str[k],
            app_psc_precision_ppm=None,
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
