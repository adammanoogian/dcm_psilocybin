# Figure Organization Guide

Comprehensive guide to the organized connectivity visualization figures following overleaf paper naming conventions.

## Directory Structure

```
figures/organized/
├── m1_rest/              # REST condition (7 figures)
├── m2_music/             # MUSIC condition (7 figures)
├── m3_movie/             # MOVIE condition (5 figures)
├── m4_meditation/        # MEDITATION condition (3 figures)
├── contrasts/            # Task contrasts (3 figures)
└── h01_multi_condition/  # Multi-condition comparisons (6 figures)
```

**Total: 31 systematically organized figures**

---

## Naming Convention

### Model Structure
- **m1** = REST
- **m2** = MUSIC
- **m3** = MOVIE
- **m4** = MEDITATION

### Letter Codes
- **a** = Session change (Post - Pre psilocybin)
- **b** = Behavioral association (11D-ASC composite sensory)
- **c** = Behavioral association (5D-ASC auditory) - *supplementary*

### Number Variants
- Base: Full network view
- **1**: Network-specific (e.g., dlPFC outgoing)
- **2**: Network-specific (e.g., hippocampus)

### New Hypotheses (h01, h02, etc.)
- **h01**: Multi-condition comparisons
- Letter variants for different visualizations:
  - `h01-a`, `h01-c`, `h01-e`: Overlay visualization
  - `h01-b`, `h01-d`, `h01-f`: Side-by-side panels

---

## Complete Figure Catalog

### M1: REST CONDITION

**Location**: `figures/organized/m1_rest/`

#### M1-A: Rest Session Change (Post - Pre Psilocybin)

| Figure | Description | Script | Data File |
|--------|-------------|--------|-----------|
| `m1-a_change_full.png` | Full network connectivity (lyrz view) | `generate_all_nilearn_figures.py` | `PEB_change_-ses-01-ses-02_-task-rest_cov-_noFD.mat` |
| `m1-a1_change_dlpfc.png` | dlPFC outgoing connections | `generate_all_nilearn_figures.py` | Same as above |
| `m1-a2_change_hippocampus.png` | Hippocampus bidirectional | `generate_all_nilearn_figures.py` | Same as above |

**Colormap**: `coolwarm` (diverging, centered at 0)
**Threshold**: Pp > 0.99
**Interpretation**: Blue = decreased connectivity, Red = increased connectivity

#### M1-B: Rest Behavioral Association (11D-ASC Composite Sensory)

| Figure | Description | Script | Data File |
|--------|-------------|--------|-----------|
| `m1-b_behavioral_asc11_full.png` | Full network | `generate_all_nilearn_figures.py` | `PEB_behav_associations_-ses-02_-task-rest_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_noFD.mat` |
| `m1-b1_behavioral_asc11_hipp.png` | Hippocampus network | `generate_all_nilearn_figures.py` | Same as above |

**Colormap**: `PRGn` (Purple-Green, diverging)
**Threshold**: Pp > 0.99
**Interpretation**: Purple = negative β, Green = positive β

#### M1-C: Rest Behavioral Association (5D-ASC Auditory) - *Supplementary*

| Figure | Description | Script | Data File |
|--------|-------------|--------|-----------|
| `m1-c_behavioral_asc5_full.png` | Full network | `generate_all_nilearn_figures.py` | `PEB_behav_associations_-ses-02_-task-rest_cov-ASC5_AUDITORY_noFD.mat` |
| `m1-c1_behavioral_asc5_hipp.png` | Hippocampus network | `generate_all_nilearn_figures.py` | Same as above |

**Colormap**: `PRGn`
**Threshold**: Pp > 0.99

---

### M2: MUSIC CONDITION

**Location**: `figures/organized/m2_music/`

#### M2-A: Music Session Change

| Figure | Description | Script | Data File |
|--------|-------------|--------|-----------|
| `m2-a_change_full.png` | Full network connectivity | `generate_all_nilearn_figures.py` | `PEB_change_-ses-01-ses-02_-task-music_cov-_noFD.mat` |
| `m2-a1_change_dlpfc.png` | dlPFC outgoing connections | `generate_all_nilearn_figures.py` | Same as above |
| `m2-a2_change_hippocampus.png` | Hippocampus bidirectional | `generate_all_nilearn_figures.py` | Same as above |

**Colormap**: `coolwarm`
**Threshold**: Pp > 0.99

