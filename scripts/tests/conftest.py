"""Shared fixtures for dcm_psilocybin tests."""

import pytest
from pathlib import Path


@pytest.fixture
def project_root():
    """Return the project root directory."""
    return Path(__file__).parent.parent.parent


@pytest.fixture
def data_dir(project_root):
    """Return the main data directory."""
    return project_root / 'data' / 'peb_outputs'
