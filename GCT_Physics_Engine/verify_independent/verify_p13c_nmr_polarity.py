"""
verify_p13c_nmr_polarity.py -- Executable preregistration verifier for P.13c.

This verifier binds App FM row P.13c to the Protocol D NMR polarity design:
n=24 preparations per isotope condition, three repeated acquisitions, 99%
bootstrap CI, 0.2 ppm systematic floor, and alpha/beta replication simulation
against the registered 5% active-state polarity-reversal target.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT.parent / "src"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(SRC))

from nmr_polarity_power import evaluate_registered_p13c_design
from report import make_result, print_summary, write_result


def main():
    design = evaluate_registered_p13c_design()
    params = design["parameters"]
    power = design["power_statistic"]
    bootstrap = design["bootstrap_ci"]
    sim = design["alpha_beta_replication_simulation"]

    status = design["status"]
    precision = (
        f"OPEN_CONDITIONAL executable preregistration: n={params['sample_size_per_isotope_condition']} "
        f"per isotope, {params['repeated_nmr_acquisitions_per_preparation']} repeated acquisitions, "
        f"99% bootstrap CI [{bootstrap['ci_low_fraction']:.4f}, {bootstrap['ci_high_fraction']:.4f}], "
        f"systematic floor {params['dominant_systematic_sigma_ppm_max']:.1f} ppm, "
        f"primary power {power['achieved_primary_power_at_budget']:.3f}, "
        f"simulated beta {sim['primary_false_negative_beta']:.3f}, "
        f"replication-pair power {sim['replication_pair_sign_positive_power']:.3f}"
    )

    res = make_result(
        name="p13c_nmr_polarity",
        app_r_label="P.13c NMR polarity gate",
        formula="99% bootstrap sign-positive Delta T2 gate powered for 5% active-state polarity reversal; design target only, no observed NMR data yet",
        predicted=params["active_state_polarity_reversal_power_target_fraction"],
        observed=None,
        unit="fractional Delta T2/T2",
        app_r_predicted=params["active_state_polarity_reversal_power_target_fraction"],
        app_r_precision_str=precision,
        app_r_precision_ppm=None,
        tier="Tier 2 mechanism + Tier 3 active-state Delta T2 calibration anchor pending O.21/O.33",
        status=status,
        tolerance_ppm=None,
        extra=design,
    )
    print_summary(res)
    write_result(res)
    return res


if __name__ == "__main__":
    main()