#### M2-B: Music Behavioral Association (11D-ASC Composite Sensory)

| Figure | Description | Script | Data File |
|--------|-------------|--------|-----------|
| `m2-b_behavioral_asc11_full.png` | Full network | `generate_all_nilearn_figures.py` | `PEB_behav_associations_-ses-02_-task-music_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_noFD.mat` |
| `m2-b1_behavioral_asc11_hipp.png` | Hippocampus network | `generate_all_nilearn_figures.py` | Same as above |

**Colormap**: `PRGn`
**Threshold**: Pp > 0.99

#### M2-C: Music Behavioral Association (5D-ASC Auditory)

| Figure | Description | Script | Data File |
|--------|-------------|--------|-----------|
| `m2-c_behavioral_asc5_full.png` | Full network | `generate_all_nilearn_figures.py` | `PEB_behav_associations_-ses-02_-task-music_cov-ASC5_AUDITORY_noFD.mat` |
| `m2-c1_behavioral_asc5_hipp.png` | Hippocampus network | `generate_all_nilearn_figures.py` | Same as above |

**Colormap**: `PRGn`
**Threshold**: Pp > 0.99

---

### M3: MOVIE CONDITION

**Location**: `figures/organized/m3_movie/`

#### M3-A: Movie Session Change

| Figure | Description | Script | Data File |
|--------|-------------|--------|-----------|
| `m3-a_change_full.png` | Full network connectivity | `generate_all_nilearn_figures.py` | `PEB_change_-ses-01-ses-02_-task-movie_cov-_noFD.mat` |
| `m3-a1_change_dlpfc.png` | dlPFC outgoing connections | `generate_all_nilearn_figures.py` | Same as above |
| `m3-a2_change_hippocampus.png` | Hippocampus bidirectional | `generate_all_nilearn_figures.py` | Same as above |

**Colormap**: `coolwarm`
**Threshold**: Pp > 0.99

#### M3-B: Movie Behavioral Association (11D-ASC Composite Sensory)

| Figure | Description | Script | Data File |
|--------|-------------|--------|-----------|
| `m3-b_behavioral_asc11_full.png` | Full network | `generate_all_nilearn_figures.py` | `PEB_behav_associations_-ses-02_-task-movie_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_noFD.mat` |
| `m3-b1_behavioral_asc11_hipp.png` | Hippocampus network | `generate_all_nilearn_figures.py` | Same as above |

**Colormap**: `PRGn`
**Threshold**: Pp > 0.99

*Note: No 5D-ASC auditory data available for movie condition*

---

### M4: MEDITATION CONDITION

**Location**: `figures/organized/m4_meditation/`

#### M4-A: Meditation Session Change

| Figure | Description | Script | Data File |
|--------|-------------|--------|-----------|
| `m4-a_change_full.png` | Full network connectivity | `generate_all_nilearn_figures.py` | `PEB_change_-ses-01-ses-02_-task-meditation_cov-_noFD.mat` |
| `m4-a1_change_dlpfc.png` | dlPFC outgoing connections | `generate_all_nilearn_figures.py` | Same as above |
| `m4-a2_change_hippocampus.png` | Hippocampus bidirectional | `generate_all_nilearn_figures.py` | Same as above |

**Colormap**: `coolwarm`
**Threshold**: Pp > 0.99

*Note: No behavioral data currently available for meditation condition*

---

### CONTRASTS

**Location**: `figures/organized/contrasts/`

#### Task Contrasts (Session 2)

| Figure | Description | Script | Data File |
|--------|-------------|--------|-----------|
| `contrast_rest_vs_music.png` | Rest - Music | `generate_all_nilearn_figures.py` | `PEB_contrast_-ses-02_-task-rest-task-music_cov-_noFD.mat` |
| `contrast_rest_vs_movie.png` | Rest - Movie | `generate_all_nilearn_figures.py` | `PEB_contrast_-ses-02_-task-rest-task-movie_cov-_noFD.mat` |
| `contrast_music_vs_movie.png` | Music - Movie | `generate_all_nilearn_figures.py` | `PEB_contrast_-ses-02_-task-music-task-movie_cov-_noFD.mat` |

**Colormap**: `RdYlBu_r` (Red-Yellow-Blue reversed)
**Threshold**: Pp > 0.99
**Interpretation**: Red = stronger in first task, Blue = stronger in second task

---

