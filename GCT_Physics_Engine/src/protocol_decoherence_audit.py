#!/usr/bin/env python3
"""
protocol_decoherence_audit.py — Quantum Coherence Viability Audit (bare Misra-Sudarshan)
=====================================================================
Evaluates the bare Misra-Sudarshan Zeno extension for a tubulin Trp
radical pair under recombination-rate Zeno sampling. Applied to the
bare Trp radical-pair Hamiltonian, the Misra-Sudarshan formula gives
~110 ns, far below the operative 100 μs–1 ms Selection-relevant
band and still farther below the conservative 10 ms upper gate. The
protected-subspace / chiral phonon-polariton DFS closure that would
bridge this gap is registered as Open
Problem O.23 in App H §H.5 (microtubule correlation-length-derived
collective dressing); this protocol does NOT close the gap.
The displayed bare ~110 ns value is an extrapolated diagnostic outside
the quadratic Misra-Sudarshan regime for the 10 ns drive interval. It is
reported to expose the scale mismatch, not as an in-regime bare lifetime.

Misra-Sudarshan formula:
  τ_eff = τ_Z² / τ_measurement
where τ_Z = 1/Δν_H is the Hamiltonian-variance Zeno time in the
cyclic-frequency convention (Δν_H = ΔE/h, Hz), NOT the exponential
decoherence time T_2. For tubulin Trp radical pairs the relevant variance
is set by the canonical hyperfine singlet-triplet manifold splitting
Δ_ST/h = 30 MHz (App X §X.12), giving τ_Z ≈ 33 ns and
τ_eff ≈ τ_Z² / τ_meas ≈ (33 ns)² / 10 ns ≈ 110 ns at the bare level.

Mechanisms modelled:
  1. Tubulin Tryptophan (Trp) Aromatic Radical Pair native T_2 ≈ 10 μs.
     T_2 is the exponential decoherence time, NOT the Zeno time —
     conflating the two is the standard Misra-Sudarshan error
     explicitly forbidden in App X §X.12.

  2. Zeno measurement rate Γ_rec = 100 MHz; τ_meas = 1/Γ_rec = 10 ns.
     This recombination-channel measurement linewidth is distinct from the
     Tavis-Cummings cavity linewidth kappa_cav used by protocol_eta_zeno.py;
     the two rates answer different physical-channel questions and are not
     directly comparable.

  3. Hamiltonian-variance Zeno time τ_Z = 1/Δ_ST ≈ 33 ns
     (Δ_ST as cyclic frequency, ΔE/h, per App X §X.12).

  4. Bare Misra-Sudarshan extension τ_eff = τ_Z² / τ_meas ~ 100 ns,
     below the 100 μs–1 ms operative band and far below the 10 ms
     conservative gate — closure of the gap requires the protected-
     subspace mechanism of O.23, pending.
"""

import sys
import json
from gct_utils import get_output_path

# ── Tubulin Trp Aromatic Radical Pair Coherence ──────────────────────────────
TAU_NATIVE_T2_S = 10.0e-6     # 10 μs (Native Trp radical pair coherence limit)

# ── Spontaneous Radical Recombination (Non-Unitary Measurement) ──────────────
GAMMA_REC_HZ = 100.0e6        # 100 MHz (Singlet recombination acts as Zeno dissipator)
TAU_REC_S = 1.0 / GAMMA_REC_HZ  # 0.01 μs

