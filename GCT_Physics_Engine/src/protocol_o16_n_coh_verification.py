#!/usr/bin/env python3
"""
protocol_o16_n_coh_verification.py
===================================

Numerical verification of the N_coh (Polaron Persistence) formula
evaluation with the canonical Tier 3 inputs documented in App H O.16
and V1 Ch17 §17.1.4b.

REGISTERED PROBLEM (App H O.16)

The formula structure is established as Tier 2:
    N_coh = (phi^(-18) * omega_d / (N_cage * g_single^eff * eta_F))^2
The formula-evaluation audit uses the pre-overlap g_single^eff reference
(38.3 MHz, calibrated to operating-point consistency). The operational
eta_Zeno branch applies the overlap factor separately. With both omega_d and
g_single^eff expressed as angular rates, canonical tubulin parameters give
N_coh ~ 1.24e-11 pre-overlap and ~1.24e-7 at f_overlap=0.01. These are
robustness-margin diagnostics under declared Tier 3 inputs, not biological
population-threshold derivations. Dissolution requires g_single^eff
suppression by the branch-specific F_crit diagnostic from
protocol_polaron_Ncoh_derivation_results.json.

Closure of O.12 (specific omega_d) and a first-principles derivation
of g_single^eff would convert the formula structure into a fully-
numerical Tier 2 prediction.

Scope: this protocol verifies the N_coh formula evaluation with current Tier 3 inputs; full O.16 closure requires first-principles g_single^eff derivation.

This protocol DOES NOT derive g_single^eff from first principles
(that is the open question of O.16). It performs a REGRESSION-STYLE
VERIFICATION: take the existing Tier 3 inputs documented in the
manuscript, substitute into the N_coh formula with a consistent angular
rate convention, and report the angular-consistent evaluation. This is a
numerical sanity-check on the formula evaluation, NOT a closure of the
first-principles derivation question.

INPUTS USED

  phi^(-18)         = 1.731e-4  (App K)
  omega_d           = 2*pi * 112 MHz = 7.037e8 rad/s
                      (Ch13 Sec 13.1.2b; Tier 3 pending O.12)
  N_cage            = 144  (V1 Ch17 / App J cage count)
  g_single^eff      = 2*pi * 38.3 MHz = 2.407e8 rad/s pre-overlap
                      (App Q renormalized: 41x lift from bare 931 kHz)
                      operational eta_Zeno branch multiplies by f_overlap
                      (Tier 3 calibrated, pending first-principles derivation)
  eta_F             = 1.0  (Foerster factor, default)

OUTPUT

  N_coh = (phi^(-18) * omega_d / (N_cage * g_single^eff * eta_F))^2

VERIFICATION

  Angular-consistent evaluation: N_coh = 1.24e-11.

  F_crit interpretation (per App H O.16):
    "Polaron robustness margin is reported by the dedicated F_crit value"
    "dissolution requires branch-specific g_single^eff suppression by F_crit"
  The load-bearing F_crit value is the operational sensitivity-branch
  suppression margin inherited from the dedicated Polaron N_coh derivation
  result. The N_coh=1 and "21 orders" calculations below are diagnostics
  only and do not override that cross-protocol value.

  Anaesthesia prediction (structurally preserved regardless of F_crit
  interpretation): Delta C_50 scales with F_disrupt / F_crit, where
  F_disrupt is the experimentally-measured Trp-pocket disruption
  factor for a candidate anaesthetic compound.
"""

import json
import math
from pathlib import Path

try:
    from gct_utils import get_output_path, C
    OUTPUT_DIR_AVAILABLE = True
except ImportError:
    OUTPUT_DIR_AVAILABLE = False

PHI = float(C.PHI)
PHI_NEG_18 = PHI ** (-18)

# Tier 3 canonical tubulin inputs
OMEGA_D_RAD_PER_S = 2.0 * math.pi * 112.0e6      # primary Protocol A-Prime branch angular drive rate
N_CAGE = 144
G_SINGLE_EFF_PRE_OVERLAP_ANGULAR_PER_S = 2.0 * math.pi * 38.3e6  # App Q angular-rate convention
F_OVERLAP_OPERATIONAL = 0.01
G_SINGLE_EFF_OVERLAP_ANGULAR_PER_S = G_SINGLE_EFF_PRE_OVERLAP_ANGULAR_PER_S * F_OVERLAP_OPERATIONAL
ETA_F = 1.0                                       # Foerster factor

