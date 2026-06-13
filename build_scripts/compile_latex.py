"""
GCT LaTeX Compiler
==================
Compiles the FULL Geometric Consciousness Theory manuscript (Volumes 1-3,
global appendices, global backmatter) into a journal-ready LaTeX/PDF document.

Approach: walks content/ recursively using the same ORDERED_SECTIONS +
natural_sort_key pipeline as compile_manuscript.py (via build_scripts/_common.py),
so the two compilers stay in sync without consuming the markdown monolith.

Usage: python build_scripts/compile_latex.py

Author: Pablo González Acosta
Date: May 14, 2026 (full-manuscript generalization)
"""

import re
import sys
import shutil
import subprocess
import tempfile
from pathlib import Path

# Try to import SVG conversion tools
try:
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPDF
    HAS_SVGLIB = True
except ImportError:
    HAS_SVGLIB = False

# --- Force UTF-8 on Windows ---
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Shared helpers + metadata
from _common import (
    PROJECT_ROOT,
    METADATA,
    walk_content_files,
)

# --- Paths ---
OUTPUT_DIR = PROJECT_ROOT / "output"

OUTPUT_TEX = OUTPUT_DIR / METADATA["output_filename_tex"]
OUTPUT_PDF = OUTPUT_DIR / METADATA["output_filename_pdf"]

# --- LaTeX preamble (injected via pandoc --include-in-header) ---
# Note: the \DeclareUnicodeCharacter block below covers every non-ASCII
# codepoint that build_scripts/scan_unicode.py finds in content/ outside
# fenced code blocks and math regions. Pdflatex with utf8 inputenc accepts
# these declarations and renders the glyphs from the loaded math/text fonts.
LATEX_PREAMBLE = r"""
\usepackage[margin=1in]{geometry}
% Honor the manuscript's MANUAL section/chapter numbers (carried in the heading
% text, e.g. "Chapter 6:", "11.15.4") which every in-text cross-reference
% resolves to. Suppress LaTeX auto-numbering of chapters and below so it does
% not collide with the manual scheme (parts at level -1 stay numbered).
\setcounter{secnumdepth}{-1}
\usepackage{array}
\usepackage{longtable}
\usepackage{booktabs}
% mathpazo must be loaded BEFORE amssymb to prevent font-slot collision
% that causes \gg to render as a left-arrow glyph in the Palatino math font.
\usepackage{mathpazo}
\usepackage{amsmath,amssymb,amsthm}
% Explicit guard: re-declare \gg and \ll from AMSb/AMSa after all font packages load.
\AtBeginDocument{%
  \DeclareMathSymbol{\gg}{\mathrel}{AMSb}{"1D}%
  \DeclareMathSymbol{\ll}{\mathrel}{AMSa}{"1C}%
}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[most]{tcolorbox}
\usepackage{xcolor}
\usepackage{graphicx}
\usepackage{textcomp}
\usepackage{newunicodechar}
\graphicspath{{../}}  % Allow relative paths to figures

% --- Running headers: chapter title only (no section) ---
% Long section/appendix titles (e.g. "M.9 The Jacobian of Screening ...
% [Tier 2 ...]") overflow the recto running head and collide with the page
% number. Use the (shorter) chapter title on both pages at \small, dropping the
% section mark entirely.
\usepackage{fancyhdr}
\setlength{\headheight}{14pt}
\renewcommand{\sectionmark}[1]{}
\renewcommand{\subsectionmark}[1]{}
\fancypagestyle{gctheadings}{%
  \fancyhf{}%
  \fancyhead[LE]{\thepage}%
  \fancyhead[RE]{\nouppercase{\small\leftmark}}%
  \fancyhead[LO]{\nouppercase{\small\leftmark}}%
  \fancyhead[RO]{\thepage}%
  \renewcommand{\headrulewidth}{0.4pt}%
}
\pagestyle{gctheadings}
% Chapter/part opening pages use plain style (page number centered, no header).
\fancypagestyle{plain}{\fancyhf{}\fancyfoot[C]{\thepage}\renewcommand{\headrulewidth}{0pt}}

% --- Breakable long monospace tokens ---
% Long file paths / script names (protocol_*.py, verify_independent/..., *.json)
% in narrow table cells or running prose otherwise overrun the cell boundary or
% clip at the right margin. hyphenat[htt] permits hyphenation/line breaks inside
% \texttt words (robust in moving arguments, unlike seqsplit), and a generous
% \emergencystretch lets the line breaker absorb the rest. Long paths in the
% widest tables are additionally shortened at the generators and the widest
% tables are set landscape (below).
\usepackage[htt]{hyphenat}
\setlength{\emergencystretch}{3em}

% --- Landscape pages for the widest appendix tables (FM.4, App R, App V) ---
\usepackage{pdflscape}

% --- Unicode character declarations ---
% pdflatex with utf8 inputenc does NOT know how to typeset arbitrary Unicode
% codepoints by default. We declare every non-ASCII codepoint that appears
% outside math/code regions in the GCT manuscript so pdflatex can render
% them via math mode or text-font glyphs. (Listed in U+ order.)
\DeclareUnicodeCharacter{00B0}{\ensuremath{^{\circ}}}      % ° degree sign
\DeclareUnicodeCharacter{00B1}{\ensuremath{\pm}}           % ± plus-minus
\DeclareUnicodeCharacter{00B2}{\ensuremath{^{2}}}          % ² superscript two
\DeclareUnicodeCharacter{00B3}{\ensuremath{^{3}}}          % ³ superscript three
\DeclareUnicodeCharacter{00B7}{\ensuremath{\cdot}}         % · middle dot
\DeclareUnicodeCharacter{00B9}{\ensuremath{^{1}}}          % ¹ superscript one
\DeclareUnicodeCharacter{00D7}{\ensuremath{\times}}        % × multiplication sign
% Latin extended with circumflex / caron (text-mode accents)
\DeclareUnicodeCharacter{0108}{\^{C}}                      % Ĉ
\DeclareUnicodeCharacter{0109}{\^{c}}                      % ĉ
\DeclareUnicodeCharacter{010C}{\v{C}}                      % Č
\DeclareUnicodeCharacter{0124}{\^{H}}                      % Ĥ
% Combining circumflex above (used for \hat-style accents in prose)
\DeclareUnicodeCharacter{0302}{\^{}}                       % ̂ combining circumflex
% Greek capitals (allow as prose chars; math mode use is unaffected)
\DeclareUnicodeCharacter{0392}{\ensuremath{\mathrm{B}}}    % Β
\DeclareUnicodeCharacter{0393}{\ensuremath{\Gamma}}        % Γ
\DeclareUnicodeCharacter{0394}{\ensuremath{\Delta}}        % Δ
\DeclareUnicodeCharacter{039B}{\ensuremath{\Lambda}}       % Λ
\DeclareUnicodeCharacter{03A3}{\ensuremath{\Sigma}}        % Σ
\DeclareUnicodeCharacter{03A6}{\ensuremath{\Phi}}          % Φ
\DeclareUnicodeCharacter{03A8}{\ensuremath{\Psi}}          % Ψ
\DeclareUnicodeCharacter{03A9}{\ensuremath{\Omega}}        % Ω
% Greek lowercase
\DeclareUnicodeCharacter{03B1}{\ensuremath{\alpha}}        % α
\DeclareUnicodeCharacter{03B2}{\ensuremath{\beta}}         % β
\DeclareUnicodeCharacter{03B4}{\ensuremath{\delta}}        % δ
\DeclareUnicodeCharacter{03B5}{\ensuremath{\varepsilon}}   % ε
\DeclareUnicodeCharacter{03B7}{\ensuremath{\eta}}          % η
\DeclareUnicodeCharacter{03B8}{\ensuremath{\theta}}        % θ
\DeclareUnicodeCharacter{03BA}{\ensuremath{\kappa}}        % κ
\DeclareUnicodeCharacter{03BB}{\ensuremath{\lambda}}       % λ
\DeclareUnicodeCharacter{03BC}{\ensuremath{\mu}}           % μ
\DeclareUnicodeCharacter{03BD}{\ensuremath{\nu}}           % ν
\DeclareUnicodeCharacter{03BE}{\ensuremath{\xi}}           % ξ
\DeclareUnicodeCharacter{03C0}{\ensuremath{\pi}}           % π
\DeclareUnicodeCharacter{03C1}{\ensuremath{\rho}}          % ρ
\DeclareUnicodeCharacter{03C3}{\ensuremath{\sigma}}        % σ
\DeclareUnicodeCharacter{03C4}{\ensuremath{\tau}}          % τ
\DeclareUnicodeCharacter{03C6}{\ensuremath{\varphi}}       % φ
\DeclareUnicodeCharacter{03C9}{\ensuremath{\omega}}        % ω
% Latin subscript small letters (Unicode block "Phonetic Extensions")
\DeclareUnicodeCharacter{1D62}{\ensuremath{_{i}}}          % ᵢ subscript i
% Punctuation / general formatting
\DeclareUnicodeCharacter{2011}{-}                          % ‑ non-breaking hyphen
\DeclareUnicodeCharacter{2016}{\ensuremath{\|}}            % ‖ double vertical line
\DeclareUnicodeCharacter{2020}{\ensuremath{\dagger}}       % † dagger
\DeclareUnicodeCharacter{2032}{\ensuremath{{}^{\prime}}}   % ′ prime
% Superscript digits + signs
\DeclareUnicodeCharacter{2074}{\ensuremath{^{4}}}          % ⁴
\DeclareUnicodeCharacter{2075}{\ensuremath{^{5}}}          % ⁵
\DeclareUnicodeCharacter{2076}{\ensuremath{^{6}}}          % ⁶
\DeclareUnicodeCharacter{2078}{\ensuremath{^{8}}}          % ⁸
\DeclareUnicodeCharacter{2079}{\ensuremath{^{9}}}          % ⁹
\DeclareUnicodeCharacter{207A}{\ensuremath{^{+}}}          % ⁺
\DeclareUnicodeCharacter{207B}{\ensuremath{^{-}}}          % ⁻
% Subscript digits
\DeclareUnicodeCharacter{2080}{\ensuremath{_{0}}}          % ₀
\DeclareUnicodeCharacter{2081}{\ensuremath{_{1}}}          % ₁
\DeclareUnicodeCharacter{2082}{\ensuremath{_{2}}}          % ₂
\DeclareUnicodeCharacter{2083}{\ensuremath{_{3}}}          % ₃
\DeclareUnicodeCharacter{2084}{\ensuremath{_{4}}}          % ₄
\DeclareUnicodeCharacter{2085}{\ensuremath{_{5}}}          % ₅
\DeclareUnicodeCharacter{2086}{\ensuremath{_{6}}}          % ₆
\DeclareUnicodeCharacter{2087}{\ensuremath{_{7}}}          % ₇
\DeclareUnicodeCharacter{2088}{\ensuremath{_{8}}}          % ₈
% Math letters / sets
\DeclareUnicodeCharacter{210F}{\ensuremath{\hbar}}         % ℏ
\DeclareUnicodeCharacter{2113}{\ensuremath{\ell}}          % ℓ
\DeclareUnicodeCharacter{2124}{\ensuremath{\mathbb{Z}}}    % ℤ
% Arrows
\DeclareUnicodeCharacter{2192}{\ensuremath{\rightarrow}}   % →
\DeclareUnicodeCharacter{2194}{\ensuremath{\leftrightarrow}} % ↔
% Math operators / relations
\DeclareUnicodeCharacter{2208}{\ensuremath{\in}}           % ∈
\DeclareUnicodeCharacter{2212}{\ensuremath{-}}             % − minus sign
\DeclareUnicodeCharacter{221E}{\ensuremath{\infty}}        % ∞
\DeclareUnicodeCharacter{2225}{\ensuremath{\parallel}}     % ∥
\DeclareUnicodeCharacter{222B}{\ensuremath{\int}}          % ∫
\DeclareUnicodeCharacter{2245}{\ensuremath{\cong}}         % ≅
\DeclareUnicodeCharacter{2248}{\ensuremath{\approx}}       % ≈
\DeclareUnicodeCharacter{2260}{\ensuremath{\neq}}          % ≠
\DeclareUnicodeCharacter{2261}{\ensuremath{\equiv}}        % ≡
\DeclareUnicodeCharacter{2265}{\ensuremath{\geq}}          % ≥
\DeclareUnicodeCharacter{226A}{\ensuremath{\ll}}           % ≪
\DeclareUnicodeCharacter{22A5}{\ensuremath{\perp}}         % ⊥ up tack
% Boxes / shapes / checkmarks
\DeclareUnicodeCharacter{25A1}{\ensuremath{\square}}       % □
\DeclareUnicodeCharacter{25B3}{\ensuremath{\triangle}}     % △
\DeclareUnicodeCharacter{25CB}{\ensuremath{\circ}}         % ○ open circle (pending pill)
\DeclareUnicodeCharacter{25D1}{\ensuremath{\circ}}         % ◑ half-filled circle (partial pill)
\DeclareUnicodeCharacter{2713}{\ensuremath{\checkmark}}    % ✓
\DeclareUnicodeCharacter{2717}{\textsf{x}}                 % ✗ ballot X
\DeclareUnicodeCharacter{2264}{\ensuremath{\leq}}          % ≤ less-or-equal
\DeclareUnicodeCharacter{2265}{\ensuremath{\geq}}          % ≥ greater-or-equal
% Angle brackets (math)
\DeclareUnicodeCharacter{27E8}{\ensuremath{\langle}}       % ⟨
\DeclareUnicodeCharacter{27E9}{\ensuremath{\rangle}}       % ⟩
% Zero-width space — inserted by the math-adjacency pre-processor to break
% pandoc's "$math$<alnum>" parse failure. Render as nothing.
\DeclareUnicodeCharacter{200B}{\hspace{0pt}}                % U+200B ZWSP
% Emoji + symbols that have no LaTeX counterpart — render as a neutral token.
% These appear only in tier banners / warning callouts.
\DeclareUnicodeCharacter{26A0}{[WARNING]}                  % ⚠
\DeclareUnicodeCharacter{2705}{[OK]}                       % ✅
\DeclareUnicodeCharacter{FE0F}{}                           % VS16 (silently dropped)

% --- tcolorbox styles for GitHub-style alerts ---
\tcbuselibrary{skins,breakable}

\newtcolorbox{gctNote}[1][]{
  enhanced,
  colback=blue!5!white, colframe=blue!50!black,
  fonttitle=\bfseries, title=Note,
  #1
}
\newtcolorbox{gctWarning}[1][]{
  enhanced,
  colback=yellow!10!white, colframe=orange!80!black,
  fonttitle=\bfseries, title=Warning,
  #1
}
\newtcolorbox{gctCaution}[1][]{
  enhanced,
  colback=red!5!white, colframe=red!60!black,
  fonttitle=\bfseries, title=Caution,
  #1
}
\newtcolorbox{gctImportant}[1][]{
  enhanced,
  colback=purple!5!white, colframe=purple!60!black,
  fonttitle=\bfseries, title=Important,
  #1
}
\newtcolorbox{gctTip}[1][]{
  enhanced,
  colback=green!5!white, colframe=green!50!black,
  fonttitle=\bfseries, title=Tip,
  #1
}
\newtcolorbox{gctSpeculative}[1][]{
  enhanced,
  colback=gray!8!white, colframe=gray!55!black,
  fonttitle=\bfseries, title=Speculative,
  #1
}
"""

