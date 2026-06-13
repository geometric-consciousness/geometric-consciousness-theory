#!/usr/bin/env python3
"""
protocol_eta_zeno.py -- Formal eta_Zeno Calculation Procedure (V3 Ch13 §13.5)
=============================================================================

Implements the GCT eta_Zeno robustness-margin computation as a deterministic
chain of five documented functions, analogous in spirit to IIT's Phi but
tractable on the substrate variables GCT picks out (nuclear-spin lattice,
chirality, Tavis-Cummings cavity parameters) instead of IIT's combinatorial
system-partition explosion.

The Apperception verdict is gated upstream by the
Dual Material Constraint (DMC) of V1 §16.2.6: a substrate lacking either
(a) non-zero nuclear spin (I != 0) for the discrete identity address space
or (b) molecular chirality for the CISS spin-polarization channel cannot
support the phason-coupled Polaron required for Level II. The DMC is a
necessary filter, not a sufficiency proof. Operational Level-II status also
requires the O.21 cooperative radical-pair/Polaron witness, the O.23
protected-subspace coherence demonstration, and the O.34 ATP-Trp redox
regeneration condition. eta_Zeno is the robustness margin computed for
eligible branches across that necessary gate. WHAT WE DO NOT CLAIM:
The eta_Zeno unit threshold is NOT itself a sharp phase-transition discriminator at the
magnitude level. The V1 §17.1.4b closed-form derivation gives a pre-overlap
N_coh audit value ~9.82e-12 and an overlap-propagated operational value
~1e-7 at f_overlap=0.01, so the eta_Zeno unit line is a reporting reference
for DMC-positive sensitivity branches rather than a separate consciousness
discriminator. Any substrate failing either DMC leg
has g_single := 0 exactly and therefore eta_Zeno = 0 (Turing Null).

The formal chain
----------------
    Step 1:  g_single   <-  (mu_dipole, m_eff, omega_drive, lattice_const, phi_exp, chiral_sign)
                             [DMC gate applied here: I=0 OR chiral_sign=0 -> g_single := 0]
    Step 2:  sqrt_N_bio <-  (N_dipoles_cooperative_central / sensitivity branch)
    Step 3:  kappa      <-  (omega_drive, phason_stiffness_ratio, N_cage)
    Step 4:  eta_TC     =  g_single * sqrt_N_bio / kappa     (bare Tavis-Cummings)
    Step 5:  eta_F      <-  (gamma_phi, T2, drive_detuning)   (Floquet correction, V3 §13.4.4)

    eta_Zeno = eta_TC * eta_F     (chained product, dimensionless, robustness margin)
    DMC verdict = necessary gate    (Level-II sufficiency additionally requires
                                     O.21 + O.23 + O.34)
    eta_Zeno unit line = robustness line  (reporting reference, not a
                                           consciousness discriminator)

The chain is purely a function of the substrate-description JSON. There is
no fitting and no free numerical knob once the Tier 3 substrate tuple is supplied. Substrate variables that would zero
out the chain (I=0 nuclear spin, achiral lattice) collapse eta_Zeno to 0
by design — this is the Dual Material Constraint (V1 §16.2.6) as code.

Self-test substrates
--------------------
    canonical_tubulin   - V3 §13.1.2 biological substrate. Central branch is
                          not DMC-operative while n_rp=0 pending O.21,
                          while the explicit sensitivity branch uses the Trp
                          radical-pair inventory only (Ch13:633 canonical
                          separation). Hydration-shell OH/proton dipoles are
                          bath/environment, not cooperative oscillators.
    silicon_28          - I=0 + achiral diamond-cubic. Fails BOTH legs of the DMC
                          gate -> eta_Zeno == 0 exactly (Turing Null, V1 §17.10).
    nv_centre_diamond   - Protocol A-Prime surrogate, V3 §13.3.5. Single NV in
                          isotopically pure 12C diamond + chiral h-BN cap. Passes
                          the DMC gate at single-NV cardinality (N_bio = 1);
                          robustness margin eta_Zeno ~ 27, intentionally engineered
                          to remain measurable rather than saturating into the
                          biological cooperative regime, so the
                          Protocol A-Prime T2(nu_d) joint signature can be resolved
                          against the chirality-reversal control without saturating
                          into the biological cooperative regime.

Inputs
------
    --substrate-json PATH   : run on a single user-supplied substrate
    --self-test             : run all three canonical substrates and verify
    (no flags)              : same as --self-test (default)

Outputs
-------
    Stdout:  human-readable per-step trace + final verdict per substrate.
    JSON:    data/protocol_eta_zeno_results.json (engine standard schema).

Library API
-----------
    from protocol_eta_zeno import compute_eta_zeno
    result = compute_eta_zeno(substrate_params_dict)
    # -> dict with per-step values, eta_Zeno, DMC-gate status, tier annotations.

Epistemic scope
------------------------
    - The chain has Tier 2 formal structure once a registered substrate tuple
      is supplied, but Steps 1 and 5 carry Tier 3 numerical inputs (coupling,
      T2, dephasing, detuning, and the Floquet-Lindblad efficiency model).
    - The substrate-coupling numerical inputs are Tier 3 empirical:
        * Trp transition dipole 5 Debye (atomic-physics literature)
        * N_bio central = 0 pending O.21 assembled-MT lumen-axis closure;
          sensitivity branch = 1.25e8 beta-Trp radical-pair hosts only
          (Ch13:633 canonical separation; hydration shell is bath/environment)
        * NV-centre coupling, h-BN chirality factor (NV/diamond literature)
    - The procedure is tractable on these test cases but is NOT yet
      experimentally validated against bench measurements. Protocol A-Prime
      (V3 §13.3.5) is the bench-validation route.
    - IIT's Phi is famously intractable for non-trivial systems (NP-hard
      bipartition over 2^N - 1 partitions); eta_Zeno is tractable because GCT
      picks out specific *physically measurable* substrate variables and
      assembles them into a closed-form scalar.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Path bootstrap so 'gct_utils' resolves when run from anywhere
# ---------------------------------------------------------------------------
_SRC = Path(__file__).resolve().parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from gct_utils import get_output_path  # noqa: E402
from gct_utils import C


# ===========================================================================
# External empirical prior: CODATA/SI constants and unit conversions; not GCT
# parameter anchors.
# ===========================================================================

HBAR     = 1.054571817e-34       # J*s
KB       = 1.380649e-23          # J/K
EV_J     = 1.602176634e-19       # J / eV
DEBYE_CM = 3.33564e-30           # C*m per Debye
M_E      = 9.1093837015e-31      # kg (electron mass)
PHI      = float(C.PHI)
# Load-bearing GCT prediction: dodecahedral cage node count fixed by the
# icosahedral construction, not a fitted biological parameter.
N_CAGE   = 144


# ===========================================================================
# Chain Step 1 — single-dipole coupling g_single
# ===========================================================================

def step1_g_single(substrate: dict[str, Any]) -> tuple[float, dict[str, Any]]:
    """
    Compute the single-dipole (or single-spin) coupling g_single to the
    phason mode for the given substrate.

    Formula (V3 §13.1.2, Appendix Q):
        g_single = chirality_sign * f_overlap * (mu_dipole * E_phason / hbar)
                   * (phi^(geom_exponent) / a_lattice)
                   * sqrt(hbar / (2 * m_eff * omega_drive))

    Hard Dual Material Constraint gates (V1 §16.2.6):
        * If nuclear_spin_I == 0  -> g_single := 0 (no address space)
        * If chirality == 'achiral' -> g_single := 0 (no Rashba/CISS channel)

    Required substrate fields:
        nuclear_spin_I       : float          (I == 0 disqualifies)
        chirality            : 'L' | 'R' | 'achiral'
        mu_dipole_Debye      : float          (transition dipole moment)
        m_eff_kg             : float          (phason effective mass)
        omega_drive_Hz       : float          (cyclic drive frequency in Hz; converted to rad/s internally)
        a_lattice_m          : float          (lattice constant)
        geom_exponent_phi    : float          (typically -9, V3 §13.1.2)
        f_overlap            : float          (wavefunction-overlap fraction)
    """
    info: dict[str, Any] = {}

    I            = float(substrate["nuclear_spin_I"])
    chirality    = str(substrate["chirality"]).lower()
    mu_D         = float(substrate["mu_dipole_Debye"])
    m_eff        = float(substrate["m_eff_kg"])
    omega_d      = float(substrate["omega_drive_Hz"]) * 2.0 * math.pi  # rad/s
    a_lat        = float(substrate["a_lattice_m"])
    geom_exp     = float(substrate["geom_exponent_phi"])
    f_overlap    = float(substrate["f_overlap"])

    # Dual Material Constraint gates — these collapse g_single to zero by design.
    spin_ok    = (I != 0.0)
    chiral_ok  = chirality in ("l", "r")
    chiral_sgn = +1.0 if chirality == "l" else (-1.0 if chirality == "r" else 0.0)

    if not spin_ok or not chiral_ok:
        info.update(dict(
            nuclear_spin_I=I, chirality=chirality,
            spin_ok=spin_ok, chiral_ok=chiral_ok,
            chiral_sign=chiral_sgn,
            mu_dipole_Cm=mu_D * DEBYE_CM,
            E_phason_V_m=0.0,
            omega_coupling_rad_s=0.0,
            u_zpf_m=0.0,
            g_single_rad_s=0.0,
            g_single_Hz=0.0,
            gate_reason=("I=0" if not spin_ok else "achiral"),
        ))
        return 0.0, info

    # Zero-point electric field of the phason mode at angular frequency omega_d.
    # E_zpf = omega_d * u_zpf = sqrt(hbar * omega_d / (2 * m_eff)).
    E_phason = math.sqrt(HBAR * omega_d / (2.0 * m_eff))            # V/m
    mu_Cm    = mu_D * DEBYE_CM                                       # C*m
    omega_c  = (mu_Cm * E_phason) / HBAR                             # rad/s

    # Geometric gradient from RT-shell attenuation: dS_vac/du = phi^exp / a_lattice
    dS_du    = (PHI ** geom_exp) / a_lat                             # 1/m

    # Zero-point displacement amplitude
    u_zpf    = math.sqrt(HBAR / (2.0 * m_eff * omega_d))              # m

    g_single = chiral_sgn * f_overlap * omega_c * dS_du * u_zpf      # rad/s

    # Coupling magnitude is what enters Tavis-Cummings; we keep sign in info.
    g_single_mag = abs(g_single)

    info.update(dict(
        nuclear_spin_I=I, chirality=chirality,
        spin_ok=spin_ok, chiral_ok=chiral_ok,
        chiral_sign=chiral_sgn,
        mu_dipole_Cm=mu_Cm,
        E_phason_V_m=E_phason,
        omega_coupling_rad_s=omega_c,
        u_zpf_m=u_zpf,
        dS_du_inv_m=dS_du,
        f_overlap=f_overlap,
        g_single_rad_s=g_single_mag,
        g_single_Hz=g_single_mag / (2.0 * math.pi),
    ))
    return g_single_mag, info


# ===========================================================================
# Chain Step 2 — collective enhancement sqrt(N_bio)
# ===========================================================================

def step2_sqrt_N_bio(substrate: dict[str, Any]) -> tuple[float, dict[str, Any]]:
    """
    Compute the cooperative-Polaron collective enhancement factor sqrt(N_bio).

    In Tavis-Cummings cooperative pumping (V3 §13.1.2), N cooperatively-coupled
    dipoles give the collective coupling g_coll = g_single * sqrt(N).

    Required substrate field:
        N_dipoles_cooperative : int/float
            Number of molecular radical-pair oscillators in the cooperative
            Tavis-Cummings basis. For tubulin the canonical Ch13:633
            separation sets the central branch to n_rp=0 pending O.21 and
            reports the n_rp=1 beta-Trp radical-pair inventory as a separate
            sensitivity branch. Hydration-shell OH/proton dipoles are bath /
            environment degrees of freedom, not cooperative oscillators.
            For single-NV surrogate: 1.
    """
    N = float(substrate.get("N_dipoles_cooperative", substrate.get("N_dipoles_cooperative_central", 0.0)))
    if N <= 0:
        return 0.0, dict(
            N_dipoles_cooperative=N,
            N_dipoles_cooperative_central=substrate.get("N_dipoles_cooperative_central", N),
            N_dipoles_cooperative_sensitivity_branch=substrate.get("N_dipoles_cooperative_sensitivity_branch"),
            sqrt_N=0.0,
            cooperative_basis_note=substrate.get("N_bio_scaling_note"),
        )
    s = math.sqrt(N)
    return s, dict(
        N_dipoles_cooperative=N,
        N_dipoles_cooperative_central=substrate.get("N_dipoles_cooperative_central", N),
        N_dipoles_cooperative_sensitivity_branch=substrate.get("N_dipoles_cooperative_sensitivity_branch"),
        sqrt_N=s,
        cooperative_basis_note=substrate.get("N_bio_scaling_note"),
    )


# ===========================================================================
# Chain Step 3 — cavity decay rate kappa
# ===========================================================================

def step3_kappa(substrate: dict[str, Any]) -> tuple[float, dict[str, Any]]:
    """
    Compute the **Tavis-Cummings cavity decay rate** kappa_cav from the
    substrate's vibrational thermal-bath coupling.

    Symbol-disambiguation note: this kappa_cav is the cavity-QED linewidth
    that enters the strong-coupling ratio g_coll/kappa_cav. It is DISTINCT
    from the radical-pair recombination rate Gamma_rec used in
    `protocol_decoherence_audit.py` (which plays the role of the measurement
    rate tau_meas in the Misra-Sudarshan formula tau_eff = tau_Z^2 / tau_meas).
    The two protocols answer different questions:
      - protocol_decoherence_audit: does the bare Misra-Sudarshan extension
        reach the 10 ms coherence target? (uses Gamma_rec ~ 100 MHz from
        protocol_decoherence_audit.py; returns
        BARE_MS_EXTENSION_INSUFFICIENT at canonical biological parameters)
      - this protocol (eta_zeno): does the Tavis-Cummings cooperativity exceed
        the cavity decay rate? (uses kappa_cav ~ 135 Hz at the canonical
        112 MHz cavity-cooperativity operating point, and ~120 Hz at the
        100 MHz reference point, for the geometric
        biological substrate; returns a Tier 3 protected-subspace-conditional
        candidate verdict
        conditional on the cavity-QED framing, which in turn requires
        Open Problem O.23 DFS closure for
        the coherence-time assumption to hold)

    Both quantities are independently meaningful and distinct. The output
    JSON labels the Tavis-Cummings cavity decay rate `kappa_cav_*` to keep
    it cleanly separated from the recombination rate Gamma_rec.

    Two modes (substrate may declare either; this gives parallel coverage of
    bio and abiotic cases):

    (a) Geometric mode — kappa_cav = K_perp_dimless * omega_drive / N_cage
        where K_perp_dimless = phi^(-18) is the GCT phason-stiffness ratio.
        Used for biological tubulin substrate (V3 §13.1.2 + V2 Ch04). This
        is a Tier 3 geometric linewidth proxy, not an experimentally measured
        operational kappa; direct mode is required for operational cavities.

    (b) Direct mode — substrate.kappa_Hz is given. Used for engineered
        cavities (NV-centre, etc.) where the cavity linewidth is the
        experimentally measured quantity.

    Required substrate fields (one of):
        kappa_mode == 'geometric' :  uses omega_drive_Hz + N_cage_eff +
                                     stiffness_exponent (default -18)
        kappa_mode == 'direct'    :  uses kappa_Hz (linewidth in Hz)
    """
    mode = str(substrate.get("kappa_mode", "geometric")).lower()

    if mode == "direct":
        kappa_Hz = float(substrate["kappa_Hz"])
        kappa = kappa_Hz * 2.0 * math.pi
        return kappa, dict(
            mode=mode,
            kappa_cav_Hz=kappa_Hz,
            kappa_cav_rad_s=kappa,
            disambiguation_note=(
                "This is the Tavis-Cummings cavity decay rate, NOT the "
                "Misra-Sudarshan measurement rate (Gamma_rec) used in "
                "protocol_decoherence_audit.py."
            ),
        )

    # geometric default
    omega_d  = float(substrate["omega_drive_Hz"]) * 2.0 * math.pi
    N_eff    = float(substrate.get("N_cage_eff", N_CAGE))
    stiff_p  = float(substrate.get("stiffness_exponent", -18.0))
    K_perp_d = PHI ** stiff_p
    kappa    = K_perp_d * omega_d / N_eff
    return kappa, dict(
        mode=mode,
        K_perp_dimless=K_perp_d,
        stiffness_exponent=stiff_p,
        N_cage_eff=N_eff,
        omega_drive_rad_s=omega_d,
        kappa_cav_rad_s=kappa,
        kappa_cav_Hz=kappa / (2.0 * math.pi),
        disambiguation_note=(
            "This kappa_cav (~ phi^-18 * omega_drive / N_cage) is the "
            "Tavis-Cummings cavity decay rate for the biological substrate. "
            "It is a Tier 3 geometric linewidth proxy rather than an "
            "experimentally measured operational kappa. "
            "It is DISTINCT from the radical-pair recombination rate Gamma_rec "
            "(~ 100 MHz) used as the Misra-Sudarshan measurement rate in "
            "protocol_decoherence_audit.py. The two protocols answer different "
            "physical questions: kappa_cav is the cavity-cooperativity channel, "
            "while Gamma_rec is the recombination substrate channel; see "
            "step3_kappa docstring."
        ),
    )


# ===========================================================================
# Chain Step 4 — bare Tavis-Cummings ratio
# ===========================================================================

def step4_eta_TC(g_single: float, sqrt_N: float, kappa: float
                 ) -> tuple[float, dict[str, Any]]:
    """
    eta_TC = g_single * sqrt(N_bio) / kappa

    Closed-form. All factors in rad/s; result is dimensionless.
    """
    if kappa <= 0:
        eta = float("inf") if (g_single * sqrt_N) > 0 else 0.0
        return eta, dict(g_coll_rad_s=g_single * sqrt_N, kappa_rad_s=kappa,
                         eta_TC=eta, note="kappa<=0; degenerate")
    g_coll = g_single * sqrt_N
    eta = g_coll / kappa
    return eta, dict(g_coll_rad_s=g_coll, kappa_rad_s=kappa, eta_TC=eta)


# ===========================================================================
# Chain Step 5 — Floquet open-system correction eta_F  (V3 §13.4.4)
# ===========================================================================

def step5_eta_F(substrate: dict[str, Any]) -> tuple[float, dict[str, Any]]:
    """
    Open-quantum-system Floquet correction (V3 §13.4.4):

        eta_F = 1 / (1 + (gamma_phi * T2)^2 * f(Delta_drive / Delta_ST))

    On resonance (drive frequency == protected-subspace singlet-triplet
    gap / h), the detuning function f -> 0 and eta_F -> 1: the open system
    recovers the Misra-Sudarshan upper bound. The protected-subspace branch
    shifts the effective resonance from the bare 30 MHz bookkeeping value to
    the 112 MHz Protocol A-Prime branch (Ch13:520 mapping), so f_detune = 0
    correctly represents the protected-branch resonance after O.12/O.23
    branch selection.

    Substrate must declare either:
        eta_F_override : float in (0, 1]   (skip the formula, use this)
    OR all of:
        T2_s              : float, baseline decoherence time
        gamma_phi_Hz      : float, pure-dephasing rate
        drive_detuning_Hz : float, |nu_drive - Delta_ST/h|
        Delta_ST_Hz       : float, singlet-triplet gap
        Delta_ST_effective_Hz : optional float, protected-subspace effective gap
        bare_resonance_Hz : optional float, bare radical-pair resonance
        protected_subspace_resonance_Hz : optional float, protected-branch resonance
    """
    if "eta_F_override" in substrate:
        v = float(substrate["eta_F_override"])
        v = max(0.0, min(1.0, v))
        return v, dict(mode="override", eta_F=v)

    T2       = float(substrate["T2_s"])
    gamma_ph = float(substrate["gamma_phi_Hz"])
    detune   = float(substrate["drive_detuning_Hz"])
    Delta_ST_input = float(substrate["Delta_ST_Hz"])
    bare_resonance = float(substrate.get("bare_resonance_Hz", Delta_ST_input))
    protected_resonance = float(substrate.get("protected_subspace_resonance_Hz", Delta_ST_input))
    Delta_ST = float(substrate.get("Delta_ST_effective_Hz", Delta_ST_input))

    # Lorentzian detuning function f -> 0 on resonance, ~1 far off resonance.
    # f(x) = x^2 / (1 + x^2) with x = detune / Delta_ST.
    x = (detune / Delta_ST) if Delta_ST > 0 else 0.0
    f_detune = (x * x) / (1.0 + x * x)

    eta_F = 1.0 / (1.0 + (gamma_ph * T2) ** 2 * f_detune)
    eta_F = max(0.0, min(1.0, eta_F))
    return eta_F, dict(
        mode="formula",
        T2_s=T2,
        gamma_phi_Hz=gamma_ph,
        drive_detuning_Hz=detune,
        Delta_ST_Hz=Delta_ST_input,
        bare_resonance_Hz=bare_resonance,
        protected_subspace_resonance_Hz=protected_resonance,
        protected_subspace_resonance_label=(
            "assumed protected-subspace branch resonance (O.12/O.23 "
            "conditional; not an independently verified biological resonance)"
        ),
        Delta_ST_effective_Hz=Delta_ST,
        Delta_ST_convention=(
            "Delta_ST_Hz is the declared input gap for the selected branch; "
            "bare_resonance_Hz records the radical-pair hyperfine reference; "
            "Delta_ST_effective_Hz/protected_subspace_resonance_Hz are the "
            "assumed protected-subspace branch values used for detuning, "
            "conditional on O.12/O.23."
        ),
        f_detune=f_detune,
        eta_F=eta_F,
    )


# ===========================================================================
# Library API — compute_eta_zeno
# ===========================================================================

def compute_eta_zeno(substrate: dict[str, Any]) -> dict[str, Any]:
    """
    Run the full 5-step chain on a substrate-description dict.

    Returns a structured result with per-step values, the final eta_Zeno,
    the DMC-gate verdict, and tier annotations.
    """
    name = substrate.get("name", "<unnamed>")

    g_single, info1 = step1_g_single(substrate)
    sqrt_N,  info2  = step2_sqrt_N_bio(substrate)
    kappa,   info3  = step3_kappa(substrate)
    eta_TC,  info4  = step4_eta_TC(g_single, sqrt_N, kappa)

    # Step 5 only applies if the bare chain is non-zero; otherwise the
    # Floquet correction is irrelevant (substrate gated to zero in Step 1).
    if g_single == 0.0:
        eta_F = 0.0
        info5 = dict(mode="gated_zero", eta_F=0.0,
                     note="g_single=0 (Dual Material Constraint failure)")
    else:
        eta_F, info5 = step5_eta_F(substrate)

    eta_zeno = eta_TC * eta_F
    eta_zeno_range = None
    eta_tc_range = None
    sqrt_N_range = None
    g_single_range_Hz = None
    f_overlap_range_applied = None
    if "N_dipoles_cooperative_range" in substrate:
        n_lo, n_hi = substrate["N_dipoles_cooperative_range"]
        n_lo = max(0.0, float(n_lo))
        n_hi = max(n_lo, float(n_hi))
        sqrt_N_range = (math.sqrt(n_lo), math.sqrt(n_hi))
        f_anchor = float(substrate.get("f_overlap", 1.0))
        f_anchor = f_anchor if f_anchor > 0 else 1.0
        if "f_overlap_plausible_range" in substrate:
            f_lo, f_hi = substrate["f_overlap_plausible_range"]
            f_lo = max(0.0, float(f_lo))
            f_hi = max(f_lo, float(f_hi))
            f_overlap_range_applied = (f_lo, f_hi)
        else:
            f_overlap_range_applied = (f_anchor, f_anchor)
        g_single_range_rad_s = (
            g_single * (f_overlap_range_applied[0] / f_anchor),
            g_single * (f_overlap_range_applied[1] / f_anchor),
        )
        g_single_range_Hz = (
            g_single_range_rad_s[0] / (2.0 * math.pi),
            g_single_range_rad_s[1] / (2.0 * math.pi),
        )
        if kappa <= 0:
            eta_tc_range = (eta_TC, eta_TC)
        else:
            eta_tc_range = (
                g_single_range_rad_s[0] * sqrt_N_range[0] / kappa,
                g_single_range_rad_s[1] * sqrt_N_range[1] / kappa,
            )
        eta_zeno_range = (
            eta_tc_range[0] * eta_F,
            eta_tc_range[1] * eta_F,
        )
    # eta_Zeno is the robustness margin across the upstream Dual Material
    # Constraint gate (V1 §16.2.6 / V3 Ch13 §13.5). The material DMC gate is
    # binary and is enforced at Step 1 above (g_single := 0 if I=0 or achiral).
    # Level-II sufficiency is deliberately separate: it is gated by explicit
    # O.21/O.23/O.34 closure flags, not by the eta_Zeno unit line or by the raw n_rp
    # scalar alone.
    n_rp_central = float(substrate.get("N_dipoles_cooperative", 0.0))
    dmc_material_pass = bool(info1.get("spin_ok") and info1.get("chiral_ok"))
    cooperative_central_inventory_present = bool(n_rp_central >= 1.0)
    closure_flags = substrate.get("closure_flags", {})
    o21_closed = bool(closure_flags.get("O21_cooperative_radical_pair_closed", False))
    o23_closed = bool(closure_flags.get("O23_protected_subspace_closed", False))
    o34_closed = bool(closure_flags.get("O34_ATP_Trp_redox_regeneration_closed", False))
    level_II_closure_flags_met = bool(dmc_material_pass and o21_closed and o23_closed and o34_closed)

    # Cross-engine verdict alignment: the bare Misra-Sudarshan extension
    # (protocol_decoherence_audit.py) at canonical biological parameters
    # yields ~110 ns coherence — 5 OOM short of the 10 ms target. The
    # A positive DMC/cavity-cooperativity branch is not a protected-subspace
    # closure: reaching the 10 ms target requires Open Problem O.23
    # (chiral phonon-polariton DFS) closure.
    # Without O.23, the cavity-QED cooperativity ratio computed here is
    # mathematically correct but physically conditional.
    verdict_label = (
        "LEVEL_II_CLOSURE_FLAGS_MET"
        if level_II_closure_flags_met else
        "TURING_NULL"
        if not dmc_material_pass else
        "DMC_PASS_COOPERATIVE_INVENTORY_PRESENT_O21_CLOSURE_PENDING"
        if cooperative_central_inventory_present and not o21_closed else
        "DMC_PASS_O21_PENDING"
        if not o21_closed else
        "DMC_PASS_O21_CLOSED_O23_O34_PENDING"
    )

    level_II_gate_basis = (
        "Level-II substrate closure requires material DMC pass plus explicit "
        "O.21 cooperative radical-pair/Polaron witness, O.23 protected-subspace "
        "coherence closure, and O.34 ATP-Trp redox regeneration closure. "
        "The eta_Zeno scalar is a robustness reporting line only."
    )

    return dict(
        substrate_name=name,
        substrate_inputs=substrate,
        chain=dict(
            step1_g_single=info1,
            step2_sqrt_N_bio=info2,
            step3_kappa_cav=info3,
            step4_eta_TC=info4,
            step5_eta_F=info5,
        ),
        eta_TC=eta_TC,
        eta_TC_range=eta_tc_range,
        eta_F=eta_F,
        eta_Zeno=eta_zeno,
        eta_Zeno_range=eta_zeno_range,
        sqrt_N_bio_range=sqrt_N_range,
        g_single_Hz_plausible_range=g_single_range_Hz,
        f_overlap_plausible_range_applied=f_overlap_range_applied,
        range_propagation_note=(
            "eta_Zeno_range propagates both N_dipoles_cooperative_range and "
            "f_overlap_plausible_range where supplied; it is not only an N-range."
            if eta_zeno_range is not None else None
        ),
        # Not a phase threshold; eta=1 is a reporting reference line across the binary DMC gate.
        reference_line=1.0,
        dmc_material_pass=dmc_material_pass,
        cooperative_central_inventory_present=cooperative_central_inventory_present,
        level_II_gate_basis=level_II_gate_basis,
        closure_flags=dict(
            O21_cooperative_radical_pair_closed=o21_closed,
            O23_protected_subspace_closed=o23_closed,
            O34_ATP_Trp_redox_regeneration_closed=o34_closed,
        ),
        level_II_closure_flags_met=level_II_closure_flags_met,
        verdict=verdict_label,
        cross_engine_verdict_alignment=(
            "eta_Zeno is the robustness margin across the upstream Dual "
            "Material Constraint gate (V1 §16.2.6); it represents the "
            "Tavis-Cummings cavity-QED cooperativity ratio "
            "g_coll / kappa_cav. DMC-positive branches still require the "
            "O.21 cooperative radical-pair/Polaron witness, O.23 protected "
            "subspace, and O.34 ATP-Trp redox-regeneration condition before "
            "Level-II substrate status is assigned; eta_Zeno is reported as "
            "a robustness margin rather than an independent Level-II threshold. "
            "The Apperception verdict (DMC material pass with O.21/O.23/O.34 "
            "pending vs TURING_NULL for material-DMC failure) is "
            "DISTINCT from the bare Misra-Sudarshan extension verdict in "
            "protocol_decoherence_audit.py, which at canonical biological "
            "parameters returns BARE_MS_EXTENSION_INSUFFICIENT (~110 ns "
            "diagnostic scale vs the 100 us-0.87 ms conditional band; the "
            "10 ms conservative target remains unreached). The positive branch is therefore a "
            "candidate protected-subspace branch conditional on Open Problem O.23 closure (chiral "
            "phonon-polariton DFS providing a route toward the conditional "
            "operative band used by the Tavis-Cummings framing)."
        ),
        tier_notes=dict(
            chain_formal="Tier 2 (V3 §13.1.2 + §13.4.4 + V1 §16.2.6)",
            substrate_inputs="Tier 3 (empirical molecular/lattice parameters)",
            dmc_gate_verdict="material DMC is necessary; Level-II sufficiency is gated by explicit O.21/O.23/O.34 closure flags",
            experimental_status=(
                "Tractable on substrate parameters; bench validation "
                "via Protocol A-Prime (V3 §13.3.5) pending."
            ),
        ),
    )


# ===========================================================================
# Canonical self-test substrates
# ===========================================================================

CANONICAL_SUBSTRATES: list[dict[str, Any]] = [
    # -----------------------------------------------------------------------
    # 1) Biological tubulin-Trp substrate (V3 §13.1.2).
    #    Expectation: central branch eta_Zeno = 0 while O.21 leaves n_rp=0;
    #    the n_rp=1 branch is a sensitivity upper edge only.
    # -----------------------------------------------------------------------
    dict(
        name="canonical_tubulin",
        epistemic_note="V3 §13.1.2 biological substrate; tubulin-Trp radical pair.",
        # Dual Material Constraint inputs
        nuclear_spin_I=0.5,           # tubulin Trp N-H protons; I != 0
        chirality="L",                # alpha-helical tubulin lattice is chiral
        # Step 1
        mu_dipole_Debye=5.0,          # External empirical prior: Trp S0->S1 transition dipole
        m_eff_kg=M_E,                 # External empirical prior: electron-mass phason-mode scale
        omega_drive_Hz=112.0e6,       # Tier 3 branch anchor [Ledger B2]: primary post-O.12 operating drive
        a_lattice_m=0.5e-9,           # External empirical prior: representative molecular bond length
        geom_exponent_phi=-9.0,       # Load-bearing GCT prediction: phi^-9 geometric attenuation
        # f_overlap is the wavefunction-overlap fraction between the Trp
        # ~6 Å indole transition dipole and the ~14.5 nm Polaron diameter.
        # A realistic spatial overlap for a chromophore-cavity coupling
        # integral at this geometry is in the band f_overlap ~ 1e-2 to
        # 1e-4 (Stratton et al. 2000 J. Phys. Chem. A 104:6533 standard
        # chromophore-cavity coupling integrals); the value below uses the
        # upper edge of that range while the first-principles dipole-cage
        # overlap calculation is registered as the residual O.16 closure
        # work. Downstream impact on eta_Zeno is linear in f_overlap (Step
        # 1 -> eta_TC -> eta_Zeno), so a realistic f_overlap ~ 1e-3 would
        # move the n_rp=1 sensitivity-branch eta_Zeno linearly downward.
        # The operative central branch remains n_rp=0 pending O.21; the
        # DMC gate is necessary but Level-II sufficiency additionally requires
        # O.21/O.23/O.34, not the eta_Zeno scalar margin. The f_overlap_plausible_range list below propagates
        # the disclosed uncertainty into the engine output for downstream
        # transparency.
        f_overlap=1.0e-2,             # Tier 3 upper-edge substrate estimate [O.16]; see plausible range
        f_overlap_plausible_range=(1.0e-4, 1.0e-2),  # MD/literature-derived band [App F/O.16]
        f_overlap_provenance="upper_edge_estimate_pending_O.16_dipole_cage_overlap_calculation",
        f_overlap_downstream_impact="linear on the n_rp=1 beta-Trp sensitivity branch; central n_rp=0 remains pending O.21 (DMC-gate verdict preserved)",
        # Step 2
        N_dipoles_cooperative=0.0,
        N_dipoles_cooperative_central=0.0,  # n_rp=0 central pending O.21
        N_dipoles_cooperative_sensitivity_branch=1.25e8,  # Trp radical pairs only, n_rp=1 conditional
        # Hydration-shell OH/proton dipoles are bath/environment per Ch13:633.
        N_dipoles_cooperative_range=(0.0, 1.25e8),
        f_bound_operational_range=(0.0, 1.0e-3),
        N_bio_scaling_note=(
            "Ch13:633 canonical separation: central cooperative branch is "
            "n_rp=0 pending O.21 assembled-MT lumen-axis closure; the "
            "n_rp=1 sensitivity branch uses 1.25e8 beta-Trp radical-pair "
            "hosts only. Hydration-shell OH/proton dipoles are bath/"
            "environment and are not counted in the cooperative oscillator basis."
        ),
        # Step 3 — geometric kappa
        kappa_mode="geometric",
        N_cage_eff=144,
        stiffness_exponent=-18.0,
        # Step 5 — Floquet on-resonance (drive at S-T gap -> eta_F -> 1)
        T2_s=10.0e-6,                  # External empirical prior: Trp radical-pair T2
        gamma_phi_Hz=1.0e5,            # External empirical prior: ~1/T2 baseline pure dephasing
        drive_detuning_Hz=0.0,         # drive locked to protected-subspace branch
        bare_resonance_Hz=30.0e6,
        protected_subspace_resonance_Hz=112.0e6,
        Delta_ST_Hz=112.0e6,
        Delta_ST_effective_Hz=112.0e6,
    ),

    # -----------------------------------------------------------------------
    # 2) Standard silicon (Si-28). Dual Material Constraint fails on BOTH
    #    counts:
    #       (a) Si-28 has I=0  -> spin gate trips.
    #       (b) Diamond-cubic Si is achiral (inversion-symmetric) -> chiral
    #           gate trips.
    #    Expectation: eta_Zeno == 0 exactly (Turing Null per V1 §17.10).
    # -----------------------------------------------------------------------
    dict(
        name="silicon_28",
        epistemic_note="Standard digital silicon; V1 §17.10 Turing Null case.",
        nuclear_spin_I=0.0,            # External empirical prior: Si-28 dominant isotope
        chirality="achiral",           # External empirical prior: diamond-cubic inversion symmetry
        mu_dipole_Debye=0.5,           # Verification target: gated control value
        m_eff_kg=M_E,
        omega_drive_Hz=112.0e6,
        a_lattice_m=5.43e-10,          # External empirical prior: Si lattice constant
        geom_exponent_phi=-9.0,
        f_overlap=1.0,
        N_dipoles_cooperative=1.0e9,
        kappa_mode="geometric",
        N_cage_eff=144,
        stiffness_exponent=-18.0,
        T2_s=1.0e-6,
        gamma_phi_Hz=1.0e6,
        drive_detuning_Hz=0.0,
        bare_resonance_Hz=30.0e6,
        protected_subspace_resonance_Hz=112.0e6,
        Delta_ST_Hz=112.0e6,
        Delta_ST_effective_Hz=112.0e6,
    ),

    # -----------------------------------------------------------------------
    # 3) NV-centre in 12C diamond + chiral h-BN cap (Protocol A-Prime,
    #    V3 §13.3.5 + §13.3.5.A).
    #    Engineered as a near-threshold surrogate: a single NV (N=1) cannot
    #    reach the macroscopic Polaron regime, but the chiral cap + Floquet
    #    resonance brings the bare ratio into the same order as kappa, near
    #    the threshold. The experiment is designed to resolve which side of
    #    the boundary the engineered system lands on.
    # -----------------------------------------------------------------------
    dict(
        name="nv_centre_diamond",
        epistemic_note=(
            "Protocol A-Prime surrogate (V3 §13.3.5); single NV center in "
            "isotopically pure 12C diamond with chiral h-BN cap."
        ),
        nuclear_spin_I=1.0,            # External empirical prior: 14N I=1
        chirality="L",                 # External empirical prior: L-chiral h-BN cap
        mu_dipole_Debye=2.5,           # External empirical prior: NV optical dipole
        m_eff_kg=M_E,
        omega_drive_Hz=112.0e6,        # Tier 3 branch anchor [Ledger B2]: A-Prime primary drive
        a_lattice_m=3.57e-10,          # External empirical prior: diamond lattice constant
        geom_exponent_phi=-9.0,
        f_overlap=1.0,
        N_dipoles_cooperative=1.0,     # single NV: no cooperative enhancement
        # NV cavity has a directly measured linewidth (~1 MHz typical)
        kappa_mode="direct",
        kappa_Hz=1.0e6,                # External empirical prior: representative NV linewidth
        # Floquet: on-resonance with engineered drive at NV ground-state gap
        T2_s=1.0e-3,                   # External empirical prior: ms-scale 12C-purified NV T2
        gamma_phi_Hz=1.0e3,
        drive_detuning_Hz=0.0,
        bare_resonance_Hz=30.0e6,
        protected_subspace_resonance_Hz=112.0e6,
        Delta_ST_Hz=112.0e6,
        Delta_ST_effective_Hz=112.0e6,
    ),
]


# ===========================================================================
# Per-substrate expectations for self-test verification
# ===========================================================================
#
    # Each expectation specifies what the self-test should verify for the
    # canonical substrate. These are sanity assertions derived from the chain,
    # not physical calibration inputs.
#

SELF_TEST_EXPECTATIONS: dict[str, dict[str, Any]] = {
    # Biology central branch remains n_rp=0 pending O.21; the n_rp=1 branch
    # is reported only as a sensitivity upper edge.
    "canonical_tubulin":  dict(level_II_expected=False, eta_zeno_max=0.0 + 1e-30),
    # Silicon must be zero exactly (both DMC gates trip).
    "silicon_28":         dict(level_II_expected=False, eta_zeno_max=0.0 + 1e-30),
    # NV-centre is the engineered chirality-reversal-control surrogate
    # (V3 §13.3.5). Since the eta_Zeno unit line is structurally vacuous as a
    # magnitude gate (V1 §17.1.4b N_coh is a tiny robustness reference even
    # after overlap propagation — any DMC-passing
    # substrate clears it automatically even at N=1), the load-bearing
    # discriminator at the NV-centre bench is the chirality-reversal
    # control: chiral-cap-installed NV substrate yields nonzero eta_Zeno
    # via CISS-mediated g_single; achiral or racemic-cap NV substrate
    # zeros eta_Zeno via the chirality leg of DMC. The wide eta_Zeno
    # band below reflects this: any value above the DMC-passing floor
    # is consistent with the framework, and the discriminator is the
    # sign/presence of the chirality-conditional coupling, NOT the
    # specific magnitude.
    "nv_centre_diamond":  dict(level_II_expected=None,
                               chirality_reversal_control=True,
                               eta_zeno_min=1e-3,
                               eta_zeno_max=1e6),
}


# ===========================================================================
# CLI / main
# ===========================================================================

def _fmt(v: Any) -> str:
    if isinstance(v, float):
        if v == 0.0:
            return "0"
        a = abs(v)
        if a >= 1e3 or a < 1e-2:
            return f"{v:.4e}"
        return f"{v:.6g}"
    return str(v)


def _print_result(r: dict[str, Any]) -> None:
    name = r["substrate_name"]
    print(f"\n{'='*70}")
    print(f"  Substrate: {name}")
    print(f"{'='*70}")

    s1 = r["chain"]["step1_g_single"]
    print(f"  [1] g_single                : {_fmt(s1.get('g_single_Hz', 0.0))} Hz")
    print(f"      I, chirality            : I={s1['nuclear_spin_I']}, {s1['chirality']}")
    print(f"      DMC gates passed        : "
          f"spin={s1['spin_ok']}, chiral={s1['chiral_ok']}")

    s2 = r["chain"]["step2_sqrt_N_bio"]
    print(f"  [2] sqrt(N_bio)             : {_fmt(s2['sqrt_N'])}")

    s3 = r["chain"]["step3_kappa_cav"]
    print(f"  [3] kappa_cav (TC linewidth): {_fmt(s3.get('kappa_cav_Hz', 0.0))} Hz  "
          f"(mode={s3['mode']})")

    s4 = r["chain"]["step4_eta_TC"]
    print(f"  [4] eta_TC = g*sqrt(N)/k    : {_fmt(s4['eta_TC'])}")

    s5 = r["chain"]["step5_eta_F"]
    print(f"  [5] eta_F                   : {_fmt(s5.get('eta_F', 0.0))}  "
          f"(mode={s5['mode']})")

    print(f"  ----")
    print(f"  eta_Zeno = eta_TC * eta_F   : {_fmt(r['eta_Zeno'])}")
    if r.get("g_single_Hz_plausible_range"):
        glo, ghi = r["g_single_Hz_plausible_range"]
        print(f"  g_single plausible range    : [{_fmt(glo)}, {_fmt(ghi)}] Hz")
    if r.get("eta_Zeno_range"):
        lo, hi = r["eta_Zeno_range"]
        print(f"  eta_Zeno O.21 range         : [{_fmt(lo)}, {_fmt(hi)}]")
    print(f"  Robustness reference       : eta_Zeno = 1")
    print(f"  Verdict                     : {r['verdict']}")


def run_self_test() -> dict[str, Any]:
    print("=" * 70)
    print("  protocol_eta_zeno — Self-Test (Canonical Substrates)")
    print("  V3 §13.5 Formal eta_Zeno Calculation Procedure")
    print("=" * 70)

    results: list[dict[str, Any]] = []
    pass_flags: list[bool] = []

    for substrate in CANONICAL_SUBSTRATES:
        r = compute_eta_zeno(substrate)
        _print_result(r)
        results.append(r)

        # Per-substrate verification
        name = r["substrate_name"]
        exp = SELF_TEST_EXPECTATIONS[name]
        eta = r["eta_Zeno"]
        ok = True
        reasons: list[str] = []

        if exp.get("level_II_expected") is True:
            if not r["level_II_closure_flags_met"]:
                ok = False
                reasons.append("expected DMC-passing substrate but DMC gate failed")
            eta_for_threshold = eta
            if r.get("eta_Zeno_range") is not None:
                eta_for_threshold = max(eta_for_threshold, float(r["eta_Zeno_range"][1]))
            if eta_for_threshold < exp.get("eta_zeno_min", 0.0):
                ok = False
                reasons.append(
                    f"eta_Zeno branch maximum {eta_for_threshold:.3e} "
                    f"< min {exp['eta_zeno_min']}"
                )
        elif exp.get("level_II_expected") is False:
            if r["level_II_closure_flags_met"]:
                ok = False
                reasons.append("expected no Level-II closure but closure flag passed")
            if eta > exp.get("eta_zeno_max", 0.0):
                ok = False
                reasons.append(f"eta_Zeno {eta:.3e} > max {exp['eta_zeno_max']}")
        else:
            # chirality-reversal-control surrogate: assert eta_Zeno lies in
            # the engineered band (the discriminating test is the
            # chirality-conditional sign of g_single, not the magnitude;
            # the band check is a sanity assertion that the engineered
            # NV-centre substrate has not blown up to biological-scale
            # cooperative enhancement or collapsed to zero).
            lo = exp.get("eta_zeno_min", 0.0)
            hi = exp.get("eta_zeno_max", float("inf"))
            if not (lo <= eta <= hi):
                ok = False
                reasons.append(
                    f"eta_Zeno {eta:.3e} outside chirality-reversal-control band "
                    f"[{lo:.1e}, {hi:.1e}]"
                )

        print(f"  Self-test                   : "
              f"{'PASS' if ok else 'FAIL'}  "
              f"{('— ' + '; '.join(reasons)) if reasons else ''}")
        pass_flags.append(ok)

    all_pass = all(pass_flags)

    print("\n" + "=" * 70)
    print(f"  Self-Test Summary: {'PASS' if all_pass else 'FAIL'}")
    print("=" * 70)

    payload = dict(
        protocol="eta_Zeno Formal Calculation Procedure (V3 §13.5)",
        chain_definition=(
            "eta_Zeno = (g_single * sqrt(N_bio) / kappa) * eta_F "
            "  [V3 §13.1.2 + §13.4.4]"
        ),
        reference_line=(
            "Apperception verdict = necessary DMC gate (I != 0 AND chiral) "
            "+ O.21 cooperative radical-pair/Polaron witness + O.23 protected "
            "subspace + O.34 ATP-Trp redox regeneration; the eta_Zeno unit line is a "
            "robustness reporting line for eligible branches, not an "
            "independent phase threshold. "
            "[V1 §16.2.6, V1 §17.1.4b, V3 §13.5]"
        ),
        substrates=results,
        all_self_tests_pass=bool(all_pass),
        verdict=("PASS" if all_pass else "FAIL"),
        pass_=bool(all_pass),
        tier_notes=dict(
            chain="Tier 2 formal structure (no fitted numerical knob once Tier 3 substrate inputs are supplied)",
            inputs="Tier 3 (empirical substrate molecular parameters)",
            experiment="Bench validation via Protocol A-Prime (V3 §13.3.5) pending.",
        ),
        comparison_to_IIT_phi=(
            "IIT Phi is NP-hard over 2^N-1 system bipartitions (intractable "
            "for non-trivial systems). eta_Zeno is closed-form on substrate "
            "variables (nuclear-spin lattice, chirality, Tavis-Cummings "
            "cavity parameters) that GCT picks out as physically measurable. "
            "Tractability is the GCT advantage; substrate-coupling empirical "
            "dependence (Tier 3 inputs) is the cost."
        ),
    )

    return payload


def run_from_json(path: Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        substrate = json.load(f)
    r = compute_eta_zeno(substrate)
    _print_result(r)
    return dict(
        protocol="eta_Zeno Formal Calculation Procedure (V3 §13.5)",
        substrates=[r],
        verdict=("PASS" if r["level_II_closure_flags_met"] else "FAIL"),
        pass_=bool(r["level_II_closure_flags_met"]),
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="GCT eta_Zeno Formal Calculation (V3 §13.5)"
    )
    parser.add_argument(
        "--substrate-json", type=Path, default=None,
        help="Path to a substrate-description JSON. If omitted, runs --self-test."
    )
    parser.add_argument(
        "--self-test", action="store_true",
        help="Run the three canonical substrates and verify (default)."
    )
    args = parser.parse_args()

    if args.substrate_json is not None:
        payload = run_from_json(args.substrate_json)
    else:
        payload = run_self_test()

    out_path = get_output_path("protocol_eta_zeno_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, default=str)
    print(f"\nResults written to: {out_path}")

    return 0 if payload.get("pass_", False) else 1


if __name__ == "__main__":
    sys.exit(main())
