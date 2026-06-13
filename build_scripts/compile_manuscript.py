"""
GCT Compiler
===========================
Manifest-free, directory-driven assembler for the Geometric Consciousness Theory.
Features live code injection for the Gauge Suite.

Usage: python3 compile_manuscript.py


Author: Pablo González Acosta
Date: February 28, 2026
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime

# FORCE UTF-8 OUTPUT (Windows Check)
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Shared helpers + metadata (single source of truth for both compilers)
from _common import (
    PROJECT_ROOT,
    CONTENT_DIR,
    METADATA,
    ORDERED_SECTIONS,
    natural_sort_key,
    parse_header_title,
)

# --- Configuration ---
OUTPUT_DIR = PROJECT_ROOT
ENGINE_SRC_DIR = PROJECT_ROOT / "GCT_Physics_Engine"
OUTPUT_FILENAME = METADATA["output_filename_md"]

def find_engine_file(filename: str) -> Path:
    """Recursively searches for a file in the engine source directory."""
    for path in ENGINE_SRC_DIR.rglob(filename):
        if path.is_file():
            return path
    return None

def inject_code(content: str) -> str:
    """
    Finds {{INJECT_CODE:filename.py}} markers and replaces them with 
    the actual file content wrapped in a python block.
    """
    pattern = r"\{\{INJECT_CODE:(.*?)\}\}"
    
    def replacer(match):
        filename = match.group(1).strip()
        file_path = find_engine_file(filename)
        
        if not file_path:
            print(f"[FATAL] Code Injection Failed: Missing file '{filename}'")
            print(f"        Searched in: {ENGINE_SRC_DIR}")
            sys.exit(1)
            
        print(f"      [INJECT] {filename} (from {file_path.parent.name})")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read().strip()
            
            ext = file_path.suffix.lower()
            lang = "python" if ext == ".py" else "json" if ext == ".json" else ""

            return f"\n```{lang}\n# [SOURCE: {filename}]\n{code}\n```\n"
        except Exception as e:
            print(f"[FATAL] Error reading '{filename}': {e}")
            sys.exit(1)

    return re.sub(pattern, replacer, content)

_processed_files: set = set()


def deduplicate_content(text: str) -> str:
    """
    Post-processes assembled text to remove duplicate consecutive content.
    Targets: duplicate callout blocks ([!NOTE], [!WARNING], etc.),
    duplicate section headers, and duplicate consecutive paragraphs
    introduced by source-file editing artifacts.
    """
    lines = text.split('\n')
    result = []
    i = 0
    prev_block_str = ""

    while i < len(lines):
        line = lines[i]

        # Detect block types: callout (> ...), section header (^#+), or regular line
        if line.startswith('> '):
            # Collect full callout block
            block = []
            while i < len(lines) and lines[i].startswith('> '):
                block.append(lines[i])
                i += 1
            block_str = '\n'.join(block)

            # Skip if identical to previous block
            if block_str != prev_block_str:
                result.extend(block)
                prev_block_str = block_str
            else:
                print(f"[DEDUP] Removed duplicate callout block ({len(block_str)} chars)")

        elif line.startswith('#') and (i == 0 or result[-1].strip() == ''):
            # Section header - check for duplicate
            header_line = line
            if result and result[-1].strip() == header_line:
                print(f"[DEDUP] Removed duplicate header: {header_line[:60]}")
                i += 1
            else:
                result.append(header_line)
                prev_block_str = ""
                i += 1

        else:
            result.append(line)
            if line.strip():
                prev_block_str = ""
            i += 1

    text = '\n'.join(result)

    # Pass 2: Remove duplicate consecutive paragraphs (separated by blank lines)
    paragraphs = re.split(r'(\n{2,})', text)
    deduped = []
    prev_para = None
    for token in paragraphs:
        stripped = token.strip()
        if stripped and stripped == prev_para:
            print(f"[DEDUP] Removed duplicate paragraph ({len(stripped)} chars)")
        else:
            deduped.append(token)
            if stripped:
                prev_para = stripped
    text = ''.join(deduped)

    # Pass 3: Remove excessive blank lines (more than 2 consecutive)
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text


def crawl_and_assemble(directory: Path, level: int = 1) -> str:
    """Recursively crawls the content directory."""
    global _processed_files
    assembled_content = ""
    entries = []
    
    if level == 1 and directory == CONTENT_DIR:
        print(f"Applying Root Order: {ORDERED_SECTIONS}")
        for section_name in ORDERED_SECTIONS:
            section_path = directory / section_name
            if section_path.exists():
                entries.append(section_path)
            else:
                print(f"[WARNING] Expected section not found: {section_name}")
    else:
        entries = sorted(list(directory.iterdir()), key=natural_sort_key)
    
    for entry in entries:
        if entry.name.startswith("."): continue # Skip hidden
        if entry.name == "ignore_me.md": continue 

        if entry.is_dir():
            print(f"{'  ' * level}📂 {entry.name}")
            assembled_content += parse_header_title(entry, level)
            assembled_content += crawl_and_assemble(entry, level + 1)
            if level == 1: 
                assembled_content += "\n\\newpage\n\n"
        
        elif entry.is_file() and entry.suffix == ".md":
            resolved_path = str(entry.resolve())
            if resolved_path in _processed_files:
                print(f"{'  ' * level}[DEDUP] Skipping already-processed: {entry.name}")
                continue
            _processed_files.add(resolved_path)
            print(f"{'  ' * level}📄 {entry.name}")
            try:
                with open(entry, "r", encoding="utf-8") as f:
                    file_content = f.read().strip()
                
                has_header = file_content.startswith("#")
                if not has_header:
                     file_header = parse_header_title(entry, level)
                     assembled_content += file_header

                if "{{INJECT_CODE" in file_content:
                    file_content = inject_code(file_content)

                if file_content.count("```") % 2 != 0:
                    print(f"[WARNING] Markdown Bleed detected in {entry.name}! Unclosed backticks.")
                    file_content += "\n```\n"

                assembled_content += file_content + "\n\n---\n\n" 
            except Exception as e:
                print(f"[ERROR] Could not read {entry.name}: {e}")
                sys.exit(1)

    return assembled_content

def main():
    print("="*60)
    print(f"GCT COMPILE | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    print(f"Root: {PROJECT_ROOT}")
    print(f"Engines: {ENGINE_SRC_DIR}")
    print("-" * 60)

    # 1. Start Assembly
    full_text = f"# {METADATA['title']}\n"
    full_text += f"**Author:** {METADATA['author']}\n"
    full_text += f"**Date:** {METADATA['date']}\n"
    full_text += f"**Version:** {METADATA['version']}\n\n---\n\n"

    print("Crawling content...")
    full_text += crawl_and_assemble(CONTENT_DIR)

    # 1b. Post-process: remove duplicate consecutive blocks
    print("Running deduplication pass...")
    full_text = deduplicate_content(full_text)

    # 2. Write Output
    OUTPUT_DIR.mkdir(exist_ok=True)
    outfile = OUTPUT_DIR / OUTPUT_FILENAME
    
    with open(outfile, "w", encoding="utf-8") as f:
        f.write(full_text)

    print("="*60)
    print(f"SUCCESS. Output written to:")
    print(f"{outfile}")
    print(f"Size: {outfile.stat().st_size / 1024:.2f} KB")
    print("="*60)

if __name__ == "__main__":
    main()
