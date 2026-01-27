#!/usr/bin/env python3
"""
Pipeline Step 03: Generate PEB matrix heatmaps for all conditions.

Organized by experimental condition matching the nilearn convention:
- m1 = REST
- m2 = MUSIC
- m3 = MOVIE
- m4 = MEDITATION

Letter codes:
- a = Session change (Post - Pre psilocybin)
- b = Behavioral association (11D-ASC composite sensory)
- c = Behavioral association (5D-ASC auditory)

Usage:
    # Paper mode (default): Generate only matrices needed for 2x2 panels
    python scripts/analysis/03_generate_all_peb_matrices.py
    python scripts/analysis/03_generate_all_peb_matrices.py --paper

    # Full mode: Generate all exploratory matrices
    python scripts/analysis/03_generate_all_peb_matrices.py --full
"""

import sys
import argparse
from pathlib import Path
import matplotlib.pyplot as plt

# Add project paths
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'scripts' / 'visualization'))

from scripts.visualization.plot_PEB_results import PEBDataLoader, PEBPlotter


def generate_peb_matrices(paper_mode=True, visualizer=None):
    """
    Generate PEB matrix heatmaps for all conditions.

    Parameters
    ----------
    paper_mode : bool
        If True (default), generate only matrices needed for 2x2 panels (m*-a, m*-b).
        If False, generate all matrices including m*-c (5D-ASC auditory).
    visualizer : optional
        Unused, kept for backward compatibility.
    """
    print("=" * 70)
    print("PIPELINE STEP 03: PEB MATRIX HEATMAP GENERATION")
    print(f"Mode: {'PAPER (panel matrices only)' if paper_mode else 'FULL (all matrices)'}")
    print("=" * 70)

    # Setup paths
    data_dir = project_root / "data" / "peb_outputs"
    output_dir = project_root / "figures" / "peb_matrices"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nData directory: {data_dir}")
    print(f"Output directory: {output_dir}")

    # Get default parameters
    params = PEBDataLoader.get_peb_plot_parameters()
    params['pp_threshold'] = 0.99

    # Define all analyses to process
    # Paper mode: Only m*-a (session change) and m*-b (behavioral 11D-ASC) are needed for panels
    # Full mode: Also includes m*-c (behavioral 5D-ASC auditory)
    analyses = {
        # =====================================================================
        # M1: REST CONDITION
        # =====================================================================
        'm1-a': {
            'file': 'PEB_change_-ses-01-ses-02_-task-rest_cov-_noFD.mat',
            'name': 'REST - Session Change',
            'peb_type': 'change',
            'paper_mode': True,  # Needed for paper
        },
        'm1-b': {
            'file': 'PEB_behav_associations_-ses-02_-task-rest_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat',
            'name': 'REST - Behavioral (11D-ASC Sensory)',
            'peb_type': 'behav_associations',
            'paper_mode': True,  # Needed for paper
        },
        'm1-c': {
            'file': 'PEB_behav_associations_-ses-02_-task-rest_cov-ASC5_AUDITORY_noFD.mat',
            'name': 'REST - Behavioral (5D-ASC Auditory)',
            'peb_type': 'behav_associations',
            'paper_mode': False,  # Full mode only
        },

        # =====================================================================
        # M2: MUSIC CONDITION
        # =====================================================================
        'm2-a': {
            'file': 'PEB_change_-ses-01-ses-02_-task-music_cov-_noFD.mat',
            'name': 'MUSIC - Session Change',
            'peb_type': 'change',
            'paper_mode': True,  # Needed for paper
        },
        'm2-b': {
            'file': 'PEB_behav_associations_-ses-02_-task-music_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat',
            'name': 'MUSIC - Behavioral (11D-ASC Sensory)',
            'peb_type': 'behav_associations',
            'paper_mode': True,  # Needed for paper
        },
        'm2-c': {
            'file': 'PEB_behav_associations_-ses-02_-task-music_cov-ASC5_AUDITORY_noFD.mat',
            'name': 'MUSIC - Behavioral (5D-ASC Auditory)',
            'peb_type': 'behav_associations',
            'paper_mode': False,  # Full mode only
        },

        # =====================================================================
        # M3: MOVIE CONDITION
        # =====================================================================
        'm3-a': {
            'file': 'PEB_change_-ses-01-ses-02_-task-movie_cov-_noFD.mat',
            'name': 'MOVIE - Session Change',
            'peb_type': 'change',
            'paper_mode': True,  # Needed for paper
        },
        'm3-b': {
            'file': 'PEB_behav_associations_-ses-02_-task-movie_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat',
            'name': 'MOVIE - Behavioral (11D-ASC Sensory)',
            'peb_type': 'behav_associations',
            'paper_mode': True,  # Needed for paper
        },

        # =====================================================================
        # M4: MEDITATION CONDITION
        # =====================================================================
        'm4-a': {
            'file': 'PEB_change_-ses-01-ses-02_-task-meditation_cov-_noFD.mat',
            'name': 'MEDITATION - Session Change',
            'peb_type': 'change',
            'paper_mode': True,  # Needed for paper
        },
        'm4-b': {
            'file': 'PEB_behav_associations_-ses-02_-task-meditation_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat',
            'name': 'MEDITATION - Behavioral (11D-ASC Sensory)',
            'peb_type': 'behav_associations',
            'paper_mode': True,  # Needed for paper
        },
    }

    # Filter analyses based on paper_mode
    if paper_mode:
        analyses = {k: v for k, v in analyses.items() if v.get('paper_mode', True)}

    # Process each analysis
    stats = {'generated': 0, 'missing': 0, 'errors': 0}
    generated_files = []

    for code, info in analyses.items():
        mat_path = data_dir / info['file']

        if not mat_path.exists():
            print(f"\n[WARN] {code}: FILE NOT FOUND")
            print(f"  {info['file']}")
            stats['missing'] += 1
            continue

        print(f"\n{'=' * 70}")
        print(f"Processing {code.upper()}: {info['name']}")
        print(f"{'=' * 70}")

        try:
            # Load PEB data
            loader = PEBDataLoader(str(mat_path), params)
            peb_data = loader.get_data()

            # Override PEB type from file detection
            peb_data['peb_type'] = info['peb_type']

            # Create plotter and generate heatmaps
            plotter = PEBPlotter(peb_data, str(mat_path), params)
            plotter.plot_heatmaps()

            # Save with systematic naming
            # For session change (type 'change'), we get multiple covariates
            # For behavioral, we get one covariate
            if info['peb_type'] == 'change':
                # Session change generates: Pre-Psilocybin, Post-Psilocybin, Change
                # Skip group mean covariate (not useful for panels)
                for i, (fig, cov_name) in enumerate(zip(plotter.figures, plotter.covariate_names)):
                    if cov_name == 'mean of group 1':
                        suffix = 'pre'
                    elif cov_name == 'mean of second group':
                        suffix = 'post'
                    elif cov_name == 'Change toward 0':
                        suffix = 'change'
                    else:
                        # Skip unknown covariates (e.g., intermediate group mean)
                        print(f"  [SKIP] Skipping unneeded covariate: {cov_name}")
                        plt.close(fig)
                        continue

                    output_file = output_dir / f"{code}_matrix_{suffix}.png"
                    fig.savefig(output_file, dpi=300, bbox_inches='tight', pad_inches=0.02)
                    print(f"  [OK] Saved: {output_file.name}")
                    generated_files.append(output_file)
                    stats['generated'] += 1
            else:
                # Behavioral generates multiple covariates
                # Covariate 0 = group mean, Covariate 1 = behavioral association (the one we want!)
                if len(plotter.figures) > 1:
                    # Save the behavioral association covariate (index 1)
                    output_file = output_dir / f"{code}_matrix.png"
                    plotter.figures[1].savefig(output_file, dpi=300, bbox_inches='tight', pad_inches=0.02)
                    print(f"  [OK] Saved: {output_file.name} (Covariate 1: Behavioral Association)")
                    generated_files.append(output_file)
                    stats['generated'] += 1
                elif len(plotter.figures) > 0:
                    # Fallback: save first figure if only one covariate exists
                    output_file = output_dir / f"{code}_matrix.png"
                    plotter.figures[0].savefig(output_file, dpi=300, bbox_inches='tight', pad_inches=0.02)
                    print(f"  [OK] Saved: {output_file.name} (Only one covariate)")
                    generated_files.append(output_file)
                    stats['generated'] += 1

        except Exception as e:
            print(f"  [ERROR] processing {code}: {e}")
            import traceback
            traceback.print_exc()
            stats['errors'] += 1
            continue

    # Summary
    print("\n" + "=" * 70)
    print("PIPELINE STEP 03 COMPLETE!")
    print("=" * 70)
    print(f"\nStatistics:")
    print(f"  [OK] Generated: {stats['generated']}")
    print(f"  [WARN] Missing: {stats['missing']}")
    print(f"  [ERROR] Errors: {stats['errors']}")
    print(f"\nAll PEB matrix heatmaps saved to: {output_dir}")

    if generated_files:
        print(f"\nGenerated {len(generated_files)} PEB matrix files:")
        for f in sorted(generated_files):
            print(f"  - {f.name}")

    return stats


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate PEB matrix heatmaps',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        '--paper',
        action='store_true',
        default=True,
        help='Generate only matrices needed for 2x2 panels (default)',
    )
    parser.add_argument(
        '--full',
        action='store_true',
        help='Generate all exploratory matrices',
    )

    args = parser.parse_args()

    # --full overrides --paper
    paper_mode = not args.full

    generate_peb_matrices(paper_mode=paper_mode)
