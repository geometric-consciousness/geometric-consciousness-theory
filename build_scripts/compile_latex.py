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

import os
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

try:
    from pypdf import PdfReader, PdfWriter
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

# Try to import SVG conversion tools
try:
    from svglib.svglib import svg2rlg
    from svglib import fonts as svglib_fonts
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
from generate_index import assert_index_fresh

# --- Paths ---
OUTPUT_DIR = PROJECT_ROOT / "output"
FIGURES_DIR = PROJECT_ROOT / "content" / "Figures"

OUTPUT_TEX = OUTPUT_DIR / METADATA["output_filename_tex"]
OUTPUT_PDF = OUTPUT_DIR / METADATA["output_filename_pdf"]

# --- LaTeX preamble (injected via pandoc --include-in-header) ---
# Note: the \DeclareUnicodeCharacter block below covers every non-ASCII
# codepoint that build_scripts/scan_unicode.py finds in content/ outside
# fenced code blocks and math regions. XeLaTeX otherwise consumes Unicode
# natively; explicit mappings preserve the manuscript's math intent.
LATEX_PREAMBLE = r"""
\usepackage[a4paper,paperwidth=210mm,paperheight=297mm,left=18mm,right=18mm,top=16mm,bottom=15mm,includeheadfoot]{geometry}
% Honor the manuscript's MANUAL section/chapter numbers (carried in the heading
% text, e.g. "Chapter 6:", "11.15.4") which every in-text cross-reference
% resolves to. Suppress LaTeX auto-numbering of chapters and below so it does
% not collide with the manual scheme (parts at level -1 stay numbered).
\setcounter{secnumdepth}{-1}
\usepackage{array}
\usepackage{longtable}
\usepackage{booktabs}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{iftex}
\ifPDFTeX
  \PackageError{gct}{XeLaTeX is required for the declared GCT publication fonts}{Use xelatex so Georgia/Segoe UI/Arial can be selected and embedded}
\else
  \usepackage{fontspec}
  % mathbf=sym: \mathbf uses the math font's bold alphabet. With the default
  % (text), \mathbf takes Segoe UI Bold, which has no math Greek, and bold
  % \Omega printed blank ("Missing character" in the build log).
  \usepackage{unicode-math}
  \unimathsetup{mathbf=sym}
  \defaultfontfeatures{Ligatures=TeX,Scale=MatchLowercase}
  \IfFontExistsTF{Segoe UI}{\setmainfont{Segoe UI}}{\IfFontExistsTF{Arial}{\setmainfont{Arial}}{\setmainfont{Latin Modern Sans}}}
  \IfFontExistsTF{Segoe UI}{\setsansfont{Segoe UI}}{\IfFontExistsTF{Arial}{\setsansfont{Arial}}{\setsansfont{Latin Modern Sans}}}
  \IfFontExistsTF{Georgia}{\newfontfamily\gctdisplayfont{Georgia}}{\IfFontExistsTF{Times New Roman}{\newfontfamily\gctdisplayfont{Times New Roman}}{\newfontfamily\gctdisplayfont{Latin Modern Roman}}}
  \setmathfont{Latin Modern Math}
\fi
\providecommand{\DeclareUnicodeCharacter}[2]{}
\usepackage[most]{tcolorbox}
\usepackage{xcolor}
\definecolor{GCTPaper}{HTML}{FBF9F4}
\definecolor{GCTInk}{HTML}{16130F}
\definecolor{GCTSoft}{HTML}{5A5247}
\definecolor{GCTLine}{HTML}{DCD5C8}
% Brand: soft copper for marks and rules,
% copper deep for small text such as links (>= 4.5:1 on paper).
\definecolor{GCTCopper}{HTML}{A8653A}
\definecolor{GCTCopperDeep}{HTML}{8E5531}
\pagecolor{GCTPaper}
\color{GCTInk}
\usepackage{graphicx}
\usepackage{textcomp}
\usepackage{newunicodechar}
\usepackage{titlesec}
% Headings are set ragged-right: a justified Huge/Large title with few words
% has no acceptable break and ran past the right margin (v1.3.0 page QA).
\titleformat{\chapter}{\gctdisplayfont\Huge\bfseries\color{GCTInk}\raggedright}{}{0pt}{}
\titleformat{\section}{\gctdisplayfont\Large\bfseries\color{GCTInk}\raggedright}{}{0pt}{}
\titleformat{\subsection}{\sffamily\large\bfseries\color{GCTInk}\raggedright}{}{0pt}{}
\titleformat{\subsubsection}{\sffamily\normalsize\bfseries\color{GCTInk}\raggedright}{}{0pt}{}
\usepackage{hyperref}
\hypersetup{
  pdftitle={Geometric Consciousness Theory: A 6D-to-3D Projective Framework},
  pdfauthor={Pablo González Acosta},
  pdfsubject={A 6D-to-3D Projective Framework},
  pdfkeywords={Geometric Consciousness Theory; 6D-to-3D projection; quasicrystal; falsifiability; verification},
  colorlinks=true,
  linkcolor=GCTCopperDeep,
  urlcolor=GCTCopperDeep,
  citecolor=GCTCopperDeep
}
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
% A heading that carries a manual \newline (e.g. V1 Ch22) must not wrap the
% running head onto two lines: \gctmark sets the mark on one line.
% (\newline is robust, so the mark stores its internal "\newline " name.)
\newcommand{\gctmark}{{\def\newline{\space}\expandafter\def\csname newline \endcsname{\space}\def\\{\space}\leftmark}}
\fancypagestyle{gctheadings}{%
  \fancyhf{}%
  \fancyhead[LE]{\thepage}%
  \fancyhead[RE]{\nouppercase{\small\gctmark}}%
  \fancyhead[LO]{\nouppercase{\small\gctmark}}%
  \fancyhead[RO]{\thepage}%
  \renewcommand{\headrulewidth}{0.4pt}%
}
\pagestyle{gctheadings}
% Chapter/part opening pages use plain style (page number centered, no header).
\fancypagestyle{plain}{\fancyhf{}\fancyfoot[C]{\thepage}\renewcommand{\headrulewidth}{0pt}}
% Blank versos inserted by \cleardoublepage carry no running head or folio.
\makeatletter
\renewcommand{\cleardoublepage}{\clearpage\if@twoside\ifodd\c@page\else
  \hbox{}\thispagestyle{empty}\newpage\if@twocolumn\hbox{}\newpage\fi\fi\fi}
% Table of contents: room for three-digit folios so long entries never run
% into the page number.
\renewcommand{\@pnumwidth}{2.6em}
\renewcommand{\@tocrmarg}{3.6em}
% A literal underscore in text may end a line: long identifiers such as
% MANUSCRIPT_STATED or S.hypercharges_and_anomaly_cancellation otherwise
% overprint the next table column.
\DeclareRobustCommand{\_}{\ifmmode\nfss@text{\textunderscore}\else\textunderscore\penalty\exhyphenpenalty\fi}
\makeatother
% Semi-ragged bottom: a page may end up to ~4 lines short (the slack goes to
% the page foot, not between paragraphs, lists and boxes). Fully ragged
% (\raggedbottom) is not used: with it every early negative-penalty break
% (before a heading) costs nothing, so pages broke far too early and a
% longtable that followed printed its header above the heading.
\makeatletter
\def\@textbottom{\vskip \z@ \@plus 4\baselineskip}
\let\@texttop\relax
\makeatother
% Keep headings with their first lines: a heading never ends a page alone.
\usepackage{etoolbox}
% \gctneedspace does nothing directly after a heading (LaTeX's @nobreak is
% still set there): a needspace break between a heading and the subheading or
% box that follows it would strand the heading. Each level asks for room for
% itself, any subheading and a few lines of text.
% \gctneedbreak measures the room left on the page now and breaks at once if
% it is less than #1; otherwise it adds nothing (no breakpoint, no glue).
% needspace.sty's \needspace is not used: it leaves a stretchable -100
% breakpoint that the page builder may take much later, after a following
% longtable has installed its own output routine, and longtable then prints
% its header row at the top of the next page, above the heading or paragraph
% that precedes the table.
\makeatletter
\newcommand{\gctneedbreak}[1]{\par\if@nobreak\else\begingroup
  \setlength{\dimen@}{#1}\dimen@ii\pagegoal\advance\dimen@ii-\pagetotal
  \ifdim\dimen@>\dimen@ii\ifdim\pagetotal>\z@\break\fi\fi\endgroup\fi}
\let\gctneedspace\gctneedbreak
\makeatother
\pretocmd{\section}{\gctneedspace{12\baselineskip}}{}{}
\pretocmd{\subsection}{\gctneedspace{9\baselineskip}}{}{}
\pretocmd{\subsubsection}{\gctneedspace{6\baselineskip}}{}{}
\pretocmd{\paragraph}{\gctneedspace{4\baselineskip}}{}{}
% Long tier annotations of display equations are set on a wrapped line under
% the equation (see preprocess_display_equation_tags) instead of running past
% the right margin.
\newcommand{\gcteqnote}[1]{\parbox{0.9\linewidth}{\centering\footnotesize #1}}

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

% --- Landscape pages for the widest appendix tables (App FSM matrix) ---
\usepackage{pdflscape}

% --- Unicode character declarations ---
% The source contains specialist Unicode symbols. These explicit mappings keep
% rendering stable across the supported XeLaTeX font fallbacks. (U+ order.)
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
% XeLaTeX ignores \DeclareUnicodeCharacter (pdfTeX/inputenc only), so the
% mappings above never fire there. Route the glyphs the body fonts lack
% (Segoe UI / Georgia) to Segoe UI Symbol, which covers all of them; the
% build log reported these as "Missing character" and they printed blank.
% \TextOrMath keeps the normal math meaning inside equations.
\ifPDFTeX\else
  \IfFontExistsTF{Segoe UI Symbol}{\newfontfamily\gctsymbolfont{Segoe UI Symbol}}{\newfontfamily\gctsymbolfont{DejaVu Sans}}
  \newcommand{\gctsym}[1]{{\gctsymbolfont\symbol{#1}}}
  \newunicodechar{^^^^2713}{\TextOrMath{\gctsym{"2713}}{\mbox{\gctsym{"2713}}}}  % check mark
  \newunicodechar{^^^^2717}{\TextOrMath{\gctsym{"2717}}{\mbox{\gctsym{"2717}}}}  % ballot x
  \newunicodechar{^^^^26a0}{\TextOrMath{\gctsym{"26A0}}{\mbox{\gctsym{"26A0}}}}  % warning sign
  \newunicodechar{^^^^2705}{\TextOrMath{\gctsym{"2705}}{\mbox{\gctsym{"2705}}}}  % heavy check mark
  \newunicodechar{^^^^25b3}{\TextOrMath{\gctsym{"25B3}}{\triangle}}               % up triangle
  \newunicodechar{^^^^22a5}{\TextOrMath{\gctsym{"22A5}}{\perp}}                   % up tack
  \newunicodechar{^^^^2208}{\TextOrMath{\gctsym{"2208}}{\in}}                     % element of
  \newunicodechar{^^^^2225}{\TextOrMath{\gctsym{"2225}}{\parallel}}               % parallel to
  \newunicodechar{^^^^27e9}{\TextOrMath{\gctsym{"27E9}}{\rangle}}                 % right angle bracket
  \newunicodechar{^^^^2245}{\TextOrMath{\gctsym{"2245}}{\cong}}                   % approximately equal
  \newunicodechar{^^^^210f}{\TextOrMath{\gctsym{"210F}}{\hbar}}                   % h-bar
  \newunicodechar{^^^^^^01d6fa}{\TextOrMath{\gctsym{"1D6FA}}{\mitOmega}}          % math italic Omega
  \newunicodechar{^^^^^^01d70e}{\TextOrMath{\gctsym{"1D70E}}{\mitsigma}}          % math italic sigma
  \newunicodechar{^^^^fe0f}{}                                                     % VS16 (dropped)
\fi

% --- tcolorbox styles for GitHub-style alerts ---
\tcbuselibrary{skins,breakable}

\newtcolorbox{gctNote}[1][]{
  enhanced, breakable,
  colback=blue!5!white, colframe=blue!50!black,
  fonttitle=\bfseries, title=Note,
  #1
}
\newtcolorbox{gctWarning}[1][]{
  enhanced, breakable,
  colback=yellow!10!white, colframe=orange!80!black,
  fonttitle=\bfseries, title=Warning,
  #1
}
\newtcolorbox{gctCaution}[1][]{
  enhanced, breakable,
  colback=red!5!white, colframe=red!60!black,
  fonttitle=\bfseries, title=Caution,
  #1
}
\newtcolorbox{gctImportant}[1][]{
  enhanced, breakable,
  colback=purple!5!white, colframe=purple!60!black,
  fonttitle=\bfseries, title=Important,
  #1
}
\newtcolorbox{gctTip}[1][]{
  enhanced, breakable,
  colback=green!5!white, colframe=green!50!black,
  fonttitle=\bfseries, title=Tip,
  #1
}
\newtcolorbox{gctSpeculative}[1][]{
  enhanced, breakable,
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

SVG_CONVERSION_TIMEOUT_SECONDS = 120.0


def validate_pdf_file(path: Path) -> None:
    """Require a structurally parseable, non-empty PDF before publication use."""
    if not path.is_file():
        raise RuntimeError(f"converted PDF is missing: {path}")
    data = path.read_bytes()
    if len(data) < 32 or not data.startswith(b"%PDF-") or b"%%EOF" not in data[-2048:]:
        raise RuntimeError(f"converted file has an invalid PDF signature/trailer: {path}")
    if not HAS_PYPDF:
        raise RuntimeError(
            "pypdf is required to validate converted SVG assets; install the "
            "pinned build_scripts/requirements.txt environment"
        )
    try:
        reader = PdfReader(str(path), strict=True)
        if len(reader.pages) < 1:
            raise RuntimeError("PDF contains no pages")
    except Exception as exc:
        raise RuntimeError(f"converted PDF failed structural parse: {path}: {exc}") from exc


SVG_LAYOUT_WHITESPACE_RE = re.compile(r"[ \t\r\n\f]+")


def _svg_element_hidden(element: ET.Element, inherited: bool) -> bool:
    """Return whether an SVG element is explicitly absent from the render tree."""
    if inherited:
        return True
    declarations = {}
    for item in element.attrib.get("style", "").split(";"):
        if ":" in item:
            key, value = item.split(":", 1)
            declarations[key.strip().lower()] = value.strip().lower()
    display = element.attrib.get("display", declarations.get("display", "")).lower()
    visibility = element.attrib.get(
        "visibility", declarations.get("visibility", "")
    ).lower()
    opacity = element.attrib.get("opacity", declarations.get("opacity", "")).strip()
    return display == "none" or visibility in {"hidden", "collapse"} or opacity == "0"


def parsed_visible_svg_text(svg_path: Path) -> str:
    """Parse rendered SVG text, excluding metadata and explicitly hidden nodes."""
    root = ET.parse(svg_path).getroot()
    parts = []

    def append_text_tree(element: ET.Element, hidden: bool) -> None:
        hidden = _svg_element_hidden(element, hidden)
        if not hidden and element.text:
            parts.append(element.text)
        for child in element:
            append_text_tree(child, hidden)
            if not hidden and child.tail:
                parts.append(child.tail)

    def visit(element: ET.Element, hidden: bool = False) -> None:
        hidden = _svg_element_hidden(element, hidden)
        if element.tag.rsplit("}", 1)[-1] == "text":
            append_text_tree(element, hidden)
            return
        for child in element:
            visit(child, hidden)

    visit(root)
    return SVG_LAYOUT_WHITESPACE_RE.sub(" ", "".join(parts)).strip()


def non_ascii_character_counts(text: str) -> Counter:
    """Count visible non-ASCII, non-whitespace characters occurrence-exactly."""
    normalized = SVG_LAYOUT_WHITESPACE_RE.sub(" ", text)
    return Counter(char for char in normalized if ord(char) > 127 and not char.isspace())


def validate_svg_unicode_text(svg_path: Path, pdf_path: Path) -> None:
    """Require visible non-ASCII SVG text to survive PDF extraction count-exactly."""
    if not HAS_PYPDF:
        raise RuntimeError("pypdf is required for SVG Unicode validation")
    required = non_ascii_character_counts(parsed_visible_svg_text(svg_path))
    if not required:
        return
    reader = PdfReader(str(pdf_path), strict=True)
    extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
    observed = non_ascii_character_counts(extracted)
    if observed != required:
        missing = required - observed
        excess = observed - required
        format_counts = lambda counts: " ".join(
            f"{char!r}:{count}" for char, count in sorted(counts.items())
        ) or "none"
        raise RuntimeError(
            "Unicode character-count preservation failed; "
            f"missing={format_counts(missing)}; excess={format_counts(excess)}"
        )


def _run_inkscape_backend(svg_path: Path, temp_path: Path, timeout: float) -> None:
    inkscape = shutil.which("inkscape")
    if not inkscape:
        raise RuntimeError("Inkscape backend is unavailable")
    result = subprocess.run(
        [
            inkscape,
            str(svg_path),
            "--export-type=pdf",
            f"--export-filename={temp_path}",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "no diagnostic").strip()
        raise RuntimeError(f"Inkscape exited {result.returncode}: {detail}")


def _run_svglib_backend(svg_path: Path, temp_path: Path, timeout: float) -> None:
    if not HAS_SVGLIB:
        raise RuntimeError("svglib/reportlab backend is unavailable")
    result = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).resolve()),
            "--svg-worker",
            str(svg_path),
            str(temp_path),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "no diagnostic").strip()
        raise RuntimeError(f"svglib/reportlab exited {result.returncode}: {detail}")


def _run_chromium_backend(svg_path: Path, temp_path: Path, timeout: float) -> None:
    """Run the Unicode-safe Chromium converter in an isolated timed process."""
    if not HAS_PLAYWRIGHT:
        raise RuntimeError("Playwright/Chromium backend is unavailable")
    result = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).resolve()),
            "--chromium-svg-worker",
            str(svg_path),
            str(temp_path),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "no diagnostic").strip()
        raise RuntimeError(f"Playwright/Chromium exited {result.returncode}: {detail}")


def _atomic_convert(
    svg_path: Path,
    target_path: Path,
    backend,
    *,
    backend_name: str,
    timeout: float = SVG_CONVERSION_TIMEOUT_SECONDS,
    validator=validate_pdf_file,
    replacer=os.replace,
) -> Path:
    """Convert to a same-directory unique temp, validate, then atomically replace."""
    target_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = target_path.with_name(
        f".{target_path.name}.{uuid.uuid4().hex}.tmp"
    )
    try:
        backend(svg_path, temp_path, timeout)
        if not temp_path.is_file():
            raise RuntimeError(f"{backend_name} produced no output for {svg_path}")
        validator(temp_path)
        replacer(str(temp_path), str(target_path))
        return target_path
    except Exception as exc:
        raise RuntimeError(
            f"SVG conversion failed for {svg_path} via {backend_name}: {exc}"
        ) from exc
    finally:
        temp_path.unlink(missing_ok=True)


def convert_svg_to_pdf(
    svg_path_str: str,
    *,
    pdf_path: Path | None = None,
    timeout: float = SVG_CONVERSION_TIMEOUT_SECONDS,
) -> str:
    """Convert an SVG through a validated atomic write, never a stale fallback."""
    svg_path = Path(svg_path_str).resolve()
    if not svg_path.is_file():
        raise RuntimeError(f"SVG source is missing: {svg_path}")
    target_path = (pdf_path or svg_path.with_suffix(".pdf")).resolve()

    attempts = []
    backends = []
    if HAS_PLAYWRIGHT:
        backends.append(("Playwright/Chromium", _run_chromium_backend))
    if shutil.which("inkscape"):
        backends.append(("Inkscape", _run_inkscape_backend))
    if not backends:
        raise RuntimeError(
            f"No SVG-to-PDF backend is available for {svg_path}; "
            "a Unicode-safe backend is required and an existing sibling PDF "
            "is not a permitted fallback"
        )

    for backend_name, backend in backends:
        try:
            return str(
                _atomic_convert(
                    svg_path,
                    target_path,
                    backend,
                    backend_name=backend_name,
                    timeout=timeout,
                    validator=lambda candidate: (
                        validate_pdf_file(candidate),
                        validate_svg_unicode_text(svg_path, candidate),
                    ),
                )
            )
        except Exception as exc:
            attempts.append(str(exc))
    raise RuntimeError(
        f"No SVG-to-PDF backend produced a validated PDF for {svg_path}: "
        + " | ".join(attempts)
    )


def _svg_worker(svg_path: Path, output_path: Path) -> int:
    """Isolated svglib worker used only through the timed parent subprocess."""
    if not HAS_SVGLIB:
        print("svglib/reportlab backend is unavailable", file=sys.stderr)
        return 2
    font_map = svglib_fonts._font_map
    original_fontconfig = font_map.use_fontconfig
    # ``fc-match`` may be present but nonfunctional on Windows and can hang
    # indefinitely for every SVG text node. ReportLab's built-in Helvetica is
    # the deterministic fallback for unregistered figure fonts in this worker.
    font_map.use_fontconfig = lambda *_args, **_kwargs: (None, False)
    try:
        drawing = svg2rlg(str(svg_path))
        if drawing is None:
            raise RuntimeError("svglib returned no drawing")
        renderPDF.drawToFile(drawing, str(output_path), fmt="PDF", invariant=1)
        return 0
    except Exception as exc:
        print(f"svglib conversion failed for {svg_path}: {exc}", file=sys.stderr)
        return 3
    finally:
        font_map.use_fontconfig = original_fontconfig


def _chromium_worker(svg_path: Path, output_path: Path) -> int:
    """Render SVG with Chromium, then normalize it to deterministic PDF bytes."""
    if not HAS_PLAYWRIGHT:
        print("Playwright/Chromium backend is unavailable", file=sys.stderr)
        return 2
    if not HAS_PYPDF:
        print("pypdf is required for deterministic Chromium PDF output", file=sys.stderr)
        return 2

    raw_path = output_path.with_name(f".{output_path.name}.chromium-raw")
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            try:
                page = browser.new_page()
                page.goto(svg_path.resolve().as_uri(), wait_until="load")
                svg = page.locator("svg")
                if svg.count() != 1:
                    raise RuntimeError("source does not contain exactly one SVG root")
                size = svg.evaluate(
                    "e => ({w: e.width.baseVal.value, h: e.height.baseVal.value})"
                )
                if not size["w"] > 0 or not size["h"] > 0:
                    raise RuntimeError("SVG has non-positive rendered dimensions")
                page.pdf(
                    path=str(raw_path),
                    width=f'{size["w"]:.3f}px',
                    height=f'{size["h"]:.3f}px',
                    print_background=True,
                    margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
                    page_ranges="1",
                )
            finally:
                browser.close()

        reader = PdfReader(str(raw_path), strict=True)
        writer = PdfWriter(clone_from=reader)
        writer.metadata = {}
        writer.generate_file_identifiers()
        with output_path.open("wb") as stream:
            writer.write(stream)

        return 0
    except Exception as exc:
        output_path.unlink(missing_ok=True)
        print(f"Playwright/Chromium conversion failed for {svg_path}: {exc}", file=sys.stderr)
        return 3
    finally:
        raw_path.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# 2. Dependency check
# ---------------------------------------------------------------------------

def check_dependencies():
    pandoc   = shutil.which("pandoc")
    xelatex = shutil.which("xelatex")

    if not pandoc:
        print("[ERROR] 'pandoc' is not installed or not on PATH.")
        print("        To install on Windows: winget install pandoc")
        print("        On macOS:  brew install pandoc")
        print("        On Linux:  sudo apt install pandoc")

    if not xelatex:
        print("[WARNING] 'xelatex' is not installed or not on PATH.")
        print("          PDF generation will be skipped.")
        print("          To install on Windows: install MiKTeX with XeLaTeX.")
        print("          On macOS:  brew install --cask mactex")
        print("          On Linux:  sudo apt install texlive-full")

    if not pandoc:
        sys.exit(1)

    return str(pandoc), xelatex


# ---------------------------------------------------------------------------
# 3. Pre-processor: GitHub alert blocks → raw LaTeX tcolorbox
# ---------------------------------------------------------------------------

def _md_to_latex_inline(text: str) -> str:
    r"""
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
                # In a raw tcolorbox body TeX treats a bare tilde as an
                # unbreakable space.  In manuscript prose it denotes an
                # approximate value, so preserve that meaning explicitly.
                s = s.replace("~", r"\ensuremath{\sim}")
                # Escape `_` only when between non-whitespace (e.g. `Γ_rec`)
                # to avoid touching emphasis markers or §-refs already escaped.
                s = re.sub(r"(?<!\\)_(?=\w)", r"\\_", s)
                out.append(s)
    return "".join(out)


