#!/usr/bin/env python3
"""Force-test verifier status branches and status/band consistency."""

from __future__ import annotations

import math
import json
import sys
from pathlib import Path
from statistics import NormalDist
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT.parent / "src"))

from report import (  # noqa: E402
    make_result,
    status_from_open_problem,
    status_from_registered_band,
    status_from_upper_bound,
)
from verify_fbound import evaluate_status as fbound_status  # noqa: E402
from verify_g2_electron import (  # noqa: E402
    evaluate_status as electron_status,
    lattice_contribution_for_threshold,
)
from verify_g2_muon import evaluate_status as muon_status  # noqa: E402
from verify_tau_mass import evaluate_registered_tolerance_status as tau_tolerance_status  # noqa: E402
from gct_utils import resolve_a3  # noqa: E402
from protocol_alpha_derivation import evaluate_alpha_derivation  # noqa: E402
from verify_engine import (  # noqa: E402
    evaluate_registered_claim_value,
    validate_fine_structure_claim_contract,
)


def expect_value_error(label: str, fn) -> None:
    try:
        fn()
    except ValueError:
        return
    raise AssertionError(f"{label}: expected ValueError")


def result_with(*, predicted: float, observed: float, tolerance: float, status: str):
    return make_result(
        name="forced_status_contract_case",
        app_psc_label="forced status-contract case",
        formula="test-only comparison",
        predicted=predicted,
        observed=observed,
        unit="dimensionless",
        status=status,
        reference_class="EMPIRICAL_ANCHOR",
        tolerance_ppm=tolerance,
    )


