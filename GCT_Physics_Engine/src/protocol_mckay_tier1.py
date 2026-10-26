#!/usr/bin/env python3
"""
protocol_mckay_tier1.py — McKay Tier 1 Verification Protocol
=============================================================
This protocol asserts the Tier 1 McKay step by checking the actual
binary-icosahedral character-fusion correspondence: irreducible 2I
representations tensor the defining SU(2) representation with adjacency
matrix equal to the affine E8 Dynkin graph.
"""

import sys
import json
import numpy as np
from gct_mckay_e8 import run_mckay_e8_audit, MCKAY_REPORT_TIER
from gct_utils import get_output_path

# App Axiom & Postulate Ledger (6D Euclidean Parent Lattice, Tier 1/2);
# Parameter Ledger (primitive-P adopted, not uniquely derived); App TAT.
LATTICE_6D_TIER = (
    "Tier 1/2 architectural postulate (P1); McKay 2I->E8 is a conditional "
    "Tier 1 result and does not derive Z^6"
)

def run_protocol():
    print("=" * 65)
    print("GCT Protocol: McKay Tier 1 Correspondence Check (within its hypotheses)")
    print("=" * 65)
    
    # Run the core E8 McKay audit
    audit_results = run_mckay_e8_audit()
    
    # Assertions
    # 1. Must pass the 2I character-fusion/E8 graph verification
    if not audit_results.get("pass"):
        print("FAIL: Core McKay E8/H4 verification failed.")
        sys.exit(1)

    mckay = audit_results.get("mckay_correspondence", {})
    if not mckay.get("mckay_equivalence_verified", audit_results.get("mckay_equivalence_verified", False)):
        # The top-level summary also exposes this value.
        if not audit_results.get("mckay_equivalence_verified"):
            print("FAIL: McKay equivalence flag not verified.")
            sys.exit(1)
    if mckay.get("irrep_dimensions") != sorted(mckay.get("expected_affine_e8_marks", [])):
        print("FAIL: 2I irrep dimensions do not match affine E8 marks.")
        sys.exit(1)
    if not mckay.get("affine_e8_graph_match"):
        print("FAIL: Fusion graph is not affine E8.")
        sys.exit(1)
    if not mckay.get("dimension_vector_is_affine_null_root"):
        print("FAIL: Irrep-dimension vector is not the affine E8 null root.")
        sys.exit(1)
        
    # 2. Report tier must carry the conditional Tier 1/2 classification
    #    (App USS Lemma III), not a derived-necessity label.
    if audit_results.get("tier") != MCKAY_REPORT_TIER:
        print("FAIL: Classification error. Expected the conditional Tier 1/2 report tier.")
        sys.exit(1)
    if audit_results.get("lemma_iii", {}).get("exhaustive_uniqueness_proof") is not False:
        print("FAIL: Lemma III must be reported as a conditional comparison, not a uniqueness proof.")
        sys.exit(1)
        
    # 3. Must verify the H4 Cartan/root-metric phi check
    h4 = audit_results.get("h4_coxeter", {})
    if not h4.get("phi_verified"):
        print("FAIL: H4 Cartan/root-metric phi check not verified.")
        sys.exit(1)
        
    print("\n[VERDICT] Tier 1 McKay correspondence (2I -> affine E8): VERIFIED within its hypotheses")
    print("[LOG] 2I irreps + defining-SU(2) fusion reproduce affine E8.")
    print(f"[LOG] 6D parent lattice: {LATTICE_6D_TIER}")
    print("=" * 65)
    
    # Save protocol-specific result and the intentionally derived compact
    # summary consumed by the publication-boundary structure listing.
    summary = {
        "protocol": "McKay_Tier1",
        "pass": True,
        "verdict": "PASS",
        "tier": "Tier 1",
        "tier_scope": "2I -> affine E8 McKay correspondence only, within its hypotheses; architecture use is Tier 1/2 conditional (App USS Lemma III)",
        "6d_lattice_tier": LATTICE_6D_TIER,
        "mckay_correspondence": {
            "irrep_dimensions": mckay.get("irrep_dimensions"),
            "expected_affine_e8_marks": mckay.get("expected_affine_e8_marks"),
            "defining_irrep_index": mckay.get("defining_irrep_index"),
            "fusion_edge_count": mckay.get("fusion_edge_count"),
            "affine_e8_graph_match": mckay.get("affine_e8_graph_match"),
            "dimension_vector_is_affine_null_root": mckay.get("dimension_vector_is_affine_null_root"),
            "method": mckay.get("method"),
        },
        "h4_coxeter": h4
    }
    
    out_path = get_output_path("protocol_mckay_tier1_results.json")
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)

    compact_summary = {
        "protocol": "McKay_Tier1",
        "verdict": "PASS",
        "tier": "Tier 1",
        "h4_coxeter": h4,
    }
    summary_path = get_output_path("protocol_mckay_tier1_summary.json")
    with open(summary_path, "w") as f:
        json.dump(compact_summary, f, indent=2)
        
    sys.exit(0)

if __name__ == "__main__":
    run_protocol()