_ALERT_MARKER_RE = re.compile(
    r"^>\s*\[!(NOTE|WARNING|CAUTION|IMPORTANT|TIP|SPECULATIVE)\]\s?(.*)$",
    re.IGNORECASE,
)
# A body line that is itself a bare alert tag (GitHub syntax nested one level
# deeper, e.g. "> > [!CAUTION] Title") is handled by the recursive call.


def preprocess_alerts(text: str) -> str:
    r"""
    Convert GitHub-style callout blocks into pandoc fenced divs
    (``::: {.gctcallout env=gctNote}``) that ``LUA_CALLOUT_FILTER`` wraps in
    the matching tcolorbox environment.

    The body stays Markdown, so pandoc parses it like any other text: bold
    that spans lines, bullet and numbered lists, pipe tables, nested
    blockquotes and nested alerts all render instead of printing as literal
    ``**`` / ``- `` / ``|`` / ``>`` / ``[!CAUTION]`` text. (Before v1.3.0 the
    body was converted to raw LaTeX line by line by ``_md_to_latex_inline``,
    which understood only single-line emphasis and inline code.)
    """
    lines = text.split("\n")
    output = []
    i = 0

    while i < len(lines):
        line = lines[i]
        alert_match = _ALERT_MARKER_RE.match(line)

        if alert_match:
            alert_type = alert_match.group(1).upper()
            env = ALERT_ENV.get(alert_type, "gctNote")

            body_lines = []
            # Capture any content on the marker line itself (e.g.
            # "> [!SPECULATIVE] **Appendix TIB…**"); otherwise it is lost.
            same_line = alert_match.group(2).strip()
            if same_line:
                body_lines.append(same_line)
            i += 1
            while i < len(lines) and lines[i].startswith(">"):
                stripped = re.sub(r"^>\s?", "", lines[i])
                body_lines.append(stripped)
                i += 1

            body = preprocess_alerts("\n".join(body_lines)).strip("\n")
            # A nested div needs a longer outer fence than any fence inside.
            inner_fences = [len(m.group(0)) for m in re.finditer(r"(?m)^:{3,}", body)]
            fence = ":" * max(3, (max(inner_fences) + 1) if inner_fences else 3)

            output.append("")
            output.append(f"{fence} {{.gctcallout env={env}}}")
            output.append(body)
            output.append(fence)
            output.append("")

        else:
            output.append(line)
            i += 1

    return "\n".join(output)


