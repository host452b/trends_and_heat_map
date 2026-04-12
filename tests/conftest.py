"""Shared test fixtures."""
import os
import pytest

@pytest.fixture
def project_root():
    """Return the project root directory."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@pytest.fixture
def weights_path(project_root):
    return os.path.join(project_root, "schema", "weights.yaml")

@pytest.fixture
def schema_path(project_root):
    return os.path.join(project_root, "schema", "SCHEMA.yaml")
