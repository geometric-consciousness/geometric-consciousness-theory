"""Regression fixtures for the Markdown-table export path of compile_latex.py.

The pure table functions and the two literal table configurations are
extracted from compile_latex.py by AST (the module itself is never imported,
so no build dependency, filesystem mutation or external tool runs). The
fixtures check, for the Parameter Ledger and every configured source file:
row census and parser/oracle cell agreement, verbatim survival of every math
span, literal code spans, explicit failure on malformed rewritten rows,
unchanged pass-through of unconfigured compact tables, and positive declared
column widths.

Run:
    py -3.13 build_scripts/check_table_export_fixtures.py
"""
import ast
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
CANDIDATE = ROOT / "build_scripts" / "compile_latex.py"
CONTENT = ROOT / "content"
LEDGER = CONTENT / "00_Global_Frontmatter" / "03_Parameter_Ledger.md"
FUNCTIONS = {
    "_table_inline_segments", "_escape_latex_table_text", "_strip_engine_paths", "_md_table_cell_to_latex",
    "_norm_header_cell", "_split_pipe_row", "_rewrite_parameter_ledger_tables",
    "_render_block_entry", "_render_wide_longtable", "_plain_len",
    "_auto_wide_spec", "_rewrite_custom_tables",
}
CONFIGS = {"_BLOCK_TABLE_CONFIGS", "_WIDE_TABLE_CONFIGS"}
MATH = re.compile(r"(?<!\\)\$(?:\\.|[^$\\\n])+(?<!\\)\$")
CODE = re.compile(r"`[^`]*`")
checks = []


def check(condition, label):
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reference_cells(line):
    # Independent token masking oracle, distinct from candidate's state scanner.
    saved = []
    def protect(match):
        saved.append(match.group())
        return f"\x01{len(saved)-1}\x01"
    masked = CODE.sub(protect, line.strip())
    masked = MATH.sub(protect, masked)
    masked = re.sub(r"\\\|", protect, masked)
    # Last regex handles odd escape runs in real source; parity fixtures below
    # have explicit expected arrays and do not depend on this oracle.
    parts = masked.split("|")
    if masked.startswith("|"):
        parts.pop(0)
    if masked.endswith("|"):
        parts.pop()
    restored = []
    for part in parts:
        for i, value in enumerate(saved):
            part = part.replace(f"\x01{i}\x01", value)
        restored.append(part.strip())
    return restored


def tables(text):
    lines, result = text.splitlines(), []
    i = 0
    while i + 1 < len(lines):
        if not lines[i].startswith("|"):
            i += 1
            continue
        header, separator = reference_cells(lines[i]), reference_cells(lines[i+1])
        if len(header) != len(separator) or not all(re.fullmatch(r":?-+:?", c) for c in separator):
            i += 1
            continue
        body, j = [], i + 2
        while j < len(lines) and lines[j].startswith("|"):
            cells = reference_cells(lines[j])
            check(len(cells) == len(header), f"source ledger row {j+1} has complete cells")
            body.append((j+1, lines[j], cells))
            j += 1
        result.append((header, body))
        i = j
    return result


def fixture(header, row):
    return "| " + " | ".join(header) + " |\n| " + " | ".join(["---"]*len(header)) + " |\n| " + " | ".join(row) + " |"


