#!/usr/bin/env python3
"""
Create Color Key Reference Images

Generates visual reference cards for the color scales used in the
hypothesis-based nilearn connectivity panels.

Output:
- colorkey_session_change.png: Green-Purple scale for session change
- colorkey_behavioral.png: Viridis (Purple-Yellow) scale for behavioral associations
"""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from pathlib import Path

# Create output directory
output_dir = Path(__file__).parent.parent.parent / "figures" / "images"
output_dir.mkdir(parents=True, exist_ok=True)

# Define custom green-purple colormap (same as in visualization module)
GREEN_PURPLE_CMAP = LinearSegmentedColormap.from_list(
    'green_purple',
    [(0.2, 0.7, 0.2), (1, 1, 1), (0.6, 0.2, 0.8)],
    N=256
)

def create_colorkey(cmap, title, left_label, right_label, filename,
                    left_sublabel="", right_sublabel=""):
    """Create a horizontal colorbar reference image."""

    fig, ax = plt.subplots(figsize=(10, 2.5))

    # Create gradient
    gradient = np.linspace(0, 1, 256).reshape(1, 256)

    # Display the gradient
    ax.imshow(gradient, aspect='auto', cmap=cmap)
    ax.set_yticks([])
    ax.set_xticks([])

    # Remove spines
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Add title
    fig.suptitle(title, fontsize=18, fontweight='bold', y=0.75)

    # Add labels
    # Left label
    ax.text(-0.02, 0.5, left_label,
            transform=ax.transAxes,
            fontsize=14, fontweight='bold',
            ha='right', va='center')

    if left_sublabel:
        ax.text(-0.02, 0.2, left_sublabel,
                transform=ax.transAxes,
                fontsize=11, style='italic',
                ha='right', va='center', color='#555555')

    # Right label
    ax.text(1.02, 0.5, right_label,
            transform=ax.transAxes,
            fontsize=14, fontweight='bold',
            ha='left', va='center')

    if right_sublabel:
        ax.text(1.02, 0.2, right_sublabel,
                transform=ax.transAxes,
                fontsize=11, style='italic',
                ha='left', va='center', color='#555555')

    # Add arrow annotations
    arrow_props = dict(arrowstyle='->', lw=2, color='black')
    ax.annotate('', xy=(-0.05, 0.5), xytext=(-0.15, 0.5),
                xycoords='axes fraction',
                arrowprops=arrow_props)
    ax.annotate('', xy=(1.15, 0.5), xytext=(1.05, 0.5),
                xycoords='axes fraction',
                arrowprops=arrow_props)

    plt.tight_layout()

    # Save
    output_path = output_dir / filename
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ Created: {output_path}")

# ============================================================================
# 1. Session Change Color Key (Green-Purple)
# ============================================================================
print("\nCreating Session Change color key...")
create_colorkey(
    cmap=GREEN_PURPLE_CMAP,
    title="Session Change: Post-psilocybin - Pre-Psilocybin",
    left_label="Weakening",
    left_sublabel="(closer to zero)",
    right_label="Strengthening",
    right_sublabel="(further from zero)",
    filename="colorkey_session_change.png"
)

# ============================================================================
# 2. Behavioral Association Color Key (Viridis)
# ============================================================================
print("Creating Behavioral Association color key...")
create_colorkey(
    cmap='viridis',
    title="Behavioral Association: ASC Composite Sensory Correlation",
    left_label="Negative β",
    left_sublabel="(anti-hallucinogenic)",
    right_label="Positive β",
    right_sublabel="(pro-hallucinogenic)",
    filename="colorkey_behavioral.png"
)

print(f"\n{'='*70}")
print("COLOR KEY IMAGES CREATED SUCCESSFULLY")
print(f"{'='*70}")
print(f"\nSaved to: {output_dir}")
print("\nFiles generated:")
print("  1. colorkey_session_change.png")
print("  2. colorkey_behavioral.png")
print("\nUse these reference images in presentations or as figure legends!")
