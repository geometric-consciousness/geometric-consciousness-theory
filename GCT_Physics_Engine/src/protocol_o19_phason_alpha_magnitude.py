#!/usr/bin/env python3
"""
protocol_o19_phason_alpha_magnitude.py
======================================

Sign-validation diagnostic for Open Problem O.19 (App H §H.5; magnitude
not closed, see verdict framework below): given the sign-validated
NAGT-style phason anti-screening mechanism (App M §M.7.1, verified by
protocol_phason_oneloop_AKN.py), test whether the candidate icosahedral
group-theory structure supplies the alpha-closure shift.

OPERATIVE TARGET VS BARE RESIDUAL

Two residuals appear in this closure problem and they must not be
conflated (App M §M.7.1; App H O.19):

  - The BARE residual is +3442 ppm: the GCT tree-level
    alpha^(-1) = 360 phi^(-2) = 137.508 sits 3442 ppm above the observed
    137.036.
  - The OPERATIVE O.19 target is the +41.6 ppm POST-BILAYER residual:
    the bilayer handle 1/(2N) = 1/288 reduces the bare 3442 ppm mismatch
    to a 41.6 ppm remainder, and that 41.6 ppm remainder is the
    magnitude the discrete AKN bubble integral must derive. App M §M.7.1
    and App H O.19 both state this verbatim: the loop calculation targets
    the 41.6 ppm residual only, NOT the full +3442 ppm bare residual.

This protocol evaluates the continuous-gauge NAGT running formula against
the BARE +3442 ppm residual as an order-of-magnitude diagnostic of the
gauge-theory template; the back-solved coefficient it reports is a
diagnostic of that template, not a closure of the operative 41.6 ppm
target. The verdict therefore stops at "sign-validated only" for both
framings (see VERDICT FRAMEWORK below). Sign validation already
established that the GCT direction alpha^(-1)_bare > alpha^(-1)_obs is
sign-consistent with NAGT-style bosonic anti-screening; the magnitude
(whether for the bare 3442 ppm template or the operative 41.6 ppm target)
remains OPEN.

ONE-LOOP RUNNING FORMULA

Standard non-abelian gauge theory (Peskin & Schroeder Ch. 16):
  alpha^(-1)(mu) = alpha^(-1)(M) + (b/(2*pi)) ln(M/mu)
  with b = (11/3) C_2(G) - (4/3) sum_f T(R_f) - (1/3) sum_s T(R_s)
  for pure-gauge (no matter): b = (11/3) C_2(G)
  Anti-screening direction: alpha^(-1)(UV) > alpha^(-1)(IR) when b > 0.

For the GCT phason-photon system, the icosahedral lattice acts as the
"gauge group" of the phason gauge field. The one-loop running between
the icosahedral UV reference (alpha^(-1)_bare = 360 phi^(-2)) and the
IR observed scale (alpha^(-1)_obs = 137.036) takes the form:

  Delta alpha^(-1) = alpha^(-1)_bare - alpha^(-1)_obs
                   = (b_phason / (2*pi)) ln(Lambda_UV / Lambda_IR)

with Lambda_UV = M_Planck (icosahedral cutoff) and Lambda_IR = m_e
(Thomson reference; below which QED screening dominates).

ICOSAHEDRAL STRUCTURE CONSTANT

Nomenclature note. H_3 (the icosahedral Coxeter group) is a finite
reflection group, not a Lie group, and does not admit a quadratic
Casimir in the standard Lie-algebraic sense (the center of its group
algebra is spanned by class sums rather than by a quadratic invariant
operator). The canonical analogues for finite reflection groups are
the Solomon-style symmetric power-sums of Coxeter exponents in the
polynomial invariant algebra S(V)^{H_3} (Solomon 1963, "Invariants of
Finite Reflection Groups," Nagoya Math. J. 22:57-64); the formulas below use class-sum / character-orthogonality
projection structure rather than Lie-Casimir eigenvalues. The code uses
the neutral name `class_sum_eff` for the back-solved finite-group
coefficient so it is not mistaken for a Lie-algebraic Casimir.

The icosahedral point group I_h has irreducible representations of
dimensions {1, 1, 3, 3, 3, 3, 4, 4, 5, 5} (incorporating the Z_2
inversion). The icosahedral-irrep-orbit weights from character
orthogonality (Sum_R |R|^2 = |G|, with |I| = 60 rotational, |I_h| =
120 full) supply the projection structure used below; the largest
irreps (dim 5) carry the largest orbit weight.

For NAGT-style b_phason:
  b_phason = (11/3) * class_sum_eff_phason
where class_sum_eff_phason is the effective coefficient capturing the
combined contributions of all icosahedral phason modes that propagate
in the vacuum-polarization bubble. It is structurally a class-sum /
character-orthogonality projection, not a Lie-Casimir eigenvalue.

NUMERICAL ANCHORS

  alpha^(-1)_bare = 360 * phi^(-2) = 137.508  (Tier 2 mechanism + Tier 3 multiplier)
  alpha^(-1)_obs  = 137.036                  (CODATA 2022)
  Delta alpha^(-1)_bare = 0.472              (~ 3442 ppm fractional; diagnostic
                                              anchor for the gauge-theory template)
  Operative O.19 target = 41.6 ppm           (post-bilayer residual after the
                                              1/(2N)=1/288 handle removes
                                              3442 -> 41.6 ppm)

  M_Planck = 1.22e19 GeV
  m_e      = 5.11e-4 GeV
  ln(M_P / m_e) ~ 51.5

  Required b_phason for the BARE +3442 ppm diagnostic template:
    b_phason = 2 * pi * Delta alpha^(-1)_bare / ln(M_P / m_e)
             = 2 * pi * 0.472 / 51.5
             ~ 0.0576
  (For the operative 41.6 ppm target the same template back-solves to
  b_phason of order 7e-4 and a class-sum coefficient of order 2e-4, which
  sits below the icosahedral bracket; see App M §M.7.1. Either way the
  magnitude is OPEN.)

VERDICT FRAMEWORK (sign-validated only)

Two structural caveats preclude promotion of this protocol's output
to a magnitude-closure of O.19:

  (a) The NAGT (11/3) C_2 beta function presupposes a continuous
      propagating gauge boson with ghost cancellation; the icosahedral
      I_h symmetry of the AKN substrate is a discrete reflection group
      that does not admit a quadratic Casimir in the standard Lie-
      algebraic sense.

  (b) The assumed class_sum_eff bracket [~0.013, ~2.0] spans two orders of
      magnitude and is therefore wide enough to be re-tuned for any
      output near the bare +3442 ppm diagnostic template. Falling inside
      this wide bracket is a posterior-bracketing observation, not a
      structural derivation of the magnitude. Moreover, for the operative
      41.6 ppm post-bilayer target the back-solved coefficient (~2e-4)
      falls BELOW the icosahedral bracket entirely, so even the wide
      bracket does not absorb the operative target -- the group theory
      under-produces the needed coefficient by ~2 orders of magnitude.

The verdict logic of this protocol consequently stops at "sign-
validated only" regardless of where the required class_sum_eff value lands
in the bracket. App M §M.7.1 magnitude-closure of O.19 remains OPEN
under two paths: (i) a discrete-lattice analogue of continuous-gauge
running (Kotani-Sunada operator algebra on AKN, or a finite-group
Bost-Connes analysis); (ii) a first-principles derivation of class_sum_eff
from explicit icosahedral irrep theory plus the AKN bubble integral.
Closure of (i) or (ii) bundles with Open Problem O.5 (QLQCD-1L).
"""

