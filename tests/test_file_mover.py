"""
Tests for the file movement functionality.
"""

import os
import tempfile
import pytest
from pathlib import Path
from src.file_mover import FileMover

@pytest.fixture
def temp_dirs():
    """Create temporary directories for testing."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        source_dir = Path(tmpdirname) / "source"
        source_dir.mkdir()
        
        # Create a test file
        test_file = source_dir / "test.md"
        test_file.write_text("Test content")
        
        # Create a nested directory with a file
        nested_dir = source_dir / "subdir"
        nested_dir.mkdir()
        nested_file = nested_dir / "nested.md"
        nested_file.write_text("Nested content")
        
        yield {
            "source_dir": str(source_dir),
            "test_file": str(test_file),
            "nested_file": str(nested_file)
        }

def test_file_mover_initialization(temp_dirs):
    """Test FileMover initialization with default clean directory."""
    mover = FileMover(temp_dirs["source_dir"])
    assert mover.source_dir == Path(temp_dirs["source_dir"])
    assert mover.clean_dir == Path(temp_dirs["source_dir"]) / "clean"
    assert mover.clean_dir.exists()

def test_file_mover_custom_clean_dir(temp_dirs):
    """Test FileMover initialization with custom clean directory."""
    custom_clean = Path(temp_dirs["source_dir"]) / "custom_clean"
    mover = FileMover(temp_dirs["source_dir"], str(custom_clean))
    assert mover.clean_dir == custom_clean
    assert custom_clean.exists()

def test_file_mover_invalid_source_dir():
    """Test FileMover initialization with invalid source directory."""
    with pytest.raises(ValueError):
        FileMover("/nonexistent/directory")

def test_move_file_success(temp_dirs):
    """Test successful file movement."""
    mover = FileMover(temp_dirs["source_dir"])
    
    # Move the test file
    result = mover.move_file(temp_dirs["test_file"])
    assert result is True
    
    # Check that file was moved
    source_path = Path(temp_dirs["test_file"])
    dest_path = mover.clean_dir / "test.md"
    assert not source_path.exists()
    assert dest_path.exists()
    assert dest_path.read_text() == "Test content"

def test_move_nested_file(temp_dirs):
    """Test moving a file from a nested directory."""
    mover = FileMover(temp_dirs["source_dir"])
    
    # Move the nested file
    result = mover.move_file(temp_dirs["nested_file"])
    assert result is True
    
    # Check that file was moved and directory structure was preserved
    source_path = Path(temp_dirs["nested_file"])
    dest_path = mover.clean_dir / "subdir" / "nested.md"
    assert not source_path.exists()
    assert dest_path.exists()
    assert dest_path.read_text() == "Nested content"

def test_move_nonexistent_file(temp_dirs):
    """Test moving a file that doesn't exist."""
    mover = FileMover(temp_dirs["source_dir"])
    result = mover.move_file("/nonexistent/file.md")
    assert result is False

def test_get_clean_directory(temp_dirs):
    """Test getting the clean directory path."""
    mover = FileMover(temp_dirs["source_dir"])
    clean_dir = mover.get_clean_directory()
    assert clean_dir == Path(temp_dirs["source_dir"]) / "clean" 