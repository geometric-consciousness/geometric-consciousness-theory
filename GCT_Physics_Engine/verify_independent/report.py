"""
report.py — Shared reporting utility for the independent verification harness.

A verification result captures, per App R claim:
    - name                : machine-readable identifier
    - app_r_label         : the label as it appears in App R
    - formula             : the GCT formula as derived independently from prose
    - predicted           : the value re-computed by this harness (independent)
    - observed            : the empirical anchor (CODATA / PDG)
    - app_r_predicted     : what App R claims the engine produces
    - app_r_precision     : what App R claims the precision is (ppm or % string)
    - independent_precision_ppm : what this harness measures
    - status              : PASS / FAIL / TENSION / TIER1_EXACT / INTERNAL_ARITHMETIC_PASS / OPEN_CONDITIONAL / PENDING-α-RESOLUTION / NOT_APPLICABLE
    - discrepancy_notes   : free-text flags for any inter-document inconsistency

PASS rule: |independent precision - engine-reported precision| within 100 ppm
of each other, AND independent value within tolerance for its tier.
FAIL: the independent re-derivation gives a materially different number.
"""

import json
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

RESULTS_DIR = Path(__file__).resolve().parent / "results"
RESULTS_DIR.mkdir(exist_ok=True, parents=True)


def make_result(
    name: str,
    app_r_label: str,
    formula: str,
    predicted: float,
    observed: float,
    unit: str,
    app_r_predicted: Optional[float] = None,
    app_r_precision_str: Optional[str] = None,
    app_r_precision_ppm: Optional[float] = None,
    tier: str = "Tier 2",
    status: str = "PASS",
    tolerance_ppm: Optional[float] = None,
    discrepancy_notes: Optional[list] = None,
    extra: Optional[dict] = None,
) -> dict:
    """Build the standard result dict for a verification script."""
    from constants import ppm_error
    independent_ppm = (
        ppm_error(predicted, observed)
        if observed not in (0, None) and predicted is not None
        else None
    )
    result = {
        "name": name,
        "app_r_label": app_r_label,
        "formula": formula,
        "tier": tier,
        "predicted": predicted,
        "observed": observed,
        "unit": unit,
        "app_r_predicted": app_r_predicted,
        "app_r_precision_str": app_r_precision_str,
        "app_r_precision_ppm": app_r_precision_ppm,
        "independent_precision_ppm": independent_ppm,
        "status": status,
        "tolerance_ppm": tolerance_ppm,
        "discrepancy_notes": discrepancy_notes or [],
        "extra": extra or {},
    }
    # Auto-flag App-R-vs-independent disagreements (>10% relative gap on the
    # precision figure itself, when both are available).
    if (
        app_r_precision_ppm is not None
        and independent_ppm is not None
        and abs(app_r_precision_ppm) > 1.0
    ):
        gap = abs(independent_ppm - app_r_precision_ppm) / max(app_r_precision_ppm, 1.0)
        if gap > 0.10:
            result["discrepancy_notes"].append(
                f"App R precision quoted as {app_r_precision_ppm:.1f} ppm; "
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
    print(f"  [{result['name']}] {result['app_r_label']}")
    print(f"  Formula           : {result['formula']}")
    print(f"  Tier              : {result['tier']}")
    pred = result["predicted"]
    obs = result["observed"]
    u = result["unit"]
    if pred is not None:
        print(f"  Independent       : {pred:.6g} {u}")
    if obs is not None:
        print(f"  Observed          : {obs:.6g} {u}")
    if result["independent_precision_ppm"] is not None:
        print(f"  |delta|/obs (ppm) : {result['independent_precision_ppm']:.2f} ppm")
    if result["app_r_precision_str"]:
        print(f"  App R claims      : {result['app_r_precision_str']}")
    print(f"  Status            : {result['status']}")
    for note in result["discrepancy_notes"]:
        print(f"  ! DISCREPANCY     : {note}")
    print("=" * 72)
