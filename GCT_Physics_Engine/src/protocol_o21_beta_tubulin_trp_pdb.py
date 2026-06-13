#!/usr/bin/env python3
"""
protocol_o21_beta_tubulin_trp_pdb.py
=====================================

Structural-biology screen for beta-tubulin tryptophan radical-pair
host candidates for Open Problem O.21. The available 6DPU coordinate
set is a partial microtubule wall patch; its PCA axis is a local
wall-patch reference, not an assembled 13-protofilament lumen axis.
The protocol therefore reports candidate inward-facing residues and
registers the assembled-microtubule lumen-axis check as pending.

  1. EXPLICIT BETA-TUBULIN CHAIN SELECTION
     From 6DPU PDB header (COMPND records):
       Alpha-tubulin chains: A, C, E, J, K, L (6 chains)
       Beta-tubulin chains:  B, D, F, G, H, I (6 chains)
     This protocol restricts analysis to the beta-tubulin chains only.

  2. LOCAL WALL-PATCH AXIS DETERMINATION
     The PCA of the available alpha+beta CA positions gives a local
     wall-patch axis. If the observed radius range does not reach the
     canonical microtubule lumen/outer-wall radii, this axis is not
     treated as a full assembled-MT lumen axis.

  3. CANDIDATE INWARD-FACING SCREEN
     Microtubule canonical inner radius: ~ 7.5 nm (75 A; ~15 nm lumen ID)
     Microtubule canonical outer radius: ~ 12.5 nm (125 A)
     In the partial 6DPU patch, classify a beta-tubulin Trp as a
     local-inward candidate when it lies inside the local radial mean.
     This is an O.21 sub-closure candidate only; full lumen-axis closure
     requires an assembled-MT reference structure or equivalent
     13-protofilament reconstruction.

  4. HYDROPHOBIC POCKET ISOLATION
     Count of HYDROPHOBIC residues (A, V, L, I, M, F, Y, W) with any
     atom within 5 A of the Trp indole-ring centroid, PLUS the
     ratio of hydrophobic to all residues in the pocket (a higher
     ratio indicates better isolation from the polar / aqueous
     environment).
"""

import json
import warnings
from pathlib import Path

import numpy as np

warnings.filterwarnings("ignore")

try:
    from Bio.PDB import PDBParser, NeighborSearch
    from Bio.PDB.Polypeptide import is_aa
except ModuleNotFoundError:
    STANDARD_AA = {
        "ALA", "ARG", "ASN", "ASP", "CYS", "GLN", "GLU", "GLY", "HIS",
        "ILE", "LEU", "LYS", "MET", "PHE", "PRO", "SER", "THR", "TRP",
        "TYR", "VAL",
    }

    class SimpleAtom:
        def __init__(self, name, coord, residue):
            self.name = name
            self._coord = np.array(coord, dtype=float)
            self._residue = residue

        def get_coord(self):
            return self._coord

        def get_parent(self):
            return self._residue

    class SimpleResidue:
        def __init__(self, resname, resseq, chain):
            self._resname = resname
            self.id = (" ", int(resseq), " ")
            self._chain = chain
            self._atoms = {}

        def add_atom(self, name, coord):
            self._atoms[name] = SimpleAtom(name, coord, self)

        def get_resname(self):
            return self._resname

        def get_parent(self):
            return self._chain

        def __contains__(self, atom_name):
            return atom_name in self._atoms

        def __getitem__(self, atom_name):
            return self._atoms[atom_name]

    class SimpleChain:
        def __init__(self, chain_id):
            self.id = chain_id
            self._residues = []
            self._by_resseq = {}

        def get_or_create_residue(self, resname, resseq):
            key = int(resseq)
            if key not in self._by_resseq:
                residue = SimpleResidue(resname, key, self)
                self._by_resseq[key] = residue
                self._residues.append(residue)
            return self._by_resseq[key]

        def __iter__(self):
            return iter(self._residues)

    class SimpleModel:
        def __init__(self):
            self._chains = {}

        def get_or_create_chain(self, chain_id):
            if chain_id not in self._chains:
                self._chains[chain_id] = SimpleChain(chain_id)
            return self._chains[chain_id]

        def get_atoms(self):
            atoms = []
            for chain in self._chains.values():
                for residue in chain:
                    atoms.extend(residue._atoms.values())
            return atoms

        def __iter__(self):
            return iter(self._chains.values())

    class SimpleStructure:
        def __init__(self, model):
            self._model = model

        def __iter__(self):
            return iter([self._model])

    class PDBParser:
        def __init__(self, QUIET=True):
            self.quiet = QUIET

        def get_structure(self, structure_id, path):
            model = SimpleModel()
            with open(path, "r", encoding="utf-8", errors="ignore") as handle:
                for line in handle:
                    if not line.startswith(("ATOM  ", "HETATM")):
                        continue
                    atom_name = line[12:16].strip()
                    resname = line[17:20].strip()
                    chain_id = line[21].strip() or "_"
                    resseq = int(line[22:26])
                    coord = (
                        float(line[30:38]),
                        float(line[38:46]),
                        float(line[46:54]),
                    )
                    chain = model.get_or_create_chain(chain_id)
                    residue = chain.get_or_create_residue(resname, resseq)
                    residue.add_atom(atom_name, coord)
            return SimpleStructure(model)

    class NeighborSearch:
        def __init__(self, atoms):
            self.atoms = atoms

        def search(self, centroid, radius):
            centroid = np.array(centroid, dtype=float)
            return [
                atom for atom in self.atoms
                if np.linalg.norm(atom.get_coord() - centroid) <= radius
            ]

    def is_aa(residue):
        return residue.get_resname() in STANDARD_AA

