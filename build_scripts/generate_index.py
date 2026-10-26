#!/usr/bin/env python3
"""Generate and verify the cross-volume Master Index.

Only files in the canonical manuscript traversal are indexable. The generated
index and companion figure catalog are explicitly excluded so build artifacts
cannot feed back into the index or leak filesystem paths into reader-facing
references.
"""
from __future__ import annotations

import argparse
import difflib
import re
import sys
from collections import defaultdict
from pathlib import Path

from _common import CONTENT_DIR, PROJECT_ROOT, walk_content_files


INDEX_OUTPUT = CONTENT_DIR / "99_Global_Backmatter" / "03_Master_Index.md"
FIGURES_CATALOG = CONTENT_DIR / "Figures" / "GCT_Figures_Catalog_DETAILED.md"
EXCLUDED_SOURCES = {INDEX_OUTPUT.resolve(), FIGURES_CATALOG.resolve()}

VOLUME_MAP = {
    "00_Global_Frontmatter": "GFM",
    "01_Volume_1_Operating_System": "V1",
    "02_Volume_2_Cosmic_Architecture": "V2",
    "03_Volume_3_Matter_Spectrum": "V3",
    "98_Global_Appendices": "App",
    "99_Global_Backmatter": "GBM",
}

# Publication scaffolding and epistemic/status labels are not concepts. Exact
# or anchored rules are intentional: a legitimate concept such as "Lattice
# Surface Tension" must survive merely containing a status word.
STRUCTURAL_LABELS = {
    "APPENDICES TO VOLUME 3", "BACK MATTER", "FRONT MATTER",
    "GLOBAL BACK MATTER", "GLOBAL FRONT MATTER",
}
GENERIC_LABELS = {
    "Description", "Index", "Index Volume 2", "Index Volume 3", "PDF",
    "Scope", "Scope/status", "Source", "Summary", "SVG", "What closed",
    "What closes", "Where it lives", "Where the analysis lives",
}
STATUS_LABELS = {
    "ACTIVE TENSION", "Fails", "GCT falsified", "Not closed",
    "OPEN_CONDITIONAL", "PASS", "Remaining open", "TENSION",
    "TENSION UNDER WP2025", "WITHHELD", "What does not close automatically",
}
EXACT_NOISE_LABELS = {
    value.casefold() for value in STRUCTURAL_LABELS | GENERIC_LABELS | STATUS_LABELS
}
OPEN_DEBT = re.compile(
    r"^(?:App ORQ )?Open Problem(?:\s|$)|^Open Research Debt(?:\s|$)|"
    r"^Open precision closure$|^Open dependency$|^O\.28$",
    re.IGNORECASE,
)
TIER_PREFIX = re.compile(
    r"^Tier-[0-4](?:(?:/|\+)\d)?\s+",
    re.IGNORECASE,
)
TIER_SUFFIX = re.compile(
    r"\s+[-—–]\s*Tier[- ]?[0-4](?:(?:/|\+)\d)?(?:\s+.*)?$",
    re.IGNORECASE,
)
TIER_LABEL = re.compile(r"(?:^|\b)Tier[- ]?[0-4](?:(?:/|\+)\d)?(?:\b|$)", re.IGNORECASE)
APPENDIX_POINTER = re.compile(r"^Appendix\s+[A-Z][A-Z0-9]*(?:\s*[§,]|\s+Section)")
VERDICT_LABEL = re.compile(r"^POSTDICTION-CONSISTENT(?:\s|$)", re.IGNORECASE)


def make_ref(path: Path) -> str:
    """Build an OS-independent reader reference for a canonical source path."""
    try:
        rel = path.resolve().relative_to(CONTENT_DIR.resolve())
    except ValueError as exc:
        raise ValueError(f"index source is outside content/: {path}") from exc
    if not rel.parts:
        raise ValueError(f"index source has no content namespace: {path}")
    top = rel.parts[0]
    try:
        volume = VOLUME_MAP[top]
    except KeyError as exc:
        raise ValueError(f"unknown index namespace {top!r}: {path}") from exc

    filename = rel.name.removesuffix(".md")
    match = re.match(r"(Ch\d+|App_[A-Z]+|\d\d_.*)", filename)
    if match:
        chapter = match.group(1)
        chapter = re.sub(r"^Ch(\d+).*", r"Ch\1", chapter)
        chapter = re.sub(r"^App_([A-Z]+).*", lambda m: "App " + m.group(1), chapter)
        chapter = re.sub(r"^\d\d_(.+)", r"\1", chapter)
        # Reader-facing titles, not file names.
        chapter = chapter.replace("_", " ")
        if chapter == volume or chapter.startswith(volume + " "):
            return chapter
        return f"{volume} {chapter}"
    return volume


def clean_term(term: str) -> str:
    """Normalize bounded adornments and terminal sentence punctuation."""
    term = re.sub(r"\$[^$]+\$", "", term)
    term = re.sub(r"\*+", "", term)
    term = TIER_PREFIX.sub("", term.strip())
    term = TIER_SUFFIX.sub("", term)
    term = re.sub(r"[(){}\[\]]", "", term)
    return term.strip().rstrip(" .:,;|")