### H01: MULTI-CONDITION COMPARISONS (New Hypotheses)

**Location**: `figures/organized/h01_multi_condition/`

#### H01-A: All Tasks Session Change - Overlay

| Figure | Description | Script |
|--------|-------------|--------|
| `h01-a_all_tasks_overlay.png` | All 4 tasks overlaid with color-coded edges | `generate_combined_nilearn_figures.py` |

**Method**: Overlay visualization using `plot_overlay_connectome()`
**Edge colormaps**: Reds (Rest), Blues (Music), Greens (Movie), Purples (Meditation)
**Edge alpha**: 0.6 (semi-transparent)
**Display mode**: `lyrz` (4 views)

#### H01-B: All Tasks Session Change - Side-by-Side

| Figure | Description | Script |
|--------|-------------|--------|
| `h01-b_all_tasks_sidebyside.png` | 2×2 grid with separate brain view per task | `generate_combined_nilearn_figures.py` |

**Method**: Side-by-side panels using `plot_sidebyside_connectome()`
**Layout**: 2×2 grid
**Colormap**: `coolwarm` (shared scale across all panels)
**Display mode**: `z` (axial view only)

#### H01-C: ASC Auditory (Rest vs Music) - Overlay

| Figure | Description | Script |
|--------|-------------|--------|
| `h01-c_auditory_rest_music_overlay.png` | Rest vs Music auditory associations overlaid | `generate_combined_nilearn_figures.py` |

**Method**: Overlay visualization
**Edge colormaps**: Reds (Rest), Blues (Music)
**Edge alpha**: 0.7

#### H01-D: ASC Auditory (Rest vs Music) - Side-by-Side

| Figure | Description | Script |
|--------|-------------|--------|
| `h01-d_auditory_rest_music_sidebyside.png` | Rest vs Music side-by-side comparison | `generate_combined_nilearn_figures.py` |

**Method**: Side-by-side panels
**Layout**: 1×2
**Colormap**: `PRGn` (shared scale)

#### H01-E: ASC Sensory (All Tasks) - Overlay

| Figure | Description | Script |
|--------|-------------|--------|
| `h01-e_sensory_all_tasks_overlay.png` | Rest/Music/Movie sensory associations overlaid | `generate_combined_nilearn_figures.py` |

**Method**: Overlay visualization
**Edge colormaps**: Reds (Rest), Blues (Music), Greens (Movie)
**Edge alpha**: 0.6

#### H01-F: ASC Sensory (All Tasks) - Side-by-Side

| Figure | Description | Script |
|--------|-------------|--------|
| `h01-f_sensory_all_tasks_sidebyside.png` | Rest/Music/Movie side-by-side comparison | `generate_combined_nilearn_figures.py` |

**Method**: Side-by-side panels
**Layout**: 2×2 (3 panels used)
**Colormap**: `PRGn` (shared scale)

---

## How to Generate Figures

### Regenerate All Single-Condition Figures (M1-M4 + Contrasts)

```bash
cd /path/to/dcm_psilocybin
conda activate dcm_psilocybin_clean
python scripts/analysis/generate_all_nilearn_figures.py
```

This generates:
- All M1 figures (REST: session changes + behavioral)
- All M2 figures (MUSIC: session changes + behavioral)
- All M3 figures (MOVIE: session changes + behavioral)
- All M4 figures (MEDITATION: session changes)
- All contrast figures (task comparisons)

**Output**: `figures/nilearn/`

### Regenerate All Multi-Condition Figures (H01)

```bash
python scripts/analysis/generate_combined_nilearn_figures.py
```

This generates:
- All H01 figures (multi-condition comparisons)

**Output**: `figures/nilearn/combined/`

### Organize All Figures

```bash
python scripts/analysis/organize_figures.py
```

This copies and renames all figures to organized structure.

**Output**: `figures/organized/`

---

## Technical Details

### Matrix Convention
- **MATLAB DCM**: `Ep[i,j]` = FROM j TO i (rows=targets, cols=sources)
- **Nilearn**: `matrix[i,j]` = FROM i TO j (rows=sources, cols=targets)
- **Solution**: Transpose matrix before passing to nilearn: `connectivity_matrix.T`

### Directed Arrows
- Nilearn 0.12+ supports directed arrows via FancyArrow patches
- Automatically displayed when matrix is asymmetric
- Arrow direction: FROM source TO target
- Arrowhead points to the target node

