#!/usr/bin/env python3
"""
GCT Figure Manager: Build manifest, validate existence, generate placeholders.
Handles all 23 figures across Volumes 1-3.
"""

import os
import json
from pathlib import Path

# ============================================================================
# FIGURE MANIFEST (All 23 figures referenced in the manuscript)
# ============================================================================
FIGURES_MANIFEST = [
    # Chapter-relative scheme: V<vol>.<chapter>.<index>
    {"id": "V1.1.1", "volume": 1, "description": "The Epistemic Staircase"},
    {"id": "V1.4.1", "volume": 1, "description": "Lattice vs. Continuum"},
    {"id": "V1.5.1", "volume": 1, "description": "The Zero-Point Schism"},
    {"id": "V1.5.2", "volume": 1, "description": "The Wheeler-DeWitt Null Constraint"},
    {"id": "V1.7.1", "volume": 1, "description": "The Adelic Solenoid Branching Structure"},
    {"id": "V1.8.1", "volume": 1, "description": "Simultaneous Projection"},
    {"id": "V1.12.1", "volume": 1, "description": "Emergence of Time from Entanglement (Page-Wootters)"},
    {"id": "V2.1.1", "volume": 2, "description": "The E8 Slice"},
    {"id": "V2.1.2", "volume": 2, "description": "The 6D to 3D Projection Geometry"},
    {"id": "V2.8.1", "volume": 2, "description": "Gravity as Phason Elasticity Gradient"},
    {"id": "V2.12.1", "volume": 2, "description": "MOND Acceleration Curves vs. Phason Elasticity"},
    {"id": "V2.14.1", "volume": 2, "description": "The Phantom Crossing"},
    {"id": "V3.1.1", "volume": 3, "description": "The Gauge Lift"},
    {"id": "V3.1.2", "volume": 3, "description": "The U(1) Phase Winding in the Superfluid"},
    {"id": "V3.2.1", "volume": 3, "description": "The SU(2) Double Cover of the Spatial Frame"},
    {"id": "V3.4.1", "volume": 3, "description": "The Sirlin Relation Bracketing"},
    {"id": "V3.5.1", "volume": 3, "description": "The Higgs Potential"},
    {"id": "V3.8.1", "volume": 3, "description": "The Fractal Resonance Spectrum of the Lepton Cage"},
    {"id": "V3.10.1", "volume": 3, "description": "The Baryonic Triad Knot"},
    {"id": "V3.11.1", "volume": 3, "description": "The 3.55 keV X-ray Anomaly"},
    {"id": "V3.13.1", "volume": 3, "description": "The Microtubule Quantum Well and Zeno Gating"},
    {"id": "V3.21.1", "volume": 3, "description": "Hellings-Downs Correlation + Icosahedral Correction"},
    {"id": "V3.22.1", "volume": 3, "description": "The Falsification Roadmap"},
]

def get_figure_path(figure_id):
    """
    Determine the path to a figure file.
    Check in order: svg, png, pdf
    """
    figures_dir = Path(__file__).parent.parent / "content" / "Figures"

    # Extract volume number from figure_id (e.g., "V3.8.1" -> "3")
    volume_num = figure_id.split('.')[0].replace('V', '')
    volume = f"Volume_{volume_num}"
    figure_name = f"Figure {figure_id}"

    vol_dir = figures_dir / volume
    if not vol_dir.exists():
        return None

    for ext in ['svg', 'png', 'pdf']:
        candidate = vol_dir / f"{figure_name}.{ext}"
        if candidate.exists():
            return str(candidate.relative_to(Path(__file__).parent.parent))

    return None

def generate_figure_markdown(figure_id, description):
    """
    Generate markdown for a single figure with fallback to placeholder.
    """
    path = get_figure_path(figure_id)

    if path:
        # Figure exists - include it
        return f"""
### Figure {figure_id}
{description}

![Figure {figure_id}]({path})

"""
    else:
        # Figure in development - show placeholder
        return f"""
### Figure {figure_id}
{description}

> [!NOTE]
> **Figure in development.** This figure will be generated/inserted in a future revision.
> Expected file format: SVG, PNG, or PDF in `content/Figures/Volume_{figure_id.split('.')[0]}/`

"""

def build_figures_catalog():
    """
    Generate a comprehensive catalog of all 23 figures.
    """
    catalog = []

    for fig in FIGURES_MANIFEST:
        path = get_figure_path(fig["id"])
        status = "✓ Available" if path else "⏳ In Development"
        catalog.append({
            "id": fig["id"],
            "volume": fig["volume"],
            "description": fig["description"],
            "path": path,
            "status": status
        })

    return catalog

def save_figures_manifest(output_path="output/figures_manifest.json"):
    """
    Save the figures manifest to JSON for reference.
    """
    catalog = build_figures_catalog()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(catalog, f, indent=2)

    # Print summary
    available = sum(1 for fig in catalog if "Available" in fig["status"])
    print(f"\n{'='*70}")
    print(f"GCT FIGURE MANIFEST")
    print(f"{'='*70}")
    print(f"Total Figures: {len(catalog)}")
    print(f"Available: {available}")
    print(f"In Development: {len(catalog) - available}")
    print(f"\nManifest saved to: {output_path}")
    print(f"{'='*70}\n")

    for fig in catalog:
        status_symbol = "[OK]" if "Available" in fig["status"] else "[--]"
        print(f"{status_symbol} {fig['id']:8s} | Vol {fig['volume']} | {fig['description']}")

if __name__ == "__main__":
    save_figures_manifest()
