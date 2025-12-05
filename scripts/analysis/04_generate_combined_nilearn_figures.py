#!/usr/bin/env python3
"""
Generate combined nilearn connectivity figures showing multiple conditions.

Creates both overlay and side-by-side panel visualizations for:
- All 4 task session changes
- Behavioral associations across tasks
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
    print("=" * 70)
    print("COMPREHENSIVE COMBINED CONNECTIVITY FIGURE GENERATION")
    print("=" * 70)

    # Setup paths
    data_dir = project_root / "massive_output_local" / "adam_m6"
    output_dir = project_root / "figures" / "nilearn" / "combined"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nData directory: {data_dir}")
    print(f"Output directory: {output_dir}")

    # Initialize
    print("\nInitializing AAL coordinate mapper...")
    coord_mapper = AALCoordinateMapper()
    visualizer = NilearnConnectivityVisualizer(coord_mapper)

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

    if len(connectivity_matrices) == 0:
        print("\nNo task data loaded! Skipping Part 1.")
    else:
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
            edge_cmap='PRGn',  # Purple-Green for behavioral
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
            edge_cmap='PRGn',  # Purple-Green for behavioral
            colorbar=True,
            roi_names=roi_names_sensory,
            subtitle=f"Session 2 Behavioral Associations | Pp>0.99 | {len(roi_names_sensory)} ROIs"
        )

    # =========================================================================
    # COMPLETE
    # =========================================================================
    print("\n" + "=" * 70)
    print("GENERATION COMPLETE!")
    print("=" * 70)
    print(f"\nAll combined figures saved to: {output_dir}")

    # List generated files
    generated_files = sorted(output_dir.glob("*.png"))
    print(f"\nGenerated {len(generated_files)} combined figures:")
    for f in generated_files:
        print(f"  - {f.name}")


if __name__ == '__main__':
    main()
