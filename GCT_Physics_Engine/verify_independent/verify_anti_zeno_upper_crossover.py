"""
verify_anti_zeno_upper_crossover.py - Bare Anti-Zeno crossover audit.

App BEB Sec BEB.12 / Ch13 Sec 13.4.7 use the Misra-Sudarshan crossover

    nu* = T2 / tau_Z^2.

For the bare Trp radical-pair Hamiltonian, T2 = 10 us and the variance
sigma_H/h = 30 MHz gives tau_Z = hbar/sigma_H ~= 5.3 ns and
nu* ~= 3.6e11 Hz. Thus the registered
nu_c = 112 +/- 10 MHz A-Prime window is inverse-Zeno for the bare
channel; the qualitative Protocol A-Prime sign test is conditional
on O.23 lowering the effective Hamiltonian variance.
"""

import sys
import math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from report import make_result, write_result, print_summary


def main():
    T2_s = 10.0e-6
    sigma_H_over_h_Hz = 30.0e6
    tau_Z_s = 1.0 / (2.0 * math.pi * sigma_H_over_h_Hz)
    nu_drive_MHz = 112.0
    nu_star_MHz = (T2_s / (tau_Z_s ** 2)) / 1.0e6
    sampling_ratio = nu_drive_MHz / nu_star_MHz
    bare_inverse_zeno = sampling_ratio < 1.0
    pass_status = bare_inverse_zeno

    discrepancies = []
    if not bare_inverse_zeno:
        discrepancies.append(
            f"Bare drive should sit below the Misra-Sudarshan crossover; got "
            f"nu_c / nu* = {sampling_ratio:.4f}."
        )

    res = make_result(
        name="anti_zeno_upper_crossover",
        app_psc_label="Bare Misra-Sudarshan anti-Zeno crossover nu* ~ 3.6e11 Hz (App BEB Sec BEB.12 / Ch13 Sec 13.4.7)",
        formula="nu* = T2 / tau_Z^2 with T2=10 us and tau_Z=hbar/sigma_H, sigma_H/h=30 MHz",
        predicted=nu_star_MHz,
        observed=nu_drive_MHz,
        unit="MHz",
        app_psc_predicted=nu_star_MHz,
        app_psc_precision_str=(
            f"Bare Misra-Sudarshan crossover nu*={nu_star_MHz:.1f} MHz; "
            f"nu_c / nu*={sampling_ratio:.4f}. The registered A-Prime window is inverse-Zeno; "
            f"positive nu_c T2 enhancement is O.23 protected-subspace-conditional."
        ),
        app_psc_precision_ppm=None,
        tier="Tier 3 qualitative sign test conditional on the Tier 3 phason-coupled Zeno lock; Tier 3 protected-subspace operating value",
        status="OPEN_CONDITIONAL" if pass_status else "FAIL",
        tolerance_ppm=None,
        discrepancy_notes=discrepancies,
        extra={
            "T2_s": T2_s,
            "sigma_H_over_h_Hz": sigma_H_over_h_Hz,
            "tau_Z_s": tau_Z_s,
            "nu_drive_MHz": nu_drive_MHz,
            "nu_star_MHz": nu_star_MHz,
            "sampling_ratio": sampling_ratio,
            "bare_inverse_zeno": bare_inverse_zeno,
            "protected_subspace_required": True,
            "derivation_note": (
            "The registered observable is qualitative: the nu_c window should lengthen T2 "
            "relative to the low-frequency control only if O.23 supplies a protected "
                "subspace with reduced effective Hamiltonian variance."
            ),
        },
    )
    print_summary(res)
    write_result(res)
    return res


if __name__ == "__main__":
    main()
