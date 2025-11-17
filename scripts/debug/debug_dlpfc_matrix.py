#!/usr/bin/env python3
"""
Debug script to show exactly what matrix is being plotted for dlPFC outgoing connections.
"""
import sys
sys.path.insert(0, '.')
sys.path.insert(0, 'scripts/visualization')
from plot_PEB_results import PEBDataLoader
import numpy as np
import pandas as pd

# Load actual data
mat_file = 'massive_output_local/adam_m6/PEB_change_-ses-01-ses-02_-task-rest_cov-_noFD.mat'
loader = PEBDataLoader(mat_file)
data = loader.get_data()
roi_names = data['roi_names']

model = data.get('model') or data.get('bma')
Ep = np.array(model['Ep']).flatten()
Pp = np.array(model['Pp']).flatten()

# Apply Pp threshold
pp_threshold = 0.99
Ep[Pp < pp_threshold] = 0

# Reshape
n_rois = len(roi_names)
n_covariates = len(Ep) // (n_rois * n_rois)
print(f'ROIs: {roi_names}')
print(f'Covariates: {n_covariates}')

Ep_3d = Ep.reshape((n_rois, n_rois, n_covariates), order='F')
connectivity_matrix = Ep_3d[:, :, 0]  # First covariate

print("\n" + "="*70)
print("ORIGINAL CONNECTIVITY MATRIX (MATLAB convention: M[i,j] = FROM j TO i)")
print("="*70)
df = pd.DataFrame(connectivity_matrix, index=roi_names, columns=roi_names)
print(df.round(4))

# Apply strength threshold (0.05)
strength_threshold = 0.05
connectivity_matrix[np.abs(connectivity_matrix) < strength_threshold] = 0

print(f"\n\nAfter strength threshold (|value| >= {strength_threshold}):")
df = pd.DataFrame(connectivity_matrix, index=roi_names, columns=roi_names)
print(df.round(4))

# Filter for outgoing from dlPFC
source_regions = ['Frontal_Mid_L', 'Frontal_Mid_R']
source_indices = [i for i, name in enumerate(roi_names) if name in source_regions]

print(f"\n\nSource regions: {source_regions}")
print(f"Source indices: {source_indices}")

# Create filtered matrix (outgoing from dlPFC)
filtered = np.zeros_like(connectivity_matrix)
for src_idx in source_indices:
    for tgt_idx in range(n_rois):
        if src_idx != tgt_idx:
            # MATLAB convention: M[target, source] = FROM source TO target
            filtered[tgt_idx, src_idx] = connectivity_matrix[tgt_idx, src_idx]

print("\n" + "="*70)
print("FILTERED MATRIX (outgoing from dlPFC)")
print("MATLAB convention: rows=targets, cols=sources")
print("="*70)
df_filtered = pd.DataFrame(filtered, index=roi_names, columns=roi_names)
print(df_filtered.round(4))

# Now transpose for nilearn
transposed = filtered.T

print("\n" + "="*70)
print("TRANSPOSED MATRIX (for nilearn)")
print("Nilearn convention: rows=sources, cols=targets")
print("M[i,j] = FROM i TO j")
print("="*70)
df_transposed = pd.DataFrame(transposed, index=roi_names, columns=roi_names)
print(df_transposed.round(4))

# List non-zero connections
print("\n" + "="*70)
print("NON-ZERO CONNECTIONS (what should be plotted)")
print("="*70)
nonzero = np.argwhere(transposed != 0)
for idx in nonzero:
    src, tgt = idx
    val = transposed[src, tgt]
    print(f"  {roi_names[src]} → {roi_names[tgt]}: {val:.4f}")

print(f"\nTotal connections: {len(nonzero)}")
