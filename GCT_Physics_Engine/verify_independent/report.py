"""
report.py — Shared reporting utility for the independent verification harness.

A verification result captures, per App PSC claim:
    - name                : machine-readable identifier
    - app_psc_label         : the label as it appears in App PSC
    - formula             : the GCT formula as derived independently from prose
    - predicted           : the value re-computed by this harness (independent)
    - observed            : the comparison reference selected by reference_class
    - reference_class     : EMPIRICAL_ANCHOR / MANUSCRIPT_STATED / PURE_MATHEMATICAL
    - app_psc_predicted     : what App PSC claims the engine produces
    - app_psc_precision     : what App PSC claims the precision is (ppm or % string)
    - independent_precision_ppm : what this harness measures
    - status              : PASS / FAIL / TENSION / TIER1_EXACT / INTERNAL_ARITHMETIC_PASS / OPEN_CONDITIONAL / PENDING-α-RESOLUTION / NOT_APPLICABLE
    - discrepancy_notes   : free-text flags for any inter-document inconsistency

Status rule: raw PASS is available only to EMPIRICAL_ANCHOR comparisons and
is evaluated against the declared row-level gate.  MANUSCRIPT_STATED and
PURE_MATHEMATICAL checks use internal-arithmetic or theorem statuses.  FAIL
means the re-derivation violates its declared comparison contract.

Numerical band outcome and derivational closure are separate axes.  A value
inside its registered band can remain OPEN_CONDITIONAL when an explicit
Tier-3 premise is unresolved; a value outside the band cannot be PASS or
OPEN_CONDITIONAL.  The executable branch contract is exercised by
``check_verifier_status_contract.py``.
"""

import json
import os
import sys
from pathlib import Path
from typing import Optional

# Force UTF-8 stdout/stderr so verifier output (which contains characters
# like phi, alpha, Delta, approximately-equal, sigma, +/-) does not raise
# UnicodeEncodeError on Windows consoles that default to cp1252.
for _stream_name in ("stdout", "stderr"):
    _stream = getattr(sys, _stream_name, None)
    if _stream is not None and hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

RESULTS_DIR = Path(
    os.environ.get(
        "GCT_VERIFY_RESULTS_DIR",
        str(Path(__file__).resolve().parent / "results"),
    )
)
RESULTS_DIR.mkdir(exist_ok=True, parents=True)


# Every canonical verifier result is assigned deliberately. Missing names fail
# closed instead of inheriting an empirical label.
_MANUSCRIPT_STATED_RESULTS = {
    "alpha_s_inv_bare",
    "cage_node_count_N144",
    "ch20_liv_delay_and_rm_coefficient",
    "chi_holographic_susceptibility",
    "fbio_jacobian",
    "polaron_healing_length",
    "pta_l6_transfer_open",
    "w_z_phantom_crossing_z028",
    "yield_strain_epsilon_y",
}
_PURE_MATHEMATICAL_RESULTS = {
    "pta_l6_first_scalar_invariant",
    "pta_l6_orientation_requirement",
    "weinberg_gut",
    # Algebraic identities whose "observed" value is the computed identity
    # itself; they are not empirical-anchor comparisons.
    "E_perp_E_para_amplitudes",
    "phason_stiffness_ratio",
    "hypercharges_and_anomaly_cancellation",
    "ckm_unitarity_3x3",
    "pmns_unitarity_3x3",
}
_EMPIRICAL_ANCHOR_RESULTS = {
    "alpha_inverse", "alpha_inverse_bilayer_corrected",
    "bottom_quark", "cabibbo_angle", "charm_quark",
    "ckm_jarlskog", "ckm_s12", "ckm_s13", "ckm_s23",
    "dm_line_3p55keV", "dm_line_width_morphology", "down_quark",
    "electron_mass", "f_bound_conservative_geometry",
    "g2_electron", "g2_muon", "higgs_mass_bare", "higgs_vev",
    "muon_mass", "neutrino_m1_floor",
    "neutrino_sum", "newton_g", "nu_zeno_van_Hove", "p13c_nmr_polarity",
    "pmns_delta_cp", "pmns_theta12", "pmns_theta13",
    "pmns_theta23", "protocol_d_mc_systematics",
    "proton_mass", "strange_quark", "strong_cp_theta_bar", "tau_mass",
    "top_quark", "up_quark", "weinberg_bare",
}
# This is manuscript-scenario arithmetic, not an empirical observation.
_EMPIRICAL_ANCHOR_RESULTS.remove("f_bound_conservative_geometry")
_MANUSCRIPT_STATED_RESULTS.add("f_bound_conservative_geometry")
# The "observed" value is the 112 MHz design drive, not a measurement; the
# inverse-Zeno sign is conditional on O.23.
_MANUSCRIPT_STATED_RESULTS.add("anti_zeno_upper_crossover")
REFERENCE_CLASS_BY_RESULT = {
    **{name: "EMPIRICAL_ANCHOR" for name in _EMPIRICAL_ANCHOR_RESULTS},
    **{name: "MANUSCRIPT_STATED" for name in _MANUSCRIPT_STATED_RESULTS},
    **{name: "PURE_MATHEMATICAL" for name in _PURE_MATHEMATICAL_RESULTS},
}


