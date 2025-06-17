"""
Unit tests for the document exporters module.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.exporters import DocumentExporter, ExporterFactory


class TestExporterFactory:
    """Test cases for the ExporterFactory class."""

    def test_create_apple_notes_exporter(self):
        """Test creating an Apple Notes exporter."""
        with patch('src.apple_notes_exporter.AppleNotesExporter') as mock_exporter:
            mock_instance = Mock()
            mock_exporter.return_value = mock_instance
            
            exporter = ExporterFactory.create_exporter("apple_notes")
            
            mock_exporter.assert_called_once()
            assert exporter == mock_instance

    def test_create_google_docs_exporter(self):
        """Test creating a Google Docs exporter."""
        with patch('src.google_docs_exporter.GoogleDocsExporter') as mock_exporter:
            mock_instance = Mock()
            mock_exporter.return_value = mock_instance
            
            exporter = ExporterFactory.create_exporter("google_docs", gdocs_folder="Test Folder")
            
            mock_exporter.assert_called_once_with(gdocs_folder="Test Folder")
            assert exporter == mock_instance

    def test_create_google_docs_exporter_without_folder(self):
        """Test creating a Google Docs exporter without specifying folder."""
        with patch('src.google_docs_exporter.GoogleDocsExporter') as mock_exporter:
            mock_instance = Mock()
            mock_exporter.return_value = mock_instance
            
            exporter = ExporterFactory.create_exporter("google_docs")
            
            mock_exporter.assert_called_once_with(gdocs_folder=None)
            assert exporter == mock_instance

    def test_create_unsupported_exporter(self):
        """Test creating an unsupported exporter type raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported export type: unsupported"):
            ExporterFactory.create_exporter("unsupported")

    def test_create_exporter_with_empty_string(self):
        """Test creating an exporter with empty string raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported export type: "):
            ExporterFactory.create_exporter("")


class TestDocumentExporter:
    """Test cases for the DocumentExporter abstract base class."""

    def test_cannot_instantiate_abstract_class(self):
        """Test that DocumentExporter cannot be instantiated directly."""
        with pytest.raises(TypeError):
            DocumentExporter()

    def test_subclass_must_implement_export(self):
        """Test that subclasses must implement export method."""
        class IncompleteExporter(DocumentExporter):
            def validate_configuration(self):
                return True

        with pytest.raises(TypeError):
            IncompleteExporter()

    def test_subclass_must_implement_validate_configuration(self):
        """Test that subclasses must implement validate_configuration method."""
        class IncompleteExporter(DocumentExporter):
            def export(self, title, content, metadata=None):
                return True

        with pytest.raises(TypeError):
            IncompleteExporter()

    def test_complete_subclass_can_be_instantiated(self):
        """Test that complete subclasses can be instantiated."""
        class CompleteExporter(DocumentExporter):
            def export(self, title, content, metadata=None):
                return True
            
            def validate_configuration(self):
                return True

        exporter = CompleteExporter()
        assert isinstance(exporter, DocumentExporter)
        assert exporter.export("test", "content") is True
        assert exporter.validate_configuration() is True