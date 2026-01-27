#!/usr/bin/env python3
"""
Pipeline Step 02: Generate nilearn supplementary figures (ROI-focused)

Generates comprehensive nilearn connectivity figures for all conditions.
Uses consistent color scales (RdBu_r) matching matrix visualizations.
Generates both session difference and behavioral association plots.

Usage:
    # Paper mode (default): Generate only ROI-focused supplementary figures (8 files)
    python scripts/analysis/02_generate_nilearn_supplementary.py
    python scripts/analysis/02_generate_nilearn_supplementary.py --paper

    # Full mode: Generate all exploratory figures (~30+ files)
    python scripts/analysis/02_generate_nilearn_supplementary.py --full
"""

import sys
import argparse
from pathlib import Path

# Add project paths
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'scripts' / 'visualization'))

from scripts.visualization.plot_nilearn_connectivity import (
    AALCoordinateMapper, NilearnConnectivityVisualizer
)


def generate_session_change_plots(visualizer, coord_mapper, data_dir, output_dir, paper_mode=True):
    """
    Generate session change (difference) plots for all tasks.

    Parameters
    ----------
    visualizer : NilearnConnectivityVisualizer
        The connectivity visualizer instance
    coord_mapper : AALCoordinateMapper
        The coordinate mapper instance
    data_dir : Path
        Directory containing .mat data files
    output_dir : Path
        Directory to save output figures
    paper_mode : bool
        If True (default), generate only ROI-focused supplementary figures.
        If False, generate all figures including full network plots.
    """
    print("\n" + "="*70)
    print("GENERATING SESSION CHANGE (DIFFERENCE) PLOTS")
    if paper_mode:
        print("(Paper mode: ROI-focused plots only)")
    print("="*70)

    tasks = {
        'rest': {
            'file': 'PEB_change_-ses-01-ses-02_-task-rest_cov-_noFD.mat',
            'title': 'Resting State',
            'subtitle': 'Session Change (Post-Psilocybin - Pre-Psilocybin)'
        },
        'music': {
            'file': 'PEB_change_-ses-01-ses-02_-task-music_cov-_noFD.mat',
            'title': 'Music Listening',
            'subtitle': 'Session Change (Post-Psilocybin - Pre-Psilocybin)'
        },
        'movie': {
            'file': 'PEB_change_-ses-01-ses-02_-task-movie_cov-_noFD.mat',
            'title': 'Movie Viewing',
            'subtitle': 'Session Change (Post-Psilocybin - Pre-Psilocybin)'
        },
        'meditation': {
            'file': 'PEB_change_-ses-01-ses-02_-task-meditation_cov-_noFD.mat',
            'title': 'Meditation',
            'subtitle': 'Session Change (Post-Psilocybin - Pre-Psilocybin)'
        }
    }

    for task_name, task_info in tasks.items():
        mat_path = data_dir / task_info['file']
        if not mat_path.exists():
            print(f"  Skipping {task_name}: file not found")
            continue

        print(f"\n--- {task_info['title']} ---")

        # Load connectivity
        try:
            conn_matrix, roi_names = visualizer.load_connectivity(str(mat_path), pp_threshold=0.99)
        except Exception as e:
            print(f"  Error loading {task_name}: {e}")
            continue

        node_coords = coord_mapper.get_coordinates(roi_names)

        # Generate full network plot - Session change uses coolwarm (diverging, centered at 0)
        # Skip in paper mode (only generate ROI-focused plots for supplementary)
        if not paper_mode:
            output_file = output_dir / f"session_change_{task_name}_full_network.png"
            visualizer.plot_connectome(
                conn_matrix,
                node_coords,
                str(output_file),
                title=f"{task_info['title']} - Session Change",
                edge_threshold='0%',
                node_size=80,  # Larger nodes
                edge_cmap='coolwarm',  # Diverging colormap for difference
                display_mode='lyrz',
                colorbar=True,
                roi_names=roi_names,
                colorbar_label="Δ Connection Strength (Hz)",
                subtitle=f"{task_info['subtitle']}\nPp>0.99 | {len(roi_names)} ROIs"
            )

        # Generate dlPFC focused plot (included in paper mode for supplementary)
        dlpfc_filtered = visualizer.filter_connections(
            conn_matrix, roi_names,
            source_regions=['Frontal_Mid'],
            connection_type='outgoing'
        )

        output_file = output_dir / f"session_change_{task_name}_dlpfc_outgoing.png"
        visualizer.plot_connectome(
            dlpfc_filtered,
            node_coords,
            str(output_file),
            title=f"{task_info['title']} - dlPFC Outgoing",
            edge_threshold='0%',
            node_size=100,  # Larger nodes
            edge_cmap='coolwarm',  # Diverging colormap
            display_mode='lyrz',
            colorbar=True,
            roi_names=roi_names,
            colorbar_label="Δ Connection Strength (Hz)",
            subtitle=f"dlPFC → Other Regions | {task_info['subtitle']}"
        )

        # Generate hippocampus focused plot
        hipp_filtered = visualizer.filter_connections(
            conn_matrix, roi_names,
            source_regions=['Hippocampus'],
            connection_type='bidirectional'
        )

        output_file = output_dir / f"session_change_{task_name}_hippocampus.png"
        visualizer.plot_connectome(
            hipp_filtered,
            node_coords,
            str(output_file),
            title=f"{task_info['title']} - Hippocampus Network",
            edge_threshold='0%',
            node_size=100,  # Larger nodes
            edge_cmap='coolwarm',  # Diverging colormap
            display_mode='lyrz',
            colorbar=True,
            roi_names=roi_names,
            colorbar_label="Δ Connection Strength (Hz)",
            subtitle=f"Hippocampus ↔ Other Regions | {task_info['subtitle']}"
        )


