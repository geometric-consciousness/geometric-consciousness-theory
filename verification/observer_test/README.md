# Observer-correction test: public record

This folder is the public record of the preregistered observer-correction test mentioned in
CHANGELOG v1.3.0. Every file here is a byte-exact copy of the frozen or output file.

## Question

A Tier 4 hypothesis of the author: the Field's properties depend on the number of observers, so
φ-derived values would be "zero-observer" values and measured constants would carry an
observer-induced shift. The test asks whether the residuals of GCT's φ formulas on the 21
constants of the constant control test follow the sign pattern of one correction rule fixed before
any residual was examined.

The candidate rules were derived blind from four chapters (V1 Ch09, Ch11, Ch18, Ch20) by a separate
AI-assistant instance that saw only the hypothesis, the names of the 21 constants and those
chapters, and no GCT prediction or residual. The chapters give no derived sign or magnitude for any
observer shift, so the rules are Tier 4.

- **Rule A ("Zeno inertia", primary):** X = X₀(1 + ε·k) with ε > 0; masses, v and m_H shift up,
  couplings get weaker (1/α and 1/α_s up), mixing parameters get smaller; δ_CP makes no prediction.
  After the frozen mechanical exclusions (rows predicted as ratios to a reference mass cancel),
  8 rows predict.
- Rule B (coarse-graining direction) and Rule C (sign undetermined) are report-only.

Decision rule for Rule A (n = 8): SUPPORTED if A ≥ 7 sign agreements, ε̂ > 0, at least 6 rows
improved leave-one-out and p_rand ≤ 0.05; REFUTED if A ≤ 4 or ε̂ ≤ 0; otherwise INCONCLUSIVE. The full
machine transcription is `frozen/prereg_observer/rules.json`.

## Freeze

Frozen 2026-10-20. Bundle hash (SHA-256 of `frozen/prereg_observer/SHA256SUMS`):
`b9f405c736aba7ee6cf64b40b85772279ac50e87764f9a71ad24fb58c0de4c04`. It reuses the constant-control
v1 targets and GCT formulas (`../constant_control_test/frozen/prereg/`), whose hashes appear in the
manifest.

## Result

**Rule A: REFUTED** under the frozen rule (`results/out_observer/verdict.json`).

| Statistic | Value | SUPPORTED needs |
| :--- | :--- | :--- |
| A (rows whose residual sign matches Rule A) | 4 of 8 | ≥ 7 |
| ε̂ (median r/k) | −0.0038 (wrong sign) | > 0 |
| Rows improved leave-one-out | 0 of 8 | ≥ 6 |
| p_rand (256 sign patterns) | 1.00 | ≤ 0.05 |

Rule B (report-only) agrees on 3 of 3 rows, which cannot reach p ≤ 0.05 by construction and is
equally explained by reading the geometric values as ultraviolet values. Rule C is not testable.

Scope: this refutes Rule A's per-row sign mapping only, not every observer hypothesis. It changes no
row, tier or count of the manuscript.

Disclosed deviation: the frozen test script crashed while writing its JSON output (a serialisation
error) before printing or saving anything; a serialisation-only fix was applied and the computation
was unchanged.

## Not included in this release

The frozen design document, the blind reader's prompt and output, and the test code are listed in
the manifest but are not published here, because they contain private correspondence identifiers
or machine-local paths. Their SHA-256 values in the manifest fix their frozen content.
