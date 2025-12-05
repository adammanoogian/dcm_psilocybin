#!/usr/bin/env python3
"""
Master Pipeline Runner - DCM Psilocybin Analysis

Executes all analysis stages in sequence with error handling and progress tracking.
Separates nilearn brain visualizations from PEB matrix heatmaps.

Pipeline Structure:
  Stage 01-04: Nilearn Brain Connectivity Visualizations
  Stage 05-06: PEB Matrix Heatmaps (separate from nilearn)
  Stage 07-08: Figure Organization and Paper Generation

Usage:
    python scripts/analysis/00_run_full_pipeline.py                    # Run all stages
    python scripts/analysis/00_run_full_pipeline.py --start=3          # Start from stage 3
    python scripts/analysis/00_run_full_pipeline.py --start=1 --end=4  # Run stages 1-4 (nilearn only)
    python scripts/analysis/00_run_full_pipeline.py --start=5 --end=6  # Run stages 5-6 (PEB only)
    python scripts/analysis/00_run_full_pipeline.py --nilearn          # Run nilearn stages only
    python scripts/analysis/00_run_full_pipeline.py --peb              # Run PEB stages only
"""

import subprocess
import sys
import argparse
from pathlib import Path
from datetime import datetime

PIPELINE_DIR = Path(__file__).parent
PROJECT_ROOT = PIPELINE_DIR.parent.parent

# Define pipeline stages with scripts and descriptions
# Organized into two main categories: Nilearn (brain visualizations) and PEB (matrix heatmaps)
PIPELINE_STAGES = [
    # =========================================================================
    # NILEARN BRAIN CONNECTIVITY VISUALIZATIONS (Stages 01-04)
    # =========================================================================
    {
        'stage': '01 - NILEARN CONNECTIVITY PANELS',
        'category': 'nilearn',
        'scripts': [
            ('01_generate_nilearn_connectivity_panels.py',
             'Multi-condition connectivity panels (session change, behavioral)'),
        ],
        'outputs': 'figures/nilearn/panels/'
    },
    {
        'stage': '02 - HYPOTHESIS-BASED NILEARN PANELS',
        'category': 'nilearn',
        'scripts': [
            ('02_generate_hypothesis_nilearn_panels.py',
             'Hypothesis-specific connectivity panels (dlPFC, hippocampus, etc.)'),
        ],
        'outputs': 'figures/nilearn/hypothesis_panels/'
    },
    {
        'stage': '03 - ALL NILEARN FIGURES',
        'category': 'nilearn',
        'scripts': [
            ('03_generate_all_nilearn_figures.py',
             'Comprehensive nilearn figures for all conditions (m1-m4)'),
        ],
        'outputs': 'figures/nilearn/'
    },
    {
        'stage': '04 - COMBINED NILEARN FIGURES',
        'category': 'nilearn',
        'scripts': [
            ('04_generate_combined_nilearn_figures.py',
             'Multi-condition overlays and comparisons (h01)'),
        ],
        'outputs': 'figures/nilearn/combined/'
    },
    # =========================================================================
    # PEB MATRIX HEATMAPS (Stages 05-06)
    # =========================================================================
    {
        'stage': '05 - PEB MATRIX HEATMAPS',
        'category': 'peb',
        'scripts': [
            ('05_generate_all_peb_matrices.py',
             'Generate PEB connectivity matrix heatmaps'),
        ],
        'outputs': 'figures/peb_matrices/'
    },
    {
        'stage': '06 - PEB MATRIX PANELS',
        'category': 'peb',
        'scripts': [
            ('06_generate_peb_matrix_panels.py',
             'Create 2x2 PEB matrix panel figures'),
        ],
        'outputs': 'figures/peb_matrices/panels/'
    },
    # =========================================================================
    # FIGURE ORGANIZATION & PAPER (Stages 07-08)
    # =========================================================================
    {
        'stage': '07 - ORGANIZE FIGURES',
        'category': 'organize',
        'scripts': [
            ('07_organize_figures.py',
             'Organize all figures to publication structure (m1-m4, h01-h03)'),
        ],
        'outputs': 'figures/organized/'
    },
    {
        'stage': '08 - GENERATE PAPER FIGURES',
        'category': 'paper',
        'scripts': [
            ('08_generate_paper_figures.py',
             'Generate final publication-ready figures'),
        ],
        'outputs': 'figures/paper/'
    },
]


