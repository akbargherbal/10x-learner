"""
conftest.py - Shared fixtures for the test suite.
"""
import pytest
import tempfile
import shutil
import json
from pathlib import Path
from datetime import datetime


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


@pytest.fixture
def sample_model(temp_data_file):
    """
    Create a sample model with pre-existing concepts for testing.
    Depends on temp_data_file to set up the temporary location.
    """
    model = {
        "schema_version": "1.0",
        "metadata": {
            "created": "2024-01-01T12:00:00",
            "last_updated": "2024-01-15T12:00:00",
            "student_profile": "Test Student"
        },
        "concepts": {
            "React Hooks": {
                "mastery": 60,
                "confidence": "medium",
                "first_encountered": "2024-01-01T12:00:00",
                "last_reviewed": "2024-01-10T12:00:00",
                "struggles": ["understanding useEffect dependencies"],
                "breakthroughs": ["realized hooks are just functions"],
                "related_concepts": []
            },
            "JavaScript Closures": {
                "mastery": 75,
                "confidence": "high",
                "first_encountered": "2023-12-01T12:00:00",
                "last_reviewed": "2024-01-05T12:00:00",
                "struggles": [],
                "breakthroughs": ["understood lexical scope"],
                "related_concepts": []
            }
        },
        "sessions": []
    }
    
    # Write the sample model to the temp file
    with open(temp_data_file, 'w', encoding='utf-8') as f:
        json.dump(model, f, indent=2)
    
    return model