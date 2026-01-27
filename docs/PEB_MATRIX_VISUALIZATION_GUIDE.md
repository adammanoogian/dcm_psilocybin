# PEB Matrix Visualization Guide

Technical guide for the PEB (Parametric Empirical Bayes) matrix heatmap visualizations, including implementation details, MATLAB/Python interoperability, and axis conventions.

## Overview

The PEB matrix visualizations display effective connectivity results as 2D heatmaps. These are generated from SPM DCM analysis results stored in MATLAB `.mat` files.

**Key Script**: `scripts/visualization/plot_PEB_results.py`

---

## Matrix Conventions

### DCM/SPM Convention

In SPM's Dynamic Causal Modeling:

```
A(i,j) = connection FROM region j TO region i
```

- **Rows (i)** = Target regions (TO)
- **Columns (j)** = Source regions (FROM)

This is the standard SPM convention where `A(to, from)` represents the influence of the source on the target.

### Visualization Convention

For intuitive visualization, we transpose the matrix:

```python
# After transpose:
# - Rows = Sources (FROM)
# - Columns = Targets (TO)
matrix_for_display = raw_matrix.T
```

**Axis Labels** (after transpose):
- **Y-axis (rows)**: "From" - Source regions
- **X-axis (columns)**: "To" - Target regions

Reading the heatmap: A cell at position (row=i, col=j) shows the connection FROM region i TO region j.

---

## MATLAB/Python Interoperability

### Column-Major vs Row-Major Storage

**Critical Implementation Detail**: MATLAB stores matrices in column-major (Fortran) order, while NumPy defaults to row-major (C) order.

#### The Problem

PEB results contain vectorized connectivity parameters. For a 10x10 matrix (100 connections), MATLAB stores them linearly as:

```
MATLAB linear index: [A(1,1), A(2,1), A(3,1), ..., A(10,1), A(1,2), A(2,2), ...]
                     (column by column)
```

If we reshape with NumPy's default order:

```python
# WRONG - uses row-major order
matrix = params.reshape(10, 10)  # Incorrect mapping!
```

This produces incorrect matrix positions where connections appear at swapped coordinates.

#### The Solution

Use Fortran order to match MATLAB:

```python
# CORRECT - matches MATLAB's column-major storage
matrix = params.reshape(10, 10, order='F')
```

**Implementation** (from `reshape_posterior_full` function):

```python
def reshape_posterior_full(roi_n, cov_n, Ep, Pp, param_n):
    """
    Reshape full connectivity model (all roi_n x roi_n connections present).

    IMPORTANT: MATLAB stores matrices in column-major (Fortran) order.
    A(i,j) where i=row (target/TO), j=col (source/FROM) is stored at
    linear index (j-1)*nrows + i in MATLAB (1-indexed).

    Using order='F' ensures correct mapping from MATLAB's linear storage.
    """
    Ep_reshaped = np.zeros((roi_n, roi_n, cov_n))
    Pp_reshaped = np.zeros((roi_n, roi_n, cov_n))

    for i_cov in range(cov_n):
        start_idx = i_cov * param_n
        end_idx = (i_cov + 1) * param_n

        # Use Fortran order to match MATLAB's column-major storage
        cov_data_ep = Ep[start_idx:end_idx].reshape(roi_n, roi_n, order='F')
        cov_data_pp = Pp[start_idx:end_idx].reshape(roi_n, roi_n, order='F')

        Ep_reshaped[:, :, i_cov] = cov_data_ep
        Pp_reshaped[:, :, i_cov] = cov_data_pp

    return Ep_reshaped, Pp_reshaped, param_n
```

---

## Self-Connection (Diagonal) Handling

### DCM Self-Connection Parameterization

In DCM, self-connections (diagonal elements) represent intrinsic neural dynamics. They are parameterized as:

```
A(i,i) = -exp(x) / 2
```

Where `x` is the estimated parameter (typically around -0.5 for prior, giving ~-0.3 Hz).

### Visualization Transformation

For display, we revert the transformation to show values in Hz:

```python
diagonal_value_hz = -np.exp(estimated_param) / 2
```

### Avoiding Spurious Diagonal Values

**Problem**: If the reversion transformation is applied to ALL diagonal elements (including zeros from unestimated connections in constrained models), it produces:

```
-exp(0) / 2 = -0.5
```

This creates spurious `-0.5` values appearing significant when they weren't estimated.

**Solution**: Only apply transformation to estimated connections with non-zero values:

```python
# Only apply diagonal reversion to estimated (non-zero) values
if is_diagonal and is_estimated and has_nonzero_value:
    display_value = -np.exp(param_value) / 2
```

---

## Constrained vs Full Connectivity Models

### Full Model

All N x N connections are estimated. The `reshape_posterior_full` function handles these.

### Constrained Model (A-constrained)

Only a subset of connections is estimated, based on significant connections from a prior analysis (e.g., session change analysis).

**Key Implementation**:
- Constrained models use a connection mask
- Box annotations highlight which connections were estimated
- Box positions must match the actual data positions after transpose

