"""
build_app_psc.py - keep Appendix PSC's registry-disposition mirror in sync.

Appendix FSM is generated directly from `falsifiability_registry.json`. Appendix PSC
also contains hand-written prose and tables, so this sibling generator maintains a
bounded mirror block whose lines are emitted from each registry entry's
`disposition_text`. The `--check` mode reports whether the checked-in block
matches the registry.

Run:
    py -3.13 GCT_Physics_Engine/build_app_psc.py
    py -3.13 GCT_Physics_Engine/build_app_psc.py --check
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ENGINE_ROOT = Path(__file__).resolve().parent
MANUSCRIPT_ROOT = ENGINE_ROOT.parent
REGISTRY_PATH = ENGINE_ROOT / "falsifiability_registry.json"
APP_PSC_PATH = MANUSCRIPT_ROOT / "content" / "98_Global_Appendices" / "App_PSC_Precision_Scorecard.md"

START = "<!-- APP_PSC_REGISTRY_DISPOSITIONS_START -->"
END = "<!-- APP_PSC_REGISTRY_DISPOSITIONS_END -->"


def load_registry() -> dict:
    with REGISTRY_PATH.open(encoding="utf-8") as f:
        return json.load(f)


LONG_LABEL_CHARS = 100


def _label(entry_id: str, verifier: str) -> str:
    """Return the monospace `id` / `verifier` label for one mirror line.

    Long `path::function` verifier names cannot hyphenate inside a monospace
    span, so labels longer than LONG_LABEL_CHARS are emitted with explicit
    line-break opportunities between the id, the script path and the function.
    """
    if len(entry_id) + len(verifier) > LONG_LABEL_CHARS and "::" in verifier:
        path, function = verifier.split("::", 1)
        return f"`{entry_id}` / \\linebreak `{path}`::\\linebreak `{function}`"
    return f"`{entry_id}` / `{verifier}`"


_NON_ASCII_MATH = {
    "m_e·φ^11": r"$m_e\cdot\phi^{11}$",
    "|Δa_e^anom|": r"$|\Delta a_e^{\rm anom}|$",
}
_ASCII_MATH = re.compile(r"[_^]|!=|<=|>=|->|sqrt\(|\w\*|\*\w")


def _markdown_safe(text: str) -> str:
    """Set the registry's ASCII math and identifiers as code spans.

    `disposition_text` is plain ASCII (``phi^(-107)``, ``rho_above_sigma_crit^2``,
    ``|E_perp|^2 != phi^-2``). Copied into Markdown as prose, the underscores
    and carets printed raw beside typeset math, and pandoc read ``^...^`` pairs
    as superscript (v1.3.0 page QA: App PSC §PSC.10). Each such token, with
    any parenthesised group it opens, is emitted verbatim inside a code span,
    so the mirror reads as the registry text it is. The registry is unchanged.
    """
    words = text.split(" ")
    out: list[str] = []
    i = 0
    while i < len(words):
        word = words[i]
        if not word or word == "*" or not _ASCII_MATH.search(word):
            out.append(word)
            i += 1
            continue
        j, token = i, word
        while token.count("(") > token.count(")") and j + 1 < len(words) and j - i < 4:
            j += 1
            token += " " + words[j]
        core = token
        trail = ""
        while core and core[-1] in ".,;:":
            trail = core[-1] + trail
            core = core[:-1]
        lead = ""
        while core.startswith("(") and core.count("(") > core.count(")"):
            lead += "("
            core = core[1:]
        while core.endswith(")") and core.count(")") > core.count("("):
            trail = ")" + trail
            core = core[:-1]
        while core and core[-1] in ".,;:":
            trail = core[-1] + trail
            core = core[:-1]
        if core and re.search(r"[^\x00-\x7f]", core):
            # The monospace font has no lowercase Greek: a token with
            # non-ASCII symbols is set as mathematics (curated), or as escaped
            # literal text.
            core = _NON_ASCII_MATH.get(core) or re.sub(r"([_^*<>\\])", r"\\\1", core)
            out.append(f"{lead}{core}{trail}")
        else:
            out.append(f"{lead}`{core}`{trail}" if core else token)
        i = j + 1
    return " ".join(out)


def registry_lines(registry: dict) -> list[str]:
    lines = [
        START,
    ]
    for entry in registry["entries"]:
        disposition = entry.get("disposition_text")
        if not disposition:
            continue
        verifier = entry.get("verifier_name") or "no_verifier"
        lines.append(f"- {_label(entry['id'], verifier)}: {_markdown_safe(disposition)}")
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

    end_marker = "**END OF APPENDIX PSC**"
    if end_marker not in text:
        raise RuntimeError(f"Could not find {end_marker!r} insertion point in {APP_PSC_PATH}")
    before, after = text.split(end_marker, 1)
    return f"{before.rstrip()}\n\n{block}{end_marker}{after}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if Appendix PSC mirror diverges")
    args = parser.parse_args(argv)

    block = expected_block()
    current = APP_PSC_PATH.read_text(encoding="utf-8")
    updated = replace_or_insert(current, block)

    if args.check:
        if current != updated:
            print("FAIL: Appendix PSC registry-disposition mirror is stale", file=sys.stderr)
            return 1
        print("PASS: Appendix PSC registry-disposition mirror matches registry")
        return 0

    APP_PSC_PATH.write_text(updated, encoding="utf-8", newline="\n")
    count = sum(1 for line in block.splitlines() if line.startswith("- `"))
    print(f"Wrote Appendix PSC registry-disposition mirror ({count} entries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
