# Documentation

This folder contains all project documentation organized by category.

## Structure

```
docs/
├── README.md                    # This file - documentation navigation
├── 01_project_protocol/         # Project setup, configuration, folder structure
│   ├── FOLDER_STRUCTURE.md      # Comprehensive project organization guide
│   ├── CONN_TOOLBOX_REFERENCE.md # CONN batch scripting reference
│   └── M3_HPC_GUIDE.md          # Monash M3 cluster guide
├── 02_pipeline_guide/           # How to run analyses
│   ├── PIPELINE_NAMING_CONVENTIONS.md  # Script and output naming standards
│   └── FIGURE_QUICK_REFERENCE.md       # Quick lookup tables for figures
├── 03_methods_reference/        # Detailed methods and algorithms
│   ├── FIGURE_ORGANIZATION_GUIDE.md    # Complete figure catalog
│   └── NILEARN_CONNECTIVITY_GUIDE.md   # Nilearn visualization details
└── legacy/                      # Archived/deprecated documentation
```

## Quick Links

### Getting Started
- [Project Goals](01_project_protocol/PROJECT_GOALS.md) - Analysis roadmap and implementation status
- [Folder Structure](01_project_protocol/FOLDER_STRUCTURE.md) - Project organization overview
- [Pipeline Guide](02_pipeline_guide/PIPELINE_NAMING_CONVENTIONS.md) - How to run the analysis pipeline

### HPC and Connectivity Analysis
- [M3 HPC Guide](01_project_protocol/M3_HPC_GUIDE.md) - Monash M3 cluster SSH/SLURM guide
- [CONN Toolbox Reference](01_project_protocol/CONN_TOOLBOX_REFERENCE.md) - CONN batch scripting for functional/dynamic connectivity

### Reference
- [Figure Quick Reference](02_pipeline_guide/FIGURE_QUICK_REFERENCE.md) - Quick lookup for figures
- [Figure Organization Guide](03_methods_reference/FIGURE_ORGANIZATION_GUIDE.md) - Complete figure catalog
- [Nilearn Connectivity Guide](03_methods_reference/NILEARN_CONNECTIVITY_GUIDE.md) - Brain visualization details

## Running the Analysis Pipeline

The analysis pipeline is organized into 8 numbered stages with a master runner:

```bash
# Run full pipeline
python scripts/analysis/00_run_full_pipeline.py

# Run nilearn visualizations only (stages 01-04)
python scripts/analysis/00_run_full_pipeline.py --nilearn

# Run PEB matrix heatmaps only (stages 05-06)
python scripts/analysis/00_run_full_pipeline.py --peb

# Run from specific stage
python scripts/analysis/00_run_full_pipeline.py --start=5

# Run specific range
python scripts/analysis/00_run_full_pipeline.py --start=3 --end=6

# Show pipeline overview
python scripts/analysis/00_run_full_pipeline.py --overview
```

## Pipeline Stages

| Stage | Category | Description |
|-------|----------|-------------|
| 01-04 | Nilearn | Brain connectivity visualizations (3D plots) |
| 05-06 | PEB | Statistical matrix heatmaps (2D plots) |
| 07-08 | Output | Figure organization and paper generation |

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

## Scripts Organization

```
scripts/analysis/
├── 00_run_full_pipeline.py      # Master pipeline runner
├── 01-08_*.py                   # Numbered pipeline scripts
├── utilities/                   # Helper scripts (12 scripts)
└── validation/                  # Debug/test scripts (17 scripts)
```

See [Folder Structure](01_project_protocol/FOLDER_STRUCTURE.md) for complete details.
