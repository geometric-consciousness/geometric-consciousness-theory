#!/usr/bin/env python3
"""
protocol_hadron_topology.py — Hadron-Sector Topological Checks
=================================================================
Numerical checks for the hadron-sector readings of lattice topology: the
Strange Quark drag coefficient (12α) and the φ⁻¹ CKM/CP exponents.

The lattice counts and holonomy arithmetic below are exact. Their physical
readings are not established here: the 12α strange-quark drag carries Tier 2
mechanism status (conditional on the Tier 3 face-defect quark assignment) with a
Tier 3 coefficient identification, and the φ⁻¹ CKM
exponents and the CP phase are Tier 3 ansätze (App PSC §PSC.4). The four
checks verify the arithmetic each reading uses.

Check I   — Z⁶ Coordination Number
    The Z⁶ hypercubic bulk lattice has exactly Z = 12 nearest-neighbour
    bonds per vertex (±e_k, k = 1…6).  This is the drag channel count
    available to an *unpinned* face defect (quark) moving through the bulk.

Check II  — CKM φ⁻¹ Exponent via SU(2) Face-Defect Holonomy
    A quark (face defect) undergoing flavour-changing face-tunneling is
    transported across the SU(2)_L weak bundle by the identical 2π loop
    that generates the Baryonic Berry Phase in protocol_proton_berry_phase.
    Under the Tier 3 ansatz the holonomy correction is taken as identical: φ_correction = φ⁻¹.

Check III — Strange Quark 12α Drag Coefficient
    The drag on an unpinned face defect is proportional to the number of
    bulk bonds broken per lattice step.  In Z⁶: Z_bulk = 12.
    The muon (vertex defect) is confined to 5 icosahedral channels.
    Therefore: C_drag(strange) = 12·α, and C_drag(muon) = 5·α.
    Ratio = 12/5 = 2.4 — a channel-count ratio under the Tier 3 drag reading.

Check IV  — CP Phase Radians (Jackiw–Rebbi Boundary Twist)
    Under the Tier 3 ansatz, the CP-violating phase is read as the Jackiw–Rebbi zero-mode accumulated by the
    full dodecahedral quasicrystal boundary twist, modulated by the φ⁻¹
    holonomy: δ_CP = 2π·φ⁻¹ radians ≈ 222.49°.

PASS criterion
--------------
Check II previously passed on (1/2)*(2*phi^-1) == phi^-1,
which holds because R = 2*phi^-1 is typed in; that comparison is retired and
recorded as an input. Check II gates on the verifier's 0.5% CKM band for
s23 and s13, with the PDG 2024 targets read from the SSOT (config/gct_constants.yaml
S23_CKM, S13_CKM; the same values as verify_independent/constants.py). s13 lies
inside the gate (about 76 ppm); s23 misses GCT's own 0.5% gate (0.98%), about
0.6 sigma from the PDG central value, so the registered tension is a miss of the
precision gate, not a clash with data. Check III repeats the Check I count
(Z = 12) and Check IV uses a 296-degree window; both are recorded, but neither
is evidence on its own.

Output
------
  data/protocol_hadron_topology_results.json
"""

import sys
import json
import math
import numpy as np
from pathlib import Path

# ---------------------------------------------------------------------------
# Path bootstrap — ensure src/ is importable from any cwd
# ---------------------------------------------------------------------------
_SRC = Path(__file__).resolve().parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from gct_utils import get_output_path, C
from gct_projections import get_m_parallel, get_m_perp

# Import the exact SU(2) Berry Phase machinery — immutable canonical source.
from protocol_proton_berry_phase import (
    compute_su2_holonomy,
    verify_minus_identity,
    compute_berry_correction,
)


# ============================================================================
# JSON Encoder (numpy-safe)
# ============================================================================

class _NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer,)):  return int(obj)
        if isinstance(obj, (np.floating,)): return float(obj)
        if isinstance(obj, (np.bool_,)):    return bool(obj)
        if isinstance(obj, np.ndarray):     return obj.tolist()
        return super().default(obj)


# ============================================================================
# SECTION 1 — Constants
# ============================================================================