try:
    from gct_utils import get_output_path
    OUTPUT_DIR_AVAILABLE = True
except ImportError:
    OUTPUT_DIR_AVAILABLE = False

ENGINE_ROOT = Path(__file__).resolve().parent.parent
PDB_DIR = ENGINE_ROOT / "data" / "pdb"

PDB_1JFF = PDB_DIR / "pdb1jff.ent"
PDB_6DPU = PDB_DIR / "pdb6dpu.ent"

# Explicit beta-tubulin chains in 6DPU (per PDB header COMPND records)
BETA_CHAINS_6DPU = ["B", "D", "F", "G", "H", "I"]
ALPHA_CHAINS_6DPU = ["A", "C", "E", "J", "K", "L"]

# Microtubule canonical dimensions
MT_INNER_RADIUS_ANG = 75.0    # ~ 7.5 nm radius; ~15 nm lumen ID
MT_OUTER_RADIUS_ANG = 125.0   # ~ 12.5 nm
MT_WALL_MIDPLANE_ANG = (MT_INNER_RADIUS_ANG + MT_OUTER_RADIUS_ANG) / 2.0
ASSEMBLED_MT_LUMEN_AXIS_AVAILABLE = False
AXIS_REFERENCE_SCOPE = (
    "6DPU partial wall-patch PCA over available alpha+beta CA positions; "
    "not an assembled 13-protofilament lumen-axis reference"
)

RADICAL_PAIR_MAX_DISTANCE_ANG = 15.0
HYDROPHOBIC_RADIUS_ANG = 5.0

AROMATIC_RESIDUES = {"TRP", "TYR", "PHE", "HIS"}
AROMATIC_RING_ATOMS = {
    "TRP": ["NE1", "CD1", "CE2", "CD2", "CZ2", "CH2", "CZ3", "CE3"],
    "PHE": ["CG", "CD1", "CD2", "CE1", "CE2", "CZ"],
    "TYR": ["CG", "CD1", "CD2", "CE1", "CE2", "CZ"],
    "HIS": ["CG", "ND1", "CD2", "CE1", "NE2"],
}
HYDROPHOBIC_RESIDUES = {"ALA", "VAL", "LEU", "ILE", "MET", "PHE", "TYR", "TRP"}
POLAR_RESIDUES = {"SER", "THR", "ASN", "GLN", "TYR", "CYS"}
CHARGED_RESIDUES = {"ASP", "GLU", "LYS", "ARG", "HIS"}


def parse_structure(pdb_path):
    parser = PDBParser(QUIET=True)
    return parser.get_structure(pdb_path.stem, str(pdb_path))


def get_trp_residues_in_chain(structure, chain_id):
    out = []
    for model in structure:
        for chain in model:
            if chain.id != chain_id:
                continue
            for residue in chain:
                if residue.get_resname() == "TRP" and is_aa(residue):
                    out.append(residue)
        break
    return out


