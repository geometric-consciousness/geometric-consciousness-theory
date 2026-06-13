#!/usr/bin/env python3
"""
protocol_preregistration.py — Falsification Registry
=============================================================
Records all numerical predictions of the GCT Physics Engine in
`config/falsification_thresholds.json` and
`data/protocol_preregistration_results.json` before experimental data arrives.

Each entry specifies:
  prediction   : the central GCT value
  tolerance    : the 5-sigma experimental window (or theory error)
  status       : "LOCKED" — held fixed for the stated falsification rule
  verdict_rule : what counts as a pass/fail
"""

import json
import sys
from pathlib import Path
from gct_utils import C, get_output_path


# ── Dynamic values from the SSOT ────────────────────────────────────────────
import numpy as np

_alpha     = float(getattr(C, "ALPHA_OBS", 1.0 / 137.035999177))
_alpha_pi  = _alpha / np.pi
_M_PLANCK_GEV = (
    (float(C.HBAR_SI) * float(C.C) / float(C.G_SI)) ** 0.5
    * float(C.C) ** 2
    / (float(C.EV_TO_J) * 1.0e9)
)
_ELECTRON_MASS_OBS_MEV = 0.51099895069
_predicted_m_e = (
    _M_PLANCK_GEV
    * 1.0e3
    * float(C.PHI) ** -107
    * (1.0 - 5.0 * (1.0 / float(C.ALPHA_INV_OBS)))
)

# RT channel count from icosahedral edge-face enumeration: N_chan = (4·30 − 3·20)/12 = 5
_N_chan  = 5
_Δa_gct = (1.0 / _N_chan) * _alpha_pi**3   # Muon g-2 lattice correction

PROTOCOL_A_PRIME_AUTHORITATIVE_SOURCE = "App V P.8 + Ch13 §13.3.5"

PROTOCOL_A_PRIME_REQUIRED_SYSTEMATICS = tuple(f"S{i}" for i in range(7))


def evaluate_protocol_a_prime_f1(observation):
    """Evaluate Protocol A-Prime F1 using the canonical joint-null rule.

    Authoritative preregistration source is App V P.8 + Ch13 §13.3.5; this
    engine config mirrors the canonical rule. T2 ratio is O.23/O.24 readout
    context, not a falsification threshold.
    """
    observed = dict(observation)
    branch_a_peak = bool(observed.get("branch_a_112mhz_peak_detected", False))
    branch_b_peak = bool(observed.get("branch_b_42mhz_peak_detected", False))
    anti_zeno_sign = bool(observed.get("anti_zeno_sign_150mhz_detected", False))
    chirality_contrast = bool(observed.get("chirality_contrast_detected", False))
    scan_complete = bool(observed.get("scan_band_32_200mhz_complete", False))
    spacing_khz = float(observed.get("max_scan_spacing_khz", float("inf")))
    p_ciss_measured = bool(observed.get("p_ciss_measured_pre_unblinding", False))
    p_ciss_net = observed.get("p_ciss_net")
    completed_systematics = set(observed.get("completed_systematics", ()))

    systematics_ok = set(PROTOCOL_A_PRIME_REQUIRED_SYSTEMATICS).issubset(completed_systematics)
    scan_ok = scan_complete and spacing_khz <= 5.0
    ciss_value = None if p_ciss_net is None else float(p_ciss_net)
    ciss_clean = p_ciss_measured and ciss_value is not None and ciss_value >= 0.1
    ciss_sensitivity_limited = (
        p_ciss_measured and ciss_value is not None and 0.025 <= ciss_value < 0.1
    )
    ciss_below_floor = p_ciss_measured and ciss_value is not None and ciss_value < 0.025
    joint_null = (
        not branch_a_peak
        and not branch_b_peak
        and not anti_zeno_sign
        and not chirality_contrast
    )
    acceptance_ready = scan_ok and systematics_ok and p_ciss_measured and ciss_value is not None

    if not acceptance_ready:
        disposition = "INCOMPLETE_ACCEPTANCE_CHECKS"
    elif ciss_below_floor:
        disposition = "NOT_FALSIFYING_P_CISS_BELOW_FLOOR"
    elif ciss_sensitivity_limited:
        disposition = "SENSITIVITY_LIMITED_REPOWER_REQUIRED"
    elif ciss_clean and joint_null:
        disposition = "FALSIFIED_F1_JOINT_BRANCH_A_B_NULL"
    else:
        disposition = "NOT_FALSIFIED_SIGNAL_OR_CONTROL_PRESENT"

    return {
        "authoritative_preregistration_source": PROTOCOL_A_PRIME_AUTHORITATIVE_SOURCE,
        "joint_null": joint_null,
        "acceptance_ready": acceptance_ready,
        "scan_ok": scan_ok,
        "systematics_ok": systematics_ok,
        "p_ciss_value_recorded": ciss_value is not None,
        "ciss_clean_falsification_possible": ciss_clean,
        "ciss_sensitivity_limited": ciss_sensitivity_limited,
        "ciss_below_floor": ciss_below_floor,
        "f1_falsified": disposition == "FALSIFIED_F1_JOINT_BRANCH_A_B_NULL",
        "disposition": disposition,
    }