# Map GitHub alert type → tcolorbox environment name
ALERT_ENV = {
    "NOTE":      "gctNote",
    "WARNING":   "gctWarning",
    "CAUTION":   "gctCaution",
    "IMPORTANT": "gctImportant",
    "TIP":       "gctTip",
    "SPECULATIVE": "gctSpeculative",
}


# ---------------------------------------------------------------------------
# 1. SVG to PDF conversion
# ---------------------------------------------------------------------------

def convert_svg_to_pdf(svg_path_str: str) -> str:
    """
    Convert SVG to PDF. Returns the PDF path (creates one if needed).
    Tries Inkscape first, then svglib. If neither converter is available but a
    committed PDF sibling exists, falls back to it (so anyone cloning the repo
    can rebuild the manuscript without Inkscape/svglib — every figure ships with
    a committed PDF). Only returns the raw SVG path as a last resort.
    """
    svg_path = Path(svg_path_str)
    pdf_path = svg_path.with_suffix('.pdf')

    # Reuse an existing sibling PDF only if it is at least as new as the SVG.
    # A stale PDF (older than its SVG) is regenerated so figure edits always
    # propagate into the typeset output.
    if pdf_path.exists() and pdf_path.stat().st_mtime >= svg_path.stat().st_mtime:
        return str(pdf_path)

    inkscape = shutil.which("inkscape")
    if inkscape:
        try:
            subprocess.run(
                [inkscape, str(svg_path), f"--export-pdf={pdf_path}"],
                capture_output=True,
                timeout=10
            )
            if pdf_path.exists():
                return str(pdf_path)
        except Exception:
            pass

    if HAS_SVGLIB:
        try:
            drawing = svg2rlg(str(svg_path))
            if drawing:
                renderPDF.drawToFile(drawing, str(pdf_path), fmt='PDF')
                if pdf_path.exists():
                    return str(pdf_path)
        except Exception:
            pass

    # No converter could (re)generate the PDF. Prefer a committed PDF sibling
    # (the normal case for a fresh clone without Inkscape/svglib) over handing
    # pdflatex a raw .svg it cannot \includegraphics.
    if pdf_path.exists():
        return str(pdf_path)
    return str(svg_path)


# ---------------------------------------------------------------------------
# 2. Dependency check
# ---------------------------------------------------------------------------

def check_dependencies():
    pandoc   = shutil.which("pandoc")
    pdflatex = shutil.which("pdflatex")

    if not pandoc:
        print("[ERROR] 'pandoc' is not installed or not on PATH.")
        print("        To install on Windows: winget install pandoc")
        print("        On macOS:  brew install pandoc")
        print("        On Linux:  sudo apt install pandoc")

    if not pdflatex:
        print("[WARNING] 'pdflatex' is not installed or not on PATH.")
        print("          PDF generation will be skipped.")
        print("          To install on Windows: winget install MiKTeX")
        print("          On macOS:  brew install --cask mactex")
        print("          On Linux:  sudo apt install texlive-full")

    if not pandoc:
        sys.exit(1)

    return str(pandoc), pdflatex


# ---------------------------------------------------------------------------
# 3. Pre-processor: GitHub alert blocks → raw LaTeX tcolorbox
# ---------------------------------------------------------------------------

def _md_to_latex_inline(text: str) -> str:
    """
    Minimal markdown→LaTeX conversion for content INSIDE raw-tex blocks
    (callout boxes). Pandoc doesn't reach inside \begin{...}...\end{...}
    raw blocks, so we have to do this ourselves.

    Handles: bold (** or __), italic (* or _ ignoring escaped underscores),
    inline code (`code`), LaTeX-special character escaping outside math.
    """
    # Split on math regions so we don't touch them.
    parts = re.split(r"(\$\$.+?\$\$|\$[^$\n]+\$)", text, flags=re.DOTALL)
    out = []
    for idx, part in enumerate(parts):
        if idx % 2 == 1:
            # Math region — leave untouched
            out.append(part)
            continue
        # Inline code first (to protect content)
        code_pieces = re.split(r"(`[^`]+`)", part)
        for cidx, cp in enumerate(code_pieces):
            if cidx % 2 == 1:
                # `code` → \texttt{code} (escape backslashes + braces)
                inner = cp[1:-1]
                inner = inner.replace("\\", r"\textbackslash{}")
                inner = inner.replace("{", r"\{").replace("}", r"\}")
                inner = inner.replace("&", r"\&").replace("%", r"\%")
                inner = inner.replace("#", r"\#").replace("_", r"\_")
                inner = inner.replace("$", r"\$")
                out.append(r"\texttt{" + inner + "}")
            else:
                s = cp
                # Bold/italic. Apply bold first so its inner * doesn't trip italic.
                s = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", s, flags=re.DOTALL)
                s = re.sub(r"__(.+?)__", r"\\textbf{\1}", s, flags=re.DOTALL)
                s = re.sub(r"(?<!\*)\*(?!\*)([^*\n]+?)\*(?!\*)", r"\\textit{\1}", s)
                # Escape stray LaTeX specials (outside math/code we already handled).
                # Order matters: don't touch backslashes (raw_tex may be in body).
                s = s.replace("&", r"\&")
                s = s.replace("%", r"\%")
                # Escape `_` only when between non-whitespace (e.g. `Γ_rec`)
                # to avoid touching emphasis markers or §-refs already escaped.
                s = re.sub(r"(?<!\\)_(?=\w)", r"\\_", s)
                out.append(s)
    return "".join(out)


