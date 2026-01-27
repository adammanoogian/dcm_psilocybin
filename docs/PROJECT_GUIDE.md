# Project Guide

Comprehensive guide to the DCM psilocybin analysis project covering structure, pipeline, and figures.

---

## 1. Project Structure

### Overview

```
dcm_psilocybin/
├── scripts/                     # All scripts (Python + MATLAB)
│   ├── analysis/               # Main Python analysis pipeline
│   ├── visualization/          # Core visualization modules
│   ├── matlab/                 # MATLAB DCM analysis scripts
│   └── behav_analysis/         # Behavioral data analysis
├── data/                        # Analysis outputs and inputs
│   └── peb_outputs/            # PEB .mat files from DCM analysis
├── figures/                     # Generated outputs
│   ├── nilearn/                # Brain connectivity visualizations
│   ├── peb_matrices/           # PEB matrix heatmaps
│   └── organized/              # Publication-organized figures
├── docs/                        # Documentation
└── paper/                       # Manuscript materials
```

### Scripts Organization

#### `scripts/analysis/` - Analysis Pipeline

Numbered pipeline scripts that execute in sequence:

```
scripts/analysis/
├── 00_run_full_pipeline.py              # Master pipeline runner
│
├── 01_generate_nilearn_panels.py        # Nilearn panels (basic, hypothesis, combined)
├── 02_generate_nilearn_supplementary.py # ROI-focused supplementary figures
│
├── 03_generate_all_peb_matrices.py      # PEB matrix heatmaps
├── 04_generate_peb_matrix_panels.py     # PEB 2x2 panel combinations
│
├── utilities/                   # Supplementary utility scripts (9 scripts)
│   ├── combine_plots.py                    # Generic SVG combiner
│   ├── create_colorkey_images.py           # Color scale references
│   ├── create_roi_anatomy_figure.py        # ROI anatomical reference
│   ├── create_roi_dorsal_lateral_gif.py    # Presentation GIF
│   ├── create_roi_glass_brain.py           # Glass brain views
│   ├── generate_brain_network_multiview.py # Node-only views
│   ├── generate_dcm_network_figure.py      # DCM architecture
│   ├── generate_example_bold_timeseries.py # Example BOLD
│   └── generate_network_diagram.py         # Network diagram
│
└── validation/                  # Reference scripts (2 scripts)
    └── reference/               # Convention documentation and visual verification
        ├── test_nilearn_transpose.py    # Documents MATLAB→nilearn convention
        └── verify_box_positions.py      # Visual verification of box/value alignment
```

#### `scripts/visualization/` - Core Modules

Reusable visualization modules imported by pipeline scripts:

```
scripts/visualization/
├── plot_nilearn_connectivity.py    # Nilearn brain visualization
└── plot_PEB_results.py             # PEB matrix heatmap plotting
```

#### `scripts/tests/` - Automated Tests

Pytest-based validation tests:

```
scripts/tests/
├── __init__.py
├── conftest.py                     # Shared fixtures
└── test_validation/                # Validation tests
    ├── __init__.py
    ├── test_peb_constraints.py     # PEB constraint integrity tests
    └── test_atlas_symmetry.py      # AAL atlas symmetry tests
```

Run tests with: `pytest scripts/tests/ -v`

#### `scripts/behav_analysis/` - Behavioral Analysis

```
scripts/behav_analysis/
└── analyze_scales.py               # ASC scale analysis
```

#### `scripts/matlab/` - MATLAB DCM Analysis

MATLAB scripts that were run on Monash M3 HPC cluster to produce the PEB `.mat` files from BIDS data. Included here for didactic/record-keeping purposes.

```
scripts/matlab/
├── m6/                              # Main analysis scripts
│   ├── ROI_time_series_extraction.m # Step 1: Extract time series
│   ├── spDCM.m                      # Step 2: Estimate spectral DCM
│   ├── PEB_run_bash.m               # Step 3: Group-level PEB
│   ├── run_peb_slurm.sh             # SLURM batch script for HPC
│   ├── match_subjects_across_groups.m
│   └── PEB_plot_results.m           # Legacy viz (replaced by Python)
└── utils/                           # Shared utility functions
    ├── PEB_reshape_posterior.m      # Reshape matrices for visualization
    ├── utils_get_constrained_A.m    # Extract significant connections
    ├── utils_remove_nan_covariates.m # Handle missing data
    ├── utils_zscore_covariates.m    # Normalize covariates
    └── check_PEB_results.m          # Reference snippet for reviewing PEB
```

