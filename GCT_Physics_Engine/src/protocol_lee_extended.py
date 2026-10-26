#!/usr/bin/env python3
"""
protocol_lee_extended.py — Extended Look-Elsewhere Effect
==================================================================
Calculates the true global significance of the GCT geometric mass spectrum
by generating a vast combinatorial space of competitor formulas and assessing
trial-factor penalties.

The p_global figure depends only on the size of the formula space; it is a
valid significance only if GCT itself lands within the 20 ppm window for both
mu and tau. The former literal pass=True is retired; the
protocol now computes the GCT mu and tau ratios with the engine formulas
(protocol_lepton_spectrum analytic limit) and passes only if both are within
20 ppm.
"""

import json
import math
import sys
from pathlib import Path
from scipy.stats import norm
from gct_utils import C, get_output_path

def run_extended_lee():
    print("=" * 70)
    print("GCT Protocol — Extended Look-Elsewhere Effect (LEE)")
    print("=" * 70)

    phi = float(C.PHI)
    alpha = 1.0 / float(C.ALPHA_INV_GCT)
    
    # Target Ratios
    # From R_Precision_Scorecard:
    muon_ratio = 105.6583755 / 0.510998950  # ~ 206.768...
    tau_ratio = 1776.93 / 0.510998950       # ~ 3477.36 (PDG 2024)
    
    # 1. Define the Extended Space
    competitors = []
    
    # {phi^N * alpha^M}
    for n in range(1, 31):
        for m in range(0, 4):
            val = (phi ** n) * (alpha ** m)
            competitors.append({"formula": f"phi^{n} * alpha^{m}", "val": val})
            # Include negative alpha powers as well (m in [-3, 3]) to span a
            # large look-elsewhere competitor space.
            if m > 0:
                val_neg = (phi ** n) * (alpha ** -m)
                competitors.append({"formula": f"phi^{n} * alpha^{-m}", "val": val_neg})
                
    # {pi^N}, {e^N}, {2^N} with alpha modifiers to match "1000+"
    for base_name, base_val in [("pi", math.pi), ("e", math.e), ("2", 2.0)]:
        for n in range(1, 31):
            for m in range(0, 4):
                val = (base_val ** n) * (alpha ** m)
                competitors.append({"formula": f"{base_name}^{n} * alpha^{m}", "val": val})
                if m > 0:
                    val_neg = (base_val ** n) * (alpha ** -m)
                    competitors.append({"formula": f"{base_name}^{n} * alpha^{-m}", "val": val_neg})
                    
    # Ensure uniqueness
    unique_vals = {}
    for c in competitors:
        # rounding to avoid float imperceptible differences
        key = round(c["val"], 10)
        if key not in unique_vals:
            unique_vals[key] = c
            
    space_size = len(unique_vals)
    print(f"[*] Generated vast combinatorial space: {space_size} unique formulas.")
    
    # 2. Test Space Against Muon and Tau mass ratios
    # Count how many achieve <= 20 ppm
    def count_hits(target, formulas, ppm_limit=20.0):
        hits = 0
        window = target * (ppm_limit / 1e6)
        for c in formulas:
            if abs(c["val"] - target) <= window:
                hits += 1
        return hits

    formulas = list(unique_vals.values())
    muon_hits = count_hits(muon_ratio, formulas, 20.0)
    tau_hits = count_hits(tau_ratio, formulas, 20.0)
    
    print(f"[*] Muon matches (<= 20 ppm): {muon_hits}")
    print(f"[*] Tau matches (<= 20 ppm): {tau_hits}")

    # GCT's own hits, with the engine's analytic-limit lepton formulas
    # (same as protocol_lepton_spectrum.py; A3 measured alpha).
    alpha_obs = float(C.ALPHA_OBS)
    gct_mu = phi**11 * (1 + float(C.N_PHASON_CHANNELS) * alpha_obs + phi**8 * alpha_obs**2)
    gct_tau = phi**17 * (1 + float(C.TAU_SCREEN_COEFF) * alpha_obs)
    gct_mu_ppm = (gct_mu - muon_ratio) / muon_ratio * 1e6
    gct_tau_ppm = (gct_tau - tau_ratio) / tau_ratio * 1e6
    gct_both_within_20ppm = bool(abs(gct_mu_ppm) <= 20.0 and abs(gct_tau_ppm) <= 20.0)
    print(f"[*] GCT muon ratio residual: {gct_mu_ppm:+.2f} ppm; tau: {gct_tau_ppm:+.2f} ppm "
          f"-> both within 20 ppm: {gct_both_within_20ppm}")
    
    # 3. Compute True Significance
    # Expected volume of the window in log space or directly as a fraction
    # Probability of a purely random value hitting a 20 ppm window (+/- 20 ppm)
    # is 40 ppm if uniformly distributed in log space.
    p_window = 40.0 / 1e6
    
    # Search trials = C(space_size, 2) since we are picking two exponents
    # one for muon, one for tau.
    trials = (space_size * (space_size - 1)) / 2
    
    # The probability of getting a hit for BOTH muon and tau in one random pair:
    p_pair = p_window * p_window
    
    # Global p-value:
    p_global = trials * p_pair
    # Cap at 1.0
    p_global = min(1.0, p_global)
    
    # Convert global p-value to sigma significance (1-tailed)
    if p_global < 1.0:
        sigma = norm.isf(p_global)
    else:
        sigma = 0.0

    print(f"[*] Search Pair Trials (T): {trials:,.0f}")
    print(f"[*] Local Pair p-value: {p_pair:.2e}")
    print(f"[*] Global Penalized p-value: {p_global:.4f} (~ {math.ceil(p_global*100)}%)")
    print(f"[*] Significance IF GCT hit both 20 ppm windows: {sigma:.2f} sigma")
    
    verdict = (
        "GCT_MU_TAU_WITHIN_20PPM_LEE_APPLIES" if gct_both_within_20ppm
        else f"GCT_OUTSIDE_20PPM_WINDOW_LEE_PREMISE_FAILS_mu={gct_mu_ppm:+.1f}ppm_tau={gct_tau_ppm:+.1f}ppm"
    )
    print(f"[*] Verdict: {verdict}")
    out_data = {
        "pass": gct_both_within_20ppm,
        "verdict": verdict,
        "gct_muon_ratio_residual_ppm": float(gct_mu_ppm),
        "gct_tau_ratio_residual_ppm": float(gct_tau_ppm),
        "gct_both_within_20ppm": gct_both_within_20ppm,
        "global_p_value_interpretation": "conditional on GCT landing within 20 ppm for both mu and tau; not a significance when that premise fails",
        "space_size": space_size,
        "search_pair_trials": trials,
        "muon_20ppm_hits": muon_hits,
        "tau_20ppm_hits": tau_hits,
        "local_pair_probability": p_pair,
        "global_p_value": p_global,
        "significance_sigma": float(sigma)
    }
    
    with open(get_output_path("protocol_lee_extended_results.json"), "w") as fp:
        json.dump(out_data, fp, indent=2)

if __name__ == "__main__":
    run_extended_lee()
