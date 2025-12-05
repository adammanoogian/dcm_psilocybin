# Pipeline and Naming Conventions

## Overview

This document defines the standardized pipeline structure and naming conventions for the DCM psilocybin analysis project. All analysis scripts and outputs should follow these conventions for consistency and reproducibility.

---

## Pipeline Structure

### Master Pipeline Runner

The pipeline is orchestrated by `00_run_full_pipeline.py`:

```bash
# Run full pipeline
python scripts/analysis/00_run_full_pipeline.py

# Run nilearn only (stages 01-04)
python scripts/analysis/00_run_full_pipeline.py --nilearn

# Run PEB matrices only (stages 05-06)
python scripts/analysis/00_run_full_pipeline.py --peb

# Run from specific stage
python scripts/analysis/00_run_full_pipeline.py --start=5

# Show pipeline overview
python scripts/analysis/00_run_full_pipeline.py --overview
```

### Numbered Pipeline Scripts

All analysis pipeline scripts are numbered sequentially in `scripts/analysis/`:

```
scripts/analysis/
├── 00_run_full_pipeline.py                       # Master runner
│
├── 01_generate_nilearn_connectivity_panels.py    # Nilearn panels
├── 02_generate_hypothesis_nilearn_panels.py      # Hypothesis panels
├── 03_generate_all_nilearn_figures.py            # All nilearn figures
├── 04_generate_combined_nilearn_figures.py       # Combined overlays
│
├── 05_generate_all_peb_matrices.py               # PEB matrix heatmaps
├── 06_generate_peb_matrix_panels.py              # PEB panel combinations
│
├── 07_organize_figures.py                        # Organize to publication
├── 08_generate_paper_figures.py                  # Final paper figures
│
├── utilities/                                    # Non-pipeline utilities
└── validation/                                   # Debug/validation scripts
```

**Naming Pattern**: `{NN}_{descriptive_name}.py`
- `NN` = Two-digit sequential number (00, 01, 02, ...)
- `descriptive_name` = Clear, lowercase description with underscores

**Categories**:
- **01-04**: Nilearn brain connectivity visualizations
- **05-06**: PEB matrix heatmaps (separate from nilearn)
- **07-08**: Figure organization and paper generation

---

## Pipeline Stages

### Stage 01: Nilearn Connectivity Panels

**Script**: `01_generate_nilearn_connectivity_panels.py`

**Outputs**: `figures/nilearn/panels/`
```
01a_panel_change_all_conditions.png
01b_panel_behav_asc_sensory_all_conditions.png
01c_panel_behav_asc_auditory_rest_music.png
```

**Description**: Multi-panel brain connectivity figures showing session changes and behavioral associations across all experimental conditions.

### Stage 02: Hypothesis-Based Nilearn Panels

**Script**: `02_generate_hypothesis_nilearn_panels.py`

**Outputs**: `figures/nilearn/hypothesis_panels/`
```
02a_panel_h01_dlpfc_hippocampus_change.png
02b_panel_h01_dlpfc_hippocampus_behavioral.png
...
```

**Description**: Hypothesis-specific connectivity panels (dlPFC, hippocampus, etc.) for targeted network analyses.

### Stage 03: All Nilearn Figures

**Script**: `03_generate_all_nilearn_figures.py`

**Outputs**: `figures/nilearn/`

**Description**: Comprehensive nilearn figures for all single conditions (m1-m4) including session change and behavioral association plots.

### Stage 04: Combined Nilearn Figures

**Script**: `04_generate_combined_nilearn_figures.py`

**Outputs**: `figures/nilearn/combined/`

**Description**: Multi-condition overlays and comparisons (h01 hypothesis figures).

### Stage 05: PEB Matrix Heatmaps

**Script**: `05_generate_all_peb_matrices.py`

**Outputs**: `figures/peb_matrices/`

**Description**: PEB statistical connectivity matrix heatmaps. **SEPARATE from nilearn outputs.**

### Stage 06: PEB Matrix Panels

**Script**: `06_generate_peb_matrix_panels.py`

**Outputs**: `figures/peb_matrices/panels/`

**Description**: Combined 2x2 PEB matrix panel figures.

### Stage 07: Organize Figures

**Script**: `07_organize_figures.py`

**Outputs**: `figures/organized/`

**Description**: Organizes all figures into publication structure (m1-m4, h01-h03).

### Stage 08: Generate Paper Figures

**Script**: `08_generate_paper_figures.py`

**Outputs**: `figures/paper/`

**Description**: Final publication-ready figures.

---

## Output Naming Convention

### Pipeline Outputs

All outputs from pipeline scripts are numbered to match their generating script:

**Naming Pattern**: `{NN}{letter}_{descriptive_name}.{ext}`
- `NN` = Two-digit pipeline step number (matches generating script)
- `letter` = Sequential letter for multiple outputs (a, b, c, ...)
- `descriptive_name` = Clear, lowercase description with underscores
- `ext` = File extension (.png, .pdf, .svg, etc.)

**Examples**:
```
01a_panel_change_all_conditions.png
01b_panel_behav_asc_sensory_all_conditions.png
02a_panel_h01_dlpfc_hippocampus_change.png
05a_peb_matrix_rest_change.svg
```

