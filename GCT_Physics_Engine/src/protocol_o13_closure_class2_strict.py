#!/usr/bin/env python3
"""
protocol_o13_closure_class2_strict.py
=====================================

Conditional Class-2 allocation diagnostic for Open Problem O.13 via the
Tier-3 modeling assumptions in V2 Ch14 Secs 14.5.2 and 14.6.2.

    "The relevant driver is not the formation of stars (Class 0), but
    the emergence of High-Order Selection Operators (Class 2 Agents).
    Biological complexity requires billions of years of stable evolution
    *after* star formation to achieve high informational density."

The protocol assigns the biogenic-channel weight to the stipulated Class-2
population and assigns zero *model weight* below the threshold. This is a
Tier-3 allocation convention, not a physical inference: the DMC/eta_Zeno
gate is not action-closed, and no audited
substrate has a derived Identity-Polaron or Level-II verdict.

CONSEQUENCES FOR THE VARIANT FAMILY

V1 (sigmoid x exp at t_origin = 9 Gyr cosmic time):
    Empirically calibrated; t_origin lies near the cosmic time at which
    Earth-template biospheres reach the Class 2 threshold
    (t_first_formation ~ 2 Gyr + tau_intel = 4.5 Gyr -> ~ 6.5 Gyr; the
    9 Gyr calibration also absorbs the lag-kernel + tau_bio convolution).
    It is Class-2-compatible as an empirical envelope, but t_origin is a
    Tier 3 calibrated timing parameter rather than a Class-2 derivation.

V2 (stage-hierarchy with weights 1, 100, 1e5, 1e8 at biosphere ages
0.5, 2.4, 3.7, 4.5 Gyr):
    Assigns NONZERO weight to LUCA, eukaryotic, and multicellular
    stages -- all below the allocation threshold. The intelligent-stage
    weight (1e8) dominates numerically by ~3 orders of magnitude, but the
    pre-Class-2 floors differ from the registered Sec 14.5.2 allocation. The
    numerical |Delta w(z=0.28)| ~ 2e-3 reflects an ANSATZ that goes
    beyond what the Sec 14.5.2 prose entails.

V6 (Class-2-strict): P_evolve(tau) = 0 for tau < tau_intel,
P_evolve(tau) = 1 for tau >= tau_intel, where tau is biosphere age.
This implements the Tier-3 model allocation in Sec 14.5.2.

V6r (conditional Class-2 allocation with full SFR-age convolution):
    P_evolve(t_cosmic) = int_{tau_intel}^{age_today} SFR(t_cosmic - tau_bio - tau)
    d(tau)
where tau is biosphere age and the integral is the SFR-weighted count
of intelligent-stage biospheres at cosmic time t_cosmic. This refines
V6 by accounting for the biosphere age-distribution at each cosmic time.

NUMERICAL DELIVERABLE

For each variant, compute |Delta w(z=0.28)| from the biogenic DE pipeline.
The conditional O.13 diagnostic records:
    - V6 / V6r implement the registered Tier-3 Class-2 allocation
    - V1 is a single-channel empirical comparison
    - V2 lies outside the registered allocation (alternative; reported only)

The V1-V6-V6r envelope is a diagnostic only, not a registered prediction
range. The registered conditional O.13 template envelope is delegated to
protocol_o13_intra_class2_dynamics.py.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit

ENGINE_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = ENGINE_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))


def _short_sci(x: float) -> str:
    mantissa, exponent = f"{x:.2e}".split("e")
    return f"{mantissa}e{int(exponent)}"


def _intra_class2_v7_band() -> str:
    """Read the V7' Kardashev-band envelope from the intra-Class-2 run."""
    path = ENGINE_ROOT / "data" / "protocol_o13_intra_class2_dynamics_results.json"
    try:
        lo, hi = json.loads(path.read_text(encoding="utf-8"))["kardashev_band_envelope_dw_z028"]
        return f"[{_short_sci(lo)}, {_short_sci(hi)}]"
    except (OSError, KeyError, ValueError, TypeError):
        return "(see protocol_o13_intra_class2_dynamics.py)"

