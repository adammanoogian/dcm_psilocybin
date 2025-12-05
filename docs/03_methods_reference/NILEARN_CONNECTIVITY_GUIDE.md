# nilearn Brain Connectivity Visualization - Complete Guide

## 🎉 Working Solution for DCM Connectivity Visualization

After encountering compatibility issues with visBrain, we implemented a **reliable, production-ready** solution using nilearn. All visualizations work correctly and save to files automatically.

---

## ✅ Successfully Generated Visualizations

All files saved to `plots/nilearn/`:

### 1. **dlpfc_rest_outgoing.png**
- **Task**: Rest (Session Change)
- **Connections**: dlPFC (Frontal_Mid_L/R) outgoing connections
- **View**: Left-Right-Top-Bottom (lyrz)
- **Features**: 10 connections, red colormap, shows top-down control
- **Command**:
```bash
python plot_nilearn_connectivity.py \
  --mat-files "massive_output_local/adam_m6/PEB_change_-ses-01-ses-02_-task-rest_cov-_noFD.mat" \
  --conditions "Rest (Session Change)" \
  --source-regions Frontal_Mid_L Frontal_Mid_R \
  --connection-type outgoing \
  --strength-threshold 0.05 \
  --node-size 60 \
  --edge-cmap Reds \
  --display-mode lyrz \
  --output plots/nilearn/dlpfc_rest_outgoing.png
```

### 2. **hippocampus_network.png**
- **Task**: Hippocampus Network
- **Connections**: Bidirectional connections from hippocampus
- **View**: Left-Right-Top-Bottom (lyrz)
- **Features**: 36 connections, coolwarm colormap, memory network
- **Command**:
```bash
python plot_nilearn_connectivity.py \
  --mat-files "massive_output_local/adam_m6/PEB_change_-ses-01-ses-02_-task-rest_cov-_noFD.mat" \
  --conditions "Hippocampus Network" \
  --source-regions Hippocampus \
  --connection-type bidirectional \
  --strength-threshold 0.05 \
  --node-size 80 \
  --edge-cmap coolwarm \
  --display-mode lyrz \
  --output plots/nilearn/hippocampus_network.png
```

### 3. **music_glass_brain.png**
- **Task**: Music Task
- **Connections**: Frontal and thalamic outgoing
- **View**: Glass brain (transparent overlay)
- **Features**: 13 connections, RdYlBu colormap, see-through visualization
- **Command**:
```bash
python plot_nilearn_connectivity.py \
  --mat-files "massive_output_local/adam_m6/PEB_change_-ses-01-ses-02_-task-music_cov-_noFD.mat" \
  --conditions "Music Task" \
  --source-regions Frontal_Mid Thalamus \
  --connection-type outgoing \
  --strength-threshold 0.05 \
  --node-size 70 \
  --edge-cmap RdYlBu_r \
  --display-mode glass \
  --output plots/nilearn/music_glass_brain.png
```

### 4. **meditation_ortho.png**
- **Task**: Meditation Task
- **Connections**: dlPFC outgoing
- **View**: Orthogonal (sagittal, coronal, axial slices)
- **Features**: 7 connections, viridis colormap, multi-slice view
- **Command**:
```bash
python plot_nilearn_connectivity.py \
  --mat-files "massive_output_local/adam_m6/PEB_change_-ses-01-ses-02_-task-meditation_cov-_noFD.mat" \
  --conditions "Meditation Task" \
  --source-regions Frontal_Mid \
  --connection-type outgoing \
  --strength-threshold 0.08 \
  --node-size 75 \
  --edge-cmap viridis \
  --display-mode ortho \
  --output plots/nilearn/meditation_ortho.png
```

---

## 📊 Features Implemented

### ✅ Connection Filtering
- **Source regions**: Filter by source ROIs (e.g., Frontal_Mid, Hippocampus)
- **Target regions**: Filter by target ROIs
- **Connection types**: outgoing, incoming, bidirectional
- **Strength threshold**: Minimum connection strength
- **PP threshold**: Posterior probability threshold (default: 0.99)