### Publication Figures

Organized figures follow the model/hypothesis convention:

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

---

## Directory Structure

```
dcm_psilocybin/
├── scripts/
│   ├── analysis/                    # Numbered pipeline scripts
│   │   ├── 00_run_full_pipeline.py  # Master runner
│   │   ├── 01_generate_*.py         # Nilearn panels
│   │   ├── 02_generate_*.py         # Hypothesis panels
│   │   ├── 03_generate_*.py         # All nilearn figures
│   │   ├── 04_generate_*.py         # Combined nilearn
│   │   ├── 05_generate_*.py         # PEB matrices
│   │   ├── 06_generate_*.py         # PEB panels
│   │   ├── 07_organize_*.py         # Organization
│   │   ├── 08_generate_*.py         # Paper figures
│   │   ├── utilities/               # Non-pipeline utilities
│   │   └── validation/              # Debug/validation scripts
│   └── visualization/               # Modular visualization functions
│       ├── plot_nilearn_connectivity.py
│       └── plot_PEB_results.py
├── figures/
│   ├── nilearn/                     # Brain connectivity visualizations
│   │   ├── panels/                  # Multi-condition panels
│   │   ├── hypothesis_panels/       # Hypothesis-based panels
│   │   └── combined/                # Multi-task overlays
│   ├── peb_matrices/                # PEB matrix heatmaps (SEPARATE)
│   │   └── panels/                  # Combined matrix panels
│   └── organized/                   # Publication-organized figures
│       ├── m1_rest/
│       ├── m2_music/
│       ├── m3_movie/
│       ├── m4_meditation/
│       ├── contrasts/
│       └── h01_multi_condition/
└── docs/
    ├── 01_project_protocol/
    ├── 02_pipeline_guide/           # This file is here
    └── 03_methods_reference/
```

---

## Key Principles

### 1. Numbered Pipeline
- Each analysis step gets a sequential number
- Outputs are numbered to match their generating script
- Master runner (00) orchestrates all stages
- Easy to run partial pipeline with --start/--end flags

### 2. Category Separation
- **Nilearn (01-04)**: Brain connectivity visualizations (3D brain plots)
- **PEB (05-06)**: Statistical matrix heatmaps (2D plots)
- These are kept **SEPARATE** to avoid confusion

### 3. Modularity
- **DO**: Import and use existing functions from `scripts/visualization/`
- **DON'T**: Reimplement functionality in each pipeline script

### 4. Documentation
- Each pipeline script documents its outputs in the header
- Update this document when adding new pipeline steps
- Maintain clear connection between script number and output numbers

---

## Quick Reference

### Running the Pipeline

```bash
# Full pipeline
python scripts/analysis/00_run_full_pipeline.py

# Nilearn only
python scripts/analysis/00_run_full_pipeline.py --nilearn

# PEB only
python scripts/analysis/00_run_full_pipeline.py --peb

# From stage N
python scripts/analysis/00_run_full_pipeline.py --start=N

# Stages N to M
python scripts/analysis/00_run_full_pipeline.py --start=N --end=M
```

### Naming Your Outputs

```
{NN}{letter}_{descriptive_name}.{ext}
 ││    │              │            └─ Extension (.png, .pdf, .svg)
 ││    │              └─────────────── What it shows (lowercase, underscores)
 ││    └────────────────────────────── Output sequence (a, b, c, ...)
 │└─────────────────────────────────── Two digits (01-99)
 └──────────────────────────────────── Pipeline step number
```

### Good Filename Examples
```
01a_panel_change_all_conditions.png
02b_panel_h01_dlpfc_behavioral.png
05a_peb_matrix_rest_change.svg
07a_organized_m1_rest_full.png
```

### Bad Filename Examples
```
generate_nilearn_panels.py        # Not numbered
panel_change_matrices.png         # No number prefix
output_final_v2_new.png           # Vague, no number
figure1.png                       # Too generic
```

---

## Integration with Publication Conventions

This pipeline numbering system complements the publication figure organization:

- **Pipeline numbering** (01a, 02b, etc.): Generation/analysis step
- **Model numbering** (m1-a, m2-b, etc.): Publication organization by condition
- **Hypothesis numbering** (h01-a, h01-b, etc.): Multi-condition comparisons

### Mapping Example

```
Pipeline Output                → Organized Figure
03_nilearn/session_change_rest → figures/organized/m1_rest/m1-a_change_full.png
04_combined/overlay_all_tasks  → figures/organized/h01_multi_condition/h01-a_overlay.png
05_peb/rest_change_matrix.svg  → figures/organized/m1_rest/m1-a_matrix.png
```

Use `07_organize_figures.py` to map pipeline outputs to publication structure.

---

## Version History

- **v2.0** (2025-12-01): Major reorganization
  - Added master pipeline runner (00_run_full_pipeline.py)
  - Numbered all pipeline scripts (01-08)
  - Separated nilearn and PEB outputs
  - Created utilities/ and validation/ subfolders
  - Updated documentation structure

- **v1.0** (2025-01-18): Initial pipeline conventions document
  - Established numbered pipeline approach
  - Defined output naming standards
  - Created template for new scripts
