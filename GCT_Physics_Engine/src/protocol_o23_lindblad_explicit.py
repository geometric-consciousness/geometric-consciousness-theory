#!/usr/bin/env python3
"""
protocol_o23_lindblad_explicit.py

Explicit Tavis-Cummings + Lindblad master-equation solver for the
chiral phonon-polariton Decoherence-Free Subspace (DFS) suppression on
the alpha-helical microtubule lattice (V1 Ch17 sec 17.1.3c, App H Open
Problem O.23). Closure-path-(a) numerical companion to
`protocol_o23_dfs_collective_dressing.py` (which uses the analytic
sqrt(N) Tavis-Cummings collective-dressing argument).

Physical setup
==============

  H = (omega_0 / 2) sum_i sigma_z^(i)

Collapse operators (per-dimer dephasing) plus ONE collective collapse
operator representing the thermal bath coupling to either the symmetric
collective lowering mode (no DFS) or the chiral OAM-l=1 collective
lowering mode (DFS for the symmetric |W> state):

  C_deph_i  = sqrt(gamma_deph) sigma_z^(i)        per-dimer dephasing
  C_emit_i  = sqrt(gamma_emit) sigma_-^(i)        per-dimer radiative
                                                  emission (small)

  B_sym   = sqrt(gamma_th) * (1/sqrt(N)) * sum_i sigma_-^(i)
  B_chir  = sqrt(gamma_th) * (1/sqrt(N)) * sum_i exp(2*pi*i*i/N) sigma_-^(i)

The CORRECT canonical DFS algebra (Lidar 2014 *Quant. Inf. Process.*
13:1505 sec 2; Plenio-Knight 1998 *Rev. Mod. Phys.* 70:101): the
single-excitation symmetric collective state
  |W> = (1/sqrt(N)) sum_i sigma_+^(i) |g...g>
is the OAM-l=0 collective excitation. The chiral OAM-l=1 collective
lowering operator
  B_chir = (1/sqrt(N)) sum_i exp(2*pi*i*i/N) sigma_-^(i)
acts on |W> as
  <g...g| B_chir |W> = (1/N) sum_i exp(2*pi*i*i/N)
which is exactly zero for N >= 2 (geometric sum of N distinct N-th roots
of unity). Therefore |W> is a *dark state* of B_chir in the orthonormal-
OAM-basis limit, and the Lindblad coherence decay <W| rho |g> generated
by B_chir vanishes identically. By contrast, the symmetric collective
lowering operator B_sym annihilates |W> -> |g> with collective matrix
element
  <g...g| B_sym |W> = 1
giving super-radiant decay at collective rate gamma_th.

Structural-discipline notes
============================

  (1) CONTROL CONSTRUCTION. Both branches (`chiral_bath=True` and
      `chiral_bath=False`) construct a collective bath operator — the
      difference is the OAM phase pattern. The symmetric branch is NOT
      the absence of a bath; it is a collective bath with all OAM
      phases set to +1 (matching the canonical Tavis-Cummings symmetric-
      coupling control).

  (2) COLLAPSE-OPERATOR ALGEBRA. The collapse operators are sigma_-
      (lowering) operators per the canonical Tavis-Cummings dark-state
      argument, NOT sigma_z (dephasing). The chiral OAM-l=1 collective
      sigma_- operator annihilates the symmetric |W> state via
      geometric-sum-of-N-th-roots-of-unity cancellation; the symmetric
      OAM-l=0 collective sigma_- operator gives super-radiant decay.

  (3) PASS PREDICATE. The pass-criterion is strict monotonic-increasing
      DFS-ratio in N AND a minimum-DFS-ratio threshold at the largest
      tractable N — NOT a loose-tolerance monotonicity test that would
      permit decreasing ratio sequences.

Tier disposition: Tier 2 mechanism (Tavis-Cummings dark-state algebra
for collective lowering operators on the symmetric W state, under
chiral-OAM-vs-symmetric collective-coupling discrimination) + Tier 3
specific numerical magnitude (set by gamma_th / gamma_deph ratio).

Output: data/protocol_o23_lindblad_explicit_results.json
"""

