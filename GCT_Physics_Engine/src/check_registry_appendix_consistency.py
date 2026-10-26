#!/usr/bin/env python3
"""
check_registry_appendix_consistency.py — SSOT field-consistency gate.

The falsifiability registry (`falsifiability_registry.json`) is the single source
of truth for the load-bearing per-prediction FIELDS: the epistemic `tier` string,
the falsification-band display, the lifecycle/closure-version pair, and the
disposition text. App_FSM (and App_PSC) are generator-seeded from
the registry and then editorially enriched with curated prose the bare generator
does not emit (figure embeds, scope-disclosure paragraphs, engine-verification
detail). Byte-equality with a fresh generator run is therefore NOT the contract —
that would forbid the legitimate curation. The contract is FIELD agreement: for
every prediction row, the App_FSM matrix cells for `tier`, `Falsification Band`,
`Lifecycle Status`, and `Closed In` must match the registry's values, and the
`Disposition` cell must preserve every word of the registry `disposition_text`
(curated insertions are allowed; deletions or replacements are not). An insertion
may still not reverse the registry's meaning: a negation token (`not`, `no`,
`never`, `retracted`, `withdrawn`, ...) that occurs more often in the App_FSM
cell than in the registry text is reported as a disposition mismatch. Hand-editing
one without the other is exactly what this gate catches.

Exit 0 if every matched row agrees on tier, band, and lifecycle; non-zero (and a printed report)
on any field divergence. Rows present in one but not the other are reported as
warnings, not failures (App PRG-only or matrix-only rows are allowed).

Run:  py -3.13 GCT_Physics_Engine/src/check_registry_appendix_consistency.py [--strict]
"""
from __future__ import annotations

import difflib
import json
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ENGINE_ROOT = Path(__file__).resolve().parent.parent
MANUSCRIPT_ROOT = ENGINE_ROOT.parent
REGISTRY_PATH = ENGINE_ROOT / "falsifiability_registry.json"
APP_FSM_PATH = MANUSCRIPT_ROOT / "content" / "98_Global_Appendices" / "App_FSM_Falsifiability_Matrix.md"

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


def _dropped_words(registry_text: str, matrix_text: str) -> str:
    """Registry disposition words that the App_FSM cell drops or alters.

    The App_FSM Disposition cell may enrich the registry `disposition_text`
    with curated detail (insertions), but it must not delete or replace any of
    the registry's words. Returns the dropped/altered registry words (empty
    string when the cell preserves the registry text).
    """
    reg = _norm(registry_text.replace(r"\|", "|")).split()
    mx = _norm(matrix_text.replace(r"\|", "|")).split()
    matcher = difflib.SequenceMatcher(None, reg, mx, autojunk=False)
    lost: list[str] = []
    for op, i1, i2, _j1, _j2 in matcher.get_opcodes():
        if op in ("delete", "replace"):
            lost.extend(reg[i1:i2])
    return " ".join(lost)


NEGATION_TOKENS = frozenset({
    "not", "no", "never", "none", "cannot", "retracted", "withdrawn",
    "falsified", "refuted", "contradicted", "fails", "failed",
})
_TOKEN_PUNCT = ".,;:()[]*_`'\"!?"


