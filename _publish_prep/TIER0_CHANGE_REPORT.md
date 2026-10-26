# Tier 0 change report

Baseline: `b3acea3855392b9ac9f01219d63bd89c8d3332d5`, branch `release-1.3.0-integration`.

Tier 0 contains exactly one item: experience is occurring, i.e. there is presence now. It is neither postulated nor derived; doubting and dreaming are occurrences of experience. No other claim may ever enter Tier 0. Axiom 1 remains the stipulated universal Level I generalisation at Tier 1. Objective idealism remains the Tier 3 parsimony choice. Level II substrate verdicts remain open (Tier 3) / NOT_EVALUATED.

The datum/Axiom-1 conflation is separated in the frontmatter, abstracts, Chapters 1–3, 6, 10 and 16, glossaries, and publication metadata. Chapter 10's certainty language about choosing is narrowed to the occurrence of experience, without granting agency or causal efficacy Tier 0 status. The three volume notation sections and Chapter 23 include Tier 0 in their summaries. Appendix TCD applies the one-item gate before its decision tree; Appendix TPR excludes Tier 0 from promotion destinations. Part VI descriptions use the epistemic tier system without a stale tier count.

GF.1.1 has a matching Tier 0 band above the existing tiers. No GF.1.1 producer was found among repository Python scripts, including ignored scripts; its SVG was edited minimally. GF.2.1's short axiom definition identifies universal Level I presence as Tier 1. Both SVG/PDF pairs were rendered and visually inspected; `TIER0_GF1_1.png` preserves the requested PNG preview.

## Tier census

The reproducible check is `py -3.13 -X utf8 _publish_prep/verify_tier0.py`. It compares every tracked file under `content/` against the baseline. [TIER0_CENSUS.csv](TIER0_CENSUS.csv) records all six tier counts per file, including zeros; [TIER0_CENSUS.json](TIER0_CENSUS.json) records exact added/removed bracket labels.

| Bracket label | Before | After |
|---|---:|---:|
| Tier 0 | 0 | 6 |
| Tier 1 | 286 | 298 |
| Tier 1/2 | 22 | 22 |
| Tier 2 | 198 | 198 |
| Tier 3 | 678 | 678 |
| Tier 4 | 106 | 106 |

All existing bracket labels survive verbatim except exactly three `[Tier 1 — Axiom of Presence]` labels for the datum: two in Ch01 and one in Ch02 become `[Tier 0 — First-Person Datum]`. Three further Tier 0 annotations identify the same datum, not additional items. Fifteen Tier 1 annotations clarify the unchanged universal axiom, producing a net Tier 1 increase of twelve. No other claim changes tier. All unchanged per-file counts are included in the CSV (204 files).

## Verification

Engine verifier: PASS, exit 0; 62/62 expected results, zero drift failures and zero failed enforced registry comparisons. Scientific closure remains 12 confirmed / 32 open / 9 conditional / 9 tension. The direct PyPhi calculation ran without cache replay. No tracked engine source or data differs from baseline.

All five existing build fixture suites pass, including the full 40-figure Chromium Unicode smoke checks and 6,766 table-export checks. Metadata, figure inventory, index, expected-outcome, JSON-producer, verifier-status, registry-ID, registry/appendix, PHI-SSOT and permanent-register fixture checks pass.

The canonical full build passes all three XeLaTeX passes. Final prose QA refinements trigger a text rebuild through the same compiler with the 40 already converted, structurally validated and Unicode-validated figure pairs reused. Final PDF acceptance passes at 1,091 pages (A4, required fonts/metadata/landmarks/link annotations, 40 SVG/PDF pairs, no replacement glyph or U+202F). The release checker's page expectation changes from 1,093 to 1,091 to match the rebuilt artifact. The 29 pages containing Tier 0 are visually covered by the initial review plus final refinement/addition renders. No clipping or overlap is observed.

The initial inventory check overlapped output reset and saw the temporarily absent PDF; its final rerun passes after the build and exact inventory regeneration (706 files). Release acceptance initially detects the changed page count; the expectation is updated and the final acceptance check passes. The commit-bound release manifest is refreshed after the source commit, as required by its ancestor/source-hash contract. [TIER0_TEST_RESULTS.json](TIER0_TEST_RESULTS.json) records commands and outcomes. Raw execution logs remain locally under `tier0_checks/`.

Law 8: zero forbidden added lines or added words across `content/` and `GCT_Physics_Engine/`. No dedicated Law 8 script is present in this worktree; the saved verification script performs the boundary diff scans. `git diff --check` passes.

## Scope and ambiguities

