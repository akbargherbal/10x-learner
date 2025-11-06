"""
conftest.py - Shared fixtures for the test suite.
"""

import pytest
import tempfile
import shutil
from pathlib import Path

@pytest.fixture
def temp_data_file(monkeypatch):
    """
    Create a temporary data file for testing and monkeypatch the global DATA_FILE constant.
    This fixture is available to all tests.
    """
    temp_dir = tempfile.mkdtemp()
    temp_file = Path(temp_dir) / "test_student_model.json"
    
    # Monkeypatch the DATA_FILE constant in the student module
    monkeypatch.setattr('student.DATA_FILE', temp_file)
    
    yield temp_file
    
    # Cleanup
    shutil.rmtree(temp_dir)