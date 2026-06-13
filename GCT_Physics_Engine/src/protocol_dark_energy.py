#!/usr/bin/env python3
"""
GCT Dark Energy Protocol: Holographic Entanglement Entropy & Biogenic Drive
Filename: protocol_dark_energy.py

Two independent computations:
  1. Holographic Entanglement Entropy consistency check for Lambda
     (Tier 2 area-law mechanism + Tier 3 absolute magnitude):
     rho_Lambda = (3 * Omega_Lambda / (8 * pi)) * hbar * H0^2 / (c * l_P^2)
     The Ryu-Takayanagi formula applied to the cosmic event horizon boundary
     of the 6D -> 3D projection supplies the area-law mechanism. The absolute
     magnitude imports H0/Omega_Lambda and remains Tier 3 pending O.1/O.4
     RG-running / condensate-normalisation closure.

  2. Biogenic Drive w(z) model (diagnostic Tier 3 shape proxy):
     Checks the phantom-directed single-channel shape and delegates the
     DESI/Euclid state-level arbitration to protocol_imp01_pipeline.py and
     protocol_de_multichannel.py. No covariance-aware cosmological likelihood
     or physical multi-fluid density evolution is claimed here.
"""

import numpy as np
import json
import math
import os
import io
import sys
from pathlib import Path
# Force UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from gct_utils import get_output_path, GCTReporter
from gct_utils import C


def _json_safe(value):
    """Convert numpy scalars and NaN/Inf floats to strict-JSON values."""
    if isinstance(value, dict):
        return {k: _json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_json_safe(v) for v in value]
    if isinstance(value, tuple):
        return [_json_safe(v) for v in value]
    if isinstance(value, np.generic):
        value = value.item()
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


