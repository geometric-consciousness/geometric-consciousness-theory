"""
verify_nu_zeno.py — Zeno Drive frequency reference for the ν_c ≈ 112 ± 10 MHz
protected-subspace branch.

V3 Ch13 §13.1.2b:
 Mechanism: magnon-polaron avoided crossing controlled by the radical-pair
 singlet-triplet gap Δ_ST. Solving v_ph k = Δ_ST/ℏ + Jk² gives an
 avoided-crossing frequency ν_vH ≈ Δ_ST/(2π·ℏ) = Δ_ST/h.

 Tier 3 SPECIFIC VALUE: ν_c = 112 ± 10 MHz registered primary peak. The
 operative bare singlet-triplet scale is set by the β-tubulin tryptophan
 indole hyperfine band (one indole nitrogen N1 plus weaker ring-proton
 couplings), A_hf,rms^indole ≈ 10–20 MHz. Reaching 112 MHz from this band
 requires a chiral phonon-polariton frequency-scale renormalization of
 ~6–11× (analogous to the ~41× coupling renormalization that lifts
 g_single^bare = 931 kHz to g_single^eff = 38.3 MHz per App Q). Exact
 derivation of the renormalization factor is Open Problem O.12 (App H §H.5).

 The FAD•⁻ semiquinone hyperfine values (A_N5 ≈ 42, A_N10 ≈ 28, A_H5 ≈ 12 MHz;
 Δ_ST/h ≈ 30 MHz) are carried only as a literature order-of-magnitude
 reference band, NOT as the operative tryptophan scale; naive substitution
 of the 30 MHz FAD gap would understate the burden as ~3.7×.

This verifier records the indole-band operative renormalization burden and
the FAD reference scale. It is OPEN_CONDITIONAL on O.12/O.23 rather than a
PASS-quality physical validation.
"""

import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from report import make_result, write_result, print_summary


def main():
 # Magnon-polaron avoided crossing: ν_vH ≈ Δ_ST / h. The operative bare
 # singlet-triplet scale is the β-tubulin tryptophan indole hyperfine band:
 # one indole nitrogen N1 (A_N1 ≈ 14–17 MHz) plus weaker ring-proton
 # couplings, giving A_hf,rms^indole ≈ 10–20 MHz. The FAD•⁻ N5/N10/H5 values
 # are an order-of-magnitude reference only (Δ_ST/h ≈ 30 MHz); β-tubulin
 # tryptophan has a different (lower) hyperfine band, so the operative
 # renormalization burden is ~6–11×, NOT the ~3.7× that naive substitution
 # of the FAD gap would give — Open Problem O.12.
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

 # Operative tryptophan indole singlet-triplet band and the renormalization
 # burden it implies to reach the registered ν_c = 112 ± 10 MHz peak:
 indole_band_lo_MHz = 10.0
 indole_band_hi_MHz = 20.0
 factor_indole_hi = nu_Zeno_target_MHz / indole_band_lo_MHz  # ~11.2x
 factor_indole_lo = nu_Zeno_target_MHz / indole_band_hi_MHz  # ~5.6x

 res = make_result(
 name="nu_zeno_van_Hove",
 app_r_label="Zeno Drive frequency ν_Zeno (magnon-polaron avoided crossing)",
 formula="ν_vH ≈ Δ_ST/h with operative tryptophan indole band Δ_ST/h ≈ 10–20 MHz (Ch13 §13.1.2b)",
 predicted=indole_band_hi_MHz * 1e6,
 observed=nu_Zeno_target_MHz * 1e6,
 unit="Hz",
 app_r_predicted=nu_Zeno_target_MHz * 1e6,
 app_r_precision_str=(
 f"Mechanism reference: magnon-polaron avoided crossing ν ≈ Δ_ST/h. "
 f"Operative β-tubulin tryptophan indole band Δ_ST/h ≈ "
 f"{indole_band_lo_MHz:.0f}–{indole_band_hi_MHz:.0f} MHz. Registered "
 f"ν_c = 112 ± 10 MHz requires a chiral phonon-polariton enhancement "
 f"factor of ~{factor_indole_lo:.0f}–{factor_indole_hi:.0f}× "
 f"(Open Problems O.12/O.23). The FAD reference gap (30 MHz) would "
 f"naively imply only ~{factor_naive_FAD:.2f}× and is not operative."
 ),
 app_r_precision_ppm=None,
 tier="Tier 2 mechanism reference + Tier 3 protected-branch value pending O.12/O.23",
 status="OPEN_CONDITIONAL",
 tolerance_ppm=None,
 extra={
 "operative_indole_band_lo_MHz": indole_band_lo_MHz,
 "operative_indole_band_hi_MHz": indole_band_hi_MHz,
 "operative_enhancement_factor_lo": factor_indole_lo,
 "operative_enhancement_factor_hi": factor_indole_hi,
 "reference_A_N5_MHz": A_ref_N5_MHz,
 "reference_A_N10_MHz": A_ref_N10_MHz,
 "reference_A_H5_MHz": A_ref_H5_MHz,
 "reference_A_other_MHz": A_ref_other_MHz,
 "reference_hyperfine_RMS_FAD_MHz": A_hf_rms_FAD_MHz,
 "reference_Delta_ST_over_h_FAD_MHz": Delta_ST_over_h_FAD_MHz,
 "reference_naive_FAD_enhancement_factor": factor_naive_FAD,
 "nu_Zeno_target_MHz": nu_Zeno_target_MHz,
 "phonon_polariton_enhancement_factor_for_coupling_App_Q": 41.0,
 "derivation_note": (
 "Magnon-polaron avoided crossing: solving v_ph k = Δ_ST/ℏ + Jk² "
 "in the small-J regime gives k_c ≈ Δ_ST/(ℏ v_ph), and the "
 "avoided-crossing frequency on the lower branch is ν ≈ Δ_ST/h. "
 "The operative β-tubulin tryptophan indole hyperfine band is "
 "Δ_ST/h ≈ 10–20 MHz (one indole N1 ≈ 14–17 MHz plus weaker ring "
 "protons), so the registered 112 ± 10 MHz peak requires a chiral "
 "phonon-polariton renormalization of ~6–11× (Open Problems "
 "O.12/O.23; analogous to the ~41× coupling renormalization that "
 "lifts g_single^bare = 931 kHz to g_single^eff = 38.3 MHz per "
 "App Q). The FAD•⁻ semiquinone values (Δ_ST/h ≈ 30 MHz) are a "
 "literature order-of-magnitude reference only; naive substitution "
 "would understate the burden as ~3.7×."
 ),
 },
 )
 print_summary(res); write_result(res)
 return res


if __name__ == "__main__":
 main()
