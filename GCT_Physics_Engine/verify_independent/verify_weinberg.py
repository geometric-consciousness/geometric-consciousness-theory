"""
verify_weinberg.py — Independent recomputation of the raw-frame Weinberg ratios

App PSC §PSC.2 rows 3–5:
 Raw Galois-frame ratio: rho_raw = φ^-2 ≈ 0.38197 [Tier 1 exact; coordinate-dependent]
 Normalized share: rho_raw/(1+rho_raw) ≈ 0.27639 [Tier 1 exact]
 Raw-frame volume ratio: V_perp,0/V_parallel,0 = φ^-3 ≈ 0.23607 [Tier 1 coordinate identity]
 Physical bare angle = Tier 3 hypothesis H-EW; observed Z-pole value = Tier 3 comparison target
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import CODATA, MATH, pct_error, ppm_error
from report import make_result, write_result, print_summary, status_from_registered_band, status_from_open_problem


def main():
 phi = MATH.PHI

 rho_gut = phi ** -2
 # Raw-frame ratio from the AKN column norms |E_perp|^2/|E_par|^2 = (1+phi^-2)/(1+phi^2)
 rho_from_norms = (1.0 + phi ** -2) / (1.0 + phi ** 2)
 rho_identity_holds = abs(rho_from_norms - rho_gut) < 1e-12
 cartan_share = rho_gut / (1.0 + rho_gut)
 s2w_bare = phi ** -3
 observed = CODATA.SIN2_THETA_W_Z

 pct_bare = pct_error(s2w_bare, observed)
 ppm_bare = ppm_error(s2w_bare, observed)
 registered_band_ppm = 50000.0

 # Raw Galois-frame ratio: exact arithmetic for the declared frames but
 # coordinate-dependent (not a physical boundary); the normalized share is
 # tracked separately.
 result_gut = make_result(
 name="weinberg_gut",
 app_psc_label="rho_raw raw Galois-frame ratio (coordinate identity)",
 formula="rho_raw = φ^-2; rho_raw/(1+rho_raw) = 0.27639320225",
 predicted=rho_gut,
 observed=None,
 reference_class="PURE_MATHEMATICAL",
 unit="(dimensionless)",
 app_psc_predicted=0.38197,
 app_psc_precision_str="Tier 1 exact raw-frame arithmetic (coordinate-dependent); normalized share = 0.27639320225",
 app_psc_precision_ppm=None,
 tier="Tier 1",
 status="TIER1_EXACT" if rho_identity_holds else "FAIL",
 tolerance_ppm=None,
 extra={"normalized_cartan_share": cartan_share},
 )
 print_summary(result_gut)
 write_result(result_gut)

 result_bare = make_result(
 name="weinberg_bare",
 app_psc_label="sin²θ_W (bare, low-energy comparison)",
 formula="sin²θ_W = φ^-3",
 predicted=s2w_bare,
 observed=observed,
 reference_class="EMPIRICAL_ANCHOR",
 unit="(dimensionless)",
 app_psc_predicted=0.23607,
 app_psc_precision_str="2.1% (cross-scale numerical alignment, not RGE support)",
 app_psc_precision_ppm=21000.0,
 tier="Tier 3 gauge-kinetic hypothesis H-EW; raw-frame volume identity is Tier 1 coordinate arithmetic; Tier 3 observed Z-pole comparison (2.1% cross-scale alignment) + Tier 4 as evidence that phi explains the value (constant control test v3 NEGATIVE-FRAGILE; App PSC §PSC.9.6)",
 # P.14 is registered as open research: H-EW is an undecided
 # Tier 3 hypothesis, so the in-band alignment is not reported as a PASS.
 status=status_from_open_problem(
 True, open_status="OPEN_RESEARCH",
 closed_status=status_from_registered_band(ppm_bare, registered_band_ppm),
 ),
 tolerance_ppm=registered_band_ppm,
 extra={"percent_error": pct_bare, "band_status_if_closed": status_from_registered_band(ppm_bare, registered_band_ppm)},
 )
 print_summary(result_bare)
 write_result(result_bare)
 return [result_gut, result_bare]


if __name__ == "__main__":
 main()