PHI      = float(C.PHI)          # golden ratio φ = (1+√5)/2 ≈ 1.6180339887
INV_PHI  = 1.0 / PHI             # φ⁻¹ = φ − 1 ≈ 0.6180339887
ALPHA    = float(C.ALPHA_OBS)    # fine structure constant α ≈ 7.2974e-3

# Z⁶ lattice dimension — the GCT parent bulk
DIM_Z6 = 6

# Icosahedral channels available to a vertex defect (Muon):
# The 5 pentagonal faces meeting at each dodecahedral vertex.
N_ICOSAHEDRAL_CHANNELS = 5

# SU(2) Pauli matrices (needed for holonomy, imported from berry phase module)
I2       = np.eye(2, dtype=complex)

# Number of path-ordered steps for holonomy (match proton Berry phase for consistency)
N_HOLONOMY_STEPS = 10_000


# ============================================================================
# SECTION 2 — Check I: Z⁶ Coordination Number Z = 12
# ============================================================================

def derive_z6_coordination_number() -> dict:
    """
    Check I [Tier 1 lattice count]: the Z⁶ hypercubic lattice has coordination number Z = 12.

    Proof
    -----
    The Z⁶ lattice is the integer lattice in R⁶ with basis {e_1, …, e_6}.
    The nearest neighbours of any vertex v ∈ Z⁶ are all w ∈ Z⁶ such that
    ||w − v||² = 1, i.e., w = v ± e_k for k ∈ {1, …, 6}.

    Number of such neighbours:
        Z = card{±e_k : k = 1, …, 6} = 2 × 6 = 12.

    This is the coordination number of the Z^n hypercubic lattice in general
    (Z = 2n), evaluated at n = 6.  It is also the value already hard-coded
    in gct_lattice.py's get_neighbors() method (12 direction vectors).

    For an *unpinned* face defect (quark) propagating through the 6D bulk
    rather than the 3D quasicrystal surface, all 12 bulk bonds are proposed to be
    accessible. Under that reading the drag coefficient is:
        C_drag = Z_bulk × α = 12 × α.
    """
    # Enumerate the 12 nearest-neighbour displacement vectors in Z⁶
    basis = np.eye(DIM_Z6, dtype=int)                   # (6, 6)
    nn_directions = np.vstack([basis, -basis])           # (12, 6)

    # Verify: every displacement has squared norm = 1
    sq_norms = np.sum(nn_directions ** 2, axis=1)        # (12,)
    all_unit_length = bool(np.all(sq_norms == 1))

    Z = len(nn_directions)                               # 12

    # Cross-check: 2 × dim(Z⁶) = 2 × 6 = 12
    analytic_Z = 2 * DIM_Z6
    analytic_match = (Z == analytic_Z)

    return {
        "lattice":              "Z⁶ hypercubic bulk",
        "dimension":            DIM_Z6,
        "nn_directions_count":  Z,
        "analytic_formula":     "2 × dim = 2 × 6 = 12",
        "analytic_Z":           analytic_Z,
        "all_directions_unit":  all_unit_length,
        "analytic_match":       analytic_match,
        "PASS":                 analytic_match and all_unit_length,
    }


# ============================================================================
# SECTION 3 — Check II: CKM φ⁻¹ via Face-Defect SU(2) Holonomy
# ============================================================================

