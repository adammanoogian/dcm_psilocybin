#!/usr/bin/env python3
"""Check what AAL atlas values correspond to which labels."""
from nilearn.datasets import fetch_atlas_aal
import nibabel as nib
import numpy as np
import warnings
warnings.filterwarnings('ignore')

aal = fetch_atlas_aal()

print("AAL Atlas Structure:")
print(f"  Labels: {len(aal.labels)} region names")
print(f"  Indices (values in atlas): {len(aal.indices)} values")
print()

# Check if indices match labels
print("First 10 labels and their indices:")
for i in range(10):
    print(f"  {i}: Label='{aal.labels[i]}', Index value in atlas={aal.indices[i]}")

print()

# Check the regions we care about
regions = ['Frontal_Mid_L', 'Frontal_Mid_R', 'Hippocampus_L', 'Hippocampus_R',
           'Temporal_Mid_L', 'Temporal_Mid_R', 'Thalamus_L', 'Thalamus_R']

print("Our regions:")
for name in regions:
    idx = aal.labels.index(name)
    atlas_value = aal.indices[idx]
    print(f"  {name}: list index={idx}, atlas value={atlas_value}")

print()

# Load the actual atlas image
atlas_img = nib.load(aal.maps)
atlas_data = atlas_img.get_fdata()
affine = atlas_img.affine

print(f"Atlas shape: {atlas_data.shape}")
print(f"Affine matrix:")
print(affine)
print()

# Compute center of mass for specific regions ourselves
from scipy.ndimage import center_of_mass

print("Computing centers of mass ourselves:")
for name in regions:
    idx = aal.labels.index(name)
    atlas_value = aal.indices[idx]

    # Find voxels with this value
    mask = atlas_data == atlas_value
    n_voxels = np.sum(mask)

    # Compute center of mass in voxel coordinates
    com_voxel = center_of_mass(mask.astype(float))

    # Convert to MNI coordinates using affine
    com_mni = nib.affines.apply_affine(affine, com_voxel)

    print(f"  {name}:")
    print(f"    Atlas value: {atlas_value}")
    print(f"    Voxels: {n_voxels}")
    print(f"    CoM (voxel): {[f'{x:.1f}' for x in com_voxel]}")
    print(f"    CoM (MNI): X={com_mni[0]:.1f}, Y={com_mni[1]:.1f}, Z={com_mni[2]:.1f}")
    print()
