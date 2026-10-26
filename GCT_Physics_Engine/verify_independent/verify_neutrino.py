"""
verify_neutrino.py — Independent re-derivation of neutrino floor + sum

App PSC §PSC.5:
 m_1 = m_e · φ^-36 → 0.0153 eV (KATRIN 2025 < 0.45 eV, 90% CL → respected; no m_1 observation)
 Σm_ν = sqrt(m_1² + Δm²_21) + sqrt(m_1² + Δm²_31) + m_1
 → 0.0853 eV vs DESI DR2 + CMB < 0.064 eV (95%, ΛCDM; arXiv:2503.14738): TENSION.
 The DR2 bound already lies below the registered 0.075 eV P.4 gate; the row is a
 tension rather than a gate crossing because the bound is ΛCDM-model-dependent.
 The retired Planck 2018 < 0.12 eV bound is kept only as historical context and
 no longer yields a PASS. Δm² inputs: NuFIT 6.0 (normal ordering, with SK).
"""

import sys
import math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from constants import CODATA, MATH, pct_error
from report import make_result, write_result, print_summary, status_from_upper_bound


def main():
 phi = MATH.PHI
 m_e_eV = CODATA.M_E_MEV * 1.0e6 # 5.110e5 eV

 # ---------- m_1 floor ----------
 m1_eV = m_e_eV * (phi ** -36)
 KATRIN_BOUND_eV = 0.45 # KATRIN 2025 (Science 388:180), 90% CL
 m1_below_bound = m1_eV < KATRIN_BOUND_eV
 # No m_1 observation exists and the m_e phi^-36 scale
 # is Tier 3 conditional (P3b/O.15(b)); a bound that the value respects is
 # OPEN_CONDITIONAL, not PASS (same rule as the Strong CP upper-limit row).
 status_m1 = status_from_upper_bound(m1_eV, KATRIN_BOUND_eV, derivation_open=True)
 res_m1 = make_result(
 name="neutrino_m1_floor",
 app_psc_label="Neutrino m_1 floor",
 formula="m_1 = m_e · φ^-36",
 predicted=m1_eV,
 observed=None, # KATRIN is an upper bound, not a measurement
 unit="eV",
 app_psc_predicted=0.0153,
 app_psc_precision_str=f"m_1 = {m1_eV:.4e} eV; KATRIN upper bound {KATRIN_BOUND_eV} eV → {'within bound' if m1_below_bound else 'OUTSIDE BOUND'}",
 app_psc_precision_ppm=None,
 tier="Tier 3 conditional (P3b/O.15(b) + anchors)",
 status=status_m1,
 tolerance_ppm=None,
 extra={
 "katrin_upper_bound_eV": KATRIN_BOUND_eV,
 "predicted_is_below_bound": m1_below_bound,
 },
 )
 print_summary(res_m1); write_result(res_m1)

 # ---------- Σm_ν (Normal Ordering) ----------
 m2_eV = math.sqrt(m1_eV ** 2 + CODATA.DELTA_M2_21)
 m3_eV = math.sqrt(m1_eV ** 2 + CODATA.DELTA_M2_31)
 sigma_m_eV = m1_eV + m2_eV + m3_eV

 planck_bound = CODATA.SIGMA_MNU_PLANCK_BOUND_EV # 0.12 (historical context only)
 desi_2024_bound = CODATA.SIGMA_MNU_DESI_2024_EV # 0.072 (superseded)
 desi_bound = CODATA.SIGMA_MNU_DESI_DR2_EV # 0.064 (registered comparator)
 p4_lower_gate = 0.075 # registered P.4 gate (definitive-precision Sigma m_nu < 0.075 eV)

 # Tension vs DESI DR2: Σm > bound
 desi_excess = sigma_m_eV - desi_bound

 res_sum = make_result(
 name="neutrino_sum",
 app_psc_label="Σ m_ν (NO)",
 formula="Σm_ν = m_1 + sqrt(m_1² + Δm²_21) + sqrt(m_1² + Δm²_31)",
 predicted=sigma_m_eV,
 observed=None, # bound, not measurement
 unit="eV",
 app_psc_predicted=0.0853,
 app_psc_precision_str=(
 "0.0853 eV > 0.064 eV (DESI DR2 + CMB, 95%, LambdaCDM): TENSION; "
 "the DR2 bound lies below the 0.075 eV P.4 gate but is model-dependent"
 ),
 app_psc_precision_ppm=None,
 tier="Tier 3 conditional (P3b/O.15(b) + anchors)",
 status="TENSION" if desi_excess > 0 else "OPEN_CONDITIONAL",
 tolerance_ppm=None,
 extra={
 "m1_eV": m1_eV, "m2_eV": m2_eV, "m3_eV": m3_eV,
 "desi_dr2_bound_eV": desi_bound,
 "desi_dr2_source": "DESI DR2 BAO + CMB, LambdaCDM, 95% (arXiv:2503.14738); < 0.16 eV under w0wa",
 "desi_dr2_status": "TENSION (Σ > 0.064)" if sigma_m_eV > desi_bound else "WITHIN_BOUND",
 "desi_excess_eV": desi_excess,
 "p4_lower_gate_eV": p4_lower_gate,
 "desi_dr2_bound_below_p4_gate": desi_bound < p4_lower_gate,
 "historical_bounds_eV": {
  "planck_2018": planck_bound,
  "planck_desi_2024": desi_2024_bound,
 },
 "note": (
 "Σm_ν = 0.0853 eV exceeds the DESI DR2 + CMB ΛCDM bound of 0.064 eV, which "
 "already lies below the registered 0.075 eV P.4 gate. The row is a TENSION "
 "rather than a gate crossing because the bound is ΛCDM-model-dependent, not a "
 "definitive measurement. The retired Planck 2018 0.12 eV bound no longer yields a PASS."
 ),
 },
 )
 print_summary(res_sum); write_result(res_sum)
 return [res_m1, res_sum]


if __name__ == "__main__":
 main()
