#!/usr/bin/env python3
"""
Brain Connectivity Visualization using nilearn

A reliable alternative to visBrain for visualizing DCM connectivity data.
Uses nilearn's plotting functions for publication-ready brain connectivity figures.

Author: Generated for DCM Psilocybin Analysis
"""

import argparse
import numpy as np
import sys
from pathlib import Path
from typing import List, Tuple, Optional, Dict
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for reliable file saving
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Create custom green-purple colormap for "change toward zero" analysis
# Green = connection moved closer to zero (weakening)
# Purple = connection moved further from zero (strengthening)
GREEN_PURPLE_CMAP = LinearSegmentedColormap.from_list(
    'green_purple',
    [(0.2, 0.7, 0.2), (1, 1, 1), (0.6, 0.2, 0.8)],  # Green → White → Purple
    N=256
)

# Import existing data loader from project root
from plot_PEB_results import PEBDataLoader


class AALCoordinateMapper:
    """
    Maps brain region names from AAL atlas to MNI coordinates.
    Uses nilearn to fetch the AAL atlas and extract centroid coordinates.
    """

    def __init__(self):
        """Initialize the coordinate mapper and fetch AAL atlas."""
        try:
            from nilearn.datasets import fetch_atlas_aal
            import nibabel as nib
            from scipy.ndimage import center_of_mass

            print("Fetching AAL atlas...")
            self.aal = fetch_atlas_aal()

            # Load atlas image directly for proper coordinate computation
            print("Extracting region coordinates...")
            atlas_img = nib.load(self.aal.maps)
            atlas_data = atlas_img.get_fdata()
            affine = atlas_img.affine

            # Create mapping from region names to coordinates
            # Compute center of mass for each region using AAL codes
            self.coord_map = {}

            for idx, label in enumerate(self.aal.labels):
                if label == 'Background':
                    continue

                # Get the actual AAL code for this region (stored as string)
                aal_code = float(self.aal.indices[idx])

                # Find voxels with this AAL code
                mask = atlas_data == aal_code
                n_voxels = np.sum(mask)

                if n_voxels > 0:
                    # Compute center of mass in voxel coordinates
                    com_voxel = center_of_mass(mask.astype(float))
                    # Convert to MNI coordinates using affine matrix
                    com_mni = nib.affines.apply_affine(affine, com_voxel)
                    self.coord_map[label] = com_mni

            print(f"Loaded {len(self.coord_map)} AAL regions")

        except ImportError as e:
            print("ERROR: nilearn is required for AAL coordinate mapping.")
            print("Install with: conda install -c conda-forge nilearn")
            raise e

    def get_coordinates(self, roi_names: List[str]) -> np.ndarray:
        """
        Get MNI coordinates for a list of ROI names.

        Parameters
        ----------
        roi_names : list of str
            List of brain region names

        Returns
        -------
        coords : np.ndarray, shape (n_rois, 3)
            MNI coordinates (x, y, z) for each ROI
        """
        coords = []
        missing = []

        for roi_name in roi_names:
            # Try exact match first
            if roi_name in self.coord_map:
                coords.append(self.coord_map[roi_name])
            else:
                # Try partial match
                matched = False
                for aal_label, aal_coord in self.coord_map.items():
                    if roi_name.lower() in aal_label.lower() or aal_label.lower() in roi_name.lower():
                        coords.append(aal_coord)
                        matched = True
                        print(f"Matched '{roi_name}' to AAL region '{aal_label}'")
                        break

                if not matched:
                    missing.append(roi_name)
                    coords.append([0, 0, 0])

        if missing:
            print(f"WARNING: Could not find coordinates for: {missing}")

        return np.array(coords)


