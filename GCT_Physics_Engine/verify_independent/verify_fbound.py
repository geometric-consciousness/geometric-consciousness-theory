"""
verify_fbound.py — Bound-water fraction f_bound via conservative hydration geometry.

Vol 1 Ch17 §17.1.2c, App NSP §NSP.4:
    N_water = π × r_lumen² × ℓ / ν_H2O / 13
        with r_lumen = 7.5 nm, ℓ = 8 nm (one ring of 13 dimers), ν_H2O = 0.0299 nm³
        ≈ 4.7 × 10⁴ water molecules per ring, ≈ 3.6 × 10³ per dimer
    N_bound = n_rp × n_contact (no ×12 face factor)
        where n_rp is the per-dimer Trp radical-pair count and
              n_contact is the first-shell water molecules per Trp-RP
    f_bound = N_bound / N_water

This verifier exercises the disclosed central/sensitivity branch discipline
(App NSP §NSP.4, Ch17 §17.1.2c) after the O.21/O.33 weakening:

    n_rp     ∈ {0, 1, 2}
        0 = operative central value while O.21 assembled-MT lumen-axis
            closure remains open
        1 = O.21 sensitivity branch (Trp21 local-inward wall-patch screen
            only; conditional on positive assembled-MT lumen-axis closure)
        2 = disfavored structural upper bound

    n_contact ∈ {4, 6, 8, 12}
        4,6,8 = conditional sensitivity cage-occupancy band
        6     = central value
        12    = perfect-cage structural stress test (not operative)

The arithmetic gate checks the disclosed n_rp = 1 sensitivity branch against
the manuscript's stated [1.1, 2.2]e-3 band.  The n_rp = 0 row is a stipulated
O.21-pending scenario, not empirical evidence and not a physical PASS gate.

The full 6-point sensitivity sweep is reported alongside, giving the
full disclosed range:
    f_bound (operative central, n_rp=0)              = 0
    f_bound (sensitivity branch, n_rp=1)             ∈ [1.1, 2.2] × 10⁻³
    f_bound (disfavored n_rp=2 sensitivity band)     ∈ [2.2, 4.4] × 10⁻³
    f_bound (structural stress test, n_rp=2, n_c=12) ≈ 6.6 × 10⁻³
(The earlier version divided by the per-ring water count and multiplied by a
×12 face factor; both are removed, giving the ×13/12 shift of every value.)

This verifier is an arithmetic self-consistency check on the manuscript's
own geometry numbers. It does NOT verify the underlying geometry inputs
(r_lumen = 7.5 nm, ℓ = 8 nm, n_contact range, 13 dimers per ring) — those come
from cryo-EM of microtubules + the N=144 cage assumption + conservative
Trp-radical-pair cage-occupancy counts. Those biological inputs
are Tier 3. Nuclear Overhauser cross-relaxation is not used as a lock
mechanism; the historical 100 MHz material-scan scenario is not an
operating rate.
"""

import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from report import make_result, write_result, print_summary


def evaluate_status(
    sensitivity_lower: float,
    sensitivity_upper: float,
    disclosed_lower: float,
    disclosed_upper: float,
    *,
    relative_tolerance: float = 0.05,
) -> str:
    """Check manuscript-scenario arithmetic without treating n_rp=0 as data."""
    if min(disclosed_lower, disclosed_upper) <= 0:
        raise ValueError("disclosed sensitivity bounds must be positive")
    lower_ok = abs(sensitivity_lower - disclosed_lower) / disclosed_lower < relative_tolerance
    upper_ok = abs(sensitivity_upper - disclosed_upper) / disclosed_upper < relative_tolerance
    return "INTERNAL_ARITHMETIC_PASS" if lower_ok and upper_ok else "FAIL"


