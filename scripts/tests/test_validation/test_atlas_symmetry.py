"""
Tests for AAL atlas coordinate symmetry.

Verifies that left/right hemisphere region pairs have symmetric coordinates
(same Y and Z, opposite X sign) within an acceptable tolerance.
"""

import pytest
import warnings

# Suppress nilearn warnings during tests
warnings.filterwarnings('ignore')


# Define hemisphere pairs to check
SYMMETRY_PAIRS = [
    ('Frontal_Mid_L', 'Frontal_Mid_R'),
    ('Hippocampus_L', 'Hippocampus_R'),
    ('Occipital_Sup_L', 'Occipital_Sup_R'),
    ('Temporal_Mid_L', 'Temporal_Mid_R'),
    ('Thalamus_L', 'Thalamus_R'),
]


@pytest.fixture(scope="module")
def aal_coords():
    """Load AAL atlas and compute coordinates (cached per module)."""
    from nilearn.datasets import fetch_atlas_aal
    from nilearn.plotting import find_parcellation_cut_coords

    aal = fetch_atlas_aal()
    coords = find_parcellation_cut_coords(aal.maps)
    return aal.labels, coords


class TestHemisphereSymmetry:
    """Test that L/R region pairs have symmetric coordinates."""

    @pytest.mark.parametrize("left_name,right_name", SYMMETRY_PAIRS)
    def test_hemisphere_symmetry(self, left_name, right_name, aal_coords):
        """Verify L/R pairs have same Y/Z coordinates (tolerance=10mm)."""
        labels, coords = aal_coords

        left_idx = labels.index(left_name)
        right_idx = labels.index(right_name)
        left_coord = coords[left_idx]
        right_coord = coords[right_idx]

        y_diff = abs(left_coord[1] - right_coord[1])
        z_diff = abs(left_coord[2] - right_coord[2])

        assert y_diff < 10, (
            f"Y asymmetry in {left_name}/{right_name}: "
            f"L={left_coord[1]:.1f}, R={right_coord[1]:.1f}, diff={y_diff:.1f}"
        )
        assert z_diff < 10, (
            f"Z asymmetry in {left_name}/{right_name}: "
            f"L={left_coord[2]:.1f}, R={right_coord[2]:.1f}, diff={z_diff:.1f}"
        )

    @pytest.mark.parametrize("left_name,right_name", SYMMETRY_PAIRS)
    def test_x_sign_opposite(self, left_name, right_name, aal_coords):
        """Verify L/R pairs have opposite X sign (L negative, R positive)."""
        labels, coords = aal_coords

        left_idx = labels.index(left_name)
        right_idx = labels.index(right_name)
        left_x = coords[left_idx][0]
        right_x = coords[right_idx][0]

        # Left hemisphere should have negative X, right should have positive
        # (or at minimum, opposite signs)
        assert left_x * right_x < 0 or (left_x < 0 and right_x > 0), (
            f"X coordinates should have opposite signs for {left_name}/{right_name}: "
            f"L={left_x:.1f}, R={right_x:.1f}"
        )