**MATLAB Analysis Pipeline (run in order):**

| Order | Script | Purpose |
|-------|--------|---------|
| 1 | `ROI_time_series_extraction.m` | Extract ROI time series from preprocessed BIDS data |
| 2 | `spDCM.m` | Specify and estimate spectral DCM for each subject |
| 3 | `PEB_run_bash.m` | Run group-level PEB analysis |

**Key Parameters:**
- Parcellation: AAL atlas with `adam_m6` masks (6 ROIs)
- Pipeline: tedana-GLM preprocessed data
- TR: 0.91s
- DCM analysis: Cross-spectral density (CSD)

### Data Organization

#### `data/peb_outputs/`

PEB analysis results (`.mat` files) produced by the MATLAB DCM pipeline:

```
data/peb_outputs/
├── PEB_change_*.mat           # Session change analyses (pre→post psilocybin)
├── PEB_behav_*.mat            # Behavioral associations (ASC subscales)
└── PEB_contrast_*.mat         # Task contrasts (rest vs music, etc.)
```

**File naming convention:**
- `PEB_change_-ses-01-ses-02_-task-{task}_cov-_noFD.mat` - Session change
- `PEB_behav_associations_-ses-02_-task-{task}_cov-{covariates}_noFD.mat` - Behavioral
- `PEB_contrast_-ses-02_-task-{task1}-task-{task2}_cov-_noFD.mat` - Task contrasts

### Figures Organization

#### `figures/nilearn/` - Brain Visualizations

Raw nilearn outputs organized by type:

```
figures/nilearn/
├── panels/                    # Multi-condition panels (01*)
├── hypothesis_panels/         # Hypothesis-based panels (02*)
├── combined/                  # Multi-task overlays
├── hypotheses/                # Individual hypothesis figures
└── [individual files]         # Single-condition outputs
```

#### `figures/peb_matrices/` - Matrix Heatmaps

PEB statistical matrix outputs (SEPARATE from nilearn):

```
figures/peb_matrices/
├── panels/                    # Combined 2x2 panels
└── [individual .svg files]    # Raw PEB matrix outputs
```

#### `figures/organized/` - Publication Structure

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

## 2. Pipeline

### Master Pipeline Runner

The pipeline is orchestrated by `00_run_full_pipeline.py`:

```bash
# Run full pipeline
python scripts/analysis/00_run_full_pipeline.py

# Run nilearn only (stages 01-02)
python scripts/analysis/00_run_full_pipeline.py --nilearn

# Run PEB matrices only (stages 03-04)
python scripts/analysis/00_run_full_pipeline.py --peb

# Run paper figures only (stages 02-04 with --paper flag)
python scripts/analysis/00_run_full_pipeline.py --paper

# Run from specific stage
python scripts/analysis/00_run_full_pipeline.py --start=3

# Run stages 1-2
python scripts/analysis/00_run_full_pipeline.py --start=1 --end=2

# Show pipeline overview
python scripts/analysis/00_run_full_pipeline.py --overview
```

### Pipeline Stages

| Stage | Category | Description |
|-------|----------|-------------|
| 01-02 | Nilearn | Brain connectivity visualizations (3D plots) |
| 03-04 | PEB | Statistical matrix heatmaps (2D plots) |

#### Stage 01: Nilearn Panels

**Script**: `01_generate_nilearn_panels.py`

**Modes**: `--mode basic`, `--mode hypothesis`, `--mode combined`, `--mode all`

**Outputs**: `figures/nilearn/`
- `panels/` - Basic multi-condition panels
- `hypothesis_panels/` - Hypothesis-filtered panels
- `combined/` - Overlay and comparison figures

#### Stage 02: Nilearn Supplementary

**Script**: `02_generate_nilearn_supplementary.py`

**Flags**: `--paper` (default), `--full`

**Outputs**:
- Paper mode: `figures/supplementary/`
- Full mode: `figures/nilearn/`

**Description**: ROI-focused supplementary figures including session change plots, behavioral association plots, and task contrast plots.

#### Stage 03: PEB Matrix Heatmaps

**Script**: `03_generate_all_peb_matrices.py`

**Flags**: `--paper` (default), `--full`

