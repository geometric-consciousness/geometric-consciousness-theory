#!/usr/bin/env python3
"""
protocol_b1_quality_space_irreps.py - graded Quality-Space irrep decomposition
=================================================================================
Ch16 §16.2.2c / §16.4 model the GCT Quality Space as the graded tensor algebra
over the 6D coordinate space R^6 = E_parallel (+) E_perp:
    - linear sector    R^6        = T_1 (+) T_2                  (6 DOF; the two 3-D irreps)
    - quadratic sector Sym^2(R^6) = 2 A_g (+) G_g (+) 3 H_g      (21 DOF; no 3-D irrep)
for a graded total of 6 + 21 = 27 DOF. Modality map (Tier 3): T_2 = E_perp -> color,
T_1 = E_parallel -> spatial/auditory (linear); 2 A_g -> valence/intensity,
G_g + 3 H_g -> olfaction/chemical (quadratic).

This protocol derives both sectors from character theory and confirms the
manuscript's decomposition. The 6D
cut-and-project representation is V = E_parallel (+) E_perp = T_1 (+) T_2 (the two
3D icosahedral irreps; the manuscript's own E_parallel = T_1, E_perp = T_2). The
icosahedral rotation group I ~ A_5 has irreps A(1), T_1(3), T_2(3), G(4), H(5)
with character table over classes [E, 15 C_2, 20 C_3, 12 C_5, 12 C_5^2]:
    A   : (1,  1,  1,    1,    1)
    T_1 : (3, -1,  0,  phi, -1/phi)
    T_2 : (3, -1,  0, -1/phi,  phi)
    G   : (4,  0,  1,   -1,   -1)
    H   : (5,  1, -1,    0,    0)
class sizes g = (1, 15, 20, 12, 12);  phi = (1+sqrt5)/2.

We compute chi_V = chi_{T_1}+chi_{T_2}, then chi_{Sym^2}(g) = (chi_V(g)^2 +
chi_V(g^2))/2, and decompose. Cross-check via Sym^2(T_1(+)T_2) =
Sym^2(T_1) (+) Sym^2(T_2) (+) (T_1 (x) T_2).
"""

import json
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

try:
    from gct_utils import get_output_path, C
    _PHI_FROM_SSOT = float(C.PHI)
except Exception:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    try:
        from gct_utils import get_output_path, C
        _PHI_FROM_SSOT = float(C.PHI)
    except Exception:
        _PHI_FROM_SSOT = (1 + 5 ** 0.5) / 2
        def get_output_path(fn):
            return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", fn)

PHI = _PHI_FROM_SSOT
IPHI = 1.0 / PHI
CLASS_SIZES = [1, 15, 20, 12, 12]          # E, C2, C3, C5, C5^2
ORDER = 60
IRREPS = {
    "A":   [1, 1, 1, 1, 1],
    "T_1": [3, -1, 0, PHI, -IPHI],
    "T_2": [3, -1, 0, -IPHI, PHI],
    "G":   [4, 0, 1, -1, -1],
    "H":   [5, 1, -1, 0, 0],
}
# g^2 maps each class -> class index: E->E, C2->E, C3->C3, C5->C5^2, C5^2->C5
SQUARE_CLASS = [0, 0, 2, 4, 3]


def decompose(chi):
    """Return {irrep: multiplicity} for a class-function chi (len 5)."""
    out = {}
    for name, ch in IRREPS.items():
        m = sum(CLASS_SIZES[i] * chi[i] * ch[i] for i in range(5)) / ORDER
        out[name] = int(round(m))
        assert abs(out[name] - m) < 1e-9, f"non-integer multiplicity for {name}: {m}"
    return out


def char_product(a, b):
    return [a[i] * b[i] for i in range(5)]


def sym2_char(chiV):
    return [(chiV[i] ** 2 + chiV[SQUARE_CLASS[i]]) / 2 for i in range(5)]


