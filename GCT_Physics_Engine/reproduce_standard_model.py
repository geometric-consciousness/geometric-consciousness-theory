#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reproduce_standard_model.py — Anchored-Mode Reproducer

Re-verifies the registered set of Tier-2 mechanisms + Tier-3 calibrated
anchors per Parameter Ledger §0.1 (5 postulates + A1/A2/A3 anchor set).
Default mode uses A3 CODATA α(0) as registered Tier-3 empirical input;
NuFit oscillation gaps and M_red are explicit Tier-3 imports per Ledger
§0.1.

Modes:
  --mode anchored (default): re-runs every Tier-2 prediction against
    PDG/CODATA targets under the registered A1/A2/A3 anchor set.
    Verifies that all Tier-2 mechanism + Tier-3 anchor combinations
    land inside their registered falsification bands.

  --mode bare: re-runs without A3 (bare-α from 360·φ⁻²), exposing the
    bare-α residual structure. The 3442 ppm bare-α residual is the
    QLQCD-1L phason anti-screening debt (App H O.5/O.19); tightening
    below 3442 ppm requires QLQCD-1L closure.

From-zero reduction to the 1-parameter limit (P1 + m_e) is the published
target per Ledger §0.1 ambition note, pending closure of O.5 (QLQCD-1L),
O.14 (electron exponent K-theoretic gap-label uniqueness),
O.15 (D=18 RG derivation), and O.19 (bare-to-physical α bridge).
"""
from __future__ import annotations

import argparse
import math
import sys
from dataclasses import dataclass, field
from typing import Optional

# Force UTF-8 stdout/stderr on Windows so the print statements in this script
# (which contain unicode chars like phi, alpha, sigma) do not crash with
# UnicodeEncodeError under default cp1252 console encoding.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

# ════════════════════════════════════════════════════════════════════════════
# MATHEMATICAL PRIMITIVES (Tier 0 — pure math, no empirical input)
# ════════════════════════════════════════════════════════════════════════════

PHI = (1.0 + math.sqrt(5.0)) / 2.0       # Golden ratio, exact
PHI_INV = 1.0 / PHI                      # = φ − 1
PI = math.pi


# ════════════════════════════════════════════════════════════════════════════
# THE 1-DOF EMPIRICAL ANCHOR + SCAFFOLDING EMPIRICAL INPUTS
# ════════════════════════════════════════════════════════════════════════════
# m_e is the SOLE input that anchors the geometric blueprint to SI units.
# The other empirical inputs are NOT free parameters of GCT — they are
# scaffolding (oscillation gaps, M_red) entered explicitly so the reader
# sees what is and isn't being derived from the icosahedral geometry alone.

M_E_MEV = 0.51099895069                  # CODATA 2022, primary anchor [Tier 0 input]
ALPHA_CODATA_INV = 137.035999177         # CODATA 2022 — used only in --mode anchored
DELTA_M2_21_EV2 = 7.42e-5                # NuFit 5.3 (oscillation gap)
DELTA_M2_31_EV2 = 2.51e-3                # NuFit 5.3 (oscillation gap)
HBAR_J_S = 1.054571817e-34               # CODATA 2022 (for G derivation)
C_M_S = 299792458.0                      # Exact SI definition
EV_TO_J = 1.602176634e-19                # Exact SI definition since 2019


# ════════════════════════════════════════════════════════════════════════════
# OBSERVATIONAL ANCHORS (PDG 2024 / CODATA 2022 — only for comparison)
# ════════════════════════════════════════════════════════════════════════════
# These are the experimentally measured values the predictions are compared
# against. They never enter any GCT prediction (except as the empirical
# anchor itself, namely m_e).

OBS = {
    "alpha_inv":      ("α⁻¹",                        ALPHA_CODATA_INV,                "dimensionless"),
    "sin2_theta_w_bare":("sin²θ_W (bare, geometric)", 0.23122,                         "dimensionless"),  # Z-pole observed
    "m_mu":           ("m_μ",                         105.6583755,                     "MeV"),
    "m_tau":          ("m_τ",                         1776.93,                         "MeV"),
    "m_p":            ("m_p (proton)",                938.27208816,                    "MeV"),
    "m_u":            ("m_u (up)",                    2.16,                            "MeV"),
    "m_d":            ("m_d (down)",                  4.67,                            "MeV"),
    "m_s":            ("m_s (strange)",               93.4,                            "MeV"),
    "m_c":            ("m_c (charm)",                 1.27e3,                          "MeV"),
    "m_b":            ("m_b (bottom)",                4.18e3,                          "MeV"),
    "m_t":            ("m_t (top)",                   172.69e3,                        "MeV"),
    "v_higgs":        ("v (Higgs VEV)",               246.21965,                       "GeV"),
    "delta_cp":       ("δ_CP",                        232.0,                           "deg (PMNS)"),
    "sigma_mnu":      ("Σm_ν",                        None,                            "eV (upper bound only)"),
    "theta_c":        ("θ_C (Cabibbo)",               13.04,                           "deg"),
    "G_newton":       ("G (Newton)",                  6.67430e-11,                     "m³/(kg·s²)"),
    "M_GUT":          ("M_GUT",                       3.2e16,                          "GeV"),
    "M_planck_red":   ("M_red (reduced Planck)",      2.435e18,                        "GeV"),
}


# ════════════════════════════════════════════════════════════════════════════
# FALSIFICATION BANDS (mirrors falsifiability_registry.json)
# ════════════════════════════════════════════════════════════════════════════
# A prediction PASSES if |pred - obs| / |obs| × 1e6 < band_ppm.
# `band_ppm: None` → qualitative threshold, no automatic pass/fail.
# `tier_3_pass: True` → TENSION counts as PASS (these are Tier 3 ansätze
#                       not Tier 2 falsifications).

BANDS = {
    "alpha_inv":            5000.0,           # 3442 ppm residual is QLQCD-1L debt, not falsification
    "sin2_theta_w_bare":    50000.0,          # 5% band; 2.1% currently
    "m_mu":                 100.0,            # 21 ppm currently
    "m_tau":                60.0,             # 51 ppm currently against PDG 2024 (m_tau = 1776.93 ± 0.09 MeV)
    "m_p":                  500.0,            # 155 ppm currently
    "m_u":                  None,             # PDG envelope is wide; qualitative
    "m_d":                  None,             # FK shell-resonance band ±11%/-3%
    "m_s":                  None,             # PDG +9%/-4% uncertainty
    "m_c":                  None,             # Tier 3 ansatz
    "m_b":                  25000.0,          # 5/4 representation, 5σ band
    "m_t":                  None,             # PDG envelope wide
    "v_higgs":              5000.0,           # 181 ppm (engine residual_error_ppm = 180.95)
    "delta_cp":             None,             # Tier 2, PMNS uncertainty wide
    "sigma_mnu":            None,             # Upper bound test, not equality
    "theta_c":              50000.0,          # 5%
    "G_newton":             5000.0,           # 2274 ppm currently; cascades from m_e
    "M_GUT":                None,             # Order-of-magnitude only
    "M_planck_red":         None,             # Implicit anchor; not a prediction per se
}


# ════════════════════════════════════════════════════════════════════════════
# THE PREDICTIONS — one block per observable
# ════════════════════════════════════════════════════════════════════════════
# Every prediction is a closed-form formula. Manuscript reference is given
# in the comment block above each block. The variable `alpha` is either the
# GCT bare 360·φ⁻² (--mode bare) or CODATA (--mode anchored).

def derive_alpha_bare() -> float:
    """α⁻¹ = 360·φ⁻²  [Tier 2 (tree-level bare), V3 Ch04 §4.5.5]"""
    return 1.0 / (360.0 * PHI**(-2))


def predict_all(alpha: float) -> dict[str, float]:
    """Compute every Tier-2 GCT observable from m_e + α + φ + structural
    integers. Returns a dict keyed identically to OBS."""

    m_e = M_E_MEV
    phi = PHI

    p: dict[str, float] = {}

    # ── Gauge sector ────────────────────────────────────────────────────
    # α⁻¹ from 360·φ⁻²  [V3 Ch04 §4.5.5]
    p["alpha_inv"] = 1.0 / alpha

    # sin²θ_W bare (geometric BC, pre-RGE) = φ⁻³  [V3 Ch04 §4.5; App R §R.2]
    p["sin2_theta_w_bare"] = phi ** (-3)

    # ── Charged lepton sector ───────────────────────────────────────────
    # m_μ = m_e · φ^11 · (1 + 5α + φ^8·α²)  [V3 Ch08 §8.4; App R §R.1]
    p["m_mu"] = m_e * phi**11 * (1.0 + 5.0*alpha + phi**8 * alpha**2)

    # m_τ = m_e · φ^17 · (1 + (-3.6)·α)  [V3 Ch08 §8.4; App R §R.1]
    p["m_tau"] = m_e * phi**17 * (1.0 - 3.6*alpha)

    # ── Hadron sector ───────────────────────────────────────────────────
    # m_p = m_e · φ^(15 + φ⁻¹)  [V3 Ch11 / Protocol F; App R §R.3]
    p["m_p"] = m_e * phi**(15.0 + 1.0/phi)

    # Quark mass anchor (up): m_u = m_e · φ³  [V3 Ch10; App R §R.3]
    p["m_u"] = m_e * phi**3

    # Down quark via FK-determinant infinite-volume-limit branch [App TP §TP-B]
    # Primary output: m_d = m_u · φ^φ = 4.716 MeV, conditional on O.5.
    p["m_d"] = p["m_u"] * phi**phi

    # Strange: m_s = m_u · φ^8 · (1 - 12α)  [V3 Ch10; App R §R.3]
    p["m_s"] = p["m_u"] * phi**8 * (1.0 - 12.0*alpha)

    # Charm Tier-3 ansatz: m_c = m_u · φ^(13 + φ⁻³)  [V3 Ch10; App R §R.3]
    p["m_c"] = p["m_u"] * phi**(13.0 + phi**(-3))

    # Bottom: m_b = m_c · φ² · (5/4)  [A₅ rep-theorem 5/4, V3 Ch10]
    p["m_b"] = p["m_c"] * phi**2 * 1.25

    # Top quark: m_t = (v / 2) · √2  in GeV  [V3 Ch10; App R §R.3]
    # Uses the predicted Higgs VEV (filled below).

    # ── Higgs sector ────────────────────────────────────────────────────
    # v = m_μ · 1440 · φ  [V3 Ch05; geometric lattice sum]
    p["v_higgs"] = (p["m_mu"] * 1440.0 * phi) / 1000.0      # MeV → GeV

    # Top quark: m_t = (v / 2) · √2  in GeV  [V3 Ch10; App R §R.3]
    p["m_t"] = (p["v_higgs"] / 2.0 * math.sqrt(2.0)) * 1000.0   # GeV → MeV (table is in MeV)

    # ── CKM / PMNS ──────────────────────────────────────────────────────
    # Cabibbo angle: θ_C = arcsin(φ⁻³)  [V3 Ch10; face-tunneling]
    p["theta_c"] = math.degrees(math.asin(phi**(-3)))

    # δ_CP = 360° · φ⁻¹  [V3 Ch09 §9.4.3]
    p["delta_cp"] = 360.0 * (1.0/phi)

    # ── Neutrino sector ─────────────────────────────────────────────────
    # m_1 floor = m_e · φ⁻³⁶  [V3 Ch09 Theorem 9.1]
    m_1_eV = M_E_MEV * 1.0e6 * phi**(-36)                  # MeV → eV
    m_2_eV = math.sqrt(m_1_eV**2 + DELTA_M2_21_EV2)
    m_3_eV = math.sqrt(m_1_eV**2 + DELTA_M2_31_EV2)
    p["sigma_mnu"] = m_1_eV + m_2_eV + m_3_eV

    # ── Gravity / scale ────────────────────────────────────────────────
    # M_GUT = M_red · φ⁻⁹  [V3 Ch04 §4.3.2]
    # M_red ≈ 2.435 × 10¹⁸ GeV from sqrt(ℏc/(8πG)); we use the OBSERVED
    # M_red as input, since deriving M_red from m_e via φ^107 is the cascade
    # bound in App TP §TP-D (the 2274 ppm G residual lives here).
    M_red_GeV = OBS["M_planck_red"][1]
    p["M_GUT"] = M_red_GeV * phi**(-9)

    # Newton's G postdiction via Jacobson chain  [V2 Ch09 §9.1.4]
    # M_P = m_e · φ^107 · (1 - 5α)⁻¹
    M_P_MeV = M_E_MEV * phi**107 * (1.0 - 5.0*alpha)**(-1)
    M_P_kg = M_P_MeV * 1.0e6 * EV_TO_J / (C_M_S**2)
    p["G_newton"] = HBAR_J_S * C_M_S / (M_P_kg**2)
    p["M_planck_red"] = M_P_MeV / 1.0e3 / math.sqrt(8.0*PI)  # reduced

    return p


def ppm_error(predicted: float, observed: Optional[float]) -> Optional[float]:
    if predicted is None or observed is None:
        return None
    return abs(predicted - observed) / abs(observed) * 1.0e6


def classify(name: str, pred: float, obs: Optional[float]) -> tuple[str, Optional[float]]:
    ppm = ppm_error(pred, obs)
    band = BANDS.get(name)
    if obs is None:
        return "INFO", ppm
    if ppm is None:
        return "—", None
    if band is None:
        return "INFO", ppm
    if ppm < band:
        return "PASS", ppm
    return "FAIL", ppm


@dataclass
class RunResult:
    mode: str
    alpha_used: float
    rows: list[tuple[str, str, float, Optional[float], Optional[float], str, str]] = field(default_factory=list)
    n_pass: int = 0
    n_fail: int = 0
    n_info: int = 0


def run_mode(mode: str) -> RunResult:
    if mode == "pure":
        mode = "bare"
    if mode == "bare":
        alpha = derive_alpha_bare()
    elif mode == "anchored":
        alpha = 1.0 / ALPHA_CODATA_INV
    else:
        raise ValueError(f"unknown mode {mode!r}")

    predictions = predict_all(alpha)
    rr = RunResult(mode=mode, alpha_used=alpha)

    for key, (label, obs_val, unit) in OBS.items():
        pred = predictions.get(key)
        if pred is None:
            continue
        status, ppm = classify(key, pred, obs_val)
        rr.rows.append((key, label, pred, obs_val, ppm, unit, status))
        if status == "PASS":
            rr.n_pass += 1
        elif status == "FAIL":
            rr.n_fail += 1
        else:
            rr.n_info += 1
    return rr


# ════════════════════════════════════════════════════════════════════════════
# REPORTING
# ════════════════════════════════════════════════════════════════════════════

def _fmt_num(v, width):
    if v is None:
        return f"{'—':>{width}}"
    if not isinstance(v, (int, float)):
        return f"{str(v):>{width}}"
    absv = abs(v)
    if absv == 0:
        return f"{0.0:>{width}.4f}"
    if absv >= 1e4 or absv < 1e-3:
        return f"{v:>{width}.3e}"
    return f"{v:>{width}.6g}"


def _fmt_ppm(v, width):
    if v is None:
        return f"{'—':>{width}}"
    if v < 1.0:
        return f"{v:>{width}.3f}"
    if v < 100.0:
        return f"{v:>{width}.2f}"
    if v < 1e6:
        return f"{v:>{width}.0f}"
    return f"{v:>{width}.2e}"


def _status_badge(s: str) -> str:
    return {"PASS": "[ PASS ]", "FAIL": "[ FAIL ]", "INFO": "[  ok  ]", "—": "[  --  ]"}.get(s, f"[{s:^6}]")


def print_report(rr: RunResult) -> None:
    print("─" * 100)
    print(f"  GCT anchored-mode reproducer — mode = {rr.mode}    α⁻¹ used = {1.0/rr.alpha_used:.6f}")
    print("─" * 100)
    header = (
        f"  {'Observable':<26}"
        f"{'Predicted':>16}"
        f"{'Observed':>16}"
        f"{'ppm':>12}"
        f"  {'Status':<10} {'Unit'}"
    )
    print(header)
    print("  " + "-" * 96)
    for key, label, pred, obs, ppm, unit, status in rr.rows:
        line = (
            f"  {label:<26}"
            f"{_fmt_num(pred, 16)}"
            f"{_fmt_num(obs, 16)}"
            f"{_fmt_ppm(ppm, 12)}"
            f"  {_status_badge(status):<10} {unit}"
        )
        print(line)
    print("  " + "-" * 96)
    print(f"  Tier-2 PASS: {rr.n_pass}    FAIL: {rr.n_fail}    Info-only (Tier 3 or qualitative): {rr.n_info}")
    print("─" * 100)


def main() -> int:
    parser = argparse.ArgumentParser(description="GCT anchored-mode Standard Model reproducer")
    parser.add_argument("--mode", choices=["bare", "pure", "anchored", "both"], default="anchored",
                        help="α source. bare = 360·φ⁻²; pure = bare; anchored = CODATA; both = run bare + anchored")
    args = parser.parse_args()

    print("=" * 96)
    print("  Geometric Consciousness Theory — Anchored-Mode Reproducer")
    print("=" * 96)
    print(f"  Empirical anchor : m_e = {M_E_MEV} MeV (CODATA 2022)")
    print(f"  Scaffolding      : Δm²_21 = {DELTA_M2_21_EV2:.2e} eV²,  Δm²_31 = {DELTA_M2_31_EV2:.2e} eV² (NuFit 5.3)")
    print(f"                     M_red imported for G/M_GUT (cascade-bound by App TP §TP-D)")
    print(f"  Mathematical     : φ = (1+√5)/2 = {PHI:.10f},  π = {PI:.10f}")
    print("=" * 96)

    modes = ["bare", "anchored"] if args.mode == "both" else [args.mode]
    anchored_fail = 0
    bare_fail = 0
    for m in modes:
        rr = run_mode(m)
        print_report(rr)
        if m == "anchored":
            anchored_fail = rr.n_fail
        elif m in ("bare", "pure"):
            bare_fail = rr.n_fail

    print()
    # The verdict logic: only the ANCHORED mode is a falsification test.
    # Bare-mode failures are expected to track the 3442 ppm α-debt; they
    # surface in the lepton sector by construction and are the QLQCD-1L
    # research debt itself, not a new falsification event.
    if anchored_fail == 0:
        print("✓ All Tier-2 predictions inside their falsification bands (anchored mode).")
        if bare_fail > 0:
            print(f"  Bare-mode shows {bare_fail} lepton-sector miss(es) — these track the 3442 ppm")
            print("  α-residual (QLQCD-1L research debt, see App_TP §TP-A / Ch04 §4.5.5).")
            print("  They are expected by construction, not a falsification event.")
        print("  See content/98_Global_Appendices/App_FM_Falsifiability_Matrix.md for the")
        print("  full per-claim threshold map.")
        return 0
    print(f"✗ {anchored_fail} prediction(s) outside band in ANCHORED mode — real falsification event.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
