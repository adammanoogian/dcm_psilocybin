# Project Folder Structure

Comprehensive guide to the DCM psilocybin analysis project organization.

## Overview

```
dcm_psilocybin/
├── scripts/                     # All Python scripts
│   ├── analysis/               # Main analysis pipeline
│   ├── visualization/          # Core visualization modules
│   └── behav_analysis/         # Behavioral data analysis
├── figures/                     # Generated outputs
│   ├── nilearn/                # Brain connectivity visualizations
│   ├── peb_matrices/           # PEB matrix heatmaps
│   └── organized/              # Publication-organized figures
├── docs/                        # Documentation
├── massive_output_local/        # Data and MATLAB outputs
└── paper/                       # Manuscript materials
```

---

## Scripts Organization

### `scripts/analysis/` - Analysis Pipeline

Numbered pipeline scripts that execute in sequence:

```
scripts/analysis/
├── 00_run_full_pipeline.py              # Master pipeline runner
│
├── 01_generate_nilearn_connectivity_panels.py    # Nilearn panels
├── 02_generate_hypothesis_nilearn_panels.py      # Hypothesis-based panels
├── 03_generate_all_nilearn_figures.py            # All nilearn figures
├── 04_generate_combined_nilearn_figures.py       # Combined overlays
│
├── 05_generate_all_peb_matrices.py               # PEB matrix heatmaps
├── 06_generate_peb_matrix_panels.py              # PEB panel combinations
│
├── 07_organize_figures.py                        # Organize to publication
├── 08_generate_paper_figures.py                  # Final paper figures
│
├── utilities/                   # Non-pipeline utility scripts
│   ├── create_colorkey_images.py
│   ├── create_roi_anatomy_figure.py
│   ├── create_roi_4views_static.py
│   ├── create_roi_dorsal_lateral_gif.py
│   ├── create_roi_glass_brain.py
│   ├── generate_network_diagram.py
│   ├── generate_brain_network_multiview.py
│   ├── generate_dcm_network_figure.py
│   ├── generate_example_bold_timeseries.py
│   ├── generate_hypothesis_panels.py     # Legacy script
│   ├── combine_plots.py
│   └── create_combined_analyses.py
│
└── validation/                  # Debug and validation scripts (17 scripts)
    ├── check_aal_atlas_values.py
    ├── check_aal_labels.py
    ├── check_behavioral_constraint.py
    ├── check_behavioral_covariates.py
    ├── check_coord_symmetry.py
    ├── check_regions.py
    ├── check_rest_matrices.py
    ├── debug_aal_atlas.py
    ├── debug_dlpfc_matrix.py
    ├── diagnose_constraint_mismatch.py
    ├── fix_aal_coordinates.py
    ├── fix_aal_coordinates2.py
    ├── test_nilearn_arrows.py
    ├── test_nilearn_transpose.py
    ├── test_overlay_connectome.py
    ├── trace_plotting_flow.py
    └── verify_box_positions.py
```

### `scripts/visualization/` - Core Modules

Reusable visualization modules imported by pipeline scripts:

```
scripts/visualization/
├── plot_nilearn_connectivity.py    # Nilearn brain visualization
└── plot_PEB_results.py             # PEB matrix heatmap plotting
```

### `scripts/behav_analysis/` - Behavioral Analysis

```
scripts/behav_analysis/
└── analyze_scales.py               # ASC scale analysis
```

---

## Figures Organization

### `figures/nilearn/` - Brain Visualizations

Raw nilearn outputs organized by type:

```
figures/nilearn/
├── panels/                    # Multi-condition panels (01*)
├── hypothesis_panels/         # Hypothesis-based panels (02*)
├── combined/                  # Multi-task overlays
├── hypotheses/                # Individual hypothesis figures
└── [individual files]         # Single-condition outputs
```

### `figures/peb_matrices/` - Matrix Heatmaps

PEB statistical matrix outputs (SEPARATE from nilearn):

```
figures/peb_matrices/
├── panels/                    # Combined 2x2 panels
└── [individual .svg files]    # Raw PEB matrix outputs
```

### `figures/organized/` - Publication Structure

Final organized figures following paper conventions:

```
figures/organized/
├── m1_rest/                   # REST condition (m1-a, m1-b, m1-c)
├── m2_music/                  # MUSIC condition (m2-a, m2-b, m2-c)
├── m3_movie/                  # MOVIE condition (m3-a, m3-b)
├── m4_meditation/             # MEDITATION condition (m4-a)
├── contrasts/                 # Task contrasts
└── h01_multi_condition/       # Multi-condition hypotheses
```

---

## Data Organization

### `massive_output_local/`

PEB analysis results from MATLAB:

```
massive_output_local/
├── adam_m6/                   # Main PEB outputs (.mat files)
│   ├── PEB_change_*.mat       # Session change analyses
│   ├── PEB_behav_*.mat        # Behavioral associations
│   └── PEB_contrast_*.mat     # Task contrasts
├── phenotype/                 # Behavioral/demographic data
└── scripts/                   # MATLAB analysis scripts
```

---

## Documentation Organization

```
docs/
├── README.md                           # Navigation hub
├── 01_project_protocol/                # Setup and configuration
│   └── FOLDER_STRUCTURE.md            # This file
├── 02_pipeline_guide/                  # How to run analyses
│   ├── PIPELINE_NAMING_CONVENTIONS.md # Script/output naming
│   └── FIGURE_QUICK_REFERENCE.md      # Quick lookup tables
├── 03_methods_reference/               # Detailed methods
│   ├── FIGURE_ORGANIZATION_GUIDE.md   # Complete figure catalog
│   └── NILEARN_CONNECTIVITY_GUIDE.md  # Nilearn details
└── legacy/                             # Archived documentation
```

---

## Pipeline Execution

### Full Pipeline

```bash
python scripts/analysis/00_run_full_pipeline.py
```

### Category-Specific

```bash
# Nilearn brain visualizations only (stages 01-04)
python scripts/analysis/00_run_full_pipeline.py --nilearn

# PEB matrix heatmaps only (stages 05-06)
python scripts/analysis/00_run_full_pipeline.py --peb
```

### Partial Pipeline

```bash
# Start from stage 5
python scripts/analysis/00_run_full_pipeline.py --start=5

# Run stages 3-6
python scripts/analysis/00_run_full_pipeline.py --start=3 --end=6
```

---

## Key Conventions

### Script Naming

- **Numbered pipeline**: `{NN}_{description}.py` (e.g., `01_generate_nilearn_connectivity_panels.py`)
- **Utilities**: Descriptive names in `utilities/` subfolder
- **Validation**: Debug/test scripts in `validation/` subfolder

### Output Naming

- **Pipeline outputs**: `{NN}{letter}_{description}.{ext}` (e.g., `01a_panel_change_all_conditions.png`)
- **Publication figures**: `{model}-{letter}_{description}.png` (e.g., `m1-a_change_full.png`)

### Category Separation

- **Nilearn**: Brain connectivity visualizations (3D brain plots)
- **PEB matrices**: Statistical heatmaps (2D matrix plots)
- These are kept SEPARATE to avoid confusion between visualization types
