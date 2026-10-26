#!/usr/bin/env python3
"""Source-preparation fixtures for ``compile_latex.py``.

No repository PDF or TeX is authored. Conversion smoke tests create validated
PDFs and renders only inside disposable operating-system temporary directories.
"""

from __future__ import annotations

import io
import html
import json
import os
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from collections import Counter
from contextlib import redirect_stderr
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import compile_latex as compiler


ROOT = Path(__file__).resolve().parent.parent
COMPILER_SOURCE = ROOT / "build_scripts" / "compile_latex.py"
EMBLEM = ROOT / "_publish_prep" / "assets" / "gct_brand" / "gct_emblem.svg"
FSM = ROOT / "content" / "98_Global_Appendices" / "App_FSM_Falsifiability_Matrix.md"
MONOLITH = ROOT / "Geometric_Consciousness_Theory.md"
REQUIREMENTS = ROOT / "build_scripts" / "requirements.txt"
COLOPHON = ROOT / "content" / "99_Global_Backmatter" / "05_Colophon.md"
LABEL_FIGURES = (
    ROOT / "content" / "Figures" / "Volume_2" / "Figure V2.14.1.svg",
    ROOT / "content" / "Figures" / "Volume_3" / "Figure V3.13.1.svg",
    ROOT / "content" / "Figures" / "Volume_3" / "Figure V3.8.2.svg",
)
FIXTURE_LAYOUT_WHITESPACE_RE = re.compile(r"[ \t\r\n\f]+")