N_COH_ANGULAR_CONSISTENT_REFERENCE = 1.235260244106657e-11
F_CRIT_REFERENCE_VALUE = 3.1561715231092423e7


def compute_n_coh(phi_neg_18, omega_d, n_cage, g_single_eff, eta_f):
    """N_coh = (phi^(-18) * omega_d / (N_cage * g_single^eff * eta_F))^2.

    Both omega_d and g_single^eff use the App Q angular-rate convention.
    A cycles/s display would differ by 2*pi and is not used in this check.
    """
    inner = phi_neg_18 * omega_d / (n_cage * g_single_eff * eta_f)
    return inner ** 2


def main():
    print("=" * 76)
    print("O.16 PROTOCOL: N_coh formula verification with canonical Tier 3 inputs")
    print("=" * 76)

    print(f"\nCanonical Tier 3 inputs:")
    print(f"  phi^(-18)                              : {PHI_NEG_18:.4e}")
    print(f"  omega_d = 2*pi * 112 MHz               : {OMEGA_D_RAD_PER_S:.4e} rad/s")
    print(f"  N_cage                                 : {N_CAGE}")
    print(f"  g_single^eff pre-overlap               : {G_SINGLE_EFF_PRE_OVERLAP_ANGULAR_PER_S:.3e} rad/s = {G_SINGLE_EFF_PRE_OVERLAP_ANGULAR_PER_S/(2*math.pi*1e6):.1f} MHz cyclic")
    print(f"  f_overlap operational branch           : {F_OVERLAP_OPERATIONAL:.2e}")
    print(f"  g_single^eff overlap-propagated        : {G_SINGLE_EFF_OVERLAP_ANGULAR_PER_S:.3e} rad/s = {G_SINGLE_EFF_OVERLAP_ANGULAR_PER_S/(2*math.pi):.3e} Hz cyclic")
    print(f"  eta_F                                  : {ETA_F}")

    n_coh = compute_n_coh(PHI_NEG_18, OMEGA_D_RAD_PER_S, N_CAGE,
                          G_SINGLE_EFF_PRE_OVERLAP_ANGULAR_PER_S, ETA_F)
    n_coh_overlap = compute_n_coh(PHI_NEG_18, OMEGA_D_RAD_PER_S, N_CAGE,
                                  G_SINGLE_EFF_OVERLAP_ANGULAR_PER_S, ETA_F)

    print(f"\nN_coh evaluation:")
    print(f"  Computed pre-overlap                    : {n_coh:.4e}")
    print(f"  Computed overlap-propagated             : {n_coh_overlap:.4e}")
    print(f"  Angular-consistent reference            : {N_COH_ANGULAR_CONSISTENT_REFERENCE:.4e}")
    rel_diff = abs(n_coh - N_COH_ANGULAR_CONSISTENT_REFERENCE) / N_COH_ANGULAR_CONSISTENT_REFERENCE
    print(f"  Relative agreement to angular reference : {rel_diff:.2%}")
    matches = rel_diff < 0.05  # within 5%

    # F_crit derivation under N_coh = 1 (single-Polaron) threshold
    # N_coh(g_suppressed) = N_coh(g_eff) * (g_eff/g_suppressed)^2
    # For N_coh(suppressed) = 1: (g_eff/g_suppressed)^2 = 1/N_coh
    # => F_crit_N1 = g_eff/g_suppressed = 1/sqrt(N_coh)
    f_crit_n1 = 1.0 / math.sqrt(n_coh)

    # F_crit implied by the 21-orders reference branch.
    # If reference = N_coh / 10^21:
    threshold_21_orders = n_coh / 10 ** 21
    f_crit_21_orders = math.sqrt(n_coh / threshold_21_orders)

    print(f"\nF_crit interpretation (reference-branch comparison):")
    print(f"  F_crit assuming N_coh=1 threshold       : {f_crit_n1:.3e}")
    print(f"  F_crit assuming 21-orders threshold     : {f_crit_21_orders:.3e}")
    print(f"  Operational F_crit reference            : {F_CRIT_REFERENCE_VALUE:.3e}")
    print(f"  Source: protocol_polaron_Ncoh_derivation_results.json")

    print(f"\n" + "=" * 76)
    print("VERDICT FOR O.16")
    print("=" * 76)
    print(f"  N_coh formula evaluation matches angular-consistent reference: {matches}")
    print(f"")
    print(f"  STATUS: FORMULA AUDIT (regression-style verification only).")
    print(f"")
    print(f"  AUDITED:")
    print(f"    - N_coh formula structure evaluates to 1.24e-11 with the")
    print(f"      pre-overlap anchor, and to 1.24e-7 with f_overlap=0.01,")
    print(f"      once omega_d and g_single^eff use the same angular-rate convention.")
    print(f"    - Structural prediction Delta C_50 ~ F_disrupt/F_crit uses the")
    print(f"      branch-specific F_crit diagnostic; the absolute value remains Tier 3.")
    print(f"")
    print(f"  NOT CLOSED (these remain as the O.16 open questions):")
    print(f"    - First-principles derivation of g_single^eff (currently calibrated")
    print(f"      via App Q ~41x pre-overlap renormalization plus overlap propagation)")
    print(f"    - First-principles derivation of omega_d (currently 112 MHz primary branch pending")
    print(f"      O.12 chiral phonon-polariton renormalization)")
    print("=" * 76)

    out = {
        "phi_neg_18": PHI_NEG_18,
        "omega_d_rad_per_s": OMEGA_D_RAD_PER_S,
        "N_cage": N_CAGE,
        "g_single_eff_pre_overlap_angular_per_s": G_SINGLE_EFF_PRE_OVERLAP_ANGULAR_PER_S,
        "g_single_eff_pre_overlap_Hz": G_SINGLE_EFF_PRE_OVERLAP_ANGULAR_PER_S / (2.0 * math.pi),
        "f_overlap_operational": F_OVERLAP_OPERATIONAL,
        "g_single_eff_overlap_angular_per_s": G_SINGLE_EFF_OVERLAP_ANGULAR_PER_S,
        "g_single_eff_overlap_Hz": G_SINGLE_EFF_OVERLAP_ANGULAR_PER_S / (2.0 * math.pi),
        "eta_F": ETA_F,
        "N_coh_pre_overlap_computed": n_coh,
        "N_coh_overlap_propagated_computed": n_coh_overlap,
        "N_coh_angular_consistent_reference": N_COH_ANGULAR_CONSISTENT_REFERENCE,
        "relative_agreement": rel_diff,
        "matches_angular_consistent_reference_within_5pct": bool(matches),
        "F_crit_N_coh_eq_1_threshold": f_crit_n1,
        "F_crit_21_orders_threshold": f_crit_21_orders,
        "F_crit_reference_value": F_CRIT_REFERENCE_VALUE,
        "F_crit_source": "protocol_polaron_Ncoh_derivation_results.json",
        "F_crit_interpretation_ambiguous": False,
        "status": "FORMULA AUDIT -- regression-style verification of formula evaluation only",
        "audited": [
            "N_coh = 1.24e-11 pre-overlap and 1.24e-7 at f_overlap=0.01 under consistent angular-rate convention",
            "Delta C_50 ~ F_disrupt/F_crit uses the branch-specific F_crit diagnostic",
        ],
        "not_closed": [
            "First-principles g_single^eff derivation (still calibrated pre-overlap plus overlap propagation)",
            "First-principles omega_d derivation (still O.12-pending)",
        ],
    }
    if OUTPUT_DIR_AVAILABLE:
        out_path = get_output_path("protocol_o16_n_coh_verification_results.json")
    else:
        out_path = Path(__file__).resolve().parent.parent / "data" / "protocol_o16_n_coh_verification_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nResults saved to: {out_path}")
    print("=" * 76)


if __name__ == "__main__":
    main()
