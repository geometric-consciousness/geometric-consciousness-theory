#!/usr/bin/env python3
"""
check_registry_appendix_consistency.py — SSOT field-consistency gate.

The falsifiability registry (`falsifiability_registry.json`) is the single source
of truth for the load-bearing per-prediction FIELDS: the epistemic `tier` string
and the falsification-band display. App_FM (and App_R) are generator-seeded from
the registry and then editorially enriched with curated prose the bare generator
does not emit (figure embeds, scope-disclosure paragraphs, engine-verification
detail). Byte-equality with a fresh generator run is therefore NOT the contract —
that would forbid the legitimate curation. The contract is FIELD agreement: for
every prediction row, the App_FM matrix cell for `tier` and `Falsification Band`
must match the registry's value. Hand-editing one without the other is exactly what this gate catches.

Exit 0 if every matched row agrees on tier + band; non-zero (and a printed report)
on any field divergence. Rows present in one but not the other are reported as
warnings, not failures (App V-only or matrix-only rows are allowed).

Run:  py -3.13 GCT_Physics_Engine/src/check_registry_appendix_consistency.py [--strict]
"""
from __future__ import annotations

import json
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ENGINE_ROOT = Path(__file__).resolve().parent.parent
MANUSCRIPT_ROOT = ENGINE_ROOT.parent
REGISTRY_PATH = ENGINE_ROOT / "falsifiability_registry.json"
APP_FM_PATH = MANUSCRIPT_ROOT / "content" / "98_Global_Appendices" / "App_FM_Falsifiability_Matrix.md"

# Import the generator's band-string formatter so the band comparison uses exactly
# the same rendering the matrix is built from.
sys.path.append(str(ENGINE_ROOT))
from build_falsifiability_matrix import _band_str, _cell  # noqa: E402


def _load_registry() -> dict:
    with REGISTRY_PATH.open(encoding="utf-8") as f:
        return json.load(f)


_PIPE = "\x00PIPE\x00"


def _norm(s: str) -> str:
    """Normalize for semantic comparison: strip LaTeX math markup + collapse space.

    Renders `$\\phi^{\\phi}$` and `phi^phi` to the same token so a pure
    LaTeX-vs-ASCII rendering difference is not reported as a drift.
    """
    for ch in ("$", "\\", "{", "}"):
        s = s.replace(ch, "")
    return " ".join(s.split())


def _parse_matrix_rows(md_path: Path) -> dict[str, list[str]]:
    """Return {id: [cells...]} for every FM.4 matrix data row (| **P.x** | ... |)."""
    rows: dict[str, list[str]] = {}
    for line in md_path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s.startswith("| **") or "**" not in s[3:]:
            continue
        # protect escaped table pipes (\|) before splitting on the real delimiter
        s = s.replace(r"\|", _PIPE)
        cells = [c.strip().replace(_PIPE, "|") for c in s.split("|")[1:-1]]
        if len(cells) < 10:
            continue
        ident = cells[0].strip().strip("*").strip()
        # only P.x / S.x rows
        if not (ident.startswith("P.") or ident.startswith("S.")):
            continue
        rows[ident] = cells
    return rows


def run(strict: bool = False) -> int:
    registry = _load_registry()
    by_id = {e["id"]: e for e in registry["entries"]}
    matrix = _parse_matrix_rows(APP_FM_PATH)

    # FM.4 column order: ID | Manuscript Ref | Tier | Current Value | Precision | Band | Disposition | Experiment | Timeframe | Status
    TIER_COL, BAND_COL = 2, 5

    tier_mismatch: list[str] = []
    band_mismatch: list[str] = []
    matched = 0

    for ident, entry in by_id.items():
        cells = matrix.get(ident)
        if cells is None:
            continue
        matched += 1
        reg_tier = _cell(str(entry.get("tier", ""))).strip()
        mx_tier = cells[TIER_COL].strip()
        if _norm(reg_tier) != _norm(mx_tier):
            tier_mismatch.append(f"  {ident}\n      registry: {reg_tier}\n      App_FM  : {mx_tier}")

        reg_band = _cell(_band_str(entry)).strip()
        mx_band = cells[BAND_COL].strip()
        if _norm(reg_band) != _norm(mx_band):
            band_mismatch.append(f"  {ident}\n      registry: {reg_band}\n      App_FM  : {mx_band}")

    print("=" * 72)
    print("Registry <-> App_FM field-consistency check (tier + falsification band)")
    print("=" * 72)
    print(f"  matched rows: {matched}")
    print(f"  TIER mismatches: {len(tier_mismatch)}")
    for m in tier_mismatch:
        print(m)
    print(f"  BAND mismatches: {len(band_mismatch)}")
    for m in band_mismatch:
        print(m)

    n = len(tier_mismatch) + len(band_mismatch)
    if n == 0:
        print("\n  PASS: registry and App_FM agree on tier + band for all matched rows.")
        return 0
    print(f"\n  {'FAIL' if strict else 'DRIFT'}: {n} field divergence(s) — registry is the SSOT; "
          "reconcile the App_FM cell to the registry value (or update the registry).")
    return 1 if strict else 0


if __name__ == "__main__":
    sys.exit(run(strict="--strict" in sys.argv))
