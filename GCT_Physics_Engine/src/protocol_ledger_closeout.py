#!/usr/bin/env python3
"""
protocol_ledger_closeout.py — Final Ledger Declarations
=======================================================================
Records two theory-status declarations: the Born Rule conditional
compatibility theorem and the muon g-2 HVP resolution stance.

Born Rule — Conditional Compatibility Theorem
---------------------------------------------------------------
Born Rule is recorded as a Tier 3 conditional compatibility theorem via
Gleason's Theorem under GCT's Selection Operator construction. This script
records the status only; it does not implement proofs of countable additivity
(O.40a) or noncontextuality (O.40b) on the projection lattice.

HVP Resolution Stance
-----------------------------
The GCT 3-loop vertex correction:
    Δa_μ = 250.65 × 10⁻¹¹
is a Tier 2 geometric mechanism with a Tier 3 equal-weight 1/5 coefficient
and A3 measured-alpha input. Under WP2025, however, the Standard
Model-experiment muon g-2 gap is only ~37.5 × 10⁻¹¹ (~0.6σ), so the
GCT correction is not load-bearing empirical evidence under WP2025 and is carried as a
Tier 4 calibration-survival conjecture pending HVP-synthesis arbitration.

Outputs
-------
  protocol_ledger_closeout_results.json  — human-readable combined declaration
  Also updates (appends to) claim_registry.json with new entries; this is an
  idempotent maintenance write by default. Pass --assert-registry-current for
  a read-only parity check that fails if the maintenance write would change
  claim_registry.json.

This protocol performs an idempotent registry
maintenance write while producing its result JSON. Production parity checks
therefore treat the registry as the source-of-truth input and expect the write
to be byte-stable. The O.40a/O.40b closure targets are read-only audit entries plus a separate
registry-generation command.
"""

import json
import sys
import argparse
from pathlib import Path
from gct_utils import get_output_path

CLAIM_REGISTRY_PATH = Path(__file__).parent.parent / "config" / "claim_registry.json"


# ── Born Rule payload ─────────────────────────────────────────────────────────

C_BORN_RULE_TIER2_STATUS = {
    "task_id":   "born_rule_closure",
    "title":     "Born Rule — Conditional Compatibility via Gleason's Theorem",
    "input_tier": "Tier 3 — Conditional compatibility theorem",
    "closed_tier": "TIER3-CONDITIONAL-COMPATIBILITY",
    "rationale": (
        "Born Rule is a conditional compatibility theorem via Gleason's "
        "Theorem under GCT's Selection Operator construction. The executable "
        "does not prove the projection-lattice hypotheses needed before "
        "Gleason can be invoked: countable additivity (O.40a) and "
        "noncontextuality / basis-independence (O.40b)."
    ),
    "falsification_condition": (
        "If future work shows that the RT acceptance-window measure is "
        "incompatible with the Born Rule (i.e., yields systematically different "
        "probabilities for any observable over the GCT Hilbert space), then GCT "
        "is falsified at the quantum measurement level."
    ),
    "status": "TIER3-CONDITIONAL-COMPATIBILITY (Gleason representation conditional on O.40a countable additivity + O.40b noncontextuality; executable proof NOT IMPLEMENTED)",
}

# ── HVP stance payload ────────────────────────────────────────────────────────

C_HVP_STANCE_STATUS = {
    "task_id":   "hvp_resolution_stance",
    "title":     "HVP Resolution Stance",
    "gct_correction_value":  "Δa_μ = 250.65 × 10⁻¹¹  (3-loop phason vertex)",
    "experimental_gap":      "WP2025 Δa_μ_exp-SM ≈ 37.5 × 10⁻¹¹  (~0.6σ; no significant anomaly)",
    "gct_stance": (
        "The GCT 3-loop phason vertex correction (derived in protocol_qed_audit.py) "
        "is a Tier 2 geometric mechanism, with the equal-weight 1/5 vertex "
        "coefficient and measured low-energy alpha input carried as Tier 3/A3 "
        "provenance inputs. Under the WP2025 lattice-HVP synthesis there is no "
        "significant SM-experiment anomaly to close. The correction therefore "
        "sits in tension with the consolidated SM total and is carried as a "
        "Tier 4 calibration-survival conjecture conditional on long-term "
        "HVP-synthesis arbitration."
    ),
    "prediction": (
        "The channel is reinstated as a decisive empirical test only if R-ratio "
        "and lattice-HVP reconciliation opens a >3σ experiment-theory gap close "
        "to the GCT correction scale. Otherwise the correction remains a structural "
        "mechanism without current validation status."
    ),
    "falsification_condition": (
        "If the consolidated HVP synthesis remains lattice-dominant with a "
        "sub-1σ SM-experiment gap, the muon g-2 channel is not load-bearing "
        "evidence for GCT. A restored >3σ gap near Δa_μ = 250.65 × 10⁻¹¹ "
        "is required for validation."
    ),
    "status": "CLOSED — WP2025 tension stance recorded; arbitration condition explicit.",
}


# ── claim_registry.json additions ────────────────────────────────────────────