# Pandoc Lua filter: wrap ``gctcallout`` divs in their tcolorbox environment.
# longtable cannot live inside a box, so a table inside a callout is rewritten
# from pandoc's longtable output into a plain tabular (same column spec).
LUA_CALLOUT_FILTER = r"""
local function longtable_to_tabular(s)
  -- drop the repeated header block of a captioned/first-head table
  s = s:gsub("\\endfirsthead.-\\endhead\n", "")
  s = s:gsub("\\endhead\n", "")
  s = s:gsub("\\bottomrule\\noalign{}\n\\endlastfoot\n", "")
  s = s:gsub("\\endlastfoot\n", "")
  s = s:gsub("\\endfoot\n", "")
  s = s:gsub("\\begin{longtable}%[[^%]]*%]", "\\begin{tabular}")
  s = s:gsub("\\end{longtable}", "\\bottomrule\\noalign{}\n\\end{tabular}")
  return s
end

local function table_block(tbl)
  local tex = pandoc.write(pandoc.Pandoc({tbl}), "latex")
  tex = longtable_to_tabular(tex)
  return pandoc.RawBlock("latex",
    "\\par\\smallskip\\noindent{\\small\\setlength{\\tabcolsep}{4pt}%\n" ..
    tex .. "}\\par\\smallskip")
end

function Div(el)
  if not el.classes:includes("gctcallout") then
    return nil
  end
  local env = el.attributes["env"] or "gctNote"
  local has_table = false
  local content = el.content:walk({ Table = function(t)
    has_table = true
    return table_block(t)
  end })
  -- a box never starts with only its title line at the foot of a page (a
  -- table inside cannot split, so such a box asks for more room)
  local room = has_table and "16" or "5"
  local out = { pandoc.RawBlock("latex",
    "\\gctneedspace{" .. room .. "\\baselineskip}\\begin{" .. env .. "}") }
  for _, b in ipairs(content) do
    table.insert(out, b)
  end
  table.insert(out, pandoc.RawBlock("latex", "\\end{" .. env .. "}"))
  return out
end
"""


# ---------------------------------------------------------------------------
# 4. Figure manager: check existence, generate placeholders
# ---------------------------------------------------------------------------

_REFRESHED_FIGURE_SVGS: set[Path] = set()


def convert_figure_svg_for_build(svg_path: Path) -> str:
    """Return the PDF refreshed earlier in this build, or refresh it now."""
    source = svg_path.resolve()
    target = source.with_suffix(".pdf")
    if source in _REFRESHED_FIGURE_SVGS:
        validate_pdf_file(target)
        return str(target)
    converted = convert_svg_to_pdf(str(source), pdf_path=target)
    _REFRESHED_FIGURE_SVGS.add(source)
    return converted


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
        pdf_path = convert_figure_svg_for_build(svg_candidate)
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
    r"""
    Several GCT source files have `\\` inside `$...$` math regions where the
    author meant `\`. (E.g. `$\\eta_0 = \\phi^{-2}$`.) pandoc passes these
    through as literal double backslashes which then break LaTeX. Walk
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
    r"""
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


