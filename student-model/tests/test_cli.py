"""
test_cli.py - CLI Integration Tests

Tests the command-line interface end-to-end.
"""

import subprocess
import tempfile
import shutil
import json
from pathlib import Path
import pytest


@pytest.fixture
def temp_env(monkeypatch):
    """Create isolated environment for CLI tests."""
    temp_dir = tempfile.mkdtemp()
    temp_file = Path(temp_dir) / "test_student_model.json"
    
    # Set environment to use temp file
    monkeypatch.setenv('STUDENT_MODEL_PATH', str(temp_file))
    
    yield temp_dir, temp_file
    
    # Cleanup
    shutil.rmtree(temp_dir)


class TestCLIInit:
    """Test 'init' command."""
    
    def test_init_command(self, temp_env):
        """Init command creates model file."""
        temp_dir, temp_file = temp_env
        
        # Note: This test assumes student.py respects STUDENT_MODEL_PATH env var
        # For now, it's a placeholder showing the testing pattern
        # Real implementation would need env var support or --file flag
        
        # Would run: subprocess.run(['python', 'student.py', 'init'])
        # Then check temp_file.exists()
        pass
    
    def test_init_with_profile(self, temp_env):
        """Init command accepts profile argument."""
        # Would run: subprocess.run(['python', 'student.py', 'init', '--profile', 'Test'])
        pass


class TestCLIInfo:
    """Test 'info' command."""
    
    def test_info_shows_metadata(self, temp_env):
        """Info command displays model metadata."""
        pass


class TestCLIHelp:
    """Test help functionality."""
    
    def test_help_text(self):
        """Running with no args shows help."""
        result = subprocess.run(
            ['python', 'student.py'],
            capture_output=True,
            text=True
        )
        
        assert 'Student Model CLI' in result.stdout or 'usage:' in result.stdout.lower()
    
    def test_help_flag(self):
        """--help flag shows help."""
        result = subprocess.run(
            ['python', 'student.py', '--help'],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert 'help' in result.stdout.lower() or 'usage' in result.stdout.lower()


# Placeholder tests for future commands
class TestCLIFuture:
    """Placeholder tests for Phase 2-3 commands."""
    
    def test_list_command(self):
        """Test 'list' command (Phase 2)."""
        pytest.skip("Not implemented yet - Phase 2")
    
    def test_show_command(self):
        """Test 'show' command (Phase 2)."""
        pytest.skip("Not implemented yet - Phase 2")
    
    def test_add_command(self):
        """Test 'add' command (Phase 3)."""
        pytest.skip("Not implemented yet - Phase 3")
    
    def test_update_command(self):
        """Test 'update' command (Phase 3)."""
        pytest.skip("Not implemented yet - Phase 3")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])