def preprocess_alerts(text: str) -> str:
    """
    Converts GitHub-style callout blocks into raw LaTeX tcolorbox environments.

    Pandoc cannot reach inside \begin{...}...\end{...} raw_tex blocks, so we
    must do the markdown→LaTeX conversion for the alert body ourselves
    (_md_to_latex_inline above).
    """
    lines  = text.split("\n")
    output = []
    i = 0

    while i < len(lines):
        line = lines[i]
        alert_match = re.match(
            r"^>\s*\[!(NOTE|WARNING|CAUTION|IMPORTANT|TIP|SPECULATIVE)\]\s?(.*)$",
            line,
            re.IGNORECASE,
        )

        if alert_match:
            alert_type = alert_match.group(1).upper()
            env = ALERT_ENV.get(alert_type, "gctNote")

            body_lines = []
            # Capture any content on the marker line itself (e.g.
            # "> [!SPECULATIVE] **Appendix I…**"); otherwise it is lost.
            same_line = alert_match.group(2).strip()
            if same_line:
                body_lines.append(same_line)
            i += 1
            while i < len(lines) and lines[i].startswith(">"):
                stripped = re.sub(r"^>\s?", "", lines[i])
                body_lines.append(stripped)
                i += 1

            # Convert blank lines inside the body to explicit \par. A blank
            # line inside a raw \begin{env}…\end{env} block makes pandoc end
            # the raw-LaTeX block early (corrupting multi-paragraph alerts —
            # the rest leaks into a stray 1-column longtable). \par keeps the
            # whole environment one raw block while preserving paragraph breaks.
            conv = [_md_to_latex_inline(b) for b in body_lines]
            parts = [(r"\par" if b.strip() == "" else b) for b in conv]
            body = "\n".join(parts).strip()
            body = re.sub(r"(?:\\par\s*){2,}", r"\\par ", body)
            body = re.sub(r"^(?:\\par\s*)+", "", body)

            output.append("")
            output.append(f"\\begin{{{env}}}")
            output.append(body)
            output.append(f"\\end{{{env}}}")
            output.append("")

        else:
            output.append(line)
            i += 1

    return "\n".join(output)


# ---------------------------------------------------------------------------
# 4. Figure manager: check existence, generate placeholders
# ---------------------------------------------------------------------------

def get_figure_path(figure_id):
    """Look up a figure file by ID (V<n>.<m>.<k>). Returns relative path or None."""
    volume_num = figure_id.split('.')[0].replace('V', '')
    volume = f"Volume_{volume_num}"
    figure_name = f"Figure {figure_id}"

    vol_dir = PROJECT_ROOT / "content" / "Figures" / volume
    if not vol_dir.exists():
        return None

    svg_candidate = vol_dir / f"{figure_name}.svg"
    if svg_candidate.exists():
        pdf_path = convert_svg_to_pdf(str(svg_candidate))
        return str(Path(pdf_path).relative_to(PROJECT_ROOT)).replace("\\", "/")

    for ext in ['png', 'pdf']:
        candidate = vol_dir / f"{figure_name}.{ext}"
        if candidate.exists():
            return str(candidate.relative_to(PROJECT_ROOT)).replace("\\", "/")

    return None


def generate_inline_figure(figure_id):
    path = get_figure_path(figure_id)
    if path:
        return f"\n![Figure {figure_id}]({path})\n"
    else:
        volume_num = figure_id.split('.')[0].replace('V', '')
        return (
            f"\n> [!NOTE]\n"
            f"> **Figure {figure_id} in development.** This figure will be generated/inserted in a future revision.\n"
            f"> Expected file: `content/Figures/Volume_{volume_num}/Figure {figure_id}.[svg|png|pdf]`\n"
        )


def preprocess_thematic_breaks(text: str) -> str:
    """
    A standalone thematic break (`---`, `***`, `___`) that is immediately
    followed by a non-blank line makes pandoc (with -yaml_metadata_block)
    misparse the break + the following text into a 1-column table, which
    renders as an unreadable one-word-per-line vertical tower swallowing
    subsequent pages. We insert a blank line AFTER any such break so pandoc
    treats it as a true horizontal rule. We only act when the break is itself
    preceded by a blank line (so a genuine setext-heading underline — `text`
    directly above `---` — is never disturbed).
    """
    lines = text.split("\n")
    out = []
    for i, line in enumerate(lines):
        out.append(line)
        if re.match(r"^(-{3,}|\*{3,}|_{3,})\s*$", line):
            prev_blank = (i == 0) or (lines[i - 1].strip() == "")
            next_nonblank = (i + 1 < len(lines)) and (lines[i + 1].strip() != "")
            if prev_blank and next_nonblank:
                out.append("")
    return "\n".join(out)


def preprocess_double_backslash_in_math(text: str) -> str:
    """
    Several GCT source files have `\\` inside `$...$` math regions where the
    author meant `\`. (E.g. `$\\eta_0 = \\phi^{-2}$`.) pandoc passes these
    through as literal double backslashes which then break pdflatex. Walk
    the text and collapse `\\` → `\` inside inline math only.
    """
    out = []
    i = 0
    n = len(text)
    in_fence = False
    while i < n:
        if (i == 0 or text[i - 1] == "\n") and text.startswith("```", i):
            j = text.find("\n", i)
            j = n if j == -1 else j + 1
            out.append(text[i:j])
            i = j
            in_fence = not in_fence
            continue
        ch = text[i]
        if in_fence:
            out.append(ch)
            i += 1
            continue
        if ch == "`":
            j = text.find("`", i + 1)
            if j == -1:
                out.append(text[i:])
                break
            out.append(text[i:j + 1])
            i = j + 1
            continue
        if text.startswith("$$", i):
            j = text.find("$$", i + 2)
            if j == -1:
                out.append(text[i:])
                break
            body = text[i + 2:j]
            # Collapse `\\X` (a doubled backslash before a letter) → `\X` —
            # those are author typos like `$$\\frac{...}$$`. Preserve `\\ `
            # and `\\\n` which can be legitimate line breaks in alignments.
            body = re.sub(r"\\\\(?=[A-Za-z])", r"\\", body)
            out.append("$$" + body + "$$")
            i = j + 2
            continue
        if ch == "$":
            j = text.find("$", i + 1)
            if j == -1 or "\n" in text[i + 1:j]:
                out.append(ch)
                i += 1
                continue
            body = text[i + 1:j]
            # Inline math: `\\` → `\`
            body = body.replace("\\\\", "\\")
            # Strip leading/trailing whitespace inside math (pandoc rejects
            # `$ math $` as not-math; the spaces are author typos).
            body = body.strip()
            out.append("$" + body + "$")
            i = j + 1
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def preprocess_math_adjacency(text: str) -> str:
    """
    Pandoc-markdown rejects `$math$` if the closing `$` is immediately
    preceded or followed by an alphanumeric (e.g. `6D$\to$3D` or `X$y$`).
    The GCT source has dozens of these. Rewrite the offending ones to use
    `\(...\)` LaTeX delimiters which pandoc passes through without the
    adjacency restriction.

    Walks the text linearly so we never confuse close-of-A with open-of-B.
    Handles fenced code blocks and `$$...$$` display math by skipping them.
    """
    out = []
    i = 0
    n = len(text)
    in_fence = False  # tracking ``` fenced code blocks
    while i < n:
        # Detect fenced code block toggle (only at line start)
        if (i == 0 or text[i - 1] == "\n") and text.startswith("```", i):
            # copy the whole fence line and toggle
            j = text.find("\n", i)
            j = n if j == -1 else j + 1
            out.append(text[i:j])
            i = j
            in_fence = not in_fence
            continue
        ch = text[i]
        if in_fence:
            out.append(ch)
            i += 1
            continue
        # Skip inline code spans
        if ch == "`":
            j = text.find("`", i + 1)
            if j == -1:
                out.append(text[i:])
                break
            out.append(text[i:j + 1])
            i = j + 1
            continue
        # Display math $$...$$ — copy verbatim
        if text.startswith("$$", i):
            j = text.find("$$", i + 2)
            if j == -1:
                out.append(text[i:])
                break
            out.append(text[i:j + 2])
            i = j + 2
            continue
        # Inline math $...$
        if ch == "$":
            j = text.find("$", i + 1)
            # Find the closing $ that's not escaped and not on a new line
            while j != -1 and j < n:
                seg = text[i + 1:j]
                if "\n" in seg:
                    # malformed math span — bail
                    j = -1
                    break
                # Accept this as closing
                break
            if j == -1 or j >= n:
                out.append(ch)
                i += 1
                continue
            after = text[j + 1] if (j + 1) < n else " "
            # Only rewrite if the closing $ is followed by an alphanumeric.
            # That's the adjacency case pandoc-markdown rejects. Pandoc DOES
            # accept it if a U+200B ZERO WIDTH SPACE separates them — and
            # then emits `\hspace{0pt}` in the .tex (no visible difference).
            if after.isalnum():
                out.append(text[i:j + 1] + "​")
            else:
                out.append(text[i:j + 1])
            i = j + 1
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def preprocess_inline_figures(text: str) -> str:
    pattern = r">\s*\*\*Figure\s+(V\d+\.\d+\.\d+):\*\*\s*\*([^*]+)\*"

    def replace_figure(match):
        figure_id = match.group(1)
        figure_md = generate_inline_figure(figure_id)
        return match.group(0) + "\n" + figure_md

    return re.sub(pattern, replace_figure, text)


