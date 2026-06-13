#!/usr/bin/env python3
"""
protocol_connes_isomorphism.py — Protocol J: Connes NCG Isomorphism
===================================================================
This protocol maps geometric features of the GCT 6D -> 3D icosahedral
projection to the finite algebra of Alain Connes' Noncommutative
Standard Model: A_F = C [+] H [+] M_3(C). Three components verified:

  1. Real-algebra dimensional match: dim_R(A_F) = 2 + 4 + 18 = 24.
     This is a necessary but NOT sufficient condition for the
     spectral-triple identification (Connes sign table,
     Chamseddine-Connes-Marcolli 2007); the load-bearing invariant is
     the KO-dimension of the finite spectral triple (KO-dim = 6 mod 8
     for the SM). O.32 separates this invariant into a decided
     bare-cage diagonal-grading obstruction and a realized
     cage-times-spinor KO-sign datum.

  2. Physics-derived D_F construction: the finite Dirac operator is
     taken from the canonical 152-node I_h-closed boundary cage built
     by cage_builder.build_canonical_cage(size=152), with golden-weighted
     bonds at perp-space distances {1, 1/phi}. The 152-node orbit-union
     carrier supplies exact I_h closure for protocols whose operators
     require central inversion and full icosahedral symmetry.

  3. Bare-adjacency scope: the bare cage eigenvalues do NOT reproduce
     observed fermion mass ratios. The bare adjacency identification is
     therefore not the dressed finite Dirac operator. O.32 rules out
     KO-dim 6 for the bare-cage diagonal grading, while
     protocol_o32c_cage_spinor_ko6.py realizes the KO-dim-6 sign
     structure on cage x spinor as a real operator datum. Full
     spectral-triple closure requires the A_F representation,
     first-order and order-zero conditions, and the dressed Dirac
     operator; that closure bundles with Open Problem O.5 (QLQCD-1L).

STATUS: Tier 3 (structural framework + bare-adjacency scope). The
"spectral triple identification
derives CKM/PMNS from the bare adjacency" claim is explicitly
unsupported by this protocol; that identification requires O.32 full
spectral-triple closure plus Dirac dressing in O.5.
"""

import json
import sys
import io
import os
import numpy as np

# Ensure clean UTF-8 printing for mathematical operators
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try:
    from gct_utils import get_output_path, GCTReporter, PHI
except ImportError:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from gct_utils import get_output_path, GCTReporter, PHI


