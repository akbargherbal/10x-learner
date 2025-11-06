"""
test_phase2_read_ops.py - Tests for Phase 2 Read Operations

Add these test classes to tests/test_core_data.py or create a new test file
"""

import json
import pytest
from pathlib import Path

# Add sys.path modification to ensure student module can be imported
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import from student.py
from student import (
    get_default_model,
    save_model,
    cmd_list,
    cmd_show,
    cmd_related,
    find_concept
)


class TestListCommand:
    """Test 'list' command."""
    
    def test_list_empty_model(self, temp_data_file, capsys):
        """List shows helpful message when no concepts."""
        model = get_default_model()
        save_model(model)
        
        # Simulate command
        from argparse import Namespace
        args = Namespace()
        cmd_list(args)
        
        captured = capsys.readouterr()
        assert "No concepts tracked yet" in captured.out
        assert "Add your first concept" in captured.out
    
    def test_list_shows_concepts(self, temp_data_file, capsys):
        """List displays all concepts with summary info."""
        model = get_default_model()
        model["concepts"]["React Hooks"] = {
            "mastery": 70,
            "confidence": "medium",
            "last_reviewed": "2025-11-06T10:00:00"
        }
        model["concepts"]["JavaScript Closures"] = {
            "mastery": 45,
            "confidence": "low",
            "last_reviewed": "2025-11-05T10:00:00"
        }
        save_model(model)
        
        from argparse import Namespace
        args = Namespace()
        cmd_list(args)
        
        captured = capsys.readouterr()
        assert "React Hooks" in captured.out
        assert "JavaScript Closures" in captured.out
        assert "70%" in captured.out
        assert "45%" in captured.out
    
    def test_list_sorts_by_mastery(self, temp_data_file, capsys):
        """List sorts concepts by mastery (highest first)."""
        model = get_default_model()
        model["concepts"]["Low"] = {"mastery": 30, "confidence": "low"}
        model["concepts"]["High"] = {"mastery": 90, "confidence": "high"}
        model["concepts"]["Medium"] = {"mastery": 60, "confidence": "medium"}
        save_model(model)
        
        from argparse import Namespace
        args = Namespace()
        cmd_list(args)
        
        captured = capsys.readouterr()
        output_lines = captured.out.split('\n')
        
        # Find concept lines (skip headers)
        concept_lines = [l for l in output_lines if 'High' in l or 'Medium' in l or 'Low' in l]
        
        # High should appear before Medium before Low
        high_idx = next(i for i, l in enumerate(concept_lines) if 'High' in l)
        medium_idx = next(i for i, l in enumerate(concept_lines) if 'Medium' in l)
        low_idx = next(i for i, l in enumerate(concept_lines) if 'Low' in l)
        
        assert high_idx < medium_idx < low_idx


class TestShowCommand:
    """Test 'show' command."""
    
    def test_show_not_found(self, temp_data_file, capsys):
        """Show handles missing concept gracefully."""
        model = get_default_model()
        save_model(model)
        
        from argparse import Namespace
        args = Namespace(concept_name="Nonexistent")
        cmd_show(args)
        
        captured = capsys.readouterr()
        assert "not found" in captured.out.lower()
        assert "Nonexistent" in captured.out
    
    def test_show_displays_concept(self, temp_data_file, capsys):
        """Show displays full concept details."""
        model = get_default_model()
        model["concepts"]["React Hooks"] = {
            "mastery": 70,
            "confidence": "medium",
            "first_encountered": "2025-10-01T10:00:00",
            "last_reviewed": "2025-11-06T10:00:00",
            "struggles": ["dependency arrays"],
            "breakthroughs": ["understood cleanup"],
            "related_concepts": ["JavaScript Closures"]
        }
        save_model(model)
        
        from argparse import Namespace
        args = Namespace(concept_name="React Hooks")
        cmd_show(args)
        
        captured = capsys.readouterr()
        assert "React Hooks" in captured.out
        assert "70%" in captured.out
        assert "medium" in captured.out
        assert "dependency arrays" in captured.out
        assert "understood cleanup" in captured.out
        assert "JavaScript Closures" in captured.out
    
    def test_show_case_insensitive(self, temp_data_file, capsys):
        """Show finds concepts case-insensitively."""
        model = get_default_model()
        model["concepts"]["React Hooks"] = {
            "mastery": 70,
            "confidence": "medium"
        }
        save_model(model)
        
        from argparse import Namespace
        args = Namespace(concept_name="react hooks")
        cmd_show(args)
        
        captured = capsys.readouterr()
        assert "React Hooks" in captured.out
        assert "70%" in captured.out


class TestRelatedCommand:
    """Test 'related' command."""
    
    def test_related_not_found(self, temp_data_file, capsys):
        """Related handles missing concept."""
        model = get_default_model()
        save_model(model)
        
        from argparse import Namespace
        args = Namespace(concept_name="Nonexistent")
        cmd_related(args)
        
        captured = capsys.readouterr()
        assert "not found" in captured.out.lower()
    
    def test_related_no_relations(self, temp_data_file, capsys):
        """Related shows message when no relations."""
        model = get_default_model()
        model["concepts"]["React Hooks"] = {
            "mastery": 70,
            "confidence": "medium",
            "related_concepts": []
        }
        save_model(model)
        
        from argparse import Namespace
        args = Namespace(concept_name="React Hooks")
        cmd_related(args)
        
        captured = capsys.readouterr()
        assert "No related concepts" in captured.out
    
    def test_related_displays_relations(self, temp_data_file, capsys):
        """Related displays related concepts with details."""
        model = get_default_model()
        model["concepts"]["React Hooks"] = {
            "mastery": 70,
            "confidence": "medium",
            "related_concepts": ["JavaScript Closures", "React Core"]
        }
        model["concepts"]["JavaScript Closures"] = {
            "mastery": 45,
            "confidence": "low",
            "last_reviewed": "2025-11-05T10:00:00"
        }
        model["concepts"]["React Core"] = {
            "mastery": 80,
            "confidence": "high",
            "last_reviewed": "2025-11-06T10:00:00"
        }
        save_model(model)
        
        from argparse import Namespace
        args = Namespace(concept_name="React Hooks")
        cmd_related(args)
        
        captured = capsys.readouterr()
        assert "JavaScript Closures" in captured.out
        assert "React Core" in captured.out
        assert "45%" in captured.out
        assert "80%" in captured.out
        assert "LOW" in captured.out  # Flag for low mastery


if __name__ == '__main__':
    pytest.main([__file__, '-v'])