def main():
    check(sys.version_info[:2] >= (3,10), "Python 3.10+")
    parsed = ast.parse(CANDIDATE.read_text(encoding="utf-8"))
    nodes = [n for n in parsed.body if isinstance(n, ast.FunctionDef) and n.name in FUNCTIONS]
    check({n.name for n in nodes} == FUNCTIONS, "all exact pure functions found")
    # Static fail-closed review before compiling the limited AST: prohibit I/O,
    # dynamic execution, imports, process spawning, and unsafe reflective access.
    forbidden = {"open", "exec", "eval", "compile", "__import__", "getattr", "setattr", "globals", "locals", "subprocess", "os", "sys", "Path"}
    for node in nodes:
        for item in ast.walk(node):
            if isinstance(item, (ast.Import, ast.ImportFrom)):
                raise AssertionError("candidate function contains import")
            if isinstance(item, ast.Name) and item.id in forbidden:
                raise AssertionError(f"candidate unsafe name {item.id}")
            if isinstance(item, ast.Attribute) and item.attr.startswith("__"):
                raise AssertionError("candidate unsafe attribute")
    namespace = {"re": re}
    found_configs = set()
    for node in parsed.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and node.targets[0].id in CONFIGS:
            namespace[node.targets[0].id] = ast.literal_eval(node.value)
            found_configs.add(node.targets[0].id)
    check(found_configs == CONFIGS, "both complete literal table configs")
    exec(compile(ast.Module(body=nodes, type_ignores=[]), "reviewed-table-functions-only", "exec"), namespace)
    split = namespace["_split_pipe_row"]
    convert = namespace["_md_table_cell_to_latex"]
    ledger_rewrite = namespace["_rewrite_parameter_ledger_tables"]
    custom_rewrite = namespace["_rewrite_custom_tables"]
    ledger = LEDGER.read_text(encoding="utf-8")
    collected = tables(ledger)
    transformed = custom_rewrite(ledger_rewrite(ledger), LEDGER.name)
    source_rows, source_math = 0, 0
    for header, rows in collected:
        for line_number, original, cells in rows:
            source_rows += 1
            check(split(original) == cells, f"ledger row {line_number} parser cells exact")
            source_codes_removed = CODE.sub("", original)
            for math in MATH.findall(source_codes_removed):
                source_math += 1
                check(math in transformed, f"ledger row {line_number} math exact: {math}")
            if original in transformed:
                check(True, f"ledger row {line_number} compact passthrough")
            else:
                strip = len(header) == 6 and header[0] == "#"
                for index, cell in enumerate(cells):
                    check(convert(cell, strip) in transformed, f"ledger row {line_number} cell {index} rendered")
    check(source_rows > 50, "entire current ledger row census substantial")
    check(r"$\|n\| = 107$" in transformed, "M_P norm retained")
    check(r"$|n| = 1^2 + 5^2 + 9^2 = 107$" in transformed, "closure horizon raw norm retained")
    check("\\textit{Target state:}" in transformed, "closure horizon rendered as breakable prose block")
    escaping = [
        (r"`\_{x}&%#$^~`", r"\texttt{\textbackslash{}\_\{x\}\&\%\#\$\^{}\textasciitilde{}}"),
        ("`$x$`", r"\texttt{\$x\$}"),
        (r"$\phi^{-18}$", r"$\phi^{-18}$"),
        (r"$\|n\|=107$", r"$\|n\|=107$"),
        (r"\$5 & 50% #1 _ ^ ~ {x}", r"\$5 \& 50\% \#1 \_ \^{} \textasciitilde{} \{x\}"),
        ("**bold** *italic*", r"\textbf{bold} \textit{italic}"),
        (r"\*literal\* and \_", r"*literal* and \_"),
        (r"A\|B", r"A\textbar{}B"),
        (r"`$x$` and $y_1$", r"\texttt{\$x\$} and $y_1$"),
    ]
    for text, expected in escaping:
        check(convert(text) == expected, f"literal/code/math ownership {text!r}")
    splitting = [
        (r"| $\|n\|$ | b |", [r"$\|n\|$", "b"]),
        (r"| $|n|$ | b |", [r"$|n|$", "b"]),
        (r"| `a|b` | c |", ["`a|b`", "c"]),
        (r"| a\|b | c |", [r"a\|b", "c"]),
        ("| a\\\\| b |", ["a\\\\", "b"]),
        ("| a\\\\\\|b | c |", ["a\\\\\\|b", "c"]),
        ("| | b |", ["", "b"]),
        ("a | b", ["a", "b"]),
    ]
    for line, expected in splitting:
        check(split(line) == expected, f"explicit pipe fixture {line!r}")
    configured = 0
    for config_name in CONFIGS:
        for filename, specs in namespace[config_name].items():
            for spec in specs:
                configured += 1
                n = spec["ncol"]
                header = [spec["header0"]] + [f"Column{i}" for i in range(1,n)]
                row = [f"unique{i} **bold** `$x$` $\\phi_{{{i}}}$" for i in range(n)]
                text = fixture(header, row)
                rendered = custom_rewrite(text, filename)
                check(rendered != text, f"configured rewrite selected {filename}/{n}")
                for cell in row:
                    check(convert(cell, spec.get("strip",False)) in rendered, f"configured cell retained {filename}/{n}/{cell}")
                broken = text + "\n| too | few |"
                try:
                    custom_rewrite(broken, filename)
                except ValueError:
                    check(True, f"configured malformed row fails {filename}/{n}")
                else:
                    raise AssertionError(f"silent configured malformed row {filename}/{n}")
    segment = namespace["_table_inline_segments"]
    rejected = ["\x00", "``double``", "$$double$$", "$x `nested`$", "`unterminated", "$unterminated", "`x\\`y`", "$x$$", "`$x`y$"]
    for bad in rejected:
        for operation in (segment, convert, split):
            try:
                operation(bad)
            except ValueError:
                check(True, f"supported syntax rejects {operation.__name__}/{bad!r}")
            else:
                raise AssertionError(f"ambiguous syntax accepted {operation.__name__}/{bad!r}")
    check(convert("`$$x$$`") == r"\texttt{\$\$x\$\$}", "double dollars inside code are literal")
    check(convert(r"\`literal\`") == "`literal`", "escaped backticks outside code are literal")
    check("\x00" not in convert("`$x$` and $y$"), "no nested restoration NUL leakage")
    configured_names = sorted(set(namespace["_BLOCK_TABLE_CONFIGS"]) | set(namespace["_WIDE_TABLE_CONFIGS"]))
    census_files = []
    for name in configured_names:
        matches = sorted(CONTENT.rglob(name))
        check(len(matches) == 1, f"configured source located {name}")
        census_files.append(matches[0])
    census_rows = 0
    for path in census_files:
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
            if not line.startswith("|"):
                continue
            parsed_cells = split(line)
            census_rows += 1
            for index, cell in enumerate(parsed_cells):
                tokens = segment(cell)
                rendered = convert(cell)
                check("\x00" not in rendered, f"actual cell no NUL {path.name}/{line_number}/{index}")
                for kind, value in tokens:
                    if kind == "math":
                        check(value in rendered, f"actual cell math verbatim {path.name}/{line_number}/{index}")
                    elif kind == "code":
                        check(namespace["_escape_latex_table_text"](value[1:-1]) in rendered, f"actual code literal {path.name}/{line_number}/{index}")
        actual_text = path.read_text(encoding="utf-8")
        actual_rendered = custom_rewrite(actual_text, path.name)
        specs = namespace["_BLOCK_TABLE_CONFIGS"].get(path.name, []) + namespace["_WIDE_TABLE_CONFIGS"].get(path.name, [])
        for header, actual_rows in tables(actual_text):
            selected = next((spec for spec in specs if spec["ncol"] == len(header) and spec["header0"] == namespace["_norm_header_cell"](header[0])), None)
            if selected is None:
                continue
            for line_number, original, cells in actual_rows:
                for index, cell in enumerate(cells):
                    check(convert(cell, selected.get("strip",False)) in actual_rendered, f"actual configured cell survives {path.name}/{line_number}/{index}")
    compact = fixture(["One","Two","Three"], ["a","b","c"]) + "\n| malformed |"
    check(custom_rewrite(compact, "unconfigured.md") == compact, "unconfigured compact malformed passthrough unchanged")
    for n in (5,7):
        header = [f"C{i}" for i in range(n)]
        text = fixture(header,[f"cell{i}" for i in range(n)])
        rendered = ledger_rewrite(text)
        check("\\setlength{\\tabcolsep}{3pt}" in rendered, f"local padding {n}")
        widths = [float(x) for x in re.findall(r"p\{\\dimexpr ([0-9.]+)\\linewidth-2\\tabcolsep\\relax\}",rendered)]
        check(len(widths) == n and sum(widths) < 1, f"ledger width fraction bounded {n}")
        check(all(w*174*72.27/25.4 - 6 > 0 for w in widths), f"ledger cell widths positive {n}")
        try:
            ledger_rewrite(text + "\n| too | few |")
        except ValueError:
            check(True, f"ledger malformed fails {n}")
        else:
            raise AssertionError(f"silent ledger malformed {n}")
    print(json.dumps({"ok":True,"checks":len(checks),"ledger_rows":source_rows,"ledger_math_segments":source_math,"configured_specs":configured,"actual_configured_pipe_rows":census_rows,"compiler_sha256":sha(CANDIDATE),"ledger_sha256":sha(LEDGER),"configured_sources":[str(p.relative_to(ROOT)) for p in census_files],"scope":"AST pure table regression; no native build/render","labels":checks},ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except BaseException as error:
        print(json.dumps({"ok":False,"error_type":type(error).__name__,"error":str(error),"passed_checks":len(checks)},ensure_ascii=False))
        raise SystemExit(1)
