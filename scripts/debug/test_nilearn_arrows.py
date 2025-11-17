#!/usr/bin/env python3
"""
Test nilearn arrow direction convention.
Creates a simple 3-node graph with one directed connection.
"""
import numpy as np
import matplotlib.pyplot as plt
from nilearn import plotting

# 3 nodes in a line: A (left), B (center), C (right)
node_coords = np.array([
    [-50, 0, 0],  # Node 0 (A) - left
    [0, 0, 0],    # Node 1 (B) - center
    [50, 0, 0]    # Node 2 (C) - right
])

# Test 1: Matrix with single connection M[1,0] = 1
# If nilearn interprets M[i,j] = FROM i TO j:
#   M[1,0] = FROM node 1 (B) TO node 0 (A) → arrow points LEFT
# If nilearn interprets M[i,j] = FROM j TO i:
#   M[1,0] = FROM node 0 (A) TO node 1 (B) → arrow points RIGHT

matrix1 = np.zeros((3, 3))
matrix1[1, 0] = 1.0  # Single entry at [1, 0]

fig, axes = plt.subplots(2, 1, figsize=(12, 8))

plt.sca(axes[0])
display1 = plotting.plot_connectome(
    matrix1, node_coords,
    node_size=100,
    edge_cmap='RdBu_r',
    colorbar=False,
    title='Matrix[1,0]=1: If arrow points LEFT → M[i,j]=FROM i TO j\nIf arrow points RIGHT → M[i,j]=FROM j TO i',
    figure=fig,
    display_mode='x'
)

# Test 2: Transpose - M[0,1] = 1
matrix2 = matrix1.T

plt.sca(axes[1])
display2 = plotting.plot_connectome(
    matrix2, node_coords,
    node_size=100,
    edge_cmap='RdBu_r',
    colorbar=False,
    title='Transposed Matrix[0,1]=1: Should flip arrow direction',
    figure=fig,
    display_mode='x'
)

plt.tight_layout()
plt.savefig('figures/nilearn/test_arrow_direction.pdf')
plt.savefig('figures/nilearn/test_arrow_direction.png', dpi=150)
print("Saved test_arrow_direction.pdf and .png")
print("\nINTERPRETATION:")
print("- Top plot has M[1,0]=1 (row 1, column 0)")
print("- Bottom plot has M[0,1]=1 (row 0, column 1)")
print("- Compare arrow directions to determine nilearn's convention")
