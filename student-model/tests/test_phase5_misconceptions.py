#!/usr/bin/env python3
"""
test_phase5_misconceptions.py - Tests for Phase 5.2 Misconception Tracking

Tests cover:
- Adding misconceptions to existing/non-existent concepts
- Duplicate prevention
- Resolving misconceptions by index
- Listing with various filters
- Data persistence
- Edge cases (invalid indices, empty states, etc.)
"""

import pytest
import json
from pathlib import Path
from datetime import datetime
import student


class TestMisconceptionAdd:
    """Test adding misconceptions."""

    def test_add_misconception_to_existing_concept(self, temp_data_file, monkeypatch, capsys):
        """Adding misconception to tracked concept should succeed."""
        monkeypatch.setattr('student.DATA_FILE', temp_data_file)

        # Setup: Create a concept first
        model = student.initialize_model()
        model["concepts"]["Test Concept"] = {
            "mastery": 50,
            "confidence": "medium",
            "first_encountered": datetime.now().isoformat(),
            "last_reviewed": datetime.now().isoformat(),
            "struggles": [],
            "breakthroughs": [],
            "related_concepts": []
        }
        student.save_model(model)

        # Add misconception
        class Args:
            concept_name = "Test Concept"
            belief = "Incorrect belief"
            correction = "Correct understanding"

        student.cmd_misconception_add(Args())

        # Verify
        model = student.load_model()
        assert "misconceptions" in model
        assert len(model["misconceptions"]) == 1
        assert model["misconceptions"][0]["concept"] == "Test Concept"
        assert model["misconceptions"][0]["belief"] == "Incorrect belief"
        assert model["misconceptions"][0]["correction"] == "Correct understanding"
        assert model["misconceptions"][0]["resolved"] is False
        assert model["misconceptions"][0]["date_resolved"] is None

        captured = capsys.readouterr()
        assert "✅" in captured.out
        assert "Test Concept" in captured.out

    def test_add_misconception_to_nonexistent_concept(self, temp_data_file, monkeypatch, capsys):
        """Adding misconception to non-existent concept should fail gracefully."""
        monkeypatch.setattr('student.DATA_FILE', temp_data_file)
        student.initialize_model()

        class Args:
            concept_name = "Nonexistent"
            belief = "Some belief"
            correction = "Some correction"

        student.cmd_misconception_add(Args())

        # Verify error message
        captured = capsys.readouterr()
        assert "❌" in captured.out
        assert "not found" in captured.out.lower()
        assert "Nonexistent" in captured.out

        # Verify no misconception was added
        model = student.load_model()
        assert len(model.get("misconceptions", [])) == 0

    def test_prevent_duplicate_misconceptions(self, temp_data_file, monkeypatch, capsys):
        """Adding duplicate misconception should be detected and prevented."""
        monkeypatch.setattr('student.DATA_FILE', temp_data_file)

        # Setup: Create concept and add misconception
        model = student.initialize_model()
        model["concepts"]["Test Concept"] = {
            "mastery": 50,
            "confidence": "medium",
            "first_encountered": datetime.now().isoformat(),
            "last_reviewed": datetime.now().isoformat(),
            "struggles": [],
            "breakthroughs": [],
            "related_concepts": []
        }
        student.save_model(model)

        class Args:
            concept_name = "Test Concept"
            belief = "Same belief"
            correction = "First correction"

        # Add first time
        student.cmd_misconception_add(Args())

        # Try to add duplicate (same concept + same belief)
        Args.correction = "Different correction"  # Even with different correction
        capsys.readouterr()  # Clear previous output
        student.cmd_misconception_add(Args())

        # Verify duplicate message
        captured = capsys.readouterr()
        assert "ℹ️" in captured.out
        assert "already logged" in captured.out.lower()

        # Verify only one misconception exists
        model = student.load_model()
        assert len(model["misconceptions"]) == 1

    def test_misconception_data_persistence(self, temp_data_file, monkeypatch):
        """Misconceptions should persist across save/load cycles."""
        monkeypatch.setattr('student.DATA_FILE', temp_data_file)

        # Setup and add misconception
        model = student.initialize_model()
        model["concepts"]["Test Concept"] = {
            "mastery": 50,
            "confidence": "medium",
            "first_encountered": datetime.now().isoformat(),
            "last_reviewed": datetime.now().isoformat(),
            "struggles": [],
            "breakthroughs": [],
            "related_concepts": []
        }
        student.save_model(model)

        class Args:
            concept_name = "Test Concept"
            belief = "Test belief"
            correction = "Test correction"

        student.cmd_misconception_add(Args())

        # Load fresh from disk
        model_reloaded = student.load_model()

        # Verify persistence
        assert len(model_reloaded["misconceptions"]) == 1
        assert model_reloaded["misconceptions"][0]["belief"] == "Test belief"
        assert model_reloaded["misconceptions"][0]["correction"] == "Test correction"


