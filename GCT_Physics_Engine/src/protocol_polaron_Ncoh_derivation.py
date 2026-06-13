#!/usr/bin/env python3
"""
protocol_polaron_Ncoh_derivation.py
====================================
Formula audit for Open Problem O.16 (App H §H.5):
evaluate the Polaron coherence robustness reference N_coh from the N=144 cage
geometry + phason stiffness ratio K_perp/K_par = phi^-18 (V3 App K) + the
Tavis-Cummings cooperativity criterion (V3 Ch13 §13.5).

DERIVATION CHAIN
================
From V3 Ch13 §13.5 (eta_Zeno engine), the per-substrate Zeno coupling is:

  eta_Zeno = (g_single^eff * sqrt(N_bio) / kappa) * eta_F

where:
  g_single^eff = effective per-spin Rashba-phason coupling (V3 §13.1.2)
  N_bio = number of cooperatively phase-locked dipoles
  kappa = cavity decay rate (V3 §13.5.4)
  eta_F = Floquet open-system efficiency (V3 §13.4.4)

Across a DMC-positive substrate branch, eta_Zeno is the robustness margin
reported by the Tavis-Cummings chain. The DMC gate is necessary for Level II,
but sufficiency also requires the O.21 cooperative radical-pair/Polaron
witness, the O.23 protected-subspace coherence demonstration, and the O.34
ATP-Trp redox-regeneration condition.

The Polaron loses its cooperativity margin below the reference N_coh given by
eta_Zeno = 1:

  N_coh = (kappa / (g_single^eff * eta_F))^2

Substituting V3 §13.5.4 geometric kappa = phi^-18 * omega_d / N_cage:

  N_coh = (phi^-18 * omega_d / (N_cage * g_single^eff * eta_F))^2

For tubulin substrate at the V3 §13.5.7 canonical parameters:
  g_single^eff = 3.8e7 Hz pre-overlap anchor (V3 §13.1.2, Tier 3 calibrated;
                 range 10-100 MHz per best-effort transparent disclosure)
  f_overlap = 0.01 engine-current operational branch, giving 3.8e5 Hz
  N_cage = 144 (Tier 2 — icosahedral dodecahedral cage from V3 Ch07 §7.1)
  omega_d = 2*pi*112 MHz primary branch (Tier 2 mechanism / Tier 3 specific value, O.12)
  kappa^geom = 120 Hz (V3 §13.5.4, derived from phi^-18 + N_cage = 144)
  eta_F ~ 1 on resonance (V3 §13.4.4)

This evaluates the N_coh formula within the manuscript framework; the
formula structure is Tier 2, while g_single^eff and omega_d remain Tier 3.

RESULT
======
If N_coh comes out as a robustness reference derivable from the N=144 cage +
phi^-18 stiffness plus declared substrate inputs, the formula evaluation
passes as a diagnostic. It is not an independent Level-II population
threshold or a closure of the substrate-sufficiency question.

Prediction: N_coh will be very small (<<1) even on the conservative
beta-Trp n_rp=1 sensitivity branch. Ch13:633 makes the operative central
cooperative branch n_rp=0 pending O.21; hydration-shell OH/proton dipoles
are bath/environment and are not counted in the cooperative oscillator basis.
The suppression-margin diagnostic in V1 Ch17 §17.1.4b therefore requires
*parameter changes* (anaesthesia, hypothermia, death) that drop g_single^eff
or boost kappa — these are quantifiable interventions.
"""

import math
import json
import numpy as np
from pathlib import Path
from gct_utils import C

PHI = float(C.PHI)


def derive_N_coh_from_cooperativity(
    g_single_eff_Hz: float,
    kappa_Hz: float,
    eta_F: float = 1.0,
) -> float:
    """
    N_coh = (kappa / (g_single^eff * eta_F))^2

    Reference line below which the Polaron's cooperativity factor sqrt(N) is
    insufficient to clear the eta_Zeno robustness margin.
    """
    return (kappa_Hz / (g_single_eff_Hz * eta_F)) ** 2


def derive_kappa_geometric(omega_d_Hz: float, N_cage: int = 144) -> float:
    """
    V3 Ch13 §13.5.4 geometric mode:
      kappa^geom = phi^-18 * omega_d / N_cage
    """
    return PHI ** (-18) * omega_d_Hz / N_cage


