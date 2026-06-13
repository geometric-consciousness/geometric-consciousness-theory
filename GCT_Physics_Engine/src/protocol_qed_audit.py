#!/usr/bin/env python3
"""
protocol_qed_audit.py — QED Precision Audit
============================================================
Verifies GCT predictions for:
  1. Muon anomalous magnetic moment
  2. Electron g-2 consistency check
  3. Hydrogen Lamb Shift correction

Muon g-2 uses A3 measured low-energy alpha as a precision-comparison input.
WP2025 is the HVP arbitration baseline, not direct support for the GCT
correction.
"""

import json
import sys
import numpy as np
from pathlib import Path


from gct_precision_qed import (
    compute_anomalous_moment,
    compute_lamb_shift_correction,
    N_LEPTON_CHANNELS,
    N_MUON_HARMONIC,
)
from gct_utils import get_output_path, C


def derive_phason_activation_threshold():
    """
    Kinematic Depinning Threshold Derivation
    -------------------------------------------------
    The N_channels = 5 lattice correction for the anomalous magnetic moment 
    requires the lepton to activate a closed phason loop inside the I_h-closed cage.
    To emit this loop, the lepton must possess enough rest-mass energy to 
    excite the fundamental acoustic cage resonance (the N=11 harmonic).
    
    E_res = m_e * phi^11  (~101.69 MeV)
    """
    PHI = float(C.PHI)
    # C.M_E is stored in MeV/c^2 (see gct_constants.yaml anchors block).
    # Keep the resonance energy in MeV for the downstream JSON field
    # `kinematic_threshold_mev`.
    m_e = float(C.M_E)  # MeV

    # Fundamental cage resonance energy (depinning threshold)
    e_res = m_e * (PHI ** 11)
    
    # Energy gap to activate the loop
    e_gap = e_res - m_e
    kinematic_ratio = e_gap / m_e
    
    return {
        "electron_mass_mev": m_e,
        "n11_resonance_mev": e_res,
        "activation_gap_mev": e_gap,
        "kinematic_deficit_ratio": kinematic_ratio
    }


