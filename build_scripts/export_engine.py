#!/usr/bin/env python3
"""
GCT Physics Engine Exporter
============================
Concatenates all source files from GCT_Physics_Engine into a single
publication-ready Markdown reference document.

Usage: python build_scripts/export_engine.py
Output: GCT_Physics_Engine_Reference.md
"""

import os
from pathlib import Path

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
ENGINE_SRC_DIR = PROJECT_ROOT / "GCT_Physics_Engine" / "src"
ENGINE_CONFIG_DIR = PROJECT_ROOT / "GCT_Physics_Engine" / "config"
OUTPUT_FILE = PROJECT_ROOT / "GCT_Physics_Engine_Reference.md"

def export_engine():
    """Export all engine source files to a single Markdown document."""

    if not ENGINE_SRC_DIR.exists():
        print(f"[ERROR] Engine source directory not found: {ENGINE_SRC_DIR}")
        return False

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
        # Header
        out.write("# GCT Physics Engine — Complete Reference\n\n")
        out.write("**Source:** `GCT_Physics_Engine/src/` and `GCT_Physics_Engine/config/`\n\n")
        out.write("This document is auto-generated from the live engine sources via `build_scripts/export_engine.py`. Do not edit by hand; regenerate after any change to the engine sources.\n\n")
        out.write("---\n\n")

        # Table of Contents
        out.write("## Table of Contents\n\n")
        out.write("### Configuration Files\n")
        out.write("- `gct_constants.yaml` — Global physical constants\n\n")
        out.write("### Core Libraries (gct_*.py)\n")
        out.write("- Fundamental mathematical and geometric objects\n\n")
        out.write("### Protocol Verification Scripts (protocol_*.py)\n")
        out.write("- Experimental and theoretical validation protocols\n\n")
        out.write("---\n\n")

        # Export gct_constants.yaml
        yaml_file = ENGINE_CONFIG_DIR / "gct_constants.yaml"
        if yaml_file.exists():
            out.write("## Configuration: gct_constants.yaml\n\n")
            out.write("```yaml\n")
            with open(yaml_file, 'r', encoding='utf-8') as f:
                out.write(f.read())
            out.write("\n```\n\n")
            out.write("---\n\n")

        # Collect and sort Python files
        py_files = sorted([f for f in ENGINE_SRC_DIR.glob("*.py") if f.name != "__init__.py"])

        # Separate gct_*.py from protocol_*.py
        gct_files = [f for f in py_files if f.name.startswith("gct_")]
        protocol_files = [f for f in py_files if f.name.startswith("protocol_")]
        other_files = [f for f in py_files if not f.name.startswith(("gct_", "protocol_"))]

        # Export Core Libraries
        out.write("## Core Libraries\n\n")
        for py_file in gct_files:
            out.write(f"### {py_file.stem}\n\n")
            out.write(f"**File:** `{py_file.name}`\n\n")
            out.write("```python\n")
            with open(py_file, 'r', encoding='utf-8') as f:
                out.write(f.read())
            out.write("\n```\n\n")
            out.write("---\n\n")

        # Export Protocol Verification Scripts
        out.write("## Protocol Verification Scripts\n\n")
        for py_file in protocol_files:
            out.write(f"### {py_file.stem}\n\n")
            out.write(f"**File:** `{py_file.name}`\n\n")
            out.write("```python\n")
            with open(py_file, 'r', encoding='utf-8') as f:
                out.write(f.read())
            out.write("\n```\n\n")
            out.write("---\n\n")

        # Export Other Files
        if other_files:
            out.write("## Utility & Support Scripts\n\n")
            for py_file in other_files:
                out.write(f"### {py_file.stem}\n\n")
                out.write(f"**File:** `{py_file.name}`\n\n")
                out.write("```python\n")
                with open(py_file, 'r', encoding='utf-8') as f:
                    out.write(f.read())
                out.write("\n```\n\n")
                out.write("---\n\n")

        # Footer
        out.write("---\n\n")
        out.write("**End of GCT Physics Engine Reference**\n")
        out.write("For verification, run: `python GCT_Physics_Engine/src/verify_engine.py`\n")

    print(f"[SUCCESS] Engine reference exported to: {OUTPUT_FILE}")
    print(f"[INFO] File size: {OUTPUT_FILE.stat().st_size / 1024 / 1024:.2f} MB")
    return True

if __name__ == "__main__":
    success = export_engine()
    exit(0 if success else 1)