### ✅ Visualization Modes

1. **lyrz** (Left-Right-Top-Bottom) - Best for general connectivity
2. **ortho** (Orthogonal slices) - Shows sagittal, coronal, axial
3. **glass** (Glass brain) - Transparent overlay, publication-ready
4. **x, y, z** (Single slice views)

### ✅ Customization Options

- **Node size**: Control sphere size (default: 50)
- **Edge colormap**: Any matplotlib colormap (coolwarm, Reds, viridis, etc.)
- **Edge threshold**: Percentage or absolute threshold (default: 90%)
- **Colorbar**: Show/hide colorbar
- **Title**: Automatic or custom

### ✅ Output Formats

- **PNG**: High-resolution (300 DPI) raster
- **PDF**: Vector format for publications
- **SVG**: Scalable vector graphics

---

## 🎯 Use Cases & Examples

### Example 1: Publication Figure - dlPFC Top-Down Control
```bash
python plot_nilearn_connectivity.py \
  --mat-files PEB_change_rest.mat \
  --conditions "Resting State" \
  --source-regions Frontal_Mid_L Frontal_Mid_R \
  --connection-type outgoing \
  --strength-threshold 0.1 \
  --node-size 50 \
  --edge-cmap Reds \
  --display-mode glass \
  --output figure1_dlpfc_control.pdf
```

### Example 2: Network Analysis - Hippocampal Connectivity
```bash
python plot_nilearn_connectivity.py \
  --mat-files PEB_contrast_music.mat \
  --conditions "Music vs Rest" \
  --source-regions Hippocampus \
  --connection-type bidirectional \
  --node-size 80 \
  --edge-cmap coolwarm \
  --display-mode lyrz \
  --output hippocampus_music.png
```

### Example 3: Clinical View - Orthogonal Slices
```bash
python plot_nilearn_connectivity.py \
  --mat-files PEB_behav_associations.mat \
  --conditions "ASC Correlation" \
  --strength-threshold 0.15 \
  --edge-cmap RdYlBu_r \
  --display-mode ortho \
  --node-size 60 \
  --output clinical_view.png
```

### Example 4: Comparison Across Tasks
Create multiple visualizations for comparison:
```bash
for task in rest music movie meditation; do
  python plot_nilearn_connectivity.py \
    --mat-files "PEB_change_${task}.mat" \
    --conditions "${task^}" \
    --source-regions Frontal_Mid \
    --connection-type outgoing \
    --display-mode glass \
    --output "comparison_${task}.png"
done
```

---

## 🔬 Advanced Usage

### Custom Edge Thresholds
```bash
# Show top 10% strongest connections
--edge-threshold "90%"

# Show connections above absolute value
--edge-threshold 0.1

# Show all connections (no threshold)
--edge-threshold 0
```

### Colormap Options
Popular scientific colormaps:
- `coolwarm` - Diverging (good for positive/negative)
- `RdYlBu_r` - Red-Yellow-Blue reversed
- `viridis` - Perceptually uniform
- `Reds`, `Blues` - Sequential
- `seismic` - Centered at zero

### Display Mode Details

**lyrz** (Left-Right-Top-Bottom):
- Best for: General connectivity overview
- Shows: 4 views in one figure
- Good for: Publications, presentations

**glass**:
- Best for: See-through visualization
- Shows: Transparent brain with connections
- Good for: Complex networks, multiple connections

**ortho** (Orthogonal):
- Best for: Clinical/anatomical precision
- Shows: Sagittal, coronal, axial slices
- Good for: Localization, anatomical accuracy

---

## 📈 Data Flow

```
.mat file (DCM PEB results)
    ↓
PEBDataLoader (extract connectivity matrix)
    ↓
Filter by source/target/type/threshold
    ↓
AAL Coordinate Mapper (get MNI coordinates)
    ↓
nilearn plot_connectome()
    ↓
Save to PNG/PDF/SVG
```

