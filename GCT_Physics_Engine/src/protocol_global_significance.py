#!/usr/bin/env python3
"""
protocol_global_significance.py — GCT cross-base and lepton-grid diagnostics (WITHDRAWN)
====================================================================================
Both constructions in this protocol are recorded with status
WITHDRAWN_NON_INFORMATIVE and emit no sigma figure:

* The cross-base Monte Carlo cannot credit any base other than phi: the alpha
  condition 360 b^-2 (1 - 1/288) within 0.3% is satisfiable only for b in
  about [1.6156, 1.6204], which lies entirely inside the excluded window
  phi +/- 0.01, so no non-phi base can pass whatever the lepton or proton
  results. The protocol computes that interval and the containment explicitly.
* The expanded lepton grid evaluates phi only; its 21 ppm window equals the
  observed muon residual (post hoc), and its (C1, C2) grid is effectively a
  covering, so its grid-hit fraction is not a p-value.

Earlier global-significance figures are withdrawn. The preregistered constant
control test comparing phi against other constants under identical formula
freedom is not implemented here; it has reported separately: v3 is
NEGATIVE-FRAGILE (p0 = 0.196; 58 of 300 random bases do at least as well as
phi on 21 constants; non-confirmatory), so the phi-formula matches are Tier 4
as evidence (App PSC §PSC.9.6).

Algorithm:
----------
1. Define the four GCT target observables and their tolerances (from SSOT).
2. For each candidate base b in a dense sample of irrationals in [1.05, 4.0]:
   a. Search over integer exponents N ∈ [1, 30] for m_mu/m_e match.
   b. Search over integer exponents N ∈ [1, 30] for m_tau/m_e match.
   c. Search over expressions b^N and b^{N+b^{-1}} for m_p/m_e match.
   d. Search over expressions 360*b^{-2}*(1 - 1/288) for alpha^{-1} match.
   e. Record whether the base b achieves SIMULTANEOUS match on all four.
3. Compute the fraction of random bases that hit all four simultaneously.
4. (Removed: no comparison with a random-numerology fraction is made.)
5. Record why the construction is non-informative (alpha-window containment);
   no p-value or sigma is reported.

The registered verdict is an expected non-pass with status
WITHDRAWN_NON_INFORMATIVE. verify_engine.py checks that the withdrawn status,
the alpha-window containment and the absence of any sigma field are stable.

Output:
-------
  data/protocol_global_significance_results.json
"""

import json
import math
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from gct_utils import PHI, get_output_path, C, resolve_a3

# ===========================================================================
# TARGETS AND TOLERANCES (from SSOT)
# ===========================================================================

M_ELECTRON_MEV     = 0.51099895069  # CODATA 2022
M_MU_OBS_MEV       = 105.6583755    # CODATA 2022
M_TAU_OBS_MEV      = 1776.93  # PDG 2024 (BES-III + Belle II)
M_PROTON_MEV       = 938.27208816
ALPHA, ALPHA_INV_OBS = resolve_a3(C)

RATIO_MU_E    = M_MU_OBS_MEV  / M_ELECTRON_MEV   # 206.7683
RATIO_TAU_E   = M_TAU_OBS_MEV / M_ELECTRON_MEV   # 3477.36 (PDG 2024)
RATIO_P_E     = M_PROTON_MEV  / M_ELECTRON_MEV   # 1836.15

# Match tolerances (generous: tree-level geometric prediction)
TOL_LEPTON_FRAC  = 0.001    # 0.1% — lepton mass ratios
TOL_PROTON_FRAC  = 0.005    # 0.5% — proton mass ratio
TOL_ALPHA_FRAC   = 0.003    # 0.3% — inverse fine-structure constant

N_BASE_SAMPLES   = 100_000  # number of random irrational bases to test
BASE_RANGE       = (1.05, 4.0)
PHI_EXCLUSION_RADIUS = 0.01 # bases within ±0.01 of φ are "near-phi" and excluded

# ===========================================================================
# MATCHING FUNCTIONS
# ===========================================================================

def best_lepton_match(base, target_ratio, n_max=30):
    """
    Return the minimum fractional error achievable by b^N for integer N in [1, n_max].
    """
    best_err = float("inf")
    for n in range(1, n_max + 1):
        pred = base ** n
        err  = abs(pred - target_ratio) / target_ratio
        if err < best_err:
            best_err = err
    return best_err

def best_proton_match(base, target_ratio, n_max=20):
    """
    Return the minimum fractional error achievable by b^{N + b^{-1}} for N in [10, n_max].
    (Proton formula includes the berry-phase correction b^{-1})
    """
    best_err = float("inf")
    correction = 1.0 / base
    for n in range(10, n_max + 1):
        pred = base ** (n + correction)
        err  = abs(pred - target_ratio) / target_ratio
        if err < best_err:
            best_err = err
    return best_err

