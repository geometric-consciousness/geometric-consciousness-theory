"""
verify_phantom_crossing.py — Biogenic dark energy CPL parameterisation
self-consistency check.

V2 Ch14 §14.5 / §14.6.3 (Tier 3 biogenic model). The biogenic DE pipeline
produces a w(z) curve that asymptotes to -1 from below and does NOT
mathematically cross the phantom divide (the direct-brentq integration
returns NaN, confirmed in §14.6.3). Two derived quantities are reported
by the manuscript:

  (a) The broad logistic reference has |w + 1| ≥ 1e-3 near z ≈ 0.28.
      This is NOT the operative Class-2 amplitude. The registered V7'
      Class-2 envelope is |Delta w(0.28)| in [2, 5]e-5, below Roman +
      DESI Year-5 joint-bin precision and tracked here as the current gate.

  (b) When the pipeline w(z) is fit by a standard CPL form
      w(a) = w_0 + w_a(1-a) over the low-z window z in [0, 0.5], the
      precise biogenic DE pipeline fit coefficients are
      (w_0, w_a) = (-1.0037973296449392, +0.013560610917121069),
      and the CPL linear extrapolation crosses w = -1 at
      z_cross^CPL ≈ 0.389 (standard CPL arithmetic
      z_cross^CPL = 1/[1 + (1+w_0)/w_a] − 1) — explicitly flagged as a
      linear-fit artifact (§14.6.3), NOT a physical crossing. Rounding
      w_0 to 3 decimal places gives 0.36 instead of 0.39; the quantity
      is sensitive to small-numerator rounding because (1+w_0) is at the
      few-permille level.

This verifier confirms the CPL arithmetic against the precise pipeline
output. The 0.36 vs 0.39 sensitivity is documented; both values report
the same linear-fit artifact on a Tier 3 calibrated ansatz, not a
Tier 2 prediction.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from report import make_result, write_result, print_summary


def main():
    # Pipeline low-z CPL fit (§14.5.3 / §14.6.3) — values taken directly from
    # the biogenic DE pipeline output (`results/imp01_biogenic_DE_pipeline.json`)
    # to avoid input-rounding sensitivity in the CPL crossing calculation.
    w_0_lag_kernel = -1.005              # §14.5.1 registered lag-kernel amplitude at z=0
    w_0_CPL = -1.0037973296449392        # Biogenic DE low-z CPL fit intercept (precise)
    w_a_CPL = +0.013560610917121069      # Biogenic DE low-z CPL fit slope (precise)

    # Manuscript-stated CPL extrapolation crossing (§14.6.3): explicitly
    # an artifact of linear CPL fit to a curve that asymptotes from below;
    # not a physical crossing. The pipeline fit gives z_cross^CPL ≈ 0.39
    # under the precise (w_0, w_a) above; rounding w_0 to 3 decimals
    # moves the result noticeably (the quantity is sensitive to small-numerator
    # rounding). Both values report the same linear-fit artifact.
    z_cross_CPL_stated = 0.389

    # Broad-reference z marker (§14.6.3): redshift at which the noncanonical
    # logistic illustration reaches |w + 1| >= 1e-3. The operative Class-2
    # envelope is |Delta w(0.28)| in [2, 5]e-5, not this broad reference.
    z_reference_marker = 0.28
    class2_delta_w_band = [2.0e-5, 5.0e-5]

    # Internal consistency: lag-kernel w_0 vs CPL intercept w_0
    w_0_disagreement = abs(w_0_lag_kernel - w_0_CPL)
    w_0_tolerance = 0.010                          # §14.5.3 non-linearity band
    w_0_consistent = w_0_disagreement <= w_0_tolerance

    # CPL arithmetic: w(a) = w_0 + w_a(1-a) = -1 at a = 1 + (1+w_0)/w_a
    a_cross_CPL = 1.0 + (1.0 + w_0_CPL) / w_a_CPL
    z_cross_CPL_computed = 1.0 / a_cross_CPL - 1.0

    z_cross_CPL_disagreement_pct = (
        abs(z_cross_CPL_computed - z_cross_CPL_stated)
        / z_cross_CPL_stated * 100.0
    )
    z_cross_CPL_consistent = z_cross_CPL_disagreement_pct < 5.0

    pass_status = w_0_consistent and z_cross_CPL_consistent

    res = make_result(
        name="w_z_phantom_crossing_z028",
        app_r_label=(
            "Biogenic dark energy CPL parameterisation (V2 Ch14 §14.5 / "
            "§14.6.3): CPL extrapolation z_cross^CPL ≈ 0.39 from precise pipeline fit (artifact; rounding sensitive); "
            "operative Class-2 envelope |Delta w(0.28)| in [2,5]e-5 "
            "(broad logistic z ≈ 0.28 marker is noncanonical)"
        ),
        formula="w(a) = w_0 + w_a(1-a); CPL extrapolation crosses w=-1 at z_cross^CPL = 1/[1 + (1+w_0)/w_a] − 1",
        predicted=z_cross_CPL_computed,
        observed=z_cross_CPL_stated,
        unit="(redshift z)",
        app_r_predicted=z_cross_CPL_stated,
        app_r_precision_str=(
            f"CPL params (w_0={w_0_CPL}, w_a={w_a_CPL}) give linear-extrapolation "
            f"z_cross^CPL = {z_cross_CPL_computed:.4f} (matches manuscript "
            f"{z_cross_CPL_stated} to {z_cross_CPL_disagreement_pct:+.2f}%). "
            f"The underlying w(z) asymptotes to -1 from below; z_cross_direct_brentq = "
            f"NaN confirms no physical crossing. The z≈0.28 marker belongs to the "
            f"broad logistic reference, not the operative Class-2 envelope; the "
            f"registered current envelope is |Delta w(0.28)| in {class2_delta_w_band}. "
            f"Registered lag-kernel w_0 = {w_0_lag_kernel} vs "
            f"CPL intercept w_0 = {w_0_CPL} disagree by {w_0_disagreement:.4f}, within "
            f"the {w_0_tolerance} non-linearity tolerance of §14.5.3."
        ),
        app_r_precision_ppm=None,
        tier="Tier 3 (biogenic model, calibrated; CPL extrapolation = linear-fit artifact, not physical crossing)",
        status="INTERNAL_ARITHMETIC_PASS" if pass_status else "TENSION",
        tolerance_ppm=None,
        extra={
            "w_0_lag_kernel": w_0_lag_kernel,
            "w_0_CPL_intercept": w_0_CPL,
            "w_a_CPL": w_a_CPL,
            "w_0_disagreement": w_0_disagreement,
            "w_0_tolerance_per_section_14_5_3": w_0_tolerance,
            "a_cross_CPL_computed": a_cross_CPL,
            "z_cross_CPL_computed": z_cross_CPL_computed,
            "z_cross_CPL_stated_in_manuscript": z_cross_CPL_stated,
            "z_cross_CPL_disagreement_pct": z_cross_CPL_disagreement_pct,
            "z_broad_logistic_reference_marker": z_reference_marker,
            "class2_delta_w_band_at_z_0_28": class2_delta_w_band,
            "falsification_target": "Stage-V/Roman Year-10 single-bin precision below 5e-5 or multi-channel O.13 fingerprint; DESI DR2 CPL amplitude is sign-opposite and cannot be sourced by the biogenic channel alone.",
            "derivation_note": (
                "This verifier confirms internal arithmetic consistency of "
                "the §14.5.3 / §14.6.3 CPL fit. The CPL extrapolation "
                "z_cross^CPL ≈ 0.39 (precise pipeline fit) is a linear-fit artifact, NOT a "
                "physical phantom crossing — the underlying w(z) asymptotes "
                "to -1 from below and z_cross_direct_brentq = NaN. The "
                "z ≈ 0.28 marker belongs to the broad logistic reference "
                "(|w+1| >= 1e-3), a separate noncanonical illustration from "
                "the CPL crossing. Tier 3 calibrated; the operative "
                "Class-2 envelope per §14.6.3 is |Delta w(0.28)| in "
                "[2,5]e-5, below Roman + DESI Year-5 joint-bin precision."
            ),
        },
    )
    print_summary(res)
    write_result(res)
    return res


if __name__ == "__main__":
    main()
