"""
run_all.py — Master harness for the independent App PSC verification stack.

Runs every verify_*.py in this directory, aggregates the per-claim JSON
results, and writes a master scorecard at results/scorecard.json plus a
human-readable summary to stdout.

Discrepancy reporting:
    Any discrepancy between App PSC and the engine outputs is reported, not
    suppressed.

PASS criteria:
    - EMPIRICAL_ANCHOR: independent re-derivation lies inside the declared
      empirical gate.
    - MANUSCRIPT_STATED: arithmetic reproduces the printed manuscript value
      and is reported separately as INTERNAL_ARITHMETIC_PASS.
    - PURE_MATHEMATICAL: the identity is reported separately as TIER1_EXACT
      or INTERNAL_ARITHMETIC_PASS.
    - When App PSC quotes a precision, the independent precision is within
      10% of it (otherwise a discrepancy note is auto-attached).

Exit code: 0 if all PASS / TIER1_EXACT / TENSION / OPEN_CONDITIONAL /
OPEN_RESEARCH / PENDING-α-RESOLUTION; nonzero if any unexpected FAIL. Registered
terminal-closure FAIL rows remain adverse scorecard facts but do not abort
the refresh pipeline.
"""

import sys
import io
import json
import importlib.util
import math
import os
import tempfile
from pathlib import Path

# Force UTF-8 on Windows stdout so box-drawing/Greek/math symbols don't crash.
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT))

# Order matters only for printing; results are aggregated independently.
SCRIPTS = [
    "verify_electron_mass",
    "verify_hypercharges",
    "verify_n144",
    "verify_stiffness_ratio",
    "verify_healing_length",
    "verify_muon_mass",
    "verify_tau_mass",
    "verify_alpha",
    "verify_weinberg",
    "verify_cabibbo",
    "verify_newton_g",
    "verify_higgs_vev",
    "verify_higgs_mass",
    "verify_g2_muon",
    "verify_g2_electron",
    "verify_proton_mass",
    "verify_quarks",
    "verify_p13c_nmr_polarity",
    "verify_ckm",
    "verify_mixing_unitarity",
    "verify_jarlskog",
    "verify_strong_cp",
    "verify_pmns",
    "verify_neutrino",
    "verify_dm_line_centroid_postdiction_check",
    "verify_dm_line_width_morphology",
    "verify_fbio_jacobian",
    "verify_fbound",
    "verify_protocol_d_mc_systematics",
    "verify_nu_zeno",
    "verify_chi_holographic",
    "verify_phantom_crossing",
    "verify_alpha_s_bare",
    "verify_E_amplitudes",
    # "check_imp01_pipeline" lives under self_consistency/ (NOT here); it
    # imports the biogenic DE pipeline protocol it checks and therefore does not meet the
    # independent-re-derivation contract of this harness. Run it separately
    # via: python GCT_Physics_Engine/verify_independent/self_consistency/check_imp01_pipeline.py
    "verify_anti_zeno_upper_crossover",
    "verify_pta_l6_invariant",
    "verify_epsilon_y",
    "verify_ch20_liv_and_rm",
    "verify_alpha_bilayer",
]


def run_script(name: str) -> list:
    """Execute a verify_*.py as a module and collect its results dicts."""
    mod_path = ROOT / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, mod_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    out = mod.main()
    if isinstance(out, list):
        return out
    return [out]


def status_bucket(status: str) -> str:
    if status in ("PASS", "TIER1_EXACT", "INTERNAL_ARITHMETIC_PASS"):
        return "ok"
    if status in ("TENSION", "OPEN_CONDITIONAL", "OPEN_RESEARCH", "PENDING-α-RESOLUTION"):
        return "tension"
    return "fail"


