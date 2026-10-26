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
import math
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

PROTOCOL_A_PRIME_AUTHORITATIVE_SOURCE = "App PRG P.8 + Ch13 §13.3.5"

PROTOCOL_A_PRIME_REQUIRED_SYSTEMATICS = tuple(f"S{i}" for i in range(8))

PROTOCOL_A_PRIME_SCAN_START_MHZ = 32.0
PROTOCOL_A_PRIME_SCAN_STOP_MHZ = 200.0
PROTOCOL_A_PRIME_BASELINE_STEP_KHZ = 5.0
PROTOCOL_A_PRIME_RAW_SHOTS_PER_BIN_CELL = round(((5.6 + 1.48) / 0.10) ** 2, 2)
PROTOCOL_A_PRIME_CELLS = (
    "L-chiral / RF frequency scan",
    "L-chiral / matched sham-no-drive",
    "R-chiral / RF frequency scan",
    "R-chiral / matched sham-no-drive",
    "achiral-racemic / RF frequency scan",
    "achiral-racemic / matched sham-no-drive",
)


def protocol_a_prime_scan_budget(cell_count=len(PROTOCOL_A_PRIME_CELLS)):
    """Return the exact baseline scan budget for the registered 3x2 design.

    The frequency grid is half-open, [32, 200) MHz.  The six-cell factorial is
    an experimental-design premise, not a physics derivation; budgets scale
    linearly with ``cell_count``.  The 5 kHz baseline is allowed only when it
    resolves half the effective linewidth, so longer measured T2_eff values
    require a finer grid and a fresh multiplicity/power budget.
    """
    span_khz = int(round((PROTOCOL_A_PRIME_SCAN_STOP_MHZ - PROTOCOL_A_PRIME_SCAN_START_MHZ) * 1000.0))
    bins = span_khz // int(PROTOCOL_A_PRIME_BASELINE_STEP_KHZ)
    bin_cells = bins * int(cell_count)
    executable_shots_per_bin_cell = math.ceil(PROTOCOL_A_PRIME_RAW_SHOTS_PER_BIN_CELL)
    raw_total_shots = int(round(PROTOCOL_A_PRIME_RAW_SHOTS_PER_BIN_CELL * bin_cells))
    executable_total_shots = executable_shots_per_bin_cell * bin_cells
    cadence_hz = 1000.0
    return {
        "grid_interval_MHz": "[32, 200)",
        "grid_endpoint_convention": "half-open; 200 MHz excluded",
        "baseline_step_kHz": PROTOCOL_A_PRIME_BASELINE_STEP_KHZ,
        "frequency_bins_per_cell": bins,
        "experimental_design_premise": "3 substrate states x 2 acquisition states",
        "primary_cells": list(PROTOCOL_A_PRIME_CELLS),
        "cell_count": int(cell_count),
        "auxiliary_calibration_outside_multiplier": "bare diamond",
        "look_elsewhere_bin_cells": bin_cells,
        "raw_shots_per_bin_cell": PROTOCOL_A_PRIME_RAW_SHOTS_PER_BIN_CELL,
        "executable_shots_per_bin_cell_ceiling": executable_shots_per_bin_cell,
        "raw_total_shots": raw_total_shots,
        "executable_total_shots": executable_total_shots,
        "raw_runtime_hours_at_1kHz": round(raw_total_shots / cadence_hz / 3600.0, 5),
        "executable_runtime_hours_at_1kHz": round(executable_total_shots / cadence_hz / 3600.0, 3),
        "cell_count_sensitivity": "all bin-cell, shot-total, and runtime budgets scale linearly with cell_count",
        "adaptive_resolution_rule": {
            "effective_linewidth_Hz": "delta_nu = 1/(2*pi*T2_eff)",
            "maximum_step_Hz": "Delta_nu <= 1/(4*pi*T2_eff)",
            "baseline_5kHz_valid_through_T2_eff_us": 1.0e6 / (4.0 * math.pi * 5000.0),
            "action_above_threshold": "tighten the grid and recompute bins, multiplicity, shots, and runtime before unblinding",
        },
        "branch_window_role": "pre-registered hypothesis regions inside the full scan; not substitute scan bands",
        "control_point_150MHz_role": "sign-unfixed diagnostic only; excluded from F1 and Holm primary decisions",
    }


PROTOCOL_A_PRIME_SCAN_BUDGET = protocol_a_prime_scan_budget()