def anti_zeno_crossover(zeno_freq_MHz=100.0):
    """
    Derive the bare Misra-Sudarshan Zeno/Anti-Zeno crossover.

    The canonical pulsed-measurement crossover is nu* = T2 / tau_Z^2,
    where T2 is the exponential decay time and tau_Z is the
    Hamiltonian-variance Zeno time in the cyclic-frequency convention.
    For the bare Trp radical-pair Hamiltonian, T2 = 10 us and
    tau_Z ~= 1/(30 MHz), so nu* ~= 9 GHz.
    """
    import numpy as np
    A_couplings_MHz = [42.0, 28.0, 12.0, 7.0, 7.0, 6.0]
    A_hf_rms_MHz    = float(np.sqrt(np.mean(np.array(A_couplings_MHz)**2)))
    tau_Z_s         = 1.0 / 30.0e6
    nu_star_Hz      = TAU_NATIVE_T2_S / (tau_Z_s ** 2)
    nu_star_MHz     = nu_star_Hz / 1.0e6
    sampling_ratio  = zeno_freq_MHz / nu_star_MHz
    in_bare_zeno    = sampling_ratio >= 1.0
    tau_meas_ns = 1.0e3 / zeno_freq_MHz
    quadratic_regime_limit_ns = tau_Z_s * tau_Z_s / TAU_NATIVE_T2_S * 1.0e9
    return {
        "A_hf_rms_MHz":             A_hf_rms_MHz,
        "tau_Z_ns":                 tau_Z_s * 1.0e9,
        "tau_Z_units":              "cyclic frequency convention, DeltaE/h",
        "anti_zeno_crossover_MHz":  nu_star_MHz,
        "bare_crossover_formula":   "nu_star = T2 / tau_Z^2",
        "zeno_drive_MHz":           zeno_freq_MHz,
        "sampling_ratio_to_crossover": sampling_ratio,
        "bare_channel_regime":      "standard_Zeno" if in_bare_zeno else "bare_anti_Zeno",
        "tau_meas_ns":              tau_meas_ns,
        "quadratic_regime_limit_ns": quadratic_regime_limit_ns,
        "regime_validity":          "outside_quadratic_regime" if tau_meas_ns > quadratic_regime_limit_ns else "inside_quadratic_regime",
        "in_zeno_regime":           in_bare_zeno,
        "protected_subspace_required": not in_bare_zeno,
        "o23_conditional_path": (
            "O.23 protected-subspace mechanism must supply Omega_DFS << omega_hf "
            "to lower the effective Hamiltonian variance before 100 MHz becomes "
            "a Zeno-regime drive."
        ),
        "pass":                     in_bare_zeno,
    }