def generate_behavioral_association_plots(visualizer, coord_mapper, data_dir, output_dir):
    """Generate behavioral association plots."""

    print("\n" + "="*70)
    print("GENERATING BEHAVIORAL ASSOCIATION PLOTS")
    print("="*70)

    # Define behavioral files to process
    behav_files = {
        'rest_asc_sensory': {
            'file': 'PEB_behav_associations_-ses-02_-task-rest_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat',
            'title': 'Rest - ASC Sensory Composite',
            'subtitle': 'Association with Sensory Experience Intensity',
            'covariate': 'ASC Sensory'
        },
        'rest_asc_auditory': {
            'file': 'PEB_behav_associations_-ses-02_-task-rest_cov-ASC5_AUDITORY_noFD.mat',
            'title': 'Rest - ASC Auditory',
            'subtitle': 'Association with Auditory Experience Intensity',
            'covariate': 'ASC Auditory'
        },
        'music_asc_auditory': {
            'file': 'PEB_behav_associations_-ses-02_-task-music_cov-ASC5_AUDITORY_noFD.mat',
            'title': 'Music - ASC Auditory',
            'subtitle': 'Association with Auditory Experience Intensity',
            'covariate': 'ASC Auditory'
        },
        'music_asc_sensory': {
            'file': 'PEB_behav_associations_-ses-02_-task-music_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat',
            'title': 'Music - ASC Sensory Composite',
            'subtitle': 'Association with Sensory Experience Intensity',
            'covariate': 'ASC Sensory'
        },
        'movie_asc_sensory': {
            'file': 'PEB_behav_associations_-ses-02_-task-movie_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat',
            'title': 'Movie - ASC Sensory Composite',
            'subtitle': 'Association with Sensory Experience Intensity',
            'covariate': 'ASC Sensory'
        },
        'meditation_asc_sensory': {
            'file': 'PEB_behav_associations_-ses-02_-task-meditation_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat',
            'title': 'Meditation - ASC Sensory Composite',
            'subtitle': 'Association with Sensory Experience Intensity',
            'covariate': 'ASC Sensory'
        }
    }

    for behav_name, behav_info in behav_files.items():
        mat_path = data_dir / behav_info['file']
        if not mat_path.exists():
            print(f"  Skipping {behav_name}: file not found")
            continue

        print(f"\n--- {behav_info['title']} ---")

        # Load connectivity
        try:
            conn_matrix, roi_names = visualizer.load_connectivity(str(mat_path), pp_threshold=0.99)
        except Exception as e:
            print(f"  Error loading {behav_name}: {e}")
            continue

        node_coords = coord_mapper.get_coordinates(roi_names)

        # Generate full network behavioral plot - Behavioral uses PRGn (diverging for correlations)
        output_file = output_dir / f"behav_{behav_name}_full_network.png"
        visualizer.plot_connectome(
            conn_matrix,
            node_coords,
            str(output_file),
            title=behav_info['title'],
            edge_threshold='0%',
            node_size=80,  # Larger nodes
            edge_cmap='PRGn',  # Purple-Green for behavioral associations
            display_mode='lyrz',
            colorbar=True,
            roi_names=roi_names,
            colorbar_label=f"β Coefficient ({behav_info['covariate']})",
            subtitle=f"{behav_info['subtitle']}\nPp>0.99 | {len(roi_names)} ROIs"
        )

        # Generate hippocampus focused behavioral plot (memory-related)
        hipp_filtered = visualizer.filter_connections(
            conn_matrix, roi_names,
            source_regions=['Hippocampus'],
            connection_type='bidirectional'
        )

        if hipp_filtered.any():
            output_file = output_dir / f"behav_{behav_name}_hippocampus.png"
            visualizer.plot_connectome(
                hipp_filtered,
                node_coords,
                str(output_file),
                title=f"{behav_info['title']} - Hippocampus",
                edge_threshold='0%',
                node_size=100,  # Larger nodes
                edge_cmap='PRGn',  # Purple-Green for behavioral
                display_mode='lyrz',
                colorbar=True,
                roi_names=roi_names,
                colorbar_label=f"β Coefficient ({behav_info['covariate']})",
                subtitle=f"Hippocampus Associations | {behav_info['subtitle']}"
            )


