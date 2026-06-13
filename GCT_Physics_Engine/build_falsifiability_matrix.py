"""
build_falsifiability_matrix.py — Compile the manuscript's Falsifiability Matrix
from two inputs:

  1. `falsifiability_registry.json` — explicit "falsified if X" metadata per
     claim (predicted, threshold, mechanism, experiment, timeframe). Sourced
     by hand from App V Prediction Registry + Ch22 binary gates + Protocol
     chapters Ch13–21.

  2. `verify_independent/results/scorecard.json` — the numerical scorecard
     (predicted vs observed, ppm, status) produced by the independent
     verification suite.

Output:

  - `<repo>/content/98_Global_Appendices/App_FM_Falsifiability_Matrix.md`
    A single-source-of-truth markdown asset embedded in the manuscript.

Run:
    py -3.13 GCT_Physics_Engine/build_falsifiability_matrix.py

Exit code: 0 if every non-terminal Tier-2 claim with a verifier is inside
its falsification band. Non-zero if any undisclosed/non-terminal row has
crossed the threshold.

Reporting rule: TENSION rows (Tier 3 or 2σ tensions) are surfaced
explicitly with their σ distance, not flattened to "ok". A TENSION row does
not cause non-zero exit — it's expected by the registry. A disclosed
non-terminal band violation with a `band_violation_disclosure` is rendered as
TENSION; an undisclosed or terminal FAIL row causes non-zero exit unless the
registry marks it as a disclosed `registered_terminal_closure_state`.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ENGINE_ROOT = Path(__file__).resolve().parent
MANUSCRIPT_ROOT = ENGINE_ROOT.parent
REGISTRY_PATH = ENGINE_ROOT / "falsifiability_registry.json"
SCORECARD_PATH = ENGINE_ROOT / "verify_independent" / "results" / "scorecard.json"
OUTPUT_PATH = MANUSCRIPT_ROOT / "content" / "98_Global_Appendices" / "App_FM_Falsifiability_Matrix.md"


def _load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"required input not found: {path}")
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def _band_violation_scope_disclosure(registry: dict, failed_count: int) -> str:
    """Emit the per-BAND-VIOLATION-row scope-disclosure paragraph as a
    canonical part of the auto-generated FM.2 output.

    The disclosure is read from the registry entries'
    `band_violation_disclosure` field (if present) so each
    BAND-VIOLATION-class row carries its own scope explanation.
    """
    if failed_count == 0:
        return ""
    lines = [
        "**Scope disclosure for BAND-VIOLATION and near-boundary rows.** Flagged rows "
        "are registered adverse or closure-target rows under known Open Problems; they are not undisclosed "
        "falsification events and they must not be re-described as successes. Reading the FM exit status "
        "without this scope is the load-bearing risk; the disclosure below is the load-bearing reading discipline.",
        "",
    ]
    for entry in registry["entries"]:
        disclosure = entry.get("band_violation_disclosure")
        if not disclosure:
            continue
        lines.append(f"- **Row {entry['id']}** — {disclosure}")
    if len(lines) == 2:
        # No registry-side disclosures; fall back to a generic note pointing
        # at the registry's closure-target entries.
        lines.append(
            "- (No per-row band_violation_disclosure fields registered in "
            "`falsifiability_registry.json`. Add a `band_violation_disclosure` field to "
            "each BAND-VIOLATION-class entry to surface the closure-target context.)"
        )
    lines.append("")
    lines.append(
        "These rows do not by themselves falsify the underlying Tier 2 mechanisms, but terminal current-source "
        "FAIL rows count as adverse evidence until their registered source-promotion or closure path lands. "
        "Their closure paths are documented in App H and the engine docstrings."
    )
    return "\n".join(lines)


def _status_pill(status: str, has_verifier: bool, entry: dict | None = None, item: dict | None = None) -> str:
    """
    Status pill with empirical-vs-algebraic granularity:
      ○ PENDING-VERIFIER  — no verifier script bound
      ○ OPEN-RESEARCH     — registry marks open_research: true (claim catalogued under an Open Problem)
      ✓ DETECTED-TIGHT    — App V Prediction row with landed empirical test at tight precision
      ✓ DETECTED-MARGINAL — App V Prediction row with landed empirical test at marginal precision
      ✓ POSTDICTION-CONSISTENT — settled-data alignment check; does not count as in-favor evidence
      ✓ CONSISTENT        — engine-internal algebraic agreement against the registered empirical anchor
      ✓ ALGEBRAIC         — algebraic identity, no empirical detection target
      ✓ TIER-1 EXACT      — Tier 1 algebraic identity verified at machine precision
      ⚠ PROTECTED-SUBSPACE-REQUIRED — bare-vs-renormalized frequency row whose PASS depends on O.23 protected-subspace renormalization
      ⚠ TENSION           — within tolerance but at 2σ-class disagreement with current data
      ⚠ PENDING-α-RESOLUTION — input-contingent; does not count as in-favor evidence
      ⚠ AT-GATE TENSION   — tension marker only; does not count as in-favor evidence
      △ CURRENT-DATA-TENSION — adverse current-data flag; does not count as in-favor evidence
      ✗ FAIL              — outside the registered falsification band or verifier-level failure; counts against GCT

    A row is DETECTED iff it is explicitly labeled as an App V Prediction row,
    marked `counts_as_empirical_detection: true`, has a landed empirical test,
    and falls within the band. Settled-data Postdiction/anchor rows use
    POSTDICTION-CONSISTENT instead. A row is ALGEBRAIC iff the verifier checks
    an internal algebraic identity but the empirical detection is forward-looking
    or explicitly Inconclusive. Otherwise PASS → CONSISTENT.

    A row with `open_research: true` in the registry overrides the verifier status
    to OPEN-RESEARCH regardless of the verifier's PASS/FAIL output, because the
    claim is catalogued under an Open Problem and the verifier output is a
    candidate-ansatz reference rather than a live prediction.
    """
    if _registry_band_failed(entry, item):
        if (
            entry is not None
            and entry.get("band_violation_disclosure")
            and entry.get("registered_terminal_closure_state") is False
        ):
            return "⚠ TENSION"
        return "✗ FAIL"
    if entry is not None and item is not None and entry.get("tau_tri_state_gate_ppm"):
        ppm = item.get("independent_precision_ppm")
        gate = entry["tau_tri_state_gate_ppm"]
        if ppm is not None and gate["pass_lt"] <= abs(ppm) < gate["at_gate_tension_lt"]:
            return "⚠ AT-GATE TENSION"
    # Open-research override: registry tag wins over verifier status
    if entry is not None and entry.get("open_research") is True:
        return "○ OPEN-RESEARCH"
    if entry is not None and entry.get("current_data_tension") is True:
        return "△ CURRENT-DATA-TENSION (DESI DR2 registered-menu closure-fail; Euclid DR1 reserved for future robustness check)"
    if entry is not None and entry.get("protected_subspace_required") is True:
        return "⚠ PROTECTED-SUBSPACE-REQUIRED"
    registry_text = ""
    if entry is not None:
        registry_text = " ".join(
            str(entry.get(key) or "") for key in ("disposition_text", "falsification", "notes")
        )
    if entry is not None and not has_verifier and "CLOSURE-FAILS" in registry_text:
        return "⚠ EVALUATED-CLOSURE-FAILURE"
    if not has_verifier:
        return "○ PENDING-VERIFIER"
    if status == "TIER1_EXACT":
        return "✓ TIER-1 EXACT"
    if status == "PENDING-α-RESOLUTION":
        return "⚠ PENDING-α-RESOLUTION"
    if status == "OPEN_CONDITIONAL":
        return "○ OPEN-CONDITIONAL"
    if status == "INTERNAL_ARITHMETIC_PASS":
        return "✓ ALGEBRAIC"
    if entry is not None and entry.get("postdiction_check") is True and status == "TENSION":
        return "✓ POSTDICTION-CONSISTENT"
    if status == "TENSION":
        # Distinguish ordinary TENSION (2σ-class disagreement) from the
        # WP2025 muon-g-2 arbitration state. The registry tier string is
        # the load-bearing source for this disposition, so regeneration
        # preserves the manuscript's WP2025-specific wording.
        tier_text = entry.get("tier", "") if entry is not None else ""
        if (
            "Tension under WP2025" in tier_text
            or "calibration-survival conjecture" in tier_text
        ):
            return "⚠ TENSION UNDER WP2025"

        # Generic ≥2.5σ disagreements remain live tensions; the verifier's
        # sigma field is the load-bearing discriminator and we fall back to
        # TENSION if sigma is unavailable.
        sigma = None
        if item is not None:
            sigma = item.get("sigma_tension") or item.get("sigma") or item.get("independent_sigma")
            if sigma is None:
                ppm = item.get("independent_precision_ppm")
                # Heuristic: if ppm is enormous (> 5e6) the row is far beyond
                # 2σ-class. This is a fallback when the verifier didn't emit
                # an explicit sigma field.
                if ppm is not None and abs(ppm) > 5_000_000:
                    sigma = 3.5
        if sigma is not None and abs(sigma) >= 2.5:
            return "⚠ TENSION"
        return "⚠ TENSION"
    if status == "FAIL":
        return "✗ FAIL"
    if status == "PASS":
        # Classify PASS into DETECTED-TIGHT / DETECTED-MARGINAL / CONSISTENT / ALGEBRAIC based on timeframe + experiment + ppm
        if entry is not None:
            if entry.get("id") == "P.37":
                return "✓ ARITHMETIC-CONSISTENT (biology pending O.21+O.33)"
            if entry.get("postdiction_check") is True:
                return "✓ POSTDICTION-CONSISTENT"
            band_ppm = entry.get("falsification_band_ppm")
            timeframe = (entry.get("timeframe") or "").lower()
            experiment = (entry.get("experiment") or "").lower()
            is_forward = any(label in timeframe for label in ("near-term", "long-horizon", "long horizon", "future", "horizon", "n/a", "ska", "roman", "euclid", "dune", "hyper-k"))
            is_algebraic_identity = "n/a" in experiment or "algebraic identity" in experiment or "machine precision" in experiment
            is_inconclusive = "inconclusive" in experiment or "under test" in experiment
            app_v_type = (entry.get("app_v_type") or "").strip().lower()
            counts_detection = bool(entry.get("counts_as_empirical_detection", False))
            # DETECTED is firewall-protected: only App V Prediction rows that
            # explicitly opt into landed empirical-detection accounting may
            # enter the in-favor evidence count. Settled postdictions and
            # anchor-normalized rows remain alignment checks.
            is_settled = ("settled" in experiment or "codata" in experiment or "pdg" in experiment or "lhc" in experiment or "lep" in experiment)
            is_immediate = "immediate" in timeframe
            if is_settled and is_immediate and not is_algebraic_identity and not is_inconclusive:
                if app_v_type == "prediction" and counts_detection:
                    # Split DETECTED into TIGHT (band <= 1000 ppm) and MARGINAL
                    # (band > 1000 ppm but within band). Rows with band == None
                    # get MARGINAL by default (no quantitative band -> cannot be TIGHT).
                    if band_ppm is not None and band_ppm <= 1000.0:
                        return "✓ DETECTED-TIGHT"
                    return "✓ DETECTED-MARGINAL"
                return "✓ POSTDICTION-CONSISTENT"
            if is_algebraic_identity:
                return "✓ ALGEBRAIC"
            if is_forward or is_inconclusive:
                return "✓ ALGEBRAIC"  # internally consistent, empirical detection pending
            return "✓ CONSISTENT"
        return "✓ CONSISTENT"
    return f"? {status}"


def _registry_band_failed(entry: dict | None, item: dict | None) -> bool:
    """True when the scorecard precision exceeds the registered falsification band."""
    if entry is None or item is None:
        return False
    ppm = item.get("independent_precision_ppm")
    band_ppm = entry.get("falsification_band_ppm")
    tau_gate = entry.get("tau_tri_state_gate_ppm")
    if tau_gate is not None:
        return ppm is not None and abs(ppm) >= tau_gate["fail_gte"]
    return ppm is not None and band_ppm is not None and abs(ppm) > band_ppm


def _ppm_str(it: dict, entry: dict | None = None) -> str:
    if entry and entry.get("precision_display"):
        return entry["precision_display"]
    if it is None:
        return "—"
    p = it.get("independent_precision_ppm")
    if p is None:
        return "—"
    if abs(p) >= 1000:
        return f"{p/1000:.2f} × 10³"
    return f"{p:.0f}"


def _value_str(it: dict, entry: dict | None = None) -> str:
    if entry and entry.get("value_display"):
        return entry["value_display"]
    if it is None:
        return "—"
    pred = it.get("predicted")
    obs = it.get("observed")
    if pred is None:
        return "—"
    parts = []
    if isinstance(pred, float):
        parts.append(f"pred = {pred:.6g}")
    else:
        parts.append(f"pred = {pred}")
    if obs is not None:
        if isinstance(obs, float):
            parts.append(f"obs = {obs:.6g}")
        else:
            parts.append(f"obs = {obs}")
    unit = it.get("unit")
    if unit and unit != "(dimensionless)":
        parts.append(f"[{unit}]")
    return " · ".join(parts)


def _cell(value: object) -> str:
    """Escape Markdown table delimiters while preserving rendered text."""
    return str(value).replace("\n", " ").replace("|", r"\|")


def _band_str(entry: dict) -> str:
    band_display = entry.get("falsification_band_display")
    if band_display:
        return str(band_display)
    ciss_clean = entry.get("S1_CISS_polarization_floor_clean_falsification_net")
    ciss_limited = entry.get("S1_CISS_polarization_floor_sensitivity_limited_net")
    if ciss_clean is not None and ciss_limited is not None:
        return f"P_CISS^net >= {ciss_clean:g} clean; >= {ciss_limited:g} sensitivity-limited"
    tau_gate = entry.get("tau_tri_state_gate_ppm")
    if tau_gate is not None:
        return (
            f"0-{tau_gate['pass_lt']:g} PASS; "
            f"{tau_gate['pass_lt']:g}-{tau_gate['at_gate_tension_lt']:g} AT-GATE TENSION; "
            f">={tau_gate['fail_gte']:g} FAIL"
        )
    band_ppm = entry.get("falsification_band_ppm")
    band_max = entry.get("falsification_band_eV_max") or entry.get("falsification_band_eV")
    if band_ppm is not None:
        return f"{band_ppm:g} ppm"
    if band_max is not None:
        falsif = entry.get("falsification") or ""
        if "W_int" in falsif:
            return f"W_int > {band_max:g} eV"
        return f"Σ < {band_max:g} eV"
    # Quantitative threshold may be embedded in the falsification text even
    # when band_ppm is null (e.g., "T_2 enhancement < 100x", "|d_n| < 1.8e-26").
    # In that case report "qualitative (threshold in mechanism column)" to
    # signal that the row has an operational falsification target but the
    # band format is not ppm-normalisable.
    falsif = entry.get("falsification") or ""
    has_embedded_threshold = any(marker in falsif for marker in ("<", ">", "exceeds", "below", "above", "outside", "deviates", "differs"))
    if has_embedded_threshold:
        return "operational (see Mechanism)"
    return "qualitative"


def _mechanism_str(entry: dict) -> str:
    text = str(entry["disposition_text"])
    decision_rule = entry.get("S1_CISS_decision_rule")
    if decision_rule:
        return f"{text} S1 CISS decision rule: {decision_rule}."
    return text


def _scorecard_lookup_keys(verifier_name: str | None) -> list[str]:
    """Return scorecard-name candidates for a registry verifier binding.

    Most rows store the scorecard `name` directly (for example
    `muon_mass`). A few rows store a verifier path plus claim selector such
    as `verify_independent/verify_pmns.py::pmns_unitarity_3x3`; for those
    rows the claim selector is the scorecard key.
    """
    if not verifier_name:
        return []
    raw = str(verifier_name)
    keys = [raw]
    if "::" in raw:
        path_part, claim_part = raw.split("::", 1)
        keys.append(claim_part)
    else:
        path_part = raw
    stem = Path(path_part).stem
    keys.append(stem)
    if stem.startswith("verify_"):
        keys.append(stem.removeprefix("verify_"))
    # Preserve order while dropping duplicates/empties.
    out: list[str] = []
    for key in keys:
        if key and key not in out:
            out.append(key)
    return out


def build_matrix() -> tuple[str, int, dict]:
    registry = _load_json(REGISTRY_PATH)
    try:
        scorecard = _load_json(SCORECARD_PATH)
    except FileNotFoundError:
        print(f"WARN: scorecard not found at {SCORECARD_PATH} — run "
              "verify_independent/run_all.py first. Building matrix with "
              "PENDING-VERIFIER status on all rows.", file=sys.stderr)
        scorecard = {"items": []}

    score_items = sorted(
        scorecard.get("items", []),
        key=lambda it: (str(it.get("name", "")), json.dumps(it, sort_keys=True, ensure_ascii=False)),
    )
    score_by_name: dict[str, dict] = {}
    for it in score_items:
        name = it.get("name")
        if name:
            score_by_name[name] = it

    rows: list[str] = []
    failed = 0
    fatal_failed = 0
    tension = 0
    at_gate_tension = 0
    current_data_tension = 0
    pending_alpha_resolution = 0
    wp2025_tension = 0
    evaluated_closure_failure = 0
    protected_subspace_required = 0
    open_conditional = 0
    pending_verifier = 0
    open_research = 0
    detected_tight = 0
    detected_marginal = 0
    postdiction_consistent = 0
    consistent = 0
    algebraic = 0
    tier1_exact = 0
    summary: dict = {"by_tier": {}, "by_timeframe": {}}

    for entry in registry["entries"]:
        verifier = entry.get("verifier_name")
        sc = None
        for lookup_key in _scorecard_lookup_keys(verifier):
            sc = score_by_name.get(lookup_key)
            if sc is not None:
                break
        has_evaluated_verifier = bool(verifier and sc)
        status_raw = sc.get("status") if sc else "PENDING"
        status_disp = _status_pill(status_raw, has_evaluated_verifier, entry, sc)

        if "OPEN-RESEARCH" in status_disp:
            open_research += 1
        elif "CURRENT-DATA-TENSION" in status_disp:
            current_data_tension += 1
        elif "AT-GATE TENSION" in status_disp:
            at_gate_tension += 1
        elif "✗ FAIL" in status_disp:
            failed += 1
            if not entry.get("registered_terminal_closure_state"):
                fatal_failed += 1
        elif "PROTECTED-SUBSPACE-REQUIRED" in status_disp:
            protected_subspace_required += 1
        elif "OPEN-CONDITIONAL" in status_disp:
            open_conditional += 1
        elif status_raw == "PENDING-α-RESOLUTION":
            pending_alpha_resolution += 1
        elif status_raw == "TENSION":
            if "TENSION UNDER WP2025" in status_disp:
                wp2025_tension += 1
            else:
                tension += 1
        elif status_raw == "TIER1_EXACT":
            tier1_exact += 1
        elif "EVALUATED-CLOSURE-FAILURE" in status_disp:
            evaluated_closure_failure += 1
        elif status_raw in ("PASS", "OPEN_CONDITIONAL"):
            # Classify into detected-tight/detected-marginal/consistent/algebraic/tension
            # using the same logic as the pill.
            if "TENSION" in status_disp:
                tension += 1
            elif "POSTDICTION-CONSISTENT" in status_disp:
                postdiction_consistent += 1
            elif "DETECTED-TIGHT" in status_disp:
                detected_tight += 1
            elif "DETECTED-MARGINAL" in status_disp:
                detected_marginal += 1
            elif "ALGEBRAIC" in status_disp:
                algebraic += 1
            else:
                consistent += 1
        else:
            pending_verifier += 1

        summary["by_tier"][entry["tier"]] = summary["by_tier"].get(entry["tier"], 0) + 1
        summary["by_timeframe"][entry["timeframe"]] = (
            summary["by_timeframe"].get(entry["timeframe"], 0) + 1
        )

        row = (
            f"| **{_cell(entry['id'])}** "
            f"| {_cell(entry['manuscript_ref'])} "
            f"| {_cell(entry['tier'])} "
            f"| {_cell(_value_str(sc, entry))} "
            f"| {_cell(_ppm_str(sc, entry))} "
            f"| {_cell(_band_str(entry))} "
            f"| {_cell(_mechanism_str(entry))} "
            f"| {_cell(entry['experiment'])} "
            f"| {_cell(entry['timeframe'])} "
            f"| {_cell(status_disp)} |"
        )
        rows.append(row)

    detected_total = detected_tight + detected_marginal
    passing = detected_total + postdiction_consistent + consistent + algebraic + tier1_exact
    total = passing + tension + at_gate_tension + current_data_tension + pending_alpha_resolution + wp2025_tension + protected_subspace_required + failed + pending_verifier + open_research + open_conditional + evaluated_closure_failure

    header = f"""# Appendix FM: Falsifiability Matrix

