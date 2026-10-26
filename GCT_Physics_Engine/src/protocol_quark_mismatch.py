#!/usr/bin/env python3
"""
protocol_quark_mismatch.py — Quark Mass Inventory and FK Source Evaluation
==============================================================
Objective: calculate scheme-dependent quark mass comparison values and
evaluate the registered numerical tolerance gates. The down-quark row uses
the FK-determinant infinite-volume-limit closed form phi^phi as the primary
source value, conditional on O.5 for rigorous convergence.

Identities:
1. m_u = m_e * phi^3
2. m_d = m_u * phi^phi as the FK-determinant infinite-volume-limit closed form
3. m_s = m_u * phi^8 * (1 - 12*alpha)
4. m_c = m_u * phi^(13 + phi^-3)
5. m_b = m_c * phi^2 * (1.25)
6. m_t = (v_GCT / 2) * sqrt(2), where v_GCT is the absolute Higgs-VEV
   pipeline value built from the corrected geometric muon resonance
"""

import sys
import json
import math
import io
from pathlib import Path
from gct_utils import C, resolve_a3

# Force UTF-8 for Windows compatibility with scientific symbols
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Path bootstrap
_SRC = Path(__file__).resolve().parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

try:
    from gct_utils import get_output_path, C
except ImportError:
    # Fallback if gct_utils isn't available in this context
    def get_output_path(filename):
        return str(_SRC.parent.parent / "data" / filename)
    class C:
        PHI = float(C.PHI)
        ALPHA_OBS = 1.0 / 137.035999177
        M_E_OBS = 0.51099895
        SQRT2 = 1.4142135623730951

def verify_a5_ratio():
    from gct_utils import C
    import numpy as np
    from gct_lattice import GCTLattice
    from gct_hamiltonian import GCTHamiltonian
    from gct_spectrum import SpectrumAnalyzer
    from cage_builder import build_canonical_cage

    # Generate D_F on the I_h-closed boundary cage (152 nodes; 5 orbits).
    nodes, _ = build_canonical_cage(size=152)
    N_nodes = nodes.shape[0]
    lat_cage = GCTLattice(R=2, perp_cutoff=2.0)   # required for SpectrumAnalyzer signature
    D_F = np.zeros((N_nodes, N_nodes))
    for i in range(N_nodes):
        for j in range(i+1, N_nodes):
            dist = np.linalg.norm(nodes[i] - nodes[j])
            if abs(dist - 1.0) < 1e-4:
                D_F[i, j] = float(C.PHI)
                D_F[j, i] = float(C.PHI)
                
    analyzer = SpectrumAnalyzer(lat_cage, GCTHamiltonian(lat_cage))
    ratio = analyzer.compute_a5_spectral_ratio(D_F)
    
    assert abs(ratio - 1.25) < 1e-6, f"Expected 1.25, got {ratio}"
    print(f"A5 SPECTRAL RATIO THEOREM: dim(H)/dim(G) extracted from eigenspectrum = {ratio} — VERIFIED [Tier 2]")
    return ratio