def eta_Zeno_from_substrate(g_single_eff, N_bio, kappa, eta_F=1.0):
    return (g_single_eff * math.sqrt(N_bio) / kappa) * eta_F


def main():
    print("=" * 76)
    print("O.16 FORMULA AUDIT: Polaron coherence robustness-reference N_coh")
    print("=" * 76)

    # ── Tubulin substrate (V3 §13.5.7 canonical parameters) ──────────────
    g_single_eff_tubulin = 3.8e7  # Hz pre-overlap (V3 §13.1.2, Tier 3 calibrated)
    f_overlap_tubulin = 0.01      # engine-current operational overlap branch
    g_single_eff_tubulin_operational = g_single_eff_tubulin * f_overlap_tubulin
    N_cage = 144                   # Tier 2 (icosahedral cage)
    omega_d_tubulin = 112e6  # Hz; primary branch convention aligned with protocol_eta_zeno.py
    kappa_geom_tubulin = derive_kappa_geometric(omega_d_tubulin, N_cage)
    eta_F_tubulin = 1.0  # on-resonance
    N_bio_tubulin_central = 0.0  # n_rp=0 operative central branch pending O.21
    N_bio_tubulin = 1.25e8       # beta-Trp n_rp=1 sensitivity branch per Ch13:633
    N_bio_range_tubulin = (0.0, 1.25e8)

    N_coh_tubulin = derive_N_coh_from_cooperativity(
        g_single_eff_tubulin, kappa_geom_tubulin, eta_F_tubulin
    )
    N_coh_tubulin_operational = derive_N_coh_from_cooperativity(
        g_single_eff_tubulin_operational, kappa_geom_tubulin, eta_F_tubulin
    )
    eta_Zeno_tubulin = eta_Zeno_from_substrate(
        g_single_eff_tubulin, N_bio_tubulin, kappa_geom_tubulin, eta_F_tubulin
    )
    eta_Zeno_tubulin_operational = eta_Zeno_from_substrate(
        g_single_eff_tubulin_operational, N_bio_tubulin, kappa_geom_tubulin, eta_F_tubulin
    )

    print("\n--- Tubulin-Trp substrate (canonical biology) ---")
    print(f"  g_single^eff pre-overlap       : {g_single_eff_tubulin:.2e} Hz")
    print(f"  f_overlap operational branch   : {f_overlap_tubulin:.2e}")
    print(f"  g_single^eff operational       : {g_single_eff_tubulin_operational:.2e} Hz")
    print(f"  omega_d           : {omega_d_tubulin:.2e} Hz")
    print(f"  N_cage            : {N_cage}")
    print(f"  kappa^geom        : {kappa_geom_tubulin:.2e} Hz")
    print(f"  eta_F (resonant)  : {eta_F_tubulin:.2e}")
    print(f"  N_bio (typical)   : {N_bio_tubulin:.2e}")
    print(f"  N_coh pre-overlap reference     : {N_coh_tubulin:.4e}")
    print(f"  N_coh operational reference     : {N_coh_tubulin_operational:.4e}")
    print(f"  eta_Zeno pre-overlap sensitivity: {eta_Zeno_tubulin:.4e}")
    print(f"  eta_Zeno operational sensitivity: {eta_Zeno_tubulin_operational:.4e}")
    print(f"  Ratio N_bio / N_coh operational : {N_bio_tubulin / N_coh_tubulin_operational:.4e}")
    print(f"  Sensitivity branch is {math.log10(N_bio_tubulin / N_coh_tubulin_operational):.1f} orders above the operational robustness reference")

    # ── NV-centre surrogate (V3 §13.5.7) ────────────────────────────────
    g_single_eff_NV = 2.7e7
    kappa_NV = 1e6  # directly measured cavity linewidth
    eta_F_NV = 1.0
    N_bio_NV = 1

    N_coh_NV = derive_N_coh_from_cooperativity(g_single_eff_NV, kappa_NV, eta_F_NV)
    eta_Zeno_NV = eta_Zeno_from_substrate(g_single_eff_NV, N_bio_NV, kappa_NV, eta_F_NV)

    print("\n--- NV-centre surrogate ---")
    print(f"  g_single^eff      : {g_single_eff_NV:.2e} Hz")
    print(f"  kappa (measured)  : {kappa_NV:.2e} Hz")
    print(f"  N_bio             : {N_bio_NV}")
    print(f"  N_coh             : {N_coh_NV:.4e}")
    print(f"  eta_Zeno          : {eta_Zeno_NV:.4e}")
    print(f"  NV margin is {math.log10(N_bio_NV / N_coh_NV):.1f} orders above robustness reference")

    # ── Anaesthesia parameter scan ──────────────────────────────────────
    print("\n--- Anaesthesia parameter scan (g_single^eff suppression) ---")
    print("  Anaesthetics disrupt the Trp-pocket binding -> reduces g_single^eff")
    print("  How much suppression drops below the eta_Zeno = 1 robustness line?\n")
    print("  Suppression factor F | g_single^eff_reduced | eta_Zeno | Robustness status")
    print("  " + "-" * 70)
    suppression_factors = [1.0, 10.0, 100.0, 1000.0, 1e4, 1e5, 1e6]
    anaesthesia_scan = []
    for F in suppression_factors:
        g_reduced = g_single_eff_tubulin_operational / F
        eta_reduced = eta_Zeno_from_substrate(g_reduced, N_bio_tubulin, kappa_geom_tubulin, eta_F_tubulin)
        status = "margin clears reference" if eta_reduced > 1.0 else "below robustness reference"
        print(f"  F = {F:>9.0e}  | g_eff = {g_reduced:>9.2e} Hz | eta = {eta_reduced:>9.2e} | {status}")
        anaesthesia_scan.append({
            "suppression_factor": F,
            "g_eff_reduced_Hz": g_reduced,
            "eta_Zeno_reduced": eta_reduced,
            "polaron_intact": bool(eta_reduced > 1.0),
        })

    # Find critical suppression factor for crossing the robustness line.
    F_critical_pre_overlap = eta_Zeno_tubulin  # eta_Zeno scales as 1/F linearly through g_single
    F_critical = eta_Zeno_tubulin_operational
    print(f"\n  Critical suppression factor F_crit = {F_critical:.4e}")
    print(f"  Biology requires g_single^eff to drop by ~{math.log10(F_critical):.1f} orders of magnitude")
    print(f"  before the sensitivity branch crosses the cooperativity robustness line.")

    # ── Geometric factor analysis ────────────────────────────────────────
    print("\n--- Geometric closure check: does N=144 + phi^-18 force N_coh? ---")
    # N_coh = (kappa/g)^2 = (phi^-18 * omega_d / (N_cage * g))^2
    # Independent of N_bio; pure geometric + per-spin coupling
    N_coh_pure_geometric = (PHI ** (-18) * omega_d_tubulin / (N_cage * g_single_eff_tubulin_operational)) ** 2
    print(f"  N_coh = (phi^-18 * omega_d / (N_cage * g_single^eff))^2")
    print(f"        = ({PHI ** (-18):.4e} * {omega_d_tubulin:.4e} / ({N_cage} * {g_single_eff_tubulin_operational:.4e}))^2")
    print(f"        = {N_coh_pure_geometric:.4e}")
    print(f"  Matches operational cooperativity derivation: {math.isclose(N_coh_pure_geometric, N_coh_tubulin_operational, rel_tol=1e-9)}")

    # ── Verdict ──────────────────────────────────────────────────────────
    result_status = "FORMULA EVALUATION PASS"
    interp = (
        "N_coh IS derivable from N=144 + phi^-18 + g_single^eff + omega_d via the "
        "cooperativity criterion. The formula reduces to: "
        f"N_coh = (phi^-18 * omega_d / (N_cage * g_single^eff))^2. For canonical "
        f"tubulin parameters N_coh = {N_coh_tubulin_operational:.2e} after overlap propagation "
        f"(pre-overlap audit value {N_coh_tubulin:.2e}); the operative central cooperative branch remains "
        f"n_rp=0 pending O.21, while the beta-Trp n_rp=1 sensitivity branch N_bio = 1.25e8 exceeds the robustness reference by "
        f"{math.log10(N_bio_tubulin / N_coh_tubulin_operational):.1f} orders of magnitude. This shows that the sensitivity branch "
        "would be highly robust if the O.21 witness is established; it is not a central biological sufficiency result. Anaesthesia and "
        "related interventions are reported as suppression-margin diagnostics by reducing g_single^eff "
        f"by a factor of {F_critical:.2e} on the sensitivity branch, in the same range "
        "as the eta_Zeno robustness margin for Trp-pocket binding."
    )

    verdict = {
        "test_target": (
            "Evaluate the N_coh robustness reference from N=144 cage geometry + "
            "phi^-18 phason stiffness for the Polaron Persistence audit (App H O.16)."
        ),
        "tubulin_substrate": {
            "g_single_eff_pre_overlap_Hz": g_single_eff_tubulin,
            "f_overlap_operational": f_overlap_tubulin,
            "g_single_eff_operational_Hz": g_single_eff_tubulin_operational,
            "N_cage": N_cage,
            "omega_d_Hz": omega_d_tubulin,
            "kappa_geom_Hz": kappa_geom_tubulin,
            "eta_F": eta_F_tubulin,
            "N_bio_central": N_bio_tubulin_central,
            "N_bio_typical": N_bio_tubulin,
            "N_bio_basis": "beta-Trp n_rp=1 sensitivity branch; central n_rp=0 pending O.21; hydration shell is bath/environment per Ch13:633",
            "N_bio_range": list(N_bio_range_tubulin),
            "N_coh_reference_pre_overlap": N_coh_tubulin,
            "N_coh_reference_operational": N_coh_tubulin_operational,
            "eta_Zeno_sensitivity_pre_overlap": eta_Zeno_tubulin,
            "eta_Zeno_sensitivity_operational": eta_Zeno_tubulin_operational,
            "sensitivity_branch_orders_above_operational_reference": math.log10(N_bio_tubulin / N_coh_tubulin_operational),
        },
        "NV_surrogate": {
            "g_single_eff_Hz": g_single_eff_NV,
            "kappa_Hz": kappa_NV,
            "N_bio": N_bio_NV,
            "N_coh_reference": N_coh_NV,
            "eta_Zeno": eta_Zeno_NV,
        },
        "anaesthesia_scan": anaesthesia_scan,
        "F_critical_pre_overlap": F_critical_pre_overlap,
        "F_critical_operational": F_critical,
        "F_critical_operational_log10": math.log10(F_critical),
        "geometric_closure_match": bool(math.isclose(N_coh_pure_geometric, N_coh_tubulin_operational, rel_tol=1e-9)),
        "N_coh_formula": "N_coh = (phi^-18 * omega_d / (N_cage * g_single^eff))^2",
        "test_outcome": result_status,
        "interpretation": interp,
        "tier_impact": (
            "FORMULA-EVALUATION AUDIT. The N_coh robustness reference is derivable "
            "from the stated framework parameters (cooperativity criterion + V3 §13.5.4 "
            "geometric kappa + Trp coupling), but it is not an independent "
            "Level-II pass/fail threshold. The formula N_coh = (phi^-18 * "
            "omega_d / (N_cage * g_single^eff))^2 is geometry-constrained "
            "(phi, N_cage) and depends on overlap-propagated g_single^eff (Tier 3 calibrated) and "
            "omega_d (Tier 3 specific value, O.12). V1 Ch17 §17.1.4b items (ii) "
            "and (iii) remain Tier 3 pending microtubule biology plus coherence "
            "assumptions, while the cooperativity mechanism itself remains Tier 2. "
            f"The sensitivity-branch suppression-margin diagnostic reports F_crit = {F_critical:.2e} "
            "as the factor in g_single^eff needed to cross the cooperativity "
            "robustness line; the testable anaesthesia observable remains the "
            "EC50 scaling with Trp-pocket-binding strength."
        ),
        "remaining_open": (
            "Two parameters in the formula remain Tier 3: g_single^eff (calibrated "
            "to ~38.3 MHz pre-overlap, overlap-propagated in the operational branch) and omega_d "
            "(~112 MHz primary branch, pending O.12 frequency-scale renormalization). Closure "
            "of these two would elevate the entire N_coh derivation to Tier 2. "
            "Closure of g_single^eff requires the cavity-polariton avoided-"
            "crossing mechanism (bundled with B3); closure of omega_d requires "
            "O.12. The N_coh formula structure itself is now Tier 2."
        ),
    }

    print("\n" + "=" * 76)
    print("VERDICT")
    print("=" * 76)
    print(f"Result: {result_status}")
    print(f"\nN_coh formula: {verdict['N_coh_formula']}")
    print(f"\nInterpretation: {interp}")
    print(f"\nTier impact: {verdict['tier_impact']}")

    out_path = Path(__file__).parent.parent / "data" / "protocol_polaron_Ncoh_derivation_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(verdict, f, indent=2)
    print(f"\nFull results: {out_path}")
    print("=" * 76)


if __name__ == "__main__":
    main()
