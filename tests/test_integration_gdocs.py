"""
Integration tests for Google Docs export functionality.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from src.app import MD2Note
from src.exporters import ExporterFactory
from src.google_docs_exporter import GoogleDocsExporter


class TestGoogleDocsIntegration:
    """Integration tests for Google Docs export workflow."""

    def setup_method(self):
        """Set up test fixtures for each test."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.source_dir = self.temp_dir / "source"
        self.clean_dir = self.temp_dir / "clean"
        self.source_dir.mkdir()

    def teardown_method(self):
        """Clean up after each test."""
        shutil.rmtree(self.temp_dir)

    def create_test_markdown_file(self, filename: str, content: str, metadata: str = ""):
        """Helper to create test markdown files."""
        file_path = self.source_dir / filename
        full_content = f"{metadata}\n{content}" if metadata else content
        file_path.write_text(full_content)
        return file_path

    @patch.object(GoogleDocsExporter, 'validate_configuration', return_value=True)
    @patch.object(GoogleDocsExporter, 'export', return_value=True)
    def test_end_to_end_google_docs_export(self, mock_export, mock_validate):
        """Test complete end-to-end Google Docs export workflow."""
        # Create test markdown files
        self.create_test_markdown_file(
            "test1.md",
            "# Test Document 1\n\nThis is test content.",
            "---\ntitle: Test Document 1\nauthor: Test Author\n---"
        )
        self.create_test_markdown_file(
            "test2.md",
            "# Test Document 2\n\nThis is more test content."
        )

        # Initialize app with Google Docs export
        app = MD2Note(
            source_dir=str(self.source_dir),
            clean_dir=str(self.clean_dir),
            export_type="google_docs",
            gdocs_folder="Test Folder"
        )

        # Run the conversion
        app.run()

        # Verify exports were called
        assert mock_export.call_count == 2
        
        # Verify files were moved to clean directory
        assert self.clean_dir.exists()
        clean_files = list(self.clean_dir.glob("*.md"))
        assert len(clean_files) == 2

    @patch.object(GoogleDocsExporter, 'validate_configuration', return_value=False)
    def test_configuration_validation_failure(self, mock_validate):
        """Test that configuration validation failure prevents processing."""
        self.create_test_markdown_file("test.md", "# Test\n\nContent")

        app = MD2Note(
            source_dir=str(self.source_dir),
            clean_dir=str(self.clean_dir),
            export_type="google_docs"
        )

        with pytest.raises(RuntimeError, match="Exporter not properly configured"):
            app.run()

    @patch.object(GoogleDocsExporter, 'validate_configuration', return_value=True)
    @patch.object(GoogleDocsExporter, 'export', return_value=False)
    def test_export_failure_handling(self, mock_export, mock_validate):
        """Test handling of export failures."""
        self.create_test_markdown_file("test.md", "# Test\n\nContent")

        app = MD2Note(
            source_dir=str(self.source_dir),
            clean_dir=str(self.clean_dir),
            export_type="google_docs"
        )

        app.run()

        # Export was attempted
        mock_export.assert_called_once()
        
        # File should not be moved on failure
        clean_files = list(self.clean_dir.glob("*.md"))
        assert len(clean_files) == 0

    @patch.object(GoogleDocsExporter, 'validate_configuration', return_value=True)
    @patch.object(GoogleDocsExporter, 'export')
    def test_metadata_extraction_and_export(self, mock_export, mock_validate):
        """Test that metadata is properly extracted and passed to exporter."""
        mock_export.return_value = True
        
        # Create file with YAML front matter
        self.create_test_markdown_file(
            "test.md",
            "# Test Document\n\nContent here.",
            "---\ntitle: Custom Title\nauthor: Test Author\ntags: [test, markdown]\n---"
        )

        app = MD2Note(
            source_dir=str(self.source_dir),
            clean_dir=str(self.clean_dir),
            export_type="google_docs"
        )

        app.run()

        # Verify export was called with metadata
        mock_export.assert_called_once()
        call_args = mock_export.call_args
        
        # Check that metadata was passed
        title, content, metadata = call_args[0]
        assert metadata is not None
        assert "filename" in metadata or "filepath" in metadata

    def test_exporter_factory_integration(self):
        """Test that ExporterFactory correctly creates Google Docs exporter."""
        exporter = ExporterFactory.create_exporter("google_docs", gdocs_folder="Test Folder")
        
        assert isinstance(exporter, GoogleDocsExporter)
        assert exporter.gdocs_folder == "Test Folder"

    @patch.object(GoogleDocsExporter, 'validate_configuration', return_value=True)
    @patch.object(GoogleDocsExporter, 'export', return_value=True)
    def test_multiple_file_types_processing(self, mock_export, mock_validate):
        """Test processing of multiple markdown file types."""
        # Create various markdown files
        self.create_test_markdown_file("README.md", "# README\n\nProject info")
        self.create_test_markdown_file("CHANGELOG.md", "# Changelog\n\n## v1.0")
        self.create_test_markdown_file("doc.markdown", "# Documentation")
        
        # Create non-markdown file (should be ignored)
        (self.source_dir / "test.txt").write_text("Not markdown")

        app = MD2Note(
            source_dir=str(self.source_dir),
            clean_dir=str(self.clean_dir),
            export_type="google_docs"
        )

        app.run()

        # Should only process markdown files
        assert mock_export.call_count == 3

    @patch.object(GoogleDocsExporter, 'validate_configuration', return_value=True)
    @patch.object(GoogleDocsExporter, 'export', return_value=True)
    def test_nested_directory_processing(self, mock_export, mock_validate):
        """Test processing of markdown files in nested directories."""
        # Create nested structure
        nested_dir = self.source_dir / "subdir"
        nested_dir.mkdir()
        
        self.create_test_markdown_file("root.md", "# Root file")
        (nested_dir / "nested.md").write_text("# Nested file\n\nContent")

        app = MD2Note(
            source_dir=str(self.source_dir),
            clean_dir=str(self.clean_dir),
            export_type="google_docs"
        )

        app.run()

        # Should process all markdown files
        assert mock_export.call_count == 2

    @patch.object(GoogleDocsExporter, 'validate_configuration', return_value=True)
    @patch.object(GoogleDocsExporter, 'export', side_effect=[True, False, True])
    def test_partial_success_handling(self, mock_export, mock_validate):
        """Test handling when some exports succeed and others fail."""
        self.create_test_markdown_file("success1.md", "# Success 1")
        self.create_test_markdown_file("failure.md", "# Failure")
        self.create_test_markdown_file("success2.md", "# Success 2")

        app = MD2Note(
            source_dir=str(self.source_dir),
            clean_dir=str(self.clean_dir),
            export_type="google_docs"
        )

        app.run()

        # All exports attempted
        assert mock_export.call_count == 3
        
        # Only successful files moved
        clean_files = list(self.clean_dir.glob("*.md"))
        assert len(clean_files) == 2

    @patch.object(GoogleDocsExporter, 'validate_configuration', return_value=True)
    def test_empty_source_directory(self, mock_validate):
        """Test handling of empty source directory."""
        app = MD2Note(
            source_dir=str(self.source_dir),
            clean_dir=str(self.clean_dir),
            export_type="google_docs"
        )

        # Should complete without error
        app.run()

    @patch.object(GoogleDocsExporter, 'validate_configuration', return_value=True)
    @patch.object(GoogleDocsExporter, 'export', return_value=True)
    def test_special_characters_in_filenames(self, mock_export, mock_validate):
        """Test handling of files with special characters in names."""
        self.create_test_markdown_file("file with spaces.md", "# File with spaces")
        self.create_test_markdown_file("file-with-dashes.md", "# File with dashes")
        self.create_test_markdown_file("file_with_underscores.md", "# File with underscores")

        app = MD2Note(
            source_dir=str(self.source_dir),
            clean_dir=str(self.clean_dir),
            export_type="google_docs"
        )

        app.run()

        assert mock_export.call_count == 3
        
        # Verify all files were moved
        clean_files = list(self.clean_dir.glob("*.md"))
        assert len(clean_files) == 3