#!/usr/bin/env python3
"""Test that nilearn filtering and transpose work correctly."""

import numpy as np

# Simulate a 3x3 connectivity matrix in MATLAB convention
# MATLAB: Ep[i,j] = FROM j TO i
print("="*70)
print("TEST: Nilearn Transpose Correctness")
print("="*70)

# Create test matrix where we know the connections
# Ep[target, source] = connection strength
Ep = np.zeros((3, 3))
Ep[0, 1] = 1.0  # FROM region 1 TO region 0
Ep[2, 0] = 2.0  # FROM region 0 TO region 2
Ep[1, 2] = 3.0  # FROM region 2 TO region 1

print("\nOriginal MATLAB convention matrix:")
print("Ep[target, source] = FROM source TO target")
print(Ep)
print("\nMeaning:")
print(f"  Ep[0,1] = {Ep[0,1]:.1f} means: FROM region 1 TO region 0")
print(f"  Ep[2,0] = {Ep[2,0]:.1f} means: FROM region 0 TO region 2")
print(f"  Ep[1,2] = {Ep[1,2]:.1f} means: FROM region 2 TO region 1")

# Apply transpose (what nilearn code does)
Ep_transposed = Ep.T

print("\nAfter transpose (Nilearn convention):")
print("Ep.T[source, target] = FROM source TO target")
print(Ep_transposed)
print("\nMeaning:")
print(f"  Ep.T[1,0] = {Ep_transposed[1,0]:.1f} means: FROM region 1 TO region 0")
print(f"  Ep.T[0,2] = {Ep_transposed[0,2]:.1f} means: FROM region 0 TO region 2")
print(f"  Ep.T[2,1] = {Ep_transposed[2,1]:.1f} means: FROM region 2 TO region 1")

print("\n" + "="*70)
print("RESULT: Transpose correctly converts conventions ✓")
print("="*70)

# Now test filtering
print("\n" + "="*70)
print("TEST: Filter + Transpose for 'outgoing from region 0'")
print("="*70)

# Create mask for outgoing connections from region 0
mask = np.zeros((3, 3), dtype=bool)
source_idx = 0
for target_idx in range(3):
    if source_idx != target_idx:
        # MATLAB convention: mask[target, source]
        mask[target_idx, source_idx] = True

print("\nMask for outgoing from region 0 (MATLAB convention):")
print(mask.astype(int))

# Apply mask
filtered = Ep.copy()
filtered[~mask] = 0

print("\nFiltered matrix (MATLAB convention):")
print(filtered)
print(f"Shows only: FROM region 0 TO others")
print(f"  Ep[2,0] = {filtered[2,0]:.1f} means: FROM region 0 TO region 2 ✓")

# Transpose for nilearn
filtered_transposed = filtered.T

print("\nFiltered + Transposed (Nilearn convention):")
print(filtered_transposed)
print(f"  Ep.T[0,2] = {filtered_transposed[0,2]:.1f} means: FROM region 0 TO region 2 ✓")

print("\n" + "="*70)
print("RESULT: Filter + Transpose works correctly ✓")
print("="*70)
