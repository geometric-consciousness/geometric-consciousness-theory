#!/usr/bin/env python3
"""
protocol_o32b_ko6_chiral_doubling.py - O.32: KO-dim 6 via chiral doubling
==========================================================================
Anchor for the positive route of O.32. Establishes, by explicit matrix
computation, that KO-dimension == 6 (mod 8) IS realizable by the chiral-
doubling mechanism that Chamseddine-Connes-Marcolli (2007) use for the
Standard Model finite triple. This is the literature-anchored ground truth
against which the GCT cage construction (protocol_o32c) is tested.

The minimal real, even, finite spectral triple (one chiral fermion, doubled
with its antiparticle):

    H = M (+) Mbar,   M = C f_L (+) C f_R          (dim 4, basis [f_L,f_R,fbar_L,fbar_R])
    gamma  = diag(-1, +1, +1, -1)                  chirality; flips on antiparticles
    J      = S . (complex conjugation),  S = [[0,I2],[I2,0]]   charge conjugation
    D      = blockdiag(sigma_x, sigma_x)           Yukawa: connects L <-> R

Connes sign table for KO-dim n (mod 8) uses (eps, eps', eps''):
    J^2 = eps . 1 ,  J D = eps' . D J ,  J gamma = eps'' . gamma J
    KO-dim 6  <=>  (eps, eps', eps'') = (+1, +1, -1).

All operators are explicit; J is applied as an antilinear map (matrix then
conjugation) and every relation is checked on deterministic complex test
vectors, not just basis vectors.

SCOPE: this verifies the KO-dim-6 SIGN structure of the real operator datum
(H, D, J, gamma). The algebra A_F is not represented here; this protocol is the
sign-structure anchor for the mechanism, not a full spectral-triple
construction.
"""

import json
import os
import sys
import numpy as np

try:
    from gct_utils import get_output_path
except ImportError:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from gct_utils import get_output_path

# fixed deterministic complex test vectors (no RNG: reproducible)
def _test_vectors(dim, k=6):
    base = np.arange(1, dim + 1, dtype=float)
    vs = []
    for t in range(k):
        re = np.cos(base * (t + 1)) + (t + 1)
        im = np.sin(base * (t + 2)) - (t + 1) * 0.5
        vs.append(re + 1j * im)
    return vs


def apply_J(S, v):
    """Antilinear J = S . conjugation."""
    return S @ np.conjugate(v)


def run():
    print("=" * 68)
    print("GCT Protocol O.32b - KO-dim 6 via chiral doubling (CCM anchor)")
    print("=" * 68)

    I2 = np.eye(2)
    sx = np.array([[0, 1], [1, 0]], dtype=complex)

    # Hilbert space dim 4, basis [f_L, f_R, fbar_L, fbar_R]
    gamma = np.diag([-1.0, +1.0, +1.0, -1.0]).astype(complex)
    S = np.block([[np.zeros((2, 2)), I2], [I2, np.zeros((2, 2))]]).astype(complex)
    D = np.block([[sx, np.zeros((2, 2))], [np.zeros((2, 2)), sx]]).astype(complex)
    dim = 4

    # --- spectral-triple axioms ---
    gamma2 = np.allclose(gamma @ gamma, np.eye(dim))
    gammaD_odd = np.allclose(gamma @ D - (-(D @ gamma)), 0)  # gamma D = -D gamma
    D_selfadj = np.allclose(D, D.conj().T)

    # --- KO signs, checked on test vectors (J antilinear) ---
    vs = _test_vectors(dim)

    def sign_J2():
        return all(np.allclose(apply_J(S, apply_J(S, v)), v) for v in vs)  # +1

    def sign_JD():
        # J D v  vs  +/- D J v
        plus = all(np.allclose(apply_J(S, D @ v), D @ apply_J(S, v)) for v in vs)
        minus = all(np.allclose(apply_J(S, D @ v), -(D @ apply_J(S, v))) for v in vs)
        return +1 if plus else (-1 if minus else 0)

    def sign_Jgamma():
        plus = all(np.allclose(apply_J(S, gamma @ v), gamma @ apply_J(S, v)) for v in vs)
        minus = all(np.allclose(apply_J(S, gamma @ v), -(gamma @ apply_J(S, v))) for v in vs)
        return +1 if plus else (-1 if minus else 0)

    eps = +1 if sign_J2() else -1
    eps_p = sign_JD()
    eps_pp = sign_Jgamma()

    print(f"\n  Spectral-triple axioms:")
    print(f"    gamma^2 = 1           : {gamma2}")
    print(f"    gamma D = -D gamma    : {gammaD_odd}")
    print(f"    D self-adjoint        : {D_selfadj}")
    print(f"\n  KO signs (checked on {len(vs)} complex test vectors):")
    print(f"    eps   (J^2 = eps)        = {eps:+d}")
    print(f"    eps'  (J D = eps' D J)   = {eps_p:+d}")
    print(f"    eps'' (J g = eps'' g J)  = {eps_pp:+d}")

    signs = (eps, eps_p, eps_pp)
    ko6 = (signs == (1, 1, -1))
    axioms_ok = gamma2 and gammaD_odd and D_selfadj

    # KO-dimension from sign table (eps, eps', eps'')
    table = {
        (1, 1, 1): 0, (1, -1, None): 1, (-1, 1, -1): 2, (-1, 1, None): 3,
        (-1, 1, 1): 4, (-1, -1, None): 5, (1, 1, -1): 6, (1, 1, None): 7,
    }
    ko_dim = table.get(signs, None)

    print(f"\n  SIGNS (eps, eps', eps''): {signs}")
    print(f"  KO-dimension (mod 8): {ko_dim}")
    verdict = ("ANCHOR CONFIRMED: chiral doubling yields the KO-dim-6 sign "
               "structure (+1,+1,-1). This is the mechanism CCM use for the SM "
               "finite triple; the chirality grading (NOT a point-function) "
               "supplies eps''=-1, and charge conjugation J flips chirality."
               if (ko6 and axioms_ok) else
               "UNEXPECTED: chiral-doubling anchor did not reproduce KO-dim 6 — "
               "verify the construction.")
    print(f"  VERDICT: {verdict}")
    print("=" * 68)

    results = {
        "model": "minimal chiral doubling (one fermion + antiparticle)",
        "dim_H": dim,
        "gamma_squared_is_1": bool(gamma2),
        "gamma_D_anticommute": bool(gammaD_odd),
        "D_self_adjoint": bool(D_selfadj),
        "eps_Jsq": eps,
        "eps_p_JD": eps_p,
        "eps_pp_Jgamma": eps_pp,
        "signs": list(signs),
        "ko_dimension_mod8": ko_dim,
        "pass_ko6": bool(ko6 and axioms_ok),
        "verdict": verdict,
        "role": ("literature anchor (CCM 2007) for the positive O.32 route; "
                 "GCT-geometric realization tested in protocol_o32c"),
    }
    out = get_output_path("protocol_o32b_ko6_chiral_doubling_results.json")
    with open(out, "w") as fp:
        json.dump(results, fp, indent=2)
    print(f"\n[Saved JSON] -> {out}")
    return results


if __name__ == "__main__":
    run()