class TestMisconceptionResolve:
    """Test resolving misconceptions."""

    def test_resolve_misconception_by_index(self, temp_data_file, monkeypatch, capsys):
        """Resolving misconception by index should mark it as resolved."""
        monkeypatch.setattr('student.DATA_FILE', temp_data_file)

        # Setup: Create concept and misconception
        model = student.initialize_model()
        model["concepts"]["Test Concept"] = {
            "mastery": 50,
            "confidence": "medium",
            "first_encountered": datetime.now().isoformat(),
            "last_reviewed": datetime.now().isoformat(),
            "struggles": [],
            "breakthroughs": [],
            "related_concepts": []
        }
        model["misconceptions"] = [{
            "concept": "Test Concept",
            "belief": "Test belief",
            "correction": "Test correction",
            "date_identified": datetime.now().isoformat(),
            "resolved": False,
            "date_resolved": None
        }]
        student.save_model(model)

        # Resolve
        class Args:
            concept_name = "Test Concept"
            index = 0

        student.cmd_misconception_resolve(Args())

        # Verify
        model = student.load_model()
        assert model["misconceptions"][0]["resolved"] is True
        assert model["misconceptions"][0]["date_resolved"] is not None

        captured = capsys.readouterr()
        assert "✅" in captured.out
        assert "Resolved" in captured.out

    def test_resolve_invalid_index(self, temp_data_file, monkeypatch, capsys):
        """Resolving with invalid index should show error."""
        monkeypatch.setattr('student.DATA_FILE', temp_data_file)

        # Setup
        model = student.initialize_model()
        model["concepts"]["Test Concept"] = {
            "mastery": 50,
            "confidence": "medium",
            "first_encountered": datetime.now().isoformat(),
            "last_reviewed": datetime.now().isoformat(),
            "struggles": [],
            "breakthroughs": [],
            "related_concepts": []
        }
        model["misconceptions"] = [{
            "concept": "Test Concept",
            "belief": "Test belief",
            "correction": "Test correction",
            "date_identified": datetime.now().isoformat(),
            "resolved": False,
            "date_resolved": None
        }]
        student.save_model(model)

        # Try invalid index
        class Args:
            concept_name = "Test Concept"
            index = 5

        student.cmd_misconception_resolve(Args())

        # Verify error
        captured = capsys.readouterr()
        assert "❌" in captured.out
        assert "out of range" in captured.out.lower()

        # Verify misconception unchanged
        model = student.load_model()
        assert model["misconceptions"][0]["resolved"] is False

    def test_resolve_nonexistent_concept(self, temp_data_file, monkeypatch, capsys):
        """Resolving for non-existent concept should show error."""
        monkeypatch.setattr('student.DATA_FILE', temp_data_file)
        student.initialize_model()

        class Args:
            concept_name = "Nonexistent"
            index = 0

        student.cmd_misconception_resolve(Args())

        captured = capsys.readouterr()
        assert "❌" in captured.out
        assert "not found" in captured.out.lower()

    def test_resolve_when_no_unresolved_misconceptions(self, temp_data_file, monkeypatch, capsys):
        """Resolving when no unresolved misconceptions exist should show info message."""
        monkeypatch.setattr('student.DATA_FILE', temp_data_file)

        # Setup: Concept exists but no unresolved misconceptions
        model = student.initialize_model()
        model["concepts"]["Test Concept"] = {
            "mastery": 50,
            "confidence": "medium",
            "first_encountered": datetime.now().isoformat(),
            "last_reviewed": datetime.now().isoformat(),
            "struggles": [],
            "breakthroughs": [],
            "related_concepts": []
        }
        student.save_model(model)

        class Args:
            concept_name = "Test Concept"
            index = 0

        student.cmd_misconception_resolve(Args())

        captured = capsys.readouterr()
        assert "ℹ️" in captured.out
        assert "No unresolved" in captured.out


