# Project Goals: Connectivity Analysis Pipeline

Overview of analysis goals and implementation status for the DCM psilocybin project.

---

## Analysis Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CONNECTIVITY ANALYSIS PIPELINE                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Phase 1: DCM/PEB Analysis                    [COMPLETE]            │
│  ├── Dynamic Causal Modeling (SPM/MATLAB)                          │
│  ├── Parametric Empirical Bayes (PEB)                              │
│  └── Visualization (Python/nilearn)                                │
│                                                                     │
│  Phase 2: Functional Connectivity            [PLANNED]              │
│  ├── ROI-to-ROI connectivity (CONN)                                │
│  ├── Seed-based correlations (CONN)                                │
│  └── Graph theory metrics                                          │
│                                                                     │
│  Phase 3: Dynamic Effective Connectivity     [PLANNED]              │
│  ├── Sliding window analysis (CONN)                                │
│  ├── Dynamic ICA (dyn-ICA)                                         │
│  └── Generalized PPI (gPPI)                                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: DCM/PEB Analysis [COMPLETE]

### Status: Complete

### Methods
- **Software**: SPM12/MATLAB
- **Analysis**: Dynamic Causal Modeling with Parametric Empirical Bayes
- **Conditions**: REST, MUSIC, MOVIE, MEDITATION

### Outputs
- PEB results: `massive_output_local/adam_m6/`
- Visualizations: `figures/nilearn/`, `figures/peb_matrices/`

### Documentation
- [Folder Structure](FOLDER_STRUCTURE.md)
- [Pipeline Guide](../02_pipeline_guide/PIPELINE_NAMING_CONVENTIONS.md)
- [Nilearn Visualization](../03_methods_reference/NILEARN_CONNECTIVITY_GUIDE.md)

---

## Phase 2: Functional Connectivity [PLANNED]

### Status: Planning

### Goals
1. Compute ROI-to-ROI functional connectivity matrices
2. Perform seed-based correlation analyses
3. Calculate graph theory metrics (modularity, efficiency, etc.)
4. Compare connectivity across conditions and sessions

### Implementation
- **Software**: CONN toolbox (MATLAB)
- **Platform**: Monash M3 HPC cluster
- **Approach**: Batch scripting via `conn_batch`

### Key Analyses

| Analysis | CONN Method | Output |
|----------|-------------|--------|
| ROI-to-ROI | RRC | Connectivity matrices |
| Seed-based | SBC | Correlation maps |
| Graph metrics | Graph theory | Network measures |
| Group comparison | Second-level GLM | Statistical maps |

### Documentation
- [CONN Toolbox Reference](CONN_TOOLBOX_REFERENCE.md)
- [M3 HPC Guide](M3_HPC_GUIDE.md)

---

## Phase 3: Dynamic Effective Connectivity [PLANNED]

### Status: Future

### Goals
1. Characterize time-varying connectivity patterns
2. Identify dynamic connectivity states
3. Relate connectivity dynamics to behavioral measures
4. Compare dynamic patterns across conditions

### Implementation
- **Software**: CONN toolbox (MATLAB)
- **Platform**: Monash M3 HPC cluster

### Key Analyses

| Analysis | CONN Method | Parameters |
|----------|-------------|------------|
| Sliding window | Temporal decomposition | 100s windows, 25s steps |
| Dynamic ICA | dyn-ICA | 20 components, 30s smoothing |
| Modulated connectivity | gPPI | Task-specific modulation |

### Dynamic Connectivity Measures

1. **dvSBC**: Dynamic variability in seed-based connectivity
2. **dvRRC**: Dynamic variability in ROI-to-ROI connectivity
3. **dyn-ICA**: Data-driven dynamic component analysis

### Documentation
- [CONN Toolbox Reference](CONN_TOOLBOX_REFERENCE.md) - See dynamic connectivity section
- [CONN Dynamic Connectivity](https://web.conn-toolbox.org/fmri-methods/connectivity-measures/dynamic-connectivity)

---

## Implementation Roadmap

### Immediate Tasks

- [ ] Test SSH connection to M3
- [ ] Verify MATLAB/SPM availability on M3
- [ ] Install CONN toolbox (or verify module)
- [ ] Transfer BIDS data to M3
- [ ] Create initial CONN batch script

### Phase 2 Tasks

- [ ] Set up CONN project structure
- [ ] Configure preprocessing pipeline
- [ ] Run denoising
- [ ] Compute first-level connectivity
- [ ] Run second-level group analyses
- [ ] Export results for visualization

### Phase 3 Tasks

- [ ] Configure sliding window parameters
- [ ] Set up dyn-ICA analysis
- [ ] Run dynamic connectivity analyses
- [ ] Extract dynamic measures
- [ ] Correlate with behavioral data

---

## Data Requirements

### Input Data (BIDS Format)

```
BIDS/
├── sub-01/
│   ├── anat/
│   │   └── sub-01_T1w.nii.gz
│   └── func/
│       ├── sub-01_task-rest_bold.nii.gz
│       ├── sub-01_task-music_bold.nii.gz
│       ├── sub-01_task-movie_bold.nii.gz
│       └── sub-01_task-meditation_bold.nii.gz
├── sub-02/
│   └── ...
└── participants.tsv
```

### ROI Definition

Using same ROIs as DCM analysis:
- Left/Right DLPFC
- Left/Right Insula
- Left/Right Hippocampus
- Posterior Cingulate Cortex (PCC)

---

## Expected Outputs

### Phase 2 Outputs

```
conn_analysis/
├── conn_project.mat              # CONN project file
├── results/
│   ├── firstlevel/
│   │   ├── SBC_01/              # Seed-based correlations
│   │   └── RRC_01/              # ROI-to-ROI results
│   └── secondlevel/
│       └── group_comparisons/
└── data/
    └── ROIs/
```

### Phase 3 Outputs

```
conn_analysis/
├── results/
│   ├── firstlevel/
│   │   ├── DYN_01/              # Dynamic ICA results
│   │   └── sliding_window/      # Windowed connectivity
│   └── secondlevel/
│       └── dynamic_comparisons/
```

---

## Resources

### Software

- [CONN Toolbox](https://web.conn-toolbox.org)
- [SPM12](https://www.fil.ion.ucl.ac.uk/spm/)
- [Monash M3](https://docs.erc.monash.edu/M3/)

### Key References

- Whitfield-Gabrieli & Nieto-Castanon (2012). CONN: A functional connectivity toolbox
- [CONN Documentation](https://web.conn-toolbox.org/resources/conn-documentation)
- [Andy's Brain Book - CONN](https://andysbrainbook.readthedocs.io/en/latest/FunctionalConnectivity/CONN_Overview.html)

---

*Last updated: 2025-12-01*