def generate_task_contrast_plots(visualizer, coord_mapper, data_dir, output_dir):
    """Generate task contrast plots."""

    print("\n" + "="*70)
    print("GENERATING TASK CONTRAST PLOTS")
    print("="*70)

    contrasts = {
        'rest_vs_music': {
            'file': 'PEB_contrast_-ses-02_-task-rest-task-music_cov-_noFD.mat',
            'title': 'Rest vs Music',
            'subtitle': 'Task Contrast (Rest - Music)'
        },
        'rest_vs_movie': {
            'file': 'PEB_contrast_-ses-02_-task-rest-task-movie_cov-_noFD.mat',
            'title': 'Rest vs Movie',
            'subtitle': 'Task Contrast (Rest - Movie)'
        },
        'music_vs_movie': {
            'file': 'PEB_contrast_-ses-02_-task-music-task-movie_cov-_noFD.mat',
            'title': 'Music vs Movie',
            'subtitle': 'Task Contrast (Music - Movie)'
        }
    }

    for contrast_name, contrast_info in contrasts.items():
        mat_path = data_dir / contrast_info['file']
        if not mat_path.exists():
            print(f"  Skipping {contrast_name}: file not found")
            continue

        print(f"\n--- {contrast_info['title']} ---")

        # Load connectivity
        try:
            conn_matrix, roi_names = visualizer.load_connectivity(str(mat_path), pp_threshold=0.99)
        except Exception as e:
            print(f"  Error loading {contrast_name}: {e}")
            continue

        node_coords = coord_mapper.get_coordinates(roi_names)

        # Generate full network contrast plot - Contrasts use RdYlBu_r (task differences)
        output_file = output_dir / f"contrast_{contrast_name}_full_network.png"
        visualizer.plot_connectome(
            conn_matrix,
            node_coords,
            str(output_file),
            title=contrast_info['title'],
            edge_threshold='0%',
            node_size=80,  # Larger nodes
            edge_cmap='RdYlBu_r',  # Red-Yellow-Blue for task contrasts
            display_mode='lyrz',
            colorbar=True,
            roi_names=roi_names,
            colorbar_label="Δ Connection Strength (Hz)",
            subtitle=f"{contrast_info['subtitle']}\nPp>0.99 | {len(roi_names)} ROIs"
        )


def main(paper_mode=True):
    """
    Main function to generate nilearn connectivity figures.

    Parameters
    ----------
    paper_mode : bool
        If True (default), generate only ROI-focused supplementary figures.
        If False, generate all exploratory figures.
    """
    print("="*70)
    print("PIPELINE STEP 02: NILEARN SUPPLEMENTARY FIGURES")
    print(f"Mode: {'PAPER (ROI-focused supplementary)' if paper_mode else 'FULL (all exploratory)'}")
    print("="*70)

    # Setup paths
    data_dir = project_root / "data" / "peb_outputs"

    # Output directory depends on mode
    if paper_mode:
        output_dir = project_root / "figures" / "supplementary"
    else:
        output_dir = project_root / "figures" / "nilearn"

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nData directory: {data_dir}")
    print(f"Output directory: {output_dir}")

    # Initialize
    print("\nInitializing AAL coordinate mapper...")
    coord_mapper = AALCoordinateMapper()
    visualizer = NilearnConnectivityVisualizer(coord_mapper)

    # Generate plots
    # Session change plots always generated (ROI-focused in paper mode)
    generate_session_change_plots(visualizer, coord_mapper, data_dir, output_dir, paper_mode=paper_mode)

    # Behavioral and contrast plots only in full mode
    if not paper_mode:
        generate_behavioral_association_plots(visualizer, coord_mapper, data_dir, output_dir)
        generate_task_contrast_plots(visualizer, coord_mapper, data_dir, output_dir)

    print("\n" + "="*70)
    print("PIPELINE STEP 02 COMPLETE!")
    print("="*70)
    print(f"\nAll figures saved to: {output_dir}")

    # List generated files
    generated_files = sorted(output_dir.glob("*.png"))
    print(f"\nGenerated {len(generated_files)} figures:")
    for f in generated_files:
        print(f"  - {f.name}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate nilearn supplementary figures',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        '--paper',
        action='store_true',
        default=True,
        help='Generate only ROI-focused supplementary figures (default)',
    )
    parser.add_argument(
        '--full',
        action='store_true',
        help='Generate all exploratory figures',
    )

    args = parser.parse_args()

    # --full overrides --paper
    paper_mode = not args.full

    main(paper_mode=paper_mode)