def derive_ckm_phi_inv() -> dict:
    """
    Check II [Tier 3 ansatz]: the proposed CKM φ⁻¹ exponent reuses the
    Baryonic Berry Phase correction, on the hypothesis that both originate
    from the same SU(2)_L weak gauge field transporting a topological defect
    around a 2π circuit of the 5-fold axis.

    Computation
    -----------
    The baryonic circuit (Proton, the face-defect baryonic triad) was computed in
    protocol_proton_berry_phase.py to yield U_weak = −I₂ (Berry phase π),
    giving φ⁻¹ correction = N_weak × R = (1/2) × (2/φ) = φ⁻¹.

    Hypothesis: the quark (face defect) undergoes *flavour-changing
    face-tunneling*, mediated by the same SU(2)_L gauge field, so that
    the weak bundle structure is shared — the 5-fold dodecahedral axis
    governs both the baryonic-triad circuit (face defects around the 5-fold
    vertex star) and face-defect tunneling (inter-generation mixing).

    The loop in both cases is:
        θ ∈ [0, 2π], A_θ = (1/2)·σ_z  [canonical SU(2) spin-1/2 connection]

    Under this hypothesis U_weak = exp(i·π·σ_z) = −I₂ for both defect types.
    The projection ratio R = 2·φ⁻¹ (pentagon edge-to-diagonal) is a property
    of the ambient icosahedral geometry, not of the defect species.

    Proposed CKM exponents (Tier 3 ansatz):
        s23 = φ^{−(6 + φ⁻¹)}     [3rd generation, double pentagon winding]
        s13 = φ^{−(11 + φ⁻¹)}    [1st↔3rd crossing, triple pentagon winding]
    """
    # Reuse the exact same holonomy computation as the Berry Phase protocol
    U_weak = compute_su2_holonomy(n_steps=N_HOLONOMY_STEPS)
    deviation, minus_id_pass = verify_minus_identity(U_weak, tol=1e-9)
    berry_data = compute_berry_correction(U_weak)

    phi_correction = berry_data["phi_correction"]
    phi_inv_ref    = INV_PHI
    corr_match     = bool(abs(phi_correction - phi_inv_ref) < 1e-9)

    # CKM exponent fractions
    s23_exponent = 6.0 + phi_correction
    s13_exponent = 11.0 + phi_correction

    # Predicted mixing element magnitudes
    s23_pred = PHI ** (-s23_exponent)
    s13_pred = PHI ** (-s13_exponent)

    # PDG 2024 targets (RPP CKM review eq. 12.28), read from the SSOT
    s23_target = float(C.S23_CKM)            # 0.04183 rounded to 0.0418
    s13_target = float(C.S13_CKM)            # 0.003732
    s23_full   = float(C.S23_CKM_PDG2024_FULL)
    s23_sig_lo = float(C.S23_CKM_PDG2024_ERR_MINUS)

    s23_err_pct = abs(s23_pred - s23_target) / s23_target * 100.0
    s13_err_pct = abs(s13_pred - s13_target) / s13_target * 100.0
    CKM_BAND_PCT = 0.5   # same 0.5% band as verify_independent/verify_ckm.py

    return {
        "U_weak_trace":           float(np.trace(U_weak).real),
        "holonomy_deviation":     float(deviation),
        "U_weak_is_minus_I2":     minus_id_pass,
        "Berry_phase_rad":        berry_data["Berry_phase_rad"],
        "N_weak":                 berry_data["N_weak"],
        "R_projection":           berry_data["R_projection"],
        "phi_correction":         float(phi_correction),
        "phi_inv_reference":      float(phi_inv_ref),
        "phi_correction_matches_phi_inv": corr_match,
        "s23_exponent":           float(s23_exponent),
        "s13_exponent":           float(s13_exponent),
        "s23_predicted":          float(s23_pred),
        "s23_target_PDG":         s23_target,
        "s23_error_pct":          float(s23_err_pct),
        "s23_target_PDG_unrounded": s23_full,
        "s23_error_pct_vs_unrounded": float(abs(s23_pred - s23_full) / s23_full * 100.0),
        "s23_sigma_from_PDG":     float(abs(s23_pred - s23_full) / s23_sig_lo),
        "s13_predicted":          float(s13_pred),
        "s13_target_PDG":         s13_target,
        "s13_error_pct":          float(s13_err_pct),
        "s13_error_ppm":          float(s13_err_pct * 1.0e4),
        "phi_correction_status":  "INPUT: R_projection = 2*phi^-1 is typed, so N_weak*R = phi^-1 holds by construction",
        "ckm_band_pct":           CKM_BAND_PCT,
        "s23_within_band":        bool(s23_err_pct < CKM_BAND_PCT),
        "s13_within_band":        bool(s13_err_pct < CKM_BAND_PCT),
        "PASS":                   bool(minus_id_pass and s23_err_pct < CKM_BAND_PCT and s13_err_pct < CKM_BAND_PCT),
    }


# ============================================================================
# SECTION 4 — Check III: Strange Quark 12α Drag Coefficient
# ============================================================================

