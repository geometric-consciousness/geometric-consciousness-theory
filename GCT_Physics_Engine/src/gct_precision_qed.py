#!/usr/bin/env python3
"""
gct_precision_qed.py — Precision QED Engine
============================================================
Computes GCT contributions to anomalous magnetic moments and the Lamb Shift
from the icosahedral lattice geometry; the muon g-2 numerical value also uses
the A3 measured alpha, and the channel count is a bookkeeping mnemonic (both
detailed below).

Muon g-2 Mechanism
---------------------------
The Muon is a vertex defect in the Rhombic Triacontahedron (RT) window.
The RT has:
  F = 30  (rhombus faces)
  V5 = 12 (degree-5 vertices  → Leptons)
  V3 = 20 (degree-3 vertices  → Quarks)

Euler / handshaking for face–vertex incidences:
  4·F = 5·V5 + 3·V3    [each rhombus has 4 corners]
  120  = 120  ✓

The incidence arithmetic is a bookkeeping mnemonic for the five A5-averaged
lepton channels, not an independent first-principles derivation of the
channel count:
  N_channels = (4·F − 3·V3) / V5 = (120 − 60) / 12 = 5

Each of the 5 averaged channels is treated as one phason form-factor channel.
In an external magnetic field the 5 channels polarise transversally.
Because they are C₅-symmetrised, only the average projection survives:

    Δaμ = (1 / N_channels) · (α_A3/π)³

The three-loop power (α/π)³ is the lowest order at which a closed
phason bubble pair (two insertions of the lattice propagator) can appear.
The numerical g-2 prediction uses A3, the observed low-energy CODATA
fine-structure constant from `gct_constants.yaml::ALPHA_OBS`. The bare
GCT tree-level α remains a separate O.19/O.5 closure target and is not
folded into this QED comparison.

Electron g-2 (N=0 threshold)
------------------------------
The electron sits at the fundamental vertex mode N=0 (ground state).
The muon occupies the N=11 phason harmonic (V3 Ch08).
The lattice loop correction activates only at N ≥ N_MU_HARMONIC,
so the electron receives zero lattice correction, preserving 10⁻¹² agreement.

Lamb Shift
------------------
The lattice scale is a_lattice ~ l_Planck ≈ 1.616e-35 m.
The Bohr radius a₀ ≈ 5.29e-11 m.  Ratio r ≈ 3.06e-25.
The shift in 2S level scales as r³ ≈ 2.9e-74 → entirely negligible.
"""

import numpy as np

# ── SSOT import (sys.exit(1) on YAML failure) ──────────────────────────────
from gct_utils import C

# ─────────────────────────────────────────────────────────────────────────────
# RT GEOMETRY  (from gct_gauge.py derivation)
# ─────────────────────────────────────────────────────────────────────────────
RT_F  = 30   # rhombus faces
V5    = 12   # degree-5 vertices  → Leptons
V3    = 20   # degree-3 vertices  → Quarks

# Verify Euler face–vertex incidence constraint:
assert 4 * RT_F == 5 * V5 + 3 * V3, (
    f"RT geometry inconsistent: 4·{RT_F}={4*RT_F} ≠ 5·{V5}+3·{V3}={5*V5+3*V3}")

# Number of phason channels per lepton vertex: Tier 2 channel-count
# mechanism; equal-weight conversion to the +5alpha pole-mass coefficient
# is Tier 3 pending the GCT self-energy calculation.
N_LEPTON_CHANNELS: int = (4 * RT_F - 3 * V3) // V5   # = (120-60)/12 = 5

# Muon occupies the N=11 phason harmonic (V3 Ch08 mass spectrum):
N_MUON_HARMONIC: int = 11


# ─────────────────────────────────────────────────────────────────────────────
# QED coefficients  (Aoyama et al. 2020 universal series)
# ─────────────────────────────────────────────────────────────────────────────
_QED_C1 =  0.5
_QED_C2 = -0.328_478_965
_QED_C3 =  1.181_241_456
_QED_C4 = -1.912_245_764

ALPHA_CODATA_A3 = float(getattr(C, "ALPHA_OBS", 1.0 / 137.035999177))


