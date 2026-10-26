#!/usr/bin/env python3
"""
protocol_fermion_audit.py — Particle Inventory Audit
=========================================================================
Generates the "Particle Inventory" of the GCT 6D vacuum by:
1. Assigning defect topologies to candidate SU(3) representations (Tier 3).
2. Checking gauge invariance under the Tier 3 gluon-redundancy reading.
3. Recording Spin-Statistics as a POSTULATE (Fermionic -1 phase under 360°).

The lepton/quark dimensions (1 and
3) are computed as orbit sizes under the RT 3-fold rotation, and
spin-statistics is recorded as a postulate. None of the three remaining checks
can fail: the vertex orbit is 1 because the rotation axis is defined through
that vertex; every off-axis point has orbit 3 under an order-3 rotation; and
the gauge-redundancy scan rotates lattice.u_displacement, which is initialised
to zero, so the energy change is identically 0. The checks are recorded as
consistent, and the protocol is registered as open (pass = false).
"""

import numpy as np
import json
from pathlib import Path

# GCT Imports
from gct_lattice import GCTLattice
from gct_utils import get_output_path
from gct_hamiltonian import GCTHamiltonian
from gct_geometry import RhombicTriacontahedron
from gct_gauge import GaugeGenerator
from gct_representations import RepresentationAnalyzer
from gct_redundancy import GaugeRedundancyVerifier


def check_fermi_statistics(n_steps: int = 360) -> dict:
    """
    Check Fermionic spin-statistics via the "Identity Tether" argument.
    
    A Fermion gains a -1 phase (Berry phase = π) under a 2π (360°) rotation.
    
    We model this as: the phason frame of a DEFECT traces a closed loop in
    E_perp. For a Topological Defect, the frame must rotate by 4π to return
    to the identity => half-integer spin => Fermionic.
    
    This is the discrete analog of the "belt trick" / spinor argument:
    A defect is a topological object. In the fundamental group of SO(3) = Z2,
    a 2π rotation is non-contractible (non-trivial loop), giving phase -1.
    """
    # Simulate 360° rotation in 6D phason frame
    # Key test: whether the internal phason frame picks up a sign under 2*pi rotation.
    
    # Use the RT's double cover (spin cover of SO(3) = SU(2))
    # Under a full circle, a spinor picks up e^(i*pi) = -1.
    
    # Simple model: track a unit vector rotating in E_perp.
    # Defect "tether" is a frame attached to its environment.
    # Under 2*pi rotation of the Lab, the tether picks up -1 for Fermions.
    
    # We simulate this via the Berry phase of the PHASON FRAME rotation.
    # For a Z2 defect (Fermion), Berry phase over 360° = pi.
    
    # Here we just implement the analytic result and its geometric derivation.
    
    # The defect lives at the center of a lattice vacancy (a hole in Z6).
    # When we carry the defect around a loop, the phason frame rotates.
    # For a GCT "Lepton" (vertex defect, N=144):
    #   The SU(2) double cover gives a -1 sign after 2*pi.
    #   This is the geometric origin of Fermi statistics.
    
    phase_per_step = np.pi / n_steps  # Half-winding per full rotation
    total_phase = 0.0
    
    for _ in range(n_steps):
        total_phase += phase_per_step
    
    fermi_phase = total_phase  # Target phase: pi.
    is_fermion = abs(fermi_phase - np.pi) < 0.01
    
    return {
        "berry_phase_lepton": float(fermi_phase / np.pi),  # In units of pi
        "expected_fermion_phase": 1.0,  # = pi in units of pi
        "is_fermion": is_fermion,
        "note": "ID-Tether (Spinor Argument): Phase = π under 2π rotation => Fermionic."
    }


def compute_z3_orbit_sizes(hull, tol: float = 1e-6) -> dict:
    """Orbit sizes of a 3-valent RT vertex and an adjacent face centre under
    the 120-degree rotation about that vertex's (3-fold) axis."""
    P = hull.points
    faces = {}
    for simp, eq in zip(hull.simplices, hull.equations):
        faces.setdefault(tuple(np.round(eq[:3], 6)), set()).update(simp.tolist())
    faces = [sorted(f) for f in faces.values()]
    v_idx = next(i for i in hull.vertices if sum(i in f for f in faces) == 3)
    axis = P[v_idx] / np.linalg.norm(P[v_idx])
    K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    R = np.eye(3) + np.sin(2 * np.pi / 3) * K + (1 - np.cos(2 * np.pi / 3)) * (K @ K)
    face_centre = P[next(f for f in faces if v_idx in f)].mean(axis=0)

    def orbit(x):
        imgs = [x, R @ x, R @ R @ x]
        return len({tuple(np.round(p / tol) * tol) for p in imgs})

    return {"vertex_orbit_size": orbit(P[v_idx]), "face_centre_orbit_size": orbit(face_centre),
            "rotation_is_order_3": bool(np.allclose(R @ R @ R, np.eye(3)))}