_LEGACY_MATH_SCRIPT_RE = re.compile(
    r"(?P<script>[_^])(?P<command>\\(?:mathcal|mathbb))"
    r"(?:\{(?P<braced>[^{}]+)\}|\s*(?P<bare>[A-Za-z]))"
)


def preprocess_legacy_math_scripts(text: str) -> str:
    """Brace legacy ``_\\mathcal K``/``_\\mathbb{R}`` operands.

    pdfLaTeX historically tolerated these shorthands, but unicode-math under
    XeLaTeX parses the script as applying to ``\\mathcal``/``\\mathbb`` itself
    and fails with ``\\__um_group_begin:`` errors.  Normalizing the generated
    build input preserves the mathematical token while making its script
    boundary explicit.
    """

    def replace(match: re.Match[str]) -> str:
        argument = match.group("braced") or match.group("bare")
        return f'{match.group("script")}{{{match.group("command")}{{{argument}}}}}'

    return _LEGACY_MATH_SCRIPT_RE.sub(replace, text)


DISPLAY_TAG_WRAP_MIN_CHARS = 30


_TEXT_GROUP_RE = re.compile(r"\\(?:text|textrm)\{")


def _brace_end(s: str, open_idx: int) -> int:
    """Index just past the brace group that opens at s[open_idx] == '{'."""
    depth = 0
    k = open_idx
    while k < len(s):
        ch = s[k]
        if ch == "\\":
            k += 2
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return k + 1
        k += 1
    return -1


def _split_trailing_annotation(body: str):
    """Return (head, annotation_text, punct, trail) or None.

    The annotation is everything after the last top-level ``\\quad``/``\\qquad``
    when it is made only of ``\\text{...}`` groups (with math between them)
    and its text opens with ``[`` or ``(``. ``annotation_text`` is returned in
    text mode: the ``\\text`` wrappers are dropped and math between them is
    set in ``$...$``.
    """
    # punct may only be preceded by spaces on the same line; the trail keeps
    # newlines and blockquote prefixes ("\n> ") so the closing $$ stays put.
    m_tail = re.search(r"(?P<punct>[ \t]*[.,;]?)(?P<trail>[\s>]*)$", body)
    core = body[:m_tail.start()]
    punct, trail = m_tail.group("punct").strip(), m_tail.group("trail")
    if not core.endswith("}"):
        return None
    seps = [m for m in re.finditer(r"\\q?quad\b", core)]
    for sep in reversed(seps):
        # the separator must sit at brace depth 0
        prefix = core[:sep.start()]
        depth = 0
        k = 0
        while k < len(prefix):
            if prefix[k] == "\\":
                k += 2
                continue
            depth += {"{": 1, "}": -1}.get(prefix[k], 0)
            k += 1
        if depth != 0:
            continue
        rest = core[sep.end():]
        rest = re.sub(r"^(?:\s|\\q?quad\b|\\[;,!]|~)*", "", rest)
        if not _TEXT_GROUP_RE.match(rest):
            return None
        pieces, pos = [], 0
        while pos < len(rest):
            mt = _TEXT_GROUP_RE.match(rest, pos)
            if mt:
                end = _brace_end(rest, mt.end() - 1)
                if end < 0:
                    return None
                pieces.append(("text", rest[mt.end():end - 1]))
                pos = end
                continue
            nxt = _TEXT_GROUP_RE.search(rest, pos)
            seg = rest[pos:nxt.start() if nxt else len(rest)]
            if seg.strip():
                pieces.append(("math", seg.strip()))
            elif seg:
                pieces.append(("text", " "))
            pos = nxt.start() if nxt else len(rest)
        # An annotation is plain trailing text: never the tail of an
        # environment (\end{aligned}), an alignment cell, or a line break.
        if any(kind == "math" and re.search(r"\\(?:begin|end)\{|&|\\\\", v)
               for kind, v in pieces):
            return None
        if len(re.findall(r"\\begin\{", core[:sep.start()])) != len(
                re.findall(r"\\end\{", core[:sep.start()])):
            return None
        text = "".join(v if kind == "text" else f"${v}$" for kind, v in pieces)
        if text.strip()[:1] not in "[(":
            return None
        return core[:sep.start()], text.strip(), punct, trail
    return None


def _wrap_display_equation_tag(body: str) -> str:
    lead = re.match(r"\s*", body).group(0)
    inner = body[len(lead):]
    boxed = False
    tail_ws = ""
    if inner.startswith("\\boxed{"):
        end = _brace_end(inner, len("\\boxed"))
        after = inner[end:] if end > 0 else ""
        if end > 0 and re.fullmatch(r"[\s.,;>]*", after):
            split = _split_trailing_annotation(inner[len("\\boxed{"):end - 1])
            if split:
                boxed = True
                head, tag, punct, _t = split
                tail_ws = after
    if not boxed:
        split = _split_trailing_annotation(inner)
        if not split:
            return body
        head, tag, punct, tail_ws = split
    if len(tag) < DISPLAY_TAG_WRAP_MIN_CHARS:
        return body
    if boxed:
        head = f"\\boxed{{{head}}}"
        punct = punct + re.sub(r"[\s>]", "", tail_ws)
        tail_ws = re.sub(r"[.,;]", "", tail_ws)
    return (
        f"{lead}\\begin{{gathered}}{head}\\\\[1pt] "
        f"\\gcteqnote{{{tag}{punct}}}\\end{{gathered}}{tail_ws}"
    )


def preprocess_display_equation_tags(text: str) -> str:
    r"""Move a long trailing ``\quad\text{[Tier …]}`` annotation of a display
    equation onto a wrapped line under the equation.

    Set beside the formula, an annotation of 30+ characters runs past the
    right margin and is clipped at the trim (v1.3.0 page QA: V1 Ch17 N_coh,
    V3 Ch09 Thm 9.2 and m_1, V3 Ch10 §10.5.1). The text is unchanged; only its
    position moves, inside one ``gathered`` display so it stays with the
    equation.
    """
    out = []
    i, n = 0, len(text)
    in_fence = False
    while i < n:
        if (i == 0 or text[i - 1] == "\n") and text.startswith("```", i):
            j = text.find("\n", i)
            j = n if j == -1 else j + 1
            out.append(text[i:j])
            i = j
            in_fence = not in_fence
            continue
        if in_fence:
            j = text.find("\n", i)
            j = n if j == -1 else j + 1
            out.append(text[i:j])
            i = j
            continue
        ch = text[i]
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
            out.append("$$" + _wrap_display_equation_tag(text[i + 2:j]) + "$$")
            i = j + 2
            continue
        if ch == "\\" and i + 1 < n:
            out.append(text[i:i + 2])
            i += 2
            continue
        if ch == "$":
            j = text.find("$", i + 1)
            if j == -1 or "\n" in text[i + 1:j]:
                out.append(ch)
                i += 1
                continue
            out.append(text[i:j + 1])
            i = j + 1
            continue
        out.append(ch)
        i += 1
    return "".join(out)


_PIPE_SEPARATOR_CELL = re.compile(r"^:?-+:?$")


def _pipe_row_parts(line: str):
    """Split a line into (blockquote prefix, indent, rest) for pipe-table tests."""
    m = re.match(r"^((?:>[ \t]?)*)([ \t]{0,3})(.*)$", line)
    return m.group(1), m.group(2), m.group(3)


def _is_pipe_separator(rest: str) -> bool:
    if "-" not in rest or "|" not in rest:
        return False
    try:
        cells = _split_pipe_row(rest)
    except ValueError:
        return False
    return bool(cells) and all(_PIPE_SEPARATOR_CELL.match(c) for c in cells)


def separate_pipe_tables(content: str) -> str:
    """Give every pipe table its own block.

    A pipe table that follows a paragraph line with no blank line between
    (or is indented one to three spaces) is read by pandoc as paragraph text
    and prints raw ``| a | b |`` rows (v1.3.0 page QA: Firewall master
    statistical table, V3 Ch04 hypercharge table, PSC §PSC.9 callout table).
    Insert the blank line (keeping any ``>`` blockquote prefix), drop the
    indentation, and close the block after the last row.
    """
    lines = content.split("\n")
    out: list[str] = []
    i, n = 0, len(lines)
    in_fence = False
    while i < n:
        line = lines[i]
        if re.match(r"^\s*```", line):
            in_fence = not in_fence
            out.append(line)
            i += 1
            continue
        if in_fence or i + 1 >= n:
            out.append(line)
            i += 1
            continue
        prefix, _indent, rest = _pipe_row_parts(line)
        nprefix, _nindent, nrest = _pipe_row_parts(lines[i + 1])
        if (
            rest.startswith("|")
            and nprefix.replace(" ", "") == prefix.replace(" ", "")
            and _is_pipe_separator(nrest)
        ):
            if out:
                pprefix, _pi, prest = _pipe_row_parts(out[-1])
                if prest.strip() != "":
                    out.append(prefix.rstrip())
            if not prefix.strip():
                # Top-level table (not inside a callout): settle the page
                # before the longtable starts (see \gctneedbreak).
                out.append(r"\gctneedbreak{10\baselineskip}")
                out.append("")
            j = i
            while j < n:
                rprefix, _ri, rrest = _pipe_row_parts(lines[j])
                if rprefix.replace(" ", "") != prefix.replace(" ", "") or not rrest.startswith("|"):
                    break
                out.append(rprefix + rrest)
                j += 1
            if j < n:
                fprefix, _fi, frest = _pipe_row_parts(lines[j])
                if frest.strip() != "":
                    out.append(prefix.rstrip())
            i = j
            continue
        out.append(line)
        i += 1
    return "\n".join(out)


_VOLUME_PART_SUBTITLE_RE = re.compile(
    r"\\part\{(?P<label>VOLUME [^{}\n]+)\}\n\\setcounter\{chapter\}\{0\}\s*"
    r"(?:\\newpage\s*)?"
    r"\\begin\{center\}\\large\\textit\{(?P<sub>[^{}\n]+)\}\\end\{center\}\s*"
    r"(?:(?:-{3,}|\*{3,}|_{3,})[ \t]*\n)?"
)


