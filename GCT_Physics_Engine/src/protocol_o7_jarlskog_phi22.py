#!/usr/bin/env python3
"""
protocol_o7_jarlskog_phi22.py
==============================

CKM Jarlskog invariant J: the icosahedral phi^(-22) suppression candidate.
Open Problem O.7 (open); this protocol evaluates the candidate ansatz.

CONTEXT (V3 Ch09 §9.4.3)

The Jarlskog invariant J is the CKM CP-violation measure (Jarlskog 1985
PRL 55:1039). It is rephasing-invariant:
    J_obs = (3.12 +/- 0.13) x 10^-5  (PDG 2024)

GCT candidate (Tier 3 ansatz):
    J_GCT = c_0 * phi^(-22)
where the phi^(-22) suppression follows from the two-loop muon-harmonic
CP-violation amplitude scaling. The leading prefactor c_0 is a
geometric / group-theoretic O(1) factor to be derived.

MOTIVATION FOR THE phi^(-22) EXPONENT (Tier 3 ansatz, O.7 open)

Under the Tier 3 ansatz, CKM CP violation appears at order O(alpha^2 * (mu/e)^2 * ...) in the
two-loop expansion of the icosahedral electroweak sector. The muon-
electron mass ratio is m_mu/m_e ~ 207, and the GCT mass hierarchy gives:
    m_mu / m_e = phi^11 * (1 + small)  -- per V3 Ch08 (Lepton ladder)
    (m_mu / m_e)^2 ~ phi^22

This (m_mu/m_e)^2 suppression at two-loop order gives the J ~ phi^(-22)
factor structure. The leading prefactor would follow from icosahedral group-
theoretic CP-violation amplitudes; for an O(1) coefficient identified
with a small-icosahedral-group invariant.

PREFACTOR CANDIDATES (none derived from first principles)

J_obs / phi^(-22) = 3.12e-5 / 2.525e-5 = 1.236

Candidate O(1) prefactors (the seven entries of PREFACTOR_CANDIDATES):
    1                 = 1.000  (bare phi^-22)
    sqrt(phi)         ~ 1.272  (golden-ratio square root)
    4/pi              ~ 1.273  (icosahedral solid-angle ratio)
    Coxeter h_3 / 8   = 1.250  (10/8)
    phi^(1/3)         ~ 1.174  (golden-ratio cube root)
    phi - 1/phi^2     ~ 1.236  (= sqrt(5) - 1)
    phi/(phi+1/phi)   ~ 0.724  (= phi^2/(phi^2+1))

The best-matching candidate is chosen post hoc from this list of seven
and is reported by the protocol as best_prefactor_name; with several O(1)
candidates spanning 0.72-1.27, a match at the percent level carries little
evidential weight (look-elsewhere effect). No candidate is derived.

ILLUSTRATIVE FORM (Tier 3 phenomenological)

    J_GCT = sqrt(phi) * phi^(-22) = phi^(-43/2) ~ 3.21e-5

lies ~3% above J_obs = 3.12e-5; the prefactor is selected post hoc.

For full Tier 2 closure, any O(1) prefactor requires
derivation from icosahedral group-theoretic CP amplitudes; this is the
residual piece bundled with O.5 (QLQCD-1L closure of quark-mass spectrum).
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
J_OBS = 3.12e-5
J_OBS_UNCERT = 0.13e-5

# GCT prediction
J_PHI_NEG_22 = PHI ** (-22)
J_GCT_SQRT_PHI = math.sqrt(PHI) * PHI ** (-22)  # = phi^(-43/2)
J_GCT_4_OVER_PI = (4.0 / math.pi) * PHI ** (-22)

# Candidate prefactors
PREFACTOR_CANDIDATES = {
    "1 (bare phi^-22)": 1.0,
    "sqrt(phi)": math.sqrt(PHI),
    "4/pi": 4.0 / math.pi,
    "Coxeter_h3/8": 10.0 / 8.0,
    "phi^(1/3)": PHI ** (1.0 / 3.0),
    "phi - 1/phi^2": PHI - 1.0 / PHI ** 2,
    "phi/(phi+1/phi)": PHI / (PHI + 1.0 / PHI),  # = phi^2 / (phi^2 + 1)
}


def main():
    print("=" * 76)
    print("O.7 PROTOCOL: CKM Jarlskog invariant via phi^(-22) suppression")
    print("=" * 76)

    print(f"\nObservational anchor (PDG 2024):")
    print(f"  J_obs                                     : ({J_OBS:.3e} +/- {J_OBS_UNCERT:.3e})")

    print(f"\nphi^(-22) bare value:")
    print(f"  phi^(-22) = 1/F_{{22}}*F_{{23}}            : {J_PHI_NEG_22:.4e}")
    print(f"  J_obs / phi^(-22)                          : {J_OBS / J_PHI_NEG_22:.4f}")

    print(f"\nPrefactor candidates (J = c0 * phi^(-22)):")
    print(f"  {'candidate':>25}  {'c0':>10}  {'J_candidate':>14}  {'agreement %':>14}")
    best_name = None
    best_agreement = float("inf")
    for name, c0 in PREFACTOR_CANDIDATES.items():
        J_pred = c0 * J_PHI_NEG_22
        rel_diff_percent = abs(J_pred - J_OBS) / J_OBS * 100
        within_uncertainty = abs(J_pred - J_OBS) <= J_OBS_UNCERT
        print(f"  {name:>25}  {c0:>10.4f}  {J_pred:>14.4e}  "
              f"{rel_diff_percent:>13.2f}%  "
              + ("(within sigma)" if within_uncertainty else ""))
        if rel_diff_percent < best_agreement:
            best_agreement = rel_diff_percent
            best_name = name

    # Inverse problem: the exponent on phi that reproduces the observed J.
    n_exact = -math.log(J_OBS) / math.log(PHI)
    print(f"\nInverse: J_obs = phi^(-{n_exact:.3f})")
    print(f"   Closest half-integer exponent (sqrt(phi)*phi^-22 = phi^-43/2 = phi^-21.5): {21.5}")

    print(f"\n" + "=" * 76)
    print("VERDICT FOR O.7")
    print("=" * 76)
    print(f"  Best O(1) prefactor candidate          : {best_name}")
    print(f"  Best agreement (% from J_obs)          : {best_agreement:.2f}%")
    print(f"")
    print(f"  CANDIDATE: The phi^(-22) suppression structure is a Tier 3 ansatz from")
    print(f"  the two-loop muon-harmonic CP-violation amplitude scaling")
    print(f"  (m_mu/m_e)^2 ~ phi^22 in the icosahedral electroweak sector.")
    print(f"  The required prefactor c_0 = {J_OBS / J_PHI_NEG_22:.3f} is matched post hoc by")
    print(f"  '{best_name}' among seven O(1) candidates (look-elsewhere; none derived).")
    print(f"  Illustrative J_GCT(sqrt(phi)*phi^-22) = {J_GCT_SQRT_PHI:.3e} vs J_obs = {J_OBS:.3e}")
    print(f"  ({abs(J_GCT_SQRT_PHI / J_OBS - 1) * 100:.1f}% off; Tier 3 phenomenological).")
    print(f"")
    print(f"  Status: Tier 3 structure ansatz (phi^(-22)) + Tier 3 prefactor; full")
    print(f"  Tier 2 closure (prefactor derivation from icosahedral CP amplitudes)")
    print(f"  is bundled with O.5 (QLQCD-1L) per the existing manuscript framing.")
    print("=" * 76)

    out = {
        "phi": PHI,
        "J_obs_PDG": J_OBS,
        "J_obs_uncertainty": J_OBS_UNCERT,
        "phi_neg_22": J_PHI_NEG_22,
        "J_GCT_sqrt_phi": J_GCT_SQRT_PHI,
        "J_GCT_4_over_pi": J_GCT_4_OVER_PI,
        "J_obs_div_phi_neg_22": J_OBS / J_PHI_NEG_22,
        "best_prefactor_name": best_name,
        "best_agreement_percent": best_agreement,
        "exact_phi_exponent_n": -math.log(J_OBS) / math.log(PHI),
        "prefactor_candidates_J_predictions": {
            name: c0 * J_PHI_NEG_22 for name, c0 in PREFACTOR_CANDIDATES.items()
        },
    }
    if OUTPUT_DIR_AVAILABLE:
        out_path = get_output_path("protocol_o7_jarlskog_phi22_results.json")
    else:
        out_path = Path(__file__).resolve().parent.parent / "data" / "protocol_o7_jarlskog_phi22_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nResults saved to: {out_path}")
    print("=" * 76)


if __name__ == "__main__":
    main()
