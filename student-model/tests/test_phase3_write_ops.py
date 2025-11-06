"""
Test Phase 3 Write Operations
Tests for add, update, struggle, breakthrough, link, unlink commands
"""

import pytest
import json
from pathlib import Path
from datetime import datetime


class TestAddCommand:
    """Test the add command for creating new concepts."""
    
    def test_add_new_concept(self, temp_data_file, capsys):
        """Add command creates new concept with all fields."""
        from student import cmd_add, load_model
        import argparse
        
        args = argparse.Namespace(
            concept_name="Test Concept",
            mastery=50,
            confidence="medium",
            related=""
        )
        
        cmd_add(args)
        captured = capsys.readouterr()
        
        assert "✅ Added concept: 'Test Concept'" in captured.out
        assert "Mastery: 50%" in captured.out
        assert "Confidence: medium" in captured.out
        
        # Verify in model
        model = load_model()
        assert "Test Concept" in model["concepts"]
        concept = model["concepts"]["Test Concept"]
        assert concept["mastery"] == 50
        assert concept["confidence"] == "medium"
        assert "first_encountered" in concept
        assert "last_reviewed" in concept
        assert concept["struggles"] == []
        assert concept["breakthroughs"] == []
        assert concept["related_concepts"] == []
    
    def test_add_duplicate_refuses(self, temp_data_file, sample_model, capsys):
        """Add refuses to create duplicate concept."""
        from student import cmd_add
        import argparse
        
        args = argparse.Namespace(
            concept_name="React Hooks",  # Already exists in sample
            mastery=70,
            confidence="high",
            related=""
        )
        
        cmd_add(args)
        captured = capsys.readouterr()
        
        assert "❌ Concept 'React Hooks' already exists" in captured.out
        assert "Use 'python student.py update'" in captured.out
    
    def test_add_validates_mastery_range(self, temp_data_file, capsys):
        """Add validates mastery is 0-100."""
        from student import cmd_add, load_model
        import argparse
        
        # Test too high
        args = argparse.Namespace(
            concept_name="New Concept",
            mastery=150,
            confidence="medium",
            related=""
        )
        cmd_add(args)
        captured = capsys.readouterr()
        assert "❌ Mastery must be 0-100" in captured.out
        
        # Verify not added
        model = load_model()
        assert "New Concept" not in model["concepts"]
        
        # Test negative
        args.mastery = -10
        cmd_add(args)
        captured = capsys.readouterr()
        assert "❌ Mastery must be 0-100" in captured.out
    
    def test_add_with_related_concepts(self, temp_data_file, capsys):
        """Add can include related concepts."""
        from student import cmd_add, load_model
        import argparse
        
        args = argparse.Namespace(
            concept_name="Advanced Topic",
            mastery=30,
            confidence="low",
            related="Prereq1,Prereq2,Prereq3"
        )
        
        cmd_add(args)
        captured = capsys.readouterr()
        
        assert "✅ Added concept" in captured.out
        assert "Related: Prereq1,Prereq2,Prereq3" in captured.out
        
        # Verify related concepts stored
        model = load_model()
        concept = model["concepts"]["Advanced Topic"]
        assert "Prereq1" in concept["related_concepts"]
        assert "Prereq2" in concept["related_concepts"]
        assert "Prereq3" in concept["related_concepts"]
    
    def test_add_case_insensitive_duplicate(self, temp_data_file, sample_model, capsys):
        """Add detects duplicates case-insensitively."""
        from student import cmd_add
        import argparse
        
        args = argparse.Namespace(
            concept_name="REACT HOOKS",  # Different case
            mastery=50,
            confidence="medium",
            related=""
        )
        
        cmd_add(args)
        captured = capsys.readouterr()
        
        assert "❌ Concept 'REACT HOOKS' already exists" in captured.out