class NilearnConnectivityVisualizer:
    """
    Visualizes brain connectivity using nilearn plotting functions.
    Provides reliable, publication-ready connectivity visualizations.
    """

    def __init__(self, coord_mapper: AALCoordinateMapper):
        """
        Initialize the visualizer.

        Parameters
        ----------
        coord_mapper : AALCoordinateMapper
            Coordinate mapper for converting ROI names to MNI coordinates
        """
        self.coord_mapper = coord_mapper

    def load_connectivity(
        self,
        mat_file: str,
        pp_threshold: float = 0.99,
        covariate_index: int = 0
    ) -> Tuple[np.ndarray, List[str]]:
        """
        Load connectivity matrix from a PEB .mat file.

        Parameters
        ----------
        mat_file : str
            Path to .mat file containing PEB results
        pp_threshold : float, optional
            Posterior probability threshold (default: 0.99)
        covariate_index : int, optional
            Which covariate to extract (default: 0)

        Returns
        -------
        connectivity_matrix : np.ndarray, shape (n_rois, n_rois)
            Connectivity matrix
        roi_names : list of str
            Region names
        """
        print(f"\nLoading {mat_file}...")

        loader = PEBDataLoader(mat_file)
        data = loader.get_data()

        model = data.get('model') or data.get('bma')
        roi_names = data['roi_names']

        if model is None:
            raise ValueError(f"Could not extract model data from {mat_file}")

        # Get Ep and Pp
        Ep = np.array(model['Ep']).flatten()
        Pp = np.array(model['Pp']).flatten()

        # Apply threshold
        below_threshold = Pp < pp_threshold
        Ep[below_threshold] = 0

        # Reshape to matrix
        n_rois = len(roi_names)
        expected_full_size = n_rois * n_rois

        if len(Ep) % expected_full_size == 0:
            # Full model
            n_covariates = len(Ep) // expected_full_size
            Ep_3d = Ep.reshape((n_rois, n_rois, n_covariates), order='F')
        else:
            # Constrained model
            print("Detected constrained connectivity model")
            Pnames = model['Pnames']
            n_covariates = len(Ep) // len(Pnames)
            Ep_3d = np.zeros((n_rois, n_rois, n_covariates))

            for param_idx, pname in enumerate(Pnames):
                if 'A(' in pname:
                    parts = pname.split('(')[1].split(')')[0].split(',')
                    i = int(parts[0]) - 1
                    j = int(parts[1]) - 1
                    for cov_idx in range(n_covariates):
                        flat_idx = param_idx + cov_idx * len(Pnames)
                        Ep_3d[i, j, cov_idx] = Ep[flat_idx]

        if covariate_index >= Ep_3d.shape[2]:
            print(f"WARNING: Covariate index {covariate_index} out of range. Using index 0.")
            covariate_index = 0

        connectivity_matrix = Ep_3d[:, :, covariate_index]

        print(f"  Loaded {n_rois} regions, covariate {covariate_index}")
        print(f"  Non-zero connections: {np.count_nonzero(connectivity_matrix)}")

        return connectivity_matrix, roi_names

    def filter_connections(
        self,
        connectivity_matrix: np.ndarray,
        roi_names: List[str],
        source_regions: Optional[List[str]] = None,
        target_regions: Optional[List[str]] = None,
        connection_type: str = 'outgoing',
        strength_threshold: float = 0.0
    ) -> np.ndarray:
        """
        Filter connectivity matrix by source/target regions and connection type.

        Parameters
        ----------
        connectivity_matrix : np.ndarray, shape (n_rois, n_rois)
            Full connectivity matrix
        roi_names : list of str
            Region names
        source_regions : list of str, optional
            Source regions to include
        target_regions : list of str, optional
            Target regions to include
        connection_type : str, optional
            'outgoing', 'incoming', or 'bidirectional'
        strength_threshold : float, optional
            Minimum absolute connection strength

        Returns
        -------
        filtered_matrix : np.ndarray, shape (n_rois, n_rois)
            Filtered connectivity matrix
        """
        filtered = connectivity_matrix.copy()
        n_rois = len(roi_names)

        # Get source and target indices
        if source_regions:
            source_indices = [i for i, name in enumerate(roi_names)
                            if any(src in name for src in source_regions)]
        else:
            source_indices = list(range(n_rois))

        if target_regions:
            target_indices = [i for i, name in enumerate(roi_names)
                            if any(tgt in name for tgt in target_regions)]
        else:
            target_indices = list(range(n_rois))

        # Create mask
        mask = np.zeros((n_rois, n_rois), dtype=bool)

        if connection_type == 'outgoing':
            for src_idx in source_indices:
                for tgt_idx in target_indices:
                    if src_idx != tgt_idx:
                        mask[tgt_idx, src_idx] = True

        elif connection_type == 'incoming':
            for src_idx in source_indices:
                for tgt_idx in target_indices:
                    if src_idx != tgt_idx:
                        mask[tgt_idx, src_idx] = True

        elif connection_type == 'bidirectional':
            # Bidirectional: connections from source to target AND from target to source
            for src_idx in source_indices:
                for tgt_idx in target_indices:
                    if src_idx != tgt_idx:
                        # Source -> Target
                        mask[tgt_idx, src_idx] = True
                        # Target -> Source (bidirectional)
                        mask[src_idx, tgt_idx] = True

        # Apply mask
        filtered[~mask] = 0

        # Apply strength threshold
        filtered[np.abs(filtered) < strength_threshold] = 0

        n_connections = np.count_nonzero(filtered)
        print(f"\nFiltered to {n_connections} connections")
        if source_regions:
            print(f"  Source regions: {[roi_names[i] for i in source_indices]}")

        return filtered

    def plot_connectome(
        self,
        connectivity_matrix: np.ndarray,
        node_coords: np.ndarray,
        output_file: str,
        title: str = "Brain Connectivity",
        edge_threshold: str = "90%",
        node_size: float = 50,
        edge_cmap: str = 'coolwarm',
        display_mode: str = 'lyrz',
        annotate: bool = True,
        colorbar: bool = True,
        roi_names: List[str] = None,
        colorbar_label: str = "Connection Strength (Ep)",
        subtitle: str = None,
        radiological: bool = False
    ):
        """
        Create connectivity visualization using nilearn.

        Parameters
        ----------
        connectivity_matrix : np.ndarray
            Connectivity matrix
        node_coords : np.ndarray
            Node coordinates
        output_file : str
            Output file path
        title : str
            Plot title
        edge_threshold : str or float
            Edge threshold (e.g., '90%' or 0.1)
        node_size : float
            Node size
        edge_cmap : str
            Colormap for edges
        display_mode : str
            Display mode: 'lyrz', 'ortho', 'x', 'y', 'z'
        annotate : bool
            Add labels
        colorbar : bool
            Show colorbar
        roi_names : list of str, optional
            Region names for labeling
        colorbar_label : str
            Label for the colorbar (e.g., 'Beta Coefficients', 'Hz')
        subtitle : str, optional
            Additional metadata to show below title
        """
        from nilearn import plotting

        print(f"\nCreating {display_mode} view...")

        # Create figure with extra space for labels - wider for better brain visibility
        fig = plt.figure(figsize=(18, 10))

        # IMPORTANT: Matrix convention for nilearn
        # MATLAB DCM convention: Ep[i,j] = FROM j TO i (rows=targets, cols=sources)
        # Nilearn convention: matrix[i,j] = FROM i TO j (rows=sources, cols=targets)
        # Therefore we MUST transpose to convert conventions
        connectivity_matrix_nilearn = connectivity_matrix.T

        # Create explicit node colors that match our legend
        from matplotlib import cm
        if roi_names is not None:
            node_cmap = cm.get_cmap('tab10')
            node_colors = [node_cmap(i % 10) for i in range(len(roi_names))]
        else:
            node_colors = 'auto'

        # Plot connectome
        display = plotting.plot_connectome(
            connectivity_matrix_nilearn,
            node_coords,
            edge_threshold=edge_threshold,
            node_size=node_size,
            edge_cmap=edge_cmap,
            display_mode=display_mode,
            colorbar=colorbar,
            figure=fig,
            annotate=annotate,
            node_color=node_colors,
            radiological=radiological
        )

        # Add title and subtitle
        if subtitle:
            fig.suptitle(f"{title}\n{subtitle}", fontsize=14, fontweight='bold', y=0.98)
        else:
            plt.suptitle(title, fontsize=16, fontweight='bold')

        # Add colorbar label - find the rightmost axis (colorbar)
        if colorbar and len(fig.axes) > 0:
            # The colorbar is typically the last or rightmost axis
            # Sort axes by their x position to find the rightmost one
            sorted_axes = sorted(fig.axes, key=lambda a: a.get_position().x0, reverse=True)
            if len(sorted_axes) > 0:
                # The rightmost axis is likely the colorbar
                cbar_ax = sorted_axes[0]
                # Check if it's narrow (typical for colorbar)
                pos = cbar_ax.get_position()
                if pos.width < 0.1:  # Colorbar is usually narrow
                    cbar_ax.set_ylabel(colorbar_label, fontsize=11, rotation=270, labelpad=20)

        # Add node legend if roi_names provided
        if roi_names is not None and len(roi_names) <= 15:
            from matplotlib.patches import Patch
            # Use the SAME colors we assigned to nodes
            legend_handles = []
            for i, name in enumerate(roi_names):
                # Shorten long names for display
                short_name = name.replace('_L', ' L').replace('_R', ' R')
                legend_handles.append(Patch(facecolor=node_colors[i], label=short_name))

            # Add legend outside the plot
            fig.legend(handles=legend_handles, loc='lower center', ncol=min(5, len(roi_names)),
                      fontsize=8, frameon=True, title='Brain Regions', title_fontsize=9,
                      bbox_to_anchor=(0.5, -0.02))

        plt.tight_layout()

        # Save
        print(f"  Saving to {output_file}...")
        plt.savefig(output_file, dpi=300, bbox_inches='tight', pad_inches=0.3)
        plt.close()
        print(f"  ✓ Saved!")

    def plot_glass_brain(
        self,
        connectivity_matrix: np.ndarray,
        node_coords: np.ndarray,
        output_file: str,
        title: str = "Brain Connectivity (Glass Brain)",
        edge_threshold: str = "90%",
        node_size: float = 50,
        edge_cmap: str = 'coolwarm',
        colorbar: bool = True,
        roi_names: List[str] = None,
        colorbar_label: str = "Connection Strength (Ep)",
        subtitle: str = None,
        radiological: bool = False
    ):
        """
        Create glass brain visualization.

        Parameters
        ----------
        connectivity_matrix : np.ndarray
            Connectivity matrix
        node_coords : np.ndarray
            Node coordinates
        output_file : str
            Output file path
        title : str
            Plot title
        edge_threshold : str or float
            Edge threshold
        node_size : float
            Node size
        edge_cmap : str
            Colormap
        colorbar : bool
            Show colorbar
        roi_names : list of str, optional
            Region names for labeling
        colorbar_label : str
            Label for the colorbar
        subtitle : str, optional
            Additional metadata to show below title
        """
        from nilearn import plotting

        print(f"\nCreating glass brain view...")

        fig = plt.figure(figsize=(16, 6))

        # IMPORTANT: Matrix convention conversion
        # MATLAB DCM convention: Ep[i,j] = FROM j TO i (rows=targets, cols=sources)
        # Nilearn convention: matrix[i,j] = FROM i TO j (rows=sources, cols=targets)
        # Therefore we MUST transpose to convert conventions
        connectivity_matrix_nilearn = connectivity_matrix.T

        # Create glass brain plot
        display = plotting.plot_connectome(
            connectivity_matrix_nilearn,
            node_coords,
            edge_threshold=edge_threshold,
            node_size=node_size,
            edge_cmap=edge_cmap,
            display_mode='lyrz',
            colorbar=colorbar,
            figure=fig,
            black_bg=False,
            radiological=radiological
        )

        # Add title and subtitle
        if subtitle:
            fig.suptitle(f"{title}\n{subtitle}", fontsize=14, fontweight='bold', y=0.98)
        else:
            plt.suptitle(title, fontsize=16, fontweight='bold')

        # Add colorbar label - find the rightmost axis (colorbar)
        if colorbar and len(fig.axes) > 0:
            sorted_axes = sorted(fig.axes, key=lambda a: a.get_position().x0, reverse=True)
            if len(sorted_axes) > 0:
                cbar_ax = sorted_axes[0]
                pos = cbar_ax.get_position()
                if pos.width < 0.1:  # Colorbar is usually narrow
                    cbar_ax.set_ylabel(colorbar_label, fontsize=11, rotation=270, labelpad=20)

        # Add node legend if roi_names provided
        if roi_names is not None and len(roi_names) <= 15:
            from matplotlib import cm
            from matplotlib.patches import Patch
            node_cmap = cm.get_cmap('Set3' if len(roi_names) > 10 else 'tab10')
            colors = [node_cmap(i / len(roi_names)) for i in range(len(roi_names))]

            legend_handles = []
            for i, name in enumerate(roi_names):
                short_name = name.replace('_L', ' L').replace('_R', ' R')
                legend_handles.append(Patch(facecolor=colors[i], label=short_name))

            fig.legend(handles=legend_handles, loc='lower center', ncol=min(5, len(roi_names)),
                      fontsize=8, frameon=True, title='Brain Regions', title_fontsize=9,
                      bbox_to_anchor=(0.5, -0.02))

        plt.tight_layout()

        print(f"  Saving to {output_file}...")
        plt.savefig(output_file, dpi=300, bbox_inches='tight', pad_inches=0.3)
        plt.close()
        print(f"  ✓ Saved!")

    def plot_overlay_connectome(
        self,
        connectivity_matrices: List[np.ndarray],
        node_coords: np.ndarray,
        output_file: str,
        condition_names: List[str],
        title: str = "Multi-Condition Connectivity Overlay",
        edge_threshold: str = "0%",
        node_size: float = 80,
        edge_cmaps: List[str] = None,
        display_mode: str = 'lyrz',
        colorbar: bool = False,
        roi_names: List[str] = None,
        subtitle: str = None,
        radiological: bool = False,
        edge_alpha: float = 0.6,
        edge_linewidth: float = 2
    ):
        """
        Overlay multiple connectivity matrices with different colors on same brain.

        Uses nilearn's add_graph() method to overlay conditions with semi-transparent edges.
        Edges will overlap but use different colormaps for visual distinction.

        Parameters
        ----------
        connectivity_matrices : List[np.ndarray]
            List of connectivity matrices to overlay
        node_coords : np.ndarray
            Node coordinates (shared across conditions)
        output_file : str
            Output file path
        condition_names : List[str]
            Names of conditions (e.g., ['Rest', 'Music', 'Movie', 'Meditation'])
        title : str
            Plot title
        edge_threshold : str or float
            Edge threshold (e.g., '0%' shows all connections)
        node_size : float
            Node size
        edge_cmaps : List[str], optional
            Colormaps for each condition. If None, uses ['Reds', 'Blues', 'Greens', 'Purples']
        display_mode : str
            Display mode: 'lyrz', 'ortho', 'x', 'y', 'z'
        colorbar : bool
            Show colorbar (typically False for overlays)
        roi_names : list of str, optional
            Region names for labeling
        subtitle : str, optional
            Additional metadata to show below title
        radiological : bool
            Radiological view (left on left)
        edge_alpha : float
            Edge transparency (0-1, default 0.6)
        edge_linewidth : float
            Edge line width (default 2)
        """
        from nilearn import plotting
        from matplotlib.patches import Patch

        # Default colormaps if not provided
        if edge_cmaps is None:
            edge_cmaps = ['Reds', 'Blues', 'Greens', 'Purples', 'Oranges', 'RdPu']

        # Ensure we have enough colormaps
        if len(edge_cmaps) < len(connectivity_matrices):
            edge_cmaps = edge_cmaps * (len(connectivity_matrices) // len(edge_cmaps) + 1)

        print(f"\nCreating overlay {display_mode} view for {len(connectivity_matrices)} conditions...")

        # Create figure
        fig = plt.figure(figsize=(18, 10))

        # Plot first condition
        print(f"  Adding condition 1: {condition_names[0]}...")
        connectivity_nilearn_0 = connectivity_matrices[0].T  # MATLAB→nilearn convention

        # Create explicit node colors that match our legend
        from matplotlib import cm
        if roi_names is not None:
            node_cmap = cm.get_cmap('tab10')
            node_colors = [node_cmap(i % 10) for i in range(len(roi_names))]
        else:
            node_colors = 'auto'

        display = plotting.plot_connectome(
            connectivity_nilearn_0,
            node_coords,
            edge_threshold=edge_threshold,
            node_size=node_size,
            edge_cmap=edge_cmaps[0],
            display_mode=display_mode,
            colorbar=colorbar,
            figure=fig,
            node_color=node_colors,
            radiological=radiological,
            edge_kwargs={'alpha': edge_alpha, 'linewidth': edge_linewidth}
        )

        # Overlay additional conditions using add_graph()
        for i in range(1, len(connectivity_matrices)):
            print(f"  Adding condition {i+1}: {condition_names[i]}...")
            connectivity_nilearn_i = connectivity_matrices[i].T  # MATLAB→nilearn convention

            display.add_graph(
                connectivity_nilearn_i,
                node_coords,
                edge_threshold=edge_threshold,
                node_size=node_size,
                edge_cmap=edge_cmaps[i],
                edge_kwargs={'alpha': edge_alpha, 'linewidth': edge_linewidth}
            )

        # Add title and subtitle
        if subtitle:
            fig.suptitle(f"{title}\n{subtitle}", fontsize=14, fontweight='bold', y=0.98)
        else:
            plt.suptitle(title, fontsize=16, fontweight='bold')

        # Add custom legend for conditions (showing edge colors)
        legend_handles = []
        for i, name in enumerate(condition_names):
            # Get representative color from colormap
            cmap = cm.get_cmap(edge_cmaps[i])
            color = cmap(0.7)  # Use upper range of colormap
            legend_handles.append(Patch(facecolor=color, label=name, alpha=edge_alpha))

        # Add condition legend
        fig.legend(handles=legend_handles, loc='upper right', ncol=1,
                  fontsize=10, frameon=True, title='Conditions', title_fontsize=11,
                  bbox_to_anchor=(0.98, 0.95))

        # Add node legend if roi_names provided (bottom)
        if roi_names is not None and len(roi_names) <= 15:
            node_legend_handles = []
            for i, name in enumerate(roi_names):
                short_name = name.replace('_L', ' L').replace('_R', ' R')
                node_legend_handles.append(Patch(facecolor=node_colors[i], label=short_name))

            fig.legend(handles=node_legend_handles, loc='lower center', ncol=min(5, len(roi_names)),
                      fontsize=8, frameon=True, title='Brain Regions', title_fontsize=9,
                      bbox_to_anchor=(0.5, -0.02))

        plt.tight_layout()

        # Save
        print(f"  Saving to {output_file}...")
        plt.savefig(output_file, dpi=300, bbox_inches='tight', pad_inches=0.3)
        plt.close()
        print(f"  ✓ Saved!")

    def plot_sidebyside_connectome(
        self,
        connectivity_matrices: List[np.ndarray],
        node_coords: np.ndarray,
        output_file: str,
        condition_names: List[str],
        title: str = "Multi-Condition Connectivity Comparison",
        edge_threshold: str = "0%",
        node_size: float = 70,
        edge_cmap: str = 'coolwarm',
        colorbar: bool = True,
        roi_names: List[str] = None,
        subtitle: str = None,
        radiological: bool = False,
        colorbar_label: str = None
    ):
        """
        Create side-by-side panel comparison of multiple conditions.

        Each condition gets its own brain view in a grid layout.
        Clean, publication-ready approach for comparing conditions.

        Parameters
        ----------
        connectivity_matrices : List[np.ndarray]
            List of connectivity matrices to compare
        node_coords : np.ndarray
            Node coordinates (shared across conditions)
        output_file : str
            Output file path
        condition_names : List[str]
            Names of conditions (e.g., ['Rest', 'Music', 'Movie', 'Meditation'])
        title : str
            Main plot title
        edge_threshold : str or float
            Edge threshold
        node_size : float
            Node size
        edge_cmap : str
            Colormap for edges (shared across all panels)
        colorbar : bool
            Show colorbar
        roi_names : list of str, optional
            Region names for labeling
        subtitle : str, optional
            Additional metadata
        radiological : bool
            Radiological view (left on left)
        colorbar_label : str, optional
            Custom label for colorbar (overrides automatic label)
        """
        from nilearn import plotting
        import matplotlib.gridspec as gridspec

        n_conditions = len(connectivity_matrices)

        # Determine grid layout
        if n_conditions <= 2:
            nrows, ncols = 1, n_conditions
            figsize = (18, 8)
        elif n_conditions <= 4:
            nrows, ncols = 2, 2
            figsize = (20, 16)
        else:
            nrows = (n_conditions + 2) // 3
            ncols = 3
            figsize = (24, 8 * nrows)

        print(f"\nCreating side-by-side comparison with {n_conditions} conditions...")
        print(f"  Layout: {nrows}x{ncols} grid")

        # Create figure with gridspec
        fig = plt.figure(figsize=figsize)
        gs = gridspec.GridSpec(nrows, ncols, figure=fig,
                              hspace=0.15, wspace=0.1,
                              top=0.92, bottom=0.08)

        # Find global min/max for consistent colormapping
        all_values = np.concatenate([mat[mat != 0] for mat in connectivity_matrices])

        if len(all_values) == 0:
            # No connections in any condition - use default range
            vmin, vmax = -0.1, 0.1
            print(f"  No connections found in any condition - using default range")
        else:
            vmin, vmax = all_values.min(), all_values.max()
            # Make symmetric around zero for diverging colormaps
            abs_max = max(abs(vmin), abs(vmax))
            vmin, vmax = -abs_max, abs_max
            print(f"  Value range: [{vmin:.3f}, {vmax:.3f}]")

        # Plot each condition in its own subplot
        for idx, (conn_matrix, cond_name) in enumerate(zip(connectivity_matrices, condition_names)):
            row = idx // ncols
            col = idx % ncols

            print(f"  Panel {idx+1}: {cond_name} (row {row}, col {col})...")

            # Create subplot for this condition
            ax = fig.add_subplot(gs[row, col])

            # MATLAB→nilearn convention
            connectivity_nilearn = conn_matrix.T

            # Handle custom colormaps
            if edge_cmap == 'green_purple':
                cmap_to_use = GREEN_PURPLE_CMAP
            else:
                cmap_to_use = edge_cmap

            # Plot connectome
            display = plotting.plot_connectome(
                connectivity_nilearn,
                node_coords,
                edge_threshold=edge_threshold,
                node_size=node_size,
                edge_cmap=cmap_to_use,
                display_mode='z',  # Axial view for panels
                colorbar=False,  # Add single shared colorbar later
                figure=fig,
                axes=ax,
                radiological=radiological,
                edge_vmin=vmin,
                edge_vmax=vmax,
                annotate=True,
                node_kwargs={'alpha': 0.8}
            )

            # Increase L/R annotation font size by 20% (from default ~10 to 12)
            for txt in ax.texts:
                if txt.get_text() in ['L', 'R']:
                    current_size = txt.get_fontsize()
                    txt.set_fontsize(current_size * 1.2)

            # Add subplot title
            ax.set_title(cond_name, fontsize=20, fontweight='bold', pad=10)

        # Add main title (ignore subtitle for cleaner appearance)
        fig.suptitle(title, fontsize=24, fontweight='bold', y=0.98)

        # Add single shared colorbar
        if colorbar:
            from matplotlib import cm
            from matplotlib.colors import Normalize

            # Create colorbar axes
            cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])

            # Handle custom colormaps
            if colorbar_label:
                # Use custom label if provided
                cbar_label = colorbar_label
            elif edge_cmap == 'green_purple':
                cbar_label = 'Change Magnitude (Hz)'
            else:
                cbar_label = 'Δ Connection Strength (Hz)'

            # Get colormap object
            if edge_cmap == 'green_purple':
                cmap_obj = GREEN_PURPLE_CMAP
            else:
                cmap_obj = cm.get_cmap(edge_cmap)

            norm = Normalize(vmin=vmin, vmax=vmax)
            sm = cm.ScalarMappable(cmap=cmap_obj, norm=norm)
            sm.set_array([])
            cbar = fig.colorbar(sm, cax=cbar_ax)
            cbar.set_label(cbar_label, rotation=270, labelpad=30, fontsize=20)
            cbar.ax.tick_params(labelsize=18)  # Increase colorbar tick label size

        # Save as both PNG and SVG
        print(f"  Saving to {output_file}...")
        plt.savefig(output_file, dpi=300, bbox_inches='tight', pad_inches=0.3)
        # Also save as SVG
        svg_file = str(output_file).replace('.png', '.svg')
        plt.savefig(svg_file, format='svg', bbox_inches='tight', pad_inches=0.3)
        plt.close()
        print(f"  ✓ Saved PNG and SVG!")