from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

import numpy as np
from scipy.linalg import expm


# -----------------------------------------------------------------------------
# Physical parameters (calibrated for tractable demonstration; absolute
# magnitudes are not load-bearing — the canonical numerical magnitude is
# the chiral-vs-symmetric DFS-ratio, which is determined by the gamma_th
# coupling structure and is unit-independent up to the dimensionless
# gamma_th / gamma_deph ratio).
# -----------------------------------------------------------------------------

OMEGA_0 = 2.0 * math.pi * 50.0e6         # TLS frequency, rad/s
GAMMA_DEPH_PER_DIMER = 1.0e5             # per-dimer pure dephasing rate, Hz
                                          # (set well below GAMMA_TH so the
                                          # DFS suppression dominates)
GAMMA_TH = 1.0e7                          # thermal-bath collective coupling, Hz
GAMMA_EMIT = 1.0e3                        # per-dimer radiative emission, Hz
                                          # (small; not load-bearing)

# Scan range for N TLS (small-N tractable; full Hilbert dim = 2^N,
# squared for the Liouville-space matrix exponentiation per time step).
# N=2..5 is tractable on desktop in ~seconds per N.
N_TLS_SCAN = [2, 3, 4, 5]
DIRECT_LINDBLAD = os.environ.get("GCT_O23_DIRECT", "0") == "1"

REFERENCE_REGIMES = [
    {
        "N_TLS": 2,
        "Hilbert_dim": 4,
        "T2_chiral_OAM_l1_s": 1.9225223493223212e-07,
        "T2_symmetric_OAM_l0_s": 9.802480027447149e-08,
        "DFS_enhancement_ratio": 1.961261174661125,
    },
    {
        "N_TLS": 3,
        "Hilbert_dim": 8,
        "T2_chiral_OAM_l1_s": 1.4557806623802016e-07,
        "T2_symmetric_OAM_l0_s": 8.425191322048201e-08,
        "DFS_enhancement_ratio": 1.7278903311910725,
    },
    {
        "N_TLS": 4,
        "Hilbert_dim": 16,
        "T2_chiral_OAM_l1_s": 1.2981112481339658e-07,
        "T2_symmetric_OAM_l0_s": 7.871846341559784e-08,
        "DFS_enhancement_ratio": 1.6490556240669056,
    },
    {
        "N_TLS": 5,
        "Hilbert_dim": 32,
        "T2_chiral_OAM_l1_s": 1.218843317691513e-07,
        "T2_symmetric_OAM_l0_s": 7.573175811276458e-08,
        "DFS_enhancement_ratio": 1.6094216588457584,
    },
]

# Integration time and grid
T_FINAL_S = 1.0e-5                        # 10 microseconds (>> 1/GAMMA_TH)
N_TIME_STEPS = 20

# Pass criteria: replace loose monotonicity with strict
# monotonic-increasing AND minimum-DFS-ratio threshold at the largest
# tractable N.
PASS_MIN_DFS_RATIO_AT_LARGEST_N = 2.0     # at least 2x enhancement at the
                                          # largest tractable N (the strict
                                          # canonical dark-state limit is
                                          # infinity; finite gamma_emit +
                                          # gamma_deph give a finite ratio)


# -----------------------------------------------------------------------------
# Operator constructors
# -----------------------------------------------------------------------------

def sigma_z():
    return np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)


def sigma_plus():
    return np.array([[0.0, 1.0], [0.0, 0.0]], dtype=complex)


def sigma_minus():
    return sigma_plus().T


def kron_list(ops):
    out = ops[0]
    for op in ops[1:]:
        out = np.kron(out, op)
    return out


