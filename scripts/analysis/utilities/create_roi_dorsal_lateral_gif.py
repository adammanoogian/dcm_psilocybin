#!/usr/bin/env python3
"""
Create Dorsal and Lateral View ROI Animated GIF

Generates an animated GIF showing brain regions of interest from
dorsal (top-down) and lateral (side) views with a color legend.

Output:
- roi_anatomy_dorsal_lateral.gif - Animated views with legend (PowerPoint-ready)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from pathlib import Path
from nilearn import datasets, plotting
from nilearn.image import new_img_like
import nibabel as nib
from matplotlib.patches import Rectangle
import imageio.v2 as imageio

# Setup paths
project_root = Path(__file__).parent.parent.parent
output_dir = project_root / "figures" / "images"
output_dir.mkdir(parents=True, exist_ok=True)

print("="*70)
print("CREATING DORSAL/LATERAL VIEW ROI ANIMATED GIF")
print("="*70)

# ============================================================================
# Step 1: Load AAL Atlas and Extract ROI Masks
# ============================================================================
print("\n[1/2] Loading AAL atlas and extracting ROI masks...")

# Fetch AAL atlas (suppress deprecation warning)
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    aal_atlas = datasets.fetch_atlas_aal()

aal_img = nib.load(aal_atlas['maps'])
aal_data = aal_img.get_fdata()
aal_labels = aal_atlas['labels']
aal_indices = aal_atlas['indices']

# Define our ROIs and their colors (SAME AS BEFORE - consistency!)
roi_config = {
    'dlPFC': {
        'aal_names': ['Frontal_Mid_L', 'Frontal_Mid_R'],
        'color_value': 1,
        'color_rgb': (0.2, 0.4, 0.8),  # Blue
        'display_name': 'dlPFC'
    },
    'MTG': {
        'aal_names': ['Temporal_Mid_L', 'Temporal_Mid_R'],
        'color_value': 2,
        'color_rgb': (0.9, 0.5, 0.1),  # Orange
        'display_name': 'MTG'
    },
    'SOG': {
        'aal_names': ['Occipital_Sup_L', 'Occipital_Sup_R'],
        'color_value': 3,
        'color_rgb': (0.2, 0.7, 0.3),  # Green
        'display_name': 'SOG'
    },
    'Hippocampus': {
        'aal_names': ['Hippocampus_L', 'Hippocampus_R'],
        'color_value': 4,
        'color_rgb': (0.6, 0.2, 0.8),  # Purple
        'display_name': 'Hippocampus'
    },
    'Thalamus': {
        'aal_names': ['Thalamus_L', 'Thalamus_R'],
        'color_value': 5,
        'color_rgb': (0.9, 0.8, 0.1),  # Yellow
        'display_name': 'Thalamus'
    }
}

# Create combined ROI volume
combined_roi_data = np.zeros_like(aal_data)

for roi_name, roi_info in roi_config.items():
    for aal_name in roi_info['aal_names']:
        try:
            idx = aal_labels.index(aal_name)
            aal_value = float(aal_indices[idx])
            mask = (aal_data == aal_value)
            combined_roi_data[mask] = roi_info['color_value']
        except ValueError:
            pass

# Create nibabel image
combined_roi_img = new_img_like(aal_img, combined_roi_data)

print(f"  [OK] Combined ROI volume created")
print(f"    Total voxels labeled: {np.count_nonzero(combined_roi_data)}")

# ============================================================================
# Step 2: Create Animated GIF with Dorsal and Lateral Views + Legend
# ============================================================================
print("\n[2/2] Creating animated GIF with dorsal and lateral views...")

frames = []

# Create custom colormap for our ROIs
from matplotlib.colors import ListedColormap
roi_colors = ['black'] + [roi_info['color_rgb'] for roi_info in roi_config.values()]
roi_cmap = ListedColormap(roi_colors)

# Generate 36 frames for smooth rotation
print("  Generating frames...")
for i, angle in enumerate(range(0, 360, 10)):
    if i % 6 == 0:
        print(f"    Frame {i+1}/36 ({angle} degrees)...")

    # Create figure with 3 panels: dorsal, lateral, and legend
    fig = plt.figure(figsize=(16, 6))

    # Title
    fig.suptitle(f'Brain Regions of Interest - Rotation: {angle} degrees',
                 fontsize=18, fontweight='bold', y=0.98)

    # Panel 1: Dorsal view (top-down, z-axis)
    ax1 = plt.subplot(1, 3, 1)
    plotting.plot_roi(
        combined_roi_img,
        title='Dorsal View (Top-Down)',
        axes=ax1,
        display_mode='z',
        cut_coords=[50],
        cmap=roi_cmap,
        alpha=0.9,
        annotate=True,
        vmin=0,
        vmax=5
    )

    # Panel 2: Lateral view (side view, rotating)
    ax2 = plt.subplot(1, 3, 2)
    # Alternate between left and right lateral views based on rotation
    if angle < 180:
        cut_coord = -50 + (angle / 180.0) * 100  # -50 to +50
        view_title = f'Lateral View (Rotating: {angle} deg)'
    else:
        cut_coord = 50 - ((angle - 180) / 180.0) * 100  # +50 to -50
        view_title = f'Lateral View (Rotating: {angle} deg)'

    plotting.plot_roi(
        combined_roi_img,
        title=view_title,
        axes=ax2,
        display_mode='x',
        cut_coords=[cut_coord],
        cmap=roi_cmap,
        alpha=0.9,
        annotate=True,
        vmin=0,
        vmax=5
    )

    # Panel 3: Color Legend
    ax3 = plt.subplot(1, 3, 3)
    ax3.axis('off')
    ax3.set_xlim(0, 1)
    ax3.set_ylim(0, 1)

    # Title for legend
    ax3.text(0.5, 0.95, 'Region Color Key',
             ha='center', va='top', fontsize=16, fontweight='bold')

    # Add color boxes and labels
    y_start = 0.8
    y_step = 0.15

    for idx, (roi_name, roi_info) in enumerate(roi_config.items()):
        y_pos = y_start - (idx * y_step)

        # Color box
        color_box = Rectangle((0.1, y_pos - 0.05), 0.15, 0.08,
                               facecolor=roi_info['color_rgb'],
                               edgecolor='black',
                               linewidth=2)
        ax3.add_patch(color_box)

        # Label text
        ax3.text(0.3, y_pos, roi_info['display_name'],
                 ha='left', va='center', fontsize=14, fontweight='bold')

    # Add note at bottom
    ax3.text(0.5, 0.05,
             'All regions shown bilaterally\n(left and right hemispheres)',
             ha='center', va='bottom', fontsize=10, style='italic',
             color='gray')

    plt.tight_layout(rect=[0, 0.02, 1, 0.96])

    # Save frame to buffer
    fig.canvas.draw()
    buf = fig.canvas.buffer_rgba()
    frame = np.asarray(buf)
    frame_rgb = frame[:, :, :3]
    frames.append(frame_rgb)

    plt.close(fig)

# Save as GIF
gif_path = output_dir / "roi_anatomy_dorsal_lateral.gif"
print(f"\n  Saving animated GIF...")
imageio.mimsave(
    str(gif_path),
    frames,
    duration=0.15,  # 150ms per frame
    loop=0  # Infinite loop
)

print(f"  [OK] Saved GIF: {gif_path.name}")
print(f"    File size: {gif_path.stat().st_size / 1024 / 1024:.2f} MB")
print(f"    Frames: {len(frames)}")

# ============================================================================
# Complete
# ============================================================================
print("\n" + "="*70)
print("DORSAL/LATERAL VIEW GIF CREATED SUCCESSFULLY!")
print("="*70)

print(f"\nFile saved to: {output_dir}")
print(f"  - roi_anatomy_dorsal_lateral.gif")

print("\nFeatures:")
print("  [VIEW] Dorsal (top-down) view on left")
print("  [VIEW] Lateral (side) view with rotation in center")
print("  [LEGEND] Color key on right (consistent with other figures)")
print("  [SIZE] Optimized for PowerPoint presentations")

print("\nUsage:")
print("  1. Drag and drop into PowerPoint slide")
print("  2. GIF will auto-play showing all angles")
print("  3. Legend clearly identifies each region")
