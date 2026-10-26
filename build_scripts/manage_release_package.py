#!/usr/bin/env python3
"""Validate the canonical PDF and write/check its deterministic release manifest."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import re
import subprocess
from pathlib import Path

from pypdf import PdfReader

from _common import METADATA, PROJECT_ROOT, walk_content_files


PDF_PATH = PROJECT_ROOT / "output" / METADATA["output_filename_pdf"]
TEX_PATH = PROJECT_ROOT / "output" / METADATA["output_filename_tex"]
MANIFEST_PATH = PROJECT_ROOT / "output" / "release_manifest.json"
FIGURES_DIR = PROJECT_ROOT / "content" / "Figures"
FULL_TITLE = "Geometric Consciousness Theory: A 6D-to-3D Projective Framework"
PDF_KEYWORDS = (
    "Geometric Consciousness Theory; 6D-to-3D projection; quasicrystal; "
    "falsifiability; verification"
)
EXPECTED_PAGES = 1149
REPOSITORY_BUILD_INPUTS = (
    PROJECT_ROOT / "build_scripts" / "compile_latex.py",
    PROJECT_ROOT / "build_scripts" / "_common.py",
    PROJECT_ROOT / "build_scripts" / "generate_index.py",
    PROJECT_ROOT / "build_scripts" / "requirements.txt",
    PROJECT_ROOT / "build_scripts" / "metadata.json",
    PROJECT_ROOT / "Geometric_Consciousness_Theory.md",
    PROJECT_ROOT / "_publish_prep" / "assets" / "gct_brand" / "gct_emblem.svg",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def normalized_text(text: str) -> str:
    """Normalize PDF extractor hyphen variants without hiding bad glyphs."""
    hyphens = text.translate({ord(char): "-" for char in "‐‑‒–−"})
    return re.sub(r"\s+", " ", hyphens).strip()


def command_version(args: list[str]) -> str:
    result = subprocess.run(args, capture_output=True, text=True, encoding="utf-8",
                            errors="replace", check=True)
    return result.stdout.splitlines()[0].strip()


def git_commit(ref: str) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--verify", f"{ref}^{{commit}}"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    require(result.returncode == 0, f"build-input commit does not resolve: {ref}")
    return result.stdout.strip()


def validate_build_input_commit(ref: str, files: dict[str, str]) -> str:
    resolved = git_commit(ref)
    head = git_commit("HEAD")
    ancestry = subprocess.run(
        ["git", "merge-base", "--is-ancestor", resolved, head],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    require(ancestry.returncode == 0,
            f"build-input commit is not an ancestor of HEAD: {resolved}")
    for relative in files:
        committed = subprocess.run(
            ["git", "rev-parse", f"{resolved}:{relative}"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        require(committed.returncode == 0,
                f"build input absent from commit {resolved}: {relative}")
        working = subprocess.run(
            ["git", "hash-object", f"--path={relative}", relative],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        require(working.returncode == 0,
                f"cannot hash working build input: {relative}")
        require(committed.stdout.strip() == working.stdout.strip(),
                f"build input differs from commit {resolved}: {relative}")
    return resolved


def build_input_manifest() -> dict:
    paths = set(REPOSITORY_BUILD_INPUTS)
    paths.update(
        path for kind, path, _level in walk_content_files() if kind == "FILE"
    )
    paths.update(FIGURES_DIR.rglob("*.svg"))
    ordered = sorted(paths, key=lambda path: path.relative_to(PROJECT_ROOT).as_posix())
    require(len(ordered) == len(paths), "duplicate release build input")

    files: dict[str, str] = {}
    aggregate = hashlib.sha256()
    for path in ordered:
        require(path.is_file(), f"missing release build input: {path}")
        relative = path.relative_to(PROJECT_ROOT).as_posix()
        digest = sha256(path)
        files[relative] = digest
        aggregate.update(f"{relative} {digest}\n".encode("utf-8"))
    require(len([path for path in files if path.endswith(".svg")]) == 41,
            "release build input must contain 40 figure SVGs plus the emblem")
    return {
        "count": len(files),
        "set_sha256": aggregate.hexdigest(),
        "files": files,
    }


def font_names(reader: PdfReader) -> set[str]:
    names: set[str] = set()
    for page in reader.pages:
        resources = page.get("/Resources")
        if not resources:
            continue
        fonts = resources.get_object().get("/Font")
        if not fonts:
            continue
        for font in fonts.get_object().values():
            obj = font.get_object()
            name = str(obj.get("/BaseFont", ""))
            names.add(name.lstrip("/").split("+")[-1])
    return names


def validate_pdf() -> dict:
    require(PDF_PATH.is_file(), f"missing canonical PDF: {PDF_PATH}")
    require(TEX_PATH.is_file(), f"missing canonical TeX: {TEX_PATH}")
    reader = PdfReader(PDF_PATH, strict=True)
    require(len(reader.pages) == EXPECTED_PAGES,
            f"page-count drift: {len(reader.pages)} != {EXPECTED_PAGES}")

    metadata = reader.metadata or {}
    expected_metadata = {
        "/Title": FULL_TITLE,
        "/Author": "Pablo González Acosta",
        "/Subject": "A 6D-to-3D Projective Framework",
        "/Keywords": PDF_KEYWORDS,
    }
    for key, value in expected_metadata.items():
        require(metadata.get(key) == value,
                f"PDF metadata drift for {key}: {metadata.get(key)!r}")

    page_sizes = {
        (round(float(page.mediabox.width), 2), round(float(page.mediabox.height), 2))
        for page in reader.pages
    }
    require(page_sizes == {(595.28, 841.89)}, f"non-A4 page geometry: {page_sizes}")

    first = normalized_text(reader.pages[0].extract_text() or "")
    second = normalized_text(reader.pages[1].extract_text() or "")
    third = normalized_text(reader.pages[2].extract_text() or "")
    for token in (METADATA["title"], METADATA["subtitle"], METADATA["author"],
                  f"Version {METADATA['version']}", "2026-10-26"):
        require(token in first, f"cover missing {token!r}")
    require("How to cite" not in first, "colophon leaked onto cover")
    for token in ("How to cite", METADATA["doi_concept"], METADATA["repo_url"],
                  METADATA["website"], METADATA["email"], METADATA["orcid"],
                  "CC-BY-4.0", "MIT"):
        require(token in second, f"colophon missing {token!r}")
    require("Contents" in third, "table of contents is not page 3")

    texts: list[str] = []
    annotation_count = 0
    for page in reader.pages:
        texts.append(page.extract_text() or "")
        annotations = page.get("/Annots")
        if annotations:
            annotation_count += len(annotations.get_object())
    text = "\n".join(texts)
    require("\u202f" not in text, "U+202F survived in extracted PDF text")
    require("\ufffd" not in text, "replacement glyph survived in extracted PDF text")
    normalized = normalized_text(text)
    for token in ("VOLUME 1", "VOLUME 2", "VOLUME 3", "The GCT Effective Action",
                  "Appendices", "Falsifiability Matrix", "Acknowledgments"):
        require(token in normalized, f"required publication landmark missing: {token}")
    require(annotation_count > 0, "PDF contains no link annotations")

    names = font_names(reader)
    for required in ("Georgia", "SegoeUI", "LatinModernMath-Regular-Identity-H"):
        require(any(required in name for name in names), f"required font absent: {required}")

    figure_svgs = sorted(FIGURES_DIR.rglob("*.svg"))
    figure_pdfs = sorted(FIGURES_DIR.rglob("*.pdf"))
    require(len(figure_svgs) == 40 and len(figure_pdfs) == 40,
            f"figure-pair count drift: {len(figure_svgs)}/{len(figure_pdfs)}")
    figure_pairs: dict[str, dict[str, str]] = {}
    for source in figure_svgs:
        target = source.with_suffix(".pdf")
        require(target.is_file(), f"missing figure PDF: {target}")
        figure_reader = PdfReader(target, strict=True)
        require(len(figure_reader.pages) > 0, f"empty figure PDF: {target}")
        relative = source.relative_to(PROJECT_ROOT).as_posix()
        figure_pairs[relative] = {
            "svg_sha256": sha256(source),
            "pdf": target.relative_to(PROJECT_ROOT).as_posix(),
            "pdf_sha256": sha256(target),
        }

    figure_digest = hashlib.sha256()
    for path in figure_pdfs:
        relative = path.relative_to(PROJECT_ROOT).as_posix()
        figure_digest.update(f"{relative} {sha256(path)}\n".encode("utf-8"))

    return {
        "page_count": len(reader.pages),
        "page_size_points": [595.28, 841.89],
        "bytes": PDF_PATH.stat().st_size,
        "sha256": sha256(PDF_PATH),
        "tex_sha256": sha256(TEX_PATH),
        "figure_pdf_count": len(figure_pdfs),
        "figure_set_sha256": figure_digest.hexdigest(),
        "figure_pairs": figure_pairs,
        "link_annotation_count": annotation_count,
        "font_families_verified": ["Georgia", "Segoe UI", "Latin Modern Math"],
        "u202f_count": 0,
        "replacement_glyph_count": 0,
    }


def build_manifest(build_input_commit: str) -> dict:
    pdf = validate_pdf()
    build_inputs = build_input_manifest()
    return {
        "schema_version": 2,
        "artifact": PDF_PATH.relative_to(PROJECT_ROOT).as_posix(),
        "build_input_commit": validate_build_input_commit(
            build_input_commit, build_inputs["files"]
        ),
        "build_inputs": build_inputs,
        "publication": {
            "title": FULL_TITLE,
            "version": METADATA["version"],
            "date": "2026-10-26",
        },
        "tools": {
            "python": platform.python_version(),
            "pandoc": command_version(["pandoc", "--version"]),
            "xelatex": command_version(["xelatex", "--version"]),
            "pypdf": importlib.metadata.version("pypdf"),
            "reportlab": importlib.metadata.version("reportlab"),
            "svglib": importlib.metadata.version("svglib"),
        },
        "pdf": pdf,
    }


def serialized(manifest: dict) -> str:
    return json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--verify-only", action="store_true")
    parser.add_argument("--build-input-commit")
    args = parser.parse_args()

    if args.verify_only:
        pdf = validate_pdf()
        print(f"PASS: release PDF acceptance ({pdf['page_count']} pages, "
              f"sha256 {pdf['sha256']})")
        return 0
    if args.write:
        require(args.build_input_commit is not None,
                "--write requires --build-input-commit from the reviewed input/tooling phase")
        expected = build_manifest(args.build_input_commit)
        MANIFEST_PATH.write_text(serialized(expected), encoding="utf-8", newline="\n")
        print(f"WROTE: {MANIFEST_PATH.relative_to(PROJECT_ROOT)}")
        return 0

    require(MANIFEST_PATH.is_file(), f"missing release manifest: {MANIFEST_PATH}")
    actual = MANIFEST_PATH.read_text(encoding="utf-8")
    parsed = json.loads(actual)
    build_input_commit = parsed.get("build_input_commit")
    require(isinstance(build_input_commit, str) and build_input_commit,
            "release manifest lacks build_input_commit")
    expected = build_manifest(build_input_commit)
    require(actual == serialized(expected), "release manifest is stale")
    print(f"PASS: release manifest ({expected['pdf']['sha256']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
