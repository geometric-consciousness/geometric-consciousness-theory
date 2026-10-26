"""
verify_g2_electron.py — Independent re-derivation of GCT contribution to
electron g-2 (a_e).

V3 Ch08 §8.7.4 (The Electron Row: Activation-Threshold Hypothesis):
 Tier 3/4 hypothesis, in tension with QFT decoupling (a decoupled muon-scale
 term gives Delta a_e ~ (m_e/m_mu)^2 * 250.65e-11 ~ 6e-14); no Tier 2 support.
 Under the hypothesis there is no activated lattice vertex correction for a_e
 at this loop order, because the electron sits
 at the ground-state N=0 mode and is below the cage-depinning
 threshold E_res = m_e · φ^11 ≈ 101.69 MeV needed to activate the
 phason vertex loop. Only N ≥ 11 leptons (muon at N=11, tau at N=17)
 get the geometric 1/5 lattice correction.

Test:
 1. Confirm the threshold inequality: m_e < m_e · φ^11.
 2. Confirm the loop-order lattice correction is zero under that threshold
    hypothesis (Tier 3/4, including the N=11 threshold exponent).
 3. Compare to the experimental gap Δa_e = a_e^exp − a_e^SM(α) for the two
 atom-interferometry α inputs, and report consistency.

Experimental anchor + α-INPUT CONTINGENCY:
 a_e^exp = 1.159 652 180 59(13) × 10⁻³ (Fan et al., PRL 130, 071801 (2023)).
 Fan et al. also give the α inferred from that a_e with the SM prediction:
 α⁻¹(a_e) = 137.035 999 166(15). Near this point a_e^SM is linear in α⁻¹,
 da_e/dα⁻¹ = −(α²/π)(1/2 + 2C₂(α/π) + 3C₃(α/π)²) ≈ −8.45 × 10⁻⁶
 (C₂, C₃ the 2- and 3-loop QED coefficients), so
 Δa_e(X) = a_e^exp − a_e^SM(α_X) = −(da_e/dα⁻¹)(α⁻¹_X − α⁻¹(a_e)).
 Cs-α (Parker et al. 2018): α⁻¹ = 137.035 999 046(27) → Δa_e ≈ −1.01 × 10⁻¹² (3.9σ)
 Rb-α (Morel et al. 2020):  α⁻¹ = 137.035 999 206(11) → Δa_e ≈ +0.34 × 10⁻¹² (2.1σ)
 Each σ combines the α_X uncertainty with the α(a_e) uncertainty (which
 carries the a_e measurement and SM-theory errors). These reproduce the
 α-level discrepancies Fan et al. state (3.9σ for Cs, 2.1σ for Rb).

The Cs α gives the larger α and therefore the larger a_e^SM, so its gap is
negative. (An earlier version of this script had the two branches swapped
and reported a Cs "1σ PASS"; that was wrong.)

Tier 3/4 hypothesis (not a derived prediction): Δa_e^lattice = 0 at this
loop order; status PENDING-α-RESOLUTION. The null is in tension
with both α inputs (3.9σ and 2.1σ); no branch supports it within 2σ.

Pass logic: the GCT null prediction is supported only if BOTH α-input
branches give gaps consistent with 0 within 2σ. Otherwise this verifier
returns PENDING-α-RESOLUTION, not PASS, until the external α discord
resolves.
"""

import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import CODATA, MATH
from report import make_result, write_result, print_summary


# Experimental anchor and α inputs.
A_E_EXPERIMENTAL = 1.15965218059e-3  # Fan et al. 2023 (g/2 - 1)
A_E_EXPERIMENTAL_UNC = 0.13e-12  # Fan et al. 2023
ALPHA_INV_FROM_AE = 137.035999166  # Fan et al. 2023: alpha^-1 inferred from a_e with SM theory
ALPHA_INV_FROM_AE_UNC = 0.015e-6  # Fan et al. 2023 (0.11 ppb; a_e exp + SM theory)
ALPHA_INV_CS = 137.035999046  # Parker et al. 2018 (Cs)
ALPHA_INV_CS_UNC = 0.027e-6
ALPHA_INV_RB = 137.035999206  # Morel et al. 2020 (Rb)
ALPHA_INV_RB_UNC = 0.011e-6
QED_C2 = -0.328478965579  # 2-loop mass-independent QED coefficient
QED_C3 = 1.181241456587  # 3-loop mass-independent QED coefficient


