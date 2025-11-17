#!/usr/bin/env python3
"""Check what AAL labels actually exist and what's being matched."""
from nilearn.datasets import fetch_atlas_aal
from nilearn.plotting import find_parcellation_cut_coords

print("Fetching AAL atlas...")
aal = fetch_atlas_aal()

print("\nAll AAL labels containing 'Frontal_Mid':")
for i, label in enumerate(aal.labels):
    if 'Frontal_Mid' in label:
        print(f"  Index {i}: {label}")

print("\nAll AAL labels containing 'Hippocampus':")
for i, label in enumerate(aal.labels):
    if 'Hippocampus' in label:
        print(f"  Index {i}: {label}")

print("\nAll AAL labels containing 'Thalamus':")
for i, label in enumerate(aal.labels):
    if 'Thalamus' in label:
        print(f"  Index {i}: {label}")

# Get coordinates
all_coords = find_parcellation_cut_coords(aal.maps)
print(f"\nTotal coordinates: {len(all_coords)}")

# Build mapping
coord_map = {}
for idx, label in enumerate(aal.labels):
    if idx < len(all_coords):
        coord_map[label] = all_coords[idx]

# Check what we're actually matching
roi_names = ['Frontal_Mid_L', 'Frontal_Mid_R', 'Hippocampus_L', 'Hippocampus_R', 'Thalamus_L', 'Thalamus_R']

print("\n" + "="*70)
print("MATCHING RESULTS:")
print("="*70)
for roi_name in roi_names:
    # Current matching logic
    if roi_name in coord_map:
        coord = coord_map[roi_name]
        print(f"{roi_name} -> EXACT MATCH: {coord}")
    else:
        for aal_label, aal_coord in coord_map.items():
            if roi_name.lower() in aal_label.lower() or aal_label.lower() in roi_name.lower():
                side = "LEFT" if aal_coord[0] < 0 else "RIGHT"
                print(f"{roi_name} -> PARTIAL MATCH: '{aal_label}' at {aal_coord} ({side} hemisphere)")
                break