def _closure_state(status: str) -> str:
    if status == "OPEN_CONDITIONAL":
        return "OPEN_CONDITIONAL"
    if status == "OPEN_RESEARCH":
        return "OPEN_RESEARCH"
    if status in ("PENDING-α-RESOLUTION", "NOT_APPLICABLE"):
        return status
    return "NO_DERIVATIONAL_CLOSURE_FLAG"


def status_from_registered_band(
    precision_ppm: float,
    tolerance_ppm: float,
    *,
    inside_status: str = "PASS",
    outside_status: str = "TENSION",
) -> str:
    """Apply a monotone two-state gate within one declared comparison class.

    Cross-observable residuals are not ordered unless they share the same
    reference class and registered band.  Within such a class, increasing
    ``abs(precision_ppm)`` cannot improve the status: values at or below the
    registered band receive ``inside_status`` and larger values receive
    ``outside_status``.
    """
    return inside_status if abs(precision_ppm) <= tolerance_ppm else outside_status


def status_from_open_problem(
    is_open: bool,
    *,
    open_status: str,
    closed_status: str,
) -> str:
    """Select the derivational-closure status without disguising it as a band test."""
    return open_status if is_open else closed_status


def status_from_upper_bound(
    predicted: float,
    upper_bound: float,
    *,
    derivation_open: bool,
) -> str:
    """Classify a signed/null prediction against an experimental upper bound."""
    if abs(predicted) >= upper_bound:
        return "FAIL"
    return "OPEN_CONDITIONAL" if derivation_open else "PASS"


def make_result(
    name: str,
    app_psc_label: str,
    formula: str,
    predicted: float,
    observed: float,
    unit: str,
    app_psc_predicted: Optional[float] = None,
    app_psc_precision_str: Optional[str] = None,
    app_psc_precision_ppm: Optional[float] = None,
    tier: str = "Tier 2",
    status: str = "PASS",
    reference_class: Optional[str] = None,
    derivational_closure: Optional[str] = None,
    tolerance_ppm: Optional[float] = None,
    discrepancy_notes: Optional[list] = None,
    extra: Optional[dict] = None,
) -> dict:
    """Build the standard result dict for a verification script.

    ``PASS`` is reserved for comparisons against an external empirical anchor.
    A manuscript-rounding/self-consistency check uses
    ``MANUSCRIPT_STATED`` + ``INTERNAL_ARITHMETIC_PASS``; an exact theorem or
    identity uses ``PURE_MATHEMATICAL`` + ``TIER1_EXACT`` (or the internal
    arithmetic status when the identity is not Tier 1).  This keeps a
    successful internal check from entering the empirical-PASS count.
    """
    from constants import ppm_error
    if reference_class is None:
        try:
            reference_class = REFERENCE_CLASS_BY_RESULT[name]
        except KeyError as exc:
            raise ValueError(
                f"result {name!r} has no declared reference_class; add it to "
                "REFERENCE_CLASS_BY_RESULT or pass reference_class explicitly"
            ) from exc
    allowed_reference_classes = {
        "EMPIRICAL_ANCHOR",
        "MANUSCRIPT_STATED",
        "PURE_MATHEMATICAL",
    }
    if reference_class not in allowed_reference_classes:
        raise ValueError(
            f"reference_class must be one of {sorted(allowed_reference_classes)}; "
            f"got {reference_class!r}"
        )
    if reference_class != "EMPIRICAL_ANCHOR" and status == "PASS":
        raise ValueError(
            "PASS is reserved for EMPIRICAL_ANCHOR comparisons; use "
            "INTERNAL_ARITHMETIC_PASS or TIER1_EXACT for internal checks"
        )
    independent_ppm = (
        ppm_error(predicted, observed)
        if observed not in (0, None) and predicted is not None
        else None
    )
    if reference_class != "EMPIRICAL_ANCHOR":
        band_outcome = "NOT_APPLICABLE"
    elif tolerance_ppm is None or independent_ppm is None:
        band_outcome = "NO_NUMERIC_VERIFIER_BAND"
    elif abs(independent_ppm) <= tolerance_ppm:
        band_outcome = "INSIDE_VERIFIER_BAND"
    else:
        band_outcome = "OUTSIDE_VERIFIER_BAND"
    if band_outcome == "OUTSIDE_VERIFIER_BAND" and status in {
        "PASS",
        "OPEN_CONDITIONAL",
    }:
        raise ValueError(
            f"status {status} contradicts OUTSIDE_VERIFIER_BAND for {name}"
        )
    if band_outcome == "INSIDE_VERIFIER_BAND" and status in {"TENSION", "FAIL"}:
        raise ValueError(
            f"status {status} contradicts INSIDE_VERIFIER_BAND for {name}"
        )
    if reference_class == "MANUSCRIPT_STATED" and status not in {
        "INTERNAL_ARITHMETIC_PASS",
        "OPEN_CONDITIONAL",
        "FAIL",
    }:
        raise ValueError(
            f"MANUSCRIPT_STATED result {name} has incompatible status {status}"
        )
    if reference_class == "PURE_MATHEMATICAL" and status not in {
        "TIER1_EXACT",
        "INTERNAL_ARITHMETIC_PASS",
        "OPEN_RESEARCH",
        "FAIL",
    }:
        raise ValueError(
            f"PURE_MATHEMATICAL result {name} has incompatible status {status}"
        )
    result = {
        "name": name,
        "app_psc_label": app_psc_label,
        "formula": formula,
        "tier": tier,
        "predicted": predicted,
        "observed": observed,
        "reference_class": reference_class,
        "band_outcome": band_outcome,
        "derivational_closure": derivational_closure or _closure_state(status),
        "unit": unit,
        "app_psc_predicted": app_psc_predicted,
        "app_psc_precision_str": app_psc_precision_str,
        "app_psc_precision_ppm": app_psc_precision_ppm,
        "independent_precision_ppm": independent_ppm,
        "status": status,
        "tolerance_ppm": tolerance_ppm,
        "discrepancy_notes": discrepancy_notes or [],
        "extra": extra or {},
    }
    # Auto-flag App-R-vs-independent disagreements (>10% relative gap on the
    # precision figure itself, when both are available).
    if (
        app_psc_precision_ppm is not None
        and independent_ppm is not None
        and abs(app_psc_precision_ppm) > 1.0
    ):
        gap = abs(independent_ppm - app_psc_precision_ppm) / max(app_psc_precision_ppm, 1.0)
        if gap > 0.10:
            result["discrepancy_notes"].append(
                f"App PSC precision quoted as {app_psc_precision_ppm:.1f} ppm; "
                f"independent re-derivation gives {independent_ppm:.1f} ppm "
                f"(rel. gap {gap * 100:.1f}%)."
            )
    return result


