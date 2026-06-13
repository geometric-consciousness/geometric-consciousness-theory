"""
verify_muon_mass.py — Independent re-derivation of m_mu

App R §R.1 row 2:
 Formula: m_mu = m_e · φ^11 · (1 + 5α_A3 + φ^8 α_A3^2)
 App R: 105.656 MeV; Tier 2 bare ~0.25%; Tier 2+3+A3 ~21 ppm
 Engine: protocol_lepton_spectrum.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import CODATA, MATH, ppm_error
from report import make_result, write_result, print_summary

# ---------- GCT formula parameters (from manuscript §R.1, Ch08 §8.4) ------
N_MU = 11 # Lucas/symmetry-octave exponent (2·S_oct − 1)
N_PHASON = 5 # phason drag channels
PHI_POWER_2 = 8 # φ^8 α^2 second-order term (Tier 2 derivation)

def main():
 phi = MATH.PHI
 # A3 disclosure: the canonical precision-comparison row uses measured
 # low-energy alpha. The bare GCT alpha tree is audited separately.
 alpha = CODATA.ALPHA
 m_e = CODATA.M_E_MEV

 # First-order stage: Tier 2 channel count + Tier 3 +5α normalization
 m_mu_first = m_e * (phi ** N_MU) * (1.0 + N_PHASON * alpha)
 # Second-order (Tier 2 + 3): + φ^8 α^2
 m_mu_second = m_e * (phi ** N_MU) * (
 1.0 + N_PHASON * alpha + (phi ** PHI_POWER_2) * alpha**2
 )

 observed = CODATA.M_MU_MEV
 ppm_first = ppm_error(m_mu_first, observed)
 ppm_second = ppm_error(m_mu_second, observed)

 result = make_result(
 name="muon_mass",
 app_r_label="Muon mass (m_mu)",
 formula="m_mu = m_e · φ^11 · (1 + 5α_A3 + φ^8 α_A3^2)",
 predicted=m_mu_second,
 observed=observed,
 unit="MeV",
 app_r_predicted=105.656,
 app_r_precision_str="~0.25% (Tier 2 bare) | ~21 ppm (Tier 2+3+A3 corrected)",
 app_r_precision_ppm=21.0,
    tier="Tier 2 bare φ^11 harmonic mechanism + Tier 3 specific exponent + A3 measured alpha input + Tier 2 phason-channel multiplicity / Tier 3 +5α pole-mass normalization + Tier 3 φ^8α² heat-kernel sub-coefficient + Tier 3 higher-loop SM-equivalence assumption (App R LEA)",
 status="PASS" if ppm_second < 50.0 else "FAIL",
 tolerance_ppm=50.0,
 extra={
 "phi": phi,
 "alpha_codata_A3": alpha,
 "alpha_anchor": "A3 measured low-energy alpha used by the corrected precision-comparison row; bare alpha_GCT = 1/(360*phi^-2) is audited separately.",
 "N_mu": N_MU,
 "phi_power_2": PHI_POWER_2,
 "m_mu_first_order_MeV": m_mu_first,
 "m_mu_second_order_MeV": m_mu_second,
 "first_order_ppm": ppm_first,
 "second_order_ppm": ppm_second,
 },
 )
 print_summary(result)
 write_result(result)
 return result


if __name__ == "__main__":
 main()
