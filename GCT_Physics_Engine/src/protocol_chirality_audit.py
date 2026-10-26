#!/usr/bin/env python3
"""
protocol_chirality_audit.py — Chirality Audit 
==========================================================
Tests whether the Fibonacci quasicrystal chain has a chiral zero-mode
structure that a generic chain does not.

The former pass (modes found and N_L != N_R or both > 0, with
L/R assigned by the SIGN of <C> even when |<C>| ~ 1e-14) could not fail. The
protocol now counts genuine chiral zero modes (|E| < 1e-8 and |<C>| > 0.5) and
compares the Fibonacci count with a seeded random-bond control on the same
chain length. An odd-length bipartite chain always carries one sublattice-
polarised zero mode, so the count is expected to be generic.

Steps
-----
1. Build Fibonacci chain (N=89, t_L=1.0, t_S=0.4).
2. Diagonalize to find midgap states.
3. Classify each as left- or right-chiral via sublattice operator C.
4. Confirm: Zero modes exist AND are localised at the boundary.
5. Output: chirality_report.json  +  chirality_spectrum.png.

GCT implication: if the 1D Fibonacci projection gives chiral zero modes,
the Atiyah-Singer Index Theorem guarantees the 6D->3D projection gives
a net topological chiral imbalance -> left-handed Standard-Model fermions.
"""

import json
import sys
from pathlib import Path
import numpy as np


from gct_chirality import ChiralityProver
from gct_utils import get_output_path


def run_chirality_audit():
    print("=" * 60)
    print("GCT Protocol — Chirality Audit")
    print("=" * 60)

    cp = ChiralityProver(N_sites=89, t_L=1.0, t_S=0.4)

    print(f"\nModel  : Fibonacci chain (slope phi = {cp.PHI:.6f})")
    print(f"Sites  : N = {cp.N}  (Fibonacci number F11 = 89)")
    print(f"t_L    = {cp.t_L}  (long bond  — 2D diagonal)")
    print(f"t_S    = {cp.t_S}  (short bond — 2D unit step)")
    print(f"Gap ≈  {abs(cp.t_L - cp.t_S):.2f}")

    print("\nSolving eigenproblem …")
    result = cp.solve_1D_model()

    # ---------------------------------------------------------------
    print(f"\nMidgap States  (|E| < {result['threshold']:.3f}) :")
    if result['zero_modes']:
        print(f"  {'Index':>5}  {'Energy':>10}  {'<C>':>8}  {'<x>':>7}  {'IPR':>8}  Label")
        for zm in result['zero_modes']:
            print(f"  {zm['index']:5d}  {zm['energy']:+10.5f}  "
                  f"{zm['chiral_charge']:+8.4f}  {zm['x_mean']:7.2f}  "
                  f"{zm['ipr']:8.5f}  {zm['chirality']}")
    else:
        print("  (none found — try lower threshold)")

    # ---------------------------------------------------------------
    print(f"\nChirality count :")
    print(f"  N_L (left-chiral)   = {result['N_L']}")
    print(f"  N_R (right-chiral)  = {result['N_R']}")
    print(f"  Net Chirality       = {result['net_chirality']}")

    # Verify: zero modes exist and are edge-localised (high IPR)
    modes_found    = len(result['zero_modes']) > 0
    modes_localised = all(zm['ipr'] > 1.0 / result['N_sites']
                         for zm in result['zero_modes'])

    # GCT verdict: even N_L = N_R = 1 is physically meaningful.
    # In the 6D projection only ONE boundary is accessible from 3D space.
    # The Index Theorem guarantees the remaining zero mode is chiral.
    def chiral_zero_count(H):
        e, v = np.linalg.eigh(H)
        c = np.array([1.0 if i % 2 == 0 else -1.0 for i in range(H.shape[0])])
        return int(sum(1 for k in range(len(e))
                       if abs(e[k]) < 1e-8 and abs(float((v[:, k] ** 2) @ c)) > 0.5))

    H_fib, _ = cp.build_hamiltonian()
    fib_count = chiral_zero_count(H_fib)
    rng = np.random.default_rng(11938)
    n_control = 200
    control_counts = []
    for _ in range(n_control):
        t = np.where(rng.random(cp.N - 1) < 0.5, cp.t_L, cp.t_S)
        H_rand = np.diag(-t, 1) + np.diag(-t, -1)
        control_counts.append(chiral_zero_count(H_rand))
    control_same_fraction = float(np.mean([c == fib_count for c in control_counts]))
    gct_verified = bool(fib_count > 0 and control_same_fraction < 0.05)
    verdict = ("FIBONACCI_SPECIFIC_CHIRAL_ZERO_MODES" if gct_verified
               else "CHIRAL_ZERO_MODE_GENERIC_NOT_FIBONACCI_SPECIFIC")

    print("\n" + "=" * 60)
    print(f"Genuine chiral zero modes (|E|<1e-8, |<C>|>0.5): Fibonacci = {fib_count}")
    print(f"Random-bond control ({n_control} chains, N={cp.N}): same count in "
          f"{100*control_same_fraction:.1f}% of trials")
    print(f"Verdict: {verdict}")
    print("=" * 60)

    # ---------------------------------------------------------------
    # Plot
    plot_path = get_output_path("chirality_spectrum.png")
    cp.plot_spectrum(result, save_path=str(plot_path))

    # ---------------------------------------------------------------
    # Save JSON
    out = {
        "N_sites":          result["N_sites"],
        "t_L":              result["t_L"],
        "t_S":              result["t_S"],
        "gap_estimate":     result["gap_estimate"],
        "threshold":        result["threshold"],
        "N_L":              result["N_L"],
        "N_R":              result["N_R"],
        "net_chirality":    result["net_chirality"],
        "zero_modes":       result["zero_modes"],
        "legacy_sign_labels_note": "N_L/N_R above label modes by the sign of <C>, which is noise for |<C>| ~ 1e-14; not used for the verdict.",
        "fibonacci_chiral_zero_modes": fib_count,
        "random_control_n_chains": n_control,
        "random_control_counts_histogram": {str(k): control_counts.count(k) for k in sorted(set(control_counts))},
        "random_control_same_count_fraction": control_same_fraction,
        "gct_verified":     gct_verified,
        "verdict":          verdict,
        "pass":             bool(gct_verified),
        "gct_implication": (
            "Odd-length bipartite chains carry a sublattice-polarised zero mode"
            " whatever the bond sequence; this chain does not by itself"
            " establish a Fibonacci-specific chirality mechanism."
        ),
        "plot_path":        "GCT_Physics_Engine/output/chirality_spectrum.png",
    }
    out_path = get_output_path("protocol_chirality_audit_results.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nReport saved → {out_path}")
    return out


if __name__ == "__main__":
    run_chirality_audit()
