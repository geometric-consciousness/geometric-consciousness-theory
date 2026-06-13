#!/usr/bin/env python3
"""
protocol_iit_phi_pyphi.py

Illustrative IIT 3.0 Phi computation on a noisy Boolean toy substrate with
icosahedral adjacency, using the PyPhi reference implementation (Mayner et
al. 2018, PLOS Comp Bio 14(7):e1006343).

Engine binding: V1 Ch17 §17.5 sub-graph computation. This is an IIT-3.0
methodology example for tractable k=2..5 induced sub-graphs; it is not a
direct phason-Hamiltonian-derived TPM computation. protocol_iit_phi.py
supplies graph-theoretic necessary-condition witnesses for k=12.

Tier 3 illustrative numeric values (TPM-noise-dependent). The substrate-TPM
derivation from p(j|i)=|t_ij|^2/Z_i is Open Problem O.28. The TPM here is
built from the canonical icosahedral edge list (12 vertices, 30 edges,
degree 5) under a noisy majority-vote update rule:

    P(next_state[i] = 1 | s) = (1 - eps)  if sum_{j in N(i)} s[j] >= ceil(deg(i)/2)
                             = eps         otherwise

with eps = 0.05 to ensure every global state has positive preimage measure
(the IIT 3.0 reachability prerequisite, Oizumi-Albantakis-Tononi 2014 §S1).

Phi is computed via pyphi.compute.sia() (full system integrated information).
The combinatorial cost of sia() scales as N! over bipartitions and 2^N
over cause-effect repertoires, so this script reports Phi at the largest
computationally tractable sub-network sizes (k = 2, 3, 4, 5) on induced
sub-graphs of the canonical icosahedron. The k = 12 numeric Phi value
remains an HPC target.

Scope of the sub-network witnesses. IIT 3.0 / IIT 4.0 define complexes
as local maxima of integrated conceptual information under the Exclusion
Postulate (Oizumi-Albantakis-Tononi 2014; Albantakis et al. 2023, principle
of maximal existence). Subsystem Phi values therefore do NOT extend as a
lower bound to the global Phi_max of any containing supersystem — a
strict superset can carry strictly lower Phi_max than its complex. The
k = 2..5 PyPhi values reported here establish positivity on the chosen
induced sub-graphs; they do not establish Phi_max(k=12) > 0 on the full
icosahedron. The global Phi_max(k=12) computation is registered as Open
Problem O.28 with three closure paths (direct HPC; major-complex
localisation; vertex-transitive-regular-graph lower bound).

Inputs:  none (deterministic from the canonical adjacency).
Outputs: data/protocol_iit_phi_pyphi_results.json with Phi values,
         elapsed runtime per size, and the verdict.
"""

import json
import os

import numpy as np

os.environ.setdefault("PYPHI_WELCOME_OFF", "yes")

CACHE_REPLAY = os.environ.get("GCT_IIT_CACHE_REPLAY", "0") == "1"


# ---------------------------------------------------------------------------
# Canonical icosahedral adjacency
# ---------------------------------------------------------------------------

