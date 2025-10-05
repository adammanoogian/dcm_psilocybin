"""
PEB Results Visualization

Loads and visualizes PEB (Parametric Empirical Bayes) results from DCM analyses.
Supports standard PEB plots and specialized "change toward zero" analysis.

Classes:
    PEBDataLoader: Loads .mat files and extracts PEB data
    PEBPlotter: Creates heatmap visualizations

Usage:
    loader = PEBDataLoader('peb_results.mat')
    plotter = PEBPlotter(loader)
    plotter.plot_heatmaps()
    plotter.save_all_svgs()
"""
import os
import re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.io import loadmat
import h5py

# =============================================================================
# DATA LOADING AND EXTRACTION CLASSES
# =============================================================================

class PEBDataLoader:
    """
    PEB Data Loader for MATLAB .mat Files
    
    Handles loading, parsing, and extraction of Parametric Empirical Bayes (PEB)
    results from Dynamic Causal Modeling analyses stored in MATLAB format.
    
    This class provides robust loading of PEB data structures including:
    - Bayesian Model Averaging (BMA) results
    - Group Connectivity Models (GCM) 
    - ROI names and parameter structures
    - Posterior expectations and probabilities
    
    Attributes:
        mat_file_path (str): Path to the input .mat file
        params (dict): Processing parameters (thresholds, font sizes, etc.)
        data (dict): Extracted PEB data including model, BMA, GCM, ROI names
        
    Methods:
        get_data(): Returns the extracted data dictionary
        load_file(): Interactive file selection dialog
        _extract_peb_data(): Core data extraction from .mat file
    """
    def __init__(self, mat_file_path=None, params=None):
        if mat_file_path is None:
            mat_file_path = self.load_file()
        self.mat_file_path = mat_file_path
        if params is None:
            params = self.get_peb_plot_parameters()
        self.params = params
        self.data = self._extract_peb_data()

    def _extract_peb_data(self):
        try:
            mat = loadmat(self.mat_file_path, squeeze_me=True, struct_as_record=False)
        except NotImplementedError:
            with h5py.File(self.mat_file_path, 'r') as f:
                raise NotImplementedError(".mat v7.3+ loading not implemented in this stub.")

        model_name = self.params['model']
        if model_name not in mat:
            raise KeyError(f"{model_name} variable not loaded in the workspace")
        model = self.matstruct_to_dict(mat[model_name])

        if 'BMA' not in mat or 'GCM' not in mat:
            raise KeyError("BMA or GCM data not found in the PEB file")
        bma = self.matstruct_to_dict(mat['BMA'])
        gcm = self.matstruct_to_dict(mat['GCM'])

        roi_names = mat.get('ROI_names', None)
        if roi_names is None:
            # Try to extract ROI names from GCM
            roi_names = self.get_ROI_names_from_GCM(gcm)
            if roi_names is None:
                raise KeyError("ROI_names not found in the .mat file and could not be extracted from GCM.")

        peb_type = mat.get('PEB_type', None)

        return {
            'model': model,
            'bma': bma,
            'gcm': gcm,
            'roi_names': roi_names,
            'peb_type': peb_type,
            'mat': mat
        }

    def get_data(self):
        return self.data

    @staticmethod
    def get_peb_plot_parameters():
        """
        Return a dictionary of parameters for PEB plotting, matching the MATLAB script.
        """
        params = {
            'model': 'BMA',
            'pp_threshold': 0.99,
            'roi_reorder': None,  # Can be set to a list of indices if needed
            'font_size': 12,
            'revert_diag': True
        }
        return params

    @staticmethod
    def load_file(mat_file_path=None):
        """
        Prompt the user to select a PEB .mat file if no path is provided.
        Returns the file path.
        """
        import os
        if mat_file_path is None:
            try:
                import tkinter as tk
                from tkinter import filedialog
                root = tk.Tk()
                root.withdraw()
                mat_file_path = filedialog.askopenfilename(
                    title="Select PEB .mat file",
                    filetypes=[("MATLAB files", "*.mat")]
                )
            except ImportError:
                raise RuntimeError("tkinter is required for file dialog. Please provide a file path.")
        if not mat_file_path or not os.path.isfile(mat_file_path):
            raise FileNotFoundError(f"File not found: {mat_file_path}")
        return mat_file_path
    
    @staticmethod
    def matstruct_to_dict(matobj):
        """
        Recursively convert mat_struct objects to nested dictionaries, and convert any scipy.sparse matrix to dense arrays. Handles all nested fields.
        """
        import numpy as np
        from scipy.io.matlab import mat_struct
        try:
            import scipy.sparse as sp
        except ImportError:
            sp = None

        # Convert any scipy sparse matrix to dense
        if sp is not None and sp.issparse(matobj):
            return matobj.toarray()

        # Recursively handle mat_struct
        if isinstance(matobj, mat_struct):
            result = {}
            for fieldname in matobj._fieldnames:
                elem = getattr(matobj, fieldname)
                result[fieldname] = PEBDataLoader.matstruct_to_dict(elem)
            return result

        # Recursively handle dict
        if isinstance(matobj, dict):
            return {k: PEBDataLoader.matstruct_to_dict(v) for k, v in matobj.items()}

        # Recursively handle list or tuple
        if isinstance(matobj, (list, tuple)):
            return [PEBDataLoader.matstruct_to_dict(item) for item in matobj]

        # Recursively handle numpy arrays
        if isinstance(matobj, np.ndarray):
            # If array of objects, recurse into each
            if matobj.dtype == object:
                return [PEBDataLoader.matstruct_to_dict(item) for item in matobj]
            else:
                return matobj

        # Return as is for other types
        return matobj

    @staticmethod
    def get_ROI_names_from_GCM(gcm):
        """
        Extract ROI names from the first DCM file in the GCM cell array.
        Equivalent to the MATLAB get_ROI_names_from_GCM function.
        
        Args:
            gcm: GCM data structure from .mat file
            
        Returns:
            list: ROI names extracted from the first DCM file
        """
        try:
            # Get the first DCM file path
            if isinstance(gcm, np.ndarray) and len(gcm) > 0:
                f_DCM = gcm[0] if isinstance(gcm[0], str) else str(gcm[0])
            elif isinstance(gcm, list) and len(gcm) > 0:
                f_DCM = gcm[0] if isinstance(gcm[0], str) else str(gcm[0])
            else:
                raise ValueError("Invalid GCM structure")
            
            # Handle path conversion matching MATLAB regex logic
            import re
            pattern = r"/home/.*/([a-zA-Z]{2}\d{2})(?:_scratch)?/"
            matches = re.search(pattern, f_DCM)
            if matches:
                project_id = matches.group(1)
                if "_scratch" in f_DCM:
                    f_DCM = re.sub(r"/home/.*/([a-zA-Z]{2}\d{2})_scratch/", f"/scratch/{project_id}/", f_DCM)
                else:
                    f_DCM = re.sub(r"/home/.*/([a-zA-Z]{2}\d{2})/", f"/projects/{project_id}/", f_DCM)
            
            # Load the DCM file
            try:
                dcm_data = loadmat(f_DCM, squeeze_me=True, struct_as_record=False)
                DCM = dcm_data['DCM']
                
                # Extract ROI names from DCM.xY.name  
                if hasattr(DCM, 'xY') and hasattr(DCM.xY, 'name'):
                    roi_names = [str(name) for name in DCM.xY.name]
                    return roi_names
                else:
                    raise KeyError("DCM.xY.name not found")
                    
            except Exception as e:
                print(f"Warning: Could not load DCM file {f_DCM}: {e}")
                return None
                
        except Exception as e:
            print(f"Error extracting ROI names from GCM: {e}")
            return None

    @staticmethod
    def parse_parameter_names(pnames):
        """
        Parse parameter names to extract field, row, and column indices.
        Equivalent to the MATLAB parameter parsing logic in PEB_reshape_posterior.
        
        Args:
            pnames: List of parameter names (e.g., ['A(1,1)', 'A(1,2)', ...])
            
        Returns:
            list: List of dicts with 'field', 'row', 'col' keys
        """
        parts = []
        pattern = r'(?P<field>[A-Za-z0-9\{\},]+)\((?P<row>\d+)(,|\))(?P<col>\d+)?(,|\))?'
        
        for pname in pnames:
            match = re.search(pattern, str(pname))
            if match:
                part = {
                    'field': match.group('field'),
                    'row': int(match.group('row')),
                    'col': int(match.group('col')) if match.group('col') else None
                }
                parts.append(part)
            else:
                # Fallback for parameters that don't match pattern
                parts.append({'field': str(pname), 'row': None, 'col': None})
        
        return parts

    @staticmethod
    def reshape_posterior_simple(model_data, roi_n):
        """
        Reshape BMA.Ep vector into connectivity matrices.
        Handles both full connectivity and constrained (sparse) connectivity models.
        
        Args:
            model_data: Model data (BMA) containing Ep, Pp
            roi_n: Number of ROIs
            
        Returns:
            tuple: (reshaped_Ep, reshaped_Pp, param_n) where Ep and Pp are (roi_n, roi_n, cov_n)
        """
        # Get number of covariates
        if hasattr(model_data, 'M') and hasattr(model_data.M, 'X'):
            cov_n = model_data.M.X.shape[1]
        else:
            cov_n = model_data['M']['X'].shape[1] if 'M' in model_data and 'X' in model_data['M'] else 1
        
        # Get Ep and Pp as flat vectors
        Ep = getattr(model_data, 'Ep', model_data.get('Ep'))
        Pp = getattr(model_data, 'Pp', model_data.get('Pp'))
        
        # Convert sparse to dense if needed
        if hasattr(Ep, 'toarray'):
            Ep = Ep.toarray()
        if hasattr(Pp, 'toarray'):
            Pp = Pp.toarray()
            
        # Flatten to ensure we have 1D arrays
        Ep = Ep.flatten()
        Pp = Pp.flatten()
        
        param_n_full = roi_n * roi_n  # Full connectivity parameters per covariate
        param_n_actual = len(Ep) // cov_n  # Actual parameters per covariate
        total_expected_full = param_n_full * cov_n
        total_actual = len(Ep)
        
        print(f"Debug: Ep length={total_actual}, full_expected={total_expected_full}, roi_n={roi_n}, cov_n={cov_n}")
        print(f"Debug: Actual params per cov={param_n_actual}, Full params per cov={param_n_full}")
        
        # Check if this is a constrained (sparse) connectivity model
        is_constrained = (total_actual != total_expected_full)
        
        if is_constrained:
            print(f"Debug: Detected constrained connectivity model ({param_n_actual}/{param_n_full} connections)")
            return PEBDataLoader.reshape_posterior_constrained(model_data, roi_n, cov_n, Ep, Pp)
        else:
            print(f"Debug: Detected full connectivity model")
            return PEBDataLoader.reshape_posterior_full(roi_n, cov_n, Ep, Pp, param_n_full)
    
    @staticmethod
    def reshape_posterior_full(roi_n, cov_n, Ep, Pp, param_n):
        """
        Reshape full connectivity model (all roi_n x roi_n connections present).
        """
        # Reshape into (roi_n, roi_n, cov_n)
        Ep_reshaped = np.zeros((roi_n, roi_n, cov_n))
        Pp_reshaped = np.zeros((roi_n, roi_n, cov_n))
        
        for i_cov in range(cov_n):
            start_idx = i_cov * param_n
            end_idx = (i_cov + 1) * param_n
            
            cov_data_ep = Ep[start_idx:end_idx].reshape(roi_n, roi_n)
            cov_data_pp = Pp[start_idx:end_idx].reshape(roi_n, roi_n)
            
            Ep_reshaped[:, :, i_cov] = cov_data_ep
            Pp_reshaped[:, :, i_cov] = cov_data_pp
        
        return Ep_reshaped, Pp_reshaped, param_n
    
    @staticmethod
    def reshape_posterior_constrained(model_data, roi_n, cov_n, Ep, Pp):
        """
        Reshape constrained connectivity model using parameter names to map connections.
        """
        param_n_actual = len(Ep) // cov_n
        
        # Try to get parameter names to determine which connections are estimated
        pnames = None
        if hasattr(model_data, 'Pnames'):
            pnames = getattr(model_data, 'Pnames')
        elif 'Pnames' in model_data:
            pnames = model_data['Pnames']
        
        if pnames is not None:
            return PEBDataLoader.reshape_with_parameter_names(roi_n, cov_n, Ep, Pp, pnames)
        else:
            # Fallback: assume connections are in row-major order for active connections only
            print("Warning: No parameter names found, using fallback method for constrained model")
            return PEBDataLoader.reshape_constrained_fallback(roi_n, cov_n, Ep, Pp, param_n_actual)
    
    @staticmethod
    def reshape_with_parameter_names(roi_n, cov_n, Ep, Pp, pnames):
        """
        Use parameter names to map constrained connections to full connectivity matrix.
        """
        param_n_actual = len(Ep) // cov_n
        
        # Parse parameter names to get connection indices
        param_info = PEBDataLoader.parse_parameter_names(pnames[:param_n_actual])
        
        # Initialize full connectivity matrices
        Ep_reshaped = np.zeros((roi_n, roi_n, cov_n))
        Pp_reshaped = np.zeros((roi_n, roi_n, cov_n))
        
        # Map constrained parameters to full matrix
        for i_cov in range(cov_n):
            start_idx = i_cov * param_n_actual
            
            for i_param, param in enumerate(param_info):
                if param['row'] is not None and param['col'] is not None:
                    # Convert to 0-based indexing
                    row_idx = param['row'] - 1
                    col_idx = param['col'] - 1
                    
                    if 0 <= row_idx < roi_n and 0 <= col_idx < roi_n:
                        param_idx = start_idx + i_param
                        Ep_reshaped[row_idx, col_idx, i_cov] = Ep[param_idx]
                        Pp_reshaped[row_idx, col_idx, i_cov] = Pp[param_idx]
        
        return Ep_reshaped, Pp_reshaped, roi_n * roi_n  # Return full param_n for consistency
    
    @staticmethod
    def reshape_constrained_fallback(roi_n, cov_n, Ep, Pp, param_n_actual):
        """
        Fallback method for constrained models without parameter names.
        Assumes parameters are ordered and fills matrix sequentially.
        """
        print(f"Warning: Using fallback reshaping for {param_n_actual} parameters per covariate")
        
        # Initialize full connectivity matrices
        Ep_reshaped = np.zeros((roi_n, roi_n, cov_n))
        Pp_reshaped = np.zeros((roi_n, roi_n, cov_n))
        
        for i_cov in range(cov_n):
            start_idx = i_cov * param_n_actual
            end_idx = (i_cov + 1) * param_n_actual
            
            # Fill available parameters (zeros remain for non-estimated connections)
            cov_ep = Ep[start_idx:end_idx]
            cov_pp = Pp[start_idx:end_idx]
            
            # Map to matrix positions (this is a best-guess approach)
            param_idx = 0
            for i in range(roi_n):
                for j in range(roi_n):
                    if param_idx < len(cov_ep):
                        Ep_reshaped[i, j, i_cov] = cov_ep[param_idx]
                        Pp_reshaped[i, j, i_cov] = cov_pp[param_idx]
                        param_idx += 1
                    if param_idx >= len(cov_ep):
                        break
                if param_idx >= len(cov_ep):
                    break
        
        return Ep_reshaped, Pp_reshaped, roi_n * roi_n


