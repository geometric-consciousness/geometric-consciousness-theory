import re

# Read the Monolith
with open('Geometric_Consciousness_Theory.md', 'r', encoding='utf-8') as f:
    monolith_lines = f.readlines()

# Figure locations from our previous search
figures = [
    (482, "V1.1.1", "The Epistemic Staircase - From Axiom to Universe"),
    (915, "V1.1.3", "Lattice vs. Continuum"),
    (1026, "V1.1.4", "The Zero-Point Schism"),
    (1120, "V1.1.5", "The Wheeler-DeWitt Null Constraint"),
    (1466, "V1.7.1", "The Adelic Solenoid Branching Structure"),
    (1523, "V1.8.1", "Simultaneous Projection"),
    (2567, "V1.12.1", "The Emergence of Time from Entanglement (Page-Wootters)"),
    (3850, "V2.2.1", "The E8 Slice"),
    (3910, "V2.1.1", "The 6D to 3D Projection Geometry"),
    (4672, "V2.8.1", "Gravity as Phason Elasticity Gradient"),
    (5033, "V2.12.1", "MOND Acceleration Curves vs. Phason Elasticity"),
    (5324, "V2.14.1", "The Phantom Crossing"),
    (5886, "V3.3.1", "The Gauge Lift"),
    (5896, "V3.1.1", "The U(1) Phase Winding in the Superfluid"),
    (6021, "V3.2.1", "The SU(2) Double Cover of the Spatial Frame"),
    (6279, "V3.3.4", "The Sirlin Relation Bracketing"),
    (6454, "V3.3.5", "The Higgs Potential"),
    (7144, "V3.8.1", "The Fractal Resonance Spectrum of the Lepton Cage"),
    (7541, "V3.10.1", "The Baryonic Triad Knot"),
    (7735, "V3.11.1", "The 3.55 keV X-ray Anomaly: Multi-Observatory Detection Context"),
    (8361, "V3.13.1", "The Microtubule Quantum Well and Zeno Gating"),
    (9241, "V3.21.1", "Hellings-Downs Correlation + Icosahedral Correction"),
    (9551, "V3.22.1", "The Falsification Roadmap"),
]

# For each figure, extract context and create description
detailed_descriptions = {}

for line_num, fig_id, fig_title in figures:
    # Get context: 30 lines before and 10 after the figure
    start = max(0, line_num - 31)  # -1 for 0-indexing, -30 for context
    end = min(len(monolith_lines), line_num + 15)
    
    context = ''.join(monolith_lines[start:end])
    detailed_descriptions[fig_id] = {
        'title': fig_title,
        'line': line_num,
        'context': context
    }

# Print first few for manual review
for i, (fig_id, data) in enumerate(list(detailed_descriptions.items())[:3]):
    print(f"\n{'='*80}")
    print(f"FIGURE {fig_id}: {data['title']}")
    print(f"{'='*80}")
    print(data['context'])
