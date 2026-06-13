"""
constants.py — Independent Verification Constants Module
=========================================================
Hardcoded empirical anchors for the App R independent verification harness.

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
# CODATA 2022 EMPIRICAL ANCHORS
# ============================================================================
# Source: CODATA 2022 recommended values
# https://physics.nist.gov/cuu/Constants/ (CODATA 2022 release, May 2024)
# ----------------------------------------------------------------------------

# Electron mass — primary GCT dimensional anchor
M_E_MEV = 0.51099895069 # MeV/c^2, CODATA 2022 (u(N) = 1.6e-10)
M_E_KG = 9.1093837139e-31 # kg, CODATA 2022

# Proton mass
M_P_MEV = 938.27208816 # MeV/c^2, CODATA 2022

# Muon mass — PDG 2024
M_MU_MEV = 105.6583755 # MeV/c^2, PDG 2024

# Tau mass — PDG 2024
M_TAU_MEV = 1776.93 # MeV/c^2, PDG 2024 (BES-III + Belle II central value)
M_TAU_MEV_ERR = 0.09

# Fine-structure constant (low-energy)
ALPHA = 7.2973525643e-3 # CODATA 2022
ALPHA_INV = 137.035999177 # CODATA 2022 (u(N) = 2.1e-10)

# Newton constant
G_SI = 6.67430e-11 # m^3 kg^-1 s^-2, CODATA 2022 (rel. unc. 2.2e-5)

# Speed of light (exact, SI definition)
C_LIGHT = 299792458.0 # m/s, exact

# Reduced Planck constant
HBAR = 1.054571817e-34 # J·s, CODATA 2022

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
M_T_GEV = 172.57 # PDG 2024 (pole/direct)

# CKM elements — PDG 2024 (Wolfenstein-parametrization extractions)
S12_CKM = 0.2250 # sin(theta_12) = |V_us| / |V_ud cos delta|, PDG 2024
S23_CKM = 0.0418 # PDG 2024
S13_CKM = 0.003732 # PDG 2024 global-fit central

# PMNS — PDG 2024 (NuFit-5.3 / NOvA / T2K consensus)
THETA12_DEG = 33.40 # PDG / NuFit 2024
THETA23_DEG = 49.5 # NOvA/T2K 2024 (NH), uncertainty ~1.1
THETA23_DEG_ERR = 1.1
THETA13_DEG = 8.58 # PDG / DayaBay
DELTA_CP_DEG = 232.0 # NuFit 5.3 central (NH)

# Cabibbo angle observed
THETA_C_DEG = 13.04 # = arcsin(0.2250)

# Neutrino mass-squared splittings (NuFit 5.3)
DELTA_M2_21 = 7.42e-5 # eV^2
DELTA_M2_31 = 2.51e-3 # eV^2
SIGMA_MNU_PLANCK_BOUND_EV = 0.12 # Planck 2018 (PR3 + BAO), 95% CL
SIGMA_MNU_DESI_2024_EV = 0.072 # Planck + DESI BAO 2024, 95% CL

# Dark matter line empirical anchor
E_DM_LINE_KEV = 3.55 # Bulbul et al. 2014, Perseus/Coma stacking
E_DM_LINE_SIG_KEV = 0.03

# Z mass, W mass
M_Z_GEV = 91.1876 # PDG 2024
M_W_GEV = 80.379 # PDG 2024

# Weinberg angle at Z-pole
SIN2_THETA_W_Z = 0.23122 # PDG 2024 (effective leptonic)


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
 M_T_GEV=M_T_GEV,
 M_Z_GEV=M_Z_GEV,
 M_W_GEV=M_W_GEV,
 V_HIGGS_GEV=V_HIGGS_GEV,

 # Couplings
 ALPHA=ALPHA,
 ALPHA_INV=ALPHA_INV,
 SIN2_THETA_W_Z=SIN2_THETA_W_Z,

 # Gravity / SI
 G_SI=G_SI,
 C_LIGHT=C_LIGHT,
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
 THETA23_DEG=THETA23_DEG,
 THETA23_DEG_ERR=THETA23_DEG_ERR,
 THETA13_DEG=THETA13_DEG,
 DELTA_CP_DEG=DELTA_CP_DEG,

 # Neutrino
 DELTA_M2_21=DELTA_M2_21,
 DELTA_M2_31=DELTA_M2_31,
 SIGMA_MNU_PLANCK_BOUND_EV=SIGMA_MNU_PLANCK_BOUND_EV,
 SIGMA_MNU_DESI_2024_EV=SIGMA_MNU_DESI_2024_EV,

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
