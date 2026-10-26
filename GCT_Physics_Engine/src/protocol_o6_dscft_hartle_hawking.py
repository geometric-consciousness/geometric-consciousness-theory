#!/usr/bin/env python3
"""
protocol_o6_dscft_hartle_hawking.py
====================================

Hartle-Hawking boundary-state and static-patch area-law consistency
calculation for the GCT critical susceptibility
chi = pi(c/H_0 ell_P)^2. The protocol distinguishes state preparation
on S^3 from the S^2 entangling surface of the static-patch bipartition.

CONSTRUCTION

Euclidean dS_4 is the four-sphere S^4 of radius R_dS = c/H_0.
The Hartle-Hawking (Hartle & Hawking 1983 PRD 28:2960) state is
defined as the Euclidean path integral over half of S^4 bounded by
the equatorial 3-sphere S^3:

  psi_HH[h_ij] = int [Dg] exp(-S_E[g]),  with g|_partial = h

This path integral prepares a pure wave functional on the whole S^3;
the preparation hemisphere of S^4 is not an entanglement subsystem.
The spatial S^3 is instead divided into two 3-balls across the S^2
static-patch bifurcation surface. Tracing over the complementary
3-ball gives a reduced state whose semi-classical entropy obeys:

  S_ent = -Tr(rho ln rho) = A_S^2 / (4 G_N)

with A_S^2 = 4 pi R_dS^2 = 4 pi (c/H_0)^2. The S^3 boundary
three-geometry has volume 2 pi^2 R_dS^3 and does not enter this area
law. The
Gibbons-Hawking (1977 PRD 15:2738) cosmological event horizon entropy
is recovered:

  S_GH = A_horizon / (4 G_N) = pi (c/H_0)^2 / G_N = pi (c/(H_0 ell_P))^2

with ell_P = sqrt(hbar G_N / c^3) the Planck length.

IDENTIFICATION WITH chi

The §14.4.3 critical susceptibility chi is defined by

  chi = A_horizon / (4 ell_P^2) = pi (c/(H_0 ell_P))^2

i.e. chi is the Bekenstein-Hawking horizon entropy in Planck units.

The dS/CFT boundary state (Strominger 2001 JHEP 10:034) identifies
the conformal-symmetry algebra of the dS_4 isometry group SO(4,1) with
the conformal CFT_3 symmetry of the future boundary. The Hartle-Hawking
state on the S^3 supplies a candidate boundary state for this
conformal dictionary.

The CLOSURE direction for O.6:

  - The Hartle-Hawking path integral prepares the state on S^3, and
    the S^2 static-patch bipartition carries the Gibbons-Hawking
    area-law entropy S_GH.

  - This constructs the dS_4 boundary state at the semi-classical
    level and verifies numerical parity of the associated S^2 area
    law with chi. The numerical equality is an identity check rather
    than an independent derivation of entropy from the path integral.

  - The remaining open piece is the FULL dS_4/CFT_3 dictionary at the
    operator level (Strominger 2001 conformal symmetry, Maldacena 2003
    non-normalizable wave functions, Anninos-Hartman-Strominger 2017
    higher-spin dS_4/CFT_3). The semi-classical Hartle-Hawking state
    is the universal entry point; the operator dictionary remains
    conjectural at the dS side but produces the same area-law entropy.

STATUS OF V2 §14.1.5

  The §14.1.5 GCT area-law identification carries Tier 2 standing. The
  Hartle-Hawking state preparation is a standard Tier 1 construction;
  the GCT identification of its static-patch S^2 area law with chi is
  Tier 2. The full dS_4/CFT_3 operator dictionary remains open.

This protocol verifies the static-patch area-law parity
chi = S_static = S_GH numerically with the standard Planck H_0 and
cross-references V2 §14.1.5.
"""

import json
import math
from pathlib import Path

try:
    from gct_utils import get_output_path
    OUTPUT_DIR_AVAILABLE = True
except ImportError:
    OUTPUT_DIR_AVAILABLE = False

# Physical constants
C_LIGHT = 2.99792458e8         # m/s
G_NEWTON = 6.67430e-11         # m^3 kg^-1 s^-2
HBAR = 1.054571817e-34         # J s
MPC_TO_METERS = 3.0857e22

# Planck length
ELL_P_METERS = math.sqrt(HBAR * G_NEWTON / C_LIGHT ** 3)

# Hubble constant Planck 2018 / CODATA 2022
H0_KM_S_MPC = 67.4
H0_SI = (H0_KM_S_MPC * 1000.0) / MPC_TO_METERS  # s^-1
R_DS_METERS = C_LIGHT / H0_SI                   # exact-de-Sitter static-patch radius