# =============================================================================
# VISUALIZATION CLASSES
# =============================================================================

class PEBPlotter:
    """
    Creates publication-ready heatmap visualizations of PEB results.
    
    Generates connectivity heatmaps with custom colormaps, significance thresholding,
    and specialized visualization for \"change toward zero\" analysis.
    
    Attributes:
        data (dict): PEB data from PEBDataLoader
        figures (list): Generated matplotlib figures
        covariate_names (list): Names of plotted covariates
    """
    def __init__(self, peb_data, mat_file_path, params):
        self.data = peb_data
        self.mat_file_path = mat_file_path
        self.params = params
        self.figures = []
        self.covariate_names = []


    def plot_heatmaps(self):
        model = self.data['model']
        roi_names = self.data['roi_names'].copy()  # Make a copy to avoid modifying original
        font_size = self.params['font_size']
        peb_type = self.data.get('peb_type', None)
        roi_reorder = self.params.get('roi_reorder', None)

        Ep = getattr(model, 'Ep', model['Ep'])
        Pp = getattr(model, 'Pp', model.get('Pp', None))
        cov_names = getattr(model, 'Xnames', model.get('Xnames', None))
        if cov_names is not None and isinstance(cov_names, np.ndarray):
            cov_names = cov_names.tolist()
        elif cov_names is not None:
            cov_names = list(cov_names)  # Ensure it's a list we can modify

        pp_threshold = self.params.get('pp_threshold', 0.99)
        revert_diag = self.params.get('revert_diag', True)

        # Use simple direct reshaping of the vector data
        roi_n = len(roi_names)
        Ep, Pp, param_n = PEBDataLoader.reshape_posterior_simple(model, roi_n)

        cov_n = Ep.shape[2]  # Third dimension is the number of covariates

        # Apply probability threshold: set values below threshold to zero (matching MATLAB)
        if pp_threshold is not None:
            below_thr = Pp < pp_threshold
            Ep[below_thr] = 0

        # Apply diagonal reversion if requested (matching MATLAB order: after threshold, before adding mean)
        # MATLAB applies g(y) = -exp(y)/2 to diagonal elements to revert DCM's log transformation f(x) = log(-2x)
        if revert_diag and peb_type == 'change' and cov_n == 2:
            # Store original diagonal values before any modifications
            original_A1_diag = np.diag(Ep[:, :, 0]).copy()
            original_A2_diag = np.diag(Ep[:, :, 1]).copy()
            
            # For "change" type with 2 covariates (group 1 mean and change)
            # Cov 1 (mean of group 1): A1_diag = -exp(diag(A1))/2
            A1 = Ep[:, :, 0].copy()
            np.fill_diagonal(A1, -np.exp(original_A1_diag) / 2)
            Ep[:, :, 0] = A1
            
            # Cov 2 (change): A2_diag = exp(diag(A1))/2 - exp(diag(A1+A2))/2  
            A2 = Ep[:, :, 1].copy()
            np.fill_diagonal(A2, np.exp(original_A1_diag) / 2 - np.exp(original_A1_diag + original_A2_diag) / 2)
            Ep[:, :, 1] = A2
            
        elif revert_diag and (peb_type == 'behav_associations' or peb_type == 'groupmean'):
            # For other types: A_diag = -exp(diag(A))/2
            for i_cov in range(cov_n):
                A = Ep[:, :, i_cov].copy()
                np.fill_diagonal(A, -np.exp(np.diag(A)) / 2)
                Ep[:, :, i_cov] = A

        # Change toward zero analysis for 'change' type PEB
        if peb_type == 'change' and cov_n == 2:
            # Final connectivity state (baseline + change)
            Ep_mean = Ep[:, :, 0] + Ep[:, :, 1]
            
            # Variables for change analysis
            group1 = Ep[:, :, 0]  # baseline
            group2 = Ep_mean      # final state
            
            change = group2 - group1  # actual change (preserves sign)
            magnitude_change = np.abs(group2) - np.abs(group1)  # distance from zero
            Ep_change_toward_0 = change
            
            sign_change_mask = (group1 * group2) < 0  # sign changes (inhibitory ↔ excitatory)
            
            # Store for custom colormap
            self.magnitude_change = magnitude_change
            
            # Expand array: [baseline, change] → [baseline, change, mean_state, change_toward_zero]
            Ep_new = np.zeros((roi_n, roi_n, cov_n + 2))
            Ep_new[:, :, :cov_n] = Ep
            Ep_new[:, :, cov_n] = Ep_mean
            Ep_new[:, :, cov_n + 1] = Ep_change_toward_0
            Ep = Ep_new
            cov_names = list(cov_names) + ['mean of second group', 'Change toward 0']
            cov_n += 2
            
            # Store for asterisk annotations
            self.sign_change_mask = sign_change_mask

        # Apply ROI reordering if requested (matching MATLAB behavior)
        if roi_reorder is not None:
            if len(roi_reorder) != roi_n:
                raise ValueError("roi_reorder must include all ROI indices")
            # Convert to 0-based indexing if needed
            if all(idx >= 1 for idx in roi_reorder):
                roi_reorder = [idx - 1 for idx in roi_reorder]
            
            # Reorder ROI names
            roi_names = [roi_names[i] for i in roi_reorder]
            
            # Reorder both dimensions of the connectivity matrices
            Ep = Ep[np.ix_(roi_reorder, roi_reorder, range(cov_n))]

        # Diagonal reversion was applied above after thresholding
        
        # A_constrained models for behavioral associations
        if peb_type == 'behav_associations':
            # For A_constrained models: try to use template from corresponding 'change' file
            # or use the available connectivity pattern from current model
            
            # Try to find corresponding change file
            mat_file_path_template = None
            if "Aconstrained" in self.mat_file_path:
                mat_file_path_template = self.mat_file_path.replace("Aconstrained", "")
                if not os.path.isfile(mat_file_path_template):
                    mat_file_path_template = None
            
            if mat_file_path_template and os.path.isfile(mat_file_path_template):
                # Use change file template if available
                try:
                    template_Ep = Ep[:, :, 1] if Ep.shape[2] > 1 else Ep[:, :, 0]
                    template_indices = np.where(~np.isnan(template_Ep) & (template_Ep != 0))
                except IndexError:
                    # Fallback: use any non-zero connections in current model
                    template_indices = np.where(np.any(Ep != 0, axis=2))
            else:
                # Fallback: use any non-zero connections in current model
                print("Warning: No corresponding change file found, using current model connectivity pattern")
                template_indices = np.where(np.any(Ep != 0, axis=2))
            
            # Create rectangles for each non-NaN connection
            rects = []
            for row, col in zip(template_indices[0], template_indices[1]):
                rect = plt.Rectangle((col, row), 1, 1, fill=False, edgecolor='black',
                                    linestyle='dotted', linewidth=2)
                rects.append(rect)



        # behav covariates use normalized beta coefficients
        heat_label = 'Normalized Beta Coefficient' if peb_type == 'behav_associations' else 'Effective Connectivity (Hz)'

        self.figures = []
        self.covariate_names = []
        for i_cov in range(cov_n):
            # Extract the 2D matrix for this covariate (already properly shaped)
            Ep_grid = Ep[:, :, i_cov]
            n_roi = len(roi_names)
            fig, ax = plt.subplots(figsize=(8, 8))

            #check plot condition specs
            # Create custom colormap matching MATLAB (cold-hot with white center)
            from matplotlib.colors import LinearSegmentedColormap
            import matplotlib.colors as mcolors
            
            # Cold colors (white to dark blue)
            cold = np.array([[1, 1, 1],           # White
                            [0, 0.266, 0.533]])   # Dark blue
            
            # Hot colors (white to dark red/orange)  
            hot = np.array([[1, 1, 1],            # White
                           [0.8, 0.2, 0.066]])    # Dark red/orange
                           
            # Create the full colormap: cold (reversed) + hot
            n_colors = 64
            cold_colors = np.linspace(cold[1], cold[0], n_colors)  # Dark blue to white
            hot_colors = np.linspace(hot[0], hot[1], n_colors)     # White to dark red
            
            # Combine colors
            colors = np.vstack([cold_colors, hot_colors])
            cmap = LinearSegmentedColormap.from_list('matlab_custom', colors)
            # if A_constrained and behav_associations, shade in template indices
            if self.data.get('peb_type') == 'behav_associations' and 'rects' in locals():
                for rect in rects:
                    ax.add_patch(rect)
            # Custom colormap for "Change toward 0" plot
            if (cov_names and len(cov_names) > i_cov and cov_names[i_cov] == 'Change toward 0'):
                # Green-Purple colormap: Green=closer to zero, Purple=further from zero
                from matplotlib.colors import LinearSegmentedColormap
                green_purple_colors = [
                    [0.2, 0.7, 0.2],  # Green: closer to zero
                    [1, 1, 1],        # White: no change
                    [0.6, 0.2, 0.8]   # Purple: further from zero
                ]
                cmap = LinearSegmentedColormap.from_list('green_purple', green_purple_colors)
                
                # Use magnitude_change for colors, actual change for display values
                if hasattr(self, 'magnitude_change'):
                    magnitude_data = self.magnitude_change.copy()
                    magnitude_data = np.where(magnitude_data == 0, np.nan, magnitude_data)
                    change_values = plot_data.copy()
                    plot_data = magnitude_data
                
                # Annotations: values + asterisks for sign changes
                annot_array = np.where(Ep_grid == 0, '', 
                    np.array([[f'{val:.2f}*' if hasattr(self, 'sign_change_mask') and self.sign_change_mask[i,j] and val != 0 
                              else f'{val:.2f}' if val != 0 else '' 
                              for j, val in enumerate(row)] 
                             for i, row in enumerate(Ep_grid)]))
            else:
                # Standard MATLAB-style blue-white-red colormap
                from matplotlib.colors import LinearSegmentedColormap
                import matplotlib.colors as mcolors
                
                cold = np.array([[1, 1, 1], [0, 0.266, 0.533]])      # White to dark blue
                hot = np.array([[1, 1, 1], [0.8, 0.2, 0.066]])       # White to dark red
                               
                # Create diverging colormap
                n_colors = 64
                cold_colors = np.linspace(cold[1], cold[0], n_colors)  # Dark blue → white
                hot_colors = np.linspace(hot[0], hot[1], n_colors)     # White → dark red
                
                colors = np.vstack([cold_colors, hot_colors])
                cmap = LinearSegmentedColormap.from_list('matlab_custom', colors)
                
                # Standard annotations
                annot_array = np.where(Ep_grid == 0, '', np.array([[f'{val:.2f}' for val in row] for row in Ep_grid]))
            
            # Handle transparency for standard plots
            if not (cov_names and len(cov_names) > i_cov and cov_names[i_cov] == 'Change toward 0'):
                plot_data = Ep_grid.copy()
                plot_data = np.where(Ep_grid == 0, np.nan, Ep_grid)  # Zeros → NaN for transparency
            
            # Matrix orientation: MATLAB Ep(i,j) = FROM j TO i → transpose for seaborn
            plot_data_transposed = plot_data.T
            annot_array_transposed = annot_array.T
            
            sns.heatmap(plot_data_transposed, annot=annot_array_transposed, fmt='', cmap=cmap, vmin=-0.5, vmax=0.5,
                        xticklabels=roi_names, yticklabels=roi_names, cbar_kws={'label': heat_label}, ax=ax)

            title = f"Posterior Expectation"
            covariate_name = None
            if cov_names and len(cov_names) > i_cov:
                title += f" - {cov_names[i_cov]}"
            covariate_name = cov_names[i_cov]
            ax.set_title(title, fontsize=font_size)
            ax.set_xlabel("From", fontsize=font_size)
            ax.set_ylabel("To", fontsize=font_size)
            plt.xticks(rotation=30)
            plt.tight_layout()
            self.figures.append(fig)
            self.covariate_names.append(covariate_name)


    def save_all_svgs(self, output_dir=None):
        if not self.figures:
            raise RuntimeError("No figures to save. Run plot_heatmaps() first.")
        base_name = os.path.splitext(os.path.basename(self.mat_file_path))[0]
        if output_dir is None:
            output_dir = os.path.dirname(self.mat_file_path)
        os.makedirs(output_dir, exist_ok=True)
        for fig, covariate_name in zip(self.figures, self.covariate_names):
            if covariate_name:
                safe_cov = str(covariate_name).replace(' ', '_').replace('/', '_')
                file_name = f"{base_name}_{safe_cov}.svg"
            else:
                file_name = f"{base_name}.svg"
            output_path = os.path.join(output_dir, file_name)
            fig.savefig(output_path, format='svg')
            print(f"Plot saved to: {output_path}")

    def show_all(self):
        for fig in self.figures:
            fig.show()



