"""
verify_E_amplitudes.py — E_∥ / E_⊥ projection amplitudes (Tier 1 algebraic).

App ZN §ZN.2.1 (Tier 1 substrate ingredient):
 |E_∥|² = (1 + φ²) / 5 ≈ 0.7236
 |E_⊥|² = (1 + φ⁻²) / 5 ≈ 0.2764
 |E_⊥|²/|E_∥|² = φ⁻² (exact, Tier 1)

These are the standard cut-and-project amplitudes for the H₃/H₄ icosahedral
projection from R⁶ to E_∥ ⊕ E_⊥. They underpin the Weinberg bare prediction
sin²θ_W = φ⁻³ (via volume cube of length ratio) and the App ZN gauge-sector
coupling weights Z_1, Z_2.

Tier 1 algebraic identity: the formulas (1+φ²)/5 and (1+φ⁻²)/5 are exact
algebraic constructs from the φ minimal polynomial φ² = φ + 1; their ratio
reduces to φ⁻² via this identity. Verifier confirms both stated values and
the ratio identity to machine precision.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import MATH
from report import make_result, write_result, print_summary


def main():
 phi = MATH.PHI

 # The two amplitudes
 E_para_sq = (1.0 + phi ** 2) / 5.0
 E_perp_sq = (1.0 + phi ** (-2)) / 5.0
 ratio = E_perp_sq / E_para_sq

 # Stated manuscript values + expected ratio
 E_para_sq_stated = 0.7236
 E_perp_sq_stated = 0.2764
 ratio_expected = phi ** (-2)

 err_para_pct = abs(E_para_sq - E_para_sq_stated) / E_para_sq_stated * 100.0
 err_perp_pct = abs(E_perp_sq - E_perp_sq_stated) / E_perp_sq_stated * 100.0
 err_ratio_pct = abs(ratio - ratio_expected) / abs(ratio_expected) * 100.0

 matches_para = err_para_pct < 0.1
 matches_perp = err_perp_pct < 0.1
 matches_ratio = err_ratio_pct < 1e-10 # algebraic identity → machine precision

 # Sum check: |E_∥|² + |E_⊥|² should = (2 + φ² + φ⁻²)/5
 # φ² + φ⁻² = φ + 1 + (φ-1)² using φ⁻¹ = φ-1; compute directly.
 sum_sq = E_para_sq + E_perp_sq
 sum_expected_check = (2.0 + phi ** 2 + phi ** (-2)) / 5.0
 sum_OK = abs(sum_sq - sum_expected_check) < 1e-12

 pass_status = matches_para and matches_perp and matches_ratio and sum_OK

 res = make_result(
 name="E_perp_E_para_amplitudes",
 app_r_label="E_∥ / E_⊥ projection amplitudes (Tier 1 — cut-and-project algebra)",
 formula="|E_∥|² = (1+φ²)/5; |E_⊥|² = (1+φ⁻²)/5; |E_⊥|²/|E_∥|² = φ⁻²",
 predicted=ratio,
 observed=ratio_expected,
 unit="(dimensionless)",
 app_r_predicted=ratio_expected,
 app_r_precision_str=(
 f"|E_∥|² = {E_para_sq:.6f} (vs stated {E_para_sq_stated}, {err_para_pct:+.4f}%); "
 f"|E_⊥|² = {E_perp_sq:.6f} (vs stated {E_perp_sq_stated}, {err_perp_pct:+.4f}%); "
 f"ratio = {ratio:.10f} (vs expected φ⁻² = {ratio_expected:.10f}, "
 f"{err_ratio_pct:.2e}%)"
 ),
 app_r_precision_ppm=err_ratio_pct * 1e4,
 tier="Tier 1 (algebraic identity from φ minimal polynomial)",
 status="PASS" if pass_status else "FAIL",
 tolerance_ppm=1.0,
 extra={
 "phi": phi,
 "E_para_sq_computed": E_para_sq,
 "E_para_sq_stated": E_para_sq_stated,
 "E_perp_sq_computed": E_perp_sq,
 "E_perp_sq_stated": E_perp_sq_stated,
 "ratio_computed": ratio,
 "ratio_expected_phi_minus_2": ratio_expected,
 "sum_amplitudes": sum_sq,
 "err_para_pct": err_para_pct,
 "err_perp_pct": err_perp_pct,
 "err_ratio_pct": err_ratio_pct,
 "derivation_note": (
 "Standard H_4/H_3 cut-and-project amplitudes from the icosahedral "
 "projection R^6 → E_∥ ⊕ E_⊥. The ratio E_⊥²/E_∥² = φ⁻² is the "
 "algebraic source of: (a) sin²θ_W^bare = φ⁻³ via volume cube "
 "(V3 Ch04 §4.3.1, Theorem U.9), (b) the App ZN gauge-sector "
 "coupling weights Z_1 = 41/6 / (120·|E_⊥|²) and Z_2 = 19/6 / "
 "(18·|E_∥|²). Tier 1: pure algebraic identity from φ² = φ + 1."
 ),
 },
 )
 print_summary(res); write_result(res)
 return res


if __name__ == "__main__":
 main()