def preprocess_svg_image_links(text: str) -> str:
    """Convert local Markdown SVG image links to sibling PDFs for pdflatex."""
    pattern = r"!\[([^\]]*)\]\(([^)\n]+?\.svg)\)"

    def replace_svg(match):
        alt_text = match.group(1)
        raw_path = match.group(2).strip()
        link_path = raw_path[1:-1] if raw_path.startswith("<") and raw_path.endswith(">") else raw_path

        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", link_path):
            return match.group(0)

        svg_path = Path(link_path)
        if not svg_path.is_absolute():
            svg_path = PROJECT_ROOT / svg_path

        if not svg_path.exists():
            return match.group(0)

        pdf_path = Path(convert_svg_to_pdf(str(svg_path)))
        if pdf_path.suffix.lower() != ".pdf" or not pdf_path.exists():
            return match.group(0)

        rel_pdf = pdf_path.relative_to(PROJECT_ROOT).as_posix()
        return f"![{alt_text}]({rel_pdf})"

    return re.sub(pattern, replace_svg, text)


# ---------------------------------------------------------------------------
# 5. Assemble full manuscript markdown (walks the whole content/ tree)
# ---------------------------------------------------------------------------

_processed_files: set = set()


def _demote_in_file_top_headings(content: str) -> str:
    """
    Normalize the in-file heading hierarchy so the default book-class
    mapping (h1 → \chapter, h2 → \section, h3 → \subsection) produces
    a clean structure.

    Source heading conventions are heterogeneous:
      - Volume / book / chapter abstracts may open with `# TITLE`     (h1)
      - Each Part's first chapter opens with `## PART X`              (h2)
      - Some files open with `## **GLOBAL FRONT MATTER**`             (h2)
      - Chapter / appendix / preface / notation openers use `### ...` (h3)
      - Inner section subdivisions also use `### N.N.N Subtitle`      (h3)
      - Inner sub-section numbers use `**1.1 X**` bold paragraphs (not
        headings — they don't auto-number).

    Goal under default top-level-division=chapter:
      - The opener of each file becomes the file's `# Title` h1 → \chapter
      - PART X grouping labels become centered bold display (NOT sectioning)
      - In-file h2/h3 numbering stays as is so it renders as \section /
        \subsection inside the chapter.

    Rules applied in order:
      1) Drop "## **GLOBAL FRONT MATTER**" / "## **GLOBAL BACK MATTER**"
         and similar all-caps organizational labels.
      2) Convert "## PART X: ..." into centered bold (non-sectioning).
      3) Promote the FIRST opener-style h3 in the file to h1 (\chapter).
         An opener is recognized by an explicit pattern set; all other h3s
         remain h3 → \subsection (these are real inner subdivisions like
         "### 5.2.1 The Macroscopic Saturation").
      4) If a file STARTS with an h1 that's the book-title-or-volume-title
         duplicate (e.g. "# Geometric Consciousness Theory" or "# VOLUME 1:
         THE OPERATING SYSTEM"), strip it — the dir-walker emits the
         right \part division.
    """
    # First-line patterns of h1 that are structural duplicates to strip
    STRIP_H1_PATTERNS = [
        re.compile(r"^#\s+\*?\*?\s*VOLUME\s+\d+[^\n]*$", re.IGNORECASE),
        re.compile(r"^#\s+Geometric\s+Consciousness\s+Theory[^\n]*$", re.IGNORECASE),
    ]

    # h3 patterns that mark a "file-opening" heading (promote to h1)
    OPENER_PATTERNS = [
        re.compile(r"^###\s+\*\*Chapter\s+\d+[^*]*\*\*\s*$"),
        re.compile(r"^###\s+Chapter\s+\d+[:\s].+$"),
        re.compile(r"^###\s+\*\*Appendix\s+[A-Z]+[^*]*\*\*\s*$"),
        re.compile(r"^###\s+\*\*Preface\s[^*]*\*\*\s*$"),
        re.compile(r"^###\s+\*\*[^*]*Notation[^*]*\*\*\s*$"),
        re.compile(r"^###\s+\*\*Volume\s+\d+\s+Abstract[^*]*\*\*\s*$"),
        re.compile(r"^###\s+\*\*The Epistemic[^*]*\*\*\s*$"),
        re.compile(r"^###\s+\*\*Global\s+Abstract[^*]*\*\*\s*$"),
        re.compile(r"^###\s+Volume\s+\d+\s+Abstract\s*$"),
        re.compile(r"^###\s+\*\*Master\s+Glossary[^*]*\*\*\s*$", re.IGNORECASE),
        re.compile(r"^###\s+\*\*Master\s+Bibliography[^*]*\*\*\s*$", re.IGNORECASE),
        re.compile(r"^###\s+\*\*Master\s+Index[^*]*\*\*\s*$", re.IGNORECASE),
        re.compile(r"^###\s+\*\*Acknowledg(e)?ments[^*]*\*\*\s*$", re.IGNORECASE),
        re.compile(r"^###\s+\*\*Colophon[^*]*\*\*\s*$", re.IGNORECASE),
    ]
    # h1 patterns whose title we want to keep as a \chapter (so promote h1 → h1
    # but make sure the body's subsections downshift accordingly).
    # We treat any leading h1 that isn't a STRIP-pattern as a valid chapter h1
    # (e.g. "# Axiom & Postulate Ledger" stays as \chapter Axiom & Postulate Ledger).

    lines = content.split("\n")
    out = []
    stripped_first_h1 = False
    promoted_first_h3 = False
    have_h1 = False
    for line in lines:
        # 4) Strip first h1 only if it matches a structural-duplicate pattern
        if not stripped_first_h1 and not have_h1 and re.match(r"^#\s+\S", line):
            if any(pat.match(line) for pat in STRIP_H1_PATTERNS):
                stripped_first_h1 = True
                continue
            else:
                have_h1 = True
        # 1) Drop "## **GLOBAL FRONT MATTER**" / "## **BACK MATTER**"
        # and similar organizational labels (these duplicate the part-level
        # divisions emitted by the directory walker).
        if re.match(
            r"^##\s+\*\*("
            r"GLOBAL\s+FRONT\s+MATTER|GLOBAL\s+BACK\s+MATTER|GLOBAL\s+APPENDICES|"
            r"FRONT\s+MATTER|BACK\s+MATTER|APPENDICES"
            r")\*\*\s*$",
            line,
            re.IGNORECASE,
        ):
            continue
        # 2) "## PART X: ..." → standalone divider page.
        # \clearpage forces the PART label to start a fresh page so it
        # doesn't end up dangling at the bottom of the previous chapter.
        m_part_h2 = re.match(r"^##\s+\*?\*?\s*(PART\s+[IVX]+[^*\n]*?)\*?\*?\s*$", line)
        if m_part_h2:
            label = m_part_h2.group(1).strip().rstrip(":")
            out.append("")
            out.append("\\clearpage")
            # No running header/footer on the part-divider page (otherwise it
            # carries the previous chapter's running head).
            out.append("\\thispagestyle{empty}")
            out.append("\\vspace*{0.35\\textheight}")
            out.append(f"\\begin{{center}}\\bfseries\\LARGE {label}\\end{{center}}")
            out.append("\\vspace*{\\fill}")
            out.append("\\clearpage\n")
            continue
        # Drop "## **Subtitle**" line immediately after a stripped volume h1
        if stripped_first_h1 and not promoted_first_h3 and not have_h1:
            m_subtitle = re.match(r"^##\s+\*\*([^*]+)\*\*\s*$", line)
            if m_subtitle and "PART" not in m_subtitle.group(1).upper():
                out.append(f"\\begin{{center}}\\large\\textit{{{m_subtitle.group(1)}}}\\end{{center}}\n")
                continue
        # 3) Promote first opener-style h3 to h1 (\chapter)
        if not promoted_first_h3 and not have_h1:
            for pat in OPENER_PATTERNS:
                if pat.match(line):
                    title = re.sub(r"^###\s+\*?\*?", "", line).rstrip()
                    title = title.rstrip("*").strip()
                    # Keep the author's manual "Chapter N:" prefix verbatim.
                    # LaTeX auto section/chapter numbering is suppressed
                    # (secnumdepth=-1 in the preamble; no --number-sections), so
                    # the manuscript's manual numbering — which every in-text
                    # cross-reference resolves to — is the single rendered scheme.
                    out.append(f"# {title}")
                    promoted_first_h3 = True
                    have_h1 = True
                    break
            else:
                out.append(line)
                continue
            continue
        out.append(line)
    return "\n".join(out)


def _promote_bold_subsection_paragraphs(content: str) -> str:
    """
    Promote bold-paragraph subsection markers of the form

        **1.1 The Problem of the Starting Point**
        **1.1.1 The Crisis in Foundational Physics**

    to real markdown headings (### / #### / etc.) so they appear in the
    table of contents and get proper LaTeX \section / \subsection
    numbering instead of being rendered as inline bold paragraphs.

    Required because most Volume 1 chapters use the bold-paragraph
    convention while Volumes 2/3 use explicit `### N.N.N` h3 headings.
    Without this promotion, Vol 1 chapters show no subsections in the
    TOC while Vol 2/3 do — the inconsistency Pablo flagged in tg1.

    Mapping (by section-number depth):
      N.N          (e.g. 1.1)       → h3 (\section)         — DEPTH 2
      N.N.N        (e.g. 1.1.1)     → h4 (\subsection)      — DEPTH 3
      N.N.N.N      (e.g. 1.1.1.1)   → h5 (\subsubsection)   — DEPTH 4

    Promotion fires only when the line is the SOLE content of a
    bold-paragraph and matches the canonical numbering pattern. Inline
    bold text inside other paragraphs is unaffected.
    """
    NUMBERED_BOLD_PARA = re.compile(
        r"^\*\*(\d+(?:\.\d+){1,3})\s+([^*\n]+?)\*\*\s*$"
    )
    out_lines: list[str] = []
    for line in content.split("\n"):
        m = NUMBERED_BOLD_PARA.match(line)
        if m:
            number = m.group(1)
            title = m.group(2).strip()
            depth = number.count(".") + 1
            # depth 2 (e.g., 1.1)   → h3
            # depth 3 (e.g., 1.1.1) → h4
            # depth 4 (e.g., 1.1.1.1) → h5
            hashes = "#" * (depth + 1)
            out_lines.append(f"{hashes} {number} {title}")
            continue
        out_lines.append(line)
    return "\n".join(out_lines)