- The requested `git grep -n -i -E "axiom 1|axiom of presence|first-person datum|tier 1 by stipulation|Universal Presence"` search covers `content/`, README, CHANGELOG, `_publish_prep/`, and the generated monolith; the global and volume abstracts are under `content/`. A complementary first-person/apperception search finds Ch02's input-datum passage.
- `_publish_prep/` contains no existing release-note prose; only the brand asset is present at baseline. CHANGELOG is a root-level release-history document, outside the timeless manuscript/engine boundary, so the v1.3.0 entry uses its existing "Added" style.
- No general tier enum/validator was found in engine Python, YAML or JSON. Numerical-constant categories, per-observable tier maps and existing result tiers are not global tier enumerations; no numerical datum or artificial engine Tier 0 parameter is introduced.
- Existing Tier 1 mathematical definitions and Tier 1 philosophical distinctions, including the Level I/II distinction, remain intact. The "missing cobordism datum" is a mathematical input, not the first-person presence datum, and remains untouched. V1.1.1 is an axioms-to-observables diagram rather than an enumeration of epistemic tiers and remains unchanged.
- The objective-idealism Tier 3 statements in Ch03 and Ch06 and all substrate verdicts retain their assignments. Release version/date metadata is unchanged; nothing is published or pushed.

Source commit: `a9a71451fa7c2a796c2a2d267b056f875066f20c` (pablogona; requested subject and Codex co-author). Release manifest write and check both pass against this source ancestor. Final PDF SHA-256: `b563d9f95fcf203cd517910dc28cae749ae186bc97f07f6ef300d434639b02ed`. The manifest and verification record are recorded in a follow-up commit because the manifest contract requires committed source inputs.

Local QA renders under `_audit_workspace/tier0_pdf_qa/` remain untracked and are excluded by the repository inventory policy. The requested GF.1.1 PNG preview is committed under `_publish_prep/`.

## Files changed



```text
.zenodo.json
CHANGELOG.md
CITATION.cff
CODEBASE_STRUCTURE.md
Geometric_Consciousness_Theory.md
README.md
_publish_prep/TIER0_CENSUS.csv
_publish_prep/TIER0_CENSUS.json
_publish_prep/TIER0_CHANGE_REPORT.md
_publish_prep/TIER0_GF1_1.png
_publish_prep/TIER0_TEST_RESULTS.json
_publish_prep/verify_tier0.py
build_scripts/manage_release_package.py
content/00_Global_Frontmatter/00_Global_Abstract.md
content/00_Global_Frontmatter/01_Epistemic_Tier_System.md
content/00_Global_Frontmatter/02_Axiom_and_Postulate_Ledger.md
content/01_Volume_1_Operating_System/00_Frontmatter/00_Abstract.md
content/01_Volume_1_Operating_System/00_Frontmatter/02_Notation.md
content/01_Volume_1_Operating_System/01_Part_I_Logic_of_Being/Ch01_Staircase_of_Certainty.md
content/01_Volume_1_Operating_System/01_Part_I_Logic_of_Being/Ch02_Axiomatic_Foundation.md
content/01_Volume_1_Operating_System/01_Part_I_Logic_of_Being/Ch03_Ontological_Fork.md
content/01_Volume_1_Operating_System/02_Part_II_Identity/Ch06_Tripartite_Ontology.md
content/01_Volume_1_Operating_System/03_Part_III_Rendering/Ch10_Russellian_Causation.md
content/01_Volume_1_Operating_System/05_Part_V_Experience/Ch16_Time_and_Qualia.md
content/01_Volume_1_Operating_System/06_Part_VI_Applications_and_Extensions/00_Part_VI_Introduction.md
content/01_Volume_1_Operating_System/06_Part_VI_Applications_and_Extensions/Ch23_Philosophy_of_Science.md
content/01_Volume_1_Operating_System/99_Backmatter/01_Glossary.md
content/02_Volume_2_Cosmic_Architecture/00_Frontmatter/02_Notation.md
content/03_Volume_3_Matter_Spectrum/00_Frontmatter/02_Notation.md
content/98_Global_Appendices/App_TCD_Tier_Classification.md
content/98_Global_Appendices/App_TPR_Tier_Promotion_Roadmap.md
content/99_Global_Backmatter/01_Master_Glossary.md
content/Figures/Frontmatter/Figure GF.1.1.pdf
content/Figures/Frontmatter/Figure GF.1.1.svg
content/Figures/Frontmatter/Figure GF.2.1.pdf
content/Figures/Frontmatter/Figure GF.2.1.svg
content/Figures/GCT_Figures_Catalog_DETAILED.md
output/GCT_Figures_Catalog_DETAILED.md
output/Geometric_Consciousness_Theory.pdf
output/Geometric_Consciousness_Theory.tex
output/figures_manifest.json
output/release_manifest.json
```