def _sanitize_nan(obj):
    """Recursively replace NaN/Inf floats with JSON-compliant alternatives
    so that the output validates under RFC 8259 (allow_nan=False)."""
    import math
    if isinstance(obj, float):
        if math.isnan(obj):
            return None  # serialize NaN as null
        if math.isinf(obj):
            return None  # serialize +/- inf as null
        return obj
    if isinstance(obj, dict):
        return {k: _sanitize_nan(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize_nan(v) for v in obj]
    if isinstance(obj, tuple):
        return [_sanitize_nan(v) for v in obj]
    return obj


def write_result(result: dict) -> Path:
    """Write a result JSON for a single verification script. NaN/Inf
    floats are serialized as JSON null (RFC 8259 compliance)."""
    path = RESULTS_DIR / f"{result['name']}.json"
    sanitized = _sanitize_nan(result)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(sanitized, f, indent=2, allow_nan=False)
    return path


def print_summary(result: dict) -> None:
    """Console pretty-print for a single verification result."""
    print("=" * 72)
    print(f"  [{result['name']}] {result['app_psc_label']}")
    print(f"  Formula           : {result['formula']}")
    print(f"  Tier              : {result['tier']}")
    pred = result["predicted"]
    obs = result["observed"]
    u = result["unit"]
    if pred is not None:
        print(f"  Independent       : {pred:.6g} {u}")
    if obs is not None:
        reference_label = {
            "EMPIRICAL_ANCHOR": "Observed",
            "MANUSCRIPT_STATED": "Manuscript ref.",
            "PURE_MATHEMATICAL": "Identity target",
        }.get(result.get("reference_class"), "Reference")
        print(f"  {reference_label:<18}: {obs:.6g} {u}")
    print(f"  Reference class   : {result.get('reference_class', 'UNCLASSIFIED')}")
    if result["independent_precision_ppm"] is not None:
        print(f"  |delta|/obs (ppm) : {result['independent_precision_ppm']:.2f} ppm")
    if result["app_psc_precision_str"]:
        print(f"  App PSC claims      : {result['app_psc_precision_str']}")
    print(f"  Status            : {result['status']}")
    for note in result["discrepancy_notes"]:
        print(f"  ! DISCREPANCY     : {note}")
    print("=" * 72)
