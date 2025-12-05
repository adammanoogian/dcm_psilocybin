# Figure Quick Reference

**Organization by EXPERIMENTAL CONDITION** (matching overleaf paper)

## Directory Structure

```
figures/organized/
├── m1_rest/              → 11 figures (REST: nilearn + PEB matrices)
├── m2_music/             → 11 figures (MUSIC: nilearn + PEB matrices)
├── m3_movie/             → 8 figures (MOVIE: nilearn + PEB matrices)
├── m4_meditation/        → 7 figures (MEDITATION: nilearn + PEB matrices)
├── contrasts/            → 3 figures (Task contrasts)
├── h01_multi_condition/  → 6 figures (Multi-condition comparisons)
├── h02_dlpfc_outgoing/   → 2 figures (Hypothesis: dlPFC outgoing connections)
├── h03_hippocampus/      → 2 figures (Hypothesis: Hippocampus connections)
└── peb_matrix_panels/    → 8 figures (2x2 PEB matrix panels - 2 files per condition)
```

**Total: 58 systematically organized figures (35 nilearn + 15 PEB matrices + 8 combined panels)**

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
- **1**: Network-specific (e.g., dlPFC)
- **2**: Network-specific (e.g., hippocampus)

---

## Complete Figure Catalog

### M1: REST CONDITION

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

### M2: MUSIC CONDITION

| Code | Analysis | Network | Colormap |
|------|----------|---------|----------|
| **m2-a** | Session change | Full | coolwarm |
| m2-a1 | Session change | dlPFC outgoing | coolwarm |
| m2-a2 | Session change | Hippocampus | coolwarm |
| **m2-b** | Behavioral (ASC11) | Full | PRGn |
| m2-b1 | Behavioral (ASC11) | Hippocampus | PRGn |
| m2-c | Behavioral (ASC5) | Full | PRGn |
| m2-c1 | Behavioral (ASC5) | Hippocampus | PRGn |

### M3: MOVIE CONDITION

| Code | Analysis | Network | Colormap |
|------|----------|---------|----------|
| **m3-a** | Session change | Full | coolwarm |
| m3-a1 | Session change | dlPFC outgoing | coolwarm |
| m3-a2 | Session change | Hippocampus | coolwarm |
| **m3-b** | Behavioral (ASC11) | Full | PRGn |
| m3-b1 | Behavioral (ASC11) | Hippocampus | PRGn |

### M4: MEDITATION CONDITION

| Code | Analysis | Network | Colormap |
|------|----------|---------|----------|
| **m4-a** | Session change | Full | coolwarm |
| m4-a1 | Session change | dlPFC outgoing | coolwarm |
| m4-a2 | Session change | Hippocampus | coolwarm |

*Note: No behavioral data currently available for meditation*

### CONTRASTS

| Figure | Description | Colormap |
|--------|-------------|----------|
| `contrast_rest_vs_music.png` | Rest - Music | RdYlBu_r |
| `contrast_rest_vs_movie.png` | Rest - Movie | RdYlBu_r |
| `contrast_music_vs_movie.png` | Music - Movie | RdYlBu_r |

### H01: MULTI-CONDITION COMPARISONS

| Code | Description | Method | Conditions |
|------|-------------|--------|-----------|
| **h01-a** | All tasks session change | Overlay | Rest/Music/Movie/Med |
| **h01-b** | All tasks session change | Side-by-side | Rest/Music/Movie/Med |
| **h01-c** | ASC Auditory | Overlay | Rest vs Music |
| **h01-d** | ASC Auditory | Side-by-side | Rest vs Music |
| **h01-e** | ASC Sensory | Overlay | Rest/Music/Movie |
| **h01-f** | ASC Sensory | Side-by-side | Rest/Music/Movie |

### H02: dlPFC OUTGOING CONNECTIONS

| Code | Description | Network Filter | Conditions |
|------|-------------|----------------|-----------|
| **h02-a** | Session change | dlPFC outgoing only | Rest/Music/Movie/Med |
| **h02-b** | Behavioral (11D-ASC) | dlPFC outgoing only | Rest/Music/Movie |