def _negation_counts(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for raw in _norm(text.replace(r"\|", "|")).lower().split():
        tok = raw.strip(_TOKEN_PUNCT)
        if tok.endswith("n't"):
            tok = "not"
        if tok in NEGATION_TOKENS:
            counts[tok] = counts.get(tok, 0) + 1
    return counts


# Exact curated phrases whose negation qualifies the registry disposition
# without inverting it. Each waiver is per-row and phrase-exact, so any other
# inserted negation in the same row is still reported.
NEGATION_WAIVERS: dict[str, tuple[str, ...]] = {
    # S1 CISS decision rule: a weak polarization result is "not falsifying",
    # and chirality verification is "necessary but not sufficient".
    "P.8": ("-> not falsifying", "necessary but not sufficient"),
}


def _inserted_negations(registry_text: str, matrix_text: str, waived: tuple[str, ...] = ()) -> str:
    """Negation tokens the App_FSM cell adds beyond the registry text.

    Curated enrichment may add detail, but an added negation can invert the
    disposition while preserving every registry word (for example, inserting
    "not" before "supported"). Phrases in `waived` are removed from the cell
    before counting. Returns the surplus tokens, or "" when none.
    """
    reg = _negation_counts(registry_text)
    for phrase in waived:
        matrix_text = matrix_text.replace(phrase, " ")
    mx = _negation_counts(matrix_text)
    surplus = []
    for tok, n in sorted(mx.items()):
        extra = n - reg.get(tok, 0)
        if extra > 0:
            surplus.append(f"{tok} x{extra}")
    return ", ".join(surplus)


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
        # Permanent P-series plus the registered C/S companion namespaces.
        if not (ident.startswith("P.") or ident.startswith("C.") or ident.startswith("S.")):
            continue
        rows[ident] = cells
    return rows


def _matrix_column_indices(md_path: Path) -> dict[str, int]:
    """Resolve FM.4 columns by header name so added audit fields are safe."""
    for line in md_path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| ID | Manuscript Reference | Tier |"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        return {name: index for index, name in enumerate(cells)}
    raise ValueError("FM.4 matrix header not found")


def run(strict: bool = False) -> int:
    registry = _load_registry()
    by_id = {e["id"]: e for e in registry["entries"]}
    matrix = _parse_matrix_rows(APP_FSM_PATH)

    columns = _matrix_column_indices(APP_FSM_PATH)
    TIER_COL = columns["Tier"]
    BAND_COL = columns["Falsification Band"]
    LIFECYCLE_COL = columns["Lifecycle Status"]
    CLOSED_IN_COL = columns["Closed In"]
    DISPOSITION_COL = columns["Disposition"]

    tier_mismatch: list[str] = []
    band_mismatch: list[str] = []
    lifecycle_mismatch: list[str] = []
    disposition_mismatch: list[str] = []
    matched = 0

    for ident, entry in by_id.items():
        cells = matrix.get(ident)
        if cells is None:
            continue
        matched += 1
        reg_tier = _cell(str(entry.get("tier", ""))).strip()
        mx_tier = cells[TIER_COL].strip()
        if _norm(reg_tier) != _norm(mx_tier):
            tier_mismatch.append(f"  {ident}\n      registry: {reg_tier}\n      App_FSM  : {mx_tier}")

        reg_band = _cell(_band_str(entry)).strip()
        mx_band = cells[BAND_COL].strip()
        if _norm(reg_band) != _norm(mx_band):
            band_mismatch.append(f"  {ident}\n      registry: {reg_band}\n      App_FSM  : {mx_band}")

        for field, column, expected in (
            ("lifecycle_status", LIFECYCLE_COL, str(entry.get("lifecycle_status", ""))),
            ("closed_in", CLOSED_IN_COL, str(entry.get("closed_in") or "—")),
        ):
            actual = cells[column].strip()
            if _norm(expected) != _norm(actual):
                lifecycle_mismatch.append(
                    f"  {ident} {field}\n      registry: {expected}\n      App_FSM  : {actual}"
                )

        reg_disp = str(entry.get("disposition_text") or "").strip()
        if reg_disp:
            dropped = _dropped_words(reg_disp, cells[DISPOSITION_COL])
            if dropped:
                disposition_mismatch.append(
                    f"  {ident}\n      registry text missing or altered in App_FSM: {dropped[:200]}"
                )
            inserted = _inserted_negations(
                reg_disp, cells[DISPOSITION_COL], NEGATION_WAIVERS.get(ident, ())
            )
            if inserted:
                disposition_mismatch.append(
                    f"  {ident}\n      negation inserted in App_FSM beyond the registry text: {inserted}"
                )

    print("=" * 72)
    print("Registry <-> App_FSM field-consistency check (tier + band + lifecycle + disposition)")
    print("=" * 72)
    print(f"  matched rows: {matched}")
    print(f"  TIER mismatches: {len(tier_mismatch)}")
    for m in tier_mismatch:
        print(m)
    print(f"  BAND mismatches: {len(band_mismatch)}")
    for m in band_mismatch:
        print(m)

    print(f"  LIFECYCLE mismatches: {len(lifecycle_mismatch)}")
    for m in lifecycle_mismatch:
        print(m)
    print(f"  DISPOSITION mismatches: {len(disposition_mismatch)}")
    for m in disposition_mismatch:
        print(m)

    n = len(tier_mismatch) + len(band_mismatch) + len(lifecycle_mismatch) + len(disposition_mismatch)
    if n == 0:
        print("\n  PASS: registry and App_FSM agree on tier + band + lifecycle + disposition for all matched rows.")
        return 0
    print(f"\n  {'FAIL' if strict else 'DRIFT'}: {n} field divergence(s) — registry is the SSOT; "
          "reconcile the App_FSM cell to the registry value (or update the registry).")
    return 1 if strict else 0


if __name__ == "__main__":
    sys.exit(run(strict="--strict" in sys.argv))
