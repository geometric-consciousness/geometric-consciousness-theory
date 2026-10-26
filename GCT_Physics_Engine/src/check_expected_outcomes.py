#!/usr/bin/env python3
"""Check the preregistered engine outcomes and report scientific closure."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ENGINE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = ENGINE_DIR / "config" / "expected_outcomes.json"
DATA_DIR = ENGINE_DIR / "data"
ALLOWED_CLOSURE_STATES = {"confirmed", "open", "conditional", "tension"}


def _get_path(payload: dict[str, Any], path: str) -> Any:
    value: Any = payload
    for component in path.split("."):
        if not isinstance(value, dict) or component not in value:
            raise KeyError(path)
        value = value[component]
    return value


def _assertion_matches(payload: dict[str, Any], assertion: dict[str, Any]) -> tuple[bool, str]:
    path = assertion["path"]
    try:
        actual = _get_path(payload, path)
    except KeyError:
        return False, f"missing field {path}"

    if "equals" in assertion:
        expected = assertion["equals"]
        return actual == expected, f"{path}: expected {expected!r}, got {actual!r}"
    if "starts_with" in assertion:
        expected = assertion["starts_with"]
        return str(actual).startswith(expected), f"{path}: expected prefix {expected!r}, got {actual!r}"
    if "contains" in assertion:
        expected = assertion["contains"]
        return expected in str(actual), f"{path}: expected to contain {expected!r}, got {actual!r}"
    if "less_than" in assertion:
        expected = assertion["less_than"]
        return float(actual) < float(expected), f"{path}: expected < {expected!r}, got {actual!r}"
    if "greater_than" in assertion:
        expected = assertion["greater_than"]
        return float(actual) > float(expected), f"{path}: expected > {expected!r}, got {actual!r}"
    if "length" in assertion:
        expected = assertion["length"]
        valid = hasattr(actual, "__len__") and len(actual) == expected
        return valid, f"{path}: expected length {expected}, got {actual!r}"
    if "list_length" in assertion:
        expected = assertion["list_length"]
        valid = isinstance(actual, list) and len(actual) == expected
        return valid, f"{path}: expected list length {expected}, got {actual!r}"
    raise ValueError(f"unsupported assertion for {path}: {assertion}")


def check_expected_outcomes(
    expected_protocols: list[str] | None = None,
    manifest_path: Path = DEFAULT_MANIFEST,
) -> dict[str, Any]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    entries = manifest.get("protocols", [])
    failures: dict[str, list[str]] = {}

    header = manifest.get("_header", {})
    if not isinstance(header.get("safeguard"), str):
        failures.setdefault("manifest", []).append("missing safeguard header")
    if not isinstance(entries, list):
        return {
            "total": 0,
            "matched": 0,
            "scientific_closure": {},
            "failures": {"manifest": ["protocols must be an array"]},
        }
    names = [entry.get("protocol") for entry in entries]
    duplicates = sorted(name for name, count in Counter(names).items() if count > 1)
    if duplicates:
        failures.setdefault("manifest", []).append(
            f"duplicate protocol entries: {', '.join(duplicates)}"
        )
    expected_count = header.get("expected_protocol_count")
    if expected_count != len(entries):
        failures.setdefault("manifest", []).append(
            f"expected_protocol_count is {expected_count!r}, found {len(entries)} entries"
        )
    if expected_protocols is not None:
        missing = sorted(set(expected_protocols) - set(names))
        extra = sorted(set(names) - set(expected_protocols))
        if missing:
            failures.setdefault("manifest", []).append(
                f"missing protocol entries: {', '.join(missing)}"
            )
        if extra:
            failures.setdefault("manifest", []).append(
                f"entries not present in suite: {', '.join(extra)}"
            )

    closure_counts: Counter[str] = Counter()
    matched = 0
    for entry in entries:
        protocol = entry["protocol"]
        closure = entry["scientific_closure"]
        if closure not in ALLOWED_CLOSURE_STATES:
            failures.setdefault(protocol, []).append(
                f"invalid scientific_closure {closure!r}"
            )
            continue
        closure_counts[closure] += 1

        result_name = entry.get("result_json", protocol.replace(".py", "_results.json"))
        result_path = DATA_DIR / result_name
        if not result_path.is_file():
            failures.setdefault(protocol, []).append(f"missing result {result_name}")
            continue
        try:
            payload = json.loads(result_path.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError) as exc:
            failures.setdefault(protocol, []).append(
                f"unreadable result {result_name}: {exc}"
            )
            continue

        entry_failures = []
        for assertion in entry.get("assertions", []):
            ok, detail = _assertion_matches(payload, assertion)
            if not ok:
                entry_failures.append(detail)
        if entry_failures:
            failures.setdefault(protocol, []).extend(
                [f"expected {entry['expected_outcome']!r}: {failure}" for failure in entry_failures]
            )
        else:
            matched += 1

    return {
        "total": len(entries),
        "matched": matched,
        "scientific_closure": {
            status: closure_counts[status]
            for status in ("confirmed", "open", "conditional", "tension")
        },
        "failures": failures,
    }


def print_report(report: dict[str, Any]) -> None:
    counts = report["scientific_closure"]
    print(f"Suite Integrity: {report['matched']}/{report['total']} expected results")
    print(
        "Scientific Closure: "
        f"{counts.get('confirmed', 0)} confirmed · "
        f"{counts.get('open', 0)} open · "
        f"{counts.get('conditional', 0)} conditional · "
        f"{counts.get('tension', 0)} tension"
    )
    if report["failures"]:
        print("Outcome drift:")
        for protocol, protocol_failures in report["failures"].items():
            for failure in protocol_failures:
                print(f"  - {protocol}: {failure}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()
    report = check_expected_outcomes(manifest_path=args.manifest)
    print_report(report)
    return 1 if report["failures"] else 0


if __name__ == "__main__":
    sys.exit(main())
