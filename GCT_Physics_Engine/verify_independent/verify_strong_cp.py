"""
verify_strong_cp.py — Strong CP / theta-bar candidate-sketch record (no prediction).

V3 Ch22 §22.3.1 states aspirationally: "QLQCD will resolve the Strong
CP Problem through geometric matching rules." No mechanism is currently
specified in the manuscript prose.

theta-bar = 0 is NOT a GCT prediction: the Strong CP problem is open in
GCT (V3 Ch18 §18.5), and the present action derives no symmetry or dynamics
that suppresses theta. This verifier records an icosahedral
chirality-preservation argument only as a Tier 3 candidate sketch, and the
scorecard row is OPEN_CONDITIONAL; respecting the nEDM bound is not a PASS.

The Tier 3 mechanism:
 The QCD θ-term enters the Lagrangian as
 L_θ = (θ / 32π²) · ε^{μνρσ} F_{μν}^a F_{ρσ}^a
 which is a total derivative integrating to a topological invariant.
 On the AKN icosahedral lattice, all chirality-preserving cycles
 (5-fold, 3-fold, 2-fold rotations of the icosahedral group I_h)
 close at multiples of 2π exactly. The cut-and-project from Z⁶ to
 the physical manifold preserves this discrete closure, forcing the
 integrated topological charge of any consistent gauge configuration
 to be an integer multiple of 2π. Modulo 2π, the physical θ-angle
 is claimed to lie in the trivial topological class:
 θ̄ ≡ 0 (mod 2π) → θ̄_physical = 0
 (Integer topological charge makes θ 2π-periodic; it does not select θ̄.)

 Why this is Tier 3 (not Tier 1):
 The mechanism is sketched but not rigorously derived. A Tier 1
 proof would require showing:
 (a) NO order of perturbation theory generates a non-vanishing
 θ̄ from the icosahedral matching rules — i.e., the topological
 quantisation is anomaly-free under phason quantum corrections.
 (b) The specific selection rule from the cut-and-project preserves
 the discrete closure exactly under projection (not merely up
 to O(α) corrections).
 Both (a) and (b) are precisely the kind of non-perturbative
 statements that QLQCD-1L closure delivers. The mechanism is
 therefore registered as Tier 3 here with explicit theorem-grade promotion
 path bundled with QLQCD-1L.

Experimental anchor (falsification target):
 Current best bound on neutron EDM: |d_n| < 1.8 × 10⁻²⁶ e·cm (2020).
 Translates to |θ̄| < 10⁻¹⁰ (using standard hadronic-matrix-element
 estimates).
 Candidate sketch output (not a GCT prediction): θ̄ = 0.
 Next-gen experiments (SNS nEDM, n2EDM at PSI) targeting |d_n| ~
 10⁻²⁸ → |θ̄| ~ 10⁻¹². Still consistent with θ̄ = 0.

This verifier records a candidate sketch; it registers no prediction.
Note on the sketch: integer topological charge is what makes θ 2π-periodic;
it does not by itself select θ̄ = 0, so the sketch is a non sequitur until
an independent selection argument is supplied.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import CODATA, MATH
from report import make_result, write_result, print_summary, status_from_upper_bound


# Experimental anchor: neutron EDM bound translates to θ̄ bound
# Standard relation: d_n ≈ θ̄ × e·m_q / Λ_QCD² ~ 10⁻¹⁶ × θ̄ e·cm
D_N_BOUND_E_CM = 1.8e-26 # nEDM Collaboration 2020 (90% CL)
THETA_BAR_BOUND = 1.0e-10 # Implied bound on θ̄ (standard estimate)


def main():
 # Candidate-sketch value θ̄ = 0 (not a GCT prediction; Strong CP open,
 # V3 Ch18 §18.5).
 theta_bar_gct = 0.0

 # This is a one-sided upper-limit compatibility check, not a measurement of
 # zero and not theorem closure.  Equality is outside the strict bound.
 status = status_from_upper_bound(
  theta_bar_gct, THETA_BAR_BOUND, derivation_open=True
 )

 res = make_result(
 name="strong_cp_theta_bar",
 app_psc_label="Strong CP / θ̄ (open; candidate matching-rule sketch only)",
 formula="θ̄ ≡ 0 (mod 2π) → θ̄_physical = 0 from chirality-preserving icosahedral cycle closure",
 predicted=theta_bar_gct,
 observed=0.0, # Consistent with 0 within bounds
 unit="(rad)",
 app_psc_predicted=0.0,
        app_psc_precision_str=f"Strong CP open in GCT (V3 Ch18 §18.5); θ̄ = 0 is a Tier 3 candidate sketch, not a prediction; nEDM bound |θ̄| < 10⁻¹⁰; OPEN_CONDITIONAL",
 app_psc_precision_ppm=None,
        tier="Open problem (Tier 3 candidate mechanism only; no derivation)",
 status=status,
 tolerance_ppm=None,
 extra={
 "theta_bar_candidate_sketch": theta_bar_gct,
 "neutron_edm_bound_e_cm": D_N_BOUND_E_CM,
 "theta_bar_bound_implied": THETA_BAR_BOUND,
 "upper_bound_rule": "OPEN_CONDITIONAL iff |theta_bar| < bound while QLQCD-1L remains open; equality or excess is FAIL",
 "mechanism": (
 "On the AKN icosahedral lattice, all chirality-preserving "
 "cycles (5-fold, 3-fold, 2-fold rotations of I_h) close at "
 "multiples of 2π exactly. The cut-and-project from Z⁶ "
 "preserves this discrete closure, forcing the topological "
 "charge of any consistent gauge configuration to integer "
 "multiples of 2π. The sketch then places θ̄ in the trivial "
 "topological class (θ̄ = 0). Integer topological charge makes "
 "θ 2π-periodic but does not by itself select θ̄ = 0; Tier 3 "
 "candidate sketch only, not a prediction."
 ),
 "tier_1_promotion_path": (
 "QLQCD-1L closure (Open Problem O.5). Requires showing "
 "(a) anomaly-free topological quantisation under phason "
 "quantum corrections; (b) cut-and-project preserves "
 "discrete closure exactly (not up to O(α) corrections). "
 "Both are non-perturbative statements bundled with the "
 "QLQCD-1L research programme."
 ),
 "falsifier": (
 "Next-gen nEDM measurements (SNS, n2EDM) reaching "
 "|d_n| < 10⁻²⁸ e·cm → |θ̄| < 10⁻¹² without detection "
 "would not support GCT, since θ̄ = 0 is not a GCT prediction. "
 "A robust non-zero θ̄ (an nEDM detection at >3σ) would rule out "
 "the candidate sketch."
 ),
 },
 )
 print_summary(res); write_result(res)
 return res


if __name__ == "__main__":
 main()
