"""Validate permanent Open-Problem and prediction-register identifiers.

The validator separates lifecycle state from scientific disposition.  Numeric
gaps are valid, while identifiers are unique, naturally ordered, resolvable,
and append-only relative to an explicitly supplied Git baseline.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path


ENGINE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ENGINE_ROOT.parent
REGISTRY = ENGINE_ROOT / "falsifiability_registry.json"
ORQ = REPO_ROOT / "content/98_Global_Appendices/App_ORQ_Research_Questions.md"
PRG = REPO_ROOT / "content/98_Global_Appendices/App_PRG_Prediction_Registry.md"
FSM = REPO_ROOT / "content/98_Global_Appendices/App_FSM_Falsifiability_Matrix.md"

ORQ_PATH = "content/98_Global_Appendices/App_ORQ_Research_Questions.md"
PRG_PATH = "content/98_Global_Appendices/App_PRG_Prediction_Registry.md"
FSM_PATH = "content/98_Global_Appendices/App_FSM_Falsifiability_Matrix.md"
REGISTRY_PATH = "GCT_Physics_Engine/falsifiability_registry.json"

P_ID = re.compile(r"P\.([1-9]\d*)(?:(?P<letters>[a-z]+)|-(?P<label>[a-z][a-z-]*))?\Z")
O_ID = re.compile(r"O\.([1-9]\d*)(?P<suffix>[a-z]+)?\Z")
C_ID = re.compile(r"C\.[A-Z][A-Z0-9_]*\Z")
S_ID = re.compile(r"S\.[a-z][a-z0-9_]*\Z")
VERSION = re.compile(r"v\d+\.\d+(?:\.\d+)*(?:[a-z])?\Z")
P_LIFECYCLES = {"ACTIVE", "CLOSED", "RETIRED"}
O_LIFECYCLES = {"OPEN", "PARTIAL", "RESERVED", "CLOSED"}
TERMINAL = {"CLOSED", "RETIRED"}
# Controlled prose compounds map to the permanent IDs they cite. Every other
# identifier-like tail is resolved at full-token scope and therefore fails if
# it is not registered. Range shorthands expand to every permanent row named.
P_PROSE_COMPOUNDS = {
    "P.7-equivalent": {"P.7"},
    "P.7c-e": {"P.7c", "P.7d", "P.7e"},
    "P.7c-g": {"P.7c", "P.7d", "P.7e", "P.7f", "P.7g"},
}
O_PROSE_COMPOUNDS = {
    token: {token.split("-", 1)[0]}
    for token in {
        "O.5-CKM", "O.12-negative", "O.12-positive", "O.14-governed",
        "O.21-class", "O.21-pending", "O.21-qualified",
        "O.23-conditional", "O.23-path-", "O.23-positive",
        "O.24-conditional", "O.26-dependent", "O.29-conditional",
        "O.29-positive", "O.31-style", "O.33-pending", "O.33-positive",
        "O.38-conditional", "O.38-dependent",
    }
}


def permanent_id_key(ident: str) -> tuple[int, int, int, str]:
    """Natural key: P/O numeric base first, then companion suffix."""
    pm = P_ID.fullmatch(ident)
    if pm:
        suffix = pm.group("letters") or (f"-{pm.group('label')}" if pm.group("label") else "")
        return (0, int(pm.group(1)), 0 if not suffix else 1, suffix)
    om = O_ID.fullmatch(ident)
    if om:
        suffix = om.group("suffix") or ""
        return (0, int(om.group(1)), 0 if not suffix else 1, suffix)
    if C_ID.fullmatch(ident):
        return (1, 0, 0, ident)
    if S_ID.fullmatch(ident):
        return (2, 0, 0, ident)
    return (9, 0, 0, ident)


def validate_sequence(ids: list[str], grammar: re.Pattern[str], label: str) -> list[str]:
    errors: list[str] = []
    for ident in ids:
        if not grammar.fullmatch(ident):
            errors.append(f"{label}: invalid identifier {ident!r}")
    for ident, count in Counter(ids).items():
        if count > 1:
            errors.append(f"{label}: duplicate identifier {ident!r} ({count}x)")
    for left, right in zip(ids, ids[1:]):
        if permanent_id_key(left) > permanent_id_key(right):
            errors.append(f"{label}: descending identifiers {left!r} then {right!r}")
    return errors


def validate_lifecycle(
    ident: str, status: object, closed_in: object, allowed: set[str], label: str
) -> list[str]:
    errors: list[str] = []
    if status not in allowed:
        errors.append(f"{label} {ident}: invalid lifecycle_status {status!r}")
        return errors
    if status in TERMINAL:
        if not isinstance(closed_in, str) or not VERSION.fullmatch(closed_in):
            errors.append(f"{label} {ident}: terminal status requires a valid closed_in version")
    elif closed_in is not None:
        errors.append(f"{label} {ident}: nonterminal status requires closed_in=null")
    return errors


# The inherited ORQ closed_in marks
# v1.4.40 / v1.4.45 / v1.4.112 were internal closure-cycle counters, not public
# versions: O.20, O.22 and O.31 are already "Closed" in the v1.0.0 release
# (git tag v1.0.0, content/98_Global_Appendices/App_H_Research_Questions.md).
# Only these exact (label, id) -> (old, new) rewrites are accepted; any other
# change to a terminal closed_in still fails the append-only check.
CLOSED_IN_CORRECTIONS: dict[tuple[str, str], tuple[str, str]] = {
    ("ORQ summary", "O.20"): ("v1.4.40", "v1.0.0"),
    ("ORQ summary", "O.22"): ("v1.4.45", "v1.0.0"),
    ("ORQ summary", "O.31"): ("v1.4.112", "v1.0.0"),
}


def validate_append_only(current: list[dict], baseline: list[dict], label: str) -> list[str]:
    errors: list[str] = []
    now = {item.get("id"): item for item in current if isinstance(item, dict)}
    for old in baseline:
        ident = old.get("id") if isinstance(old, dict) else None
        if ident not in now:
            errors.append(f"{label}: baseline identifier {ident!r} was removed or renumbered")
            continue
        old_status = old.get("lifecycle_status")
        if old_status in TERMINAL:
            new = now[ident]
            if new.get("lifecycle_status") != old_status:
                errors.append(f"{label} {ident}: terminal lifecycle status was changed")
            if new.get("closed_in") != old.get("closed_in"):
                allowed = CLOSED_IN_CORRECTIONS.get((label, ident))
                if allowed != (old.get("closed_in"), new.get("closed_in")):
                    errors.append(f"{label} {ident}: closed_in was changed")
    return errors


def prediction_citations(text: str) -> set[str]:
    """Return each P citation as one complete identifier-like token.

    The deliberately broad tail captures malformed case, underscore, unknown
    suffix, and trailing-junk forms.  The registry set-difference in ``run``
    then rejects them instead of silently accepting a valid numeric prefix.
    """
    candidates = {
        match.group(0)
        for match in re.finditer(
            r"(?<![A-Za-z0-9_])P\.\d+[A-Za-z0-9_-]*",
            text,
        )
    }
    citations = candidates - set(P_PROSE_COMPOUNDS)
    for token in candidates & set(P_PROSE_COMPOUNDS):
        citations.update(P_PROSE_COMPOUNDS[token])
    return citations


def open_problem_citations(text: str) -> set[str]:
    """Return each O citation as one complete identifier-like token."""
    candidates = {
        match.group(0)
        for match in re.finditer(
            r"(?<![A-Za-z0-9_])O\.\d+[A-Za-z0-9_-]*",
            text,
        )
    }
    citations = candidates - set(O_PROSE_COMPOUNDS)
    for token in candidates & set(O_PROSE_COMPOUNDS):
        citations.update(O_PROSE_COMPOUNDS[token])
    return citations


def _split_row(line: str) -> list[str]:
    protected = line.replace(r"\|", "\0PIPE\0")
    return [cell.strip().replace("\0PIPE\0", "|") for cell in protected.strip().strip("|").split("|")]


def parse_orq(text: str) -> tuple[list[dict], list[dict]]:
    summary: list[dict] = []
    for line in text.splitlines():
        if not re.match(r"^\| O\.\d", line):
            continue
        cells = _split_row(line)
        if len(cells) != 4:
            summary.append({"id": cells[0] if cells else "", "_schema_error": len(cells)})
            continue
        summary.append({
            "id": cells[0], "topic": cells[1], "lifecycle_status": cells[2],
            "closed_in": None if cells[3] == "—" else cells[3],
        })
    markers = [
        {"id": m.group(1), "lifecycle_status": m.group(2),
         "closed_in": None if m.group(3) == "-" else m.group(3)}
        for m in re.finditer(
            r"^<!-- ORQ-STATUS (O\.\d+[a-z]*) (OPEN|PARTIAL|RESERVED|CLOSED) closed_in=([^ ]+) -->$",
            text, re.M,
        )
    ]
    details = re.findall(r"^> \*\*Open Problem (O\.\d+[a-z]*):", text, re.M)
    for index, item in enumerate(markers):
        item["detail_id"] = details[index] if index < len(details) else None
    if len(details) != len(markers):
        markers.append({"_detail_count": len(details), "_marker_count": len(markers)})
    return summary, markers


def parse_table(text: str, header_first: str) -> tuple[list[str], dict[str, list[str]]]:
    header: list[str] = []
    rows: dict[str, list[str]] = {}
    for line in text.splitlines():
        cells = _split_row(line) if line.startswith("|") else []
        if cells and cells[0] == header_first:
            header = cells
        if cells and re.fullmatch(r"\*\*(?:P\.\d[^*]*|C\.[^*]+|S\.[^*]+)\*\*", cells[0]):
            rows[cells[0].strip("*")] = cells
    return header, rows


def _git_show(ref: str, path: str) -> str:
    proc = subprocess.run(
        ["git", "show", f"{ref}:{path}"], cwd=REPO_ROOT, text=True,
        encoding="utf-8", errors="replace", capture_output=True,
    )
    if proc.returncode:
        raise RuntimeError(f"cannot read baseline {ref}:{path}: {proc.stderr.strip()}")
    return proc.stdout


def _baseline_entries(ref: str) -> list[dict]:
    payload = json.loads(_git_show(ref, REGISTRY_PATH))
    return payload.get("entries", [])


def run(baseline_ref: str) -> list[str]:
    errors: list[str] = []
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    entries = registry.get("entries")
    if registry.get("schema_version") != "1.1" or not isinstance(entries, list):
        errors.append("falsifiability registry: expected schema_version 1.1 and entries list")
        entries = entries if isinstance(entries, list) else []
    ids = [item.get("id", "") if isinstance(item, dict) else "" for item in entries]
    grammar = re.compile(r"(?:" + P_ID.pattern[:-2] + r"|" + C_ID.pattern[:-2] + r"|" + S_ID.pattern[:-2] + r")\Z")
    errors.extend(validate_sequence(ids, grammar, "falsifiability registry"))
    for item in entries:
        if not isinstance(item, dict):
            errors.append("falsifiability registry: entry is not an object")
            continue
        for field in ("id", "lifecycle_status", "closed_in", "tier", "manuscript_ref", "falsification", "experiment", "timeframe"):
            if field not in item:
                errors.append(f"falsifiability registry {item.get('id', '<unknown>')}: missing required field {field}")
        errors.extend(validate_lifecycle(
            str(item.get("id", "")), item.get("lifecycle_status"), item.get("closed_in"),
            P_LIFECYCLES, "falsifiability registry",
        ))
    try:
        errors.extend(validate_append_only(entries, _baseline_entries(baseline_ref), "falsifiability registry"))
    except (RuntimeError, json.JSONDecodeError) as exc:
        errors.append(str(exc))

    summary, markers = parse_orq(ORQ.read_text(encoding="utf-8"))
    errors.extend(validate_sequence([x.get("id", "") for x in summary], O_ID, "ORQ summary"))
    errors.extend(validate_sequence([x.get("id", "") for x in markers if "id" in x], O_ID, "ORQ detail"))
    for item in summary:
        if "_schema_error" in item:
            errors.append(f"ORQ summary {item.get('id')}: expected four columns")
        else:
            errors.extend(validate_lifecycle(item["id"], item["lifecycle_status"], item["closed_in"], O_LIFECYCLES, "ORQ summary"))
    if any("_detail_count" in x for x in markers):
        errors.append("ORQ detail: status-marker/detail count mismatch")
    clean_markers = [x for x in markers if "id" in x]
    if [(x.get("id"), x.get("lifecycle_status"), x.get("closed_in")) for x in summary] != [
        (x.get("detail_id"), x.get("lifecycle_status"), x.get("closed_in")) for x in clean_markers
    ]:
        errors.append("ORQ summary/detail identifiers, order, lifecycle, or closed_in disagree")
    try:
        baseline_summary, _ = parse_orq(_git_show(baseline_ref, ORQ_PATH))
        errors.extend(validate_append_only(summary, baseline_summary, "ORQ summary"))
    except RuntimeError as exc:
        errors.append(str(exc))

    reg_by_id = {item["id"]: item for item in entries if isinstance(item, dict) and "id" in item}
    fsm_header, fsm_rows = parse_table(FSM.read_text(encoding="utf-8"), "ID")
    prg_header, prg_rows = parse_table(PRG.read_text(encoding="utf-8"), "Prediction ID")
    fsm_sequence = re.findall(r"^\| \*\*((?:P\.\d[^*]*|C\.[^*]+|S\.[^*]+))\*\* \|", FSM.read_text(encoding="utf-8"), re.M)
    prg_sequence = re.findall(r"^\| \*\*(P\.\d[^*]*)\*\* \|", PRG.read_text(encoding="utf-8"), re.M)
    errors.extend(validate_sequence(fsm_sequence, grammar, "FSM"))
    errors.extend(validate_sequence(prg_sequence, P_ID, "PRG subset"))
    for name, header in (("FSM", fsm_header), ("PRG", prg_header)):
        for required in ("Lifecycle Status", "Closed In"):
            if required not in header:
                errors.append(f"{name}: missing {required} column")
    if set(fsm_rows) != set(reg_by_id):
        errors.append("FSM identifiers do not exactly match the machine registry")
    prg_ids = list(prg_rows)
    if not set(prg_ids) <= set(reg_by_id):
        errors.append("PRG contains an identifier absent from the machine registry")
    for name, header, rows in (("FSM", fsm_header, fsm_rows), ("PRG", prg_header, prg_rows)):
        if "Lifecycle Status" not in header or "Closed In" not in header:
            continue
        for ident, cells in rows.items():
            entry = reg_by_id.get(ident)
            if entry is None:
                continue
            expected_closed = entry.get("closed_in") or "—"
            # Some inherited prose cells contain unescaped mathematical |x|.
            # Lifecycle columns are anchored at the table tail, independent of
            # those non-structural internal delimiters.
            actual_status, actual_closed = (cells[-3], cells[-2]) if name == "FSM" else (cells[-2], cells[-1])
            if actual_status != entry.get("lifecycle_status") or actual_closed != expected_closed:
                errors.append(f"{name} {ident}: lifecycle mirror disagrees with machine registry")

    content_text = "\n".join(path.read_text(encoding="utf-8") for path in sorted((REPO_ROOT / "content").rglob("*.md")))
    o_cited = open_problem_citations(content_text)
    p_cited = prediction_citations(content_text)
    o_defined = {x.get("id") for x in summary}
    p_defined = {x for x in reg_by_id if P_ID.fullmatch(x)}
    for ident in sorted(o_cited - o_defined, key=permanent_id_key):
        errors.append(f"unresolved Open Problem citation {ident}")
    for ident in sorted(p_cited - p_defined, key=permanent_id_key):
        errors.append(f"unresolved prediction citation {ident}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--baseline-ref", required=True, help="explicit local Git ref used for append-only comparison")
    args = parser.parse_args(argv)
    if not args.baseline_ref.strip():
        print("ERROR --baseline-ref must be a non-empty explicit local Git ref", file=sys.stderr)
        return 2
    errors = run(args.baseline_ref)
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 1
    print("PASS permanent registers: schema, mirrors, full-token references, and append-only baseline")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