def main() -> int:
    # A3 direct/inverse SSOT and exact failover must be reciprocal. Exercise
    # missing, inverse-only, direct-only, and contradictory namespaces.
    a3_inverse = 137.035999177
    a3_direct = 1.0 / a3_inverse
    assert resolve_a3(SimpleNamespace()) == (a3_direct, a3_inverse)
    assert resolve_a3(SimpleNamespace(ALPHA_INV_OBS=a3_inverse)) == (a3_direct, a3_inverse)
    assert resolve_a3(SimpleNamespace(ALPHA_OBS=a3_direct)) == (a3_direct, a3_inverse)
    try:
        resolve_a3(SimpleNamespace(ALPHA_OBS=0.007, ALPHA_INV_OBS=a3_inverse))
    except RuntimeError:
        pass
    else:
        raise AssertionError("contradictory A3 direct/inverse namespace did not fail closed")

    # Fine-structure F21: the scientific claim is an external CODATA
    # comparison; reproducing 360*phi^-2 is a separate internal regression.
    registry_path = ROOT.parent / "config" / "claim_registry.json"
    claims = json.loads(registry_path.read_text(encoding="utf-8"))
    fine_claim = next(c for c in claims if c.get("claim_id") == "C_FINE_STRUCTURE")
    assert fine_claim["json_field"] == "alpha_bare_inv"
    assert fine_claim["target_value"] == a3_inverse
    assert fine_claim["tolerance"] == 5000
    assert fine_claim["tolerance_type"] == "ppm"
    assert fine_claim["verification_scope"] == "external_empirical_comparison"
    assert fine_claim["claim_type"] == "external_postdiction"
    assert "10.1103/RevModPhys.97.025002" in fine_claim["target_provenance"]
    assert validate_fine_structure_claim_contract(fine_claim) is True

    threshold_ppm = float(fine_claim["tolerance"])
    upper_099 = a3_inverse * (1.0 + 0.99 * threshold_ppm / 1.0e6)
    upper_exact = a3_inverse * (1.0 + threshold_ppm / 1.0e6)
    lower_exact = a3_inverse * (1.0 - threshold_ppm / 1.0e6)
    upper_101 = a3_inverse * (1.0 + 1.01 * threshold_ppm / 1.0e6)

    canonical_formula = 360.0 * ((1.0 + math.sqrt(5.0)) / 2.0) ** -2
    canonical = evaluate_alpha_derivation(canonical_formula)
    assert canonical["status"] == "OPEN_CONDITIONAL"
    assert canonical["external_comparison_pass"] is True
    assert canonical["formula_regression_pass"] is True
    assert canonical["precision_validation_pass"] is False
    assert canonical["pass"] is False

    for value in (upper_099, upper_exact, lower_exact):
        forced = evaluate_alpha_derivation(
            value, formula_expected_inv=value, tolerance_ppm=threshold_ppm
        )
        assert forced["status"] == "OPEN_CONDITIONAL"
        assert forced["external_comparison_pass"] is True
        assert evaluate_registered_claim_value(value, fine_claim)[0] is True

    outside = evaluate_alpha_derivation(
        upper_101, formula_expected_inv=upper_101, tolerance_ppm=threshold_ppm
    )
    assert outside["status"] == "FAIL"
    assert outside["external_comparison_pass"] is False
    assert evaluate_registered_claim_value(upper_101, fine_claim)[0] is False

    formula_mismatch = evaluate_alpha_derivation(
        canonical_formula + 1.0e-8,
        formula_expected_inv=canonical_formula,
        tolerance_ppm=threshold_ppm,
    )
    assert formula_mismatch["external_comparison_pass"] is True
    assert formula_mismatch["formula_regression_pass"] is False
    assert formula_mismatch["status"] == "FAIL"

    assert evaluate_registered_claim_value(None, fine_claim)[0] is False
    for stale_patch in (
        {"target_value": 137.507764},
        {"tolerance_type": "relative"},
        {"verification_scope": "internal_regression"},
        {"target_provenance": ""},
    ):
        stale_claim = {**fine_claim, **stale_patch}
        expect_value_error(
            f"stale C_FINE_STRUCTURE mutation {stale_patch}",
            lambda stale_claim=stale_claim: validate_fine_structure_claim_contract(
                stale_claim
            ),
        )

    # Monotone registered-band boundary: equality is inside.
    assert status_from_registered_band(99.0, 100.0) == "PASS"
    assert status_from_registered_band(100.0, 100.0) == "PASS"
    assert status_from_registered_band(101.0, 100.0) == "TENSION"
    assert status_from_registered_band(
        99.0, 100.0, inside_status="OPEN_CONDITIONAL", outside_status="FAIL"
    ) == "OPEN_CONDITIONAL"
    assert status_from_registered_band(
        101.0, 100.0, inside_status="OPEN_CONDITIONAL", outside_status="FAIL"
    ) == "FAIL"

    # Registered 50/55 ppm tri-state tolerance (not a derived theory floor): equality remains inside, the
    # narrow 50-55 ppm interval is explicitly at-gate, and 55 ppm is hard fail.
    assert tau_tolerance_status(49.99) == "PASS"
    assert tau_tolerance_status(50.0) == "PASS"
    assert tau_tolerance_status(50.0001) == "AT_GATE_TENSION"
    assert tau_tolerance_status(54.999) == "AT_GATE_TENSION"
    assert tau_tolerance_status(55.0) == "HARD_FAIL"

    # Proton auxiliary LEA: preserve the stated primitive and its one-sided
    # conversion rather than reverse-engineering a p-value from a rounded sigma.
    p_single = 1.0e-4
    p_global = min(1.0, 100.0 * p_single)
    normal = NormalDist()
    assert math.isclose(normal.inv_cdf(1.0 - p_single), 3.719016485455709, rel_tol=0.0, abs_tol=1e-12)
    assert math.isclose(normal.inv_cdf(1.0 - p_global), 2.3263478740408408, rel_tol=0.0, abs_tol=1e-12)

    # Derivational closure is orthogonal to the numerical band.
    assert status_from_open_problem(
        True, open_status="OPEN_RESEARCH", closed_status="PASS"
    ) == "OPEN_RESEARCH"
    assert status_from_open_problem(
        False, open_status="OPEN_RESEARCH", closed_status="PASS"
    ) == "PASS"

    # make_result rejects status/band contradictions.
    expect_value_error(
        "outside-band PASS",
        lambda: result_with(predicted=200.0, observed=100.0, tolerance=1.0, status="PASS"),
    )
    expect_value_error(
        "exact-match FAIL",
        lambda: result_with(predicted=100.0, observed=100.0, tolerance=1.0, status="FAIL"),
    )

    # Muon g-2: exact and uncertainty-dilated cases remain open; >=3 sigma is tension.
    assert muon_status(2.5, 2.5, 0.1) == "OPEN_CONDITIONAL"
    assert muon_status(2.5, 0.0, 1.0) == "OPEN_CONDITIONAL"
    assert muon_status(2.5, 0.0, 0.5) == "TENSION"

    # Strong CP is a strict one-sided upper-limit test with theorem closure open.
    bound = 1.0e-10
    assert status_from_upper_bound(0.0, bound, derivation_open=True) == "OPEN_CONDITIONAL"
    assert status_from_upper_bound(0.5 * bound, bound, derivation_open=True) == "OPEN_CONDITIONAL"
    assert status_from_upper_bound(bound, bound, derivation_open=True) == "FAIL"
    assert status_from_upper_bound(2.0 * bound, bound, derivation_open=True) == "FAIL"

    # f_bound checks stated scenario arithmetic, including bad disclosed bounds.
    n_water = math.pi * 7.5**2 * 8.0 / 0.0299
    f_lo = 1 * 4 * 12 / n_water
    f_hi = 1 * 8 * 12 / n_water
    assert fbound_status(f_lo, f_hi, 1.0e-3, 2.0e-3) == "INTERNAL_ARITHMETIC_PASS"
    assert fbound_status(f_lo, f_hi, 2.0e-3, 1.0e-3) == "FAIL"
    expect_value_error("bad f_bound lower bound", lambda: fbound_status(f_lo, f_hi, 0.0, 2.0e-3))

    # Electron threshold: below is null; at/above must supply an activated value.
    assert lattice_contribution_for_threshold(0.99, 1.0) == 0.0
    expect_value_error("electron at threshold", lambda: lattice_contribution_for_threshold(1.0, 1.0))
    expect_value_error("electron above threshold", lambda: lattice_contribution_for_threshold(1.01, 1.0))
    assert lattice_contribution_for_threshold(1.01, 1.0, activated_contribution=0.25) == 0.25
    sigma = 1.0
    assert electron_status(0.0, (0.5, 1.5), sigma) == "PASS"
    assert electron_status(0.0, (0.5, 2.5), sigma) == "PENDING-α-RESOLUTION"
    assert electron_status(0.0, (2.5, 3.0), sigma) == "PENDING-α-RESOLUTION"

    print("PASS: verifier status contract branches are reachable and status/band pairs are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
