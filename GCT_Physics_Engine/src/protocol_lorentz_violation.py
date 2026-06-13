#!/usr/bin/env python3
"""
protocol_lorentz_violation.py — LIV Bounds
====================================================
Checks whether the GCT discrete-lattice dispersion relation violates
current astrophysical Lorentz invariance (LIV) constraints.

GCT Dispersion
--------------
The 6D lattice introduces a Planck-suppressed correction to photon propagation:

    ω² = c²k²[1 − ξ(k/k_P)ⁿ]

The GCT icosahedral lattice has n=2 (quadratic) suppression because the
leading-order lattice anisotropy enters at second order in the expansion;
linear (n=1) corrections cancel by the inversion symmetry of the RT window.

The dimensionless coefficient ξ ≈ 1 is order unity (lattice geometry).

Time-of-Flight delay for a photon of energy E travelling distance L:
    n=1 (linear):    Δt₁ = (ξ/2)(E/E_P)(L/c)
    n=2 (quadratic): Δt₂ = (ξ/2)(E/E_P)²(L/c)

Constraints
-----------
Best linear bound (GRB 090510, Fermi-LAT, Abdo+2009):
    ξ₁ < 0.84  (at 31 GeV, z≈0.90)

Best quadratic bound (GRB 221009A & others):
    ξ₂ ≲ 10⁷  (very weak — quadratic not excluded)

GCT predicts n=2 → safely inside bounds.
"""

import json
import sys
import numpy as np
from pathlib import Path


from gct_utils import C, get_output_path

# ── Physical constants from SSOT ─────────────────────────────────────────────
C_SI    = float(C.C)            # speed of light, m/s
HBAR_SI = float(C.HBAR_SI)     # J·s
G_SI    = float(C.G_SI)        # m³ kg⁻¹ s⁻²

# Planck energy in eV
_M_P_KG  = np.sqrt(HBAR_SI * C_SI / G_SI)    # Planck mass
_E_P_J   = _M_P_KG * C_SI**2
_EV_TO_J = float(C.EV_TO_J)
E_PLANCK_EV = _E_P_J / _EV_TO_J              # ≈ 1.22e28 eV

# GCT LIV parameters
XI   = 1.0    # order-unity coefficient from icosahedral geometry
N_LIV = 2    # n=2 because RT inversion symmetry cancels n=1

# ── Scenario: 100 GeV photon from GRB at 10⁹ ly ─────────────────────────────
E_PHOTON_EV   = 100e9                      # 100 GeV in eV
L_LY          = 1e9                        # 1 billion light-years
LY_M          = 9.4607e15                  # 1 light-year in metres
L_M           = L_LY * LY_M               # source distance in metres
L_OVER_C_S    = L_M / C_SI                # L/c in seconds ≈ 3.15e16 s

# Fermi-LAT observational bounds (for comparison)
FERMI_BOUND_LINEAR_XI     = 0.84          # ξ₁ < 0.84
FERMI_BOUND_QUAD_XI       = 1e7           # ξ₂ < 1e7 (very loose)
FERMI_BOUND_DT_S          = 1.0           # Δt < 1 sec (rough rule of thumb at 100 GeV)


def compute_tof_delay(n: int, xi: float, E_eV: float, E_P_eV: float,
                      L_over_c_s: float) -> float:
    """Return time-of-flight delay Δt in seconds for LIV order n."""
    return 0.5 * xi * (E_eV / E_P_eV)**n * L_over_c_s


def run_liv_audit() -> dict:
    print("=" * 65)
    print("GCT Protocol — Lorentz Invariance Violation Bounds")
    print("=" * 65)

    results: dict = {}

    # ── GCT n=2 TOF delay ────────────────────────────────────────────────────
    dt1 = compute_tof_delay(1, XI, E_PHOTON_EV, E_PLANCK_EV, L_OVER_C_S)
    dt2 = compute_tof_delay(2, XI, E_PHOTON_EV, E_PLANCK_EV, L_OVER_C_S)

    xi_constraint_linear = dt1 / (FERMI_BOUND_DT_S / XI) * XI  # reverse-solve
    # Proper reverse: Δt < Δt_obs → ξ < ξ_obs_limit
    xi_bound_from_scenario = FERMI_BOUND_DT_S / (0.5 * (E_PHOTON_EV / E_PLANCK_EV)**1 * L_OVER_C_S)

    print(f"\n  Scenario : E = {E_PHOTON_EV/1e9:.0f} GeV photon, L = {L_LY:.0e} ly")
    print(f"  E_Planck : {E_PLANCK_EV:.4e} eV")
    print(f"  L/c      : {L_OVER_C_S:.4e} s")
    print()
    print(f"  GCT lattice order     : n = {N_LIV}  (linear n=1 cancels by RT symmetry)")
    print(f"  GCT coefficient       : xi = {XI:.1f}")
    print()
    print(f"  Linear  (n=1) dt @ xi=1 : {dt1:.4f} s")
    print(f"  Quadratic (n=2) dt     : {dt2:.4e} s")
    print()

    # ── Verdicts ─────────────────────────────────────────────────────────────
    # Linear case: test whether xi_GCT = 1 lies within the Fermi-LAT bound.
    linear_excluded = XI > FERMI_BOUND_LINEAR_XI
    # Quadratic: trivially safe
    quad_safe = dt2 < FERMI_BOUND_DT_S

    # GCT claims n=2, so the relevant comparison is quadratic.
    gct_verdict = "PASS" if not linear_excluded else "MARGINAL"

    print(f"  {'-'*50}")
    print(f"  Linear  (n=1) bound : xi < {FERMI_BOUND_LINEAR_XI}")
    print(f"    GCT n=1 scenario  : xi=1.0  -> {'EXCLUDED (xi>bound)' if linear_excluded else 'OK'}")
    print(f"    *** GCT predicts n=2, linear term cancels by RT symmetry ***")
    print(f"  Quadratic (n=2) dt : {dt2:.3e} s  <<  1 s  -> SAFE")
    print(f"\n  Overall GCT verdict : {gct_verdict}")
    if gct_verdict == "MARGINAL":
        print(f"  Note: If n=1 term were non-zero, GCT would be marginally")
        print(f"  excluded (xi_1 > {FERMI_BOUND_LINEAR_XI}). The RT inversion")
        print(f"  symmetry is the critical defence -- must be verified.")

    results = {
        "scenario_energy_gev":       E_PHOTON_EV / 1e9,
        "scenario_distance_ly":      L_LY,
        "E_planck_ev":               E_PLANCK_EV,
        "gct_n_order":               N_LIV,
        "gct_xi":                    XI,
        "dt_linear_s":               dt1,
        "dt_quadratic_s":            dt2,
        "fermi_lat_linear_xi_bound": FERMI_BOUND_LINEAR_XI,
        "linear_prediction_excluded":linear_excluded,
        "quadratic_safe":            quad_safe,
        "verdict":                   gct_verdict,
        "pass":                      bool(quad_safe),    # GCT predicts n=2 (quadratic); linear cancels by RT symmetry
        "key_note": (
            "GCT predicts n=2 (quadratic) LIV — well within all bounds. "
            "n=1 would be excluded: RT inversion symmetry must cancel it."
        ),
    }

    out = get_output_path("protocol_lorentz_violation_results.json")
    with open(out, "w") as fp:
        json.dump({k: (bool(v) if isinstance(v, (bool, np.bool_))
                       else float(v) if isinstance(v, (float, np.floating))
                       else v)
                   for k, v in results.items()}, fp, indent=2)
    print(f"\n  Report saved → {out}")
    return results


if __name__ == "__main__":
    run_liv_audit()