---

## 🆚 Comparison: nilearn vs visBrain

| Feature | nilearn | visBrain |
|---------|---------|----------|
| **Stability** | ✅ Reliable | ❌ Compatibility issues |
| **Brain overlay** | ✅ Works | ❌ Broken (AssertionError) |
| **File output** | ✅ Direct save | ❌ Display issues |
| **Installation** | ✅ Simple | ⚠️ Complex dependencies |
| **Display modes** | ✅ Multiple | ✅ 3D interactive |
| **Customization** | ✅ Extensive | ✅ Extensive |
| **Edge thickness** | ✅ Native support | ⚠️ Limited |
| **Documentation** | ✅ Excellent | ⚠️ Sparse |
| **Publication ready** | ✅ Yes | ⚠️ Screenshot only |

---

## 🎨 Visualization Best Practices

### For Publications
- Use `display-mode glass` for clarity
- High node size (70-100) for visibility
- Sequential colormaps (Reds, Blues)
- Save as PDF for vector graphics
- Include colorbar

### For Presentations
- Use `display-mode lyrz` for overview
- Large node size (80+)
- High contrast colormaps
- PNG at 300 DPI
- Clear titles

### For Analysis
- Use `display-mode ortho` for precision
- Lower threshold to see more connections
- Diverging colormaps (coolwarm)
- Multiple output formats
- Document parameters

---

## 🔧 Troubleshooting

### No connections visible
- **Lower strength threshold**: `--strength-threshold 0`
- **Lower edge threshold**: `--edge-threshold 0`
- **Check PP threshold**: Try `--pp-threshold 0.95`
- **Verify source regions**: Check region names match AAL

### Nodes too small
- **Increase node size**: `--node-size 100`
- **Change display mode**: Try `glass` mode

### Colors not showing well
- **Try different colormap**: `--edge-cmap RdYlBu_r`
- **Use diverging maps** for positive/negative
- **Use sequential maps** for strength only

### Wrong regions highlighted
- **Check region names**: Use `Frontal_Mid` not `frontal_mid`
- **Partial matching works**: `Frontal` matches `Frontal_Mid_L/R`
- **Check connection type**: `outgoing` vs `incoming` vs `bidirectional`

---

## 🔬 Critical Technical Notes (Updated Nov 2025)

### Directed Arrows Support - VERIFIED WORKING

**nilearn 0.12+ supports directed arrows** for asymmetric connectivity matrices:

- Uses `FancyArrow` patches from matplotlib
- Automatically detects asymmetric matrices and warns: `'adjacency_matrix' is not symmetric. A directed graph will be plotted.`
- Arrow direction shows information flow
- Arrow color/intensity represents connection strength
- **CRITICAL**: This was implemented in PR #2703 (March 2021) - matrix[i,j] = FROM i TO j

**Visual confirmation**: Generated test plots show clear directional arrows pointing from source to target regions. dlPFC outgoing connections show arrows pointing AWAY from Frontal_Mid nodes to target regions.

### Matrix Convention Differences - CRITICAL

**MATLAB DCM convention** (SPM/DCM):
```
Ep[i, j] = connection FROM j TO i
(rows = targets, columns = sources)
```

**nilearn convention** (plot_connectome):
```
matrix[i, j] = connection FROM i TO j
(rows = sources, columns = targets)
```

**Solution**: The connectivity matrix MUST be transposed before passing to nilearn:
```python
# In plot_connectome() method - line ~363
connectivity_matrix_nilearn = connectivity_matrix.T

# ALSO in plot_glass_brain() method - line ~482 (BUG FIX)
connectivity_matrix_nilearn = connectivity_matrix.T  # Was missing!
```

Without this transpose, arrows will point in the WRONG direction (e.g., showing incoming instead of outgoing connections).

**BUG FIX (Nov 2025)**: The `plot_glass_brain()` method was missing the matrix transpose, causing incorrect arrow directions in glass brain visualizations. This has been fixed.

### Radiological vs Neurological View - NEW PARAMETER