**Box Position Fix**:

```python
# After transpose: rows=FROM, cols=TO
# Rectangle(xy, width, height) where xy is (x, y) = (col, row)
# Since we transposed, position (row, col) in data = (col, row) for Rectangle
rect = patches.Rectangle(
    (col, row),  # (x, y) position
    1, 1,        # width, height
    ...
)
```

---

## Combined Panel Layout

### 2x2 Panel Structure

The combined PEB analysis panels show:

| Position | Panel | Description |
|----------|-------|-------------|
| Top-Left | Pre | Baseline session connectivity |
| Top-Right | Post | Post-psilocybin connectivity |
| Bottom-Left | Change | Session difference (Post - Pre) |
| Bottom-Right | Behavioral | Behavioral covariate association |

### Constrained Model Verification

For behavioral covariate panels (bottom-right), the connections should be constrained to only those significant in the change panel (bottom-left).

**Verification**: All significant behavioral connections (Pp >= 0.99) must appear at the same matrix positions as in the change panel.

---

## ROI Order

Standard 10-ROI order used across all visualizations:

| Index | ROI Name |
|-------|----------|
| 0 | Frontal_Mid_L |
| 1 | Frontal_Mid_R |
| 2 | Hippocampus_L |
| 3 | Hippocampus_R |
| 4 | Occipital_Sup_L |
| 5 | Occipital_Sup_R |
| 6 | Temporal_Mid_L |
| 7 | Temporal_Mid_R |
| 8 | Thalamus_L |
| 9 | Thalamus_R |

---

## How to Regenerate Plots

### All PEB Matrix Heatmaps

```bash
cd /path/to/dcm_psilocybin
conda activate dcm_psilocybin_clean

# Regenerate all individual matrices
python scripts/analysis/03_generate_all_peb_matrices.py

# Regenerate combined 2x2 panels
python scripts/analysis/04_generate_peb_matrix_panels.py

# Or use the convenience script
python scripts/analysis/utilities/regenerate_all_peb_plots.py
```

### Full Pipeline

```bash
# Run PEB stages only (03-04)
python scripts/analysis/00_run_full_pipeline.py --peb

# Run paper mode (generates paper-ready figures)
python scripts/analysis/00_run_full_pipeline.py --paper
```

---

## Output Files

### Individual Matrices

Location: `figures/peb_matrices/individual/`

Files per condition:
- `{condition}_pre.png` - Pre-session
- `{condition}_post.png` - Post-session
- `{condition}_change.png` - Session change
- `{condition}_behavioral.png` - Behavioral association

### Combined Panels

Location: `figures/peb_matrices/panels/`

- `m1_peb_panel_2x2.png` - REST
- `m2_peb_panel_2x2.png` - MUSIC
- `m3_peb_panel_2x2.png` - MOVIE
- `m4_peb_panel_2x2.png` - MEDITATION

---

## Troubleshooting

### Connections at Wrong Positions

**Symptom**: Same connections appear in different panels but at different matrix positions.

**Cause**: Reshape order mismatch between MATLAB and NumPy.

**Fix**: Ensure `order='F'` in all reshape operations:
```python
matrix.reshape(n, n, order='F')
```

### Spurious Diagonal Values

**Symptom**: All diagonal elements show -0.5 in constrained models.

**Cause**: Diagonal reversion transformation applied to zero values.

**Fix**: Only apply transformation to estimated, non-zero values.

### Axis Labels Inverted

**Symptom**: From/To labels don't match expected directions.

**Cause**: Labels not updated after transpose.

**Fix**: After transpose, set:
```python
ax.set_xlabel("To")    # columns = targets
ax.set_ylabel("From")  # rows = sources
```

---

## Validation Scripts

Located in `scripts/analysis/validation/`:

| Script | Purpose |
|--------|---------|
| `verify_behavioral_constraint.py` | Verify behavioral connections match change analysis |
| `check_self_connections.py` | Check diagonal values vs raw data |
| `verify_positions_match.py` | Verify positions match across panels |
| `debug_position_mismatch.py` | Debug coordinate issues |

---

## Technical Reference

### Key Functions in `plot_PEB_results.py`

| Function | Purpose |
|----------|---------|
| `reshape_posterior_full()` | Reshape vectorized params to matrix (full model) |
| `reshape_posterior_constrained()` | Reshape for constrained models |
| `create_heatmap()` | Generate single heatmap visualization |
| `create_combined_peb_heatmap()` | Generate 2x2 combined panel |

### Threshold

All visualizations use Pp >= 0.99 (posterior probability threshold).

### Colormaps

| Panel Type | Colormap | Center |
|------------|----------|--------|
| Pre/Post | `coolwarm` | 0 |
| Change | `coolwarm` | 0 |
| Behavioral | `PRGn` | 0 |

---

## References

- SPM DCM documentation: https://www.fil.ion.ucl.ac.uk/spm/doc/
- NumPy reshape order: https://numpy.org/doc/stable/reference/generated/numpy.reshape.html
