#!/usr/bin/env python3
"""Set or check the release date at every place the release records it.

build_scripts/metadata.json is the source. This tool writes the same date to
the other places that carry it, and --check fails if any of them disagrees:

  build_scripts/metadata.json            "date": "Month D, YYYY"
  CITATION.cff                           date-released: YYYY-MM-DD
  CHANGELOG.md                           "## vX.Y.Z — YYYY-MM-DD" (current version)
  Geometric_Consciousness_Theory.md      "**Date:** Month D, YYYY" (monolith header)
  build_scripts/check_compile_latex_fixtures.py   pinned cover/colophon date,
                                         year and SOURCE_DATE_EPOCH
  build_scripts/manage_release_package.py         pinned cover date and
                                         manifest publication.date

The PDF title page and colophon read the date from metadata.json when
compile_latex.py runs, and the release manifest records it on
manage_release_package.py --write. So after this tool, rebuild the PDF and
rewrite the manifest, in this order:

  1. py -3.13 -X utf8 build_scripts/set_release_date.py --date YYYY-MM-DD
  2. py -3.13 -X utf8 build_scripts/manage_publication_metadata.py --check
     py -3.13 -X utf8 build_scripts/check_compile_latex_fixtures.py
  3. Commit the inputs (call the commit INPUTS).
  4. py -3.13 build_scripts/compile_latex.py        (full build)
  5. py -3.13 -X utf8 build_scripts/manage_release_package.py --write --build-input-commit INPUTS
  6. Commit the outputs, then run manage_release_package.py --verify-only and --check.

Usage:
  py -3.13 -X utf8 build_scripts/set_release_date.py --check
  py -3.13 -X utf8 build_scripts/set_release_date.py --date 2026-11-02 --dry-run
  py -3.13 -X utf8 build_scripts/set_release_date.py --date 2026-11-02
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
METADATA = ROOT / "build_scripts" / "metadata.json"
CITATION = ROOT / "CITATION.cff"
CHANGELOG = ROOT / "CHANGELOG.md"
MONOLITH = ROOT / "Geometric_Consciousness_Theory.md"
FIXTURES = ROOT / "build_scripts" / "check_compile_latex_fixtures.py"
RELEASE = ROOT / "build_scripts" / "manage_release_package.py"

MONTHS = ("January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December")


def long_form(day: date) -> str:
    return f"{MONTHS[day.month - 1]} {day.day}, {day.year}"


def parse_long_form(text: str) -> date:
    match = re.fullmatch(r"([A-Z][a-z]+) (\d{1,2}), (\d{4})", text)
    if not match or match.group(1) not in MONTHS:
        raise ValueError(f"metadata date is not 'Month D, YYYY': {text!r}")
    return date(int(match.group(3)), MONTHS.index(match.group(1)) + 1, int(match.group(2)))


def epoch(day: date) -> str:
    return str(int(datetime(day.year, day.month, day.day, tzinfo=timezone.utc).timestamp()))


def read(path: Path) -> str:
    return path.read_bytes().decode("utf-8")


def sites(day: date, version: str) -> list[tuple[Path, str, str, int]]:
    """(file, regex with one capture group per variable part, expected text, count)."""
    iso = day.isoformat()
    ver = re.escape(version)
    return [
        (METADATA, r'^  "date": "[^"\n]*",\r?$', f'  "date": "{long_form(day)}",', 1),
        (CITATION, r"^date-released: \S+\r?$", f"date-released: {iso}", 1),
        (CHANGELOG, rf"^## v{ver} — \S+\r?$", f"## v{version} — {iso}", 1),
        (MONOLITH, r"^\*\*Date:\*\* .*?\r?$", f"**Date:** {long_form(day)}", 1),
        (FIXTURES, r'^    require\(compiler\.publication_date_iso\(\) == "[^"]*", "date drift"\)\r?$',
         f'    require(compiler.publication_date_iso() == "{iso}", "date drift")', 1),
        (FIXTURES, r'^    require\(compiler\.source_date_epoch\(\) == "\d+", "source-date epoch drift"\)\r?$',
         f'    require(compiler.source_date_epoch() == "{epoch(day)}", "source-date epoch drift")', 1),
        (FIXTURES, rf'^                  metadata\["author"\], "Version {ver}", "[^"]*"\):\r?$',
         f'                  metadata["author"], "Version {version}", "{iso}"):', 1),
        (FIXTURES, r'^        "Version\.\}\\\\, ' + ver + r'", "Publication date\.\}\\\\, [^"]*", "\(\d{4}\)",\r?$',
         f'        "Version.}}\\\\, {version}", "Publication date.}}\\\\, {iso}", "({day.year})",', 1),
        (RELEASE, r'^                  f"Version \{METADATA\[\'version\'\]\}", "[^"]*"\):\r?$',
         f'                  f"Version {{METADATA[\'version\']}}", "{iso}"):', 1),
        (RELEASE, r'^            "date": "[^"]*",\r?$', f'            "date": "{iso}",', 1),
    ]


def current_state() -> tuple[date, str]:
    metadata = json.loads(read(METADATA))
    return parse_long_form(metadata["date"]), metadata["version"]


def check(day: date, version: str) -> list[str]:
    problems = []
    for path, pattern, expected, count in sites(day, version):
        lines = [m.group(0).rstrip("\r") for m in re.finditer(pattern, read(path), re.MULTILINE)]
        if len(lines) != count:
            problems.append(f"{path.relative_to(ROOT)}: expected {count} date site(s) for {pattern!r}, found {len(lines)}")
        elif any(line != expected for line in lines):
            problems.append(f"{path.relative_to(ROOT)}: {lines[0]!r} != {expected!r}")
    return problems


def apply(day: date, version: str, dry_run: bool) -> None:
    pending: dict[Path, str] = {}
    for path, pattern, expected, count in sites(day, version):
        text = pending.get(path, read(path))
        found = len(re.findall(pattern, text, re.MULTILINE))
        if found != count:
            raise SystemExit(f"ABORT {path.relative_to(ROOT)}: {found} matches for {pattern!r}, expected {count}; nothing written")

        def keep_eol(match: re.Match) -> str:
            return expected + ("\r" if match.group(0).endswith("\r") else "")

        pending[path] = re.sub(pattern, keep_eol, text, flags=re.MULTILINE)
    for path, text in pending.items():
        changed = text != read(path)
        print(f"{'WOULD WRITE' if dry_run else 'WROTE'}{'' if changed else ' (unchanged)'}: {path.relative_to(ROOT)}")
        if changed and not dry_run:
            path.write_bytes(text.encode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="fail if any date site disagrees with metadata.json")
    mode.add_argument("--date", help="new release date, YYYY-MM-DD")
    parser.add_argument("--dry-run", action="store_true", help="with --date: report, write nothing")
    args = parser.parse_args()

    current, version = current_state()
    if args.check:
        problems = check(current, version)
        for problem in problems:
            print("FAIL " + problem, file=sys.stderr)
        if problems:
            return 1
        print(f"PASS: every release-date site says {current.isoformat()} (v{version}, "
              f"SOURCE_DATE_EPOCH {epoch(current)})")
        return 0

    try:
        new = date.fromisoformat(args.date)
    except ValueError:
        raise SystemExit(f"--date must be YYYY-MM-DD, got {args.date!r}")
    problems = check(current, version)
    if problems:
        print("Refusing: the date sites already disagree before the change:", file=sys.stderr)
        for problem in problems:
            print("  " + problem, file=sys.stderr)
        return 1
    print(f"Release date {current.isoformat()} -> {new.isoformat()} (v{version})")
    apply(new, version, args.dry_run)
    if not args.dry_run:
        after = check(new, version)
        if after:
            for problem in after:
                print("FAIL " + problem, file=sys.stderr)
            return 1
        print("PASS: all date sites updated. Next: metadata and fixture checks, commit inputs, "
              "rebuild, manifest --write (see this script's docstring).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