def lindblad_collective_verification(N_spins_proxy=100):
    """
    Proxy Lindblad verification for conditional beta-Trp spin coherence.
    N_spins_proxy=100 simulates the n_rp=1 sensitivity branch by scaling;
    Ch13:633 makes the central cooperative branch n_rp=0 pending O.21.
    Hydration-shell OH/proton dipoles are bath/environment, not the
    cooperative oscillator basis.
    FULL_LATTICE_MODE=False: uses analytic Radical Pair Recombination result.
    """
    import numpy as np
    
    # Parameters from SSOT
    T2_s       = 10e-6          # 10 microseconds (Trp T2, model-derived extrapolation from cryptochrome FAD-Trp magnetoreception studies; direct beta-tubulin EPR pending O.24)
    gamma      = 1.0 / T2_s    # single-spin decoherence rate (Hz)
    g_s_Hz     = 931e3          # single-spin coupling (Hz)
    N_bio      = 1.25e8         # conditional beta-Trp n_rp=1 sensitivity branch per Ch13:633
    
    # Recombination Dissipator (The Non-Unitary Measurement)
    Gamma_rec_Hz = 100e6         # Recombination rate (100 MHz; acts as Zeno dissipator)
    tau_meas_s   = 1.0 / Gamma_rec_Hz

    # Hamiltonian-variance Zeno time (NOT T_2; per App X §X.12).
    # Hyperfine singlet-triplet manifold splitting Δ_ST/h = 30 MHz is reported
    # as cyclic frequency (DeltaE/h).
    Delta_ST_Hz = 30e6
    tau_Z_s     = 1.0 / Delta_ST_Hz

    # Bare Misra-Sudarshan effective time: τ_eff = τ_Z² / τ_meas
    tau_eff_s = (tau_Z_s ** 2) / tau_meas_s
    tau_eff_us = tau_eff_s * 1e6

    # Operative Selection-relevant target band per App X §X.2b: ~100 µs–1 ms
    # (covers individual action-potential coincidence windows on the 1–10 ms
    # neural firing timescale). The 10 ms value below is the structurally
    # conservative pass-gate that bounds the operative band from above; the
    # bare_pass = False verdict at canonical biological parameters holds
    # under either bound (bare τ_eff ≈ 110 ns sits 3–5 OOM short of either).
    # The protected-subspace closure (App H O.23 chiral phonon-polariton DFS)
    # is required to bridge to the operative band and is NOT computed here.
    bare_target_us  = 10_000.0   # 10 ms structurally conservative pass-gate (App X §X.2b operative band: 100 µs–1 ms)
    bare_pass       = tau_eff_us >= bare_target_us  # expected False at the bare level

    return {
        "T2_single_us":          T2_s * 1e6,
        "N_bio_spins":           N_bio,
        "N_bio_central_spins":   0.0,
        "N_bio_basis":           "conditional beta-Trp n_rp=1 sensitivity branch; central n_rp=0 pending O.21; hydration shell is bath/environment per Ch13:633",
        "Gamma_recombination_Hz": Gamma_rec_Hz,
        "Delta_ST_Hz":           Delta_ST_Hz,
        "Delta_ST_units":        "cyclic frequency Hz (DeltaE/h)",
        "tau_Z_ns":              tau_Z_s * 1e9,
        "tau_Z_units":           "cyclic frequency convention, tau_Z = 1/Delta_ST_Hz",
        "tau_meas_ns":           tau_meas_s * 1e9,
        "tau_effective_s":       tau_eff_s,
        "tau_effective_us":      tau_eff_us,
        "bare_target_us":        bare_target_us,
        "bare_misra_sudarshan_closes_target": bare_pass,
        "protected_subspace_closure_pending": "App H Open Problem O.23 (chiral phonon-polariton DFS)",
        "full_lattice_mode":     False,
        "pass":                  False,   # bare formula does NOT reach 10 ms; pending O.23
        "verdict":               "BARE_MS_EXTENSION_INSUFFICIENT — O.23 closure required"
    }