def inventory_1jff_chain_b():
    """Inventory isolated 1JFF chain B; no assembled-lumen inference."""
    expected_trp_auth_seq = [21, 103, 346, 407]
    inventory = {
        "pdb_id": "1JFF",
        "chain_id": "B",
        "scope": (
            "Isolated beta-tubulin chain-B residue inventory only; "
            "no assembled microtubule lumen-axis inference."
        ),
        "pdb_file_available": PDB_1JFF.exists(),
        "expected_trp_auth_seq_ids": expected_trp_auth_seq,
    }
    if not PDB_1JFF.exists():
        inventory.update({
            "standard_residue_count": 0,
            "trp_auth_seq_ids": [],
            "matches_expected_auth_seq_ids": False,
        })
        return inventory

    structure = parse_structure(PDB_1JFF)
    chain_b = None
    for model in structure:
        for chain in model:
            if chain.id == "B":
                chain_b = chain
                break
        break

    if chain_b is None:
        inventory.update({
            "standard_residue_count": 0,
            "trp_auth_seq_ids": [],
            "matches_expected_auth_seq_ids": False,
            "error": "chain B not found",
        })
        return inventory

    standard_residues = [res for res in chain_b if is_aa(res)]
    trp_residues = [res for res in standard_residues if res.get_resname() == "TRP"]
    trp_auth_seq_ids = [int(res.id[1]) for res in trp_residues]
    inventory.update({
        "standard_residue_count": len(standard_residues),
        "auth_seq_id_min": int(min(res.id[1] for res in standard_residues)),
        "auth_seq_id_max": int(max(res.id[1] for res in standard_residues)),
        "trp_auth_seq_ids": trp_auth_seq_ids,
        "trp_residue_names": [f"TRP{int(res.id[1])}" for res in trp_residues],
        "matches_expected_auth_seq_ids": trp_auth_seq_ids == expected_trp_auth_seq,
    })
    return inventory


def get_atom_coords(residue, atom_names):
    coords = [residue[a].get_coord() for a in atom_names if a in residue]
    return np.array(coords, dtype=float) if coords else None


def get_aromatic_ring_centroid(residue):
    atom_names = AROMATIC_RING_ATOMS.get(residue.get_resname(), [])
    coords = get_atom_coords(residue, atom_names)
    if coords is None:
        return residue["CA"].get_coord() if "CA" in residue else None
    return np.mean(coords, axis=0)


def get_trp_indole_centroid(residue):
    return get_aromatic_ring_centroid(residue)


def closest_aromatic_heavy_atom_distance(res_a, res_b):
    coords_a = get_atom_coords(res_a, AROMATIC_RING_ATOMS.get(res_a.get_resname(), []))
    coords_b = get_atom_coords(res_b, AROMATIC_RING_ATOMS.get(res_b.get_resname(), []))
    if coords_a is None or coords_b is None:
        return None
    deltas = coords_a[:, None, :] - coords_b[None, :, :]
    distances = np.linalg.norm(deltas, axis=2)
    idx = np.unravel_index(np.argmin(distances), distances.shape)
    return {
        "distance_angstroms": float(distances[idx]),
        "source_atom_index": int(idx[0]),
        "target_atom_index": int(idx[1]),
    }


def compute_mt_axis_via_pca(structure, target_chains):
    """MT axis from PCA of CA-coordinates restricted to target chains."""
    cas = []
    for model in structure:
        for chain in model:
            if chain.id not in target_chains:
                continue
            for residue in chain:
                if "CA" in residue and is_aa(residue):
                    cas.append(residue["CA"].get_coord())
        break
    cas = np.array(cas)
    centroid = cas.mean(axis=0)
    rel = cas - centroid
    cov = np.cov(rel.T)
    eigvals, eigvecs = np.linalg.eigh(cov)
    axis = eigvecs[:, -1]  # largest variance = MT axis
    along = rel @ axis
    radial_vec = rel - np.outer(along, axis)
    radial = np.linalg.norm(radial_vec, axis=1)
    return centroid, axis, {
        "n_atoms": len(cas),
        "axis_eigenvalues": eigvals.tolist(),
        "axis_length_extent_A": float(along.max() - along.min()),
        "r_min_A": float(radial.min()),
        "r_max_A": float(radial.max()),
        "r_median_A": float(np.median(radial)),
        "r_25pct_A": float(np.percentile(radial, 25)),
        "r_75pct_A": float(np.percentile(radial, 75)),
        "r_mean_A": float(np.mean(radial)),
    }


