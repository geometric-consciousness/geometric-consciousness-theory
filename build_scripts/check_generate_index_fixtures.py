"""Focused, non-production fixtures for the Master Index generator."""
from __future__ import annotations

import tempfile
from collections import defaultdict
from pathlib import Path

import generate_index as indexer


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    sources = {path.resolve() for path in indexer.canonical_sources()}
    require(indexer.INDEX_OUTPUT.resolve() not in sources, "generated index fed itself")
    require(indexer.FIGURES_CATALOG.resolve() not in sources, "noncanonical figure catalog was indexed")
    require(all(indexer.make_ref(path) in {
        "GFM", "GBM", "App",
    } or indexer.make_ref(path).startswith(("V1 ", "V2 ", "V3 ", "App ", "GFM ", "GBM "))
                for path in sources), "raw path escaped the reference mapper")
    require(not any("_" in indexer.make_ref(path) for path in sources),
            "a file-name underscore leaked into a reader-facing reference")
    require(indexer.make_ref(indexer.CONTENT_DIR / "99_Global_Backmatter" / "02_Master_Bibliography.md")
            == "GBM Master Bibliography", "back-matter title was not rendered readably")

    try:
        indexer.make_ref(indexer.CONTENT_DIR / "Figures" / "trap.md")
    except ValueError:
        pass
    else:
        raise AssertionError("unknown content namespace did not fail closed")

    rejected = {
        "APPENDICES TO VOLUME 3", "GLOBAL FRONT MATTER", "PASS",
        "ACTIVE TENSION", "Not closed", "Open Problem O.14",
        "Open Research Debt QLQCD-1L", "Appendix USS §USS.8",
        "Tier 0", "Tier 1", "Tier 3 conditional step", "Summary", "Scope/status",
        "Index Volume 2", "POSTDICTION-CONSISTENT conditional on O.5",
        "What closed", "What closes", "Where it lives", "Where the analysis lives",
    }
    require(not any(indexer.is_indexable_term(term) for term in rejected),
            "publication scaffolding survived the noise policy")
    retained = {
        "Lattice Surface Tension", "Open-System Dynamics", "Tiered Cohomology", "CPT",
    }
    require(all(indexer.is_indexable_term(term) for term in retained),
            "anchored noise policy rejected a legitimate concept")

    require(indexer.clean_term("Topological Limit of Complexity — Tier 2 structural bound")
            == "Topological Limit of Complexity", "trailing Tier adornment was not normalized")
    require(indexer.clean_term("Tier-3 Lattice Fracture ansatz") == "Lattice Fracture ansatz",
            "leading Tier adornment was not normalized")

    legitimate_terms: dict[str, set[str]] = defaultdict(set)
    indexer.collect_terms(
        "**Topological Limit of Complexity — Tier 2 structural bound** (engine)\n"
        "**Tier-3 Lattice Fracture ansatz**: candidate\n"
        "The **CPT** (Charge, Parity, Time) requirement",
        "App ORQ",
        legitimate_terms,
    )
    require(set(legitimate_terms) == {
        "Topological Limit of Complexity", "Lattice Fracture ansatz", "CPT",
    }, "named legitimate concepts were not extracted after normalization")

    tier0_terms: dict[str, set[str]] = defaultdict(set)
    indexer.collect_terms("**Tier 0**: experience is occurring.", "Global Front Matter", tier0_terms)
    require(not tier0_terms, "the raw Tier 0 label became an index entry")

    terms: dict[str, set[str]] = defaultdict(set)
    indexer.collect_terms("**Acoustic Metric**: first\n**Acoustic Metric**: second", "V2 Ch08", terms)
    require(terms == {"Acoustic Metric": {"V2 Ch08"}}, "reference deduplication failed")
    duplicate_variants = {
        "Lemma PUP.3.1": "Lemma PUP.3.1.",
        "Lemma PUP.3.2": "Lemma PUP.3.2.",
        "Lemma PUP.3.5": "Lemma PUP.3.5.",
        "Postulate P1": "Postulate P1.",
        "Theorem 3.10": "Theorem 3.10.",
        "Theorem 4.0": "Theorem 4.0.",
        "Wheeler-DeWitt Equation": "Wheeler-DeWitt equation",
    }
    raw_variants = {}
    for offset, (canonical, variant) in enumerate(duplicate_variants.items(), start=1):
        raw_variants[canonical] = {f"V1 Ch{offset:02d}"}
        raw_variants[variant] = {f"V2 Ch{offset:02d}"}
    merged = indexer.canonicalize_index_map(raw_variants)
    require(set(merged) == set(duplicate_variants), "semantic duplicate display selection failed")
    require(all(len(refs) == 2 for refs in merged.values()), "semantic duplicate ref union failed")

    rendered_a = indexer.render_index({"alpha": {"V1 Ch02", "V1 Ch01"}, "Alpha": {"V1 Ch03"}})
    rendered_b = indexer.render_index({"Alpha": {"V1 Ch03"}, "alpha": {"V1 Ch01", "V1 Ch02"}})
    require(rendered_a == rendered_b, "total ordering depends on insertion order")
    require("generate_index.py" not in rendered_a and "auto-generated" not in rendered_a,
            "generator provenance sentence leaked into the reader-facing index")
    require(rendered_a.count("**Alpha:**") == 1 and "V1 Ch01, V1 Ch02, V1 Ch03" in rendered_a,
            "casefold semantic deduplication failed")

    expected = indexer.expected_index()
    original_output = indexer.INDEX_OUTPUT
    with tempfile.TemporaryDirectory() as directory:
        probe = Path(directory) / "Master_Index.md"
        indexer.INDEX_OUTPUT = probe
        probe.write_text(expected, encoding="utf-8", newline="\n")
        require(indexer.index_is_fresh(), "fresh temporary index was rejected")
        probe.write_text(expected + "stale\n", encoding="utf-8", newline="\n")
        try:
            indexer.assert_index_fresh()
        except RuntimeError:
            pass
        else:
            raise AssertionError("stale temporary index did not fail closed")
    indexer.INDEX_OUTPUT = original_output

    print("PASS Master Index fixtures: traversal, tokens, order, dedup, freshness")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
