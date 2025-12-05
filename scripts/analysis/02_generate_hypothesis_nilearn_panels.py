#!/usr/bin/env python3
"""
Pipeline Step 02: Hypothesis-Based Nilearn Connectivity Panels

This script generates panel figures for specific connectivity hypotheses.
Each hypothesis is tested across multiple experimental conditions for both:
  - Session change (Post - Pre psilocybin)
  - Behavioral correlations (ASC composite sensory)

Output Numbering Convention:
- 02a_panel_h01_dlpfc_hippocampus_change.png - Hypothesis 1: dlPFC ↔ Hippocampus (change)
- 02b_panel_h01_dlpfc_hippocampus_behavioral.png - Hypothesis 1: dlPFC ↔ Hippocampus (behavioral)
- 02c_panel_h02_sog_mtg_to_hippocampus_change.png - Hypothesis 2: SOG+MTG → Hippocampus (change)
- 02d_panel_h02_sog_mtg_to_hippocampus_behavioral.png - Hypothesis 2: SOG+MTG → Hippocampus (behavioral)
- ... (continues for all 7 hypotheses × 2 analyses = 14 outputs)

Usage:
    python scripts/analysis/02_generate_hypothesis_nilearn_panels.py
"""

import sys
from pathlib import Path
import numpy as np

# Add project paths
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'scripts' / 'visualization'))

# Import modular functions (reuse existing!)
from scripts.visualization.plot_nilearn_connectivity import (
    AALCoordinateMapper, NilearnConnectivityVisualizer
)


def main():
    print("="*70)
    print("PIPELINE STEP 02: HYPOTHESIS-BASED NILEARN CONNECTIVITY PANELS")
    print("="*70)

    # Setup paths
    data_dir = project_root / "massive_output_local" / "adam_m6"
    output_dir = project_root / "figures" / "nilearn" / "hypothesis_panels"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nData directory: {data_dir}")
    print(f"Output directory: {output_dir}")

    # Initialize
    print("\nInitializing AAL coordinate mapper...")
    coord_mapper = AALCoordinateMapper()
    visualizer = NilearnConnectivityVisualizer(coord_mapper)

    # Define hypotheses with region filters
    # ROI names: Frontal_Mid (dlPFC), Hippocampus, Occipital_Sup (SOG), Temporal_Mid (MTG), Thalamus
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
            'target_regions': None,  # All regions
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

        # =====================================================================
        # SESSION CHANGE (Post - Pre Psilocybin)
        # =====================================================================
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

                # Always add condition even if no connections (show all 4 brains)
                change_matrices.append(filtered_matrix)
                change_names.append(cond['name'])

                # Get coordinates (same for all)
                if node_coords is None:
                    node_coords = coord_mapper.get_coordinates(roi_names)

            except Exception as e:
                print(f"  Error loading {cond['name']}: {e}")
                continue

        # Generate side-by-side panel for session change
        if len(change_matrices) > 0:
            output_file = output_dir / f"02{chr(output_counter)}_panel_{hyp['id']}_{hyp['name'].replace(' ', '_').replace('↔', 'bidirectional').replace('→', 'to').replace('+', '_').replace('/', '_')}_change.png"
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
            print(f"  ✓ Saved: {output_file.name}")
        else:
            print(f"  No connections found for {hyp['id']} session change - skipping panel")

        # =====================================================================
        # BEHAVIORAL ASSOCIATIONS (ASC Composite Sensory)
        # =====================================================================
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
                # Load covariate 1 (behavioral association), not covariate 0 (group mean)
                conn_matrix, roi_names = visualizer.load_connectivity(str(mat_path), pp_threshold=0.99, covariate_index=1)

                # Filter connections for this hypothesis
                filtered_matrix = visualizer.filter_connections(
                    conn_matrix,
                    roi_names,
                    source_regions=hyp['source_regions'],
                    target_regions=hyp['target_regions'],
                    connection_type=hyp['connection_type']
                )

                # Always add condition even if no connections (show all 4 brains)
                behav_matrices.append(filtered_matrix)
                behav_names.append(cond['name'])

            except Exception as e:
                print(f"  Error loading {cond['name']}: {e}")
                continue

        # Generate side-by-side panel for behavioral
        if len(behav_matrices) > 0:
            output_file = output_dir / f"02{chr(output_counter)}_panel_{hyp['id']}_{hyp['name'].replace(' ', '_').replace('↔', 'bidirectional').replace('→', 'to').replace('+', '_').replace('/', '_')}_behavioral.png"
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
                edge_cmap='viridis',  # Purple-to-Yellow for behavioral (matches PEB matrices)
                colorbar=True,
                roi_names=roi_names,
                colorbar_label='Normalised Beta Coefficient'  # Correct label for behavioral
            )
            print(f"  ✓ Saved: {output_file.name}")
        else:
            print(f"  No connections found for {hyp['id']} behavioral - skipping panel")

    # =========================================================================
    # COMPLETE
    # =========================================================================
    print("\n" + "="*70)
    print("PIPELINE STEP 02 COMPLETE!")
    print("="*70)

    # List generated files
    generated_files = sorted(output_dir.glob("02*.png"))
    print(f"\nGenerated {len(generated_files)} hypothesis-based panels:")
    for f in generated_files:
        print(f"  ✓ {f.name}")

    print(f"\nAll figures saved to: {output_dir}")


if __name__ == '__main__':
    main()
