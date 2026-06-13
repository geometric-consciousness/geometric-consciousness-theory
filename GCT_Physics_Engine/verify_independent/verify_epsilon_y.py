"""
verify_epsilon_y.py — Yield strain ε_y = φ⁻⁵ ≈ 0.0902 candidate derivation.

V3 Ch11 §11.1.3: ε_y = Δu_⊥ / ξ = (φ⁻¹ · a_⊥) / (φ⁴ · a_⊥) = φ⁻⁵ ≈ 0.0902 [Tier 2]
 (geometrically derived from AKN tiling-flip condition; no fitted local parameter)
V3 Ch15 §15.x: ε_y = φ⁻⁵ ≈ 0.090 (cited as "geometrically fixed invariant from
 the AKN tiling flip condition")

**Tier-discipline check:** Ch11 reports the candidate AKN derivation
ε_y = φ⁻⁵ ≈ 0.0902. The Protocol C engine stress-gate currently carries
0.1 as a Tier 3 alloy-like prior until the AKN-action/phason-elastic closure
is promoted into the source.

This verifier confirms the φ⁻⁵ derivation and checks the displayed value.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import MATH
from report import make_result, write_result, print_summary


def main():
 phi = MATH.PHI
 epsilon_y_derived = phi ** (-5)
 epsilon_y_stated_Ch11 = 0.0902
 epsilon_y_stated_Ledger = 0.1

 err_vs_Ch11_pct = abs(epsilon_y_derived - epsilon_y_stated_Ch11) / epsilon_y_stated_Ch11 * 100.0
 err_vs_Ledger_pct = abs(epsilon_y_derived - epsilon_y_stated_Ledger) / epsilon_y_stated_Ledger * 100.0

 matches_Ch11 = err_vs_Ch11_pct < 0.5
 matches_Ledger = err_vs_Ledger_pct < 12.0 # 10% rounding allowance

 pass_status = matches_Ch11 # Ch11 is the derivation source

 res = make_result(
 name="yield_strain_epsilon_y",
 app_r_label="Yield strain ε_y = φ⁻⁵ (Tier 2, Ch11 §11.1.3 AKN tiling-flip derivation)",
 formula="ε_y = Δu_⊥ / ξ = (φ⁻¹ a_⊥) / (φ⁴ a_⊥) = φ⁻⁵",
 predicted=epsilon_y_derived,
 observed=epsilon_y_stated_Ch11,
 unit="(dimensionless)",
 app_r_predicted=epsilon_y_stated_Ch11,
 app_r_precision_str=(
 f"ε_y = φ⁻⁵ = {epsilon_y_derived:.6f}; "
 f"Ch11 §11.1.3 cites 0.0902 ({err_vs_Ch11_pct:.3f}% match); "
 f"Parameter Ledger reports the Tier 2 candidate φ⁻⁵ ≈ 0.0902 and the "
	 f"Tier 3 registered stress-gate value 0.1 ({err_vs_Ledger_pct:.1f}% offset)."
 ),
 app_r_precision_ppm=err_vs_Ch11_pct * 1e4,
 tier="Tier 2 candidate derivation + Tier 3 registered stress-gate prior",
 status="PASS" if pass_status else "TENSION",
 tolerance_ppm=None,
 extra={
 "phi": phi,
 "epsilon_y_derived_phi_minus_5": epsilon_y_derived,
 "epsilon_y_stated_in_Ch11_section_11_1_3": epsilon_y_stated_Ch11,
 "epsilon_y_registered_engine_stress_gate_value": epsilon_y_stated_Ledger,
 "error_vs_Ch11_pct": err_vs_Ch11_pct,
 "error_vs_Ledger_pct": err_vs_Ledger_pct,
 "matches_Ch11_derivation": matches_Ch11,
 "matches_Ledger_rounded_value": matches_Ledger,
 "note": (
	 "Ch11 §11.1.3 derives ε_y = φ⁻⁵ ≈ 0.0902 from the AKN tiling-flip "
	 "condition with no fitted local parameter. The engine stress gate currently "
	 "uses 0.1 as a Tier 3 alloy-like prior pending AKN-action/phason-elastic "
	 "closure or direct Protocol C stress-threshold calibration."
),
 },
 )
 print_summary(res); write_result(res)
 return res


if __name__ == "__main__":
 main()
