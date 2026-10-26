"""
verify_ch20_liv_and_rm.py - Ch20 Protocol H two-claim audit.

(a) Sec 20.2.2 LIV time delay (Tier 2):
    Delta_t = (L/c) * xi_2 * (E/E_Planck)^2
    L = 1e26 m, E = 100 GeV, E/E_Planck approximately 8e-18,
    and the registered benchmark Delta_t approximately 2e-17 s.

(b) Sec 20.2.3 RM angular power coefficient (Tier 3 geometric heuristic):
    C_6^RM / C_0^RM approximately phi^-18 approximately 1.73e-4

Audit checks both numerical claims against direct computation.
"""

import sys
import math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import CODATA, MATH
from report import make_result, write_result, print_summary


def evaluate_liv_rm_consistency(
    ratio_computed,
    ratio_stated,
    delta_t_at_xi2_unity,
    delta_t_stated,
    rm_computed,
    rm_stated,
):
    """Evaluate injected LIV/RM values and construct live discrepancy messages."""
    if ratio_computed <= 0 or ratio_stated <= 0 or rm_stated == 0:
        raise ValueError("LIV ratios must be positive and the stated RM value nonzero")
    ratio_error_orders = math.log10(ratio_stated / ratio_computed)
    rm_error_pct = abs(rm_computed - rm_stated) / abs(rm_stated) * 100.0
    liv_ok = abs(ratio_error_orders) < 0.5
    rm_ok = rm_error_pct < 5.0
    discrepancies = []
    if not liv_ok:
        implied_xi2 = delta_t_stated / delta_t_at_xi2_unity
        discrepancies.append(
            f"LIV mismatch: computed E/E_P={ratio_computed:.6e}, stated={ratio_stated:.6e} "
            f"({abs(ratio_error_orders):.3f} decades); computed Delta_t(xi_2=1)="
            f"{delta_t_at_xi2_unity:.6e} s versus stated {delta_t_stated:.6e} s, "
            f"which implies xi_2={implied_xi2:.6e}."
        )
    if not rm_ok:
        discrepancies.append(
            f"RM mismatch: computed C_6^RM/C_0^RM={rm_computed:.6e}, "
            f"stated={rm_stated:.6e}, residual={rm_error_pct:.3f}%."
        )
    return {
        "liv_ok": liv_ok,
        "rm_ok": rm_ok,
        "ratio_error_orders": ratio_error_orders,
        "rm_error_pct": rm_error_pct,
        "discrepancies": discrepancies,
    }


def _force_test_all_branch_combinations():
    """Force live-value messages for all four LIV/RM branch combinations."""
    cases = {
        (True, True): (8.0e-18, 8.0e-18, 1.73e-4, 1.73e-4),
        (False, True): (8.0e-19, 8.0e-18, 1.73e-4, 1.73e-4),
        (True, False): (8.0e-18, 8.0e-18, 8.65e-5, 1.73e-4),
        (False, False): (8.0e-19, 8.0e-18, 8.65e-5, 1.73e-4),
    }
    for expected, values in cases.items():
        result = evaluate_liv_rm_consistency(
            values[0], values[1], 2.5e-18, 2.0e-17, values[2], values[3]
        )
        assert (result["liv_ok"], result["rm_ok"]) == expected
        assert len(result["discrepancies"]) == 2 - sum(expected)
        for message in result["discrepancies"]:
            assert any(f"{value:.6e}" in message for value in values)


def main():
    _force_test_all_branch_combinations()
    phi = MATH.PHI
    c = CODATA.C_LIGHT
    G = CODATA.G_SI
    hbar = CODATA.HBAR

    # (a) LIV time delay
    E_Planck_J = math.sqrt(hbar * c ** 5 / G)
    E_Planck_GeV = E_Planck_J / (1e9 * CODATA.EV_TO_J)

    E_photon_GeV = 100.0
    ratio_E_over_EP = E_photon_GeV / E_Planck_GeV
    L_meters = 1e26
    L_over_c = L_meters / c

    stated_ratio = 8e-18
    Delta_t_xi2_unity = L_over_c * ratio_E_over_EP ** 2
    stated_Delta_t = 2e-17
    implied_xi2 = (
        stated_Delta_t / Delta_t_xi2_unity
        if Delta_t_xi2_unity > 0
        else float('inf')
    )

    # (b) RM angular power coefficient
    phi_neg_18 = phi ** (-18)
    stated_C6_RM_over_C0_RM = 1.73e-4
    evaluation = evaluate_liv_rm_consistency(
        ratio_E_over_EP,
        stated_ratio,
        Delta_t_xi2_unity,
        stated_Delta_t,
        phi_neg_18,
        stated_C6_RM_over_C0_RM,
    )
    ratio_error_orders = evaluation["ratio_error_orders"]
    err_RM_pct = evaluation["rm_error_pct"]
    liv_ratio_consistent = evaluation["liv_ok"]
    rm_value_consistent = evaluation["rm_ok"]

    pass_status = liv_ratio_consistent and rm_value_consistent

    discrepancies = evaluation["discrepancies"]

    res = make_result(
        name="ch20_liv_delay_and_rm_coefficient",
        app_psc_label="Ch20 Protocol H - LIV Delta_t + RM C_6/C_0 audit",
        formula="(a) Delta_t = (L/c)*xi_2*(E/E_P)^2; (b) C_6^RM/C_0^RM = phi^-18",
        predicted=phi_neg_18,
        observed=stated_C6_RM_over_C0_RM,
        reference_class="MANUSCRIPT_STATED",
        unit="dimensionless ratio C_6^RM / C_0^RM",
        app_psc_predicted=stated_C6_RM_over_C0_RM,
        app_psc_precision_str=(
            f"(a) LIV: stated E/E_Planck={stated_ratio:.0e} for E=100 GeV; actual ratio {ratio_E_over_EP:.2e} "
            f"({abs(ratio_error_orders):.1f} decades off). "
            f"(b) RM: manuscript reference = {stated_C6_RM_over_C0_RM:.3e}; "
            f"computed phi^-18 = {phi_neg_18:.3e}; residual = {err_RM_pct:.3f}%."
        ),
        app_psc_precision_ppm=None,
        tier="(a) Tier 2 LIV time delay; (b) Tier 3 RM coefficient (Geometric Heuristic)",
        status="INTERNAL_ARITHMETIC_PASS" if pass_status else "TENSION",
        tolerance_ppm=None,
        discrepancy_notes=discrepancies,
        extra={
            "phi": phi,
            "phi_neg_18": phi_neg_18,
            "E_Planck_GeV_standard": E_Planck_GeV,
            "E_photon_GeV": E_photon_GeV,
            "ratio_E_over_EP_computed": ratio_E_over_EP,
            "ratio_E_over_EP_stated_in_manuscript": stated_ratio,
            "ratio_error_orders": ratio_error_orders,
            "L_meters": L_meters,
            "L_over_c_seconds": L_over_c,
            "Delta_t_at_xi2_unity": Delta_t_xi2_unity,
            "Delta_t_stated_in_manuscript": stated_Delta_t,
            "implied_xi2_from_stated_Delta_t": implied_xi2,
            "C6_RM_C0_RM_stated_in_manuscript": stated_C6_RM_over_C0_RM,
            "C6_RM_C0_RM_phi_neg_18": phi_neg_18,
            "RM_error_pct_from_phi_neg_18_only": err_RM_pct,
        },
    )
    print_summary(res)
    write_result(res)
    return res


if __name__ == "__main__":
    main()