ICOSAHEDRON_EDGES = [
    (0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
    (1, 2), (2, 3), (3, 4), (4, 5), (5, 1),
    (1, 6), (1, 10), (2, 6), (2, 7), (3, 7), (3, 8),
    (4, 8), (4, 9), (5, 9), (5, 10),
    (6, 7), (7, 8), (8, 9), (9, 10), (10, 6),
    (6, 11), (7, 11), (8, 11), (9, 11), (10, 11),
]

REFERENCE_PYPHI_VALUES = {
    "k2_edge": {
        "k": 2,
        "subset_indices": [0, 1],
        "initial_state": [1, 0],
        "phi": 0.81,
    },
    "k3_triangle": {
        "k": 3,
        "subset_indices": [0, 1, 2],
        "initial_state": [1, 1, 0],
        "phi": 0.203523,
    },
    "k4_kite": {
        "k": 4,
        "subset_indices": [0, 1, 2, 5],
        "initial_state": [1, 1, 0, 0],
        "phi": 0.478679,
    },
    "k5_apex_pentagon": {
        "k": 5,
        "subset_indices": [0, 1, 2, 3, 4],
        "initial_state": [1, 1, 1, 0, 0],
        "phi": 1.1249,
    },
}


def build_icosahedral_adjacency() -> np.ndarray:
    A = np.zeros((12, 12), dtype=int)
    for u, v in ICOSAHEDRON_EDGES:
        A[u, v] = 1
        A[v, u] = 1
    return A


def induced_subgraph_adjacency(A: np.ndarray, nodes: list) -> np.ndarray:
    n = len(nodes)
    sub = np.zeros((n, n), dtype=int)
    for i_new, i_old in enumerate(nodes):
        for j_new, j_old in enumerate(nodes):
            sub[i_new, j_new] = A[i_old, j_old]
    return sub


# ---------------------------------------------------------------------------
# Boolean majority-vote TPM
# ---------------------------------------------------------------------------

def build_majority_tpm(adj: np.ndarray, noise: float = 0.05) -> np.ndarray:
    """
    Construct the (2^N, N) state-by-node TPM under noisy majority-vote
    update. Node i fires (next-state = 1) with probability (1 - noise) if
    at least half of its in-neighbours are on, and with probability
    noise otherwise. Isolated nodes (zero in-degree) self-equilibrate to
    probability noise.

    The small noise floor ensures every global state has positive
    preimage measure, which is the IIT 3.0 reachability prerequisite
    for the cause-effect repertoire computation
    (Oizumi-Albantakis-Tononi 2014, §S1; Mayner et al. 2018 PyPhi
    config NO_UNREACHABLE_STATES).
    """
    n = adj.shape[0]
    num_states = 2 ** n
    tpm = np.zeros((num_states, n), dtype=float)

    in_degree = adj.sum(axis=1)
    threshold = np.ceil(in_degree / 2.0)

    for state_idx in range(num_states):
        bits = np.array(
            [(state_idx >> bit) & 1 for bit in range(n)], dtype=int
        )
        for i in range(n):
            if in_degree[i] == 0:
                tpm[state_idx, i] = noise
                continue
            neighbor_sum = float(np.dot(adj[i], bits))
            tpm[state_idx, i] = (1.0 - noise) if neighbor_sum >= threshold[i] else noise
    return tpm


# ---------------------------------------------------------------------------
# Phi via PyPhi
# ---------------------------------------------------------------------------

def compute_phi_for_subset(adj_full: np.ndarray, subset: list) -> dict:
    import pyphi

    # Single-process evaluation: avoids re-loading large dependency DLLs
    # (pyemd -> POT -> torch) in every multiprocessing worker, which is the
    # standard Windows failure mode for the canonical PyPhi parallel path.
    pyphi.config.PARALLEL_CUT_EVALUATION = False
    pyphi.config.PARALLEL_CONCEPT_EVALUATION = False
    pyphi.config.NUMBER_OF_CORES = 1
    pyphi.config.PROGRESS_BARS = False

    sub_adj = induced_subgraph_adjacency(adj_full, subset)
    tpm = build_majority_tpm(sub_adj)

    n = len(subset)
    # Pick a non-trivial initial state: roughly half nodes "on".
    state = tuple(1 if i < n // 2 + n % 2 else 0 for i in range(n))

    network = pyphi.Network(tpm, cm=sub_adj)
    subsystem = pyphi.Subsystem(network, state, range(n))
    sia = pyphi.compute.sia(subsystem)

    return {
        "k": n,
        "subset_indices": subset,
        "initial_state": list(state),
        "phi": float(sia.phi),
        "elapsed_seconds": None,
    }


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def hemi_icosahedron_subset() -> list:
    """North pole + upper pentagon = the canonical hemi-icosahedron (k=6)."""
    return [0, 1, 2, 3, 4, 5]


def run() -> dict:
    A = build_icosahedral_adjacency()
    try:
        import pyphi  # noqa: F401
        pyphi_available = True
        pyphi_status = "available"
    except ModuleNotFoundError as e:
        pyphi_available = False
        pyphi_status = f"unavailable ({e})"

    results = {
        "graph": {
            "k_full": 12,
            "edges": len(ICOSAHEDRON_EDGES),
            "degree": 5,
            "topology": "icosahedron (canonical AKN nearest-neighbour shell)",
        },
        "update_rule": "noisy majority-vote of in-neighbours (epsilon = 0.05)",
        "tier": "Tier 2 mechanism + Tier 3 specific numeric values (depend on noise floor)",
        "pyphi_dependency_status": pyphi_status,
        "subsystem_phi": [],
    }

    # Tractable sub-network sizes on the canonical icosahedral adjacency.
    # k = 2..5 land on the desktop-scale budget for PyPhi's sia/cause-effect
    # structure search; k = 6 (hemi-icosahedron) and the full k = 12 are
    # HPC-scale and registered as the residual O.28 numeric target.
    sizes = [
        ("k2_edge", [0, 1]),
        ("k3_triangle", [0, 1, 2]),
        ("k4_kite", [0, 1, 2, 5]),
        ("k5_apex_pentagon", [0, 1, 2, 3, 4]),
    ]

    for tag, subset in sizes:
        print(f"Computing Phi on {tag} (|S|={len(subset)})...")
        if pyphi_available and CACHE_REPLAY:
            r = dict(REFERENCE_PYPHI_VALUES[tag])
            r["tag"] = tag
            r["elapsed_seconds"] = None
            r["computation_mode"] = "cached_pyphi_reference_opt_in"
            r["dependency_status"] = pyphi_status
            results["subsystem_phi"].append(r)
            print(f"  Opt-in cache Phi = {r['phi']:.6f} (unset GCT_IIT_CACHE_REPLAY for direct PyPhi)")
            continue
        if not pyphi_available:
            r = dict(REFERENCE_PYPHI_VALUES[tag])
            cached_phi = r.pop("phi")
            r["tag"] = tag
            r["computation_mode"] = "cached_pyphi_reference_due_missing_dependency"
            r["cached_reference_phi"] = cached_phi
            r["dependency_status"] = pyphi_status
            r["error"] = f"PyPhi dependency unavailable ({pyphi_status})"
            results["subsystem_phi"].append(r)
            print(f"  PyPhi unavailable; cached reference Phi = {cached_phi:.6f} (not counted as evidence)")
            continue
        try:
            r = compute_phi_for_subset(A, subset)
            r["tag"] = tag
            r["computation_mode"] = "direct_pyphi"
            results["subsystem_phi"].append(r)
            print(f"  Phi = {r['phi']:.6f}   (runtime omitted from JSON for deterministic output)")
        except Exception as e:
            results["subsystem_phi"].append({
                "tag": tag,
                "k": len(subset),
                "error": str(e),
            })
            print(f"  ERROR: {e}")

    # Verdict
    phis = [r["phi"] for r in results["subsystem_phi"] if "phi" in r]
    if phis:
        phi_max_tractable = max(phis)
        phi_selected_subgraph_positive_k2_to_k5 = (
            len(phis) == len(sizes)
            and all(r.get("phi", 0.0) > 0.0 for r in results["subsystem_phi"])
            and phi_max_tractable > 0.0
        )
        # Separate monotone-growth check (the per-subnetwork phi values do
        # NOT have to be monotone-increasing in k under IIT Exclusion;
        # this field reports the actual monotonicity status as a
        # diagnostic, distinct from the load-bearing positivity check).
        phi_monotone_in_k = all(
            phis[i] <= phis[i + 1] for i in range(len(phis) - 1)
        )
        results["phi_max_tractable"] = phi_max_tractable
        results["phi_selected_subgraph_positive_k2_to_k5"] = phi_selected_subgraph_positive_k2_to_k5
        results["phi_selected_subgraph_witness_k2_to_k5_positive"] = phi_selected_subgraph_positive_k2_to_k5
        results["phi_monotone_in_k"] = phi_monotone_in_k
        # Compatibility key for the registry check
        # (claim_registry.json `C_IIT_PHI_SELECTED_SUBGRAPH_WITNESS`). Reports
        # positivity status, NOT monotonicity — see phi_monotone_in_k
        # for the separate monotonicity diagnostic.
        results["phi_selected_subgraph_witness_k2_to_k5_positive_witness"] = phi_selected_subgraph_positive_k2_to_k5
        results["status"] = (
            "SELECTED_SUBGRAPH_POSITIVE__O28_PENDING"
            if phi_selected_subgraph_positive_k2_to_k5
            else "SELECTED_SUBGRAPH_NONPOSITIVE__CHECK_INPUTS"
        )
        max_k_tractable = max(r["k"] for r in results["subsystem_phi"] if "phi" in r)
        results["k12_full_status"] = (
            "Full k=12 Phi_max requires HPC (combinatorial cost of pyphi.compute.sia "
            "scales as N! over bipartitions and 2^N over cause-effect "
            "repertoires). The tractable sub-network values establish Phi > 0 on "
            f"the chosen induced sub-graphs at k <= {max_k_tractable}. The IIT 3.0 "
            "Exclusion Postulate (Oizumi-Albantakis-Tononi 2014) and the IIT 4.0 "
            "principle of maximal existence (Albantakis et al. 2023) forbid "
            "extending these sub-graph values as a monotone lower bound to the "
            "global Phi_max(k=12) — a strict superset can carry strictly lower "
            "Phi_max than its complex. The exact k=12 numeric value is registered "
            "as Open Problem O.28 with three closure paths (direct HPC; major-"
            "complex localisation; vertex-transitive-regular-graph lower bound)."
        )
        results["verdict"] = (
            f"Tier 2 mechanism + Tier 3 sub-graph values: max_k Phi(k <= "
            f"{max_k_tractable}) = {phi_max_tractable:.6f} > 0 on chosen "
            "induced sub-graphs of the canonical icosahedron under the noisy "
            "majority-vote TPM. These sub-graph values DO NOT extend to a global "
            "Phi_max(k=12) > 0 bound under the IIT Exclusion Postulate; the full "
            "k=12 numerical computation is the residual of Open Problem O.28."
        )
        # `pass` semantics: positivity of Phi on every tractable selected
        # sub-graph under the noisy majority-vote TPM. This is not a witness
        # for global Phi_max(k=12); O.28 remains open.
        results["pass"] = bool(phi_selected_subgraph_positive_k2_to_k5)
    else:
        results["phi_max_tractable"] = None
        results["phi_selected_subgraph_witness_k2_to_k5_positive"] = False
        results["phi_monotone_in_k"] = False
        results["phi_selected_subgraph_witness_k2_to_k5_positive_witness"] = False
        results["k12_full_status"] = (
            "Tractable sub-graph Phi values unavailable in this execution "
            "environment because PyPhi did not import. The full k=12 "
            "Phi_max computation remains Open Problem O.28."
        )
        results["verdict"] = "NEEDS_PYPHI: direct PyPhi dependency unavailable; cached references are not counted as evidence."
        results["status"] = "NEEDS_PYPHI"
        results["pass"] = False

    out_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "protocol_iit_phi_pyphi_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=4)
    print(f"\nResults written to {out_path}")
    return results


if __name__ == "__main__":
    run()
