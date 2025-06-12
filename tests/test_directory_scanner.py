"""
Tests for the directory scanner functionality.
"""

import os
import tempfile
from pathlib import Path
import pytest
from src.md2note import DirectoryScanner


@pytest.fixture
def temp_dir():
    """Create a temporary directory with some test files."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Create some test files
        test_files = [
            "test1.md",
            "test2.md",
            "test3.txt",
            "subdir/test4.md",
            "subdir/test5.txt"
        ]
        
        for file_path in test_files:
            full_path = os.path.join(tmpdirname, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as f:
                f.write("Test content")
        
        yield tmpdirname


def test_directory_scanner_initialization(temp_dir):
    """Test that DirectoryScanner initializes correctly."""
    scanner = DirectoryScanner(temp_dir)
    assert scanner.directory == Path(temp_dir)


def test_directory_scanner_invalid_directory():
    """Test that DirectoryScanner raises error for invalid directory."""
    with pytest.raises(ValueError):
        DirectoryScanner("/nonexistent/directory")


def test_directory_scanner_invalid_path(temp_dir):
    """Test that DirectoryScanner raises error for non-directory path."""
    file_path = os.path.join(temp_dir, "test1.md")
    with pytest.raises(ValueError):
        DirectoryScanner(file_path)


def test_scan_for_markdown(temp_dir):
    """Test that scan_for_markdown finds all markdown files."""
    scanner = DirectoryScanner(temp_dir)
    markdown_files = scanner.scan_for_markdown()
    
    # Should find 3 markdown files
    assert len(markdown_files) == 3
    
    # Check that all found files are markdown files
    for file_path in markdown_files:
        assert file_path.suffix == '.md'
    
    # Check that we found all expected files
    found_files = {str(f.relative_to(temp_dir)) for f in markdown_files}
    expected_files = {'test1.md', 'test2.md', 'subdir/test4.md'}
    assert found_files == expected_files


def test_get_file_count(temp_dir):
    """Test that get_file_count returns correct number of markdown files."""
    scanner = DirectoryScanner(temp_dir)
    assert scanner.get_file_count() == 3 