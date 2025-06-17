"""
Unit tests for the Google Docs exporter.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, mock_open
from pathlib import Path
from googleapiclient.errors import HttpError
from src.google_docs_exporter import GoogleDocsExporter


class TestGoogleDocsExporter:
    """Test cases for the GoogleDocsExporter class."""

    def test_init_without_folder(self):
        """Test initialization without folder."""
        exporter = GoogleDocsExporter()
        assert exporter.gdocs_folder is None
        assert exporter.credentials is None
        assert exporter.docs_service is None
        assert exporter.drive_service is None
        assert exporter.folder_id is None

    def test_init_with_folder(self):
        """Test initialization with folder."""
        exporter = GoogleDocsExporter(gdocs_folder="Test Folder")
        assert exporter.gdocs_folder == "Test Folder"

    @patch('pathlib.Path.exists')
    def test_validate_configuration_no_credentials_file(self, mock_exists):
        """Test validation failure when credentials.json is missing."""
        mock_exists.return_value = False
        exporter = GoogleDocsExporter()
        
        result = exporter.validate_configuration()
        assert result is False

    @patch('pathlib.Path.exists')
    @patch.object(GoogleDocsExporter, '_authenticate')
    def test_validate_configuration_auth_failure(self, mock_auth, mock_exists):
        """Test validation failure when authentication fails."""
        mock_exists.return_value = True
        mock_auth.return_value = False
        exporter = GoogleDocsExporter()
        
        result = exporter.validate_configuration()
        assert result is False

    @patch('pathlib.Path.exists')
    @patch.object(GoogleDocsExporter, '_authenticate')
    @patch.object(GoogleDocsExporter, '_find_or_create_folder')
    def test_validate_configuration_folder_failure(self, mock_folder, mock_auth, mock_exists):
        """Test validation failure when folder creation fails."""
        mock_exists.return_value = True
        mock_auth.return_value = True
        mock_folder.return_value = None
        exporter = GoogleDocsExporter(gdocs_folder="Test Folder")
        
        result = exporter.validate_configuration()
        assert result is False

    @patch('pathlib.Path.exists')
    @patch.object(GoogleDocsExporter, '_authenticate')
    @patch.object(GoogleDocsExporter, '_find_or_create_folder')
    def test_validate_configuration_success(self, mock_folder, mock_auth, mock_exists):
        """Test successful validation."""
        mock_exists.return_value = True
        mock_auth.return_value = True
        mock_folder.return_value = "folder123"
        exporter = GoogleDocsExporter(gdocs_folder="Test Folder")
        
        result = exporter.validate_configuration()
        assert result is True
        assert exporter.folder_id == "folder123"

    @patch.object(GoogleDocsExporter, '_authenticate')
    @patch.object(GoogleDocsExporter, '_insert_content')
    def test_export_success(self, mock_insert, mock_auth):
        """Test successful document export."""
        mock_auth.return_value = True
        mock_insert.return_value = True
        
        # Mock Google Docs service
        mock_docs_service = Mock()
        mock_create_response = {'documentId': 'doc123'}
        mock_docs_service.documents().create().execute.return_value = mock_create_response
        
        exporter = GoogleDocsExporter()
        exporter.docs_service = mock_docs_service
        exporter.drive_service = Mock()
        
        result = exporter.export("Test Title", "Test content")
        assert result is True

    @patch.object(GoogleDocsExporter, '_authenticate')
    def test_export_auth_failure(self, mock_auth):
        """Test export failure when authentication fails."""
        mock_auth.return_value = False
        exporter = GoogleDocsExporter()
        
        result = exporter.export("Test Title", "Test content")
        assert result is False

    @patch.object(GoogleDocsExporter, '_authenticate')
    def test_export_http_error(self, mock_auth):
        """Test export failure with HTTP error."""
        mock_auth.return_value = True
        
        # Mock Google Docs service with HTTP error
        mock_docs_service = Mock()
        mock_docs_service.documents().create().execute.side_effect = HttpError(
            resp=Mock(status=400), content=b'{"error": "Bad Request"}'
        )
        
        exporter = GoogleDocsExporter()
        exporter.docs_service = mock_docs_service
        exporter.drive_service = Mock()
        
        result = exporter.export("Test Title", "Test content")
        assert result is False

    @patch('src.google_docs_exporter.build')
    @patch('src.google_docs_exporter.InstalledAppFlow.from_client_secrets_file')
    @patch('src.google_docs_exporter.pickle.dump')
    @patch('src.google_docs_exporter.pickle.load')
    @patch('src.google_docs_exporter.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_authenticate_new_credentials(self, mock_file, mock_exists, mock_load, mock_dump, mock_flow, mock_build):
        """Test authentication with new credentials."""
        mock_exists.return_value = False
        
        # Mock OAuth flow
        mock_creds = Mock()
        mock_creds.valid = True
        mock_flow_instance = Mock()
        mock_flow_instance.run_local_server.return_value = mock_creds
        mock_flow.return_value = mock_flow_instance
        
        # Mock service build
        mock_docs = Mock()
        mock_drive = Mock()
        mock_build.side_effect = [mock_docs, mock_drive]
        
        exporter = GoogleDocsExporter()
        result = exporter._authenticate()
        
        assert result is True
        assert exporter.credentials == mock_creds
        assert exporter.docs_service == mock_docs
        assert exporter.drive_service == mock_drive

    @patch('src.google_docs_exporter.build')
    @patch('src.google_docs_exporter.pickle.load')
    @patch('src.google_docs_exporter.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_authenticate_existing_valid_credentials(self, mock_file, mock_exists, mock_load, mock_build):
        """Test authentication with existing valid credentials."""
        mock_exists.return_value = True
        
        # Mock existing valid credentials
        mock_creds = Mock()
        mock_creds.valid = True
        mock_load.return_value = mock_creds
        
        # Mock service build
        mock_docs = Mock()
        mock_drive = Mock()
        mock_build.side_effect = [mock_docs, mock_drive]
        
        exporter = GoogleDocsExporter()
        result = exporter._authenticate()
        
        assert result is True
        assert exporter.credentials == mock_creds

    def test_convert_markdown_to_text(self):
        """Test markdown to text conversion."""
        exporter = GoogleDocsExporter()
        
        # Test basic markdown
        text = exporter._convert_markdown_to_text("# Header\n\nParagraph with **bold** text")
        assert "Header" in text
        assert "Paragraph with bold text" in text
        assert "#" not in text
        assert "**" not in text

    def test_convert_markdown_to_text_empty(self):
        """Test markdown to text conversion with empty content."""
        exporter = GoogleDocsExporter()
        assert exporter._convert_markdown_to_text("") == ""
        assert exporter._convert_markdown_to_text(None) == ""

    def test_format_metadata(self):
        """Test metadata formatting."""
        exporter = GoogleDocsExporter()
        metadata = {
            "filename": "test.md",
            "filepath": "/path/to/test.md",
            "size": 1024,
            "modified_time": "2024-01-01T12:00:00"
        }
        
        formatted = exporter._format_metadata(metadata)
        assert "📄 File Info:" in formatted
        assert "test.md" in formatted
        assert "/path/to/test.md" in formatted
        assert "1.0 KB" in formatted

    def test_format_metadata_empty(self):
        """Test metadata formatting with empty metadata."""
        exporter = GoogleDocsExporter()
        assert exporter._format_metadata({}) == ""
        assert exporter._format_metadata(None) == ""

    def test_insert_content_success(self):
        """Test successful content insertion."""
        mock_docs_service = Mock()
        mock_docs_service.documents().batchUpdate().execute.return_value = {}
        
        exporter = GoogleDocsExporter()
        exporter.docs_service = mock_docs_service
        
        result = exporter._insert_content("doc123", "Test content")
        assert result is True

    def test_insert_content_with_metadata(self):
        """Test content insertion with metadata."""
        mock_docs_service = Mock()
        mock_docs_service.documents().batchUpdate().execute.return_value = {}
        
        exporter = GoogleDocsExporter()
        exporter.docs_service = mock_docs_service
        
        metadata = {"filename": "test.md"}
        result = exporter._insert_content("doc123", "Test content", metadata)
        assert result is True

    def test_insert_content_failure(self):
        """Test content insertion failure."""
        mock_docs_service = Mock()
        mock_docs_service.documents().batchUpdate().execute.side_effect = Exception("API Error")
        
        exporter = GoogleDocsExporter()
        exporter.docs_service = mock_docs_service
        
        result = exporter._insert_content("doc123", "Test content")
        assert result is False

    def test_find_or_create_folder_existing(self):
        """Test finding existing folder."""
        mock_drive_service = Mock()
        mock_drive_service.files().list().execute.return_value = {
            'files': [{'id': 'folder123', 'name': 'Test Folder'}]
        }
        
        exporter = GoogleDocsExporter()
        exporter.drive_service = mock_drive_service
        
        folder_id = exporter._find_or_create_folder("Test Folder")
        assert folder_id == "folder123"

    def test_find_or_create_folder_new(self):
        """Test creating new folder."""
        mock_drive_service = Mock()
        mock_drive_service.files().list().execute.return_value = {'files': []}
        mock_drive_service.files().create().execute.return_value = {'id': 'newfolder123'}
        
        exporter = GoogleDocsExporter()
        exporter.drive_service = mock_drive_service
        
        folder_id = exporter._find_or_create_folder("Test Folder")
        assert folder_id == "newfolder123"

    def test_find_or_create_folder_error(self):
        """Test folder creation error."""
        mock_drive_service = Mock()
        mock_drive_service.files().list().execute.side_effect = Exception("API Error")
        
        exporter = GoogleDocsExporter()
        exporter.drive_service = mock_drive_service
        
        folder_id = exporter._find_or_create_folder("Test Folder")
        assert folder_id is None

    def test_move_to_folder_success(self):
        """Test successful file move to folder."""
        mock_drive_service = Mock()
        mock_drive_service.files().get().execute.return_value = {'parents': ['parent1']}
        mock_drive_service.files().update().execute.return_value = {}
        
        exporter = GoogleDocsExporter()
        exporter.drive_service = mock_drive_service
        
        result = exporter._move_to_folder("file123", "folder123")
        assert result is True

    def test_move_to_folder_failure(self):
        """Test file move failure."""
        mock_drive_service = Mock()
        mock_drive_service.files().get().execute.side_effect = Exception("API Error")
        
        exporter = GoogleDocsExporter()
        exporter.drive_service = mock_drive_service
        
        result = exporter._move_to_folder("file123", "folder123")
        assert result is False