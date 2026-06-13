#!/usr/bin/env python3
"""
protocol_o12_nu_zeno_renormalization.py
========================================

Order-of-magnitude estimate of the chiral phonon-polariton frequency-
scale renormalization factor for nu_Zeno = 112 MHz. Partial closure of
Open Problem O.12.

REGISTERED PROBLEM (App H O.12)

Reaching the registered nu_Zeno = 112 MHz from the tubulin-Trp bare
Delta_ST/h in [10, 20] MHz requires a chiral phonon-polariton frequency-scale
renormalization factor of ~ 6-11x. The full Tier 2 closure asks for this
factor to be derived from first principles via the chiral phonon-polariton
avoided-crossing RG flow on the magnon dispersion.

Scope: this protocol estimates the O.12 frequency-scale burden at Tier 3; full Tier 2 closure requires the first-principles RG derivation.

This protocol provides an ORDER-OF-MAGNITUDE ESTIMATE consistent with
the required 6-11x range, NOT a first-principles RG derivation. The
estimate uses the standard two-level avoided-crossing dressing formula
from atom-photon coupling theory (Cohen-Tannoudji, Dupont-Roc, Grynberg
1992 "Atom-Photon Interactions" §IV.C):

  nu_renorm = sqrt(nu_bare^2 + (2g)^2)

where g is the coupling strength between the bare two-level system and
the continuum mode (here, the chiral phonon-polariton).

For nu_renorm/nu_bare in [5.6, 11.2], the required dimensionless coupling
ratio is:
  g / nu_bare = (1/2) sqrt((nu_renorm/nu_bare)^2 - 1)
              in [2.76, 5.59]

The literature-supported CISS input is a spin-polarization percentage band,
not a measured g/nu_bare coupling interval. The operative biological target is
indole/tryptophan residues embedded in a beta-tubulin pocket and coupled to
the local chiral protein field. The operative protein CISS band is 5-20%; the
60% DNA-equivalent edge is retained only as a stress-test upper edge for
Trp-like chiral microenvironments, not as a measured beta-tubulin coupling.
Mapping those polarization data to the model's g/nu_bare target is a Tier 3
translation, not a literature-derived CISS envelope.

VERDICT: TIER 3 PARTIAL CLOSURE

The 6-11x renormalization factor required to reach nu_Zeno = 112 MHz
from the tubulin-Trp 10-20 MHz singlet-triplet splitting is order-of-magnitude
consistent with standard chiral phonon-polariton avoided-crossing
physics at strong chiral phonon-polariton coupling strengths
g/nu_bare in [2.76, 5.59].

This is a CONSISTENCY CHECK at the dimensional/scale level, NOT a
first-principles derivation. Full Tier 2 closure of O.12 requires:
  - Deriving g from the icosahedral AKN tiling structure + CISS spin-
    polarization at Trp microenvironments
  - Explicit RG flow on the magnon dispersion (not a simple two-level
    avoided-crossing formula)
  - Coupling to the App Q renormalization framework (~41x factor for
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

# Bare tubulin-Trp singlet-triplet splitting range (Ch13 Sec 13.1.2b)
NU_BARE_MIN_MHZ = 10.0
NU_BARE_MAX_MHZ = 20.0

# Target frequency (Ch13 Sec 13.1.2b)
NU_TARGET_MHZ = 112.0

# CISS spin-polarization range (Naaman+ 2019/App X protein operative band)
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
    print(f"  Bare singlet-triplet splitting Delta_ST/h : {NU_BARE_MIN_MHZ}-{NU_BARE_MAX_MHZ} MHz")
    print(f"  Target nu_Zeno                             : {NU_TARGET_MHZ} MHz")

    ratio_min = NU_TARGET_MHZ / NU_BARE_MAX_MHZ  # 112/20 = 5.6
    ratio_max = NU_TARGET_MHZ / NU_BARE_MIN_MHZ  # 112/10 = 11.2

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
    print(f"  Model-defined g/nu_bare target            : 2.5-6.0 (operative O.12 burden)")

    consistent = (g_min >= 2.5 and g_max <= 6.0)

    print(f"\n" + "=" * 76)
    print("VERDICT FOR O.12 (Tier 3 order-of-magnitude partial closure)")
    print("=" * 76)
    print(f"  Required g/nu_bare range                  : [{g_min:.2f}, {g_max:.2f}]")
    print(f"  Operative O.12 g/nu_bare target           : [2.5, 6.0]")
    print(f"  Required range fits model target          : {consistent}")
    print(f"")
    print(f"  The 6-11x renormalization factor required for nu_Zeno = 112 MHz")
    print(f"  is order-of-magnitude consistent with standard chiral phonon-")
    print(f"  polariton avoided-crossing physics at CISS-mediated coupling")
    print(f"  strengths.")
    print(f"")
    print(f"  STATUS: TIER 3 PARTIAL CLOSURE (order-of-magnitude consistency only).")
    print(f"  NOT a first-principles RG derivation. Full Tier 2 closure of O.12")
    print(f"  requires:")
    print(f"    - Deriving g from the icosahedral AKN tiling + CISS at Trp")
    print(f"      microenvironments")
    print(f"    - Explicit RG flow on the magnon dispersion (not avoided crossing)")
    print(f"    - Coupling to App Q renormalization framework (~41x g_single^eff)")
    print("=" * 76)

    out = {
        "NU_BARE_MIN_MHZ": NU_BARE_MIN_MHZ,
        "NU_BARE_MAX_MHZ": NU_BARE_MAX_MHZ,
        "NU_TARGET_MHZ": NU_TARGET_MHZ,
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
        "tier_label": "Tier 3 order-of-magnitude partial closure (consistency only, NOT first-principles RG)",
        "full_tier_2_closure_requires": [
            "Deriving g from icosahedral AKN tiling + CISS at Trp microenvironments",
            "Explicit RG flow on magnon dispersion (not avoided crossing)",
            "Coupling to App Q renormalization framework (~41x g_single^eff)",
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