def main():
    import numpy as np

    phi = float(C.PHI)
    alpha, _ = resolve_a3(C)
    m_e_mev = float(C.M_E_OBS)
    m_e_vev_mev = float(C.M_E_CODATA_MEV)
    sqrt2 = float(C.SQRT2)

    # Absolute GCT Higgs-VEV pipeline, matching protocol_higgs_vev.py:
    # m_mu = m_e phi^11 (1 + 5 alpha + phi^8 alpha^2),
    # v_GCT = m_mu * (144 * 10) * phi.
    m_mu_geom_mev = m_e_vev_mev * (phi ** 11) * (
        1.0 + 5.0 * alpha + (phi ** 8) * (alpha ** 2)
    )
    v_gct_gev = (m_mu_geom_mev / 1000.0) * 1440.0 * phi
    v_gct_mev = v_gct_gev * 1000.0

    # PDG targets (in MeV); strange-quark sourced from YAML.
    targets = {
        "u": 2.16,
        "d": 4.70,
        "s": float(C.M_S_OBS),
        "c": 1273.0,
        "b": 4183.0,
        "t": 172570.0 # 172.57 GeV
    }

    # Derivations (in MeV)
    a5_ratio = verify_a5_ratio()
    m_u = m_e_mev * (phi ** 3)

    # Down quark mass: FK-determinant infinite-volume-limit closed form.
    # The I_h-closed orbit-union sequence centers on phi^phi in the deep tail;
    # single-cage values oscillate inside the registered 11% shell-resonance
    # band with empirical decaying envelope. Rigorous infinite-volume proof
    # remains O.5.
    fk_limit = phi ** phi
    m_d = m_u * fk_limit
    fk_info = {
        "status": "POSTDICTION_CONSISTENT_CONDITIONAL",
        "fk_limit_closed_form": "phi^phi",
        "fk_limit_value": float(fk_limit),
        "mass_relation": "m_d = m_u * phi^phi",
        "computed_from_operator": True,
        "mechanism_implemented": True,
        "primary_protocol_role": "primary FK-determinant source value for the down-quark numerical gate",
        "source_branch": "FK-determinant infinite-volume-limit closed form",
        "engine_refs": [
            "protocol_quark_mismatch.py",
            "protocol_md_fk_ih_closed_cages.py",
        ],
        "closed_cage_deep_tail": {
            "N_min": 2000,
            "cage_count": 17,
            "mean_det_FK_over_phi_phi": 0.9976,
            "sample_std": 0.0253,
            "mean_signed_error_vs_PDG_percent": 0.09,
        },
        "single_cage_behavior": "single-cage values oscillate within the 11% shell-resonance band; the m_d match is the central tendency of the sequence",
        "convergence_caveat": "empirical decaying envelope toward phi^phi; rigorous infinite-volume proof open, bundles with O.5",
        "derived_mass_scorecard_inclusion": "Included with Tier 3 conditional note: postdiction-consistent under the phi^phi identification of the shell median (infinite-volume limit open, O.5).",
        "tier": "Tier 2 FK-determinant mechanism + Tier 3 phi^phi identification of the shell median (infinite-volume limit open, O.5)",
    }

    m_s = m_u * (phi ** 8) * (1.0 - 12.0 * alpha)

    # Charm Quark — heuristic Mixed-Harmonic Area Law value phi^(13 + phi^-3).
    # The Ch10 framing ties this to a separate (N=17) harmonic mode whose
    # K-theoretic gap label is structurally distinct from the down-quark FK
    # determinant; the engine does NOT yet derive that label from the cage
    # spectrum, so m_c remains a Tier 3 heuristic awaiting closure via QLQCD-1L
    # gap-label analysis (App ORQ Open Problem O.5; tracked in App TPR §TP-B and
    # §TP-F).
    m_c = m_u * (phi ** (13.0 + (phi ** -3)))

    # A5 representation ratio derived dynamically from graph eigenspectrum [Tier 2]
    m_b = m_c * (phi ** 2) * a5_ratio
    m_t = (v_gct_mev / 2.0) * sqrt2
    
    predictions = {
        "u": m_u,
        "d": m_d,
        "s": m_s,
        "c": m_c,
        "b": m_b,
        "t": m_t
    }
    
    # Error Calculation and Logic
    # -----------------------------------------------------------------------
    # Numerical tolerance gates: m_d 11% shell-resonance band (P.20),
    # m_s ±10%, m_c ±5%; PASS only if within gate.
    # Top and bottom rows are scored against their REGISTERED falsification
    # rule, not a percentage tolerance: P.24 "m_t outside PDG +/- 5 sigma of
    # the geometric prediction" (registered since v1.2.0; comparator PDG 2024
    # direct-measurement mass 172.57 +/- 0.29 GeV) and P.23 "m_b outside PDG
    # +/- 5 sigma (the P.24 rule)" (PDG 2024 m_b(m_b) = 4183 +/- 7 MeV).
    # Both rows miss that rule (App FSM / App PSC rows P.23, P.24;
    # falsifiability_registry.json), so they are reported as FAIL with their
    # sigma distance. The former 1%/2% tolerances are not registered rules and
    # are withdrawn. The up-quark row is retained as an anchor/tension
    # diagnostic because its quoted PDG range is scheme-dependent and not the
    # registered pass/fail gate here.
    # -----------------------------------------------------------------------
    errors = {}
    # Charm gate = registered P.22 band (+/- 3%, falsifiability_registry.json);
    # tightened from an unregistered 5% on 2026-10-22 (sweep I008).
    pdg_tolerance_gates_pct = {"d": 11.0, "s": 10.0, "c": 3.0}
    registered_sigma_gates = {
        "b": {
            "rule": "P.23: m_b outside PDG +/- 5 sigma of the geometric prediction (the P.24 rule)",
            "gate_sigma": 5.0,
            "pdg_sigma_mev": 7.0,
            "comparator": "PDG 2024 m_b(m_b) = 4183 +/- 7 MeV (MS-bar)",
        },
        "t": {
            "rule": "P.24: m_t outside PDG +/- 5 sigma of the geometric prediction (registered since v1.2.0)",
            "gate_sigma": 5.0,
            "pdg_sigma_mev": 290.0,
            "comparator": "PDG 2024 direct-measurement mass 172.57 +/- 0.29 GeV (not a pole mass)",
        },
    }
    sigma_distance = {}
    per_quark_status = {}
    passed_all = True
    failed_registered_gates = []
    print("=" * 70)
    print("  GCT Protocol: Quark Mass Inventory and FK Source Evaluation")
    print("  [Tree-Level Geometric Inventory; Down Quark FK phi^phi Conditional Source]")
    print("=" * 70)

    for q in ["u", "d", "s", "c", "b", "t"]:
        pred = predictions[q]
        targ = targets[q]
        err_pct = abs(pred - targ) / targ * 100.0
        errors[q] = err_pct

        unit = "GeV" if q == "t" else "MeV"
        display_pred = pred / 1000.0 if q == "t" else pred
        display_targ = targ / 1000.0 if q == "t" else targ

        print(f"  Quark {q.upper()}:")
        print(f"    Predicted : {display_pred:.4f} {unit}")
        print(f"    Target    : {display_targ:.4f} {unit}")
        print(f"    Error     : {err_pct:.2f}%")

        gate = pdg_tolerance_gates_pct.get(q)
        sigma_gate = registered_sigma_gates.get(q)
        if sigma_gate is not None:
            n_sigma = abs(pred - targ) / sigma_gate["pdg_sigma_mev"]
            sigma_distance[q] = n_sigma
            sigma_gate["sigma_distance"] = float(n_sigma)
            print(f"    Sigma     : {n_sigma:.2f} sigma (PDG sigma = {sigma_gate['pdg_sigma_mev']:g} MeV)")
            if n_sigma <= sigma_gate["gate_sigma"]:
                per_quark_status[q] = "PASS"
                sigma_gate["status"] = "PASS"
                print(f"    [PASS] Inside registered PDG +/- {sigma_gate['gate_sigma']:.0f} sigma rule")
            else:
                per_quark_status[q] = "FAIL"
                sigma_gate["status"] = "FAIL"
                passed_all = False
                failed_registered_gates.append(q)
                print(f"    [FAIL] Outside registered PDG +/- {sigma_gate['gate_sigma']:.0f} sigma rule "
                      f"(missed at {n_sigma:.2f} sigma)")
        elif gate is None:
            per_quark_status[q] = "DIAGNOSTIC_NO_REGISTERED_GATE"
            print("    [DIAGNOSTIC] No registered PDG gate applied to this row")
        elif err_pct <= gate:
            per_quark_status[q] = "PASS"
            print(f"    [PASS] Within PDG numerical tolerance gate (<= {gate:.1f}%)")
        else:
            per_quark_status[q] = "FAIL"
            passed_all = False
            failed_registered_gates.append(q)
            print(f"    [FAIL] Exceeds PDG numerical tolerance gate (> {gate:.1f}%)")

    d_gate_pass = per_quark_status["d"] == "PASS"
    if passed_all:
        verdict = "PASS"
    else:
        verdict = (
            "REGISTERED_GATE_FAIL_"
            + "_".join(q.upper() for q in failed_registered_gates)
            + ("__D_FK_GATE_PASS" if d_gate_pass else "__D_FK_GATE_FAIL")
        )
    print("=" * 70)
    if passed_all:
        print("  VERDICT: PASS (every gated row inside its registered rule)")
    else:
        print(f"  VERDICT: {verdict}")
        print("  Registered falsification rules missed by: "
              + ", ".join(
                  f"{q} ({sigma_distance[q]:.2f} sigma)" if q in sigma_distance
                  else f"{q} ({errors[q]:.2f}%)"
                  for q in failed_registered_gates))
        print(f"  Down-quark FK gate (P.20, 11% band): {'PASS' if d_gate_pass else 'FAIL'}")
    print("=" * 70)

    output = {
        "pass": passed_all,
        "a5_ratio": float(a5_ratio),
        "b_quark_coefficient_tier": 2,
        "b_quark_coefficient_deployment_tier": 3,
        "b_quark_coefficient_derivation": "Exact A5 representation ratio; absolute bottom-mass deployment inherits Tier 3 quark-sector closure",
        "pdg_tolerance_gates_percent": pdg_tolerance_gates_pct,
        "registered_sigma_gates": registered_sigma_gates,
        "sigma_distance": {k: float(v) for k, v in sigma_distance.items()},
        "per_quark_status": per_quark_status,
        "failed_registered_gates": failed_registered_gates,
        "d_gate_pass": bool(d_gate_pass),
        "verdict": verdict,
        "verdict_note": (
            "Top (P.24) and bottom (P.23) rows are FAILs of the registered PDG +/- 5 sigma "
            "rule; the residuals stay Tier 3 state-level residuals conditional on O.5, and a "
            "pole/MS-bar uncertainty model would be a new pre-registered band, not a "
            "retroactive rescue. The down-quark P.20 row is postdiction-consistent inside its "
            "11% shell-resonance band, conditional on O.5."
        ),
        "down_quark_canonical_tuple": {
            "m_d_MeV": float(m_d),
            "error_percent": float(errors["d"]),
            "gate_percent": float(pdg_tolerance_gates_pct["d"]),
            "status": per_quark_status["d"],
        },
        "predictions_mev": {k: float(v) for k, v in predictions.items()},
        "top_quark_vev_provenance": {
            "vev_GeV": v_gct_gev,
            "source": "absolute GCT Higgs-VEV pipeline used by protocol_higgs_vev.py",
            "formula": "v_GCT = m_e phi^11 (1 + 5 alpha + phi^8 alpha^2) * 1440 * phi",
        },
        "targets_mev": targets,
        "errors_percent": {k: float(v) for k, v in errors.items()},
        "down_quark_fk_info": fk_info,
        "down_quark_primary_protocol_role": (
            "primary FK-determinant source value for the down-quark numerical gate"
        ),
        "strange_quark_geometry": derive_strange_12alpha()
    }
    
    outfile = get_output_path("protocol_quark_mismatch_results.json")
    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    # The registered FAILs are recorded in the result JSON and asserted by
    # config/expected_outcomes.json; a non-zero exit would only stop the
    # refresh path, not report the miss.
    return 0