def compute_anomalous_moment(lepton_type: str) -> dict:
    """
    Return the full anomalous magnetic moment a = (g-2)/2.

    Parameters
    ----------
    lepton_type : 'electron' | 'muon'

    Returns
    -------
    dict with keys: total, sm_part, gct_part, N_channels, harmonic, formula
    """
    alpha    = ALPHA_CODATA_A3
    alpha_pi = alpha / np.pi

    # Universal QED contribution (mass-independent up to four loops):
    a_univ = (
        _QED_C1 * alpha_pi
        + _QED_C2 * alpha_pi**2
        + _QED_C3 * alpha_pi**3
        + _QED_C4 * alpha_pi**4
    )

    if lepton_type == "electron":
        # N=0 — below the phason activation threshold (N_MUON_HARMONIC = 11).
        # No lattice correction for the electron.
        return {
            "total":      a_univ,
            "sm_part":    a_univ,
            "gct_part":   0.0,
            "N_channels": 0,
            "harmonic":   0,
            "formula":    "SM QED only (N=0, below N=11 phason threshold)",
        }

    elif lepton_type == "muon":
        # SM total including HVP + EW (consolidated SM White Paper 2025,
        # Aliberti et al. arXiv:2505.21476):
        a_mu_sm = float(C.MUON_G2_SM_WP2025)

        # Lattice correction from RT vertex topology:
        gct_part = (1.0 / N_LEPTON_CHANNELS) * alpha_pi**3

        return {
            "total":      a_mu_sm + gct_part,
            "sm_part":    a_mu_sm,
            "gct_part":   gct_part,
            "N_channels": N_LEPTON_CHANNELS,
            "harmonic":   N_MUON_HARMONIC,
            "formula":    (
                f"SM_WP2025 + (1/{N_LEPTON_CHANNELS})·(α_A3/π)³  "
                f"[A3 measured alpha; N_channels as A5-averaged RT incidence mnemonic: "
                f"(4·{RT_F}−3·{V3})/{V5}]"
            ),
            "alpha_anchor": "A3 measured low-energy alpha; bare GCT alpha is audited separately under O.19/O.5.",
        }

    elif lepton_type == "tau":
        # Tau mass (1776.93 MeV PDG 2024) is ~17.5x above the N=11 activation threshold
        # (101.69 MeV from m_e * phi^11), so the closed-phason-loop correction
        # applies. Under the assumption that the 5-channel A_5 averaging is
        # universal across above-threshold leptons (Tier 3 assumption; a
        # generation-dependent channel count would be a candidate sub-problem
        # of App H O.26), the form-factor is the same as the muon:
        gct_part = (1.0 / N_LEPTON_CHANNELS) * alpha_pi**3

        # SM tau g-2 prediction is not currently catalogued at the same
        # precision as muon (PDG bound on a_tau is ~1e-1, dominated by EW
        # uncertainty), so we report only the GCT correction here.
        return {
            "total":      gct_part,  # SM a_tau dominated by EW; not catalogued
            "sm_part":    None,
            "gct_part":   gct_part,
            "N_channels": N_LEPTON_CHANNELS,
            "harmonic":   17,  # N=17 Lucas-pair anchor (V3 Ch08)
            "formula":    (
                f"(1/{N_LEPTON_CHANNELS})·(α_A3/π)³  [Tier 2 mechanism + A3 + "
                f"Tier 3 channel-count universality assumption; current PDG "
                f"bound on a_tau is ~1e-1, FCC-ee target ~1e-6; prediction is "
                f"currently unfalsifiable on operational grounds]"
            ),
            "alpha_anchor": "A3 measured low-energy alpha; bare GCT alpha is audited separately under O.19/O.5.",
        }

    else:
        raise ValueError(f"Unknown lepton type: '{lepton_type}'")


def compute_lamb_shift_correction() -> dict:
    """
    Estimate the GCT lattice correction to the hydrogen Lamb Shift.

    Correction scales as (a_lattice / a_Bohr)³ ≈ 10⁻⁷⁴ → negligible.
    """
    A_LATTICE_M = 1.616e-35   # Planck length (GCT lattice scale)
    A_BOHR_M    = 5.292e-11   # Bohr radius

    ratio       = A_LATTICE_M / A_BOHR_M
    suppression = ratio**3

    # Standard Lamb shift (H, 2S½ – 2P½):
    LS_STANDARD_MHZ = 1057.845

    return {
        "standard_lamb_MHz":  LS_STANDARD_MHZ,
        "gct_correction_MHz": LS_STANDARD_MHZ * suppression,
        "suppression_factor": suppression,
        "verdict":            "NEGLIGIBLE",
        "note":               (
            "Correction ∝ (l_Planck / a_Bohr)³ ≈ 2.9e-74. "
            "GCT makes no measurable prediction for the ordinary Lamb Shift."
        ),
    }


# ── Quick self-test ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"RT lepton channels derived: N = {N_LEPTON_CHANNELS}")
    print(f"Muon harmonic:              N = {N_MUON_HARMONIC}")

    for l in ("electron", "muon"):
        r = compute_anomalous_moment(l)
        print(f"\n{l.capitalize()} g-2:")
        print(f"  SM part   = {r['sm_part']:.11e}")
        print(f"  GCT Δa    = {r['gct_part']:.5e}")
        print(f"  Total     = {r['total']:.11e}")
        print(f"  Formula:    {r['formula']}")