def derive_strange_drag(z6_data: dict, ckm_data: dict) -> dict:
    """
    Check III: the proposed Strange Quark drag coefficient 12α, read from
    the Z⁶ bulk coordination number (Tier 2 mechanism, conditional on the
    Tier 3 face-defect assignment; Tier 3 coefficient identification, App PSC §PSC.4).

    Reasoning
    ---------
    Topological drag on a lattice defect is a frictional coupling to the
    surrounding lattice oscillators (phonons/phasons).  The drag coefficient
    scales with the number of active coupling channels.

    Two defect species, two channel counts:

    1. Vertex Defect (Muon/Lepton):
       Pinned to the icosahedral quasicrystal surface in 3D.
       Couples through the 5 pentagonal faces of the local icosahedral
       neighbourhood (5-fold symmetry axis of the dodecahedron).
       → C_drag(vertex) = 5 × α
       → Lepton correction factor: (1 − 5α)

    2. Face Defect (Quark) — UNPINNED:
       Under the Tier 3 face-defect assignment (V3 Ch03 §3.4), the quark is an interstitial face defect NOT pinned to the
       3D quasicrystal surface.  It interacts with the 6D bulk lattice.
       In the Z⁶ parent lattice, every site has 12 nearest-neighbour bonds
       (Check I: Z = 2 × 6 = 12).
       → C_drag(face) = 12 × α
       → Strange quark correction factor: (1 − 12α)

    The ratio of drag coefficients:
        12 / 5 = 2.4   [channel-count ratio — no additional fitted coefficient]

    Numerical verification
    ----------------------
    The strange quark mass formula currently used is:
        m_s = m_u × φ^8 × (1 − 12α)    [protocol_quark_mismatch.py strange-mass branch]

    We verify that the 12 in the suppression factor is *exactly* the Z⁶
    coordination number derived in Check I, to machine precision.
    """
    Z_bulk = z6_data["nn_directions_count"]       # 12 (from Check I)
    Z_icosahedral = N_ICOSAHEDRAL_CHANNELS        # 5

    # Drag coefficients
    drag_face_defect   = Z_bulk * ALPHA           # 12α
    drag_vertex_defect = Z_icosahedral * ALPHA    # 5α
    drag_ratio         = Z_bulk / Z_icosahedral   # 12/5 = 2.4

    # Cross-check: 12 must match the Z⁶ coordination number exactly
    coord_number_match = bool(Z_bulk == 12)

    # Suppression factors
    suppression_strange = 1.0 - drag_face_defect    # (1 − 12α) — used in m_s
    suppression_muon    = 1.0 - drag_vertex_defect  # (1 − 5α)  — used in m_e/m_mu

    return {
        "Z6_coordination_number":      Z_bulk,
        "icosahedral_channels_muon":   Z_icosahedral,
        "drag_channel_ratio":          float(drag_ratio),
        "drag_channel_ratio_formula":  "Z_bulk / Z_icosahedral = 12 / 5 = 2.4",
        "alpha":                       float(ALPHA),
        "12_alpha_value":              float(drag_face_defect),
        "5_alpha_value":               float(drag_vertex_defect),
        "suppression_strange_quark":   float(suppression_strange),
        "suppression_muon_lepton":     float(suppression_muon),
        "coord_number_exact_12":       coord_number_match,
        "repeat_of_check_I":           True,
        "PASS":                        coord_number_match,
    }


# ============================================================================
# SECTION 5 — Check IV: CP Phase in Radians (Jackiw–Rebbi)
# ============================================================================

