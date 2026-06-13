"""
verify_jarlskog.py — Independent verification reference for the GCT
Jarlskog invariant (CKM J) prediction status.

V3 Ch09 §9.4.3 (CP Violation Phase) currently holds the Jarlskog
invariant under OPEN RESEARCH (Open Problem O.7, App H §H.5). A
candidate φ⁻²² ansatz is catalogued under O.7:
 - Literal formula evaluation: φ⁻²² = 2.525 × 10⁻⁵
 - PDG 2024 reference: |J_CKM| ≈ 3.12 × 10⁻⁵
 - The literal formula sits about 4.6σ from PDG with a 19% gap.

The Jarlskog invariant is not a load-bearing Tier 2 prediction in the
current framework; the eEDM derivation in Ch09 §9.6.3 is explicitly
decoupled from any specific J ansatz via the bounded Tier 2 envelope
|d_e^GCT| ≲ 1.1 × 10⁻²⁹ e·cm (J-independent unitarity bound).

This verifier:
 1. Computes the literal formula φ⁻²² as a candidate ansatz reference.
 2. Records the manuscript's prior literal value (for traceability).
 3. Compares both to PDG 2024 |J|.
 4. Records the residual gap as a property of the candidate ansatz.
 5. Registers J under OPEN RESEARCH disposition (Open Problem O.7).

The Jarlskog invariant is held as Open Problem O.7 (App H §H.5): the
GCT framework does not currently supply a closed Tier 2 prediction for
|J_CKM|. The φ⁻²² ansatz is one of multiple candidate forms catalogued
under O.7 and is not load-bearing on any other observable in this
verifier suite (the eEDM scope-restriction in Ch09 §9.6.3 explicitly
decouples from the J magnitude). Independent closure routes under O.7:
 (a) a φ-power ansatz with a corrected exponent or O(1) icosahedral
     prefactor that evaluates to the PDG value within tolerance;
 (b) a non-φ-power derivation tied to the harmonic-ladder structure
     of the CKM mixing sector (Ch10 §10.6);
 (c) closure of the underlying icosahedral chirality phase via the
     Connes-Moscovici local index on the AKN spectral triple.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import CODATA, MATH
from report import make_result, write_result, print_summary

# PDG 2024 reference value
J_CKM_PDG = 3.12e-5
J_CKM_PDG_UNC = 0.13e-5
# Manuscript-stated value (V3 Ch09 §9.4.3)
J_GCT_MANUSCRIPT_STATED = 3.19e-5


def main():
 phi = MATH.PHI
 # Literal evaluation of the formula stated in V3 Ch09 §9.4.3
 j_gct_literal = phi ** (-22)

 # Comparisons
 gap_literal_vs_pdg = (j_gct_literal - J_CKM_PDG) / J_CKM_PDG
 gap_literal_sigmas = abs(j_gct_literal - J_CKM_PDG) / J_CKM_PDG_UNC
 gap_stated_vs_pdg = (J_GCT_MANUSCRIPT_STATED - J_CKM_PDG) / J_CKM_PDG
 gap_stated_sigmas = abs(J_GCT_MANUSCRIPT_STATED - J_CKM_PDG) / J_CKM_PDG_UNC

 # Percent difference between the manuscript-stated value and the literal formula value
 manuscript_vs_formula_pct = 100.0 * (J_GCT_MANUSCRIPT_STATED - j_gct_literal) / j_gct_literal

 res = make_result(
 name="ckm_jarlskog",
 app_r_label="CKM Jarlskog invariant |J|",
 formula="|J_GCT| = φ⁻²² (V3 Ch09 §9.4.3, '22-step volumetric displacement')",
 predicted=j_gct_literal,
 observed=J_CKM_PDG,
 unit="(dimensionless)",
 app_r_predicted=j_gct_literal,
 app_r_precision_str=(
 f"literal φ⁻²² = {j_gct_literal*1e5:.3f}×10⁻⁵ → "
 f"{gap_literal_vs_pdg*100:+.1f}% vs PDG ({gap_literal_sigmas:.1f}σ); "
 f"manuscript-stated value {J_GCT_MANUSCRIPT_STATED*1e5:.2f}×10⁻⁵ would give "
 f"{gap_stated_vs_pdg*100:+.1f}% ({gap_stated_sigmas:.1f}σ); it differs from the literal formula value by {manuscript_vs_formula_pct:.1f}%"
 ),
 app_r_precision_ppm=None,
 tier="OPEN RESEARCH (O.7) — awaiting first-principles closure",
 status="OPEN_RESEARCH",
 tolerance_ppm=None,
 extra={
 "j_gct_literal_phi_minus_22": j_gct_literal,
 "j_gct_manuscript_stated": J_GCT_MANUSCRIPT_STATED,
 "manuscript_value_vs_literal_formula_pct": manuscript_vs_formula_pct,
 "j_pdg_2024": J_CKM_PDG,
 "j_pdg_uncertainty": J_CKM_PDG_UNC,
 "literal_gap_vs_pdg_pct": gap_literal_vs_pdg * 100.0,
 "literal_gap_sigmas": gap_literal_sigmas,
 "stated_gap_vs_pdg_pct": gap_stated_vs_pdg * 100.0,
 "stated_gap_sigmas": gap_stated_sigmas,
 "candidate_ansatz_status": (
 "The literal φ⁻²² candidate ansatz catalogued under O.7 evaluates "
 "to 2.525×10⁻⁵, 19% (4.6σ) below the PDG value 3.12×10⁻⁵. A "
 "Wolfenstein-form alternative A²λ⁶η ≈ 3.24×10⁻⁵ sits closer to "
 "PDG (+5%) but is not a φ-power form. The Jarlskog invariant is "
 "held under OPEN RESEARCH (O.7) with no current Tier 2 GCT "
 "prediction; the eEDM derivation in Ch09 §9.6.3 is explicitly "
 "decoupled via the J-independent Tier 2 bounded form."
 ),
 },
 )
 print_summary(res); write_result(res)
 return res


if __name__ == "__main__":
 main()