def alpha_match(base):
    """
    Return fractional error of 360 * base^{-2} * (1 - 1/288) vs observed alpha^{-1}.
    (The 600-cell has 720 edges; the 360 factor is their antipodal-pair quotient,
    fixed independently of the base. We test whether base alone reproduces the alpha^{-1} formula.)
    """
    pred = 360.0 * (base ** -2) * (1.0 - 1.0/288.0)
    return abs(pred - ALPHA_INV_OBS) / ALPHA_INV_OBS


def alpha_condition_base_interval():
    """Bases b for which 360 b^-2 (1 - 1/288) lies within TOL_ALPHA_FRAC of alpha^-1.

    pred(b) is monotone decreasing in b, so the admissible set is the closed
    interval [sqrt(K / (A (1 + tol))), sqrt(K / (A (1 - tol)))] with
    K = 360 (287/288) and A = alpha^-1 (CODATA 2022).
    """
    k = 360.0 * (1.0 - 1.0 / 288.0)
    lo = math.sqrt(k / (ALPHA_INV_OBS * (1.0 + TOL_ALPHA_FRAC)))
    hi = math.sqrt(k / (ALPHA_INV_OBS * (1.0 - TOL_ALPHA_FRAC)))
    return lo, hi


WITHDRAWN_STATUS = "WITHDRAWN_NON_INFORMATIVE"

# ===========================================================================
# MAIN MONTE CARLO
# ===========================================================================