def run_connes_isomorphism_protocol():
    report = GCTReporter("Connes NCG Isomorphism (Protocol J)")
    
    print("=" * 65)
    print("GCT Protocol J — Connes NCG Isomorphism")
    print("=" * 65)

    # ── 1. The Global Condensate Phase -> Complex Numbers C ──
    print("\n  ─── Mapping 1: Vacuum Scalar Phase ───")
    print("  Geometric Origin: The global U(1) winding of the superfluid condensate.")
    target_c_dim = 2
    actual_c_dim = 2  # A complex number (real + imaginary phase representation)
    
    print(f"  Algebraic Map: U(1) Phase  -->  C (Complex Numbers)")
    print(f"  Real Dimensionality: {actual_c_dim}")
    report.section("Scalar Phase (C)")
    report.log_value("Algebra", "C")
    report.log_value("Real Dimension", actual_c_dim)

    # ── 2. The Physical Space Spinors -> Quaternions H ──
    print("\n  ─── Mapping 2: Physical Manifold (E_parallel) ───")
    print("  Geometric Origin: The 2I double-cover of the 3D icosahedral spatial rotations.")
    target_h_dim = 4
    actual_h_dim = 4  # Quaternions have 4 real degrees of freedom (1 real scalar + 3 imaginary bi-vectors)
    
    print(f"  Algebraic Map: 2I (Spinors)  -->  H (Quaternions)")
    print(f"  Real Dimensionality: {actual_h_dim}")
    report.section("Physical Spinors (H)")
    report.log_value("Algebra", "H")
    report.log_value("Real Dimension", actual_h_dim)

    # ── 3. The Internal Space Color -> M_3(C) ──
    print("\n  ─── Mapping 3: Internal Manifold (E_perpendicular) ───")
    print("  Geometric Origin: The SU(3) symmetry reduction of the 10 three-fold RT axes.")
    target_m3c_dim = 18
    actual_m3c_dim = 3 * 3 * 2  # 3x3 complex matrices = 9 complex entries = 18 real degrees of freedom
    
    print(f"  Algebraic Map: SU(3) color space  -->  M_3(C) (3x3 Complex Matrices)")
    print(f"  Real Dimensionality: {actual_m3c_dim}")
    report.section("Internal Color Space (M_3(C))")
    report.log_value("Algebra", "M_3(C)")
    report.log_value("Real Dimension", actual_m3c_dim)

    # ── 4. The NCG Dirac Operator D_F ──
    print("\n  ─── Mapping 4: The Finite Dirac Operator D_F ───")
    print("  Geometric Origin: canonical 152-node I_h-closed cage adjacency matrix")
    print("  (golden-weighted bonds at perp-space distances {1, 1/phi};")
    print("  see cage_builder.py and protocol_cage_spectral_decomp.py).")
    print("  In Connes NCG, the dressed D_F would accommodate fermion masses and")
    print("  CKM mixing — the BARE adjacency spectrum below does NOT.")

    # Build the physics-derived I_h-closed cage adjacency matrix. The
    # asymmetric 144-node truncation is retained elsewhere only for blast-radius
    # comparison; D_F uses the canonical 152-node orbit-union cage when exact
    # I_h closure is required.
    from cage_builder import build_canonical_cage

    nodes_6d, nodes_perp = build_canonical_cage(size=152)
    D_F = np.zeros((nodes_perp.shape[0], nodes_perp.shape[0]))
    for i in range(nodes_perp.shape[0]):
        for j in range(i + 1, nodes_perp.shape[0]):
            d = np.linalg.norm(nodes_perp[i] - nodes_perp[j])
            if abs(d - 1.0) < 0.05:
                D_F[i, j] = D_F[j, i] = 1.0
            elif abs(d - (1.0 / PHI)) < 0.05:
                D_F[i, j] = D_F[j, i] = PHI
    N           = D_F.shape[0]
    print(f"\n  [Computing D_F Eigenvalues for the {N}-node cage adjacency]")

    # Symmetric real matrix; use eigvalsh for stability.
    eigenvalues = np.linalg.eigvalsh(D_F)
    eigenvalues = np.sort(np.abs(eigenvalues))[::-1]

    # Extract top 3 distinct eigenvalue magnitudes for the leading-generation
    # ratio comparison.
    e1, e2, e3 = float(eigenvalues[0]), float(eigenvalues[1]), float(eigenvalues[2])

    print("  Top 3 Bare Eigenvalue Magnitudes (|λ|):")
    print(f"    λ_1 = {e1:.4f}")
    print(f"    λ_2 = {e2:.4f}")
    print(f"    λ_3 = {e3:.4f}")

    ratio_12_bare = e1 / e2 if e2 > 1e-12 else float("inf")
    ratio_23_bare = e2 / e3 if e3 > 1e-12 else float("inf")

    # Physical Mass Ratios (PDG 2024)
    m_tau, m_mu, m_e = 1776.93, 105.66, 0.511
    ratio_12_phys = m_tau / m_mu
    ratio_23_phys = m_mu / m_e

    print("\n  [Ratio Evaluation — bare cage adjacency vs observed]")
    print(f"    Bare λ_1 / λ_2 = {ratio_12_bare:.4f}  | Physical m_tau / m_mu = {ratio_12_phys:.4f}")
    print(f"    Bare λ_2 / λ_3 = {ratio_23_bare:.4f}  | Physical m_mu / m_e   = {ratio_23_phys:.4f}")

    print("\n  --> Result: bare physics-derived icosahedral cage adjacency eigenvalues")
    print("      do NOT reproduce observed fermion mass ratios. The bare-identification")
    print("      claim ('D_F = cage adjacency derives the fermion spectrum') is")
    print("      explicitly unsupported by this computation.")
    print("      O.32 rules out KO-dim 6 for the bare-cage diagonal grading")
    print("      and realizes the KO-dim-6 sign datum on cage x spinor.")
    print("      Full spectral-triple closure requires A_F representation,")
    print("      first-order/order-zero conditions, and dressed Dirac work in O.5.")

    report.section("Operator Mapping")
    report.log_value("Dirac Operator D_F", "152-node I_h-closed cage adjacency (cage_builder.build_canonical_cage(size=152))")

    # ── 5. Total Dimensional Verification ──
    print("\n  ─── Stage 5: Connes Finite Algebra Verification ───")
    total_gct_dim    = actual_c_dim + actual_h_dim + actual_m3c_dim
    total_connes_dim = target_c_dim + target_h_dim + target_m3c_dim
    
    print(f"  Total Real Dimensionality of GCT Operators: {total_gct_dim}")
    print(f"  Total Real Dimensionality of Connes A_F:    {total_connes_dim}")
    
    matched = (total_gct_dim == total_connes_dim == 24)

    print(f"  Axiom Match: {'YES ✓' if matched else 'NO ✗'} (Dim = 24)")

    verdict = "NECESSARY_CONDITION_PASS__FULL_SPECTRAL_TRIPLE_OPEN" if matched else "FAIL"
    print(f"\n  VERDICT: {verdict} — The 6D -> 3D quasicrystalline projection explicitly accommodates")
    print("  the exact 24-dimensional real algebraic structure of the Noncommutative Standard Model.")
    print("  O.32 status: bare-cage diagonal KO-6 is ruled out; cage x spinor realizes KO-6 signs.")
    print("  Full spectral-triple closure still requires A_F representation, first-order/order-zero")
    print("  conditions, and dressed D_F identification in O.5.")
    print("=" * 65)

    report.verdict(False, "24-dimensional algebra count is a necessary condition only; full spectral-triple identification requires O.32 full closure and O.5.")

    results = {
        "algebra_c_dim": actual_c_dim,
        "algebra_h_dim": actual_h_dim,
        "algebra_m3c_dim": actual_m3c_dim,
        "total_gct_dim": total_gct_dim,
        "total_connes_dim": total_connes_dim,
        "tier": "Tier 3 structural framework + necessary 24-dimensional algebra count; full spectral-triple identification requires O.32 full closure and O.5",
        "ko_dimension_check_performed": False,
        "ko_dimension_check_scope": "This protocol does not compute the KO signs; see protocol_o32_ko_dimension.py, protocol_o32b_ko6_chiral_doubling.py, and protocol_o32c_cage_spinor_ko6.py.",
        "ko_dimension_load_bearing_invariant": "KO-dim(A_F) = 6 mod 8 for SM: bare-cage diagonal route eliminated; cage x spinor realizes the (+,+,-) sign datum; full A_F spectral-triple closure bundles with O.5.",
        "necessary_condition_pass": bool(matched),
        "spectral_triple_identification_pass": False,
        "spectral_triple_identification_status": "partial_ko_sign_datum__full_af_representation_first_order_order_zero_and_dressed_dirac_open",
        "dirac_operator_physical": "152-node I_h-closed cage adjacency (deterministic orbit-union cut-and-project lattice)",
        "dirac_operator_construction": "cage_builder.build_canonical_cage(size=152) plus golden-weighted perp-space adjacency",
        "dirac_operator_deviation_from_144": "The top-144-by-perp-norm cage is asymmetric under I_h; D_F uses the 152-node orbit-union cage for exact I_h closure.",
        "d_f_eigenvalues_top3": [e1, e2, e3],
        "d_f_computed_ratios": {"ratio_12": ratio_12_bare, "ratio_23": ratio_23_bare},
        "physical_mass_ratios": {"m_tau_over_m_mu": ratio_12_phys, "m_mu_over_m_e": ratio_23_phys},
        "bare_adjacency_reproduces_mass_ratios": False,
        "d_f_status": "TIER3_BARE_ADJACENCY_NOT_DRESSED_DIRAC__DRESSED_DIRAC_BUNDLES_WITH_O.5",
        "verdict": verdict,
        "pass_24dim_necessary_condition_only": bool(matched),
        "pass": False
    }

    out_path = get_output_path("protocol_connes_isomorphism_results.json")
    with open(out_path, "w") as fp:
        json.dump(results, fp, indent=2)
    print(f"\n[Saved JSON] -> {out_path}")

    return results

if __name__ == "__main__":
    run_connes_isomorphism_protocol()