def _load_muon_g2_wp2025_disposition():
    """Read the WP2025 muon g-2 disposition from the independent verifier."""
    result_path = Path(__file__).resolve().parents[1] / "verify_independent" / "results" / "g2_muon.json"
    fallback_gap = float(C.MUON_G2_EXP_VALUE) - float(C.MUON_G2_SM_WP2025)
    fallback_sigma = (float(C.MUON_G2_SM_WP2025_UNCERT) ** 2 + float(C.MUON_G2_EXP_UNCERTAINTY) ** 2) ** 0.5
    fallback_disposition = (
        "Tier 2 mechanism + Tier 3 1/5 coefficient + A3 + Tier 4 calibration-survival conjecture (HVP arbitration); "
        "Tension under WP2025; falsification conditional on long-term HVP-synthesis arbitration"
    )
    fallback_precision = (
        "WP2025 gap (a_exp - a_SM) = +37.5e-11 at 0.59 sigma "
        "(no significant anomaly); GCT prediction overshoots the gap by ~6.7x."
    )
    if not result_path.exists():
        return fallback_gap, fallback_sigma, fallback_disposition, fallback_precision

    data = json.loads(result_path.read_text(encoding="utf-8"))
    extra = data.get("extra", {})
    gap = float(data.get("observed", fallback_gap))
    sigma = float(extra.get("wp2025_gap_sigma_x_10_11", fallback_sigma / 1e-11)) * 1e-11
    disposition = str(data.get("tier", fallback_disposition))
    precision = str(data.get("app_r_precision_str", fallback_precision))
    return gap, sigma, disposition, precision


_WP2025_GAP, _WP2025_GAP_SIGMA, _MUON_G2_DISPOSITION, _MUON_G2_PRECISION = (
    _load_muon_g2_wp2025_disposition()
)


