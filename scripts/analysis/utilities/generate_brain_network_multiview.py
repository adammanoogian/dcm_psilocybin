#!/usr/bin/env python3
"""
Generate brain network overlays with multiple viewing angles.

Creates clean visualizations of the 5 left hemisphere regions on brain templates
with different display modes (sagittal, axial, coronal, ortho).
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Add project paths
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'scripts' / 'visualization'))

from scripts.visualization.plot_nilearn_connectivity import AALCoordinateMapper


def plot_brain_nodes_only(output_path, display_mode='x', view_name='Sagittal'):
    """
    Create a brain visualization showing only nodes (no arrows).

    Parameters
    ----------
    output_path : str or Path
        Path to save the SVG file
    display_mode : str
        Nilearn display mode ('x', 'y', 'z', 'ortho', 'lyrz', etc.)
    view_name : str
        Descriptive name for the view
    """
    from nilearn import plotting

    # Define the 5 left hemisphere regions
    region_names = [
        'Frontal_Mid_L',
        'Hippocampus_L',
        'Occipital_Sup_L',
        'Temporal_Mid_L',
        'Thalamus_L'
    ]

    # Define readable labels
    labels = {
        'Frontal_Mid_L': 'dlPFC',
        'Hippocampus_L': 'HC',
        'Occipital_Sup_L': 'SOC',
        'Temporal_Mid_L': 'MTG',
        'Thalamus_L': 'Thal'
    }

    # Define colors
    colors = {
        'Frontal_Mid_L': '#E69F00',     # Orange
        'Hippocampus_L': '#56B4E9',     # Sky Blue
        'Occipital_Sup_L': '#009E73',   # Bluish Green
        'Temporal_Mid_L': '#F0E442',    # Yellow
        'Thalamus_L': '#CC79A7'         # Reddish Purple
    }

    print(f"\n--- {view_name} View ({display_mode}) ---")

    # Get coordinates
    coord_mapper = AALCoordinateMapper()
    node_coords = coord_mapper.get_coordinates(region_names)

    # Prepare colors
    node_color_list = [colors[name] for name in region_names]

    # Determine figure size based on display mode
    if display_mode == 'ortho':
        figsize = (16, 10)
    elif display_mode in ['lyrz', 'lzry']:
        figsize = (18, 8)
    else:
        figsize = (12, 10)

    # Create figure
    fig = plt.figure(figsize=figsize)

    # Plot brain with nodes only (use empty connectivity matrix)
    empty_matrix = np.zeros((len(region_names), len(region_names)))

    display = plotting.plot_connectome(
        empty_matrix,  # Empty connectivity - no edges
        node_coords,
        node_size=250,  # Large nodes
        node_color=node_color_list,
        display_mode=display_mode,
        figure=fig,
        annotate=False,
        colorbar=False,
        edge_threshold=1.0  # No edges drawn
    )

    # Create legend with region labels
    from matplotlib.patches import Patch
    legend_elements = []
    for name in region_names:
        short_name = labels[name]
        full_name = name.replace('_L', ' (Left)')
        legend_elements.append(
            Patch(facecolor=colors[name], edgecolor='black', linewidth=2,
                  label=f'{short_name} = {full_name}')
        )

    # Add legend
    if display_mode in ['ortho', 'lyrz', 'lzry']:
        # For multi-view displays, place legend at bottom
        legend = fig.legend(
            handles=legend_elements,
            loc='lower center',
            ncol=3,
            fontsize=11,
            frameon=True,
            fancybox=True,
            shadow=True,
            title='Brain Regions',
            title_fontsize=13,
            bbox_to_anchor=(0.5, -0.02)
        )
    else:
        # For single views, place legend at bottom
        legend = fig.legend(
            handles=legend_elements,
            loc='lower center',
            ncol=2,
            fontsize=13,
            frameon=True,
            fancybox=True,
            shadow=True,
            title='Brain Regions',
            title_fontsize=15,
            bbox_to_anchor=(0.5, -0.05)
        )

    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_alpha(0.98)
    legend.get_frame().set_linewidth(2)

    # Save figure
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Adjust layout
    plt.tight_layout(rect=[0, 0.10, 1, 1.0])

    # Save as SVG
    plt.savefig(output_path, format='svg', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"  Saved: {output_path.name}")

    # Also save PNG
    png_path = output_path.with_suffix('.png')
    plt.savefig(png_path, format='png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')

    plt.close()


def generate_all_views(output_dir):
    """Generate brain network overlays from multiple viewing angles."""

    print("="*70)
    print("GENERATING BRAIN NETWORK VIEWS")
    print("="*70)

    # Initialize coordinate mapper once
    print("\nInitializing AAL coordinate mapper...")
    coord_mapper = AALCoordinateMapper()

    # Get coordinates and display
    region_names = [
        'Frontal_Mid_L',
        'Hippocampus_L',
        'Occipital_Sup_L',
        'Temporal_Mid_L',
        'Thalamus_L'
    ]
    node_coords = coord_mapper.get_coordinates(region_names)

    print("\nRegion coordinates (MNI):")
    for name, coord in zip(region_names, node_coords):
        print(f"  {name:20s}: [{coord[0]:6.1f}, {coord[1]:6.1f}, {coord[2]:6.1f}]")

    # Define views to generate
    views = [
        {'mode': 'x', 'name': 'Sagittal', 'filename': 'brain_nodes_sagittal.svg'},
        {'mode': 'y', 'name': 'Coronal', 'filename': 'brain_nodes_coronal.svg'},
        {'mode': 'z', 'name': 'Axial', 'filename': 'brain_nodes_axial.svg'},
        {'mode': 'ortho', 'name': 'Orthogonal (3-plane)', 'filename': 'brain_nodes_ortho.svg'},
        {'mode': 'lyrz', 'name': 'Multi-view (4-plane)', 'filename': 'brain_nodes_multiview.svg'},
    ]

    print(f"\nGenerating {len(views)} different views...")

    for view in views:
        output_path = output_dir / view['filename']
        plot_brain_nodes_only(
            output_path,
            display_mode=view['mode'],
            view_name=view['name']
        )


def main():
    """Main function to generate multiple brain views."""
    print("="*70)
    print("BRAIN NETWORK MULTI-VIEW GENERATOR")
    print("="*70)

    # Setup output path
    output_dir = project_root / "figures" / "images"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nOutput directory: {output_dir}")

    # Generate all views
    generate_all_views(output_dir)

    print("\n" + "="*70)
    print("COMPLETE!")
    print("="*70)
    print("\nGenerated views:")
    print("  1. Sagittal (x) - Side view of left hemisphere")
    print("  2. Coronal (y) - Front view")
    print("  3. Axial (z) - Top view")
    print("  4. Orthogonal (ortho) - 3-plane view")
    print("  5. Multi-view (lyrz) - 4-plane comprehensive view")
    print("\nFeatures:")
    print("  ✓ Large colored nodes at MNI coordinates")
    print("  ✓ No connecting arrows (clean view)")
    print("  ✓ Enlarged legend")
    print("  ✓ No header (clean layout)")
    print("  ✓ SVG format (editable)")


if __name__ == '__main__':
    main()
