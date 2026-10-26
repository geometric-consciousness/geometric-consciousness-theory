"""
constants.py — Independent Verification Constants Module
=========================================================
Hardcoded empirical anchors for the App PSC independent verification harness.

Design rule (epistemic-circularity guard):
 - Every constant declared here is sourced directly from CODATA 2022
 or PDG 2024 (or an exact mathematical definition).
 - NO constant is imported from the GCT engine, the gct_constants.yaml
 SSOT, or any GCT-derived calculation.
 - This module is the SOLE empirical input of the verification stack.
 - If a verification script needs a number not declared here, it must
 add it here with its CODATA/PDG citation — not pull it from the engine.

The GCT theoretical predictions are re-derived from the manuscript prose
in each verify_<name>.py script, using ONLY:
 (a) The mathematical primitives below (PHI, PI, SQRT2, SQRT5).
 (b) The CODATA/PDG empirical anchors below.
 (c) The structural integer/exponent inputs declared in each script as
 "GCT FORMULA PARAMETER" (e.g. N_MU=11, N_TAU=17). These are read
 from the manuscript, NOT from gct_constants.yaml.

Module name intentionally collides with `gct_utils.C` to make accidental
re-import a hard error. Imports in this harness should always be:
 from verify_independent.constants import CODATA, MATH
"""

from types import SimpleNamespace
import math as _math


# ============================================================================
# MATHEMATICAL PRIMITIVES
# ============================================================================
# Exact constructions from first principles. No empirical input.
# ----------------------------------------------------------------------------

PHI = (1.0 + _math.sqrt(5.0)) / 2.0 # Golden ratio, exact construction
PHI_INV = 1.0 / PHI # = phi - 1
PI = _math.pi # Python's math.pi (double precision)
SQRT2 = _math.sqrt(2.0)
SQRT5 = _math.sqrt(5.0)
LN2 = _math.log(2.0)

MATH = SimpleNamespace(
 PHI=PHI,
 PHI_INV=PHI_INV,
 PI=PI,
 SQRT2=SQRT2,
 SQRT5=SQRT5,
 LN2=LN2,
)


# ============================================================================
# CODATA 2022 / PDG 2024 EMPIRICAL ANCHORS — COMPARISON SINGLE SOURCE OF TRUTH
# ============================================================================
# Source: CODATA 2022 recommended values
# https://physics.nist.gov/cuu/Constants/ (CODATA 2022 release, May 2024)
# ----------------------------------------------------------------------------

# Electron mass — primary GCT dimensional anchor
M_E_MEV = 0.51099895069 # MeV/c^2, CODATA 2022 (u_r = 3.1e-10)
M_E_KG = 9.1093837139e-31 # kg, CODATA 2022

# Proton mass
M_P_MEV = 938.27208816 # MeV/c^2, CODATA 2022

# Muon mass — CODATA 2022
M_MU_MEV = 105.6583755 # MeV/c^2, CODATA 2022 (u_r = 2.2e-8)

# Tau mass — PDG 2024
M_TAU_MEV = 1776.93 # MeV/c^2, PDG 2024 (BES-III + Belle II central value)
M_TAU_MEV_ERR = 0.09

# Fine-structure constant (low-energy)
ALPHA_INV = 137.035999177 # CODATA 2022 (u_r = 1.5e-10)
ALPHA = 1.0 / ALPHA_INV # CODATA 2022, evaluated from the declared reciprocal anchor

# Strong coupling at the Z pole — PDG 2024 world average
ALPHA_S_MZ_PDG_2024 = 0.1180
ALPHA_S_MZ_PDG_2024_ERR = 0.0009

# Newton constant
G_SI = 6.67430e-11 # m^3 kg^-1 s^-2, CODATA 2022 (rel. unc. 2.2e-5)

# Speed of light (exact, SI definition)
C_LIGHT = 299792458.0 # m/s, exact

# Planck constant is exact by the post-2019 SI definition.  Derive hbar from
# that exact input so the formula and evaluated digits share one source.
H_PLANCK = 6.62607015e-34 # J·s, exact
HBAR = H_PLANCK / (2.0 * _math.pi) # J·s

# Planck mass (standard, M_P = sqrt(hbar c / G))
# Derived from CODATA c, hbar, G — kept here as a derived empirical anchor
# rather than recomputed in each script. NB the m_e protocol uses this M_P.
M_PLANCK_STD_KG = _math.sqrt(HBAR * C_LIGHT / G_SI) # ~2.176434e-8 kg

# eV to Joule conversion
EV_TO_J = 1.602176634e-19 # exact (SI definition since 2019)