def lift_tls(op, i, N_TLS):
    """Embed single-TLS operator `op` at site i in the full Hilbert space
    of N_TLS two-level systems."""
    ops = []
    for j in range(N_TLS):
        ops.append(op if j == i else np.eye(2, dtype=complex))
    return kron_list(ops)


def collective_lowering(N_TLS, oam_l):
    """Construct the OAM-l collective lowering operator
    (1/sqrt(N)) sum_i exp(2*pi*i*l*i/N) sigma_-^(i).

    oam_l=0 -> symmetric collective bath (no DFS for |W>)
    oam_l=1 -> chiral OAM-l=1 collective bath (|W> dark state)
    """
    op = np.zeros((2 ** N_TLS, 2 ** N_TLS), dtype=complex)
    for i in range(N_TLS):
        phase = np.exp(2j * math.pi * oam_l * i / N_TLS)
        op = op + phase * lift_tls(sigma_minus(), i, N_TLS)
    return op / math.sqrt(N_TLS)


# -----------------------------------------------------------------------------
# Lindblad master-equation evolution (Liouville-space matrix exponential)
# -----------------------------------------------------------------------------

def build_hamiltonian(N_TLS):
    H = np.zeros((2 ** N_TLS, 2 ** N_TLS), dtype=complex)
    for i in range(N_TLS):
        H += 0.5 * OMEGA_0 * lift_tls(sigma_z(), i, N_TLS)
    return H


def build_collapse_operators(N_TLS, oam_l):
    """Per-dimer dephasing + per-dimer radiative emission + ONE collective
    OAM-l bath operator."""
    ops = []
    for i in range(N_TLS):
        ops.append(math.sqrt(GAMMA_DEPH_PER_DIMER) * lift_tls(sigma_z(), i, N_TLS))
        ops.append(math.sqrt(GAMMA_EMIT) * lift_tls(sigma_minus(), i, N_TLS))
    ops.append(math.sqrt(GAMMA_TH) * collective_lowering(N_TLS, oam_l))
    return ops


def lindbladian_matrix(H, C_ops):
    """Vectorise the Lindblad superoperator (column-stacked rho).

    L[rho] = -i[H, rho] + sum_k (C_k rho C_k^dag
                                  - 0.5 * {C_k^dag C_k, rho})

    In column-stacked vec(rho) convention:
      vec(A rho B) = (B^T kron A) vec(rho)

    So:
      vec([H, rho]) = (I kron H - H^T kron I) vec(rho)
      vec(C rho C^dag) = (C^* kron C) vec(rho)   [since C^dag = (C^*)^T]
      vec(C^dag C rho) = (I kron C^dag C) vec(rho)
      vec(rho C^dag C) = ((C^dag C)^T kron I) vec(rho)
    """
    dim = H.shape[0]
    I = np.eye(dim, dtype=complex)
    L = -1j * (np.kron(I, H) - np.kron(H.T, I))
    for C in C_ops:
        C_dag = C.conj().T
        CdC = C_dag @ C
        L += np.kron(C.conj(), C)
        L -= 0.5 * (np.kron(I, CdC) + np.kron(CdC.T, I))
    return L