def radial_position(coord, centroid, axis):
    rel = coord - centroid
    along = float(rel @ axis)
    radial_vec = rel - along * axis
    return float(np.linalg.norm(radial_vec))


def find_nearest_aromatic(structure, trp_residue, trp_centroid, max_distance=RADICAL_PAIR_MAX_DISTANCE_ANG):
    nearest = None
    for model in structure:
        for chain in model:
            for residue in chain:
                if residue == trp_residue:
                    continue
                if residue.get_resname() not in AROMATIC_RESIDUES:
                    continue
                if not is_aa(residue):
                    continue
                ring_centroid = get_aromatic_ring_centroid(residue)
                if ring_centroid is None:
                    continue
                centroid_d = float(np.linalg.norm(ring_centroid - trp_centroid))
                if centroid_d > max_distance + 5.0:  # quick prune
                    continue
                heavy_atom_gate = closest_aromatic_heavy_atom_distance(trp_residue, residue)
                if heavy_atom_gate is None:
                    continue
                d = heavy_atom_gate["distance_angstroms"]
                if d > max_distance:
                    continue
                if nearest is None or d < nearest["distance_angstroms"]:
                    nearest = {
                        "distance_angstroms": d,
                        "centroid_distance_angstroms": centroid_d,
                        "distance_basis": "closest_aromatic_heavy_atom_edge_to_edge",
                        "chain": chain.id,
                        "resnum": int(residue.id[1]),
                        "resname": residue.get_resname(),
                    }
        break
    return nearest


def analyse_pocket_composition(structure, centroid, exclude_residue, radius=HYDROPHOBIC_RADIUS_ANG):
    """Pocket analysis: count hydrophobic, polar, charged residues within radius."""
    counts = {"HYDROPHOBIC": 0, "POLAR": 0, "CHARGED": 0, "OTHER": 0}
    residues_seen = set()
    for model in structure:
        atoms = list(model.get_atoms())
        ns = NeighborSearch(atoms)
        near_atoms = ns.search(centroid, radius)
        for atom in near_atoms:
            res = atom.get_parent()
            if res == exclude_residue or not is_aa(res):
                continue
            res_uid = (res.get_parent().id, res.id[1])
            if res_uid in residues_seen:
                continue
            residues_seen.add(res_uid)
            n = res.get_resname()
            if n in HYDROPHOBIC_RESIDUES:
                counts["HYDROPHOBIC"] += 1
            elif n in CHARGED_RESIDUES:
                counts["CHARGED"] += 1
            elif n in POLAR_RESIDUES:
                counts["POLAR"] += 1
            else:
                counts["OTHER"] += 1
        break
    total = sum(counts.values())
    if total == 0:
        hydrophobic_ratio = 0.0
    else:
        hydrophobic_ratio = counts["HYDROPHOBIC"] / total
    return counts, hydrophobic_ratio, total


def classify_lumen_facing(r, r_axis_mean):
    """Local wall-patch classification; not a full lumen-axis verdict."""
    midplane = r_axis_mean
    if r < midplane - 5.0:  # 5 A inside the midplane
        return "local-inward-candidate"
    elif r > midplane + 5.0:  # 5 A outside the midplane
        return "local-outward-candidate"
    else:
        return "wall-interior"


