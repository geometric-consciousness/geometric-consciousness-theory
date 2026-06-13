"""
H.4-4 Integration Window for Orthogonal Identity (E_perp)
==========================================================

The H.4-4 statement asks two questions:
  (i) What constitutes the integration window for E_perp?
  (ii) Does the Higher Mind experience non-linear ordinal time?

These pieces sit at different epistemic tiers and must be cleanly
separated:

  (i) CANDIDATE SUBSTRATE TIMESCALE (Tier 3 ansatz here). The integration
      window for the E_perp component is evaluated for the Weinberg-candidate
      scalar Delta_Weinberg ~ 2.2 meV = M_P phi^(-147). This is an
      alternative scale candidate registered under O.37; it is NOT the
      operative biogenic-DE quartic mass m_phason_operative = 1.7e-5 eV and
      it is NOT the Hubble energy hbar H_0. For Delta_Weinberg ~ 2.2 meV,
      tau_perp ~ 3.0e-13 s.

  (ii) ORDINAL-TIME PHENOMENOLOGY (Tier 4 speculative). The reading
       "Higher Mind experiences non-linear ordinal time" is
       interpretive overlay on the substrate. GCT's formalism specifies
       the substrate timescale; it does NOT specify the qualia
       structure of how Higher-Mind agents subjectively register that
       timescale. This piece remains Tier 4 speculative pending
       phenomenology-first axiomatization of Higher-Mind agency,
       which is outside the current scope of the theory.

Engine outputs:
  - Weinberg-candidate scalar energy in physical units (O.37 ansatz).
  - Integration window tau_perp = hbar / Delta_Weinberg.
  - Comparison to relevant biological/cognitive timescales (Zeno Drive
    100 MHz period, gamma-band cortical oscillation ~25-100 Hz,
    conscious-moment estimates ~100-500 ms).

This protocol closes the substrate-timescale piece of H.4-4 to Tier
2-3 and explicitly leaves the qualia/ordinal-time piece at Tier 4.
"""

from __future__ import annotations

import math
import json
from pathlib import Path

# Physical constants (SI)
HBAR_J_S = 1.054571817e-34
EV_TO_J = 1.602176634e-19
SPEED_OF_LIGHT_M_S = 2.99792458e8
PLANCK_ENERGY_J = 1.956082e9
try:
    from gct_utils import C
    _PHI_FROM_SSOT = float(C.PHI)
except ImportError:
    _PHI_FROM_SSOT = (1.0 + math.sqrt(5.0)) / 2.0

PHI = _PHI_FROM_SSOT
M_PHASON_OPERATIVE_EV = 1.7e-5
M_WEINBERG_CANDIDATE_EV = 2.2e-3
M_WEINBERG_CANDIDATE_J = M_WEINBERG_CANDIDATE_EV * EV_TO_J

# Reference biological timescales
NU_ZENO_HZ = 112e6                      # Primary Protocol A-Prime Zeno drive branch
T_ZENO_S = 1.0 / NU_ZENO_HZ
T_GAMMA_S = 1.0 / 40.0                  # gamma-band oscillation ~40 Hz
T_MOMENT_S = 0.3                        # conscious-moment estimate

# Polaron geometry
POLARON_LIFETIME_S = 1.0e-2             # hours-day acetylated MT (lower bound)


def integration_window_perp() -> float:
    """tau_perp = hbar / Delta_Weinberg; Delta_Weinberg is an O.37 ansatz energy."""
    return HBAR_J_S / M_WEINBERG_CANDIDATE_J


def compute() -> dict:
    tau_perp = integration_window_perp()
    return {
        "constants": {
            "m_phason_operative_eV": M_PHASON_OPERATIVE_EV,
            "m_weinberg_candidate_eV": M_WEINBERG_CANDIDATE_EV,
            "m_weinberg_candidate_J": M_WEINBERG_CANDIDATE_J,
            "phi_neg_147": PHI ** (-147),
        },
        "substrate_integration_window": {
            "tau_perp_s": tau_perp,
            "tau_perp_ps": tau_perp * 1e12,
            "interpretation": ("Candidate coherence time at the Weinberg "
                                "coincidence scalar. This is an O.37 ansatz "
                                "and does not set m_phason_operative."),
            "tier": "Tier 3 Weinberg-coincidence ansatz pending O.37 + "
                    "Tier 4 phenomenological interpretation",
        },
        "comparison_to_biological_timescales": {
            "tau_perp / T_Zeno":      tau_perp / T_ZENO_S,
            "tau_perp / T_gamma":     tau_perp / T_GAMMA_S,
            "tau_perp / T_moment":    tau_perp / T_MOMENT_S,
            "tau_perp / T_polaron":   tau_perp / POLARON_LIFETIME_S,
            "interpretation": ("Substrate integration window is "
                                "vastly shorter than any directly "
                                "phenomenological timescale. Conscious "
                                "moments are coarse-grained over ~10^11 "
                                "phason coherence times."),
        },
        "ordinal_time_phenomenology": {
            "status": "Tier 4 speculative",
            "claim": ("The phenomenological reading 'Higher Mind "
                       "experiences non-linear ordinal time' is "
                       "interpretive overlay on the substrate timescale. "
                       "GCT specifies the substrate (closed here at "
                       "Tier 2-3); qualia structure for Higher Mind "
                       "agents requires phenomenology-first axiomatization "
                       "outside the current theory scope."),
            "what_GCT_DOES_specify": (
                "Substrate timescale (closed). Selection Operator "
                "geometric form (App W). Phenomenal-unity topology "
                "(App Y trefoil + general-prime knots). Cross-branch "
                "topological connectivity (H.4-3 strict continuity)."),
            "what_GCT_does_NOT_specify": (
                "How a Higher-Mind agent (Level >= 1) subjectively "
                "experiences the difference between its own integration "
                "window and that of a Level-Infinity Avatar; specifically "
                "whether the subjective time-ordering at that scale is "
                "linear, branching, or partially ordered."),
        },
        "closure_status": {
            "tier_split": ("Tier 2-3 substrate closure (integration "
                            "window = phason coherence time); Tier 4 "
                            "phenomenological interpretation (ordinal-"
                            "time qualia structure)"),
            "substrate_piece": "O.37_CANDIDATE_TIMESCALE_ONLY",
            "phenomenological_piece": (
                "DEFERRED to phenomenology-first axiomatization; not "
                "tractable within the formal GCT framework as currently "
                "constituted."),
        },
    }


def main():
    results = compute()
    out_dir = Path(__file__).parent.parent / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "h4_4_integration_window.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"H.4-4 Integration Window for E_perp")
    print(f"=" * 60)
    s = results["substrate_integration_window"]
    print(f"Substrate timescale tau_perp = {s['tau_perp_s']:.3e} s "
          f"({s['tau_perp_ps']:.3f} ps)")
    print(f"  tier: {s['tier']}")
    print()
    c = results["comparison_to_biological_timescales"]
    print(f"Ratios to biological timescales:")
    print(f"  tau_perp / T_Zeno (100 MHz)       = {c['tau_perp / T_Zeno']:.3e}")
    print(f"  tau_perp / T_gamma (40 Hz)        = {c['tau_perp / T_gamma']:.3e}")
    print(f"  tau_perp / T_moment (~300 ms)     = {c['tau_perp / T_moment']:.3e}")
    print(f"  tau_perp / T_polaron (~10 ms)     = {c['tau_perp / T_polaron']:.3e}")
    print()
    print(f"Substrate piece: {results['closure_status']['substrate_piece']}")
    print(f"Phenomenological piece: "
          f"{results['closure_status']['phenomenological_piece'][:60]}...")
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