def evolve_W_to_g_coherence(N_TLS, t_final, n_steps, oam_l):
    """Initialise the system in the (|W> + |g...g>)/sqrt(2) superposition
    and evolve via the Lindblad master equation. Return the |W>-|g...g>
    coherence |<W|rho|g...g>| as a function of time."""
    H = build_hamiltonian(N_TLS)
    C_ops = build_collapse_operators(N_TLS, oam_l)
    L = lindbladian_matrix(H, C_ops)

    dim = 2 ** N_TLS
    # |W> = (1/sqrt(N)) sum_i |g..e_i..g>
    psi_W = np.zeros(dim, dtype=complex)
    g_state = np.array([1.0, 0.0], dtype=complex)
    e_state = np.array([0.0, 1.0], dtype=complex)
    for i in range(N_TLS):
        psi_i = None
        for j in range(N_TLS):
            v = e_state if j == i else g_state
            psi_i = v if psi_i is None else np.kron(psi_i, v)
        psi_W += psi_i / math.sqrt(N_TLS)

    # |g...g>
    psi_g = None
    for _ in range(N_TLS):
        psi_g = g_state if psi_g is None else np.kron(psi_g, g_state)

    # rho_0 = |psi_0><psi_0| with psi_0 = (|W> + |g>)/sqrt(2)
    psi_0 = (psi_W + psi_g) / math.sqrt(2)
    rho_0 = np.outer(psi_0, psi_0.conj())
    # Column-stacked vec(rho)
    rho_0_vec = rho_0.flatten("F")

    times = np.linspace(0.0, t_final, n_steps)
    coherences = []
    for t in times:
        rho_t_vec = expm(L * t) @ rho_0_vec
        rho_t = rho_t_vec.reshape((dim, dim), order="F")
        coh = abs(psi_W.conj() @ rho_t @ psi_g)
        coherences.append(coh)
    return times, np.array(coherences)


def extract_T2(times, coherences):
    """Fit single-exponential decay |coh(t)| = C_0 exp(-t / T_2). Return
    T_2 in seconds; +inf if no decay detected."""
    mask = coherences > 1e-14
    if mask.sum() < 5:
        return float("nan")
    t_fit = times[mask]
    log_coh = np.log(coherences[mask])
    p = np.polyfit(t_fit, log_coh, 1)
    slope = p[0]
    if slope >= -1e-3:
        return float("inf")
    return -1.0 / slope


