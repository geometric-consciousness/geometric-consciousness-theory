#!/usr/bin/env python3
"""Build and verify the canonical GCT figure inventory.

Published membership and order come from Markdown image embeds encountered by the
canonical content traversal. Stable figure identifiers come from asset filenames,
never from mutable line numbers or list positions.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable

sys.dont_write_bytecode = True

from _common import walk_content_files


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONTENT_CATALOG = PurePosixPath("content/Figures/GCT_Figures_Catalog_DETAILED.md")
OUTPUT_CATALOG = PurePosixPath("output/GCT_Figures_Catalog_DETAILED.md")
OUTPUT_MANIFEST = PurePosixPath("output/figures_manifest.json")
FIGURES_ROOT = PROJECT_ROOT / "content" / "Figures"

IMAGE_RE = re.compile(
    r"!\[(?P<description>[^\]]*)\]\((?P<target>content/Figures/[^)\r\n]+)\)"
)
ASSET_RE = re.compile(r"^content/Figures/(?:[^/]+/)*Figure (?P<id>[^/]+)\.svg$")
INTERNAL_ID_RE = re.compile(r"<title>\s*Figure\s+([^<]+?)\s*</title>", re.IGNORECASE)


@dataclass(frozen=True)
class PublishedFigure:
    figure_id: str
    description: str
    source_path: str
    svg_path: str
    pdf_path: str


@dataclass(frozen=True)
class UnembeddedPair:
    figure_id: str
    svg_path: str
    pdf_path: str
    internal_svg_id: str | None

    @property
    def identifier_conflict(self) -> bool:
        return self.internal_svg_id is not None and self.internal_svg_id != self.figure_id


def _posix_relative(path: Path) -> str:
    return path.resolve().relative_to(PROJECT_ROOT.resolve()).as_posix()


def _asset_id(svg_path: str) -> str:
    match = ASSET_RE.fullmatch(svg_path)
    if not match:
        raise ValueError(f"Figure embed is not a canonical SVG asset path: {svg_path}")
    return match.group("id")


def _canonical_content_files() -> Iterable[Path]:
    for kind, entry, _entry_level in walk_content_files():
        if kind != "FILE":
            continue
        path = Path(entry)
        if path.resolve() == (PROJECT_ROOT / CONTENT_CATALOG).resolve():
            continue
        yield path


def discover_published_figures() -> list[PublishedFigure]:
    figures: list[PublishedFigure] = []
    seen_ids: set[str] = set()
    seen_assets: set[str] = set()

    for source in _canonical_content_files():
        source_text = source.read_text(encoding="utf-8")
        source_path = _posix_relative(source)
        for match in IMAGE_RE.finditer(source_text):
            description = " ".join(match.group("description").split())
            svg_path = PurePosixPath(match.group("target").strip()).as_posix()
            figure_id = _asset_id(svg_path)
            pdf_path = str(PurePosixPath(svg_path).with_suffix(".pdf"))

            if figure_id in seen_ids:
                raise ValueError(f"Duplicate published figure ID: {figure_id}")
            if svg_path in seen_assets:
                raise ValueError(f"Duplicate published figure asset: {svg_path}")
            if not description:
                raise ValueError(f"Missing declarative description for {figure_id}")
            if not (PROJECT_ROOT / PurePosixPath(svg_path)).is_file():
                raise FileNotFoundError(f"Missing SVG for {figure_id}: {svg_path}")
            if not (PROJECT_ROOT / PurePosixPath(pdf_path)).is_file():
                raise FileNotFoundError(f"Missing PDF for {figure_id}: {pdf_path}")

            figures.append(
                PublishedFigure(
                    figure_id=figure_id,
                    description=description,
                    source_path=source_path,
                    svg_path=svg_path,
                    pdf_path=pdf_path,
                )
            )
            seen_ids.add(figure_id)
            seen_assets.add(svg_path)

    if not figures:
        raise ValueError("Canonical content traversal yielded no published figure embeds")
    return figures


def _asset_pairs() -> dict[str, tuple[str, str]]:
    svg_by_id: dict[str, str] = {}
    pdf_by_id: dict[str, str] = {}

    for path in sorted(FIGURES_ROOT.rglob("Figure *.svg")):
        relative = _posix_relative(path)
        figure_id = _asset_id(relative)
        if figure_id in svg_by_id:
            raise ValueError(f"Duplicate supplied SVG ID: {figure_id}")
        svg_by_id[figure_id] = relative

    for path in sorted(FIGURES_ROOT.rglob("Figure *.pdf")):
        relative = _posix_relative(path)
        figure_id = Path(relative).stem.removeprefix("Figure ")
        if figure_id in pdf_by_id:
            raise ValueError(f"Duplicate supplied PDF ID: {figure_id}")
        pdf_by_id[figure_id] = relative

    svg_only = sorted(set(svg_by_id) - set(pdf_by_id))
    pdf_only = sorted(set(pdf_by_id) - set(svg_by_id))
    if svg_only or pdf_only:
        raise ValueError(f"Unpaired figure assets: SVG-only={svg_only}, PDF-only={pdf_only}")

    return {figure_id: (svg_by_id[figure_id], pdf_by_id[figure_id]) for figure_id in svg_by_id}


def _internal_svg_id(svg_path: str) -> str | None:
    text = (PROJECT_ROOT / PurePosixPath(svg_path)).read_text(encoding="utf-8")
    match = INTERNAL_ID_RE.search(text)
    return html.unescape(match.group(1)).strip() if match else None


def discover_unembedded_pairs(
    published: list[PublishedFigure], pairs: dict[str, tuple[str, str]]
) -> list[UnembeddedPair]:
    published_ids = {figure.figure_id for figure in published}
    unknown = sorted(published_ids - set(pairs))
    if unknown:
        raise ValueError(f"Published IDs lack supplied asset pairs: {unknown}")

    return [
        UnembeddedPair(
            figure_id=figure_id,
            svg_path=pairs[figure_id][0],
            pdf_path=pairs[figure_id][1],
            internal_svg_id=_internal_svg_id(pairs[figure_id][0]),
        )
        for figure_id in sorted(set(pairs) - published_ids)
    ]


def render_catalog(
    published: list[PublishedFigure], unembedded: list[UnembeddedPair], pair_count: int
) -> str:
    lines = [
        "# GCT Figures — Published Inventory",
        "",
        "This catalog records figures embedded by the canonical manuscript traversal. "
        "Stable identifiers come from asset filenames, and every published entry has "
        "matching SVG and PDF assets.",
        "",
        f"- **Published figures:** {len(published)}",
        f"- **Supplied SVG/PDF pairs:** {pair_count}",
        f"- **Unembedded supplied pairs:** {len(unembedded)}",
        "",
    ]

    if unembedded:
        lines.extend(["## Unembedded supplied asset pairs", ""])
        for pair in unembedded:
            conflict = (
                f"; its SVG internally declares `Figure {pair.internal_svg_id}`, "
                "so the filename and internal identifiers conflict"
                if pair.identifier_conflict
                else ""
            )
            lines.append(
                f"- `{pair.figure_id}` — `{pair.svg_path}` and `{pair.pdf_path}` are not "
                f"embedded by the canonical manuscript traversal{conflict}."
            )
        lines.append("")

    lines.extend(["## Published figures", ""])
    for figure in published:
        lines.extend(
            [
                f"### Figure {figure.figure_id}",
                "",
                f"- **Description:** {figure.description}",
                f"- **Source:** `{figure.source_path}`",
                f"- **SVG:** `{figure.svg_path}`",
                f"- **PDF:** `{figure.pdf_path}`",
                "",
            ]
        )
    return "\n".join(lines)


def render_manifest(
    published: list[PublishedFigure], unembedded: list[UnembeddedPair], pair_count: int
) -> str:
    payload = {
        "schema_version": 1,
        "summary": {
            "published_figure_count": len(published),
            "supplied_pair_count": pair_count,
            "unembedded_pair_count": len(unembedded),
        },
        "published_figures": [
            {
                "id": figure.figure_id,
                "description": figure.description,
                "source_path": figure.source_path,
                "svg_path": figure.svg_path,
                "pdf_path": figure.pdf_path,
            }
            for figure in published
        ],
        "unembedded_asset_pairs": [
            {
                "id": pair.figure_id,
                "svg_path": pair.svg_path,
                "pdf_path": pair.pdf_path,
                "internal_svg_id": pair.internal_svg_id,
                "identifier_conflict": pair.identifier_conflict,
            }
            for pair in unembedded
        ],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def expected_outputs() -> dict[PurePosixPath, str]:
    published = discover_published_figures()
    pairs = _asset_pairs()
    unembedded = discover_unembedded_pairs(published, pairs)
    catalog = render_catalog(published, unembedded, len(pairs))
    manifest = render_manifest(published, unembedded, len(pairs))
    return {
        CONTENT_CATALOG: catalog,
        OUTPUT_CATALOG: catalog,
        OUTPUT_MANIFEST: manifest,
    }


def _forced_tests() -> None:
    assert _asset_id("content/Figures/Volume_1/Figure V1.1.1.svg") == "V1.1.1"
    try:
        _asset_id("content/Figures/Volume_1/not-a-figure.svg")
    except ValueError:
        pass
    else:
        raise AssertionError("Noncanonical asset path was accepted")

    conflict = UnembeddedPair("X.1", "a.svg", "a.pdf", "X.2")
    assert conflict.identifier_conflict
    consistent = UnembeddedPair("V1.1.1", "a.svg", "a.pdf", "V1.1.1")
    assert not consistent.identifier_conflict


def check_outputs(outputs: dict[PurePosixPath, str], output_root: Path) -> int:
    mismatches: list[str] = []
    for relative, expected in outputs.items():
        target = output_root / relative
        if not target.is_file():
            mismatches.append(f"missing: {relative.as_posix()}")
        elif target.read_text(encoding="utf-8") != expected:
            mismatches.append(f"stale: {relative.as_posix()}")
    if mismatches:
        for mismatch in mismatches:
            print(mismatch)
        return 1
    print("Figure inventory check passed")
    return 0


def write_outputs(outputs: dict[PurePosixPath, str], output_root: Path) -> None:
    for relative, content in outputs.items():
        target = output_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")
        print(target)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify generated files without writing")
    parser.add_argument(
        "--output-root",
        type=Path,
        help="write or check generated files beneath a separate root",
    )
    args = parser.parse_args()

    _forced_tests()
    outputs = expected_outputs()
    output_root = args.output_root.resolve() if args.output_root else PROJECT_ROOT
    if args.check:
        return check_outputs(outputs, output_root)
    write_outputs(outputs, output_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