def fixture_visible_non_ascii_counts(svg_path: Path) -> Counter:
    """Independently derive visible SVG non-ASCII counts for fixture oracles."""
    root = ET.parse(svg_path).getroot()
    pieces = []

    def hidden(element: ET.Element, inherited: bool) -> bool:
        if inherited:
            return True
        style = {}
        for declaration in element.attrib.get("style", "").split(";"):
            if ":" in declaration:
                key, value = declaration.split(":", 1)
                style[key.strip().lower()] = value.strip().lower()
        display = element.attrib.get("display", style.get("display", "")).lower()
        visibility = element.attrib.get(
            "visibility", style.get("visibility", "")
        ).lower()
        opacity = element.attrib.get("opacity", style.get("opacity", "")).strip()
        return display == "none" or visibility in {"hidden", "collapse"} or opacity == "0"

    def text_tree(element: ET.Element, inherited: bool) -> None:
        suppressed = hidden(element, inherited)
        if not suppressed and element.text:
            pieces.append(element.text)
        for child in element:
            text_tree(child, suppressed)
            if not suppressed and child.tail:
                pieces.append(child.tail)

    def visit(element: ET.Element, inherited: bool = False) -> None:
        suppressed = hidden(element, inherited)
        if element.tag.rsplit("}", 1)[-1] == "text":
            text_tree(element, suppressed)
            return
        for child in element:
            visit(child, suppressed)

    visit(root)
    normalized = FIXTURE_LAYOUT_WHITESPACE_RE.sub(" ", "".join(pieces)).strip()
    return Counter(
        char for char in normalized if ord(char) > 127 and not char.isspace()
    )


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def check_publication_source() -> None:
    metadata = compiler.METADATA
    require(metadata["title"] == "Geometric Consciousness Theory", "title drift")
    require(metadata["subtitle"] == "A 6D-to-3D Projective Framework", "subtitle drift")
    require(metadata["author"] == "Pablo González Acosta", "author drift")
    require(metadata["version"] == "1.3.0", "version drift")
    require(compiler.publication_date_iso() == "2026-10-26", "date drift")
    require(compiler.source_date_epoch() == "1792972800", "source-date epoch drift")

    preamble = compiler.LATEX_PREAMBLE
    required = (
        "paperwidth=210mm", "paperheight=297mm", "left=18mm", "right=18mm",
        "top=16mm", "bottom=15mm", "\\ifPDFTeX", "\\usepackage{fontspec}",
        "\\IfFontExistsTF{Segoe UI}", "\\IfFontExistsTF{Arial}",
        "\\IfFontExistsTF{Georgia}", "\\IfFontExistsTF{Times New Roman}",
        "pdftitle={Geometric Consciousness Theory: A 6D-to-3D Projective Framework}",
        "pdfauthor={Pablo González Acosta}",
        "pdfsubject={A 6D-to-3D Projective Framework}",
        "pdfkeywords={Geometric Consciousness Theory; 6D-to-3D projection; quasicrystal; falsifiability; verification}",
    )
    for token in required:
        require(token in preamble, f"missing publication token: {token}")
    require("margin=1in" not in preamble, "generic geometry survived")
    require("mathpazo" not in preamble, "obsolete font package survived")

    cover = compiler.render_manual_cover("emblem-output-sentinel")
    require(cover.count(compiler.MANUAL_COVER_BEGIN) == 1, "manual cover count != 1")
    require(not cover.startswith("%"), "manual cover triggers pandoc percent-title syntax")
    require(
        compiler.MANUAL_COVER_BEGIN == r"\typeout{GCT_MANUAL_COVER_BEGIN}",
        "manual cover sentinel is not raw TeX",
    )
    for token in ("emblem-output-sentinel", metadata["title"], metadata["subtitle"],
                  metadata["author"], "Version 1.3.0", "2026-10-26"):
        require(token in cover, f"cover missing {token}")
    require("\\maketitle" not in cover, "manual cover invokes maketitle")

    source = COMPILER_SOURCE.read_text(encoding="utf-8")
    for token in ('f"title=', 'f"author=', 'f"date=', "\\\\maketitle"):
        require(token not in source, f"pandoc/template title mechanism survived: {token}")

    colophon = compiler.render_colophon()
    for token in (
        "Version.}\\, 1.3.0", "Publication date.}\\, 2026-10-26", "(2026)",
        metadata["doi_concept"], metadata["repo_url"], metadata["website"],
        metadata["email"], metadata["orcid"], "CC-BY-4.0", "MIT",
    ):
        require(token in colophon, f"colophon missing {token}")

    before_body = compiler.render_before_body("emblem-output-sentinel")
    require(before_body.count(compiler.MANUAL_COVER_BEGIN) == 1,
            "before-body cover count != 1")
    require(before_body.index(compiler.MANUAL_COVER_BEGIN) < before_body.index("Version.}"),
            "colophon precedes manual cover")

    declared = {
        line.strip() for line in REQUIREMENTS.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    require(
        declared == {
            "playwright==1.58.0", "pypdf==6.9.2",
            "reportlab==4.4.10", "svglib==1.6.0",
        },
        f"PDF/SVG dependency declaration drift: {sorted(declared)}",
    )

    colophon = COLOPHON.read_text(encoding="utf-8")
    for token in (
        "11 pt", "Georgia display headings", "Segoe UI body text",
        "Latin Modern Math", "custom GCT publication style",
    ):
        require(token in colophon, f"canonical colophon missing {token}")


def check_legacy_math_script_normalizer() -> None:
    source = (
        r"$\Gamma_\mathcal K+\Gamma_\mathcal{K}+"
        r"\dim_\mathbb R+\dim_\mathbb{R}+X^\mathcal P$"
    )
    expected = (
        r"$\Gamma_{\mathcal{K}}+\Gamma_{\mathcal{K}}+"
        r"\dim_{\mathbb{R}}+\dim_{\mathbb{R}}+X^{\mathcal{P}}$"
    )
    actual = compiler.preprocess_legacy_math_scripts(source)
    require(actual == expected, f"legacy math-script normalization drift: {actual!r}")
    require(
        compiler.preprocess_legacy_math_scripts(actual) == actual,
        "legacy math-script normalization is not idempotent",
    )


def check_pdf_chapter_title_qualifiers() -> None:
    source = (
        "## **Chapter 11: Dark Matter I (Topological Glass)**\n"
        "## **Chapter 1: The Phase Sector (U(1))**\n"
        "A prose reference to Chapter 11 (unchanged)."
    )
    expected = (
        "## **Chapter 11: Dark Matter I — Topological Glass**\n"
        "## **Chapter 1: The Phase Sector — $\\mathrm{U}(1)$**\n"
        "A prose reference to Chapter 11 (unchanged)."
    )
    actual = compiler.normalize_pdf_chapter_title_qualifiers(source)
    require(actual == expected, f"PDF chapter-title normalization drift: {actual!r}")
    require(
        compiler.normalize_pdf_chapter_title_qualifiers(actual) == actual,
        "PDF chapter-title normalization is not idempotent",
    )
    canonical = ROOT / "content" / "03_Volume_3_Matter_Spectrum" / \
        "01_Part_I_Forces" / "Ch01_Phase_Sector_U1.md"
    require("Chapter 1: The Phase Sector (U(1))" in canonical.read_text(encoding="utf-8"),
            "canonical Markdown chapter title was changed")


def check_generated_tex_trailing_whitespace() -> None:
    source = (
        b"first line  \r\n"
        b"internal  spacing\tkept\t\r\n"
        b"lf line \n"
        b"final tab\t"
    )
    expected = (
        b"first line\r\n"
        b"internal  spacing\tkept\r\n"
        b"lf line\n"
        b"final tab"
    )
    actual = compiler.trim_generated_tex_trailing_whitespace(source)
    require(actual == expected, "generated TeX trailing-whitespace trim drift")
    require(
        compiler.trim_generated_tex_trailing_whitespace(actual) == actual,
        "generated TeX trailing-whitespace trim is not idempotent",
    )


def check_terminal_backmatter_removal() -> None:
    source = b"colophon\r\n\\backmatter\r\n\\end{document}\r\n"
    expected = b"colophon\r\n\\end{document}\r\n"
    require(
        compiler.remove_redundant_terminal_backmatter(source) == expected,
        "terminal Pandoc backmatter removal drift",
    )
    for malformed in (
        b"colophon\n\\end{document}\n",
        b"colophon\n\\backmatter\ntrailing\n\\end{document}\n",
    ):
        try:
            compiler.remove_redundant_terminal_backmatter(malformed)
        except RuntimeError as exc:
            require("expected one terminal" in str(exc), "unclear backmatter failure")
        else:
            raise AssertionError("malformed terminal backmatter unexpectedly passed")


def check_figure_label_sizes() -> None:
    """Every SVG text label is 8.5--10 pt at the 174 mm placed width.

    SVG CSS px convert to 0.75 PostScript point.  Plain labels carry their
    final inline size; Matplotlib mathtext keeps its internal script ratios
    and scales the complete text run so its base label reaches the same band.
    """
    namespace = "{http://www.w3.org/2000/svg}"
    placed_width_pt = 174.0 * 72.0 / 25.4
    for path in LABEL_FIGURES:
        root = ET.parse(path).getroot()
        require(root.attrib["width"].endswith("pt"), f"non-pt SVG width: {path.name}")
        source_width_pt = float(root.attrib["width"][:-2])
        placement_scale = min(1.0, placed_width_pt / source_width_pt)
        measured: list[float] = []
        for text_node in root.iter(namespace + "text"):
            sizes = []
            for node in (text_node, *list(text_node)):
                sizes.extend(
                    float(value) for value in re.findall(
                        r"font-size:\s*([0-9.]+)px", node.attrib.get("style", "")
                    )
                )
            if not sizes:
                continue
            transform = text_node.attrib.get("transform", "")
            match = re.search(r"scale\(([0-9.]+)\)", transform)
            text_scale = float(match.group(1)) if match else 1.0
            measured.append(max(sizes) * 0.75 * placement_scale * text_scale)
        require(measured, f"no SVG labels found: {path.name}")
        require(min(measured) >= 8.5, f"undersized label in {path.name}: {min(measured):.4f} pt")
        require(max(measured) <= 10.0, f"oversized label in {path.name}: {max(measured):.4f} pt")


def _browser_svg_geometry(path: Path) -> dict:
    """Measure the actual SVG render tree with installed headless Chromium."""
    candidates = (
        Path(os.environ.get("PROGRAMFILES", r"C:\Program Files"))
        / "Google" / "Chrome" / "Application" / "chrome.exe",
        Path.home() / "AppData" / "Local" / "ms-playwright"
        / "chromium-1208" / "chrome-win64" / "chrome.exe",
    )
    chrome = next((candidate for candidate in candidates if candidate.is_file()), None)
    require(chrome is not None, "renderer-backed SVG check requires installed Chromium")
    svg = path.read_text(encoding="utf-8")
    script = r"""
<script>
const svg = document.querySelector('svg');
const root = svg.getBoundingClientRect();
const vb = svg.viewBox.baseVal;
const sx = vb.width / root.width, sy = vb.height / root.height;
function box(node) {
  const r = node.getBoundingClientRect();
  return [vb.x+(r.x-root.x)*sx, vb.y+(r.y-root.y)*sy, r.width*sx, r.height*sy];
}
const texts = [...svg.querySelectorAll('g[id^="text_"] text')].map(node => ({
  group: node.closest('g[id^="text_"]').id, box: box(node), value: node.textContent.trim()
}));
const shapes = {};
for (const node of svg.querySelectorAll('g[id^="patch_"],g[id^="line2d_"],g[id^="PathCollection_"]')) {
  shapes[node.id] = box(node);
}
const result = document.createElement('pre');
result.id = 'result';
result.textContent = JSON.stringify({x: vb.x, y: vb.y, width: vb.width, height: vb.height, texts, shapes});
document.body.appendChild(result);
</script>
"""
    with tempfile.TemporaryDirectory(prefix="gct-svg-render-") as directory:
        directory_path = Path(directory)
        html_path = directory_path / "fixture.html"
        html_path.write_text(f"<!doctype html><body>{svg}{script}</body>", encoding="utf-8")
        run = subprocess.run(
            [
                str(chrome), "--headless=new", "--disable-gpu", "--no-sandbox",
                f"--user-data-dir={directory_path / 'profile'}", "--dump-dom",
                html_path.resolve().as_uri(),
            ],
            capture_output=True, text=True, encoding="utf-8", timeout=30,
            check=False,
        )
        require(run.returncode == 0, f"Chromium SVG renderer failed for {path.name}: {run.stderr}")
        match = re.search(r'<pre id="result">(.*?)</pre>', run.stdout, re.DOTALL)
        require(match is not None, f"Chromium SVG geometry missing for {path.name}")
        return json.loads(html.unescape(match.group(1)))


def _union_boxes(boxes: list[list[float]]) -> tuple[float, float, float, float]:
    return (
        min(box[0] for box in boxes), min(box[1] for box in boxes),
        max(box[0] + box[2] for box in boxes), max(box[1] + box[3] for box in boxes),
    )


def _overlap(left, right, clearance=1.5) -> bool:
    return (
        min(left[2], right[2]) - max(left[0], right[0]) > clearance
        and min(left[3], right[3]) - max(left[1], right[1]) > clearance
    )


def _contains(outer, inner, padding=1.0) -> bool:
    return (
        inner[0] >= outer[0] + padding and inner[1] >= outer[1] + padding
        and inner[2] <= outer[2] - padding and inner[3] <= outer[3] - padding
    )


def check_figure_text_geometry() -> None:
    expected_group_counts = {
        "Figure V2.14.1.svg": 44,
        "Figure V3.13.1.svg": 18,
        "Figure V3.8.2.svg": 24,
    }
    required_groups = {
        "Figure V2.14.1.svg": {"text_16", "text_17", "text_18", "text_32", "text_33", "text_34", "text_35", "text_36", "text_42"},
        "Figure V3.13.1.svg": {"text_7", "text_9", "text_10", "text_11", "text_12", "text_13", "text_14", "text_16", "text_17"},
        "Figure V3.8.2.svg": {"text_11", "text_12", "text_13", "text_14", "text_15", "text_16", "text_18", "text_19", "text_20", "text_21", "text_22"},
    }
    required_tokens = {
        "Figure V2.14.1.svg": (
            "Equation of state $w(z)=P/\\rho$", "GCT: $w(z)\\leq -1$ for all plotted redshifts",
            "DESI CPL uncertainty band", "registered Class-2 envelope", "No literal", "phantom crossing",
        ),
        "Figure V3.13.1.svg": (
            "anaesthetic-modulation differential; no decisive gate; historical $N \\gtrsim 10^5$ design estimate",
            "anaesthetic-modulation differential; no decisive gate",
            "historical N ≳ 10⁵ design estimate; detection conditional on",
            "after Dicke integration: ∼500× below the cavity thermal floor",
            "(multimode) to SNR ∼6 (mode-matched); bracket-dependent, O.10",
        ),
        "Figure V3.8.2.svg": (
            "$a_\\mu$ residual after subtracting SM(WP2025), units of $10^{-11}$",
            "aμ residual after subtracting SM(WP2025), units of 10⁻¹¹",
            "$\\Delta a_\\mu^{GCT}$", "Δaμᴳᶜᵀ", "arbitration reopens a &gt;3σ gap",
            "protocol_qed_audit_results.json. Units are residuals in 10^-11.",
        ),
    }
    for path in LABEL_FIGURES:
        geometry = _browser_svg_geometry(path)
        canvas_x, canvas_y = geometry["x"], geometry["y"]
        width, height = geometry["width"], geometry["height"]
        fragments: dict[str, list[list[float]]] = {}
        for item in geometry["texts"]:
            fragments.setdefault(item["group"], []).append(item["box"])
        boxes = {group: _union_boxes(group_boxes) for group, group_boxes in fragments.items()}
        shape_boxes = {
            key: (value[0], value[1], value[0] + value[2], value[1] + value[3])
            for key, value in geometry["shapes"].items()
        }
        source = path.read_text(encoding="utf-8")
        require(len(boxes) == expected_group_counts[path.name], f"text-group count drift: {path.name}")
        for token in required_tokens[path.name]:
            require(token in source, f"scientific label token drift in {path.name}: {token}")
        require(required_groups[path.name] <= boxes.keys(), f"annotation/legend group drift: {path.name}")
        for group_id, box in boxes.items():
            require(
                box[0] >= canvas_x and box[1] >= canvas_y
                and box[2] <= canvas_x + width and box[3] <= canvas_y + height,
                f"text escapes canvas: {path.name}:{group_id} {box}",
            )
        semantic_groups = {
            "Figure V2.14.1.svg": required_groups[path.name] | {
                "text_11", "text_12", "text_13", "text_14", "text_15",
                "text_30", "text_31", "text_37", "text_38", "text_39", "text_40",
                "text_41", "text_43", "text_44",
            },
            "Figure V3.13.1.svg": required_groups[path.name] | {"text_15", "text_18"},
            "Figure V3.8.2.svg": required_groups[path.name] | {"text_23", "text_24"},
        }[path.name]
        items = [item for item in boxes.items() if item[0] in semantic_groups]
        for index, (left_id, left) in enumerate(items):
            for right_id, right in items[index + 1:]:
                overlap_x = min(left[2], right[2]) - max(left[0], right[0])
                overlap_y = min(left[3], right[3]) - max(left[1], right[1])
                require(
                    overlap_x <= 1.5 or overlap_y <= 1.5,
                    f"text overlap: {path.name}:{left_id}/{right_id} "
                    f"({overlap_x:.2f}, {overlap_y:.2f})",
                )
        for group_id, group_boxes in fragments.items():
            element_boxes = [
                (box[0], box[1], box[0] + box[2], box[1] + box[3])
                for box in group_boxes
            ]
            for index, left in enumerate(element_boxes):
                for right in element_boxes[index + 1:]:
                    require(not _overlap(left, right), f"intragroup overlap: {path.name}:{group_id}")

        containment = {
            "Figure V2.14.1.svg": {
                "text_18": "patch_10",
                "text_32": "patch_16", "text_33": "patch_16", "text_34": "patch_16",
                "text_35": "patch_16", "text_36": "patch_16", "text_42": "patch_22",
            },
            "Figure V3.13.1.svg": {
                "text_10": "patch_24", "text_13": "patch_31", "text_15": "patch_32",
                "text_16": "patch_32", "text_17": "patch_32",
            },
            "Figure V3.8.2.svg": {
                "text_18": "patch_15", "text_19": "patch_17", "text_20": "patch_19",
                "text_21": "patch_21",
            },
        }[path.name]
        for text_id, shape_id in containment.items():
            require(_contains(shape_boxes[shape_id], boxes[text_id]),
                    f"text leaves assigned shape: {path.name}:{text_id}/{shape_id}")

        exclusions = {
            "Figure V2.14.1.svg": {
                "text_38": ("PathCollection_2", "patch_19"),
                "text_39": ("PathCollection_3", "patch_19", "patch_20"),
                "text_40": ("PathCollection_4", "patch_20", "patch_21"),
                "text_41": ("PathCollection_5", "patch_21"),
            },
            "Figure V3.13.1.svg": {
                "text_10": ("patch_25",), "text_13": ("patch_30",),
            },
            "Figure V3.8.2.svg": {
                "text_18": ("patch_16",), "text_19": ("patch_16", "patch_18"),
                "text_20": ("patch_18", "patch_20"), "text_21": ("patch_20",),
            },
        }[path.name]
        for text_id, shape_ids in exclusions.items():
            for shape_id in shape_ids:
                require(not _overlap(boxes[text_id], shape_boxes[shape_id]),
                        f"text/shape collision: {path.name}:{text_id}/{shape_id}")


def check_figure_renderer_forced_negatives() -> None:
    """Prove the browser-backed gate catches representative reviewed regressions."""
    mutations = (
        (
            LABEL_FIGURES[0],
            'x="274" y="91">GCT:',
            'x="58.369734" y="52">GCT:',
            "text_18", "text_44", "overlap",
        ),
        (
            LABEL_FIGURES[0],
            'transform="translate(14.5 287.8255) rotate(-90)"',
            'transform="translate(28 287.8255) rotate(-90)"',
            "text_15", "text_11", "overlap",
        ),
        (
            LABEL_FIGURES[1],
            'x="58.0932" y="475">(multimode)',
            'x="58.0932" y="490">(multimode)',
            "text_17", "patch_32", "containment",
        ),
        (
            LABEL_FIGURES[2],
            'x="527.24" y="155">Add GCT vertex:',
            'x="527.24" y="120">Add GCT vertex:',
            "text_19", "patch_17", "containment",
        ),
    )
    with tempfile.TemporaryDirectory(prefix="gct-svg-negative-") as directory:
        directory_path = Path(directory)
        for index, (source_path, old, new, text_id, other_id, mode) in enumerate(mutations):
            source = source_path.read_text(encoding="utf-8")
            require(source.count(old) == 1, f"forced-negative mutation anchor drift: {source_path.name}")
            mutated = directory_path / f"negative-{index}.svg"
            mutated.write_text(source.replace(old, new), encoding="utf-8")
            geometry = _browser_svg_geometry(mutated)
            fragments: dict[str, list[list[float]]] = {}
            for item in geometry["texts"]:
                fragments.setdefault(item["group"], []).append(item["box"])
            text_box = _union_boxes(fragments[text_id])
            if mode == "overlap":
                other_box = _union_boxes(fragments[other_id])
                require(_overlap(text_box, other_box),
                        f"renderer failed to reproduce text collision: {source_path.name}")
            else:
                raw = geometry["shapes"][other_id]
                shape_box = (raw[0], raw[1], raw[0] + raw[2], raw[1] + raw[3])
                require(not _contains(shape_box, text_box),
                        f"renderer failed to reproduce shape escape: {source_path.name}")


def check_emblem_and_discovery() -> None:
    root = ET.parse(EMBLEM).getroot()
    require(root.attrib["width"] == "200" and root.attrib["height"] == "200", "emblem size drift")
    require(root.attrib["viewBox"] == "0 0 200 200", "emblem viewBox drift")
    require(root.attrib["fill"] == "none", "emblem fill drift")
    require(root.attrib["stroke"] == "currentColor", "emblem stroke drift")
    # Brand: soft copper, thin round line.
    # 1.25 user units at the cover's 20 mm width is ~0.35 pt (the print minimum).
    require(root.attrib["color"] == "#A8653A", "emblem colour is not brand copper")
    require(root.attrib["stroke-width"] == "1.25", "emblem stroke width drift")
    require(root.attrib["stroke-linecap"] == "round" and root.attrib["stroke-linejoin"] == "round",
            "emblem line caps/joins are not round")
    ns = {"s": "http://www.w3.org/2000/svg"}
    polygon = root.find("s:polygon", ns)
    paths = root.findall("s:path", ns)
    require(polygon is not None and polygon.attrib["points"] ==
            "100,12 178,60 178,140 100,188 22,140 22,60", "emblem polygon drift")
    require(len(paths) == 2, "emblem path count drift")
    require(paths[0].attrib["d"] ==
            "M100,12 L100,188 M22,60 L178,140 M178,60 L22,140", "diameter geometry drift")
    require(paths[1].attrib["d"] ==
            "M100,100 L100,12 M100,100 L178,60 M100,100 L178,140 M100,100 L100,188 M100,100 L22,140 M100,100 L22,60",
            "ray geometry drift")
    figures = sorted((ROOT / "content" / "Figures").rglob("*.svg"))
    require(len(figures) == 40, f"expected 40 figure SVGs, found {len(figures)}")

    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        second = root / "b" / "second.svg"
        first = root / "a" / "first.svg"
        second.parent.mkdir(parents=True)
        first.parent.mkdir(parents=True)
        second.write_text("second", encoding="utf-8")
        first.write_text("first", encoding="utf-8")
        calls: list[tuple[Path, Path]] = []

        def convert(source: str, pdf_path: Path | None = None) -> str:
            calls.append((Path(source), Path(pdf_path)))
            return str(pdf_path)

        with mock.patch.object(compiler, "convert_svg_to_pdf", side_effect=convert):
            discovered = compiler.prepare_all_figure_pdfs(root)
        require(discovered == [first, second], "figure traversal is not stable/sorted")
        require(
            calls == [(first, first.with_suffix(".pdf")),
                      (second, second.with_suffix(".pdf"))],
            f"full figure conversion coverage drift: {calls}",
        )
        with mock.patch.object(compiler, "convert_svg_to_pdf") as duplicate, \
             mock.patch.object(compiler, "validate_pdf_file") as validate:
            require(
                compiler.convert_figure_svg_for_build(first) == str(first.with_suffix(".pdf")),
                "prepared figure reuse returned wrong target",
            )
            duplicate.assert_not_called()
            validate.assert_called_once_with(first.with_suffix(".pdf"))


def check_unicode_boundary() -> None:
    require("\u202f" not in FSM.read_text(encoding="utf-8"), "U+202F remains in FSM")
    require("\u202f" not in MONOLITH.read_text(encoding="utf-8"), "U+202F remains in monolith")


def check_fsm_landscape_table() -> None:
    """The 15-column FM.4 matrix must never fall back to portrait auto-sizing."""
    header = [
        "ID", "Manuscript Reference", "Tier", "Reference Class", "Current Value",
        "Precision (ppm)", "Falsification Band", "Band Outcome",
        "Derivational Closure", "Disposition", "Experiment", "Timeframe",
        "Lifecycle Status", "Closed In", "Status",
    ]
    separator = [":---"] * len(header)
    row = ["fixture"] * len(header)
    source = "\n".join(
        "| " + " | ".join(cells) + " |"
        for cells in (header, separator, row)
    )
    rendered = compiler._rewrite_custom_tables(source, FSM.name)
    require(rendered.count(r"\begin{landscape}") == 1, "FSM landscape begin count drift")
    require(rendered.count(r"\end{landscape}") == 1, "FSM landscape end count drift")
    require(r"\fontsize{6.8}{8}\selectfont" in rendered, "FSM controlled font drift")
    require(r"\setlength{\tabcolsep}{1.5pt}" in rendered, "FSM column spacing drift")
    require(rendered.index(r"\begin{landscape}") < rendered.index(r"\begin{longtable}"),
            "FSM longtable begins outside landscape")
    require(rendered.index(r"\end{longtable}") < rendered.index(r"\end{landscape}"),
            "FSM longtable ends outside landscape")


def check_atomic_success() -> None:
    events: list[str] = []
    with tempfile.TemporaryDirectory() as raw:
        directory = Path(raw)
        source = directory / "source.svg-sentinel"
        target = directory / "target.target-sentinel"
        source.write_bytes(b"svg-source")
        target.write_bytes(b"old-target")

        def backend(_source: Path, temp: Path, _timeout: float) -> None:
            events.append("convert")
            temp.write_bytes(b"new-target")

        def validator(temp: Path) -> None:
            events.append("validate")
            require(temp.read_bytes() == b"new-target", "validator saw wrong bytes")

        def replacer(source_name: str, target_name: str) -> None:
            events.append("replace")
            os.replace(source_name, target_name)

        compiler._atomic_convert(
            source, target, backend, backend_name="fixture",
            validator=validator, replacer=replacer,
        )
        require(events == ["convert", "validate", "replace"], f"wrong event order: {events}")
        require(target.read_bytes() == b"new-target", "successful replacement failed")
        require(not list(directory.glob("*.tmp")), "temporary output survived success")


def check_atomic_failures() -> None:
    def exercise(label: str, backend, *, validator=lambda _path: None, replacer=os.replace) -> None:
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw)
            source = directory / "source.svg-sentinel"
            target = directory / "target.target-sentinel"
            source.write_bytes(b"svg-source")
            target.write_bytes(b"old-target")
            try:
                compiler._atomic_convert(
                    source, target, backend, backend_name=label,
                    validator=validator, replacer=replacer,
                )
            except RuntimeError as exc:
                require(str(source) in str(exc) and label in str(exc), f"unclear {label} error")
            else:
                raise AssertionError(f"{label} failure unexpectedly succeeded")
            require(target.read_bytes() == b"old-target", f"{label} changed stale target")
            require(not list(directory.glob("*.tmp")), f"{label} left temporary output")

    def nonzero(_source: Path, _temp: Path, _timeout: float) -> None:
        raise subprocess.CalledProcessError(7, ["fixture"])

    def timed_out(_source: Path, _temp: Path, timeout: float) -> None:
        raise subprocess.TimeoutExpired(["fixture"], timeout)

    def missing(_source: Path, _temp: Path, _timeout: float) -> None:
        return None

    def writes(_source: Path, temp: Path, _timeout: float) -> None:
        temp.write_bytes(b"candidate")

    def invalid(_temp: Path) -> None:
        raise RuntimeError("invalid structure")

    def replace_error(_source: str, _target: str) -> None:
        raise OSError("replace denied")

    exercise("nonzero", nonzero)
    exercise("timeout", timed_out)
    exercise("missing-output", missing)
    exercise("invalid-output", writes, validator=invalid)
    exercise("replace-error", writes, replacer=replace_error)

    with tempfile.TemporaryDirectory() as raw:
        directory = Path(raw)
        source = directory / "source.svg-sentinel"
        target = directory / "target.target-sentinel"
        source.write_bytes(b"svg-source")
        target.write_bytes(b"old-target")
        with mock.patch.object(compiler.shutil, "which", return_value=None), \
             mock.patch.object(compiler, "HAS_PLAYWRIGHT", False), \
             mock.patch.object(compiler, "HAS_SVGLIB", True):
            try:
                compiler.convert_svg_to_pdf(str(source), pdf_path=target)
            except RuntimeError as exc:
                require("No SVG-to-PDF backend" in str(exc), "missing-backend message drift")
            else:
                raise AssertionError("missing-backend path unexpectedly succeeded")
        require(target.read_bytes() == b"old-target", "missing backend changed target")

    source = COMPILER_SOURCE.read_text(encoding="utf-8")
    convert_body = source[source.index("def convert_svg_to_pdf"):source.index("def _svg_worker")]
    require("st_mtime" not in convert_body and ".stat()" not in convert_body, "mtime reuse survived")
    require("return str(svg_path)" not in convert_body, "raw-SVG fallback survived")