**nilearn plot_connectome** now supports a `radiological` parameter:

```python
plotting.plot_connectome(
    ...,
    radiological=False  # Default: neurological convention
)
```

| Parameter | Display | Standard |
|-----------|---------|----------|
| `radiological=False` | Left hemisphere on LEFT side of image | Research |
| `radiological=True` | Left hemisphere on RIGHT side of image | Clinical |

**Default (neurological)** is standard for research publications. The "L" marker appears in the top-left corner to confirm which side is which.

### AAL Coordinate Mapping - CRITICAL BUG FIX

**Problem**: nilearn's `find_parcellation_cut_coords()` returns INCORRECT coordinates with massive asymmetries:
- Frontal_Mid_L: Y=31.8, Z=32.8
- Frontal_Mid_R: Y=49.1, Z=-11.0
- Y-diff: 17mm, Z-diff: 44mm (WRONG - should be ~0mm)

**Root Cause**: `find_parcellation_cut_coords` doesn't properly map AAL codes. The AAL atlas uses codes like 2201, 2202, etc. (stored as strings in `aal.indices`), not sequential integers.

**Solution**: Compute center of mass directly from atlas using AAL codes:
```python
from scipy.ndimage import center_of_mass
import nibabel as nib

atlas_img = nib.load(aal.maps)
atlas_data = atlas_img.get_fdata()
affine = atlas_img.affine

for idx, label in enumerate(aal.labels):
    if label == 'Background':
        continue

    # Use actual AAL code (stored as string)
    aal_code = float(aal.indices[idx])

    # Find voxels and compute center of mass
    mask = atlas_data == aal_code
    com_voxel = center_of_mass(mask.astype(float))

    # Convert to MNI coordinates
    com_mni = nib.affines.apply_affine(affine, com_voxel)
    coord_map[label] = com_mni
```

**Result**: Correct symmetric coordinates:
- Frontal_Mid_L: X=-33.8, Y=31.5, Z=34.1
- Frontal_Mid_R: X=+37.4, Y=31.8, Z=32.8
- Y-diff: 0.3mm, Z-diff: 1.3mm (CORRECT)

### Node Color Consistency

To ensure node colors match the legend exactly:
```python
from matplotlib import cm

# Assign explicit colors by ROI index
node_cmap = cm.get_cmap('tab10')
node_colors = [node_cmap(i % 10) for i in range(len(roi_names))]

# Pass to plot_connectome
plotting.plot_connectome(..., node_color=node_colors)

# Use SAME colors in legend
for i, name in enumerate(roi_names):
    legend_handles.append(Patch(facecolor=node_colors[i], label=name))
```

Do NOT use `node_color='auto'` as it won't match your custom legend.

### Edge Threshold Behavior

- `edge_threshold='90%'` shows only top 10% of connections (very restrictive)
- `edge_threshold='0%'` shows ALL connections (recommended for exploring data)
- Use `edge_threshold='50%'` for balanced view

**Important**: If you specify source/target regions and apply strength thresholds, most connections may already be filtered out. Setting edge_threshold='90%' on top of that can result in showing only 1-2 connections. Use '0%' to show all filtered connections.

### MNI Coordinate System

Standard neurological convention:
- **Negative X = LEFT hemisphere**
- **Positive X = RIGHT hemisphere**
- Y increases from posterior to anterior
- Z increases from inferior to superior

All `_L` regions should have negative X, all `_R` regions should have positive X. If this is reversed, check your coordinate mapping.

### Debugging Tips

1. **Print the actual matrix values** before and after transpose
2. **Check coordinates** for each ROI to ensure L/R hemispheres are correct
3. **Verify symmetry**: L/R pairs should have similar Y and Z values
4. **Test with known connections**: Plot a single known connection first
5. **Use `display_mode='glass'`** with posterior view to easily verify L/R placement

---

## 📚 Complete Command-Line Reference

