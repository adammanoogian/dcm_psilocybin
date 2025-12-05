#!/usr/bin/env python3
"""Fix AAL coordinates by properly mapping labels to atlas values."""
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

# Get unique values in the atlas
unique_vals = np.unique(atlas_data)
print(f"Unique values in atlas: {len(unique_vals)}")
print(f"Min: {unique_vals.min()}, Max: {unique_vals.max()}")
print(f"First 20 values: {unique_vals[:20]}")
print()

# The atlas uses sequential integers starting from 0
# So label at index i corresponds to value i in the atlas (0=background)
print("Computing correct coordinates by atlas integer value:")
print()

regions = ['Frontal_Mid_L', 'Frontal_Mid_R', 'Hippocampus_L', 'Hippocampus_R',
           'Occipital_Sup_L', 'Occipital_Sup_R', 'Temporal_Mid_L', 'Temporal_Mid_R',
           'Thalamus_L', 'Thalamus_R']

correct_coords = {}

for name in regions:
    label_idx = aal.labels.index(name)
    # The atlas value is the label_idx itself (since labels include Background at 0)
    atlas_val = label_idx

    mask = atlas_data == atlas_val
    n_voxels = np.sum(mask)

    if n_voxels > 0:
        com_voxel = center_of_mass(mask.astype(float))
        com_mni = nib.affines.apply_affine(affine, com_voxel)
        correct_coords[name] = com_mni
        print(f"{name}:")
        print(f"  Label index: {label_idx}, Atlas value: {atlas_val}, Voxels: {n_voxels}")
        print(f"  MNI: X={com_mni[0]:.1f}, Y={com_mni[1]:.1f}, Z={com_mni[2]:.1f}")
    else:
        print(f"{name}: NOT FOUND at value {atlas_val}")
    print()

# Check symmetry with correct coordinates
print("="*70)
print("SYMMETRY CHECK with correct coordinates:")
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
        left_coord = correct_coords[left_name]
        right_coord = correct_coords[right_name]

        y_diff = abs(left_coord[1] - right_coord[1])
        z_diff = abs(left_coord[2] - right_coord[2])

        print(f"{left_name}:  X={left_coord[0]:7.1f}, Y={left_coord[1]:7.1f}, Z={left_coord[2]:7.1f}")
        print(f"{right_name}: X={right_coord[0]:7.1f}, Y={right_coord[1]:7.1f}, Z={right_coord[2]:7.1f}")
        print(f"  Y-diff: {y_diff:.1f}, Z-diff: {z_diff:.1f}")
        if y_diff > 5 or z_diff > 5:
            print("  WARNING: Still asymmetric!")
        else:
            print("  OK - Symmetric!")
        print()
