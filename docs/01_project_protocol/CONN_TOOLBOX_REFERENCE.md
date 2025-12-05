# CONN Toolbox Batch Scripting Reference

Reference documentation for CONN toolbox batch processing for functional and dynamic effective connectivity analysis.

---

## Overview

CONN is a MATLAB-based fMRI connectivity toolbox offering:
- **Functional connectivity**: Seed-based correlations (SBC), ROI-to-ROI connectivity (RRC)
- **Dynamic connectivity**: Sliding-window analyses, dynamic ICA (dyn-ICA)
- **Effective connectivity**: Generalized PPI (gPPI), semipartial correlations

---

## Batch Scripting Syntax

### Three Invocation Methods

```matlab
% Method 1: Structure-based
clear BATCH;
BATCH.Setup.RT = 2;
conn_batch(BATCH);

% Method 2: Field-value pairs
conn_batch('Setup.RT', 2, 'Setup.nsubjects', 20);

% Method 3: File-based
conn_batch('mybatchfile.mat');   % MATLAB .mat file
conn_batch('mybatchfile.json');  % JSON configuration
conn_batch('mybatchfile.m');     % MATLAB script
```

---

## Core BATCH Structure Fields

| Field | Description |
|-------|-------------|
| `filename` | Project file path (conn_*.mat) |
| `subjects` | Subset of subjects to process |
| `parallel` | Parallelization configuration |
| `Setup` | Experiment setup and preprocessing |
| `Denoising` | Confound removal and filtering |
| `Analysis` | First-level connectivity analyses |
| `Results` | Second-level group analyses |
| `QA` | Quality assurance plots |
| `dynAnalysis` | Dynamic ICA analyses |

---

## Complete Batch Script Template

```matlab
%% CONN Batch Script - Full Pipeline
% Template for functional connectivity analysis

clear BATCH;

%% Project Setup
BATCH.filename = '/path/to/conn_project.mat';
BATCH.Setup.isnew = 1;                    % Create new project
BATCH.Setup.nsubjects = 20;               % Number of subjects
BATCH.Setup.RT = 2;                       % TR in seconds

%% Data Specification
% Functional data (cell array: subjects x sessions)
BATCH.Setup.functionals{1}{1} = '/path/to/sub-01/func/bold.nii';
% Or use conn_dir for pattern matching:
% BATCH.Setup.functionals = cellstr(conn_dir('sub-*/func/*_bold.nii.gz'));

% Structural data (cell array: one per subject)
BATCH.Setup.structurals{1} = '/path/to/sub-01/anat/T1w.nii';

%% ROI Specification
BATCH.Setup.rois.files{1} = '/path/to/atlas.nii';
BATCH.Setup.rois.multiplelabels = 1;      % Atlas with multiple labels

%% Conditions (for task-based connectivity)
BATCH.Setup.conditions.names = {'rest', 'task1', 'task2'};
BATCH.Setup.conditions.onsets{1}{1}{1} = 0;           % Subject 1, Session 1, Condition 1
BATCH.Setup.conditions.durations{1}{1}{1} = inf;      % Entire session

%% Preprocessing Pipeline
BATCH.Setup.preprocessing.steps = 'default_mni';      % Standard MNI pipeline
BATCH.Setup.preprocessing.sliceorder = 'interleaved (Siemens)';
BATCH.Setup.preprocessing.fwhm = 6;                   % Smoothing kernel (mm)
BATCH.Setup.done = 1;
BATCH.Setup.overwrite = 'Yes';

%% Denoising
BATCH.Denoising.filter = [0.01, 0.1];     % Band-pass filter (Hz)
BATCH.Denoising.detrending = 1;           % Linear detrending
BATCH.Denoising.confounds.names = {'White Matter', 'CSF', 'realignment'};
BATCH.Denoising.done = 1;
BATCH.Denoising.overwrite = 'Yes';

%% First-Level Analysis
BATCH.Analysis.type = 3;                  % 1=ROI-to-ROI, 2=Seed-to-Voxel, 3=Both
BATCH.Analysis.measure = 1;               % 1=correlation, 2=regression
BATCH.Analysis.done = 1;

%% Execute Pipeline
conn_batch(BATCH);
```

---

## Dynamic Connectivity Analysis

### Sliding Window Analysis

```matlab
%% Setup sliding window decomposition
% Configure in Setup.conditions with temporal decomposition
% Default: 100s windows, 25s steps, 75s overlap

% Results location:
% conn_project/results/firstlevel/SBC_01/corr_Subject001_Condition012_Source134.nii
% Where Condition012 = time window 12, Source134 = ROI index
```

### Dynamic ICA (dyn-ICA)