# Reuse biogenic DE infrastructure
from protocol_imp01_pipeline import (
    age_at_z, sfr_at_time, ALPHA, TAU_LAG_GYR, TAU_BIO_GYR,
    W0_TARGET, DELTA_W_TARGET, cpl,
)
from protocol_p_evolve_first_principles import (
    p_evolve_V1_sigmoid_exp,
    p_evolve_V2_stage_hierarchy,
    i_dot_for_variant,
    p_info_for_variant,
    w_of_z_for_variant,
    fit_cpl,
    run_variant,
)

# Tier 3 calibrated anchor [Ledger C3/O.13]: Class-2 threshold biosphere age
# from the Earth-template intelligent-emergence timescale.
TAU_INTEL_GYR = 4.5


def p_evolve_V6_class2_strict(t_gyr: np.ndarray,
                               tau_intel: float = TAU_INTEL_GYR) -> np.ndarray:
    """V6: strict Class-2 step function.

    P_evolve(t) = 0   for t < tau_intel  (zero assigned model weight)
    P_evolve(t) = 1   for t >= tau_intel  (intelligent stage, constant amplitude)

    The argument t here is interpreted as biosphere age in the integration
    inherited from the conditional biogenic-DE model; with the
    integration convention of t = cosmic time and t_anchor = 0, this is
    equivalent to t = biosphere age for biospheres that formed at cosmic
    time 0. The cosmic-mean P_evolve(t_cosmic) is the cumulative-stage
    indicator. For full SFR-age convolution see V6r.
    """
    t = np.atleast_1d(t_gyr).astype(np.float64)
    pe = np.where(t < tau_intel, 0.0, 1.0)
    return pe if pe.ndim == t_gyr.ndim else pe[0]


def p_evolve_V6r_class2_sfr_convolved(t_cosmic_gyr: np.ndarray,
                                       age_today_gyr: float,
                                       tau_intel: float = TAU_INTEL_GYR
                                       ) -> np.ndarray:
    """V6r: conditional Class-2 allocation with full SFR-age convolution.

    At cosmic time t_cosmic, the density of INTELLIGENT biospheres is:
        n_intel(t_cosmic) = int_{tau_intel}^{age_today} SFR(t_cosmic - tau_bio - tau) d(tau)
    where:
      - tau is biosphere age
      - tau_intel is the age threshold for Class 2 emergence (~4.5 Gyr)
      - tau_bio is the standard biological delay (~4.5 Gyr, biogenic DE pipeline)
      - the SFR is evaluated at the biosphere FORMATION time
        (= t_cosmic - tau_bio - tau)

    Biospheres of age 0 to tau_intel receive zero weight in this model.
    Biospheres of age >= tau_intel contribute at unit weight; the integral
    sums the SFR-rate at the formation times of all currently-intelligent
    biospheres.

    P_evolve = n_intel(t_cosmic) is the registered conditional driver.
    """
    t = np.atleast_1d(t_cosmic_gyr).astype(np.float64)
    pe = np.zeros_like(t)
    for i, tc in enumerate(t):
        # tau ranges from tau_intel to age_today (biosphere age)
        # Note: t_form = tc - tau_bio - tau must be >= 0
        tau_max = tc - TAU_BIO_GYR
        if tau_max <= tau_intel:
            pe[i] = 0.0
            continue
        # Numerical integration grid for the SFR-age convolution; not a
        # physical calibration constant.
        tau_grid = np.linspace(tau_intel, tau_max, 400)
        t_form = tc - TAU_BIO_GYR - tau_grid
        # Clip to physical range
        t_form = np.maximum(t_form, 0.001)
        sfr_vals = sfr_at_time(t_form, age_today_gyr)
        pe[i] = np.trapz(sfr_vals, tau_grid)
    return pe if pe.ndim == t_cosmic_gyr.ndim else pe[0]


