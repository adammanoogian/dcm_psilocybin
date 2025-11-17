#!/usr/bin/env python3
"""Fix AAL coordinates using actual AAL codes."""
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

print("Computing coordinates using AAL codes (aal.indices):")
print()

regions = ['Frontal_Mid_L', 'Frontal_Mid_R', 'Hippocampus_L', 'Hippocampus_R',
           'Occipital_Sup_L', 'Occipital_Sup_R', 'Temporal_Mid_L', 'Temporal_Mid_R',
           'Thalamus_L', 'Thalamus_R']

correct_coords = {}

for name in regions:
    label_idx = aal.labels.index(name)
    aal_code = aal.indices[label_idx]  # Use the actual AAL code

    mask = atlas_data == aal_code
    n_voxels = np.sum(mask)

    if n_voxels > 0:
        com_voxel = center_of_mass(mask.astype(float))
        com_mni = nib.affines.apply_affine(affine, com_voxel)
        correct_coords[name] = com_mni
        print(f"{name}:")
        print(f"  AAL code: {aal_code}, Voxels: {n_voxels}")
        print(f"  MNI: X={com_mni[0]:.1f}, Y={com_mni[1]:.1f}, Z={com_mni[2]:.1f}")
    else:
        print(f"{name}: NOT FOUND with AAL code {aal_code}")
    print()

# Check symmetry
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
        left_coord = correct_coords[left_name]
        right_coord = correct_coords[right_name]

        y_diff = abs(left_coord[1] - right_coord[1])
        z_diff = abs(left_coord[2] - right_coord[2])

        print(f"{left_name}:  X={left_coord[0]:7.1f}, Y={left_coord[1]:7.1f}, Z={left_coord[2]:7.1f}")
        print(f"{right_name}: X={right_coord[0]:7.1f}, Y={right_coord[1]:7.1f}, Z={right_coord[2]:7.1f}")
        print(f"  Y-diff: {y_diff:.1f}mm, Z-diff: {z_diff:.1f}mm")
        if y_diff > 5 or z_diff > 5:
            print("  Asymmetric (normal for biological variation)")
        else:
            print("  Symmetric!")
        print()

# Compare with nilearn's find_parcellation_cut_coords
print("="*70)
print("COMPARISON: Our method vs nilearn's find_parcellation_cut_coords")
print("="*70)

from nilearn.plotting import find_parcellation_cut_coords
nilearn_coords = find_parcellation_cut_coords(aal.maps)

for name in regions:
    label_idx = aal.labels.index(name)
    nilearn_coord = nilearn_coords[label_idx]
    our_coord = correct_coords.get(name, [np.nan]*3)

    print(f"{name}:")
    print(f"  Nilearn: X={nilearn_coord[0]:7.1f}, Y={nilearn_coord[1]:7.1f}, Z={nilearn_coord[2]:7.1f}")
    print(f"  Ours:    X={our_coord[0]:7.1f}, Y={our_coord[1]:7.1f}, Z={our_coord[2]:7.1f}")

    if not np.isnan(our_coord[0]):
        diff = np.sqrt(np.sum((nilearn_coord - our_coord)**2))
        print(f"  Distance: {diff:.1f}mm")
    print()
