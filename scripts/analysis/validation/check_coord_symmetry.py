#!/usr/bin/env python3
"""Check if AAL coordinates are symmetric for L/R pairs."""
from nilearn.datasets import fetch_atlas_aal
from nilearn.plotting import find_parcellation_cut_coords
import warnings
warnings.filterwarnings('ignore')

aal = fetch_atlas_aal()
all_coords = find_parcellation_cut_coords(aal.maps)

print('Comparing LEFT vs RIGHT region coordinates:')
print('Expected: Same Y and Z, opposite X sign')
print()

pairs = [
    ('Frontal_Mid_L', 'Frontal_Mid_R'),
    ('Hippocampus_L', 'Hippocampus_R'),
    ('Occipital_Sup_L', 'Occipital_Sup_R'),
    ('Temporal_Mid_L', 'Temporal_Mid_R'),
    ('Thalamus_L', 'Thalamus_R'),
]

for left_name, right_name in pairs:
    left_idx = aal.labels.index(left_name)
    right_idx = aal.labels.index(right_name)
    left_coord = all_coords[left_idx]
    right_coord = all_coords[right_idx]

    # Check for symmetry
    y_diff = abs(left_coord[1] - right_coord[1])
    z_diff = abs(left_coord[2] - right_coord[2])

    print(f'{left_name}:')
    print(f'  Raw: X={left_coord[0]:7.1f}, Y={left_coord[1]:7.1f}, Z={left_coord[2]:7.1f}')
    print(f'{right_name}:')
    print(f'  Raw: X={right_coord[0]:7.1f}, Y={right_coord[1]:7.1f}, Z={right_coord[2]:7.1f}')
    print(f'  Y-diff: {y_diff:.1f}, Z-diff: {z_diff:.1f}')
    if y_diff > 10 or z_diff > 10:
        print('  WARNING: Large asymmetry in Y or Z!')
    print()