def run_pipeline(start_stage: int = 1, end_stage: int = None,
                 category: str = None, verbose: bool = True):
    """
    Run the analysis pipeline.

    Parameters
    ----------
    start_stage : int
        Stage number to start from (1-indexed).
    end_stage : int, optional
        Stage number to end at (inclusive). If None, run all remaining stages.
    category : str, optional
        Filter by category: 'nilearn', 'peb', 'organize', 'paper', or None for all.
    verbose : bool
        Print detailed progress information.
    """
    start_time = datetime.now()

    print("=" * 80)
    print("DCM PSILOCYBIN ANALYSIS PIPELINE")
    print("=" * 80)
    print(f"Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Project root: {PROJECT_ROOT}")

    if end_stage is None:
        end_stage = len(PIPELINE_STAGES)

    # Filter stages by category if specified
    if category:
        stages_to_run = [s for i, s in enumerate(PIPELINE_STAGES, 1)
                         if start_stage <= i <= end_stage and s['category'] == category]
        print(f"\nRunning {category.upper()} stages only")
    else:
        stages_to_run = PIPELINE_STAGES[start_stage - 1:end_stage]
        print(f"\nRunning stages {start_stage} to {end_stage}")

    print("=" * 80)

    if not stages_to_run:
        print("No stages to run with the specified filters.")
        return True

    failed_stages = []

    for i, stage_info in enumerate(stages_to_run):
        # Find actual stage number
        stage_num = PIPELINE_STAGES.index(stage_info) + 1

        print(f"\n{'=' * 80}")
        print(f"STAGE {stage_num:02d}: {stage_info['stage']}")
        print(f"Category: {stage_info['category'].upper()}")
        print(f"Outputs: {stage_info['outputs']}")
        print(f"{'=' * 80}\n")

        for script_name, description in stage_info['scripts']:
            script_path = PIPELINE_DIR / script_name

            if not script_path.exists():
                print(f"WARNING: Script not found: {script_path}")
                print(f"   Skipping: {description}")
                failed_stages.append((stage_num, script_name, "Script not found"))
                continue

            print(f"Running: {description}")
            print(f"   Script: {script_name}")
            print("-" * 40)

            # Run the script
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=str(PROJECT_ROOT),
                capture_output=not verbose,
                text=True,
            )

            if result.returncode != 0:
                print(f"\nERROR: {script_name} failed with return code {result.returncode}")
                if not verbose and result.stderr:
                    print(f"Error output:\n{result.stderr}")
                failed_stages.append((stage_num, script_name, f"Exit code {result.returncode}"))

                # Ask whether to continue
                try:
                    response = input("\nContinue with remaining stages? (y/n): ")
                    if response.lower() != 'y':
                        print("\nPipeline execution aborted.")
                        return False
                except EOFError:
                    print("\nPipeline execution aborted (non-interactive mode).")
                    return False
            else:
                print(f"[OK] {script_name} completed successfully")

    # Pipeline summary
    end_time = datetime.now()
    duration = end_time - start_time

    print("\n" + "=" * 80)
    print("PIPELINE SUMMARY")
    print("=" * 80)
    print(f"Start time:  {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"End time:    {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duration:    {duration}")
    print(f"Stages run:  {len(stages_to_run)}")

    if failed_stages:
        print(f"\n{len(failed_stages)} stage(s) had errors:")
        for stage_num, script, error in failed_stages:
            print(f"   Stage {stage_num:02d}: {script} - {error}")
        return False
    else:
        print("\n[OK] All stages completed successfully!")
        return True


def print_pipeline_overview():
    """Print a summary of all pipeline stages."""
    print("\n" + "=" * 80)
    print("DCM PSILOCYBIN ANALYSIS PIPELINE - OVERVIEW")
    print("=" * 80)

    current_category = None
    for i, stage in enumerate(PIPELINE_STAGES, 1):
        if stage['category'] != current_category:
            current_category = stage['category']
            print(f"\n--- {current_category.upper()} ---")

        print(f"  {i:02d}. {stage['stage']}")
        for script, desc in stage['scripts']:
            print(f"      -> {desc}")
        print(f"      Output: {stage['outputs']}")

    print("\n" + "=" * 80)
    print("\nUsage examples:")
    print("  python 00_run_full_pipeline.py              # Run all stages")
    print("  python 00_run_full_pipeline.py --nilearn    # Run nilearn only (01-04)")
    print("  python 00_run_full_pipeline.py --peb        # Run PEB only (05-06)")
    print("  python 00_run_full_pipeline.py --start=5    # Start from stage 5")
    print("  python 00_run_full_pipeline.py --overview   # Show this overview")
    print("=" * 80)


def main():
    """Parse arguments and run pipeline."""
    parser = argparse.ArgumentParser(
        description='Run the DCM psilocybin analysis pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        '--start',
        type=int,
        default=1,
        help='Stage number to start from (default: 1)',
    )
    parser.add_argument(
        '--end',
        type=int,
        default=None,
        help='Stage number to end at (default: run all remaining)',
    )
    parser.add_argument(
        '--nilearn',
        action='store_true',
        help='Run only nilearn brain visualization stages (01-04)',
    )
    parser.add_argument(
        '--peb',
        action='store_true',
        help='Run only PEB matrix heatmap stages (05-06)',
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress verbose output from scripts',
    )
    parser.add_argument(
        '--overview',
        action='store_true',
        help='Print pipeline overview and exit',
    )

    args = parser.parse_args()

    if args.overview:
        print_pipeline_overview()
        sys.exit(0)

    # Determine category filter
    category = None
    if args.nilearn:
        category = 'nilearn'
    elif args.peb:
        category = 'peb'

    success = run_pipeline(
        start_stage=args.start,
        end_stage=args.end,
        category=category,
        verbose=not args.quiet,
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