class TestUpdateCommand:
    """Test the update command for modifying concepts."""
    
    def test_update_mastery(self, temp_data_file, sample_model, capsys):
        """Update changes mastery level."""
        from student import cmd_update, load_model
        import argparse
        
        args = argparse.Namespace(
            concept_name="React Hooks",
            mastery=85,
            confidence=None
        )
        
        cmd_update(args)
        captured = capsys.readouterr()
        
        assert "✅ Updated 'React Hooks'" in captured.out
        assert "mastery 60% → 85%" in captured.out
        
        # Verify change
        model = load_model()
        assert model["concepts"]["React Hooks"]["mastery"] == 85
    
    def test_update_confidence(self, temp_data_file, sample_model, capsys):
        """Update changes confidence level."""
        from student import cmd_update, load_model
        import argparse
        
        args = argparse.Namespace(
            concept_name="React Hooks",
            mastery=None,
            confidence="high"
        )
        
        cmd_update(args)
        captured = capsys.readouterr()
        
        assert "✅ Updated 'React Hooks'" in captured.out
        assert "confidence medium → high" in captured.out
        
        # Verify change
        model = load_model()
        assert model["concepts"]["React Hooks"]["confidence"] == "high"
    
    def test_update_both_fields(self, temp_data_file, sample_model, capsys):
        """Update can change both mastery and confidence."""
        from student import cmd_update, load_model
        import argparse
        
        args = argparse.Namespace(
            concept_name="React Hooks",
            mastery=95,
            confidence="high"
        )
        
        cmd_update(args)
        captured = capsys.readouterr()
        
        assert "✅ Updated 'React Hooks'" in captured.out
        assert "mastery 60% → 95%" in captured.out
        assert "confidence medium → high" in captured.out
        
        # Verify both changes
        model = load_model()
        concept = model["concepts"]["React Hooks"]
        assert concept["mastery"] == 95
        assert concept["confidence"] == "high"
    
    def test_update_nonexistent_concept(self, temp_data_file, capsys):
        """Update fails gracefully for nonexistent concept."""
        from student import cmd_update
        import argparse
        
        args = argparse.Namespace(
            concept_name="Nonexistent",
            mastery=50,
            confidence=None
        )
        
        cmd_update(args)
        captured = capsys.readouterr()
        
        assert "❌ Concept 'Nonexistent' not found" in captured.out
    
    def test_update_validates_mastery(self, temp_data_file, sample_model, capsys):
        """Update validates mastery range."""
        from student import cmd_update, load_model
        import argparse
        
        original_mastery = load_model()["concepts"]["React Hooks"]["mastery"]
        
        args = argparse.Namespace(
            concept_name="React Hooks",
            mastery=200,
            confidence=None
        )
        
        cmd_update(args)
        captured = capsys.readouterr()
        
        assert "❌ Mastery must be 0-100" in captured.out
        
        # Verify no change
        model = load_model()
        assert model["concepts"]["React Hooks"]["mastery"] == original_mastery
    
    def test_update_with_no_changes(self, temp_data_file, sample_model, capsys):
        """Update with no parameters shows info message."""
        from student import cmd_update
        import argparse
        
        args = argparse.Namespace(
            concept_name="React Hooks",
            mastery=None,
            confidence=None
        )
        
        cmd_update(args)
        captured = capsys.readouterr()
        
        assert "ℹ️  No changes specified" in captured.out
    
    def test_update_updates_last_reviewed(self, temp_data_file, sample_model):
        """Update always updates last_reviewed timestamp."""
        from student import cmd_update, load_model
        import argparse
        from datetime import datetime
        
        original_time = load_model()["concepts"]["React Hooks"]["last_reviewed"]
        
        args = argparse.Namespace(
            concept_name="React Hooks",
            mastery=65,
            confidence=None
        )
        
        cmd_update(args)
        
        model = load_model()
        new_time = model["concepts"]["React Hooks"]["last_reviewed"]
        
        assert new_time != original_time
        # Verify it's a valid ISO timestamp
        datetime.fromisoformat(new_time)


