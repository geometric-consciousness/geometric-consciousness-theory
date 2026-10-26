# Constant control test (φ against random constants): public record

This folder is the public record of the preregistered constant control test reported in
App PSC §PSC.9.6. It holds the frozen design data, the bundle hash manifests, and the machine
verdicts of the three frozen versions. Every file here is a byte-exact copy of the frozen or
output file; `.gitattributes` keeps this folder out of line-ending conversion so the SHA-256
values below can be checked on any checkout.

## Question

Under one formula grammar built from GCT's own formula templates and applied identically to every
base, does φ fit 21 measured constants (lepton, quark and Higgs masses, couplings, CKM and PMNS
mixing parameters) better than random constants do? Comparator values and their sources are in
`frozen/COMPARATORS.md` (retrieved 2026-10-19; PDG 2024, CODATA 2022, NuFIT 6.0).

## Versions and verdicts

| Version | Frozen | Bundle hash (SHA-256 of the bundle's `SHA256SUMS`) | Validity | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| v1 | 2026-10-19 | `2510829f30423bd7f32651cd70fed24d182c5a0f1ed48fffb3a111e7621553ba` | INVALID: the scrambled-target negative control favoured φ (KS p = 6×10⁻⁹) because the description-length score trended with the size of the base; underpowered | None issued (`results/out/verdict.json`) |
| v2 | 2026-10-20 | `c382047f8c3a40bf9be2d649738e312953c29d147a1aa6e9d2f2d89ae564066e` | INVALID: self-calibration fixed the v1 problem (scrambled control KS 0.23), but 300 random bases on the real targets did not give uniform p-values (KS p = 0.0022) | None issued (`results/out_v2/verdict_v2.json`) |
| v3 | 2026-10-20 | `8ea95ce700dbadb116eeca91cda71aae9a02853651737e9c968d78a43d4c043d` | Valid and powered | **NEGATIVE-FRAGILE** (`results/out_v3/verdict_v3.json`) |

The seeds of each run derive from its bundle hash, and each run verified the bundle before
starting. v2 and v3 reuse the v1 data files (targets, grammar, configuration, GCT formulas), whose
hashes appear in their manifests.

## v3 result

- Primary statistic: φ's rank among 300 random bases on the same real targets, each base
  self-calibrated against its own dithered targets; a hit counts only if the base enters the
  formula's exponent. Decision threshold p ≤ 0.01.
- **p₀ = 0.196**: 58 of 300 random bases do at least as well as φ.
- Power for a planted effect on 6 of the 8 informative rows (k = 6): **1.00** (50 of 50).
- φ hits 18 of 21 rows; it misses m_t, m_H and sin²θ_W.
- **FRAGILE**: when GCT's own integers get cheap codes (variant V2), φ ranks first of 101
  (p = 0.0099). That variant rewards GCT's after-the-fact choice of integers and is not a positive
  signal. Variant V6 (drop the rows GCT itself scores as failure or tension) gives 0.143.
- Validity checks passed: paired scrambled-target control (two-sample KS 0.994), reference
  regression, a blind second implementation written from the frozen document (identical
  results), and bit-identical determinism. In v3 the one-sample uniformity check of the random
  bases on the real targets (the v2 failure) is report-only under the frozen rules, because the
  primary statistic is now a rank among those bases; it reads KS 0.015.

Frozen scope sentence: the test "excludes, at power ≥ 0.8, an effect in which φ hits at least 6 of
the 8 informative rows through a real effect; weaker effects are not excluded."

The test is **non-confirmatory**: it re-analyses public data, and the v3 statistic was chosen after
v1 and v2 had been run. Confirmatory evidence can only come from formulas registered before their
targets are compared. The test froze PDG 2024's sin²θ_W (0.23129); the manuscript uses the PDG 2026
MS-bar value 0.23122.

Disclosed deviations (none touched the real-target scores): before the v2 freeze, a compute-timing
script evaluated random bases on dithered real targets and its scores were discarded unseen; the
v2 power control (k = 6) was fixed after a scrambled-target pilot; the v3 design was informed by
the public v2 control arrays and by φ's known v2 result; the v3 cloud run was pre-empted three times
and resumed from checkpointed chunks.

## Consequence in the manuscript

Every row or claim that presents a φ-based mass or constant formula as evidence that φ or
icosahedral structure is special is Tier 4 as evidence. The numbers are kept as descriptive
arithmetic, and the earlier global-significance figures stay withdrawn (App PSC §PSC.9.6).

## Contents

- `frozen/COMPARATORS.md`, `frozen/prereg/` (v1 data: `targets.json`, `grammar.json`,
  `config.json`, `gct_formulas.json`, `forward_ledger.json`, `SHA256SUMS`)
- `frozen/prereg_v2/` (`config_v2.json`, `decision_rules_v2.json`, `SHA256SUMS`)
- `frozen/prereg_v3/` (`config_v3.json`, `decision_rules_v3.json`, `SHA256SUMS`)
- `results/` (machine verdicts of v1, v2 and v3, and the SHA-256 of the v2/v3 unit plans)

## Not included in this release

The frozen design documents (`PREREG_FROZEN.md`, `PREREG_V2_FROZEN.md`, `PREREG_V3_FROZEN.md`),
the v1 `prereg/decision_rules.json`, the test code (`src/`) and the cloud run scripts are listed in
the `SHA256SUMS` manifests but are not published here, because they contain private correspondence
identifiers or machine-local paths. Their SHA-256 values in the manifests fix their frozen content,
so a later public copy can be checked against them. The decision rules of v2 and v3, which govern
the verdicts above, are included.

## Checking the hashes

From this folder, for each bundle (example for v3):

```
cd frozen
sha256sum prereg_v3/SHA256SUMS      # must equal the v3 bundle hash above
sha256sum prereg_v3/config_v3.json prereg_v3/decision_rules_v3.json prereg/targets.json
# compare with the corresponding lines of prereg_v3/SHA256SUMS
```