### Laterality
- Parameter: `radiological=False` (default)
- Result: Left hemisphere on left side of image (neurological convention)
- MNI coordinates: X < 0 = left, X > 0 = right

### Colormap Usage by Analysis Type

| Analysis Type | Colormap | Rationale |
|--------------|----------|-----------|
| Session Change | `coolwarm` | Diverging, centered at 0 for increases/decreases |
| Behavioral | `PRGn` | Purple-Green diverging for positive/negative correlations |
| Task Contrast | `RdYlBu_r` | Red-Yellow-Blue for task differences |
| Multi-condition Overlay | Varies | Reds, Blues, Greens, Purples for distinct conditions |

---

## Figure Parameters

### Standard Settings
- **Node size**: 70-100 (larger for focused views)
- **Edge threshold**: 0% (show all Pp>0.99 connections)
- **Display mode**:
  - `lyrz` for single plots (4 views: sagittal L/R, coronal Y, axial Z)
  - `z` for multi-panel plots (axial view only)
- **DPI**: 300 (high resolution)
- **Figure size**: 18×10 for single, varies for multi-panel

### Region Filtering
- **dlPFC outgoing**: `source_regions=['Frontal_Mid']`, `connection_type='outgoing'`
- **Hippocampus**: `source_regions=['Hippocampus']`, `connection_type='bidirectional'`

---

## Data Files Location

All PEB analysis results: `massive_output_local/adam_m6/`

### File Naming Pattern
- Session changes: `PEB_change_-ses-01-ses-02_-task-{TASK}_cov-_noFD.mat`
- Behavioral: `PEB_behav_associations_-ses-02_-task-{TASK}_cov-{COVARIATE}_noFD.mat`
- Contrasts: `PEB_contrast_-ses-02_-task-{TASK1}-task-{TASK2}_cov-_noFD.mat`

---

## Quick Lookup by Overleaf Table Row

| Overleaf | Code | Description |
|----------|------|-------------|
| 1a | m1-a | REST - Session Change |
| 2a | m2-a | MUSIC - Session Change |
| 3a | m3-a | MOVIE - Session Change |
| 4a | m4-a | MEDITATION - Session Change |
| 1b | m1-b | REST - Behavioral (11D-ASC) |
| 2b | m2-b | MUSIC - Behavioral (11D-ASC) |
| 3b | m3-b | MOVIE - Behavioral (11D-ASC) |
| 4b | m4-b | MEDITATION - Behavioral *[not available]* |

---

## Quick Reference

### Find figures by experimental condition:
- **REST**: `figures/organized/m1_rest/m1-*`
- **MUSIC**: `figures/organized/m2_music/m2-*`
- **MOVIE**: `figures/organized/m3_movie/m3-*`
- **MEDITATION**: `figures/organized/m4_meditation/m4-*`

### Find figures by analysis type:
- **Session changes**: `m*-a*`
- **Behavioral (11D-ASC)**: `m*-b*`
- **Behavioral (5D-ASC)**: `m*-c*`
- **Contrasts**: `contrasts/contrast_*`
- **Multi-condition**: `h01_multi_condition/h01-*`

### Find figures by network focus:
- **Full network**: Base code (`m1-a`, `m2-b`, etc.)
- **dlPFC**: Variant 1 for session change (`m1-a1`, `m2-a1`, etc.)
- **Hippocampus**: Variant 2 for session change (`m1-a2`, `m2-a2`, etc.) or variant 1 for behavioral (`m1-b1`, etc.)

---

## File Path Examples

```
# REST session change (full network)
figures/organized/m1_rest/m1-a_change_full.png

# MUSIC behavioral 11D-ASC (hippocampus)
figures/organized/m2_music/m2-b1_behavioral_asc11_hipp.png

# MOVIE session change (dlPFC)
figures/organized/m3_movie/m3-a1_change_dlpfc.png

# Multi-condition overlay
figures/organized/h01_multi_condition/h01-a_all_tasks_overlay.png

# Task contrast
figures/organized/contrasts/contrast_rest_vs_music.png
```

---

## Notes

- All figures use Pp > 0.99 threshold
- AAL atlas coordinates for brain regions
- 10 ROIs per analysis (specific regions vary by PEB model)
- Figures maintain consistent styling within categories
- Multi-condition figures support 2-4 conditions optimally
- Bold codes in tables (e.g., **m1-a**) indicate primary full network figures for publication
