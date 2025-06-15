"""Integration tests for the Markdown to Apple Notes converter."""

import os
import shutil
import tempfile
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock
from src.app import MD2Note
from src.md2note import parse_args

@pytest.fixture
def test_environment():
    """Set up a test environment with sample markdown files."""
    # Create temporary directories
    temp_dir = tempfile.mkdtemp()
    source_dir = Path(temp_dir) / "source"
    clean_dir = Path(temp_dir) / "clean"
    source_dir.mkdir()
    clean_dir.mkdir()

    # Create test markdown files with different scenarios
    test_files = {
        "simple.md": "# Simple Note\nThis is a simple note.",
        "with_metadata.md": """---
title: Test Note
tags: [test, integration]
---
# Test Note
This is a test note with metadata.""",
        "nested/subdir/note.md": "# Nested Note\nThis is a note in a subdirectory.",
        "special_chars.md": "# Special Characters\nThis note has special characters: !@#$%^&*()",
        "empty.md": "",
        "invalid.md": "This is not valid markdown"
    }

    # Create the files
    for file_path, content in test_files.items():
        full_path = source_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content)

    yield {
        "source_dir": source_dir,
        "clean_dir": clean_dir,
        "test_files": test_files
    }

    # Cleanup
    shutil.rmtree(temp_dir)

@pytest.fixture
def mock_subprocess():
    """Mock subprocess.Popen for testing."""
    with patch('src.applescript.subprocess.Popen') as mock_popen:
        mock_process = MagicMock()
        mock_process.communicate.return_value = (b'', b'')
        mock_process.returncode = 0
        mock_popen.return_value = mock_process
        yield mock_popen

def test_full_workflow(test_environment):
    """Test the complete workflow from scanning to note creation."""
    app = MD2Note(str(test_environment["source_dir"]), str(test_environment["clean_dir"]))
    app.run()

    # Verify files were moved to clean directory
    for file_path in test_environment["test_files"].keys():
        clean_path = test_environment["clean_dir"] / file_path
        assert clean_path.exists(), f"File {file_path} was not moved to clean directory"

def test_cli_argument_parsing():
    """Test CLI argument parsing with various combinations."""
    import sys
    from src.md2note import parse_args

    # Test required source argument
    sys.argv = ["main.py", "--source", "/test/path"]
    args = parse_args()
    assert args.source == "/test/path"
    assert args.clean is None

    # Test with clean directory
    sys.argv = ["main.py", "--source", "/test/path", "--clean", "/clean/path"]
    args = parse_args()
    assert args.source == "/test/path"
    assert args.clean == "/clean/path"

def test_error_handling(test_environment, caplog):
    """Test error handling in production scenarios."""
    # Test with non-existent source directory
    with pytest.raises(Exception):
        app = MD2Note("/non/existent/path")
        app.run()

    # Test with read-only clean directory
    os.chmod(test_environment["clean_dir"], 0o444)
    app = MD2Note(str(test_environment["source_dir"]), str(test_environment["clean_dir"]))
    with caplog.at_level("ERROR"):
        app.run()
        assert any("Permission denied" in message for message in caplog.text.splitlines())
    os.chmod(test_environment["clean_dir"], 0o777)

def test_logging_in_production(test_environment):
    """Test logging behavior in production scenarios."""
    import logging
    app = MD2Note(str(test_environment["source_dir"]), str(test_environment["clean_dir"]))
    app.run()

    # Flush and close all logging handlers to ensure log is written
    for handler in logging.getLogger().handlers:
        handler.flush()
        handler.close()
    
    # Verify log file was created
    assert Path("md2note.log").exists()
    
    # Check log content
    log_content = Path("md2note.log").read_text()
    assert "Starting conversion process" in log_content
    assert "Successfully processed file" in log_content or "Successfully processed" in log_content

    # Cleanup
    Path("md2note.log").unlink()

def test_file_preservation(test_environment):
    """Test that file content and structure is preserved."""
    app = MD2Note(str(test_environment["source_dir"]), str(test_environment["clean_dir"]))
    app.run()

    # Verify content preservation
    for file_path, original_content in test_environment["test_files"].items():
        clean_path = test_environment["clean_dir"] / file_path
        if clean_path.exists():
            assert clean_path.read_text() == original_content

def test_directory_structure_preservation(test_environment):
    """Test that directory structure is preserved during file movement."""
    app = MD2Note(str(test_environment["source_dir"]), str(test_environment["clean_dir"]))
    app.run()

    # Verify nested directory structure
    nested_dir = test_environment["clean_dir"] / "nested" / "subdir"
    assert nested_dir.exists()
    assert (nested_dir / "note.md").exists()

def test_end_to_end_with_custom_folder(test_environment, mock_subprocess):
    """Test end-to-end processing with custom folder."""
    # Create test markdown file
    content = "# Test Note\n\nThis is a test note for folder testing."
    test_file = test_environment["source_dir"] / "test.md"
    test_file.write_text(content)

    # Run the application with custom folder
    app = MD2Note(str(test_environment["source_dir"]), str(test_environment["clean_dir"]), folder="Test Folder")
    app.run()

    # Verify file was moved
    moved_file = test_environment["clean_dir"] / "test.md"
    assert moved_file.exists()
    assert not test_file.exists()

@patch('src.applescript.AppleNotesCreator.generate_unique_folder_name')
def test_end_to_end_with_auto_folder(mock_generate, test_environment, mock_subprocess):
    """Test end-to-end processing with auto-generated folder."""
    # Mock folder name generation
    mock_generate.return_value = "md2note-20250615-120000"
    
    # Create test markdown file
    content = "# Test Note\n\nThis is a test note for auto-folder testing."
    test_file = test_environment["source_dir"] / "test.md" 
    test_file.write_text(content)

    # Run the application with auto-folder
    app = MD2Note(str(test_environment["source_dir"]), str(test_environment["clean_dir"]), auto_folder=True)
    app.run()

    # Verify unique folder name was generated
    mock_generate.assert_called_once()

    # Verify file was moved
    moved_file = test_environment["clean_dir"] / "test.md"
    assert moved_file.exists()
    assert not test_file.exists()

def test_folder_with_special_characters(test_environment, mock_subprocess):
    """Test folder creation with special characters in folder name."""
    # Create test markdown file
    content = "# Test Note\n\nTesting folder with special characters."
    test_file = test_environment["source_dir"] / "test.md"
    test_file.write_text(content)

    # Run with folder containing special characters
    special_folder = 'Import "Batch" & More'
    app = MD2Note(str(test_environment["source_dir"]), str(test_environment["clean_dir"]), folder=special_folder)
    app.run()

    # Verify file was processed
    moved_file = test_environment["clean_dir"] / "test.md"
    assert moved_file.exists() 