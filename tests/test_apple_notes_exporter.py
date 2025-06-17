"""
Unit tests for the Apple Notes exporter.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.apple_notes_exporter import AppleNotesExporter


class TestAppleNotesExporter:
    """Test cases for the AppleNotesExporter class."""

    def setUp(self):
        """Set up test fixtures."""
        self.exporter = AppleNotesExporter()

    def test_validate_configuration_success(self):
        """Test successful configuration validation."""
        exporter = AppleNotesExporter()
        with patch.object(exporter, '_run_script', return_value=True):
            result = exporter.validate_configuration()
            assert result is True

    def test_validate_configuration_failure(self):
        """Test configuration validation failure."""
        exporter = AppleNotesExporter()
        with patch.object(exporter, '_run_script', return_value=False):
            result = exporter.validate_configuration()
            assert result is False

    def test_validate_configuration_exception(self):
        """Test configuration validation with exception."""
        exporter = AppleNotesExporter()
        with patch.object(exporter, '_run_script', side_effect=Exception("Test error")):
            result = exporter.validate_configuration()
            assert result is False

    def test_export_success(self):
        """Test successful note export."""
        exporter = AppleNotesExporter()
        with patch.object(exporter, '_run_script', return_value=True), \
             patch.object(exporter, '_convert_markdown_to_html', return_value="<p>Test content</p>"), \
             patch.object(exporter, '_escape_for_applescript', side_effect=lambda x: x):
            
            result = exporter.export("Test Title", "Test content")
            assert result is True

    def test_export_failure(self):
        """Test failed note export."""
        exporter = AppleNotesExporter()
        with patch.object(exporter, '_run_script', return_value=False), \
             patch.object(exporter, '_convert_markdown_to_html', return_value="<p>Test content</p>"), \
             patch.object(exporter, '_escape_for_applescript', side_effect=lambda x: x):
            
            result = exporter.export("Test Title", "Test content")
            assert result is False

    def test_export_with_metadata(self):
        """Test note export with metadata."""
        exporter = AppleNotesExporter()
        metadata = {"filename": "test.md", "size": 1024}
        
        with patch.object(exporter, '_run_script', return_value=True), \
             patch.object(exporter, '_convert_markdown_to_html', return_value="<p>Test content</p>"), \
             patch.object(exporter, '_format_metadata', return_value="**File Info:**\n• Filename: test.md"), \
             patch.object(exporter, '_escape_for_applescript', side_effect=lambda x: x):
            
            result = exporter.export("Test Title", "Test content", metadata)
            assert result is True

    def test_convert_markdown_to_html(self):
        """Test markdown to HTML conversion."""
        exporter = AppleNotesExporter()
        
        # Test basic markdown
        html = exporter._convert_markdown_to_html("# Header\n\nParagraph")
        assert "<h1>" in html
        assert "<p>" in html

    def test_convert_markdown_to_html_empty(self):
        """Test markdown to HTML conversion with empty content."""
        exporter = AppleNotesExporter()
        
        assert exporter._convert_markdown_to_html("") == ""
        assert exporter._convert_markdown_to_html(None) == ""

    def test_format_metadata(self):
        """Test metadata formatting."""
        exporter = AppleNotesExporter()
        metadata = {
            "filename": "test.md",
            "filepath": "/path/to/test.md",
            "size": 1024,
            "modified_time": "2024-01-01T12:00:00"
        }
        
        formatted = exporter._format_metadata(metadata)
        assert "📄 **File Info:**" in formatted
        assert "test.md" in formatted
        assert "/path/to/test.md" in formatted
        assert "1.0 KB" in formatted

    def test_format_metadata_empty(self):
        """Test metadata formatting with empty metadata."""
        exporter = AppleNotesExporter()
        assert exporter._format_metadata({}) == ""
        assert exporter._format_metadata(None) == ""

    def test_escape_for_applescript(self):
        """Test AppleScript escaping."""
        exporter = AppleNotesExporter()
        
        # Test quote escaping
        result = exporter._escape_for_applescript('He said "Hello"')
        assert result == 'He said \\"Hello\\"'
        
        # Test newline escaping
        result = exporter._escape_for_applescript("Line 1\nLine 2")
        assert result == "Line 1\\nLine 2"

    @patch('subprocess.Popen')
    def test_run_script_success(self, mock_popen):
        """Test successful AppleScript execution."""
        exporter = AppleNotesExporter()
        
        # Mock successful process
        mock_process = Mock()
        mock_process.returncode = 0
        mock_process.communicate.return_value = (b"success", b"")
        mock_popen.return_value = mock_process
        
        result = exporter._run_script("test script")
        assert result is True

    @patch('subprocess.Popen')
    def test_run_script_failure(self, mock_popen):
        """Test failed AppleScript execution."""
        exporter = AppleNotesExporter()
        
        # Mock failed process
        mock_process = Mock()
        mock_process.returncode = 1
        mock_process.communicate.return_value = (b"", b"error message")
        mock_popen.return_value = mock_process
        
        result = exporter._run_script("test script")
        assert result is False

    @patch('subprocess.Popen')
    def test_run_script_exception(self, mock_popen):
        """Test AppleScript execution with exception."""
        exporter = AppleNotesExporter()
        mock_popen.side_effect = Exception("Process error")
        
        result = exporter._run_script("test script")
        assert result is False

    def test_remove_title_header_matching(self):
        """Test removal of title header when it matches the title."""
        exporter = AppleNotesExporter()
        content = "# My Title\n\nThis is the content."
        title = "My Title"
        
        result = exporter._remove_title_header(content, title)
        assert result == "This is the content."

    def test_remove_title_header_not_matching(self):
        """Test that title header is not removed when it doesn't match."""
        exporter = AppleNotesExporter()
        content = "# Different Title\n\nThis is the content."
        title = "My Title"
        
        result = exporter._remove_title_header(content, title)
        assert result == "# Different Title\n\nThis is the content."

    def test_remove_title_header_no_header(self):
        """Test content without H1 header remains unchanged."""
        exporter = AppleNotesExporter()
        content = "This is just content without headers."
        title = "My Title"
        
        result = exporter._remove_title_header(content, title)
        assert result == "This is just content without headers."

    def test_remove_title_header_empty_lines(self):
        """Test removal with empty lines after title header."""
        exporter = AppleNotesExporter()
        content = "# My Title\n\n\n\nThis is the content."
        title = "My Title"
        
        result = exporter._remove_title_header(content, title)
        assert result == "This is the content."

    def test_remove_title_header_empty_content(self):
        """Test with empty content."""
        exporter = AppleNotesExporter()
        
        assert exporter._remove_title_header("", "Title") == ""
        assert exporter._remove_title_header("Content", "") == "Content"