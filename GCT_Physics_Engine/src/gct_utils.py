#!/usr/bin/env python3
"""
gct_utils.py - SSOT Interface (dot-accessible constants)
=========================================================
Provides: from gct_utils import C
Then use: C.PHI, C.ALPHA_INV_GCT, C.N, ...

Failure policy: sys.exit(1) if YAML cannot be loaded.
"""

import sys
import yaml
from pathlib import Path
from types import SimpleNamespace

# Force UTF-8 stdout/stderr at import time so protocol output (containing
# Greek letters phi, alpha, Delta, Gamma, approx-equal, sigma, +/-) does
# not raise UnicodeEncodeError on Windows consoles defaulting to cp1252.
for _stream_name in ("stdout", "stderr"):
    _stream = getattr(sys, _stream_name, None)
    if _stream is not None and hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

_YAML_PATH = (
    Path(__file__).resolve().parent     # src/
    .parent                              # GCT_Physics_Engine/
    / "config"
    / "gct_constants.yaml"
)


def _load_constants() -> SimpleNamespace:
    """Load YAML, flatten leaf `value` fields, return SimpleNamespace.

    Implementation note: the canonical SSOT YAML uses a flat layout where
    section headers (e.g. ``math:``), constant identifiers (``PHI:``), and
    metadata keys (``value:``, ``units:``, ``tier:``, ``notes:``, ``formula:``)
    are interleaved at the same indentation. PyYAML's safe_load would
    overwrite metadata across constants in that layout, so we re-parse
    line-by-line: every ``UPPERCASE_KEY:`` with an empty inline value is
    treated as a constant identifier, and the subsequent ``value:`` line
    (if any) before the next constant identifier supplies its numeric value.
    """

    if not _YAML_PATH.exists():
        print(f"FATAL [gct_utils]: YAML not found at {_YAML_PATH}", file=sys.stderr)
        sys.exit(1)

    try:
        text = _YAML_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"FATAL [gct_utils]: YAML read error:\n{exc}", file=sys.stderr)
        sys.exit(1)

    flat: dict = {}
    current_key = None  # the most recently seen constant identifier awaiting a value:
    section_re = ("math:", "fundamental:", "derived:", "calibrated:", "anchors:")

    for raw_line in text.splitlines():
        # Strip inline comments + trailing whitespace
        no_comment = raw_line.split("#", 1)[0].rstrip()
        if not no_comment.strip():
            continue
        stripped = no_comment.strip()

        # Section header (e.g. "math:") -- reset current_key
        if stripped in section_re:
            current_key = None
            continue

        # KEY: <inline-value>  OR  KEY: <empty>
        if ":" in stripped:
            key, _, after = stripped.partition(":")
            key = key.strip()
            after = after.strip()

            # Metadata keys land here -- bind their value to current_key (if numeric)
            if key in {"value"} and current_key is not None:
                try:
                    flat[current_key] = _coerce_scalar(after)
                except ValueError:
                    # Non-numeric value (e.g. string-shaped) -- store raw
                    flat[current_key] = after.strip("\"'")
                current_key = None
                continue
            if key in {"units", "tier", "formula", "notes", "source", "ref", "uncertainty_codata"}:
                # Metadata-only line we do not surface as a constant
                continue

            # Otherwise this is (likely) a constant identifier
            # Accept anything that is plausibly an identifier (uppercase / underscore / digits / mixed)
            if after == "" or after.startswith("|") or after.startswith(">"):
                current_key = key
                continue
            # KEY: <inline-value> case -- bind immediately
            try:
                flat[key] = _coerce_scalar(after)
                current_key = None
            except ValueError:
                # Could not parse as scalar; treat as identifier
                current_key = key

    if not flat:
        print("FATAL [gct_utils]: No constants extracted from YAML.", file=sys.stderr)
        sys.exit(1)

    return SimpleNamespace(**flat)


def _coerce_scalar(text: str):
    """Try to parse a YAML-ish scalar (int, float, sci-notation, bool, str).
    Raises ValueError on failure."""
    s = text.strip().strip("\"'")
    if s.lower() in {"true", "yes", "on"}:
        return True
    if s.lower() in {"false", "no", "off"}:
        return False
    if s.lower() == "null" or s == "":
        return None
    # Try int, then float
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        pass
    raise ValueError(f"not a scalar: {s!r}")


# -- module-level singleton ---------------------------------------------------
C = _load_constants()


# -- Utility Functions --------------------------------------------------------

def get_output_path(filename: str) -> Path:
    """Return absolute path to data/ or output/filename, creating dir if needed."""
    root = Path(__file__).resolve().parent.parent  # GCT_Physics_Engine/
    if filename.endswith('.json'):
        out_dir = root / "data"
    else:
        out_dir = root / "output"
    out_dir.mkdir(exist_ok=True)
    return out_dir / filename


class GCTReporter:
    """Simple reporter for protocol audits."""

    def __init__(self, title: str):
        self.title = title
        print("=" * 60)
        print(f"GCT Protocol Audit: {title}")
        print("=" * 60)

    def section(self, name: str):
        print(f"\n[{name}]")
        print("-" * 60)

    def log_value(self, label: str, value, unit: str = ""):
        if isinstance(value, float):
            val_str = f"{value:.6g}"
        else:
            val_str = str(value)
        print(f"{label:<40} : {val_str} {unit}")

    def log_comparison(self, label: str, predicted, observed):
        p_val = predicted if not isinstance(predicted, float) else f"{predicted:.6g}"
        o_val = observed if not isinstance(observed, float) else f"{observed:.6g}"

        print(f"{label:<40}")
        print(f"  Predicted: {p_val}")
        print(f"  Observed : {o_val}")

        try:
            diff = abs(float(predicted) - float(observed))
            ref = abs(float(observed))
            if ref > 0:
                err = (diff / ref) * 100
                print(f"  Error    : {err:.4f}%")
        except (ValueError, TypeError):
            pass

    def verdict(self, passed: bool, message: str):
        status = "PASSED" if passed else "FAILED"
        print("\n" + "=" * 60)
        print(f"VERDICT: {status}")
        print(f"Reason : {message}")
        print("=" * 60)


# -- convenience aliases (canonical SSOT consumers) ---------------------------
PHI = C.PHI
ALPHA_INV = C.ALPHA_INV_GCT
N_CAGE = C.N        # 144
M_E_MEV = C.M_E     # 0.5109989 MeV
M_E_OBS = C.M_E_OBS # observed target


if __name__ == "__main__":
    print(f"YAML loaded OK - {len(vars(C))} constants.")
    print(f"  PHI            = {PHI}")
    print(f"  ALPHA_INV_GCT  = {ALPHA_INV}")
    print(f"  N (cage)       = {N_CAGE}")
    print(f"  M_E            = {M_E_MEV} MeV")