def is_indexable_term(term: str) -> bool:
    """Apply the bounded, anchored publication-noise policy."""
    if term.casefold() in EXACT_NOISE_LABELS:
        return False
    if len(term) <= 3 and not re.fullmatch(r"[A-Z]{2,3}", term):
        return False
    if term.isdigit() or re.fullmatch(r"[\d\.\s]+", term):
        return False
    if (OPEN_DEBT.search(term) or TIER_LABEL.search(term)
            or APPENDIX_POINTER.search(term) or VERDICT_LABEL.search(term)):
        return False
    return True


def collect_terms(text: str, ref: str, index_map: dict[str, set[str]]) -> None:
    """Extract indexable terms from one canonical source."""
    for line in text.splitlines():
        for match in re.finditer(r"\*\*([A-Z][^*$\n]{2,60}?)\*\*\s*[:(]", line):
            term = clean_term(match.group(1))
            if is_indexable_term(term):
                index_map[term].add(ref)

        for match in re.finditer(r"(Theorem|Lemma|Corollary|Postulate)\s+([\d\.A-Z]+)", line):
            term = clean_term(f"{match.group(1)} {match.group(2)}")
            if is_indexable_term(term):
                index_map[term].add(ref)

        for match in re.finditer(r"Protocol\s+([A-Z][\w\-]*)", line):
            term = clean_term(f"Protocol {match.group(1)}")
            if is_indexable_term(term):
                index_map[term].add(ref)

        header = re.match(
            r"^#{2,4}\s+\*{0,2}([\d\.A-Z][\w\s\(\)\$\\,\-–]{3,60}?)\*{0,2}\s*$",
            line,
        )
        if header:
            term = clean_term(header.group(1))
            if is_indexable_term(term):
                index_map[term].add(ref)


def canonical_sources() -> list[Path]:
    """Return only canonical, non-generated manuscript sources."""
    sources: list[Path] = []
    for kind, path, _level in walk_content_files():
        if kind != "FILE" or path.resolve() in EXCLUDED_SOURCES:
            continue
        make_ref(path)  # validate namespace before consuming prose
        sources.append(path)
    return sources


def build_index_map(sources: list[Path] | None = None) -> dict[str, set[str]]:
    index_map: dict[str, set[str]] = defaultdict(set)
    for path in canonical_sources() if sources is None else sources:
        collect_terms(path.read_text(encoding="utf-8"), make_ref(path), index_map)
    return canonicalize_index_map(index_map)


def canonicalize_index_map(index_map: dict[str, set[str]]) -> dict[str, set[str]]:
    """Merge punctuation/case variants with deterministic display and ref union."""
    grouped: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    for raw_term, refs in index_map.items():
        term = clean_term(raw_term)
        if not term:
            continue
        grouped[term.casefold()][term].update(refs)

    canonical: dict[str, set[str]] = {}
    for variants in grouped.values():
        display = min(variants, key=lambda value: (value.casefold(), value))
        canonical[display] = set().union(*variants.values())
    return canonical


def render_index(index_map: dict[str, set[str]]) -> str:
    """Render an index with a platform-independent total order."""
    index_map = canonicalize_index_map(index_map)
    lines = [
        "### **Master Index (Cross-Volume)**\n", "\n",
        "*References use volume/chapter shorthand: V1 = Volume 1, V2 = Volume 2, V3 = Volume 3,*\n",
        "*App = Global Appendices, GFM = Global Front Matter, GBM = Global Back Matter.*\n", "\n",
    ]
    current_letter = ""
    for term in sorted(index_map, key=lambda value: (value.casefold(), value)):
        letters = re.sub(r"[^A-Za-z]", "", term)
        if not letters:
            continue
        first_letter = letters[0].upper()
        if first_letter != current_letter:
            current_letter = first_letter
            lines.append(f"\n#### **{current_letter}**\n\n")
        refs = sorted(index_map[term], key=lambda value: (value.casefold(), value))
        lines.append(f"* **{term}:** {', '.join(refs)}\n")
    return "".join(lines)


def expected_index() -> str:
    return render_index(build_index_map())


def index_is_fresh() -> bool:
    return INDEX_OUTPUT.is_file() and INDEX_OUTPUT.read_bytes() == expected_index().encode("utf-8")


def assert_index_fresh() -> None:
    """Fail a compiler before it can propagate a stale generated index."""
    if not index_is_fresh():
        raise RuntimeError(
            "Master Index is stale; run `py -3.13 build_scripts/generate_index.py` "
            "and commit the regenerated source before compiling"
        )


def check_index() -> int:
    expected = expected_index()
    if INDEX_OUTPUT.is_file() and INDEX_OUTPUT.read_bytes() == expected.encode("utf-8"):
        print(f"PASS Master Index is current ({len(build_index_map())} entries)")
        return 0
    actual = INDEX_OUTPUT.read_text(encoding="utf-8") if INDEX_OUTPUT.is_file() else ""
    print("ERROR Master Index is stale", file=sys.stderr)
    for line in difflib.unified_diff(
        actual.splitlines(), expected.splitlines(),
        fromfile=str(INDEX_OUTPUT.relative_to(PROJECT_ROOT)),
        tofile="expected generated index", n=2,
    ):
        print(line, file=sys.stderr)
    return 1


def write_index() -> int:
    index_map = build_index_map()
    INDEX_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    INDEX_OUTPUT.write_text(render_index(index_map), encoding="utf-8", newline="\n")
    print(f"SUCCESS: Master Index generated with {len(index_map)} entries -> {INDEX_OUTPUT}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="compare in memory; never write")
    args = parser.parse_args(argv)
    return check_index() if args.check else write_index()


if __name__ == "__main__":
    raise SystemExit(main())