def main():
    """Main CLI entry point."""

    parser = argparse.ArgumentParser(
        description='Visualize brain connectivity from DCM PEB results using nilearn',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:

  # dlPFC outgoing connections
  python plot_nilearn_connectivity.py \\
    --mat-files PEB_change_rest.mat \\
    --conditions Rest \\
    --source-regions Frontal_Mid_L Frontal_Mid_R \\
    --connection-type outgoing \\
    --output dlpfc_connectivity.png

  # Glass brain view
  python plot_nilearn_connectivity.py \\
    --mat-files PEB_change_music.mat \\
    --conditions Music \\
    --display-mode glass \\
    --output music_glass_brain.png
        """
    )

    # Required arguments
    parser.add_argument('--mat-files', nargs='+', required=True,
                        help='Path(s) to PEB .mat files')
    parser.add_argument('--conditions', nargs='+', required=True,
                        help='Labels for each condition/file')

    # Filtering arguments
    parser.add_argument('--source-regions', nargs='+',
                        help='Source regions (partial name matching)')
    parser.add_argument('--target-regions', nargs='+',
                        help='Target regions (default: all)')
    parser.add_argument('--connection-type', choices=['outgoing', 'incoming', 'bidirectional'],
                        default='outgoing',
                        help='Type of connections (default: outgoing)')

    # Threshold arguments
    parser.add_argument('--pp-threshold', type=float, default=0.99,
                        help='Posterior probability threshold (default: 0.99)')
    parser.add_argument('--strength-threshold', type=float, default=0.0,
                        help='Minimum connection strength (default: 0.0)')
    parser.add_argument('--edge-threshold', default='90%',
                        help='Edge display threshold (default: 90%%)')

    # Visual arguments
    parser.add_argument('--node-size', type=float, default=50,
                        help='Node size (default: 50)')
    parser.add_argument('--edge-cmap', default='coolwarm',
                        help='Edge colormap (default: coolwarm)')
    parser.add_argument('--display-mode', default='lyrz',
                        choices=['lyrz', 'ortho', 'x', 'y', 'z', 'glass'],
                        help='Display mode (default: lyrz)')

    # Output arguments
    parser.add_argument('--output', required=True,
                        help='Output file path (PNG, PDF, SVG)')
    parser.add_argument('--colorbar', action='store_true', default=True,
                        help='Show colorbar (default: True)')
    parser.add_argument('--title', type=str, default=None,
                        help='Custom figure title (default: auto-generated from condition)')
    parser.add_argument('--colorbar-label', type=str, default='Connection Strength (Ep)',
                        help='Label for colorbar (default: "Connection Strength (Ep)")')
    parser.add_argument('--subtitle', type=str, default=None,
                        help='Subtitle with metadata (default: auto-generated from mat file)')

    args = parser.parse_args()

    # Validate
    if len(args.mat_files) != len(args.conditions):
        parser.error("Number of --mat-files must match number of --conditions")

    print("="*60)
    print("nilearn Brain Connectivity Visualization")
    print("="*60)

    # Initialize
    coord_mapper = AALCoordinateMapper()
    visualizer = NilearnConnectivityVisualizer(coord_mapper)

    # Process first file (multi-file support coming later)
    mat_file = args.mat_files[0]
    condition = args.conditions[0]

    # Load connectivity
    conn_matrix, roi_names = visualizer.load_connectivity(
        mat_file,
        pp_threshold=args.pp_threshold
    )

    # Filter
    filtered_matrix = visualizer.filter_connections(
        conn_matrix,
        roi_names,
        source_regions=args.source_regions,
        target_regions=args.target_regions,
        connection_type=args.connection_type,
        strength_threshold=args.strength_threshold
    )

    # Get coordinates
    node_coords = coord_mapper.get_coordinates(roi_names)

    # Determine title
    plot_title = args.title if args.title else f"{condition} - Brain Connectivity"

    # Generate subtitle with metadata if not provided
    if args.subtitle:
        plot_subtitle = args.subtitle
    else:
        # Extract metadata from filename
        mat_basename = Path(mat_file).stem
        # Parse filename components
        parts = mat_basename.replace('_noFD', '').replace('_Aconstrained', ' (Constrained)').split('_')

        # Identify analysis type
        if 'change' in mat_basename:
            analysis_type = "Session Change"
            # Extract sessions
            for part in parts:
                if 'ses-' in part:
                    sessions = part.replace('-ses-', ' vs ses-')
                    analysis_type = f"Change: ses{sessions}"
        elif 'contrast' in mat_basename:
            analysis_type = "Task Contrast"
            # Extract tasks
            for part in parts:
                if 'task-' in part:
                    tasks = part.replace('-task-', ' vs ')
                    analysis_type = f"Contrast: {tasks}"
        elif 'behav' in mat_basename:
            analysis_type = "Behavioral Association"
            # Extract covariates
            cov_parts = [p for p in parts if p.startswith('cov-')]
            if cov_parts:
                covariate = cov_parts[0].replace('cov-', '').replace('_', ' ')
                analysis_type = f"Behavioral: {covariate}"
        else:
            analysis_type = "PEB Analysis"

        # Add connection info
        conn_info = f"{args.connection_type.capitalize()} connections"
        if args.source_regions:
            src_str = ', '.join(args.source_regions[:3])
            if len(args.source_regions) > 3:
                src_str += '...'
            conn_info = f"{conn_info} from {src_str}"

        plot_subtitle = f"Matrix: {mat_basename}\n{analysis_type} | {conn_info} | Pp>{args.pp_threshold}"

    # Get colorbar label
    colorbar_label = getattr(args, 'colorbar_label', 'Connection Strength (Ep)')

    # Plot
    if args.display_mode == 'glass':
        visualizer.plot_glass_brain(
            filtered_matrix,
            node_coords,
            args.output,
            title=plot_title,
            edge_threshold=args.edge_threshold,
            node_size=args.node_size,
            edge_cmap=args.edge_cmap,
            colorbar=args.colorbar,
            roi_names=roi_names,
            colorbar_label=colorbar_label,
            subtitle=plot_subtitle
        )
    else:
        visualizer.plot_connectome(
            filtered_matrix,
            node_coords,
            args.output,
            title=plot_title,
            edge_threshold=args.edge_threshold,
            node_size=args.node_size,
            edge_cmap=args.edge_cmap,
            display_mode=args.display_mode,
            colorbar=args.colorbar,
            roi_names=roi_names,
            colorbar_label=colorbar_label,
            subtitle=plot_subtitle
        )

    print("\n" + "="*60)
    print("✓ Complete!")
    print("="*60)

    return 0


if __name__ == '__main__':
    sys.exit(main())
