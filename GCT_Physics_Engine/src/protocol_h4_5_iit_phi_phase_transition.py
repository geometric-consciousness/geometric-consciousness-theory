"""
H.4-5 Conditional N=144 Construction-Defined Scalar Score
===========================================================

Records a declared scalar-score assignment on the adopted N_cage=144 branch.
The score is 1 immediately below that branch and 25 on the branch. Its
difference (24) and ratio (25) are exact arithmetic on those two assigned
numbers.

No graph G_N is constructed by this protocol. Consequently the score is not a
graph invariant, an edge/vertex min-cut, an IIT quantity, or evidence for a
physical phase transition. The branch location N_cage=144 is inherited from
the Tier 3 O.38 structural posit; the assignment cannot select the cage size.

Cross-reference: App ORQ O.38 (physical cage-size closure) and H.4-5.
"""

from __future__ import annotations

import json
from pathlib import Path

N_CAGE = 144  # Tier 3 cage posit pending O.38
SCORE_BELOW_BRANCH = 1
SCORE_AT_BRANCH = 25


def compute() -> dict:
    delta = SCORE_AT_BRANCH - SCORE_BELOW_BRANCH
    ratio = SCORE_AT_BRANCH / SCORE_BELOW_BRANCH

    return {
        "assignment_parameters": {
            "N_cage": N_CAGE,
            "N_cage_status": (
                "Tier 3 structural posit pending O.38; not selected by this "
                "scalar-score assignment"
            ),
            "score_at_N_minus_1": SCORE_BELOW_BRANCH,
            "score_at_N_cage": SCORE_AT_BRANCH,
        },
        "construction_defined_score_at_N_cage": {
            "score_at_N_minus_1": SCORE_BELOW_BRANCH,
            "score_at_N_cage": SCORE_AT_BRANCH,
            "delta": delta,
            "ratio": ratio,
            "assigned_transition": [SCORE_BELOW_BRANCH, SCORE_AT_BRANCH],
        },
        "closure_status": {
            "tier": (
                "Tier 3 construction-defined diagnostic conditional on the "
                "Tier 3 O.38 N=144 cage posit"
            ),
            "claim": (
                "The declared scalar assignment changes from 1 to 25 at the "
                "adopted N_cage=144 branch; delta=24 and ratio=25 are exact "
                "arithmetic on the assigned values."
            ),
            "scope": (
                "No graph G_N is constructed, so this score is not a graph "
                "invariant or min-cut. It is not IIT Phi and supplies no "
                "physical phase-transition or cage-selection inference."
            ),
            "remaining_open_research_level": (
                "Physical cage-size selection remains O.38. Any graph or IIT "
                "claim requires a separately constructed object and proof."
            ),
        },
    }


def main():
    results = compute()
    out_dir = Path(__file__).parent.parent / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "h4_5_iit_phi_phase_transition.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    transition = results["construction_defined_score_at_N_cage"]
    print("H.4-5 Conditional N=144 Construction-Defined Scalar Score")
    print("=" * 64)
    print(f"Assigned score at N=143: {transition['score_at_N_minus_1']}")
    print(f"Assigned score at N=144: {transition['score_at_N_cage']}")
    print(f"Delta: {transition['delta']}; ratio: {transition['ratio']:.1f}")
    print("No graph invariant, min-cut, IIT, phase-transition, or cage-selection claim.")
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
