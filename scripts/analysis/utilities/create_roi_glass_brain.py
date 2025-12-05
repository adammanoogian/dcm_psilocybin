#!/usr/bin/env python3
"""
Create Glass Brain View of ROIs

Generates transparent "glass brain" visualizations showing all brain regions
simultaneously from multiple angles.

Output:
- Glass brain static images (ortho, 4-panel, single views)
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
print("CREATING GLASS BRAIN VIEWS OF ROIs")
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
# Step 2: Create Glass Brain Views
# ============================================================================
print("\n[2/2] Creating glass brain visualizations...")

# View 1: Orthogonal glass brain (shows all 4 planes)
print("  Creating orthogonal glass brain view...")
fig1 = plt.figure(figsize=(12, 4), facecolor='#e8e8e8')
display1 = plotting.plot_glass_brain(
    combined_roi_img,
    display_mode='lzry',
    colorbar=False,
    figure=fig1,
    cmap='tab10',
    alpha=0.8,
    black_bg=False,
    title='Glass Brain View - All Planes',
    vmin=0,
    vmax=5
)

# Add legend
legend_elements = []
for roi_name, roi_info in roi_config.items():
    from matplotlib.patches import Patch
    legend_elements.append(
        Patch(facecolor=roi_info['color_rgb'],
              edgecolor='black',
              label=roi_info['display_name'])
    )

fig1.legend(handles=legend_elements,
            loc='upper right',
            fontsize=10,
            frameon=True,
            title='Regions',
            ncol=5,
            bbox_to_anchor=(0.98, 0.98))

output1_png = output_dir / "roi_glass_brain_ortho.png"
output1_svg = output_dir / "roi_glass_brain_ortho.svg"
plt.savefig(output1_png, dpi=300, bbox_inches='tight', facecolor='#e8e8e8')
plt.savefig(output1_svg, format='svg', bbox_inches='tight', facecolor='#e8e8e8')
plt.close()
print(f"    [OK] Saved: roi_glass_brain_ortho.png")
print(f"    [OK] Saved: roi_glass_brain_ortho.svg")

# View 2: Individual single views (4 separate images)
print("  Creating individual single-view images...")

# View 2a: Left Lateral
print("    Creating left lateral view...")
fig2a = plt.figure(figsize=(8, 8), facecolor='#e8e8e8')
plotting.plot_glass_brain(
    combined_roi_img,
    display_mode='x',
    colorbar=False,
    figure=fig2a,
    cmap='tab10',
    alpha=0.8,
    black_bg=False,
    title='Glass Brain - Left Lateral',
    vmin=0,
    vmax=5
)
fig2a.legend(handles=legend_elements,
            loc='upper right',
            fontsize=12,
            frameon=True,
            title='Brain Regions',
            title_fontsize=13)

output2a_png = output_dir / "roi_glass_brain_left_lateral.png"
output2a_svg = output_dir / "roi_glass_brain_left_lateral.svg"
plt.savefig(output2a_png, dpi=300, bbox_inches='tight', facecolor='#e8e8e8')
plt.savefig(output2a_svg, format='svg', bbox_inches='tight', facecolor='#e8e8e8')
plt.close()
print(f"    [OK] Saved: roi_glass_brain_left_lateral (PNG + SVG)")

# View 2b: Dorsal
print("    Creating dorsal view...")
fig2b = plt.figure(figsize=(8, 8), facecolor='#e8e8e8')
plotting.plot_glass_brain(
    combined_roi_img,
    display_mode='z',
    colorbar=False,
    figure=fig2b,
    cmap='tab10',
    alpha=0.8,
    black_bg=False,
    title='Glass Brain - Dorsal',
    vmin=0,
    vmax=5
)
fig2b.legend(handles=legend_elements,
            loc='upper right',
            fontsize=12,
            frameon=True,
            title='Brain Regions',
            title_fontsize=13)

output2b_png = output_dir / "roi_glass_brain_dorsal.png"
output2b_svg = output_dir / "roi_glass_brain_dorsal.svg"
plt.savefig(output2b_png, dpi=300, bbox_inches='tight', facecolor='#e8e8e8')
plt.savefig(output2b_svg, format='svg', bbox_inches='tight', facecolor='#e8e8e8')
plt.close()
print(f"    [OK] Saved: roi_glass_brain_dorsal (PNG + SVG)")

# View 2c: Right Lateral
print("    Creating right lateral view...")
fig2c = plt.figure(figsize=(8, 8), facecolor='#e8e8e8')
plotting.plot_glass_brain(
    combined_roi_img,
    display_mode='x',
    colorbar=False,
    figure=fig2c,
    cmap='tab10',
    alpha=0.8,
    black_bg=False,
    title='Glass Brain - Right Lateral',
    vmin=0,
    vmax=5
)
fig2c.legend(handles=legend_elements,
            loc='upper right',
            fontsize=12,
            frameon=True,
            title='Brain Regions',
            title_fontsize=13)

output2c_png = output_dir / "roi_glass_brain_right_lateral.png"
output2c_svg = output_dir / "roi_glass_brain_right_lateral.svg"
plt.savefig(output2c_png, dpi=300, bbox_inches='tight', facecolor='#e8e8e8')
plt.savefig(output2c_svg, format='svg', bbox_inches='tight', facecolor='#e8e8e8')
plt.close()
print(f"    [OK] Saved: roi_glass_brain_right_lateral (PNG + SVG)")

# View 2d: Posterior
print("    Creating posterior view...")
fig2d = plt.figure(figsize=(8, 8), facecolor='#e8e8e8')
plotting.plot_glass_brain(
    combined_roi_img,
    display_mode='y',
    colorbar=False,
    figure=fig2d,
    cmap='tab10',
    alpha=0.8,
    black_bg=False,
    title='Glass Brain - Posterior',
    vmin=0,
    vmax=5
)
fig2d.legend(handles=legend_elements,
            loc='upper right',
            fontsize=12,
            frameon=True,
            title='Brain Regions',
            title_fontsize=13)

output2d_png = output_dir / "roi_glass_brain_posterior.png"
output2d_svg = output_dir / "roi_glass_brain_posterior.svg"
plt.savefig(output2d_png, dpi=300, bbox_inches='tight', facecolor='#e8e8e8')
plt.savefig(output2d_svg, format='svg', bbox_inches='tight', facecolor='#e8e8e8')
plt.close()
print(f"    [OK] Saved: roi_glass_brain_posterior (PNG + SVG)")

# View 2e: 4-Panel Vertical (stacked)
print("  Creating 4-panel vertical view...")
fig2e = plt.figure(figsize=(8, 16), facecolor='#e8e8e8')
fig2e.suptitle('Glass Brain View - Multiple Angles (Vertical)', fontsize=16, fontweight='bold', y=0.995)

# Left lateral (top)
ax1 = plt.subplot(4, 1, 1)
plotting.plot_glass_brain(
    combined_roi_img,
    display_mode='x',
    colorbar=False,
    axes=ax1,
    cmap='tab10',
    alpha=0.8,
    black_bg=False,
    title='Left Lateral',
    vmin=0,
    vmax=5
)

# Dorsal
ax2 = plt.subplot(4, 1, 2)
plotting.plot_glass_brain(
    combined_roi_img,
    display_mode='z',
    colorbar=False,
    axes=ax2,
    cmap='tab10',
    alpha=0.8,
    black_bg=False,
    title='Dorsal',
    vmin=0,
    vmax=5
)

# Right lateral
ax3 = plt.subplot(4, 1, 3)
plotting.plot_glass_brain(
    combined_roi_img,
    display_mode='x',
    colorbar=False,
    axes=ax3,
    cmap='tab10',
    alpha=0.8,
    black_bg=False,
    title='Right Lateral',
    vmin=0,
    vmax=5
)

# Posterior (bottom)
ax4 = plt.subplot(4, 1, 4)
plotting.plot_glass_brain(
    combined_roi_img,
    display_mode='y',
    colorbar=False,
    axes=ax4,
    cmap='tab10',
    alpha=0.8,
    black_bg=False,
    title='Posterior',
    vmin=0,
    vmax=5
)

# Add legend
fig2e.legend(handles=legend_elements,
            loc='lower center',
            fontsize=11,
            frameon=True,
            ncol=5,
            bbox_to_anchor=(0.5, -0.01))

plt.tight_layout(rect=[0, 0.02, 1, 0.99])

output2e_png = output_dir / "roi_glass_brain_4panel_vertical.png"
output2e_svg = output_dir / "roi_glass_brain_4panel_vertical.svg"
plt.savefig(output2e_png, dpi=300, bbox_inches='tight', facecolor='#e8e8e8')
plt.savefig(output2e_svg, format='svg', bbox_inches='tight', facecolor='#e8e8e8')
plt.close()
print(f"    [OK] Saved: roi_glass_brain_4panel_vertical (PNG + SVG)")

# View 3: Single large glass brain (best overview)
print("  Creating single large glass brain view...")
fig3 = plt.figure(figsize=(10, 8), facecolor='#e8e8e8')
display3 = plotting.plot_glass_brain(
    combined_roi_img,
    display_mode='lyrz',
    colorbar=False,
    figure=fig3,
    cmap='tab10',
    alpha=0.8,
    black_bg=False,
    title='Glass Brain View - Comprehensive',
    vmin=0,
    vmax=5
)

# Add legend
fig3.legend(handles=legend_elements,
            loc='upper right',
            fontsize=12,
            frameon=True,
            title='Brain Regions',
            title_fontsize=13,
            shadow=True,
            fancybox=True)

output3_png = output_dir / "roi_glass_brain_single.png"
output3_svg = output_dir / "roi_glass_brain_single.svg"
plt.savefig(output3_png, dpi=300, bbox_inches='tight', facecolor='#e8e8e8')
plt.savefig(output3_svg, format='svg', bbox_inches='tight', facecolor='#e8e8e8')
plt.close()
print(f"    [OK] Saved: roi_glass_brain_single.png")
print(f"    [OK] Saved: roi_glass_brain_single.svg")

# ============================================================================
# Complete
# ============================================================================
print("\n" + "="*70)
print("GLASS BRAIN VIEWS CREATED SUCCESSFULLY!")
print("="*70)

print(f"\nFiles saved to: {output_dir}")
print("\nGenerated files (PNG + SVG):")
print("  1. roi_glass_brain_ortho - Orthogonal view (4 planes: lzry)")
print("  2. roi_glass_brain_left_lateral - Single view (left side)")
print("  3. roi_glass_brain_dorsal - Single view (top down)")
print("  4. roi_glass_brain_right_lateral - Single view (right side)")
print("  5. roi_glass_brain_posterior - Single view (back)")
print("  6. roi_glass_brain_4panel_vertical - 4 views stacked vertically")
print("  7. roi_glass_brain_single - Comprehensive view (lyrz)")

print("\nFeatures:")
print("  - Transparent 'see-through' brain visualization")
print("  - Visible brain anatomical outlines (dark on light background)")
print("  - All regions visible simultaneously")
print("  - High resolution PNG (300 DPI) + Vector SVG")
print("  - Color legend on each image")
print("  - Perfect for showing spatial relationships")

print("\nUsage:")
print("  - PowerPoint/Presentations: Use individual single views")
print("  - Papers/Publications: Use SVG for scalable vector graphics")
print("  - Posters: Use high-res PNG files")