def expect_validation_failure(path: Path, expected: str) -> None:
    try:
        compiler.validate_pdf_file(path)
    except RuntimeError as exc:
        require(expected in str(exc), f"validation message lacks {expected!r}: {exc}")
    else:
        raise AssertionError(f"validation unexpectedly passed: {path.name}")


def check_validation_contract() -> None:
    """Force validator dependency, signature, parse, and page-count branches."""
    with tempfile.TemporaryDirectory() as raw:
        directory = Path(raw)
        missing = directory / "missing.sentinel"
        expect_validation_failure(missing, "missing")

        bad_signature = directory / "bad-signature.sentinel"
        bad_signature.write_bytes(b"ordinary sentinel bytes")
        expect_validation_failure(bad_signature, "signature/trailer")

        shaped = directory / "shaped.sentinel"
        shaped.write_bytes(b"%PDF-1.7\nmock-only shaped sentinel payload\n%%EOF")
        with mock.patch.object(compiler, "HAS_PYPDF", False):
            expect_validation_failure(shaped, "pypdf is required")

        with mock.patch.object(compiler, "HAS_PYPDF", True), \
             mock.patch.object(compiler, "PdfReader", side_effect=ValueError("parse sentinel")):
            expect_validation_failure(shaped, "structural parse")

        with mock.patch.object(compiler, "HAS_PYPDF", True), \
             mock.patch.object(compiler, "PdfReader", return_value=SimpleNamespace(pages=[])):
            expect_validation_failure(shaped, "no pages")

        with mock.patch.object(compiler, "HAS_PYPDF", True), \
             mock.patch.object(compiler, "PdfReader", return_value=SimpleNamespace(pages=[object()])):
            compiler.validate_pdf_file(shaped)

        unicode_source = directory / "unicode.svg-sentinel"
        unicode_source.write_text(
            "<svg><metadata>Ω</metadata><text>  Λ\n≤\tν ᴳ ⅕ − −  </text>"
            "<text style='display:none'>Ψ</text></svg>",
            encoding="utf-8",
        )
        expected = Counter({"−": 2, "Λ": 1, "≤": 1, "ν": 1, "ᴳ": 1, "⅕": 1})
        require(fixture_visible_non_ascii_counts(unicode_source) == expected,
                "independent visible-text fixture oracle drift")
        require(compiler.non_ascii_character_counts(
                    compiler.parsed_visible_svg_text(unicode_source)) == expected,
                "production visible-text parser drift")

        preserved = "Λ ≤ ν ᴳ ⅕ − −"
        forced_losses = {
            "Greek": "≤ ν ᴳ ⅕ − −",
            "operator": "Λ ν ᴳ ⅕ − −",
            "modifier": "Λ ≤ ν ⅕ − −",
            "fraction": "Λ ≤ ν ᴳ − −",
            "partial repeated minus": "Λ ≤ ν ᴳ ⅕ −",
        }
        for label, extracted in forced_losses.items():
            page = SimpleNamespace(extract_text=lambda value=extracted: value)
            with mock.patch.object(compiler, "HAS_PYPDF", True), \
                 mock.patch.object(
                     compiler, "PdfReader", return_value=SimpleNamespace(pages=[page])
                 ):
                try:
                    compiler.validate_svg_unicode_text(unicode_source, shaped)
                except RuntimeError as exc:
                    require("character-count preservation failed" in str(exc),
                            f"{label} loss diagnostic drift")
                else:
                    raise AssertionError(f"{label} loss unexpectedly passed")

        preserved_page = SimpleNamespace(extract_text=lambda: preserved)
        with mock.patch.object(compiler, "HAS_PYPDF", True), \
             mock.patch.object(
                 compiler, "PdfReader", return_value=SimpleNamespace(pages=[preserved_page])
             ):
            compiler.validate_svg_unicode_text(unicode_source, shaped)