> Compiled from `falsifiability_registry.json` +
> `verify_independent/results/scorecard.json`.

## FM.1 Purpose

This appendix consolidates every quantitative GCT claim that carries an
explicit falsification threshold into a single machine-readable matrix. It
extends App V (Prediction Registry) by row-by-row tying each prediction to
(a) the verifier script that re-derives it from the engine, (b) the explicit
threshold beyond which the claim is falsified, and (c) the scorecard status
from the independent-verification suite.

The matrix is the manuscript's single source of truth for "is GCT still
empirically consistent?" — a TENSION or FAIL row is a real signal, not a
qualitative footnote.

## FM.2 Summary

Aggregated by status pill (see FM.3 below for pill semantics):

| Pill | Count | Reading |
| :--- | ---: | :--- |
| ✓ DETECTED-TIGHT | {detected_tight} | App V Prediction row whose decisive empirical test has landed inside a tight band (band ≤ 1000 ppm) — strongest empirical evidence for GCT |
| ✓ DETECTED-MARGINAL | {detected_marginal} | App V Prediction row whose decisive empirical test has landed inside a marginal band (band > 1000 ppm) — confirmatory but at lower-resolution |
| ✓ POSTDICTION-CONSISTENT | {postdiction_consistent} | Settled-data postdictive alignment check; internal consistency only, not prospective detection evidence |
| ✓ CONSISTENT | {consistent} | Engine-internal agreement with a settled empirical anchor |
| ✓ ALGEBRAIC | {algebraic} | Internal algebraic identity verified; empirical detection forward-looking or inconclusive |
| ✓ TIER-1 EXACT | {tier1_exact} | Tier-1 algebraic identity at machine precision |
| ⚠ TENSION | {tension} | Within the engine-internal enforcement contract but at 2σ-class disagreement or a non-falsifying disclosed tension |
| ⚠ AT-GATE TENSION | {at_gate_tension} | Row-specific tri-state tolerance band: above the pass edge but below the hard-fail edge |
| △ CURRENT-DATA-TENSION | {current_data_tension} | DESI DR2 registered-menu closure-fail; Euclid DR1 reserved for future robustness check |
| ⚠ PENDING-α-RESOLUTION | {pending_alpha_resolution} | Detection requires resolution of α-input ambiguity between Cs-α and Rb-α determinations; outcome locked when external α discord resolves. Does **not** count as detection evidence. |
| ⚠ TENSION UNDER WP2025 | {wp2025_tension} | The verifier reports the muon g-2 channel under the WP2025 lattice-dominant HVP synthesis: Tier 2 mechanism + Tier 3 1/5 coefficient + A3 + Tier 4 calibration-survival conjecture; Tension under WP2025; falsification conditional on long-term HVP-synthesis arbitration. The row is not "within tolerance" and is not load-bearing empirical evidence under the consolidated synthesis. |
| ⚠ EVALUATED-CLOSURE-FAILURE | {evaluated_closure_failure} | Closed-form scan completed and the registered closure menu fails; this is distinct from observational TENSION. |
| ⚠ PROTECTED-SUBSPACE-REQUIRED | {protected_subspace_required} | Bare-vs-renormalized frequency row where the verifier PASS is conditional on O.23 protected-subspace renormalization rather than direct bare-frequency agreement. |
| ✗ FAIL | {failed} | Outside the registered falsification band or verifier-level failure against the engine-internal enforcement contract |
| ○ OPEN-RESEARCH | {open_research} | Claim catalogued under an Open Problem; verifier output is a candidate-ansatz reference rather than a live prediction |
| ○ OPEN-CONDITIONAL | {open_conditional} | Executable verifier/preregistration exists, but decisive external data have not landed |
| ○ PENDING-VERIFIER | {pending_verifier} | No verifier script bound |
| **TOTAL** | **{total}** | |