**Outputs**: `figures/peb_matrices/`

**Description**: PEB statistical connectivity matrix heatmaps. **SEPARATE from nilearn outputs.**

#### Stage 04: PEB Matrix Panels

**Script**: `04_generate_peb_matrix_panels.py`

**Flags**: `--paper` (default), `--full`

**Outputs**:
- Paper mode: `figures/paper/`
- Full mode: `figures/peb_matrices/panels/`

**Description**: Combined 2x2 PEB matrix panel figures.

### Naming Conventions

#### Script Naming

- **Numbered pipeline**: `{NN}_{description}.py` (e.g., `01_generate_nilearn_panels.py`)
- **Utilities**: Descriptive names in `utilities/` subfolder
- **Validation**: Debug/test scripts in `validation/` subfolder

#### Output Naming

**Pipeline Outputs Pattern**: `{NN}{letter}_{descriptive_name}.{ext}`
- `NN` = Two-digit pipeline step number (matches generating script)
- `letter` = Sequential letter for multiple outputs (a, b, c, ...)
- `descriptive_name` = Clear, lowercase description with underscores
- `ext` = File extension (.png, .pdf, .svg)

**Examples**:
```
01a_panel_change_all_conditions.png
01b_panel_behav_asc_sensory_all_conditions.png
02a_panel_h01_dlpfc_hippocampus_change.png
```

#### Publication Figures

**Pattern**: `{model}-{letter}[{number}]_{description}.{ext}`
- `model` = m1, m2, m3, m4 (conditions) or h01, h02, h03 (hypotheses)
- `letter` = a (session change), b (behavioral ASC11), c (behavioral ASC5)
- `number` = 1, 2 (optional region-specific variants)

**Examples**:
```
m1-a_change_full.png           # REST session change, full network
m2-b1_behavioral_asc11_hipp.png # MUSIC ASC11, hippocampus
h01-a_all_tasks_overlay.png    # Hypothesis 01, overlay view
```

### Key Principles

1. **Numbered Pipeline**: Each analysis step gets a sequential number. Outputs numbered to match generating script.

2. **Category Separation**: Nilearn (01-02) for 3D brain plots, PEB (03-04) for 2D matrix heatmaps. These are kept **SEPARATE**.

3. **Paper vs Full Mode**: Paper mode (default) generates only publication-ready figures. Full mode generates all exploratory figures.

4. **Modularity**: Import and use existing functions from `scripts/visualization/`.

---

## 3. Figure Reference

### Model/Condition Codes

| Code | Condition |
|------|-----------|
| **m1** | REST |
| **m2** | MUSIC |
| **m3** | MOVIE |
| **m4** | MEDITATION |

### Letter Codes (Analysis Type)

| Letter | Analysis |
|--------|----------|
| **a** | Session change (Post - Pre psilocybin) |
| **b** | Behavioral association (11D-ASC composite sensory) |
| **c** | Behavioral association (5D-ASC auditory) - *supplementary* |

### Number Variants (Network Focus)

| Variant | Network |
|---------|---------|
| Base | Full network view |
| **1** | dlPFC outgoing connections |
| **2** | Hippocampus bidirectional |

### Complete Figure Catalog

#### M1: REST CONDITION

| Code | Analysis | Type | Colormap |
|------|----------|------|----------|
| **m1-a** | Session change | Nilearn brain | coolwarm |
| m1-a1 | Session change | dlPFC outgoing | coolwarm |
| m1-a2 | Session change | Hippocampus | coolwarm |
| m1-a_matrix_pre | Session change | PEB matrix (Pre) | blue-white-red |
| m1-a_matrix_post | Session change | PEB matrix (Post) | blue-white-red |
| m1-a_matrix_change | Session change | PEB matrix (Change) | green-purple |
| **m1-b** | Behavioral (ASC11) | Nilearn brain | PRGn |
| m1-b1 | Behavioral (ASC11) | Hippocampus | PRGn |
| m1-b_matrix | Behavioral (ASC11) | PEB matrix | viridis |
| m1-c | Behavioral (ASC5) | Nilearn brain | PRGn |
| m1-c1 | Behavioral (ASC5) | Hippocampus | PRGn |
| m1-c_matrix | Behavioral (ASC5) | PEB matrix | viridis |

#### M2: MUSIC CONDITION

