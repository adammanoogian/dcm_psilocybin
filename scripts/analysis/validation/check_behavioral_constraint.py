#!/usr/bin/env python3
"""Check if behavioral matrices are truly constrained."""

import sys
from pathlib import Path
import numpy as np

# Add project paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'scripts' / 'visualization'))

from scripts.visualization.plot_PEB_results import PEBDataLoader

# Setup paths
data_dir = project_root / 'massive_output_local' / 'adam_m6'

print('='*70)
print('CHECKING BEHAVIORAL CONSTRAINT INTEGRITY')
print('='*70)

# Load REST behavioral constrained
behav_file = data_dir / 'PEB_behav_associations_-ses-02_-task-rest_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat'
print(f'\nLoading: {behav_file.name}')

params = PEBDataLoader.get_peb_plot_parameters()
params['pp_threshold'] = 0.99
loader = PEBDataLoader(str(behav_file), params)
peb_data = loader.get_data()

# Get the model
model = peb_data.get('model') or peb_data.get('bma')
Pnames = model.get('Pnames', [])
Ep = np.array(model['Ep']).flatten()
Pp = np.array(model['Pp']).flatten()

print(f'\nModel has {len(Pnames)} parameters')
print(f'ROIs: {len(peb_data["roi_names"])}')
print(f'Expected full model: {len(peb_data["roi_names"])**2} parameters')

# Show which connections are in the model
print(f'\n{len(Pnames)} estimated connections:')
for i, pname in enumerate(Pnames[:20]):  # Show first 20
    print(f'  {i+1}. {pname}: Ep={Ep[i]:.4f}, Pp={Pp[i]:.4f}')
if len(Pnames) > 20:
    print(f'  ... and {len(Pnames)-20} more')

# Apply posterior probability threshold
Ep_thresh = Ep.copy()
Ep_thresh[Pp < params['pp_threshold']] = 0

# Count significant connections
n_significant = np.sum(Ep_thresh != 0)
print(f'\nAfter Pp>{params["pp_threshold"]} threshold:')
print(f'  Significant connections: {n_significant}/{len(Pnames)}')

# Parse parameter names to see which connections
print(f'\nSignificant connections (Pp>{params["pp_threshold"]}):')
for i, pname in enumerate(Pnames):
    if Ep_thresh[i] != 0:
        print(f'  {pname}: Ep={Ep_thresh[i]:.4f}')

# Now check if these match what's in the reshaped matrix
print('\n' + '='*70)
print('CHECKING RESHAPED MATRIX')
print('='*70)

# The reshape should only have values where connections were estimated
roi_names = peb_data['roi_names']
n_rois = len(roi_names)

# Get the reshaped 3D matrix
from scripts.visualization.plot_PEB_results import PEBDataLoader
full_data = loader.get_data()

# Check if we have the Ep_3d from data
if 'Ep_3d' in full_data:
    Ep_3d = full_data['Ep_3d']
    print(f'Ep_3d shape: {Ep_3d.shape}')

    # For first covariate
    Ep_cov0 = Ep_3d[:, :, 0]

    print(f'\nNon-zero connections in reshaped matrix (covariate 0):')
    non_zero = np.where(Ep_cov0 != 0)
    print(f'  Total non-zero: {len(non_zero[0])}')

    for i, j in zip(non_zero[0][:20], non_zero[1][:20]):
        print(f'  [{i},{j}] ({roi_names[j]} → {roi_names[i]}): {Ep_cov0[i,j]:.4f}')

    if len(non_zero[0]) > 20:
        print(f'  ... and {len(non_zero[0])-20} more')

    # Check if number matches
    print(f'\nValidation:')
    print(f'  Parameters in model: {len(Pnames)}')
    print(f'  Significant after threshold: {n_significant}')
    print(f'  Non-zero in matrix: {len(non_zero[0])}')

    if len(non_zero[0]) > len(Pnames):
        print('\n⚠️  WARNING: Matrix has MORE non-zero values than estimated parameters!')
        print('   This suggests the matrix is NOT properly constrained.')
    elif len(non_zero[0]) == len(Pnames):
        print('\n✓ Matrix has same number of non-zero values as parameters (OK)')
    else:
        print(f'\n✓ Matrix has fewer non-zero ({len(non_zero[0])}) than parameters ({len(Pnames)})')
        print('   This is expected after Pp thresholding')
