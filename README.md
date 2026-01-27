# DCM Psilocybin Analysis

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

Dynamic Causal Modeling (DCM) analysis of psilocybin effects on brain connectivity using Parametric Empirical Bayes (PEB), with behavioral covariate associations.

## Citation

If you use this code or data, please cite:

```bibtex
@software{manoogian2024dcm,
  author = {Manoogian, Adam},
  title = {DCM Psilocybin Analysis},
  year = {2024},
  url = {https://github.com/adammanoogian/dcm_psilocybin}
}
```

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/adammanoogian/dcm_psilocybin.git
cd dcm_psilocybin
```

### 2. Set Up the Environment

**Option A: Using Conda (Recommended)**
```bash
conda env create -f environment.yml
conda activate dcm_psilocybin
```

**Option B: Using pip**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the Analysis Pipeline

```bash
# Generate paper figures only (recommended for publication)
python scripts/analysis/00_run_full_pipeline.py --paper

# Run full pipeline (all 4 stages)
python scripts/analysis/00_run_full_pipeline.py

# Run nilearn brain visualizations only (stages 01-02)
python scripts/analysis/00_run_full_pipeline.py --nilearn

# Run PEB matrix heatmaps only (stages 03-04)
python scripts/analysis/00_run_full_pipeline.py --peb

# Run from specific stage
python scripts/analysis/00_run_full_pipeline.py --start=3

# Show pipeline overview
python scripts/analysis/00_run_full_pipeline.py --overview
```

### 4. View Results

Generated figures are saved to:
- `figures/supplementary/` - ROI-focused nilearn brain plots (dlPFC, hippocampus)
- `figures/peb_matrices/` - Individual PEB matrix heatmaps
- `figures/paper/` - Combined 2x2 publication panels

## Project Structure

```
dcm_psilocybin/
├── scripts/
│   ├── analysis/                    # Main analysis pipeline
│   │   ├── 00_run_full_pipeline.py  # Master pipeline runner
│   │   ├── 01_generate_nilearn_panels.py
│   │   ├── 02_generate_nilearn_supplementary.py
│   │   ├── 03_generate_all_peb_matrices.py
│   │   ├── 04_generate_peb_matrix_panels.py
│   │   └── validation/reference/    # Reference validation scripts
│   ├── visualization/               # Core visualization modules
│   │   ├── plot_nilearn_connectivity.py
│   │   └── plot_PEB_results.py
│   ├── matlab/                      # MATLAB DCM/PEB scripts
│   │   ├── m6/                      # Main analysis scripts
│   │   └── utils/                   # Utility functions
│   └── tests/                       # Test suite
│
├── data/
│   └── peb_outputs/                 # PEB analysis results (.mat files)
│
├── figures/
│   ├── supplementary/               # ROI-focused brain visualizations
│   ├── peb_matrices/                # Individual matrix heatmaps
│   ├── paper/                       # Combined publication panels
│   └── project_images/              # Static reference images
│
└── docs/                            # Documentation
    ├── PROJECT_GUIDE.md
    ├── NILEARN_CONNECTIVITY_GUIDE.md
    ├── PEB_MATRIX_VISUALIZATION_GUIDE.md
    └── SUPPLEMENTARY_UTILITIES_GUIDE.md
```

## Pipeline Stages

| Stage | Script | Description | Output |
|-------|--------|-------------|--------|
| 01 | `01_generate_nilearn_panels.py` | Multi-condition brain connectivity panels | `figures/nilearn/` |
| 02 | `02_generate_nilearn_supplementary.py` | ROI-focused supplementary figures (dlPFC, hippocampus) | `figures/supplementary/` |
| 03 | `03_generate_all_peb_matrices.py` | PEB matrix heatmaps (pre, post, change, behavioral) | `figures/peb_matrices/` |
| 04 | `04_generate_peb_matrix_panels.py` | Combined 2x2 publication panels | `figures/paper/` |

### Paper Mode (`--paper`)

Generates 32 publication-ready figures:
- **8 nilearn supplementary** - dlPFC outgoing + hippocampus network × 4 conditions
- **16 PEB matrices** - pre, post, change, behavioral × 4 conditions
- **8 combined panels** - 2x2 panels in PNG + SVG × 4 conditions

## Naming Conventions

### Experimental Conditions
- **m1** = REST
- **m2** = MUSIC
- **m3** = MOVIE
- **m4** = MEDITATION

### Analysis Types
- **a** = Session change (Post - Pre psilocybin)
- **b** = Behavioral association (11D-ASC composite sensory)

### Example Filenames
```
session_change_rest_dlpfc_outgoing.png  # REST, dlPFC outgoing connections
m1-a_matrix_change.png                  # REST session change matrix
combined_PEB_analysis_rest.png          # REST 2x2 combined panel
```

## Documentation

See `docs/` for detailed documentation:
- [Project Guide](docs/PROJECT_GUIDE.md) - Complete project overview
- [Nilearn Connectivity Guide](docs/NILEARN_CONNECTIVITY_GUIDE.md) - Brain visualization methods
- [PEB Matrix Visualization Guide](docs/PEB_MATRIX_VISUALIZATION_GUIDE.md) - Matrix heatmap methods
- [Supplementary Utilities Guide](docs/SUPPLEMENTARY_UTILITIES_GUIDE.md) - Helper scripts and utilities

## Related Repository

The manuscript for this project is maintained in a separate repository:
- **Paper Repository**: [DCM_psilocybin_v2](https://github.com/adammanoogian/DCM_psilocybin_v2)

## License

This project is licensed under the [Creative Commons Attribution 4.0 International License](LICENSE).
