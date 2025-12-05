#!/usr/bin/env python3
"""
Generate hypothesis-based connectivity panels.

Each hypothesis focuses on specific network connections (e.g., dlPFC outgoing, hippocampus)
and shows all experimental conditions (rest, music, movie, meditation) for that network.

Hypothesis Structure:
- h02: dlPFC outgoing connections
  - h02-a: Session change (all 4 tasks)
  - h02-b: Behavioral 11D-ASC (rest, music, movie)
- h03: Hippocampus bidirectional connections
  - h03-a: Session change (all 4 tasks)
  - h03-b: Behavioral 11D-ASC (rest, music, movie)
"""

import sys
from pathlib import Path
import numpy as np

# Add project paths
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'scripts' / 'visualization'))

from scripts.visualization.plot_nilearn_connectivity import (
    AALCoordinateMapper, NilearnConnectivityVisualizer
)


# Define hypotheses
HYPOTHESES = {
    'h02': {
        'name': 'dlPFC Outgoing Connections',
        'source_regions': ['Frontal_Mid'],
        'connection_type': 'outgoing',
        'description': 'Connections FROM dlPFC (Frontal_Mid) to other regions'
    },
    'h03': {
        'name': 'Hippocampus Connections',
        'source_regions': ['Hippocampus'],
        'connection_type': 'bidirectional',
        'description': 'Bidirectional connections involving Hippocampus'
    }
}


def generate_hypothesis_panel(
    visualizer,
    coord_mapper,
    data_dir,
    output_dir,
    hypothesis_id,
    hypothesis_config,
    analysis_type='session_change'
):
    """
    Generate panel for a specific hypothesis and analysis type.

    Parameters
    ----------
    visualizer : NilearnConnectivityVisualizer
        Visualizer instance
    coord_mapper : AALCoordinateMapper
        Coordinate mapper instance
    data_dir : Path
        Directory containing PEB data files
    output_dir : Path
        Output directory for figures
    hypothesis_id : str
        Hypothesis ID (e.g., 'h02', 'h03')
    hypothesis_config : dict
        Hypothesis configuration (source_regions, connection_type, name, etc.)
    analysis_type : str
        'session_change' or 'behavioral'
    """

    print(f"\n{'='*70}")
    print(f"Hypothesis {hypothesis_id.upper()}: {hypothesis_config['name']}")
    print(f"Analysis: {analysis_type.replace('_', ' ').title()}")
    print(f"{'='*70}")
    print(f"Network filter: {hypothesis_config['description']}")

    # Define data files based on analysis type
    if analysis_type == 'session_change':
        letter_code = 'a'
        data_files = {
            'Rest': 'PEB_change_-ses-01-ses-02_-task-rest_cov-_noFD.mat',
            'Music': 'PEB_change_-ses-01-ses-02_-task-music_cov-_noFD.mat',
            'Movie': 'PEB_change_-ses-01-ses-02_-task-movie_cov-_noFD.mat',
            'Meditation': 'PEB_change_-ses-01-ses-02_-task-meditation_cov-_noFD.mat'
        }
        edge_cmap = 'coolwarm'
        subtitle_prefix = "Session Change (Post - Pre Psilocybin)"

    elif analysis_type == 'behavioral':
        letter_code = 'b'
        data_files = {
            'Rest': 'PEB_behav_associations_-ses-02_-task-rest_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat',
            'Music': 'PEB_behav_associations_-ses-02_-task-music_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat',
            'Movie': 'PEB_behav_associations_-ses-02_-task-movie_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat',
            'Meditation': 'PEB_behav_associations_-ses-02_-task-meditation_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat'
        }
        edge_cmap = 'PRGn'
        subtitle_prefix = "Behavioral Associations (11D-ASC Composite Sensory)"

    else:
        raise ValueError(f"Unknown analysis_type: {analysis_type}")

    # Load and filter connectivity matrices
    print("\nLoading and filtering connectivity data...")
    connectivity_matrices = []
    condition_names = []
    roi_names = None
    node_coords = None

    for condition_name, filename in data_files.items():
        mat_path = data_dir / filename

        if not mat_path.exists():
            print(f"  Skipping {condition_name}: file not found")
            continue

        print(f"  Loading {condition_name}...")
        try:
            # Load connectivity
            conn_matrix, task_roi_names = visualizer.load_connectivity(
                str(mat_path), pp_threshold=0.99
            )

            # Apply network filter
            filtered_matrix = visualizer.filter_connections(
                conn_matrix,
                task_roi_names,
                source_regions=hypothesis_config['source_regions'],
                connection_type=hypothesis_config['connection_type']
            )

            # Count non-zero connections
            n_connections = np.count_nonzero(filtered_matrix)
            print(f"    {n_connections} connections after filtering")

            if n_connections == 0:
                print(f"    Warning: No connections found after filtering!")

            connectivity_matrices.append(filtered_matrix)
            condition_names.append(condition_name)

            if roi_names is None:
                roi_names = task_roi_names
                node_coords = coord_mapper.get_coordinates(roi_names)

        except Exception as e:
            print(f"  Error loading {condition_name}: {e}")
            import traceback
            traceback.print_exc()
            continue

    if len(connectivity_matrices) == 0:
        print("\nNo data loaded! Skipping this hypothesis.")
        return

    print(f"\nSuccessfully loaded {len(connectivity_matrices)} conditions")

    # Generate side-by-side panel
    output_filename = f"{hypothesis_id}-{letter_code}_{hypothesis_config['source_regions'][0].lower()}_{analysis_type}.png"
    output_file = output_dir / output_filename

    subtitle = f"{subtitle_prefix} | {hypothesis_config['description']} | Pp>0.99 | {len(roi_names)} ROIs"

    print(f"\nGenerating panel...")
    visualizer.plot_sidebyside_connectome(
        connectivity_matrices=connectivity_matrices,
        node_coords=node_coords,
        output_file=str(output_file),
        condition_names=condition_names,
        title=f"{hypothesis_id.upper()}-{letter_code.upper()}: {hypothesis_config['name']} - {analysis_type.replace('_', ' ').title()}",
        edge_threshold='0%',
        node_size=70,
        edge_cmap=edge_cmap,
        colorbar=True,
        roi_names=roi_names,
        subtitle=subtitle
    )

    print(f"✓ Saved: {output_filename}")


