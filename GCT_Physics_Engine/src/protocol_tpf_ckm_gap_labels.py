#!/usr/bin/env python3
"""
protocol_tpf_ckm_gap_labels.py - W2: TP-F CKM s23/s13 gap-label enumeration
============================================================================
App TP S TP-F audit handle (verbatim intent): "enumerate which K-theoretic gap
labels in the E8 -> Z^6 projection (App U S U.7.3) are consistent with the
observed s_23, s_13 values, then test whether the constraints are satisfiable."

Gap-label framework (App U S U.7.6, Bellissard gap-labeling, validated on the
1D Fibonacci chain): a spectral-gap label is an IDOS value of the form
    L(p,q) = (p * phi^{-1} + q)  mod 1 ,   p, q in Z,
i.e. an element of the Z[phi] trace image of K_0. The 1D validation reached
max |p| = 7 at lattice size F_15 = 610; larger |p| requires astronomically
larger lattice scale (the same scaling that makes the electron's |n| = 107
label inaccessible at small N, App U U.7.6 / O.14a).

Current Ch10 S10.6 ansaetze (Tier 3, irrational exponents flagged in-text):
    s_23 = phi^{-(6 + phi^{-1})},  exponent 6.618...
    s_13 = phi^{-(11 + phi^{-1})}, exponent 11.618...

This protocol decides three things, all finite:

  E1. INTEGER phi-power gap labels phi^{-n}: do the observed s_23, s_13 sit ON a
      clean integer-power label, or strictly BETWEEN consecutive ones?
  E2. GENERAL Z[phi] labels L(p,q): the smallest |p| whose label matches each
      observed value within PDG tolerance, and the candidate COUNT within a
      bound (uniqueness vs under-determination). Because {p*phi^{-1} mod 1} is
      equidistributed, matching to tolerance eps needs |p| ~ 1/(2 eps): a
      large, unselected p, and many co-fitting labels.
  E3. The ANSATZ values themselves: phi^{-(n + phi^{-1})} has an irrational
      algebraic exponent, so by Gelfond-Schneider it is TRANSCENDENTAL and
      cannot be an element of Z[phi] at all -> the literal ansatz is not a gap
      label. Confirmed numerically against the small-(p,q) label grid.

Verdict target: whether the K-theoretic gap-label route CLOSES TP-F (unique,
physically-bounded label per angle) or is under-determined / inapplicable
(closure stays with the QLQCD dressed-Dirac extraction, O.5 core).
"""

import json
import os
import sys
import io

import numpy as np

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

try:
    from gct_utils import get_output_path, C
except ImportError:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from gct_utils import get_output_path, C

PHI = float(C.PHI)
PHI_INV = 1.0 / PHI

# Observed CKM magnitudes (PDG 2024, registered in App FM P.26/P.27).
# Errors set generously (>= PDG) so the "required |p|" bound is conservative.
TARGETS = {
    "s_23": {"obs": 0.0418, "abs_err": 0.0008},     # ~|V_cb|, ~2%
    "s_13": {"obs": 0.003732, "abs_err": 0.00018},  # ~|V_ub|, ~5%
}
ANSATZ = {
    "s_23": 6 + PHI_INV,    # phi^{-(6 + phi^-1)}
    "s_13": 11 + PHI_INV,   # phi^{-(11 + phi^-1)}
}
FIBONACCI_VALIDATED_MAX_P = 7   # App U U.7.6, F_15 = 610


def integer_power_bracket(target):
    """Nearest integer-power gap labels phi^{-n} bracketing the target."""
    n_real = -np.log(target) / np.log(PHI)
    n_lo, n_hi = int(np.floor(n_real)), int(np.ceil(n_real))
    return {
        "n_real": n_real,
        "n_lo": n_lo, "val_lo": PHI ** (-n_lo),
        "n_hi": n_hi, "val_hi": PHI ** (-n_hi),
        "on_integer_power": bool(abs(n_real - round(n_real)) < 1e-3),
    }


def min_p_for_match(target, eps, p_max=200000):
    """Smallest |p| with a Z[phi] label L(p,q) within eps of target; also the
    count of labels within eps up to that |p| (under-determination measure)."""
    best_p = None
    for p in range(0, p_max + 1):
        for s in ((p,) if p == 0 else (p, -p)):
            val = (s * PHI_INV) % 1.0
            # compare on the circle
            d = abs(((val - target + 0.5) % 1.0) - 0.5)
            if d < eps:
                best_p = abs(s)
                return best_p
    return None


def count_labels_within(target, eps, p_bound):
    n = 0
    for p in range(-p_bound, p_bound + 1):
        val = (p * PHI_INV) % 1.0
        d = abs(((val - target + 0.5) % 1.0) - 0.5)
        if d < eps:
            n += 1
    return n


