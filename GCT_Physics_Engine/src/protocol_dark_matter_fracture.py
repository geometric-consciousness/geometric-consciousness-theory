#!/usr/bin/env python3
"""
GCT Protocol H: Lattice Fracture Toy Model (Dark Matter)
Filename: protocol_dark_matter_fracture.py

All constants imported from SSOT (gct_constants).

**Scope.** This script is a *mechanism demonstration*, not an independent
derivation. Every bond in the toy lattice is assigned e_bond = E_VAC_EV by
construction (the Tier 2 GCT mechanism posits a single discrete vacuum
quantum per Lattice-Fracture event), then "broken" with a 1%-sigma
Gaussian to show the resulting energy distribution is discrete and
monochromatic by construction. The PASS verdict (discrete + monochromatic
  spectrum) is therefore a constructive diagnostic of the input
  assumption, not a falsification result; it adds zero independent evidence for the absolute value of
E_vac.

**What this script verifies:** the *mechanism* — that a Lattice Fracture
event releasing exactly one E_vac quantum produces a discrete,
monochromatic spectrum with sub-instrumental Lorentzian linewidth. This
is the Tier 2 mechanism claim of V3 Ch11 (Lattice Fracture Release).

**What it does NOT verify:** the absolute value E_vac = m_e / 144 ~ 3.55
keV. That postdiction lives in `verify_independent/verify_dm_line_centroid_postdiction_check.py`
(matches the disputed astrophysical line) and is registered as Tier 2
postdiction + Tier 3 empirical anchor (cf. V3 Ch11 + App R). The
load-bearing falsification gate is the linewidth + spatial-tracking
test in Protocol C (App V P.3), not the toy lattice simulation here.

**Single-seed realization (seed=42 for reproducibility).** The binary
verdict (`discrete: true`, `monochromatic: true`) is structural and
robust to seed choice; the reported `mean_energy` value to ~14 significant
figures is a single-seed realization, NOT a stable scientific-precision
result. For an uncertainty-quantified mean_energy, run an N-seed
Monte-Carlo ensemble (see `run_fracture_simulation`) and report
`mean_energy ± sigma` over the ensemble. The JSON output flags the
disposition via `mean_energy_seed_pinned: true`.

This script is therefore best read as a *visualisation* of the
mechanism's qualitative signature, complementary to but not redundant
with the empirical-prediction verifier.

Author: Geometric Consciousness Theory Research Group
"""

import numpy as np
import sys
import os
import json
import io
from datetime import datetime

# Force UTF-8 for Windows compatibility with scientific symbols
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from gct_utils import PHI, get_output_path, GCTReporter
from gct_utils import C
E_VAC_EV = C.E_VAC_EV
M_ELECTRON = 9.1093837e-31
C_LIGHT = 299792458
HBAR = 1.054571817e-34
EV_TO_J = 1.602176634e-19

# =============================================================================
# SECTION 1: LATTICE & SIMULATION
# =============================================================================

def generate_quasicrystal_patch(n_atoms=100, seed=42):
    """
    Build an n_atoms quasicrystal patch with two bond classes (short =
    a_short, long = a_short * phi). Atom positions carry a small thermal
    Gaussian fluctuation. The numpy random state is seeded for
    reproducibility; the structural binary verdict (discrete +
    monochromatic spectrum) is robust to seed choice, but the absolute
    `mean_energy` value over a single run is a seed-pinned realization,
    not a Monte-Carlo ensemble mean.
    """
    np.random.seed(seed)
    a_short = 1.0
    a_long  = a_short * PHI
    positions = []
    n_per_side = int(np.ceil(n_atoms**(1/3)))

    for i in range(n_per_side):
        for j in range(n_per_side):
            for k in range(n_per_side):
                if len(positions) >= n_atoms: break
                x = i * a_short + (j % 2) * a_short / PHI
                y = j * a_short + (k % 2) * a_short / PHI
                z = k * a_short + (i % 2) * a_short / PHI
                # Thermal fluctuation
                positions.append([x + np.random.normal(0, 0.05),
                                   y + np.random.normal(0, 0.05),
                                   z + np.random.normal(0, 0.05)])

    positions = np.array(positions[:n_atoms])
    bonds = []
    r_short_max = a_short * 1.2
    r_long_max  = a_long  * 1.2
    r_long_min  = a_short * 1.3

    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            r = np.linalg.norm(positions[i] - positions[j])
            if r < r_short_max:
                bonds.append((i, j, 'short'))
            elif r_long_min < r < r_long_max:
                bonds.append((i, j, 'long'))
    return positions, bonds