```matlab
%% Dynamic ICA Configuration
BATCH.dynAnalysis.done = 1;
BATCH.dynAnalysis.name = 'DYN_01';
BATCH.dynAnalysis.sources = {'ROI1', 'ROI2', 'ROI3'};  % Specific ROIs (or leave empty for all)
BATCH.dynAnalysis.factors = 20;           % Number of independent components
BATCH.dynAnalysis.window = 30;            % Temporal smoothing FWHM (seconds)
BATCH.dynAnalysis.overwrite = 1;

conn_batch(BATCH);
```

### dyn-ICA Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `dynAnalysis.done` | Run analysis (1) or define only (0) | 0 |
| `dynAnalysis.name` | Analysis identifier | 'DYN_01' |
| `dynAnalysis.sources` | Cell array of ROI names | All ROIs |
| `dynAnalysis.factors` | Number of components | 20 |
| `dynAnalysis.window` | Temporal smoothing FWHM (s) | 30 |
| `dynAnalysis.overwrite` | Overwrite existing results | 1 |

---

## Preprocessing Pipeline Options

### Predefined Pipelines

| Pipeline | Description |
|----------|-------------|
| `default_mni` | Standard MNI-space processing |
| `default_mnifield` | MNI with field map correction |
| `default_ss` | Subject-space processing |
| `default_ssfield` | Subject-space with field map |

### Individual Preprocessing Steps

```matlab
% Available individual steps:
BATCH.Setup.preprocessing.steps = {
    'functional_center'           % Center functional volumes
    'functional_slicetime'        % Slice-timing correction
    'functional_realign'          % Motion correction
    'functional_art'              % Artifact detection
    'functional_segment&normalize' % Combined segmentation/normalization
    'functional_smooth'           % Spatial smoothing
    'structural_center'           % Center structural
    'structural_segment'          % Tissue segmentation
    'structural_normalize'        % Normalize to MNI
};
```

---

## Parallelization (HPC)

```matlab
%% Parallel Processing Configuration
BATCH.parallel.N = 8;                     % Number of parallel jobs
BATCH.parallel.profile = 'Slurm';         % HPC profile name

% For local processing (no parallelization):
BATCH.parallel.N = 0;
```

---

## Quality Assurance Plots

```matlab
%% QA Plot Types
BATCH.QA.plots = 1;          % Normalization check
BATCH.QA.plots = 2;          % Registration validation
BATCH.QA.plots = 3;          % Coregistration check
BATCH.QA.plots = 4;          % Temporal consistency
BATCH.QA.plots = 5;          % Denoising assessment
```

---

## Example Scripts (Included with CONN)

| Script | Description |
|--------|-------------|
| `conn_batch.m` | Main batch function with documentation |
| `conn_batch_workshop_nyudataset.m` | NYU workshop example |
| `conn_batch_humanconnectomeproject.m` | HCP processing |
| `conn_batchexample_qcplot.m` | QA plotting example |

---

## Resources

### Official Documentation

- [CONN Toolbox Home](https://web.conn-toolbox.org)
- [conn_batch Documentation](https://web.conn-toolbox.org/resources/conn-documentation/conn_batch)
- [Dynamic Connectivity Guide](https://web.conn-toolbox.org/fmri-methods/connectivity-measures/dynamic-connectivity)
- [CONN Tutorials](https://web.conn-toolbox.org/tutorials)

### Code Repositories

- [CONN GitHub (alfnie/conn)](https://github.com/alfnie/conn/blob/master/conn_batch.m)
- [NITRC Downloads](https://www.nitrc.org/projects/conn)
- [MATLAB File Exchange](https://www.mathworks.com/matlabcentral/fileexchange/78700-conn)

### Tutorials

- [Andy's Brain Book - CONN Scripting](https://andysbrainbook.readthedocs.io/en/latest/FunctionalConnectivity/CONN_ShortCourse/CONN_12_Scripting.html)
- [Andy's Brain Book - Dynamic Connectivity](https://andysbrainbook.readthedocs.io/en/latest/FunctionalConnectivity/CONN_ShortCourse/CONN_AppendixE_DynamicConnectivity.html)
- [Batch Processing Gist Example](https://gist.github.com/A2ed/3114405e2eb216f53a6b)

---

## Project Integration Notes

### Current Project Status

- **DCM Analysis**: Complete (MATLAB/SPM, PEB results in `massive_output_local/`)
- **Visualization**: Complete (Python/nilearn pipeline)
- **Functional Connectivity**: Planned (CONN toolbox)
- **Effective Connectivity**: Planned (CONN gPPI/dyn-ICA)

### Data Location on M3

```
/path/to/project/
├── BIDS/                    # BIDS-formatted input data
├── derivatives/             # Preprocessed data
└── conn_analysis/           # CONN project files (to be created)
```

### Execution Environment

- **HPC**: Monash M3 cluster
- **MATLAB**: Available via module system
- **CONN**: Requires installation in MATLAB path

---

*Last updated: 2025-12-01*
