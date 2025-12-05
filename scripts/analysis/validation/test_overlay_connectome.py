#!/usr/bin/env python3
"""
Quick test of overlay connectome visualization with 4 tasks.
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
    print("TESTING OVERLAY CONNECTOME VISUALIZATION")
    print("=" * 70)

    # Setup paths
    data_dir = project_root / "massive_output_local" / "adam_m6"
    output_dir = project_root / "figures" / "nilearn" / "test_overlay"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nData directory: {data_dir}")
    print(f"Output directory: {output_dir}")

    # Initialize
    print("\nInitializing AAL coordinate mapper...")
    coord_mapper = AALCoordinateMapper()
    visualizer = NilearnConnectivityVisualizer(coord_mapper)

    # Load all 4 task session changes
    tasks = {
        'rest': 'PEB_change_-ses-01-ses-02_-task-rest_cov-_noFD.mat',
        'music': 'PEB_change_-ses-01-ses-02_-task-music_cov-_noFD.mat',
        'movie': 'PEB_change_-ses-01-ses-02_-task-movie_cov-_noFD.mat',
        'meditation': 'PEB_change_-ses-01-ses-02_-task-meditation_cov-_noFD.mat'
    }

    print("\n" + "=" * 70)
    print("LOADING CONNECTIVITY DATA")
    print("=" * 70)

    connectivity_matrices = []
    condition_names = []
    roi_names = None
    node_coords = None

    for task_name, filename in tasks.items():
        mat_path = data_dir / filename
        if not mat_path.exists():
            print(f"  Skipping {task_name}: file not found")
            continue

        print(f"\nLoading {task_name}...")
        try:
            conn_matrix, task_roi_names = visualizer.load_connectivity(
                str(mat_path), pp_threshold=0.99
            )
            connectivity_matrices.append(conn_matrix)
            condition_names.append(task_name.capitalize())

            if roi_names is None:
                roi_names = task_roi_names
                node_coords = coord_mapper.get_coordinates(roi_names)
                print(f"  Loaded {len(roi_names)} ROIs")

            non_zero = (conn_matrix != 0).sum()
            print(f"  Non-zero connections: {non_zero}")

        except Exception as e:
            print(f"  Error loading {task_name}: {e}")
            continue

    if len(connectivity_matrices) == 0:
        print("\nNo data loaded! Exiting.")
        return

    print(f"\nSuccessfully loaded {len(connectivity_matrices)} conditions")

    # Test 1: Full network overlay
    print("\n" + "=" * 70)
    print("TEST 1: Full Network Overlay (All 4 Tasks)")
    print("=" * 70)

    output_file = output_dir / "test_overlay_all_tasks_full_network.png"
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

    # Test 2: Try with just 2 conditions for clearer comparison
    print("\n" + "=" * 70)
    print("TEST 2: Two-Condition Overlay (Rest vs Music)")
    print("=" * 70)

    if len(connectivity_matrices) >= 2:
        output_file = output_dir / "test_overlay_rest_vs_music.png"
        visualizer.plot_overlay_connectome(
            connectivity_matrices=[connectivity_matrices[0], connectivity_matrices[1]],
            node_coords=node_coords,
            output_file=str(output_file),
            condition_names=[condition_names[0], condition_names[1]],
            title="Session Change - Rest vs Music",
            edge_threshold='0%',
            node_size=80,
            edge_cmaps=['Reds', 'Blues'],
            display_mode='lyrz',
            colorbar=False,
            roi_names=roi_names,
            subtitle=f"Post-Psilocybin - Pre-Psilocybin | Pp>0.99",
            edge_alpha=0.7,  # Less transparent for 2 conditions
            edge_linewidth=2.5
        )

    # Test 3: Side-by-side panel comparison
    print("\n" + "=" * 70)
    print("TEST 3: Side-by-Side Panels (All 4 Tasks)")
    print("=" * 70)

    output_file = output_dir / "test_sidebyside_all_tasks.png"
    visualizer.plot_sidebyside_connectome(
        connectivity_matrices=connectivity_matrices,
        node_coords=node_coords,
        output_file=str(output_file),
        condition_names=condition_names,
        title="Session Change - Side-by-Side Comparison",
        edge_threshold='0%',
        node_size=70,
        edge_cmap='coolwarm',
        colorbar=True,
        roi_names=roi_names,
        subtitle=f"Post-Psilocybin - Pre-Psilocybin | Pp>0.99 | {len(roi_names)} ROIs"
    )

    print("\n" + "=" * 70)
    print("TESTING COMPLETE!")
    print("=" * 70)
    print(f"\nTest figures saved to: {output_dir}")

    # List generated files
    generated_files = sorted(output_dir.glob("*.png"))
    print(f"\nGenerated {len(generated_files)} test figures:")
    for f in generated_files:
        print(f"  - {f.name}")


if __name__ == '__main__':
    main()