import json
import math
import numpy as np
from pathlib import Path

try:
    from gct_utils import get_output_path, C
    OUTPUT_DIR_AVAILABLE = True
except ImportError:
    OUTPUT_DIR_AVAILABLE = False

# Constants
PHI = float(C.PHI)
ALPHA_INV_BARE = 360.0 * PHI ** (-2)  # 137.508
ALPHA_INV_OBS = 137.036
DELTA_ALPHA_INV = ALPHA_INV_BARE - ALPHA_INV_OBS

# Energy scales
M_PLANCK_GEV = 1.220890e19
M_ELECTRON_GEV = 5.10999e-4
LN_RATIO_UV_IR = math.log(M_PLANCK_GEV / M_ELECTRON_GEV)  # ~ 51.5

# NAGT formula factor
NAGT_FACTOR = 11.0 / 3.0


def required_b_phason():
    """b_phason required from one-loop running formula."""
    return 2.0 * math.pi * DELTA_ALPHA_INV / LN_RATIO_UV_IR


def required_class_sum_eff(b_phason):
    """Finite-group class-sum coefficient from b = (11/3) * class_sum_eff."""
    return b_phason / NAGT_FACTOR


def icosahedral_class_sum_estimates():
    """Estimate the class_sum_eff range for icosahedral phason gauge structure.

    NOMENCLATURE NOTE: H_3 / I_h is a finite reflection / Coxeter group,
    not a Lie group; the center of its group algebra is spanned by
    class sums rather than a quadratic Lie-Casimir invariant. The
    "class_sum_eff_phason" coefficient below is a CLASS-SUM / CHARACTER-
    ORTHOGONALITY PROJECTION COEFFICIENT, derived by analogy with the
    SO(3) quadratic-Casimir contribution to the gauge-theory beta
    function (Peskin & Schroeder eq. 16.131) but constructed via the
    Newton power-sum / class-sum apparatus appropriate to a finite
    reflection group. The name "C_2" is retained for cross-reference
    with the gauge-theory literature it benchmarks against, NOT as a
    claim that I_h admits a quadratic Casimir.

    The icosahedral group I_h has rotational subgroup I of order 60 with
    irreps of dimensions {1, 3, 3, 4, 5}. The class-sum / character-
    orthogonality projection coefficient for these irreps can be
    computed via the standard finite-group character-table apparatus
    (Solomon 1963 for the reflection-group Newton power-sum form). For
    an order-of-magnitude estimate the relevant icosahedral class-sum
    weight is the discrete-group analogue of the SO(3) Casimir
    contribution; it is not a Lie-algebra structure constant of H_3/I_h.

    The standard SO(3) NAGT case gives b = (11/3) * 2 = 22/3 with
    C_2(SO(3) adjoint) = 2 (Peskin & Schroeder eq. 16.131). For the
    icosahedral phason, the analogous discrete-group structure constant
    differs from SO(3) by:
      1. The discrete nature: only 120 group elements (I_h) contribute
         to the vacuum polarization bubble vs continuous SO(3).
      2. The icosahedral irreps {1, 3, 3, 4, 5} replace continuous SO(3)
         irreps of integer spin.
      3. The lattice cutoff suppresses high-momentum modes.

    A conservative estimate: class_sum_eff_phason ~ 1/N_sites * SO(3)_C_2
    where N_sites is the number of I_h-closed cage sites contributing.
    Reasonable sites: 12 vertices + 30 edges + 20 faces + 60 inversion-
    paired sites + 30 edge-pairs = 152 sites (per the I_h-closed cage
    construction; see cage_builder.build_canonical_cage(size=152)). This
    is a site-count dilution heuristic, not an orbit count.

    Estimate: class_sum_eff_phason ~ 2 / 152 ~ 0.013 (lower bound, single
    leading site)
    OR class_sum_eff_phason ~ 2 * sum_d d^2 / 60 ~ 2 * (1 + 9 + 9 + 16 + 25)/60
                     = 2 * 60/60 = 2 (icosahedral irrep-sum normalised)

    These two estimates bracket the icosahedral group-theory range.
    """
    # SO(3) baseline
    so3_c2_adjoint = 2.0
    so3_irrep_dim_sum_sq = 1 + 9  # (1)^2 + (3)^2 dimensions for spin-0 and spin-1

    # I_h-closed cage site count from the C2 investigation.
    n_icosahedral_sites = 152

    # Icosahedral irrep dimensions {1, 3, 3, 4, 5}; sum of squared dims = 60 = |I|
    ico_irrep_dims = [1, 3, 3, 4, 5]
    ico_irrep_dim_sum_sq = sum(d ** 2 for d in ico_irrep_dims)
    ico_group_order = 60  # |I|

    # Range estimates
    c2_lower = so3_c2_adjoint / n_icosahedral_sites  # ~0.013
    c2_upper = so3_c2_adjoint * ico_irrep_dim_sum_sq / ico_group_order  # ~2.0
    c2_geometric_mean = math.sqrt(c2_lower * c2_upper)

    return {
        "SO3_baseline_C2": so3_c2_adjoint,
        "n_icosahedral_sites_Ih_closed_cage": n_icosahedral_sites,
        "icosahedral_irrep_dims": ico_irrep_dims,
        "icosahedral_irrep_dim_sum_sq": ico_irrep_dim_sum_sq,
        "icosahedral_group_order": ico_group_order,
        "class_sum_eff_lower_bound": c2_lower,
        "class_sum_eff_upper_bound": c2_upper,
        "class_sum_eff_geometric_mean": c2_geometric_mean,
    }