def fmt(dec):
    order = ["A", "T_1", "T_2", "G", "H"]
    dims = {"A": 1, "T_1": 3, "T_2": 3, "G": 4, "H": 5}
    parts = [f"{dec[k]} {k}({dims[k]})" for k in order if dec.get(k, 0)]
    total = sum(dec.get(k, 0) * dims[k] for k in order)
    return " + ".join(parts) + f"   [dim {total}]"


def run():
    print("=" * 72)
    print("GCT Protocol B1 - Graded Quality-Space irrep decomposition")
    print("=" * 72)

    chi_T1, chi_T2 = IRREPS["T_1"], IRREPS["T_2"]
    chi_V = [chi_T1[i] + chi_T2[i] for i in range(5)]
    print(f"\n  6D rep V = T_1 (+) T_2 : chi_V = {[round(x,4) for x in chi_V]}  (dim {chi_V[0]:.0f})")

    chi_sym2 = sym2_char(chi_V)
    print(f"  chi_Sym^2(V)          : {[round(x,4) for x in chi_sym2]}  (dim {chi_sym2[0]:.0f})")
    dec = decompose(chi_sym2)
    print(f"\n  CORRECT decomposition : Sym^2(R^6) = {fmt(dec)}")

    # cross-check building blocks
    sym2_T1 = decompose(sym2_char(chi_T1))
    sym2_T2 = decompose(sym2_char(chi_T2))
    t1t2 = decompose(char_product(chi_T1, chi_T2))
    print(f"\n  Cross-check (Sym^2(T_1(+)T_2) = Sym^2 T_1 (+) Sym^2 T_2 (+) T_1(x)T_2):")
    print(f"    Sym^2(T_1) = {fmt(sym2_T1)}")
    print(f"    Sym^2(T_2) = {fmt(sym2_T2)}")
    print(f"    T_1 (x) T_2 = {fmt(t1t2)}")
    combined = {k: sym2_T1.get(k,0)+sym2_T2.get(k,0)+t1t2.get(k,0) for k in IRREPS}
    print(f"    sum        = {fmt(combined)}")
    assert combined == dec, "cross-check mismatch!"

    # Graded Quality-Space assembly: the linear coordinate sector R^6 carries the
    # two 3-D irreps (E_parallel = T_1, E_perp = T_2); the quadratic stress sector
    # Sym^2(R^6) carries 2A_g (+) G_g (+) 3H_g. The full graded quality space is
    # R^6 (+) Sym^2(R^6) = 6 + 21 = 27 DOF. The load-bearing distinction is the
    # tensor grading: the coordinate modes and their symmetric square are genuinely
    # distinct representations, so the two 3-D irreps live in the linear sector
    # (vision/spatial-auditory) and never in the quadratic stress sector (valence/
    # intensity/olfaction). The rotation group I computed here has no inversion, so
    # only the dimensional content (not any g/u inversion-parity label) is asserted
    # by this engine; the inversion parity of the coordinate vector sector is fixed
    # by the gauge-sector conventions (App ZN), not by this protocol.
    lin = decompose(chi_V)            # R^6 itself
    print(f"\n  Linear sector R^6     : {fmt(lin)}")
    n_3d_linear = lin.get("T_1", 0) + lin.get("T_2", 0)
    graded_dof = chi_V[0] + chi_sym2[0]
    print(f"  Quadratic sector      : Sym^2(R^6) = {fmt(dec)}")
    print(f"  GRADED Quality Space  : R^6 (+) Sym^2(R^6) = {chi_V[0]:.0f} + {chi_sym2[0]:.0f} = {graded_dof:.0f} DOF")
    print(f"    3-D irreps in linear sector R^6 (vision T_2/E_perp + spatial-auditory T_1/E_par): {n_3d_linear}")

    # Manuscript quadratic-sector decomposition (Ch16 §16.2.2c / §16.4):
    # Sym^2(R^6) = 2 A_g + G_g + 3 H_g. This engine is the source of that
    # decomposition; the check below confirms the engine reproduces it.
    manuscript_quadratic_claim = {"A": 2, "T_1": 0, "T_2": 0, "G": 1, "H": 3}
    print(f"\n  Manuscript quadratic-sector claim : Sym^2(R^6) = {fmt(manuscript_quadratic_claim)}")
    matches = (manuscript_quadratic_claim == dec)
    has_3d = dec.get("T_1", 0) + dec.get("T_2", 0)
    n_Ag = dec.get("A", 0)

    print("\n  " + "-" * 64)
    print(f"  3-D irrep (T_1/T_2) multiplicity in Sym^2(R^6): {has_3d}  "
          f"(the two 3-D irreps occur in the linear sector R^6, not in Sym^2)")
    print(f"  A_g (trivial / independent-constant) multiplicity: {n_Ag}  "
          f"(matches textbook 'icosahedral -> 2 independent elastic constants')")
    print(f"  Manuscript quadratic-sector claim matches the computed decomposition: {matches}")

    verdict = (
        "CONFIRMED: Sym^2(R^6) under the icosahedral group decomposes as "
        "2 A_g (+) G_g (+) 3 H_g (2+4+15 = 21), verified two ways (direct Sym^2 "
        "character and the Sym^2 T_1 (+) Sym^2 T_2 (+) T_1(x)T_2 cross-check), in "
        "agreement with the manuscript's quadratic-sector claim (Ch16 §16.2.2c / "
        "§16.4). The symmetric stress tensor contains NO 3-D irrep (T_1, T_2 "
        "multiplicity 0); the two 3-D irreps occur in the linear coordinate sector "
        "R^6 = E_parallel (+) E_perp = T_1 (+) T_2, so the graded Quality Space is "
        "R^6 (+) Sym^2(R^6) = 6 + 21 = 27 DOF. Color/spatial-auditory attach to the "
        "linear coordinate irreps (T_2 = E_perp, T_1 = E_parallel); valence/intensity "
        "and olfaction/chemical attach to the quadratic stress irreps (2 A_g, "
        "G_g + 3 H_g). The modality-to-irrep assignment is Tier 3."
        if (matches and has_3d == 0 and n_Ag == 2) else
        "Unexpected result -- review.")
    print("\n  VERDICT:", verdict)
    print("=" * 72)

    results = {
        "object": "Sym^2(R^6), 21-DOF symmetric stress tensor, icosahedral group",
        "chi_V": chi_V, "chi_Sym2": chi_sym2,
        "correct_decomposition": dec,
        "correct_decomposition_str": "2 A_g + G_g + 3 H_g",
        "linear_sector_R6": lin,
        "linear_sector_R6_str": "T_1 (E_par) + T_2 (E_perp)",
        "graded_quality_space_str": "R^6 (+) Sym^2(R^6) = 6 + 21 = 27 DOF",
        "graded_quality_space_dof": graded_dof,
        "n_3D_irreps_in_linear_R6": n_3d_linear,
        "crosscheck_sym2_T1": sym2_T1, "crosscheck_sym2_T2": sym2_T2,
        "crosscheck_T1xT2": t1t2,
        "manuscript_claim": manuscript_quadratic_claim,
        "manuscript_claim_str": "Sym^2(R^6) = 2 A_g + G_g + 3 H_g (quadratic); R^6 = T_1 + T_2 (linear)",
        "manuscript_claim_correct": bool(matches),
        "n_3D_irreps_in_Sym2": has_3d,
        "n_Ag_in_Sym2": n_Ag,
        "verdict": verdict,
    }
    out = get_output_path("protocol_b1_quality_space_irreps_results.json")
    with open(out, "w") as fp:
        json.dump(results, fp, indent=2)
    print(f"\n[Saved JSON] -> {out}")
    return results


if __name__ == "__main__":
    run()
