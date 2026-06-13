"""
verify_pta_l6_anisotropy.py - PTA l=6 icosahedral anisotropy.

V3 Ch21 Sec 21.1.3 (boxed Tier 2 prediction):
    Gamma_GCT(theta) = Gamma_HD(theta) + epsilon * P_6(cos theta)
    epsilon = phi^-18 ~ 1.74e-4

Three observationally distinct quantities follow from this single anisotropy:

    (1) Peak angular-correlation deviation (Legendre-polynomial bound):
        Delta_Gamma_max = epsilon * max|P_6(cos theta)| = phi^-18 ~ 1.73e-4
        since max|P_6| = 1 over [-1, 1].

    (2) Linear Legendre projection coefficient (linear-in-epsilon):
        C_hat_6^GCT = (4*pi / 13) * epsilon = (4*pi / 13) * phi^-18 ~ 1.67e-4

    (3) Squared angular-power-spectrum ratio (quadratic-in-epsilon):
        C_6 / C_0 = (4*pi / 13) * epsilon^2 = (4*pi / 13) * phi^-36 ~ 2.92e-8

All three are derived from the same epsilon = phi^-18 stiffness ratio at
machine precision; they are different *observables*, not different physics.
"""

import sys
import math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
from scipy.special import legendre

from constants import MATH
from report import make_result, write_result, print_summary


def _verify_peak_deviation(epsilon: float, max_abs_P6: float) -> dict:
    """Peak angular-correlation deviation: Delta_Gamma_max = epsilon * 1."""
    predicted = epsilon * max_abs_P6
    boxed = epsilon
    err_pct = abs(predicted - boxed) / boxed * 100.0
    return make_result(
        name="pta_l6_peak_deviation",
        app_r_label="PTA l=6 peak angular-correlation deviation (Ch21 Sec 21.1.3, Tier 2)",
        formula="Delta_Gamma_max = phi^-18 * max|P_6(cos theta)| = phi^-18",
        predicted=predicted,
        observed=boxed,
        unit="(dimensionless angular correlation deviation)",
        app_r_predicted=boxed,
        app_r_precision_str=(
            f"Algebraic-identity check: epsilon * max|P_6| = {epsilon:.4e} * "
            f"{max_abs_P6:.4f} = {predicted:.4e} reproduces the manuscript boxed "
            f"value {boxed:.4e} ({err_pct:.2e}% residual). Single-formula "
            f"identity, not a two-route convergence."
        ),
        app_r_precision_ppm=err_pct * 1e4,
        tier="Tier 2 (phason-graviton linear coupling; algebraic identity once stiffness ratio is fixed)",
        status="PASS" if err_pct < 0.1 else "TENSION",
        tolerance_ppm=None,
        extra={
            "phi": MATH.PHI,
            "epsilon_phi_minus_18": epsilon,
            "max_abs_P_6_over_full_range": max_abs_P6,
        },
    )


def _verify_linear_legendre(epsilon: float) -> dict:
    """Linear Legendre projection coefficient: C_hat_6 = (4 pi / 13) * epsilon."""
    norm = 4.0 * math.pi / 13.0
    predicted = norm * epsilon
    boxed = 1.67e-4
    err_pct = abs(predicted - boxed) / boxed * 100.0
    return make_result(
        name="pta_l6_linear_legendre",
        app_r_label="PTA l=6 linear Legendre projection C_hat_6 (Ch21 Sec 21.3.2, Tier 2)",
        formula="C_hat_6 = (4 pi / 13) * phi^-18",
        predicted=predicted,
        observed=boxed,
        unit="(dimensionless Legendre coefficient)",
        app_r_predicted=boxed,
        app_r_precision_str=(
            f"(4 pi / 13) * phi^-18 = {norm:.6f} * {epsilon:.4e} = {predicted:.4e}; "
            f"manuscript value {boxed:.4e}; agreement {err_pct:.2f}%."
        ),
        app_r_precision_ppm=err_pct * 1e4,
        tier="Tier 2 (linear-in-epsilon Legendre projection)",
        status="PASS" if err_pct < 1.0 else "TENSION",
        tolerance_ppm=None,
        extra={
            "phi": MATH.PHI,
            "epsilon_phi_minus_18": epsilon,
            "legendre_normalization_4pi_over_13": norm,
        },
    )


def _verify_squared_power_ratio(epsilon: float) -> dict:
    """Squared angular-power-spectrum ratio: C_6/C_0 = (4 pi / 13) * epsilon^2."""
    norm = 4.0 * math.pi / 13.0
    predicted = norm * (epsilon ** 2)
    boxed = 2.92e-8
    err_pct = abs(predicted - boxed) / boxed * 100.0
    return make_result(
        name="pta_l6_squared_power_ratio",
        app_r_label="PTA l=6 squared angular-power-spectrum ratio C_6/C_0 (Ch21 Sec 21.1.2, Tier 2)",
        formula="C_6 / C_0 = (4 pi / 13) * phi^-36",
        predicted=predicted,
        observed=boxed,
        unit="(dimensionless C_l ratio)",
        app_r_predicted=boxed,
        app_r_precision_str=(
            f"(4 pi / 13) * phi^-36 = {norm:.6f} * {epsilon**2:.4e} = {predicted:.4e}; "
            f"manuscript value {boxed:.4e}; agreement {err_pct:.2f}%."
        ),
        app_r_precision_ppm=err_pct * 1e4,
        tier="Tier 2 (quadratic-in-epsilon angular-power-spectrum form)",
        status="PASS" if err_pct < 1.0 else "TENSION",
        tolerance_ppm=None,
        extra={
            "phi": MATH.PHI,
            "epsilon_phi_minus_18": epsilon,
            "epsilon_squared_phi_minus_36": epsilon ** 2,
            "legendre_normalization_4pi_over_13": norm,
        },
    )


def main():
    phi = MATH.PHI
    epsilon = phi ** (-18)

    P_6 = legendre(6)
    xs = np.linspace(-1.0, 1.0, 10000)
    max_abs_P6 = float(max(abs(P_6(xs))))

    results = [
        _verify_peak_deviation(epsilon, max_abs_P6),
        _verify_linear_legendre(epsilon),
        _verify_squared_power_ratio(epsilon),
    ]

    for r in results:
        print_summary(r)
        write_result(r)

    return results


if __name__ == "__main__":
    main()