**Reading-discipline note:** POSTDICTION-CONSISTENT + CONSISTENT + ALGEBRAIC + TIER-1 EXACT pills indicate the manuscript is *internally self-consistent* on the row; they are not empirical confirmations of GCT. **DETECTED-TIGHT / DETECTED-MARGINAL pills count as empirical evidence in favour of GCT only for rows labeled Prediction in App V whose decisive empirical test has landed. Postdiction rows use POSTDICTION-CONSISTENT and constitute alignment-check evidence, not prospective falsification-surviving detections.** PENDING-α-RESOLUTION, AT-GATE TENSION, CURRENT-DATA-TENSION, OPEN-CONDITIONAL, PENDING-VERIFIER, and OPEN-RESEARCH do **not** count as in-favor detection evidence. FAIL counts against the framework. Currently the DETECTED total is {detected_total} ({detected_tight} TIGHT + {detected_marginal} MARGINAL) out of {total} rows, reflecting that most of the GCT prediction set has its empirical-detection moment in long-horizon observational programmes. The POSTDICTION-CONSISTENT + CONSISTENT + ALGEBRAIC pills together quantify the manuscript's *internal coherence*, not its *empirical confirmation*.

**Verifier status from the scorecard:**
{"✓ No verifier-level falsification events." if failed == 0 else f"✗ {failed} falsification-band failure row(s) detected; see the scope disclosure that follows."}