*Shows only connections FROM dlPFC (Frontal_Mid) to other regions*

### H03: HIPPOCAMPUS CONNECTIONS

| Code | Description | Network Filter | Conditions |
|------|-------------|----------------|-----------|
| **h03-a** | Session change | Hippocampus bidirectional | Rest/Music/Movie/Med |
| **h03-b** | Behavioral (11D-ASC) | Hippocampus bidirectional | Rest/Music/Movie |

*Shows bidirectional connections involving Hippocampus*

---

## Quick Lookup

### By Overleaf Table Row

| Overleaf | Code | Description |
|----------|------|-------------|
| 1a | m1-a | REST - Change |
| 2a | m2-a | MUSIC - Change |
| 3a | m3-a | MOVIE - Change |
| 4a | m4-a | MEDITATION - Change |
| 1b | m1-b | REST - Behavioral (11D-ASC) |
| 2b | m2-b | MUSIC - Behavioral (11D-ASC) |
| 3b | m3-b | MOVIE - Behavioral (11D-ASC) |
| 4b | m4-b | MEDITATION - Behavioral (11D-ASC) *[not available]* |

---

## Generate Commands

```bash
# Step 1: Generate all nilearn brain connectivity figures (M1-M4)
python scripts/analysis/generate_all_nilearn_figures.py

# Step 2: Generate all PEB matrix heatmaps (M1-M4)
python scripts/analysis/generate_all_peb_matrices.py

# Step 3: Generate 2x2 PEB matrix panels (M1-M4)
python scripts/analysis/generate_peb_matrix_panels.py

# Step 4: Generate multi-condition figures (H01)
python scripts/analysis/generate_combined_nilearn_figures.py

# Step 5: Generate hypothesis-based panels (H02, H03)
python scripts/analysis/generate_hypothesis_panels.py

# Step 6: Organize all figures (nilearn + PEB matrices + panels) into structured folders
python scripts/analysis/organize_figures.py
```

---

## Colormap Guide

### Nilearn Brain Connectivity

| Colormap | Use Case | Interpretation |
|----------|----------|----------------|
| `coolwarm` | Session changes | Blue = decrease, Red = increase |
| `PRGn` | Behavioral | Purple = negative β, Green = positive β |
| `RdYlBu_r` | Task contrasts | Red = more in task 1, Blue = more in task 2 |

### PEB Matrix Heatmaps

| Colormap | Use Case | Interpretation |
|----------|----------|----------------|
| `blue-white-red` | Session change (Pre/Post) | Blue = inhibitory, Red = excitatory |
| `green-purple` | Change toward zero | Green = closer to zero, Purple = further from zero |
| `viridis` | Behavioral associations | Yellow = positive β, Purple = negative β |

**Note:** PEB matrices are displayed in MATLAB convention (rows=targets, columns=sources) with transposed orientation in seaborn heatmaps. A-constrained behavioral models show template boxes (dotted lines) indicating active connections in the model.

---

## Common Searches

### Find figures by condition:
- **REST**: `m1_rest/m1-*`
- **MUSIC**: `m2_music/m2-*`
- **MOVIE**: `m3_movie/m3-*`
- **MEDITATION**: `m4_meditation/m4-*`

### Find figures by analysis type:
- **Session changes**: `m*-a*`
- **Behavioral (11D-ASC)**: `m*-b*`
- **Behavioral (5D-ASC)**: `m*-c*`
- **Contrasts**: `contrasts/contrast_*`
- **Multi-condition**: `h01_multi_condition/h01-*`

### Find figures by network focus:
- **Full network**: Base code (`m1-a`, `m2-b`, etc.)
- **dlPFC**: Variant 1 (`m1-a1`, `m2-a1`, etc.)
- **Hippocampus**: Variant 2 (`m1-a2`, `m2-a2`, etc.) or variant 1 for behavioral (`m1-b1`, etc.)

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
```

---

## Data Sources

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
