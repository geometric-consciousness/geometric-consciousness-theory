"""Strict uniqueness audit for publication-boundary registry IDs."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path


ENGINE_ROOT = Path(__file__).resolve().parents[1]
CHECKS = (
    {
        "path": ENGINE_ROOT / "falsifiability_registry.json",
        "container": "entries",
        "field": "id",
    },
    {
        "path": ENGINE_ROOT / "config" / "claim_registry.json",
        "container": None,
        "field": "claim_id",
    },
)


def load_items(path: Path, container: str | None) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        payload = json.load(f)
    if container is not None:
        payload = payload.get(container, [])
    if not isinstance(payload, list):
        raise TypeError(f"{path} does not contain a list at {container or '<root>'}")
    return payload


def audit_registry(path: Path, container: str | None, field: str, strict: bool) -> list[str]:
    errors: list[str] = []
    items = load_items(path, container)
    ids: list[str] = []
    for index, item in enumerate(items):
        value = item.get(field) if isinstance(item, dict) else None
        if value in (None, ""):
            if strict:
                errors.append(f"{path.relative_to(ENGINE_ROOT)}[{index}] missing {field}")
            continue
        if not isinstance(value, str):
            errors.append(f"{path.relative_to(ENGINE_ROOT)}[{index}] {field} is not a string")
            continue
        ids.append(value)

    counts = Counter(ids)
    for value, count in sorted(counts.items()):
        if count > 1:
            errors.append(f"{path.relative_to(ENGINE_ROOT)} duplicate {field}={value!r} ({count}x)")
    if not errors:
        print(f"OK {path.relative_to(ENGINE_ROOT)}: {len(ids)} unique {field} values")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="fail on missing IDs as well as duplicates")
    args = parser.parse_args(argv)

    errors: list[str] = []
    for check in CHECKS:
        errors.extend(audit_registry(check["path"], check["container"], check["field"], args.strict))
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