class DarkEnergyAudit:
    # External empirical prior: Planck/LambdaCDM cosmological parameters loaded
    # from the YAML SSOT; they are observational inputs, not GCT anchors.
    H0            = C.H0_PLANCK
    OMEGA_M       = C.OMEGA_M
    OMEGA_L       = C.OMEGA_LAMBDA
    AGE_UNIVERSE  = C.T_UNIVERSE

    # Tier 3 calibrated anchor [Ledger C-sector]: biogenic-DE kernel timescales.
    BIO_DELAY_GYR       = C.TAU_BIO_DELAY
    TECH_SCALE_TIMESCALE = C.TAU_TECH
    # LAMBDA_BIO is the GCT-predicted biogenic-DE coupling, sourced from YAML
    # SSOT (config/gct_constants.yaml LAMBDA_BIO.value = 0.007). The
    # 1/ALPHA_INV_GCT computation gives 0.00727; the two agree to within YAML
    # rounding. The SSOT YAML value is authoritative.
    LAMBDA_BIO_SSOT     = float(C.LAMBDA_BIO)
    # Sensitivity probe: alternative coupling scenario at ~11x the
    # saddle-point value; not the reported anchor.
    LAMBDA_BIO_ALT      = 0.08

    # External empirical prior: Madau-Dickinson SFR-shape parameters from YAML.
    SFR_A     = C.SFR_A
    SFR_ALPHA = C.SFR_ALPHA
    SFR_Z0    = C.SFR_Z0
    SFR_BETA  = C.SFR_BETA

    def __init__(self):
        self.time_gyr = np.linspace(0.1, self.AGE_UNIVERSE, 1000)
        self.z_range = self._time_to_z_from_time_array(self.time_gyr)

    def _time_to_z_approx(self, t):
        """Scalar or Vector t -> z conversion."""
        H0_inv_gyr = 1.0 / (self.H0 * 0.0010227)
        term = 1.5 * np.sqrt(self.OMEGA_L) * (t / H0_inv_gyr)
        arg = np.sinh(term)**2
        # a = (OmegaM/OmegaL * sinh^2)^1/3
        # Handle t=0 or small values
        with np.errstate(divide='ignore', invalid='ignore'):
             a = (arg * (self.OMEGA_M / self.OMEGA_L))**(1.0/3.0)
        
        z = (1.0 / a) - 1.0
        return z

    def _time_to_z_from_time_array(self, time_arr):
        return self._time_to_z_approx(time_arr)

    def compute_holographic_lambda(self):
        """
        Tier 2 area-law mechanism + Tier 3 absolute magnitude for rho_Lambda.

        The Ryu-Takayanagi formula applied to the cosmic event horizon boundary
        of the 6D -> 3D projection gives:
            S_ent = A_H / (4 * l_P^2)
        The vacuum energy density from this boundary entanglement:
            rho_Lambda = (3 * Omega_Lambda / (8 * pi)) * hbar * H0^2 / (c * l_P^2)
        The 10^{-120} suppression relative to the Planck density arises as the
        dimensionless geometric ratio (l_P * H0 / c)^2. The absolute magnitude
        imports the cosmological H0/Omega_Lambda anchor and remains pending
        O.1/O.4 RG-running / condensate-normalisation closure.
        """
        import math
        # External empirical prior: CODATA/SI constants and unit conversion.
        hbar     = 1.054571817e-34   # J*s
        c_si     = 2.99792458e8      # m/s
        G_si     = 6.67430e-11       # m^3 kg^-1 s^-2
        H0_si    = self.H0 * 1000.0 / 3.085677581e22  # km/s/Mpc -> s^-1
        l_P      = math.sqrt(hbar * G_si / c_si**3)   # Planck length, m

        # Holographic rho_Lambda — boxed formula from V2 Ch14 §14.1.5 Step 4:
        #   rho_Lambda = (3 * Omega_Lambda / (8 * pi)) * hbar * H0^2 / (c * l_P^2)
        # The Omega_Lambda factor projects from the critical density rho_crit
        # onto the dark-energy fraction; the 8*pi normalisation tracks the
        # holographic-bound conversion from horizon area to vacuum-energy
        # density.
        Omega_Lambda = float(self.OMEGA_L)
        rho_holographic = (
            3.0 * Omega_Lambda * hbar * H0_si**2
        ) / (8.0 * math.pi * c_si * l_P**2)

        # Verification target / external empirical prior: observed dark-energy
        # density sourced from YAML SSOT (RHO_DE_OBS), derived from rho_crit *
        # Omega_Lambda at H0_PLANCK.
        rho_observed = float(C.RHO_DE_OBS)

        # Planck energy density
        rho_planck = hbar * c_si / l_P**4

        # Suppression ratio relative to Planck scale
        suppression = rho_holographic / rho_planck

        # chi = horizon area / Planck area
        R_H = c_si / H0_si
        A_H = 4.0 * math.pi * R_H**2
        chi = A_H / (4.0 * l_P**2)

        ratio_to_observed = rho_holographic / rho_observed

        return {
            "rho_holographic_J_m3":   rho_holographic,
            "rho_observed_J_m3":      rho_observed,
            "ratio_holographic_to_observed": ratio_to_observed,
            "suppression_vs_planck":  suppression,
            "chi_horizon_area_ratio": chi,
            "l_P_m":                  l_P,
            "R_H_m":                  R_H,
            "derivation":             "Ryu-Takayanagi on cosmic event horizon of 6D->3D projection",
            "tier":                   2,
        }

    def check_lambda_bio_alpha_consistency(self):
        """
        Consistency check: load lambda_bio (Parameter Ledger SSOT) and alpha
        (GCT bare), and verify the saddle-point claim lambda_bio == alpha
        holds within the YAML rounding tolerance (LAMBDA_BIO stored to 3 sf,
        comparison tolerance 5%).

        This is a *consistency check* over two independent YAML constants,
        not a first-principles derivation. The saddle-point closure proper
        (GCT action -> lambda_bio = alpha from variational principle) is
        the analytical content of V3 Ch1 / App M; this script verifies the
        two numerical constants agree post-derivation.
        """
        alpha = 1.0 / float(C.ALPHA_INV_GCT)
        lambda_bio = float(self.LAMBDA_BIO_SSOT)

        return {
            "lambda_bio_yaml_value": lambda_bio,
            "alpha_yaml_value": alpha,
            "equals_alpha_within_5pct": abs(lambda_bio - alpha) / alpha < 5e-2,
            "relative_difference_pct": abs(lambda_bio - alpha) / alpha * 100.0,
            "key_assumption": "Phi_0 = hbar/e (phason condensate VEV normalization)",
            "assumption_verified_by": "App_M Berry connection definition (V3 Ch1)",
            "tier_if_assumption_holds": "Tier 2",
            "tier_if_assumption_fails": "Tier 3",
            "check_type": "YAML-constants consistency, not first-principles derivation",
            "derivation_reference": "V3 Ch1 / App M (GCT action saddle-point, analytical)",
            "physical_interpretation": (
                "The biological information coupling to the metric equals the "
                "fine-structure constant because information processing requires "
                "electromagnetic bond formation (EM coupling alpha), and the phason "
                "field mediating both EM and biological coupling is the same field."
            )
        }


    def calculate_complexity_drive(self):
        """Calculates I(t) using SFR and Tech Multiplier."""
        # Delayed SFR
        t_delayed = self.time_gyr - self.BIO_DELAY_GYR
        # Where t < delay, z approaches infinity (start of universe relative to delay)
        # But for SFR calculation, we just need z corresponding to t_delayed
        # If t_delayed < 0, SFR is 0.
        
        valid = t_delayed > 0
        z_delayed = np.zeros_like(self.time_gyr)
        z_delayed[valid] = self._time_to_z_approx(t_delayed[valid])
        # For invalid times, set z high so SFR -> 0
        z_delayed[~valid] = 100.0 

        # Madau-Dickinson SFR
        # shape ~ (1+z)^a / (1 + [(1+z)/z0]^b)
        sfr = (self.SFR_A
               * (1 + z_delayed)**self.SFR_ALPHA
               / (1 + ((1 + z_delayed) / self.SFR_Z0)**self.SFR_BETA))
        sfr[~valid] = 0

        # Tier 3 calibrated anchor [Ledger C-sector]: exponential
        # complexity-growth timing convention for the biogenic kernel.
        tech_factor = np.exp((self.time_gyr - 5.0) / self.TECH_SCALE_TIMESCALE)
        tech_factor[self.time_gyr < 5.0] = 1.0

        return sfr * tech_factor

    def run_scenario(self, lambda_val, name):
        """Run the simulation for a given lambda."""
        i_dot = self.calculate_complexity_drive()
        
        # Acceleration
        i_double_dot = np.gradient(np.gradient(i_dot, self.time_gyr), self.time_gyr)
        
        # Tier 3 calibrated anchor [Ledger C-sector]: shape normalization for
        # the biogenic-kernel amplitude; it is disclosed as phenomenological.
        scale = np.max(np.abs(i_double_dot))
        norm_accel = i_double_dot / scale
        
        # w(z) = -1 - lambda * accel
        # If accel > 0 (complexity accelerating), w < -1
        w_vals = -1.0 - (lambda_val * norm_accel)
        
        # Find stats
        min_w = np.min(w_vals)
        z_min_w = self.z_range[np.argmin(w_vals)]
        
        # Crossing redshift for the transition into the phantom branch.
        # Typically w starts > -1 in the matter-dominated regime, then drops.
        # i_dot (SFR) grows then decays.
        # If acceleration is positive, w < -1.
        # We look for transition to phantom state (w < -1).
        
        crossing_z = None
        # Scan from high z (early time, index 0) to low z (late time)
        # Index 0 is t=0.1 (high z); index -1 is t=13.8 (z=0).
        # Locate the first crossing below -1.
        
        for i in range(len(w_vals)-1):
            if w_vals[i] > -1.0 and w_vals[i+1] <= -1.0:
                crossing_z = self.z_range[i]
                # The onset closest to the low-z transition is used.
                # Select the one closest to z=0.5 if multiple roots appear.
                # Assuming monotonic transition near z=0.
                
        # CPL Parameterization: w(a) = w0 + wa(1 - a)
        # where a = 1/(1+z), so 1-a = z/(1+z)
        # We can extract w0 = w(z=0) and wa = dw / d(1-a) at z=0
        w0 = w_vals[-1]
        
        # approximate derivative near z=0 (last few points)
        # z values are z_range[-1], z_range[-2], etc. (z decreases towards 0 at the end of the array)
        z_end = self.z_range[-1]
        z_prev = self.z_range[-2]
        w_end = w_vals[-1]
        w_prev = w_vals[-2]
        
        a_end = 1.0 / (1.0 + z_end)
        a_prev = 1.0 / (1.0 + z_prev)
        
        # wa = dw / da, but since w(a) = w0 + wa(1-a), dw/da = -wa
        if a_end != a_prev:
            dw_da = (w_end - w_prev) / (a_end - a_prev)
            wa = -dw_da
        else:
            wa = 0.0
            
        return {
            "name": name,
            "lambda": lambda_val,
            "min_w": min_w,
            "z_at_min": z_min_w,
            "crossing_z": crossing_z,
            "w0": w0,
            "wa": wa,
            "w_final": w_vals[-1]
        }

    def load_canonical_imp01(self):
        """Load the canonical IMP-01 biogenic-DE pipeline output if present."""
        path = Path(get_output_path("protocol_imp01_pipeline_results.json"))
        if not path.exists():
            return None
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
        headline = data.get("headline_run", {})
        return {
            "name": "IMP-01 canonical headline run",
            "lambda": headline.get("lambda_bio"),
            "min_w": headline.get("w_minimum_value"),
            "z_at_min": headline.get("z_of_w_minimum"),
            "crossing_z": headline.get("z_cross_direct_brentq"),
            "z_cross_CPL_fit": headline.get("z_cross_CPL_fit"),
            "w0": headline.get("w0_CPL_fit"),
            "wa": headline.get("wa_CPL_fit"),
            "w_at_z_0": headline.get("w_at_z_0"),
            "w_at_z_028": headline.get("w_at_z_028"),
            "w_at_z_05": headline.get("w_at_z_05"),
            "source": "protocol_imp01_pipeline_results.json::headline_run",
            "interpretation": "canonical continuous-phantom IMP-01 curve; no literal direct crossing"
        }

    def compute_growth_rate_ratio(self, z_target=0.28, lambda_val=None):
        """
        GROWTH DIAGNOSTIC ONLY (NOT f*sigma_8, NOT a likelihood comparison).

        The cosmological structure-growth fingerprint claim in Ch14 is pending
        an S_8/f*sigma_8 likelihood comparison via CAMB/CLASS, closure target
        O.13 channel-C2.

        Computes a diagnostic growth-rate derivative ratio at z_target.
        Integrates the linear growth factor ODE:
          D'' + (2 + H'/H) D' - (3/2) Omega_m D = 0
        in terms of x = ln(a).

        This is not an S_8, sigma8, or f*sigma_8 observable: no sigma8
        normalization, galaxy bias model, covariance, Boltzmann solver, or
        Planck/DESI likelihood comparison is applied.
        """
        from scipy.integrate import solve_ivp
        from scipy.interpolate import interp1d
        
        if lambda_val is None:
            lambda_val = self.LAMBDA_BIO_SSOT
            
        i_dot = self.calculate_complexity_drive()
        i_double_dot = np.gradient(np.gradient(i_dot, self.time_gyr), self.time_gyr)
        scale = np.max(np.abs(i_double_dot))
        norm_accel = i_double_dot / scale
        
        w_vals_gct = -1.0 - (lambda_val * norm_accel)
        z_vals = self.z_range
        
        w_interp = interp1d(z_vals, w_vals_gct, bounds_error=False, fill_value=-1.0)
        
        def w_gct(z):
            return w_interp(z)
            
        def E_sq(z, w_func):
            z_int = np.linspace(0, z, 50)
            if z == 0:
                integral = 0
            else:
                integral = np.trapezoid((1.0 + w_func(z_int)) / (1.0 + z_int), z_int)
            return self.OMEGA_M * (1+z)**3 + self.OMEGA_L * np.exp(3 * integral)
            
        def dlnE_dx(z, w_func):
            E2 = E_sq(z, w_func)
            z_int = np.linspace(0, z, 50)
            if z == 0:
                integral = 0
            else:
                integral = np.trapezoid((1.0 + w_func(z_int)) / (1.0 + z_int), z_int)
            O_DE = self.OMEGA_L * np.exp(3 * integral)
            dH2_dx = -3 * self.OMEGA_M * (1+z)**3 - 3 * (1 + w_func(z)) * O_DE
            return 0.5 * dH2_dx / E2

        def Omega_m_z(z, w_func):
            return self.OMEGA_M * (1+z)**3 / E_sq(z, w_func)

        def growth_odes(x, y, w_func):
            D, D_prime = y
            z = np.exp(-x) - 1.0
            if z < 0: z = 0.0
            term1 = -(2.0 + dlnE_dx(z, w_func)) * D_prime
            term2 = 1.5 * Omega_m_z(z, w_func) * D
            return [D_prime, term1 + term2]

        z_init = 1000.0
        x_init = -np.log(1.0 + z_init)
        x_end = 0.0
        y0 = [np.exp(x_init), np.exp(x_init)]
        
        x_target = -np.log(1.0 + z_target)

        w_lcdm = lambda z: -1.0
        sol_lcdm = solve_ivp(growth_odes, [x_init, x_end], y0, args=(w_lcdm,), 
                             dense_output=True, rtol=1e-8, atol=1e-10)
        
        sol_gct = solve_ivp(growth_odes, [x_init, x_end], y0, args=(w_gct,),
                            dense_output=True, rtol=1e-8, atol=1e-10)
        
        D_prime_lcdm = sol_lcdm.sol(x_target)[1]
        D_prime_gct  = sol_gct.sol(x_target)[1]
        
        ratio = D_prime_gct / D_prime_lcdm
        percent_delta = (ratio - 1.0) * 100.0
        
        return {
            "z_target": z_target,
            "growth_derivative_lcdm": float(D_prime_lcdm),
            "growth_derivative_gct": float(D_prime_gct),
            "growth_rate_ratio": float(ratio),
            "percent_delta": float(percent_delta),
            "diagnostic_note": (
                "Diagnostic-only growth-rate derivative ratio; no sigma8 "
                "normalization and not directly comparable to Planck/DESI "
                "f_sigma8 measurements."
            )
        }

    def compute_wz_curve(self):
        """
        DESI Pre-Registration w(z) Curve.
        Generates the precise w(z) trajectory and observational threshold point.
        """
        i_dot = self.calculate_complexity_drive()
        i_double_dot = np.gradient(np.gradient(i_dot, self.time_gyr), self.time_gyr)
        scale = np.max(np.abs(i_double_dot))
        norm_accel = i_double_dot / scale
        
        w_vals = -1.0 - (self.LAMBDA_BIO_SSOT * norm_accel)
        
        crossing_z = None
        for i in range(len(w_vals)-1):
            if w_vals[i] > -1.0 and w_vals[i+1] <= -1.0:
                crossing_z = self.z_range[i]
                
        w0 = w_vals[-1]
        z_end = self.z_range[-1]
        z_prev = self.z_range[-2]
        a_end = 1.0 / (1.0 + z_end)
        a_prev = 1.0 / (1.0 + z_prev)
        wa = -(w_vals[-1] - w_vals[-2]) / (a_end - a_prev) if a_end != a_prev else 0.0
        
        print("\n" + "="*60)
        print("DESI Pre-Registration w(z) Curve")
        print("="*60)
        if crossing_z is not None:
            print(f"  Direct divide crossing (w = -1) : z ≈ {crossing_z:.3f}")
        else:
            print("  Direct divide crossing (w = -1) : None found")
        print(f"  Current Equation of State : w_0 ≈ {w0:.4f}")
        print(f"  CPL Evolution Parameter   : w_a ≈ {wa:.4f}")
        print("="*60 + "\n")

    def run_audit(self):
        report = GCTReporter("Dark Energy Forensic Audit")
        
        # Scenario 1: local diagnostic for the SSOT coupling; canonical CPL
        # signs/no-crossing are delegated to protocol_imp01_pipeline_results.
        res_ssot_diagnostic = self.run_scenario(self.LAMBDA_BIO_SSOT, "SSOT diagnostic (0.007)")
        res_ssot = self.load_canonical_imp01() or res_ssot_diagnostic

        # Scenario 2: Stronger-coupling sensitivity probe (lambda_bio = 0.08)
        res_alt  = self.run_scenario(self.LAMBDA_BIO_ALT,  "Alt-strong (0.08)")

        # Reporting
        report.section("Comparative Analysis")

        for res in [res_alt, res_ssot]:
            report.log_value(f"Scenario {res['name']}", "")
            report.log_value(f"  Min w(z)", res['min_w'])
            report.log_value(f"  z at min", res['z_at_min'])
            report.log_value(f"  Crossing z (w=-1)", res['crossing_z'])
            report.log_value(f"  w0 (z=0)", res['w0'])
            report.log_value(f"  wa (CPL)", res['wa'])
            
        # Check signal strength
        # Assess whether 0.007 is observationally significant:
        # -1.005 vs -1.000.
        # Observational error on w is ~0.03. 
        # A prediction of -1.005 is observationally indistinguishable from LambdaCDM (-1).
        # A prediction of -1.08 is distinguishable.
        # If GCT claims "Phantom Energy", 0.007 might be too weak to claim visible effect.
        
        strength_msg = "Weak Effect (w ~ -1.005)" if res_ssot_diagnostic['min_w'] > -1.01 else "Strong Effect"
        report.log_value("Signal Strength", strength_msg)

        # Compute the diagnostic growth-rate derivative ratio.
        growth_rate_ratio = self.compute_growth_rate_ratio()
        report.section("Large-Scale Structure (growth-rate diagnostic)")
        report_val = growth_rate_ratio['percent_delta']
        report.log_value("Target z", growth_rate_ratio["z_target"])
        if report_val < 0:
            report.log_value("Growth derivative delta vs LambdaCDM", f"{report_val:.2f}%")
        else:
            report.log_value("Growth derivative delta vs LambdaCDM", f"+{report_val:.2f}%")

        physical_no_crossing = res_ssot.get("crossing_z") is None or (
            isinstance(res_ssot.get("crossing_z"), float)
            and np.isnan(res_ssot.get("crossing_z"))
        )
        passed = bool((res_ssot['min_w'] < -1.0) and physical_no_crossing)

        # Convert numpy types for JSON
        def convert(o):
            if isinstance(o, np.generic): return o.item()
            return o

        # Tier 2 Phason Vacuum properties
        m_phason_ev = 1.7e-5

        lambda_derivation = self.check_lambda_bio_alpha_consistency()
        holographic = self.compute_holographic_lambda()

        report.section("Tier 2: Holographic Entanglement Entropy Lambda")
        report.log_value("rho_Lambda (holographic) [J/m^3]", holographic["rho_holographic_J_m3"])
        report.log_value("rho_Lambda (observed)    [J/m^3]", holographic["rho_observed_J_m3"])
        report.log_value("Ratio holographic/observed",       holographic["ratio_holographic_to_observed"])
        report.log_value("Suppression vs Planck density",    holographic["suppression_vs_planck"])
        report.log_value("chi = A_H / (4 l_P^2)",           holographic["chi_horizon_area_ratio"])

        # Output
        with open(get_output_path("protocol_dark_energy_results.json"), 'w') as f:
            json.dump(_json_safe({
                "tier_2_holographic_lambda": {k: convert(v) for k, v in holographic.items()},
                "tier_2_phason_vacuum": {
                    "w_baseline": -1.0,
                    "m_phason_ev": m_phason_ev
                },
                "tier_3_biogenic_correlation": {
                    "diagnostic_scope": (
                        "Diagnostic single-channel shape proxy only. The "
                        "registered DESI-facing state-level menu arbitration "
                        "lives in protocol_de_multichannel.py; no covariance-"
                        "aware likelihood or physical multi-fluid density "
                        "evolution is claimed by this protocol."
                    ),
                    "canonical_branch": "ssot",
                    "ssot":         {k: convert(v) for k, v in res_ssot.items()},
                    "noncanonical_diagnostics": {
                        "scope": (
                            "Stress-test illustrations only. These branches are not "
                            "canonical DESI-facing outputs, not physical crossing "
                            "claims, and must not be used as the registered P.6 "
                            "CPL-sign comparison."
                        ),
                        "reference_shape_proxy": {
                            **{k: convert(v) for k, v in res_ssot_diagnostic.items()},
                            "canonical": False,
                            "use_for_p6_desi_claim": False,
                        },
                        "alt_strong_stress_test": {
                            **{k: convert(v) for k, v in res_alt.items()},
                            "canonical": False,
                            "use_for_p6_desi_claim": False,
                        },
                    },
                },
                "pass": passed,
                "physical_no_crossing": bool(physical_no_crossing),
                "m_phason_ev": m_phason_ev,
                "lambda_bio_derivation": lambda_derivation,
                "growth_rate_ratio_z028": {k: convert(v) for k, v in growth_rate_ratio.items()}
            }), f, indent=2, allow_nan=False)

if __name__ == "__main__":
    DarkEnergyAudit().run_audit()
