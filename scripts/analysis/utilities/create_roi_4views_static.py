#!/usr/bin/env python3
"""
Create 4 Static Brain ROI Views

Generates 4 static images showing brain regions of interest from different angles:
1. Left lateral view
2. Dorsal (top-down) view
3. Right lateral view
4. Posterior view

Output:
- 4 separate PNG files for each view
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

# Setup paths
project_root = Path(__file__).parent.parent.parent
output_dir = project_root / "figures" / "images"
output_dir.mkdir(parents=True, exist_ok=True)

print("="*70)
print("CREATING 4 STATIC BRAIN ROI VIEWS")
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

# Create custom colormap for our ROIs
from matplotlib.colors import ListedColormap
roi_colors = ['black'] + [roi_info['color_rgb'] for roi_info in roi_config.values()]
roi_cmap = ListedColormap(roi_colors)

# ============================================================================
# Step 2: Create 4 Static Views
# ============================================================================
print("\n[2/2] Creating 4 static view images...")

# Define the 4 views
views = [
    {
        'name': 'Left Lateral',
        'filename': 'roi_view_left_lateral.png',
        'display_mode': 'x',
        'cut_coords': [-40],
        'title': 'Left Lateral View'
    },
    {
        'name': 'Dorsal (Top-Down)',
        'filename': 'roi_view_dorsal.png',
        'display_mode': 'z',
        'cut_coords': [50],
        'title': 'Dorsal View'
    },
    {
        'name': 'Right Lateral',
        'filename': 'roi_view_right_lateral.png',
        'display_mode': 'x',
        'cut_coords': [40],
        'title': 'Right Lateral View'
    },
    {
        'name': 'Posterior',
        'filename': 'roi_view_posterior.png',
        'display_mode': 'y',
        'cut_coords': [-60],
        'title': 'Posterior View'
    }
]

# Generate each view
for view in views:
    print(f"  Creating {view['name']}...")

    # Create figure with legend
    fig = plt.figure(figsize=(10, 8))

    # Main brain view
    ax_brain = plt.subplot(1, 1, 1)

    plotting.plot_roi(
        combined_roi_img,
        title=view['title'],
        axes=ax_brain,
        display_mode=view['display_mode'],
        cut_coords=view['cut_coords'],
        cmap=roi_cmap,
        alpha=0.9,
        annotate=True,
        vmin=0,
        vmax=5
    )

    # Add legend in top-right corner
    legend_elements = []
    for roi_name, roi_info in roi_config.items():
        from matplotlib.patches import Patch
        legend_elements.append(
            Patch(facecolor=roi_info['color_rgb'],
                  edgecolor='black',
                  label=roi_info['display_name'])
        )

    ax_brain.legend(handles=legend_elements,
                    loc='upper right',
                    fontsize=11,
                    frameon=True,
                    fancybox=True,
                    shadow=True,
                    title='Brain Regions',
                    title_fontsize=12)

    # Save
    output_path = output_dir / view['filename']
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

    print(f"    [OK] Saved: {view['filename']}")

# ============================================================================
# Complete
# ============================================================================
print("\n" + "="*70)
print("4 STATIC BRAIN ROI VIEWS CREATED SUCCESSFULLY!")
print("="*70)

print(f"\nFiles saved to: {output_dir}")
print("\nGenerated files:")
for i, view in enumerate(views, 1):
    print(f"  {i}. {view['filename']} - {view['name']}")

print("\nFeatures:")
print("  - High resolution (300 DPI)")
print("  - Color legend on each image")
print("  - Consistent colors across all views")
print("  - Ready for PowerPoint or publications")

print("\nUsage:")
print("  - Insert any/all views into presentations")
print("  - Use side-by-side in papers")
print("  - Show multiple angles of ROI locations")
