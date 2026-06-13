#!/usr/bin/env python3
"""
Protocol W4b: Spectral-ordinal audit of the lepton harmonic integers.

Verifies that N=11 and N=17 do not arise as activation ordinals of the
phason-vector channel in the icosahedrally-decomposed linear spectrum of the
canonical 152-node defect cage (the linear-spectral analogue of the W4
arithmetic-invariant audit); the non-perturbative soliton extraction remains
the closure target (App H, O.5).

The protocol builds the phason-sector central-force spring Hessian on the
456 perpendicular-displacement degrees of freedom of the canonical I_h-closed
152-node cage. The spring operator uses the three-band bond convention
sqrt(0.5) -> k=1, 1.0 -> k=1, and 1/phi -> k=phi.

The I_h representation is resolved by character projectors over the ten
classes of I_h = A_5 x Z_2. The two order-five classes are distinguished by
the trace of the carried perpendicular-space rotation, which fixes the
projector convention at the group-action level.
"""

from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np

SRC_PATH = Path(__file__).resolve().parent
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from cage_builder import build_canonical_cage  # noqa: E402
import gct_projections as proj  # noqa: E402
from gct_utils import get_output_path  # noqa: E402
from protocol_cage_repair import (  # noqa: E402
    icosahedral_rotations_lattice_frame,
    lift_to_6d_signed_perm,
    vertex_pairs_from_projection,
)

PHI = (1.0 + math.sqrt(5.0)) / 2.0

N_NODES = 152
N_DOF = 3 * N_NODES
DEG_TOL_REL = 1e-6
ZERO_TOL = 1e-8
GATE_TOL = 1e-8
INT_TOL = 1e-6
BOND_TOL = 0.05
TARGET_PAIR = (11, 17)
EXPECTED_FIRST_ACTIVATIONS = [5, 18, 26]
EXPECTED_ZERO_MODES = 6
EXPECTED_NONZERO_CLUSTERS = 120

CLASS_NAMES = [
    "E",
    "C2",
    "C3",
    "C5",
    "C5^2",
    "i",
    "i*C2",
    "i*C3",
    "i*C5",
    "i*C5^2",
]
CLASS_SIZES_EXPECTED = [1, 15, 20, 12, 12, 1, 15, 20, 12, 12]

A5_CHI = {
    "A": [1.0, 1.0, 1.0, 1.0, 1.0],
    "T1": [3.0, -1.0, 0.0, PHI, 1.0 - PHI],
    "T2": [3.0, -1.0, 0.0, 1.0 - PHI, PHI],
    "G": [4.0, 0.0, 1.0, -1.0, -1.0],
    "H": [5.0, 1.0, -1.0, 0.0, 0.0],
}
IRREPS = ["Ag", "T1g", "T2g", "Gg", "Hg", "Au", "T1u", "T2u", "Gu", "Hu"]
IRREP_DIM = {
    "Ag": 1,
    "T1g": 3,
    "T2g": 3,
    "Gg": 4,
    "Hg": 5,
    "Au": 1,
    "T1u": 3,
    "T2u": 3,
    "Gu": 4,
    "Hu": 5,
}

RESULTS_PATH = get_output_path("protocol_w4b_lepton_spectral_ordinals_results.json")


class ProtocolFailure(RuntimeError):
    def __init__(self, stage: str, message: str, extra: dict | None = None):
        super().__init__(message)
        self.stage = stage
        self.extra = extra or {}


def ih_character(irrep: str) -> list[float]:
    """Return the I_h character row over the ten proper and improper classes."""
    base, parity = irrep[:-1], irrep[-1]
    chi = A5_CHI[base]
    sign = 1.0 if parity == "g" else -1.0
    return list(chi) + [sign * c for c in chi]


IH_CHI = {r: ih_character(r) for r in IRREPS}


def assert_gate(condition: bool, stage: str, message: str, extra: dict | None = None) -> None:
    """Raise a protocol failure when a validation gate does not close."""
    if not condition:
        raise ProtocolFailure(stage, message, extra)


def proper_class_of_trace(trace_value: float) -> int:
    """Classify a proper icosahedral rotation by its perpendicular-frame trace."""
    if abs(trace_value - 3.0) < 1e-6:
        return 0
    if abs(trace_value + 1.0) < 1e-6:
        return 1
    if abs(trace_value) < 1e-6:
        return 2
    if abs(trace_value - PHI) < 1e-6:
        return 3
    if abs(trace_value - (1.0 - PHI)) < 1e-6:
        return 4
    raise ProtocolFailure("class-resolution", f"unclassifiable rotation trace {trace_value}")


