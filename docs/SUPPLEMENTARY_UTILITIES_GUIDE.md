# Supplementary Utilities Guide

## Overview

These utilities generate supplementary figures for methods sections, presentations, and documentation. They are **NOT** part of the main analysis pipeline but provide supporting visualizations.

**Location:** `scripts/analysis/utilities/`

---

## General Utilities

### combine_plots.py

**Purpose:** Generic SVG/PNG combiner for creating figure panels

**Output:** Combined SVG/PNG files

**Use Case:** Manual figure assembly, one-off combinations outside the main pipeline

**Usage:**
```bash
python scripts/analysis/utilities/combine_plots.py
```

---

## Methods/Documentation Figures

### generate_network_diagram.py

**Purpose:** Creates conceptual DCM network diagram showing theoretical architecture

**Output:** `figures/images/dcm_network_diagram.*`

**Use Case:** Methods section - illustrates the theoretical network model

**Usage:**
```bash
python scripts/analysis/utilities/generate_network_diagram.py
```

---

### generate_dcm_network_figure.py

**Purpose:** Generates detailed DCM architecture diagrams with directional arrows

**Output:** Multi-view network diagrams

**Use Case:** Methods section - detailed architecture views showing connectivity directions

**Usage:**
```bash
python scripts/analysis/utilities/generate_dcm_network_figure.py
```

---

### generate_example_bold_timeseries.py

**Purpose:** Creates simulated BOLD signal timeseries plots

**Output:** `figures/images/example_bold_timeseries_LH.*`

**Use Case:** Supplementary methods - example data visualization

**Usage:**
```bash
python scripts/analysis/utilities/generate_example_bold_timeseries.py
```

---

### create_colorkey_images.py

**Purpose:** Generates color scale reference images for figure legends

**Output:** `figures/images/colorkey_*.png`

**Use Case:** Figure legends - helps readers interpret color scales in connectivity matrices

**Usage:**
```bash
python scripts/analysis/utilities/create_colorkey_images.py
```

---

## ROI Anatomical Visualizations

### create_roi_anatomy_figure.py

**Purpose:** Comprehensive ROI anatomical reference generator

**Output:** PNG + SVG + HTML (interactive) + GIF (6 views)

**Use Case:** Primary anatomical reference figure for the paper

**Usage:**
```bash
python scripts/analysis/utilities/create_roi_anatomy_figure.py
```

---

### create_roi_glass_brain.py

**Purpose:** Glass brain overlays showing ROI locations

**Output:** Multi-view transparent glass brain images

**Use Case:** Publication-quality transparent brain views

**Usage:**
```bash
python scripts/analysis/utilities/create_roi_glass_brain.py
```

---

### create_roi_dorsal_lateral_gif.py

**Purpose:** Animated rotating brain view

**Output:** GIF animation

**Use Case:** PowerPoint presentations, talks

**Usage:**
```bash
python scripts/analysis/utilities/create_roi_dorsal_lateral_gif.py
```

---

### generate_brain_network_multiview.py

**Purpose:** Multi-angle brain views showing nodes only (no edges)

**Output:** Multi-angle SVG/PNG

**Use Case:** Clean node-only visualization for diagrams

**Usage:**
```bash
python scripts/analysis/utilities/generate_brain_network_multiview.py
```

---

## Quick Reference

| Script | Output Type | Primary Use |
|--------|-------------|-------------|
| `combine_plots.py` | SVG/PNG | Manual figure assembly |
| `generate_network_diagram.py` | SVG/PNG | Methods - network model |
| `generate_dcm_network_figure.py` | Multi-view | Methods - architecture |
| `generate_example_bold_timeseries.py` | SVG/PNG | Supplementary - example data |
| `create_colorkey_images.py` | PNG | Figure legends |
| `create_roi_anatomy_figure.py` | PNG/SVG/HTML/GIF | Anatomical reference |
| `create_roi_glass_brain.py` | Multi-view PNG | Publication figures |
| `create_roi_dorsal_lateral_gif.py` | GIF | Presentations |
| `generate_brain_network_multiview.py` | SVG/PNG | Node diagrams |

---

## Note on Main Pipeline

These utilities are supplementary. For the main analysis pipeline, use:

```bash
# Full pipeline
python scripts/analysis/00_run_full_pipeline.py --all

# PEB analysis only
python scripts/analysis/00_run_full_pipeline.py --peb

# Paper figures
python scripts/generate_figures.py --paper
```

See `docs/02_pipeline_guide/` for main pipeline documentation.