# Higgs VEV — PDG 2024
V_HIGGS_GEV = 246.21965 # GeV, from G_F = 1/(sqrt(2) v^2), PDG 2024

# Quark masses — PDG 2024 central values (MSbar at scale 2 GeV for u,d,s)
M_U_MEV = 2.16 # PDG 2024 (range 1.67–2.65)
M_D_MEV = 4.70 # PDG 2024
M_S_MEV = 93.5 # PDG 2024
M_C_GEV = 1.2730 # PDG 2024 (MSbar at m_c)
M_B_GEV = 4.183 # PDG 2024 (MSbar at m_b)
M_B_GEV_ERR = 0.007 # PDG 2024 quoted uncertainty (labelled CL = 90%)
M_C_GEV_ERR = 0.0046 # PDG 2024 quoted uncertainty (labelled CL = 90%)
M_T_GEV = 172.57 # PDG 2024 direct-measurement mass (not a pole mass; PDG pole from cross sections: 172.4 +/- 0.7 GeV)
M_T_GEV_ERR = 0.29 # PDG 2024 direct-measurement uncertainty (GeV)

# CKM elements — PDG 2024 RPP CKM global-fit standard parametrization
S12_CKM = 0.22501 # s_12 = |V_us| / c_13, PDG 2024 CKM review
S23_CKM = 0.0418 # PDG 2024
S13_CKM = 0.003732 # PDG 2024 global-fit central

# PMNS — NuFIT 6.0 (Esteban et al., JHEP 12 (2024) 216, arXiv:2410.05380),
# Table 1, normal ordering, IC24 with SK atmospheric data unless noted.
THETA12_DEG = 33.68 # +0.73/-0.70 (same with and without SK)
THETA12_DEG_ERR_MINUS = 0.70
THETA12_DEG_ERR_PLUS = 0.73
THETA23_DEG = 43.3 # +1.0/-0.8 with SK; 3-sigma range 41.3-49.9
THETA23_DEG_WITHOUT_SK = 48.5 # +0.7/-0.9 without SK; 3-sigma range 41.0-50.5
THETA23_3SIGMA_WITH_SK = (41.3, 49.9)
THETA23_3SIGMA_WITHOUT_SK = (41.0, 50.5)
# Delta chi^2 at theta23 = 45 deg from the NuFIT 6.0 one-dimensional sin^2(theta23)
# projections (v60.release-TByes-NO / -TBoff-NO), measured from the global minimum.
THETA23_DCHI2_45_WITH_SK = 2.02
THETA23_DCHI2_45_WITHOUT_SK = 4.20
THETA13_DEG = 8.56 # +/-0.11 with SK (8.52 +/- 0.11 without)
THETA13_DEG_ERR = 0.11
THETA13_DEG_WITHOUT_SK = 8.52
DELTA_CP_DEG = 212.0 # +26/-41 with SK (non-Gaussian)
DELTA_CP_DEG_ERR_PLUS = 26.0
DELTA_CP_DEG_WITHOUT_SK = 177.0 # +19/-20 without SK
DELTA_CP_DEG_WITHOUT_SK_ERR_PLUS = 19.0

# Cabibbo angle observed
THETA_C_DEG = _math.degrees(_math.asin(S12_CKM))  # Cabibbo angle from the PDG s_12 anchor

# Neutrino mass-squared splittings (NuFIT 6.0, normal ordering, IC24 with SK)
DELTA_M2_21 = 7.49e-5 # eV^2
DELTA_M2_31 = 2.513e-3 # eV^2 (Delta m^2_3l for NO)
SIGMA_MNU_PLANCK_BOUND_EV = 0.12 # Planck 2018 (PR3 + BAO), 95% CL (historical context only)
SIGMA_MNU_DESI_2024_EV = 0.072 # Planck + DESI BAO 2024, 95% CL (superseded by DR2)
SIGMA_MNU_DESI_DR2_EV = 0.064 # DESI DR2 BAO + CMB, LambdaCDM, 95% (arXiv:2503.14738); the registered comparator

# Dark matter line empirical anchor
E_DM_LINE_KEV = 3.55 # Bulbul et al. 2014, Perseus/Coma stacking
E_DM_LINE_SIG_KEV = 0.03

# Z mass, W mass
M_Z_GEV = 91.1876 # PDG 2024
M_W_GEV = 80.3692 # GeV, PDG 2024 (Navas et al., PRD 110, 030001)
M_W_GEV_ERR = 0.0133 # GeV, PDG 2024

# Weinberg angle at Z-pole
SIN2_THETA_W_Z = 0.23122 # PDG 2026 MS-bar s^2_Z(M_Z) (not the effective leptonic angle 0.23154)


