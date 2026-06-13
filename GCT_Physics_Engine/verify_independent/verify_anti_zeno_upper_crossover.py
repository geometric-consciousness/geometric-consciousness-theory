"""
verify_anti_zeno_upper_crossover.py - Bare Anti-Zeno crossover audit.

App X Sec X.12 / Ch13 Sec 13.4.6 use the Misra-Sudarshan crossover

    nu* = T2 / tau_Z^2.

For the bare Trp radical-pair Hamiltonian, T2 = 10 us and
tau_Z ~= 1/(30 MHz), giving nu* ~= 9 GHz. Thus the registered
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
    tau_Z_s = 1.0 / 30.0e6
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
        app_r_label="Bare Misra-Sudarshan anti-Zeno crossover nu* ~ 9 GHz (App X Sec X.12 / Ch13 Sec 13.4.6)",
        formula="nu* = T2 / tau_Z^2 with T2=10 us and tau_Z=1/(30 MHz)",
        predicted=nu_star_MHz,
        observed=nu_drive_MHz,
        unit="MHz",
        app_r_predicted=nu_star_MHz,
        app_r_precision_str=(
            f"Bare Misra-Sudarshan crossover nu*={nu_star_MHz:.1f} MHz; "
            f"nu_c / nu*={sampling_ratio:.4f}. The registered A-Prime window is inverse-Zeno; "
            f"positive nu_c T2 enhancement is O.23 protected-subspace-conditional."
        ),
        app_r_precision_ppm=None,
        tier="Tier 2 qualitative sign test; Tier 3 protected-subspace operating value",
        status="PASS" if pass_status else "TENSION",
        tolerance_ppm=None,
        discrepancy_notes=discrepancies,
        extra={
            "T2_s": T2_s,
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
