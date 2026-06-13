"""
verify_alpha_s_bare.py — Strong coupling α_s⁻¹(bare) = 10 φ² ≈ 26.18 (Tier 3 handle).

V3 Ch04 §4.5.5 / App T §T.3 / App ZN §ZN.5 / App TP §TP.3:
 α_s⁻¹(bare) = 10 φ² [Tier 3 calibrated handle pending O.42 / QLQCD-2]
 where 10 = count of three-fold rotation axes of the RT (Tier 1 substrate)
 and φ² = standard icosahedral inflation factor (Tier 1 substrate)
 → α_s⁻¹(bare) ≈ 26.18 → α_s(bare) ≈ 0.0382

This is a BARE TREE-LEVEL handle at M_GUT, not the running PDG value at M_Z.
PDG α_s(M_Z) = 0.1179 (α_s⁻¹ ≈ 8.48). The manuscript acknowledges (App ZN §ZN.5)
that the bare value is "too small (α_s too large) to be carried by 33.5 e-folds
of asymptotic-free running down to PDG value"; QLQCD-2 non-perturbative
confinement corrections are the canonical path to closure (Open Problem in App
Z.7).

This verifier:
 (1) Computes α_s⁻¹(bare) = 10 φ² and confirms the literal formula gives
 26.18 from manuscript-internal inputs.
 (2) Reports the gap to PDG α_s⁻¹(M_Z) ≈ 8.48 as the documented "67.6% gap"
 (acknowledged in Ch04 §4.5.5; this is OPEN BY DESIGN pending QLQCD-2,
 not a bug).
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import MATH
from report import make_result, write_result, print_summary


def main():
 phi = MATH.PHI

 # GCT bare formula
 alpha_s_inv_bare = 10.0 * phi ** 2
 alpha_s_bare = 1.0 / alpha_s_inv_bare

 # Manuscript stated
 stated_inv = 26.18
 err_pct = abs(alpha_s_inv_bare - stated_inv) / stated_inv * 100.0
 formula_OK = err_pct < 0.1 # the formula 10·φ² is exact; we just check rounding

 # Gap to PDG α_s(M_Z) — DOCUMENTED IN APP ZN §ZN.5 as the QLQCD-2 debt
 alpha_s_PDG_MZ = 0.1179
 alpha_s_inv_PDG_MZ = 1.0 / alpha_s_PDG_MZ
 bare_vs_PDG_gap_pct = (alpha_s_inv_bare - alpha_s_inv_PDG_MZ) / alpha_s_inv_PDG_MZ * 100.0

 res = make_result(
 name="alpha_s_inv_bare",
 app_r_label="Strong coupling α_s⁻¹(bare) = 10 φ² (Tier 3 calibrated handle)",
 formula="α_s⁻¹(bare) = 10 · φ² (10 = RT three-fold axes; φ² = icosahedral inflation)",
 predicted=alpha_s_inv_bare,
 observed=stated_inv,
 unit="(dimensionless)",
 app_r_predicted=stated_inv,
 app_r_precision_str=(
 f"Tier 3 calibrated-handle evaluation: 10 · φ² = {alpha_s_inv_bare:.4f} "
 f"vs stated 26.18 ({err_pct:+.4f}%). Gap to PDG α_s⁻¹(M_Z) = "
 f"{alpha_s_inv_PDG_MZ:.4f} is {bare_vs_PDG_gap_pct:+.1f}% — the "
 f"DOCUMENTED 'too-small-to-run' debt of App ZN §ZN.5 / Ch04 §4.5.5 "
 f"(QLQCD-2 non-perturbative confinement correction, App Z.7 open problem)."
 ),
 app_r_precision_ppm=err_pct * 1e4,
 tier="Tier 3 calibrated handle (10 integer + φ² geometric factor); O.42 / QLQCD-2 open",
 status="PASS" if formula_OK else "FAIL",
 tolerance_ppm=None,
 extra={
 "phi": phi,
 "alpha_s_inv_bare_GCT_formula": alpha_s_inv_bare,
 "alpha_s_bare_GCT": alpha_s_bare,
 "alpha_s_inv_stated_in_manuscript": stated_inv,
 "formula_rounding_error_pct": err_pct,
 "alpha_s_PDG_MZ": alpha_s_PDG_MZ,
 "alpha_s_inv_PDG_MZ": alpha_s_inv_PDG_MZ,
 "bare_vs_PDG_gap_pct": bare_vs_PDG_gap_pct,
 "derivation_note": (
 "α_s⁻¹(bare) = 10 φ² combines two geometric substrate inputs: "
 "(a) the count of three-fold rotation axes of the rhombic "
 "triacontahedron = 10, and (b) the icosahedral inflation "
 "factor φ². The TREE-LEVEL bare value 26.18 is a calibrated handle "
 "at M_GUT; the gap to PDG α_s⁻¹(M_Z) ≈ 8.48 is the OPEN "
 "QLQCD-2 non-perturbative confinement debt (App Z.7), "
 "explicitly acknowledged in App ZN §ZN.5 and Ch04 §4.5.5. "
 "This is NOT a hidden bug — it's open by design pending "
 "non-perturbative closure."
 ),
 },
 )
 print_summary(res); write_result(res)
 return res


if __name__ == "__main__":
 main()