def run_variant_with_age_today(label, p_evolve_fn) -> dict:
    """Same as run_variant but explicitly threads age_today for V6r
    which needs it inside the P_evolve evaluation."""
    return run_variant(label, p_evolve_fn)


def main():
    print("=" * 76)
    print("O.13 DIAGNOSTIC: conditional Class-2 allocation (Tier 3)")
    print("=" * 76)

    _, age_today = age_at_z(np.array([0.0]))

    # Wrap V6r to bind age_today
    def p_evolve_V6r_bound(t):
        return p_evolve_V6r_class2_sfr_convolved(t, age_today)

    variants = [
        ("V1 sigmoid x exp (single-channel pipeline)", p_evolve_V1_sigmoid_exp),
        ("V2 stage-hierarchy (outside registered Class-2 allocation)",
            p_evolve_V2_stage_hierarchy),
        ("V6 Class-2 allocation step (Tier 3 premise)", p_evolve_V6_class2_strict),
        ("V6r Class-2 allocation + SFR-age convolution", p_evolve_V6r_bound),
    ]

    results = []
    for label, fn in variants:
        print(f"\n--- Running {label} ---")
        r = run_variant(label, fn)
        results.append(r)
        print(f"  w(z=0)    = {r['w_at_z_0']:+.5f}")
        print(f"  w(z=0.28) = {r['w_at_z_028']:+.5f}")
        print(f"  w(z=0.5)  = {r['w_at_z_05']:+.5f}")

    print("\n" + "=" * 76)
    print("CONDITIONAL-ALLOCATION ANALYSIS")
    print("=" * 76)
    print(f"  {'variant':<60}  {'w(z=.28)':>10}  {'|Dw(z=.28)|':>12}")
    for r in results:
        dw_028 = abs(r['w_at_z_028'] - (-1.0))
        print(f"  {r['label']:<60}  {r['w_at_z_028']:>+10.5f}  {dw_028:>12.5e}")

    # Extract the relevant numbers
    w028 = {r["label"].split()[0]: abs(r["w_at_z_028"] - (-1.0)) for r in results}
    v1 = w028["V1"]
    v2 = w028["V2"]
    v6 = w028["V6"]
    v6r = w028["V6r"]

    print(f"\n  V1 (single-channel pipeline) |Dw(z=0.28)| = {v1:.3e}")
    print(f"  V2 (outside registered allocation) |Dw(z=0.28)| = {v2:.3e}  [alternative]")
    print(f"  V6 (Class-2-strict)      |Dw(z=0.28)| = {v6:.3e}")
    print(f"  V6r (Class-2 + SFR conv) |Dw(z=0.28)| = {v6r:.3e}")

    # Diagnostic envelope (V1, V6, V6r); not the
    # registered conditional O.13 template after intra-Class-2 weighting.
    class2_consistent = [v1, v6, v6r]
    class2_min = min(class2_consistent)
    class2_max = max(class2_consistent)
    class2_geometric_mean = float(np.exp(np.mean(np.log(class2_consistent))))
    registered_min = 2.0e-5
    registered_max = 5.0e-5
    registered_geometric_mean = float(np.sqrt(registered_min * registered_max))

    print(f"\n  Diagnostic V1/V6/V6r envelope (not registered amplitude):")
    print(f"    min:            {class2_min:.3e}")
    print(f"    max:            {class2_max:.3e}")
    print(f"    geometric mean: {class2_geometric_mean:.3e}")
    print(f"    spread (max/min): {class2_max/class2_min:.2f}x")
    print(f"\n  Registered Class-2 + intra-Class-2 envelope delegated to")
    print(f"  protocol_o13_intra_class2_dynamics.py:")
    print(f"    |Delta w(z=0.28)| in [{registered_min:.2e}, {registered_max:.2e}]")

    print(f"\n  V2 is {v2/class2_geometric_mean:.1f}x the registered-allocation geometric mean")
    print(f"  V2 / V6 ratio: {v2/v6:.2f}")

    # Verdict
    print(f"\n" + "=" * 76)
    print("VERDICT FOR O.13")
    print("=" * 76)
    print(f"  MODEL ALLOCATION (Sec 14.5.2, Tier 3): the registered kernel assigns")
    print(f"  biogenic-channel weight only to the stipulated Class-2 population.")
    print(f"  Zero pre-Class-2 weight is bookkeeping, not a substrate verdict.")
    print(f"  DMC/eta_Zeno is not action-closed; Level II is NOT_EVALUATED (open, Tier 3): no validated substrate criterion yet.")
    print(f"")
    print(f"  V2 stage-hierarchy assigns non-zero weights to pre-Class 2 stages,")
    print(f"  so it is retained as an alternative reference outside this allocation.")
    print(f"")
    print(f"  V6 and V6r implement the allocation; V1 is retained only as")
    print(f"  a diagnostic broad-reference ansatz, not as the registered amplitude.")
    print(f"")
    print(f"  The registered conditional O.13 envelope is delegated to the intra-Class-2")
    print(f"  Kardashev-band protocol:")
    print(f"  |Delta w(z=0.28)| in [{registered_min:.2e}, {registered_max:.2e}]")
    print(f"  with geometric mean {registered_geometric_mean:.2e}.")
    print(f"  V2's 2e-3 value is above the registered conditional envelope.")
    print("=" * 76)

    summary = {
        "tau_intel_gyr": TAU_INTEL_GYR,
        "tau_bio_gyr": TAU_BIO_GYR,
        "tau_lag_gyr": TAU_LAG_GYR,
        "variants_run": results,
        "delta_w_z028_by_variant": {
            "V1_sigmoid_exp": v1,
            "V2_stage_hierarchy_violates_Class2": v2,
            "V6_Class2_strict_step": v6,
            "V6r_Class2_SFR_convolved": v6r,
        },
        "diagnostic_v1_v6_v6r_envelope_not_registered": {
            "min": float(class2_min),
            "max": float(class2_max),
            "geometric_mean": float(class2_geometric_mean),
            "spread_max_over_min": float(class2_max / class2_min),
        },
        "registered_class2_intra_dynamics_envelope": {
            "min": registered_min,
            "max": registered_max,
            "geometric_mean": registered_geometric_mean,
            "source": "protocol_o13_intra_class2_dynamics.py",
            "status": "registered conditional O.13 template envelope; V1/V6/V6r envelope is diagnostic only",
            "disclosure": (
                "Declared band, kept as registered (not re-registered after seeing runs). "
                f"Current runs do not reproduce its edges: V6r gives {v6r:.3g} and the intra-Class-2 "
                f"Kardashev-band V7' runs give {_intra_class2_v7_band()} (protocol_o13_intra_class2_dynamics.py)."
            ),
        },
        "V2_relative_to_class2_envelope": {
            "V2_over_geometric_mean": float(v2 / class2_geometric_mean),
            "V2_over_V6": float(v2 / v6),
        },
        "conditional_scope": (
            "No Tier-2 closure is claimed. Sec 14.5.2 defines "
            "a Tier-3 Class-2 allocation; zero pre-Class-2 weight is bookkeeping, "
            "not an Identity-Polaron, Level-II, or physical-coupling verdict. "
            "The DMC/eta_Zeno gate is action-open. The "
            "V1/V6/V6r span is retained as a "
            "diagnostic broad-reference envelope only. The registered conditional "
            "Class-2 + intra-Class-2 O.13 template envelope is delegated to "
            "protocol_o13_intra_class2_dynamics.py and is |Delta w(z=0.28)| in "
            f"[{registered_min:.2e}, {registered_max:.2e}] conditional on the "
            "allocation. V2 remains an alternative reference outside it."
        ),
    }
    out_path = ENGINE_ROOT / "data" / "protocol_o13_closure_class2_strict_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nResults saved to: {out_path}")
    print("=" * 76)


if __name__ == "__main__":
    main()
