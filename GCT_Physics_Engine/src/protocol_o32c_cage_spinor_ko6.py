#!/usr/bin/env python3
"""
protocol_o32c_cage_spinor_ko6.py - O.32: KO-dim 6 on the cage (X) spinor space
==============================================================================
Positive route of O.32. protocol_o32 showed the BARE 152-node cage with a
DIAGONAL grading cannot reach eps''=-1 (bond graph non-bipartite). protocol_o32b
showed KO-dim 6 IS realizable by chiral doubling. This protocol tests whether
the GCT geometry supplies that chirality: tensor the cage with a 2-component
spinor (the 2I binary-icosahedral double cover = the H quaternion factor of
A_F), so the grading becomes gamma = 1 (X) gamma_spin -- a UNIFORM spinor
chirality, not a point-function, hence immune to the bipartiteness obstruction.

    H = C^152 (X) C^2
    J     = (P (X) K) . conjugation     P = cage central inversion, K real 2x2
    gamma = 1_152 (X) gamma_spin         spinor chirality
    D     = D_F (X) D_spin                cage adjacency (X) chirality-odd spinor op

Because P D_F = D_F P (proven in protocol_o32), the cage parts are consistent
and the three KO signs are fixed ENTIRELY by the 2x2 spinor data:
    eps   = +1  iff  K^2 = +I
    eps'  : K conj(D_spin) = eps'  D_spin K
    eps'' : K conj(gamma_spin) = eps'' gamma_spin K
plus the spectral-triple requirements gamma_spin^2 = I (Hermitian),
{D_spin, gamma_spin} = 0, D_spin Hermitian and nonzero.

We SEARCH the Pauli/real-involution space for all (K, gamma_spin, D_spin) that
yield a consistent KO-dim-6 triple, then build the full 304-dim operators for a
found solution and verify (eps,eps',eps'')=(+1,+1,-1) on complex test vectors.

SCOPE (read carefully -- deliberately limited to avoid the standard NCG overclaim): the object
built here is a real OPERATOR DATUM (H, D, J, gamma) carrying the KO-dim-6 SIGN
structure (eps,eps',eps'') = (+1,+1,-1). It is NOT yet a spectral triple,
because the algebra A_F = C+H+M_3(C) is not represented on H; KO-dimension is
formally defined only once A_F acts. What is established is therefore:
  (1) the bare-cage diagonal-grading obstruction of protocol_o32 is LIFTED once
      the 2-component spinor factor is added (eps''=-1 needs no bipartiteness);
  (2) the KO-dim-6 sign datum is REALIZABLE on cage(X)spinor.
What remains OPEN (bundles with O.5): (a) the icosahedral projection UNIQUELY
FORCING this structure rather than merely permitting it; (b) the full A_F
representation; (c) the first-order condition; (d) the order-zero condition;
(e) the physical (dressed) Dirac, whose cage/spinor mixing would break the
product ansatz D = D_F (X) D_spin on which the sign-factorization rests.
"""

import json
import os
import sys
import numpy as np

try:
    from gct_utils import get_output_path, PHI
except ImportError:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from gct_utils import get_output_path, PHI

from cage_builder import build_canonical_cage

I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)


def _test_vectors(dim, k=6):
    base = np.arange(1, dim + 1, dtype=float)
    vs = []
    for t in range(k):
        re = np.cos(base * (t + 1)) + (t + 1)
        im = np.sin(base * (t + 2)) - (t + 1) * 0.5
        vs.append(re + 1j * im)
    return vs


