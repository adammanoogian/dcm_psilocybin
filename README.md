# DCM Psilocybin Analysis

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

Dynamic Causal Modeling (DCM) analysis of psilocybin effects on brain connectivity using Parametric Empirical Bayes (PEB), with behavioral covariate associations.

## Quick Start

```bash
git clone https://github.com/adammanoogian/dcm_psilocybin.git
cd dcm_psilocybin

# Set up environment (pick one)
conda env create -f environment.yml && conda activate dcm_psilocybin
# or: python -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# Run the analysis pipeline
python scripts/analysis/00_run_full_pipeline.py          # full pipeline
python scripts/analysis/00_run_full_pipeline.py --paper   # publication figures only
python scripts/analysis/00_run_full_pipeline.py --overview # show pipeline stages
```

## Citation

```bibtex
@software{manoogian2024dcm,
  author = {Manoogian, Adam},
  title = {DCM Psilocybin Analysis},
  year = {2024},
  url = {https://github.com/adammanoogian/dcm_psilocybin}
}
```

## License

This project is licensed under the [Creative Commons Attribution 4.0 International License](LICENSE).