def check_backend_wrappers_and_fallbacks() -> None:
    """Exercise backend command construction and fallback without conversion."""
    source = Path("source.svg-sentinel")
    target = Path("target.target-sentinel")
    completed = SimpleNamespace(returncode=0, stdout="", stderr="")

    with mock.patch.object(compiler.shutil, "which", return_value=None):
        try:
            compiler._run_inkscape_backend(source, target, 7.5)
        except RuntimeError as exc:
            require("unavailable" in str(exc), "Inkscape-unavailable message drift")
        else:
            raise AssertionError("unavailable Inkscape branch passed")

    with mock.patch.object(compiler.shutil, "which", return_value="inkscape-sentinel"), \
         mock.patch.object(compiler.subprocess, "run", return_value=completed) as run:
        compiler._run_inkscape_backend(source, target, 7.5)
        args = run.call_args.args[0]
        require(args[0] == "inkscape-sentinel" and str(source) in args, "Inkscape source drift")
        require(f"--export-filename={target}" in args, "Inkscape target drift")
        require(run.call_args.kwargs["timeout"] == 7.5, "Inkscape timeout drift")

    failed = SimpleNamespace(returncode=9, stdout="", stderr="backend rejected sentinel")
    with mock.patch.object(compiler.shutil, "which", return_value="inkscape-sentinel"), \
         mock.patch.object(compiler.subprocess, "run", return_value=failed):
        try:
            compiler._run_inkscape_backend(source, target, 7.5)
        except RuntimeError as exc:
            require("exited 9" in str(exc), "Inkscape nonzero message drift")
        else:
            raise AssertionError("Inkscape nonzero branch passed")

    with mock.patch.object(compiler, "HAS_SVGLIB", False):
        try:
            compiler._run_svglib_backend(source, target, 8.5)
        except RuntimeError as exc:
            require("unavailable" in str(exc), "svglib-unavailable message drift")
        else:
            raise AssertionError("unavailable svglib branch passed")

    with mock.patch.object(compiler, "HAS_SVGLIB", True), \
         mock.patch.object(compiler.subprocess, "run", return_value=completed) as run:
        compiler._run_svglib_backend(source, target, 8.5)
        args = run.call_args.args[0]
        require("--svg-worker" in args and str(source) in args and str(target) in args,
                "svglib worker command drift")
        require(run.call_args.kwargs["timeout"] == 8.5, "svglib timeout drift")

    with mock.patch.object(compiler, "HAS_SVGLIB", True), \
         mock.patch.object(compiler.subprocess, "run", return_value=failed):
        try:
            compiler._run_svglib_backend(source, target, 8.5)
        except RuntimeError as exc:
            require("exited 9" in str(exc), "svglib nonzero message drift")
        else:
            raise AssertionError("svglib nonzero branch passed")

    with mock.patch.object(compiler, "HAS_PLAYWRIGHT", False):
        try:
            compiler._run_chromium_backend(source, target, 9.5)
        except RuntimeError as exc:
            require("unavailable" in str(exc), "Chromium-unavailable message drift")
        else:
            raise AssertionError("unavailable Chromium branch passed")

    with mock.patch.object(compiler, "HAS_PLAYWRIGHT", True), \
         mock.patch.object(compiler.subprocess, "run", return_value=completed) as run:
        compiler._run_chromium_backend(source, target, 9.5)
        args = run.call_args.args[0]
        require("--chromium-svg-worker" in args and str(source) in args and str(target) in args,
                "Chromium worker command drift")
        require(run.call_args.kwargs["timeout"] == 9.5, "Chromium timeout drift")

    with mock.patch.object(compiler, "HAS_PLAYWRIGHT", True), \
         mock.patch.object(compiler.subprocess, "run", return_value=failed):
        try:
            compiler._run_chromium_backend(source, target, 9.5)
        except RuntimeError as exc:
            require("exited 9" in str(exc), "Chromium nonzero message drift")
        else:
            raise AssertionError("Chromium nonzero branch passed")

    with tempfile.TemporaryDirectory() as raw:
        directory = Path(raw)
        svg = directory / "source.svg-sentinel"
        destination = directory / "target.target-sentinel"
        svg.write_bytes(b"svg source")
        destination.write_bytes(b"old target")
        with mock.patch.object(compiler.shutil, "which", return_value="inkscape-sentinel"), \
             mock.patch.object(compiler, "HAS_PLAYWRIGHT", True), \
             mock.patch.object(
                 compiler, "_atomic_convert",
                 side_effect=[RuntimeError("Chromium sentinel failure"), destination],
             ) as atomic:
            result = compiler.convert_svg_to_pdf(str(svg), pdf_path=destination)
            require(Path(result) == destination.resolve(), "fallback result drift")
            require([call.kwargs["backend_name"] for call in atomic.call_args_list] ==
                    ["Playwright/Chromium", "Inkscape"], "backend fallback order drift")
        require(destination.read_bytes() == b"old target", "mock fallback changed target")

        with mock.patch.object(compiler.shutil, "which", return_value="inkscape-sentinel"), \
             mock.patch.object(compiler, "HAS_PLAYWRIGHT", True), \
             mock.patch.object(
                 compiler, "_atomic_convert",
                 side_effect=[RuntimeError("Chromium sentinel failure"),
                              RuntimeError("inkscape sentinel failure")],
             ):
            try:
                compiler.convert_svg_to_pdf(str(svg), pdf_path=destination)
            except RuntimeError as exc:
                message = str(exc)
                require("inkscape sentinel failure" in message and
                        "Chromium sentinel failure" in message,
                        "aggregate fallback diagnostics incomplete")
            else:
                raise AssertionError("all-backend failure unexpectedly passed")
        require(destination.read_bytes() == b"old target", "aggregate failure changed target")

        absent = directory / "absent.svg-sentinel"
        before = set(directory.iterdir())
        try:
            compiler.convert_svg_to_pdf(str(absent), pdf_path=destination)
        except RuntimeError as exc:
            require("source is missing" in str(exc), "missing-source message drift")
        else:
            raise AssertionError("missing SVG source unexpectedly passed")
        require(destination.read_bytes() == b"old target", "missing source changed target")
        require(set(directory.iterdir()) == before, "missing source created an artifact")