def run():
    results = {
        "tier": "Tier 2 mechanism (Tavis-Cummings dark-state algebra: chiral OAM-l=1 collective sigma_- bath annihilates the symmetric |W> via geometric-sum-of-N-th-roots-of-unity cancellation; symmetric OAM-l=0 collective sigma_- bath gives super-radiant decay of |W>) + Tier 3 specific numerical magnitude (set by gamma_th / gamma_deph ratio).",
        "model": "H = (omega_0/2) sum_i sigma_z^(i); per-dimer sigma_z dephasing + per-dimer sigma_- emission + ONE collective OAM-l bath = sqrt(gamma_th) * (1/sqrt(N)) * sum_i exp(2*pi*i*l*i/N) sigma_-^(i)",
        "inputs": {
            "OMEGA_0_rad_per_s": OMEGA_0,
            "GAMMA_DEPH_PER_DIMER_Hz": GAMMA_DEPH_PER_DIMER,
            "GAMMA_TH_Hz": GAMMA_TH,
            "GAMMA_EMIT_Hz": GAMMA_EMIT,
            "N_TLS_scan": N_TLS_SCAN,
            "t_final_s": T_FINAL_S,
            "n_time_steps": N_TIME_STEPS,
            "PASS_MIN_DFS_RATIO_AT_LARGEST_N": PASS_MIN_DFS_RATIO_AT_LARGEST_N,
        },
        "regimes": [],
    }

    if not DIRECT_LINDBLAD:
        results["regimes"] = [dict(r) for r in REFERENCE_REGIMES]
        valid_ratios = [r["DFS_enhancement_ratio"] for r in results["regimes"]]
        largest_N_ratio = valid_ratios[-1]
        results["DFS_ratio_monotonic_strict_in_N"] = False
        results["DFS_ratio_at_largest_N"] = largest_N_ratio
        results["DFS_magnitude_threshold_pass"] = False
        results["PASS_criterion"] = (
            f"strict monotonic-increasing DFS ratio in N AND "
            f"DFS ratio at largest N (N={N_TLS_SCAN[-1]}) >= {PASS_MIN_DFS_RATIO_AT_LARGEST_N}"
        )
        results["verdict_status"] = "DFS_SUPPRESSION_NOT_DEMONSTRATED"
        results["verdict"] = (
            f"DFS enhancement ratio sequence: {[f'{r:.3g}' for r in valid_ratios]}. "
            f"Strict monotonic-increasing: False. Magnitude at largest N: "
            f"{largest_N_ratio:.3g} (threshold: {PASS_MIN_DFS_RATIO_AT_LARGEST_N}x). "
            "Fast verification mode uses the canonical direct-Lindblad reference output; "
            "set GCT_O23_DIRECT=1 for the expensive Liouville-space matrix-exponential run."
        )
        results["pass"] = False
        out_dir = Path(__file__).parent.parent / "data"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "protocol_o23_lindblad_explicit_results.json"
        with open(out_path, "w") as f:
            json.dump(results, f, indent=4)
        print(f"Fast verification reference written to {out_path}")
        return results

    for N_TLS in N_TLS_SCAN:
        # Chiral OAM-l=1 bath: |W> dark state
        t_chi, coh_chi = evolve_W_to_g_coherence(N_TLS, T_FINAL_S, N_TIME_STEPS, oam_l=1)
        T2_chi = extract_T2(t_chi, coh_chi)
        # Symmetric OAM-l=0 bath: |W> super-radiantly decays
        t_sym, coh_sym = evolve_W_to_g_coherence(N_TLS, T_FINAL_S, N_TIME_STEPS, oam_l=0)
        T2_sym = extract_T2(t_sym, coh_sym)

        if math.isfinite(T2_chi) and math.isfinite(T2_sym) and T2_sym > 0:
            ratio = T2_chi / T2_sym
        elif math.isinf(T2_chi):
            ratio = float("inf")
        else:
            ratio = float("nan")

        results["regimes"].append({
            "N_TLS": N_TLS,
            "Hilbert_dim": 2 ** N_TLS,
            "T2_chiral_OAM_l1_s": T2_chi,
            "T2_symmetric_OAM_l0_s": T2_sym,
            "DFS_enhancement_ratio": ratio,
        })

    # STRICT monotonic-increasing predicate (no slack).
    valid_ratios = [
        r["DFS_enhancement_ratio"]
        for r in results["regimes"]
        if math.isfinite(r["DFS_enhancement_ratio"]) or math.isinf(r["DFS_enhancement_ratio"])
    ]

    monotonic_strict = all(
        valid_ratios[i] < valid_ratios[i + 1] or
        (math.isinf(valid_ratios[i + 1]) and math.isfinite(valid_ratios[i]))
        for i in range(len(valid_ratios) - 1)
    ) if len(valid_ratios) >= 2 else False

    # DFS-magnitude threshold at largest N
    largest_N_ratio = valid_ratios[-1] if valid_ratios else float("nan")
    magnitude_pass = (
        math.isinf(largest_N_ratio)
        or (math.isfinite(largest_N_ratio) and largest_N_ratio >= PASS_MIN_DFS_RATIO_AT_LARGEST_N)
    )

    results["DFS_ratio_monotonic_strict_in_N"] = monotonic_strict
    results["DFS_ratio_at_largest_N"] = largest_N_ratio
    results["DFS_magnitude_threshold_pass"] = magnitude_pass
    results["PASS_criterion"] = (
        f"strict monotonic-increasing DFS ratio in N AND "
        f"DFS ratio at largest N (N={N_TLS_SCAN[-1]}) >= {PASS_MIN_DFS_RATIO_AT_LARGEST_N}"
    )

    if monotonic_strict and magnitude_pass:
        results["verdict_status"] = "DFS_SUPPRESSION_CONFIRMED_BY_LINDBLAD_MASTER_EQUATION"
        results["verdict"] = (
            f"Explicit Lindblad master-equation solution for the symmetric |W> "
            f"collective excitation under a chiral OAM-l=1 collective sigma_- bath "
            f"vs symmetric OAM-l=0 collective sigma_- bath: the chiral-OAM bath "
            f"gives strictly larger T_2 than the symmetric bath across the N={N_TLS_SCAN} "
            f"scan, with DFS enhancement ratio strictly monotonic-increasing in N "
            f"(observed sequence: {[f'{r:.3g}' for r in valid_ratios]}). The DFS ratio "
            f"at the largest tractable N (N={N_TLS_SCAN[-1]}) is {largest_N_ratio:.3g}, "
            f">= the {PASS_MIN_DFS_RATIO_AT_LARGEST_N}x threshold. The result is "
            f"consistent with the analytic Tavis-Cummings dark-state argument used "
            f"by the companion protocol_o23_dfs_collective_dressing.py: in the "
            f"orthonormal-OAM-basis limit, the chiral OAM-l=1 collective sigma_- "
            f"operator annihilates |W> exactly (geometric sum of N-th roots of "
            f"unity vanishes for N>=2), realising a Decoherence-Free Subspace for "
            f"the symmetric W collective excitation. The residual finite T_2(chiral) "
            f"comes from per-dimer dephasing and emission channels (sigma_z + "
            f"sigma_- on individual sites) that are not OAM-symmetric and therefore "
            f"do leak the |W> coherence at small rate."
        )
    else:
        results["verdict_status"] = "DFS_SUPPRESSION_NOT_DEMONSTRATED"
        results["verdict"] = (
            f"DFS enhancement ratio sequence: {[f'{r:.3g}' for r in valid_ratios]}. "
            f"Strict monotonic-increasing: {monotonic_strict}. Magnitude at largest N: "
            f"{largest_N_ratio:.3g} (threshold: {PASS_MIN_DFS_RATIO_AT_LARGEST_N}x). "
            f"At least one of the two PASS criteria failed; the chiral OAM bath does "
            f"not show the expected dark-state DFS protection of the symmetric |W> "
            f"state at the tested parameter values."
        )

    results["pass"] = monotonic_strict and magnitude_pass

    # Convert any inf/nan to JSON-safe sentinel strings, and any numpy
    # scalar types (bool_, int64, float64) to Python natives before
    # serialising. json.dump only handles Python builtins; numpy types
    # raise TypeError("not JSON serializable").
    def _walk_and_sanitise(o):
        if isinstance(o, dict):
            return {k: _walk_and_sanitise(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [_walk_and_sanitise(v) for v in o]
        # numpy scalar conversions
        if isinstance(o, np.generic):
            o = o.item()  # cast to Python native
        if isinstance(o, float):
            if math.isinf(o) or math.isnan(o):
                return f"<{'inf' if math.isinf(o) and o > 0 else '-inf' if math.isinf(o) else 'nan'}>"
            return o
        return o

    out_dir = Path(__file__).parent.parent / "data"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "protocol_o23_lindblad_explicit_results.json"
    sanitised = _walk_and_sanitise(results)
    with open(out_path, "w") as f:
        json.dump(sanitised, f, indent=4)
    print(f"Results written to {out_path}")
    return results


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    r = run()
    print("\n" + "=" * 76)
    print("O.23 LINDBLAD EXPLICIT — Tavis-Cummings + Chiral-OAM-Bath DFS suppression")
    print("=" * 76)
    for regime in r["regimes"]:
        print(
            f"N={regime['N_TLS']:>2}  "
            f"T2(chiral OAM-l=1)={regime['T2_chiral_OAM_l1_s']:.3e}s  "
            f"T2(symmetric OAM-l=0)={regime['T2_symmetric_OAM_l0_s']:.3e}s  "
            f"DFS ratio={regime['DFS_enhancement_ratio']:.3g}"
        )
    print(f"\nDFS ratio at largest N: {r['DFS_ratio_at_largest_N']:.3g}")
    print(f"Strict monotonic in N: {r['DFS_ratio_monotonic_strict_in_N']}")
    print(f"verdict: {r['verdict_status']}")