REGISTRY_ENTRIES = [
    {
        "claim_id":   "C_BORN_RULE_TIER2",
        "description": "Born Rule is a Tier 3 conditional compatibility theorem via Gleason's Theorem under GCT's Selection Operator construction, pending O.40a/O.40b.",
        "disposition_text": "TIER3-CONDITIONAL-COMPATIBILITY (Gleason representation conditional on O.40a countable additivity + O.40b noncontextuality; executable proof NOT IMPLEMENTED)",
        "monograph_location": "Global Frontmatter §3, Appendix D",
        "protocol_script":    "protocol_ledger_closeout.py",
        "protocol_output_json": "data/protocol_ledger_closeout_results.json",
        "json_field":         "C_BORN_RULE_TIER2_STATUS.status",
        "target_value":       "TIER3-CONDITIONAL-COMPATIBILITY (Gleason representation conditional on O.40a countable additivity + O.40b noncontextuality; executable proof NOT IMPLEMENTED)",
        "tolerance":          0,
        "tolerance_type":     "string_match",
        "claim_type":         "conditional_compatibility_theorem",
        "tier":               "Tier 3 conditional compatibility theorem pending O.40a/O.40b",
        "enforce":            False,
        "target_prompt":      "born_rule_closure",
    },
    {
        "claim_id":   "C_HVP_STANCE",
        "description": "Muon g-2 HVP stance under WP2025: no significant anomaly; GCT correction survives only conditionally on HVP-synthesis arbitration",
        "disposition_text": "Tier 2 mechanism + Tier 3 1/5 coefficient + A3 + Tier 4 calibration-survival conjecture (HVP arbitration); Tension under WP2025; falsification conditional on long-term HVP-synthesis arbitration",
        "monograph_location": "V3 Ch09, Appendix R.9",
        "protocol_script":    "protocol_ledger_closeout.py",
        "protocol_output_json": "data/protocol_ledger_closeout_results.json",
        "json_field":         "C_HVP_STANCE_STATUS.status",
        "target_value":       "CLOSED — WP2025 tension stance recorded; arbitration condition explicit.",
        "tolerance":          0,
        "tolerance_type":     "string_match",
        "claim_type":         "theoretical_stance",
        "tier":               "Tier 2 mechanism + Tier 3 1/5 coefficient + A3 + Tier 4 calibration-survival conjecture",
        "enforce":            False,
        "target_prompt":      "hvp_resolution_stance",
    },
]


# ── Main execution ────────────────────────────────────────────────────────────

def _load_claim_registry() -> list:
    if CLAIM_REGISTRY_PATH.exists():
        with open(CLAIM_REGISTRY_PATH, "r") as f:
            return json.load(f)
    return []


def _candidate_claim_registry(registry: list) -> tuple[list, int, int, list[str]]:
    candidate = [dict(entry) for entry in registry]
    existing_ids = {entry["claim_id"] for entry in candidate}
    added = 0
    updated = 0
    messages = []

    for entry in REGISTRY_ENTRIES:
        if entry["claim_id"] not in existing_ids:
            candidate.append(entry)
            existing_ids.add(entry["claim_id"])
            added += 1
            messages.append(f"+ Added: {entry['claim_id']}")
        else:
            for i, existing in enumerate(candidate):
                if existing["claim_id"] == entry["claim_id"]:
                    if existing != entry:
                        candidate[i] = entry
                        updated += 1
                        messages.append(f"↺ Updated: {entry['claim_id']}")
                    else:
                        messages.append(f"↺ Already current: {entry['claim_id']}")
                    break

    return candidate, added, updated, messages


def run_ledger_closeout(update_registry: bool = True) -> dict:
    print("=" * 65)
    print("GCT Protocol Ledger Closeout")
    print("=" * 65)

    # ── Print Born Rule status
    print("\n  ── Born Rule Status ──")
    print(f"  Input tier:    {C_BORN_RULE_TIER2_STATUS['input_tier']}")
    print(f"  Closed tier:   {C_BORN_RULE_TIER2_STATUS['closed_tier']}")
    print(f"  Status:        {C_BORN_RULE_TIER2_STATUS['status']}")

    # ── Print HVP stance
    print("\n  ── HVP Resolution Stance ──")
    print(f"  GCT correction:    {C_HVP_STANCE_STATUS['gct_correction_value']}")
    print(f"  Experimental gap:  {C_HVP_STANCE_STATUS['experimental_gap']}")
    print(f"  Status:            {C_HVP_STANCE_STATUS['status']}")

    # ── Write combined report
    report = {
        "protocol":  "ledger_status",
        "C_BORN_RULE_TIER2_STATUS": C_BORN_RULE_TIER2_STATUS,
        "C_HVP_STANCE_STATUS": C_HVP_STANCE_STATUS,
        "pass":      True,
    }
    report_path = get_output_path("protocol_ledger_closeout_results.json")
    with open(report_path, "w") as fp:
        json.dump(report, fp, indent=2)
    print(f"\n  Report saved → {report_path}")

    registry = _load_claim_registry()
    candidate, added, updated, messages = _candidate_claim_registry(registry)

    if update_registry:
        print(f"\n  Updating claim_registry.json...")
        for message in messages:
            print(f"    {message}")
        with open(CLAIM_REGISTRY_PATH, "w") as f:
            json.dump(candidate, f, indent=4)
        print(f"  claim_registry.json updated ({added} new entries, {updated} updated entries).")
    else:
        print(f"\n  Asserting claim_registry.json is current (read-only)...")
        for message in messages:
            print(f"    {message}")
        if candidate != registry:
            raise SystemExit(
                "claim_registry.json is not current; rerun protocol_ledger_closeout.py "
                "without --assert-registry-current to apply the maintenance write."
            )
        print("  claim_registry.json already current.")

    print("\n  ═══ VERDICT ═══")
    print("  Born Rule: Tier 3 conditional compatibility recorded; O.40a/O.40b proof not implemented.")
    print("  HVP Stance: CLOSED — formalised.")

    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Record ledger closeout status and maintain claim_registry.json.")
    parser.add_argument(
        "--assert-registry-current",
        action="store_true",
        help="Run read-only and fail if claim_registry.json would be changed.",
    )
    args = parser.parse_args()
    run_ledger_closeout(update_registry=not args.assert_registry_current)