def run_fermion_audit():
    print("=" * 60)
    print("GCT Protocol: Fermion Audit")
    print("=" * 60)

    results = {}

    # Setup
    rt = RhombicTriacontahedron()
    analyzer = RepresentationAnalyzer(rt.hull)

    # -------------------------------------------------------
    # Step 1: Classify Vertex Defect (Lepton)
    # -------------------------------------------------------
    print("\n1. Vertex Defect (Lepton Candidate)...")
    lepton_rep = analyzer.classify_defect_topology("vertex")
    bp_lepton  = analyzer.compute_berry_phase("vertex")
    orbits     = compute_z3_orbit_sizes(rt.hull)
    print(f"   Computed Z3 orbit sizes: vertex {orbits['vertex_orbit_size']}, "
          f"adjacent face centre {orbits['face_centre_orbit_size']}")

    print(f"   Representation: {lepton_rep['name']}")
    print(f"   Berry Phase:    {bp_lepton:.4f} * pi  (expect 0)")

    results["lepton"] = {
        **lepton_rep,
        "berry_phase_pi": bp_lepton,
        "su3_coupling": 0,
        "computed_z3_orbit_size": orbits["vertex_orbit_size"],
        "verdict": "Lepton Candidate Consistent" if orbits["vertex_orbit_size"] == lepton_rep["dimension"] == 1 else "FAIL"
    }

    # -------------------------------------------------------
    # Step 2: Classify Face Defect (Quark)
    # -------------------------------------------------------
    print("\n2. Face Defect (Quark Candidate)...")
    quark_rep = analyzer.classify_defect_topology("face")
    bp_quark  = analyzer.compute_berry_phase("face")

    print(f"   Representation: {quark_rep['name']}")
    print(f"   Berry Phase:    {bp_quark:.4f} * pi  (expect 2/3 ≈ 0.667)")

    results["quark"] = {
        **quark_rep,
        "berry_phase_pi": bp_quark,
        "su3_coupling": 1,
        "computed_z3_orbit_size": orbits["face_centre_orbit_size"],
        "verdict": "Quark Candidate Consistent" if orbits["face_centre_orbit_size"] == quark_rep["dimension"] == 3 else "FAIL"
    }

    # -------------------------------------------------------
    # Step 3: Gauge Invariance (Gluon Redundancy)
    # -------------------------------------------------------
    print("\n3. Verifying Gauge Invariance (Gluon Redundancy)...")

    lattice = GCTLattice(R=1, perp_cutoff=1.5)
    H = GCTHamiltonian(lattice)

    # Build a generator from RT axes
    rt_axes = GaugeGenerator.identify_3fold_axes(rt.hull)
    if rt_axes:
        seed_axis = rt_axes[0]
        v = seed_axis.reshape(3, 1)
        gen = (v @ v.T - np.eye(3) / 3.0)
    else:
        gen = np.diag([1.0, -1.0, 0.0])

    gauge_result = GaugeRedundancyVerifier.scan_all_sites(lattice, H, gen, max_sites=5)

    print(f"   Sites tested:   {gauge_result['n_sites_tested']}")
    print(f"   Invariant:      {gauge_result['n_invariant']}/{gauge_result['n_sites_tested']}")
    print(f"   Max delta_E:    {gauge_result['max_delta_E']:.2e}")

    results["gauge_invariance"] = {
        **gauge_result,
        "verdict": "Gluon Redundancy Candidate Consistent" if gauge_result["all_invariant"] else "FAIL"
    }

    # -------------------------------------------------------
    # Step 4: Spin-Statistics
    # -------------------------------------------------------
    print("\n4. Spin-Statistics (POSTULATE; not computed, does not gate PASS)...")
    spin_result = check_fermi_statistics()

    print(f"   Berry Phase (Lepton):   {spin_result['berry_phase_lepton']:.4f} * pi")
    print(f"   Is Fermion:            {spin_result['is_fermion']}")

    results["spin_statistics"] = {
        **spin_result,
        "status": "POSTULATE_NOT_COMPUTED: the phase loop sums pi/n n times and cannot fail; Fermi statistics of the defect is assumed",
        "verdict": "POSTULATE"
    }

    # -------------------------------------------------------
    # Final Summary
    # -------------------------------------------------------
    print("\n" + "=" * 60)
    all_verdicts = [
        results["lepton"]["verdict"] == "Lepton Candidate Consistent",
        results["quark"]["verdict"] == "Quark Candidate Consistent",
        results["gauge_invariance"]["verdict"] == "Gluon Redundancy Candidate Consistent",
    ]
    results["z3_orbit_computation"] = orbits

    checks_consistent = all(all_verdicts)
    results["checks_consistent"] = checks_consistent
    results["closure_status"] = (
        "OPEN: the vertex orbit is 1 by construction (axis through the vertex), any off-axis point "
        "has orbit 3 under an order-3 rotation, and the gauge scan rotates a zero displacement field "
        "(max |u| = 0), so delta_E = 0 for any generator; none of the checks can fail"
    )
    results["verdict"] = ("OPEN_INVENTORY_CHECKS_HOLD_BY_CONSTRUCTION" if checks_consistent
                          else "FAIL")
    if checks_consistent:
        print("Particle-inventory checks consistent (they hold by construction; open).")
        print("  Leptons => SU(3) singlet candidate (vertex defect).")
        print("  Quarks  => SU(3) triplet candidate (face defect).")
        print("  Gluons  => proposed local gauge redundancy of phason orientation.")
        print("  Candidate reading: SM particles as topological features of the 6D lattice.")
    else:
        print("PARTIAL: Some checks failed. See results for details.")
    print("=" * 60)

    # Save: the checks cannot fail, so they do not count as a confirmation.
    results["pass"] = False
    out_path = get_output_path("protocol_fermion_audit_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_path}")

    return results


if __name__ == "__main__":
    run_fermion_audit()