REGISTRY = {
    "meta": {
        "theory_name": "Geometric Consciousness Theory (GCT)",

        "claim":       (
            "5-postulate (P1-P5) + A1 m_e dimensional anchor for the bare "
            "topology/exponent sub-sector, A2 alpha_2^{-1}(M_GUT) Tier-3 "
            "calibrated native-RGE boundary, and A3 measured low-energy "
            "alpha for corrected precision-comparison rows; the "
            "zero-continuous-free-parameter claim applies only to the bare "
            "topology/exponent sub-sector."
        ),
    },

    # ──────────────────────────────────────────────────────────────────────
    "fine_structure_constant": {
        "prediction":     137.0303,
        "formula":        "360·phi^-2·(1 − 1/(2·N))",
        "experiment":     137.035999178,
        "tolerance_ppm":  50,
        "verdict_rule":   "|pred − obs| / obs < 50e-6",
        "status":         "LOCKED",
    },

    # ──────────────────────────────────────────────────────────────────────
    "electron_mass_mev": {
        "prediction":     _predicted_m_e,
        "formula":        "M_Planck · phi^-107 · (1 − 5·alpha)",
        "experiment":     _ELECTRON_MASS_OBS_MEV,
        "residual_ppm":   (_predicted_m_e - _ELECTRON_MASS_OBS_MEV) / _ELECTRON_MASS_OBS_MEV * 1e6,
        "tolerance_ppm":  1000,
        "verdict_rule":   "|pred − obs| / obs < 1000e-6",
        "status":         "LOCKED",
    },

    # ──────────────────────────────────────────────────────────────────────
    "muon_g_minus_2": {
        "prediction_correction": float(_Δa_gct),
        "formula":             f"(1/{_N_chan})·(alpha_A3/pi)^3",
        "alpha_anchor":        "A3 measured low-energy alpha; bare GCT alpha remains O.19/O.5.",
        "experiment_gap":      float(_WP2025_GAP),
        "wp2025_gap":          float(_WP2025_GAP),
        "target_gap":          float(_WP2025_GAP),
        "tolerance_1sigma":    float(_WP2025_GAP_SIGMA),
        "verdict_rule":        "WP2025 arbitration: no anomaly-gap closure; report pred_correction vs wp2025_gap and HVP-synthesis disposition",
        "disposition_text":    _MUON_G2_DISPOSITION,
        "wp2025_precision_summary": _MUON_G2_PRECISION,
        "bmw_contingency":     "Tension under WP2025; falsification conditional on long-term HVP-synthesis arbitration",
        "status":              "LOCKED",
    },

    # ──────────────────────────────────────────────────────────────────────
    "lamb_shift_correction": {
        "prediction_MHz":  0.0,
        "formula":         "Suppressed by (l_Planck / a_Bohr)^3 ~ 2.9e-74",
        "verdict_rule":    "GCT contribution < 1 Hz (unmeasurable)",
        "status":          "LOCKED",
    },

    # ──────────────────────────────────────────────────────────────────────
    "xrism_line_fwhm_ev": {
        "prediction":      9.7,
        "formula":         "sqrt((E0·v_turb/c)^2 + sigma_inst^2) · 2.355",
        "contrast_fwhm":   36.6,   # Standard CDM
        "falsification":   "Full Protocol C package: terminal no-line non-detection at the Bulbul-level empirical-derived floor Gamma <= 2.0e-28 s^-1 in >=94 Ms equivalent stacked exposure, OR deconvolved intrinsic line-width residual W_int > 20 eV after instrument and registered kinematic/turbulence deconvolution, OR morphology failing stress-gated rho_above_sigma_crit^2 by Delta chi^2 >= 9 vs smooth rho and smooth rho^2 templates inside the numerically frozen sigma_crit = 0.53 keV cm^-3 aperture. The 26 Ms / Gamma <= 3.8e-28 s^-1 stack remains a morphology-linewidth milestone; background-limited Gamma <= 1.2e-30 s^-1 is theoretical, not operative.",
        "status":          "LOCKED",
    },

    # ──────────────────────────────────────────────────────────────────────
    "chirality": {
        "prediction":        "Net chirality = 1 per generation",
        "mechanism":         "Domain-wall fermion at quasicrystal boundary",
        "simulation_result": "N_L − N_R = 1 (Fibonacci chain N=89)",
        "status":            "LOCKED",
    },

    # ──────────────────────────────────────────────────────────────────────
    # ──────────────────────────────────────────────────────────────────────
    "imp01_pipeline_gate": {
        "claim_registry_claim_id": "C_IMP01_PIPELINE_GATE",
        "prediction_w_behavior":  "continuous phantom-side IMP-01 curve; no literal direct crossing in the scanned window",
        "diagnostic_cpl_target":  "headline_run (w0_CPL_fit, wa_CPL_fit, z_cross_CPL_fit) is a projection diagnostic, not a DESI support gate",
        "tier":                   3,
        "falsification":          "DESI DR2 + Euclid DR1 produce a 3sigma+ CPL detection of w_0 > -1 AND w_a < 0 with no GCT-native biogenic-channel likelihood or fingerprint closure",
        "status":                 "ACTIVE_TENSION_PENDING_NATIVE_LIKELIHOOD",

    },

    "shapley_biogenic_dipole": {
        "prediction_delta_w_w":      2.0e-4,
        "alignment_l_deg":           311.0,
        "alignment_b_deg":           30.0,
        "alignment_tolerance_deg":   30.0,
        "amplitude_basis":           (
            "V7' Class-2 envelope cosmic-mean |Delta w(z=0.28)| in "
            "[2, 5] x 10^-5 (Ch14 §14.6.3) x realistic biogenic-"
            "overdensity factor delta_bio in [1, 3] at Shapley scale "
            "(Local Sheet to Laniakea)"
        ),
        "mechanism":                 "Biogenic phason vacuum strain Shapley orientation",
        "tier":                      3,
        "falsification":             (
            "Post-Roman successor mission (or DESI Y10+ extended "
            "spatial-mapping program) finds no dipole amplitude "
            ">= 2e-4 aligned within +/-30 deg of Shapley at > 3sigma"
        ),
        "experiment":                "Post-Roman successor (or DESI Y10+ extended spatial-w(z) mapping)",
        "timeframe":                 "Post-Roman successor",
        "status":                    "SHAPLEY_DIPOLE_SPECIFICATION_AVAILABLE",

    },
    "pta_l6_anisotropy": {
        "prediction_delta_gamma_max": 0.00017307,
        "prediction_c6_c0":           2.92e-08,
        "mechanism":    "Icosahedral vacuum anisotropy (phason-graviton limit)",
        "verdict_rule": (
            "IMMEDIATE ACTION — Joint Bayesian analysis of NANOGrav 15yr + "
            "PPTA DR3 + EPTA DR2 using 15-angle icosahedral mask and "
            "spherical harmonic decomposition. Positive detection: "
            "combined C_6/sigma(C_6) >= 3.0."
        ),
        "immediate_datasets":   ["NANOGrav 15yr", "PPTA DR3", "EPTA DR2"],
        "immediate_sensitivity": "sigma(C_6) ~ 3e-3 (~8000 pulsar pairs combined)",
        "preregistration_required": True,
        "preregistration_status":   "PTA anisotropy protocol specified for external deposit",
        "decision_criterion":       "C6 / sigma(C6) >= 3.0",
        "status":   "PTA anisotropy analysis specification available",
        "priority": "HIGHEST_LEVERAGE_NEAR_TERM",
    },

    # ──────────────────────────────────────────────────────────────────────
    "neutrino_mass_sum": {
        "prediction": 0.0853,
        "falsification": "Fork A canonical registered band: the phason coupling mechanism (m₁ = mₑ·φ⁻³⁶) is definitively excluded if a pre-registered CMB+BAO+LSS likelihood finds Σmν < 0.075 eV at definitive precision or Σmν > 0.15 eV. The lower edge sits deliberately above the normal-ordering oscillation floor near 0.059 eV, so the gate fires on NO-allowed values that still definitively exclude the 0.0853 eV floor; the upper edge brackets the inverted/high-mass branch. DESI 2024 Σmν < 0.072 eV and DESI DR2 Σmν < 0.064 eV are TENSION, not falsification, under this band.",
        "falsification_band_eV_lower": 0.075,
        "falsification_band_eV_upper": 0.15,
        "survival_gate_eV": 0.10,
        "desi_2024_disposition": "TENSION under the registered 0.075/0.15 eV band",
        "status": "LOCKED",
        "euclid_dr1_pre_registration_rule": "Public pre-registration must occur before first Euclid DR1 weak-lensing power spectrum unblinding.",
        "osf_template": {
            "a": "prediction: Σmν = 0.0853±0.0003 eV, Normal Ordering",
            "b": "primary analysis: Euclid weak-lensing + galaxy clustering joint analysis",
            "c": "falsification: Σmν < 0.075 eV at definitive precision OR Σmν > 0.15 eV",
            "d": "blinding: pre-registration before data release",
            "e": "secondary: Σmν > 0.10 eV at 3σ keeps the biogenic-DE survival branch active; DESI 2024 <0.072 eV is tension only"
        }
    },

    # ──────────────────────────────────────────────────────────────────────
    "nv_center_chiral_proxy": {
        "authoritative_preregistration_source": PROTOCOL_A_PRIME_AUTHORITATIVE_SOURCE,
        "engine_config_mirror": (
            "This entry mirrors App V P.8 and Ch13 §13.3.5. The F1 decision "
            "rule is the joint Branch A + Branch B null after the required "
            "scan, controls, chirality comparison, and per-cap P_CISS acceptance."
        ),
        "readout_context": (
            "T2_chiral / T2_achiral is an O.23/O.24 peak-amplitude readout "
            "context, not the Protocol A-Prime falsification threshold."
        ),
        "readout_reference": {
            "observable": "T2_chiral / T2_achiral",
            "context": "O.23/O.24 protected-subspace amplitude readout only",
            "falsification_role": "NONE"
        },
        "prediction_branch_A_MHz": 112.0,
        "prediction_branch_A_window_MHz": [102.0, 122.0],
        "prediction_branch_B_MHz": 42.0,
        "prediction_branch_B_window_MHz": [32.0, 52.0],
        "required_scan_band_MHz": [32.0, 200.0],
        "max_scan_spacing_kHz": 5.0,
        "anti_zeno_control_MHz": 150.0,
        "chirality_control": "R-vs-S enantiomer measurement required",
        "per_cap_P_CISS_requirement": (
            "P_CISS^net measured pre-unblinding on each cap; >=0.1 at >=5sigma "
            "across all 50 caps for clean F1, 0.025-0.1 sensitivity-limited, "
            "<0.025 not falsifying."
        ),
        "mechanism": "CISS-dependent protected-subspace Zeno lock; chirality requirement of GCT biophysics",
        "verdict_rule": (
            "F1 = joint Branch A + B null. Protocol A-Prime F1 is falsified "
            "only if BOTH no peak is detected in the Branch A 112 +/- 10 MHz "
            "window and no peak is detected in the Branch B 42 +/- 10 MHz "
            "window across the required 32-200 MHz scan with <=5 kHz spacing, "
            "S0-S7 acceptance checks, no 150 MHz anti-Zeno sign, no R-vs-S "
            "chirality contrast, measured pre-unblinding per-cap P_CISS, and "
            "post-transfer CISS retention on the h-BN/NV process flow meeting "
            "the clean-falsification floor. A single-branch null does "
            "not falsify. Peak-amplitude magnitude is O.23/O.24 readout "
            "context, not a falsification threshold."
        ),
        "evaluation_function": "evaluate_protocol_a_prime_f1",
        "dataset":   "NV centres in diamond with controlled h-BN chirality capping",
        "timeline":  "2-5 years (established nanofabrication technology)",
        "status":    "TIER_2_PREDICTION — execution protocol specified",
        "priority":  "HIGH — non-biological validation of core CISS mechanism",
    },

    # ──────────────────────────────────────────────────────────────────────
    "directional_bell_inequality": {
        "prediction": "Icosahedral violation of rotational isotropy",
        "mechanism": "Anisotropic entanglement collapse due to 10 three-fold vacuum axes and c-anisotropy at phi^-18",
        "alignment_mask": "15-angle icosahedral mask (identical to PTA l=6 prediction)",
        "falsification": "Isotropic Bell inequality violation across all baselines -> GCT excluded",
        "status": "BELL_TEST_SPECIFICATION_AVAILABLE"
    },
}