def check_real_chromium_unicode_backend() -> None:
    """Prove real deterministic Unicode-safe conversion and raster rendering."""
    require(compiler.HAS_PLAYWRIGHT, "pinned Playwright dependency is unavailable")
    require(compiler.HAS_PYPDF, "pinned pypdf dependency is unavailable")
    pdftoppm = compiler.shutil.which("pdftoppm")
    require(pdftoppm is not None, "pdftoppm is required for render smoke testing")

    with tempfile.TemporaryDirectory(prefix="gct-unicode-svg-") as raw:
        directory = Path(raw)
        for svg in LABEL_FIGURES:
            outputs = [directory / f"{svg.stem}.{index}.pdf" for index in (1, 2)]
            for output in outputs:
                compiler.convert_svg_to_pdf(str(svg), pdf_path=output)
            require(outputs[0].read_bytes() == outputs[1].read_bytes(),
                    f"Chromium output is not byte deterministic: {svg.name}")

            reader = compiler.PdfReader(str(outputs[0]), strict=True)
            require(len(reader.pages) == 1, f"Chromium page count drift: {svg.name}")
            extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
            required = fixture_visible_non_ascii_counts(svg)
            observed = Counter(
                char for char in FIXTURE_LAYOUT_WHITESPACE_RE.sub(" ", extracted)
                if ord(char) > 127 and not char.isspace()
            )
            require(observed == required,
                    f"Chromium character-count drift in {svg.name}: "
                    f"required={required}, observed={observed}")

            prefix = directory / f"{svg.stem}.render"
            result = subprocess.run(
                [pdftoppm, "-png", "-r", "150", "-singlefile",
                 str(outputs[0]), str(prefix)],
                capture_output=True,
                timeout=30,
            )
            require(result.returncode == 0, f"Poppler render failed: {svg.name}")
            rendered = Path(f"{prefix}.png")
            data = rendered.read_bytes()
            require(len(data) > 1024 and data.startswith(b"\x89PNG\r\n\x1a\n"),
                    f"Poppler render is invalid: {svg.name}")

        all_svgs = sorted((ROOT / "content" / "Figures").rglob("*.svg"))
        require(len(all_svgs) == 40, f"expected 40 SVG assets, found {len(all_svgs)}")
        all_dir = directory / "all-40"
        all_dir.mkdir()
        for index, svg in enumerate(all_svgs, start=1):
            output = all_dir / f"{index:02d}.pdf"
            compiler.convert_svg_to_pdf(str(svg), pdf_path=output)
            reader = compiler.PdfReader(str(output), strict=True)
            extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
            observed = Counter(
                char for char in FIXTURE_LAYOUT_WHITESPACE_RE.sub(" ", extracted)
                if ord(char) > 127 and not char.isspace()
            )
            require(observed == fixture_visible_non_ascii_counts(svg),
                    f"all-40 character-count drift: {svg.name}")