class TestStruggleCommand:
    """Test the struggle command for logging difficulties."""
    
    def test_log_struggle(self, temp_data_file, sample_model, capsys):
        """Struggle command adds struggle to concept."""
        from student import cmd_struggle, load_model
        import argparse
        
        args = argparse.Namespace(
            concept_name="React Hooks",
            description="confused about dependency arrays"
        )
        
        cmd_struggle(args)
        captured = capsys.readouterr()
        
        assert "✅ Logged struggle for 'React Hooks'" in captured.out
        assert "confused about dependency arrays" in captured.out
        
        # Verify added
        model = load_model()
        struggles = model["concepts"]["React Hooks"]["struggles"]
        assert "confused about dependency arrays" in struggles
    
    def test_struggle_prevents_duplicates(self, temp_data_file, sample_model, capsys):
        """Struggle command prevents duplicate entries."""
        from student import cmd_struggle, load_model
        import argparse
        
        # Add first struggle
        args = argparse.Namespace(
            concept_name="React Hooks",
            description="closure confusion"
        )
        cmd_struggle(args)
        
        # Try to add same struggle again
        cmd_struggle(args)
        captured = capsys.readouterr()
        
        assert "ℹ️  This struggle already logged" in captured.out
        
        # Verify only one instance
        model = load_model()
        struggles = model["concepts"]["React Hooks"]["struggles"]
        assert struggles.count("closure confusion") == 1
    
    def test_struggle_nonexistent_concept(self, temp_data_file, capsys):
        """Struggle fails gracefully for nonexistent concept."""
        from student import cmd_struggle
        import argparse
        
        args = argparse.Namespace(
            concept_name="Nonexistent",
            description="some struggle"
        )
        
        cmd_struggle(args)
        captured = capsys.readouterr()
        
        assert "❌ Concept 'Nonexistent' not found" in captured.out
        assert "Add it first" in captured.out
    
    def test_struggle_updates_last_reviewed(self, temp_data_file, sample_model):
        """Struggle updates last_reviewed timestamp."""
        from student import cmd_struggle, load_model
        import argparse
        
        original_time = load_model()["concepts"]["React Hooks"]["last_reviewed"]
        
        args = argparse.Namespace(
            concept_name="React Hooks",
            description="new struggle"
        )
        
        cmd_struggle(args)
        
        model = load_model()
        new_time = model["concepts"]["React Hooks"]["last_reviewed"]
        
        assert new_time != original_time


class TestBreakthroughCommand:
    """Test the breakthrough command for logging insights."""
    
    def test_log_breakthrough(self, temp_data_file, sample_model, capsys):
        """Breakthrough command adds breakthrough to concept."""
        from student import cmd_breakthrough, load_model
        import argparse
        
        args = argparse.Namespace(
            concept_name="React Hooks",
            description="understood closure connection"
        )
        
        cmd_breakthrough(args)
        captured = capsys.readouterr()
        
        assert "✅ Logged breakthrough for 'React Hooks'" in captured.out
        assert "💡" in captured.out
        assert "understood closure connection" in captured.out
        
        # Verify added
        model = load_model()
        breakthroughs = model["concepts"]["React Hooks"]["breakthroughs"]
        assert "understood closure connection" in breakthroughs
    
    def test_breakthrough_prevents_duplicates(self, temp_data_file, sample_model, capsys):
        """Breakthrough command prevents duplicate entries."""
        from student import cmd_breakthrough, load_model
        import argparse
        
        # Add first breakthrough
        args = argparse.Namespace(
            concept_name="React Hooks",
            description="eureka moment"
        )
        cmd_breakthrough(args)
        
        # Try to add same breakthrough again
        cmd_breakthrough(args)
        captured = capsys.readouterr()
        
        assert "ℹ️  This breakthrough already logged" in captured.out
        
        # Verify only one instance
        model = load_model()
        breakthroughs = model["concepts"]["React Hooks"]["breakthroughs"]
        assert breakthroughs.count("eureka moment") == 1
    
    def test_breakthrough_nonexistent_concept(self, temp_data_file, capsys):
        """Breakthrough fails gracefully for nonexistent concept."""
        from student import cmd_breakthrough
        import argparse
        
        args = argparse.Namespace(
            concept_name="Nonexistent",
            description="some insight"
        )
        
        cmd_breakthrough(args)
        captured = capsys.readouterr()
        
        assert "❌ Concept 'Nonexistent' not found" in captured.out