def run_qed_audit() -> dict:
    print("=" * 65)
    print("GCT Protocol — QED Precision Audit")
    print("=" * 65)

    results: dict = {}

    # ─────────────────────────────────────────────────────────────
    # 1. Muon g-2
    # ─────────────────────────────────────────────────────────────
    from gct_utils import C
    # Experimental combined (Fermilab E989 final + BNL E821):
    val_exp = getattr(C, 'MUON_G2_EXP_VALUE', 116_592_070.5e-11)
    err_exp = getattr(C, 'MUON_G2_EXP_UNCERTAINTY', 14.8e-11)
    # SM Theory: White Paper 2025 (Aliberti et al. arXiv:2505.21476)
    # uses the consolidated lattice-QCD HVP average after data-driven
    # LO-HVP evaluations became too mutually tense for a clean combination.
    val_sm  = float(C.MUON_G2_SM_WP2025)
    err_sm  = float(C.MUON_G2_SM_WP2025_UNCERT)

    gap          = val_exp - val_sm
    sigma_before = gap / np.sqrt(err_exp**2 + err_sm**2)

    gct_mu  = compute_anomalous_moment("muon")
    residual    = val_exp - gct_mu["total"]
    sigma_after = residual / np.sqrt(err_exp**2 + err_sm**2)

    print(f"\n{'─'*65}")
    print(f"1.  Muon Anomalous Magnetic Moment  a_μ = (g−2)/2")
    print(f"{'─'*65}")
    print(f"    Experiment  (Fermilab E989 final + BNL E821) : {val_exp:.11e}  ± {err_exp:.1e}")
    print(f"    SM Theory   (WP 2025 Aliberti et al. arXiv:2505.21476): {val_sm:.11e}  ± {err_sm:.1e}")
    print(f"    Discrepancy                                  : {gap:.5e}  ({sigma_before:.2f}σ)")
    print()
    print(f"    RT Geometry derivation:")
    print(f"      N_channels = (4·{30}−3·{20})/{12} = {N_LEPTON_CHANNELS}")
    print(f"      Formula    : {gct_mu['formula']}")
    print(f"      Alpha input: A3 measured low-energy alpha (bare alpha_GCT audited separately)")
    print(f"      GCT Δaμ    : {gct_mu['gct_part']:.5e}")
    print(f"      GCT total  : {gct_mu['total']:.11e}")
    print()
    print(f"    Residual (Exp − GCT) : {residual:.5e}  ({sigma_after:.2f}σ)")

    print(f"\n    [HVP synthesis status]")
    print(f"    Under the consolidated SM theory the experiment-SM gap sits at")
    print(f"    ~{sigma_before:.1f}σ. The GCT (α/π)³/5 correction sits above")
    print(f"    the consolidated SM by approximately {abs(sigma_after):.1f}σ — disposition:")
    print(f"    Tension under WP2025; falsification conditional on long-term")
    print(f"    HVP-synthesis arbitration (App R §R.2 / App V §P.5).")

    verdict_mu = "PASS" if abs(sigma_after) <= 0.6 else "TENSION"
    print(f"    Verdict              : {verdict_mu}")

    results["muon_g2"] = {
        "experiment":       val_exp,
        "sm_theory":        val_sm,
        "gap":              gap,
        "sigma_before":     float(sigma_before),
        "gct_correction":   gct_mu["gct_part"],
        "gct_total":        gct_mu["total"],
        "residual":         residual,
        "sigma_after":      float(sigma_after),
        "N_channels":       N_LEPTON_CHANNELS,
        "formula":          gct_mu["formula"],
        "alpha_anchor":     "A3 measured low-energy alpha; bare GCT alpha remains O.19/O.5.",
        "verdict":          verdict_mu,
    }

    # ─────────────────────────────────────────────────────────────
    # 2. Electron g-2 consistency check
    # ─────────────────────────────────────────────────────────────
    gct_e = compute_anomalous_moment("electron")
    
    print(f"\n{'─'*65}")
    print(f"2.  Electron g-2 Consistency (Kinematic Threshold Derivation)")
    print(f"{'─'*65}")
    
    thresh = derive_phason_activation_threshold()
    print(f"    Fundamental cage resonance (N=11) : {thresh['n11_resonance_mev']:.2f} MeV")
    print(f"    Electron rest mass (N=0)          : {thresh['electron_mass_mev']:.3f} MeV")
    print(f"    Activation deficit ratio          : ~{thresh['kinematic_deficit_ratio']:.0f}x too light")
    
    print(f"\n    GCT lattice correction : {gct_e['gct_part']:.1e}  (exact zero)")
    print(f"    Reason : The electron is kinematically forbidden from emitting")
    print(f"             a closed phason loop. It lacks the {thresh['activation_gap_mev']:.1f} MeV gap")
    print(f"             required to depin the acoustic cage resonance.")
    print(f"             → Electron QED precision ({10**-12:.0e}) unaffected.")
    electron_g2_tier = (
        "Tier 2 kinematic-threshold mechanism + Tier 3 threshold exponent; "
        "alpha-input contingent"
    )
    print(f"    Verdict: CONSISTENT ({electron_g2_tier})")

    results["electron_g2"] = {
        "gct_correction": 0.0,
        "kinematic_threshold_mev": thresh['n11_resonance_mev'],
        "electron_deficit_ratio": thresh['kinematic_deficit_ratio'],
        "tier": electron_g2_tier,
        "verdict": "CONSISTENT",
        "explanation": (
            f"Kinematically forbidden (requires >{thresh['activation_gap_mev']:.1f} MeV gap to depin "
            f"N=11 resonance). Electron is ~{thresh['kinematic_deficit_ratio']:.0f}x too light to activate lattice loops."
        ),
    }

    # ─────────────────────────────────────────────────────────────
    # 2b. Tau g-2 prediction (above-threshold lepton; analogous to muon)
    # ─────────────────────────────────────────────────────────────
    tau_mass_mev = float(C.M_TAU_OBS)

    # By the same kinematic-threshold argument that gates the electron at
    # zero correction (mass from SSOT << N=11 resonance), the tau
    # (mass from SSOT >> N=11 resonance) is above threshold and the
    # closed-phason-loop correction applies. The mechanism is the same
    # 5-channel A_5 averaging that gives the muon prediction; the
    # numerical value is therefore the same form-factor (1/5)(alpha/pi)^3
    # ≈ 250.65 x 10^-11, with Tier 3 caveats on the channel-count universality
    # across leptons (see Open Problem registry — tau-coupling channel
    # generation-dependence is a candidate sub-problem of O.26).
    gct_tau = compute_anomalous_moment("tau")

    print(f"\n{'─'*65}")
    print(f"2b. Tau g-2 Prediction (Above-Threshold Lepton)")
    print(f"{'─'*65}")
    print(f"    Tau rest mass                     : {tau_mass_mev:.2f} MeV")
    print(f"    Above N=11 threshold              : YES (~17.5x above {thresh['n11_resonance_mev']:.1f} MeV)")
    print(f"    GCT lattice correction            : {gct_tau.get('gct_part', 0.0):.3e}")
    print(f"    Form-factor universality          : Tier 3 (assumes same 5-channel A_5 averaging as muon)")
    print(f"    Current PDG bound on Delta_a_tau  : ~1e-1 (loose; FCC-ee target ~1e-6)")
    print(f"    Predicted Delta_a_tau             : {gct_tau.get('gct_part', 0.0):.3e}")
    print(f"    Verdict: UNDETECTABLE-AT-CURRENT-SENSITIVITY (Tier 2 mechanism + Tier 3 form-factor universality)")

    results["tau_g2"] = {
        "gct_correction": gct_tau.get('gct_part', 0.0),
        "above_threshold_mev_ratio": tau_mass_mev / thresh['n11_resonance_mev'],
        "form_factor_assumption": (
            "Assumes the same (1/5)(alpha/pi)^3 form-factor as the muon prediction; "
            "channel-count universality across leptons is Tier 3, candidate sub-problem of O.26"
        ),
        "current_pdg_bound": 1e-1,
        "fcc_ee_target_sensitivity": 1e-6,
        "verdict": "UNDETECTABLE-AT-CURRENT-SENSITIVITY",
        "explanation": (
            f"Tau ({tau_mass_mev:.2f} MeV) is ~17.5x above the N=11 activation threshold "
            f"({thresh['n11_resonance_mev']:.1f} MeV), so the closed-phason-loop "
            f"correction applies. Predicted Delta_a_tau equals the muon value under "
            f"5-channel A_5 form-factor universality (Tier 3 assumption). Current PDG "
            f"bound (~1e-1) is 8 OOM weaker than the prediction; even the FCC-ee tau-g-2 "
            f"program target sensitivity (~1e-6) is 3 OOM short. Prediction is real "
            f"but currently unfalsifiable on operational grounds."
        ),
    }

    # ─────────────────────────────────────────────────────────────
    # 3. Lamb Shift
    # ─────────────────────────────────────────────────────────────
    lamb = compute_lamb_shift_correction()

    print(f"\n{'─'*65}")
    print(f"3.  Hydrogen Lamb Shift Correction")
    print(f"{'─'*65}")
    print(f"    Standard 2S½–2P½ Lamb Shift : {lamb['standard_lamb_MHz']:.3f} MHz")
    print(f"    Suppression factor           : {lamb['suppression_factor']:.3e}")
    print(f"      = (l_Planck / a_Bohr)³")
    print(f"    GCT correction               : {lamb['gct_correction_MHz']:.3e} MHz")
    print(f"    Verdict: {lamb['verdict']}")
    print(f"    Note: {lamb['note']}")

    results["lamb_shift"] = lamb

    # ─────────────────────────────────────────────────────────────
    # Save JSON
    # ─────────────────────────────────────────────────────────────
    def _serialise(v):
        if isinstance(v, np.floating):
            return float(v)
        if isinstance(v, np.integer):
            return int(v)
        return v

    out_pass = verdict_mu == "PASS"
    out: dict = {
        "pass": bool(out_pass),
        "pass_compatible": bool(out_pass),
    }
    for sec, content in results.items():
        out[sec] = {k: _serialise(v) for k, v in content.items()}

    out_path = get_output_path("protocol_qed_audit_results.json")
    with open(out_path, "w") as fp:
        json.dump(out, fp, indent=2)

    print(f"\n{'=' * 65}")
    print(f"Report saved → {out_path}")
    return results


if __name__ == "__main__":
    run_qed_audit()
