#!/usr/bin/env python3
"""Validate and render bounded public metadata from committed authorities.

Only README.md, CITATION.cff, and .zenodo.json are rendered.  Scientific
closure counts come from expected_outcomes.json; the dark-energy diagnostic
values come from protocol_de_multichannel_results.json.  Version and date stay
in build_scripts/metadata.json and are checked, not advanced by this tool.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
METADATA_PATH = ROOT / "build_scripts" / "metadata.json"
EXPECTED_PATH = ROOT / "GCT_Physics_Engine" / "config" / "expected_outcomes.json"
DE_PATH = ROOT / "GCT_Physics_Engine" / "data" / "protocol_de_multichannel_results.json"
README_PATH = ROOT / "README.md"
CITATION_PATH = ROOT / "CITATION.cff"
ZENODO_PATH = ROOT / ".zenodo.json"
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "audit.yml"


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load valid JSON from {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def derive_publication_summary(
    expected: dict, de_result: dict, handles: object, handle_notes: object, handle_scope: object
) -> dict:
    protocols = expected.get("protocols")
    if not isinstance(protocols, list) or not protocols:
        raise ValueError("expected_outcomes.protocols must be a non-empty list")
    closures = Counter(row.get("scientific_closure") for row in protocols)
    allowed = {"confirmed", "open", "conditional", "tension"}
    if set(closures) != allowed:
        raise ValueError(f"unexpected scientific_closure vocabulary: {sorted(closures)}")
    if (
        not isinstance(handles, list)
        or not handles
        or not all(isinstance(item, str) and item.strip() == item and item for item in handles)
        or len(handles) != len(set(handles))
    ):
        raise ValueError("metadata handle authority must be a non-empty list of unique, trimmed strings")
    if (
        not isinstance(handle_notes, dict)
        or set(handle_notes) != set(handles)
        or not all(isinstance(note, str) and note.strip() == note and note for note in handle_notes.values())
    ):
        raise ValueError("metadata handle notes must provide one non-empty note for every authoritative handle")
    if not isinstance(handle_scope, str) or not handle_scope.strip():
        raise ValueError("metadata handle subset scope must be a non-empty string")

    try:
        bio = de_result["multichannel_eos_shape_proxy"]["biogenic_terrestrial"]
        best = de_result["best_fit"]["joint_marginal_distance_diagnostic"]
        spread = de_result["omega_lambda_diagnostic_spread"]
    except (KeyError, TypeError) as exc:
        raise ValueError(f"dark-energy result schema is incomplete: {exc}") from exc

    return {
        "expected_protocol_count": len(protocols),
        "scientific_closure": {key: closures[key] for key in ("confirmed", "open", "conditional", "tension")},
        "calibrated_discrete_coefficient_handles": list(handles),
        "calibrated_discrete_coefficient_handle_notes": dict(handle_notes),
        "calibrated_discrete_coefficient_handle_count": len(handles),
        "calibrated_discrete_coefficient_subset_scope": handle_scope,
        "de_multichannel": {
            "biogenic_terrestrial_w0": round(float(bio["w0"]), 4),
            "biogenic_terrestrial_wa": round(float(bio["wa"]), 4),
            "best_fit_diagonal_diagnostic_score": round(float(best), 3),
            "omega_lambda_diagnostic_spread": round(float(spread), 4),
            "physical_behavior": "continuous phantom phase with no literal phantom-divide crossing",
        },
    }


def validate_metadata(metadata: dict, derived: dict) -> None:
    for key in ("version", "date", "publication_summary"):
        if key not in metadata:
            raise ValueError(f"metadata.json lacks required key {key!r}")
    if not isinstance(metadata["version"], str) or not re.fullmatch(r"\d+\.\d+\.\d+", metadata["version"]):
        raise ValueError("metadata version must use semantic X.Y.Z form")
    try:
        datetime.strptime(metadata["date"], "%B %d, %Y")
    except (TypeError, ValueError) as exc:
        raise ValueError("metadata date must use 'Month D, YYYY' form") from exc
    persisted_authority = dict(derived)
    persisted_authority.pop("calibrated_discrete_coefficient_handle_count")
    if metadata["publication_summary"] != persisted_authority:
        raise ValueError("metadata publication_summary does not match committed producer authorities")


def handle_list(summary: dict) -> str:
    handles = summary["calibrated_discrete_coefficient_handles"]
    if len(handles) == 1:
        return handles[0]
    return ", ".join(handles[:-1]) + f", and {handles[-1]}"


def handle_statement(summary: dict) -> str:
    return (
        f"{summary['calibrated_discrete_coefficient_handle_count']} calibrated Tier-3 discrete coefficient "
        f"handles ({handle_list(summary)}) form a {summary['calibrated_discrete_coefficient_subset_scope']}"
    )


def markdown_handle(value: str) -> str:
    return {"10phi^2": "$10\\phi^2$", "1/5": "$1/5$"}.get(value, value)


def readme_handle_inventory(summary: dict) -> str:
    handles = summary["calibrated_discrete_coefficient_handles"]
    notes = summary["calibrated_discrete_coefficient_handle_notes"]
    bullets = "\n".join(f"- {markdown_handle(value)} ({notes[value]})" for value in handles)
    return (
        "**Named Tier-3 discrete coefficient handles in the precision/gauge comparison subset:**\n"
        f"{bullets}\n\n"
        f"Subset total: {handle_statement(summary)}."
    )


def replace_one(text: str, pattern: str, replacement: str, label: str, flags: int = 0) -> str:
    rendered, count = re.subn(pattern, lambda _match: replacement, text, count=1, flags=flags)
    if count != 1:
        raise ValueError(f"{label}: expected exactly one bounded match, found {count}")
    return rendered


def render_readme(text: str, summary: dict) -> str:
    c = summary["scientific_closure"]
    protocol_count = summary["expected_protocol_count"]
    suite_badge = (
        f"[![Suite integrity: {protocol_count}/{protocol_count} expected results]"
        f"(https://img.shields.io/badge/Suite%20integrity-{protocol_count}%2F{protocol_count}%20expected%20results-brightgreen.svg)]()"
    )
    text = replace_one(text, r"^\[!\[Suite integrity:.*$", suite_badge, "README suite badge", re.MULTILINE)
    badge = (
        f"[![Scientific closure: {c['confirmed']} confirmed · {c['open']} open · "
        f"{c['conditional']} conditional · {c['tension']} tension]"
        f"(https://img.shields.io/badge/Scientific%20closure-{c['confirmed']}%20confirmed%20%C2%B7%20"
        f"{c['open']}%20open%20%C2%B7%20{c['conditional']}%20conditional%20%C2%B7%20"
        f"{c['tension']}%20tension-blue.svg)]()"
    )
    text = replace_one(text, r"^\[!\[Scientific closure:.*$", badge, "README closure badge", re.MULTILINE)
    text = replace_one(
        text,
        r"^\* 📄 \*\*\[Read the compiled monograph — PDF(?:, \d+ pp)?\]\(\./output/Geometric_Consciousness_Theory\.pdf\)\*\*(?: — or \[download from the latest release\]\([^\n]+\))?$",
        "* 📄 **[Read the compiled monograph — PDF](./output/Geometric_Consciousness_Theory.pdf)**",
        "README PDF link",
        re.MULTILINE,
    )
    text = replace_one(
        text,
        r"The (?:build is deterministic; a clean clone reproduces\n"
        r"the shipped PDF|script rebuilds the PDF from tracked sources;\n"
        r"pagination and byte serialization depend on the installed TeX toolchain)\.",
        "The script rebuilds the PDF from tracked sources;\n"
        "pagination and byte serialization depend on the installed TeX toolchain.",
        "README PDF reproducibility statement",
    )

    de = summary["de_multichannel"]
    text = replace_one(
        text,
        r"single-channel biogenic-DE output \$\(-?\d+\.\d+,\+?\d+\.\d+\)\$",
        f"single-channel biogenic-DE output $({de['biogenic_terrestrial_w0']:.4f},+{de['biogenic_terrestrial_wa']:.4f})$",
        "README biogenic-DE pair",
    )
    text = replace_one(
        text,
        r"best-fit diagonal diagnostic score \$\\approx\d+\.\d+\$, flat to within \$\d+\.\d+\$ score units",
        f"best-fit diagonal diagnostic score $\\approx{de['best_fit_diagonal_diagnostic_score']:.3f}$, "
        f"flat to within ${de['omega_lambda_diagnostic_spread']:.4f}$ score units",
        "README diagnostic score",
    )
    text = replace_one(
        text,
        r"the biogenic contribution (?:remains in a continuous phantom phase and )?asymptotically approaches \$w=-1\$ from below, with no physical (?:quintessence-to-phantom|phantom-divide) crossing",
        "the biogenic contribution remains in a continuous phantom phase and asymptotically approaches "
        "$w=-1$ from below, with no physical phantom-divide crossing",
        "README continuous-phantom semantics",
    )
    text = replace_one(
        text,
        r"^\*\*Named Tier-3 discrete coefficient handles in the precision/gauge comparison subset:\*\*\n"
        r"(?:- .*\n)+\nSubset total:.*$",
        readme_handle_inventory(summary),
        "README handle inventory",
        re.MULTILINE,
    )
    # The bullet inventory above is the sole README handle enumeration.  Remove
    # the older narrative copies if they are reintroduced by a stale branch.
    text = re.sub(
        r" A named precision/gauge comparison subset contains six calibrated Tier-3 discrete coefficient handles,"
        r" counted separately from the six continuous anchors: .*? remain separately catalogued\.",
        "",
        text,
    )
    text = re.sub(
        r" The named precision/gauge comparison subset's six calibrated Tier-3 discrete coefficient handles .*?"
        r" additional sector-specific handles are separately catalogued\.",
        "",
        text,
    )
    readme_intro = text.split("## 📖 The Manuscript", 1)[0]
    if readme_intro.count("**Named Tier-3 discrete coefficient handles in the precision/gauge comparison subset:**") != 1:
        raise ValueError("README must retain exactly one manager-owned handle inventory")
    if readme_intro.count("Subset total:") != 1:
        raise ValueError("README must retain exactly one manager-owned handle subtotal")
    return text


def render_citation(text: str, summary: dict, metadata: dict) -> str:
    c = summary["scientific_closure"]
    text = replace_one(
        text,
        r"electron mass as the sole dimensional input; .*?(?:and|while) the O\.38 N=144 cage posit (?:are|is) disclosed separately\.",
        f"electron mass as the sole dimensional input; {handle_statement(summary)}, while the O.38 N=144 "
        "cage posit is disclosed separately.",
        "CITATION handle authority",
        re.DOTALL,
    )
    protocol_count = summary["expected_protocol_count"]
    text = replace_one(
        text,
        r"\d+/\d+ expected results for suite integrity",
        f"{protocol_count}/{protocol_count} expected results for suite integrity",
        "CITATION protocol count",
    )
    text = replace_one(
        text,
        r"scientific-closure breakdown of \d+ confirmed, \d+ open, \d+ conditional,\n  and \d+ tension",
        f"scientific-closure breakdown of {c['confirmed']} confirmed, {c['open']} open, "
        f"{c['conditional']} conditional,\n  and {c['tension']} tension",
        "CITATION closure counts",
    )
    text = replace_one(
        text,
        r"^  - (?:phantom crossing|continuous phantom phase)$",
        "  - continuous phantom phase",
        "CITATION dark-energy keyword",
        re.MULTILINE,
    )
    text = replace_one(
        text,
        r"^version: .+$",
        f"version: {metadata['version']}",
        "CITATION version",
        re.MULTILINE,
    )
    date_iso = datetime.strptime(metadata["date"], "%B %d, %Y").date().isoformat()
    text = replace_one(
        text,
        r"^date-released: \d{4}-\d{2}-\d{2}$",
        f"date-released: {date_iso}",
        "CITATION date",
        re.MULTILINE,
    )
    return text


def render_zenodo(document: dict, summary: dict, metadata: dict) -> dict:
    description = document.get("description")
    keywords = document.get("keywords")
    if not isinstance(description, str) or not isinstance(keywords, list):
        raise ValueError(".zenodo.json needs string description and list keywords")
    description = replace_one(
        description,
        r"(?:\d+|four|five|six) calibrated Tier-3 .*?(?:and|while) the O\.38 N=144 cage posit (?:are|is) disclosed separately\.",
        f"{handle_statement(summary)}, while the O.38 N=144 cage posit is disclosed separately.",
        "Zenodo handle authority",
    )
    protocol_count = summary["expected_protocol_count"]
    description = replace_one(
        description,
        r"\d+/\d+ expected results for suite integrity",
        f"{protocol_count}/{protocol_count} expected results for suite integrity",
        "Zenodo protocol count",
    )
    c = summary["scientific_closure"]
    description = replace_one(
        description,
        r"scientific-closure breakdown of \d+ confirmed, \d+ open, \d+ conditional, and \d+ tension",
        f"scientific-closure breakdown of {c['confirmed']} confirmed, {c['open']} open, "
        f"{c['conditional']} conditional, and {c['tension']} tension",
        "Zenodo closure counts",
    )
    normalized = ["continuous phantom phase" if item == "phantom crossing" else item for item in keywords]
    if "continuous phantom phase" not in normalized:
        raise ValueError("Zenodo keywords lack the dark-energy semantic keyword")
    if len(normalized) != len(set(normalized)):
        raise ValueError("Zenodo keywords must be unique")
    result = dict(document)
    result["version"] = metadata["version"]
    result["description"] = description
    result["keywords"] = normalized
    return result


def expected_outputs() -> dict[Path, str]:
    metadata = load_json(METADATA_PATH)
    publication = metadata.get("publication_summary")
    if not isinstance(publication, dict):
        raise ValueError("metadata.json publication_summary must be an object")
    derived = derive_publication_summary(
        load_json(EXPECTED_PATH),
        load_json(DE_PATH),
        publication.get("calibrated_discrete_coefficient_handles"),
        publication.get("calibrated_discrete_coefficient_handle_notes"),
        publication.get("calibrated_discrete_coefficient_subset_scope"),
    )
    validate_metadata(metadata, derived)
    readme = render_readme(README_PATH.read_text(encoding="utf-8"), derived)
    citation = render_citation(CITATION_PATH.read_text(encoding="utf-8"), derived, metadata)
    zenodo = render_zenodo(load_json(ZENODO_PATH), derived, metadata)
    return {
        README_PATH: readme,
        CITATION_PATH: citation,
        ZENODO_PATH: json.dumps(zenodo, indent=2, ensure_ascii=False) + "\n",
    }


def check_workflow() -> None:
    workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
    command = "python3 -X utf8 build_scripts/manage_publication_metadata.py --check"
    if workflow.count(command) != 1:
        raise ValueError("audit workflow must invoke publication metadata check exactly once")


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="render the three bounded public files")
    mode.add_argument("--check", action="store_true", help="fail if any bounded public field drifts")
    args = parser.parse_args()

    outputs = expected_outputs()
    check_workflow()
    if args.check:
        drift = [str(path.relative_to(ROOT)) for path, expected in outputs.items() if path.read_text(encoding="utf-8") != expected]
        if drift:
            print("Publication metadata drift: " + ", ".join(drift), file=sys.stderr)
            return 1
        print("PASS: publication metadata matches committed producer authorities.")
        return 0

    for path, expected in outputs.items():
        path.write_text(expected, encoding="utf-8", newline="\n")
    print("Updated: " + ", ".join(str(path.relative_to(ROOT)) for path in outputs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
