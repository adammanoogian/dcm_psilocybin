#!/usr/bin/env python3
"""Debug AAL atlas data type issues."""
from nilearn.datasets import fetch_atlas_aal
import nibabel as nib
import numpy as np
from scipy.ndimage import center_of_mass
import warnings
warnings.filterwarnings('ignore')

aal = fetch_atlas_aal()
atlas_img = nib.load(aal.maps)
atlas_data = atlas_img.get_fdata()
affine = atlas_img.affine

print(f"Atlas data type: {atlas_data.dtype}")
unique_vals = np.unique(atlas_data)
print(f"Unique values in atlas: {len(unique_vals)}")
print(f"Sample values: {unique_vals[7:13]}")  # Around Frontal_Mid indices
print()

# Check if 2201 (Frontal_Mid_L code) is in the atlas
frontal_mid_l_code = aal.indices[aal.labels.index('Frontal_Mid_L')]
print(f"Frontal_Mid_L AAL code: {frontal_mid_l_code} (type: {type(frontal_mid_l_code)})")

# Convert to int if it's a string
frontal_mid_l_int = int(frontal_mid_l_code)
print(f"As integer: {frontal_mid_l_int}")
print(f"Is {frontal_mid_l_int} in unique values? {frontal_mid_l_int in unique_vals}")
print(f"Is {float(frontal_mid_l_int)} in unique values? {float(frontal_mid_l_int) in unique_vals}")

# Use integer comparison
atlas_int = atlas_data.astype(int)
mask = atlas_int == frontal_mid_l_int
print(f"Voxels with value {frontal_mid_l_code} (as int): {np.sum(mask)}")

print()
print("Computing coordinates with integer comparison:")

regions = ['Frontal_Mid_L', 'Frontal_Mid_R', 'Hippocampus_L', 'Hippocampus_R',
           'Occipital_Sup_L', 'Occipital_Sup_R', 'Temporal_Mid_L', 'Temporal_Mid_R',
           'Thalamus_L', 'Thalamus_R']

correct_coords = {}

for name in regions:
    label_idx = aal.labels.index(name)
    aal_code = float(aal.indices[label_idx])  # Convert string to float

    mask = atlas_data == aal_code
    n_voxels = np.sum(mask)

    if n_voxels > 0:
        com_voxel = center_of_mass(mask.astype(float))
        com_mni = nib.affines.apply_affine(affine, com_voxel)
        correct_coords[name] = com_mni
        print(f"{name}:")
        print(f"  MNI: X={com_mni[0]:.1f}, Y={com_mni[1]:.1f}, Z={com_mni[2]:.1f}")
    else:
        print(f"{name}: NOT FOUND")

print()
print("="*70)
print("SYMMETRY CHECK:")
print("="*70)

pairs = [
    ('Frontal_Mid_L', 'Frontal_Mid_R'),
    ('Hippocampus_L', 'Hippocampus_R'),
    ('Occipital_Sup_L', 'Occipital_Sup_R'),
    ('Temporal_Mid_L', 'Temporal_Mid_R'),
    ('Thalamus_L', 'Thalamus_R'),
]

for left_name, right_name in pairs:
    if left_name in correct_coords and right_name in correct_coords:
        lc = correct_coords[left_name]
        rc = correct_coords[right_name]
        y_diff = abs(lc[1] - rc[1])
        z_diff = abs(lc[2] - rc[2])
        print(f"{left_name}:  X={lc[0]:7.1f}, Y={lc[1]:7.1f}, Z={lc[2]:7.1f}")
        print(f"{right_name}: X={rc[0]:7.1f}, Y={rc[1]:7.1f}, Z={rc[2]:7.1f}")
        print(f"  Y-diff: {y_diff:.1f}mm, Z-diff: {z_diff:.1f}mm")
        print()