def multiplicities_from_character(chi_rep: list[float]) -> dict[str, float]:
    """Compute I_h irrep multiplicities from a class character."""
    out = {}
    for r in IRREPS:
        chi_r = IH_CHI[r]
        out[r] = sum(
            CLASS_SIZES_EXPECTED[c] * chi_r[c] * chi_rep[c] for c in range(10)
        ) / 120.0
    return out


def build_group_action(nodes_6d: np.ndarray) -> tuple[list[dict], list[int]]:
    """Build the carried I_h action as 6D matrices, 3D actions, and node maps."""
    nodes_int = np.round(nodes_6d).astype(np.int64)
    vertices_perp, _ = vertex_pairs_from_projection()
    rotations = icosahedral_rotations_lattice_frame(vertices_perp)
    m_perp = proj.get_m_perp()

    assert_gate(len(rotations) == 60, "group-size", f"got {len(rotations)} rotations")

    proper: list[tuple[np.ndarray, np.ndarray]] = []
    seen: set[tuple[int, ...]] = set()
    for rotation in rotations:
        lifted = lift_to_6d_signed_perm(rotation, vertices_perp)
        assert_gate(lifted is not None, "group-lift", "rotation did not lift to Z^6")
        matrix = np.round(lifted).astype(np.int64)
        key = tuple(matrix.flatten().tolist())
        assert_gate(key not in seen, "group-lift", "duplicate lifted matrix")
        seen.add(key)

        r_eff = m_perp @ matrix @ m_perp.T
        assert_gate(
            np.linalg.norm(r_eff - rotation) <= 1e-9,
            "group-lift",
            "lifted matrix and carried perpendicular action disagree",
            {"norm_diff": float(np.linalg.norm(r_eff - rotation))},
        )
        assert_gate(
            np.linalg.norm(r_eff @ r_eff.T - np.eye(3)) <= 1e-10,
            "group-lift",
            "carried perpendicular action is not orthogonal",
        )
        proper.append((matrix, r_eff))

    elements: list[dict] = []
    for matrix, r_eff in proper:
        elements.append({"M": matrix, "R_eff": r_eff, "parity": 1})
    for matrix, r_eff in proper:
        elements.append({"M": -matrix, "R_eff": -r_eff, "parity": -1})

    coord_to_index = {tuple(row): i for i, row in enumerate(nodes_int.tolist())}
    for element in elements:
        images = nodes_int @ element["M"].T
        perm = np.empty(N_NODES, dtype=np.int64)
        for i in range(N_NODES):
            j = coord_to_index.get(tuple(images[i].tolist()))
            assert_gate(j is not None, "node-action", "group element leaves the cage")
            perm[i] = j
        assert_gate(
            len(set(perm.tolist())) == N_NODES,
            "node-action",
            "group element induced a non-bijective node map",
        )
        element["perm"] = perm

    for element in elements:
        proper_trace = float(
            np.trace(element["R_eff"] if element["parity"] == 1 else -element["R_eff"])
        )
        class_index = proper_class_of_trace(proper_trace)
        element["class"] = class_index if element["parity"] == 1 else class_index + 5

    class_sizes = [sum(1 for element in elements if element["class"] == c) for c in range(10)]
    assert_gate(
        class_sizes == CLASS_SIZES_EXPECTED,
        "class-size-gate",
        f"class sizes {class_sizes} != {CLASS_SIZES_EXPECTED}",
        {"observed": class_sizes, "expected": CLASS_SIZES_EXPECTED},
    )
    return elements, class_sizes