CODATA = SimpleNamespace(
 # Particle masses
 M_E_MEV=M_E_MEV,
 M_E_KG=M_E_KG,
 M_P_MEV=M_P_MEV,
 M_MU_MEV=M_MU_MEV,
 M_TAU_MEV=M_TAU_MEV,
 M_TAU_MEV_ERR=M_TAU_MEV_ERR,
 M_U_MEV=M_U_MEV,
 M_D_MEV=M_D_MEV,
 M_S_MEV=M_S_MEV,
 M_C_GEV=M_C_GEV,
 M_B_GEV=M_B_GEV,
 M_B_GEV_ERR=M_B_GEV_ERR,
 M_C_GEV_ERR=M_C_GEV_ERR,
 M_T_GEV=M_T_GEV,
 M_T_GEV_ERR=M_T_GEV_ERR,
 M_Z_GEV=M_Z_GEV,
 M_W_GEV=M_W_GEV,
 M_W_GEV_ERR=M_W_GEV_ERR,
 V_HIGGS_GEV=V_HIGGS_GEV,

 # Couplings
 ALPHA=ALPHA,
 ALPHA_INV=ALPHA_INV,
 SIN2_THETA_W_Z=SIN2_THETA_W_Z,

 # Gravity / SI
 G_SI=G_SI,
 C_LIGHT=C_LIGHT,
 H_PLANCK=H_PLANCK,
 HBAR=HBAR,
 M_PLANCK_STD_KG=M_PLANCK_STD_KG,
 EV_TO_J=EV_TO_J,

 # CKM
 S12_CKM=S12_CKM,
 S23_CKM=S23_CKM,
 S13_CKM=S13_CKM,
 THETA_C_DEG=THETA_C_DEG,

 # PMNS
 THETA12_DEG=THETA12_DEG,
 THETA12_DEG_ERR_MINUS=THETA12_DEG_ERR_MINUS,
 THETA12_DEG_ERR_PLUS=THETA12_DEG_ERR_PLUS,
 THETA23_DEG=THETA23_DEG,
 THETA23_DEG_WITHOUT_SK=THETA23_DEG_WITHOUT_SK,
 THETA23_3SIGMA_WITH_SK=THETA23_3SIGMA_WITH_SK,
 THETA23_3SIGMA_WITHOUT_SK=THETA23_3SIGMA_WITHOUT_SK,
 THETA23_DCHI2_45_WITH_SK=THETA23_DCHI2_45_WITH_SK,
 THETA23_DCHI2_45_WITHOUT_SK=THETA23_DCHI2_45_WITHOUT_SK,
 THETA13_DEG=THETA13_DEG,
 THETA13_DEG_ERR=THETA13_DEG_ERR,
 THETA13_DEG_WITHOUT_SK=THETA13_DEG_WITHOUT_SK,
 DELTA_CP_DEG=DELTA_CP_DEG,
 DELTA_CP_DEG_ERR_PLUS=DELTA_CP_DEG_ERR_PLUS,
 DELTA_CP_DEG_WITHOUT_SK=DELTA_CP_DEG_WITHOUT_SK,
 DELTA_CP_DEG_WITHOUT_SK_ERR_PLUS=DELTA_CP_DEG_WITHOUT_SK_ERR_PLUS,

 # Neutrino
 DELTA_M2_21=DELTA_M2_21,
 DELTA_M2_31=DELTA_M2_31,
 SIGMA_MNU_PLANCK_BOUND_EV=SIGMA_MNU_PLANCK_BOUND_EV,
 SIGMA_MNU_DESI_2024_EV=SIGMA_MNU_DESI_2024_EV,
 SIGMA_MNU_DESI_DR2_EV=SIGMA_MNU_DESI_DR2_EV,

 # Dark sector
 E_DM_LINE_KEV=E_DM_LINE_KEV,
 E_DM_LINE_SIG_KEV=E_DM_LINE_SIG_KEV,
)


# ============================================================================
# UTILITIES
# ============================================================================

def ppm_error(predicted: float, observed: float) -> float:
 """Relative error in ppm: |pred - obs| / obs * 1e6."""
 return abs(predicted - observed) / abs(observed) * 1.0e6


def pct_error(predicted: float, observed: float) -> float:
 """Relative error in percent."""
 return abs(predicted - observed) / abs(observed) * 100.0


def kg_to_mev(kg: float) -> float:
 """E = mc^2; report in MeV."""
 return kg * (C_LIGHT ** 2) / (EV_TO_J * 1.0e6)


def mev_to_kg(mev: float) -> float:
 return mev * 1.0e6 * EV_TO_J / (C_LIGHT ** 2)
