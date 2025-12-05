#!/usr/bin/env python3
"""
Generate a network diagram showing all connections between DCM regions.

Creates an SVG with 5 nodes (brain regions) and curved arrows showing
all possible connections between them.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Circle
from matplotlib.path import Path
import matplotlib.patheffects as PathEffects
from pathlib import Path as FilePath
import sys

# Add project root to path
project_root = FilePath(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


def create_network_diagram(output_path):
    """
    Create a network diagram with 5 brain regions and curved connections.

    Parameters
    ----------
    output_path : str or Path
        Path to save the SVG file
    """
    # Define regions with abbreviated names
    regions = [
        {'name': 'dlPFC', 'full_name': 'Left Middle Frontal', 'color': '#E69F00'},
        {'name': 'HC', 'full_name': 'Left Hippocampus', 'color': '#56B4E9'},
        {'name': 'SOC', 'full_name': 'Left Superior Occipital', 'color': '#009E73'},
        {'name': 'MTG', 'full_name': 'Left Middle Temporal', 'color': '#F0E442'},
        {'name': 'Thal', 'full_name': 'Left Thalamus', 'color': '#CC79A7'}
    ]

    n_regions = len(regions)

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')

    # Add title
    title = ax.text(0, 1.35, 'DCM Network Architecture',
                    ha='center', va='top', fontsize=20, fontweight='bold')

    # Arrange nodes in a circle
    radius = 1.0
    node_radius = 0.22
    angles = np.linspace(0, 2*np.pi, n_regions, endpoint=False) + np.pi/2  # Start at top

    # Calculate node positions
    positions = []
    for angle in angles:
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        positions.append((x, y))

    # Draw curved arrows between all pairs of nodes
    arrow_color = '#666666'
    arrow_alpha = 0.15
    arrow_width = 1.5

    for i in range(n_regions):
        for j in range(n_regions):
            if i != j:  # Skip self-connections
                x1, y1 = positions[i]
                x2, y2 = positions[j]

                # Calculate control point for curved arrow
                # Place control point perpendicular to the line connecting the nodes
                mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                dx, dy = x2 - x1, y2 - y1
                # Perpendicular vector
                perp_x, perp_y = -dy, dx
                # Normalize
                length = np.sqrt(perp_x**2 + perp_y**2)
                perp_x, perp_y = perp_x / length, perp_y / length
                # Control point offset (creates the curve)
                curve_amount = 0.15
                ctrl_x = mid_x + perp_x * curve_amount
                ctrl_y = mid_y + perp_y * curve_amount

                # Adjust start and end points to be at edge of circles
                angle_to_end = np.arctan2(y2 - y1, x2 - x1)
                start_x = x1 + node_radius * np.cos(angle_to_end)
                start_y = y1 + node_radius * np.sin(angle_to_end)

                angle_to_start = np.arctan2(y1 - y2, x1 - x2)
                end_x = x2 + node_radius * np.cos(angle_to_start)
                end_y = y2 + node_radius * np.sin(angle_to_start)

                # Create curved arrow using quadratic Bezier curve
                arrow = FancyArrowPatch(
                    (start_x, start_y), (end_x, end_y),
                    connectionstyle=f"arc3,rad=.2",
                    arrowstyle='->,head_width=0.15,head_length=0.15',
                    color=arrow_color,
                    alpha=arrow_alpha,
                    linewidth=arrow_width,
                    zorder=1
                )
                ax.add_patch(arrow)

    # Draw nodes on top of arrows
    for i, (region, (x, y)) in enumerate(zip(regions, positions)):
        # Draw circle with white background
        circle_bg = Circle((x, y), node_radius,
                          facecolor='white',
                          edgecolor=region['color'],
                          linewidth=4,
                          zorder=10)
        ax.add_patch(circle_bg)

        # Draw colored circle border (thicker)
        circle = Circle((x, y), node_radius,
                       facecolor='white',
                       edgecolor=region['color'],
                       linewidth=5,
                       zorder=11)
        ax.add_patch(circle)

        # Add label inside circle
        text = ax.text(x, y, region['name'],
                      ha='center', va='center',
                      fontsize=14, fontweight='bold',
                      color='#333333',
                      zorder=12)

        # Add subtle shadow to text for readability
        text.set_path_effects([
            PathEffects.withStroke(linewidth=3, foreground='white', alpha=0.8)
        ])

    # Add legend/key below
    legend_y = -1.25
    legend_text = "Each arrow represents a potential effective connection in the DCM model"
    ax.text(0, legend_y, legend_text,
            ha='center', va='top', fontsize=11,
            style='italic', color='#666666')

    # Add region name legend
    legend_items = []
    for region in regions:
        legend_items.append(f"{region['name']} = {region['full_name']}")

    legend_str = " | ".join(legend_items)
    ax.text(0, legend_y - 0.15, legend_str,
            ha='center', va='top', fontsize=9, color='#888888')

    # Save figure
    output_path = FilePath(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.savefig(output_path, format='svg', bbox_inches='tight',
                facecolor='white', edgecolor='none', dpi=300)
    print(f"\nNetwork diagram saved to: {output_path}")

    # Also save PNG version
    png_path = output_path.with_suffix('.png')
    plt.savefig(png_path, format='png', bbox_inches='tight',
                facecolor='white', edgecolor='none', dpi=300)
    print(f"PNG version saved to: {png_path}")

    plt.close()


def main():
    """Main function to generate the network diagram."""
    print("="*70)
    print("GENERATING DCM NETWORK DIAGRAM")
    print("="*70)

    # Setup output path
    output_dir = project_root / "figures" / "images"
    output_path = output_dir / "dcm_network_diagram.svg"

    print(f"\nOutput directory: {output_dir}")
    print(f"Output file: {output_path.name}")

    # Generate diagram
    print("\nGenerating network diagram with 5 regions and connections...")
    create_network_diagram(output_path)

    print("\n" + "="*70)
    print("COMPLETE!")
    print("="*70)
    print("\nThe diagram shows:")
    print("  • 5 brain regions arranged in a circle")
    print("  • Curved arrows showing all possible connections")
    print("  • Color-coded nodes matching time series figure")
    print("  • Editable SVG format")
    print("\nRegions:")
    print("  • dlPFC = Left Middle Frontal (dorsolateral prefrontal cortex)")
    print("  • HC = Left Hippocampus")
    print("  • SOC = Left Superior Occipital")
    print("  • MTG = Left Middle Temporal")
    print("  • Thal = Left Thalamus")


if __name__ == '__main__':
    main()