def derive_cp_phase(ckm_data: dict) -> dict:
    """
    Check IV [Tier 3 ansatz]: the proposed CP-violating phase δ_CP = 2π·φ⁻¹ radians.

    Proposed Mechanism — Jackiw–Rebbi Boundary Twist
    -------------------------------------------------
    The dodecahedral quasicrystal tiling has a topological boundary.  When
    a face defect (quark) is transported around the full boundary, it
    accumulates a geometrical phase from the Jackiw–Rebbi zero-mode.

    The Jackiw–Rebbi mechanism: a domain wall in a 1D topological field
    theory supports a zero-energy bound state.  When the defect winds around
    the 3D quasicrystal boundary, the zero-mode contributes a boundary twist
    proportional to the Berry holonomy.

    Full boundary twist = 2π (one complete winding of the dodecahedral surface)
    Holonomy modulation = φ⁻¹ (from Check II — the SU(2) projection ratio)

    Under this proposal:
        δ_CP = 2π × φ⁻¹  [radians]
             = 360° × φ⁻¹  [degrees]

    Cross-check: this matches the CP phase in protocol_mixing_geometry.py
    (360 × φ⁻¹ degrees), reproduced here from the proposed boundary-twist holonomy.

    PDG 2024 best fit: δ_CP ≈ 222° (NO range: 108°–404°).
    Tier 3 ansatz:     δ_CP = 360·φ⁻¹ ≈ 222.49°  [within 1-sigma]
    """
    phi_inv       = ckm_data["phi_correction"]   # φ⁻¹ from Check II

    delta_cp_rad  = 2.0 * math.pi * phi_inv      # 2π·φ⁻¹
    delta_cp_deg  = 360.0 * phi_inv              # 360°·φ⁻¹

    # PDG 2024 central value and range
    delta_cp_PDG_deg        = 222.0   # degrees (NO best fit 2024)
    delta_cp_PDG_range_low  = 108.0
    delta_cp_PDG_range_high = 404.0

    within_pdg_range = bool(delta_cp_PDG_range_low <= delta_cp_deg <= delta_cp_PDG_range_high)
    error_pct = abs(delta_cp_deg - delta_cp_PDG_deg) / delta_cp_PDG_deg * 100.0

    # Verify radian formula matches degree formula (consistency check)
    delta_cp_rad_from_deg = math.radians(delta_cp_deg)
    radian_consistency = bool(abs(delta_cp_rad - delta_cp_rad_from_deg) < 1e-12)

    return {
        "phi_inv":                    float(phi_inv),
        "formula_radians":            "2π × φ⁻¹",
        "formula_degrees":            "360 × φ⁻¹",
        "delta_cp_rad":               float(delta_cp_rad),
        "delta_cp_deg":               float(delta_cp_deg),
        "delta_cp_PDG_deg":           float(delta_cp_PDG_deg),
        "delta_cp_PDG_range_low_deg": float(delta_cp_PDG_range_low),
        "delta_cp_PDG_range_high_deg":float(delta_cp_PDG_range_high),
        "within_PDG_1sigma_range":    within_pdg_range,
        "error_from_PDG_central_pct": float(error_pct),
        "jackiw_rebbi_mechanism":     (
            "Tier 3 ansatz: full dodecahedral boundary winding (2π) × φ⁻¹ holonomy "
            "(Check II SU(2) projection ratio) = δ_CP"
        ),
        "radian_degree_consistent":   radian_consistency,
        "window_note":                "The 108-404 degree window spans 296 degrees; most random phases fall inside it, so this check is weak.",
        "PASS":                       within_pdg_range and radian_consistency,
    }


# ============================================================================
# SECTION 6 — Projection Matrix Verification (E8 → Z⁶ → H₃)
# ============================================================================

def verify_projection_geometry() -> dict:
    """
    Structural verification: the AKN projection matrices encode the φ-scale
    hierarchy between E_parallel (physical space) and E_perp (phason bulk).

    The E⁸ root system decomposes into two H₃ copies under the Z[φ] module
    structure. The cut-and-project selects the Z⁶ sublattice that maps onto
    the Ammann icosahedral quasicrystal (H₃ tiling) in E_parallel.

    We verify the completeness identity M_∥ᵀM_∥ + M_⊥ᵀM_⊥ = I₆, which
    confirms that the parent is genuinely 6D (not a lower-dimensional embed).
    """
    M_para = get_m_parallel()    # (3, 6)
    M_perp = get_m_perp()        # (3, 6)
    I6     = np.eye(6)

    completeness = M_para.T @ M_para + M_perp.T @ M_perp
    completeness_err = float(np.max(np.abs(completeness - I6)))
    completeness_ok  = completeness_err < 1e-12

    orth = M_para @ M_perp.T    # (3, 3), zero by orthogonality.
    orth_err = float(np.max(np.abs(orth)))
    orth_ok  = orth_err < 1e-12

    return {
        "M_para_shape":                list(M_para.shape),
        "M_perp_shape":                list(M_perp.shape),
        "completeness_max_err":        completeness_err,
        "completeness_I6_verified":    completeness_ok,
        "orthogonality_max_err":       orth_err,
        "orthogonality_verified":      orth_ok,
        "PASS":                        completeness_ok and orth_ok,
    }