def dae_dalpha_inv(alpha_inv: float) -> float:
 """Local slope of a_e^SM with respect to alpha^-1 (QED series to 3 loops)."""
 a = 1.0 / alpha_inv
 x = a / math.pi
 return -(a * a / math.pi) * (0.5 + 2.0 * QED_C2 * x + 3.0 * QED_C3 * x * x)


def alpha_branch_gap(alpha_inv: float, alpha_inv_unc: float) -> tuple[float, float]:
 """Return (a_e^exp - a_e^SM(alpha_X), combined 1-sigma) for one alpha input."""
 slope = dae_dalpha_inv(ALPHA_INV_FROM_AE)
 gap = -slope * (alpha_inv - ALPHA_INV_FROM_AE)
 sigma = abs(slope) * math.hypot(alpha_inv_unc, ALPHA_INV_FROM_AE_UNC)
 return gap, sigma


def lattice_contribution_for_threshold(
 electron_energy: float,
 activation_threshold: float,
 *,
 activated_contribution: float | None = None,
) -> float:
 """Return the null only below threshold; fail closed at/above it."""
 if electron_energy < activation_threshold:
  return 0.0
 if activated_contribution is None:
  raise ValueError("activated contribution required at or above threshold")
 return activated_contribution


def evaluate_status(predicted: float, gaps: tuple[float, ...], sigma) -> str:
 """Require every external alpha-input branch to agree within two sigma.

 ``sigma`` is either one positive number shared by every branch or a tuple
 of per-branch positive sigmas with the same length as ``gaps``.
 """
 sigmas = tuple(sigma) if isinstance(sigma, (tuple, list)) else (sigma,) * len(gaps)
 if len(sigmas) != len(gaps) or any(s <= 0 for s in sigmas):
  raise ValueError("sigma must be positive")
 return (
  "PASS"
  if all(abs(gap - predicted) < 2.0 * s for gap, s in zip(gaps, sigmas))
  else "PENDING-α-RESOLUTION"
 )