def main():
    print("=" * 70)
    print("HYPOTHESIS-BASED CONNECTIVITY PANEL GENERATION")
    print("=" * 70)

    # Setup paths
    data_dir = project_root / "massive_output_local" / "adam_m6"
    output_dir = project_root / "figures" / "nilearn" / "hypotheses"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nData directory: {data_dir}")
    print(f"Output directory: {output_dir}")

    # Initialize
    print("\nInitializing AAL coordinate mapper...")
    coord_mapper = AALCoordinateMapper()
    visualizer = NilearnConnectivityVisualizer(coord_mapper)

    # Generate panels for each hypothesis
    for hypothesis_id, hypothesis_config in HYPOTHESES.items():

        # Session change (letter 'a')
        generate_hypothesis_panel(
            visualizer=visualizer,
            coord_mapper=coord_mapper,
            data_dir=data_dir,
            output_dir=output_dir,
            hypothesis_id=hypothesis_id,
            hypothesis_config=hypothesis_config,
            analysis_type='session_change'
        )

        # Behavioral associations (letter 'b')
        generate_hypothesis_panel(
            visualizer=visualizer,
            coord_mapper=coord_mapper,
            data_dir=data_dir,
            output_dir=output_dir,
            hypothesis_id=hypothesis_id,
            hypothesis_config=hypothesis_config,
            analysis_type='behavioral'
        )

    # Summary
    print("\n" + "=" * 70)
    print("GENERATION COMPLETE!")
    print("=" * 70)
    print(f"\nAll hypothesis panels saved to: {output_dir}")

    generated_files = sorted(output_dir.glob("*.png"))
    print(f"\nGenerated {len(generated_files)} hypothesis panels:")
    for f in generated_files:
        print(f"  - {f.name}")


if __name__ == '__main__':
    main()
