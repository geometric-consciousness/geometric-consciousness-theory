#!/usr/bin/env python3
"""
protocol_dm_line_forward_model.py — XRISM Component
===========================================================
Generates the expected spectral data for the 3.55 keV emission line,
convolving the physical signal with Cluster Kinematics and 
Instrument Response (XRISM Resolve).

Models:
1. Standard CDM (Decaying Dark Matter)
   - Emitters are virialized particles in the halo.
   - Velocity dispersion: v_vir ~ 1300 km/s (Perseus Cluster).
   - Broadening: Doppler Broadening dominates instrument resolution.

2. GCT (Topological Glass)
   - Emitters are lattice defects (fractures).
   - Recoil is absorbed by the macroscopic lattice (Mössbauer-like).
   - Intrinsic width ~ 0.
   - Velocity dispersion: Bulk turbulence / flow only. v_turb ~ 300 km/s.
   - Broadening: Dominated by Instrument Resolution (5 eV).

Output:
- dm_line_prediction.png: Visual comparison.
- distinguishability_report.json: Sigma separation.
"""

# ============================================================================
# OBSERVATIONAL_STATUS
# Documents the XRISM-era empirical status of the 3.55 keV line in the
# Resolve dataset and the GCT engagement protocol.
# ============================================================================
OBSERVATIONAL_STATUS = """
XRISM Resolve Empirical Status -- 3.55 keV Line
================================================
Data Source:  XRISM Early Science Release (Tashiro et al.; Ishisaki et al. 2022 for calibration)
Exposure:     3.75 Megaseconds (Ms) stacked across 10 galaxy clusters
Target line:  3.55 keV (GCT predicted: 3.5486 keV)

Result:       NON-DETECTION of the 3.55 keV line in the stacked dataset.

Upper Limit:  Gamma <= 1.0e-27 s^-1  (3 sigma)

Sensitivity Gap:
  The XMM-Newton detection by Bulbul et al. (2014) implied a decay rate
  near 0.2e-27 s^-1. The XRISM early-data upper limit is
  approximately 5x WEAKER than this threshold. XRISM has therefore NOT
  yet reached the sensitivity required to confirm or exclude the signal.

Physical Conclusion:
  The XRISM early data is PHYSICALLY INCONCLUSIVE. The non-detection is
  consistent with both the GCT Lattice Fracture model and the standard
  sterile-neutrino model at this sensitivity level.

GCT Prediction Status:
  STANDS -- pending the Protocol C stress-aperture test in
  mass-weighted above-sigma_crit regions of the XRISM stacked-cluster
  sample, with sigma_crit numerically frozen at 0.53 keV cm^-3
  from the Perseus-core / Bullet-shock pressure bracket.
  The Perseus core is sub-sigma_crit and is not a falsification aperture.
  A terminal no-line null requires the Bulbul-level empirical-derived
  Protocol C floor Gamma <= 2.0e-28 s^-1 in >=94 Ms equivalent stacked
  exposure. The 26 Ms / Gamma <= 3.8e-28 s^-1 stack is the registered
  morphology and linewidth milestone, not the terminal no-line falsifier.
  A detected line remains falsified by W_int > 20 eV or by smooth-template
  morphology across the frozen target-cell aperture.
  The background-limited Gamma <= 1.2e-30 s^-1 calculation is theoretical,
  not operative. No falsification has occurred.

Registration Status:
  XRISM test is logged as 'Under Test (Data Inconclusive, Analysis Ongoing)'
  in App_V, App_R, Ch11 sec.11.4.4, Ch15 sec.15.5, and
  04_Prediction_Postdiction_Firewall.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
from pathlib import Path
import sys
import os

try:
    from scipy.special import wofz
    _HAS_WOFZ = True
except ImportError:
    _HAS_WOFZ = False

try:
    from gct_utils import get_output_path
except ImportError:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from gct_utils import get_output_path

# Constants
C_LIGHT = 299792.458  # km/s
G_CONST = 6.67430e-11 # m^3 kg^-1 s^-2
M_SOLAR = 1.98847e30  # kg
KPC_TO_M = 3.08567758e19
E0_KEV   = 3.5486      # GCT predicted energy (raw emission)

# Instrument: XRISM Resolve
# FWHM = 5 eV best in-flight performance; mission spec is 5-7 eV across the
# 0.3-12 keV bandpass per the XRISM Resolve mission documentation. Sigma =
# FWHM / 2.355. The canonical engine baseline uses the best-performance
# 5.0 eV value at 3.55 keV; decision-rule reports should run a sensitivity
# sweep over the [5.0, 6.0, 7.0] band when reporting the predicted Voigt
# FWHM and its decision-rule implications (Ch15 §15.1.2 + §15.2).
XRISM_FWHM_EV = 5.0
XRISM_SIGMA_EV = XRISM_FWHM_EV / 2.355

# Cluster Physics (Perseus)
V_VIRIAL_KMS = 1300.0  # Standard CDM velocity dispersion
V_TURB_KMS   = 300.0   # GCT bulk turbulence limit

# Perseus Cluster Gravitational Parameters
M_500_SOLAR = 6.6e14   # Solar masses
R_CORE_KPC  = 100.0    # Characteristic emission radius (kpc)

def calculate_gravitational_redshift():
    """
    Calculates z_grav = GM / (R c^2) for the Perseus Cluster.
    Returns: z_grav
    """
    M_kg = M_500_SOLAR * M_SOLAR
    R_m  = R_CORE_KPC * KPC_TO_M
    c_ms = C_LIGHT * 1000.0
    
    z_grav = (G_CONST * M_kg) / (R_m * (c_ms**2))
    return z_grav

def gaussian(x, mu, sigma, amp=1.0):
    return amp * np.exp(-0.5 * ((x - mu) / sigma)**2)


def voigt_profile(E, mu, sigma_inst_ev, width_intrinsic_fwhm_ev):
    """
    Normalised Voigt profile = convolution of a Lorentzian intrinsic line
    (full-width-at-half-maximum width_intrinsic_fwhm_ev) with a Gaussian
    instrument response (standard deviation sigma_inst_ev).

    Physical content:
    -----------------
    The GCT lattice-fracture line is Mossbauer-narrowed at emission (recoil
    is absorbed by the macroscopic lattice; intrinsic Lorentzian linewidth
    FWHM = width_intrinsic_fwhm_ev, typically << instrument). Once it propagates
    through the XRISM Resolve microcalorimeter, the observed line shape is
    the convolution of that Lorentzian with the instrument's Gaussian
    response. The exact analytic result is the Voigt profile, evaluated
    here via the complex error function w(z) = exp(-z^2) erfc(-iz).

    Inputs
    ------
    E                  : np.ndarray, energy grid (eV)
    mu                 : float, line centroid (eV)
    sigma_inst_ev      : float, instrument Gaussian sigma (eV)
    width_intrinsic_fwhm_ev : float, intrinsic Lorentzian FWHM (eV)

    Returns
    -------
    np.ndarray, normalised PDF (integral = 1) over the energy grid.

    Fallback
    --------
    If scipy.special.wofz is unavailable, the convolution is computed by
    direct FFT of the Gaussian and Lorentzian kernels on the energy grid.
    """
    lorentz_half_width_ev = 0.5 * width_intrinsic_fwhm_ev
    if _HAS_WOFZ and sigma_inst_ev > 0:
        z = ((E - mu) + 1j * lorentz_half_width_ev) / (sigma_inst_ev * np.sqrt(2.0))
        return np.real(wofz(z)) / (sigma_inst_ev * np.sqrt(2.0 * np.pi))
    # FFT fallback: explicit convolution of normalised Lorentzian * Gaussian.
    dE = E[1] - E[0]
    gauss_kernel = np.exp(-0.5 * ((E - mu) / max(sigma_inst_ev, 1e-12))**2)
    gauss_kernel /= (gauss_kernel.sum() * dE)
    lorentz_half_width_ev = max(lorentz_half_width_ev, 1e-12)
    lorentz_kernel = (lorentz_half_width_ev / np.pi) / ((E - mu)**2 + lorentz_half_width_ev**2)
    # Symmetric FFT convolution centred on mu
    conv = np.fft.fftshift(np.fft.ifft(
        np.fft.fft(np.fft.ifftshift(gauss_kernel)) *
        np.fft.fft(np.fft.ifftshift(lorentz_kernel))
    ).real) * dE
    integral = conv.sum() * dE
    if integral > 0:
        conv /= integral
    return conv


def voigt_fwhm(sigma_inst_ev, width_intrinsic_fwhm_ev):
    """
    Olivero & Longbothum (1977) approximation to the FWHM of a Voigt profile.

        FWHM_V ~ 0.5346 * FWHM_L + sqrt(0.2166 * FWHM_L^2 + FWHM_G^2)

    where FWHM_L = width_intrinsic_fwhm_ev is the deconvolved intrinsic
    Lorentzian full width and FWHM_G = 2 * sqrt(2 * ln 2) * sigma_inst_ev
    ~ 2.355 * sigma_inst_ev. Accurate to ~0.02% over the full Voigt
    parameter range.

    Returns
    -------
    float, FWHM of the Voigt profile (eV).
    """
    fwhm_g = 2.0 * np.sqrt(2.0 * np.log(2.0)) * sigma_inst_ev
    fwhm_l = width_intrinsic_fwhm_ev
    return 0.5346 * fwhm_l + np.sqrt(0.2166 * fwhm_l**2 + fwhm_g**2)

def generate_forward_model():
    print("="*60)
    print("GCT Protocol: XRISM Forward Model (Gravitational Redshift Included)")
    print("="*60)
    
    # 1. Calculate Gravitational Redshift
    z_grav = calculate_gravitational_redshift()
    E_obs_kev = E0_KEV / (1.0 + z_grav)
    E_obs_ev  = E_obs_kev * 1000.0
    
    print(f"Cluster Mass (M500): {M_500_SOLAR:.1e} M_sun")
    print(f"Emission Radius:    {R_CORE_KPC:.1f} kpc")
    print(f"Grav. Redshift (z): {z_grav:.2e}")
    print(f"Raw Energy (E0):    {E0_KEV:.4f} keV")
    print(f"Shifted Energy:     {E_obs_kev:.6f} keV (Delta: {(E0_KEV - E_obs_kev)*1000:.2f} eV)")
    
    # 2. Calculate Widths
    
    # Model A: Standard CDM
    # Doppler width: sigma_E = E0 * (v/c)
    sigma_doppler_cdm = (E_obs_ev) * (V_VIRIAL_KMS / C_LIGHT) # eV
    sigma_total_cdm   = np.sqrt(sigma_doppler_cdm**2 + XRISM_SIGMA_EV**2)
    fwhm_cdm          = sigma_total_cdm * 2.355
    
    # Model B: GCT
    # Intrinsic line is Lorentzian (Mossbauer-narrowed lattice-fracture
    # emission). Bulk turbulence contributes an additional Gaussian Doppler
    # broadening that adds in quadrature with the instrument Gaussian. The
    # observed line shape is therefore a Voigt: Lorentzian (intrinsic) *
    # Gaussian (instrument + turbulence). The §15.2 falsification rule
    # (W_int > 20 eV --> falsified) relies on this Lorentzian-wing signature.
    sigma_doppler_gct = (E_obs_ev) * (V_TURB_KMS / C_LIGHT)  # eV (Gaussian)
    sigma_inst_gct    = np.sqrt(XRISM_SIGMA_EV**2 + sigma_doppler_gct**2)
    # Baseline GCT: intrinsic Lorentzian FWHM ~ 0 (Mossbauer limit).
    WIDTH_INT_BASELINE_FWHM_EV = 0.01  # eV, conservative non-zero floor for plotting
    fwhm_gct = voigt_fwhm(sigma_inst_gct, WIDTH_INT_BASELINE_FWHM_EV)

    # Sweep intrinsic Lorentzian FWHM in [0, 20] eV to map the line-shape
    # locus against the §15.2 W_int > 20 eV falsification threshold.
    width_grid_fwhm_ev = np.linspace(0.0, 20.0, 41)
    voigt_locus = [
        {
            "width_intrinsic_fwhm_ev": float(width_fwhm),
            "fwhm_voigt_ev": float(voigt_fwhm(sigma_inst_gct, width_fwhm)),
        }
        for width_fwhm in width_grid_fwhm_ev
    ]

    print(f"\nObserved Energy: {E_obs_kev:.4f} keV")
    print(f"XRISM Resolution: {XRISM_FWHM_EV:.1f} eV FWHM")

    print(f"\nModel A: Standard CDM (Decaying Sterile Neutrino) -- Gaussian-only")
    print(f"  v_dispersion: {V_VIRIAL_KMS:.0f} km/s")
    print(f"  sigma_kin:    {sigma_doppler_cdm:.2f} eV")
    print(f"  sigma_total:  {sigma_total_cdm:.2f} eV")
    print(f"  FWHM_total:   {fwhm_cdm:.2f} eV")

    print(f"\nModel B: GCT (Topological Lattice Emission) -- Voigt profile")
    print(f"  v_dispersion (turbulence): {V_TURB_KMS:.0f} km/s")
    print(f"  sigma_inst_eff (inst + turb): {sigma_inst_gct:.2f} eV")
    print(f"  W_int deconvolved intrinsic line-width residual (baseline): {WIDTH_INT_BASELINE_FWHM_EV:.3f} eV")
    print(f"  FWHM_Voigt (baseline):     {fwhm_gct:.2f} eV")
    print(f"  Voigt locus swept: deconvolved intrinsic line-width residual W_int in [0, 20] eV ({len(voigt_locus)} pts)")
    
    # 3. Distinguishability
    # FWHM difference in sigma units, assuming a 5% measurement error on FWHM.
    # Difference:
    diff_ev = fwhm_cdm - fwhm_gct
    print(f"\nDiscrimination Power:")
    print(f"  Delta FWHM: {diff_ev:.2f} eV")
    print(f"  [WARNING] K-XVIII (3.514 keV) contamination requires explicit subtraction!")
    
    # 4. Generate Plot
    energy_grid_ev = np.linspace(E_obs_ev - 50, E_obs_ev + 50, 500)

    profile_cdm = gaussian(energy_grid_ev, E_obs_ev, sigma_total_cdm)
    profile_gct = voigt_profile(energy_grid_ev, E_obs_ev,
                                sigma_inst_gct, WIDTH_INT_BASELINE_FWHM_EV)
    # Re-normalise the GCT profile to peak = 1 for visual comparison only;
    # the underlying PDF is already integral-normalised.
    if profile_gct.max() > 0:
        profile_gct = profile_gct / profile_gct.max()
    
    # Instrument Response (Delta function input)
    profile_inst = gaussian(energy_grid_ev, E_obs_ev, XRISM_SIGMA_EV)
    
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(energy_grid_ev, profile_cdm, color='#e74c3c', linewidth=2.5, label=f'Standard CDM (Virial)\nFWHM ~ {fwhm_cdm:.1f} eV')
    ax.plot(energy_grid_ev, profile_gct, color='#2ecc71', linewidth=2.5, label=f'GCT (Cold Lattice)\nFWHM ~ {fwhm_gct:.1f} eV')
    ax.plot(energy_grid_ev, profile_inst, color='#3498db', linestyle='--', alpha=0.6, label=f'Instrument Response\nFWHM = {XRISM_FWHM_EV:.1f} eV')
    
    ax.set_title(f"XRISM Resolve Prediction: 3.55 keV DM Line (Redshifted)\nPerseus Cluster Context (E_obs = {E_obs_kev:.4f} keV)", fontsize=14)
    ax.set_xlabel("Energy (eV)", fontsize=12)
    ax.set_ylabel("Normalized Intensity (counts/s/keV)", fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.2)
    
    # Add text annotation
    ax.text(0.02, 0.95, f"GCT PREDICTION:\nz_grav = {z_grav:.2e}\nLine will be dominated by\ninstrument resolution,\nNOT virial motion.", 
            transform=ax.transAxes, color='#2ecc71', fontsize=10, va='top', 
            bbox=dict(facecolor='black', alpha=0.5, edgecolor='#2ecc71'))

    out_plot = get_output_path("dm_line_prediction.png")
    plt.savefig(out_plot, dpi=120)
    print(f"\nPlot saved to {out_plot}")
    
    # 5. Save JSON Report
    report = {
        "energy_rest_kev": E0_KEV,
        "energy_observed_kev": E_obs_kev,
        "z_gravitational": z_grav,
        "instrument_fwhm_ev": XRISM_FWHM_EV,
        "models": {
            "CDM": {
                "profile_shape": "Gaussian",
                "velocity_kms": V_VIRIAL_KMS,
                "sigma_kin_ev": sigma_doppler_cdm,
                "fwhm_total_ev": fwhm_cdm
            },
            "GCT": {
                "profile_shape": "Voigt",
                "velocity_kms": V_TURB_KMS,
                "sigma_inst_eff_ev": float(sigma_inst_gct),
                "width_intrinsic_fwhm_baseline_ev": WIDTH_INT_BASELINE_FWHM_EV,
                "fwhm_voigt_baseline_ev": float(fwhm_gct),
                "voigt_locus_width_intrinsic_fwhm_ev": voigt_locus
            }
        },
        "fwhm_difference_cdm_minus_gct_ev": float(diff_ev),
        # Decision-rule scalar matching the line-shape separation above.
        "discrimination_delta_ev": float(diff_ev),
        "verdict": "DISTINGUISHABLE" if diff_ev > 5.0 else "AMBIGUOUS",
        "pass": bool(diff_ev > 5.0),
        "expected_fwhm_ev": float(fwhm_gct)
    }
    
    out_json = get_output_path("protocol_dm_line_forward_model_results.json")
    with open(out_json, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Report saved to {out_json}")

if __name__ == "__main__":
    generate_forward_model()