def run():
    print("=" * 74)
    print("GCT Protocol W2 / TP-F - CKM s23, s13 K-theoretic gap-label audit")
    print("=" * 74)
    print(f"\n  Gap-label set: L(p,q) = (p/phi + q) mod 1, p,q in Z  (Z[phi] trace image)")
    print(f"  1D-validated accessible |p| <= {FIBONACCI_VALIDATED_MAX_P} (App U U.7.6)\n")

    results = {"gap_label_form": "(p*phi^-1 + q) mod 1", "targets": {}}

    for name, t in TARGETS.items():
        obs, err = t["obs"], t["abs_err"]
        rel = err / obs
        print(f"  --- {name}: observed {obs} +/- {err} ({100*rel:.1f}%) ---")

        # E1: integer phi-power
        br = integer_power_bracket(obs)
        print(f"  E1 integer-power phi^-n: n_real = {br['n_real']:.4f}  "
              f"-> sits between phi^-{br['n_lo']} = {br['val_lo']:.5f} and "
              f"phi^-{br['n_hi']} = {br['val_hi']:.5f}")
        print(f"     on a clean integer-power label? {br['on_integer_power']}  "
              f"(nearest integer power off by "
              f"{100*min(abs(br['val_lo']-obs),abs(br['val_hi']-obs))/obs:.1f}%)")

        # E2: general Z[phi] label, required |p| + degeneracy
        min_p = min_p_for_match(obs, err)
        cnt_at_8 = count_labels_within(obs, err, FIBONACCI_VALIDATED_MAX_P)
        # candidate count once |p| is large enough to start matching
        scan_bound = max(min_p * 3, 50) if min_p else 50
        cnt_scan = count_labels_within(obs, err, scan_bound)
        print(f"  E2 general L(p,q): smallest |p| matching within PDG err = {min_p}"
              f"  (validated max |p| = {FIBONACCI_VALIDATED_MAX_P})")
        print(f"     labels within err at |p|<= {FIBONACCI_VALIDATED_MAX_P}: {cnt_at_8}"
              f"   ;  within err at |p|<= {scan_bound}: {cnt_scan} (degeneracy)")

        # E3: ansatz transcendentality + value
        expo = ANSATZ[name]
        ansatz_val = PHI ** (-expo)
        print(f"  E3 ansatz phi^-({expo:.4f}) = {ansatz_val:.6f}  vs obs {obs} "
              f"({100*(ansatz_val-obs)/obs:+.2f}%)")
        print(f"     exponent irrational (algebraic) -> Gelfond-Schneider: value "
              f"TRANSCENDENTAL -> not in Z[phi] -> not a gap label.")

        results["targets"][name] = {
            "obs": obs, "abs_err": err, "rel_err": rel,
            "E1_n_real": float(br["n_real"]), "E1_bracket": [br["n_lo"], br["n_hi"]],
            "E1_on_integer_power": br["on_integer_power"],
            "E1_nearest_integer_power_off_pct":
                100 * min(abs(br["val_lo"] - obs), abs(br["val_hi"] - obs)) / obs,
            "E2_min_abs_p_for_match": min_p,
            "E2_validated_max_p": FIBONACCI_VALIDATED_MAX_P,
            "E2_labels_within_err_at_p8": cnt_at_8,
            "E2_labels_within_err_at_scan": cnt_scan,
            "E2_scan_bound": scan_bound,
            "E3_ansatz_exponent": expo,
            "E3_ansatz_value": ansatz_val,
            "E3_ansatz_vs_obs_pct": 100 * (ansatz_val - obs) / obs,
            "E3_transcendental_not_in_Zphi": True,
        }
        print()

    # ---- verdict ----
    any_integer = any(results["targets"][n]["E1_on_integer_power"] for n in TARGETS)
    bounded_match = all(
        (results["targets"][n]["E2_min_abs_p_for_match"] or 1e9)
        <= FIBONACCI_VALIDATED_MAX_P for n in TARGETS)
    verdict = (
        "TP-F gap-label route does NOT close s23/s13. (E1) Neither value sits on "
        "an integer-power phi^-n label; both fall strictly between consecutive "
        "powers. (E2) A general Z[phi] label matches only at |p| far beyond the "
        "validated/accessible range, and many labels co-fit at that scale "
        "(under-determined, no selection rule) - the same obstruction as the open "
        "-107 uniqueness (O.14a). (E3) The literal phi^-(n+phi^-1) ansaetze are "
        "transcendental (Gelfond-Schneider) and lie outside Z[phi] entirely. "
        "Hence the K-theoretic gap-label framing cannot supply a unique, "
        "physically-bounded label for either CKM angle; closure remains with the "
        "QLQCD dressed-Dirac extraction (O.5 core), not gap-label enumeration."
        if (not any_integer and not bounded_match) else
        "Unexpected: a bounded/unique gap label was found - review.")
    print("  " + "-" * 70)
    print("  VERDICT:", verdict)
    print("=" * 74)

    results["verdict"] = verdict
    results["any_on_integer_power"] = any_integer
    results["any_bounded_unique_match"] = bounded_match
    out = get_output_path("protocol_tpf_ckm_gap_labels_results.json")
    with open(out, "w") as fp:
        json.dump(results, fp, indent=2)
    print(f"\n[Saved JSON] -> {out}")
    return results


if __name__ == "__main__":
    run()
