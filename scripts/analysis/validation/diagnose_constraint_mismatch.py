#!/usr/bin/env python3
"""Diagnose why values appear outside dotted boxes."""

import sys
from pathlib import Path
import numpy as np

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'scripts' / 'visualization'))

from scripts.visualization.plot_PEB_results import PEBDataLoader

data_dir = project_root / 'massive_output_local' / 'adam_m6'
behav_file = data_dir / 'PEB_behav_associations_-ses-02_-task-rest_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat'

print('='*70)
print('DIAGNOSING CONSTRAINT MISMATCH')
print('='*70)

params = PEBDataLoader.get_peb_plot_parameters()
params['pp_threshold'] = 0.99
loader = PEBDataLoader(str(behav_file), params)
peb_data = loader.get_data()

# Compute estimated_indices by calling reshape
model = peb_data.get('model') or peb_data.get('bma')
Pnames = model.get('Pnames', [])
roi_names = peb_data['roi_names']
roi_n = len(roi_names)

# Call reshape to get estimated_indices
result = PEBDataLoader.reshape_posterior_simple(model, roi_n)
if len(result) == 4:
    Ep_reshaped, Pp_reshaped, param_n, estimated_indices = result
    peb_data['estimated_indices'] = estimated_indices
    peb_data['Ep_3d'] = Ep_reshaped
else:
    Ep_reshaped, Pp_reshaped, param_n = result
    peb_data['estimated_indices'] = None
    peb_data['Ep_3d'] = Ep_reshaped

print(f'\nModel has {len(Pnames)} estimated parameters')
print(f'ROI names: {roi_names}')

# Parse Pnames to get which connections were estimated
print('\nEstimated connections from Pnames:')
estimated_from_pnames = []
for pname in Pnames:
    # Parse "A(i,j)" format
    parts = pname.replace('A(', '').replace(')', '').split(',')
    row = int(parts[0]) - 1  # Convert to 0-indexed
    col = int(parts[1]) - 1
    estimated_from_pnames.append((row, col))
    if len(estimated_from_pnames) <= 10:
        print(f'  {pname} -> ({row},{col}): {roi_names[col]} -> {roi_names[row]}')

if len(Pnames) > 10:
    print(f'  ... and {len(Pnames)-10} more')

# Get template_indices from the loader data
if 'estimated_indices' in peb_data and peb_data['estimated_indices'] is not None:
    template_indices = peb_data['estimated_indices']
    template_positions = list(zip(template_indices[0], template_indices[1]))
    print(f'\nTemplate indices (box positions): {len(template_positions)} positions')
    for i, (row, col) in enumerate(template_positions[:10]):
        print(f'  Box at ({row},{col}): {roi_names[col]} -> {roi_names[row]}')
    if len(template_positions) > 10:
        print(f'  ... and {len(template_positions)-10} more')
else:
    print('\nWARNING: No estimated_indices found in peb_data!')
    template_positions = []

# Get actual non-zero values from the reshaped matrix
Ep_cov0 = Ep_reshaped[:, :, 0]  # First covariate
nonzero = np.where(Ep_cov0 != 0)
actual_positions = list(zip(nonzero[0], nonzero[1]))
print(f'\nActual non-zero values in matrix: {len(actual_positions)} positions')
for i, (row, col) in enumerate(actual_positions[:10]):
    print(f'  Value at ({row},{col}): {roi_names[col]} -> {roi_names[row]} = {Ep_cov0[row,col]:.4f}')
if len(actual_positions) > 10:
    print(f'  ... and {len(actual_positions)-10} more')

# Compare sets
print('\n' + '='*70)
print('COMPARISON')
print('='*70)

estimated_set = set(estimated_from_pnames)
template_set = set(template_positions)
actual_set = set(actual_positions)

print(f'\nEstimated from Pnames: {len(estimated_set)} positions')
print(f'Template boxes: {len(template_set)} positions')
print(f'Actual values: {len(actual_set)} positions')

if estimated_set == template_set:
    print('\n✓ Template boxes match Pnames')
else:
    print('\n✗ MISMATCH: Template boxes DO NOT match Pnames!')
    in_pnames_not_template = estimated_set - template_set
    in_template_not_pnames = template_set - estimated_set
    if in_pnames_not_template:
        print(f'  In Pnames but not template: {len(in_pnames_not_template)}')
        for row, col in list(in_pnames_not_template)[:5]:
            print(f'    ({row},{col}): {roi_names[col]} -> {roi_names[row]}')
    if in_template_not_pnames:
        print(f'  In template but not Pnames: {len(in_template_not_pnames)}')
        for row, col in list(in_template_not_pnames)[:5]:
            print(f'    ({row},{col}): {roi_names[col]} -> {roi_names[row]}')

# Check if actual values are subset of template
values_outside_boxes = actual_set - template_set
if values_outside_boxes:
    print(f'\n✗ PROBLEM: {len(values_outside_boxes)} values OUTSIDE boxes!')
    print('  These connections have values but no boxes:')
    for row, col in list(values_outside_boxes)[:10]:
        print(f'    ({row},{col}): {roi_names[col]} -> {roi_names[row]} = {Ep_cov0[row,col]:.4f}')
else:
    print('\n✓ All values are inside boxes')
