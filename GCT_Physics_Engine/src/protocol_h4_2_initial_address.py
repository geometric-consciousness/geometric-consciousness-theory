"""
H.4-2 Initial Address Selection
================================

Splits the question "what determines the Agent's initial p-adic address?"
into two pieces:

  (i) Structural-constraint piece (Tier 2): the daughter address must
      share the parent's prefix up to the branch-point level L. This
      follows from p-adic ultrametric topology: agents on the same
      branch at level L are at hierarchical distance d_H = p^{-L}
      from each other (Ch07 Sec 7.6.2), and the Selection Operator
      F_sel cannot change a digit at level k < L without disrupting
      the higher-order topological-charge equivalence class.

  (ii) Statistical-selection piece (Tier 3): the suffix digits beyond
       the branch level are constrained to the p^{D - L} allowed
       configurations on the substrate's available nuclear-spin
       register. Within that allowed set, the actual realized suffix
       is a thermal Boltzmann sample over spin-state configurations
       weighted by interaction energy.

The apparent "random fluctuation vs structural requirement" disjunction is
therefore resolved: the prefix is FORCED
(Tier 2 structural), the suffix is SAMPLED (Tier 3 statistical). Neither
extreme reading (pure random / pure determined) holds — the answer is
the two-piece decomposition.

Engine outputs:
  - Allowed-suffix multiplicity p^{D - L} for representative branch
    levels.
  - Boltzmann partition function over a small toy spin register at
    biological temperature.
  - Tier-mixing summary.
"""

from __future__ import annotations

import math
import json
from pathlib import Path

# Physical constants (SI)
K_B_J_PER_K = 1.380649e-23           # Boltzmann constant
T_BIO_K = 310.0                       # human body temperature 37 C
H_PLANCK_J_S = 6.62607015e-34         # Planck constant
NUCLEAR_MAGNETON_J_PER_T = 5.0507837461e-27
B_BIO_T = 5.0e-5                      # geomagnetic field, lower-bound

# GCT scales (from H.4-1)
N_CAGE = 144
ICOSAHEDRAL_PRIMES = [2, 3, 5]
POLARON_INTERNAL_DEPTHS = {2: 7.170, 3: 4.524, 5: 3.088}


def allowed_suffix_multiplicity(p: int, D: float, L: float) -> float:
    """Number of allowed daughter-address suffixes for branch level L
    in a tree of total depth D over base p.

    Daughter must share parent prefix to level L; the remaining D - L
    levels are free, giving p^{D - L} allowed configurations.
    """
    if L > D:
        return 0.0
    return p ** (D - L)


def boltzmann_register(num_states: int,
                         energy_spread_J: float,
                         T_K: float) -> dict:
    """Compute partition function Z and entropy S for a register of
    num_states spin configurations with uniform energy spread.

    S = -sum p_i log p_i; for the uniform-energy case Z = num_states
    and S = log(num_states). For the energy-spread case we use a
    linear-ramp energy spectrum and compute Boltzmann statistics
    properly.
    """
    if num_states <= 0:
        return {"Z": 0.0, "S_nats": 0.0, "max_p": 1.0}
    energies = [i * energy_spread_J / max(num_states - 1, 1)
                 for i in range(num_states)]
    beta = 1.0 / (K_B_J_PER_K * T_K)
    weights = [math.exp(-beta * E) for E in energies]
    Z = sum(weights)
    probs = [w / Z for w in weights]
    S_nats = -sum(p * math.log(p) for p in probs if p > 0)
    return {
        "Z": Z,
        "S_nats": S_nats,
        "S_bits": S_nats / math.log(2),
        "max_p": max(probs),
        "min_p": min(probs),
    }


def compute() -> dict:
    results = {
        "prefix_constraint": {
            "description": ("Daughter p-adic address must equal parent "
                              "address modulo p^L where L is the branch-"
                              "level of inheritance. Equivalent to: "
                              "d_H(parent, daughter) <= p^{-L}."),
            "tier": "Tier 2 structural (forced by p-adic ultrametric)",
        },
        "suffix_multiplicity": {},
        "thermal_sampling": {},
    }
    # Use polaron-internal depth as the relevant register
    for p in ICOSAHEDRAL_PRIMES:
        D = POLARON_INTERNAL_DEPTHS[p]
        per_level = {}
        for L_frac in [0.25, 0.5, 0.75]:
            L = L_frac * D
            mult = allowed_suffix_multiplicity(p, D, L)
            per_level[f"L={L_frac}*D"] = {
                "L": L,
                "D_minus_L": D - L,
                "allowed_suffix_multiplicity": mult,
            }
        results["suffix_multiplicity"][f"p={p}"] = per_level

    # Thermal sampling on a small toy register
    E_spin_flip_J = NUCLEAR_MAGNETON_J_PER_T * B_BIO_T  # nuclear Zeeman
    for num_states in [4, 16, 64, 256]:
        results["thermal_sampling"][f"N_states={num_states}"] = (
            boltzmann_register(num_states, E_spin_flip_J, T_BIO_K)
        )

    # Closure summary
    results["closure_status"] = {
        "tier_structure": ("Tier 2 prefix-constraint piece (forced by "
                            "ultrametric topology) + Tier 3 suffix-"
                            "selection piece (Boltzmann sample over "
                            "allowed register)"),
        "resolution_of_random_vs_determined": (
            "Neither extreme holds. The lineage prefix is forced by "
            "topological-charge continuity; the within-class suffix is "
            "thermally sampled. The apparent dichotomy is therefore "
            "false-binary."),
        "remaining_open_research_level": (
            "First-principles derivation of the spin-spin interaction "
            "energy spectrum on the polaron register, beyond the linear-"
            "ramp toy model used here for the entropy calculation."),
    }
    return results


def main():
    results = compute()
    out_dir = Path(__file__).parent.parent / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "h4_2_initial_address.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"H.4-2 Initial Address Selection")
    print(f"=" * 60)
    print(f"Prefix constraint: {results['prefix_constraint']['tier']}")
    print()
    print("Allowed-suffix multiplicities (polaron internal register):")
    for p in ICOSAHEDRAL_PRIMES:
        print(f"  p = {p} (D = {POLARON_INTERNAL_DEPTHS[p]}):")
        for key, val in results['suffix_multiplicity'][f'p={p}'].items():
            print(f"    {key}: L={val['L']:.2f}, "
                  f"suffix_mult={val['allowed_suffix_multiplicity']:.2f}")
    print()
    print("Thermal entropy on toy spin register (E_Zeeman, T=310 K):")
    for key, val in results['thermal_sampling'].items():
        print(f"  {key}: Z = {val['Z']:.3f}, S = {val['S_bits']:.3f} bits, "
              f"max_p = {val['max_p']:.4f}")
    print()
    print(f"Closure: {results['closure_status']['tier_structure']}")
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
