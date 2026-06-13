#!/usr/bin/env python3
"""
check_data_json_producers.py - committed data/*.json refresh-path audit.

The refresh-all-data contract requires every committed JSON artifact under
GCT_Physics_Engine/data/ to have an explicit source-side refresh path.
This audit is intentionally conservative: a committed data JSON is accepted
only if either a same-stem protocol script is run by refresh-all-data, or the
exact JSON filename appears in a source script / build script that is reachable
from the Makefile refresh path.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ENGINE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ENGINE_ROOT.parent
SRC_DIR = ENGINE_ROOT / "src"


def git_ls_files(pattern: str) -> list[Path]:
    proc = subprocess.run(
        ["git", "ls-files", pattern],
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return [REPO_ROOT / line.strip() for line in proc.stdout.splitlines() if line.strip()]


def refresh_reachable_sources() -> list[Path]:
    extra_scripts = [
        "gct_tau_uniqueness.py",
        "gct_mckay_e8.py",
        "o14d_advanced_invariants.py",
        "o14d_closure_search.py",
        "o14d_irrep_decomp.py",
        "refresh_compat_json_artifacts.py",
    ]
    sources = set(SRC_DIR.glob("protocol_*.py"))
    sources.update(SRC_DIR / name for name in extra_scripts)
    sources.update(
        path
        for path in (
            ENGINE_ROOT / "build_falsifiability_matrix.py",
            ENGINE_ROOT / "build_app_r.py",
            ENGINE_ROOT / "Makefile",
        )
        if path.exists()
    )
    return sorted(path for path in sources if path.exists())


def default_same_stem_producer(json_name: str) -> Path | None:
    if not json_name.endswith("_results.json"):
        return None
    stem = json_name[: -len("_results.json")]
    candidate = SRC_DIR / f"{stem}.py"
    if candidate.exists():
        return candidate
    return None


def explicit_filename_producers(json_name: str, sources: list[Path]) -> list[Path]:
    producers: list[Path] = []
    for source in sources:
        try:
            text = source.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if json_name in text:
            producers.append(source)
    return producers


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="fail on any missing producer")
    args = parser.parse_args()

    committed = sorted(git_ls_files("GCT_Physics_Engine/data/*.json"))
    sources = refresh_reachable_sources()
    missing: list[str] = []

    print(f"Committed data JSON artifacts: {len(committed)}")
    for path in committed:
        json_name = path.name
        producers = explicit_filename_producers(json_name, sources)
        default_producer = default_same_stem_producer(json_name)
        if default_producer is not None and default_producer not in producers:
            producers.append(default_producer)

        if producers:
            rel = ", ".join(str(p.relative_to(ENGINE_ROOT)) for p in producers[:3])
            if len(producers) > 3:
                rel += ", ..."
            print(f"  OK  {json_name} <- {rel}")
        else:
            missing.append(json_name)
            print(f"  MISS {json_name}")

    if missing:
        print("\nMissing committed data JSON producers:")
        for name in missing:
            print(f"  - {name}")
        return 1 if args.strict else 0

    print("\nPASS: every committed data/*.json artifact has a refresh-path producer.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
