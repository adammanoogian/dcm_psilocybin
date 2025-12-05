#!/usr/bin/env python3
"""Check which covariate is displayed in behavioral PEB files."""

from pathlib import Path
from scipy.io import loadmat
import numpy as np

# Load REST behavioral file
data_dir = Path('massive_output_local/adam_m6')
behav_file = data_dir / 'PEB_behav_associations_-ses-02_-task-rest_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat'

print('='*70)
print('CHECKING BEHAVIORAL COVARIATE STRUCTURE')
print('='*70)

mat = loadmat(str(behav_file), squeeze_me=True, struct_as_record=False)
bma = mat['BMA']

# Get covariate names
if hasattr(bma, 'Xnames'):
    xnames = bma.Xnames
    print(f'\nCovariate names (Xnames):')
    if hasattr(xnames, '__iter__') and not isinstance(xnames, str):
        for i, name in enumerate(xnames):
            print(f'  Covariate {i}: {name}')
    else:
        print(f'  {xnames}')
else:
    print('\nNo Xnames found in BMA')

# Check parameter structure
ep = np.array(bma.Ep).flatten()
pnames = bma.Pnames
n_params = len(pnames)

print(f'\nParameter structure:')
print(f'  Total Ep length: {len(ep)}')
print(f'  Number of Pnames: {n_params}')
print(f'  Implied covariates: {len(ep) // n_params}')

print(f'\nConclusion:')
print(f'  - Behavioral PEB files have {len(ep) // n_params} covariates')
print(f'  - Covariate 0: Group mean/intercept')
print(f'  - Covariate 1: Behavioral association with 11D-ASC (THE ONE WE WANT!)')
print(f'\n  Currently saving: plotter.figures[0] = Covariate 0 (GROUP MEAN)')
print(f'  Should be saving: plotter.figures[1] = Covariate 1 (BEHAVIORAL ASSOCIATION)')