def phason_vector_label(elements: list[dict]) -> tuple[str, dict]:
    """Identify the I_h irrep carried by perpendicular displacement components."""
    m_para = proj.get_m_parallel()
    chi_vec = []
    chi_para = []
    for c in range(10):
        traces_vec = []
        traces_para = []
        for element in elements:
            if element["class"] != c:
                continue
            traces_vec.append(float(np.trace(element["R_eff"])))
            r_para = m_para @ element["M"].astype(float) @ m_para.T
            traces_para.append(float(np.trace(r_para)))
        assert_gate(
            max(traces_vec) - min(traces_vec) <= 1e-9,
            "phason-vector-character",
            f"perpendicular character is not class-constant on class {c}",
        )
        assert_gate(
            max(traces_para) - min(traces_para) <= 1e-9,
            "parallel-vector-character",
            f"parallel character is not class-constant on class {c}",
        )
        chi_vec.append(float(np.mean(traces_vec)))
        chi_para.append(float(np.mean(traces_para)))

    mult_vec = multiplicities_from_character(chi_vec)
    mult_para = multiplicities_from_character(chi_para)
    hits = [r for r in IRREPS if abs(mult_vec[r] - 1.0) < 1e-9]
    zeros = [r for r in IRREPS if abs(mult_vec[r]) < 1e-9]
    assert_gate(
        len(hits) == 1 and len(zeros) == 9,
        "phason-vector-label",
        "perpendicular vector channel is not a single clean I_h irrep",
        {"multiplicities": mult_vec},
    )
    para_hits = [r for r in IRREPS if abs(mult_para[r] - 1.0) < 1e-9]
    record = {
        "rho_star_label": hits[0],
        "rho_star_designation": "phason-vector channel",
        "chi_vec_per_class": dict(zip(CLASS_NAMES, [round(x, 12) for x in chi_vec])),
        "chi_parallel_per_class": dict(zip(CLASS_NAMES, [round(x, 12) for x in chi_para])),
        "gamma_vec_multiplicities": {r: round(mult_vec[r], 12) for r in IRREPS},
        "parallel_vector_label": para_hits[0] if len(para_hits) == 1 else None,
    }
    return hits[0], record


def build_hessian(nodes_perp: np.ndarray) -> tuple[np.ndarray, dict[str, int]]:
    """Build the phason-sector spring Hessian for perpendicular displacements."""
    hessian = np.zeros((N_DOF, N_DOF))
    bond_census = {"sqrt0.5_k1": 0, "1.0_k1": 0, "1/phi_kphi": 0}
    sqrt_half = math.sqrt(0.5)
    for i in range(N_NODES):
        for j in range(i + 1, N_NODES):
            dvec = nodes_perp[i] - nodes_perp[j]
            distance = float(np.linalg.norm(dvec))
            if abs(distance - sqrt_half) < BOND_TOL:
                stiffness = 1.0
                bond_census["sqrt0.5_k1"] += 1
            elif abs(distance - 1.0) < BOND_TOL:
                stiffness = 1.0
                bond_census["1.0_k1"] += 1
            elif abs(distance - (1.0 / PHI)) < BOND_TOL:
                stiffness = PHI
                bond_census["1/phi_kphi"] += 1
            else:
                continue
            direction = dvec / distance
            block = stiffness * np.outer(direction, direction)
            si, sj = 3 * i, 3 * j
            hessian[si : si + 3, si : si + 3] += block
            hessian[sj : sj + 3, sj : sj + 3] += block
            hessian[si : si + 3, sj : sj + 3] -= block
            hessian[sj : sj + 3, si : si + 3] -= block
    return 0.5 * (hessian + hessian.T), bond_census


def build_displacement_action(perm: np.ndarray, r_eff: np.ndarray) -> np.ndarray:
    """Build D(g) on node-indexed perpendicular displacement vectors."""
    action = np.zeros((N_DOF, N_DOF))
    base_col = 3 * np.arange(N_NODES)
    base_row = 3 * perm
    for a in range(3):
        for b in range(3):
            action[base_row + a, base_col + b] = r_eff[a, b]
    return action


def build_projectors(elements: list[dict]) -> tuple[dict[str, np.ndarray], np.ndarray]:
    """Build all I_h isotypic projectors by class-summed displacement actions."""
    class_sums = np.zeros((10, N_DOF, N_DOF))
    for element in elements:
        class_sums[element["class"]] += build_displacement_action(
            element["perm"], element["R_eff"]
        )

    projectors = {}
    for r in IRREPS:
        projector = np.zeros((N_DOF, N_DOF))
        for c in range(10):
            chi = IH_CHI[r][c]
            if chi != 0.0:
                projector += chi * class_sums[c]
        projectors[r] = (IRREP_DIM[r] / 120.0) * projector
    return projectors, class_sums


