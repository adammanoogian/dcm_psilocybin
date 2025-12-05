#!/usr/bin/env python3
"""
Generate 2x2 PEB Matrix Panels

Creates combined 2x2 panels for each experimental condition showing:
- Panel A (top-left): Pre-Psilocybin (baseline)
- Panel B (top-right): Post-Psilocybin
- Panel C (bottom-left): Change toward zero
- Panel D (bottom-right): Behavioral Associations (11D-ASC A-constrained)

Follows the m1-m4 naming convention:
- m1 = REST
- m2 = MUSIC
- m3 = MOVIE
- m4 = MEDITATION
"""

import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Add project paths
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


def create_2x2_panel(condition_code, condition_name, input_dir, output_dir):
    """
    Create a 2x2 panel from 4 individual PEB matrix heatmaps.

    Parameters
    ----------
    condition_code : str
        Condition code (m1, m2, m3, m4)
    condition_name : str
        Full condition name (REST, MUSIC, MOVIE, MEDITATION)
    input_dir : Path
        Directory containing individual matrix PNG files
    output_dir : Path
        Output directory for combined panels
    """

    print(f"\n{'='*70}")
    print(f"{condition_code.upper()}: {condition_name}")
    print(f"{'='*70}")

    # Define the 4 required PNG files
    files_to_combine = {
        'pre': input_dir / f"{condition_code}-a_matrix_pre.png",
        'post': input_dir / f"{condition_code}-a_matrix_post.png",
        'change': input_dir / f"{condition_code}-a_matrix_change.png",
        'behavioral': input_dir / f"{condition_code}-b_matrix.png"
    }

    # Check if all files exist
    missing_files = []
    existing_files = {}

    for key, file_path in files_to_combine.items():
        if file_path.exists():
            existing_files[key] = file_path
            print(f"  ✓ Found: {file_path.name}")
        else:
            missing_files.append(file_path)
            print(f"  ✗ Missing: {file_path.name}")

    # Create combined figure only if we have all 4 files
    if len(existing_files) == 4:
        print(f"  → Creating 2x2 panel...")

        try:
            # Create 2x2 subplot grid
            fig, axes = plt.subplots(2, 2, figsize=(16, 16))

            # Minimize spacing between subplots
            plt.subplots_adjust(left=0.01, right=0.99, top=0.97, bottom=0.01,
                              wspace=0.03, hspace=0.03)

            # Load and display each image in the correct position
            panel_config = [
                ('pre', (0, 0), 'A) Pre-Psilocybin'),
                ('post', (0, 1), 'B) Post-Psilocybin'),
                ('change', (1, 0), 'C) Change'),
                ('behavioral', (1, 1), 'D) Behavioral (11D-ASC)')
            ]

            for key, pos, label in panel_config:
                img = mpimg.imread(str(existing_files[key]))
                axes[pos].imshow(img)
                axes[pos].axis('off')
                # Panel labels removed per user request

            # Add overall title
            fig.suptitle(f"{condition_name} - PEB Matrix Analysis",
                        fontsize=18, fontweight='bold', y=0.995)

            # Save the combined figure
            output_file_svg = output_dir / f"{condition_code}_peb_panel_2x2.svg"
            output_file_png = output_dir / f"{condition_code}_peb_panel_2x2.png"
            output_file_pdf = output_dir / f"{condition_code}_peb_panel_2x2.pdf"

            fig.savefig(str(output_file_svg), bbox_inches='tight', pad_inches=0.05)
            fig.savefig(str(output_file_png), dpi=300, bbox_inches='tight', pad_inches=0.05)
            fig.savefig(str(output_file_pdf), bbox_inches='tight', pad_inches=0.05)
            plt.close(fig)

            print(f"  ✓ Saved: {output_file_svg.name}")
            print(f"  ✓ Saved: {output_file_png.name}")
            print(f"  ✓ Saved: {output_file_pdf.name}")
            return True

        except Exception as e:
            print(f"  ✗ Error creating panel: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    else:
        print(f"  ⚠ Only {len(existing_files)}/4 files found - skipping panel")
        return False


def generate_all_panels():
    """Generate 2x2 PEB matrix panels for all conditions."""

    print("=" * 70)
    print("PEB MATRIX 2x2 PANEL GENERATION")
    print("=" * 70)

    # Setup paths
    input_dir = project_root / "figures" / "peb_matrices"
    output_dir = project_root / "figures" / "peb_matrices" / "panels"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nInput directory: {input_dir}")
    print(f"Output directory: {output_dir}")

    # Define conditions
    conditions = {
        'm1': 'REST',
        'm2': 'MUSIC',
        'm3': 'MOVIE',
        'm4': 'MEDITATION'
    }

    # Generate panels for each condition
    stats = {'generated': 0, 'missing': 0}

    for code, name in conditions.items():
        success = create_2x2_panel(code, name, input_dir, output_dir)
        if success:
            stats['generated'] += 1
        else:
            stats['missing'] += 1

    # Summary
    print(f"\n{'='*70}")
    print("GENERATION COMPLETE!")
    print(f"{'='*70}")
    print(f"\nStatistics:")
    print(f"  ✓ Generated: {stats['generated']}")
    print(f"  ⚠ Missing: {stats['missing']}")
    print(f"\nAll 2x2 panels saved to: {output_dir}")

    # List generated files
    generated_files = sorted(output_dir.glob("*_peb_panel_2x2.*"))
    if generated_files:
        print(f"\nGenerated {len(generated_files)} panel files:")
        for f in generated_files:
            print(f"  - {f.name}")

    return stats


if __name__ == '__main__':
    generate_all_panels()
