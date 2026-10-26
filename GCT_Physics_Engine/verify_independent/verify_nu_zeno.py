"""
verify_nu_zeno.py — Zeno Drive frequency reference for the ν_c ≈ 112 ± 10 MHz
protected-subspace branch.

V3 Ch13 §13.1.2b:
 Mechanism: magnon-polaron avoided crossing controlled by the radical-pair
 singlet-triplet gap Δ_ST. Solving v_ph k = Δ_ST/ℏ + Jk² gives an
 avoided-crossing frequency ν_vH ≈ Δ_ST/(2π·ℏ) = Δ_ST/h.

 Tier 3 SPECIFIC VALUE: ν_c = 112 ± 10 MHz registered primary peak. The
 operative bare scale is the TrpH•+ effective hyperfine coupling ≈ 0.97 mT
 ≈ 27 MHz, which is larger than the FAD•− value ≈ 0.70 mT ≈ 20 MHz (Wong,
 Benjamin & Hore 2023, PCCP 25:975). Reaching 112 ± 10 MHz from it requires a
 residual frequency-scale factor of ≈4× (3.7–4.5×); the earlier 10–20 MHz
 indole band and 6–11× factor are withdrawn (compare the ~41× calibrated, not derived, ratio between
 g_single^bare = 931 kHz and the calibrated constant g_single^eff = 38.3 MHz per App GPE). Exact
 derivation of the renormalization factor is Open Problem O.12 (App ORQ §ORQ.5).

 The 30 MHz figure is the 3-term rms of the FAD•⁻ semiquinone values
 A_N5 ≈ 42, A_N10 ≈ 28, A_H5 ≈ 12 MHz (≈ 29.96 MHz); it is a placeholder,
 not the operative scale. (The 6-term rms that also includes three 7 MHz
 proton terms is ≈ 21.75 MHz and is emitted separately for reference.)

This verifier records the TrpH•+ operative renormalization burden and
the FAD reference scale. It is OPEN_CONDITIONAL on O.12/O.23 rather than a
PASS-quality physical validation.
"""

import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from report import make_result, write_result, print_summary, status_from_open_problem


