#!/usr/bin/env python3
"""
protocol_zeno_energy_budget.py -- Zeno Drive Energy Budget: Tavis-Cummings Cooperative Pumping
=================================================================
Tavis-Cummings cooperative pumping model for the Zeno Drive.

Conditional sensitivity calculation for whether N nuclear spins (fueled by
ATP) can cooperatively pump energy into the phason field to nucleate the
3.55 keV Identity Polaron without thermal decoherence destroying the process.

Three Acceptance Tests
----------------------
  B1. Derive the single-spin coupling g_single to the phason mode.
  B2. Compute N_crit and N_bio; verify cooperativity N_crit <= N_bio.
  B3. Phonon cascade / Landauer energy-entropy accounting.

Output
------
  data/zeno_energy_budget_results.json
"""

import sys
import json
import math
import numpy as np
from pathlib import Path

# ---------------------------------------------------------------------------
# Path bootstrap
# ---------------------------------------------------------------------------
_SRC = Path(__file__).resolve().parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from gct_utils import get_output_path
from gct_utils import C


# ============================================================================
# JSON encoder for numpy types
# ============================================================================
class _NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, (np.bool_,)):
            return bool(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


# ============================================================================
# External empirical prior: CODATA/SI constants and unit conversions.
# ============================================================================

HBAR    = 1.054571817e-34   # J·s   (reduced Planck constant)
KB      = 1.380649e-23      # J/K   (Boltzmann constant)
EV      = 1.602176634e-19   # J     (electron-volt)
NA      = 6.02214076e23     # mol^-1 (Avogadro)
C_LIGHT = 2.99792458e8      # m/s

# Golden ratio (from GCT SSOT)
PHI = float(C.PHI)

# Load-bearing GCT prediction: cage geometry parameter from the icosahedral
# construction and YAML SSOT, not a fitted Zeno value.
N_CAGE = 144

# External empirical prior: representative Posner/molecular bond-length scale
# used in the substrate coupling estimate.
A_LATTICE_NM = 0.5          # nm
A_LATTICE_M  = A_LATTICE_NM * 1e-9   # m

# External empirical prior: proton mass used for the longitudinal nuclear-scale mode.
M_PROTON = 1.67262192e-27   # kg

# ============================================================================
# GCT Parameters (from SSOT / prior protocols)
# ============================================================================

# Tier 3 branch anchor [Ledger B2]: primary Protocol A-Prime Zeno drive.
OMEGA_PHASON_HZ = 112e6     # cyclic Hz (primary branch center)
OMEGA_PHASON    = OMEGA_PHASON_HZ * 2 * math.pi  # angular frequency


def hz_to_rad_s(freq_hz: float) -> float:
    return 2.0 * math.pi * freq_hz


def _assert_angular_frequency(label: str, angular_value: float, cyclic_hz: float) -> None:
    expected = hz_to_rad_s(cyclic_hz)
    if not math.isclose(angular_value, expected, rel_tol=1.0e-12, abs_tol=0.0):
        raise ValueError(
            f"{label} unit guard failed: angular rad/s value {angular_value} "
            f"does not equal 2*pi*{cyclic_hz} Hz"
        )


_assert_angular_frequency("OMEGA_PHASON", OMEGA_PHASON, OMEGA_PHASON_HZ)

# Phason stiffness K_perp = K_parallel * phi^{-18}
# K_parallel is set by the lattice (harmonic spring constant):
#   K_parallel = m_eff * omega^2 where omega is the longitudinal phonon frequency
# External empirical prior: 1 THz representative longitudinal phonon frequency.
OMEGA_LONG_HZ   = 1e12      # 1 THz longitudinal phonon frequency
OMEGA_LONG      = hz_to_rad_s(OMEGA_LONG_HZ)
_assert_angular_frequency("OMEGA_LONG", OMEGA_LONG, OMEGA_LONG_HZ)
UNIT_CONVENTION_GUARD_PASS = True
K_PARALLEL = M_PROTON * OMEGA_LONG**2   # N/m

K_PERP = K_PARALLEL * PHI**(-18)   # Phason stiffness (soft mode)

# External empirical prior plus model identification: electron-mass scale for
# the Identity Polaron core.
M_EFF_PHASON = 9.1093837e-31  # kg (Electron mass)

# Verification target / diagnostic display: reference polaron radius used only
# for volume reporting in this protocol. The operative healing-length entry is
# disclosed in Parameter Ledger xi / App K §K.5.
XI_HEALING_M = 7.25e-9  # m   (7.25 nm -- Tier 1 a_0/alpha; Tier 3 MT-lumen scale match)


# ============================================================================
# TEST B1: Single-spin coupling g_single
# ============================================================================
# Formula: g_single = f_overlap * (mu_Trp_dipole * E_phason_field / hbar) * phi^{-9} * u_zpf
#
# Interpretation:
#   - mu_Trp_dipole   : Trp S0->S1 transition dipole moment (5 Debye, in C*m)
#   - E_phason_field  : effective phason electric field at the tubulin dimer,
#                       derived from the phason zero-point energy and dimer volume
#   - (mu_Trp * E_phason / hbar) : coupling frequency [rad/s]
#   - phi^{-9} / a_lattice : geometric gradient from RT shell attenuation [1/m]
#   - u_zpf           : zero-point fluctuation amplitude of phason [m]
#
# The coupling is the Trp dipole transition moment native to beta-tubulin.
# O.21 currently identifies Trp21 as the local-inward wall-patch candidate;
# Trp103/Trp346/Trp407 remain screened candidate partners until assembled-MT
# lumen-axis closure fixes the actual radical-pair geometry.

def compute_g_single():
    """
    Compute the single-spin coupling to the phason mode.

    The tryptophan radical chain in beta-tubulin is the chromophore.
    E_phason_field is not calibrated; it is the kinematic zero-point
    fluctuation field of an electron-mass phason mode.

    The coupling is:
        g_single = f_overlap * (mu_Trp_dipole * E_phason_field / hbar) * phi^{-9}
    """
    # External empirical prior: Debye conversion and Trp S0->S1 transition dipole.
    DEBYE_TO_CM = 3.33564e-30           # C*m per Debye
    mu_Trp_dipole = 5.0 * DEBYE_TO_CM   # 5 Debye -> C*m  (Trp S0->S1)

    # Kinematic Zero-Point Electric Field of the Phason
    # E_zpf = omega * u_zpf = sqrt(hbar * omega / (2 * m_e))
    E_phason_field = math.sqrt((HBAR * OMEGA_PHASON) / (2.0 * M_EFF_PHASON)) # V/m

    # Base dipole coupling frequency [rad/s]
    omega_coupling = (mu_Trp_dipole * E_phason_field) / HBAR

    # Geometric gradient: dS_vac/du [1/m] (RT shell attenuation)
    dS_du = PHI**(-9) / A_LATTICE_M    

    # Single-spin coupling
    # Tier 3 upper-edge substrate estimate [O.16]: wavefunction-overlap
    # factor; disclosed as a first-principles dipole-cage overlap task.
    f_overlap = 1.0e-2
    g_single = f_overlap * omega_coupling * dS_du * math.sqrt(HBAR / (2.0 * M_EFF_PHASON * OMEGA_PHASON))

    return g_single, {
        "chromophore": "Trp aromatic radical chain in beta-tubulin",
        "mu_Trp_dipole_Debye": 5.0,
        "E_phason_field_V_m": E_phason_field,
        "omega_coupling_MHz": omega_coupling / (2 * math.pi) / 1e6,
        "PHI_to_neg9": PHI**(-9),
        "f_overlap": f_overlap,
        "g_single_Hz": g_single / (2 * math.pi),
    }


# ============================================================================
# TEST B2: Cooperativity — N_crit vs N_bio
# ============================================================================

def compute_cooperativity(g_single: float):
    """
    Compute N_crit (critical spin count for collective enhancement)
    and N_bio (spins available in biological volume).

    Verdict: PASS if N_crit <= N_bio

    Physical interpretation of kappa
    ---------------------------------
    The phason decay rate kappa = K_perp_dimless * omega_c / N_cage where
    K_perp_dimless = phi^{-18} is the *dimensionless* geometric stiffness
    ratio (fraction of longitudinal stiffness that is transverse in the RT
    lattice).  This gives kappa units of rad/s consistently.

    Physical interpretation of N_bio
    ----------------------------------
    N_bio in the load-bearing verdict is the central beta-tubulin branch:
    n_rp = 0 until O.21 identifies an assembled-microtubule lumen-axis
    radical-pair oscillator. The n_rp = 1 beta-Trp count is retained as a
    separate sensitivity branch, not as live arithmetic for the central verdict.
    The Posner 31P pathway is reported separately as a secondary comparison,
    not used for the load-bearing verdict.

    Parameters
    ----------
    g_single : float
        Single-spin coupling in rad/s.
    """
    # ---- Decoherence rates -------------------------------------------------
    # gamma: pessimistic spin decoherence rate
    # External empirical prior: conservative spin-decoherence scale.
    GAMMA_HZ   = 1000.0                          # Hz (spin decoherence)
    GAMMA      = GAMMA_HZ * 2 * math.pi          # rad/s

    # kappa: phason decay rate
    # kappa = K_perp_dimless * omega_c / N_cage
    # where K_perp_dimless = phi^{-18}  (geometric stiffness fraction)
    K_PERP_DIMLESS = PHI**(-18)                  # dimensionless
    OMEGA_C        = OMEGA_PHASON                # rad/s  (= 2*pi*112 MHz)
    KAPPA          = K_PERP_DIMLESS * OMEGA_C / N_CAGE   # rad/s

    # ---- N_crit -----------------------------------------------------------
    # N_crit = gamma * kappa / g_single^2   (all in rad/s units)
    N_CRIT = GAMMA * KAPPA / (g_single**2)

    # ---- Polaron volume (for reference only) --------------------------------
    # Verification target / diagnostic display: reference polaron radius only.
    R_POLARON_NM = 8.5       # nm
    V_POLARON_NM3 = (4.0/3.0) * math.pi * R_POLARON_NM**3   # nm^3
    V_POLARON_L   = V_POLARON_NM3 * 1e-24                    # liters

    # ---- Biological spin pool: central branch + separate sensitivity branch -
    # Ch13 §13.1.2 / V1 Ch17 §17.1.4b use:
    #   central branch n_rp=0 pending O.21;
    #   sensitivity branch ~10^5 MTs/neuron x 1250 dimers/MT x n_rp=1
    #   viable beta-Trp host = 1.25e8 participating radical-pair dipoles.
    # The Posner 31P path is kept as a secondary comparison only.
    R_CELL_NM     = 15e3                          # nm  (= 15 um)
    V_CELL_NM3    = (4.0/3.0) * math.pi * R_CELL_NM**3   # nm^3
    V_CELL_L      = V_CELL_NM3 * 1e-24            # liters

    # Geometric-cage-derived branch per App F §F.4 + O.33: beta-Trp sensitivity substrate count.
    MT_PER_NEURON = 1.0e5
    DIMERS_PER_MT = 1250.0
    N_RP_PER_DIMER_CENTRAL = 0.0
    N_RP_PER_DIMER_SENSITIVITY = 1.0
    N_BIO = MT_PER_NEURON * DIMERS_PER_MT * N_RP_PER_DIMER_CENTRAL
    N_BIO_SENSITIVITY = MT_PER_NEURON * DIMERS_PER_MT * N_RP_PER_DIMER_SENSITIVITY

    # External empirical prior: secondary Posner comparison, not load-bearing closure.
    C_POSNER_M        = 100e-6      # mol/L  (100 uM Posner concentration; secondary substrate per O.30)
    SPINS_PER_POSNER  = 6           # 31P nuclei per Posner molecule
    N_POSNER_PROXY = C_POSNER_M * NA * V_CELL_L * SPINS_PER_POSNER

    cooperativity = N_BIO / N_CRIT if N_CRIT > 0 else float('inf')
    cooperativity_sensitivity = N_BIO_SENSITIVITY / N_CRIT if N_CRIT > 0 else float('inf')
    verdict_b2 = bool(N_CRIT <= N_BIO)
    verdict_b2_sensitivity = bool(N_CRIT <= N_BIO_SENSITIVITY)

    return verdict_b2, {
        "gamma_Hz": GAMMA_HZ,
        "gamma_rad_s": GAMMA,
        "K_perp_dimless": K_PERP_DIMLESS,
        "PHI_to_neg18": K_PERP_DIMLESS,
        "omega_c_Hz": OMEGA_C / (2 * math.pi),
        "kappa_rad_s": KAPPA,
        "kappa_Hz": KAPPA / (2 * math.pi),
        "N_crit": N_CRIT,
        "R_polaron_nm": R_POLARON_NM,
        "V_polaron_nm3": V_POLARON_NM3,
        "V_polaron_L": V_POLARON_L,
        "R_cell_nm": R_CELL_NM,
        "V_cell_nm3": V_CELL_NM3,
        "V_cell_L": V_CELL_L,
        "MT_per_neuron": MT_PER_NEURON,
        "dimers_per_MT": DIMERS_PER_MT,
        "n_rp_per_dimer": N_RP_PER_DIMER_CENTRAL,
        "n_rp_per_dimer_sensitivity_branch": N_RP_PER_DIMER_SENSITIVITY,
        "N_bio_basis": "central beta-tubulin branch n_rp=0 pending O.21; n_rp=1 beta-Trp count reported only as sensitivity branch",
        "C_posner_M": C_POSNER_M,
        "spins_per_posner": SPINS_PER_POSNER,
        "N_posner_secondary_comparison": N_POSNER_PROXY,
        "N_bio": N_BIO,
        "N_bio_central": N_BIO,
        "N_bio_sensitivity_branch": N_BIO_SENSITIVITY,
        "cooperativity_ratio": cooperativity,
        "cooperativity_ratio_sensitivity_branch": cooperativity_sensitivity,
        "sensitivity_branch": {
            "n_rp_per_dimer": N_RP_PER_DIMER_SENSITIVITY,
            "N_bio": N_BIO_SENSITIVITY,
            "cooperativity_ratio": cooperativity_sensitivity,
            "verdict": verdict_b2_sensitivity,
            "basis": "conditional beta-Trp n_rp=1 sensitivity branch; not the central live-arithmetic branch",
        },
        "verdict": verdict_b2,
    }



# ============================================================================
# TEST B3: Phonon Cascade Energy Accounting (Landauer)
# ============================================================================

def compute_energy_budget(N_bio: float):
    """
    Verify that the ATP-driven energy cascade can nucleate the Identity Polaron.

    Checks:
    1. Does N_bio contain enough spins to process E_vac worth of ATP energy?
    2. Does the entropy released by ATP hydrolysis cover polaron negentropy?

    Verdict: PASS if both close within a factor of 2.
    """
    # ---- Polaron energy target ---------------------------------------------
    # Load-bearing GCT prediction: 3.55 keV Identity Polaron energy.
    E_VAC_EV    = 3548.6                     # eV  (3.55 keV Identity Polaron)
    E_VAC_J     = E_VAC_EV * EV              # J

    # ---- ATP energy budget -------------------------------------------------
    # External empirical prior: ATP hydrolysis free-energy scale.
    EPS_ATP_EV  = 0.52                       # eV per ATP hydrolysis
    EPS_ATP_J   = EPS_ATP_EV * EV            # J

    N_ATP_RAW   = E_VAC_EV / EPS_ATP_EV     # dimensionless

    # ---- Check 1: Can N_bio generate enough ATP throughput? ----------------
    # Each spin can mediate one ATP-phonon coupling event per decoherence time.
    # Over the Zeno cycle time T_zeno = 1/omega_c, each spin contributes
    # one "transaction" of energy ~ hbar * omega_phason.
    E_PER_SPIN_EV = HBAR * OMEGA_PHASON / EV   # eV per spin per Zeno cycle
    N_SPINS_NEEDED = E_VAC_EV / E_PER_SPIN_EV  # spins needed to deliver E_vac

    ratio_spins = N_bio / N_SPINS_NEEDED if N_SPINS_NEEDED > 0 else float('inf')
    check1 = ratio_spins >= 0.5             # within factor of 2

    # ---- Check 2: Entropy balance (Landauer) --------------------------------
    # Entropy released by N_ATP hydrolysis events:
    #   Delta_S_released = N_ATP * k_B * ln(2)      [J/K]
    # Negentropy cost of forming the polaron (ordering of N_cage modes):
    #   Delta_S_polaron   = k_B * N_cage * ln(phi)  [J/K]  (RT symmetry reduction)
    #
    # Condition: Delta_S_released >= Delta_S_polaron

    DELTA_S_RELEASED_J_K = N_ATP_RAW * KB * math.log(2)
    DELTA_S_POLARON_J_K  = KB * N_CAGE * math.log(PHI)

    ratio_entropy = DELTA_S_RELEASED_J_K / DELTA_S_POLARON_J_K
    check2 = ratio_entropy >= 0.5           # within factor of 2

    verdict_b3 = bool(check1 and check2)

    return verdict_b3, {
        "E_vac_eV": E_VAC_EV,
        "E_vac_J": E_VAC_J,
        "eps_ATP_eV": EPS_ATP_EV,
        "N_ATP_raw": N_ATP_RAW,
        "E_per_spin_eV": E_PER_SPIN_EV,
        "N_spins_needed": N_SPINS_NEEDED,
        "N_bio": N_bio,
        "ratio_spins_bio_needed": ratio_spins,
        "check1_spins_sufficient": check1,
        "Delta_S_released_J_K": DELTA_S_RELEASED_J_K,
        "Delta_S_polaron_J_K": DELTA_S_POLARON_J_K,
        "ratio_entropy": ratio_entropy,
        "check2_entropy_sufficient": check2,
        "verdict": verdict_b3,
    }


# ============================================================================
# TEST B4: Anti-Zeno Crossover
# ============================================================================

def compute_antizeno_crossover():
    """
    Computes the operational signature of the protected-subspace Zeno
    enhancement: a frequency-dependent effective T_2 with peak at the
    chiral phonon-polariton resonance (~112 MHz) and decay off-resonance
    (anti-Zeno regime). The current peak T_2 value is synchronized to
    protocol_o23_dfs_collective_dressing.py: O.23 shows the qualitative
    direction but remains short of the 10 ms Protocol A-Prime target.

    Bare single-pair Misra-Sudarshan extension (Facchi-Pascazio 2008 eq.
    16 applied to the Trp hyperfine Hamiltonian) uses the cyclic-frequency
    convention tau_Z = 1/f_hf. At the engine midpoint f_hf ~ 30 MHz and
    tau_meas ~ 10 ns, tau_eff^{bare MS} ~ (33 ns)^2 / 10 ns ~ 110 ns;
    the 10 ms target requires a protected-subspace effective coupling
    Omega_DFS ~ 10^5 rad/s; current O.23 collective dressing reaches
    a sub-ms best case rather than the target.
    """
    # Tier 3 calibrated anchor [Ledger B2] and external empirical prior:
    # operating resonance and in-vitro radical-pair baseline.
    f_res = 112e6  # primary Protocol A-Prime operating branch
    T2_raw = 10e-6 # 10 us in-vitro radical-pair baseline

    # Current O.23 collective-dressing output (best_tau_eff_collective_s).
    # The 10 ms value is retained as the target, not as the achieved peak.
    peak_T2 = 8.686658405550221e-4
    target_T2 = 10e-3

    freqs = np.linspace(50e6, 500e6, 451)
    
    # Lorentzian DOS (Sharp geometric resonance)
    # Verification target: operational resonance-width sentinel for A-Prime
    # scan design. This anti-Zeno subcheck is diagnostic, not a physical
    # crossover calculation; the physical crossover requires solving the
    # bath spectral density far-tail integral against the Misra-Sudarshan
    # kernel (pending O.23).
    gamma = 1.5e6  # 1.5 MHz width
    L = (gamma**2) / ((freqs - f_res)**2 + gamma**2)
    
    # T2_eff profile: Peaks at peak_T2, decays below T2_raw at high frequencies (Anti-Zeno)
    # We assign an Anti-Zeno floor of say 0.01 * T2_raw for extreme off-resonance fast driving
    anti_zeno_floor = T2_raw * 0.01 
    T2_eff = anti_zeno_floor + (peak_T2 - anti_zeno_floor) * L
    
    # Find crossover where T2_eff drops back below T2_raw (transition to Anti-Zeno)
    crossover_idx = np.where(T2_eff < T2_raw)[0]
    if len(crossover_idx) > 0:
        f_cross = freqs[crossover_idx[0]]
    else:
        f_cross = 0.0
        
    # Query specific points
    idx_112 = np.argmin(np.abs(freqs - 112e6))
    idx_150 = np.argmin(np.abs(freqs - 150e6))
    
    T2_112 = T2_eff[idx_112]
    T2_150 = T2_eff[idx_150]
    
    diagnostic_shape_pass = bool(T2_112 > T2_raw and T2_150 < T2_raw)
    physical_crossover_verdict = False
    
    return physical_crossover_verdict, {
        "f_res_MHz": 112.0,
        "diagnostic_sentinel": True,
        "closure_target": "O.23: physical anti-Zeno crossover from bath spectral density integral",
        "peak_T2_ms": peak_T2 * 1000.0,
        "target_T2_ms": target_T2 * 1000.0,
        "current_peak_source": "protocol_o23_dfs_collective_dressing.best_tau_eff_collective_s",
        "status": "DIAGNOSTIC_SENTINEL_ONLY__PHYSICAL_CROSSOVER_PENDING",
        "crossover_f_MHz": f_cross / 1e6,
        "T2_at_112MHz_ms": T2_112 * 1000.0,
        "T2_at_150MHz_ms": T2_150 * 1000.0,
        "T2_raw_ms": T2_raw * 1000.0,
        "diagnostic_shape_pass": diagnostic_shape_pass,
        "physical_crossover_verdict": physical_crossover_verdict,
        "verdict": physical_crossover_verdict
    }

# ============================================================================
# TEST B5: Chiral Phonon-Polaritons & OAM DFS
# ============================================================================

def compute_chiral_phonon_polariton_dfs():
    """
    Computes candidate OAM-DFS isolation and the Berry Phase steering condition.
    
    Verifies that the Zeno Drive does NOT supply the energy.
    Instead, it couples Trp radical pairs to Chiral Phonon-Polaritons in the alpha-helix.
    Because these polaritons carry Orbital Angular Momentum (OAM), they are a
    candidate DFS-protection channel pending O.23, not a closed immunity claim.
    The topological mismatch Gamma_OAM_loss << gamma_0 acts as the filter.
    The 112 MHz primary-branch drive imparts a geometric Berry Phase that breaks spatial symmetry,
    steering the ambient ATP energy (0.52 eV) into the correct conformational change.
    Current O.23 collective dressing reaches the 100 us operative floor but remains
    below the 1 ms and 10 ms targets; this is not a closed DFS pass.
    """
    # External empirical prior: base thermal decoherence rate for linear phonons.
    gamma_0 = 1000.0
    # Load-bearing GCT prediction: single OAM mismatch quantum.
    OAM_quantum = 1
    
    # O.23 collective-dressing result. The 1000 s DFS isolation assumption is
    # outside this calculation.
    tau_dfs = 8.686658405550221e-4
    gamma_dfs = 1.0 / tau_dfs
    dfs_target_s = 1.0e-2
    
    # Berry Phase Steering Energy Budget
    # External empirical prior: ATP hydrolysis energy.
    E_atp_eV = 0.52
    E_drive_eV = HBAR * (2 * math.pi * 112e6) / EV # 112 MHz quantum (negligible)
    
    # The condition is that ATP supplies energy and the O.23 DFS reaches the
    # registered 10 ms target. Current O.23 remains short of that target.
    verdict_b5 = bool(E_atp_eV >= 0.52 and tau_dfs >= dfs_target_s)
    
    return verdict_b5, {
        "OAM_quantum": OAM_quantum,
        "gamma_0_Hz": gamma_0,
        "gamma_dfs_Hz": gamma_dfs,
        "tau_dfs_s": tau_dfs,
        "dfs_target_s": dfs_target_s,
        "reaches_operative_target_100us": bool(tau_dfs >= 1.0e-4),
        "reaches_operative_target_1ms": bool(tau_dfs >= 1.0e-3),
        "reaches_selection_target_10ms": bool(tau_dfs >= dfs_target_s),
        "E_atp_eV": E_atp_eV,
        "E_drive_eV": E_drive_eV,
        "berry_phase_steering": True,
        "verdict": verdict_b5
    }

# ============================================================================
# TEST B6: Relativistic Zeno Decoherence Limit
# ============================================================================

def compute_relativistic_zeno_decoherence(g_single: float, N_bio_rest: float):
    """
    Computes the maximum conscious velocity (v_max) by calculating the critical
    Lorentz factor (gamma_crit) where time-dilated ATP flux drops below the
    Tavis-Cummings threshold (N_crit).
    """
    # Recalculate N_crit
    GAMMA_HZ = 1000.0
    GAMMA = GAMMA_HZ * 2 * math.pi
    K_PERP_DIMLESS = PHI**(-18)
    OMEGA_C = OMEGA_PHASON
    KAPPA = K_PERP_DIMLESS * OMEGA_C / N_CAGE
    N_CRIT = GAMMA * KAPPA / (g_single**2)
    
    # As v -> c, effective pumping spins N_eff = N_bio_rest / gamma
    # Decoherence limit: N_eff = N_crit  => gamma_crit = N_bio_rest / N_crit
    if N_CRIT > 0 and N_bio_rest >= N_CRIT:
        gamma_crit = N_bio_rest / N_CRIT
        # v_max is sub-c by delta_v = c/(2*gamma_crit^2)
        # This ensures the conscious velocity is strictly less than c
        delta_v_over_c = 0.5 / (gamma_crit**2)
        v_max_c = 1.0 - delta_v_over_c
        v_max = v_max_c * C_LIGHT
    else:
        gamma_crit = 1.0
        v_max_c = 0.0
        v_max = 0.0

    verdict_b6 = bool(gamma_crit > 1.0)

    return verdict_b6, {
        "N_crit": N_CRIT,
        "N_bio_rest": N_bio_rest,
        "gamma_crit": gamma_crit,
        "v_max_m_s": v_max,
        "v_max_c": v_max_c,
        "verdict": verdict_b6
    }

# ============================================================================
# MAIN
# ============================================================================

# Global to share N_bio across tests without threading
N_BIO_GLOBAL = 0.0


def main():
    global N_BIO_GLOBAL

    print("=" * 70)
    print("  Zeno Drive Energy Budget: Tavis-Cummings Cooperative Pumping")
    print("  Zeno Drive Energy Budget: Tavis-Cummings Cooperative Pumping")
    print("=" * 70)

    # -----------------------------------------------------------------------
    # Print physical parameters used
    # -----------------------------------------------------------------------
    print("\n[Parameters]")
    print(f"  PHI (golden ratio)         : {PHI:.10f}")
    print(f"  N_cage                     : {N_CAGE}")
    print(f"  K_parallel                 : {K_PARALLEL:.4e} N/m")
    print(f"  K_perp = K_par * phi^-18   : {K_PERP:.4e} N/m")
    print(f"  omega_phason               : {OMEGA_PHASON/(2*math.pi)/1e6:.1f} MHz")
    print(f"  m_eff (phason)             : {M_EFF_PHASON:.4e} kg  (electron-mass scale)")

    # -----------------------------------------------------------------------
    # B1: g_single
    # -----------------------------------------------------------------------
    print("\n[B1] Computing single-spin coupling g_single...")
    g_single, b1_info = compute_g_single()

    print(f"  Chromophore                : {b1_info['chromophore']}")
    print(f"  mu_Trp (dipole moment)    : {b1_info['mu_Trp_dipole_Debye']:.1f} Debye")
    print(f"  E_phason_field (approx)   : {b1_info['E_phason_field_V_m']:.4e} V/m")
    print(f"  omega_coupling            : {b1_info['omega_coupling_MHz']:.4f} MHz")
    print(f"  phi^-9 (geometric factor) : {b1_info['PHI_to_neg9']:.6f}")
    print(f"  f_overlap (Tier 3)        : {b1_info['f_overlap']:.2e}  [upper-edge substrate estimate]")
    print(f"  g_single                  : {b1_info['g_single_Hz']:.4e} Hz")

    b1_pass = b1_info['g_single_Hz'] > 0

    print(f"  B1 status                 : {'[PASS] g_single > 0' if b1_pass else '[FAIL]'}")

    # -----------------------------------------------------------------------
    # B2: Cooperativity
    # -----------------------------------------------------------------------
    print("\n[B2] Computing cooperativity condition...")
    verdict_b2, b2_info = compute_cooperativity(g_single)
    N_BIO_GLOBAL = b2_info['N_bio']

    print(f"  gamma (spin decoherence)  : {b2_info['gamma_Hz']:.1f} Hz")
    print(f"  K_perp (phi^-18, dimless) : {b2_info['K_perp_dimless']:.6f}")
    print(f"  omega_c                   : {b2_info['omega_c_Hz']/1e6:.1f} MHz")
    print(f"  kappa (phason decay)      : {b2_info['kappa_Hz']:.4e} Hz")
    print(f"  g_single                  : {g_single/(2*math.pi):.4e} Hz")
    print()
    print(f"  R_polaron                 : {b2_info['R_polaron_nm']:.1f} nm")
    print(f"  V_polaron                 : {b2_info['V_polaron_nm3']:.2f} nm^3")
    print(f"  R_cell (biological pool)  : {b2_info['R_cell_nm']/1e3:.0f} um")
    print(f"  V_cell                    : {b2_info['V_cell_L']:.4e} L")
    print(f"  MTs/neuron                : {b2_info['MT_per_neuron']:.2e}")
    print(f"  dimers/MT                 : {b2_info['dimers_per_MT']:.0f}")
    print(f"  n_rp/dimer (central)      : {b2_info['n_rp_per_dimer']:.0f}")
    print(f"  n_rp/dimer (sensitivity)  : {b2_info['n_rp_per_dimer_sensitivity_branch']:.0f}")
    print(f"  Posner comparison        : {b2_info['N_posner_secondary_comparison']:.4e} spins")
    print()
    print(f"  N_crit = gamma*kappa/g^2  : {b2_info['N_crit']:.4e}")
    print(f"  N_bio  central branch     : {b2_info['N_bio']:.4e}")
    print(f"  N_bio  sensitivity branch : {b2_info['N_bio_sensitivity_branch']:.4e}")
    print(f"  Cooperativity ratio       : {b2_info['cooperativity_ratio']:.4f}")
    print(f"  Sensitivity ratio         : {b2_info['cooperativity_ratio_sensitivity_branch']:.4f}")
    print(f"  N_crit <= N_bio?          : {verdict_b2}   {'[PASS]' if verdict_b2 else '[FAIL]'}")

    # -----------------------------------------------------------------------
    # B3: Energy Budget
    # -----------------------------------------------------------------------
    print("\n[B3] Computing phonon cascade energy budget...")
    verdict_b3, b3_info = compute_energy_budget(N_BIO_GLOBAL)

    print(f"  E_vac (Identity Polaron)  : {b3_info['E_vac_eV']:.1f} eV")
    print(f"  eps_ATP                   : {b3_info['eps_ATP_eV']:.2f} eV")
    print(f"  N_ATP required            : {b3_info['N_ATP_raw']:.1f}")
    print()
    print(f"  E per spin per Zeno cycle : {b3_info['E_per_spin_eV']:.4e} eV")
    print(f"  N_spins needed            : {b3_info['N_spins_needed']:.4e}")
    print(f"  N_bio available           : {b3_info['N_bio']:.4e}")
    print(f"  Ratio bio/needed          : {b3_info['ratio_spins_bio_needed']:.4f}")
    print(f"  CHECK 1: N_bio sufficient : {b3_info['check1_spins_sufficient']}   {'[PASS]' if b3_info['check1_spins_sufficient'] else '[FAIL] -- factor of 2 margin not met'}")
    print()
    print(f"  Delta_S released (ATP)    : {b3_info['Delta_S_released_J_K']:.4e} J/K")
    print(f"  Delta_S polaron (cost)    : {b3_info['Delta_S_polaron_J_K']:.4e} J/K")
    print(f"  Entropy ratio             : {b3_info['ratio_entropy']:.4f}")
    print(f"  CHECK 2: Entropy balance  : {b3_info['check2_entropy_sufficient']}   {'[PASS]' if b3_info['check2_entropy_sufficient'] else '[FAIL] -- factor of 2 margin not met'}")
    print(f"  B3 verdict                : {'[PASS]' if verdict_b3 else '[FAIL]'}")

    # -----------------------------------------------------------------------
    # B5: Chiral Phonon-Polaritons & OAM DFS
    # -----------------------------------------------------------------------
    print("\n[B5] Computing Chiral Phonon-Polaritons & Berry Phase Steering...")
    verdict_b5, b5_info = compute_chiral_phonon_polariton_dfs()

    print(f"  OAM Quantum Mismatch      : {b5_info['OAM_quantum']}")
    print(f"  gamma_0 (Symmetric decay) : {b5_info['gamma_0_Hz']} Hz")
    print(f"  gamma_dfs (OAM protected) : {b5_info['gamma_dfs_Hz']:.2e} Hz")
    print()
    print(f"  tau_dfs (Protection Code) : {b5_info['tau_dfs_s']*1e3:.3f} ms")
    print(f"  E_atp (Hydrolysis Fuel)   : {b5_info['E_atp_eV']:.2f} eV")
    print(f"  E_drive (100 MHz quantum) : {b5_info['E_drive_eV']:.2e} eV")
    print(f"  Berry Phase Steering      : {b5_info['verdict']}   {'[PASS] ATP supplies energy; OAM-DFS candidate condition satisfied' if b5_info['verdict'] else '[FAIL]'}")

    # -----------------------------------------------------------------------
    # B6: Relativistic Zeno Decoherence
    # -----------------------------------------------------------------------
    print("\n[B6] Computing Relativistic Zeno Decoherence Limit...")
    verdict_b6, b6_info = compute_relativistic_zeno_decoherence(g_single, N_BIO_GLOBAL)
    print(f"  N_crit (Zeno threshold)   : {b6_info['N_crit']:.4e}")
    print(f"  N_bio (rest frame spins)  : {b6_info['N_bio_rest']:.4e}")
    print(f"  gamma_crit (Decoherence)  : {b6_info['gamma_crit']:.4f}")
    if verdict_b6:
        print(f"  v_max (Conscious Limit)   : {b6_info['v_max_m_s']:.2f} m/s  ({b6_info['v_max_c']:.6f} c)")
    print(f"  B6 verdict                : {'[PASS] Agent liquefies before c' if verdict_b6 else '[FAIL] Cannot safely compute limits'}")

    # -----------------------------------------------------------------------
    # Final verdict
    # -----------------------------------------------------------------------
    all_pass = b1_pass and verdict_b2 and verdict_b3 and verdict_b5 and verdict_b6
    central_nrp_zero_o21_pending = (
        b1_pass
        and verdict_b2 is False
        and b2_info.get("N_bio_central") == 0.0
        and b2_info.get("sensitivity_branch", {}).get("verdict") is True
        and b3_info.get("check1_spins_sufficient") is False
        and b5_info.get("reaches_operative_target_100us") is True
        and b5_info.get("reaches_selection_target_10ms") is False
    )
    canonical_trp_spin_gap = (
        b1_pass and verdict_b2 and (not verdict_b3) and verdict_b5 and verdict_b6
        and b3_info.get("check1_spins_sufficient") is False
        and b3_info.get("check2_entropy_sufficient") is True
    )
    canonical_trp_spin_gap_plus_o23 = (
        b1_pass and verdict_b2 and (not verdict_b3) and (not verdict_b5) and verdict_b6
        and b3_info.get("check1_spins_sufficient") is False
        and b3_info.get("check2_entropy_sufficient") is True
        and b5_info.get("reaches_operative_target_100us") is True
        and b5_info.get("reaches_selection_target_10ms") is False
    )
    final_tag = (
        "PASS" if all_pass else
        "CENTRAL_N_RP_ZERO_O21_PENDING_WITH_SENSITIVITY_BRANCH" if central_nrp_zero_o21_pending else
        "B3_SPIN_COUNT_GAP_CANONICAL_TRP" if canonical_trp_spin_gap else
        "B3_SPIN_COUNT_GAP_PLUS_O23_DFS_SHORTFALL" if canonical_trp_spin_gap_plus_o23 else
        "FAIL"
    )
    disposition_text = (
        "Operative biological central branch uses n_rp=0 pending O.21, so B2 "
        "cooperativity and downstream B3/B6 energy-delivery checks do not close "
        "as live arithmetic. The n_rp=1 beta-Trp count is reported only as a "
        "sensitivity branch; it preserves the arithmetic cooperativity ratio but "
        "does not become the central verdict until O.21 closes. Current O.23 DFS "
        "collective dressing reaches the 100 us floor but remains below the 10 ms "
        "Selection target. Posner concentration is reported only as a secondary "
        "comparison, not as load-bearing closure."
    )

    print("\n" + "=" * 70)
    print("  FINAL VERDICT")
    print("=" * 70)
    if all_pass:
        print("  [PASS] B1 (g_single)         : PASS  -- coupling is real and positive")
        print("  [PASS] B2 (Cooperativity)    : PASS  -- N_crit <= N_bio achieved")
        print("  [PASS] B3 (Energy Balance)   : PASS  -- Landauer budget closes")
        print("  [PASS] B5 (Chiral Phonon DFS): PASS  -- OAM isolation and ATP steering")
        print("  [PASS] B6 (Relativistic Lim) : PASS  -- gamma_crit correctly bounds velocity")
        print()
        print("  VERDICT: PASS")
        print("  ATP-driven cooperative pumping satisfies this arithmetic budget under the stated closure assumptions.")
    else:
        print(f"  B1: {'PASS' if b1_pass else 'FAIL'}   "
              f"B2: {'PASS' if verdict_b2 else 'FAIL'}   "
              f"B3: {'PASS' if verdict_b3 else 'FAIL'}   "
              f"B5: {'PASS' if verdict_b5 else 'FAIL'}   "
              f"B6: {'PASS' if verdict_b6 else 'FAIL'}")
        print(f"  VERDICT: {final_tag}")
        if central_nrp_zero_o21_pending or canonical_trp_spin_gap:
            print(f"  DISPOSITION: {disposition_text}")

    # -----------------------------------------------------------------------
    # Zeno Formula & Anti-Zeno
    # -----------------------------------------------------------------------
    def zeno_coherence_time(tau_Z_seconds, tau_zeno_seconds):
        """
        Misra-Sudarshan Zeno formula (Misra & Sudarshan 1977 J. Math. Phys. 18:756;
        Facchi & Pascazio 2008 J. Phys. A 41:493001 eq. 16).

            tau_eff = tau_Z^2 / tau_zeno

        Valid in the quadratic-decay regime tau_zeno < tau* = tau_Z^2 / T_2;
        for tau_zeno > tau* the system is in the inverse-Zeno regime and the
        formula is an extrapolated diagnostic rather than a universal lower
        bound or guaranteed enhancement (Facchi-Pascazio 2008 §2.2.5). tau_Z is reported in the cyclic-frequency convention
        (DeltaE/h, Hz) for consistency with protocol_decoherence_audit.py:

            tau_Z^{-2} = <psi_0 | H_int^2 | psi_0> - <psi_0 | H_int | psi_0>^2

        For the Trp radical-pair singlet driven by the canonical hyperfine
        singlet-triplet variance Delta_ST/h = 30 MHz, tau_Z ~ 33 ns.
        """
        return tau_Z_seconds**2 / tau_zeno_seconds

    # Trp radical-pair Zeno time: variance of hyperfine Hamiltonian in singlet
    # state, using the canonical Delta_ST/h = 30 MHz cyclic-frequency value.
    f_hf_Hz = 30e6                         # canonical bare S-T variance, cyclic Hz
    tau_Z_s = 1.0 / f_hf_Hz                # ~ 33 ns
    tau_zeno_s = 1.0 / OMEGA_PHASON_HZ     # ~8.9 ns (112 MHz primary drive)
    tau_eff = zeno_coherence_time(tau_Z_s, tau_zeno_s)

    # Bare single-pair Misra-Sudarshan extension for the Trp radical-pair channel
    # is sub-microsecond and does NOT close the ~10^3 shielding gap to the 10 ms Selection
    # target alone. The closure mechanism (chiral phonon-polariton DFS, V1
    # §17.1.3c) is registered as App H Open Problem O.23; this protocol reports
    # the bare radical-pair channel only.
    
    print("\n[B4] Computing Anti-Zeno Crossover...")
    verdict_b4, b4_info = compute_antizeno_crossover()
    print(f"  T2 at 112 MHz (Resonance) : {b4_info['T2_at_112MHz_ms']:.3f} ms")
    print(f"  T2 at 150 MHz (Off-Res)   : {b4_info['T2_at_150MHz_ms']:.3f} ms")
    print(f"  Crossover Frequency       : {b4_info['crossover_f_MHz']:.1f} MHz")
    print(
        "  B4 status                 : "
        f"{b4_info['status']} "
        f"(diagnostic shape pass={b4_info['diagnostic_shape_pass']})"
    )

    # -----------------------------------------------------------------------
    # Save JSON
    # -----------------------------------------------------------------------
    results = {
        "protocol": "Zeno Drive Energy Budget (Tavis-Cummings)",
        "tau_raw_corrected": 1e-5,
        "shielding_required": 1000,
        "shielding_from_zeno": tau_eff / 1e-5,
        "shielding_from_current_dfs": b4_info["peak_T2_ms"] / (1e-5 * 1000.0),
        "tau_eff_ms": tau_eff * 1000.0,
        "surface_code_removed": True,
        "model_note": "Trp radical-pair chromophore chain coupled via chiral phonon-polariton DFS.",
        "B1_g_single": b1_info,
        "B2_cooperativity": b2_info,
        "B3_energy_balance": b3_info,
        "B4_antizeno_crossover": b4_info,
        "anti_zeno_subcheck_scope": (
            "Lorentzian width parameter gamma=1.5e6 is a DIAGNOSTIC sentinel, "
            "not a physical crossover. Physical anti-Zeno crossover requires "
            "solving the bath spectral density far-tail integral against the "
            "Misra-Sudarshan kernel; pending O.23."
        ),
        "B5_chiral_polariton_dfs": b5_info,
        "B6_relativistic_decoherence": b6_info,
        "parameters": {
            "PHI": PHI,
            "N_cage": N_CAGE,
            "K_parallel_N_m": K_PARALLEL,
            "K_perp_N_m": K_PERP,
            "omega_phason_MHz": OMEGA_PHASON / (2 * math.pi) / 1e6,
            "m_eff_kg": M_EFF_PHASON,
        },
        "verdict": final_tag,
        "disposition_text": disposition_text,
        "pass": bool(all_pass),
    }

    out_path = get_output_path("protocol_zeno_energy_budget_results.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2, cls=_NumpyEncoder)
    print(f"\n  Results saved to: {out_path}")
    print("=" * 70)

    # Standalone refresh success means the registered expected-verdict artifact
    # was generated. The intrinsic closure status remains in results["pass"].
    return 0


if __name__ == "__main__":
    sys.exit(main())
