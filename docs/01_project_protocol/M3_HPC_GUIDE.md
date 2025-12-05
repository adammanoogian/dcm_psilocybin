# Monash M3 HPC Guide for Connectivity Analysis

Guide for running CONN toolbox batch scripts on Monash M3 cluster via SSH.

---

## Connecting to M3

### SSH Connection

```bash
# Basic connection
ssh username@m3.massive.org.au

# Replace 'username' with your HPC ID (not Monash authcate)
```

### Windows Users (PuTTY)

1. Download PuTTY
2. Configure:
   - Host Name: `username@m3.massive.org.au`
   - Connection type: SSH
3. Click Open and authenticate with HPC ID password

### SSH Key Authentication (Recommended)

```bash
# Generate key pair
ssh-keygen -t ed25519

# Add to ssh-agent
ssh-add ~/.ssh/id_ed25519

# Copy public key to M3 via Strudel2 terminal
```

### Successful Connection

You'll see: `[user@m3-login1 ~]$`

---

## M3 Environment Setup

### Loading MATLAB

```bash
# Check available MATLAB versions
module avail matlab

# Load MATLAB (example version)
module load matlab/r2023a

# Set cache directory (prevents conflicts)
export MCR_CACHE_ROOT=$TMPDIR
```

### Loading SPM/CONN

```bash
# Check if SPM module exists
module avail spm

# If available:
module load spm/12

# Otherwise, set path in MATLAB manually (see below)
```

### Manual CONN Setup in MATLAB

If CONN is not a module, add to your MATLAB startup:

```matlab
% Add SPM to path
addpath('/path/to/spm12');

% Add CONN to path
addpath('/path/to/conn');

% Initialize
spm('defaults', 'fmri');
```

---

## Job Submission with SLURM

### Basic sbatch Script Template

Create file: `conn_batch_job.slurm`

```bash
#!/bin/bash
#SBATCH --job-name=conn_analysis
#SBATCH --account=YOUR_PROJECT_ID
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --mail-user=your.email@monash.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --output=conn_%j.out
#SBATCH --error=conn_%j.err

# Load modules
module load matlab/r2023a

# Set environment
export MCR_CACHE_ROOT=$TMPDIR

# Run MATLAB batch script
matlab -nodisplay -nosplash -r "run('/path/to/conn_batch_script.m'); exit;"
```

### SLURM Directives Reference

| Directive | Description | Example |
|-----------|-------------|---------|
| `--job-name` | Job identifier | `conn_analysis` |
| `--account` | Project allocation | `nq46` |
| `--time` | Max runtime | `24:00:00` (max 7 days) |
| `--ntasks` | Number of tasks | `1` |
| `--cpus-per-task` | CPUs per task | `8` |
| `--mem` | Total memory | `64G` |
| `--mem-per-cpu` | Memory per CPU | `4G` |
| `--partition` | Queue/partition | `m3a`, `m3c`, `m3d`, `m3f` |
| `--mail-user` | Email address | `user@monash.edu` |
| `--mail-type` | Email triggers | `BEGIN,END,FAIL,ALL` |
| `--output` | Stdout file | `job_%j.out` |
| `--error` | Stderr file | `job_%j.err` |

### Time Format

```bash
--time=15              # 15 minutes
--time=1:30:00         # 1 hour 30 minutes
--time=2-12:00:00      # 2 days 12 hours
```

### Submitting Jobs

```bash
# Submit job
sbatch conn_batch_job.slurm

# Check job status
squeue -u $USER

# Cancel job
scancel JOBID

# Cancel all your jobs
scancel -u $USER
```

---

## CONN Batch Script for M3

### Complete MATLAB Script: `conn_batch_m3.m`

