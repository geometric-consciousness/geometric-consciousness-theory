"""
Shared helpers for the GCT build pipeline.

Provides:
  - METADATA dict (loaded from build_scripts/metadata.json)
  - natural_sort_key
  - parse_header_title
  - walk_content_files: yields (path, level) for every .md in the manifest order

Both compile_manuscript.py (markdown monolith) and compile_latex.py (PDF) use
this module so the source-of-truth ordering and metadata live in one place.
"""

import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
CONTENT_DIR = PROJECT_ROOT / "content"
METADATA_PATH = Path(__file__).parent / "metadata.json"

with open(METADATA_PATH, "r", encoding="utf-8") as _f:
    METADATA = json.load(_f)

ORDERED_SECTIONS = METADATA["ordered_sections"]
APPENDIX_ORDER = METADATA["appendix_order"]
APPENDIX_ORDER_INDEX = {
    appendix_id: index for index, appendix_id in enumerate(APPENDIX_ORDER)
}

# Files whose canonical reading position cannot be represented by natural
# filename sorting alone.  The effective-action bridge belongs after Chapter
# 4 even though its historical ``Ch04_00_`` filename sorts before Chapter 4.
# Keep the filename stable: chapter identifiers and external references must
# not be renumbered merely to control build traversal.
READ_AFTER = {
    "Ch04_00_Effective_Action_Bridge.md": "Ch04_Lattice_Dynamics.md",
}


def natural_sort_key(path: Path):
    """Sort paths with numbers naturally (1, 2, 10 instead of 1, 10, 2)."""
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', path.name)]


def ordered_directory_entries(directory: Path):
    """Return directory entries in canonical order."""
    entries = list(directory.iterdir())
    if directory == CONTENT_DIR / "98_Global_Appendices":
        def appendix_sort_key(path: Path):
            match = re.match(r"^App_([A-Z]+)_", path.name)
            if match:
                return (0, APPENDIX_ORDER_INDEX.get(match.group(1), len(APPENDIX_ORDER)))
            return (1, natural_sort_key(path))
        ordered = sorted(entries, key=appendix_sort_key)
    else:
        ordered = sorted(entries, key=natural_sort_key)

    # Apply explicit local reading-order constraints after the base sort.
    # A constraint is active only when both files are siblings in this
    # directory; unrelated directories therefore retain their natural order.
    by_name = {entry.name: entry for entry in ordered}
    for dependent_name, anchor_name in READ_AFTER.items():
        dependent = by_name.get(dependent_name)
        anchor = by_name.get(anchor_name)
        if dependent is None or anchor is None:
            continue
        ordered.remove(dependent)
        ordered.insert(ordered.index(anchor) + 1, dependent)
    return ordered


def parse_header_title(path: Path, level: int) -> str:
    """Turn a directory or file stem into a Markdown header line."""
    name = path.stem
    name = re.sub(r'^\d+_', '', name)
    name = name.replace("Volume_1", "VOLUME 1") \
               .replace("Volume_2", "VOLUME 2") \
               .replace("Volume_3", "VOLUME 3") \
               .replace("Volume_4", "VOLUME 4") \
               .replace("Global_Appendices", "APPENDICES") \
               .replace("Global Frontmatter", "") \
               .replace("Global Backmatter", "") \
               .replace("Part_", "Part ") \
               .replace("Ch", "Chapter ") \
               .replace("App_", "Appendix ") \
               .replace("_", " ")
    hashes = "#" * max(1, level)
    if name.strip() == "":
        return ""
    return f"{hashes} {name}\n\n"


def walk_content_files():
    """
    Yield every .md file under content/ in canonical reading order.

    Each yielded item is a (path, level) tuple where level is the directory
    nesting depth used for the markdown header that introduces the file.
    """
    def _walk(directory: Path, level: int):
        if level == 1 and directory == CONTENT_DIR:
            entries = []
            for section_name in ORDERED_SECTIONS:
                section_path = directory / section_name
                if section_path.exists():
                    entries.append(section_path)
                else:
                    print(f"[WARNING] Expected section not found: {section_name}",
                          file=sys.stderr)
        else:
            entries = ordered_directory_entries(directory)

        for entry in entries:
            if entry.name.startswith("."):
                continue
            if entry.name == "ignore_me.md":
                continue
            if entry.is_dir():
                yield ("DIR", entry, level)
                yield from _walk(entry, level + 1)
            elif entry.is_file() and entry.suffix == ".md":
                yield ("FILE", entry, level)

    yield from _walk(CONTENT_DIR, 1)
