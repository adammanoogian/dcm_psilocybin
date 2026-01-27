# Documentation

This folder contains all project documentation.

## Structure

```
docs/
├── README.md                         # This file - documentation navigation
├── PROJECT_GUIDE.md                  # Comprehensive project, pipeline, and figure guide
├── NILEARN_CONNECTIVITY_GUIDE.md     # Nilearn visualization details
├── PEB_MATRIX_VISUALIZATION_GUIDE.md # PEB heatmap technical details
└── SUPPLEMENTARY_UTILITIES_GUIDE.md  # Utility scripts reference
```

## Quick Links

### Getting Started
- [Project Guide](PROJECT_GUIDE.md) - Comprehensive guide covering project structure, pipeline, and figures

### Visualization Reference
- [Nilearn Connectivity Guide](NILEARN_CONNECTIVITY_GUIDE.md) - Brain visualization details
- [PEB Matrix Visualization Guide](PEB_MATRIX_VISUALIZATION_GUIDE.md) - Heatmap technical details
- [Supplementary Utilities Guide](SUPPLEMENTARY_UTILITIES_GUIDE.md) - Utility scripts reference

## Running the Analysis Pipeline

The analysis pipeline is organized into 4 numbered stages with a master runner:

```bash
# Run full pipeline
python scripts/analysis/00_run_full_pipeline.py

# Run nilearn visualizations only (stages 01-02)
python scripts/analysis/00_run_full_pipeline.py --nilearn

# Run PEB matrix heatmaps only (stages 03-04)
python scripts/analysis/00_run_full_pipeline.py --peb

# Run from specific stage
python scripts/analysis/00_run_full_pipeline.py --start=3

# Run specific range
python scripts/analysis/00_run_full_pipeline.py --start=1 --end=2

# Show pipeline overview
python scripts/analysis/00_run_full_pipeline.py --overview
```

## Pipeline Stages

| Stage | Category | Description |
|-------|----------|-------------|
| 01-02 | Nilearn | Brain connectivity visualizations (3D plots) |
| 03-04 | PEB | Statistical matrix heatmaps (2D plots) |

## Output Organization

Figures are organized into two main categories (kept **separate**):

1. **Nilearn Brain Visualizations** (`figures/nilearn/`)
   - Brain connectivity plots using nilearn
   - Connectome visualizations with directed arrows
   - Panels, hypothesis panels, combined overlays

2. **PEB Matrix Heatmaps** (`figures/peb_matrices/`)
   - Statistical connectivity matrices
   - Heatmap visualizations of PEB results

Both are organized into publication structure in `figures/organized/`.

## Running Validation Tests

```bash
# Run all validation tests
pytest scripts/tests/test_validation/ -v

# Run specific test category
pytest scripts/tests/test_validation/test_peb_constraints.py -v
pytest scripts/tests/test_validation/test_atlas_symmetry.py -v
```