def b_phason_for_class_sum(class_sum_eff):
    """b_phason from NAGT-style formula given class_sum_eff."""
    return NAGT_FACTOR * class_sum_eff


def delta_alpha_inv_from_b(b_phason):
    """Predicted Delta alpha^(-1) from running formula."""
    return b_phason * LN_RATIO_UV_IR / (2.0 * math.pi)


def run_sign_diagnostic():
    """Compute the sign diagnostic; the magnitude remains open."""
    b_required = required_b_phason()
    class_sum_required = required_class_sum_eff(b_required)
    ico = icosahedral_class_sum_estimates()

    # Sweep over class_sum_eff in the icosahedral range
    c2_grid = np.logspace(
        math.log10(ico["class_sum_eff_lower_bound"]),
        math.log10(ico["class_sum_eff_upper_bound"]),
        20,
    )
    sweep = []
    for c2 in c2_grid:
        b = b_phason_for_class_sum(c2)
        dalpha = delta_alpha_inv_from_b(b)
        delta_ppm = dalpha / ALPHA_INV_OBS * 1e6
        sweep.append({
            "class_sum_eff": float(c2),
            "b_phason": float(b),
            "delta_alpha_inv": float(dalpha),
            "delta_ppm": float(delta_ppm),
        })

    # Identify the class-sum value that gives the observed 3442 ppm
    delta_ppm_arr = np.array([s["delta_ppm"] for s in sweep])
    c2_arr = np.array([s["class_sum_eff"] for s in sweep])
    target_ppm = DELTA_ALPHA_INV / ALPHA_INV_OBS * 1e6  # ~ 3445 ppm
    if delta_ppm_arr.min() <= target_ppm <= delta_ppm_arr.max():
        # log-log interp
        # Interpolated diagnostic value — NOT a derived match (see verdict framing).
        c2_match = float(10 ** np.interp(
            math.log10(target_ppm),
            np.log10(delta_ppm_arr),
            np.log10(c2_arr),
        ))
    else:
        c2_match = float("nan")

    # Verdict — sign-validated only.
    # This diagnostic back-solves the class-sum coefficient against the bare
    # +3442 ppm residual as an order-of-magnitude test of the continuous-gauge
    # template; the operative O.19 closure target is the 41.6 ppm post-bilayer
    # residual (App M §M.7.1; App H O.19), for which the back-solved coefficient
    # (~2e-4) falls below the icosahedral bracket.
    # The NAGT (11/3) C_2 beta function presupposes a continuous propagating
    # gauge boson + ghost cancellation; the icosahedral I_h symmetry of the
    # AKN substrate is a discrete reflection group that does not admit a
    # quadratic Casimir in the standard Lie-algebraic sense. The
    # class_sum_eff range [~0.013, ~2.0] spans two orders of magnitude and is
    # therefore wide enough to be re-tuned for any output near the bare
    # +3442 ppm template. Falling inside this wide range is NOT a structural
    # derivation of the magnitude; it is a posterior-bracketing observation.
    # The required value is reported, the wide-bracket-membership is reported,
    # and the verdict explicitly stops at "sign-validated only" regardless
    # of where in the bracket the required value lands.
    consistent_with_range = (
        ico["class_sum_eff_lower_bound"] <= class_sum_required <= ico["class_sum_eff_upper_bound"]
    )

    direction = (
        "Sign-validated only. NAGT-style continuous-gauge running framework "
        "reproduces the +3442 ppm shift direction with bosonic-anti-screening "
        "convention. The magnitude is NOT structurally derived: the "
        "icosahedral I_h symmetry is a discrete reflection group without a "
        "quadratic Casimir in the Lie-algebraic sense, and the assumed "
        "class_sum_eff bracket spans two orders of magnitude -- wide enough to "
        "be re-tuned for any output near the +3442 ppm target."
    )
    bracket_membership = "INSIDE bracket" if consistent_with_range else (
        "BELOW bracket" if class_sum_required < ico["class_sum_eff_lower_bound"] else "ABOVE bracket"
    )
    framing = (
        f"Required class_sum_eff = {class_sum_required:.4f}; assumed icosahedral bracket "
        f"[{ico['class_sum_eff_lower_bound']:.4f}, {ico['class_sum_eff_upper_bound']:.4f}] "
        f"(two orders of magnitude wide). Required value is {bracket_membership}. "
        f"App M §M.7.1 status: sign-validated mechanism only; magnitude closure "
        f"remains open under O.19 with two closure paths — (a) a discrete-"
        f"lattice analogue of the continuous-gauge running (Kotani-Sunada "
        f"operator algebra on AKN, or finite-group Bost-Connes), or (b) a "
        f"first-principles derivation of class_sum_eff from icosahedral irrep "
        f"theory + AKN bubble integral; bundles with O.5."
    )

    return {
        "alpha_inv_bare": ALPHA_INV_BARE,
        "alpha_inv_obs": ALPHA_INV_OBS,
        "delta_alpha_inv": DELTA_ALPHA_INV,
        "delta_ppm_target": float(target_ppm),
        "M_Planck_GeV": M_PLANCK_GEV,
        "M_electron_GeV": M_ELECTRON_GEV,
        "ln_ratio_UV_IR": LN_RATIO_UV_IR,
        "NAGT_factor_11_over_3": NAGT_FACTOR,
        "b_phason_required": b_required,
        "class_sum_eff_backsolved_required__diagnostic_only": class_sum_required,
        "icosahedral_estimates": ico,
        "class_sum_eff_sweep": sweep,
        "class_sum_eff_backsolved_interp_to_target_ppm__diagnostic_only": c2_match,
        "class_sum_eff_backsolved_interp_to_target_ppm__diagnostic_note": "Interpolation-on-log-grid diagnostic; not a derived match -- the protocol's verdict is sign-validated-only, the class_sum_eff value here is for inspection of where the target ppm sits in the swept range and should NOT be treated as the magnitude derivation. Magnitude derivation closure is registered under App H O.19; the sweep here gives only the order-of-magnitude bracket.",
        "backsolved_value_falls_inside_wide_retunable_bracket__not_validation": bool(consistent_with_range),
        "registry_claim_scope": "Sign-validation only; not a parameter-free magnitude closure.",
        "verdict": direction,
        "framing": framing,
    }