def run_cross_base_monte_carlo(n_samples=N_BASE_SAMPLES, seed=42):
    """
    Sample random irrational bases and test simultaneous four-target match.
    """
    rng = np.random.default_rng(seed)

    # Generate random bases in [BASE_RANGE[0], BASE_RANGE[1]]
    # Exclude rational approximations by requiring |base - p/q| > 1e-4
    # for all p/q with q < 20 (simple rationals).
    bases_raw = rng.uniform(BASE_RANGE[0], BASE_RANGE[1], n_samples * 5)
    # Keep bases well away from simple rationals (approximate irrationality filter)
    bases = []
    for b in bases_raw:
        rational_approx = min(
            abs(b - round(b * q) / q) for q in range(1, 20) if q > 0
        )
        if rational_approx > 1e-4 and abs(b - PHI) > PHI_EXCLUSION_RADIUS:
            bases.append(b)
        if len(bases) >= n_samples:
            break
    bases = np.array(bases[:n_samples])

    # For each base, test all four targets simultaneously
    hit_mu_arr    = np.array([best_lepton_match(b, RATIO_MU_E)  <= TOL_LEPTON_FRAC for b in bases])
    hit_tau_arr   = np.array([best_lepton_match(b, RATIO_TAU_E) <= TOL_LEPTON_FRAC for b in bases])
    hit_p_arr     = np.array([best_proton_match(b, RATIO_P_E)   <= TOL_PROTON_FRAC for b in bases])
    hit_alpha_arr = np.array([alpha_match(b)                    <= TOL_ALPHA_FRAC   for b in bases])

    hit_all = hit_mu_arr & hit_tau_arr & hit_p_arr & hit_alpha_arr

    n_hit_all       = int(hit_all.sum())
    n_alpha_hits    = int(hit_alpha_arr.sum())

    # Non-informativeness by construction: the alpha condition admits only an
    # interval of bases that lies inside the excluded phi window.
    alpha_lo, alpha_hi = alpha_condition_base_interval()
    excl_lo, excl_hi = PHI - PHI_EXCLUSION_RADIUS, PHI + PHI_EXCLUSION_RADIUS
    alpha_interval_inside_exclusion = bool(excl_lo < alpha_lo and alpha_hi < excl_hi)

    # Bare-phi test uses the same deliberately sparse formula family as the
    # cross-base control. The physical comparison also records the registered
    # corrected lepton formulae, because those are the manuscript-cited rows.
    phi_bare_errors = {
        "muon": best_lepton_match(PHI, RATIO_MU_E),
        "tau": best_lepton_match(PHI, RATIO_TAU_E),
        "proton": best_proton_match(PHI, RATIO_P_E),
        "alpha": alpha_match(PHI),
    }
    phi_bare_hits = {
        "muon": phi_bare_errors["muon"] <= TOL_LEPTON_FRAC,
        "tau": phi_bare_errors["tau"] <= TOL_LEPTON_FRAC,
        "proton": phi_bare_errors["proton"] <= TOL_PROTON_FRAC,
        "alpha": phi_bare_errors["alpha"] <= TOL_ALPHA_FRAC,
    }
    phi_bare_passes_all = all(phi_bare_hits.values())

    phi_corrected_errors = {
        "muon": abs(PHI**11 * (1.0 + 5.0 * ALPHA + PHI**8 * ALPHA**2) - RATIO_MU_E) / RATIO_MU_E,
        "tau": abs(PHI**17 * (1.0 - 3.6 * ALPHA) - RATIO_TAU_E) / RATIO_TAU_E,
        "proton": phi_bare_errors["proton"],
        "alpha": phi_bare_errors["alpha"],
    }
    phi_corrected_hits = {
        "muon": phi_corrected_errors["muon"] <= TOL_LEPTON_FRAC,
        "tau": phi_corrected_errors["tau"] <= TOL_LEPTON_FRAC,
        "proton": phi_corrected_errors["proton"] <= TOL_PROTON_FRAC,
        "alpha": phi_corrected_errors["alpha"] <= TOL_ALPHA_FRAC,
    }
    phi_corrected_passes_all = all(phi_corrected_hits.values())

    return {
        "n_samples":            n_samples,
        "base_range":           list(BASE_RANGE),
        "phi_exclusion_radius": PHI_EXCLUSION_RADIUS,
        "tolerances": {
            "lepton_frac":  TOL_LEPTON_FRAC,
            "proton_frac":  TOL_PROTON_FRAC,
            "alpha_frac":   TOL_ALPHA_FRAC,
        },
        "phi_bare_target_fractional_errors": phi_bare_errors,
        "phi_bare_target_hits": phi_bare_hits,
        "phi_bare_passes_all_four_targets": phi_bare_passes_all,
        "phi_corrected_target_fractional_errors": phi_corrected_errors,
        "phi_corrected_target_hits": phi_corrected_hits,
        "phi_corrected_passes_all_four_targets": phi_corrected_passes_all,
        "n_non_phi_bases_hitting_all_four": n_hit_all,
        "n_non_phi_bases_passing_alpha_condition": n_alpha_hits,
        "alpha_condition_base_interval": [alpha_lo, alpha_hi],
        "phi_exclusion_window": [excl_lo, excl_hi],
        "alpha_interval_inside_exclusion_window": alpha_interval_inside_exclusion,
        "status": WITHDRAWN_STATUS,
        "withdrawal_reasons": [
            "The alpha condition is satisfiable only inside the excluded phi window, so no non-phi base can pass whatever the lepton or proton results; the zero-hit count carries no information about phi.",
            "phi is credited with corrected formulae while other bases receive only bare forms; bare phi itself misses the muon and tau bands.",
            "No p-value or sigma is reported; the earlier p_null bound and its sigma conversion are withdrawn.",
        ],
        "pass": False,
        "verdict": (
            f"WITHDRAWN-NON-INFORMATIVE — {n_hit_all} non-phi bases hit all four bare targets, "
            f"as forced by construction: the alpha condition admits only b in [{alpha_lo:.5f}, {alpha_hi:.5f}], "
            f"inside the excluded window [{excl_lo:.5f}, {excl_hi:.5f}]. No significance is claimed."
        ),
    }

# ===========================================================================
# EXPANDED LEPTON GRID (withdrawn; grid-hit fraction reported, not a p-value)
# ===========================================================================