| Code | Analysis | Network | Colormap |
|------|----------|---------|----------|
| **m2-a** | Session change | Full | coolwarm |
| m2-a1 | Session change | dlPFC outgoing | coolwarm |
| m2-a2 | Session change | Hippocampus | coolwarm |
| **m2-b** | Behavioral (ASC11) | Full | PRGn |
| m2-b1 | Behavioral (ASC11) | Hippocampus | PRGn |
| m2-c | Behavioral (ASC5) | Full | PRGn |
| m2-c1 | Behavioral (ASC5) | Hippocampus | PRGn |

#### M3: MOVIE CONDITION

| Code | Analysis | Network | Colormap |
|------|----------|---------|----------|
| **m3-a** | Session change | Full | coolwarm |
| m3-a1 | Session change | dlPFC outgoing | coolwarm |
| m3-a2 | Session change | Hippocampus | coolwarm |
| **m3-b** | Behavioral (ASC11) | Full | PRGn |
| m3-b1 | Behavioral (ASC11) | Hippocampus | PRGn |

#### M4: MEDITATION CONDITION

| Code | Analysis | Network | Colormap |
|------|----------|---------|----------|
| **m4-a** | Session change | Full | coolwarm |
| m4-a1 | Session change | dlPFC outgoing | coolwarm |
| m4-a2 | Session change | Hippocampus | coolwarm |

*Note: No behavioral data currently available for meditation*

#### CONTRASTS

| Figure | Description | Colormap |
|--------|-------------|----------|
| `contrast_rest_vs_music.png` | Rest - Music | RdYlBu_r |
| `contrast_rest_vs_movie.png` | Rest - Movie | RdYlBu_r |
| `contrast_music_vs_movie.png` | Music - Movie | RdYlBu_r |

#### H01: MULTI-CONDITION COMPARISONS

| Code | Description | Method | Conditions |
|------|-------------|--------|-----------|
| **h01-a** | All tasks session change | Overlay | Rest/Music/Movie/Med |
| **h01-b** | All tasks session change | Side-by-side | Rest/Music/Movie/Med |
| **h01-c** | ASC Auditory | Overlay | Rest vs Music |
| **h01-d** | ASC Auditory | Side-by-side | Rest vs Music |
| **h01-e** | ASC Sensory | Overlay | Rest/Music/Movie |
| **h01-f** | ASC Sensory | Side-by-side | Rest/Music/Movie |

#### H02: dlPFC OUTGOING CONNECTIONS

| Code | Description | Network Filter | Conditions |
|------|-------------|----------------|-----------|
| **h02-a** | Session change | dlPFC outgoing only | Rest/Music/Movie/Med |
| **h02-b** | Behavioral (11D-ASC) | dlPFC outgoing only | Rest/Music/Movie |

#### H03: HIPPOCAMPUS CONNECTIONS

| Code | Description | Network Filter | Conditions |
|------|-------------|----------------|-----------|
| **h03-a** | Session change | Hippocampus bidirectional | Rest/Music/Movie/Med |
| **h03-b** | Behavioral (11D-ASC) | Hippocampus bidirectional | Rest/Music/Movie |

### Colormap Guide

#### Nilearn Brain Connectivity

| Colormap | Use Case | Interpretation |
|----------|----------|----------------|
| `coolwarm` | Session changes | Blue = decrease, Red = increase |
| `PRGn` | Behavioral | Purple = negative β, Green = positive β |
| `RdYlBu_r` | Task contrasts | Red = more in task 1, Blue = more in task 2 |

#### PEB Matrix Heatmaps

| Colormap | Use Case | Interpretation |
|----------|----------|----------------|
| `blue-white-red` | Session change (Pre/Post) | Blue = inhibitory, Red = excitatory |
| `green-purple` | Change toward zero | Green = closer to zero, Purple = further from zero |
| `viridis` | Behavioral associations | Yellow = positive β, Purple = negative β |

### Quick Lookup Tables

#### By Overleaf Table Row

| Overleaf | Code | Description |
|----------|------|-------------|
| 1a | m1-a | REST - Change |
| 2a | m2-a | MUSIC - Change |
| 3a | m3-a | MOVIE - Change |
| 4a | m4-a | MEDITATION - Change |
| 1b | m1-b | REST - Behavioral (11D-ASC) |
| 2b | m2-b | MUSIC - Behavioral (11D-ASC) |
| 3b | m3-b | MOVIE - Behavioral (11D-ASC) |
| 4b | m4-b | MEDITATION - Behavioral *[not available]* |