class TestLinkCommand:
    """Test the link command for creating concept relationships."""
    
    def test_link_two_concepts(self, temp_data_file, sample_model, capsys):
        """Link command creates relationship between concepts."""
        from student import cmd_link, load_model
        import argparse
        
        args = argparse.Namespace(
            concept_name="React Hooks",
            related_concept="JavaScript Closures"
        )
        
        cmd_link(args)
        captured = capsys.readouterr()
        
        assert "✅ Linked 'React Hooks' → 'JavaScript Closures'" in captured.out
        
        # Verify link added
        model = load_model()
        related = model["concepts"]["React Hooks"]["related_concepts"]
        assert "JavaScript Closures" in related
    
    def test_link_prevents_duplicates(self, temp_data_file, sample_model, capsys):
        """Link command prevents duplicate relationships."""
        from student import cmd_link
        import argparse
        
        # Create first link
        args = argparse.Namespace(
            concept_name="React Hooks",
            related_concept="JavaScript Closures"
        )
        cmd_link(args)
        
        # Try to create same link again
        cmd_link(args)
        captured = capsys.readouterr()
        
        assert "ℹ️  Already linked" in captured.out
    
    def test_link_to_nonexistent_warns(self, temp_data_file, sample_model, capsys):
        """Link warns when related concept doesn't exist yet."""
        from student import cmd_link, load_model
        import argparse
        
        args = argparse.Namespace(
            concept_name="React Hooks",
            related_concept="Nonexistent Concept"
        )
        
        cmd_link(args)
        captured = capsys.readouterr()
        
        assert "⚠️  'Nonexistent Concept' not tracked yet" in captured.out
        assert "Link will be created" in captured.out
        assert "✅ Linked" in captured.out
        
        # Verify link still created
        model = load_model()
        related = model["concepts"]["React Hooks"]["related_concepts"]
        assert "Nonexistent Concept" in related
    
    def test_link_nonexistent_source(self, temp_data_file, capsys):
        """Link fails when source concept doesn't exist."""
        from student import cmd_link
        import argparse
        
        args = argparse.Namespace(
            concept_name="Nonexistent",
            related_concept="Something"
        )
        
        cmd_link(args)
        captured = capsys.readouterr()
        
        assert "❌ Concept 'Nonexistent' not found" in captured.out
    
    def test_link_case_insensitive_duplicate(self, temp_data_file, sample_model, capsys):
        """Link detects duplicates case-insensitively."""
        from student import cmd_link
        import argparse
        
        # Create first link
        args = argparse.Namespace(
            concept_name="React Hooks",
            related_concept="JavaScript Closures"
        )
        cmd_link(args)
        
        # Try with different case
        args.related_concept = "javascript closures"
        cmd_link(args)
        captured = capsys.readouterr()
        
        assert "ℹ️  Already linked" in captured.out


class TestUnlinkCommand:
    """Test the unlink command for removing relationships."""
    
    def test_unlink_concepts(self, temp_data_file, sample_model, capsys):
        """Unlink removes relationship between concepts."""
        from student import cmd_link, cmd_unlink, load_model
        import argparse
        
        # First create a link
        link_args = argparse.Namespace(
            concept_name="React Hooks",
            related_concept="JavaScript Closures"
        )
        cmd_link(link_args)
        
        # Now unlink
        unlink_args = argparse.Namespace(
            concept_name="React Hooks",
            related_concept="JavaScript Closures"
        )
        cmd_unlink(unlink_args)
        captured = capsys.readouterr()
        
        assert "✅ Unlinked 'React Hooks' ✗ 'JavaScript Closures'" in captured.out
        
        # Verify link removed
        model = load_model()
        related = model["concepts"]["React Hooks"]["related_concepts"]
        assert "JavaScript Closures" not in related
    
    def test_unlink_nonexistent_link(self, temp_data_file, sample_model, capsys):
        """Unlink handles nonexistent relationship gracefully."""
        from student import cmd_unlink
        import argparse
        
        args = argparse.Namespace(
            concept_name="React Hooks",
            related_concept="Nonexistent Link"
        )
        
        cmd_unlink(args)
        captured = capsys.readouterr()
        
        assert "ℹ️  No link found" in captured.out
    
    def test_unlink_nonexistent_concept(self, temp_data_file, capsys):
        """Unlink fails when concept doesn't exist."""
        from student import cmd_unlink
        import argparse
        
        args = argparse.Namespace(
            concept_name="Nonexistent",
            related_concept="Something"
        )
        
        cmd_unlink(args)
        captured = capsys.readouterr()
        
        assert "❌ Concept 'Nonexistent' not found" in captured.out
    
    def test_unlink_case_insensitive(self, temp_data_file, sample_model, capsys):
        """Unlink works case-insensitively."""
        from student import cmd_link, cmd_unlink, load_model
        import argparse
        
        # Create link
        link_args = argparse.Namespace(
            concept_name="React Hooks",
            related_concept="JavaScript Closures"
        )
        cmd_link(link_args)
        
        # Unlink with different case
        unlink_args = argparse.Namespace(
            concept_name="React Hooks",
            related_concept="JAVASCRIPT CLOSURES"
        )
        cmd_unlink(unlink_args)
        captured = capsys.readouterr()
        
        assert "✅ Unlinked" in captured.out
        
        # Verify removed
        model = load_model()
        related = model["concepts"]["React Hooks"]["related_concepts"]
        assert len([r for r in related if r.lower() == "javascript closures"]) == 0





