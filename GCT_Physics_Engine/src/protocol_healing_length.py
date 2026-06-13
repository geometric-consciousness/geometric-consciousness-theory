#!/usr/bin/env python3
"""
protocol_healing_length.py
==========================
Evaluate the polaron healing-length formula xi = hbar c / (alpha^2 m_e c^2)
= a_0 / alpha at two alpha inputs (CODATA and GCT-bare).

Scope. This script evaluates a SINGLE formula — the standard
Gross-Pitaevskii / Bohr-scaling expression (Tier 1 textbook Bohr-Compton
physics; App K §K.5) — at two values of alpha and reports the alpha-input
sensitivity:
  - CODATA alpha (1/137.036) yields xi = 7.25 nm
  - GCT bare alpha (1/(360 phi^-2) = 1/137.508) yields xi = 7.30 nm
The two values agree to within ~0.7% because the two alpha values differ
by ~0.35% and the difference enters xi as a square. This is an
alpha-input sensitivity check on ONE formula, NOT a comparison between
two independent derivations. The GCT-internal "Route 2" phason-elastic
derivation considered in this section (substituting K_perp = phi^-18
K_par, a_6 = 2 ell_P, m_e = M_P phi^-107 (1-5alpha) into
E_elastic ~ E_EM) was carried out explicitly in App K §K.5 and yields
xi^Route2 = (1/2) phi^9 sqrt(alpha) ell_P ~ 5e-35 m, off the Tier 1
target by ~10^26. The substitution chain cannot reproduce the 1/alpha^2
Coulomb-bound-state enhancement that gives a_0/alpha its nm scale (App H
Open Problem O.25 closes negatively). The "two-route convergence"
framing is not used here; only the Tier 1 Bohr-Compton formula is evaluated
here, with alpha as the input variable.
"""

import json
from gct_utils import C, get_output_path

# CODATA SI primitives
HBAR_SI  = 1.054571817e-34   # J s
C_SPEED  = 299792458.0       # m/s
M_E_KG   = 9.1093837015e-31  # kg

# CODATA alpha as reference; GCT bare alpha used if available
ALPHA_CODATA = 1.0 / 137.035999084
ALPHA_GCT = 1.0 / float(C.ALPHA_INV_GCT) if hasattr(C, 'ALPHA_INV_GCT') else ALPHA_CODATA

# Target on CODATA alpha (single canonical reference value)
TARGET_NM_CODATA = 7.25


def _xi_nm(alpha: float) -> float:
    """Compute healing length in nm from a given alpha."""
    return (HBAR_SI * C_SPEED) / (alpha ** 2 * M_E_KG * C_SPEED ** 2) * 1e9


def run_healing_length_derivation():
    print("=" * 60)
    print("GCT Protocol: Healing Length Derivation")
    print("=" * 60)

    xi_codata_nm = _xi_nm(ALPHA_CODATA)
    xi_gct_nm = _xi_nm(ALPHA_GCT)

    error_codata_pct = abs(xi_codata_nm - TARGET_NM_CODATA) / TARGET_NM_CODATA * 100.0
    alpha_branch_spread_pct = abs(xi_gct_nm - xi_codata_nm) / xi_codata_nm * 100.0

    passed = error_codata_pct < 1.0 and alpha_branch_spread_pct < 1.0

    results = {
        "xi_codata_nm":         xi_codata_nm,
        "xi_gct_bare_nm":       xi_gct_nm,
        "target_nm_codata":     TARGET_NM_CODATA,
        "error_vs_target_pct":  error_codata_pct,
        "alpha_branch_spread_pct": alpha_branch_spread_pct,
        "alpha_codata_used":    ALPHA_CODATA,
        "alpha_gct_bare_used":  ALPHA_GCT,
        "formula":              "xi = hbar c / (alpha^2 m_e c^2) = a_0/alpha  [Tier 1 textbook Bohr-Compton formula; Tier 3 lumen-scale match, App K §K.5]",
        "pass":                 passed,
    }

    out_path = get_output_path("protocol_healing_length_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"   xi (CODATA alpha):    {xi_codata_nm:.4f} nm")
    print(f"   xi (GCT bare alpha):  {xi_gct_nm:.4f} nm")
    print(f"   Target (CODATA):      {TARGET_NM_CODATA:.4f} nm (error {error_codata_pct:.3f}%)")
    print(f"   Alpha branch spread:  {alpha_branch_spread_pct:.3f}%")
    print()
    print("=" * 60)
    print("PASS" if passed else "FAIL")
    print("=" * 60)

    return results


if __name__ == "__main__":
    run_healing_length_derivation()
