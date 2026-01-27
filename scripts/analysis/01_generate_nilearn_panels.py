#!/usr/bin/env python3
"""
Pipeline Step 01: Generate nilearn brain connectivity panel figures

This script consolidates all panel-based nilearn visualizations into a single
entry point with different modes.

Modes:
    --mode basic      : Multi-condition connectivity panels (session change, behavioral)
    --mode hypothesis : Hypothesis-filtered connectivity panels (dlPFC, hippocampus, etc.)
    --mode combined   : Overlays and side-by-side comparisons
    --mode all        : Generate all panel types (default)

Output Directories:
    basic      -> figures/nilearn/panels/
    hypothesis -> figures/nilearn/hypothesis_panels/
    combined   -> figures/nilearn/combined/

Usage:
    python scripts/analysis/01_generate_nilearn_panels.py --mode basic
    python scripts/analysis/01_generate_nilearn_panels.py --mode hypothesis
    python scripts/analysis/01_generate_nilearn_panels.py --mode combined
    python scripts/analysis/01_generate_nilearn_panels.py --mode all
    python scripts/analysis/01_generate_nilearn_panels.py  # defaults to --mode all
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


# =============================================================================
# SHARED UTILITIES
# =============================================================================

def initialize_visualizer():
    """Initialize the coordinate mapper and visualizer."""
    print("\nInitializing AAL coordinate mapper...")
    coord_mapper = AALCoordinateMapper()
    visualizer = NilearnConnectivityVisualizer(coord_mapper)
    return visualizer, coord_mapper


def load_conditions(visualizer, coord_mapper, file_dict, data_dir, pp_threshold=0.99, covariate_index=0):
    """
    Load connectivity matrices for multiple conditions.

    Parameters
    ----------
    visualizer : NilearnConnectivityVisualizer
        The connectivity visualizer instance
    coord_mapper : AALCoordinateMapper
        The coordinate mapper instance
    file_dict : dict
        Dictionary mapping condition names to filenames
    data_dir : Path
        Directory containing .mat data files
    pp_threshold : float
        Posterior probability threshold
    covariate_index : int
        Index of covariate to load (0=group mean, 1=behavioral)

    Returns
    -------
    tuple
        (matrices, names, roi_names, node_coords)
    """
    matrices = []
    names = []
    roi_names = None
    node_coords = None

    for task_name, filename in file_dict.items():
        mat_path = data_dir / filename
        if not mat_path.exists():
            print(f"  Skipping {task_name}: file not found")
            continue

        print(f"  Loading {task_name}...")
        try:
            conn_matrix, task_roi_names = visualizer.load_connectivity(
                str(mat_path), pp_threshold=pp_threshold, covariate_index=covariate_index
            )
            matrices.append(conn_matrix)
            names.append(task_name)

            if roi_names is None:
                roi_names = task_roi_names
                node_coords = coord_mapper.get_coordinates(roi_names)

        except Exception as e:
            print(f"  Error loading {task_name}: {e}")
            continue

    return matrices, names, roi_names, node_coords


# =============================================================================
# MODE: BASIC - Multi-condition connectivity panels
# =============================================================================

def generate_basic_panels(visualizer, coord_mapper, data_dir, output_dir):
    """
    Generate basic multi-condition connectivity panels.

    Outputs:
    - 01a_panel_change_all_conditions.png - Session change across all 4 conditions
    - 01b_panel_behav_asc_sensory_all_conditions.png - ASC Sensory across conditions
    - 01c_panel_behav_asc_auditory_rest_music.png - ASC Auditory (rest vs music)
    """
    print("\n" + "="*70)
    print("MODE: BASIC - Multi-condition connectivity panels")
    print("="*70)

    output_dir = output_dir / "panels"
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {output_dir}")

    # =========================================================================
    # OUTPUT 01a: Session Change - All Conditions Panel
    # =========================================================================
    print("\n" + "="*70)
    print("OUTPUT 01a: SESSION CHANGE - ALL CONDITIONS PANEL")
    print("="*70)

    tasks = {
        'Rest': 'PEB_change_-ses-01-ses-02_-task-rest_cov-_noFD.mat',
        'Music': 'PEB_change_-ses-01-ses-02_-task-music_cov-_noFD.mat',
        'Movie': 'PEB_change_-ses-01-ses-02_-task-movie_cov-_noFD.mat',
        'Meditation': 'PEB_change_-ses-01-ses-02_-task-meditation_cov-_noFD.mat'
    }

    print("\nLoading connectivity matrices...")
    matrices, names, roi_names, node_coords = load_conditions(
        visualizer, coord_mapper, tasks, data_dir
    )

    if len(matrices) > 0:
        output_file = output_dir / "01a_panel_change_all_conditions.png"
        visualizer.plot_sidebyside_connectome(
            connectivity_matrices=matrices,
            node_coords=node_coords,
            output_file=str(output_file),
            condition_names=names,
            title="Session Change - All Experimental Conditions",
            edge_threshold='0%',
            node_size=70,
            edge_cmap='coolwarm',
            colorbar=True,
            roi_names=roi_names,
            subtitle=f"Post-Psilocybin - Pre-Psilocybin | Pp>0.99 | {len(roi_names)} ROIs"
        )

    # =========================================================================
    # OUTPUT 01b: Behavioral ASC Sensory - All Conditions Panel
    # =========================================================================
    print("\n" + "="*70)
    print("OUTPUT 01b: BEHAVIORAL ASC SENSORY - ALL CONDITIONS PANEL")
    print("="*70)

    sensory_files = {
        'Rest': 'PEB_behav_associations_-ses-02_-task-rest_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat',
        'Music': 'PEB_behav_associations_-ses-02_-task-music_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat',
        'Movie': 'PEB_behav_associations_-ses-02_-task-movie_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat',
        'Meditation': 'PEB_behav_associations_-ses-02_-task-meditation_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat'
    }

    matrices, names, roi_names, node_coords = load_conditions(
        visualizer, coord_mapper, sensory_files, data_dir
    )

    if len(matrices) > 0:
        output_file = output_dir / "01b_panel_behav_asc_sensory_all_conditions.png"
        visualizer.plot_sidebyside_connectome(
            connectivity_matrices=matrices,
            node_coords=node_coords,
            output_file=str(output_file),
            condition_names=names,
            title="ASC Sensory Composite - All Experimental Conditions",
            edge_threshold='0%',
            node_size=70,
            edge_cmap='PRGn',
            colorbar=True,
            roi_names=roi_names,
            subtitle=f"Behavioral Associations | Session 2 | Pp>0.99 | {len(roi_names)} ROIs"
        )

    # =========================================================================
    # OUTPUT 01c: Behavioral ASC Auditory - Rest vs Music Panel
    # =========================================================================
    print("\n" + "="*70)
    print("OUTPUT 01c: BEHAVIORAL ASC AUDITORY - REST VS MUSIC PANEL")
    print("="*70)

    auditory_files = {
        'Rest': 'PEB_behav_associations_-ses-02_-task-rest_cov-ASC5_AUDITORY_noFD.mat',
        'Music': 'PEB_behav_associations_-ses-02_-task-music_cov-ASC5_AUDITORY_noFD.mat'
    }

    matrices, names, roi_names, node_coords = load_conditions(
        visualizer, coord_mapper, auditory_files, data_dir
    )

    if len(matrices) > 0:
        output_file = output_dir / "01c_panel_behav_asc_auditory_rest_music.png"
        visualizer.plot_sidebyside_connectome(
            connectivity_matrices=matrices,
            node_coords=node_coords,
            output_file=str(output_file),
            condition_names=names,
            title="ASC Auditory - Rest vs Music",
            edge_threshold='0%',
            node_size=70,
            edge_cmap='PRGn',
            colorbar=True,
            roi_names=roi_names,
            subtitle=f"Behavioral Associations | Session 2 | Pp>0.99 | {len(roi_names)} ROIs"
        )

    # List generated files
    generated_files = sorted(output_dir.glob("01*.png"))
    print(f"\nGenerated {len(generated_files)} basic panel figures:")
    for f in generated_files:
        print(f"  - {f.name}")


# =============================================================================
# MODE: HYPOTHESIS - Hypothesis-filtered connectivity panels
# =============================================================================

def generate_hypothesis_panels(visualizer, coord_mapper, data_dir, output_dir):
    """
    Generate hypothesis-specific connectivity panels.

    Each hypothesis is tested across multiple experimental conditions for both:
    - Session change (Post - Pre psilocybin)
    - Behavioral correlations (ASC composite sensory)
    """
    print("\n" + "="*70)
    print("MODE: HYPOTHESIS - Hypothesis-filtered connectivity panels")
    print("="*70)

    output_dir = output_dir / "hypothesis_panels"
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {output_dir}")

    # Define hypotheses with region filters
    hypotheses = [
        {
            'id': 'h01',
            'name': 'dlPFC ↔ Hippocampus',
            'description': 'dlPFC to Hippocampus and Hippocampus back to dlPFC (bidirectional)',
            'source_regions': ['Frontal_Mid', 'Hippocampus'],
            'target_regions': ['Frontal_Mid', 'Hippocampus'],
            'connection_type': 'bidirectional'
        },
        {
            'id': 'h02',
            'name': 'SOG+MTG → Hippocampus',
            'description': 'Superior Occipital Gyrus and Middle Temporal Gyrus into Hippocampus',
            'source_regions': ['Occipital_Sup', 'Temporal_Mid'],
            'target_regions': ['Hippocampus'],
            'connection_type': 'outgoing'
        },
        {
            'id': 'h03',
            'name': 'MTG → dlPFC',
            'description': 'Middle Temporal Gyrus into dlPFC',
            'source_regions': ['Temporal_Mid'],
            'target_regions': ['Frontal_Mid'],
            'connection_type': 'outgoing'
        },
        {
            'id': 'h04',
            'name': 'MTG ↔ SOG',
            'description': 'MTG and SOG bidirectional connections',
            'source_regions': ['Temporal_Mid', 'Occipital_Sup'],
            'target_regions': ['Temporal_Mid', 'Occipital_Sup'],
            'connection_type': 'bidirectional'
        },
        {
            'id': 'h05',
            'name': 'Hippocampus → Thalamus',
            'description': 'Hippocampus into Thalamus',
            'source_regions': ['Hippocampus'],
            'target_regions': ['Thalamus'],
            'connection_type': 'outgoing'
        },
        {
            'id': 'h06',
            'name': 'Thalamus → All',
            'description': 'Thalamus to most regions (outgoing)',
            'source_regions': ['Thalamus'],
            'target_regions': None,
            'connection_type': 'outgoing'
        },
        {
            'id': 'h07',
            'name': 'Thalamus ↔ MTG',
            'description': 'Thalamus and MTG bidirectional',
            'source_regions': ['Thalamus', 'Temporal_Mid'],
            'target_regions': ['Thalamus', 'Temporal_Mid'],
            'connection_type': 'bidirectional'
        },
        {
            'id': 'h08',
            'name': 'Thalamus ↔ MTG/SOG',
            'description': 'Thalamus bidirectional with MTG and SOG',
            'source_regions': ['Thalamus', 'Temporal_Mid', 'Occipital_Sup'],
            'target_regions': ['Thalamus', 'Temporal_Mid', 'Occipital_Sup'],
            'connection_type': 'bidirectional'
        },
        {
            'id': 'h09',
            'name': 'dlPFC ↔ Thalamus',
            'description': 'dlPFC and Thalamus bidirectional connections',
            'source_regions': ['Frontal_Mid', 'Thalamus'],
            'target_regions': ['Frontal_Mid', 'Thalamus'],
            'connection_type': 'bidirectional'
        },
        {
            'id': 'h10',
            'name': 'SOG+MTG ↔ Hippocampus',
            'description': 'SOG and MTG bidirectional with Hippocampus',
            'source_regions': ['Occipital_Sup', 'Temporal_Mid', 'Hippocampus'],
            'target_regions': ['Occipital_Sup', 'Temporal_Mid', 'Hippocampus'],
            'connection_type': 'bidirectional'
        },
        {
            'id': 'h11',
            'name': 'Thalamus ↔ Hippocampus',
            'description': 'Thalamus and Hippocampus bidirectional connections',
            'source_regions': ['Thalamus', 'Hippocampus'],
            'target_regions': ['Thalamus', 'Hippocampus'],
            'connection_type': 'bidirectional'
        }
    ]

    # Define experimental conditions
    change_conditions = [
        {'name': 'Rest', 'file': 'PEB_change_-ses-01-ses-02_-task-rest_cov-_noFD.mat'},
        {'name': 'Music', 'file': 'PEB_change_-ses-01-ses-02_-task-music_cov-_noFD.mat'},
        {'name': 'Movie', 'file': 'PEB_change_-ses-01-ses-02_-task-movie_cov-_noFD.mat'},
        {'name': 'Meditation', 'file': 'PEB_change_-ses-01-ses-02_-task-meditation_cov-_noFD.mat'}
    ]

    behavioral_conditions = [
        {'name': 'Rest', 'file': 'PEB_behav_associations_-ses-02_-task-rest_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat'},
        {'name': 'Music', 'file': 'PEB_behav_associations_-ses-02_-task-music_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat'},
        {'name': 'Movie', 'file': 'PEB_behav_associations_-ses-02_-task-movie_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat'},
        {'name': 'Meditation', 'file': 'PEB_behav_associations_-ses-02_-task-meditation_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat'},
    ]

    # Counter for output numbering
    output_counter = ord('a')

    # Generate panels for each hypothesis
    for hyp in hypotheses:
        print("\n" + "="*70)
        print(f"HYPOTHESIS {hyp['id'].upper()}: {hyp['name']}")
        print(f"Description: {hyp['description']}")
        print("="*70)

        # SESSION CHANGE
        print(f"\n--- Generating Session Change Panel for {hyp['id']} ---")

        change_matrices = []
        change_names = []
        node_coords = None
        roi_names = None

        for cond in change_conditions:
            mat_path = data_dir / cond['file']
            if not mat_path.exists():
                print(f"  Skipping {cond['name']}: file not found")
                continue

            print(f"  Loading {cond['name']}...")
            try:
                conn_matrix, roi_names = visualizer.load_connectivity(str(mat_path), pp_threshold=0.99)

                # Filter connections for this hypothesis
                filtered_matrix = visualizer.filter_connections(
                    conn_matrix,
                    roi_names,
                    source_regions=hyp['source_regions'],
                    target_regions=hyp['target_regions'],
                    connection_type=hyp['connection_type']
                )

                change_matrices.append(filtered_matrix)
                change_names.append(cond['name'])

                if node_coords is None:
                    node_coords = coord_mapper.get_coordinates(roi_names)

            except Exception as e:
                print(f"  Error loading {cond['name']}: {e}")
                continue

        if len(change_matrices) > 0:
            safe_name = hyp['name'].replace(' ', '_').replace('↔', 'bidirectional').replace('→', 'to').replace('+', '_').replace('/', '_')
            output_file = output_dir / f"02{chr(output_counter)}_panel_{hyp['id']}_{safe_name}_change.png"
            output_counter += 1

            print(f"\n  Creating side-by-side panel with {len(change_matrices)} conditions...")
            visualizer.plot_sidebyside_connectome(
                change_matrices,
                node_coords,
                str(output_file),
                condition_names=change_names,
                title=f"{hyp['name']} - Post-psilocybin - Pre-Psilocybin",
                edge_threshold='0%',
                node_size=70,
                edge_cmap='green_purple',
                colorbar=True,
                roi_names=roi_names
            )
            print(f"  Saved: {output_file.name}")

        # BEHAVIORAL ASSOCIATIONS
        print(f"\n--- Generating Behavioral Panel for {hyp['id']} ---")

        behav_matrices = []
        behav_names = []

        for cond in behavioral_conditions:
            mat_path = data_dir / cond['file']
            if not mat_path.exists():
                print(f"  Skipping {cond['name']}: file not found")
                continue

            print(f"  Loading {cond['name']}...")
            try:
                conn_matrix, roi_names = visualizer.load_connectivity(str(mat_path), pp_threshold=0.99, covariate_index=1)

                filtered_matrix = visualizer.filter_connections(
                    conn_matrix,
                    roi_names,
                    source_regions=hyp['source_regions'],
                    target_regions=hyp['target_regions'],
                    connection_type=hyp['connection_type']
                )

                behav_matrices.append(filtered_matrix)
                behav_names.append(cond['name'])

            except Exception as e:
                print(f"  Error loading {cond['name']}: {e}")
                continue

        if len(behav_matrices) > 0:
            safe_name = hyp['name'].replace(' ', '_').replace('↔', 'bidirectional').replace('→', 'to').replace('+', '_').replace('/', '_')
            output_file = output_dir / f"02{chr(output_counter)}_panel_{hyp['id']}_{safe_name}_behavioral.png"
            output_counter += 1

            print(f"\n  Creating side-by-side panel with {len(behav_matrices)} conditions...")
            visualizer.plot_sidebyside_connectome(
                behav_matrices,
                node_coords,
                str(output_file),
                condition_names=behav_names,
                title=f"{hyp['name']} - Behavioral Association",
                edge_threshold='0%',
                node_size=70,
                edge_cmap='viridis',
                colorbar=True,
                roi_names=roi_names,
                colorbar_label='Normalised Beta Coefficient'
            )
            print(f"  Saved: {output_file.name}")

    # List generated files
    generated_files = sorted(output_dir.glob("02*.png"))
    print(f"\nGenerated {len(generated_files)} hypothesis-based panels:")
    for f in generated_files:
        print(f"  - {f.name}")


# =============================================================================
# MODE: COMBINED - Overlays and side-by-side comparisons
# =============================================================================

def generate_combined_panels(visualizer, coord_mapper, data_dir, output_dir):
    """
    Generate combined overlay and side-by-side visualizations.

    Creates both overlay and side-by-side panel visualizations for:
    - All 4 task session changes
    - Behavioral associations across tasks
    """
    print("\n" + "="*70)
    print("MODE: COMBINED - Overlays and side-by-side comparisons")
    print("="*70)

    output_dir = output_dir / "combined"
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {output_dir}")

    # =========================================================================
    # PART 1: ALL TASKS SESSION CHANGES
    # =========================================================================
    print("\n" + "=" * 70)
    print("PART 1: ALL TASKS SESSION CHANGES")
    print("=" * 70)

    tasks = {
        'rest': 'PEB_change_-ses-01-ses-02_-task-rest_cov-_noFD.mat',
        'music': 'PEB_change_-ses-01-ses-02_-task-music_cov-_noFD.mat',
        'movie': 'PEB_change_-ses-01-ses-02_-task-movie_cov-_noFD.mat',
        'meditation': 'PEB_change_-ses-01-ses-02_-task-meditation_cov-_noFD.mat'
    }

    print("\nLoading all task session changes...")
    connectivity_matrices = []
    condition_names = []
    roi_names = None
    node_coords = None

    for task_name, filename in tasks.items():
        mat_path = data_dir / filename
        if not mat_path.exists():
            print(f"  Skipping {task_name}: file not found")
            continue

        print(f"  Loading {task_name}...")
        try:
            conn_matrix, task_roi_names = visualizer.load_connectivity(
                str(mat_path), pp_threshold=0.99
            )
            connectivity_matrices.append(conn_matrix)
            condition_names.append(task_name.capitalize())

            if roi_names is None:
                roi_names = task_roi_names
                node_coords = coord_mapper.get_coordinates(roi_names)

        except Exception as e:
            print(f"  Error loading {task_name}: {e}")
            continue

    if len(connectivity_matrices) > 0:
        print(f"\nSuccessfully loaded {len(connectivity_matrices)} task conditions")

        # Generate Overlay visualization
        print("\n--- Overlay Visualization ---")
        output_file = output_dir / "overlay_all_tasks_session_change.png"
        visualizer.plot_overlay_connectome(
            connectivity_matrices=connectivity_matrices,
            node_coords=node_coords,
            output_file=str(output_file),
            condition_names=condition_names,
            title="Session Change - All Tasks Overlaid",
            edge_threshold='0%',
            node_size=80,
            edge_cmaps=['Reds', 'Blues', 'Greens', 'Purples'],
            display_mode='lyrz',
            colorbar=False,
            roi_names=roi_names,
            subtitle=f"Post-Psilocybin - Pre-Psilocybin | Pp>0.99 | {len(roi_names)} ROIs",
            edge_alpha=0.6,
            edge_linewidth=2
        )

        # Generate Side-by-Side visualization
        print("\n--- Side-by-Side Panels ---")
        output_file = output_dir / "sidebyside_all_tasks_session_change.png"
        visualizer.plot_sidebyside_connectome(
            connectivity_matrices=connectivity_matrices,
            node_coords=node_coords,
            output_file=str(output_file),
            condition_names=condition_names,
            title="Session Change - Multi-Task Comparison",
            edge_threshold='0%',
            node_size=70,
            edge_cmap='coolwarm',
            colorbar=True,
            roi_names=roi_names,
            subtitle=f"Post-Psilocybin - Pre-Psilocybin | Pp>0.99 | {len(roi_names)} ROIs"
        )

    # =========================================================================
    # PART 2: BEHAVIORAL ASSOCIATIONS ACROSS TASKS
    # =========================================================================
    print("\n" + "=" * 70)
    print("PART 2: BEHAVIORAL ASSOCIATIONS")
    print("=" * 70)

    # ASC Auditory across tasks
    print("\n--- ASC Auditory Associations ---")
    auditory_files = {
        'rest': 'PEB_behav_associations_-ses-02_-task-rest_cov-ASC5_AUDITORY_noFD.mat',
        'music': 'PEB_behav_associations_-ses-02_-task-music_cov-ASC5_AUDITORY_noFD.mat'
    }

    auditory_matrices = []
    auditory_names = []
    roi_names_auditory = None
    node_coords_auditory = None

    for task_name, filename in auditory_files.items():
        mat_path = data_dir / filename
        if not mat_path.exists():
            continue

        print(f"  Loading {task_name} ASC Auditory...")
        try:
            conn_matrix, task_roi_names = visualizer.load_connectivity(
                str(mat_path), pp_threshold=0.99
            )
            auditory_matrices.append(conn_matrix)
            auditory_names.append(f"{task_name.capitalize()} Auditory")

            if roi_names_auditory is None:
                roi_names_auditory = task_roi_names
                node_coords_auditory = coord_mapper.get_coordinates(roi_names_auditory)

        except Exception as e:
            print(f"  Error loading {task_name}: {e}")
            continue

    if len(auditory_matrices) >= 2:
        # Overlay
        output_file = output_dir / "overlay_asc_auditory_rest_vs_music.png"
        visualizer.plot_overlay_connectome(
            connectivity_matrices=auditory_matrices,
            node_coords=node_coords_auditory,
            output_file=str(output_file),
            condition_names=auditory_names,
            title="ASC Auditory Associations - Rest vs Music",
            edge_threshold='0%',
            node_size=80,
            edge_cmaps=['Reds', 'Blues'],
            display_mode='lyrz',
            colorbar=False,
            roi_names=roi_names_auditory,
            subtitle=f"Session 2 Behavioral Associations | Pp>0.99 | {len(roi_names_auditory)} ROIs",
            edge_alpha=0.7,
            edge_linewidth=2
        )

        # Side-by-side
        output_file = output_dir / "sidebyside_asc_auditory_rest_vs_music.png"
        visualizer.plot_sidebyside_connectome(
            connectivity_matrices=auditory_matrices,
            node_coords=node_coords_auditory,
            output_file=str(output_file),
            condition_names=auditory_names,
            title="ASC Auditory Associations - Rest vs Music",
            edge_threshold='0%',
            node_size=70,
            edge_cmap='PRGn',
            colorbar=True,
            roi_names=roi_names_auditory,
            subtitle=f"Session 2 Behavioral Associations | Pp>0.99 | {len(roi_names_auditory)} ROIs"
        )

    # ASC Sensory across tasks
    print("\n--- ASC Sensory Composite Associations ---")
    sensory_files = {
        'rest': 'PEB_behav_associations_-ses-02_-task-rest_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat',
        'music': 'PEB_behav_associations_-ses-02_-task-music_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat',
        'movie': 'PEB_behav_associations_-ses-02_-task-movie_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat',
        'meditation': 'PEB_behav_associations_-ses-02_-task-meditation_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat'
    }

    sensory_matrices = []
    sensory_names = []
    roi_names_sensory = None
    node_coords_sensory = None

    for task_name, filename in sensory_files.items():
        mat_path = data_dir / filename
        if not mat_path.exists():
            continue

        print(f"  Loading {task_name} ASC Sensory...")
        try:
            conn_matrix, task_roi_names = visualizer.load_connectivity(
                str(mat_path), pp_threshold=0.99
            )
            sensory_matrices.append(conn_matrix)
            sensory_names.append(f"{task_name.capitalize()} Sensory")

            if roi_names_sensory is None:
                roi_names_sensory = task_roi_names
                node_coords_sensory = coord_mapper.get_coordinates(roi_names_sensory)

        except Exception as e:
            print(f"  Error loading {task_name}: {e}")
            continue

    if len(sensory_matrices) >= 2:
        # Overlay
        output_file = output_dir / "overlay_asc_sensory_all_tasks.png"
        visualizer.plot_overlay_connectome(
            connectivity_matrices=sensory_matrices,
            node_coords=node_coords_sensory,
            output_file=str(output_file),
            condition_names=sensory_names,
            title="ASC Sensory Composite Associations - Multi-Task",
            edge_threshold='0%',
            node_size=80,
            edge_cmaps=['Reds', 'Blues', 'Greens', 'Purples'],
            display_mode='lyrz',
            colorbar=False,
            roi_names=roi_names_sensory,
            subtitle=f"Session 2 Behavioral Associations | Pp>0.99 | {len(roi_names_sensory)} ROIs",
            edge_alpha=0.6,
            edge_linewidth=2
        )

        # Side-by-side
        output_file = output_dir / "sidebyside_asc_sensory_all_tasks.png"
        visualizer.plot_sidebyside_connectome(
            connectivity_matrices=sensory_matrices,
            node_coords=node_coords_sensory,
            output_file=str(output_file),
            condition_names=sensory_names,
            title="ASC Sensory Composite Associations - Multi-Task",
            edge_threshold='0%',
            node_size=70,
            edge_cmap='PRGn',
            colorbar=True,
            roi_names=roi_names_sensory,
            subtitle=f"Session 2 Behavioral Associations | Pp>0.99 | {len(roi_names_sensory)} ROIs"
        )

    # List generated files
    generated_files = sorted(output_dir.glob("*.png"))
    print(f"\nGenerated {len(generated_files)} combined figures:")
    for f in generated_files:
        print(f"  - {f.name}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Generate nilearn brain connectivity panel figures',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        '--mode',
        choices=['basic', 'hypothesis', 'combined', 'all'],
        default='all',
        help='Visualization mode: basic, hypothesis, combined, or all (default: all)',
    )

    args = parser.parse_args()

    print("=" * 70)
    print("PIPELINE STEP 01: NILEARN CONNECTIVITY PANELS")
    print(f"Mode: {args.mode.upper()}")
    print("=" * 70)

    # Setup paths
    data_dir = project_root / "data" / "peb_outputs"
    output_dir = project_root / "figures" / "nilearn"

    print(f"\nData directory: {data_dir}")
    print(f"Base output directory: {output_dir}")

    # Initialize
    visualizer, coord_mapper = initialize_visualizer()

    # Run selected mode(s)
    if args.mode == 'basic' or args.mode == 'all':
        generate_basic_panels(visualizer, coord_mapper, data_dir, output_dir)

    if args.mode == 'hypothesis' or args.mode == 'all':
        generate_hypothesis_panels(visualizer, coord_mapper, data_dir, output_dir)

    if args.mode == 'combined' or args.mode == 'all':
        generate_combined_panels(visualizer, coord_mapper, data_dir, output_dir)

    print("\n" + "=" * 70)
    print("PIPELINE STEP 01 COMPLETE!")
    print("=" * 70)
    print(f"\nAll figures saved under: {output_dir}")


if __name__ == '__main__':
    main()