def main():
 # Magnon-polaron avoided crossing: ν_vH ≈ Δ_ST / h. Operative bare scale:
 # TrpH•+ effective hyperfine 0.97 mT ≈ 27.2 MHz (> FAD•− 0.70 mT ≈ 19.6 MHz;
 # Wong, Benjamin & Hore 2023). Residual factor to 112 ± 10 MHz ≈ 3.7–4.5×
 # (Open Problem O.12). The 30 MHz value is the 3-term FAD rms placeholder only.
 A_ref_N5_MHz = 42.0 # FAD-like order-of-magnitude N5 reference (not operative)
 A_ref_N10_MHz = 28.0 # FAD-like order-of-magnitude N10 reference (not operative)
 A_ref_H5_MHz = 12.0 # FAD-like order-of-magnitude H5 reference (not operative)
 A_ref_other_MHz = 7.0 # representative proton hyperfine reference

 A_hf_rms_FAD_MHz = math.sqrt(
 (A_ref_N5_MHz ** 2 + A_ref_N10_MHz ** 2 + A_ref_H5_MHz ** 2
 + 3.0 * A_ref_other_MHz ** 2) / 6.0
 )
 # FAD reference gap (NOT operative) and the naive factor it would imply:
 Delta_ST_over_h_FAD_MHz = 30.0
 nu_Zeno_target_MHz = 112.0
 factor_naive_FAD = nu_Zeno_target_MHz / Delta_ST_over_h_FAD_MHz  # ~3.73x (reference)

 # Operative TrpH•+ scale and the residual factor to the registered window:
 MHZ_PER_MT = 28.025  # electron gyromagnetic ratio, MHz per mT
 trp_aeff_MHz = 0.97 * MHZ_PER_MT  # ≈ 27.2 MHz
 fad_aeff_MHz = 0.70 * MHZ_PER_MT  # ≈ 19.6 MHz
 factor_trp_lo = (nu_Zeno_target_MHz - 10.0) / trp_aeff_MHz  # ≈ 3.75x
 factor_trp_hi = (nu_Zeno_target_MHz + 10.0) / trp_aeff_MHz  # ≈ 4.49x

 res = make_result(
 name="nu_zeno_van_Hove",
 app_psc_label="Zeno Drive frequency ν_Zeno (magnon-polaron avoided crossing)",
 formula="ν_vH ≈ Δ_ST/h with operative TrpH•+ effective hyperfine ≈ 27 MHz (Ch13 §13.1.2b); 112 MHz is a registered Tier 3 branch value",
 predicted=trp_aeff_MHz * 1e6,
 observed=nu_Zeno_target_MHz * 1e6,
 unit="Hz",
 app_psc_predicted=nu_Zeno_target_MHz * 1e6,
 app_psc_precision_str=(
 f"Mechanism reference: magnon-polaron avoided crossing ν ≈ Δ_ST/h. "
 f"Operative TrpH•+ effective hyperfine ≈ {trp_aeff_MHz:.1f} MHz "
 f"(> FAD•− ≈ {fad_aeff_MHz:.1f} MHz). The registered Tier 3 branch value "
 f"ν_c = 112 ± 10 MHz (not an observation) requires a residual factor of "
 f"≈{factor_trp_lo:.1f}–{factor_trp_hi:.1f}× (Open Problems O.12/O.23). "
 f"The 30 MHz value is the 3-term FAD rms placeholder only."
 ),
 app_psc_precision_ppm=None,
 tier="Tier 1 two-branch model mathematics / Tier 3 realization and value (phason coupling; protected-branch value pending O.12/O.23)",
 status=status_from_open_problem(
  True, open_status="OPEN_CONDITIONAL", closed_status="TENSION"
 ),
 tolerance_ppm=None,
 extra={
 "operative_trp_aeff_MHz": trp_aeff_MHz,
 "fad_aeff_MHz": fad_aeff_MHz,
 "operative_enhancement_factor_lo": factor_trp_lo,
 "operative_enhancement_factor_hi": factor_trp_hi,
 "hyperfine_source": "Wong, Benjamin & Hore 2023, PCCP 25:975-982 (TrpH•+ 0.97 mT, FAD•− 0.70 mT)",
 "withdrawn": "the earlier 10-20 MHz indole band and 6-11x factor",
 "reference_A_N5_MHz": A_ref_N5_MHz,
 "reference_A_N10_MHz": A_ref_N10_MHz,
 "reference_A_H5_MHz": A_ref_H5_MHz,
 "reference_A_other_MHz": A_ref_other_MHz,
 "reference_hyperfine_RMS_6term_incl_protons_MHz": A_hf_rms_FAD_MHz,
 "reference_Delta_ST_over_h_FAD_MHz": Delta_ST_over_h_FAD_MHz,
 "reference_naive_FAD_enhancement_factor": factor_naive_FAD,
 "nu_Zeno_target_MHz": nu_Zeno_target_MHz,
 "phonon_polariton_enhancement_factor_for_coupling_App_GPE": 41.0,
 "derivation_note": (
 "Magnon-polaron avoided crossing: solving v_ph k = Δ_ST/ℏ + Jk² "
 "in the small-J regime gives k_c ≈ Δ_ST/(ℏ v_ph), and the "
 "avoided-crossing frequency on the lower branch is ν ≈ Δ_ST/h. "
 "The operative TrpH•+ effective hyperfine is ≈ 27 MHz "
 "(0.97 mT; larger than FAD•− ≈ 20 MHz), so the registered 112 ± 10 MHz "
 "branch value requires a residual factor of ≈ 3.7–4.5× (Open Problems "
 "O.12/O.23; compare the ~41× calibrated (not derived) ratio between "
 "g_single^bare = 931 kHz and the calibrated constant g_single^eff = 38.3 MHz per "
 "App GPE). The 30 MHz figure is the 3-term FAD rms placeholder only."
 ),
 },
 )
 print_summary(res); write_result(res)
 return res


if __name__ == "__main__":
 main()
