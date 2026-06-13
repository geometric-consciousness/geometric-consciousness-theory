"""
build_app_r.py - keep Appendix R's registry-disposition mirror in sync.

Appendix FM is generated directly from `falsifiability_registry.json`. Appendix R
also contains hand-written prose and tables, so this sibling generator maintains a
bounded mirror block whose lines are emitted from each registry entry's
`disposition_text`. The `--check` mode reports whether the checked-in block
matches the registry.

Run:
    py -3.13 GCT_Physics_Engine/build_app_r.py
    py -3.13 GCT_Physics_Engine/build_app_r.py --check
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ENGINE_ROOT = Path(__file__).resolve().parent
MANUSCRIPT_ROOT = ENGINE_ROOT.parent
REGISTRY_PATH = ENGINE_ROOT / "falsifiability_registry.json"
APP_R_PATH = MANUSCRIPT_ROOT / "content" / "98_Global_Appendices" / "App_R_Precision_Scorecard.md"

START = "<!-- APP_R_REGISTRY_DISPOSITIONS_START -->"
END = "<!-- APP_R_REGISTRY_DISPOSITIONS_END -->"


def load_registry() -> dict:
    with REGISTRY_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def registry_lines(registry: dict) -> list[str]:
    lines = [
        "### **R.10 Registry Disposition Mirror**",
        "",
        "This block is the Appendix R source-of-truth mirror for narrative disposition text. Each line is emitted from `GCT_Physics_Engine/falsifiability_registry.json::entries[*].disposition_text` so Appendix R and Appendix FM preserve identical registry dispositions.",
        "",
        START,
    ]
    for entry in registry["entries"]:
        disposition = entry.get("disposition_text")
        if not disposition:
            continue
        verifier = entry.get("verifier_name") or "no_verifier"
        lines.append(f"- `{entry['id']}` / `{verifier}`: {disposition}")
    lines.extend([END, ""])
    return lines


def expected_block() -> str:
    return "\n".join(registry_lines(load_registry()))


def replace_or_insert(text: str, block: str) -> str:
    if START in text and END in text:
        before, rest = text.split(START, 1)
        _, after = rest.split(END, 1)
        header = before.rstrip()
        if "### **R.10 Registry Disposition Mirror**" in header:
            marker = "### **R.10 Registry Disposition Mirror**"
            header = header[: header.rfind(marker)].rstrip()
        return f"{header}\n\n{block}{after.lstrip()}"

    end_marker = "**END OF APPENDIX R**"
    if end_marker not in text:
        raise RuntimeError(f"Could not find {end_marker!r} insertion point in {APP_R_PATH}")
    before, after = text.split(end_marker, 1)
    return f"{before.rstrip()}\n\n{block}{end_marker}{after}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if Appendix R mirror diverges")
    args = parser.parse_args(argv)

    block = expected_block()
    current = APP_R_PATH.read_text(encoding="utf-8")
    updated = replace_or_insert(current, block)

    if args.check:
        if current != updated:
            print("FAIL: Appendix R registry-disposition mirror is stale", file=sys.stderr)
            return 1
        print("PASS: Appendix R registry-disposition mirror matches registry")
        return 0

    APP_R_PATH.write_text(updated, encoding="utf-8", newline="\n")
    count = sum(1 for line in block.splitlines() if line.startswith("- `"))
    print(f"Wrote Appendix R registry-disposition mirror ({count} entries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
