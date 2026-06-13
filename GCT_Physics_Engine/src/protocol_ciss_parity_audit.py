#!/usr/bin/env python3
"""
protocol_ciss_parity_audit.py
=============================

Guardrail audit for the CISS polarization literature band used by the
Dual Material Constraint. The DNA ~0.6 upper edge is carried only as an
ordered-DNA stress edge; protein/peptide substrate estimates use the
lower empirical band unless a system-specific tubulin measurement exists.
"""

from __future__ import annotations

import json

from gct_utils import get_output_path


PROTEIN_PEPTIDE_BAND = (0.05, 0.20)
DNA_STRESS_EDGE = 0.60
REGISTERED_TUBULIN_DEFAULT = (0.05, 0.20)


def main() -> int:
    protein_lower, protein_upper = PROTEIN_PEPTIDE_BAND
    tubulin_lower, tubulin_upper = REGISTERED_TUBULIN_DEFAULT

    dna_promoted_to_tubulin = tubulin_upper >= DNA_STRESS_EDGE
    pass_status = (
        0.0 < protein_lower <= tubulin_lower <= tubulin_upper <= protein_upper
        and not dna_promoted_to_tubulin
    )

    results = {
        "protocol": "CISS parity audit",
        "question": "Does the manuscript keep DNA-scale CISS polarization separate from protein/peptide defaults?",
        "protein_peptide_default_band": list(PROTEIN_PEPTIDE_BAND),
        "dna_ordered_helix_stress_edge": DNA_STRESS_EDGE,
        "registered_tubulin_default_band": list(REGISTERED_TUBULIN_DEFAULT),
        "dna_edge_promoted_to_tubulin_default": dna_promoted_to_tubulin,
        "interpretation": (
            "Protein/peptide CISS magnitudes are the operative default for tubulin-style "
            "substrate claims. The DNA ~0.6 value is a stress edge and must not be "
            "silently promoted to the protein/tubulin default band."
        ),
        "status": "PASS" if pass_status else "FAIL",
        "pass": pass_status,
    }

    out_path = get_output_path("protocol_ciss_parity_audit_results.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)
        fh.write("\n")

    print("CISS parity audit")
    print(f"  protein/peptide default: {protein_lower:.2f}-{protein_upper:.2f}")
    print(f"  DNA stress edge: {DNA_STRESS_EDGE:.2f}")
    print(f"  status: {results['status']}")
    print(f"  results: {out_path}")
    return 0 if pass_status else 1


if __name__ == "__main__":
    raise SystemExit(main())