# ============================================================================
# MAIN
# ============================================================================

def main() -> int:
    print("=" * 72)
    print("  Hadron Topology Protocol: Lattice Topological Derivations")
    print("  Deriving 12α and φ⁻¹ from Lattice Topology")
    print("=" * 72)
    print(f"\n  φ          = {PHI:.10f}")
    print(f"  φ⁻¹        = {INV_PHI:.10f}")
    print(f"  α          = {ALPHA:.13f}")
    print(f"  12α        = {12 * ALPHA:.13f}")

    # ------------------------------------------------------------------
    # Check I — Z⁶ Coordination Number
    # ------------------------------------------------------------------
    print("\n" + "─" * 72)
    print("  THEOREM I — Z⁶ Coordination Number: The Source of 12α")
    print("─" * 72)
    z6 = derive_z6_coordination_number()
    print(f"  Z⁶ dimension              : {z6['dimension']}")
    print(f"  Nearest-neighbour formula : {z6['analytic_formula']}")
    print(f"  Enumerated NN directions  : {z6['nn_directions_count']}")
    print(f"  All directions ||·||² = 1 : {z6['all_directions_unit']}")
    print(f"  Analytic match (2d = 12)  : {z6['analytic_match']}")
    t1 = "PASS" if z6["PASS"] else "FAIL"
    print(f"\n  Check I Verdict         : [{t1}]")

    # ------------------------------------------------------------------
    # Check II — CKM φ⁻¹ Holonomy
    # ------------------------------------------------------------------
    print("\n" + "─" * 72)
    print("  CHECK II [Tier 3 ansatz] — CKM φ⁻¹ via Face-Defect SU(2) Holonomy")
    print("─" * 72)
    print(f"  Reusing exact SU(2) machinery from protocol_proton_berry_phase")
    print(f"  Loop: 2π circuit, connection A_θ = (1/2)σ_z, N={N_HOLONOMY_STEPS} steps")
    ckm = derive_ckm_phi_inv()
    print(f"\n  U_weak trace              : {ckm['U_weak_trace']:.10f}  (expected -2.0)")
    print(f"  U_weak = −I₂              : {ckm['U_weak_is_minus_I2']}")
    print(f"  Berry phase γ             : {ckm['Berry_phase_rad']:.10f} rad  (expected π)")
    print(f"  Winding N_weak            : {ckm['N_weak']:.10f}  (expected 0.5)")
    print(f"  Projection R = 2·φ⁻¹     : {ckm['R_projection']:.10f}")
    print(f"  φ_correction = N·R        : {ckm['phi_correction']:.10f}")
    print(f"  φ⁻¹ reference             : {ckm['phi_inv_reference']:.10f}")
    print(f"  Match (tol 1e-9)          : {ckm['phi_correction_matches_phi_inv']}")
    print(f"\n  → s23 exponent = 6 + φ⁻¹ : {ckm['s23_exponent']:.10f}")
    print(f"    s23 ansatz value        : {ckm['s23_predicted']:.6f}  (PDG: {ckm['s23_target_PDG']})")
    print(f"    s23 error               : {ckm['s23_error_pct']:.2f}%")
    print(f"\n  → s13 exponent = 11 + φ⁻¹: {ckm['s13_exponent']:.10f}")
    print(f"    s13 ansatz value        : {ckm['s13_predicted']:.6f}  (PDG: {ckm['s13_target_PDG']})")
    print(f"    s13 error               : {ckm['s13_error_pct']:.2f}%")
    print(f"    0.5% CKM band gate      : s23 {ckm['s23_within_band']}, s13 {ckm['s13_within_band']}")
    t2 = "PASS" if ckm["PASS"] else "FAIL"
    print(f"\n  Check II Verdict        : [{t2}]")

    # ------------------------------------------------------------------
    # Check III — Strange Quark 12α Drag
    # ------------------------------------------------------------------
    print("\n" + "─" * 72)
    print("  CHECK III [Tier 3 coefficient identification] — Strange Quark 12α Drag Coefficient")
    print("─" * 72)
    drag = derive_strange_drag(z6, ckm)
    print(f"  Z⁶ bulk coordination (Z)  : {drag['Z6_coordination_number']}  [Check I]")
    print(f"  Icosahedral channels (μ)  : {drag['icosahedral_channels_muon']}  [5-fold vertex]")
    print(f"  Drag ratio (quark/muon)   : {drag['drag_channel_ratio']:.4f}  = 12/5 [geometric]")
    print(f"  α                         : {drag['alpha']:.13f}")
    print(f"  12·α (quark drag)         : {drag['12_alpha_value']:.13f}")
    print(f"  5·α  (muon  drag)         : {drag['5_alpha_value']:.13f}")
    print(f"  (1 − 12α) strange factor  : {drag['suppression_strange_quark']:.13f}")
    print(f"  (1 −  5α) lepton factor   : {drag['suppression_muon_lepton']:.13f}")
    print(f"  Z = 12 exact integer match: {drag['coord_number_exact_12']}")
    t3 = "PASS" if drag["PASS"] else "FAIL"
    print(f"\n  Check III Verdict       : [{t3}]")

    # ------------------------------------------------------------------
    # Check IV — CP Phase in Radians
    # ------------------------------------------------------------------
    print("\n" + "─" * 72)
    print("  CHECK IV [Tier 3 ansatz] — CP Phase δ_CP = 2π·φ⁻¹ (Jackiw–Rebbi)")
    print("─" * 72)
    cp = derive_cp_phase(ckm)
    print(f"  φ⁻¹ holonomy (Check II) : {cp['phi_inv']:.10f}")
    print(f"  δ_CP formula (radians)    : {cp['formula_radians']}")
    print(f"  δ_CP formula (degrees)    : {cp['formula_degrees']}")
    print(f"  δ_CP                      : {cp['delta_cp_rad']:.10f} rad")
    print(f"  δ_CP                      : {cp['delta_cp_deg']:.6f}°")
    print(f"  PDG 2024 central          : {cp['delta_cp_PDG_deg']:.1f}°")
    print(f"  PDG 2024 allowed range    : [{cp['delta_cp_PDG_range_low_deg']:.0f}°, "
          f"{cp['delta_cp_PDG_range_high_deg']:.0f}°]")
    print(f"  Error from PDG central    : {cp['error_from_PDG_central_pct']:.2f}%")
    print(f"  Within PDG range          : {cp['within_PDG_1sigma_range']}")
    print(f"  Radian/degree consistent  : {cp['radian_degree_consistent']}")
    print(f"  Jackiw–Rebbi link:")
    print(f"    {cp['jackiw_rebbi_mechanism']}")
    t4 = "PASS" if cp["PASS"] else "FAIL"
    print(f"\n  Check IV Verdict        : [{t4}]")

    # ------------------------------------------------------------------
    # Projection Geometry Verification
    # ------------------------------------------------------------------
    print("\n" + "─" * 72)
    print("  AUXILIARY — E8 → Z⁶ → H₃ Projection Completeness Verification")
    print("─" * 72)
    proj_check = verify_projection_geometry()
    print(f"  M_∥ shape                 : {proj_check['M_para_shape']}")
    print(f"  M_⊥ shape                 : {proj_check['M_perp_shape']}")
    print(f"  Completeness max error    : {proj_check['completeness_max_err']:.2e}")
    print(f"  M_∥ᵀM_∥ + M_⊥ᵀM_⊥ = I₆  : {proj_check['completeness_I6_verified']}")
    print(f"  M_∥ M_⊥ᵀ = 0₃ₓ₃          : {proj_check['orthogonality_verified']}")
    tp = "PASS" if proj_check["PASS"] else "FAIL"
    print(f"\n  Projection Verdict        : [{tp}]")

    # ------------------------------------------------------------------
    # Final Verdict
    # ------------------------------------------------------------------
    all_theorems = [z6["PASS"], ckm["PASS"], drag["PASS"], cp["PASS"], proj_check["PASS"]]
    all_pass = all(all_theorems)
    failing = [k for k in ("s23", "s13") if not ckm[f"{k}_within_band"]]
    verdict  = ("PASS" if all_pass
                else ("CKM_" + "_".join(k.upper() for k in failing)
                      + "_EXPONENT_OUTSIDE_0P5PCT_GATE"
                      + f"_s23={ckm['s23_error_pct']:.2f}pct_s13={ckm['s13_error_pct']:.4f}pct")
                if (not ckm["PASS"] and failing and ckm["U_weak_is_minus_I2"]) else "FAIL")

    print("\n" + "=" * 72)
    print("  FINAL VERDICT — HADRON-SECTOR CHECKS")
    print("=" * 72)
    print(f"  Check I   (Z⁶ coord. = 12)      : {'PASS' if z6['PASS']  else 'FAIL'}")
    print(f"  Check II  (CKM φ⁻¹ holonomy)    : {'PASS' if ckm['PASS'] else 'FAIL'}")
    print(f"  Check III (12α drag coeff.)      : {'PASS' if drag['PASS'] else 'FAIL'}")
    print(f"  Check IV  (δ_CP = 2π·φ⁻¹)       : {'PASS' if cp['PASS']  else 'FAIL'}")
    print(f"  Aux.        (E8→Z⁶→H₃ projection) : {'PASS' if proj_check['PASS'] else 'FAIL'}")
    print(f"\n  VERDICT: {verdict}")
    if all_pass:
        print()
        print("  The arithmetic used by the hadron-sector readings checks out;")
        print("  the readings themselves remain Tier 2/3 as tagged (App PSC §PSC.4):")
        print("    12 = 2 × dim(Z⁶)  — bulk coordination number [Check I]")
        print("    φ⁻¹ = SU(2)_L holonomy over 5-fold face-defect circuit [Check II]")
        print("    12α = face-defect drag in Z⁶ bulk       [Check III]")
        print("    δ_CP = 2π·φ⁻¹ (Jackiw–Rebbi boundary)  [Check IV]")
    print("=" * 72)

    # ------------------------------------------------------------------
    # JSON Output
    # ------------------------------------------------------------------
    results = {
        "protocol":           "protocol_hadron_topology",

        "tier":               "Tier 1 lattice counts; Tier 2 12-alpha drag mechanism conditional on the Tier 3 face-defect assignment; Tier 3 CKM phi^-1 exponents and CP phase",
        "pass":               bool(all_pass),
        "verdict":            verdict,
        "theorem_I_z6_coordination":   z6,
        "theorem_II_ckm_phi_inv":      ckm,
        "theorem_III_strange_drag":    drag,
        "theorem_IV_cp_phase":         cp,
        "auxiliary_projection_check":  proj_check,
        "summary": {
            "z6_coordination_number":     int(z6["nn_directions_count"]),
            "phi_inv_holonomy":           float(ckm["phi_correction"]),
            "12_alpha_value":             float(drag["12_alpha_value"]),
            "5_alpha_value":              float(drag["5_alpha_value"]),
            "drag_ratio_12_over_5":       float(drag["drag_channel_ratio"]),
            "delta_cp_rad":               float(cp["delta_cp_rad"]),
            "delta_cp_deg":               float(cp["delta_cp_deg"]),
            "ckm_s23_exponent":           float(ckm["s23_exponent"]),
            "ckm_s13_exponent":           float(ckm["s13_exponent"]),
            "all_theorems_pass":          bool(all_pass),
        },
    }

    out_path = get_output_path("protocol_hadron_topology_results.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2, cls=_NumpyEncoder)

    print(f"\n  Results saved to: {out_path}")
    print("=" * 72)

    # The verdict is recorded in the JSON; the non-pass outcome is registered in
    # config/expected_outcomes.json, so the script itself exits cleanly.
    return 0


if __name__ == "__main__":
    sys.exit(main())