def static_patch_S2_area_entropy():
    """Area-law entropy across the S^2 static-patch bifurcation surface.

    The Hartle-Hawking path integral prepares a state on S^3. This
    function evaluates the distinct S^2 area law
      S_static = A_S2 / (4 G_N),
    where A_S2 = 4 pi R_dS^2.
    """
    area_s2 = 4.0 * math.pi * R_DS_METERS ** 2
    return area_s2 / (4.0 * G_NEWTON / C_LIGHT ** 3 * HBAR)


def gibbons_hawking_horizon_entropy():
    """Standard Gibbons-Hawking 1977 cosmological-horizon entropy.

    S_GH = A_horizon / (4 G_N) in natural units, or
         = pi (c / (H_0 ell_P))^2 dimensionless.
    """
    return math.pi * (C_LIGHT / (H0_SI * ELL_P_METERS)) ** 2


def chi_susceptibility_per_section_14_4_3():
    """Critical susceptibility from V2 Ch14 §14.4.3."""
    return math.pi * (C_LIGHT / (H0_SI * ELL_P_METERS)) ** 2


def run():
    s_static = static_patch_S2_area_entropy()
    s_gh = gibbons_hawking_horizon_entropy()
    chi = chi_susceptibility_per_section_14_4_3()

    print("=" * 76)
    print("O.6 PROTOCOL: Hartle-Hawking boundary state for chi")
    print("=" * 76)

    print(f"\nInputs:")
    print(f"  H_0                                       : {H0_KM_S_MPC} km/s/Mpc")
    print(f"  ell_P (Planck length)                     : {ELL_P_METERS:.4e} m")
    print(f"  R_dS = c/H_0 (exact-dS static-patch radius): {R_DS_METERS:.4e} m")
    print(f"  Dimensionless ratio R_dS / ell_P          : {R_DS_METERS/ELL_P_METERS:.4e}")

    print(f"\nStatic-patch area-law parity:")
    print(f"  S_2 static-patch area entropy S_static      : {s_static:.4e}")
    print(f"  Gibbons-Hawking horizon entropy S_GH       : {s_gh:.4e}")
    print(f"  Critical susceptibility chi (§14.4.3)      : {chi:.4e}")

    # Relative differences vanish up to numerical precision.
    rel_static_gh = abs(s_static - s_gh) / s_gh
    rel_chi_gh = abs(chi - s_gh) / s_gh

    print(f"\nRelative differences (should be ~0 for closure):")
    print(f"  |S_static - S_GH| / S_GH                   : {rel_static_gh:.3e}")
    print(f"  |chi - S_GH| / S_GH                        : {rel_chi_gh:.3e}")

    # Closure verdict
    closed = rel_static_gh < 1e-10 and rel_chi_gh < 1e-10
    print(f"\n" + "=" * 76)
    print("VERDICT FOR O.6")
    print("=" * 76)
    if closed:
        verdict = ("Static-patch S^2 area-law parity confirmed: "
                   "S_static = S_GH = chi numerically. The Hartle-Hawking path "
                   "integral prepares the state on S^3; it does not make the "
                   "S^3 a horizon area or entangling surface. Full dS_4/CFT_3 "
                   "operator matching remains open.")
    else:
        verdict = ("Numerical mismatch in the S_static = S_GH = chi area-law parity. "
                   "Check unit conventions and Planck-length definition.")
    print(f"  {verdict}")
    print("=" * 76)

    out = {
        "H0_km_per_s_per_Mpc": H0_KM_S_MPC,
        "H0_SI": H0_SI,
        "c_light_SI": C_LIGHT,
        "G_Newton_SI": G_NEWTON,
        "hbar_SI": HBAR,
        "ell_P_SI": ELL_P_METERS,
        "R_dS_SI": R_DS_METERS,
        "R_dS_over_ell_P": R_DS_METERS / ELL_P_METERS,
        "S_static_patch_S2_area_law": s_static,
        "S_Gibbons_Hawking_horizon": s_gh,
        "chi_critical_susceptibility_section_14_4_3": chi,
        "relative_diff_static_patch_vs_GH": rel_static_gh,
        "relative_diff_chi_vs_GH": rel_chi_gh,
        "closed_at_semiclassical_level": closed,
        "verdict": verdict,
    }
    if OUTPUT_DIR_AVAILABLE:
        out_path = get_output_path("protocol_o6_dscft_hartle_hawking_results.json")
    else:
        out_path = Path(__file__).resolve().parent.parent / "data" / "protocol_o6_dscft_hartle_hawking_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nResults saved to: {out_path}")
    print("=" * 76)


if __name__ == "__main__":
    run()