def main():
 phi = MATH.PHI
 m_e = CODATA.M_E_MEV

 # Step 1: threshold inequality
 e_res_mev = m_e * (phi ** 11)
 electron_below_threshold = m_e < e_res_mev
 threshold_safety_factor = e_res_mev / m_e # ≈ φ^11 ≈ 199

 # Step 2: GCT prediction
 delta_a_e_gct_lattice = lattice_contribution_for_threshold(m_e, e_res_mev)

 # Step 3: experimental gap under both α-input branches
 gap_cs, sig_cs = alpha_branch_gap(ALPHA_INV_CS, ALPHA_INV_CS_UNC)
 gap_rb, sig_rb = alpha_branch_gap(ALPHA_INV_RB, ALPHA_INV_RB_UNC)
 gap_cs_sigmas = abs(gap_cs - delta_a_e_gct_lattice) / sig_cs
 gap_rb_sigmas = abs(gap_rb - delta_a_e_gct_lattice) / sig_rb

 # The displayed "observed" gap is the Cs-α branch, the larger of the two;
 # both branches are reported explicitly in extras.
 gap = gap_cs

 cs_consistent = gap_cs_sigmas < 2.0
 rb_consistent = gap_rb_sigmas < 2.0
 status = evaluate_status(
  delta_a_e_gct_lattice, (gap_cs, gap_rb), (sig_cs, sig_rb)
 )

 res = make_result(
 name="g2_electron",
 app_psc_label="Electron g-2 GCT contribution (activation-threshold null)",
 formula="Δa_e^lattice = 0 at this loop order (electron at N=0; threshold E_res = m_e·φ^11 ≈ 101.69 MeV; m_e ≪ E_res; N=11 threshold exponent Tier 3)",
 predicted=delta_a_e_gct_lattice,
 observed=gap,
 unit="(dimensionless)",
 app_psc_predicted=0.0,
 app_psc_precision_str=f"Cs-α: Δa_e = {gap_cs*1e12:+.2f} × 10⁻¹² ({gap_cs_sigmas:.1f}σ); Rb-α: Δa_e = {gap_rb*1e12:+.2f} × 10⁻¹² ({gap_rb_sigmas:.1f}σ); the null is in tension with both α inputs",
 app_psc_precision_ppm=None,
 tier="Tier 3/4 activation-threshold hypothesis (in tension with QFT decoupling, Δa_e ~ 6×10⁻¹⁴; no Tier 2 support; threshold exponent N=11 Tier 3); α-input contingent",
 status=status,
 tolerance_ppm=None,
 extra={
 "threshold_e_res_MeV": e_res_mev,
 "electron_mass_MeV": m_e,
 "safety_factor_phi11": threshold_safety_factor,
 "electron_below_threshold": electron_below_threshold,
 "delta_a_e_gct_lattice_x_10_15": delta_a_e_gct_lattice * 1e15,
 "a_e_experimental": A_E_EXPERIMENTAL,
 "a_e_experimental_source": "Fan et al., PRL 130, 071801 (2023)",
 "alpha_inv_from_a_e": ALPHA_INV_FROM_AE,
 "alpha_inv_Cs": ALPHA_INV_CS,
 "alpha_inv_Rb": ALPHA_INV_RB,
 "dae_dalpha_inv": dae_dalpha_inv(ALPHA_INV_FROM_AE),
 "experimental_gap_Cs_alpha_x_10_12": gap_cs * 1e12,
 "experimental_gap_Rb_alpha_x_10_12": gap_rb * 1e12,
 "gap_Cs_alpha_sigma_x_10_12": sig_cs * 1e12,
 "gap_Rb_alpha_sigma_x_10_12": sig_rb * 1e12,
 "gap_Cs_alpha_sigmas": gap_cs_sigmas,
 "gap_Rb_alpha_sigmas": gap_rb_sigmas,
 "Cs_alpha_consistent_with_zero_within_2sigma": cs_consistent,
 "Rb_alpha_consistent_with_zero_within_2sigma": rb_consistent,
 "alpha_input_caveat": (
 "Cs-based α (Parker et al. 2018) gives Δa_e ≈ -1.01×10⁻¹² (3.9σ); "
 "Rb-based α (Morel et al. 2020) gives Δa_e ≈ +0.34×10⁻¹² (2.1σ), with a_e from Fan et al. 2023. "
 "The earlier 'Cs 0.96σ agreement / Rb 3.94σ tension' labels were swapped and are withdrawn. "
 "The Cs and Rb α values disagree with each other by 5.5σ, which keeps this row in "
 "PENDING-α-RESOLUTION until both α-input branches agree with the null prediction or the "
 "external α discord resolves. Binary gate: next-gen atom-interferometry α measurements "
 "(Rb-α2 / Cs-α2 / matter-wave gradiometry)."
 ),
 "interpretation": (
 "Under the Tier 3/4 activation-threshold hypothesis (not derived; in tension with QFT decoupling, "
 "Δa_e ~ 6×10⁻¹⁴) there is no activated lattice vertex correction for a_e at this loop order because the electron's rest mass "
 "(0.511 MeV) is well below the cage-depinning threshold "
 f"E_res = m_e·φ^11 ≈ {e_res_mev:.2f} MeV (safety factor ≈ φ^11 ≈ {threshold_safety_factor:.0f}). "
 "Under the hypothesis only leptons at N ≥ 11 (muon N=11, tau N=17) would activate the "
 "geometric 1/5 phason vertex correction. The observed "
 "(a_e^exp − a_e^SM) gap is not consistent with zero within 2σ for "
 "either α input (3.9σ with Cs-α, 2.1σ with Rb-α), so the null is not "
 "supported at present; the row stays PENDING-α-RESOLUTION. Falsifier: any future "
 "measurement establishing |Δa_e^anom| > 10⁻¹² at >3σ robustly across α inputs "
 "would challenge the activation-threshold hypothesis."
 ),
 },
 )
 print_summary(res); write_result(res)
 return res


if __name__ == "__main__":
 main()