```matlab
%% CONN Batch Script for M3 HPC
% Functional connectivity analysis pipeline
% Run via: matlab -nodisplay -nosplash -r "run('conn_batch_m3.m'); exit;"

clear BATCH;

%% Paths (adjust for your M3 setup)
project_dir = '/home/username/project/';
bids_dir = fullfile(project_dir, 'BIDS');
output_dir = fullfile(project_dir, 'conn_analysis');

%% Project Configuration
BATCH.filename = fullfile(output_dir, 'conn_project.mat');
BATCH.Setup.isnew = 1;
BATCH.Setup.nsubjects = 20;  % Adjust to your N
BATCH.Setup.RT = 2;          % TR in seconds

%% Data Specification
% Use conn_dir for BIDS pattern matching
functional_files = cellstr(conn_dir(fullfile(bids_dir, 'sub-*/func/*_bold.nii.gz')));
structural_files = cellstr(conn_dir(fullfile(bids_dir, 'sub-*/anat/*_T1w.nii')));

for nsub = 1:BATCH.Setup.nsubjects
    BATCH.Setup.functionals{nsub}{1} = functional_files{nsub};
    BATCH.Setup.structurals{nsub} = structural_files{nsub};
end

%% ROI Setup
BATCH.Setup.rois.files{1} = '/path/to/atlas.nii';
BATCH.Setup.rois.multiplelabels = 1;

%% Preprocessing
BATCH.Setup.preprocessing.steps = 'default_mni';
BATCH.Setup.preprocessing.fwhm = 6;
BATCH.Setup.done = 1;
BATCH.Setup.overwrite = 'Yes';

%% Denoising
BATCH.Denoising.filter = [0.01, 0.1];
BATCH.Denoising.detrending = 1;
BATCH.Denoising.done = 1;
BATCH.Denoising.overwrite = 'Yes';

%% First-Level Analysis
BATCH.Analysis.type = 3;  % ROI-to-ROI and Seed-to-Voxel
BATCH.Analysis.measure = 1;  % Correlation
BATCH.Analysis.done = 1;

%% Parallel Processing (for M3)
% Set N=0 for serial processing, or configure for SLURM
BATCH.parallel.N = 0;  % Run serially within SLURM job

%% Execute
fprintf('Starting CONN batch processing...\n');
fprintf('Project: %s\n', BATCH.filename);
fprintf('Subjects: %d\n', BATCH.Setup.nsubjects);

conn_batch(BATCH);

fprintf('CONN batch processing complete.\n');
```

---

## File Transfer

### SCP (Command Line)

```bash
# Upload to M3
scp -r local_folder/ username@m3.massive.org.au:/home/username/project/

# Download from M3
scp -r username@m3.massive.org.au:/home/username/results/ ./local_results/
```

### rsync (Recommended for Large Data)

```bash
# Sync to M3 (with progress)
rsync -avzP local_folder/ username@m3.massive.org.au:/home/username/project/

# Sync from M3
rsync -avzP username@m3.massive.org.au:/home/username/results/ ./local_results/
```

---

## Directory Structure on M3

```
/home/username/
├── project/
│   ├── BIDS/                    # BIDS-formatted input data
│   │   ├── sub-01/
│   │   │   ├── anat/
│   │   │   └── func/
│   │   └── sub-02/
│   ├── conn_analysis/           # CONN output directory
│   │   └── conn_project.mat
│   ├── scripts/
│   │   ├── conn_batch_m3.m
│   │   └── conn_batch_job.slurm
│   └── logs/
```

---

## Monitoring and Debugging

### Check Job Status

```bash
# Your jobs
squeue -u $USER

# Detailed job info
scontrol show job JOBID

# Job history
sacct -j JOBID
```

### View Output Logs

```bash
# Real-time monitoring
tail -f conn_JOBID.out

# Check errors
cat conn_JOBID.err
```

### Interactive Session (Debugging)

```bash
# Request interactive node
srun --time=1:00:00 --mem=16G --cpus-per-task=4 --pty bash

# Load MATLAB and test
module load matlab/r2023a
matlab -nodisplay
```

---

## Typical Workflow

1. **Connect to M3**
   ```bash
   ssh username@m3.massive.org.au
   ```

2. **Transfer data**
   ```bash
   rsync -avzP ./BIDS/ username@m3.massive.org.au:/home/username/project/BIDS/
   ```

3. **Create/edit batch scripts**
   ```bash
   nano scripts/conn_batch_m3.m
   nano scripts/conn_batch_job.slurm
   ```

4. **Submit job**
   ```bash
   sbatch scripts/conn_batch_job.slurm
   ```

5. **Monitor progress**
   ```bash
   squeue -u $USER
   tail -f conn_*.out
   ```

6. **Download results**
   ```bash
   rsync -avzP username@m3.massive.org.au:/home/username/project/conn_analysis/ ./results/
   ```

---

## Resources

### Monash eResearch Documentation

- [M3 Overview](https://docs.erc.monash.edu/M3/)
- [Connecting to M3 via SSH](https://docs.erc.monash.edu/M3/ConnectingToM3/SSH/)
- [Specifying SLURM Resources](https://docs.erc.monash.edu/M3/RunningJobsOnM3/SpecifyingResources/)
- [MATLAB on MonARCH](https://docs.erc.monash.edu/MonARCH/software/matlab/)
- [Getting Started](https://docs.erc.monash.edu/M3/GettingStarted/)

### Support

- Email: help@massive.org.au
- Request software: Submit ticket with software name, version, URL, urgency

---

*Last updated: 2025-12-01*
