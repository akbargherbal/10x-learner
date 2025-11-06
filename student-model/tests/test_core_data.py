"""
test_core_data.py - Tests for Phase 1.2 Core Data Operations

Tests cover:
- Model initialization
- Loading with various error conditions
- Saving with atomic writes
- Backup/restore functionality
- Concept finding (case-insensitive)
"""

import json
import pytest
from pathlib import Path
from datetime import datetime

# Import functions to test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from student import (
    get_default_model,
    validate_model,
    load_model,
    save_model,
    initialize_model,
    find_concept,
    DATA_FILE
)

# The temp_data_file fixture is now in conftest.py and will be automatically discovered.

class TestDefaultModel:
    """Test default model structure."""
    
    def test_default_model_structure(self):
        """Default model has all required keys."""
        model = get_default_model()
        
        assert "schema_version" in model
        assert "metadata" in model
        assert "concepts" in model
        assert "sessions" in model
    
    def test_default_model_metadata(self):
        """Default model metadata contains required fields."""
        model = get_default_model()
        
        assert "created" in model["metadata"]
        assert "last_updated" in model["metadata"]
        assert "student_profile" in model["metadata"]
    
    def test_default_model_timestamps(self):
        """Timestamps are valid ISO format."""
        model = get_default_model()
        
        # Should not raise exception
        datetime.fromisoformat(model["metadata"]["created"])
        datetime.fromisoformat(model["metadata"]["last_updated"])

class TestValidation:
    """Test model validation."""
    
    def test_validate_valid_model(self):
        """Valid model passes validation."""
        model = get_default_model()
        assert validate_model(model) is True
    
    def test_validate_missing_concepts(self):
        """Model without concepts fails validation."""
        model = get_default_model()
        del model["concepts"]
        assert validate_model(model) is False
    
    def test_validate_missing_metadata(self):
        """Model without metadata fails validation."""
        model = get_default_model()
        del model["metadata"]
        assert validate_model(model) is False
    
    def test_validate_missing_created(self):
        """Model without created timestamp fails."""
        model = get_default_model()
        del model["metadata"]["created"]
        assert validate_model(model) is False

class TestSaveLoad:
    """Test save and load operations."""
    
    def test_save_and_load_roundtrip(self, temp_data_file):
        """Saved model can be loaded back."""
        model = get_default_model()
        model["metadata"]["student_profile"] = "Test Student"
        
        # Save
        assert save_model(model) is True
        assert temp_data_file.exists()
        
        # Load
        loaded = load_model()
        assert loaded["metadata"]["student_profile"] == "Test Student"
    
    def test_save_creates_backup(self, temp_data_file):
        """Saving creates backup of existing file."""
        # Create initial model
        model1 = get_default_model()
        model1["metadata"]["student_profile"] = "Version 1"
        save_model(model1)
        
        # Save new version
        model2 = get_default_model()
        model2["metadata"]["student_profile"] = "Version 2"
        save_model(model2)
        
        # Check backup exists
        backup = temp_data_file.with_suffix('.json.backup')
        assert backup.exists()
        
        # Backup should have version 1
        with open(backup, 'r') as f:
            backup_data = json.load(f)
        assert backup_data["metadata"]["student_profile"] == "Version 1"
    
    def test_save_updates_timestamp(self, temp_data_file):
        """Saving updates last_updated timestamp."""
        model = get_default_model()
        original_time = model["metadata"]["last_updated"]
        
        # Small delay to ensure timestamp changes
        import time
        time.sleep(0.01)
        
        save_model(model)
        loaded = load_model()
        
        assert loaded["metadata"]["last_updated"] != original_time
    
    def test_save_refuses_invalid_model(self, temp_data_file, capsys):
        """Save refuses to write invalid model."""
        model = get_default_model()
        del model["metadata"]  # Make invalid
        
        result = save_model(model)
        assert result is False
        
        captured = capsys.readouterr()
        assert "invalid" in captured.out.lower()

