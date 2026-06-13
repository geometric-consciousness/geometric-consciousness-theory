#!/usr/bin/env python3
"""
protocol_md_fk_ih_closed_cages.py - Down-quark FK determinant on I_h-closed cages
==================================================================================
The down-quark chain m_d = m_u * det_FK(D_F) requires a principled rule for
WHICH lattice truncation carries the FK pseudo-determinant. Arbitrary
top-N-by-perp-norm shells truncate the outermost I_h orbit asymmetrically and
break icosahedral symmetry (the same defect cage_builder.py documents for the
144-vs-152 cage); the finite-size sequence over arbitrary shells oscillates
rather than converging monotonically.

Extraction rule (fixed in advance of evaluation, on geometric grounds): the FK
determinant is read ONLY on I_h-CLOSED ORBIT-UNION cages -- truncations that
contain every I_h image of every node they contain. This is the same closure
discipline the manuscript already applies to the 152-node D_F cage and the
N=144 polaron cage. ALL I_h-closed cages in the lattice window are reported;
none are dropped.

Construction (registered down-quark FK chain convention, matching
protocol_quark_mismatch_scaling.py / verify_a5_ratio):
  - 6D lattice nodes from GCTLattice(R=4, perp_cutoff=3.0)
  - adjacency edges where the 6D ambient distance equals 1.0, edge weight phi
  - det_FK = exp(mean(log|lambda_i|)) over the non-zero spectrum
    (Fuglede-Kadison normalized pseudo-determinant; gct_spectrum discipline)
  - m_d = m_u * det_FK with m_u = m_e * phi^3

Outputs the closed-cage sequence det_FK(N) and m_d(N), the comparison against
PDG 2024 m_d = 4.70 +/- 0.07 MeV and against the phi^phi closed-form candidate,
and the verdict on whether the I_h-closed sequence stabilises inside the
registered shell-resonance band.
"""

import json
import os
import sys
import io

import numpy as np

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

try:
    from gct_utils import get_output_path, C
except ImportError:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from gct_utils import get_output_path, C

from gct_lattice import GCTLattice
import gct_projections as proj
from cage_builder import _build_Ih_group, _full_orbit

PHI = float(C.PHI)
M_E = float(C.M_E_OBS)
M_D_PDG = 4.70
M_D_PDG_ERR = 0.07
PHI_POW_PHI = PHI ** PHI


def enumerate_closed_cages(R=4, perp_cutoff=3.0, n_cap=3200):
    """Walk outward in perp-norm accumulating FULL I_h orbits; record every
    cumulative orbit-union (each is an I_h-closed cage)."""
    lattice = GCTLattice(R=R, perp_cutoff=perp_cutoff)
    x_eq = lattice.x_equilibrium
    x_perp = proj.project_perp(x_eq)
    norms = np.linalg.norm(x_perp, axis=1)
    idx = np.argsort(norms)
    if norms[idx[0]] < 1e-8:
        idx = idx[1:]  # drop origin

    group = _build_Ih_group()
    node_set = {tuple(int(round(c)) for c in x_eq[j]) for j in idx}

    cages = []          # list of (N_cumulative, orbit_size, perp_radius)
    accumulated = []
    seen = set()
    for j in idx:
        seed = tuple(int(round(c)) for c in x_eq[j])
        if seed in seen:
            continue
        orbit = _full_orbit(seed, group)
        if not orbit.issubset(node_set):
            # orbit leaks outside the acceptance window: not closable here
            seen |= orbit
            continue
        seen |= orbit
        accumulated.extend(sorted(orbit))
        if len(accumulated) > n_cap:
            break
        cages.append({
            "N": len(accumulated),
            "orbit_size": len(orbit),
            "perp_radius": float(np.linalg.norm(proj.project_perp(
                np.array([seed], dtype=float))[0])),
        })
    return cages, np.array(accumulated, dtype=float)