def analyse_beta_tubulin_6dpu():
    print(f"\n--- 6DPU: explicit β-tubulin chain analysis ---")
    print(f"  α-tubulin chains: {ALPHA_CHAINS_6DPU}")
    print(f"  β-tubulin chains: {BETA_CHAINS_6DPU}")

    structure = parse_structure(PDB_6DPU)

    # MT axis from BOTH α and β CA-positions (better cylinder representation)
    all_chains = ALPHA_CHAINS_6DPU + BETA_CHAINS_6DPU
    centroid, axis, axis_stats = compute_mt_axis_via_pca(structure, all_chains)

    print(f"\n  MT axis statistics (from α + β CA-positions):")
    print(f"    n_atoms used                           : {axis_stats['n_atoms']}")
    print(f"    axis-direction eigenvalues             : {axis_stats['axis_eigenvalues']}")
    print(f"    axis-direction length extent (Å)        : {axis_stats['axis_length_extent_A']:.1f}")
    print(f"    radial distribution: r_min={axis_stats['r_min_A']:.1f}, "
          f"r_25%={axis_stats['r_25pct_A']:.1f}, "
          f"r_median={axis_stats['r_median_A']:.1f}, "
          f"r_75%={axis_stats['r_75pct_A']:.1f}, "
          f"r_max={axis_stats['r_max_A']:.1f}")

    assembled_axis_available = (
        axis_stats["r_max_A"] >= MT_INNER_RADIUS_ANG
        and axis_stats["r_mean_A"] >= 0.75 * MT_INNER_RADIUS_ANG
    )

    # Observed radial mean = local wall-patch radial midplane
    r_axis_mean = axis_stats["r_mean_A"]
    print(f"    observed r_mean (local midplane)       : {r_axis_mean:.1f} Å")
    print(f"    assembled lumen-axis available         : {assembled_axis_available}")

    # Beta-tubulin Trp analysis
    results = []
    print(f"\n  β-tubulin Trp analysis (6 chains):")
    print(f"  {'chain':>5} {'resnum':>6} {'r [Å]':>7} {'classification':>16} "
          f"{'nearest':>15} {'<1.5nm?':>8} {'HΦ':>3} {'PL':>3} {'CH':>3} {'HΦ-ratio':>9}")
    for chain_id in BETA_CHAINS_6DPU:
        trps = get_trp_residues_in_chain(structure, chain_id)
        for residue in trps:
            indole_centroid = get_trp_indole_centroid(residue)
            r = radial_position(indole_centroid, centroid, axis)
            classification = classify_lumen_facing(r, r_axis_mean)
            nearest = find_nearest_aromatic(structure, residue, indole_centroid)
            within_15A = (nearest is not None
                          and nearest["distance_angstroms"] <= RADICAL_PAIR_MAX_DISTANCE_ANG)
            pocket_counts, h_ratio, total_in_pocket = analyse_pocket_composition(
                structure, indole_centroid, residue
            )
            result = {
                "chain": chain_id,
                "resnum": int(residue.id[1]),
                "radial_position_A": r,
                "classification": classification,
                "is_lumen_facing": False,
                "is_local_inward_candidate": classification == "local-inward-candidate",
                "lumen_axis_verified": False,
                "nearest_aromatic": nearest,
                "nearest_within_15A": within_15A,
                "pocket_hydrophobic_count": pocket_counts["HYDROPHOBIC"],
                "pocket_polar_count": pocket_counts["POLAR"],
                "pocket_charged_count": pocket_counts["CHARGED"],
                "pocket_other_count": pocket_counts["OTHER"],
                "pocket_total_count": total_in_pocket,
                "pocket_hydrophobic_ratio": h_ratio,
            }
            results.append(result)
            na_str = (f"{nearest['resname']}{nearest['resnum']}({nearest['distance_angstroms']:.1f})"
                      if nearest else "(none)")
            print(f"  {chain_id:>5} {result['resnum']:>6} {r:>7.1f} "
                  f"{classification:>16} {na_str:>15} "
                  f"{str(within_15A):>8} {pocket_counts['HYDROPHOBIC']:>3} "
                  f"{pocket_counts['POLAR']:>3} {pocket_counts['CHARGED']:>3} "
                  f"{h_ratio:>9.2f}")

    # Aggregate by resnum across the 6 beta chains
    by_resnum = {}
    for r in results:
        by_resnum.setdefault(r["resnum"], []).append(r)

    print(f"\n  Aggregation across the 6 β-tubulin chains:")
    print(f"  {'resnum':>7} {'n_chains':>10} {'local_in%':>11} {'<1.5nm_freq':>12} "
          f"{'mean_HΦ':>9} {'mean_HΦ-ratio':>14}")
    # Clopper-Pearson exact 95% CI for binomial proportion k/n
    # using scipy.stats.beta when available (canonical small-N method).
    def _clopper_pearson(k: int, n: int, alpha: float = 0.05):
        if n == 0:
            return (0.0, 1.0)
        try:
            from scipy.stats import beta as _beta
            lo = _beta.ppf(alpha / 2.0, k, n - k + 1) if k > 0 else 0.0
            hi = _beta.ppf(1 - alpha / 2.0, k + 1, n - k) if k < n else 1.0
            return (float(lo), float(hi))
        except Exception:
            # Fallback: Wilson approximation if scipy unavailable
            p = k / n
            z = 1.96
            denom = 1 + z * z / n
            centre = (p + z * z / (2 * n)) / denom
            half = (z / denom) * (((p * (1 - p) / n) + z * z / (4 * n * n)) ** 0.5)
            return (max(0.0, centre - half), min(1.0, centre + half))

    summary = {}
    for resnum, rows in sorted(by_resnum.items()):
        n = len(rows)
        k_local = sum(1 for r in rows if r["is_local_inward_candidate"])
        local_inward_freq = k_local / n
        k_within = sum(1 for r in rows if r["nearest_within_15A"])
        within_freq = k_within / n
        mean_h = sum(r["pocket_hydrophobic_count"] for r in rows) / n
        mean_h_ratio = sum(r["pocket_hydrophobic_ratio"] for r in rows) / n
        local_inward_ci = _clopper_pearson(k_local, n)
        within_ci = _clopper_pearson(k_within, n)
        summary[resnum] = {
            "n_chains": n,
            "local_inward_freq": local_inward_freq,
            "local_inward_freq_95ci_clopper_pearson": list(local_inward_ci),
            "lumen_freq": None,
            "lumen_axis_verified": False,
            "within_15A_freq": within_freq,
            "within_15A_freq_95ci_clopper_pearson": list(within_ci),
            "mean_hydrophobic_count": mean_h,
            "mean_hydrophobic_ratio": mean_h_ratio,
        }
        print(f"  {resnum:>7} {n:>10} {local_inward_freq:>11.0%} {within_freq:>12.0%} "
              f"{mean_h:>9.1f} {mean_h_ratio:>14.2f}")
        print(f"          local-inward 95% CI: "
              f"[{local_inward_ci[0]:.3f}, {local_inward_ci[1]:.3f}]")

    axis_stats["assembled_mt_lumen_axis_available"] = bool(assembled_axis_available)
    axis_stats["axis_reference_scope"] = AXIS_REFERENCE_SCOPE
    return results, axis_stats, r_axis_mean, summary