class TestLoadErrors:
    """Test load error handling."""
    
    def test_load_missing_file(self, temp_data_file, capsys):
        """Loading missing file returns default model."""
        model = load_model()
        assert validate_model(model) is True
        
        captured = capsys.readouterr()
        assert "No model found" in captured.out
    
    def test_load_corrupt_json(self, temp_data_file, capsys):
        """Loading corrupt JSON falls back to default."""
        # Write corrupt JSON
        with open(temp_data_file, 'w') as f:
            f.write("{ this is not valid json }")
        
        model = load_model()
        assert validate_model(model) is True
        
        captured = capsys.readouterr()
        assert "Corrupt JSON" in captured.out
    
    def test_load_corrupt_json_with_backup(self, temp_data_file, capsys):
        """Loading corrupt JSON restores from backup."""
        # Create good backup
        backup = temp_data_file.with_suffix('.json.backup')
        good_model = get_default_model()
        good_model["metadata"]["student_profile"] = "From Backup"
        with open(backup, 'w') as f:
            json.dump(good_model, f)
        
        # Write corrupt main file
        with open(temp_data_file, 'w') as f:
            f.write("{ corrupt }")
        
        model = load_model()
        assert model["metadata"]["student_profile"] == "From Backup"
        
        captured = capsys.readouterr()
        assert "Restored from backup" in captured.out
    
    def test_load_invalid_structure(self, temp_data_file, capsys):
        """Loading invalid structure returns default."""
        # Write valid JSON but invalid structure
        with open(temp_data_file, 'w') as f:
            json.dump({"wrong": "structure"}, f)
        
        model = load_model()
        assert validate_model(model) is True
        
        captured = capsys.readouterr()
        assert "invalid structure" in captured.out.lower()

class TestInitialize:
    """Test model initialization."""
    
    def test_initialize_creates_file(self, temp_data_file):
        """Initialize creates new model file."""
        model = initialize_model("Test Profile")
        
        assert temp_data_file.exists()
        assert model["metadata"]["student_profile"] == "Test Profile"
    
    def test_initialize_default_profile(self, temp_data_file):
        """Initialize with no profile creates empty profile."""
        model = initialize_model()
        assert model["metadata"]["student_profile"] == ""

class TestFindConcept:
    """Test concept finding."""
    
    def test_find_exact_match(self):
        """Find concept with exact name match."""
        model = get_default_model()
        model["concepts"]["React Hooks"] = {}
        
        result = find_concept(model, "React Hooks")
        assert result == "React Hooks"
    
    def test_find_case_insensitive(self):
        """Find concept ignoring case."""
        model = get_default_model()
        model["concepts"]["React Hooks"] = {}
        
        result = find_concept(model, "react hooks")
        assert result == "React Hooks"
        
        result = find_concept(model, "REACT HOOKS")
        assert result == "React Hooks"
    
    def test_find_not_found(self):
        """Return None when concept doesn't exist."""
        model = get_default_model()
        
        result = find_concept(model, "Nonexistent Concept")
        assert result is None
    
    def test_find_multiple_concepts(self):
        """Find correct concept among multiple."""
        model = get_default_model()
        model["concepts"]["React Hooks"] = {}
        model["concepts"]["JavaScript Closures"] = {}
        model["concepts"]["Python Decorators"] = {}
        
        result = find_concept(model, "javascript closures")
        assert result == "JavaScript Closures"

class TestAtomicWrites:
    """Test atomic write behavior."""
    
    def test_atomic_write_uses_temp_file(self, temp_data_file):
        """Save uses temp file for atomic operation."""
        model = get_default_model()
        save_model(model)
        
        # Temp file should not exist after save
        temp = temp_data_file.with_suffix('.json.tmp')
        assert not temp.exists()
    
    def test_backup_preserved_on_save_failure(self, temp_data_file):
        """Backup is not corrupted if save fails."""
        # Create good initial state
        model1 = get_default_model()
        model1["metadata"]["student_profile"] = "Good Backup"
        save_model(model1)
        
        # Try to save invalid model
        model2 = get_default_model()
        del model2["metadata"]
        save_model(model2)  # Should fail
        
        # Backup should still have good data
        backup = temp_data_file.with_suffix('.json.backup')
        with open(backup, 'r') as f:
            backup_data = json.load(f)
        assert backup_data["metadata"]["student_profile"] == "Good Backup"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])