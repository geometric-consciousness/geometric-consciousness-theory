#!/usr/bin/env python3
"""
nmr_polarity_power.py -- Protocol D P.13c design-sketch helper.

The helper is imported by both the Protocol D engine path and the independent
P.13c verifier so the design-sketch parameters remain single-sourced from
falsifiability_registry.json.

GATE STATUS: P.13c is HELD PENDING REDESIGN. As written the gate rejected by
construction (17O shortens water-1H T2 by scalar relaxation). The power
arithmetic below is a design sketch only; no decision output of this module is
operative, and until the redesign no outcome supports or rejects the branch.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from statistics import NormalDist

import numpy as np


ENGINE_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ENGINE_ROOT / "falsifiability_registry.json"
GATE_STATUS = "HELD_PENDING_REDESIGN"


def load_registered_p13c_entry() -> dict:
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        registry = json.load(f)
    for entry in registry.get("entries", []):
        if entry.get("id") == "P.13c":
            return entry
    raise KeyError("P.13c registry entry not found")


def _bootstrap_ci_delta(
    n_per_condition: int,
    effect_fraction: float,
    sigma_fraction: float,
    n_resamples: int,
    alpha_two_sided: float,
    seed: int,
) -> dict:
    """Deterministic synthetic-data bootstrap for the design-sketch budget."""
    rng = np.random.default_rng(seed)
    template = np.linspace(-1.0, 1.0, n_per_condition, dtype=float)
    template = (template - np.mean(template)) / np.std(template, ddof=1)

    control = 1.0 + sigma_fraction * template
    active = (1.0 + effect_fraction) + sigma_fraction * np.roll(template, n_per_condition // 3)

    control_idx = rng.integers(0, n_per_condition, size=(n_resamples, n_per_condition))
    active_idx = rng.integers(0, n_per_condition, size=(n_resamples, n_per_condition))
    deltas = active[active_idx].mean(axis=1) - control[control_idx].mean(axis=1)

    lo_q = 100.0 * alpha_two_sided / 2.0
    hi_q = 100.0 * (1.0 - alpha_two_sided / 2.0)
    ci_low, ci_high = np.percentile(deltas, [lo_q, hi_q])
    return {
        "n_resamples": int(n_resamples),
        "ci_level": float(1.0 - alpha_two_sided),
        "ci_low_fraction": float(ci_low),
        "ci_high_fraction": float(ci_high),
        "ci_excludes_zero": bool(ci_low > 0.0 or ci_high < 0.0),
        "ci_sign_positive": bool(ci_low > 0.0 and ci_high > 0.0),
    }


def _replication_simulation(
    n_per_condition: int,
    effect_fraction: float,
    sigma_fraction: float,
    alpha_two_sided: float,
    n_simulations: int,
    seed: int,
) -> dict:
    """Monte Carlo alpha/beta check for primary and replication cohorts (design sketch)."""
    rng = np.random.default_rng(seed)
    norm = NormalDist()
    zcrit = norm.inv_cdf(1.0 - alpha_two_sided / 2.0)
    se = math.sqrt(2.0 * sigma_fraction * sigma_fraction / n_per_condition)
    noncentrality = effect_fraction / se

    z_null = rng.normal(0.0, 1.0, size=n_simulations)
    z_primary = rng.normal(noncentrality, 1.0, size=n_simulations)
    z_replication = rng.normal(noncentrality, 1.0, size=n_simulations)

    false_positive = np.abs(z_null) > zcrit
    primary_positive = z_primary > zcrit
    replication_positive = z_replication > zcrit
    replicated_positive = primary_positive & replication_positive

    return {
        "n_simulations": int(n_simulations),
        "alpha_false_positive_rate_two_sided": float(false_positive.mean()),
        "primary_sign_positive_power": float(primary_positive.mean()),
        "primary_false_negative_beta": float(1.0 - primary_positive.mean()),
        "replication_pair_sign_positive_power": float(replicated_positive.mean()),
        "zcrit_two_sided_alpha": float(zcrit),
        "noncentrality_at_effect_target": float(noncentrality),
    }


def evaluate_registered_p13c_design(
    *,
    bootstrap_resamples: int = 10_000,
    replication_simulations: int = 50_000,
    seed: int = 13013,
) -> dict:
    """Evaluate the P.13c design sketch against its 5% target.

    The result is design-sketch power arithmetic, not lab evidence and not an
    operative gate: P.13c is held pending redesign. The power statistic answers
    whether an n=24 / alpha=0.01 / beta=0.20 design could resolve a 5%
    active-state isotope x activity interaction once the pilot variance budget
    is at or below the returned sigma ceiling.
    """
    entry = load_registered_p13c_entry()
    prereg = entry["preregistration_package"]

    n_per_condition = int(prereg["sample_size_per_isotope_condition"])
    repeated_acquisitions = int(prereg["repeated_nmr_acquisitions_per_preparation"])
    alpha_two_sided = float(prereg["alpha_two_sided"])
    beta = float(prereg["beta"])
    target_power = 1.0 - beta
    effect_fraction = float(prereg["active_state_polarity_reversal_power_target_fraction"])
    # Systematic floor registered as a fraction of water-1H T2 (the former
    # "0.2 ppm" key mixed units; 0.2 ppm == 2e-7 of T2).
    systematic_sigma_fraction = float(prereg["dominant_systematic_sigma_fraction_of_T2"])

    norm = NormalDist()
    zcrit = norm.inv_cdf(1.0 - alpha_two_sided / 2.0)
    zbeta = norm.inv_cdf(target_power)
    total_sigma_fraction_max = effect_fraction * math.sqrt(n_per_condition / 2.0) / (zcrit + zbeta)
    statistical_sigma_fraction_budget = math.sqrt(
        max(total_sigma_fraction_max * total_sigma_fraction_max - systematic_sigma_fraction * systematic_sigma_fraction, 0.0)
    )
    se_at_budget = math.sqrt(2.0 * total_sigma_fraction_max * total_sigma_fraction_max / n_per_condition)
    noncentrality = effect_fraction / se_at_budget
    achieved_power = (
        1.0
        - norm.cdf(zcrit - noncentrality)
        + norm.cdf(-zcrit - noncentrality)
    )

    bootstrap = _bootstrap_ci_delta(
        n_per_condition,
        effect_fraction,
        statistical_sigma_fraction_budget,
        bootstrap_resamples,
        alpha_two_sided,
        seed,
    )
    replication = _replication_simulation(
        n_per_condition,
        effect_fraction,
        total_sigma_fraction_max,
        alpha_two_sided,
        replication_simulations,
        seed + 1,
    )

    status = "OPEN_CONDITIONAL"
    pass_design = (
        n_per_condition == 24
        and repeated_acquisitions == 3
        and abs(alpha_two_sided - 0.01) < 1.0e-12
        and abs(beta - 0.20) < 1.0e-12
        and achieved_power >= target_power - 5.0e-4
        and systematic_sigma_fraction < effect_fraction
        and bootstrap["ci_sign_positive"]
    )
    if not pass_design:
        status = "TENSION" if achieved_power >= 0.50 else "FAIL"

    return {
        "registry_id": "P.13c",
        "status": status,
        "gate_status": GATE_STATUS,
        "decision_outputs_operative": False,
        # Design-budget arithmetic only; never a gate pass while the gate is held.
        "pass": False,
        "design_budget_consistent": bool(pass_design),
        "verdict": f"{status}_DESIGN_SKETCH_{GATE_STATUS}",
        "parameters": {
            "sample_size_per_isotope_condition": n_per_condition,
            "repeated_nmr_acquisitions_per_preparation": repeated_acquisitions,
            "alpha_two_sided": alpha_two_sided,
            "beta": beta,
            "target_power": target_power,
            "active_state_polarity_reversal_power_target_fraction": effect_fraction,
            "dominant_systematic_sigma_fraction_of_T2": systematic_sigma_fraction,
        },
        "power_statistic": {
            "effect_fraction": effect_fraction,
            "effect_ppm": effect_fraction * 1.0e6,
            "zcrit_two_sided_alpha": zcrit,
            "zbeta_target": zbeta,
            "max_total_per_preparation_sigma_fraction_for_80pct_power": total_sigma_fraction_max,
            "pilot_variance_acceptance_threshold": (
                "Non-operative while the gate is held pending redesign. After the redesign, a decisive 5% "
                "support/rejection of the registered polarity branch would require pilot total "
                "per-preparation sigma fraction <= max_total_per_preparation_sigma_fraction_for_80pct_power."
            ),
            "statistical_sigma_fraction_budget_after_systematic_floor": statistical_sigma_fraction_budget,
            "systematic_sigma_fraction": systematic_sigma_fraction,
            "systematic_fraction_of_effect": systematic_sigma_fraction / effect_fraction,
            "standard_error_fraction_at_budget": se_at_budget,
            "noncentrality_at_effect_target": noncentrality,
            "achieved_primary_power_at_budget": achieved_power,
        },
        "bootstrap_ci": bootstrap,
        "alpha_beta_replication_simulation": replication,
        "decision_rule": (
            "Held pending redesign. As written the gate rejected by construction "
            "(17O shortens water-1H T2 by scalar relaxation). The former sign-aware "
            "rule -- reject the registered sign-positive branch on a powered, "
            "significant negative isotope x activity interaction in water-1H Delta T2, "
            "Delta T2 = [T2(17O,active) - T2(17O,inactive)] - [T2(16O,active) - "
            "T2(16O,inactive)] -- applies only after the redesign; until then no "
            "outcome supports or rejects the branch. Neither outcome would be a "
            "verdict on GCT as a whole, and no phason, Selection-Operator or "
            "Level-II inference follows (V1 Ch17 §17.1.3)."
        ),
        "decision_rule_operative": False,
        "scope": (
            "Design-sketch power calculation; gate held pending redesign; "
            "lab-data status open."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(evaluate_registered_p13c_design(), indent=2))