class TestMisconceptionList:
    """Test listing misconceptions with various filters."""

    def test_list_empty_misconceptions(self, temp_data_file, monkeypatch, capsys):
        """Listing when no misconceptions exist should show helpful message."""
        monkeypatch.setattr('student.DATA_FILE', temp_data_file)
        student.initialize_model()

        class Args:
            concept_name = None
            resolved_only = False
            unresolved_only = False

        student.cmd_misconception_list(Args())

        captured = capsys.readouterr()
        assert "No misconceptions tracked yet" in captured.out

    def test_list_all_misconceptions(self, temp_data_file, monkeypatch, capsys):
        """Listing all misconceptions should show grouped by concept."""
        monkeypatch.setattr('student.DATA_FILE', temp_data_file)

        # Setup: Multiple misconceptions
        model = student.initialize_model()
        model["concepts"]["Concept A"] = {
            "mastery": 50, "confidence": "medium",
            "first_encountered": datetime.now().isoformat(),
            "last_reviewed": datetime.now().isoformat(),
            "struggles": [], "breakthroughs": [], "related_concepts": []
        }
        model["concepts"]["Concept B"] = {
            "mastery": 60, "confidence": "high",
            "first_encountered": datetime.now().isoformat(),
            "last_reviewed": datetime.now().isoformat(),
            "struggles": [], "breakthroughs": [], "related_concepts": []
        }
        model["misconceptions"] = [
            {
                "concept": "Concept A",
                "belief": "Belief A1",
                "correction": "Correction A1",
                "date_identified": datetime.now().isoformat(),
                "resolved": False,
                "date_resolved": None
            },
            {
                "concept": "Concept A",
                "belief": "Belief A2",
                "correction": "Correction A2",
                "date_identified": datetime.now().isoformat(),
                "resolved": True,
                "date_resolved": datetime.now().isoformat()
            },
            {
                "concept": "Concept B",
                "belief": "Belief B1",
                "correction": "Correction B1",
                "date_identified": datetime.now().isoformat(),
                "resolved": False,
                "date_resolved": None
            }
        ]
        student.save_model(model)

        class Args:
            concept_name = None
            resolved_only = False
            unresolved_only = False

        student.cmd_misconception_list(Args())

        captured = capsys.readouterr()
        assert "3 total" in captured.out
        assert "Concept A" in captured.out
        assert "Concept B" in captured.out
        assert "Belief A1" in captured.out
        assert "Belief B1" in captured.out

    def test_list_filtered_by_concept(self, temp_data_file, monkeypatch, capsys):
        """Filtering by concept should show only that concept's misconceptions."""
        monkeypatch.setattr('student.DATA_FILE', temp_data_file)

        # Setup
        model = student.initialize_model()
        model["concepts"]["Concept A"] = {
            "mastery": 50, "confidence": "medium",
            "first_encountered": datetime.now().isoformat(),
            "last_reviewed": datetime.now().isoformat(),
            "struggles": [], "breakthroughs": [], "related_concepts": []
        }
        model["concepts"]["Concept B"] = {
            "mastery": 60, "confidence": "high",
            "first_encountered": datetime.now().isoformat(),
            "last_reviewed": datetime.now().isoformat(),
            "struggles": [], "breakthroughs": [], "related_concepts": []
        }
        model["misconceptions"] = [
            {
                "concept": "Concept A",
                "belief": "Belief A",
                "correction": "Correction A",
                "date_identified": datetime.now().isoformat(),
                "resolved": False,
                "date_resolved": None
            },
            {
                "concept": "Concept B",
                "belief": "Belief B",
                "correction": "Correction B",
                "date_identified": datetime.now().isoformat(),
                "resolved": False,
                "date_resolved": None
            }
        ]
        student.save_model(model)

        class Args:
            concept_name = "Concept A"
            resolved_only = False
            unresolved_only = False

        student.cmd_misconception_list(Args())

        captured = capsys.readouterr()
        assert "Concept A" in captured.out
        assert "Belief A" in captured.out
        assert "Concept B" not in captured.out
        assert "Belief B" not in captured.out

    def test_list_unresolved_only(self, temp_data_file, monkeypatch, capsys):
        """Filtering by unresolved should show only active misconceptions."""
        monkeypatch.setattr('student.DATA_FILE', temp_data_file)

        # Setup
        model = student.initialize_model()
        model["concepts"]["Test Concept"] = {
            "mastery": 50, "confidence": "medium",
            "first_encountered": datetime.now().isoformat(),
            "last_reviewed": datetime.now().isoformat(),
            "struggles": [], "breakthroughs": [], "related_concepts": []
        }
        model["misconceptions"] = [
            {
                "concept": "Test Concept",
                "belief": "Unresolved belief",
                "correction": "Correction",
                "date_identified": datetime.now().isoformat(),
                "resolved": False,
                "date_resolved": None
            },
            {
                "concept": "Test Concept",
                "belief": "Resolved belief",
                "correction": "Correction",
                "date_identified": datetime.now().isoformat(),
                "resolved": True,
                "date_resolved": datetime.now().isoformat()
            }
        ]
        student.save_model(model)

        class Args:
            concept_name = None
            resolved_only = False
            unresolved_only = True

        student.cmd_misconception_list(Args())

        captured = capsys.readouterr()
        assert "Unresolved belief" in captured.out
        assert "Resolved belief" not in captured.out
        assert "⚠️  Active" in captured.out

    def test_list_resolved_only(self, temp_data_file, monkeypatch, capsys):
        """Filtering by resolved should show only resolved misconceptions."""
        monkeypatch.setattr('student.DATA_FILE', temp_data_file)

        # Setup
        model = student.initialize_model()
        model["concepts"]["Test Concept"] = {
            "mastery": 50, "confidence": "medium",
            "first_encountered": datetime.now().isoformat(),
            "last_reviewed": datetime.now().isoformat(),
            "struggles": [], "breakthroughs": [], "related_concepts": []
        }
        model["misconceptions"] = [
            {
                "concept": "Test Concept",
                "belief": "Unresolved belief",
                "correction": "Correction",
                "date_identified": datetime.now().isoformat(),
                "resolved": False,
                "date_resolved": None
            },
            {
                "concept": "Test Concept",
                "belief": "Resolved belief",
                "correction": "Correction",
                "date_identified": datetime.now().isoformat(),
                "resolved": True,
                "date_resolved": datetime.now().isoformat()
            }
        ]
        student.save_model(model)

        class Args:
            concept_name = None
            resolved_only = True
            unresolved_only = False

        student.cmd_misconception_list(Args())

        captured = capsys.readouterr()
        assert "Resolved belief" in captured.out
        assert "Unresolved belief" not in captured.out
        assert "✅ Resolved" in captured.out

    def test_list_nonexistent_concept(self, temp_data_file, monkeypatch, capsys):
        """Filtering by non-existent concept shows empty result (graceful)."""
        monkeypatch.setattr('student.DATA_FILE', temp_data_file)
        student.initialize_model()

        class Args:
            concept_name = "Nonexistent"
            resolved_only = False
            unresolved_only = False

        student.cmd_misconception_list(Args())

        captured = capsys.readouterr()
        # Should show "None found" message, not an error
        # This is graceful behavior - doesn't error on typos
        assert "None found" in captured.out or "No misconceptions" in captured.out