def fk_determinant(nodes_6d):
    """det_FK over nonzero spectrum of the ambient-distance-1.0 phi-weighted
    adjacency (registered down-quark chain convention)."""
    diffs = nodes_6d[:, None, :] - nodes_6d[None, :, :]
    dists = np.linalg.norm(diffs, axis=2)
    mask = np.abs(dists - 1.0) < 1e-4
    np.fill_diagonal(mask, False)
    A = np.where(mask, PHI, 0.0)
    n_edges = int(mask.sum() // 2)
    if n_edges == 0:
        return None, 0
    evals = np.linalg.eigvalsh(A)
    nz = np.abs(evals)[np.abs(evals) > 1e-10]
    if nz.size == 0:
        return None, n_edges
    return float(np.exp(np.mean(np.log(nz)))), n_edges


def run():
    print("=" * 74)
    print("GCT Protocol - Down-quark FK determinant on I_h-CLOSED orbit-union cages")
    print("=" * 74)
    m_u = M_E * PHI ** 3
    print(f"\n  m_u = m_e * phi^3 = {m_u:.5f} MeV")
    print(f"  PDG 2024 target: m_d = {M_D_PDG} +/- {M_D_PDG_ERR} MeV")
    print(f"  Closed-form candidate: phi^phi = {PHI_POW_PHI:.6f} "
          f"-> m_d = {m_u * PHI_POW_PHI:.4f} MeV\n")

    cages, all_nodes = enumerate_closed_cages()
    print(f"  I_h-closed orbit-union cages found in window: {len(cages)}\n")
    print(f"  {'N':>5} {'orbit':>6} {'r_perp':>8} {'edges':>7} {'det_FK':>9} "
          f"{'m_d(MeV)':>9} {'vs PDG':>8} {'vs phi^phi':>10}")
    print("  " + "-" * 70)

    rows = []
    for cage in cages:
        N = cage["N"]
        det, n_edges = fk_determinant(all_nodes[:N])
        row = dict(cage)
        row["edges"] = n_edges
        if det is None:
            row.update({"det_fk": None, "m_d": None, "err_pct": None,
                        "ratio_phiphi": None})
            print(f"  {N:>5} {cage['orbit_size']:>6} {cage['perp_radius']:>8.4f} "
                  f"{n_edges:>7}   --- no spectrum ---")
        else:
            m_d = m_u * det
            err = (m_d - M_D_PDG) / M_D_PDG * 100.0
            row.update({"det_fk": det, "m_d": m_d, "err_pct": err,
                        "ratio_phiphi": det / PHI_POW_PHI})
            print(f"  {N:>5} {cage['orbit_size']:>6} {cage['perp_radius']:>8.4f} "
                  f"{n_edges:>7} {det:>9.5f} {m_d:>9.4f} {err:>+7.2f}% "
                  f"{det / PHI_POW_PHI:>10.4f}")
        rows.append(row)

    # Pre-registered reading: behaviour of the closed-cage sequence at large N.
    valid = [r for r in rows if r["det_fk"] is not None]
    tail = [r for r in valid if r["N"] >= 1000]
    verdict_data = {}
    if tail:
        errs = [r["err_pct"] for r in tail]
        m_ds = [r["m_d"] for r in tail]
        in_band_3pct = all(abs(e) <= 3.0 for e in errs)
        in_band_resonance = all(abs(e) <= 11.0 for e in errs)
        verdict_data = {
            "tail_N_range": [tail[0]["N"], tail[-1]["N"]],
            "tail_n_cages": len(tail),
            "tail_m_d_min": min(m_ds), "tail_m_d_max": max(m_ds),
            "tail_err_min_pct": min(errs), "tail_err_max_pct": max(errs),
            "all_tail_within_3pct": in_band_3pct,
            "all_tail_within_11pct_band": in_band_resonance,
        }
        print("\n  Closed-cage tail (N >= 1000):")
        print(f"    cages: {len(tail)}   m_d range: [{min(m_ds):.4f}, "
              f"{max(m_ds):.4f}] MeV   err range: [{min(errs):+.2f}%, "
              f"{max(errs):+.2f}%]")
        print(f"    all within +/-3%:  {in_band_3pct}")
        print(f"    all within +/-11% shell-resonance band: {in_band_resonance}")

        # Oscillation diagnostics (NOT a registered extraction-rule change):
        # tail-mean ratio to phi^phi and decaying-envelope check.
        deep = [r for r in valid if r["N"] >= 2000]
        if deep:
            ratios = [r["ratio_phiphi"] for r in deep]
            errs_d = [r["err_pct"] for r in deep]
            mean_ratio = float(np.mean(ratios))
            std_ratio = float(np.std(ratios, ddof=1)) if len(ratios) > 1 else 0.0
            half = len(tail) // 2
            amp_early = max(abs(r["err_pct"]) for r in tail[:half]) if half else None
            amp_late = max(abs(r["err_pct"]) for r in tail[half:])
            verdict_data.update({
                "deep_tail_N_min": deep[0]["N"],
                "deep_tail_n_cages": len(deep),
                "deep_tail_mean_ratio_phiphi": mean_ratio,
                "deep_tail_std_ratio_phiphi": std_ratio,
                "deep_tail_mean_err_pct": float(np.mean(errs_d)),
                "envelope_amp_early_half_pct": amp_early,
                "envelope_amp_late_half_pct": amp_late,
                "envelope_decaying": (amp_early is not None
                                      and amp_late < amp_early),
            })
            print(f"\n  Oscillation diagnostics (N >= 2000, {len(deep)} cages):")
            print(f"    mean det_FK / phi^phi = {mean_ratio:.4f} "
                  f"(sample std {std_ratio:.4f})")
            print(f"    mean signed error vs PDG: "
                  f"{float(np.mean(errs_d)):+.2f}%")
            print(f"    oscillation envelope: early-half max |err| = "
                  f"{amp_early:.2f}%, late-half max |err| = {amp_late:.2f}% "
                  f"-> decaying: {amp_late < amp_early}")

    out = {
        "extraction_rule": ("FK determinant read only on I_h-closed orbit-union "
                            "cages (all reported, none dropped); rule fixed on "
                            "geometric grounds prior to evaluation"),
        "adjacency_convention": "6D ambient distance 1.0, edge weight phi",
        "m_u_mev": m_u,
        "m_d_pdg": M_D_PDG,
        "phi_pow_phi": PHI_POW_PHI,
        "closed_cages": rows,
        "tail_verdict": verdict_data,
    }
    path = get_output_path("protocol_md_fk_ih_closed_cages_results.json")
    with open(path, "w") as fp:
        json.dump(out, fp, indent=2)
    print(f"\n[Saved JSON] -> {path}")
    return out


if __name__ == "__main__":
    run()
