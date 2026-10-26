#!/usr/bin/env python3
"""
protocol_o12_nu_zeno_renormalization.py
========================================

Order-of-magnitude estimate of the chiral phonon-polariton frequency-
scale renormalization factor for nu_Zeno = 112 MHz: a Tier 3
order-of-magnitude estimate for Open Problem O.12 (no closure).

REGISTERED PROBLEM (App ORQ O.12)

Reaching the registered nu_Zeno = 112 +/- 10 MHz (a Tier 3 branch value) from
the TrpH+ effective hyperfine scale ~27 MHz (0.97 mT; larger than FAD- ~20 MHz,
Wong, Benjamin & Hore 2023) requires a residual frequency-scale factor of
~4x (3.7-4.5x). The earlier 10-20 MHz indole band and 6-11x factor are withdrawn. The full Tier 2 closure asks for this
factor to be derived from first principles via the chiral phonon-polariton
avoided-crossing RG flow on the magnon dispersion.

Scope: this protocol estimates the O.12 frequency-scale burden at Tier 3; full Tier 2 closure requires the first-principles RG derivation.

This protocol provides an ARITHMETIC ESTIMATE of the coupling the two-level
formula would need for the ~4x residual factor, NOT a consistency check or
a first-principles RG derivation. The
estimate uses the standard two-level avoided-crossing dressing formula
from atom-photon coupling theory (Cohen-Tannoudji, Dupont-Roc, Grynberg
1992 "Atom-Photon Interactions" §IV.C):

  nu_renorm = sqrt(nu_bare^2 + (2g)^2)

where g is the coupling strength between the bare two-level system and
the continuum mode (here, the chiral phonon-polariton).

For nu_renorm/nu_bare in [3.75, 4.49], the required dimensionless coupling
ratio is:
  g / nu_bare = (1/2) sqrt((nu_renorm/nu_bare)^2 - 1)
              in [1.81, 2.19]

The literature-supported CISS input is a spin-polarization percentage band,
not a measured g/nu_bare coupling interval. The operative biological target is
indole/tryptophan residues embedded in a beta-tubulin pocket and coupled to
the local chiral protein field. The operative protein CISS band is 5-20%; the
60% DNA-equivalent edge is retained only as a stress-test upper edge for
Trp-like chiral microenvironments, not as a measured beta-tubulin coupling.
Mapping those polarization data to the model's g/nu_bare target is a Tier 3
translation, not a literature-derived CISS envelope.

VERDICT: TIER 3 ORDER-OF-MAGNITUDE ESTIMATE

The ~4x (3.7-4.5x) residual factor required to reach the 112 +/- 10 MHz branch
window from the TrpH+ ~27 MHz scale corresponds to g/nu_bare in [1.81, 2.19]
in the two-level avoided-crossing formula. The earlier model-defined target
[2.5, 6.0] was set for the withdrawn 10-20 MHz band and is retained only for
comparison; the required range does not fall inside it.

This is an ARITHMETIC ESTIMATE of the coupling the two-level formula would
need (a formula inversion), NOT a consistency check or a first-principles
derivation. Full Tier 2 closure of O.12 requires:
  - Deriving g from the icosahedral AKN tiling structure + CISS spin-
    polarization at Trp microenvironments
  - Explicit RG flow on the magnon dispersion (not a simple two-level
    avoided-crossing formula)
  - Coupling to the App GPE renormalization framework (~41x factor for
    g_single^eff)
"""

import json
import math
from pathlib import Path

try:
    from gct_utils import get_output_path
    OUTPUT_DIR_AVAILABLE = True
except ImportError:
    OUTPUT_DIR_AVAILABLE = False

# Bare scale: TrpH+ effective hyperfine 0.97 mT (Wong, Benjamin & Hore 2023,
# PCCP 25:975), larger than FAD- 0.70 mT. The earlier 10-20 MHz band is withdrawn.
MHZ_PER_MT = 28.025
NU_BARE_MHZ = 0.97 * MHZ_PER_MT  # ~27.2 MHz
NU_BARE_FAD_MHZ = 0.70 * MHZ_PER_MT  # ~19.6 MHz (reference)

# Registered Tier 3 branch window (Ch13 Sec 13.1.2b); a branch value, not an observation
NU_TARGET_MHZ = 112.0
NU_TARGET_HALFWIDTH_MHZ = 10.0

# CISS spin-polarization range (Naaman+ 2019/App BEB protein operative band)
CISS_EFFICIENCY_MIN = 0.05
CISS_EFFICIENCY_MAX = 0.20
# DNA-equivalent ordered-helix stress-test upper edge; not the operative
# protein band used for the A-Prime CISS floor.
CISS_EFFICIENCY_DNA_STRESS_TEST_MAX = 0.60


def renormalized_freq(nu_bare, g):
    """Avoided-crossing dressing: nu_renorm = sqrt(nu_bare^2 + (2g)^2)."""
    return math.sqrt(nu_bare ** 2 + (2 * g) ** 2)


def required_g_over_nu_bare(nu_renorm_over_nu_bare):
    """Invert: given target ratio, solve for g/nu_bare."""
    return 0.5 * math.sqrt(nu_renorm_over_nu_bare ** 2 - 1)