def main():
    # Manuscript geometry inputs (Ch17 §17.1.2c)
    r_lumen_nm = 7.5       # microtubule inner radius
    ell_dimer_nm = 8.0     # length per tubulin dimer
    nu_H2O_nm3 = 0.0299    # molecular volume of water (29.9 Å³/molecule)
    n_protofilaments = 13  # dimers per 8 nm ring

    # Compute N_water per dimer (ring lumen volume / molecular volume / 13)
    N_water_ring = math.pi * r_lumen_nm ** 2 * ell_dimer_nm / nu_H2O_nm3
    N_water = N_water_ring / n_protofilaments
    N_water_int = round(N_water)   # integer precision (3637) used for sweep table

    # Disclosed joint sensitivity range over (n_rp, n_contact)
    # n_rp ∈ {0, 1, 2}; n_contact ∈ {4, 6, 8, 12}
    n_rp_values = (0, 1, 2)
    n_contact_values = (4, 6, 8, 12)

    # Canonical / operative central point used by the manuscript main text
    n_rp_canonical = 0
    n_contact_canonical = 6

    # Stated targets and disclosed bounds
    f_bound_stated_O21 = 0.0          # operative central target (n_rp=0 while O.21 is open)
    f_bound_lower_disclosed = 1.1e-3  # sensitivity-branch lower edge
    f_bound_upper_disclosed = 2.2e-3  # sensitivity-branch upper edge
    f_bound_structural_upper = 6.6e-3 # structural stress test (n_rp=2, n_contact=12)

    # Build the full sensitivity sweep
    sweep = []
    canonical_record = None
    for n_rp in n_rp_values:
        for n_contact in n_contact_values:
            N_bound = n_rp * n_contact
            f_bound = N_bound / N_water
            entry = {
                "n_rp": n_rp,
                "n_contact": n_contact,
                "n_bound": N_bound,
                "f_bound": f_bound,
                "f_bound_int_form": f"{N_bound} / {N_water_int}",
            }
            sweep.append(entry)
            if n_rp == n_rp_canonical and n_contact == n_contact_canonical:
                canonical_record = entry

    assert canonical_record is not None, \
        "Canonical (n_rp=0, n_contact=6) point missing from sweep grid."

    # Record the stipulated O.21-pending central scenario.  It is not a gate.
    f_bound_canonical = canonical_record["f_bound"]
    err_canonical = 0.0 if f_bound_canonical == 0.0 else float("inf")

    canonical_point = {
        "n_rp": n_rp_canonical,
        "n_contact": n_contact_canonical,
        "n_bound": canonical_record["n_bound"],
        "f_bound": f_bound_canonical,
        "f_bound_predicted": f_bound_stated_O21,
        "delta_pct": err_canonical,
        "pass": None,
    }

    # Cross-check that sensitivity sweep extremes match the disclosed bounds
    f_bound_sensitivity_lower = next(
        e["f_bound"] for e in sweep if e["n_rp"] == 1 and e["n_contact"] == 4
    )
    f_bound_sensitivity_central = next(
        e["f_bound"] for e in sweep if e["n_rp"] == 1 and e["n_contact"] == 6
    )
    f_bound_sensitivity_upper = next(
        e["f_bound"] for e in sweep if e["n_rp"] == 1 and e["n_contact"] == 8
    )
    f_bound_structural = next(
        e["f_bound"] for e in sweep if e["n_rp"] == 2 and e["n_contact"] == 12
    )
    status = evaluate_status(
        f_bound_sensitivity_lower,
        f_bound_sensitivity_upper,
        f_bound_lower_disclosed,
        f_bound_upper_disclosed,
    )
    pass_status = status == "INTERNAL_ARITHMETIC_PASS"

    canonical_point["pass"] = pass_status

    res = make_result(
        name="f_bound_conservative_geometry",
        app_psc_label="Bound-water fraction f_bound (O.21/O.33 conservative geometry)",
        formula=(
            "f_bound = N_bound / N_water = (n_rp × n_contact) / "
            "(π r_lumen² ℓ / ν_H2O / 13); operative central n_rp=0; "
            "sensitivity sweep over n_rp ∈ {1,2}, n_contact ∈ {4,6,8,12}"
        ),
        predicted=f_bound_canonical,
        observed=f_bound_stated_O21,
        unit="(dimensionless)",
        app_psc_predicted=f_bound_stated_O21,
        app_psc_precision_str=(
            f"N_water = {N_water:.4g} (geometry, integer-form {N_water_int}); "
            f"operative central (n_rp=0): f_bound = {f_bound_canonical:.4g}; "
            f"sensitivity central (n_rp=1, n_contact=6): {f_bound_sensitivity_central:.4g}; "
            f"sensitivity range [{f_bound_lower_disclosed:.3g}, {f_bound_upper_disclosed:.3g}], "
            f"structural stress test {f_bound_structural:.4g}"
        ),
        app_psc_precision_ppm=None,
        tier="Tier 3 biological substrate value (O.21/O.33 conservative geometry; Nuclear Overhauser transfer is not the lock mechanism)",
        status=status,
        reference_class="MANUSCRIPT_STATED",
        tolerance_ppm=None,
        extra={
            "geometry": {
                "r_lumen_nm": r_lumen_nm,
                "ell_dimer_nm": ell_dimer_nm,
                "water_vol_nm3": nu_H2O_nm3,
                "n_protofilaments_per_ring": n_protofilaments,
                "N_water_per_ring": N_water_ring,
                "N_water": N_water_int,
                "N_water_exact": N_water,
            },
            "canonical_point": canonical_point,
            "sensitivity_sweep": sweep,
            "operative_central_f_bound": 0.0,
            "sensitivity_branch_f_bound": [
                f_bound_lower_disclosed,
                f_bound_upper_disclosed,
            ],
            "sensitivity_branch_central": f_bound_sensitivity_central,
            "structural_upper_bound": f_bound_structural_upper,
            "n_rp_values_swept": list(n_rp_values),
            "n_contact_values_swept": list(n_contact_values),
            "derivation_note": (
                "Pure arithmetic check on the manuscript's own §17.1.2c "
                "derivation chain. The geometry inputs (microtubule lumen "
                "radius, tubulin dimer length, water molecular volume, "
                "Trp-radical-pair cage-occupancy count range, 13 dimers per "
                "ring) are accepted as inputs; the "
                "arithmetic is verified across the disclosed central branch "
                "and joint sensitivity range over (n_rp, n_contact). The "
                "central O.21-pending branch (n_rp = 0) is a stipulated scenario, "
                "while the arithmetic gate checks the conditional n_rp = 1 band. If the "
                "geometry inputs change, this verifier should be re-run."
            ),
        },
    )

    # Augment top-level result with the new payload fields requested by callers
    res["canonical_point"] = canonical_point
    res["sensitivity_sweep"] = sweep
    res["operative_central_f_bound"] = 0.0
    res["sensitivity_branch_f_bound"] = [f_bound_lower_disclosed, f_bound_upper_disclosed]
    res["sensitivity_branch_central"] = f_bound_sensitivity_central
    res["disclosed_range_f_bound"] = [f_bound_lower_disclosed, f_bound_upper_disclosed]
    res["structural_upper_bound"] = f_bound_structural_upper
    res["geometry"] = res["extra"]["geometry"]
    res["pass"] = pass_status
    res["verdict"] = status

    print_summary(res)
    # Sensitivity sweep print-out
    print("  Sensitivity sweep (n_rp × n_contact):")
    print(f"    {'n_rp':>4}  {'n_contact':>9}  {'N_bound':>7}  {'f_bound':>11}")
    for e in sweep:
        marker = "  <-- canonical" if (
            e["n_rp"] == n_rp_canonical and e["n_contact"] == n_contact_canonical
        ) else ""
        print(
            f"    {e['n_rp']:>4}  {e['n_contact']:>9}  "
            f"{e['n_bound']:>7}  {e['f_bound']:>11.4e}{marker}"
        )
    print("=" * 72)

    write_result(res)
    return res


if __name__ == "__main__":
    main()
