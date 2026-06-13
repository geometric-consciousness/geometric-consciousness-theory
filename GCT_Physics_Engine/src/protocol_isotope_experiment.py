#!/usr/bin/env python3
"""
protocol_isotope_experiment.py -- Protocol D H2^16O vs H2^17O LORR/NMR design
================================================================================

Implements the named Protocol D isotope-substitution experiment from V3 Ch16:
compare H2^16O control water against H2^17O-enriched water using the LORR
anesthetic-threshold endpoint and an orthogonal NMR/quadrupolar-relaxation
polarity check.

Endpoint A: LORR anesthetic threshold
-------------------------------------
GCT predicts that ^17O (I=5/2) adds a nuclear-spin entropy load to the
bound-water channel. ^16O has I=0 and contributes no oxygen nuclear-spin
address entropy. For the operative bound-water fraction f_bound, the signed
shift is

    (C50_17O - C50_16O) / C50_16O = -f_bound * DeltaS/Smax = -f_bound

because DeltaS/Smax = ln(6)/ln(6) = 1 for ^17O vs ^16O.

Endpoint B: NMR polarity gate
-----------------------------
The same samples must show a bound-water ^17O quadrupolar-relaxation signature:
active-state baseline-subtracted R2 decrease / T2 lengthening in the ^17O channel must have
the predicted sign, while H2^16O has no ^17O quadrupole line. This gate prevents
a pure bulk-solvent isotope effect from masquerading as the GCT spin-entropy
signal. The mechanism is Tier 2; the active-state Delta T2 sign/magnitude
calibration is Tier 3 pending assembled-substrate and lumen-water NMR closure
(O.21/O.33).
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass

from gct_utils import get_output_path
from nmr_polarity_power import evaluate_registered_p13c_design


@dataclass(frozen=True)
class WaterIsotope:
    key: str
    label: str
    oxygen_mass_u: float
    oxygen_spin: float
    enrichment_fraction: float


H2_16O = WaterIsotope(
    key="H2_16O",
    label="H2^16O control",
    oxygen_mass_u=15.99491461957,
    oxygen_spin=0.0,
    enrichment_fraction=0.99757,
)

H2_17O = WaterIsotope(
    key="H2_17O",
    label="H2^17O test",
    oxygen_mass_u=16.99913175650,
    oxygen_spin=2.5,
    enrichment_fraction=0.95,
)

F_BOUND_OPERATIVE_CENTRAL = 0.0
F_BOUND_SENSITIVITY_RANGE = (1.0e-3, 2.0e-3)
F_BOUND_SENSITIVITY_CENTRAL = 1.5e-3
REGISTERED_SOLVENT_KIE_BOUND = 4.0e-3
REGISTERED_SOLVENT_KIE_BOUND_STATUS = "Tier 3 literature-prior control; no direct H2^16O-to-H2^17O radical-pair solvent-KIE verifier"
REGISTERED_SOLVENT_KIE_BOUND_PROVENANCE = (
    "Heavy-atom solvent/substrate isotope-effect control imported from the "
    "anaesthesia solvent-KIE literature; registered as a conservative control "
    "bound, not as a GCT-derived constant."
)
REGISTERED_SOLVENT_KIE_BOUND_CLOSURE_TARGET = (
    "O.21/O.33: direct assembled-substrate and solvent-KIE calibration for the H2^16O/H2^17O "
    "radical-pair and NMR-polarity protocol."
)
N_RP_OPERATIVE_CENTRAL = 0
N_RP_SENSITIVITY = 1


def spin_entropy_kB(spin: float) -> float:
    """Dimensionless nuclear spin entropy S/k_B = ln(2I + 1)."""
    return math.log(2.0 * spin + 1.0)


def normalized_entropy_load(control: WaterIsotope, test: WaterIsotope) -> float:
    s_control = spin_entropy_kB(control.oxygen_spin)
    s_test = spin_entropy_kB(test.oxygen_spin)
    s_max = max(s_control, s_test, 1.0e-30)
    return abs(s_test - s_control) / s_max


def lorr_shift_fraction(f_bound: float) -> float:
    """Signed GCT LORR C50 shift for H2^17O relative to H2^16O."""
    return -f_bound * normalized_entropy_load(H2_16O, H2_17O)


def enrichment_applied_lorr_shift_fraction(f_bound: float) -> float:
    """Signed cohort shift after multiplying by verified H2^17O enrichment."""
    return H2_17O.enrichment_fraction * lorr_shift_fraction(f_bound)


def raw_vibrational_mass_diagnostic() -> float:
    """Simple oxygen-mass vibrational diagnostic, not the registered LORR gate."""
    return abs(math.sqrt(H2_16O.oxygen_mass_u / H2_17O.oxygen_mass_u) - 1.0)


def build_protocol_results() -> dict:
    lorr_central = lorr_shift_fraction(F_BOUND_OPERATIVE_CENTRAL)
    lorr_low = lorr_shift_fraction(F_BOUND_SENSITIVITY_RANGE[0])
    lorr_high = lorr_shift_fraction(F_BOUND_SENSITIVITY_RANGE[1])
    lorr_sensitivity_central = lorr_shift_fraction(F_BOUND_SENSITIVITY_CENTRAL)
    lorr_enriched_low = enrichment_applied_lorr_shift_fraction(F_BOUND_SENSITIVITY_RANGE[0])
    lorr_enriched_high = enrichment_applied_lorr_shift_fraction(F_BOUND_SENSITIVITY_RANGE[1])
    lorr_enriched_central = enrichment_applied_lorr_shift_fraction(F_BOUND_SENSITIVITY_CENTRAL)
    entropy_load = normalized_entropy_load(H2_16O, H2_17O)
    raw_mass_diag = raw_vibrational_mass_diagnostic()
    nmr_preregistration_power = evaluate_registered_p13c_design()

    lorr_gate = {
        "observable": "(C50_H2_17O - C50_H2_16O) / C50_H2_16O",
        "operative_central_shift": lorr_central,
        "reported_lorr_shift_convention": (
            "pure-endpoint/enrichment-normalized; multiply by verified enrichment "
            "for cohort-level decision statistics"
        ),
        "verified_H2_17O_enrichment_fraction": H2_17O.enrichment_fraction,
        "sensitivity_branch_signed_shift_range": [lorr_high, lorr_low],
        "sensitivity_branch_signed_shift_central": lorr_sensitivity_central,
        "sensitivity_branch_signed_shift_range_at_verified_enrichment": [
            lorr_enriched_high,
            lorr_enriched_low,
        ],
        "sensitivity_branch_signed_shift_central_at_verified_enrichment": lorr_enriched_central,
        "predicted_signed_shift_central": lorr_central,
        "prediction_percent_range": [100.0 * lorr_high, 100.0 * lorr_low],
        "prediction_percent_central": 100.0 * lorr_central,
        "prediction_percent_range_at_verified_enrichment": [
            100.0 * lorr_enriched_high,
            100.0 * lorr_enriched_low,
        ],
        "prediction_percent_central_at_verified_enrichment": 100.0 * lorr_enriched_central,
        "decision_rule": (
            "Central branch is n_rp=0 -> no LORR signal while O.21 is open. "
            "The n_rp=1 Trp21 branch is a sensitivity branch only; LORR remains "
            "a no-gate mechanism probe under the registered systematic budget."
        ),
    }

    nmr_gate = {
        "primary_readout": "baseline-subtracted H2^17O bound-water quadrupolar R2/T2",
        "predicted_polarity": "active-state H2^17O R2 decreases relative to H2^16O control",
        "tier_scope": "Tier 2 mechanism + Tier 3 active-state Delta T2 calibration anchor pending O.21/O.33",
        "executable_preregistration": nmr_preregistration_power,
        "power_statistic": nmr_preregistration_power["power_statistic"],
        "bootstrap_ci_design_check": nmr_preregistration_power["bootstrap_ci"],
        "alpha_beta_replication_simulation": nmr_preregistration_power["alpha_beta_replication_simulation"],
        "null_control": "H2^16O has oxygen spin I=0 and no ^17O quadrupole line",
        "systematic_controls": [
            "S1 matched osmolarity",
            "S2 locked ^17O enrichment assay",
            "S3 matched anesthetic concentration ladder",
            "S4 blinded LORR scoring",
            "S5 temperature and pH lock",
            "S6 viscosity/osmotic-pressure covariates",
            "S7 NMR baseline subtraction",
            "S8 enrichment-label blind maintained through analysis",
        ],
    }

    kie_controls = {
        "raw_vibrational_mass_diagnostic": raw_mass_diag,
        "raw_vibrational_mass_diagnostic_percent": 100.0 * raw_mass_diag,
        "registered_solvent_kie_bound": REGISTERED_SOLVENT_KIE_BOUND,
        "registered_solvent_kie_bound_percent": 100.0 * REGISTERED_SOLVENT_KIE_BOUND,
        "registered_solvent_kie_bound_status": REGISTERED_SOLVENT_KIE_BOUND_STATUS,
        "registered_solvent_kie_bound_provenance": REGISTERED_SOLVENT_KIE_BOUND_PROVENANCE,
        "registered_solvent_kie_bound_closure_target": REGISTERED_SOLVENT_KIE_BOUND_CLOSURE_TARGET,
        "interpretation": (
            "The raw oxygen-mass diagnostic is a bulk-solvent control, not the "
            "registered spin-entropy endpoint. Protocol D requires the signed LORR "
            "shift plus the ^17O NMR polarity gate to separate spin entropy from "
            "ordinary isotope chemistry."
        ),
    }

    self_consistency_ok = (
        abs(entropy_load - 1.0) < 1.0e-12
        and abs(lorr_central + F_BOUND_OPERATIVE_CENTRAL) < 1.0e-15
        and lorr_high < lorr_low < 0.0
    )

    return {
        "protocol": "Protocol D -- H2^16O vs H2^17O LORR/NMR isotope substitution",
        "implementation_scope": "Ch16 Protocol D, not xenon MAC",
        "isotopes": {
            H2_16O.key: asdict(H2_16O),
            H2_17O.key: asdict(H2_17O),
        },
        "n_rp_operative_central": N_RP_OPERATIVE_CENTRAL,
        "n_rp_sensitivity_branch": N_RP_SENSITIVITY,
        "f_bound_operative_central": F_BOUND_OPERATIVE_CENTRAL,
        "f_bound_sensitivity_range": list(F_BOUND_SENSITIVITY_RANGE),
        "f_bound_sensitivity_central": F_BOUND_SENSITIVITY_CENTRAL,
        "f_bound_range": list(F_BOUND_SENSITIVITY_RANGE),
        "f_bound_central": F_BOUND_OPERATIVE_CENTRAL,
        "spin_entropy_H2_16O_kB": spin_entropy_kB(H2_16O.oxygen_spin),
        "spin_entropy_H2_17O_kB": spin_entropy_kB(H2_17O.oxygen_spin),
        "normalized_entropy_load": entropy_load,
        "lorr_gate": lorr_gate,
        "nmr_quadrupole_gate": nmr_gate,
        "kie_controls": kie_controls,
        "recommendation": (
            "Run LORR as the behavioral endpoint and treat the ^17O NMR polarity "
            "gate as mandatory. A LORR-only shift is not sufficient for GCT "
            "closure because solvent isotope systematics can be sign-ambiguous."
        ),
        "pass": bool(self_consistency_ok),
        "self_consistency_check": {
            "entropy_load_is_unity_for_17O_vs_16O": abs(entropy_load - 1.0) < 1.0e-12,
            "central_shift_equals_minus_f_bound": abs(lorr_central + F_BOUND_OPERATIVE_CENTRAL) < 1.0e-15,
            "signed_band_is_negative": lorr_high < lorr_low < 0.0,
        },
    }


def run_protocol_d() -> dict:
    print("=" * 72)
    print("GCT Protocol D -- H2^16O vs H2^17O LORR/NMR isotope substitution")
    print("=" * 72)

    results = build_protocol_results()
    lorr = results["lorr_gate"]
    nmr = results["nmr_quadrupole_gate"]

    print(f"  f_bound operative central : {F_BOUND_OPERATIVE_CENTRAL:.1e} (n_rp=0 pending O.21)")
    print(f"  f_bound sensitivity branch: {F_BOUND_SENSITIVITY_RANGE[0]:.1e} to {F_BOUND_SENSITIVITY_RANGE[1]:.1e} (n_rp=1)")
    print(f"  Sensitivity LORR shift    : {lorr['prediction_percent_range'][0]:.3f}% to {lorr['prediction_percent_range'][1]:.3f}%")
    print(f"  Enrichment-applied shift  : {lorr['prediction_percent_range_at_verified_enrichment'][0]:.3f}% to {lorr['prediction_percent_range_at_verified_enrichment'][1]:.3f}%")
    print(f"  Central LORR shift        : {lorr['prediction_percent_central']:.3f}%")
    print(f"  NMR polarity gate       : {nmr['predicted_polarity']}")
    print(
        "  NMR prereg power       : "
        f"{nmr['power_statistic']['achieved_primary_power_at_budget']:.3f} "
        f"({nmr['executable_preregistration']['status']})"
    )
    print(f"  Self-consistency pass   : {results['pass']}")

    out = get_output_path("protocol_isotope_experiment_results.json")
    with open(out, "w", encoding="utf-8") as fp:
        json.dump(results, fp, indent=2)
    print(f"\n  Report saved -> {out}")
    return results


if __name__ == "__main__":
    run_protocol_d()