class TestMisconceptionIndexing:
    """Test that indexing works correctly for resolve operations."""

    def test_index_counts_only_unresolved(self, temp_data_file, monkeypatch, capsys):
        """Indices should only count unresolved misconceptions."""
        monkeypatch.setattr('student.DATA_FILE', temp_data_file)

        # Setup: Mix of resolved and unresolved
        model = student.initialize_model()
        model["concepts"]["Test Concept"] = {
            "mastery": 50, "confidence": "medium",
            "first_encountered": datetime.now().isoformat(),
            "last_reviewed": datetime.now().isoformat(),
            "struggles": [], "breakthroughs": [], "related_concepts": []
        }
        model["misconceptions"] = [
            {
                "concept": "Test Concept",
                "belief": "First (resolved)",
                "correction": "Correction",
                "date_identified": datetime.now().isoformat(),
                "resolved": True,
                "date_resolved": datetime.now().isoformat()
            },
            {
                "concept": "Test Concept",
                "belief": "Second (unresolved)",
                "correction": "Correction",
                "date_identified": datetime.now().isoformat(),
                "resolved": False,
                "date_resolved": None
            },
            {
                "concept": "Test Concept",
                "belief": "Third (unresolved)",
                "correction": "Correction",
                "date_identified": datetime.now().isoformat(),
                "resolved": False,
                "date_resolved": None
            }
        ]
        student.save_model(model)

        # List should show indices [0] and [1] for unresolved
        class ListArgs:
            concept_name = "Test Concept"
            resolved_only = False
            unresolved_only = False

        student.cmd_misconception_list(ListArgs())
        captured = capsys.readouterr()

        # Should see two unresolved with indices 0 and 1
        assert "[0]" in captured.out
        assert "[1]" in captured.out
        assert "Second (unresolved)" in captured.out
        assert "Third (unresolved)" in captured.out

        # Resolved should not have index
        assert "First (resolved)" in captured.out


class TestMisconceptionEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_case_insensitive_concept_matching(self, temp_data_file, monkeypatch, capsys):
        """Concept names should be matched case-insensitively."""
        monkeypatch.setattr('student.DATA_FILE', temp_data_file)

        # Setup with specific case
        model = student.initialize_model()
        model["concepts"]["Test Concept"] = {
            "mastery": 50, "confidence": "medium",
            "first_encountered": datetime.now().isoformat(),
            "last_reviewed": datetime.now().isoformat(),
            "struggles": [], "breakthroughs": [], "related_concepts": []
        }
        student.save_model(model)

        # Add with different case
        class Args:
            concept_name = "test concept"  # lowercase
            belief = "Test belief"
            correction = "Test correction"

        student.cmd_misconception_add(Args())

        # Should succeed (case-insensitive match)
        captured = capsys.readouterr()
        assert "✅" in captured.out

        # Verify it was stored with the correct case from model
        model = student.load_model()
        assert model["misconceptions"][0]["concept"] == "Test Concept"

    def test_empty_belief_or_correction(self, temp_data_file, monkeypatch):
        """Empty strings for belief/correction should still be stored."""
        monkeypatch.setattr('student.DATA_FILE', temp_data_file)

        model = student.initialize_model()
        model["concepts"]["Test Concept"] = {
            "mastery": 50, "confidence": "medium",
            "first_encountered": datetime.now().isoformat(),
            "last_reviewed": datetime.now().isoformat(),
            "struggles": [], "breakthroughs": [], "related_concepts": []
        }
        student.save_model(model)

        class Args:
            concept_name = "Test Concept"
            belief = ""
            correction = ""

        student.cmd_misconception_add(Args())

        model = student.load_model()
        assert len(model["misconceptions"]) == 1
        assert model["misconceptions"][0]["belief"] == ""
        assert model["misconceptions"][0]["correction"] == ""

    def test_unicode_in_misconceptions(self, temp_data_file, monkeypatch):
        """Unicode characters should be handled correctly."""
        monkeypatch.setattr('student.DATA_FILE', temp_data_file)

        model = student.initialize_model()
        model["concepts"]["Test Concept"] = {
            "mastery": 50, "confidence": "medium",
            "first_encountered": datetime.now().isoformat(),
            "last_reviewed": datetime.now().isoformat(),
            "struggles": [], "breakthroughs": [], "related_concepts": []
        }
        student.save_model(model)

        class Args:
            concept_name = "Test Concept"
            belief = "λ函数是匿名的 🚀"
            correction = "Lambda functions can have names via assignment"

        student.cmd_misconception_add(Args())

        # Verify persistence
        model = student.load_model()
        assert model["misconceptions"][0]["belief"] == "λ函数是匿名的 🚀"