def _rewrite_parameter_ledger_tables(content: str) -> str:
    """
    The Parameter Ledger has 7-column pipe tables where the "Notes" column
    contains long narrative text. Pandoc's default column auto-sizing gives
    every column roughly equal width, which forces the Notes column to wrap
    one-word-per-line and produces the visually broken layout Pablo flagged.

    We detect 7-column pipe tables in this file and rewrite them as raw
    LaTeX `longtable` with explicit column widths:
        Symbol            5%
        Name              12%
        Type              12%
        Value             12%
        First Appearance  10%
        Used In           10%
        Notes             39%

    The total is intentionally < 100% to leave room for column separators
    (`\tabcolsep` × 2 per column boundary).
    """
    # Column widths sum to a bit less than 1.0 so the table doesn't bleed
    # over the linewidth and the natural tabcolsep padding shifts the whole
    # block toward visual centre.
    # 7-col: Symbol / Name / Type / Value / First App / Used In / Notes.
    # Type carries prose (e.g. "Tier 2 integer-identification (H_3 Shephard-
    # Todd anchor) + Tier 3 physical-link conjecture"), so it gets generous
    # width to avoid the one-to-two-word-per-line crush.
    WIDTHS_7 = [0.09, 0.09, 0.18, 0.08, 0.09, 0.10, 0.30]
    # 5-col: Symbol / Name / Value / Mechanical Origin / Needed for Tier 2
    # (the last two are narrative-heavy so get the bulk of the width)
    WIDTHS_5 = [0.08, 0.14, 0.13, 0.32, 0.30]
    WIDTHS_BY_NCOL = {5: WIDTHS_5, 7: WIDTHS_7}

    def md_inline_to_latex(s: str) -> str:
        """Minimal bold/italic/code + escape for raw-LaTeX table cells."""
        s = s.strip()
        # First protect inline `code` spans by replacing with sentinels
        code_spans: list[str] = []

        def _code_sub(m: re.Match) -> str:
            inner = m.group(1)
            inner = inner.replace("\\", r"\textbackslash{}")
            inner = inner.replace("{", r"\{").replace("}", r"\}")
            inner = inner.replace("&", r"\&").replace("%", r"\%")
            inner = inner.replace("#", r"\#").replace("$", r"\$")
            inner = inner.replace("_", r"\_").replace("^", r"\^{}")
            inner = inner.replace("~", r"\~{}")
            idx = len(code_spans)
            code_spans.append(rf"\texttt{{{inner}}}")
            return f"\x00CODE{idx}\x00"

        s = re.sub(r"`([^`]+)`", _code_sub, s)
        # Bold: **text** → \textbf{text}
        s = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", s)
        # Italic: *text* → \textit{text}
        s = re.sub(r"(?<!\*)\*(?!\*)([^*\n]+?)\*(?!\*)", r"\\textit{\1}", s)
        # Escape LaTeX specials outside `$math$` regions.
        parts = re.split(r"(\$[^$\n]+\$)", s)
        out_parts = []
        for i, part in enumerate(parts):
            if i % 2 == 1:
                out_parts.append(part)  # math region unchanged
                continue
            # Escape `&`, `%`, `#`. Don't touch `_` here because pandoc-style
            # input may have valid escape sequences like `\_`; instead escape
            # bare underscores that aren't already preceded by a backslash.
            part = part.replace("&", r"\&").replace("%", r"\%").replace("#", r"\#")
            part = re.sub(r"(?<!\\)_", r"\\_", part)
            out_parts.append(part)
        result = "".join(out_parts)
        # Restore code spans
        for idx, code in enumerate(code_spans):
            result = result.replace(f"\x00CODE{idx}\x00", code)
        return result

    lines = content.split("\n")
    out: list[str] = []
    i = 0
    n = len(lines)
    while i < n:
        # Look for pipe-table header followed by separator row.
        line = lines[i]
        # Header pattern: starts with `|`, has 7 cells (so 7 `|` separators
        # plus the leading/trailing), is followed by a `| :--- |` separator.
        if line.startswith("|") and "|" in line[1:] and i + 1 < n:
            header_cells = [c.strip() for c in line.strip().strip("|").split("|")]
            sep_line = lines[i + 1].strip()
            sep_cells = [c.strip() for c in sep_line.strip("|").split("|")]
            if (
                len(header_cells) in WIDTHS_BY_NCOL
                and len(sep_cells) == len(header_cells)
                and all(re.match(r"^:?-+:?$", c) for c in sep_cells)
            ):
                ncol = len(header_cells)
                widths = WIDTHS_BY_NCOL[ncol]
                # Collect body rows until first non-pipe line.
                j = i + 2
                body_rows: list[list[str]] = []
                while j < n and lines[j].startswith("|"):
                    cells = [c.strip() for c in lines[j].strip("|").split("|")]
                    if len(cells) == ncol:
                        body_rows.append(cells)
                    j += 1
                # Build the longtable. The leading group sets local
                # parameters: small font, allow aggressive hyphenation so
                # long words like "Electromagnetism" can wrap inside their
                # column instead of overflowing into the next, and centre
                # the table on the line by omitting the explicit @{} hooks
                # so the standard \tabcolsep padding flanks both edges.
                col_spec = "".join(
                    f">{{\\raggedright\\arraybackslash\\hspace{{0pt}}}}p{{{w}\\linewidth}}"
                    for w in widths
                )
                lt = []
                # \begingroup / \endgroup keeps \footnotesize and the
                # hyphenation parameter changes scoped to the table.
                # Using raw \begingroup (not `{`) so pandoc passes it
                # through as raw LaTeX rather than escaping the brace.
                lt.append(r"\begingroup")
                lt.append(r"\footnotesize")
                lt.append(r"\setlength{\LTpre}{0pt}\setlength{\LTpost}{0pt}")
                lt.append(r"\hyphenpenalty=50\exhyphenpenalty=50")
                lt.append(r"\sloppy")
                lt.append(rf"\begin{{longtable}}{{{col_spec}}}")
                # Header
                lt.append(r"\toprule")
                lt.append(
                    " & ".join(rf"\textbf{{{md_inline_to_latex(c)}}}" for c in header_cells)
                    + r" \\"
                )
                lt.append(r"\midrule")
                lt.append(r"\endhead")
                lt.append(r"\bottomrule")
                lt.append(r"\endlastfoot")
                # Body
                for row in body_rows:
                    lt.append(" & ".join(md_inline_to_latex(c) for c in row) + r" \\")
                    lt.append(r"\addlinespace[2pt]")
                lt.append(r"\end{longtable}")
                lt.append(r"\endgroup")
                out.append("")
                out.append("\n".join(lt))
                out.append("")
                i = j
                continue
        out.append(line)
        i += 1
    return "\n".join(out)


def _strip_engine_paths(s: str) -> str:
    """Shorten long engine/verifier path prefixes to their basename so they
    don't overrun narrow table cells. The markdown source keeps the full
    machine-readable path; only the typeset PDF shows the basename."""
    for pref in (
        "GCT_Physics_Engine/src/",
        "GCT_Physics_Engine/data/",
        "verify_independent/results/",
        "verify_independent/",
    ):
        s = s.replace(pref, "")
    return s


