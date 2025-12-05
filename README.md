# DCM Psilocybin Analysis

Dynamic Causal Modeling (DCM) analysis of psilocybin effects on brain connectivity, with behavioral covariate associations.

## Quick Start

### Running the Analysis Pipeline

```bash
# Activate environment
conda activate dcm_psilocybin

# Run full pipeline
python scripts/analysis/00_run_full_pipeline.py

# Run nilearn brain visualizations only (stages 01-04)
python scripts/analysis/00_run_full_pipeline.py --nilearn

# Run PEB matrix heatmaps only (stages 05-06)
python scripts/analysis/00_run_full_pipeline.py --peb

# Run from specific stage
python scripts/analysis/00_run_full_pipeline.py --start=5

# Show pipeline overview
python scripts/analysis/00_run_full_pipeline.py --overview
```

## Project Structure

```
dcm_psilocybin/
├── scripts/
│   ├── analysis/                    # Main analysis pipeline
│   │   ├── 00_run_full_pipeline.py  # Master pipeline runner
│   │   ├── 01_generate_nilearn_connectivity_panels.py
│   │   ├── 02_generate_hypothesis_nilearn_panels.py
│   │   ├── 03_generate_all_nilearn_figures.py
│   │   ├── 04_generate_combined_nilearn_figures.py
│   │   ├── 05_generate_all_peb_matrices.py
│   │   ├── 06_generate_peb_matrix_panels.py
│   │   ├── 07_organize_figures.py
│   │   ├── 08_generate_paper_figures.py
│   │   ├── utilities/               # Helper scripts (ROI creation, etc.)
│   │   └── validation/              # Debug and validation scripts
│   ├── visualization/               # Core visualization modules
│   │   ├── plot_nilearn_connectivity.py
│   │   └── plot_PEB_results.py
│   └── behav_analysis/              # Behavioral data analysis
│
├── figures/
│   ├── nilearn/                     # Brain connectivity visualizations
│   │   ├── panels/                  # Multi-condition panels
│   │   ├── hypothesis_panels/       # Hypothesis-based panels
│   │   └── combined/                # Multi-task overlays
│   ├── peb_matrices/                # PEB matrix heatmaps (separate)
│   └── organized/                   # Publication-organized figures
│       ├── m1_rest/                 # REST condition
│       ├── m2_music/                # MUSIC condition
│       ├── m3_movie/                # MOVIE condition
│       ├── m4_meditation/           # MEDITATION condition
│       ├── contrasts/               # Task contrasts
│       └── h01_multi_condition/     # Multi-condition hypotheses
│
├── docs/                            # Documentation
│   ├── 01_project_protocol/         # Project setup and structure
│   ├── 02_pipeline_guide/           # How to run analyses
│   └── 03_methods_reference/        # Detailed methods
│
├── massive_output_local/            # Data and MATLAB outputs
│   └── adam_m6/                     # PEB analysis results (.mat files)
│
└── paper/                           # Manuscript materials
```

## Pipeline Stages

| Stage | Script | Description | Output |
|-------|--------|-------------|--------|
| 01 | `01_generate_nilearn_connectivity_panels.py` | Multi-condition connectivity panels | `figures/nilearn/panels/` |
| 02 | `02_generate_hypothesis_nilearn_panels.py` | Hypothesis-specific panels | `figures/nilearn/hypothesis_panels/` |
| 03 | `03_generate_all_nilearn_figures.py` | All single-condition figures | `figures/nilearn/` |
| 04 | `04_generate_combined_nilearn_figures.py` | Multi-condition overlays | `figures/nilearn/combined/` |
| 05 | `05_generate_all_peb_matrices.py` | PEB matrix heatmaps | `figures/peb_matrices/` |
| 06 | `06_generate_peb_matrix_panels.py` | Combined matrix panels | `figures/peb_matrices/panels/` |
| 07 | `07_organize_figures.py` | Organize to publication structure | `figures/organized/` |
| 08 | `08_generate_paper_figures.py` | Final paper figures | `figures/paper/` |

## Output Categories

### Nilearn Brain Visualizations (Stages 01-04)
3D brain connectivity plots showing directed connections between regions.

### PEB Matrix Heatmaps (Stages 05-06)
2D statistical heatmaps of connectivity matrices from PEB analysis.

These are kept **separate** to distinguish visualization types.

## Naming Conventions

### Experimental Conditions
- **m1** = REST
- **m2** = MUSIC
- **m3** = MOVIE
- **m4** = MEDITATION

### Analysis Types
- **a** = Session change (Post - Pre psilocybin)
- **b** = Behavioral association (11D-ASC composite sensory)
- **c** = Behavioral association (5D-ASC auditory)

### Example Filenames
```
m1-a_change_full.png           # REST session change, full network
m2-b1_behavioral_asc11_hipp.png # MUSIC ASC11, hippocampus focus
h01-a_all_tasks_overlay.png    # Multi-condition overlay
```

## Documentation

See `docs/` for detailed documentation:
- [Folder Structure](docs/01_project_protocol/FOLDER_STRUCTURE.md) - Complete project organization
- [Pipeline Guide](docs/02_pipeline_guide/PIPELINE_NAMING_CONVENTIONS.md) - How to run the pipeline
- [Figure Organization](docs/03_methods_reference/FIGURE_ORGANIZATION_GUIDE.md) - Complete figure catalog

## Requirements

- Python 3.8+
- nilearn
- matplotlib
- scipy
- numpy

```bash
conda activate dcm_psilocybin
```
