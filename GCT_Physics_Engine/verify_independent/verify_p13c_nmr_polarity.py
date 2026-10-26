"""
verify_p13c_nmr_polarity.py -- Design-sketch verifier for P.13c (sign-aware rule held pending redesign; no outcome supports or rejects the branch until then).

This verifier binds App FSM row P.13c to the Protocol D NMR polarity design:
n=24 preparations per isotope condition, three repeated acquisitions, 99%
bootstrap CI, a dominant-systematic floor of 2e-7 of T_2 (the former
"0.2 ppm" restated as a fraction of water-1H T_2), and alpha/beta replication
simulation against a 5% active-state effect-size design target (not a registered gate).
Delta T_2 is the isotope x activity interaction on water-1H T_2. The gate is
sensitivity-limited pending redesign.

INDEPENDENCE SCOPE: this script is NOT fully independent. It imports
`nmr_polarity_power` from the engine `src/` tree for the registered design
calculation, so its agreement is a consistency check against the engine rather
than a CODATA/PDG-anchored re-derivation of the P.13c design.
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

    # The gate is held pending redesign: no decision output may be operative.
    if design.get("gate_status") != "HELD_PENDING_REDESIGN" or design.get("decision_outputs_operative") is not False:
        raise RuntimeError("P.13c helper must report the gate as held pending redesign with non-operative decision outputs")
    status = design["status"]
    precision = (
        f"OPEN_CONDITIONAL design sketch (sign-aware rule held pending redesign; no outcome supports or rejects the branch until then): n={params['sample_size_per_isotope_condition']} "
        f"per isotope, {params['repeated_nmr_acquisitions_per_preparation']} repeated acquisitions, "
        f"99% bootstrap CI [{bootstrap['ci_low_fraction']:.4f}, {bootstrap['ci_high_fraction']:.4f}], "
        f"systematic floor {params['dominant_systematic_sigma_fraction_of_T2']:.0e} of T2, "
        f"design-sketch primary power {power['achieved_primary_power_at_budget']:.3f}, "
        f"simulated beta {sim['primary_false_negative_beta']:.3f}, "
        f"design-sketch replication-pair power {sim['replication_pair_sign_positive_power']:.3f}"
    )

    res = make_result(
        name="p13c_nmr_polarity",
        app_psc_label="P.13c NMR polarity gate",
        formula="Delta T2 = isotope x activity interaction on water-1H T2; former sign-aware rule (reject the sign-positive branch on a powered, significant negative interaction) held pending redesign; design sketch only, no observed NMR data",
        predicted=params["active_state_polarity_reversal_power_target_fraction"],
        observed=None,
        unit="fractional Delta T2/T2",
        app_psc_predicted=params["active_state_polarity_reversal_power_target_fraction"],
        app_psc_precision_str=precision,
        app_psc_precision_ppm=None,
        tier="Tier 3 material-response sign hypothesis (ordinary isotope/spin-coherence material mechanism; no phason or Level-II content) conditional on O.21/O.33 + Tier 3 active-state Delta T2 calibration anchor pending O.21/O.33",
        status=status,
        tolerance_ppm=None,
        extra=design,
    )
    print_summary(res)
    write_result(res)
    return res


if __name__ == "__main__":
    main()