def irrep_content(
    basis: np.ndarray, label: str, projectors: dict[str, np.ndarray]
) -> dict[str, int]:
    """Return the I_h irrep content of the subspace spanned by basis columns."""
    content = {}
    max_dev = 0.0
    for r in IRREPS:
        raw = float(np.trace(basis.T @ projectors[r] @ basis)) / IRREP_DIM[r]
        count = int(round(raw))
        max_dev = max(max_dev, abs(raw - count))
        if count:
            content[r] = count
    assert_gate(
        max_dev < INT_TOL,
        "irrep-content",
        f"non-integral irrep content in {label}",
        {"max_deviation": max_dev},
    )
    return content


def cluster_nonzero_spectrum(evals_nz: np.ndarray, evecs_nz: np.ndarray) -> tuple[list[dict], float, float]:
    """Cluster distinct non-zero eigenvalues by relative degeneracy tolerance."""
    order = np.argsort(evals_nz)
    values = evals_nz[order]
    vectors = evecs_nz[:, order]
    clusters: list[dict] = []
    i = 0
    while i < len(values):
        anchor = values[i]
        j = i + 1
        while j < len(values) and (values[j] - anchor) <= DEG_TOL_REL * abs(anchor):
            j += 1
        clusters.append(
            {
                "i0": i,
                "i1": j,
                "eigenvalue": float(np.mean(values[i:j])),
                "degeneracy": j - i,
                "basis": vectors[:, i:j],
            }
        )
        i = j

    max_intra = 0.0
    for cluster in clusters:
        segment = values[cluster["i0"] : cluster["i1"]]
        if len(segment) > 1:
            max_intra = max(max_intra, float((segment[-1] - segment[0]) / abs(segment[0])))
    min_inter = min(
        (clusters[k + 1]["eigenvalue"] - clusters[k]["eigenvalue"])
        / abs(clusters[k]["eigenvalue"])
        for k in range(len(clusters) - 1)
    )
    return clusters, max_intra, min_inter