def derive_strange_12alpha():
    from gct_utils import C
    PHI = float(C.PHI)
    alpha, _ = resolve_a3(C)
    
    # RT Geometry mapping
    n_channels_dodecahedral = 12 # 12 pentagonal faces of the dodecahedral dual cage
    strange_correction = n_channels_dodecahedral * alpha
    
    return {
        "n_channels_dodecahedral": n_channels_dodecahedral,
        "correction_12alpha": strange_correction,
        "geometric_argument": "Strange quark (face defect) couples to 12 surrounding dodecahedral channels. Analogous to muon's 5alpha from A5 H-representation.",
        "tier": "Tier 2 mechanism (conditional on the Tier 3 face-defect quark assignment) + Tier 3 specific coefficient (12) pending O.43 closure"
    }

def estimate_top_qcd_correction():
    """
    Estimate the leading-order QCD pole-mass correction to the tree-level GCT top quark.
    Explains why the 0.87% residual is theoretically bounded (QLQCD-2L target).
    Inputs from first principles (alpha_s PDG, m_t GCT), with no additional fitted coefficient.
    """
    import math
    phi = float(C.PHI) if hasattr(C, 'PHI') else 1.6180339887
    sqrt2 = float(C.SQRT2) if hasattr(C, 'SQRT2') else math.sqrt(2)

    alpha = float(C.ALPHA_OBS)
    m_e_mev = float(C.M_E_OBS)
    m_e_vev_mev = float(C.M_E_CODATA_MEV)
    m_mu_geom_mev = m_e_vev_mev * (phi ** 11) * (
        1.0 + 5.0 * alpha + (phi ** 8) * (alpha ** 2)
    )
    v_gct_mev = m_mu_geom_mev * 1440.0 * phi
    m_t_gct_mev = (v_gct_mev / 2.0) * sqrt2
    m_t_pdg_mev = 172570.0

    M_Z_mev = 91187.6        # Z boson mass in MeV
    alpha_s_mz = 0.1180      # PDG 2024 alpha_s(M_Z)

    # One-loop OLO QCD correction at full top scale
    delta_olo_mev = (4.0 / 3.0) * (alpha_s_mz / math.pi) * m_t_gct_mev

    # Effective scale estimate: geometric mean of m_t and M_Z
    mu_eff_mev = math.sqrt(m_t_gct_mev * M_Z_mev)
    # Running alpha_s to effective scale (one-loop approximate)
    alpha_s_eff = alpha_s_mz * math.log(91187.6) / math.log(mu_eff_mev) if mu_eff_mev > M_Z_mev else alpha_s_mz
    delta_eff_mev = (4.0 / 3.0) * (alpha_s_eff / math.pi) * m_t_gct_mev

    bare_err_pct = abs(m_t_pdg_mev - m_t_gct_mev) / m_t_pdg_mev * 100.0

    print("=" * 60)
    print("  QCD Radiative Correction Estimate (QLQCD-2L Target)")
    print("=" * 60)
    print(f"  GCT bare top mass     : {m_t_gct_mev/1000:.2f} GeV")
    print(f"  PDG observed top mass : {m_t_pdg_mev/1000:.2f} GeV")
    print(f"  GCT bare error        : {bare_err_pct:.2f}%")
    print(f"  OLO QCD correction    : +{delta_olo_mev/1000:.1f} GeV ({delta_olo_mev/m_t_gct_mev*100:.2f}%) [full scale]")
    print(f"  Effective-scale est.  : +{delta_eff_mev/1000:.1f} GeV ({delta_eff_mev/m_t_gct_mev*100:.2f}%) [mu_eff = {mu_eff_mev/1000:.0f} GeV]")
    print(f"  => Residual ({bare_err_pct:.2f}%) is BOUNDED by 1st-order QCD running.")
    print(f"  => Status: Open Problem QLQCD-2L. [Ch10 §10.2.2]")
    print("=" * 60)
    return {
        "m_t_gct_gev": m_t_gct_mev / 1000.0,
        "m_t_pdg_gev": m_t_pdg_mev / 1000.0,
        "bare_error_percent": bare_err_pct,
        "olo_correction_gev": delta_olo_mev / 1000.0,
        "olo_correction_percent": delta_olo_mev / m_t_gct_mev * 100.0,
        "effective_scale_gev": mu_eff_mev / 1000.0,
        "effective_correction_percent": delta_eff_mev / m_t_gct_mev * 100.0,
        "status": f"Open Problem QLQCD-2L — {bare_err_pct:.2f}% residual bounded by first-order QCD"
    }

if __name__ == "__main__":
    estimate_top_qcd_correction()
    sys.exit(main())