def main():
    print("=" * 76)
    print("O.12 PROTOCOL: nu_Zeno chiral phonon-polariton renormalization estimate")
    print("=" * 76)

    print(f"\nInputs:")
    print(f"  Bare TrpH+ effective hyperfine            : {NU_BARE_MHZ:.1f} MHz (FAD- {NU_BARE_FAD_MHZ:.1f} MHz)")
    print(f"  Target nu_Zeno                             : {NU_TARGET_MHZ} MHz")

    ratio_min = (NU_TARGET_MHZ - NU_TARGET_HALFWIDTH_MHZ) / NU_BARE_MHZ  # ~3.75
    ratio_max = (NU_TARGET_MHZ + NU_TARGET_HALFWIDTH_MHZ) / NU_BARE_MHZ  # ~4.49

    print(f"\nRequired renormalization factor             : "
          f"{ratio_min:.1f}-{ratio_max:.1f}x")

    g_min = required_g_over_nu_bare(ratio_min)
    g_max = required_g_over_nu_bare(ratio_max)

    print(f"\nRequired dimensionless coupling g/nu_bare  :")
    print(f"  For ratio = {ratio_min:.1f}x: g/nu_bare = {g_min:.3f}")
    print(f"  For ratio = {ratio_max:.1f}x: g/nu_bare = {g_max:.3f}")

    print(f"\nCISS-mediated coupling envelope (Tier 3 anchor):")
    print(f"  CISS spin-polarization efficiency        : {CISS_EFFICIENCY_MIN:.0%}-{CISS_EFFICIENCY_MAX:.0%}")
    print(f"  (Naaman-Paltiel-Waldeck 2019 Nat. Rev. Chem. 3:250)")
    print(f"  Earlier model-defined target (comparison only): 2.5-6.0")

    consistent = (g_min >= 2.5 and g_max <= 6.0)

    print(f"\n" + "=" * 76)
    print("VERDICT FOR O.12 (Tier 3 order-of-magnitude estimate; no closure)")
    print("=" * 76)
    print(f"  Required g/nu_bare range                  : [{g_min:.2f}, {g_max:.2f}]")
    print(f"  Earlier model target (comparison only)    : [2.5, 6.0]")
    print(f"  Required range fits model target          : {consistent}")
    print(f"")
    print(f"  The ~4x residual factor (TrpH+ ~27 MHz to the 112 +/- 10 MHz branch window)")
    print(f"  needs g/nu_bare in [{g_min:.2f}, {g_max:.2f}]; the earlier [2.5, 6.0] target")
    print(f"  was set for the withdrawn 10-20 MHz band and is reported for comparison only.")
    print(f"")
    print(f"  STATUS: TIER 3 ORDER-OF-MAGNITUDE ESTIMATE (no closure claimed).")
    print(f"  NOT a first-principles RG derivation. Full Tier 2 closure of O.12")
    print(f"  requires:")
    print(f"    - Deriving g from the icosahedral AKN tiling + CISS at Trp")
    print(f"      microenvironments")
    print(f"    - Explicit RG flow on the magnon dispersion (not avoided crossing)")
    print(f"    - Coupling to App GPE renormalization framework (~41x g_single^eff)")
    print("=" * 76)

    out = {
        "NU_BARE_MHZ": NU_BARE_MHZ,
        "NU_BARE_FAD_MHZ": NU_BARE_FAD_MHZ,
        "bare_scale_source": "Wong, Benjamin & Hore 2023, PCCP 25:975-982 (TrpH+ 0.97 mT; FAD- 0.70 mT)",
        "withdrawn_inputs": "10-20 MHz indole band and 6-11x factor",
        "NU_TARGET_MHZ": NU_TARGET_MHZ,
        "NU_TARGET_HALFWIDTH_MHZ": NU_TARGET_HALFWIDTH_MHZ,
        "required_ratio_min": ratio_min,
        "required_ratio_max": ratio_max,
        "required_g_over_nu_bare_min": g_min,
        "required_g_over_nu_bare_max": g_max,
        "CISS_efficiency_range": [CISS_EFFICIENCY_MIN, CISS_EFFICIENCY_MAX],
        "CISS_DNA_stress_test_upper_edge": CISS_EFFICIENCY_DNA_STRESS_TEST_MAX,
        "CISS_efficiency_scope": "operative protein band [0.05,0.20]; DNA-equivalent 0.60 retained only as stress-test upper edge",
        "avoid_crossing_source": "Cohen-Tannoudji, Dupont-Roc, Grynberg 1992 Atom-Photon Interactions Sec IV.C",
        "ciss_source": "Naaman, Paltiel, Waldeck 2019 Nature Reviews Chemistry 3:250",
        "model_defined_g_over_nu_bare_target": [2.5, 6.0],
        "required_range_fits_model_target": consistent,
        "g_over_nu_scope": "The g/nu_bare interval is a GCT model-defined strong-coupling target inferred from avoided-crossing bookkeeping; CISS literature supplies spin-polarization percentages, not a direct coupling interval.",
        "model_target_note": "The [2.5, 6.0] target was set for the withdrawn 10-20 MHz band; reported for comparison only.",
        "tier_label": "Tier 3 order-of-magnitude estimate (no closure claimed; NOT first-principles RG)",
        "full_tier_2_closure_requires": [
            "Deriving g from icosahedral AKN tiling + CISS at Trp microenvironments",
            "Explicit RG flow on magnon dispersion (not avoided crossing)",
            "Coupling to App GPE renormalization framework (~41x g_single^eff)",
        ],
    }
    if OUTPUT_DIR_AVAILABLE:
        out_path = get_output_path("protocol_o12_nu_zeno_renormalization_results.json")
    else:
        out_path = Path(__file__).resolve().parent.parent / "data" / "protocol_o12_nu_zeno_renormalization_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nResults saved to: {out_path}")
    print("=" * 76)


if __name__ == "__main__":
    main()
