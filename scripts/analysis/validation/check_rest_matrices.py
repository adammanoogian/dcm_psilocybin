#!/usr/bin/env python3
"""Check REST PEB matrices for correct constraint usage."""

import sys
from pathlib import Path

# Add project paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'scripts' / 'visualization'))

from scripts.visualization.plot_PEB_results import PEBDataLoader

# Setup paths
data_dir = project_root / 'massive_output_local' / 'adam_m6'

# Check REST behavioral (constrained)
print('='*70)
print('CHECKING REST BEHAVIORAL (CONSTRAINED)')
print('='*70)
behav_file = data_dir / 'PEB_behav_associations_-ses-02_-task-rest_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat'
print(f'File: {behav_file.name}')
print(f'Exists: {behav_file.exists()}')
print()

params = PEBDataLoader.get_peb_plot_parameters()
params['pp_threshold'] = 0.99
loader = PEBDataLoader(str(behav_file), params)
peb_data = loader.get_data()

print(f'Model type: {peb_data.get("model_type", "unknown")}')
print(f'PEB type: {peb_data.get("peb_type", "unknown")}')
print()

model = peb_data.get('model') or peb_data.get('bma')
if model:
    Pnames = model.get('Pnames', [])
    print(f'Number of parameters: {len(Pnames)}')
    print(f'First 10 parameters:')
    for i, pname in enumerate(Pnames[:10]):
        print(f'  {i+1}. {pname}')
    print()

    # Check if it's truly constrained
    n_rois = len(peb_data['roi_names'])
    expected_full = n_rois * n_rois
    print(f'Number of ROIs: {n_rois}')
    print(f'Expected full A matrix size: {expected_full}')
    print(f'Actual parameters: {len(Pnames)}')
    print(f'Is constrained: {len(Pnames) < expected_full}')
    print()

# Check REST change
print('='*70)
print('CHECKING REST CHANGE')
print('='*70)
change_file = data_dir / 'PEB_change_-ses-01-ses-02_-task-rest_cov-_noFD.mat'
print(f'File: {change_file.name}')
print(f'Exists: {change_file.exists()}')
print()

loader2 = PEBDataLoader(str(change_file), params)
peb_data2 = loader2.get_data()

print(f'Model type: {peb_data2.get("model_type", "unknown")}')
print(f'PEB type: {peb_data2.get("peb_type", "unknown")}')
print()

model2 = peb_data2.get('model') or peb_data2.get('bma')
if model2:
    Pnames2 = model2.get('Pnames', [])
    print(f'Number of parameters: {len(Pnames2)}')
    print(f'First 10 parameters:')
    for i, pname in enumerate(Pnames2[:10]):
        print(f'  {i+1}. {pname}')
    print()

    n_rois2 = len(peb_data2['roi_names'])
    expected_full2 = n_rois2 * n_rois2
    print(f'Number of ROIs: {n_rois2}')
    print(f'Expected full A matrix size: {expected_full2}')
    print(f'Actual parameters: {len(Pnames2)}')
    print(f'Is constrained: {len(Pnames2) < expected_full2}')