def _md_table_cell_to_latex(s: str, strip_paths: bool = False) -> str:
    """Convert a markdown table/block cell to raw LaTeX. Because this output
    bypasses pandoc, the converter must do pandoc's job: protect math, code,
    and markdown backslash-escapes, then escape every text-mode LaTeX special
    (incl. bare `^`, `~`, braces — common in prose cells like `phi^phi`),
    then apply bold/italic. Order matters so generated \\textbf/\\textit
    braces are not themselves escaped."""
    s = s.strip()
    if strip_paths:
        s = _strip_engine_paths(s)

    saved: list[str] = []

    def _save(txt: str) -> str:
        saved.append(txt)
        return f"\x00S{len(saved) - 1}\x00"

    # 1. Protect inline math $...$ (rendered verbatim).
    s = re.sub(r"\$[^$\n]+\$", lambda m: _save(m.group(0)), s)

    # 2. Protect `code` spans (escape their interior for \texttt).
    def _code(m: "re.Match") -> str:
        inner = m.group(1)
        for a, b in (("\\", r"\textbackslash{}"), ("{", r"\{"), ("}", r"\}"),
                     ("&", r"\&"), ("%", r"\%"), ("#", r"\#"), ("$", r"\$"),
                     ("_", r"\_"), ("^", r"\^{}"), ("~", r"\~{}")):
            inner = inner.replace(a, b)
        return _save(rf"\texttt{{{inner}}}")

    s = re.sub(r"`([^`]+)`", _code, s)

    # 3. Protect markdown backslash-escapes so they aren't parsed as emphasis
    #    or escaped again (e.g. a stray `\*\*`).
    s = s.replace(r"\*", _save("*")).replace(r"\_", _save(r"\_"))

    # 4. Escape text-mode LaTeX specials in the remaining plain text. Backslash
    #    first (the others insert backslashes). This turns bare `phi^phi`,
    #    `{x}`, stray `\foo`, etc. into harmless literal text.
    for a, b in (("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
                 ("#", r"\#"), ("{", r"\{"), ("}", r"\}"), ("_", r"\_"),
                 ("^", r"\^{}"), ("~", r"\textasciitilde{}")):
        s = s.replace(a, b)

    # 5. Emphasis — inserted AFTER escaping so their braces survive.
    s = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", s)
    s = re.sub(r"(?<!\*)\*(?!\*)([^*\n]+?)\*(?!\*)", r"\\textit{\1}", s)

    # 6. Restore protected segments.
    for i, txt in enumerate(saved):
        s = s.replace(f"\x00S{i}\x00", txt)
    return s


def _norm_header_cell(c: str) -> str:
    """Normalize a header cell for config matching: strip markdown emphasis."""
    return re.sub(r"[*_`]", "", c).strip()


def _split_pipe_row(line: str) -> list:
    """Split a markdown pipe-table row into cells, honoring escaped pipes
    (`\\|`, common in cells like `\\|Delta_a_tau\\|`). A naive split('|')
    over-splits these and silently drops the row from the rebuilt table."""
    inner = line.strip()
    if inner.startswith("|"):
        inner = inner[1:]
    if inner.endswith("|"):
        inner = inner[:-1]
    cells = re.split(r"(?<!\\)\|", inner)
    return [c.strip().replace(r"\|", "|") for c in cells]


# Tables whose cells contain multi-paragraph prose (a single cell can exceed a
# page) cannot be set as a longtable — longtable cannot break one row across
# pages, so a 400-word cell overflows the bottom margin. These are restructured
# into per-row prose blocks: the short fields become a labeled run-in and the
# long fields become ordinary paragraphs that page-break naturally.
#   title_idx → bold entry heading; badge_idx → appended after an em dash;
#   labels[i]=None → that column is consumed by the title/badge (not re-printed).
_BLOCK_TABLE_CONFIGS = {
    "03_Parameter_Ledger.md": [
        {  # postulate ledger: every row's Status + Tier columns hold prose
            "ncol": 6, "header0": "#", "title_idx": 0, "badge_idx": 3,
            "strip": True,
            "labels": [None, "Postulate", "Type", None, "Status",
                       "Cross-reference"],
        },
    ],
    "App_FM_Falsifiability_Matrix.md": [
        {
            "ncol": 10, "header0": "ID", "title_idx": 0, "badge_idx": 9,
            "strip": True,
            "labels": [None, "Reference", "Tier", "Value", "Precision (ppm)",
                       "Falsification band", "Disposition", "Experiment",
                       "Timeframe", None],
        },
    ],
    "Ch17_Physical_Substrate.md": [
        {
            "ncol": 4, "header0": "System", "title_idx": 0, "badge_idx": None,
            "strip": False,
            "labels": [None, "GCT prediction", "IIT prediction",
                       "Distinguishing test"],
        },
    ],
    # App R precision-scorecard tables carry two prose-heavy columns per row
    # (a "what it means" justification plus a Tier accounting), so for some
    # rows two columns each hold ~100 words — impossible to set as a readable
    # multi-column longtable. Restructured to per-row blocks like FM.4.
    "App_R_Precision_Scorecard.md": [
        {  # particle precision scorecard
            "ncol": 9, "header0": "Particle", "title_idx": 0, "badge_idx": 6,
            "strip": True,
            "labels": [None, "Formula", "Derived", "Observed",
                       "Coefficient accounting", "Headline precision",
                       None, "Provenance", "Tier"],
        },
        {  # coupling-constant scorecard
            "ncol": 8, "header0": "Constant", "title_idx": 0, "badge_idx": 5,
            "strip": True,
            "labels": [None, "Formula", "Derived (bare)", "Observed",
                       "Residual (gap)", None, "Provenance", "Tier"],
        },
        {  # extended particle scorecard
            "ncol": 10, "header0": "Particle", "title_idx": 0, "badge_idx": 7,
            "strip": True,
            "labels": [None, "Formula", "Derived", "Empirical convention",
                       "Scale", "Observed", "Precision (residual)",
                       None, "Provenance", "Tier"],
        },
        {  # observable scorecards (three structurally identical 7-col tables)
            "ncol": 7, "header0": "Observable", "title_idx": 0, "badge_idx": 5,
            "strip": True,
            "labels": [None, "Formula", "Prediction", "Observed / bound",
                       "Precision / status", None, "Tier"],
        },
    ],
}

# Column-data tables (short cells, many columns / long monospace paths) that
# overflow the portrait text width with pandoc's equal-width auto-sizing. These
# are re-emitted as a scriptsize longtable with explicit column widths and
# basename-shortened paths. Single \endhead (no \endfirsthead) also removes the
# duplicate-header artifact pandoc emits for these.
# Width arrays sum to ~0.85-0.89 of \linewidth; the remainder is consumed by
# the (tightened) tabcolsep so the rendered table fits inside the text block.
_WIDE_TABLE_CONFIGS = {
    "App_V_Prediction_Registry.md": [
        {"ncol": 8, "header0": "Prediction ID", "strip": True, "font": r"\scriptsize",
         "widths": [0.06, 0.06, 0.11, 0.09, 0.18, 0.11, 0.09, 0.14]},
    ],
}


def _render_block_entry(spec: dict, header_cells: list, row: list) -> str:
    """Render one table row as a per-row prose block (raw LaTeX, no blank
    lines so pandoc keeps it as a single raw block)."""
    strip = spec.get("strip", False)
    labels = spec["labels"]
    title = _md_table_cell_to_latex(row[spec["title_idx"]], strip)
    head = rf"\medskip\textbf{{{title}}}"
    if spec.get("badge_idx") is not None:
        badge = _md_table_cell_to_latex(row[spec["badge_idx"]], strip)
        if badge and badge != "—":
            head += rf" — {badge}"
    lines = [head + r"\par"]
    for i, cell in enumerate(row):
        label = labels[i] if i < len(labels) else None
        if label is None:
            continue
        val = _md_table_cell_to_latex(cell, strip)
        if not val:
            continue
        lines.append(rf"\textit{{{label}:}} {val}\par")
    return "\n".join(lines)


def _render_wide_longtable(spec: dict, header_cells: list, body_rows: list) -> str:
    """Render a column-data table as a scriptsize raw-LaTeX longtable with
    explicit widths and basename-shortened paths."""
    strip = spec.get("strip", False)
    widths = spec["widths"]
    font = spec.get("font", r"\footnotesize")
    col_spec = "".join(
        rf">{{\raggedright\arraybackslash\hspace{{0pt}}}}p{{{w}\linewidth}}"
        for w in widths
    )
    lt = [r"\begingroup", font,
          r"\setlength{\LTpre}{0pt}\setlength{\LTpost}{0pt}",
          # Tight inter-column padding: with many columns the default 6pt
          # tabcolsep adds ~0.12-0.13\linewidth of overhead, which pushes the
          # declared table width past \linewidth and clips the last column.
          r"\setlength{\tabcolsep}{3pt}",
          r"\hyphenpenalty=50\exhyphenpenalty=50", r"\sloppy",
          rf"\begin{{longtable}}{{{col_spec}}}", r"\toprule",
          " & ".join(rf"\textbf{{{_md_table_cell_to_latex(c, strip)}}}" for c in header_cells) + r" \\",
          r"\midrule", r"\endhead", r"\bottomrule", r"\endlastfoot"]
    for row in body_rows:
        lt.append(" & ".join(_md_table_cell_to_latex(c, strip) for c in row) + r" \\")
        lt.append(r"\addlinespace[2pt]")
    lt.append(r"\end{longtable}")
    lt.append(r"\endgroup")
    return "\n".join(lt)


def _plain_len(cell: str) -> int:
    """Approximate rendered length of a cell for width proportioning: drop
    markdown/math markup characters that don't take horizontal space."""
    return len(re.sub(r"[*`$\\]", "", cell))


def _auto_wide_spec(header_cells: list, body_rows: list):
    """If an unconfigured pipe table is wide or prose-heavy enough to overflow
    the portrait text width under pandoc's equal-width auto-sizing, return a
    wide-longtable spec with column widths proportional to each column's
    longest cell. Otherwise return None (let pandoc render it normally)."""
    ncol = len(header_cells)
    rows = [header_cells] + body_rows
    col_max = [max((_plain_len(r[c]) for r in rows if c < len(r)), default=1)
               for c in range(ncol)]
    longest = max(col_max)
    # Trigger only for genuinely wide or prose-heavy tables; leave compact
    # tables (legends, short 3-4 col tables) to pandoc.
    if not (ncol >= 6 or (ncol >= 4 and longest > 160)):
        return None
    weights = [min(max(m, 6), 360) for m in col_max]
    total = sum(weights) or 1
    widths = [round(w / total * 0.88, 4) for w in weights]
    # Floor very narrow columns so single short words still fit.
    widths = [max(w, 0.03) for w in widths]
    return {"widths": widths, "font": r"\scriptsize", "strip": True}


def _rewrite_custom_tables(content: str, file_name: str) -> str:
    """Scan pipe tables and re-render: configured prose tables as per-row
    blocks (_BLOCK_TABLE_CONFIGS), configured wide tables as scriptsize
    longtables (_WIDE_TABLE_CONFIGS), and any other wide/prose-heavy table via
    a proportional-width auto-wide fallback. Compact tables pass through to
    pandoc."""
    block_specs = _BLOCK_TABLE_CONFIGS.get(file_name, [])
    wide_specs = _WIDE_TABLE_CONFIGS.get(file_name, [])

    def _match(specs, ncol, header0):
        for sp in specs:
            if sp["ncol"] == ncol and _norm_header_cell(header0) == sp["header0"]:
                return sp
        return None

    lines = content.split("\n")
    out: list[str] = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if line.startswith("|") and "|" in line[1:] and i + 1 < n:
            header_cells = _split_pipe_row(line)
            sep_cells = _split_pipe_row(lines[i + 1])
            if (
                len(sep_cells) == len(header_cells)
                and all(re.match(r"^:?-+:?$", c) for c in sep_cells)
            ):
                ncol = len(header_cells)
                header0 = header_cells[0]
                block_sp = _match(block_specs, ncol, header0)
                wide_sp = _match(wide_specs, ncol, header0)
                # Collect body rows.
                j = i + 2
                body_rows: list[list[str]] = []
                while j < n and lines[j].startswith("|"):
                    cells = _split_pipe_row(lines[j])
                    if len(cells) == ncol:
                        body_rows.append(cells)
                    j += 1
                auto_sp = None
                if not block_sp and not wide_sp:
                    auto_sp = _auto_wide_spec(header_cells, body_rows)
                if block_sp or wide_sp or auto_sp:
                    out.append("")
                    if block_sp:
                        out.append(r"\begingroup\setlength{\parindent}{0pt}")
                        for row in body_rows:
                            out.append(_render_block_entry(block_sp, header_cells, row))
                        out.append(r"\endgroup")
                    else:
                        out.append(_render_wide_longtable(wide_sp or auto_sp, header_cells, body_rows))
                    out.append("")
                    i = j
                    continue
        out.append(line)
        i += 1
    return "\n".join(out)


def _is_unnumbered_chapter_file(path: Path) -> bool:
    """
    Files that should produce \chapter* (unnumbered) so the \chapter
    counter doesn't increment past them. Real chapters (Ch01_*) keep
    their normal numbered \chapter behavior.

    Triggers on:
      - Global Frontmatter files (content/00_Global_Frontmatter/*.md)
      - Volume frontmatter files (content/0N_Volume_*/00_Frontmatter/*.md)
      - Volume backmatter files (content/0N_Volume_*/99_Backmatter/*.md)
      - Global Backmatter files (content/99_Global_Backmatter/*.md)
      - Global Appendices files (content/98_Global_Appendices/*.md) —
        29 appendices (A-Z + R2 + TP + ZN) exceed LaTeX \appendix A-Z
        letter mode, so we keep them as \chapter* with the title
        carrying its own "Appendix X:" prefix.
    """
    parts_in_path = [p.name for p in path.parents]
    if "00_Global_Frontmatter" in parts_in_path:
        return True
    if "99_Global_Backmatter" in parts_in_path:
        return True
    if "98_Global_Appendices" in parts_in_path:
        return True
    # Per-volume frontmatter/backmatter sit one level under a Volume_ dir
    parent = path.parent.name
    if parent in ("00_Frontmatter", "99_Backmatter"):
        return True
    return False


def _convert_first_h1_to_unnumbered_chapter(content: str) -> str:
    """
    Replace the first `# Title` h1 in the content with a raw LaTeX
    `\chapter*{Title}` + a TOC line, so this file shows up in the table of
    contents but does NOT advance the \chapter counter. Also reset the
    section counter so any internal `## Section` doesn't inherit a prefix
    from the previous numbered chapter (e.g. "26.1, 26.2" inside the
    appendices).
    """
    lines = content.split("\n")
    out = []
    converted = False
    for line in lines:
        if not converted:
            m = re.match(r"^#\s+(.+?)\s*$", line)
            if m:
                title = m.group(1).strip().strip("*").strip()
                # Escape LaTeX special chars that survive into the title
                tex_title = title.replace("&", r"\&").replace("%", r"\%")
                out.append(f"\n\\chapter*{{{tex_title}}}")
                out.append(f"\\addcontentsline{{toc}}{{chapter}}{{{tex_title}}}")
                out.append(f"\\markboth{{{tex_title}}}{{{tex_title}}}")
                # Reset section counter so internal `## Section` lines
                # get clean 1.x.y numbering rather than inheriting the
                # previous numbered chapter's prefix. We also bump the
                # chapter counter temporarily for the section prefix.
                out.append(f"\\setcounter{{section}}{{0}}\n")
                converted = True
                continue
        out.append(line)
    return "\n".join(out)


def _dir_header_markdown(path: Path, level: int) -> str:
    """
    Emit the markdown header for a directory traversal node.

    Top-level (level=1) directories emit raw LaTeX \part or \part*
    (bypassing pandoc's heading-to-section mapping, since we're using the
    default top-level-division=chapter where h1 → \chapter):
      00_Global_Frontmatter   → \part* (unnumbered)
      01_Volume_1_*           → \part (numbered I)
      02_Volume_2_*           → \part (numbered II)
      03_Volume_3_*           → \part (numbered III)
      98_Global_Appendices    → \part* (unnumbered)
      99_Global_Backmatter    → \part* (unnumbered)

    After each numbered \part for a Volume, reset the chapter counter so
    chapter numbering restarts from 1 within each Volume (Vol 1 Ch 1-25,
    Vol 2 Ch 1-14, Vol 3 Ch 1-22, plus Appendices A-ZN).

    Mid-level directories (level >= 2) are NOT emitted — the chapters
    within them carry their own opener heading and we don't want
    spurious section labels.
    """
    name = path.stem
    if level == 1:
        # Map filesystem dir name → display label and numbered/unnumbered class
        m = re.match(r"^\d+_(.+)$", name)
        clean = (m.group(1) if m else name).replace("_", " ")
        if clean.lower().startswith("volume"):
            # Numbered part — Roman-numbered. Reset \chapter counter so
            # chapter numbering restarts at 1 within each Volume.
            label = clean.replace("Volume ", "VOLUME ")
            return (
                f"\n\\part{{{label}}}\n"
                f"\\setcounter{{chapter}}{{0}}\n\n"
            )
        else:
            # Unnumbered part — keeps a TOC entry but no Part-N label.
            label = {
                "Global Frontmatter": "Front Matter",
                "Global Appendices": "Appendices",
                "Global Backmatter": "Back Matter",
            }.get(clean, clean)
            return (
                f"\n\\part*{{{label}}}\n"
                f"\\addcontentsline{{toc}}{{part}}{{{label}}}\n"
                f"\\markboth{{{label}}}{{{label}}}\n\n"
            )
    return ""


def assemble_markdown() -> str:
    """
    Walk content/ in canonical order and concatenate every .md file.

    Heading-hierarchy convention (with pandoc --top-level-division=part):
      h1 → \part     ← top-level dirs only (Volumes; Front/Back/Appendices use raw \part*)
      h2 → \chapter  ← actual chapters (Ch01, Ch02, ...) after normalization
      h3 → \section  ← section headings inside chapters
    """
    parts = []
    # Title block — printed once at the very top of the PDF. We deliberately
    # omit the internal version label here so that the public PDF carries
    # only title + subtitle + author + date.
    parts.append(
        f"\\thispagestyle{{empty}}\n"
        f"\\begin{{center}}\n"
        f"\\Large\\textbf{{{METADATA['title']}}}\\\\[0.5em]\n"
        f"\\large{{{METADATA.get('subtitle', '')}}}\\\\[1em]\n"
        f"\\normalsize {METADATA['author']}\\\\[0.5em]\n"
        f"{METADATA['date']}\n"
        f"\\end{{center}}\n"
        f"\\newpage\n"
    )

    last_top_level_dir = None
    for kind, entry, level in walk_content_files():
        if kind == "DIR":
            header = _dir_header_markdown(entry, level)
            if header:
                parts.append(header)
            if level == 1:
                # Page break between top-level sections (volumes / appendices)
                if last_top_level_dir is not None:
                    parts.append("\n\\newpage\n")
                last_top_level_dir = entry
        elif kind == "FILE":
            resolved = str(entry.resolve())
            if resolved in _processed_files:
                continue
            _processed_files.add(resolved)
            print(f"  [READ] {entry.relative_to(PROJECT_ROOT)}")
            content = entry.read_text(encoding="utf-8").strip()
            # Demote in-file headings to align with the part/chapter hierarchy
            content = _demote_in_file_top_headings(content)
            # Promote bold-paragraph subsection markers (`**1.1 X**`) to
            # real h3/h4 headings so they appear in the TOC. Most Vol 1
            # chapters use this convention; Vol 2/3 already use explicit
            # `### N.N.N` h3 syntax. Normalising both keeps the TOC
            # consistent across volumes.
            content = _promote_bold_subsection_paragraphs(content)
            # If this is the Parameter Ledger, rewrite its wide 7-column
            # tables to raw LaTeX longtable with explicit column widths so
            # the Notes column gets enough room.
            if entry.name == "03_Parameter_Ledger.md":
                content = _rewrite_parameter_ledger_tables(content)
            # Restructure prose-heavy / wide appendix + chapter tables that
            # overflow the portrait text width (FM.4 matrix, GCT-vs-IIT,
            # App R scorecards, App V registry). No-op for unconfigured files.
            content = _rewrite_custom_tables(content, entry.name)
            # If post-demotion content has NO h1 anywhere, prepend a fallback
            # chapter header derived from the file stem. We attach it to
            # the content (not the parts list) so the subsequent
            # unnumbered-chapter conversion can see it.
            has_h1 = re.search(r"^#\s+\S", content, re.MULTILINE) is not None
            if not has_h1:
                stem = entry.stem
                # Strip multiple numeric prefixes: "01_", "00_", "Ch04_00_", etc.
                stem = re.sub(r"^(\d+_)+", "", stem)
                stem = re.sub(r"^Ch\d+_(\d+_)?", "", stem)
                stem = re.sub(r"^App_[A-Z]+_", r"Appendix \g<0>", stem) if stem.startswith("App_") else stem
                stem = stem.replace("_", " ")
                content = f"# {stem}\n\n" + content
                has_h1 = True
            # If the file is volume frontmatter / global frontmatter /
            # volume backmatter / global backmatter / appendix, demote the
            # chapter to \chapter* (unnumbered) so the chapter counter
            # doesn't advance for these non-content sections. This way real
            # chapters (Ch01_Staircase, etc.) start at Chapter 1 within each
            # volume.
            if _is_unnumbered_chapter_file(entry):
                content = _convert_first_h1_to_unnumbered_chapter(content)
            parts.append(content)
            parts.append("\n")

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# 6. Clean output directory (idempotent build)
# ---------------------------------------------------------------------------

def reset_output_dir():
    """
    Remove every auxiliary file generated by previous pdflatex runs so the
    build is reproducible from scratch. Keeps unrelated artifacts (figure
    catalogs, manifests) untouched.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    stem = Path(METADATA["output_filename_tex"]).stem
    aux_exts = [".aux", ".log", ".toc", ".out", ".lof", ".lot", ".tex", ".pdf"]
    for ext in aux_exts:
        p = OUTPUT_DIR / f"{stem}{ext}"
        if p.exists():
            p.unlink()


# ---------------------------------------------------------------------------
# 7. Log-file error detection (C-6 fix)
# ---------------------------------------------------------------------------

# Lines starting with "! " in a pdflatex .log are real errors (LaTeX
# Error / Package Error / Undefined control sequence / etc.). We collect them.
_ERROR_LINE_RE = re.compile(r"^!\s")


def collect_log_errors(log_path: Path, limit: int = 50):
    """Return a list of error lines (and surrounding context) from a pdflatex log."""
    if not log_path.exists():
        return []
    errors = []
    try:
        text = log_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return [f"<could not read log: {log_path}>"]
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if _ERROR_LINE_RE.match(line):
            # Capture this line and 2 following lines for context
            block = "\n".join(lines[i:i + 3])
            errors.append(block)
            if len(errors) >= limit:
                break
    return errors


# ---------------------------------------------------------------------------
# 8. Main build pipeline
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("GCT LaTeX Compiler — Full Manuscript")
    print("=" * 60)

    # 8a. Dependency check
    pandoc, pdflatex = check_dependencies()
    print(f"  pandoc   : {pandoc}")
    print(f"  pdflatex : {pdflatex or 'NOT FOUND (PDF skipped)'}")
    print("-" * 60)

    # 8b. Reset output dir (idempotent build)
    print("Resetting output directory...")
    reset_output_dir()
    print(f"  Output dir: {OUTPUT_DIR}")

    # 8c. Assemble markdown from full content tree
    print("\nAssembling source files (full manuscript)...")
    markdown = assemble_markdown()
    print(f"  Total markdown size: {len(markdown) / 1024:.1f} KB")

    # 8d. Pre-process math, inline figures, alert blocks
    print("Running double-backslash-in-math normalizer...")
    markdown = preprocess_thematic_breaks(markdown)
    markdown = preprocess_double_backslash_in_math(markdown)
    print("Running math-adjacency pre-processor...")
    markdown = preprocess_math_adjacency(markdown)
    print("Running inline figure pre-processor...")
    markdown = preprocess_inline_figures(markdown)
    print("Running SVG image-link pre-processor...")
    markdown = preprocess_svg_image_links(markdown)
    print("Running alert pre-processor...")
    markdown = preprocess_alerts(markdown)

    # 8e. Write preamble + markdown to temp files
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".tex", delete=False, encoding="utf-8"
    ) as tmp_preamble:
        tmp_preamble.write(LATEX_PREAMBLE)
        preamble_path = tmp_preamble.name

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as tmp_md:
        tmp_md.write(markdown)
        md_path = tmp_md.name

    # Colophon / citation page — rendered on the verso (immediately after the
    # cover, before the table of contents) via pandoc --include-before-body, so
    # a forwarded PDF is self-contained: how-to-cite, the always-latest concept
    # DOI, repository, website, contact, and license travel with the file.
    colophon_path = None
    if METADATA.get("doi_concept"):
        _year = METADATA["date"].split()[-1]
        _colophon = (
            r"\thispagestyle{empty}" "\n"
            r"\vspace*{\fill}" "\n"
            r"\begin{center}" "\n"
            r"{\large\textbf{" + METADATA["title"] + r"}}\\[0.3em]" "\n"
            r"{\itshape " + METADATA.get("subtitle", "") + r"}\\[1.5em]" "\n"
            r"\end{center}" "\n"
            r"{\raggedright" "\n"
            r"\noindent\textbf{Author.}\, " + METADATA["author"]
            + r"\par\medskip" "\n"
            r"\noindent\textbf{How to cite.}\, González Acosta, P. (" + _year
            + r"). \textit{" + METADATA["title"] + r": "
            + METADATA.get("subtitle", "") + r".} Zenodo. "
            r"\url{https://doi.org/" + METADATA["doi_concept"] + r"}\par\medskip" "\n"
            r"\noindent\textbf{DOI (all versions).}\, "
            r"\url{https://doi.org/" + METADATA["doi_concept"] + r"}\par\smallskip" "\n"
            r"\noindent\textbf{Repository \& verification engine.}\, "
            r"\url{" + METADATA["repo_url"] + r"}\par\smallskip" "\n"
            r"\noindent\textbf{Web.}\, \url{" + METADATA["website"] + r"}\par\smallskip" "\n"
            r"\noindent\textbf{Contact.}\, \href{mailto:" + METADATA["email"]
            + r"}{\texttt{" + METADATA["email"] + r"}}\quad ORCID: "
            r"\href{https://orcid.org/" + METADATA["orcid"] + r"}{"
            + METADATA["orcid"] + r"}\par\medskip" "\n"
            r"\noindent\textbf{License.}\, Manuscript: CC-BY-4.0.\quad Engine: MIT.\par" "\n"
            r"}" "\n"
            r"\vspace*{\fill}" "\n"
            r"\newpage" "\n"
        )
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tex", delete=False, encoding="utf-8"
        ) as tmp_colophon:
            tmp_colophon.write(_colophon)
            colophon_path = tmp_colophon.name

    try:
        # 8f. Run pandoc → .tex
        print(f"\nRunning pandoc → {OUTPUT_TEX.name} ...")
        pandoc_cmd = [
            pandoc,
            md_path,
            "--standalone",
            # Disable yaml_metadata_block: lots of source files use --- as
            # section separators which would otherwise be parsed as YAML.
            # Enable tex_math_single_backslash so we can rewrite `$math$`
            # adjacent to alphanumerics as `\(math\)` (which pandoc-markdown
            # doesn't restrict like `$...$`).
            "--from", "markdown+raw_tex+tex_math_single_backslash-yaml_metadata_block",
            "--to", "latex",
            "--output", str(OUTPUT_TEX),
            "--include-in-header", preamble_path,
            "--variable", "documentclass=book",
            # `openright` (default) forces every chapter to start on a
            # right-hand (recto) page, inserting a blank verso when the
            # previous chapter ends on a recto. This is the convention
            # for printed books — kept because Pablo plans to print.
            "--variable", "fontsize=11pt",
            "--variable", f"title={METADATA['title']}: {METADATA.get('subtitle', '')}",
            "--variable", f"author={METADATA['author']}",
            "--variable", f"date={METADATA['date']}",
            "--toc",
            "--toc-depth=3",
            # Heading-hierarchy strategy:
            #   - Default top-level-division=chapter for book class
            #     (h1 → \chapter, h2 → \section, h3 → \subsection)
            #   - Top-level directories (Volumes / Front-/Back-matter /
            #     Appendices) emit RAW LaTeX \part / \part* via the dir
            #     walker — bypassing pandoc heading processing entirely.
            #   - Each content file is normalized by
            #     _demote_in_file_top_headings so its opener becomes the
            #     chapter h1, "PART X" labels become centered bold display,
            #     and inner h2/h3 numbering survives intact.
            #   - This eliminates the cascade where front-matter dirs were
            #     promoted to Chapter 1, 2, 3 and real chapters ended up as
            #     6.3.1, 6.3.2, ...
        ]
        if colophon_path:
            # Lands between \maketitle and \tableofcontents (verso citation page).
            pandoc_cmd += ["--include-before-body", colophon_path]
        result = subprocess.run(
            pandoc_cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode != 0:
            print(f"[ERROR] pandoc failed:\n{result.stderr}")
            sys.exit(1)
        print(f"  [OK] .tex written: {OUTPUT_TEX} ({OUTPUT_TEX.stat().st_size / 1024:.1f} KB)")

        # 8g. Run pdflatex (twice for TOC/refs)
        if pdflatex:
            log_path = OUTPUT_TEX.with_suffix(".log")
            for pass_num in (1, 2):
                print(f"\nRunning pdflatex (pass {pass_num}/2)...")
                pdf_result = subprocess.run(
                    [
                        pdflatex,
                        "-interaction=nonstopmode",
                        "-output-directory", str(OUTPUT_DIR),
                        str(OUTPUT_TEX),
                    ],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    cwd=str(OUTPUT_DIR),
                )

                # C-6 fix: detect errors from the .log, not the exit code.
                # pdflatex's exit code is unreliable in nonstopmode; the truth
                # lives in the log file's "! " error lines.
                log_errors = collect_log_errors(log_path)

                if log_errors:
                    print(f"  [FAIL] pdflatex pass {pass_num}: {len(log_errors)} LaTeX error(s) detected.")
                    print("  ---- First errors ----")
                    for err in log_errors[:10]:
                        print("  " + err.replace("\n", "\n  "))
                    print("  ----------------------")
                    if pass_num == 2:
                        print(f"[ERROR] Build failed. See {log_path} for details.")
                        sys.exit(2)
                    else:
                        # Pass 1 may have pseudo-errors that pass 2 resolves
                        # (e.g. forward refs). Continue but warn.
                        print(f"  [WARN] Continuing to pass 2 to see if these resolve.")
                else:
                    print(f"  [OK] pdflatex pass {pass_num} clean.")

            if OUTPUT_PDF.exists():
                page_count = "?"
                try:
                    # Pull page count from the log: "Output written ... (N pages, ..."
                    # pdflatex wraps log lines, so flatten line breaks first.
                    log_text = log_path.read_text(encoding="utf-8", errors="replace")
                    flat = log_text.replace("\r", "").replace("\n", " ")
                    m = re.search(r"Output written on .*?\((\d+)\s*pages", flat)
                    if m:
                        page_count = m.group(1)
                except Exception:
                    pass
                print(
                    f"\n  [OK] PDF written: {OUTPUT_PDF} "
                    f"({OUTPUT_PDF.stat().st_size / 1024:.1f} KB, {page_count} pages)"
                )
            else:
                print(f"[ERROR] PDF not found after pdflatex run. See {log_path}.")
                sys.exit(3)
        else:
            print("\n[SKIP] pdflatex not available — .tex file only.")

    finally:
        Path(preamble_path).unlink(missing_ok=True)
        Path(md_path).unlink(missing_ok=True)
        if colophon_path:
            Path(colophon_path).unlink(missing_ok=True)

    print("\n" + "=" * 60)
    print("BUILD COMPLETE")
    print(f"  TEX : {OUTPUT_TEX}")
    if pdflatex and OUTPUT_PDF.exists():
        print(f"  PDF : {OUTPUT_PDF}")
    print("=" * 60)


if __name__ == "__main__":
    main()
