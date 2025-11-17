#!/usr/bin/env python3
"""
Trace through the exact plotting flow to debug color mismatch.
"""
import sys
sys.path.insert(0, '.')
sys.path.insert(0, 'scripts/visualization')
from plot_PEB_results import PEBDataLoader
from plot_nilearn_connectivity import AALCoordinateMapper
import numpy as np
from matplotlib import cm

print("="*70)
print("STEP 1: Load PEB data")
print("="*70)
mat_file = 'massive_output_local/adam_m6/PEB_change_-ses-01-ses-02_-task-rest_cov-_noFD.mat'
loader = PEBDataLoader(mat_file)
data = loader.get_data()
roi_names = list(data['roi_names'])

print(f"ROI names from .mat file (ORDER MATTERS):")
for i, name in enumerate(roi_names):
    print(f"  Index {i}: {name}")

print("\n" + "="*70)
print("STEP 2: Get MNI coordinates for each ROI")
print("="*70)
coord_mapper = AALCoordinateMapper()
node_coords = coord_mapper.get_coordinates(roi_names)
for i, name in enumerate(roi_names):
    coord = node_coords[i]
    print(f"  {i}: {name} -> MNI {coord}")

print("\n" + "="*70)
print("STEP 3: Assign colors (tab10 colormap)")
print("="*70)
node_cmap = cm.get_cmap('tab10')
node_colors = [node_cmap(i % 10) for i in range(len(roi_names))]

print("Colors assigned to each ROI index:")
for i, name in enumerate(roi_names):
    rgba = node_colors[i]
    print(f"  Index {i}: {name} -> RGBA{tuple(round(x, 2) for x in rgba)}")

print("\n" + "="*70)
print("STEP 4: What nilearn receives")
print("="*70)
print("nilearn.plot_connectome receives:")
print(f"  - node_coords: {node_coords.shape} array")
print(f"  - node_color: list of {len(node_colors)} RGBA tuples")
print("")
print("The key assumption: nilearn plots node i at coords[i] with color colors[i]")
print("")
print("So if node_coords[0] = [-32.92, 44.46, 32.73] (Left dlPFC)")
print("And node_colors[0] = tab10(0) = Blue")
print("Then the node at LEFT dlPFC position should be BLUE")
print("")

print("="*70)
print("VERIFICATION: Check actual coordinates")
print("="*70)
print("Blue node (index 0, Frontal_Mid_L):")
print(f"  Expected at: x={node_coords[0, 0]:.1f} (LEFT side, negative x)")
print("")
print("Orange node (index 1, Frontal_Mid_R):")
print(f"  Expected at: x={node_coords[1, 0]:.1f} (RIGHT side, positive x)")
print("")
print("If left dlPFC shows BLUE and right dlPFC shows ORANGE, colors match.")
print("If not, the coordinates might be wrong or nilearn's ordering is different.")

print("\n" + "="*70)
print("STEP 5: Check coordinate mapper implementation")
print("="*70)
print("AAL atlas uses standard MNI space:")
print("  - Negative X = Left hemisphere")
print("  - Positive X = Right hemisphere")
print("")
print("Our coordinate mapping:")
for name in ['Frontal_Mid_L', 'Frontal_Mid_R']:
    idx = roi_names.index(name)
    coord = node_coords[idx]
    side = "LEFT (x<0)" if coord[0] < 0 else "RIGHT (x>0)"
    print(f"  {name}: x={coord[0]:.1f} -> {side}")