# ── Write files ──────────────────────────────────────────────────────────────
_SRC_DIR  = Path(__file__).resolve().parent
_CONFIG_DIR = _SRC_DIR.parent / "config"
_CONFIG_DIR.mkdir(parents=True, exist_ok=True)

_paths = [
    _CONFIG_DIR / "falsification_thresholds.json",
]

if __name__ == "__main__":
    print("=" * 60)
    print("GCT Protocol — Preregistration Lock")
    print("=" * 60)

    for p in _paths:
        with open(p, "w") as fp:
            json.dump(REGISTRY, fp, indent=4)
        print(f"Registry saved → {p}")

    print("\nLocked predictions:")
    for key, val in REGISTRY.items():
        if key == "meta":
            continue
        pred = val.get("prediction", val.get("prediction_correction",
               val.get("prediction_MHz", val.get("prediction", "—"))))
        status = val.get("status", "—")
        print(f"  {key:<30}  {str(pred):<20}  [{status}]")

    # Also write a machine-readable output to data/
    ci_output = {"locked": True, "pass": True, "n_predictions": len(REGISTRY) - 1}
    with open(get_output_path("protocol_preregistration_results.json"), "w") as fp:
        json.dump(ci_output, fp, indent=2)
    print("Output written to data/protocol_preregistration_results.json")
