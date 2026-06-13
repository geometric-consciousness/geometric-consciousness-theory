"""
verify_hypercharges.py — Right-handed hypercharges + four-anomaly cancellation.

Two checks performed on the SM hypercharge assignment used throughout
the manuscript:

  (1) Right-handed singlet identity Y_R = 2Q (V3 Ch04). For right-handed
      sterile singlets (I_3 = 0) the Gell-Mann–Nishijima relation
      Q = T_3 + Y/2 reduces to Y_R = 2Q. Trivial algebraic check given
      the standard SM electric charges; the Tier 2 epistemic content
      attaches to the E_∥/E_⊥ split assumption identifying right-handed
      singlets with E_⊥-sterile states (Parameter Ledger §2).

  (2) The four Standard Model gauge-anomaly cancellation conditions on
      the L/R-asymmetric hypercharge assignment (one generation):

        (a) [SU(3)]² U(1)_Y  : 2 Y_Q  − Y_u − Y_d                  = 0
        (b) [SU(2)]² U(1)_Y  : 3 Y_Q  + Y_L                        = 0
        (c) grav² U(1)_Y     : 6 Y_Q + 2 Y_L − 3 Y_u − 3 Y_d − Y_e = 0
        (d) [U(1)_Y]³        : 6 Y_Q³ + 2 Y_L³ − 3 Y_u³ − 3 Y_d³ − Y_e³ = 0

      Convention: Q = T_3 + Y/2 (Connes-Chamseddine / typical NCG-SM
      convention; see Ch06 §6.5). Color multiplicity 3 enters explicitly
      on quark contributions; the SU(2) multiplicity 2 enters on the
      gravitational and U(1)³ anomalies via the doublet components.
      Coefficients (+) and (−) reflect LH (positive) vs RH (negative,
      via chirality flip) contributions to the anomaly trace.

      Manuscript hypercharges (one generation):
        Y_Q  = +1/3   (LH quark doublet, color triplet)
        Y_u  = +4/3   (u_R, color triplet)
        Y_d  = -2/3   (d_R, color triplet)
        Y_L  = -1     (LH lepton doublet)
        Y_e  = -2     (e_R)

      Each of the four anomaly traces must vanish identically; the four
      conditions form a system of three independent constraints
      (one is implied by the others modulo overall normalization), so
      the SM hypercharges are essentially anomaly-uniquely-determined
      modulo the Y_Q overall scale.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from report import make_result, write_result, print_summary


def main():
    # ── (1) Right-handed singlet check ────────────────────────────────
    Q_uR, Q_dR, Q_eR = +2.0 / 3.0, -1.0 / 3.0, -1.0
    Y_uR_pred = 2.0 * Q_uR
    Y_dR_pred = 2.0 * Q_dR
    Y_eR_pred = 2.0 * Q_eR
    Y_uR_stated = 4.0 / 3.0
    Y_dR_stated = -2.0 / 3.0
    Y_eR_stated = -2.0
    rh_residuals = [
        abs(Y_uR_pred - Y_uR_stated),
        abs(Y_dR_pred - Y_dR_stated),
        abs(Y_eR_pred - Y_eR_stated),
    ]
    rh_max_resid = max(rh_residuals)
    rh_matches = rh_max_resid < 1e-12

    # ── (2) Four-anomaly cancellation check ───────────────────────────
    # Convention: Q = T_3 + Y/2; hypercharges as defined above.
    Y_Q = 1.0 / 3.0      # LH quark doublet
    Y_u = 4.0 / 3.0      # u_R
    Y_d = -2.0 / 3.0     # d_R
    Y_L = -1.0           # LH lepton doublet
    Y_e = -2.0           # e_R

    # (a) [SU(3)]² U(1)_Y : 2 Y_Q − Y_u − Y_d
    A_su3_sq = 2.0 * Y_Q - Y_u - Y_d

    # (b) [SU(2)]² U(1)_Y : 3 Y_Q + Y_L  (color multiplicity 3 on quark
    #     doublet; SU(2) multiplicity 2 cancels symmetrically)
    A_su2_sq = 3.0 * Y_Q + Y_L

    # (c) gravitational² U(1)_Y : Σ_LH Y − Σ_RH Y, with color × SU(2)
    #     multiplicities. LH: 6 Y_Q (quark doublet 3 × 2) + 2 Y_L (lepton doublet 2).
    #     RH: 3 Y_u + 3 Y_d + Y_e (the three singlets, color counted).
    A_grav = 6.0 * Y_Q + 2.0 * Y_L - 3.0 * Y_u - 3.0 * Y_d - Y_e

    # (d) [U(1)_Y]³ : same multiplicities, cubed hypercharges
    A_u1_cube = (
        6.0 * Y_Q**3 + 2.0 * Y_L**3
        - 3.0 * Y_u**3 - 3.0 * Y_d**3 - Y_e**3
    )

    anomaly_results = {
        "[SU(3)]^2 U(1)_Y":    A_su3_sq,
        "[SU(2)]^2 U(1)_Y":    A_su2_sq,
        "grav^2 U(1)_Y":       A_grav,
        "[U(1)_Y]^3":          A_u1_cube,
    }
    anomaly_max_resid = max(abs(v) for v in anomaly_results.values())
    anomaly_cancels   = anomaly_max_resid < 1e-12

    # ── Combined verdict ──────────────────────────────────────────────
    total_max_resid = max(rh_max_resid, anomaly_max_resid)
    all_pass = rh_matches and anomaly_cancels

    res = make_result(
        name="hypercharges_and_anomaly_cancellation",
        app_r_label="Right-handed hypercharges Y_R = 2Q + four-anomaly SM cancellation",
        formula="Y_R = 2Q (right-handed singlets); [SU(3)]^2 U(1), [SU(2)]^2 U(1), grav^2 U(1), [U(1)]^3 anomalies all vanish",
        predicted=total_max_resid,
        observed=0.0,
        unit="(L_inf residual across right-handed identity + four anomaly traces)",
        app_r_predicted=0.0,
        app_r_precision_str=(
            "Right-handed singlet identity Y_R = 2Q exact; "
            "four SM anomaly conditions all evaluate to 0 to machine precision "
            "with Y_Q=+1/3, Y_u=+4/3, Y_d=-2/3, Y_L=-1, Y_e=-2 (Q = T_3 + Y/2 convention). "
            f"Anomaly values: [SU(3)]^2 U(1) = {A_su3_sq:.2e}, "
            f"[SU(2)]^2 U(1) = {A_su2_sq:.2e}, "
            f"grav^2 U(1) = {A_grav:.2e}, "
            f"[U(1)]^3 = {A_u1_cube:.2e}."
        ),
        app_r_precision_ppm=0.0,
        tier="Tier 1 algebraic identity (anomaly cancellation is the standard SM textbook identity check per Bilal 2008 §7.3 given the L/R-asymmetric hypercharge assignment) + Tier 2 GCT-specific L/R-asymmetric assignment Y_R = 2Q (App R §R.2.2)",
        status="PASS" if all_pass else "FAIL",
        tolerance_ppm=None,
        extra={
            "right_handed_singlet_check": {
                "Y_uR_predicted": Y_uR_pred,
                "Y_dR_predicted": Y_dR_pred,
                "Y_eR_predicted": Y_eR_pred,
                "residuals": rh_residuals,
                "L_inf_residual": rh_max_resid,
                "exact_match": rh_matches,
            },
            "anomaly_cancellation_check": {
                "convention": "Q = T_3 + Y/2 (Connes-Chamseddine / NCG-SM)",
                "hypercharges": {
                    "Y_Q_LH_quark_doublet": Y_Q,
                    "Y_u_uR_singlet":       Y_u,
                    "Y_d_dR_singlet":       Y_d,
                    "Y_L_LH_lepton_doublet": Y_L,
                    "Y_e_eR_singlet":       Y_e,
                },
                "anomaly_traces": anomaly_results,
                "L_inf_residual": anomaly_max_resid,
                "all_anomalies_cancel": anomaly_cancels,
            },
            "derivation_note": (
                "Two checks: (1) for RH singlets I_3 = 0 forces Y_R = 2Q "
                "(trivial algebraic identity); (2) the four SM gauge-anomaly "
                "conditions on the full L/R-asymmetric one-generation "
                "hypercharge assignment all vanish to machine precision. "
                "The L/R-asymmetric assignment with three colors and the "
                "doublet multiplicity is the load-bearing structure; the "
                "anomaly cancellation is the standard textbook consistency "
                "of the SM particle content, here verified explicitly on "
                "GCT's identified hypercharges (App R §R.6)."
            ),
        },
    )
    print_summary(res); write_result(res)
    return res


if __name__ == "__main__":
    main()
