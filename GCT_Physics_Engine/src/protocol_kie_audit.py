#!/usr/bin/env python3
"""
protocol_kie_audit.py
=====================

Guardrail audit for Protocol D solvent-KIE discipline. The registered
0.4% KIE value is a literature-prior control bound by analogy, not a
direct H2^16O-to-H2^17O radical-pair solvent-KIE measurement.
"""

from __future__ import annotations

import json

from gct_utils import get_output_path


REGISTERED_KIE_BOUND = 4.0e-3
DIRECT_H216O_H217O_RADICAL_PAIR_VERIFIER_AVAILABLE = False


def main() -> int:
    status = "OPEN_CONDITIONAL"
    results = {
        "protocol": "Protocol D solvent-KIE calibration audit",
        "registered_kie_bound_fraction": REGISTERED_KIE_BOUND,
        "registered_kie_bound_percent": REGISTERED_KIE_BOUND * 100.0,
        "direct_H2_16O_to_H2_17O_radical_pair_verifier_available": (
            DIRECT_H216O_H217O_RADICAL_PAIR_VERIFIER_AVAILABLE
        ),
        "provenance": (
            "Tier 3 literature-prior control from general heavy-atom solvent/substrate "
            "isotope-effect and anaesthesia mechanism literature; not a direct "
            "H2^16O/H2^17O radical-pair solvent-KIE calibration."
        ),
        "closure_target": (
            "O.33 requires a direct assembled-substrate H2^16O/H2^17O radical-pair "
            "solvent-KIE calibration before the LORR magnitude comparison can become "
            "an operative quantitative gate."
        ),
        "interpretation": (
            "Protocol D LORR remains a pilot/systematics study under the registered "
            "budget. The NMR polarity gate is the operative spin-entropy discriminator."
        ),
        "status": status,
        "pass": False,
    }

    out_path = get_output_path("protocol_kie_audit_results.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)
        fh.write("\n")

    print("Protocol D solvent-KIE audit")
    print(f"  registered bound: {REGISTERED_KIE_BOUND * 100.0:.2f}%")
    print("  direct H2^16O/H2^17O radical-pair verifier: absent")
    print(f"  status: {status}")
    print(f"  results: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