def run_decoherence_audit():
    import numpy as np
    print("=" * 65)
    print("GCT Protocol — Decoherence Audit: Quantum Coherence Viability in Neural Tissue")
    print("=" * 65)

    print(f"\n  Input constants:")
    print(f"  T_2 (Native)    = {TAU_NATIVE_T2_S:.2e} s  (Tubulin Trp T2)")
    print(f"  Recombination Rate Γ_rec = {GAMMA_REC_HZ / 1e6:.1f} MHz")
    print(f"  τ_recombination = {TAU_REC_S:.2e} s  (Sampling interval)")

    # ── 1. Timescale diagnostic, not closure ───────────────────────────────
    print(f"\n  ─── Diagnostic: recombination sampling vs T_2 (not closure) ───")
    print(f"  Diagnostic condition: τ_recombination ≪ T_2")
    
    ratio = TAU_NATIVE_T2_S / TAU_REC_S
    print(f"  T_2 / τ_recomb = {ratio:.1e}")

    pass_condition = TAU_REC_S < (TAU_NATIVE_T2_S / 100.0) # Require at least 2 OOM
    print(f"  Is τ_recomb small relative to T_2? {'YES ✓ (diagnostic only)' if pass_condition else 'NO ✗'}")

    if not pass_condition:
        print("\n  VERDICT: FAIL — timescale diagnostic fails; Zeno closure is not established.")
        sys.exit(1)

    # ── 2. Bare Misra-Sudarshan Zeno Coherence Extension ──────────────────
    # τ_Z is the Hamiltonian-variance Zeno time (Misra-Sudarshan 1977
    # J. Math. Phys. 18:756; Facchi-Pascazio 2008 J. Phys. A 41:493001),
    # NOT the exponential decoherence time T_2. Per App X §X.12 the
    # tubulin Trp radical-pair singlet-triplet manifold splitting is
    # Δ_ST/h = 30 MHz in cyclic frequency (DeltaE/h), giving
    # τ_Z = 1/Δ_ST ≈ 33 ns. The bare Misra-Sudarshan extension is then
    # τ_eff = τ_Z² / τ_meas ≈ (33 ns)² / 10 ns ≈ 110 ns — roughly five
    # orders of magnitude short of the 10 ms neurobiological target, and
    # roughly three orders short of a 100 µs lower operative benchmark. The remaining
    # gap is registered as App H Open Problem O.23 (chiral phonon-polariton
    # DFS); this protocol does NOT close it.
    print(f"\n  ─── Verification: Bare Misra-Sudarshan Zeno Extension ───")
    Delta_ST_Hz = 30.0e6
    tau_Z_s     = 1.0 / Delta_ST_Hz
    print(f"  τ_Z (variance time, Δ_ST = {Delta_ST_Hz/1e6:.1f} MHz cyclic) = {tau_Z_s*1e9:.1f} ns")
    print(f"  τ_meas (Γ_rec = 100 MHz) = {TAU_REC_S*1e9:.1f} ns")
    print(f"  Formula: τ_eff = τ_Z² / τ_meas  [NOT τ_eff = T_2² / τ_meas — that conflates"
          " decoherence with variance times, App X §X.12 / App X §X.12]")
    tau_eff_s = (tau_Z_s ** 2) / TAU_REC_S
    print(f"  Calculated bare τ_eff = {tau_eff_s*1e9:.1f} ns")

    bare_target_s = 10.0e-3
    pass_target   = tau_eff_s >= bare_target_s
    print(f"  Does bare τ_eff reach the 10 ms neurobiological target? {'YES ✓' if pass_target else 'NO ✗ (expected: bare extension is ~5 orders short of 10 ms and ~3 orders short of 100 µs)'}")
    print(f"  Remaining gap closure: App H Open Problem O.23 (chiral phonon-polariton DFS).")

    print(f"\n  ─── Verification: Anti-Zeno Crossover ───")
    az_results = anti_zeno_crossover(GAMMA_REC_HZ / 1e6)
    print(f"  Bare crossover ν* = T2/τ_Z²: {az_results['anti_zeno_crossover_MHz']:.2f} MHz")
    print(f"  100 MHz / ν*:               {az_results['sampling_ratio_to_crossover']:.4f}x")
    print(f"  Bare channel regime:         {az_results['bare_channel_regime']}")
    print(f"  Quadratic-regime limit:      tau_meas < {az_results['quadratic_regime_limit_ns']:.3f} ns")
    print(f"  Regime validity:             {az_results['regime_validity']}")
    print(f"  O.23 protected subspace required? {'YES' if az_results['protected_subspace_required'] else 'NO'}")

    # ── 3. Collective Misra-Sudarshan accounting ──────────────────────────
    # The lindblad_collective_verification() helper computes the bare
    # Misra-Sudarshan extension using the Hamiltonian-variance Zeno time
    # tau_Z = 1/Delta_ST in the cyclic-frequency convention (NOT T_2).
    # The bare extension does NOT reach the 10 ms target; the protected-subspace
    # closure (chiral phonon-polariton DFS) that would bridge the five-order gap is registered as App H
    # Open Problem O.23 and is NOT computed here.
    print(f"\n  ─── Bare Misra-Sudarshan Collective Accounting ───")
    lvl = lindblad_collective_verification()
    print(f"  N_bio spins              : {lvl['N_bio_spins']:.1e}")
    print(f"  Recombination rate Gamma_rec : {lvl['Gamma_recombination_Hz']:.2e} Hz")
    print(f"  Delta_ST (variance Zeno H)   : {lvl['Delta_ST_Hz']:.2e} Hz cyclic")
    print(f"  tau_Z = 1/Delta_ST             : {lvl['tau_Z_ns']:.1f} ns")
    print(f"  tau_meas = 1/Gamma_rec         : {lvl['tau_meas_ns']:.1f} ns")
    print(f"  tau_eff (bare MS)          : {lvl['tau_effective_us']:.3f} us")
    print(f"  Bare target reached?     : {'YES' if lvl['bare_misra_sudarshan_closes_target'] else 'NO (bare extension is about five orders short of 10 ms)'}")
    print(f"  Closure pending          : {lvl['protected_subspace_closure_pending']}")

    print()
    print(f"  VERDICT: BARE_MS_EXTENSION_INSUFFICIENT - the bare Misra-Sudarshan")
    print(f"    extension reaches tau_eff ~ {lvl['tau_effective_us']:.2f} us, about five orders below")
    print(f"    the 10 ms neurobiological target and about three orders below 100 us. Zeno Drive sampling at 100 MHz is")
    print(f"    below the bare Misra-Sudarshan crossover nu* ~ {az_results['anti_zeno_crossover_MHz']:.0f} MHz,")
    print(f"    so the bare radical-pair channel is anti-Zeno/inverse-Zeno. The")
    print(f"    protected-subspace closure required to lower the effective Hamiltonian")
    print(f"    variance bundles with App H Open Problem O.23 (chiral phonon-polariton")
    print(f"    DFS) and is not computed by this audit.")
    print("=" * 65)

    results = {
        "protocol":              "decoherence_audit",
        "T2_native_s":           TAU_NATIVE_T2_S,
        "Gamma_rec_hz":          GAMMA_REC_HZ,
        "tau_rec_s":             TAU_REC_S,
        "ratio_T2_to_taurec":    ratio,
        "Delta_ST_Hz":           lvl['Delta_ST_Hz'],
        "tau_Z_ns":              lvl['tau_Z_ns'],
        "tau_Z_units":           lvl.get("tau_Z_units"),
        "tau_eff_bare_us_extrapolated_outside_quadratic_regime": lvl['tau_effective_us'],
        "bare_tau_regime_validity": az_results["regime_validity"],
        "quadratic_regime_limit_ns": az_results["quadratic_regime_limit_ns"],
        "rate_channel_disambiguation": "Gamma_rec is the recombination-channel measurement linewidth used for bare Misra-Sudarshan decoherence balance; kappa_cav in protocol_eta_zeno.py is the Tavis-Cummings cavity-cooperativity linewidth. Different physical channels; not directly comparable.",
        "bare_target_us":        lvl['bare_target_us'],
        "bare_MS_closes_target": lvl['bare_misra_sudarshan_closes_target'],
        "protected_subspace_closure_pending": lvl['protected_subspace_closure_pending'],
        "verdict": "BARE_MS_EXTENSION_INSUFFICIENT - O.23 closure required",
        "pass": False,
        "anti_zeno_crossover_MHz": az_results["anti_zeno_crossover_MHz"],
        "anti_zeno_formula":        az_results["bare_crossover_formula"],
        "bare_sampling_ratio_to_crossover": az_results["sampling_ratio_to_crossover"],
        "bare_100MHz_channel_regime": az_results["bare_channel_regime"],
        "protected_subspace_required_for_zeno": az_results["protected_subspace_required"],
        "o23_conditional_path":      az_results["o23_conditional_path"],
    }
    out = get_output_path("protocol_decoherence_audit_results.json")

    with open(out, "w") as fp:
        json.dump(results, fp, indent=2)
    print(f"\n  Report saved → {out}")
    return results


if __name__ == "__main__":
    run_decoherence_audit()