{_band_violation_scope_disclosure(registry, failed)}

## FM.3 Status Pill Legend

To distinguish empirical detection from algebraic-internal consistency, the Status column uses the following pills. The Evidence Credibility column is normative for all App FM uses:

| Pill | Meaning | Evidence Credibility |
| :--- | :--- | :--- |
| **✓ DETECTED-TIGHT** | App V row labeled Prediction; empirical experiment has run, returned data, and the prediction falls within a tight falsification band (≤1000 ppm). | Counts as in-favor empirical evidence for GCT. |
| **✓ DETECTED-MARGINAL** | App V row labeled Prediction; empirical experiment has run, returned data, and the prediction falls within a marginal falsification band (>1000 ppm). | Counts as in-favor empirical evidence with an explicit lower-resolution caveat. |
| **✓ POSTDICTION-CONSISTENT** | Settled-data row used as a postdictive alignment check or dimensional-anchor closure audit. | Does **not** count as in-favor evidence; firewall-protected alignment only. |
| **✓ CONSISTENT** | Engine-internal algebraic agreement against the registered empirical anchor; the verifier reproduces the manuscript value within tolerance. | Does **not** count as empirical evidence in favor; internal consistency only. |
| **✓ ALGEBRAIC** | Algebraic identity verified at machine precision *or* a forward-looking prediction whose internal-consistency is checked but whose empirical detection target is not yet reached. | Does **not** count as empirical evidence in favor; internal consistency only. |
| **✓ TIER-1 EXACT** | Tier 1 algebraic identity verified at machine precision (e.g. Gram-determinant ratio). | Does **not** count as empirical evidence in favor; theorem/algebra status only. |
| **⚠ TENSION** | Within the engine-internal enforcement contract but at 2σ-class disagreement with current data, or a non-falsifying disclosed tension. | Does **not** count as in-favor evidence. |
| **⚠ AT-GATE TENSION** | Row-specific tri-state tolerance band: above the pass edge but below the hard-fail edge. | Does **not** count as in-favor evidence; tension marker only. |
| **△ CURRENT-DATA-TENSION** | DESI DR2 registered-menu closure-fail; Euclid DR1 is reserved for future robustness check. | Does **not** count as in-favor evidence; flags adverse current data. |
| **⚠ PENDING-α-RESOLUTION** | Detection requires resolution of α-input ambiguity between Cs-α and Rb-α determinations; outcome locked when external α discord resolves. | Does **not** count as in-favor evidence; input-contingent. |
| **⚠ TENSION UNDER WP2025** | Muon g-2 arbitration row under the WP2025 lattice-dominant HVP synthesis: Tier 2 mechanism + Tier 3 1/5 coefficient + A3 + Tier 4 calibration-survival conjecture; Tension under WP2025; falsification conditional on long-term HVP-synthesis arbitration. | Does **not** count as in-favor evidence; live tension. |
| **⚠ EVALUATED-CLOSURE-FAILURE** | Closed-form scan completed and the registered closure menu fails; reported separately from observational TENSION. | Does **not** count as in-favor evidence; failed closure menu. |
| **⚠ PROTECTED-SUBSPACE-REQUIRED** | Bare-vs-renormalized frequency row whose engine PASS is conditional on the O.23 protected-subspace renormalization closure, not direct agreement between the bare and observed frequency channels. | Does **not** count as in-favor evidence until O.23 closes and the empirical gate is rerun. |
| **✗ FAIL** | Outside the falsification band — a real falsification event. | Counts as against-GCT evidence. |
| **○ OPEN-RESEARCH** | The registry marks the row with `open_research: true` because the claim is catalogued under an Open Problem (App H §H.5). The verifier output is a candidate-ansatz reference (e.g. literal φ⁻²² evaluation for the Jarlskog invariant) rather than a live Tier 2 prediction. | Does **not** count as in-favor evidence; future-research target. |
| **○ OPEN-CONDITIONAL** | Verifier/preregistration is executable, but the decisive empirical dataset has not landed. | Does **not** count as in-favor evidence; externally undecided. |
| **○ PENDING-VERIFIER** | No verifier script bound to this row; verifier scaffold not yet implemented. | Does **not** count as in-favor evidence; no measurement/verifier yet. |

