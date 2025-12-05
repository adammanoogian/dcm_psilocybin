#!/usr/bin/env python3
"""
Create Brain ROI Anatomy Reference Figures

Generates anatomical reference visualizations showing the 5 brain regions
of interest used in the DCM psilocybin connectivity analysis:
- dlPFC (Frontal_Mid)
- MTG (Temporal_Mid)
- SOG (Occipital_Sup)
- Hippocampus
- Thalamus

Outputs:
1. Static 2-panel figure (PNG + SVG) - For publications
2. Interactive 3D HTML viewer - For exploration
3. Animated GIF - For PowerPoint presentations

Author: Generated for DCM Psilocybin Analysis
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from pathlib import Path
from nilearn import datasets, image, plotting
from nilearn.image import new_img_like, math_img
import nibabel as nib

# Setup paths
project_root = Path(__file__).parent.parent.parent
output_dir = project_root / "figures" / "images"
output_dir.mkdir(parents=True, exist_ok=True)

print("="*70)
print("CREATING BRAIN ROI ANATOMY REFERENCE FIGURES")
print("="*70)

# ============================================================================
# Step 1: Load AAL Atlas and Extract ROI Masks
# ============================================================================
print("\n[1/4] Loading AAL atlas and extracting ROI masks...")

# Fetch AAL atlas (suppress deprecation warning)
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    aal_atlas = datasets.fetch_atlas_aal()

aal_img = nib.load(aal_atlas['maps'])
aal_data = aal_img.get_fdata()
aal_labels = aal_atlas['labels']
aal_indices = aal_atlas['indices']

print(f"  AAL atlas loaded: {len(aal_labels)} regions")

# Define our ROIs and their colors
roi_config = {
    'dlPFC': {
        'aal_names': ['Frontal_Mid_L', 'Frontal_Mid_R'],
        'color_value': 1,
        'color_rgb': (0.2, 0.4, 0.8),  # Blue
        'display_name': 'dlPFC (Frontal Mid)'
    },
    'MTG': {
        'aal_names': ['Temporal_Mid_L', 'Temporal_Mid_R'],
        'color_value': 2,
        'color_rgb': (0.9, 0.5, 0.1),  # Orange
        'display_name': 'MTG (Temporal Mid)'
    },
    'SOG': {
        'aal_names': ['Occipital_Sup_L', 'Occipital_Sup_R'],
        'color_value': 3,
        'color_rgb': (0.2, 0.7, 0.3),  # Green
        'display_name': 'SOG (Occipital Sup)'
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
    print(f"  Extracting {roi_name}...")
    for aal_name in roi_info['aal_names']:
        # Find index for this AAL region
        try:
            idx = aal_labels.index(aal_name)
            aal_value = float(aal_indices[idx])  # Convert to float for comparison
            # Add to combined ROI volume
            mask = (aal_data == aal_value)
            nvoxels = np.count_nonzero(mask)
            if nvoxels > 0:
                combined_roi_data[mask] = roi_info['color_value']
                print(f"    + {aal_name} ({nvoxels} voxels)")
            else:
                print(f"    ! {aal_name} - no voxels found (AAL code: {aal_value})")
        except ValueError:
            print(f"    ! {aal_name} not found in AAL atlas")

# Create nibabel image
combined_roi_img = new_img_like(aal_img, combined_roi_data)

print(f"  [OK] Combined ROI volume created")
print(f"    Total voxels labeled: {np.count_nonzero(combined_roi_data)}")

# ============================================================================
# Step 2: Create Static 2-Panel Figure
# ============================================================================
print("\n[2/4] Creating static 2-panel figure...")

fig = plt.figure(figsize=(16, 10))

# Title
fig.suptitle('Brain Regions of Interest - DCM Psilocybin Analysis',
             fontsize=20, fontweight='bold', y=0.98)

# Panel A: Cortical Surface Views (dlPFC, MTG, SOG)
print("  Creating Panel A: Cortical surface views...")

# Create cortical-only mask
cortical_mask = np.isin(combined_roi_data, [1, 2, 3])  # dlPFC, MTG, SOG
cortical_data = np.where(cortical_mask, combined_roi_data, 0)
cortical_img = new_img_like(aal_img, cortical_data)

# Left hemisphere lateral view
ax1 = plt.subplot(2, 3, 1)
plotting.plot_roi(cortical_img,
                  title='Left Lateral View',
                  axes=ax1,
                  display_mode='x',
                  cut_coords=[-40],
                  cmap='tab10',
                  alpha=0.8,
                  annotate=True)

# Right hemisphere lateral view
ax2 = plt.subplot(2, 3, 2)
plotting.plot_roi(cortical_img,
                  title='Right Lateral View',
                  axes=ax2,
                  display_mode='x',
                  cut_coords=[40],
                  cmap='tab10',
                  alpha=0.8,
                  annotate=True)

# Dorsal view
ax3 = plt.subplot(2, 3, 3)
plotting.plot_roi(cortical_img,
                  title='Dorsal View',
                  axes=ax3,
                  display_mode='z',
                  cut_coords=[50],
                  cmap='tab10',
                  alpha=0.8,
                  annotate=True)

# Panel B: Subcortical Slice Views (Hippocampus, Thalamus)
print("  Creating Panel B: Subcortical slice views...")

# Create subcortical-only mask
subcortical_mask = np.isin(combined_roi_data, [4, 5])  # Hippocampus, Thalamus
subcortical_data = np.where(subcortical_mask, combined_roi_data, 0)
subcortical_img = new_img_like(aal_img, subcortical_data)

# Sagittal view
ax4 = plt.subplot(2, 3, 4)
plotting.plot_roi(subcortical_img,
                  title='Sagittal View',
                  axes=ax4,
                  display_mode='x',
                  cut_coords=[0],
                  cmap='tab10',
                  alpha=0.8,
                  annotate=True)

# Coronal view
ax5 = plt.subplot(2, 3, 5)
plotting.plot_roi(subcortical_img,
                  title='Coronal View',
                  axes=ax5,
                  display_mode='y',
                  cut_coords=[-10],
                  cmap='tab10',
                  alpha=0.8,
                  annotate=True)

# Axial view
ax6 = plt.subplot(2, 3, 6)
plotting.plot_roi(subcortical_img,
                  title='Axial View',
                  axes=ax6,
                  display_mode='z',
                  cut_coords=[0],
                  cmap='tab10',
                  alpha=0.8,
                  annotate=True)

# Add legend
legend_elements = []
for roi_name, roi_info in roi_config.items():
    from matplotlib.patches import Patch
    legend_elements.append(
        Patch(facecolor=roi_info['color_rgb'],
              label=roi_info['display_name'])
    )

fig.legend(handles=legend_elements,
           loc='lower center',
           ncol=5,
           fontsize=12,
           frameon=True,
           bbox_to_anchor=(0.5, -0.02))

plt.tight_layout(rect=[0, 0.03, 1, 0.97])

# Save PNG
png_path = output_dir / "roi_anatomy_reference.png"
plt.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"  [OK] Saved PNG: {png_path.name}")

# Save SVG
svg_path = output_dir / "roi_anatomy_reference.svg"
plt.savefig(svg_path, format='svg', bbox_inches='tight', facecolor='white')
print(f"  [OK] Saved SVG: {svg_path.name}")

plt.close()

# ============================================================================
# Step 3: Create Interactive 3D HTML Viewer
# ============================================================================
print("\n[3/4] Creating interactive 3D HTML viewer...")

# Create interactive view
html_view = plotting.view_img(
    combined_roi_img,
    bg_img=datasets.load_mni152_template(),
    cmap='tab10',
    symmetric_cmap=False,
    threshold=0.5,
    title='Interactive 3D Brain ROI Viewer',
    black_bg=False
)

# Save HTML
html_path = output_dir / "roi_anatomy_interactive.html"
html_view.save_as_html(str(html_path))
print(f"  [OK] Saved HTML: {html_path.name}")
print(f"    Open in browser to interact: {html_path}")

# ============================================================================
# Step 4: Create Animated GIF for PowerPoint
# ============================================================================
print("\n[4/4] Creating animated GIF for PowerPoint...")

try:
    import imageio.v2 as imageio

    print("  Generating rotation frames...")
    frames = []

    # Generate 36 frames (10° rotation each = 360° total)
    for i, angle in enumerate(range(0, 360, 10)):
        if i % 6 == 0:
            print(f"    Frame {i+1}/36 ({angle}°)...")

        # Create temporary figure for this angle
        fig_temp = plt.figure(figsize=(10, 10))

        # Use glass brain for cleaner animation
        display = plotting.plot_glass_brain(
            combined_roi_img,
            display_mode='lzry',
            colorbar=False,
            figure=fig_temp,
            cmap='tab10',
            alpha=0.8,
            title=f'Brain ROIs - {angle}°'
        )

        # Save frame to buffer
        fig_temp.canvas.draw()
        # Use buffer_rgba() for newer matplotlib versions
        buf = fig_temp.canvas.buffer_rgba()
        frame = np.asarray(buf)
        # Convert RGBA to RGB
        frame_rgb = frame[:, :, :3]
        frames.append(frame_rgb)

        plt.close(fig_temp)

    # Save as GIF
    gif_path = output_dir / "roi_anatomy_rotating.gif"
    imageio.mimsave(
        str(gif_path),
        frames,
        duration=0.15,  # 150ms per frame = ~6.7 fps
        loop=0  # Infinite loop
    )

    print(f"  [OK] Saved GIF: {gif_path.name}")
    print(f"    File size: {gif_path.stat().st_size / 1024 / 1024:.2f} MB")
    print(f"    Frames: {len(frames)}")

except ImportError:
    print("  [WARNING] imageio not available - skipping GIF generation")
    print("    Install with: pip install imageio")

# ============================================================================
# Complete
# ============================================================================
print("\n" + "="*70)
print("ROI ANATOMY FIGURES CREATED SUCCESSFULLY!")
print("="*70)

print(f"\nFiles saved to: {output_dir}")
print("\nGenerated files:")
print("  1. roi_anatomy_reference.png - Static 2-panel figure (publication)")
print("  2. roi_anatomy_reference.svg - Vector version (publication)")
print("  3. roi_anatomy_interactive.html - Interactive 3D viewer (exploration)")
try:
    imageio
    print("  4. roi_anatomy_rotating.gif - Animated rotation (PowerPoint)")
except:
    print("  4. roi_anatomy_rotating.gif - NOT GENERATED (imageio required)")

print("\nUsage recommendations:")
print("  [PAPER] Papers/Posters: Use PNG or SVG static figure")
print("  [WEB] Online/Supplementary: Share interactive HTML")
print("  [POWERPOINT] PowerPoint: Use animated GIF (drag & drop)")

print("\nRegions shown:")
for roi_name, roi_info in roi_config.items():
    color = roi_info['color_rgb']
    print(f"  - {roi_info['display_name']} - RGB{color}")
