#!/usr/bin/env python3
"""Verify dotted box positions match values after transpose."""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print("="*70)
print("VERIFYING BOX POSITIONS VS VALUES")
print("="*70)

# Simulate a constrained model
# Parameter "A(3,1)" means FROM region 1 TO region 3 in MATLAB convention
# In matrix: Ep[3,1] = FROM 1 TO 3

# Create 5x5 matrix with some estimated connections
Ep = np.zeros((5, 5))
# Parameter A(3,1): FROM 1 TO 3
Ep[3, 1] = 0.5
# Parameter A(1,2): FROM 2 TO 1
Ep[1, 2] = 0.3
# Parameter A(4,0): FROM 0 TO 4
Ep[4, 0] = 0.7

print("\nOriginal Ep (MATLAB convention)")
print("Ep[target, source] = FROM source TO target")
print(Ep)

# These are the positions that were estimated (row, col)
estimated_positions = [(3, 1), (1, 2), (4, 0)]
print(f"\nEstimated positions (row, col): {estimated_positions}")
print("  [3,1]: FROM region 1 TO region 3")
print("  [1,2]: FROM region 2 TO region 1")
print("  [4,0]: FROM region 0 TO region 4")

# Transpose for plotting (what the code does)
Ep_T = Ep.T
print("\nAfter transpose Ep.T:")
print(Ep_T)

# Create figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# LEFT: Original with boxes at (col, row)
sns.heatmap(Ep_T, annot=True, fmt='.2f', cmap='viridis',
            vmin=0, vmax=1, ax=ax1, cbar=False)
ax1.set_title('Boxes at (col, row) - ORIGINAL CODE')
for row, col in estimated_positions:
    rect = plt.Rectangle((col, row), 1, 1, fill=False, edgecolor='red',
                         linestyle='--', linewidth=3)
    ax1.add_patch(rect)

# RIGHT: With boxes at (row, col)
sns.heatmap(Ep_T, annot=True, fmt='.2f', cmap='viridis',
            vmin=0, vmax=1, ax=ax2, cbar=False)
ax2.set_title('Boxes at (row, col) - MY FIX')
for row, col in estimated_positions:
    rect = plt.Rectangle((row, col), 1, 1, fill=False, edgecolor='red',
                         linestyle='--', linewidth=3)
    ax2.add_patch(rect)

plt.tight_layout()
plt.savefig('C:/Users/aman0087/Documents/Github/dcm_psilocybin/box_position_test.png',
            dpi=150, bbox_inches='tight')
print("\nSaved visualization to: box_position_test.png")

# Determine which is correct
print("\n" + "="*70)
print("ANALYSIS:")
print("="*70)
print("\nFor connection A(3,1) = FROM region 1 TO region 3:")
print(f"  Original matrix: Ep[3,1] = {Ep[3,1]}")
print(f"  After transpose: Ep.T[1,3] = {Ep_T[1,3]}")
print(f"  Seaborn plots Ep.T[1,3] at visual position (x=3, y=1)")
print(f"  So box should be at (x=3, y=1) = (col=3, row=1)")
print(f"  Original code: (col, row) = (1, 3) ❌ WRONG")
print(f"  My fix: (row, col) = (3, 1) ❌ ALSO WRONG!")
print(f"  CORRECT: Should actually stay at (col, row) but SWAP the tuple!")
print(f"           We need (estimated_col, estimated_row) which = (col, row)")

print("\nWAIT - Let me recalculate...")
print("\nIf estimated_positions = (row, col) from Ep:")
print(f"  (row=3, col=1) means Ep[3,1]")
print(f"  After transpose: Ep.T[col, row] = Ep.T[1,3]")
print(f"  Seaborn plots Ep.T[i,j] at (x=j, y=i)")
print(f"  So Ep.T[1,3] plots at (x=3, y=1)")
print(f"  Box should be at plt.Rectangle((x=3, y=1))")
print(f"  So we need (3, 1) = (col, row) ✓ ORIGINAL WAS CORRECT!")

print("\n" + "="*70)
print("CONCLUSION: I need to REVERT my fix!")
print("="*70)