def run_lepton_expanded_lea():
    """
    Expanded lepton grid (phi only). WITHDRAWN as a significance: the 21 ppm
    window equals the observed muon residual (post hoc), no other base is
    evaluated, and the (C1, C2) grid is effectively a covering. The grid-hit
    fraction is reported as a diagnostic, not as a p-value, and no sigma is
    computed. Targets use CODATA 2022 m_mu/m_e and PDG 2024 m_tau.
    Search Space:
      N_mu, N_tau in [1, 30] with N_mu < N_tau => 435 pairs
      C1_mu, C1_tau in [-20, 20] in steps of 0.2 (k/5) => 201 choices each
      C2_mu, C2_tau in [-50, 50] in steps of 1.0 => 101 choices each
    Target matches:
      pred = phi**N * (1 + C1*ALPHA + C2*ALPHA**2)
      hit means abs(pred - observed_ratio)/observed_ratio < 21e-6 (21 ppm)
    """
    import numpy as np
    import math
    from gct_utils import PHI

    ALPHA = 1.0 / ALPHA_INV_OBS
    RATIO_MU = RATIO_MU_E    # CODATA 2022
    RATIO_TAU = RATIO_TAU_E  # PDG 2024 (the earlier 3477.15 target was stale)
    TOLERANCE = 21e-6

    # 1. Precompute matches for all N, C1, C2
    N_list = list(range(1, 31))
    C1_list = np.linspace(-20, 20, 201)  # 201 choices
    C2_list = np.linspace(-50, 50, 101)  # 101 choices

    def count_hits(target_ratio):
        hits_per_n = {}
        for n in N_list:
            base_mass = PHI**n
            hit_count = 0
            # We can vectorize this inner loop
            C1_grid, C2_grid = np.meshgrid(C1_list, C2_list)
            preds = base_mass * (1.0 + C1_grid * ALPHA + C2_grid * ALPHA**2)
            errs = np.abs(preds - target_ratio) / target_ratio
            hit_count = np.sum(errs <= TOLERANCE)
            hits_per_n[n] = int(hit_count)
        return hits_per_n

    muon_hits = count_hits(RATIO_MU)
    tau_hits = count_hits(RATIO_TAU)

    # 2. Count total joint pairs N_mu < N_tau
    total_valid_combinations = 0
    for n_mu in N_list:
        for n_tau in range(n_mu + 1, 31):
            total_valid_combinations += muon_hits[n_mu] * tau_hits[n_tau]

    total_combinations = 435 * (201 * 101)**2

    grid_hit_fraction = total_valid_combinations / total_combinations

    return {
        "lepton_exponent_pair": {
            "search_space_expanded": True,
            "total_combinations": total_combinations,
            "valid_combinations": total_valid_combinations,
            "grid_hit_fraction_not_a_p_value": float(grid_hit_fraction),
            "tolerance_ppm": TOLERANCE * 1e6,
            "muon_target_ratio": RATIO_MU,
            "tau_target_ratio": RATIO_TAU,
            "n_exponents_with_muon_hits": sum(1 for v in muon_hits.values() if v > 0),
            "n_exponents_with_tau_hits": sum(1 for v in tau_hits.values() if v > 0),
            "status": WITHDRAWN_STATUS,
            "canonical": False,
            "withdrawal_reasons": [
                "The 21 ppm hit window equals the observed muon residual, so it was fixed after the data were seen.",
                "Only phi is evaluated; the grid says nothing about phi against other constants.",
                "The C2 step alpha^2 (about 5.3e-5) is comparable to the window width (about 4.2e-5), so the (C1, C2) grid is effectively a covering and the hit fraction measures grid volume, not specialness.",
                "The earlier run used a stale tau target (3477.15); the target is PDG 2024.",
            ],
            "note": "Diagnostic only. No sigma is computed; the earlier expanded-grid sigma is withdrawn.",
        },
        "joint_4param_monte_carlo": {
            "status": WITHDRAWN_STATUS,
            "canonical": False,
            "note": "The cross-base bare-control test is non-informative by construction (see cross_base_monte_carlo.withdrawal_reasons).",
        },
    }

# ===========================================================================
# MAIN
# ===========================================================================

def main():
    print("=" * 70)
    print("  GCT Cross-Base Monte Carlo + Expanded Lepton Grid (WITHDRAWN diagnostics)")
    print("=" * 70)

    mc = run_cross_base_monte_carlo()
    lea = run_lepton_expanded_lea()

    results = {
        "protocol":              "protocol_global_significance.py",
        "cross_base_monte_carlo": mc,
        "lepton_lea":            lea,
        "canonical_sigma": None,
        "headline_significance": (
            "None. Earlier global-significance figures for the numerical matches are withdrawn: the cross-base comparison "
            "could not, by construction, credit any base other than phi, and the trial counts behind the quoted sigma values "
            "were asserted rather than enumerated. The preregistered constant control test that compares phi against other "
            "constants under identical formula freedom has reported: v3 is NEGATIVE-FRAGILE (p0 = 0.196; 58 of 300 random "
            "bases do at least as well as phi on the 21 constants; non-confirmatory). The phi-formula matches are therefore "
            "Tier 4 as evidence that phi explains the value (constant control test v3 NEGATIVE-FRAGILE; App PSC §PSC.9.6)."
        ),
        "pass": mc["pass"],
    }

    out_path = get_output_path("protocol_global_significance_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nVERDICT: {mc['verdict']}")
    print(f"Cross-base Monte Carlo: {mc['status']} (alpha interval {mc['alpha_condition_base_interval']} inside {mc['phi_exclusion_window']})")
    print(f"Expanded lepton grid:   {lea['lepton_exponent_pair']['status']} (grid-hit fraction {lea['lepton_exponent_pair']['grid_hit_fraction_not_a_p_value']:.3e}; not a p-value)")
    print(f"Results saved to:   {out_path}")
    print("=" * 70)
    if not mc["pass"]:
        print("Protocol completed with a registered non-pass verdict encoded in JSON.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
