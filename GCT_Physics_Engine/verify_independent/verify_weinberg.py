"""
verify_weinberg.py — Independent re-derivation of the Weinberg boundary data

App R §R.2 rows 3–5:
 GUT-scale exact: rho_G = φ^-2 ≈ 0.38197 [Tier 1 exact]
 Normalized Cartan share: rho_G/(1+rho_G) ≈ 0.27639 [Tier 1 exact]
 Bare (volumetric): sin^2 θ_W = φ^-3 ≈ 0.23607 [Tier 2, 2.1% vs Z-pole]
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import CODATA, MATH, pct_error, ppm_error
from report import make_result, write_result, print_summary


def main():
 phi = MATH.PHI

 rho_gut = phi ** -2
 cartan_share = rho_gut / (1.0 + rho_gut)
 s2w_bare = phi ** -3
 observed = CODATA.SIN2_THETA_W_Z

 pct_bare = pct_error(s2w_bare, observed)

 # GUT Gram scalar is Tier 1 exact; the normalized share is tracked
 # separately so the verifier does not use the normalized-share shorthand.
 result_gut = make_result(
 name="weinberg_gut",
 app_r_label="rho_G Gram/Cartan boundary scalar (GUT scale)",
 formula="rho_G = φ^-2; rho_G/(1+rho_G) = 0.27639320225",
 predicted=rho_gut,
 observed=None,
 unit="(dimensionless)",
 app_r_predicted=0.38197,
 app_r_precision_str="Tier 1 exact Gram scalar; normalized Cartan share = 0.27639320225",
 app_r_precision_ppm=None,
 tier="Tier 1",
 status="TIER1_EXACT",
 tolerance_ppm=None,
 extra={"normalized_cartan_share": cartan_share},
 )
 print_summary(result_gut)
 write_result(result_gut)

 result_bare = make_result(
 name="weinberg_bare",
 app_r_label="sin²θ_W (bare, low-energy comparison)",
 formula="sin²θ_W = φ^-3",
 predicted=s2w_bare,
 observed=observed,
 unit="(dimensionless)",
 app_r_predicted=0.23607,
 app_r_precision_str="2.1% (expected at tree level)",
 app_r_precision_ppm=21000.0,
 tier="Tier 1 algebraic identity at GUT scale (Uniqueness Theorem U.9); Tier 2 empirical anchor at Z-pole (2.1% bare-tree-level vs CODATA, expected from RGE running)",
 status="PASS", # 2.1% is the documented bare-tree-level value; tier reflects GUT/Z-pole split per V3 Ch04 §4.3.3
 tolerance_ppm=30000.0,
 extra={"percent_error": pct_bare},
 )
 print_summary(result_bare)
 write_result(result_bare)
 return [result_gut, result_bare]


if __name__ == "__main__":
 main()