A row tagged POSTDICTION-CONSISTENT, CONSISTENT, ALGEBRAIC, or OPEN-CONDITIONAL is **not** an empirical confirmation — it is internal-consistency-checked, postdictively aligned, or executable-but-awaiting-data. Readers comparing the matrix's status pills should treat DETECTED-TIGHT and DETECTED-MARGINAL as the only in-favor empirical-evidence pills, and only for App V Prediction rows; PENDING-α-RESOLUTION and all tension/open/verifier-pending pills are non-evidential or adverse as specified above.

## FM.4 The Matrix

| ID | Manuscript Reference | Tier | Current Value | Precision (ppm) | Falsification Band | Disposition | Experiment | Timeframe | Status |
| :--- | :--- | :--- | :--- | ---: | :--- | :--- | :--- | :--- | :--- |
"""

    body = "\n".join(rows)

    footer = f"""

## FM.5 Cross-references

- **App V** — Prediction Registry (the user-facing P.X registration of
  pre-registered predictions; this matrix is its machine-readable companion).
- **App R** — Precision Scorecard (the engine-output precision report; this
  matrix consumes its `scorecard.json` artefact).
- **App TP** — Tier Promotion Roadmap (the candidates that, if closed,
  would change the Tier column of one or more rows in this matrix).
- **Ch22 §22.1** — Binary Gates (the four near-term falsification events
  that anchor the experimental programme).
"""

    summary["fatal_failed_rows"] = fatal_failed
    return header + body + footer, failed, summary


def main() -> int:
    # Reconfigure stdout to UTF-8 so the tier-summary print (which contains
    # non-ASCII characters such as alpha, sigma) does not crash on Windows
    # cp1252 consoles. Older Python builds without reconfigure() silently
    # skip this; the matrix output file itself is always written UTF-8.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    md, failed, summary = build_matrix()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(md, encoding="utf-8", newline="\n")
    print(f"Wrote {OUTPUT_PATH}")
    print(f"  by_tier: {json.dumps(summary['by_tier'], ensure_ascii=False, sort_keys=True)}")
    print(f"  failed_rows: {failed}")
    print(f"  fatal_failed_rows: {summary['fatal_failed_rows']}")
    return 0 if summary["fatal_failed_rows"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
