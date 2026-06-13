"""
verify_protocol_d_mc_systematics.py — Registry parity check for Protocol D MC.

The executable Monte Carlo lives in src/protocol_d_mc_systematics.py and writes
data/protocol_d_mc_systematics_results.json. This independent-harness wrapper
binds the App FM P.13 row to that artifact so the matrix reports the registered
no-gate / expected-non-pass disposition instead of PENDING-VERIFIER.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from report import make_result, write_result, print_summary


EXPECTED_VERDICT = "BELOW_TARGET_POWER_AT_010_PCT_EFFECT_UNDER_BONFERRONI_CORRECTION"


def main():
    data_path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "protocol_d_mc_systematics_results.json"
    )
    with data_path.open(encoding="utf-8") as f:
        data = json.load(f)

    verdict = data.get("verdict_status")
    registered = data.get("registered_budget", {})
    syst = registered.get("systematic_only_SD_total")
    rel_gate = registered.get("systematic_only_SD_relative_to_gate")
    power_010 = registered.get("statistical_power_at_0p10pct_effect_confidence_99pct_gaussian_gate")
    fpr_010 = registered.get("false_positive_rate_at_confidence_99pct_gate_under_null_naive")

    status = "OPEN_CONDITIONAL" if verdict == EXPECTED_VERDICT else "FAIL"
    notes = []
    if verdict != EXPECTED_VERDICT:
        notes.append(
            f"Protocol D MC verdict differs from registered: {EXPECTED_VERDICT} to {verdict}."
        )

    result = make_result(
        name="protocol_d_mc_systematics",
        app_r_label="Protocol D LORR MC systematics gate",
        formula="End-to-end MC propagation of S1-S6 systematics through Hill-equation C50 fit",
        predicted=None,
        observed=None,
        unit="verdict",
        app_r_predicted=None,
        app_r_precision_str="Expected non-pass/no-gate under registered systematic budget",
        app_r_precision_ppm=None,
        tier="Tier 2 mechanism + Tier 4 operational no-gate under current systematics",
        status=status,
        tolerance_ppm=None,
        discrepancy_notes=notes,
        extra={
            "artifact": str(data_path),
            "verdict_status": verdict,
            "expected_verdict": EXPECTED_VERDICT,
            "systematic_only_SD_total": syst,
            "systematic_only_SD_relative_to_0p10pct_gate": rel_gate,
            "power_at_0p10pct_effect": power_010,
            "false_positive_rate_at_0p10pct_gate_under_null": fpr_010,
            "interpretation": (
                "The registered 0.10%-0.20% LORR effect band is below the "
                "current systematic noise floor; Protocol D has no operative "
                "quantitative falsification gate until the budget is tightened "
                "or a replacement decision statistic is preregistered."
            ),
        },
    )
    print_summary(result)
    write_result(result)
    return result


if __name__ == "__main__":
    main()