#### Find Figures by Condition

- **REST**: `figures/organized/m1_rest/m1-*`
- **MUSIC**: `figures/organized/m2_music/m2-*`
- **MOVIE**: `figures/organized/m3_movie/m3-*`
- **MEDITATION**: `figures/organized/m4_meditation/m4-*`

#### Find Figures by Analysis Type

- **Session changes**: `m*-a*`
- **Behavioral (11D-ASC)**: `m*-b*`
- **Behavioral (5D-ASC)**: `m*-c*`
- **Contrasts**: `contrasts/contrast_*`
- **Multi-condition**: `h01_multi_condition/h01-*`

#### Find Figures by Network Focus

- **Full network**: Base code (`m1-a`, `m2-b`, etc.)
- **dlPFC**: Variant 1 (`m1-a1`, `m2-a1`, etc.)
- **Hippocampus**: Variant 2 (`m1-a2`, `m2-a2`, etc.) or variant 1 for behavioral (`m1-b1`, etc.)

### File Path Examples

```
# REST session change (full network)
figures/organized/m1_rest/m1-a_change_full.png

# MUSIC behavioral 11D-ASC (hippocampus)
figures/organized/m2_music/m2-b1_behavioral_asc11_hipp.png

# MOVIE session change (dlPFC)
figures/organized/m3_movie/m3-a1_change_dlpfc.png

# Multi-condition overlay
figures/organized/h01_multi_condition/h01-a_all_tasks_overlay.png
```

---

## 4. Technical Details

### Matrix Convention

- **MATLAB DCM**: `A(i,j)` = FROM j TO i (rows=targets, cols=sources)
- **Visualization**: After transpose, rows=sources (FROM), cols=targets (TO)
- **Nilearn**: `matrix[i,j]` = FROM i TO j (rows=sources, cols=targets)
- **Solution**: Transpose matrix before display: `connectivity_matrix.T`

**Note:** PEB matrices are displayed in MATLAB convention (rows=targets, columns=sources) with transposed orientation in seaborn heatmaps. A-constrained behavioral models show template boxes (dotted lines) indicating active connections in the model.

### Directed Arrows

- Nilearn 0.12+ supports directed arrows via FancyArrow patches
- Automatically displayed when matrix is asymmetric
- Arrow direction: FROM source TO target
- Arrowhead points to the target node

### Laterality

- Parameter: `radiological=False` (default)
- Result: Left hemisphere on left side of image (neurological convention)
- MNI coordinates: X < 0 = left, X > 0 = right

### Figure Parameters

**Standard Settings:**
- **Node size**: 70-100 (larger for focused views)
- **Edge threshold**: 0% (show all Pp>0.99 connections)
- **Display mode**:
  - `lyrz` for single plots (4 views: sagittal L/R, coronal Y, axial Z)
  - `z` for multi-panel plots (axial view only)
- **DPI**: 300 (high resolution)
- **Figure size**: 18×10 for single, varies for multi-panel

**Region Filtering:**
- **dlPFC outgoing**: `source_regions=['Frontal_Mid']`, `connection_type='outgoing'`
- **Hippocampus**: `source_regions=['Hippocampus']`, `connection_type='bidirectional'`

### Data Sources

All figures use Pp > 0.99 threshold from:
- **Session changes**: `PEB_change_-ses-01-ses-02_-task-{TASK}_cov-_noFD.mat`
- **Behavioral (11D-ASC)**: `PEB_behav_associations_-ses-02_-task-{TASK}_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_noFD.mat`
- **Behavioral (5D-ASC)**: `PEB_behav_associations_-ses-02_-task-{TASK}_cov-ASC5_AUDITORY_noFD.mat`
- **Contrasts**: `PEB_contrast_-ses-02_-task-{TASK1}-task-{TASK2}_cov-_noFD.mat`

---

## Legend

- **Bold codes** (e.g., **m1-a**): Primary full network figure for publication
- Numbered variants: Focused network views (dlPFC, hippocampus)
- Letter codes: Analysis type within condition (a=change, b=behavioral, etc.)
- ASC11 = 11D-ASC Composite Sensory scale
- ASC5 = 5D-ASC Auditory subscale