def search_spinor_structures():
    """Find all (K, gamma_spin, D_spin) over real involutions / Pauli ops that
    give a consistent KO-dim-6 spinor triple. K must be REAL (it is the linear
    part of an antilinear J = K.conj)."""
    # real 2x2 involutions (K^2=+I) plus the K^2=-I option for completeness
    K_choices = {
        "I": I2, "sx": SX, "sz": SZ,
        "isy": np.array([[0, 1], [-1, 0]], dtype=complex),  # real, K^2=-I
    }
    grades = {"sx": SX, "sy": SY, "sz": SZ}
    dops = {"sx": SX, "sy": SY, "sz": SZ}
    sols = []
    for kn, K in K_choices.items():
        if not np.allclose(K.imag, 0):
            continue  # K must be real
        eps = +1 if np.allclose(K @ K, I2) else -1
        for gn, g in grades.items():
            if not np.allclose(g @ g, I2):
                continue
            for dn, Dop in dops.items():
                # spectral-triple: gamma Hermitian (all Pauli are), D Hermitian,
                # {D,gamma}=0, D != 0
                if not np.allclose(Dop, Dop.conj().T):
                    continue
                if not np.allclose(g @ Dop + Dop @ g, 0):
                    continue
                # eps' : K conj(D) = eps' D K
                lhs = K @ np.conjugate(Dop)
                if np.allclose(lhs, Dop @ K):
                    epsp = +1
                elif np.allclose(lhs, -(Dop @ K)):
                    epsp = -1
                else:
                    continue
                # eps'': K conj(gamma) = eps'' gamma K
                lhsg = K @ np.conjugate(g)
                if np.allclose(lhsg, g @ K):
                    epspp = +1
                elif np.allclose(lhsg, -(g @ K)):
                    epspp = -1
                else:
                    continue
                sols.append({
                    "K": kn, "gamma_spin": gn, "D_spin": dn,
                    "signs": (eps, epsp, epspp),
                    "ko_dim6": (eps, epsp, epspp) == (1, 1, -1),
                })
    return sols


def verify_full(cage_perp, cage_6d, K, g, Dop):
    """Build the full 304-dim operators and verify the three signs on complex
    test vectors (J applied as a genuine antilinear map)."""
    N = cage_perp.shape[0]
    # cage adjacency D_F
    D_F = np.zeros((N, N))
    for i in range(N):
        for j in range(i + 1, N):
            d = np.linalg.norm(cage_perp[i] - cage_perp[j])
            if abs(d - 1.0) < 0.05:
                D_F[i, j] = D_F[j, i] = 1.0
            elif abs(d - 1.0 / PHI) < 0.05:
                D_F[i, j] = D_F[j, i] = PHI
    # inversion permutation P
    key = {tuple(np.round(x).astype(int)): i for i, x in enumerate(cage_6d)}
    P = np.zeros((N, N))
    for i, x in enumerate(cage_6d):
        P[i, key[tuple(np.round(-x).astype(int))]] = 1.0

    Dfull = np.kron(D_F, Dop)
    gfull = np.kron(np.eye(N), g)
    Slin = np.kron(P, K)  # linear part of J = Slin . conj

    def J(v):
        return Slin @ np.conjugate(v)

    vs = _test_vectors(2 * N)
    eps = +1 if all(np.allclose(J(J(v)), v) for v in vs) else -1
    epsp = (+1 if all(np.allclose(J(Dfull @ v), Dfull @ J(v)) for v in vs)
            else (-1 if all(np.allclose(J(Dfull @ v), -(Dfull @ J(v))) for v in vs) else 0))
    epspp = (+1 if all(np.allclose(J(gfull @ v), gfull @ J(v)) for v in vs)
             else (-1 if all(np.allclose(J(gfull @ v), -(gfull @ J(v))) for v in vs) else 0))
    checks = {
        "gamma_sq_1": bool(np.allclose(gfull @ gfull, np.eye(2 * N))),
        "gamma_D_anticommute": bool(np.allclose(gfull @ Dfull + Dfull @ gfull, 0)),
        "D_self_adjoint": bool(np.allclose(Dfull, Dfull.conj().T)),
        "P_commutes_D_F": bool(np.allclose(P @ D_F, D_F @ P)),
    }
    return (eps, epsp, epspp), checks, 2 * N