# -----------------------------------------------------------------------------
def run_peb_plot(
    mat_file="C:\\Users\\aman0087\\Documents\\Github\\dcm_psilocybin\\massive_output_local\\adam_m6\\PEB_change_-ses-01-ses-02_-task-rest_cov-_noFD.mat",
    output_dir="C:/Users/aman0087/Documents/Github/dcm_psilocybin/plots",
    show=True,
    save=True
):
    import os
    params = PEBDataLoader.get_peb_plot_parameters()
    # Batch run if a directory is provided
    if os.path.isdir(mat_file):
        mat_files = [os.path.join(mat_file, f) for f in os.listdir(mat_file) if f.lower().endswith('.mat')]
        if not mat_files:
            raise FileNotFoundError("No .mat files found in the provided directory.")
        for mat_path in mat_files:
            print(f"Processing file: {mat_path}")
            loader = PEBDataLoader(mat_path, params)
            peb_data = loader.get_data()
            plotter = PEBPlotter(peb_data, mat_path, params)
            plotter.plot_heatmaps()
            if save:
                plotter.save_all_svgs(output_dir=output_dir)
            if show:
                plotter.show_all()
    else:
        loader = PEBDataLoader(mat_file, params)
        peb_data = loader.get_data()
        plotter = PEBPlotter(peb_data, mat_file, params)
        plotter.plot_heatmaps()
        if save:
            plotter.save_all_svgs(output_dir=output_dir)
        if show:
            plotter.show_all()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Plot PEB results from a MATLAB .mat file.")
    #parser.add_argument("--mat_file", type=str, default="C:\\Users\\aman0087\\Documents\\Github\\dcm_psilocybin\\massive_output_local\\adam_m6\\PEB_change_-ses-01-ses-02_-task-rest_cov-_noFD.mat", help="Path to the PEB .mat file or directory")
    parser.add_argument("--mat_file", type=str, default="C:\\Users\\aman0087\\Documents\\Github\\dcm_psilocybin\\massive_output_local\\adam_m6\\PEB_behav_associations_-ses-02_-task-rest_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat", help="Path to the PEB .mat file or directory")
    parser.add_argument("--output_dir", type=str, default="C:\\Users\\aman0087\\Documents\\Github\\dcm_psilocybin\\plots", help="Directory to save SVG plots (default: alongside .mat file)")
    parser.add_argument("--no-show", action="store_true", help="Do not display plots interactively")
    parser.add_argument("--no-save", action="store_true", help="Do not save SVG plots")
    args, unknown = parser.parse_known_args()


    run_peb_plot(
        mat_file=args.mat_file,
        output_dir=args.output_dir,
        show=not args.no_show,
        save=not args.no_save
    )
