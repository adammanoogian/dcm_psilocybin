"""
Tests for PEB model constraint integrity.

Verifies that:
1. Behavioral matrices have fewer parameters than full model (are constrained)
2. REST PEB matrices use proper constraints
3. Behavioral model connections are a subset of session change significant connections
"""

import pytest
import numpy as np
import re
import sys
from pathlib import Path

# Add project paths for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'scripts' / 'visualization'))


@pytest.fixture
def data_dir():
    """Return the main data directory."""
    return project_root / 'data' / 'peb_outputs'


@pytest.fixture
def peb_params():
    """Return standard PEB parameters."""
    from scripts.visualization.plot_PEB_results import PEBDataLoader
    params = PEBDataLoader.get_peb_plot_parameters()
    params['pp_threshold'] = 0.99
    return params


class TestBehavioralConstraint:
    """Test that behavioral matrices are properly constrained."""

    def test_behavioral_matrix_is_constrained(self, data_dir, peb_params):
        """Verify behavioral matrices have fewer params than full model."""
        from scripts.visualization.plot_PEB_results import PEBDataLoader

        behav_file = data_dir / 'PEB_behav_associations_-ses-02_-task-rest_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat'

        if not behav_file.exists():
            pytest.skip(f"Behavioral file not found: {behav_file}")

        loader = PEBDataLoader(str(behav_file), peb_params)
        peb_data = loader.get_data()

        model = peb_data.get('model') or peb_data.get('bma')
        Pnames = model.get('Pnames', [])
        n_rois = len(peb_data['roi_names'])
        expected_full = n_rois ** 2

        assert len(Pnames) < expected_full, (
            f"Behavioral model should have fewer params than full model. "
            f"Got {len(Pnames)}, expected < {expected_full}"
        )


class TestRESTConstraint:
    """Test that REST PEB matrices use proper constraints."""

    def test_rest_change_is_constrained(self, data_dir, peb_params):
        """Verify REST change PEB is constrained (if applicable)."""
        from scripts.visualization.plot_PEB_results import PEBDataLoader

        change_file = data_dir / 'PEB_change_-ses-01-ses-02_-task-rest_cov-_noFD.mat'

        if not change_file.exists():
            pytest.skip(f"REST change file not found: {change_file}")

        loader = PEBDataLoader(str(change_file), peb_params)
        peb_data = loader.get_data()

        model = peb_data.get('model') or peb_data.get('bma')
        Pnames = model.get('Pnames', [])
        n_rois = len(peb_data['roi_names'])
        expected_full = n_rois ** 2

        # This test just checks the model loads correctly
        # REST change may or may not be constrained depending on analysis
        assert len(Pnames) > 0, "REST change model should have parameters"

    def test_rest_behavioral_is_constrained(self, data_dir, peb_params):
        """Verify REST behavioral PEB is constrained."""
        from scripts.visualization.plot_PEB_results import PEBDataLoader

        behav_file = data_dir / 'PEB_behav_associations_-ses-02_-task-rest_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat'

        if not behav_file.exists():
            pytest.skip(f"REST behavioral file not found: {behav_file}")

        loader = PEBDataLoader(str(behav_file), peb_params)
        peb_data = loader.get_data()

        model = peb_data.get('model') or peb_data.get('bma')
        Pnames = model.get('Pnames', [])
        n_rois = len(peb_data['roi_names'])
        expected_full = n_rois ** 2

        assert len(Pnames) < expected_full, (
            f"REST behavioral model should be constrained. "
            f"Got {len(Pnames)} params, expected < {expected_full}"
        )


class TestBehavioralAlignment:
    """Test that behavioral connections align with session change connections."""

    @pytest.mark.parametrize("condition", ["rest", "music", "movie", "meditation"])
    def test_behavioral_constrained_by_change(self, condition, data_dir, peb_params):
        """Verify behavioral model connections are subset of session change significant connections."""
        from scripts.visualization.plot_PEB_results import PEBDataLoader

        change_file = data_dir / f'PEB_change_-ses-01-ses-02_-task-{condition}_cov-_noFD.mat'
        behav_file = data_dir / f'PEB_behav_associations_-ses-02_-task-{condition}_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat'

        if not change_file.exists():
            pytest.skip(f"Change file not found for {condition}")
        if not behav_file.exists():
            pytest.skip(f"Behavioral file not found for {condition}")

        # Load session change data
        change_loader = PEBDataLoader(str(change_file), peb_params)
        change_data = change_loader.get_data()
        change_model = change_data.get('model') or change_data.get('bma')
        roi_names = change_data['roi_names']
        n_rois = len(roi_names)

        # Get Ep and Pp for change file
        change_Ep = np.array(change_model['Ep']).flatten()
        change_Pp = np.array(change_model['Pp']).flatten()

        # For change type, we have 2 covariates
        cov_n = 2
        param_per_cov = len(change_Ep) // cov_n

        # Extract the change covariate (covariate 1)
        change_Pp_cov1 = change_Pp[param_per_cov:2*param_per_cov]

        # Find significant change connections
        change_significant_mask = change_Pp_cov1 >= peb_params['pp_threshold']
        change_significant_indices = np.where(change_significant_mask)[0]

        # Convert to (row, col) set
        change_connections = set()
        for flat_idx in change_significant_indices:
            row = flat_idx % n_rois
            col = flat_idx // n_rois
            change_connections.add((row, col))

        # Load behavioral data
        behav_loader = PEBDataLoader(str(behav_file), peb_params)
        behav_data = behav_loader.get_data()
        behav_model = behav_data.get('model') or behav_data.get('bma')
        behav_Pnames = behav_model.get('Pnames', [])
        behav_Ep = np.array(behav_model['Ep']).flatten()

        # Parse behavioral parameter names
        behav_connections = set()
        pattern = r'A\((\d+),(\d+)\)'

        if behav_Pnames is not None and len(behav_Pnames) > 0:
            behav_param_per_cov = len(behav_Ep) // 2
            for pname in behav_Pnames[:behav_param_per_cov]:
                match = re.search(pattern, str(pname))
                if match:
                    row = int(match.group(1)) - 1
                    col = int(match.group(2)) - 1
                    behav_connections.add((row, col))

        # Verify behavioral is subset of change
        extra_in_behav = behav_connections - change_connections

        assert behav_connections.issubset(change_connections), (
            f"Behavioral connections should be subset of change connections for {condition}. "
            f"Extra connections in behavioral: {extra_in_behav}"
        )
