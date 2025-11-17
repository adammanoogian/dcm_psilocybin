#!/usr/bin/env python3
"""
Automated Figure Generation Pipeline for Paper

Reads hypothesis configuration and generates all DCM connectivity visualizations.
Integrates with the paper's hypothesis structure to ensure figures match analysis goals.

Usage (from project root):
    python scripts/analysis/generate_paper_figures.py --config scripts/analysis/config/hypothesis_config.yaml
    python scripts/analysis/generate_paper_figures.py --config scripts/analysis/config/hypothesis_config.yaml --hypothesis H1
    python scripts/analysis/generate_paper_figures.py --config scripts/analysis/config/hypothesis_config.yaml --dry-run
"""

import argparse
import yaml
import os
import sys
from pathlib import Path
from datetime import datetime
import subprocess
import json


def load_config(config_path):
    """Load hypothesis configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def get_mat_file_path(config, mat_file):
    """Construct full path to .mat file."""
    data_dir = config['project']['data_dir']
    return os.path.join(data_dir, mat_file)


def build_visualization_command(config, hypothesis, verbose=False):
    """Build the command-line call to plot_nilearn_connectivity.py"""

    defaults = config.get('defaults', {})
    viz = hypothesis['visualization']
    output_dir = config['project']['output_dir']

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Full paths
    mat_file = get_mat_file_path(config, hypothesis['mat_file'])
    output_file = os.path.join(output_dir, viz['output'])

    # Build command - use relative path from project root
    cmd = ['python', 'scripts/visualization/plot_nilearn_connectivity.py']

    # Required arguments
    cmd.extend(['--mat-files', mat_file])
    cmd.extend(['--conditions', hypothesis['name']])
    cmd.extend(['--output', output_file])

    # Source regions
    if viz.get('source_regions'):
        cmd.append('--source-regions')
        cmd.extend(viz['source_regions'])

    # Target regions
    if viz.get('target_regions'):
        cmd.append('--target-regions')
        cmd.extend(viz['target_regions'])

    # Connection type
    if viz.get('connection_type'):
        cmd.extend(['--connection-type', viz['connection_type']])

    # Thresholds
    pp_threshold = viz.get('pp_threshold', defaults.get('pp_threshold', 0.99))
    cmd.extend(['--pp-threshold', str(pp_threshold)])

    strength_threshold = viz.get('strength_threshold', defaults.get('strength_threshold', 0.0))
    cmd.extend(['--strength-threshold', str(strength_threshold)])

    edge_threshold = viz.get('edge_threshold', defaults.get('edge_threshold', '90%'))
    cmd.extend(['--edge-threshold', str(edge_threshold)])

    # Visual parameters
    node_size = viz.get('node_size', defaults.get('node_size', 50))
    cmd.extend(['--node-size', str(node_size)])

    edge_cmap = viz.get('edge_cmap', 'coolwarm')
    cmd.extend(['--edge-cmap', edge_cmap])

    display_mode = viz.get('display_mode', 'lyrz')
    cmd.extend(['--display-mode', display_mode])

    # Title
    if viz.get('title'):
        cmd.extend(['--title', viz['title']])

    # Colorbar label - describe what the values represent
    colorbar_label = viz.get('colorbar_label', defaults.get('colorbar_label', 'Connection Strength (Ep)'))
    cmd.extend(['--colorbar-label', colorbar_label])

    # Subtitle (optional custom subtitle)
    if viz.get('subtitle'):
        cmd.extend(['--subtitle', viz['subtitle']])

    # Colorbar
    if viz.get('colorbar', defaults.get('colorbar', True)):
        cmd.append('--colorbar')
    else:
        cmd.append('--no-colorbar')

    return cmd


def validate_hypothesis(config, hypothesis):
    """Validate that hypothesis configuration is complete."""
    errors = []

    # Check required fields
    required = ['id', 'name', 'mat_file', 'visualization']
    for field in required:
        if field not in hypothesis:
            errors.append(f"Missing required field: {field}")

    # Check mat file exists
    mat_file = get_mat_file_path(config, hypothesis['mat_file'])
    if not os.path.exists(mat_file):
        errors.append(f"MAT file not found: {mat_file}")

    # Check visualization has output
    if 'visualization' in hypothesis:
        if 'output' not in hypothesis['visualization']:
            errors.append("Visualization missing 'output' field")

    return errors


def generate_figure(config, hypothesis, dry_run=False, verbose=False):
    """Generate a single figure from hypothesis configuration."""

    hyp_id = hypothesis['id']
    hyp_name = hypothesis['name']

    print(f"\n{'='*60}")
    print(f"Hypothesis {hyp_id}: {hyp_name}")
    print(f"{'='*60}")

    # Validate
    errors = validate_hypothesis(config, hypothesis)
    if errors:
        print(f"  ERRORS:")
        for error in errors:
            print(f"    - {error}")
        return False

    # Build command
    cmd = build_visualization_command(config, hypothesis, verbose)

    if verbose or dry_run:
        print(f"\n  Command:")
        print(f"    {' '.join(cmd)}")

    if dry_run:
        print(f"\n  [DRY RUN] Would generate: {hypothesis['visualization']['output']}")
        return True

    # Execute
    print(f"\n  Generating: {hypothesis['visualization']['output']}")
    try:
        # Set cwd to project root (two directories up from this script)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=project_root
        )

        if result.returncode != 0:
            print(f"  ERROR: Command failed")
            print(f"  STDERR: {result.stderr}")
            if verbose:
                print(f"  STDOUT: {result.stdout}")
            return False

        # Check output file created
        output_path = os.path.join(
            config['project']['output_dir'],
            hypothesis['visualization']['output']
        )
        if os.path.exists(output_path):
            size_kb = os.path.getsize(output_path) / 1024
            print(f"  SUCCESS: Generated {output_path} ({size_kb:.1f} KB)")
            return True
        else:
            print(f"  WARNING: Command succeeded but output file not found")
            return False

    except Exception as e:
        print(f"  ERROR: {str(e)}")
        return False


def generate_latex_includes(config, successful_hypotheses):
    """Generate LaTeX code for including figures in paper."""

    lines = []
    lines.append("% Auto-generated figure includes from hypothesis_config.yaml")
    lines.append(f"% Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    for hyp_id in successful_hypotheses:
        # Find hypothesis in config
        hyp = next((h for h in config['hypotheses'] if h['id'] == hyp_id), None)
        if not hyp:
            continue

        viz = hyp['visualization']
        output_file = viz['output']
        title = viz.get('title', hyp['name'])
        section = hyp.get('paper_section', '')

        # Remove extension for LaTeX
        figure_name = os.path.splitext(output_file)[0]

        lines.append(f"% {hyp_id}: {hyp['name']}")
        lines.append(f"% Paper Section: {section}")
        lines.append("\\begin{figure}[htbp]")
        lines.append("  \\centering")
        lines.append(f"  \\includegraphics[width=\\textwidth]{{figures/{output_file}}}")
        lines.append(f"  \\caption{{{title}. {hyp['description'].strip()}}}")
        lines.append(f"  \\label{{fig:{figure_name}}}")
        lines.append("\\end{figure}")
        lines.append("")

    return "\n".join(lines)


def generate_summary_report(config, results):
    """Generate a summary report of figure generation."""

    report = []
    report.append("=" * 70)
    report.append("FIGURE GENERATION SUMMARY")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 70)

    successful = [h for h, success in results.items() if success]
    failed = [h for h, success in results.items() if not success]

    report.append(f"\nTotal hypotheses: {len(results)}")
    report.append(f"Successful: {len(successful)}")
    report.append(f"Failed: {len(failed)}")

    if successful:
        report.append(f"\n{'SUCCESS':^70}")
        report.append("-" * 70)
        for hyp_id in successful:
            hyp = next((h for h in config['hypotheses'] if h['id'] == hyp_id), None)
            if hyp:
                output = hyp['visualization']['output']
                report.append(f"  {hyp_id}: {output}")

    if failed:
        report.append(f"\n{'FAILED':^70}")
        report.append("-" * 70)
        for hyp_id in failed:
            hyp = next((h for h in config['hypotheses'] if h['id'] == hyp_id), None)
            if hyp:
                output = hyp['visualization']['output']
                report.append(f"  {hyp_id}: {output}")

    # List output files
    output_dir = config['project']['output_dir']
    if os.path.exists(output_dir):
        files = sorted(os.listdir(output_dir))
        pdf_files = [f for f in files if f.endswith('.pdf')]
        png_files = [f for f in files if f.endswith('.png')]

        report.append(f"\n{'OUTPUT FILES':^70}")
        report.append("-" * 70)
        report.append(f"  Directory: {output_dir}")
        report.append(f"  PDF files: {len(pdf_files)}")
        report.append(f"  PNG files: {len(png_files)}")

        total_size = sum(os.path.getsize(os.path.join(output_dir, f)) for f in files)
        report.append(f"  Total size: {total_size / (1024*1024):.2f} MB")

    report.append("\n" + "=" * 70)

    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(
        description="Generate paper figures from hypothesis configuration"
    )
    parser.add_argument(
        '--config',
        type=str,
        default='paper/hypothesis_config.yaml',
        help='Path to hypothesis configuration YAML file'
    )
    parser.add_argument(
        '--hypothesis',
        type=str,
        nargs='+',
        help='Generate only specific hypotheses (e.g., H1 H2). Default: all'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show commands without executing'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed output'
    )
    parser.add_argument(
        '--generate-latex',
        action='store_true',
        help='Generate LaTeX include file for paper'
    )
    parser.add_argument(
        '--summary-only',
        action='store_true',
        help='Only show summary of what would be generated'
    )

    args = parser.parse_args()

    # Load configuration
    if not os.path.exists(args.config):
        print(f"ERROR: Config file not found: {args.config}")
        sys.exit(1)

    config = load_config(args.config)
    print(f"\nLoaded configuration: {config['project']['name']}")
    print(f"Paper title: {config['project']['paper_title']}")

    # Determine which hypotheses to process
    all_hypotheses = config.get('hypotheses', [])

    if args.hypothesis:
        # Filter to requested hypotheses
        hypotheses = [h for h in all_hypotheses if h['id'] in args.hypothesis]
        missing = set(args.hypothesis) - set(h['id'] for h in hypotheses)
        if missing:
            print(f"\nWARNING: Hypotheses not found: {missing}")
    else:
        hypotheses = all_hypotheses

    print(f"\nHypotheses to process: {len(hypotheses)}")
    for hyp in hypotheses:
        print(f"  - {hyp['id']}: {hyp['name']}")

    if args.summary_only:
        print("\n[SUMMARY MODE - No files will be generated]")
        for hyp in hypotheses:
            errors = validate_hypothesis(config, hyp)
            status = "READY" if not errors else "INVALID"
            print(f"\n  {hyp['id']} ({status})")
            if errors:
                for err in errors:
                    print(f"    - {err}")
            else:
                print(f"    Output: {hyp['visualization']['output']}")
        return

    # Generate figures
    results = {}
    for hyp in hypotheses:
        success = generate_figure(config, hyp, dry_run=args.dry_run, verbose=args.verbose)
        results[hyp['id']] = success

    # Summary
    print("\n" + generate_summary_report(config, results))

    # Generate LaTeX includes if requested
    if args.generate_latex and not args.dry_run:
        successful = [h for h, s in results.items() if s]
        latex_code = generate_latex_includes(config, successful)

        latex_file = os.path.join(config['project']['output_dir'], 'figure_includes.tex')
        with open(latex_file, 'w') as f:
            f.write(latex_code)
        print(f"\nGenerated LaTeX includes: {latex_file}")

    # Exit code
    failed_count = sum(1 for s in results.values() if not s)
    if failed_count > 0:
        print(f"\nWARNING: {failed_count} hypothesis/hypotheses failed")
        sys.exit(1)
    else:
        print(f"\nAll figures generated successfully!")
        sys.exit(0)


if __name__ == '__main__':
    main()
