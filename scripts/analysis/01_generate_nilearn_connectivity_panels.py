#!/usr/bin/env python3
"""
Pipeline Step 01: Generate nilearn brain connectivity panel figures

This script orchestrates the generation of multi-condition connectivity panels
using the existing modular visualization scripts.

Output Numbering Convention:
- 01a_panel_change_all_conditions.png - Session change across all 4 conditions
- 01b_panel_behav_asc_sensory_all_conditions.png - ASC Sensory across conditions
- 01c_panel_behav_asc_auditory_rest_music.png - ASC Auditory (rest vs music)

Usage:
    python scripts/analysis/01_generate_nilearn_connectivity_panels.py
"""

import sys
from pathlib import Path

# Add project paths
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'scripts' / 'visualization'))

from scripts.visualization.plot_nilearn_connectivity import (
    AALCoordinateMapper, NilearnConnectivityVisualizer
)


def main():
    print("="*70)
    print("PIPELINE STEP 01: NILEARN CONNECTIVITY PANELS")
    print("="*70)

    # Setup paths
    data_dir = project_root / "massive_output_local" / "adam_m6"
    output_dir = project_root / "figures" / "nilearn" / "panels"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nData directory: {data_dir}")
    print(f"Output directory: {output_dir}")

    # Initialize
    print("\nInitializing AAL coordinate mapper...")
    coord_mapper = AALCoordinateMapper()
    visualizer = NilearnConnectivityVisualizer(coord_mapper)

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
            condition_names.append(task_name)

            if roi_names is None:
                roi_names = task_roi_names
                node_coords = coord_mapper.get_coordinates(roi_names)

        except Exception as e:
            print(f"  Error loading {task_name}: {e}")
            continue

    if len(connectivity_matrices) > 0:
        output_file = output_dir / "01a_panel_change_all_conditions.png"
        visualizer.plot_sidebyside_connectome(
            connectivity_matrices=connectivity_matrices,
            node_coords=node_coords,
            output_file=str(output_file),
            condition_names=condition_names,
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

    sensory_matrices = []
    sensory_names = []
    roi_names_sensory = None
    node_coords_sensory = None

    for task_name, filename in sensory_files.items():
        mat_path = data_dir / filename
        if not mat_path.exists():
            print(f"  Skipping {task_name}: file not found")
            continue

        print(f"  Loading {task_name} ASC Sensory...")
        try:
            conn_matrix, task_roi_names = visualizer.load_connectivity(
                str(mat_path), pp_threshold=0.99
            )
            sensory_matrices.append(conn_matrix)
            sensory_names.append(task_name)

            if roi_names_sensory is None:
                roi_names_sensory = task_roi_names
                node_coords_sensory = coord_mapper.get_coordinates(roi_names_sensory)

        except Exception as e:
            print(f"  Error loading {task_name}: {e}")
            continue

    if len(sensory_matrices) > 0:
        output_file = output_dir / "01b_panel_behav_asc_sensory_all_conditions.png"
        visualizer.plot_sidebyside_connectome(
            connectivity_matrices=sensory_matrices,
            node_coords=node_coords_sensory,
            output_file=str(output_file),
            condition_names=sensory_names,
            title="ASC Sensory Composite - All Experimental Conditions",
            edge_threshold='0%',
            node_size=70,
            edge_cmap='PRGn',
            colorbar=True,
            roi_names=roi_names_sensory,
            subtitle=f"Behavioral Associations | Session 2 | Pp>0.99 | {len(roi_names_sensory)} ROIs"
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
            auditory_names.append(task_name)

            if roi_names_auditory is None:
                roi_names_auditory = task_roi_names
                node_coords_auditory = coord_mapper.get_coordinates(roi_names_auditory)

        except Exception as e:
            print(f"  Error loading {task_name}: {e}")
            continue

    if len(auditory_matrices) > 0:
        output_file = output_dir / "01c_panel_behav_asc_auditory_rest_music.png"
        visualizer.plot_sidebyside_connectome(
            connectivity_matrices=auditory_matrices,
            node_coords=node_coords_auditory,
            output_file=str(output_file),
            condition_names=auditory_names,
            title="ASC Auditory - Rest vs Music",
            edge_threshold='0%',
            node_size=70,
            edge_cmap='PRGn',
            colorbar=True,
            roi_names=roi_names_auditory,
            subtitle=f"Behavioral Associations | Session 2 | Pp>0.99 | {len(roi_names_auditory)} ROIs"
        )

    # =========================================================================
    # COMPLETE
    # =========================================================================
    print("\n" + "="*70)
    print("PIPELINE STEP 01 COMPLETE!")
    print("="*70)
    print(f"\nAll panel figures saved to: {output_dir}")

    # List generated files
    generated_files = sorted(output_dir.glob("01*.png"))
    print(f"\nGenerated {len(generated_files)} numbered panel figures:")
    for f in generated_files:
        print(f"  ✓ {f.name}")


if __name__ == '__main__':
    main()