def evaluate_protocol_a_prime_f1(observation):
    """Evaluate Protocol A-Prime F1 using the canonical joint-null rule.

    Authoritative preregistration source is App PRG P.8 + Ch13 §13.3.5; this
    engine config mirrors the canonical rule. T2 ratio is O.23/O.24 readout
    context, not a falsification threshold.
    """
    observed = dict(observation)
    branch_a_peak = bool(observed.get("branch_a_112mhz_peak_detected", False))
    branch_b_peak = bool(observed.get("branch_b_42mhz_peak_detected", False))
    response_150mhz = bool(observed.get("response_150mhz_detected", False))
    chirality_contrast = bool(observed.get("chirality_contrast_detected", False))
    scan_complete = bool(observed.get("scan_band_32_200mhz_complete", False))
    spacing_khz = float(observed.get("max_scan_spacing_khz", float("inf")))
    t2_eff_us = observed.get("t2_eff_us")
    p_ciss_measured = bool(observed.get("p_ciss_measured_pre_unblinding", False))
    p_ciss_net = observed.get("p_ciss_net")
    completed_systematics = set(observed.get("completed_systematics", ()))

    systematics_ok = set(PROTOCOL_A_PRIME_REQUIRED_SYSTEMATICS).issubset(completed_systematics)
    adaptive_step_khz = (
        None if t2_eff_us is None
        else 1_000.0 / (4.0 * math.pi * float(t2_eff_us))
    )
    allowed_step_khz = (
        None if adaptive_step_khz is None
        else min(PROTOCOL_A_PRIME_BASELINE_STEP_KHZ, adaptive_step_khz)
    )
    scan_ok = (
        scan_complete
        and allowed_step_khz is not None
        and spacing_khz <= allowed_step_khz
    )
    ciss_value = None if p_ciss_net is None else float(p_ciss_net)
    ciss_clean = p_ciss_measured and ciss_value is not None and ciss_value >= 0.1
    ciss_sensitivity_limited = (
        p_ciss_measured and ciss_value is not None and 0.025 <= ciss_value < 0.1
    )
    ciss_below_floor = p_ciss_measured and ciss_value is not None and ciss_value < 0.025
    joint_null = (
        not branch_a_peak
        and not branch_b_peak
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
        "response_150mhz_diagnostic": response_150mhz,
        "t2_eff_us_recorded": t2_eff_us is not None,
        "allowed_max_scan_spacing_khz": allowed_step_khz,
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
    precision = str(data.get("app_psc_precision_str", fallback_precision))
    return gap, sigma, disposition, precision


_WP2025_GAP, _WP2025_GAP_SIGMA, _MUON_G2_DISPOSITION, _MUON_G2_PRECISION = (
    _load_muon_g2_wp2025_disposition()
)


REGISTRY = {
    "meta": {
        "theory_name": "Geometric Consciousness Theory (GCT)",

        "claim":       (
            "5-postulate (P1-P5) + A1 m_e dimensional anchor for the bare "
            "topology/exponent sub-sector; A2 alpha_2^{-1}(M_GUT) Tier-3 "
            "calibrated native-RGE boundary and A4-A6 Tier-3 calibrated "
            "Z1/Z2/Z3 beta-coefficient magnitude normalisations for the "
            "native-RGE flow; A3 measured low-energy alpha for corrected "
            "precision-comparison rows. The current sector accounting is "
            "six continuous anchors A1-A6. A named precision/gauge comparison "
            "subset contains six calibrated Tier-3 discrete coefficient handles "
            "(1440, 12, 360, 2, 10 phi^2, 1/5); this is not a manuscript-wide "
            "handle total. The O.38 N=144 cage posit and other sector-specific "
            "handles are counted separately. The bare topology/exponent "
            "sub-sector takes no continuous fitted input beyond the A1 "
            "dimensional anchor."
        ),
    },

    # ──────────────────────────────────────────────────────────────────────
    "fine_structure_constant": {
        "prediction":     137.0303,
        "formula":        "360·phi^-2·(1 − 1/(2·N))",
        "experiment":     float(C.ALPHA_INV_OBS),
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
        "simulation_result": "N_L − N_R = 1 (Fibonacci chain N=89). Audit caveat (protocol_chirality_audit): "
                             "the N_L/N_R sign labels are noise (|<C>| ~ 1e-14) and the zero mode is generic to "
                             "odd-length bipartite chains (200/200 random controls), not Fibonacci-specific; "
                             "gct_verified false, verdict CHIRAL_ZERO_MODE_GENERIC_NOT_FIBONACCI_SPECIFIC.",
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

    "shapley_source_proxy_template": {
        "prediction_delta_w_w_band": [2.0e-5, 1.5e-4],
        "alignment_l_deg":           311.0,
        "alignment_b_deg":           30.0,
        "alignment_tolerance_deg":   30.0,
        "amplitude_basis":           (
            "Stipulated product of the conditional Class-2 coordinate "
            "envelope [2, 5] x 10^-5 and a source-proxy overdensity "
            "factor in [1, 3] at Shapley scale; model arithmetic only"
        ),
        "mechanism":                 (
            "Stipulated Shapley-oriented source-proxy/template test; "
            "not physical biogenic strain"
        ),
        "tier":                      3,
        "falsification":             (
            "Post-Roman successor mission (or DESI Y10+ extended "
            "spatial-mapping program) finds no dipole amplitude in the "
            "registered [2e-5, 1.5e-4] delta_w/w band aligned within "
            "+/-30 deg of Shapley at > 3sigma; this excludes the "
            "stipulated template only, while a match supports the "
            "template without establishing a physical source or coupling"
        ),
        "experiment":                "Post-Roman successor (or DESI Y10+ extended spatial-w(z) mapping)",
        "timeframe":                 "Post-Roman successor",
        "status":                    "CONDITIONAL_SOURCE_PROXY_TEMPLATE_REGISTERED",

    },
    "pta_l6_anisotropy": {
        "structural_theorem": (
            "The first nonconstant rotational-icosahedral scalar harmonic "
            "occurs uniquely at ell=6."
        ),
        "physical_response_status": (
            "OPEN: no action-to-propagator-to-generalized-ORF transfer, amplitude, "
            "frequency law, or sky orientation is derived."
        ),
        "empirical_gate": (
            "No PTA detection or exclusion threshold is registered until the "
            "physical transfer and normalization are derived."
        ),
        "preregistration_required": False,
        "status": "EXACT_L6_STRUCTURE__PHYSICAL_PTA_TRANSFER_OPEN",
        "priority": "THEOREM_COMPLETE_TRANSFER_REQUIRED",
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
            "e": "secondary model-comparison evidence: Σmν > 0.10 eV at 3σ supports the independent P.4 neutrino template; it cannot activate P.6 or a causal biogenic channel; DESI 2024 <0.072 eV is tension only"
        }
    },

    # ──────────────────────────────────────────────────────────────────────
    "nv_center_chiral_proxy": {
        "authoritative_preregistration_source": PROTOCOL_A_PRIME_AUTHORITATIVE_SOURCE,
        "engine_config_mirror": (
            "This entry mirrors App PRG P.8 and Ch13 §13.3.5. The F1 decision "
            "rule is the three-conjunct Branch A + Branch B + chirality null after the required "
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
        "required_scan_grid": PROTOCOL_A_PRIME_SCAN_BUDGET,
        "baseline_max_scan_spacing_kHz_through_T2_eff_15p915us": 5.0,
        "sign_unfixed_diagnostic_MHz": 150.0,
        "chirality_control": "R-vs-S enantiomer measurement required",
        "per_cap_P_CISS_requirement": (
            "P_CISS^net measured pre-unblinding on each cap; >=0.1 at >=5sigma "
            "across all 50 caps for clean F1, 0.025-0.1 sensitivity-limited, "
            "<0.025 not falsifying."
        ),
        "mechanism": "CISS material-proxy branch; chirality is a candidate missing-leg control (DMC), not a requirement; no Zeno lock implied",
        "verdict_rule": (
            "F1 = joint Branch A + B + chirality null. Protocol A-Prime F1 is falsified "
            "only if BOTH no peak is detected in the Branch A 112 +/- 10 MHz "
            "window and no peak is detected in the Branch B 42 +/- 10 MHz "
            "window across the authoritative half-open [32,200) MHz scan, with "
            "adaptive spacing Delta_nu <= 1/(4*pi*T2_eff) and a 5 kHz ceiling only "
            "through T2_eff = 15.915 us, "
            "S0-S7 acceptance checks, no R-vs-S chirality contrast, measured "
            "pre-unblinding per-cap P_CISS, and "
            "post-transfer CISS retention on the h-BN/NV process flow meeting "
            "the clean-falsification floor. A single-branch null does "
            "not falsify. The 150 MHz sign is unfixed and is a Tier 3 mechanism "
            "diagnostic outside F1 and Holm primary decisions. Peak-amplitude magnitude "
            "is O.23/O.24 readout context, not a falsification threshold."
        ),
        "evaluation_function": "evaluate_protocol_a_prime_f1",
        "dataset":   "NV centres in diamond with controlled h-BN chirality capping",
        "timeline":  "2-5 years (established nanofabrication technology)",
        "status":    "MATERIAL_PROXY_TEST — execution protocol specified; not evidence for GCT (no phason, Selection-Operator or Level-II inference; App PRG P.8)",
        "priority":  "HIGH — non-biological material-proxy test of the CISS candidate",
    },

    # ──────────────────────────────────────────────────────────────────────
    "directional_bell_inequality": {
        "prediction": "Icosahedral violation of rotational isotropy",
        "mechanism": "Physical directional-response mechanism and normalization remain open",
        "orientation_requirement": (
            "Any icosahedral test must retain an oriented A6(R n) structure "
            "rather than a finite separation mask"
        ),
        "falsification": "No Bell-test exclusion rule is registered until a physical directional transfer is derived",
        "status": "DIRECTIONAL_RESPONSE_TRANSFER_OPEN"
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
    ci_output = {
        "locked": True,
        "pass": True,
        "pass_scope": "BOOKKEEPING: pass means the registry file was written; no prediction is tested here (closure label open, not confirmed)",
        "n_predictions": len(REGISTRY) - 1,
        "protocol_a_prime_scan_budget": PROTOCOL_A_PRIME_SCAN_BUDGET,
    }
    with open(get_output_path("protocol_preregistration_results.json"), "w") as fp:
        json.dump(ci_output, fp, indent=2)
    print("Output written to data/protocol_preregistration_results.json")