def fold_volume_subtitles_into_part_pages(markdown: str) -> str:
    """Set each volume's subtitle on its part page.

    The subtitle used to land alone on the page after the part page, under a
    running head and above a stray rule (v1.3.0 page QA: PDF 71/325/449).
    """
    def repl(m: re.Match) -> str:
        label, sub = m.group("label"), m.group("sub")
        return (
            f"\\part[{label}]{{{label}\\\\[4ex]{{\\Large\\mdseries\\itshape {sub}}}}}\n"
            "\\setcounter{chapter}{0}\n\n"
        )
    return _VOLUME_PART_SUBTITLE_RE.sub(repl, markdown)


def preprocess_inline_figures(text: str) -> str:
    pattern = r">\s*\*\*Figure\s+(V\d+\.\d+\.\d+):\*\*\s*\*([^*]+)\*"

    def replace_figure(match):
        figure_id = match.group(1)
        figure_md = generate_inline_figure(figure_id)
        return match.group(0) + "\n" + figure_md

    return re.sub(pattern, replace_figure, text)


def preprocess_svg_image_links(text: str) -> str:
    """Convert local Markdown SVG image links to sibling PDFs for XeLaTeX."""
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

        pdf_path = Path(convert_figure_svg_for_build(svg_path))
        if pdf_path.suffix.lower() != ".pdf" or not pdf_path.exists():
            return match.group(0)

        rel_pdf = pdf_path.relative_to(PROJECT_ROOT).as_posix()
        return f"![{alt_text}]({rel_pdf})"

    return re.sub(pattern, replace_svg, text)


# ---------------------------------------------------------------------------
# 5. Assemble full manuscript markdown (walks the whole content/ tree)
# ---------------------------------------------------------------------------

_processed_files: set = set()

MANUAL_COVER_BEGIN = r"\typeout{GCT_MANUAL_COVER_BEGIN}"
BRAND_EMBLEM_SVG = PROJECT_ROOT / "_publish_prep" / "assets" / "gct_brand" / "gct_emblem.svg"
BRAND_EMBLEM_PDF = OUTPUT_DIR / ".texbuild-anchor" / "gct_emblem.pdf"


def publication_date_iso() -> str:
    """Return the metadata publication date in the colophon's stable ISO form."""
    return datetime.strptime(METADATA["date"], "%B %d, %Y").date().isoformat()


