#!/usr/bin/env python3
"""PTA observable-map derivation boundary.

The exact I_h l=6 invariant is verified in protocol_pta_l6_template.py. This
calculation records the scientific boundary: a one-variable P6 correction to
the Hellings--Downs curve is rotation invariant and cannot encode an oriented
icosahedral frame. A nonzero PTA response and its amplitude remain open.
"""

from __future__ import annotations

import json
from pathlib import Path

from gct_utils import get_output_path
from protocol_pta_l6_template import character_decomposition


def main() -> dict[str, object]:
    rows = character_decomposition()
    exact_l6 = (
        all(rows[ell]["trivial_scalar_multiplicity"] == 0 for ell in range(1, 6))
        and rows[6]["trivial_scalar_multiplicity"] == 1
    )
    result = {
        "protocol": "PTA_OBSERVABLE_MAP_OBSTRUCTION",
        "status": "PASS_EXACT_L6_INVARIANT__PHYSICAL_PTA_RESPONSE_OPEN",
        "pass": bool(exact_l6),
        "exact_l6_invariant": bool(exact_l6),
        "separation_only_model": "Gamma_HD(zeta) + epsilon P6(cos zeta)",
        "separation_only_model_is_SO3_invariant": True,
        "fifteen_angle_mask_valid": False,
        "physical_response_derived": False,
        "amplitude_derived": False,
        "orientation_derived": False,
        "frequency_law_derived": False,
        "p3b_implies_pta_amplitude": False,
        "undefined_pta_conversions_without_transfer": ["1.67e-4", "2.90e-8"],
        "conditional_sky_power_model": {
            "power": "P(Omega;R) = 1 + eta A6(R^-1 Omega)",
            "covariance": "Gamma_ab = Gamma_HD_ab + eta sum_m a_6m(R) Gamma_ab,6m",
            "orientation_space": "SO(3)/I",
            "eta": "undetermined",
            "scope": "phenomenological sky-power model, not a derived GCT propagation response",
        },
        "required_next_map": "action -> directional kernel -> Green function -> polarization/source/pulsar transfer -> generalized ORFs",
        "null_falsifies_exact_angular_theorem": False,
    }
    out = Path(get_output_path("protocol_pta_anisotropy_results.json"))
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"pass": result["pass"], "status": result["status"], "output": str(out)}, indent=2))
    return result


def run_pta_anisotropy_protocol() -> dict[str, object]:
    """Backward-compatible entry point used by older callers."""
    return main()


if __name__ == "__main__":
    main()
