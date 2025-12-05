#!/usr/bin/env python3
"""
Generate DCM network architecture figures for publication.

Creates brain visualizations showing all effective connectivity connections
between the 5 left hemisphere regions used in spectral DCM analysis.

Features:
- Fully connected network (all 20 directed connections)
- Perfect mirror symmetry for bidirectional arrows
- Multiple viewing angles (sagittal, axial, coronal, ortho)
- Clean, publication-ready SVG output

Usage:
    python generate_dcm_network_figure.py --view sagittal
    python generate_dcm_network_figure.py --view ortho
    python generate_dcm_network_figure.py --all-views
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Patch
from pathlib import Path
import sys

# Add project paths
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'scripts' / 'visualization'))

from scripts.visualization.plot_nilearn_connectivity import AALCoordinateMapper


# Define brain regions and colors
REGION_NAMES = [
    'Frontal_Mid_L',    # 0: dlPFC
    'Hippocampus_L',    # 1: HC
    'Occipital_Sup_L',  # 2: SOC
    'Temporal_Mid_L',   # 3: MTG
    'Thalamus_L'        # 4: Thal
]

REGION_LABELS = {
    'Frontal_Mid_L': 'dlPFC',
    'Hippocampus_L': 'HC',
    'Occipital_Sup_L': 'SOC',
    'Temporal_Mid_L': 'MTG',
    'Thalamus_L': 'Thal'
}

REGION_COLORS = {
    'Frontal_Mid_L': '#E69F00',     # Orange
    'Hippocampus_L': '#56B4E9',     # Sky Blue
    'Occipital_Sup_L': '#009E73',   # Bluish Green
    'Temporal_Mid_L': '#F0E442',    # Yellow
    'Thalamus_L': '#CC79A7'         # Reddish Purple
}

# Display mode configurations
DISPLAY_MODES = {
    'sagittal': {'mode': 'x', 'name': 'Sagittal', 'figsize': (14, 11)},
    'coronal': {'mode': 'y', 'name': 'Coronal', 'figsize': (14, 11)},
    'axial': {'mode': 'z', 'name': 'Axial', 'figsize': (14, 11)},
    'ortho': {'mode': 'ortho', 'name': 'Orthogonal', 'figsize': (16, 10)},
    'multiview': {'mode': 'lyrz', 'name': 'Multi-view', 'figsize': (18, 8)}
}


def generate_all_connections():
    """
    Generate arrow specifications for fully connected network.

    Returns
    -------
    arrow_specs : list of dict
        List of all bidirectional arrow specifications with perfect mirror symmetry
    """
    n_nodes = len(REGION_NAMES)
    arrow_specs = []

    # For each unique pair, add both directions with mirrored curves
    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            # First direction: i -> j
            arrow_specs.append({
                'from_idx': i,
                'to_idx': j,
                'color': '#333333',
                'width': 3.0,
                'curve': 0.25
            })

            # Second direction: j -> i (automatically mirrors due to matplotlib arc3)
            arrow_specs.append({
                'from_idx': j,
                'to_idx': i,
                'color': '#333333',
                'width': 3.0,
                'curve': 0.25
            })

    return arrow_specs


def plot_dcm_network(output_path, view='sagittal'):
    """
    Create a brain visualization with fully connected DCM network.

    Parameters
    ----------
    output_path : str or Path
        Path to save the SVG file
    view : str
        View type: 'sagittal', 'coronal', 'axial', 'ortho', or 'multiview'
    """
    from nilearn import plotting

    if view not in DISPLAY_MODES:
        raise ValueError(f"Unknown view: {view}. Choose from {list(DISPLAY_MODES.keys())}")

    view_config = DISPLAY_MODES[view]
    display_mode = view_config['mode']
    view_name = view_config['name']
    figsize = view_config['figsize']

    print(f"\n--- Generating {view_name} View ---")

    # Get coordinates
    coord_mapper = AALCoordinateMapper()
    node_coords = coord_mapper.get_coordinates(REGION_NAMES)

    print(f"\nRegion coordinates (MNI):")
    for name, coord in zip(REGION_NAMES, node_coords):
        print(f"  {name:20s}: [{coord[0]:6.1f}, {coord[1]:6.1f}, {coord[2]:6.1f}]")

    # Prepare colors
    node_color_list = [REGION_COLORS[name] for name in REGION_NAMES]

    # Create figure
    fig = plt.figure(figsize=figsize)

    # Plot brain with nodes only (empty connectivity matrix)
    empty_matrix = np.zeros((len(REGION_NAMES), len(REGION_NAMES)))

    display = plotting.plot_connectome(
        empty_matrix,
        node_coords,
        node_size=280,
        node_color=node_color_list,
        display_mode=display_mode,
        figure=fig,
        annotate=False,
        colorbar=False,
        edge_threshold=1.0
    )

    # Get axes for drawing arrows
    axes = display.axes

    # For single-plane views, get the main axis
    if display_mode in ['x', 'y', 'z']:
        brain_ax = axes[display_mode].ax

        # Project 3D coordinates to 2D based on view
        if display_mode == 'x':  # Sagittal (Y-Z plane)
            coords_2d = node_coords[:, [1, 2]]
        elif display_mode == 'y':  # Coronal (X-Z plane)
            coords_2d = node_coords[:, [0, 2]]
        else:  # 'z' - Axial (X-Y plane)
            coords_2d = node_coords[:, [0, 1]]

        # Draw arrows on this view
        draw_arrows(brain_ax, coords_2d)

    # Generate all connections
    arrow_specs = generate_all_connections()

    print(f"\nNetwork configuration:")
    print(f"  • {len(arrow_specs)} directed connections")
    print(f"  • {len(arrow_specs) // 2} bidirectional pairs")
    print(f"  • View: {view_name} ({display_mode})")

    # Create legend
    legend_elements = []
    for name in REGION_NAMES:
        short_name = REGION_LABELS[name]
        full_name = name.replace('_L', ' (Left)')
        legend_elements.append(
            Patch(facecolor=REGION_COLORS[name], edgecolor='black', linewidth=2,
                  label=f'{short_name} = {full_name}')
        )

    # Adjust legend based on view type
    if display_mode in ['ortho', 'lyrz']:
        ncol = 3
        fontsize = 11
        title_fontsize = 13
    else:
        ncol = 2
        fontsize = 13
        title_fontsize = 15

    legend = fig.legend(
        handles=legend_elements,
        loc='lower center',
        ncol=ncol,
        fontsize=fontsize,
        frameon=True,
        fancybox=True,
        shadow=True,
        title='Brain Regions',
        title_fontsize=title_fontsize,
        bbox_to_anchor=(0.5, -0.05)
    )
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_alpha(0.98)
    legend.get_frame().set_linewidth(2)

    # Save figure
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.tight_layout(rect=[0, 0.10, 1, 1.0])

    # Save as SVG
    plt.savefig(output_path, format='svg', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"\nSaved: {output_path}")

    # Also save PNG
    png_path = output_path.with_suffix('.png')
    plt.savefig(png_path, format='png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')

    plt.close()


def draw_arrows(ax, coords_2d):
    """
    Draw all connection arrows on the given axis.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axis to draw arrows on
    coords_2d : np.ndarray
        2D projected coordinates of nodes
    """
    # Node radius in coordinate space (for arrow endpoints)
    node_radius = 2

    # Generate all connections
    arrow_specs = generate_all_connections()

    # Draw each arrow
    for spec in arrow_specs:
        from_idx = spec['from_idx']
        to_idx = spec['to_idx']
        arrow_color = spec['color']
        arrow_width = spec['width']
        curve_amount = spec['curve']

        # Get node center coordinates
        y1_center, z1_center = coords_2d[from_idx]
        y2_center, z2_center = coords_2d[to_idx]

        # Calculate direction vector
        dy, dz = y2_center - y1_center, z2_center - z1_center
        length = np.sqrt(dy**2 + dz**2)

        if length < 1e-6:
            continue

        # Normalize direction vector
        dy_norm, dz_norm = dy / length, dz / length

        # Calculate arrow start and end points at node edges
        y1_start = y1_center + dy_norm * node_radius
        z1_start = z1_center + dz_norm * node_radius
        y2_end = y2_center - dy_norm * node_radius
        z2_end = z2_center - dz_norm * node_radius

        # Create curved arrow with mirror symmetry
        arrow = FancyArrowPatch(
            (y1_start, z1_start), (y2_end, z2_end),
            connectionstyle=f"arc3,rad={curve_amount}",
            arrowstyle='->,head_width=5,head_length=7',
            color=arrow_color,
            alpha=0.9,
            linewidth=arrow_width,
            zorder=5
        )
        ax.add_patch(arrow)


def main():
    """Main function to generate DCM network figures."""
    parser = argparse.ArgumentParser(
        description='Generate DCM network architecture figures'
    )
    parser.add_argument(
        '--view',
        type=str,
        default='sagittal',
        choices=list(DISPLAY_MODES.keys()),
        help='Brain view to generate (default: sagittal)'
    )
    parser.add_argument(
        '--all-views',
        action='store_true',
        help='Generate all available views'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default=None,
        help='Output directory (default: figures/images)'
    )

    args = parser.parse_args()

    print("="*70)
    print("DCM NETWORK FIGURE GENERATOR")
    print("="*70)

    # Setup output directory
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = project_root / "figures" / "images"

    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"\nOutput directory: {output_dir}")

    # Generate requested views
    if args.all_views:
        print("\nGenerating all views...")
        for view_key in DISPLAY_MODES.keys():
            output_path = output_dir / f"dcm_network_{view_key}.svg"
            plot_dcm_network(output_path, view=view_key)
    else:
        output_path = output_dir / f"dcm_network_{args.view}.svg"
        plot_dcm_network(output_path, view=args.view)

    print("\n" + "="*70)
    print("COMPLETE!")
    print("="*70)
    print("\nFeatures:")
    print("  ✓ 20 directed connections (fully connected)")
    print("  ✓ 10 bidirectional pairs with mirror symmetry")
    print("  ✓ Dark black arrows (90% opacity)")
    print("  ✓ Arrows end near node centers")
    print("  ✓ Large colored nodes with legend")
    print("  ✓ Editable SVG format")


if __name__ == '__main__':
    main()