def main():
    print("=" * 76)
    print("O.21 PROTOCOL v2: β-tubulin Trp radical-pair host PDB analysis")
    print("=" * 76)

    inventory_1jff = inventory_1jff_chain_b()
    print("\n--- 1JFF: isolated β-tubulin chain-B inventory ---")
    print(f"  PDB available                : {inventory_1jff['pdb_file_available']}")
    print(f"  Standard residues in chain B : {inventory_1jff.get('standard_residue_count')}")
    print(f"  Trp auth_seq_ids             : {inventory_1jff.get('trp_auth_seq_ids')}")
    print(f"  Inventory-only scope         : {inventory_1jff['scope']}")

    results, axis_stats, r_axis_mean, summary = analyse_beta_tubulin_6dpu()

    # Verdict: beta-tubulin Trp residues that are consistently local-inward
    # candidates (>= 50% of chains) AND meet the microenvironment criteria.
    candidates_lumen = [n for n, s in summary.items() if s["local_inward_freq"] >= 0.5]
    candidates_aromatic = [n for n, s in summary.items() if s["within_15A_freq"] >= 0.5]
    candidates_hydrophobic = [n for n, s in summary.items() if s["mean_hydrophobic_ratio"] >= 0.5]

    fully_meets = [n for n in candidates_lumen
                    if n in candidates_aromatic and n in candidates_hydrophobic]

    print(f"\n" + "=" * 76)
    print("VERDICT FOR O.21 (β-tubulin-restricted)")
    print("=" * 76)
    print(f"  Observed local wall-patch midplane (r_mean): {r_axis_mean:.1f} Å")
    print(f"  (Canonical MT inner ~75 Å, outer ~125 Å; observed range "
          f"r_min={axis_stats['r_min_A']:.1f} to r_max={axis_stats['r_max_A']:.1f})")
    print(f"  Assembled lumen-axis reference available  : "
          f"{axis_stats['assembled_mt_lumen_axis_available']}")
    print(f"")
    print(f"  Local-inward in ≥ 50% of β-chains          : {candidates_lumen}")
    print(f"  Nearest aromatic within 1.5 nm (≥ 50%)      : {candidates_aromatic}")
    print(f"  Hydrophobic-pocket ratio ≥ 50% (≥ 50%)     : {candidates_hydrophobic}")
    print(f"  All three criteria met                     : {fully_meets}")

    if fully_meets:
        verdict = (f"(i-partial) CANDIDATE ONLY: β-tubulin Trp residue(s) "
                   f"{fully_meets} satisfy the local 6DPU wall-patch screen "
                   f"(local-inward position, near-neighbour aromatic within "
                   f"1.5 nm, hydrophobic-pocket ratio ≥ 50%) across ≥ 50% of "
                   f"the 6 β-tubulin chains. The assembled-microtubule lumen-axis "
                   f"criterion is not tested by the available 6DPU reference; "
                   f"O.21 full geometric closure requires an assembled-MT "
                   f"lumen-axis analysis.")
    elif candidates_lumen:
        verdict = (f"(i-partial) β-tubulin Trp residue(s) {candidates_lumen} are "
                   f"local-inward in ≥ 50% of chains, but do not meet all three "
                   f"criteria consistently. The assembled-MT lumen-axis criterion "
                   f"remains pending. Other criteria met in "
                   f"varying degrees: near-neighbour aromatic ≥ 50% chains "
                   f"= {candidates_aromatic}; hydrophobic-pocket ratio ≥ 50% "
                   f"= {candidates_hydrophobic}.")
    else:
        verdict = ("(ii) NO β-tubulin Trp residue is local-inward in ≥ 50% of "
                   "the 6 β-tubulin chains in the 6DPU wall-patch screen. "
                   "If the β-tubulin Trp screen returns null, register O.21 "
                   "as an Open Problem; no automatic α-tubulin fallback. "
                   "Alternative substrates require a fresh O.21-class screen.")
    print(f"\n  {verdict}")
    print("=" * 76)

    out = {
        "beta_chains_6DPU": BETA_CHAINS_6DPU,
        "alpha_chains_6DPU": ALPHA_CHAINS_6DPU,
        "pdb_1jff_chain_B_inventory": inventory_1jff,
        "axis_statistics": axis_stats,
        "r_axis_midplane_A": r_axis_mean,
        "axis_reference_scope": AXIS_REFERENCE_SCOPE,
        "assembled_mt_lumen_axis_available": bool(axis_stats["assembled_mt_lumen_axis_available"]),
        "closure_status": "PARTIAL_CANDIDATE_ASSEMBLED_MT_AXIS_PENDING" if fully_meets else "O21_SUBCLOSURE_PENDING",
        "pass": False,
        "MT_canonical_inner_radius_A": MT_INNER_RADIUS_ANG,
        "MT_canonical_outer_radius_A": MT_OUTER_RADIUS_ANG,
        "per_chain_per_resnum_results": [
            {k: (v if not isinstance(v, np.ndarray) else v.tolist())
             for k, v in r.items() if k != "nearest_aromatic"}
            for r in results
        ],
        "aggregation_by_resnum": summary,
        "candidates_local_inward": candidates_lumen,
        "candidates_lumen_facing": [],
        "candidates_within_15A": candidates_aromatic,
        "candidates_hydrophobic": candidates_hydrophobic,
        "fully_meets_local_wall_screen": fully_meets,
        "fully_meets_all_three": [],
        "pending_closure_target": (
            "Assembled-microtubule lumen-axis verification for the candidate "
            "Trp residues using a full 13-protofilament reference or an "
            "equivalent reconstructed lumen-axis frame."
        ),
        "verdict": verdict,
    }

    def sanitize(o):
        if isinstance(o, dict):
            return {k: sanitize(v) for k, v in o.items()}
        if isinstance(o, list):
            return [sanitize(x) for x in o]
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.floating):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, bool):
            return bool(o)
        return o

    if OUTPUT_DIR_AVAILABLE:
        out_path = get_output_path("protocol_o21_beta_tubulin_trp_pdb_results.json")
    else:
        out_path = (ENGINE_ROOT / "data"
                    / "protocol_o21_beta_tubulin_trp_pdb_results.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(sanitize(out), f, indent=2)
    print(f"\nResults saved to: {out_path}")
    print("=" * 76)


if __name__ == "__main__":
    main()