def _expected_registered_fail_names() -> set[str]:
    """Verifier result names whose FAIL status is explicitly registered."""
    registry_path = ROOT.parent / "falsifiability_registry.json"
    try:
        with open(registry_path, encoding="utf-8") as f:
            registry = json.load(f)
    except FileNotFoundError:
        return set()
    names: set[str] = set()
    for entry in registry.get("entries", []):
        if not entry.get("registered_terminal_closure_state"):
            continue
        if not entry.get("band_violation_disclosure"):
            continue
        raw = str(entry.get("verifier_name") or "")
        if not raw:
            continue
        stem = Path(raw.split("::", 1)[0]).stem
        for key in (raw, stem, stem.removeprefix("verify_")):
            if key:
                names.add(key)
    return names


def _fmt(v, width):
    if v is None:
        return f"{'-':>{width}}"
    if isinstance(v, float) and abs(v) < 1e-3:
        return f"{v:>{width}.4g}"
    return f"{v:>{width}.6g}" if isinstance(v, (int, float)) else f"{str(v):>{width}}"


def _json_safe(value):
    """Replace NaN/Inf values before writing strict JSON artifacts."""
    if isinstance(value, dict):
        return {k: _json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_json_safe(v) for v in value]
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def main():
    print("\n" + "#" * 72)
    print("# GCT App PSC - INDEPENDENT VERIFICATION HARNESS")
    print("# Separates external-anchor comparisons, manuscript-stated")
    print("# arithmetic checks, and pure mathematical identities.")
    print("#" * 72 + "\n")

    # Verifiers write into a new isolated directory. Aggregation consumes only
    # objects returned by this invocation, so stale/excluded JSON files in the
    # committed results directory cannot enter the scorecard.
    returned_items: list[dict] = []
    with tempfile.TemporaryDirectory(prefix="gct-independent-") as isolated:
        os.environ["GCT_VERIFY_RESULTS_DIR"] = isolated
        for name in SCRIPTS:
            print(f"\n-- Running {name} --")
            try:
                run_script(name)
            except Exception as e:
                print(f"  [ERROR] {name} raised: {type(e).__name__}: {e}")
                returned_items.append(
                    {
                        "name": name,
                        "status": "FAIL",
                        "reference_class": "UNCLASSIFIED",
                        "band_outcome": "NOT_EVALUATED",
                        "derivational_closure": "NOT_EVALUATED",
                        "error": str(e),
                        "error_type": type(e).__name__,
                    }
                )
        for path in sorted(Path(isolated).glob("*.json")):
            with path.open(encoding="utf-8") as f:
                returned_items.append(json.load(f))

    by_name: dict[str, dict] = {}
    for item in returned_items:
        name = item.get("name")
        if not name:
            raise ValueError("verifier returned an item without a name")
        if name in by_name:
            raise ValueError(f"duplicate verifier result name: {name}")
        by_name[name] = item
    items = [by_name[name] for name in sorted(by_name)]
    if len(items) != 54:
        raise ValueError(f"expected 54 verifier results from this run; got {len(items)}")
    unclassified = [it["name"] for it in items if it.get("reference_class") == "UNCLASSIFIED"]
    if unclassified:
        raise ValueError(f"unclassified verifier results: {unclassified}")

    # Publish only the 54 fresh canonical results. Excluded artifacts may
    # remain on disk for their own self-consistency harness, but are never
    # globbed into this scorecard.
    for item in items:
        with open(RESULTS_DIR / f"{item['name']}.json", "w", encoding="utf-8") as f:
            json.dump(_json_safe(item), f, indent=2, allow_nan=False)

    ok = [it for it in items if status_bucket(it["status"]) == "ok"]
    not_yet_closed = [it for it in items if status_bucket(it["status"]) == "tension"]
    tensions = [it for it in items if it["status"] == "TENSION"]
    open_conditional = [it for it in items if it["status"] == "OPEN_CONDITIONAL"]
    open_research = [it for it in items if it["status"] == "OPEN_RESEARCH"]
    pending_alpha = [it for it in items if it["status"] == "PENDING-α-RESOLUTION"]
    fail = [it for it in items if status_bucket(it["status"]) == "fail"]
    expected_fail_names = _expected_registered_fail_names()
    unexpected_fail = [it for it in fail if it.get("name") not in expected_fail_names]
    discrepancies = [it for it in items if it.get("discrepancy_notes")]
    reference_counts = {
        key: sum(1 for it in items if it.get("reference_class") == key)
        for key in ("EMPIRICAL_ANCHOR", "MANUSCRIPT_STATED", "PURE_MATHEMATICAL")
    }
    pass_empirical = sum(
        1 for it in items
        if it.get("reference_class") == "EMPIRICAL_ANCHOR"
        and it.get("status") == "PASS"
    )
    pass_internal_arithmetic = sum(
        1 for it in items if it.get("status") == "INTERNAL_ARITHMETIC_PASS"
    )
    pass_pure_mathematical = sum(
        1 for it in items if it.get("status") == "TIER1_EXACT"
    )

    print("\n" + "=" * 72)
    print("  MASTER SCORECARD - INDEPENDENT VERIFICATION RESULTS")
    print("=" * 72)
    print(f"  Total claims verified : {len(items)}")
    print(f"  Empirical-anchor PASS : {pass_empirical}")
    print(f"  Internal arithmetic   : {pass_internal_arithmetic}")
    print(f"  Tier-1 exact          : {pass_pure_mathematical}")
    print(f"  TENSION               : {len(tensions)}")
    print(f"  OPEN_CONDITIONAL      : {len(open_conditional)}")
    print(f"  OPEN_RESEARCH         : {len(open_research)}")
    print(f"  PENDING-alpha         : {len(pending_alpha)}")
    print(f"  Not yet closed (sum)  : {len(not_yet_closed)}")
    print(f"  FAIL                  : {len(fail)}")
    print(f"  Registered FAIL       : {len(fail) - len(unexpected_fail)}")
    print(f"  Unexpected FAIL       : {len(unexpected_fail)}")
    print(f"  With discrepancy notes: {len(discrepancies)}")
    print("=" * 72)

    print("\nPER-CLAIM TABLE:")
    print(
        f"  {'Name':<24}{'Independent':>14}{'Observed':>14}{'ppm':>10}"
        f"{'App PSC ppm':>12}  Status"
    )
    print("  " + "-" * 86)
    for it in items:
        ind_ppm = it.get("independent_precision_ppm")
        app_psc_ppm = it.get("app_psc_precision_ppm")
        pred = it.get("predicted")
        obs = it.get("observed")
        line = (
            f"  {it['name']:<24}"
            f"{_fmt(pred, 14)}{_fmt(obs, 14)}"
            f"{_fmt(ind_ppm, 10)}{_fmt(app_psc_ppm, 12)}  {it['status']}"
        )
        print(line)

    if discrepancies:
        print("\n" + "=" * 72)
        print("  DISCREPANCIES FLAGGED")
        print("=" * 72)
        for it in discrepancies:
            print(f"\n  [{it['name']}]")
            for note in it["discrepancy_notes"]:
                print(f"    - {note}")

    scorecard = {
        "summary": {
            "total": len(items),
            "pass_or_tier1": len(ok),
            "pass_empirical": pass_empirical,
            "pass_internal_arithmetic": pass_internal_arithmetic,
            "pass_pure_mathematical": pass_pure_mathematical,
            "reference_class_counts": reference_counts,
            "not_yet_closed": len(not_yet_closed),
            "tension": len(tensions),
            "open_conditional": len(open_conditional),
            "open_research": len(open_research),
            "pending_alpha_resolution": len(pending_alpha),
            "fail": len(fail),
            "registered_fail": len(fail) - len(unexpected_fail),
            "unexpected_fail": len(unexpected_fail),
            "discrepancies_count": len(discrepancies),
        },
        "items": items,
    }
    with open(RESULTS_DIR / "scorecard.json", "w", encoding="utf-8") as f:
        json.dump(_json_safe(scorecard), f, indent=2, allow_nan=False)
    print(f"\nScorecard written to {RESULTS_DIR / 'scorecard.json'}")

    return 0 if not unexpected_fail else 1


if __name__ == "__main__":
    sys.exit(main())
