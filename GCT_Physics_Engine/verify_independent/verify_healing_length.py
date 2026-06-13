"""
verify_healing_length.py — Polaron healing length ξ = ℏc/(α² m_e c²).

**Scope.** Independent evaluation of the algebraic formula from CODATA
primitives (ℏ, c, α, m_e). No imports from `protocol_healing_length.py`
or from the engine-side cage adjacency code; this verifier re-derives ξ
directly from constants and compares to the canonical single value
ξ ≈ 7.25 nm published in Parameter Ledger §2 (V1 Ch7, V3 Ch13, App K §K.5)
as a Tier 1 textbook Bohr-Compton result. The GCT-internal phason-elastic
Route 2 derivation arriving at the same expression is registered as App H
Open Problem O.25 and closes NEGATIVELY (the substitution chain
K_⊥ = φ^-18 K_∥, a_6 = 2 ℓ_P, m_e = M_P φ^-107 (1-5α) yields
ξ^Route2 = (1/2) φ^9 √α ℓ_P ~ 5e-35 m, off the Tier 1 target by ~10^26;
the missing 1/α^2 Coulomb enhancement is not derivable from the GCT chain).
The "two-route convergence" framing is not used here in App K §K.5; this
verifier evaluates only the Tier 1 Bohr-Compton formula, with α as the
input variable.

Steps:
 (1) Compute ξ_CODATA = ℏc/(α_CODATA² m_e c²) from CODATA-2022 primitives.
 (2) Compute ξ_GCT = ℏc/(α_GCT² m_e c²) using GCT bare α = 1/(360 φ⁻²).
 (3) Confirm both branches agree within ~1% (the formula is α-input-
 insensitive at the percent level — both values evaluate the SAME
 formula, not two independent derivations).
 (4) Compare the result to the canonical single value 7.25 nm.

The IDENTIFICATION of ξ with the microtubule lumen (Tier 3 biological
correlation; polaron diameter 2ξ = 14.5 nm vs lumen ID ~15 nm, 3% match
per Ch07 §7.3.3) is OUT OF SCOPE for this verifier; only the algebraic
formula is checked.
"""

import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import CODATA, MATH
from report import make_result, write_result, print_summary


def main():
 phi = MATH.PHI
 hbar = CODATA.HBAR
 c = CODATA.C_LIGHT
 m_e_MeV = CODATA.M_E_MEV
 m_e_kg = CODATA.M_E_KG
 alpha_CODATA = CODATA.ALPHA
 alpha_GCT = 1.0 / (360.0 * phi ** (-2)) # GCT bare formula

 # m_e c² in joules
 m_e_c2_J = m_e_kg * c ** 2

 # ξ = ℏc / (α² m_e c²)
 xi_CODATA_m = hbar * c / (alpha_CODATA ** 2 * m_e_c2_J)
 xi_GCT_m = hbar * c / (alpha_GCT ** 2 * m_e_c2_J)
 xi_CODATA_nm = xi_CODATA_m * 1e9
 xi_GCT_nm = xi_GCT_m * 1e9

 # Canonical single value (Parameter Ledger row 23, App K §K.5)
 xi_stated_nm = 7.25 # nm — both α branches converge here to ~0.7%

 err_CODATA_pct = 100.0 * (xi_CODATA_nm - xi_stated_nm) / xi_stated_nm
 err_GCT_pct = 100.0 * (xi_GCT_nm - xi_stated_nm) / xi_stated_nm

 # The two α branches should agree to <1% (the formula is α-input-insensitive
 # at the percent level because CODATA α and GCT bare α differ by only ~0.35%
 # and the difference enters ξ as a square).
 inter_branch_pct = 100.0 * abs(xi_GCT_nm - xi_CODATA_nm) / xi_CODATA_nm

 consistent_CODATA = abs(err_CODATA_pct) < 1.0
 consistent_GCT = abs(err_GCT_pct) < 2.0
 branches_agree = inter_branch_pct < 2.0
 pass_status = consistent_CODATA and consistent_GCT and branches_agree

 res = make_result(
 name="polaron_healing_length",
 app_r_label="Polaron healing length ξ = ℏc/(α² m_e c²)",
 formula="ξ = ℏc/(α² m_e c²) = a_0/α (single value; no manuscript-derivable O(1) prefactor)",
 predicted=xi_CODATA_nm,
 observed=xi_stated_nm,
 unit="nm",
 app_r_predicted=7.25,
 app_r_precision_str=(
 f"ξ(CODATA α) = {xi_CODATA_nm:.3f} nm ({err_CODATA_pct:+.2f}% vs stated 7.25 nm); "
 f"ξ(GCT bare α) = {xi_GCT_nm:.3f} nm ({err_GCT_pct:+.2f}%); "
 f"inter-branch agreement {inter_branch_pct:.2f}%"
 ),
 app_r_precision_ppm=None,
 tier="Tier 1 textbook (Bohr-Compton ξ = a_0/α); GCT-internal Route 2 closed negatively under O.25; lumen identification = Tier 3",
 status="PASS" if pass_status else "TENSION",
 tolerance_ppm=None,
 extra={
 "alpha_CODATA": alpha_CODATA,
 "alpha_GCT_bare": alpha_GCT,
 "xi_CODATA_alpha_nm": xi_CODATA_nm,
 "xi_GCT_alpha_nm": xi_GCT_nm,
 "xi_stated_in_ledger_nm": xi_stated_nm,
 "error_CODATA_pct": err_CODATA_pct,
 "error_GCT_pct": err_GCT_pct,
 "inter_branch_agreement_pct": inter_branch_pct,
 "alpha_ratio_squared": (alpha_CODATA / alpha_GCT) ** 2,
 "polaron_diameter_nm": 2.0 * xi_CODATA_nm,
 "microtubule_lumen_ID_nm": 15.0,
 "diameter_vs_lumen_match_pct": 100.0 * abs(2.0 * xi_CODATA_nm - 15.0) / 15.0,
 "derivation_note": (
 "Standard Gross-Pitaevskii healing-length formula applied to "
 "the Compton-Bohr lengthscale: ξ = ℏc/(α²m_ec²) = a_0/α. The "
 "formula has no manuscript-derivable O(1) prefactor; both "
 "CODATA α and GCT bare α = φ²/360 inputs give the same ξ ≈ "
 "7.25 nm to within ~0.7% (the formula is α-input-insensitive "
 "at the percent level since the two α values differ by ~0.35% "
 "and the difference enters ξ as a square). Microtubule lumen "
 "identification: 2ξ = 14.5 nm vs lumen ID 15 nm = 3% match "
 "(Tier 3 biological correlation per Ch07 §7.3.3)."
 ),
 },
 )
 print_summary(res); write_result(res)
 return res


if __name__ == "__main__":
 main()