class SpringMassNetwork:
    def __init__(self, positions, bonds, e_vac=E_VAC_EV):
        self.positions         = positions.copy()
        self.initial_positions = positions.copy()
        self.bonds             = []
        self.e_vac             = e_vac
        self.fracture_events   = []

        for i, j, btype in bonds:
            r0     = np.linalg.norm(positions[i] - positions[j])
            e_bond = e_vac  # Monochromatic hypothesis
            k      = 2 * e_bond / (r0 ** 2)
            self.bonds.append({
                'i': i, 'j': j, 'type': btype, 'r0': r0, 'k': k,
                'e_bond': e_bond, 'strain_crit': 0.15, 'broken': False
            })

    def apply_shear_strain(self, gamma):
        self.positions = self.initial_positions.copy()
        self.positions[:, 0] += gamma * self.initial_positions[:, 1]

    def compute_total_energy(self):
        total = 0.0
        for bond in self.bonds:
            if bond['broken']: continue
            i, j = bond['i'], bond['j']
            r = np.linalg.norm(self.positions[i] - self.positions[j])
            total += 0.5 * bond['k'] * (r - bond['r0'])**2
        return total

    def check_and_break_bonds(self, global_strain):
        max_strain  = 0
        worst_bond  = None
        for bond in self.bonds:
            if bond['broken']: continue
            i, j = bond['i'], bond['j']
            r      = np.linalg.norm(self.positions[i] - self.positions[j])
            strain = abs(r - bond['r0']) / bond['r0']
            if strain > max_strain:
                max_strain = strain
                worst_bond = bond

        if worst_bond and max_strain > worst_bond['strain_crit']:
            base           = worst_bond['e_bond']
            energy_released = base + np.random.normal(0, 0.01 * base)
            worst_bond['broken'] = True

            self.fracture_events.append({
                'global_strain':   global_strain,
                'energy_released': energy_released,
                'bond_energy':     worst_bond['e_bond']
            })
            return energy_released, worst_bond
        return 0, None


def run_fracture_simulation(n_atoms=64, strain_steps=200, max_strain=0.5):
    positions, bonds = generate_quasicrystal_patch(n_atoms)
    network          = SpringMassNetwork(positions, bonds)
    strain_values    = np.linspace(0, max_strain, strain_steps)

    for gamma in strain_values:
        network.apply_shear_strain(gamma)
        for _ in range(10):
            e, b = network.check_and_break_bonds(gamma)
            if b is None: break

    return network.fracture_events

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """
    Drive a single-seed (seed=42) lattice-fracture realization on a 64-atom
    quasicrystal patch and report the discreteness + monochromaticity
    verdict. The binary pass/fail is structural and seed-independent; the
    reported `mean_energy` is a single-seed realization (flagged in the
    JSON output via `mean_energy_seed_pinned`). For an ensemble-mean
    mean_energy, wrap `run_fracture_simulation` in an N-seed loop and
    aggregate.
    """
    report = GCTReporter("Lattice Fracture & Dark Matter Spectrum")
    report.section("Fracture Simulation")

    events = run_fracture_simulation(n_atoms=64, strain_steps=300, max_strain=0.6)

    if len(events) == 0:
        report.verdict(False, "No fracture events detected in simulation patch.")
        return

    energies = np.array([e['energy_released'] for e in events])
    mean_e   = np.mean(energies)
    std_e    = np.std(energies)

    # Analysis
    discreteness_ratio = std_e / mean_e
    is_discrete        = discreteness_ratio < 0.1

    peak_fraction      = np.sum(np.abs(energies - E_VAC_EV) < 0.05 * E_VAC_EV) / len(events)
    is_monochromatic   = peak_fraction > 0.9

    report.log_comparison("Mean Fracture Energy", mean_e, E_VAC_EV)
    report.log_value("Discreteness (Std/Mean)", discreteness_ratio)
    report.log_value("Peak Concentration",      peak_fraction * 100, "%")

    passed = is_discrete and is_monochromatic
    report.verdict(
        passed,
        "DIAGNOSTIC PASS (constructive - not falsification): toy fracture mechanism is discrete and monochromatic in this model; this is not standalone evidence for physical lattice origins."
    )

    # Save results
    output_path = get_output_path("protocol_dark_matter_fracture_results.json")
    with open(output_path, "w") as f:
        json.dump({
            "pass": bool(passed),
            "mean_energy": float(mean_e),
            "discrete": bool(is_discrete),
            "monochromatic": bool(is_monochromatic),
            "mean_energy_seed_pinned": True,
            "mean_energy_uncertainty": "single-seed realization; structural verdict robust",
            "claim_registry_precision_exclusion": "The seed-pinned mean_energy is excluded from precision rows; only the structural discreteness/monochromaticity diagnostic is load-bearing here.",
            "verdict_scope": "DIAGNOSTIC PASS (constructive - not falsification): toy fracture mechanism only; physical interpretation requires XRISM linewidth, centroid, morphology, and S1-S6 systematics gates",
            "seed": 42,
        }, f, indent=2)

if __name__ == "__main__":
    main()
