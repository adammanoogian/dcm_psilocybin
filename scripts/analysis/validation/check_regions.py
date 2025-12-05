#!/usr/bin/env python3
"""Quick script to check which regions are in the DCM models."""

import sys
from pathlib import Path
from scipy.io import loadmat

# Add project paths
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Load a sample PEB file
data_dir = project_root / "massive_output_local" / "adam_m6"
mat_file = data_dir / "PEB_change_-ses-01-ses-02_-task-rest_cov-_noFD.mat"

if mat_file.exists():
    print(f"Loading: {mat_file.name}")
    mat = loadmat(str(mat_file), squeeze_me=True, struct_as_record=False)

    roi_names = mat.get('ROI_names', None)

    if roi_names is not None:
        print(f"\nTotal regions: {len(roi_names)}")
        print("\nAll ROI names:")
        for i, name in enumerate(roi_names):
            print(f"  {i+1}. {name}")

        # Filter for left hemisphere
        left_regions = [name for name in roi_names if name.endswith('_L')]
        print(f"\nLeft hemisphere regions ({len(left_regions)}):")
        for i, name in enumerate(left_regions):
            print(f"  {i+1}. {name}")
    else:
        print("ROI_names not found directly in mat file")
else:
    print(f"File not found: {mat_file}")
