#!/bin/bash

# Extract figures from Monolith
{
    echo "# GCT Figures and Descriptions"
    echo ""
    echo "*Auto-generated catalog of all figures in the Monolith*"
    echo ""
    echo "---"
    echo ""
    
    # Find all figure lines
    grep -n "^> \*\*Figure" Geometric_Consciousness_Theory.md | while IFS=: read line_num line_text; do
        echo "## ${line_text:2}"  # Remove leading "> "
        echo ""
        echo "**Location:** Line $line_num"
        echo ""
        
        # Get next 5 lines for description
        sed -n "$((line_num+1)),$((line_num+5))p" Geometric_Consciousness_Theory.md | head -3
        
        echo ""
        echo "---"
        echo ""
    done
} > output/GCT_Figures_Catalog.md

echo "✓ Created output/GCT_Figures_Catalog.md"