def check_svg_worker_branches() -> None:
    """Force every isolated worker branch with mocks and ordinary sentinels."""
    with tempfile.TemporaryDirectory() as raw:
        directory = Path(raw)
        source = directory / "source.svg-sentinel"
        output = directory / "output.target-sentinel"
        source.write_bytes(b"svg source")
        baseline = set(directory.iterdir())

        with mock.patch.object(compiler, "HAS_SVGLIB", False), redirect_stderr(io.StringIO()):
            require(compiler._svg_worker(source, output) == 2, "worker unavailable exit drift")
        require(set(directory.iterdir()) == baseline, "unavailable worker created an artifact")

        with mock.patch.object(compiler, "HAS_SVGLIB", True), \
             mock.patch.object(compiler, "svg2rlg", return_value=None), \
             redirect_stderr(io.StringIO()):
            require(compiler._svg_worker(source, output) == 3, "worker no-drawing exit drift")
        require(set(directory.iterdir()) == baseline, "no-drawing worker created an artifact")

        drawing = object()
        with mock.patch.object(compiler, "HAS_SVGLIB", True), \
             mock.patch.object(compiler, "svg2rlg", return_value=drawing), \
             mock.patch.object(compiler.renderPDF, "drawToFile", side_effect=OSError("render sentinel")), \
             redirect_stderr(io.StringIO()):
            require(compiler._svg_worker(source, output) == 3, "worker render-error exit drift")
        require(set(directory.iterdir()) == baseline, "render-error worker created an artifact")

        with mock.patch.object(compiler, "HAS_SVGLIB", True), \
             mock.patch.object(compiler, "svg2rlg", return_value=drawing), \
             mock.patch.object(compiler.renderPDF, "drawToFile") as render:
            require(compiler._svg_worker(source, output) == 0, "worker success exit drift")
            render.assert_called_once_with(drawing, str(output), fmt="PDF", invariant=1)
        require(set(directory.iterdir()) == baseline, "mock worker success created an artifact")



def main() -> int:
    check_publication_source()
    check_legacy_math_script_normalizer()
    check_pdf_chapter_title_qualifiers()
    check_generated_tex_trailing_whitespace()
    check_terminal_backmatter_removal()
    check_figure_label_sizes()
    check_figure_text_geometry()
    check_figure_renderer_forced_negatives()
    check_emblem_and_discovery()
    check_unicode_boundary()
    check_fsm_landscape_table()
    check_atomic_success()
    check_atomic_failures()
    check_validation_contract()
    check_backend_wrappers_and_fallbacks()
    check_svg_worker_branches()
    check_real_chromium_unicode_backend()
    print("PASS: compile_latex source-preparation fixtures (temporary PDF smoke only)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