def main():
    print("=" * 76)
    print("O.19 Phason α Sign Validation (Diagnostic, NOT closure). Magnitude remains Open per App H O.19 / App M §M.7.1.")
    print("=" * 76)

    out = run_sign_diagnostic()

    print(f"\nInputs:")
    print(f"  alpha^(-1)_bare = 360 * phi^(-2)       : {out['alpha_inv_bare']:.4f}")
    print(f"  alpha^(-1)_obs  (CODATA 2022)         : {out['alpha_inv_obs']:.4f}")
    print(f"  Delta alpha^(-1)                       : {out['delta_alpha_inv']:.4f}")
    print(f"  Delta ppm (target)                     : {out['delta_ppm_target']:.0f}")
    print(f"  ln(M_Planck / m_e)                     : {out['ln_ratio_UV_IR']:.2f}")
    print(f"  NAGT pure-gauge factor (11/3)          : {out['NAGT_factor_11_over_3']:.4f}")

    print(f"\nRequired coefficients:")
    print(f"  b_phason (from running formula)        : {out['b_phason_required']:.4f}")
    print(f"  class_sum_eff backsolved diagnostic    : {out['class_sum_eff_backsolved_required__diagnostic_only']:.4f}")

    ico = out["icosahedral_estimates"]
    print(f"\nIcosahedral group-theory range:")
    print(f"  SO(3) C_2 baseline                     : {ico['SO3_baseline_C2']:.1f}")
    print(f"  N icosahedral sites (I_h-closed cage)  : {ico['n_icosahedral_sites_Ih_closed_cage']}")
    print(f"  Icosahedral irrep dimensions           : {ico['icosahedral_irrep_dims']}")
    print(f"  Sum of squared dims                    : {ico['icosahedral_irrep_dim_sum_sq']} (= |I|)")
    print(f"  class_sum_eff lower bound              : {ico['class_sum_eff_lower_bound']:.4f}")
    print(f"  class_sum_eff upper bound              : {ico['class_sum_eff_upper_bound']:.4f}")
    print(f"  class_sum_eff geometric mean           : {ico['class_sum_eff_geometric_mean']:.4f}")

    print(f"\nSweep over class_sum_eff (log-log):")
    print(f"  {'class_sum':>10}  {'b_phason':>10}  {'Delta alpha^-1':>15}  {'Delta ppm':>12}")
    for s in out["class_sum_eff_sweep"]:
        print(f"  {s['class_sum_eff']:>10.4f}  {s['b_phason']:>10.4f}  "
              f"{s['delta_alpha_inv']:>15.4e}  {s['delta_ppm']:>12.0f}")

    print(f"\n" + "=" * 76)
    print("VERDICT FOR O.19")
    print("=" * 76)
    print(f"  Direction: {out['verdict']}")
    print(f"")
    print(f"  class_sum_eff backsolved for +3442 ppm : {out['class_sum_eff_backsolved_required__diagnostic_only']:.4f}")
    print(f"  backsolved interpolation diagnostic    : {out['class_sum_eff_backsolved_interp_to_target_ppm__diagnostic_only']:.4f}")
    print(f"  Falls inside wide retunable bracket    : "
          f"{'YES' if out['backsolved_value_falls_inside_wide_retunable_bracket__not_validation'] else 'NO'}")
    print(f"")
    print(f"  Framing: {out['framing']}")
    print("=" * 76)

    if OUTPUT_DIR_AVAILABLE:
        out_path = get_output_path("protocol_o19_phason_alpha_magnitude_results.json")
    else:
        out_path = Path(__file__).resolve().parent.parent / "data" / "protocol_o19_phason_alpha_magnitude_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nResults saved to: {out_path}")
    print("=" * 76)


if __name__ == "__main__":
    main()