def run():
    print("=" * 70)
    print("GCT Protocol O.32c - KO-dim 6 on cage (X) spinor (positive route)")
    print("=" * 70)

    sols = search_spinor_structures()
    ko6 = [s for s in sols if s["ko_dim6"]]
    print(f"\n  Spinor-structure search: {len(sols)} consistent triples, "
          f"{len(ko6)} with KO-dim 6 (+1,+1,-1):")
    for s in ko6:
        print(f"    K={s['K']:>4}  gamma_spin={s['gamma_spin']}  "
              f"D_spin={s['D_spin']}  -> signs {s['signs']}")

    if not ko6:
        print("\n  NO geometrically-motivated spinor structure yields KO-dim 6.")
        results = {"ko6_spinor_solutions": [], "pass_ko6": False}
        out = get_output_path("protocol_o32c_cage_spinor_ko6_results.json")
        with open(out, "w") as fp:
            json.dump(results, fp, indent=2)
        print(f"\n[Saved JSON] -> {out}")
        return results

    # Build full operators for the first KO-dim-6 solution and verify on the
    # actual 152-node cage.
    nodes_6d, nodes_perp = build_canonical_cage(size=152)
    pick = ko6[0]
    Kmap = {"I": I2, "sx": SX, "sz": SZ,
            "isy": np.array([[0, 1], [-1, 0]], dtype=complex)}
    pmap = {"sx": SX, "sy": SY, "sz": SZ}
    signs_full, checks, dimH = verify_full(
        nodes_perp, nodes_6d, Kmap[pick["K"]], pmap[pick["gamma_spin"]],
        pmap[pick["D_spin"]])

    print(f"\n  Full verification on H = C^152 (X) C^2  (dim {dimH}), "
          f"solution K={pick['K']}, gamma_spin={pick['gamma_spin']}, "
          f"D_spin={pick['D_spin']}:")
    for k, v in checks.items():
        print(f"    {k:24s}: {v}")
    print(f"    signs (eps,eps',eps'')   : {signs_full}")
    ko_dim = 6 if signs_full == (1, 1, -1) else None
    print(f"    KO-dimension (mod 8)     : {ko_dim}")

    axioms_ok = all(checks.values())
    passed = (signs_full == (1, 1, -1)) and axioms_ok
    verdict = (
        "POSITIVE (scoped): tensoring the cage with the 2-component spinor "
        "(2I double-cover / H factor) yields a real OPERATOR DATUM (H,D,J,gamma) "
        "with the KO-dim-6 SIGN structure (+1,+1,-1) -- the uniform spinor "
        "chirality supplies eps''=-1 with no bipartiteness requirement, lifting "
        "the bare-cage obstruction of protocol_o32. NOT yet a spectral triple "
        "(A_F unrepresented). OPEN (bundle with O.5): uniqueness/forcing by the "
        "projection; full A_F representation; first-order + order-zero "
        "conditions; dressed (non-product) Dirac."
        if passed else
        "Full-operator verification did not confirm the KO-dim-6 sign datum -- review.")
    print(f"\n  VERDICT: {verdict}")
    print("=" * 70)

    results = {
        "search_total_consistent": len(sols),
        "ko6_spinor_solutions": ko6,
        "chosen_solution": pick,
        "full_dim_H": dimH,
        "full_signs": list(signs_full),
        "full_axiom_checks": checks,
        "ko_dimension_mod8": ko_dim,
        "pass_ko6": bool(passed),
        "verdict": verdict,
        "scope_open": ("uniqueness/forcing by projection + full A_F "
                       "representation + first-order condition + dressed Dirac "
                       "(bundles with O.5)"),
    }
    out = get_output_path("protocol_o32c_cage_spinor_ko6_results.json")
    with open(out, "w") as fp:
        json.dump(results, fp, indent=2)
    print(f"\n[Saved JSON] -> {out}")
    return results


if __name__ == "__main__":
    run()