def source_date_epoch() -> str:
    """Stable UTC epoch used by TeX for reproducible PDF metadata/trailer IDs."""
    day = datetime.strptime(publication_date_iso(), "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return str(int(day.timestamp()))


def render_manual_cover(emblem_path: str) -> str:
    """Render the sole branded title mechanism; pandoc title metadata stays unset."""
    return (
        f"{MANUAL_COVER_BEGIN}\n"
        "\\thispagestyle{empty}\n"
        "\\begin{center}\n"
        "\\vspace*{18mm}\n"
        f"\\includegraphics[width=20mm]{{{emblem_path}}}\\\\[12mm]\n"
        f"{{\\gctdisplayfont\\fontsize{{32}}{{36}}\\selectfont\\bfseries\\color{{GCTInk}} {METADATA['title']}}}\\\\[4mm]\n"
        f"{{\\gctdisplayfont\\fontsize{{18}}{{22}}\\selectfont\\color{{GCTSoft}} {METADATA['subtitle']}}}\\\\[12mm]\n"
        f"{{\\sffamily\\large {METADATA['author']}}}\\\\[3mm]\n"
        f"{{\\sffamily Version {METADATA['version']} · {publication_date_iso()}}}\n"
        "\\vfill\n"
        "{\\color{GCTCopper}\\rule{42mm}{0.8pt}}\n"
        "\\end{center}\n"
        "\\newpage\n"
        "\\typeout{GCT_MANUAL_COVER_END}\n"
    )


def prepare_brand_emblem() -> str:
    """Convert the canonical emblem into the ignored build cache atomically."""
    converted = Path(
        convert_svg_to_pdf(str(BRAND_EMBLEM_SVG), pdf_path=BRAND_EMBLEM_PDF)
    )
    return converted.relative_to(OUTPUT_DIR).as_posix()


def prepare_all_figure_pdfs(figure_root: Path = FIGURES_DIR) -> list[Path]:
    """Fail closed while refreshing every canonical SVG/PDF figure pair.

    The publication catalog intentionally retains one explicit orphan, so
    converting only figures encountered while walking manuscript embeds would
    leave that governed pair stale.  The sorted inventory is the authoritative
    build traversal for all figure sources, embedded or not.
    """
    _REFRESHED_FIGURE_SVGS.clear()
    sources = sorted(figure_root.rglob("*.svg"))
    for source in sources:
        convert_svg_to_pdf(str(source), pdf_path=source.with_suffix(".pdf"))
        _REFRESHED_FIGURE_SVGS.add(source.resolve())
    return sources


def render_colophon() -> str:
    """Render the current-version citation and publication metadata page."""
    year = publication_date_iso()[:4]
    return (
        r"\thispagestyle{empty}" "\n"
        r"\vspace*{\fill}" "\n"
        r"\begin{center}" "\n"
        r"{\gctdisplayfont\large\bfseries " + METADATA["title"] + r"}\\[0.3em]" "\n"
        r"{\gctdisplayfont\itshape " + METADATA.get("subtitle", "") + r"}\\[1.5em]" "\n"
        r"\end{center}" "\n"
        r"{\raggedright" "\n"
        r"\noindent\textbf{Version.}\, " + METADATA["version"]
        + r"\quad\textbf{Publication date.}\, " + publication_date_iso()
        + r"\par\medskip" "\n"
        r"\noindent\textbf{Author.}\, " + METADATA["author"]
        + r"\par\medskip" "\n"
        r"\noindent\textbf{How to cite.}\, González Acosta, P. (" + year
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


def render_before_body(emblem_path: str) -> str:
    """Render the ordered cover and colophon block ahead of the TOC."""
    cover = render_manual_cover(emblem_path)
    colophon = render_colophon() if METADATA.get("doi_concept") else ""
    return cover + colophon


def _demote_in_file_top_headings(content: str) -> str:
    r"""
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
            if m_subtitle and not re.match(
                r"^PART\s+[IVX]+\b", m_subtitle.group(1), re.IGNORECASE
            ):
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
    r"""
    Promote bold-paragraph subsection markers of the form

        **1.1 The Problem of the Starting Point**
        **1.1.1 The Crisis in Foundational Physics**

    to real markdown headings (### / #### / etc.) so they appear in the
    table of contents and get proper LaTeX \section / \subsection
    numbering instead of being rendered as inline bold paragraphs.

    Required because most Volume 1 chapters use the bold-paragraph
    convention while Volumes 2/3 use explicit `### N.N.N` h3 headings.
    Without this promotion, Vol 1 chapters show no subsections in the
    TOC while Vol 2/3 do.

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


_BOLD_HEAD_LINE = re.compile(r"^\*\*[^*\n]{3,160}\*\*\s*$")


def keep_bold_heads_with_text(content: str) -> str:
    """A paragraph that is only a bold line (a run-in heading such as
    ``**TPF.3 Relativistic Kinematics ...**``) asks for room for itself and a
    few following lines, so it never ends a page alone (v1.3.0 page QA:
    TPF.3, QCT.1.2)."""
    lines = content.split("\n")
    out: list[str] = []
    in_fence = False

    def next_nonblank(k: int) -> str:
        for nxt in lines[k + 1:]:
            if nxt.strip():
                return nxt.lstrip()
        return ""

    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        if not in_fence and (i == 0 or lines[i - 1].strip() == ""):
            bold = _BOLD_HEAD_LINE.match(line)
            heading = re.match(r"^#{2,6}\s", line)
            # A heading or bold lead-in directly above a table: the table's
            # first rows cannot split, so ask for room for them too.
            nxt = next_nonblank(i)
            boxed_table = False
            if (bold or heading) and nxt.startswith("> [!"):
                # a callout right under the heading that holds a table
                k = next(j for j in range(i + 1, len(lines)) if lines[j].strip())
                while k < len(lines) and lines[k].startswith(">"):
                    if re.match(r"^>\s*\|", lines[k]):
                        boxed_table = True
                        break
                    k += 1
            if boxed_table:
                out.append(r"\gctneedbreak{30\baselineskip}")
                out.append("")
            elif (bold or heading) and nxt.startswith("|"):
                out.append(r"\gctneedbreak{20\baselineskip}")
                out.append("")
            elif bold:
                out.append(r"\gctneedspace{5\baselineskip}")
                out.append("")
        out.append(line)
    return "\n".join(out)


def normalize_pdf_chapter_title_qualifiers(content: str) -> str:
    """Make parenthetical chapter qualifiers extractable in the built PDF.

    XeLaTeX renders the original headings correctly, but pypdf can drop the
    entire chapter-title text when a TOC entry contains an outer parenthetical
    qualifier.  Replace only that outer pair with an em dash in the transient
    PDF assembly stream.  Nested notation such as ``U(1)`` remains intact, and
    canonical Markdown is never written.
    """
    out: list[str] = []
    chapter_heading = re.compile(r"^#{1,6}\s+.*?Chapter\s+\d{1,2}:")
    for line in content.split("\n"):
        if chapter_heading.match(line):
            start = line.find(" (")
            end = line.rfind(")")
            if start >= 0 and end > start:
                line = line[:start] + " — " + line[start + 2:end] + line[end + 1:]
            # The three nested group labels retain standard visible notation,
            # but use Latin Modern Math so their parentheses carry a correct
            # Unicode map for pypdf (Segoe UI's map is otherwise read as RTL
            # ornamental parentheses and the complete TOC line disappears).
            line = re.sub(
                r"(?<![A-Za-z])(U|SU)\(([123])\)",
                lambda m: rf"$\mathrm{{{m.group(1)}}}({m.group(2)})$",
                line,
            )
        out.append(line)
    return "\n".join(out)


def trim_generated_tex_trailing_whitespace(payload: bytes) -> bytes:
    """Trim line-end spaces/tabs while preserving Pandoc's line endings."""
    return re.sub(rb"[ \t]+(?=\r?$)", b"", payload, flags=re.MULTILINE)


def remove_redundant_terminal_backmatter(payload: bytes) -> bytes:
    """Remove Pandoc's terminal ``\\backmatter`` before ``\\end{document}``.

    The canonical content walker already emits the Back Matter part and all
    of its chapters.  Pandoc's book template then appends ``\\backmatter``
    after the final colophon; in the open-right layout that state transition
    creates a blank trailing page.  Require the exact template tail so a
    future Pandoc-template change fails closed instead of silently deleting
    unrelated TeX.
    """
    pattern = rb"(?m)^\\backmatter\r?\n(?=\\end\{document\}\s*$)"
    cleaned, count = re.subn(pattern, b"", payload)
    if count != 1:
        raise RuntimeError(
            f"expected one terminal Pandoc \\backmatter, found {count}"
        )
    return cleaned


def _rewrite_parameter_ledger_tables(content: str) -> str:
    """
    The Parameter Ledger has 7-column pipe tables where the "Notes" column
    contains long narrative text. Pandoc's default column auto-sizing gives
    every column roughly equal width, which forces the Notes column to wrap
    one-word-per-line and produces a visually broken layout.

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
    # v1.3.0 layout round: Value widened from 0.08 (formulas such as
    # M_P = m_e phi^107 (1-5 alpha)^-1 cannot break and overprinted First
    # Appearance) at the expense of Type and Notes.
    # The 7-column tables are set landscape: one Notes cell (eta_stiff,
    # ~2,100 characters) is taller than a portrait page, and a longtable row
    # cannot split, so its last lines were lost below the page edge.
    WIDTHS_7 = [0.08, 0.09, 0.15, 0.16, 0.09, 0.10, 0.30]
    LANDSCAPE_NCOL = {7}
    # 5-col: Symbol / Name / Value / Mechanical Origin / Needed for Tier 2
    # (the last two are narrative-heavy so get the bulk of the width)
    WIDTHS_5 = [0.08, 0.14, 0.13, 0.32, 0.30]
    # 5-col "# | Symbol | Description | Tier | Cross-Reference" tables
    # (0.3, 0.4): the Description column carries the prose.
    WIDTHS_5_DESCRIPTION = [0.05, 0.14, 0.43, 0.18, 0.16]
    WIDTHS_BY_NCOL = {5: WIDTHS_5, 7: WIDTHS_7}

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
            header_cells = _split_pipe_row(line)
            sep_line = lines[i + 1].strip()
            sep_cells = _split_pipe_row(sep_line)
            if (
                len(header_cells) in WIDTHS_BY_NCOL
                and len(sep_cells) == len(header_cells)
                and all(re.match(r"^:?-+:?$", c) for c in sep_cells)
            ):
                ncol = len(header_cells)
                widths = WIDTHS_BY_NCOL[ncol]
                if ncol == 5 and _norm_header_cell(header_cells[2]) == "Description":
                    widths = WIDTHS_5_DESCRIPTION
                landscape = ncol in LANDSCAPE_NCOL
                # Collect body rows until first non-pipe line.
                j = i + 2
                body_rows: list[list[str]] = []
                while j < n and lines[j].startswith("|"):
                    cells = _split_pipe_row(lines[j])
                    if len(cells) != ncol:
                        raise ValueError(f"Parameter Ledger table row {j + 1}: expected {ncol} cells, got {len(cells)}")
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
                    f">{{\\raggedright\\arraybackslash\\hspace{{0pt}}}}p{{\\dimexpr {w}\\linewidth-2\\tabcolsep\\relax}}"
                    for w in widths
                )
                lt = []
                if landscape:
                    lt.append(r"\begin{landscape}")
                # \begingroup / \endgroup keeps \footnotesize and the
                # hyphenation parameter changes scoped to the table.
                # Using raw \begingroup (not `{`) so pandoc passes it
                # through as raw LaTeX rather than escaping the brace.
                lt.append(r"\begingroup")
                lt.append(r"\footnotesize")
                lt.append(r"\setlength{\tabcolsep}{3pt}")
                lt.append(r"\setlength{\LTpre}{6pt}\setlength{\LTpost}{4pt}")
                lt.append(r"\hyphenpenalty=50\exhyphenpenalty=50")
                lt.append(r"\sloppy")
                lt.append(rf"\begin{{longtable}}{{{col_spec}}}")
                # Header
                lt.append(r"\toprule")
                lt.append(
                    " & ".join(rf"\textbf{{{_md_table_cell_to_latex(c)}}}" for c in header_cells)
                    + r" \\"
                )
                lt.append(r"\midrule")
                lt.append(r"\endhead")
                lt.append(r"\bottomrule")
                lt.append(r"\endlastfoot")
                # Body
                # No \addlinespace after the last row: it could push the
                # bottom rule (with a repeated header) onto a page of its own.
                for k, row in enumerate(body_rows):
                    lt.append(" & ".join(_md_table_cell_to_latex(c) for c in row) + r" \\")
                    if k < len(body_rows) - 1:
                        lt.append(r"\addlinespace[2pt]")
                lt.append(r"\end{longtable}")
                lt.append(r"\endgroup")
                if landscape:
                    lt.append(r"\end{landscape}")
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


def _escape_latex_table_text(text: str) -> str:
    """Escape original characters once, without revisiting generated TeX."""
    mapping = {
        "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%",
        "#": r"\#", "{": r"\{", "}": r"\}", "_": r"\_",
        "$": r"\$", "^": r"\^{}", "~": r"\textasciitilde{}",
        "|": r"\textbar{}",
        # Section-reference lists ("§14.5.2/§14.6.2/§14.6.3") and paths may
        # break after a slash inside a narrow cell.
        "/": r"/\allowbreak{}",
    }
    escaped = "".join(mapping.get(char, char) for char in text)
    # Identifiers such as S.hypercharges_and_anomaly_cancellation may also
    # break after a period that is followed by a letter.
    return re.sub(r"\.(?=[A-Za-z])", r".\\allowbreak{}", escaped)


def _table_inline_segments(text: str) -> list:
    """Single-backtick code/single-dollar math only; reject ambiguous nesting."""
    if "\x00" in text:
        raise ValueError("NUL is unsupported in table input")
    result, plain = [], []
    i = 0
    while i < len(text):
        char = text[i]
        if char == "\\" and i + 1 < len(text):
            plain.extend(text[i:i+2])
            i += 2
            continue
        if char not in "`$":
            plain.append(char)
            i += 1
            continue
        if text[i:i+2] == char*2:
            raise ValueError("Double-backtick/double-dollar table delimiters unsupported")
        if plain:
            result.append(("text", "".join(plain)))
            plain = []
        kind, j = ("code" if char == "`" else "math"), i + 1
        while j < len(text):
            current = text[j]
            if current == "\\" and j + 1 < len(text):
                if kind == "code" and text[j+1] == "`":
                    raise ValueError("Escaped backtick inside code unsupported")
                j += 2
                continue
            if kind == "math" and current == "`":
                raise ValueError("Nested code in table math unsupported")
            if current == char:
                if text[j:j+2] == char*2:
                    raise ValueError("Doubled closing table delimiter unsupported")
                break
            j += 1
        if j >= len(text):
            raise ValueError(f"Unterminated table {kind} span")
        result.append((kind, text[i:j+1]))
        i = j + 1
    if plain:
        result.append(("text", "".join(plain)))
    return result


def _md_table_cell_to_latex(s: str, strip_paths: bool = False) -> str:
    """Use explicit shared code/math ownership before escaping literal text."""
    s = s.strip()
    if strip_paths:
        s = _strip_engine_paths(s)
    saved, text_parts = [], []

    def _save(txt: str) -> str:
        saved.append(txt)
        return f"\x00S{len(saved) - 1}\x00"

    for kind, value in _table_inline_segments(s):
        if kind == "math":
            text_parts.append(_save(value))
        elif kind == "code":
            text_parts.append(_save(rf"\texttt{{{_escape_latex_table_text(value[1:-1])}}}"))
        else:
            text_parts.append(re.sub(r"\\([*_`|$%&#{}^~])", lambda m: _save(
                _escape_latex_table_text(m.group(1))
            ), value))
    s = _escape_latex_table_text("".join(text_parts))
    s = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", s)
    s = re.sub(r"(?<!\*)\*(?!\*)([^*\n]+?)\*(?!\*)", r"\\textit{\1}", s)
    for i, txt in enumerate(saved):
        s = s.replace(f"\x00S{i}\x00", txt)
    return s


def _norm_header_cell(c: str) -> str:
    """Normalize a header cell for config matching: strip markdown emphasis."""
    return re.sub(r"[*_`]", "", c).strip()


def _split_pipe_row(line: str) -> list:
    """Split literal separators under the converter's shared span ownership."""
    inner = line.strip()
    cells, current = [], []
    last_was_separator = False
    for kind, value in _table_inline_segments(inner):
        if kind != "text":
            current.append(value)
            last_was_separator = False
            continue
        backslashes = 0
        for char in value:
            if char == "|" and backslashes % 2 == 0:
                cells.append("".join(current).strip())
                current = []
                last_was_separator = True
            else:
                current.append(char)
                last_was_separator = False
            backslashes = backslashes + 1 if char == "\\" else 0
    cells.append("".join(current).strip())
    if inner.startswith("|"):
        cells.pop(0)
    if last_was_separator:
        cells.pop()
    return cells


# Tables whose cells contain multi-paragraph prose (a single cell can exceed a
# page) cannot be set as a longtable — longtable cannot break one row across
# pages, so a 400-word cell overflows the bottom margin. These are restructured
# into per-row prose blocks: the short fields become a labeled run-in and the
# long fields become ordinary paragraphs that page-break naturally.
#   title_idx → bold entry heading; badge_idx → appended after an em dash;
#   labels[i]=None → that column is consumed by the title/badge (not re-printed).
_BLOCK_TABLE_CONFIGS = {
    "03_Parameter_Ledger.md": [
        {  # closure-horizon narrative exceeds compact table layout
            "ncol": 3, "header0": "Sector", "title_idx": 0,
            "strip": False,
            "labels": [None, "Target state", "Required closures"],
        },
        {  # postulate ledger: every row's Status + Tier columns hold prose
            "ncol": 6, "header0": "#", "title_idx": 0, "badge_idx": 3,
            "strip": True,
            "labels": [None, "Postulate", "Type", None, "Status",
                       "Cross-reference"],
        },
    ],
    "App_FSM_Falsifiability_Matrix.md": [
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
    # App PSC precision-scorecard tables carry two prose-heavy columns per row
    # (a "what it means" justification plus a Tier accounting), so for some
    # rows two columns each hold ~100 words — impossible to set as a readable
    # multi-column longtable. Restructured to per-row blocks like FM.4.
    "App_PSC_Precision_Scorecard.md": [
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
    "App_FSM_Falsifiability_Matrix.md": [
        {  # FM.4: 15-column registry matrix; landscape is required for legibility.
            "ncol": 15, "header0": "ID", "strip": True,
            "font": r"\fontsize{6.8}{8}\selectfont", "landscape": True,
            "tabcolsep": "1.5pt",
            # v1.3.0 layout round: ID, Reference Class and Precision widened
            # (long S.* IDs, MANUSCRIPT_STATED and 3171372.84 overprinted the
            # next column); Disposition and Experiment give up the room.
            "widths": [0.067, 0.070, 0.080, 0.068, 0.060,
                       0.052, 0.080, 0.050, 0.050, 0.118,
                       0.068, 0.045, 0.040, 0.035, 0.050],
        },
    ],
    "App_PRG_Prediction_Registry.md": [
        # PRG.1 has 10 columns and one 2,500-character Falsification Threshold
        # cell (P.3). In portrait the last column ran off the page and the P.3
        # row ran past the bottom edge (a longtable row cannot split), so its
        # last words never printed. Landscape gives the threshold column room
        # for the whole cell on one page.
        {"ncol": 10, "header0": "Prediction ID", "strip": True,
         "font": r"\scriptsize", "landscape": True, "tabcolsep": "3pt",
         "widths": [0.045, 0.065, 0.10, 0.11, 0.29, 0.06, 0.09, 0.075, 0.045, 0.03]},
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
    landscape = spec.get("landscape", False)
    tabcolsep = spec.get("tabcolsep", "3pt")
    lt = []
    if landscape:
        lt.append(r"\begin{landscape}")
    lt.extend([r"\begingroup", font,
          r"\setlength{\LTpre}{6pt}\setlength{\LTpost}{4pt}",
          # Tight inter-column padding: with many columns the default 6pt
          # tabcolsep adds ~0.12-0.13\linewidth of overhead, which pushes the
          # declared table width past \linewidth and clips the last column.
          rf"\setlength{{\tabcolsep}}{{{tabcolsep}}}",
          r"\hyphenpenalty=50\exhyphenpenalty=50", r"\sloppy",
          rf"\begin{{longtable}}{{{col_spec}}}", r"\toprule",
          " & ".join(rf"\textbf{{{_md_table_cell_to_latex(c, strip)}}}" for c in header_cells) + r" \\",
          r"\midrule", r"\endhead", r"\bottomrule", r"\endlastfoot"])
    for k, row in enumerate(body_rows):
        lt.append(" & ".join(_md_table_cell_to_latex(c, strip) for c in row) + r" \\")
        if k < len(body_rows) - 1:
            lt.append(r"\addlinespace[2pt]")
    lt.append(r"\end{longtable}")
    lt.append(r"\endgroup")
    if landscape:
        lt.append(r"\end{landscape}")
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

    # v1.3.0 layout round: widths proportional to the longest cell starved
    # short columns that hold unbreakable content (a formula, a ppm value, a
    # one-word claim), and their cells overprinted the neighbouring column
    # (page QA: Firewall statistical table, IVH.3, TAT.1, PSC.2.1). Each column
    # now first gets room for its longest unbreakable token (a math span is
    # one token), and only the remaining line capacity is shared out by how
    # much text the column carries.
    def rendered_len(token: str) -> float:
        if token.startswith("$") and token.endswith("$") and len(token) > 1:
            body = re.sub(r"\\(?:mathrm|rm|text|mathbf|mathcal|mathbb|left|right|,|;|!|quad)\b", "", token[1:-1])
            body = re.sub(r"\\[A-Za-z]+", "x", body)       # \alpha -> one glyph
            body = re.sub(r"[_^]\{([^{}]*)\}", lambda m: "s" * max(1, int(len(m.group(1)) * 0.7)), body)
            body = re.sub(r"[_^]", "", body)
            return len(re.sub(r"[{}\s]", "", body)) * 1.1
        if token.startswith("`"):
            return min(len(token) - 2, 12)                  # code breaks (hyphenat)
        return len(re.sub(r"[*\\]", "", token))

    def tokens(cell: str) -> list:
        out = []
        for kind, value in _table_inline_segments(cell.strip()):
            if kind in ("math", "code"):
                out.append(value)
            else:
                out.extend(w for w in re.split(r"[\s/]+|(?<=[-–—])", value) if w)
        return out

    def cell_len(cell: str) -> float:
        return sum(rendered_len(t) + 1 for t in tokens(cell))

    capacity = 124.0  # characters per \scriptsize line across 0.88\linewidth
    tok_max, mean_len, max_len = [], [], []
    for c in range(ncol):
        cells = [r[c] for r in rows if c < len(r)]
        toks = [rendered_len(t) for cell in cells for t in tokens(cell)] or [1]
        lens = [cell_len(cell) for cell in cells] or [1]
        tok_max.append(min(max(toks), 24) + 2)
        mean_len.append(sum(lens) / len(lens))
        max_len.append(max(lens) + 2)
    chars = [max(t, 4) for t in tok_max]
    spare = capacity - sum(chars)
    if spare > 0:
        want = [max(0.0, min(max_len[c], 3 * mean_len[c] + 8) - chars[c]) for c in range(ncol)]
        for _ in range(4):
            total_want = sum(want)
            if spare <= 0.5 or total_want <= 0:
                break
            give = [spare * w / total_want for w in want]
            for c in range(ncol):
                g = min(give[c], want[c])
                chars[c] += g
                want[c] -= g
            spare = capacity - sum(chars)
        if spare > 0.5:  # every column satisfied: share the rest evenly
            chars = [ch + spare / ncol for ch in chars]
    total = sum(chars) or 1
    widths = [round(ch / total * 0.88, 4) for ch in chars]
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
                malformed_rows = []
                while j < n and lines[j].startswith("|"):
                    cells = _split_pipe_row(lines[j])
                    if len(cells) == ncol:
                        body_rows.append(cells)
                    else:
                        malformed_rows.append((j + 1, len(cells)))
                    j += 1
                auto_sp = None
                if not block_sp and not wide_sp:
                    auto_sp = _auto_wide_spec(header_cells, body_rows)
                if block_sp or wide_sp or auto_sp:
                    if malformed_rows:
                        raise ValueError(f"{file_name}: expected {ncol} cells; malformed table rows {malformed_rows}")
                    spec = wide_sp or auto_sp
                    heading_tex = ""
                    if not block_sp and spec.get("landscape"):
                        # A heading directly above a landscape table would
                        # stand alone on a portrait page: set it as the first
                        # line of the landscape page instead.
                        k = len(out) - 1
                        while k >= 0 and (not out[k].strip() or out[k].startswith("\\gctneedbreak")):
                            k -= 1
                        hm = re.match(r"^(#{2,4})\s+(.+?)\s*$", out[k]) if k >= 0 else None
                        if hm:
                            cmd = {2: "section", 3: "subsection", 4: "subsubsection"}[len(hm.group(1))]
                            title = hm.group(2).strip().strip("*").strip()
                            title_tex = title.replace("&", r"\&").replace("%", r"\%")
                            heading_tex = f"\\{cmd}{{{title_tex}}}"
                            del out[k:]
                    out.append("")
                    if block_sp:
                        out.append(r"\begingroup\setlength{\parindent}{0pt}")
                        for row in body_rows:
                            out.append(_render_block_entry(block_sp, header_cells, row))
                        out.append(r"\endgroup")
                    else:
                        rendered = _render_wide_longtable(spec, header_cells, body_rows)
                        if heading_tex:
                            rendered = rendered.replace(
                                "\\begin{landscape}", "\\begin{landscape}\n" + heading_tex, 1)
                        out.append(rendered)
                    out.append("")
                    i = j
                    continue
        out.append(line)
        i += 1
    return "\n".join(out)


def _is_unnumbered_chapter_file(path: Path) -> bool:
    r"""
    Files that should produce \chapter* (unnumbered) so the \chapter
    counter doesn't increment past them. Real chapters (Ch01_*) keep
    their normal numbered \chapter behavior.

    Triggers on:
      - Global Frontmatter files (content/00_Global_Frontmatter/*.md)
      - Volume frontmatter files (content/0N_Volume_*/00_Frontmatter/*.md)
      - Volume backmatter files (content/0N_Volume_*/99_Backmatter/*.md)
      - Global Backmatter files (content/99_Global_Backmatter/*.md)
      - Global Appendices files (content/98_Global_Appendices/*.md) —
        29 appendices (A-Z + R2 + TP + ZN) exceed LaTeX \appendix MTI-Z
        letter mode, so we keep them as \chapter* with the title
        carrying its own "Appendix BEB:" prefix.
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
    r"""
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
    r"""
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
    r"""
    Walk content/ in canonical order and concatenate every .md file.

    Heading-hierarchy convention (with pandoc --top-level-division=part):
      h1 → \part     ← top-level dirs only (Volumes; Front/Back/Appendices use raw \part*)
      h2 → \chapter  ← actual chapters (Ch01, Ch02, ...) after normalization
      h3 → \section  ← section headings inside chapters
    """
    parts = []

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
            # PDF-only accessibility normalization: pypdf drops TOC chapter
            # entries whose title ends in an outer parenthetical qualifier.
            # The canonical Markdown remains byte-identical.
            content = normalize_pdf_chapter_title_qualifiers(content)
            # Promote bold-paragraph subsection markers (`**1.1 X**`) to
            # real h3/h4 headings so they appear in the TOC. Most Vol 1
            # chapters use this convention; Vol 2/3 already use explicit
            # `### N.N.N` h3 syntax. Normalising both keeps the TOC
            # consistent across volumes.
            content = _promote_bold_subsection_paragraphs(content)
            content = keep_bold_heads_with_text(content)
            # Every pipe table becomes its own block (blank line before and
            # after, no indentation) before the table rewriters look for it.
            content = separate_pipe_tables(content)
            # If this is the Parameter Ledger, rewrite its wide 7-column
            # tables to raw LaTeX longtable with explicit column widths so
            # the Notes column gets enough room.
            if entry.name == "03_Parameter_Ledger.md":
                content = _rewrite_parameter_ledger_tables(content)
            # Restructure prose-heavy / wide appendix + chapter tables that
            # overflow the portrait text width (FM.4 matrix, GCT-vs-IIT,
            # App PSC scorecards, App PRG registry). No-op for unconfigured files.
            content = _rewrite_custom_tables(content, entry.name)
            # If post-demotion content has NO h1 anywhere, prepend a fallback
            # chapter header derived from the file stem. We attach it to
            # the content (not the parts list) so the subsequent
            # unnumbered-chapter conversion can see it.
            # A thematic break at the very top of a file would be set alone on
            # the page before the file's opening chapter page (v1.3.0 page QA:
            # PDF 1015, a page holding only the running head and a rule).
            content = re.sub(r"\A\s*(?:(?:-{3,}|\*{3,}|_{3,})[ \t]*\n\s*)+", "", content)
            has_h1 = re.search(r"^#\s+\S", content, re.MULTILINE) is not None
            if not has_h1:
                stem = entry.stem
                # Strip multiple numeric prefixes: "01_", "00_", "Ch04_00_", etc.
                stem = re.sub(r"^(\d+_)+", "", stem)
                stem = re.sub(r"^Ch\d+_(\d+_)?", "", stem)
                stem = re.sub(r"^App_[A-Z]+_", r"Appendix \g<0>", stem) if stem.startswith("App_") else stem
                stem = stem.replace("_", " ")
                # Keep a leading PART divider page ahead of the fallback
                # chapter heading; otherwise the chapter page comes first and
                # stands empty before the divider (v1.3.0 page QA: Part VI).
                divider = re.match(
                    r"\A\s*\\clearpage\n\\thispagestyle\{empty\}\n.*?\\vspace\*\{\\fill\}\n\\clearpage\n",
                    content, re.S,
                )
                if divider:
                    content = (content[:divider.end()] + f"\n# {stem}\n\n"
                               + content[divider.end():])
                else:
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

    return fold_volume_subtitles_into_part_pages("\n".join(parts))


# ---------------------------------------------------------------------------
# 6. Clean output directory (idempotent build)
# ---------------------------------------------------------------------------

def reset_output_dir():
    """
    Remove every auxiliary file generated by previous XeLaTeX runs so the
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

# Lines starting with "! " in a XeLaTeX .log are real errors (LaTeX
# Error / Package Error / Undefined control sequence / etc.). We collect them.
_ERROR_LINE_RE = re.compile(r"^!\s")


def collect_log_errors(log_path: Path, limit: int = 50):
    """Return a list of error lines (and surrounding context) from a XeLaTeX log."""
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

# Pandoc reader. Beyond pandoc's defaults:
#   -yaml_metadata_block: source files use --- as section separators.
#   +tex_math_single_backslash: \(...\) math survives the adjacency rewrite.
#   +lists_without_preceding_blankline / -blank_before_blockquote /
#   -blank_before_header: a list, blockquote or heading written directly under
#     a paragraph line starts its own block instead of printing as literal
#     "* " / "- " / "1." / ">" / "####" text inside the paragraph (v1.3.0 page
#     QA root cause 1: ~100 pages). Source paragraphs are one line each, so a
#     line that opens with one of these markers is always meant as the block.
PANDOC_READER = (
    "markdown+raw_tex+tex_math_single_backslash"
    "+lists_without_preceding_blankline"
    "-blank_before_blockquote-blank_before_header"
    "-yaml_metadata_block"
)
# Three passes: the second resolves the table of contents and references; the
# third writes PDF page labels that match the final front-matter length (with
# two passes the viewer's page numbers ran 14 ahead of the printed folios).
XELATEX_PASSES = 3


def main():
    print("=" * 60)
    print("GCT LaTeX Compiler — Full Manuscript")
    print("=" * 60)

    # Fail before dependency checks or output mutation if the index is stale.
    assert_index_fresh()

    # 8a. Dependency check
    pandoc, xelatex = check_dependencies()
    print(f"  pandoc   : {pandoc}")
    print(f"  xelatex  : {xelatex or 'NOT FOUND (PDF skipped)'}")
    print("-" * 60)

    # 8b. Reset output dir (idempotent build)
    print("Resetting output directory...")
    reset_output_dir()
    print(f"  Output dir: {OUTPUT_DIR}")

    print("\nRefreshing all canonical figure PDF pairs...")
    figure_sources = prepare_all_figure_pdfs()
    print(f"  [OK] {len(figure_sources)} figure SVG/PDF pairs refreshed.")

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
    print("Running legacy math-script normalizer...")
    markdown = preprocess_legacy_math_scripts(markdown)
    print("Running inline figure pre-processor...")
    markdown = preprocess_inline_figures(markdown)
    print("Running SVG image-link pre-processor...")
    markdown = preprocess_svg_image_links(markdown)
    print("Running alert pre-processor...")
    markdown = preprocess_alerts(markdown)
    print("Running display-equation tag pre-processor...")
    markdown = preprocess_display_equation_tags(markdown)

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

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".lua", delete=False, encoding="utf-8"
    ) as tmp_lua:
        tmp_lua.write(LUA_CALLOUT_FILTER)
        lua_path = tmp_lua.name

    # Manual cover followed by the self-contained citation/colophon verso.
    # Supplying both through one include-before-body block keeps their order
    # ahead of Pandoc's table of contents.
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".tex", delete=False, encoding="utf-8"
    ) as tmp_before_body:
        tmp_before_body.write(render_before_body(prepare_brand_emblem()))
        before_body_path = tmp_before_body.name

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
            "--from", PANDOC_READER,
            "--to", "latex",
            "--output", str(OUTPUT_TEX),
            "--lua-filter", lua_path,
            "--include-in-header", preamble_path,
            "--variable", "documentclass=book",
            # `openright` (default) forces every chapter to start on a
            # right-hand (recto) page, inserting a blank verso when the
            # previous chapter ends on a recto. This is the convention
            # for printed books.
            "--variable", "fontsize=11pt",
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
        pandoc_cmd += ["--include-before-body", before_body_path]
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
        tex_payload = OUTPUT_TEX.read_bytes()
        tex_payload = remove_redundant_terminal_backmatter(tex_payload)
        trimmed_payload = trim_generated_tex_trailing_whitespace(tex_payload)
        OUTPUT_TEX.write_bytes(trimmed_payload)
        print("  [OK] removed redundant terminal Pandoc \\backmatter.")
        if trimmed_payload != tex_payload:
            print("  [OK] removed generated TeX trailing whitespace.")
        print(f"  [OK] .tex written: {OUTPUT_TEX} ({OUTPUT_TEX.stat().st_size / 1024:.1f} KB)")

        # 8g. Run XeLaTeX (twice for TOC/refs and system-font embedding)
        if xelatex:
            log_path = OUTPUT_TEX.with_suffix(".log")
            reproducible_env = os.environ.copy()
            reproducible_env["SOURCE_DATE_EPOCH"] = source_date_epoch()
            reproducible_env["FORCE_SOURCE_DATE"] = "1"
            for pass_num in range(1, XELATEX_PASSES + 1):
                print(f"\nRunning xelatex (pass {pass_num}/{XELATEX_PASSES})...")
                pdf_result = subprocess.run(
                    [
                        xelatex,
                        "-interaction=nonstopmode",
                        "-output-directory", str(OUTPUT_DIR),
                        str(OUTPUT_TEX),
                    ],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    cwd=str(OUTPUT_DIR),
                    env=reproducible_env,
                )

                # C-6 fix: detect errors from the .log, not the exit code.
                # XeLaTeX's exit code is unreliable in nonstopmode; the truth
                # lives in the log file's "! " error lines.
                log_errors = collect_log_errors(log_path)

                if log_errors:
                    print(f"  [FAIL] xelatex pass {pass_num}: {len(log_errors)} LaTeX error(s) detected.")
                    print("  ---- First errors ----")
                    for err in log_errors[:10]:
                        print("  " + err.replace("\n", "\n  "))
                    print("  ----------------------")
                    if pass_num == XELATEX_PASSES:
                        print(f"[ERROR] Build failed. See {log_path} for details.")
                        sys.exit(2)
                    else:
                        # Pass 1 may have pseudo-errors that pass 2 resolves
                        # (e.g. forward refs). Continue but warn.
                        print(f"  [WARN] Continuing to pass 2 to see if these resolve.")
                else:
                    print(f"  [OK] xelatex pass {pass_num} clean.")

            if OUTPUT_PDF.exists():
                page_count = "?"
                try:
                    # Pull page count from the log: "Output written ... (N pages, ..."
                    # XeLaTeX wraps log lines, so flatten line breaks first.
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
                print(f"[ERROR] PDF not found after xelatex run. See {log_path}.")
                sys.exit(3)
        else:
            print("\n[SKIP] xelatex not available — .tex file only.")

    finally:
        Path(preamble_path).unlink(missing_ok=True)
        Path(md_path).unlink(missing_ok=True)
        Path(lua_path).unlink(missing_ok=True)
        Path(before_body_path).unlink(missing_ok=True)

    print("\n" + "=" * 60)
    print("BUILD COMPLETE")
    print(f"  TEX : {OUTPUT_TEX}")
    if xelatex and OUTPUT_PDF.exists():
        print(f"  PDF : {OUTPUT_PDF}")
    print("=" * 60)


if __name__ == "__main__":
    if any(a in ("-h", "--help") for a in sys.argv[1:]):
        print(__doc__)
        raise SystemExit(0)
    if len(sys.argv) == 4 and sys.argv[1] == "--svg-worker":
        raise SystemExit(_svg_worker(Path(sys.argv[2]), Path(sys.argv[3])))
    if len(sys.argv) == 4 and sys.argv[1] == "--chromium-svg-worker":
        raise SystemExit(_chromium_worker(Path(sys.argv[2]), Path(sys.argv[3])))
    main()
