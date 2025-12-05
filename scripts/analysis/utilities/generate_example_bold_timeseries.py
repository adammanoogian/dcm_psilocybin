#!/usr/bin/env python3
"""
Generate example BOLD time series figure for supplementary materials.

Creates simulated BOLD signals for the 5 left hemisphere regions used in the DCM analysis.
Time series are stacked vertically with distinct colors for each region.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


def generate_bold_signal(duration=600, tr=2.0, seed=None):
    """
    Generate a realistic simulated BOLD time series.

    Parameters
    ----------
    duration : float
        Total duration in seconds (default: 600s = 10 minutes)
    tr : float
        Repetition time in seconds (default: 2.0s)
    seed : int, optional
        Random seed for reproducibility

    Returns
    -------
    t : ndarray
        Time points in seconds
    signal : ndarray
        Simulated BOLD signal
    """
    if seed is not None:
        np.random.seed(seed)

    # Create time axis
    n_timepoints = int(duration / tr)
    t = np.arange(n_timepoints) * tr

    # Initialize signal
    signal = np.zeros(n_timepoints)

    # Add slow drift (scanner drift)
    drift_freq = 0.01  # Hz
    drift_amplitude = 0.5
    signal += drift_amplitude * np.sin(2 * np.pi * drift_freq * t)

    # Add physiological noise (respiratory ~0.3 Hz, cardiac ~1.2 Hz)
    resp_freq = 0.25  # Hz
    resp_amplitude = 0.15
    signal += resp_amplitude * np.sin(2 * np.pi * resp_freq * t + np.random.rand() * 2 * np.pi)

    cardiac_freq = 1.0  # Hz
    cardiac_amplitude = 0.08
    signal += cardiac_amplitude * np.sin(2 * np.pi * cardiac_freq * t + np.random.rand() * 2 * np.pi)

    # Add spontaneous BOLD fluctuations (0.01-0.1 Hz)
    for freq in np.linspace(0.01, 0.1, 5):
        amplitude = np.random.uniform(0.1, 0.3)
        phase = np.random.rand() * 2 * np.pi
        signal += amplitude * np.sin(2 * np.pi * freq * t + phase)

    # Add white noise
    noise_level = 0.2
    signal += np.random.randn(n_timepoints) * noise_level

    # Add occasional "events" (simulated neural activity)
    n_events = np.random.randint(3, 8)
    for _ in range(n_events):
        event_time = np.random.randint(50, n_timepoints - 50)
        event_duration = np.random.randint(5, 15)
        event_amplitude = np.random.uniform(0.5, 1.5)

        # Create HRF-like response
        hrf_time = np.arange(event_duration)
        hrf = event_amplitude * (hrf_time ** 2) * np.exp(-hrf_time / 3)

        # Add to signal
        signal[event_time:event_time+event_duration] += hrf

    # Normalize to percent signal change
    signal = (signal / np.std(signal)) * 1.5  # Typical BOLD signal change is ~1-3%

    return t, signal


def plot_stacked_bold_timeseries(output_path, duration=600, tr=2.0):
    """
    Create a stacked plot of BOLD time series for 5 left hemisphere regions.

    Parameters
    ----------
    output_path : str or Path
        Path to save the figure
    duration : float
        Total duration in seconds
    tr : float
        Repetition time in seconds
    """
    # Define the 5 left hemisphere regions
    regions = [
        'Frontal_Mid_L',
        'Hippocampus_L',
        'Occipital_Sup_L',
        'Temporal_Mid_L',
        'Thalamus_L'
    ]

    # Define readable labels
    labels = [
        'Left Middle Frontal Gyrus (dlPFC)',
        'Left Hippocampus',
        'Left Superior Occipital',
        'Left Middle Temporal',
        'Left Thalamus'
    ]

    # Define distinct colors for each region (using a colorblind-friendly palette)
    colors = [
        '#E69F00',  # Orange - Frontal
        '#56B4E9',  # Sky Blue - Hippocampus
        '#009E73',  # Bluish Green - Occipital
        '#F0E442',  # Yellow - Temporal
        '#CC79A7'   # Reddish Purple - Thalamus
    ]

    # Create figure with subplots stacked vertically
    fig, axes = plt.subplots(5, 1, figsize=(12, 10), sharex=True)
    fig.subplots_adjust(hspace=0.3, top=0.95, bottom=0.08, left=0.12, right=0.97)

    # Add main title
    fig.suptitle('Example BOLD Time Series: Left Hemisphere Regions',
                 fontsize=16, fontweight='bold', y=0.98)

    # Generate and plot time series for each region
    for idx, (region, label, color, ax) in enumerate(zip(regions, labels, colors, axes)):
        # Generate signal with different seed for each region
        t, signal = generate_bold_signal(duration=duration, tr=tr, seed=idx)

        # Plot the time series
        ax.plot(t, signal, color=color, linewidth=1.5, alpha=0.9)

        # Styling
        ax.set_ylabel('Activation\n(% signal change)', fontsize=10, fontweight='bold')
        ax.set_title(label, fontsize=11, fontweight='bold', loc='left', pad=5)
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8, alpha=0.3)

        # Set y-axis limits for consistency
        ax.set_ylim(-4, 4)

        # Add background color for region identification
        ax.set_facecolor('#f8f8f8')

        # Style spines
        for spine in ax.spines.values():
            spine.set_linewidth(1.2)
            spine.set_edgecolor(color)

    # Set x-axis label only on bottom subplot
    axes[-1].set_xlabel('Time (seconds)', fontsize=12, fontweight='bold')
    axes[-1].set_xlim(0, duration)

    # Add minor gridlines for better readability
    for ax in axes:
        ax.minorticks_on()
        ax.grid(which='minor', alpha=0.1, linestyle=':', linewidth=0.5)

    # Save figure
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save as SVG (vector format for editing)
    plt.savefig(output_path, format='svg', dpi=300, bbox_inches='tight')
    print(f"\nFigure saved to: {output_path}")

    # Also save as high-res PNG for convenience
    png_path = output_path.with_suffix('.png')
    plt.savefig(png_path, format='png', dpi=300, bbox_inches='tight')
    print(f"PNG version saved to: {png_path}")

    plt.close()


def main():
    """Main function to generate the figure."""
    print("="*70)
    print("GENERATING EXAMPLE BOLD TIME SERIES FIGURE")
    print("="*70)

    # Setup output path
    output_dir = project_root / "figures" / "images"
    output_path = output_dir / "example_bold_timeseries_LH.svg"

    print(f"\nOutput directory: {output_dir}")
    print(f"Output file: {output_path.name}")

    # Generate figure
    print("\nGenerating simulated BOLD signals...")
    plot_stacked_bold_timeseries(output_path, duration=600, tr=2.0)

    print("\n" + "="*70)
    print("COMPLETE!")
    print("="*70)
    print("\nThe figure shows example BOLD time series for the 5 left hemisphere")
    print("regions used in the spectral DCM analysis:")
    print("  1. Left Middle Frontal Gyrus (dlPFC) - Orange")
    print("  2. Left Hippocampus - Sky Blue")
    print("  3. Left Superior Occipital - Bluish Green")
    print("  4. Left Middle Temporal - Yellow")
    print("  5. Left Thalamus - Reddish Purple")
    print("\nEach time series includes:")
    print("  • Slow scanner drift")
    print("  • Physiological noise (respiratory & cardiac)")
    print("  • Spontaneous BOLD fluctuations (0.01-0.1 Hz)")
    print("  • Random neural events with HRF-like responses")
    print("  • Measurement noise")


if __name__ == '__main__':
    main()