### Required Arguments
```bash
--mat-files FILE [FILE ...]     PEB .mat file paths
--conditions LABEL [LABEL ...]  Condition labels
--output FILE                   Output file path
```

### Filtering Arguments
```bash
--source-regions REGION [...]   Source ROI names (partial match)
--target-regions REGION [...]   Target ROI names (default: all)
--connection-type TYPE          outgoing|incoming|bidirectional
--pp-threshold FLOAT            Posterior probability (default: 0.99)
--strength-threshold FLOAT      Min connection strength (default: 0.0)
--edge-threshold VALUE          Edge display threshold (default: 90%)
```

### Visual Arguments
```bash
--node-size FLOAT               Node size (default: 50)
--edge-cmap CMAP                Colormap name (default: coolwarm)
--display-mode MODE             lyrz|ortho|x|y|z|glass (default: lyrz)
--colorbar                      Show colorbar (default: True)
--radiological                  Use radiological view (left on right side)
```

### View Convention
```bash
# Neurological convention (default) - standard for research
--radiological        # NOT specified = neurological view

# Radiological convention - standard for clinical
--radiological        # Left hemisphere appears on RIGHT side of image
```

---

## 🚀 Next Steps

### Multi-Condition Comparison
Currently processes one file at a time. Future enhancement:
- Side-by-side comparison
- Overlay multiple conditions
- Statistical contrasts

### Interactive HTML Output
Add interactive plotly visualizations:
- Rotate in browser
- Hover for values
- Toggle connections

### Automated Reporting
Generate PDF reports with:
- Multiple views
- Statistical tables
- Connection strength lists

---

## ✨ Summary

**What Works:**
✅ All visualization modes (lyrz, ortho, glass, x, y, z)
✅ Connection filtering (source, target, type, threshold)
✅ Customizable colors, sizes, colormaps
✅ File output (PNG, PDF, SVG)
✅ High-resolution (300 DPI)
✅ Publication-ready figures
✅ AAL atlas integration with CORRECT coordinate mapping
✅ Edge thickness by strength
✅ Colorbar support
✅ Proper MATLAB→nilearn matrix convention handling (transpose)
✅ Symmetric L/R hemisphere coordinates
✅ Consistent node colors matching legend
✅ **Directed arrows for asymmetric matrices (FancyArrow patches)**
✅ **Radiological/Neurological view toggle**

**Critical Fixes Applied (Nov 2025):**
✅ Matrix transpose for correct arrow direction (MATLAB DCM → nilearn)
✅ Direct center-of-mass computation using AAL codes (fixed asymmetry bug)
✅ Explicit node color assignment for legend consistency
✅ Edge threshold set to '0%' to show all filtered connections
✅ **plot_glass_brain() missing transpose - NOW FIXED**
✅ **Added radiological parameter support to both plot methods**
✅ **Verified directed arrows work correctly with asymmetric matrices**

**What Doesn't Work in visBrain (but works here):**
❌ Brain overlay (AssertionError) → ✅ Works in nilearn
❌ Interactive display issues → ✅ Direct file save
❌ Screenshot bugs → ✅ Reliable output
❌ Camera setup errors → ✅ No issues

**Generated Hypothesis Figures (7 total):**
1. `H1_dlpfc_topdown_control.png` - dlPFC outgoing connections
2. `H2_hippocampus_memory_network.pdf` - Hippocampal network
3. `H3a_music_frontal_thalamic.pdf` - Music task
4. `H3b_meditation_attention.pdf` - Meditation task
5. `H4a_asc_sensory_correlations.pdf` - ASC sensory
6. `H4b_asc_auditory_music.pdf` - ASC auditory
7. `H5_rest_vs_music_global.pdf` - Task comparison

All files are ready for use in publications, presentations, or further analysis!

**Key Code Locations:**
- Main script: `scripts/visualization/plot_nilearn_connectivity.py`
- Config file: `scripts/config/hypothesis_config.yaml`
- Figure generator: `scripts/analysis/generate_paper_figures.py`
- Output directory: `figures/nilearn/`