def run() -> dict:
    t0 = time.time()
    print("=" * 78)
    print("GCT Protocol W4b - spectral-ordinal audit of lepton harmonic integers")
    print("=" * 78)

    print("\n[1] Building canonical 152-node I_h-closed cage and group action")
    nodes_6d, nodes_perp = build_canonical_cage(size=N_NODES)
    assert_gate(nodes_6d.shape[0] == N_NODES, "cage-size", f"got {nodes_6d.shape[0]} nodes")
    nodes_int = np.round(nodes_6d).astype(np.int64)
    assert_gate(
        np.allclose(nodes_6d, nodes_int, atol=1e-9),
        "cage-integrality",
        "cage coordinates are not integral in Z^6",
    )

    elements, class_sizes = build_group_action(nodes_6d)
    print(f"    class sizes: {dict(zip(CLASS_NAMES, class_sizes))}")
    print("    Gate PASS: class sizes = (1,15,20,12,12)x2")

    rho_star, rho_record = phason_vector_label(elements)
    print(f"    phason-vector channel rho* = {rho_star}")

    print("\n[2] Building 456x456 phason-sector spring Hessian")
    hessian, bond_census = build_hessian(nodes_perp)
    print(f"    bond census: {bond_census} (total {sum(bond_census.values())})")

    print("\n[3] Building I_h projectors and closing validation gates")
    projectors, class_sums = build_projectors(elements)

    idem = {
        r: float(np.linalg.norm(projectors[r] @ projectors[r] - projectors[r]))
        for r in IRREPS
    }
    idem_max = max(idem.values())
    assert_gate(
        idem_max < GATE_TOL,
        "projector-idempotency",
        f"max ||P^2-P||_F = {idem_max}",
        {"per_irrep": idem},
    )
    print(f"    Gate PASS: projector idempotency max = {idem_max:.3e}")

    equiv = {
        r: float(np.linalg.norm(hessian @ projectors[r] - projectors[r] @ hessian))
        for r in IRREPS
    }
    equiv_max = max(equiv.values())
    assert_gate(
        equiv_max < GATE_TOL,
        "operator-equivariance",
        f"max ||[H,P]||_F = {equiv_max}",
        {"per_irrep": equiv},
    )
    print(f"    Gate PASS: equivariance max = {equiv_max:.3e}")

    multiplicities_raw = {
        r: float(np.trace(projectors[r])) / IRREP_DIM[r] for r in IRREPS
    }
    multiplicities = {r: int(round(multiplicities_raw[r])) for r in IRREPS}
    mult_dev = max(abs(multiplicities_raw[r] - multiplicities[r]) for r in IRREPS)
    dim_sum = sum(multiplicities[r] * IRREP_DIM[r] for r in IRREPS)
    completeness = float(np.linalg.norm(sum(projectors[r] for r in IRREPS) - np.eye(N_DOF)))
    assert_gate(
        mult_dev < INT_TOL,
        "multiplicity-integrality",
        f"max integrality deviation = {mult_dev}",
        {"raw": multiplicities_raw},
    )
    assert_gate(
        dim_sum == N_DOF,
        "multiplicity-sum-rule",
        f"sum multiplicity*dimension = {dim_sum}",
        {"multiplicities": multiplicities},
    )
    chi_disp = [
        float(np.trace(class_sums[c])) / CLASS_SIZES_EXPECTED[c] for c in range(10)
    ]
    multiplicities_char = multiplicities_from_character(chi_disp)
    char_dev = max(abs(multiplicities_char[r] - multiplicities[r]) for r in IRREPS)
    print(f"    Gate PASS: multiplicities = {multiplicities}")
    print(f"    Gate PASS: multiplicity sum rule = {dim_sum}")

    print("\n[4] Diagonalizing H and clustering non-zero spectrum")
    evals, evecs = np.linalg.eigh(hessian)
    min_eval = float(evals.min())
    zero_mask = np.abs(evals) <= ZERO_TOL
    n_zero = int(zero_mask.sum())
    nz_idx = np.where(~zero_mask)[0]
    evals_nz = evals[nz_idx]
    evecs_nz = evecs[:, nz_idx]
    assert_gate(
        not np.any(evals_nz < 0),
        "positive-semidefinite-spectrum",
        "negative non-zero eigenvalue found",
        {"min_eigenvalue": min_eval},
    )

    zero_content = irrep_content(evecs[:, zero_mask], "zero-mode space", projectors)
    zero_dimsum = sum(IRREP_DIM[r] * n for r, n in zero_content.items())
    assert_gate(
        zero_dimsum == n_zero,
        "zero-mode-census",
        "zero-mode irrep content does not span the zero space",
        {"zero_modes": n_zero, "content": zero_content},
    )
    assert_gate(
        n_zero == EXPECTED_ZERO_MODES,
        "zero-mode-census",
        f"zero-mode count {n_zero} != {EXPECTED_ZERO_MODES}",
    )
    print(f"    Gate PASS: zero-mode census = {n_zero}, content {zero_content}")

    clusters, max_intra, min_inter = cluster_nonzero_spectrum(evals_nz, evecs_nz)
    assert_gate(
        len(clusters) == EXPECTED_NONZERO_CLUSTERS,
        "cluster-count",
        f"non-zero cluster count {len(clusters)} != {EXPECTED_NONZERO_CLUSTERS}",
    )

    activation_table = []
    rho_ordinals = []
    cumulative = {r: 0 for r in IRREPS}
    for ordinal, cluster in enumerate(clusters, start=1):
        content = irrep_content(cluster["basis"], f"cluster {ordinal}", projectors)
        dimsum = sum(IRREP_DIM[r] * n for r, n in content.items())
        assert_gate(
            dimsum == cluster["degeneracy"],
            "cluster-degeneracy",
            f"cluster {ordinal}: degeneracy {cluster['degeneracy']} != irrep dimension sum {dimsum}",
            {"content": content},
        )
        for r, n in content.items():
            if n:
                cumulative[r] += 1
        rho_present = rho_star in content
        if rho_present:
            rho_ordinals.append(ordinal)
        activation_table.append(
            {
                "ordinal": ordinal,
                "eigenvalue": cluster["eigenvalue"],
                "degeneracy": cluster["degeneracy"],
                "irrep_content": content,
                "rho_star_present": rho_present,
                "cumulative_rho_star": cumulative[rho_star],
            }
        )
    print("    Gate PASS: each cluster degeneracy equals its irrep dimension sum")

    total_nz_dim = sum(cluster["degeneracy"] for cluster in clusters)
    assert_gate(
        total_nz_dim + n_zero == N_DOF,
        "spectral-dimension-count",
        f"non-zero dimensions {total_nz_dim} + zero modes {n_zero} != {N_DOF}",
    )

    observed_pair = tuple(rho_ordinals[:2])
    protocol_passes = observed_pair != TARGET_PAIR
    first_three = rho_ordinals[:3]
    assert_gate(
        first_three == EXPECTED_FIRST_ACTIVATIONS,
        "activation-ordinal-check",
        f"first three rho* activations {first_three} != {EXPECTED_FIRST_ACTIVATIONS}",
    )

    results = {
        "protocol": "W4b",
        "status": "PASS" if protocol_passes else "FAIL",
        "pass_condition": "N=11 and N=17 are not the first two phason-vector activation ordinals",
        "cage": {
            "N_nodes": N_NODES,
            "N_dof": N_DOF,
            "construction": "cage_builder.build_canonical_cage(size=152)",
        },
        "operator": {
            "sector": "phason",
            "type": "central-force spring Hessian",
            "bond_convention": {
                "sqrt0.5": {"stiffness": 1.0, "tolerance": BOND_TOL},
                "1.0": {"stiffness": 1.0, "tolerance": BOND_TOL},
                "1/phi": {"stiffness": PHI, "tolerance": BOND_TOL},
            },
            "bond_census": bond_census,
        },
        "group": {
            "name": "I_h",
            "order": 120,
            "class_names": CLASS_NAMES,
            "class_sizes": dict(zip(CLASS_NAMES, class_sizes)),
            "order5_class_split": "trace(R_perp)=phi for C5; trace(R_perp)=1-phi for C5^2",
        },
        "rho_star": rho_record,
        "validation_gates": {
            "class_sizes_pass": True,
            "projector_idempotency_max_frobenius": idem_max,
            "projector_idempotency_per_irrep": idem,
            "equivariance_max_frobenius": equiv_max,
            "equivariance_per_irrep": equiv,
            "multiplicities": multiplicities,
            "multiplicity_max_integrality_deviation": mult_dev,
            "multiplicity_sum_rule": dim_sum,
            "projector_completeness_frobenius": completeness,
            "character_crosscheck_max_deviation": char_dev,
            "zero_mode_census": {"count": n_zero, "irrep_content": zero_content},
            "cluster_degeneracy_equals_irrep_dim_sum": True,
            "all_gates_pass": True,
        },
        "spectrum": {
            "min_eigenvalue": min_eval,
            "zero_tolerance": ZERO_TOL,
            "n_zero_modes": n_zero,
            "zero_mode_interpretation": "rigid translations and rotations",
            "smallest_nonzero_eigenvalue": float(evals_nz.min()),
            "largest_eigenvalue": float(evals.max()),
            "n_nonzero_clusters": len(clusters),
            "degeneracy_tolerance_relative": DEG_TOL_REL,
            "max_intracluster_relative_spread": max_intra,
            "min_intercluster_relative_gap": min_inter,
        },
        "activation_audit": {
            "rho_star_channel": rho_star,
            "rho_star_activation_ordinals": rho_ordinals,
            "first_activation_ordinal": rho_ordinals[0],
            "second_activation_ordinal": rho_ordinals[1],
            "third_activation_ordinal": rho_ordinals[2],
            "observed_pair": list(observed_pair),
            "excluded_pair": list(TARGET_PAIR),
            "confirms_negative": protocol_passes,
        },
        "activation_table": activation_table,
        "runtime_s": round(time.time() - t0, 3),
    }
    RESULTS_PATH.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print("\n" + "=" * 78)
    print("W4b VERDICT")
    print("=" * 78)
    print(f"Status: {'PASS' if protocol_passes else 'FAIL'}")
    print(f"rho* channel: {rho_star}")
    print(f"rho*-activation ordinals: {rho_ordinals}")
    print(f"First/second activation: {observed_pair}")
    print(f"Excluded W4b pair: {TARGET_PAIR}")
    print(f"Non-zero clusters: {len(clusters)}")
    print(f"Zero modes: {n_zero} {zero_content} (rigid translations and rotations)")
    print("All validation gates: PASS")
    print(f"JSON results: {RESULTS_PATH}")
    print(f"Runtime: {results['runtime_s']} s")
    return results


def main() -> int:
    try:
        results = run()
    except ProtocolFailure as exc:
        failure = {
            "protocol": "W4b",
            "status": "FAIL",
            "stage": exc.stage,
            "message": str(exc),
            "extra": exc.extra,
        }
        RESULTS_PATH.write_text(json.dumps(failure, indent=2), encoding="utf-8")
        print("\n" + "=" * 78)
        print("W4b VERDICT")
        print("=" * 78)
        print("Status: FAIL")
        print(f"Stage: {exc.stage}")
        print(f"Reason: {exc}")
        print(f"JSON results: {RESULTS_PATH}")
        return 2
    return 0 if results["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
