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


def natural_sort_key(path: Path):
    """Sort paths with numbers naturally (1, 2, 10 instead of 1, 10, 2)."""
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', path.name)]


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
            entries = sorted(list(directory.iterdir()), key=natural_sort_key)

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