class TestSessionEndCommand:
    """Test the session-end batch operation command."""
    
    def test_session_end_update_only(self, temp_data_file, sample_model, capsys):
        """Session-end with only update operations."""
        from student import cmd_session_end, load_model
        import argparse
        
        args = argparse.Namespace(
            update=['React Hooks:75:high'],
            struggle=None,
            breakthrough=None
        )
        
        cmd_session_end(args)
        captured = capsys.readouterr()
        
        assert "📊 Session-End Updates:" in captured.out
        assert "✅ Updated 'React Hooks'" in captured.out
        assert "60% → 75%" in captured.out
        assert "medium → high" in captured.out
        
        # Verify changes
        model = load_model()
        concept = model["concepts"]["React Hooks"]
        assert concept["mastery"] == 75
        assert concept["confidence"] == "high"
    
    def test_session_end_multiple_updates(self, temp_data_file, sample_model, capsys):
        """Session-end can update multiple concepts."""
        from student import cmd_session_end, cmd_add, load_model
        import argparse
        
        # Add another concept
        add_args = argparse.Namespace(
            concept_name="TypeScript",
            mastery=50,
            confidence="medium",
            related=""
        )
        cmd_add(add_args)
        
        # Update both concepts
        args = argparse.Namespace(
            update=[
                'React Hooks:70:high',
                'TypeScript:60:medium'
            ],
            struggle=None,
            breakthrough=None
        )
        
        cmd_session_end(args)
        captured = capsys.readouterr()
        
        assert "React Hooks" in captured.out
        assert "TypeScript" in captured.out
        assert "2 operations" in captured.out
        
        # Verify both changed
        model = load_model()
        assert model["concepts"]["React Hooks"]["mastery"] == 70
        assert model["concepts"]["TypeScript"]["mastery"] == 60
    
    def test_session_end_struggle_only(self, temp_data_file, sample_model, capsys):
        """Session-end with only struggle operations."""
        from student import cmd_session_end, load_model
        import argparse
        
        args = argparse.Namespace(
            update=None,
            struggle=['React Hooks:confusion about dependency arrays'],
            breakthrough=None
        )
        
        cmd_session_end(args)
        captured = capsys.readouterr()
        
        assert "✅ Added struggle to 'React Hooks'" in captured.out
        assert "confusion about dependency arrays" in captured.out
        
        # Verify added
        model = load_model()
        struggles = model["concepts"]["React Hooks"]["struggles"]
        assert "confusion about dependency arrays" in struggles
    
    def test_session_end_breakthrough_only(self, temp_data_file, sample_model, capsys):
        """Session-end with only breakthrough operations."""
        from student import cmd_session_end, load_model
        import argparse
        
        args = argparse.Namespace(
            update=None,
            struggle=None,
            breakthrough=['React Hooks:understood cleanup functions by tracing code']
        )
        
        cmd_session_end(args)
        captured = capsys.readouterr()
        
        assert "✅ Added breakthrough to 'React Hooks'" in captured.out
        assert "💡" in captured.out
        assert "understood cleanup functions" in captured.out
        
        # Verify added
        model = load_model()
        breakthroughs = model["concepts"]["React Hooks"]["breakthroughs"]
        assert "understood cleanup functions by tracing code" in breakthroughs
    
    def test_session_end_all_operations(self, temp_data_file, sample_model, capsys):
        """Session-end can combine all operation types."""
        from student import cmd_session_end, load_model
        import argparse
        
        args = argparse.Namespace(
            update=['React Hooks:80:high'],
            struggle=['React Hooks:still unclear about performance implications'],
            breakthrough=['React Hooks:grasped the closure connection']
        )
        
        cmd_session_end(args)
        captured = capsys.readouterr()
        
        assert "✅ Updated 'React Hooks'" in captured.out
        assert "✅ Added struggle" in captured.out
        assert "✅ Added breakthrough" in captured.out
        assert "3 operations" in captured.out
        
        # Verify all changes
        model = load_model()
        concept = model["concepts"]["React Hooks"]
        assert concept["mastery"] == 80
        assert concept["confidence"] == "high"
        assert "still unclear about performance implications" in concept["struggles"]
        assert "grasped the closure connection" in concept["breakthroughs"]
    
    def test_session_end_invalid_update_format(self, temp_data_file, sample_model, capsys):
        """Session-end validates update format."""
        from student import cmd_session_end
        import argparse
        
        # Missing confidence
        args = argparse.Namespace(
            update=['React Hooks:75'],
            struggle=None,
            breakthrough=None
        )
        
        cmd_session_end(args)
        captured = capsys.readouterr()
        
        assert "❌ Errors encountered:" in captured.out
        assert "Invalid update format" in captured.out
        assert "expected 'Concept:mastery:confidence'" in captured.out
    
    def test_session_end_invalid_mastery(self, temp_data_file, sample_model, capsys):
        """Session-end validates mastery range."""
        from student import cmd_session_end, load_model
        import argparse
        
        original_mastery = load_model()["concepts"]["React Hooks"]["mastery"]
        
        args = argparse.Namespace(
            update=['React Hooks:150:high'],
            struggle=None,
            breakthrough=None
        )
        
        cmd_session_end(args)
        captured = capsys.readouterr()
        
        assert "❌ Errors encountered:" in captured.out
        assert "Invalid mastery" in captured.out
        assert "must be 0-100" in captured.out
        
        # Verify no change
        model = load_model()
        assert model["concepts"]["React Hooks"]["mastery"] == original_mastery
    
    def test_session_end_invalid_confidence(self, temp_data_file, sample_model, capsys):
        """Session-end validates confidence values."""
        from student import cmd_session_end, load_model
        import argparse
        
        original_conf = load_model()["concepts"]["React Hooks"]["confidence"]
        
        args = argparse.Namespace(
            update=['React Hooks:75:super-high'],
            struggle=None,
            breakthrough=None
        )
        
        cmd_session_end(args)
        captured = capsys.readouterr()
        
        assert "❌ Errors encountered:" in captured.out
        assert "Invalid confidence" in captured.out
        
        # Verify no change
        model = load_model()
        assert model["concepts"]["React Hooks"]["confidence"] == original_conf
    
    def test_session_end_nonexistent_concept(self, temp_data_file, sample_model, capsys):
            """Session-end handles nonexistent concepts gracefully."""
            from student import cmd_session_end
            import argparse

            args = argparse.Namespace(
                update=['Nonexistent:50:medium'],
                struggle=['Nonexistent:some struggle'],
                breakthrough=['Nonexistent:some breakthrough']
            )

            cmd_session_end(args)
            captured = capsys.readouterr()

            assert "❌ Errors encountered:" in captured.out
            # CORRECTED: Count the occurrences of the full error string in the output.
            assert captured.out.count("Concept 'Nonexistent' not found") == 3
    ###
    def test_session_end_partial_success(self, temp_data_file, sample_model, capsys):
        """Session-end reports both successes and failures."""
        from student import cmd_session_end, load_model
        import argparse
        
        args = argparse.Namespace(
            update=[
                'React Hooks:75:high',  # Valid
                'Nonexistent:50:medium'  # Invalid
            ],
            struggle=None,
            breakthrough=None
        )
        
        cmd_session_end(args)
        captured = capsys.readouterr()
        
        # Should show both error and success
        assert "❌ Errors encountered:" in captured.out
        assert "Concept 'Nonexistent' not found" in captured.out
        assert "✅ Updated 'React Hooks'" in captured.out
        
        # Valid change should be applied
        model = load_model()
        assert model["concepts"]["React Hooks"]["mastery"] == 75
    
    def test_session_end_duplicate_struggle(self, temp_data_file, sample_model, capsys):
        """Session-end detects duplicate struggles."""
        from student import cmd_session_end, cmd_struggle, load_model
        import argparse
        
        # Add struggle first
        struggle_args = argparse.Namespace(
            concept_name="React Hooks",
            description="dependency array confusion"
        )
        cmd_struggle(struggle_args)
        
        # Try to add same struggle via session-end
        args = argparse.Namespace(
            update=None,
            struggle=['React Hooks:dependency array confusion'],
            breakthrough=None
        )
        
        cmd_session_end(args)
        captured = capsys.readouterr()
        
        assert "ℹ️  Struggle already logged" in captured.out
        
        # Verify only one instance
        model = load_model()
        struggles = model["concepts"]["React Hooks"]["struggles"]
        assert struggles.count("dependency array confusion") == 1
    
    def test_session_end_duplicate_breakthrough(self, temp_data_file, sample_model, capsys):
        """Session-end detects duplicate breakthroughs."""
        from student import cmd_session_end, cmd_breakthrough, load_model
        import argparse
        
        # Add breakthrough first
        bt_args = argparse.Namespace(
            concept_name="React Hooks",
            description="understood closure connection"
        )
        cmd_breakthrough(bt_args)
        
        # Try to add same breakthrough via session-end
        args = argparse.Namespace(
            update=None,
            struggle=None,
            breakthrough=['React Hooks:understood closure connection']
        )
        
        cmd_session_end(args)
        captured = capsys.readouterr()
        
        assert "ℹ️  Breakthrough already logged" in captured.out
        
        # Verify only one instance
        model = load_model()
        breakthroughs = model["concepts"]["React Hooks"]["breakthroughs"]
        assert breakthroughs.count("understood closure connection") == 1
    
    def test_session_end_empty_operations(self, temp_data_file, sample_model, capsys):
        """Session-end with no operations shows info message."""
        from student import cmd_session_end
        import argparse
        
        args = argparse.Namespace(
            update=None,
            struggle=None,
            breakthrough=None
        )
        
        cmd_session_end(args)
        captured = capsys.readouterr()
        
        assert "ℹ️  No changes to apply" in captured.out
        assert "Use --update, --struggle, or --breakthrough" in captured.out
    
    def test_session_end_invalid_struggle_format(self, temp_data_file, sample_model, capsys):
        """Session-end validates struggle format."""
        from student import cmd_session_end
        import argparse
        
        args = argparse.Namespace(
            update=None,
            struggle=['No colon separator here'],
            breakthrough=None
        )
        
        cmd_session_end(args)
        captured = capsys.readouterr()
        
        assert "❌ Errors encountered:" in captured.out
        assert "Invalid struggle format" in captured.out
        assert "expected 'Concept:description'" in captured.out
    
    def test_session_end_updates_last_reviewed(self, temp_data_file, sample_model):
        """Session-end updates last_reviewed timestamp for all modified concepts."""
        from student import cmd_session_end, load_model
        import argparse
        from datetime import datetime
        
        original_time = load_model()["concepts"]["React Hooks"]["last_reviewed"]
        
        args = argparse.Namespace(
            update=['React Hooks:65:medium'],
            struggle=['React Hooks:new struggle'],
            breakthrough=['React Hooks:new breakthrough']
        )
        
        cmd_session_end(args)
        
        model = load_model()
        new_time = model["concepts"]["React Hooks"]["last_reviewed"]
        
        assert new_time != original_time
        # Verify it's a valid ISO timestamp
        datetime.fromisoformat(new_time)
    
    def test_session_end_colon_in_description(self, temp_data_file, sample_model, capsys):
        """Session-end handles colons in struggle/breakthrough descriptions."""
        from student import cmd_session_end, load_model
        import argparse
        
        args = argparse.Namespace(
            update=None,
            struggle=['React Hooks:understood that cleanup runs before: next effect OR unmount'],
            breakthrough=None
        )
        
        cmd_session_end(args)
        captured = capsys.readouterr()
        
        assert "✅ Added struggle" in captured.out
        
        # Verify the full description is preserved
        model = load_model()
        struggles = model["concepts"]["React Hooks"]["struggles"]
        assert "understood that cleanup runs before: next effect OR unmount" in struggles
    
    def test_session_end_multiple_same_type(self, temp_data_file, sample_model, capsys):
        """Session-end can add multiple struggles/breakthroughs to same concept."""
        from student import cmd_session_end, load_model
        import argparse
        
        args = argparse.Namespace(
            update=None,
            struggle=[
                'React Hooks:struggle one',
                'React Hooks:struggle two'
            ],
            breakthrough=[
                'React Hooks:breakthrough one',
                'React Hooks:breakthrough two'
            ]
        )
        
        cmd_session_end(args)
        captured = capsys.readouterr()
        
        assert captured.out.count("✅ Added struggle") == 2
        assert captured.out.count("✅ Added breakthrough") == 2
        
        # Verify all added
        model = load_model()
        concept = model["concepts"]["React Hooks"]
        assert "struggle one" in concept["struggles"]
        assert "struggle two" in concept["struggles"]
        assert "breakthrough one" in concept["breakthroughs"]
        assert "breakthrough two" in concept["breakthroughs"]
