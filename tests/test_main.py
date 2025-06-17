"""Tests for the main application module."""

import argparse
import logging
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.app import MD2Note

@pytest.fixture
def temp_source_dir(tmp_path):
    """Create a temporary directory with test files."""
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    subdir = source_dir / "subdir"
    subdir.mkdir()
    (source_dir / "test1.md").write_text("# Test 1\nContent 1")
    (source_dir / "test2.md").write_text("# Test 2\nContent 2")
    (subdir / "test3.md").write_text("# Test 3\nContent 3")
    return source_dir

@pytest.fixture
def mock_components():
    """Mock all component classes."""
    with patch("src.md2note.DirectoryScanner") as mock_scanner, \
         patch("src.exporters.ExporterFactory") as mock_factory, \
         patch("src.metadata.MarkdownMetadataExtractor") as mock_processor, \
         patch("src.file_mover.FileMover") as mock_mover:
        # Configure mock scanner
        mock_scanner.return_value.scan_for_markdown.return_value = [
            Path("test1.md"),
            Path("test2.md"),
            Path("subdir/test3.md")
        ]
        # Configure mock processor
        mock_processor.return_value.get_content.return_value = "Processed content"
        mock_processor.return_value.extract.return_value = {"title": "Test Title"}
        # Configure mock exporter factory
        mock_exporter = MagicMock()
        mock_exporter.export.return_value = True
        mock_exporter.validate_configuration.return_value = True
        mock_factory.create_exporter.return_value = mock_exporter
        yield {
            "scanner": mock_scanner,
            "factory": mock_factory,
            "exporter": mock_exporter,
            "processor": mock_processor,
            "mover": mock_mover
        }

def test_md2note_initialization(temp_source_dir):
    """Test MD2Note initialization."""
    app = MD2Note(str(temp_source_dir))
    assert app.source_dir == temp_source_dir
    assert app.clean_dir == temp_source_dir / "clean"
    custom_clean = temp_source_dir / "custom_clean"
    app = MD2Note(str(temp_source_dir), str(custom_clean))
    assert app.clean_dir == custom_clean

def test_md2note_process_file(temp_source_dir):
    scanner = MagicMock()
    exporter = MagicMock()
    processor_cls = MagicMock()
    mover = MagicMock()
    processor_instance = MagicMock()
    processor_instance.get_content.return_value = "Processed content"
    processor_instance.extract.return_value = {"title": "Test Title"}
    processor_instance.get_title.return_value = "Test Title"
    processor_cls.return_value = processor_instance
    exporter.export.return_value = True
    exporter.validate_configuration.return_value = True
    app = MD2Note(
        str(temp_source_dir),
        directory_scanner=scanner,
        exporter=exporter,
        file_processor=processor_cls,
        file_mover=mover
    )
    file_path = temp_source_dir / "test1.md"
    assert app.process_file(file_path) is True
    processor_cls.assert_called_with(str(file_path))
    processor_instance.get_content.assert_called_once()
    processor_instance.extract.assert_called_once()
    processor_instance.get_title.assert_called_once()
    exporter.export.assert_called_once_with("Test Title", "Processed content", {"title": "Test Title"})
    mover.move_file.assert_called_once_with(file_path)

def test_md2note_run(temp_source_dir):
    scanner = MagicMock()
    exporter = MagicMock()
    processor_cls = MagicMock()
    mover = MagicMock()
    processor_instance = MagicMock()
    processor_instance.get_content.return_value = "Processed content"
    processor_instance.extract.return_value = {"title": "Test Title"}
    processor_instance.get_title.return_value = "Test Title"
    processor_cls.return_value = processor_instance
    exporter.export.return_value = True
    exporter.validate_configuration.return_value = True
    scanner.scan_for_markdown.return_value = [
        temp_source_dir / "test1.md",
        temp_source_dir / "test2.md"
    ]
    app = MD2Note(
        str(temp_source_dir),
        directory_scanner=scanner,
        exporter=exporter,
        file_processor=processor_cls,
        file_mover=mover
    )
    app.run()
    scanner.scan_for_markdown.assert_called_once()
    assert processor_cls.call_count == 2
    assert exporter.export.call_count == 2
    assert mover.move_file.call_count == 2

def test_md2note_run_no_files(temp_source_dir):
    scanner = MagicMock()
    exporter = MagicMock()
    processor_cls = MagicMock()
    mover = MagicMock()
    scanner.scan_for_markdown.return_value = []
    exporter.validate_configuration.return_value = True
    app = MD2Note(
        str(temp_source_dir),
        directory_scanner=scanner,
        exporter=exporter,
        file_processor=processor_cls,
        file_mover=mover
    )
    app.run()
    scanner.scan_for_markdown.assert_called_once()
    processor_cls.assert_not_called()
    exporter.export.assert_not_called()
    mover.move_file.assert_not_called()

def test_md2note_error_handling(temp_source_dir):
    scanner = MagicMock()
    exporter = MagicMock()
    processor_cls = MagicMock()
    mover = MagicMock()
    processor_instance = MagicMock()
    processor_instance.get_content.side_effect = Exception("Processing error")
    processor_cls.return_value = processor_instance
    exporter.validate_configuration.return_value = True
    app = MD2Note(
        str(temp_source_dir),
        directory_scanner=scanner,
        exporter=exporter,
        file_processor=processor_cls,
        file_mover=mover
    )
    assert app.process_file(temp_source_dir / "test1.md") is False
    scanner.scan_for_markdown.side_effect = Exception("Scanner error")