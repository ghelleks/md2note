"""
Tests for the AppleScript interface.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.applescript import AppleNotesCreator

@pytest.fixture
def mock_subprocess():
    """Mock subprocess.Popen for testing."""
    with patch('subprocess.Popen') as mock_popen:
        mock_process = MagicMock()
        mock_process.communicate.return_value = (b'', b'')
        mock_process.returncode = 0
        mock_popen.return_value = mock_process
        yield mock_popen

@pytest.fixture
def notes_creator(mock_subprocess):
    """Create an AppleNotesCreator instance with mocked subprocess."""
    return AppleNotesCreator()

def test_verify_notes_app_running(notes_creator, mock_subprocess):
    """Test that verify_notes_app works when Notes is running."""
    assert notes_creator._verify_notes_app() is None

def test_verify_notes_app_not_running(mock_subprocess):
    """Test that verify_notes_app raises error when Notes is not running."""
    mock_process = MagicMock()
    mock_process.communicate.return_value = (b'', b'')
    mock_process.returncode = 1
    mock_subprocess.return_value = mock_process
    
    with pytest.raises(RuntimeError):
        AppleNotesCreator()

def test_create_note_success(notes_creator, mock_subprocess):
    """Test successful note creation."""
    title = "Test Note"
    content = "Test content"
    metadata = {"author": "Test Author"}
    
    result = notes_creator.create_note(title, content, metadata)
    assert result is True
    
    # Verify the AppleScript command was called with correct parameters
    # We expect two calls: one for verification and one for note creation
    assert mock_subprocess.call_count == 2
    
    # Get the second call (note creation)
    note_creation_call = mock_subprocess.call_args_list[1]
    args = note_creation_call[0]
    # args[0] is the list of command-line arguments: ['osascript', '-e', script]
    script = args[0][2]
    assert title in script
    assert content in script
    assert "Test Author" in script

def test_create_note_failure(notes_creator, mock_subprocess):
    """Test note creation failure."""
    mock_process = MagicMock()
    mock_process.communicate.return_value = (b'', b'Error')
    mock_process.returncode = 1
    mock_subprocess.return_value = mock_process
    
    result = notes_creator.create_note("Test Note", "Test content")
    assert result is False

def test_escape_for_applescript(notes_creator):
    """Test escaping special characters for AppleScript."""
    text = 'Hello "World"\nNew line'
    escaped = notes_creator._escape_for_applescript(text)
    assert '\\"' in escaped
    assert '\\n' in escaped

def test_format_metadata_basic(notes_creator):
    """Test basic metadata formatting."""
    metadata = {
        "filename": "test.md",
        "filepath": "/path/to/test.md",
        "modified_time": "2025-06-15T07:23:40.698187",
        "size": 1024
    }
    
    formatted = notes_creator._format_metadata(metadata)
    assert "📄 **File Info:**" in formatted
    assert "**Filename:** test.md" in formatted
    assert "**File Path:** /path/to/test.md" in formatted
    assert "June 15, 2025 at 07:23 AM" in formatted
    assert "**Size:** 1.0 KB" in formatted

def test_format_metadata_small_file(notes_creator):
    """Test metadata formatting for small files."""
    metadata = {
        "filename": "small.md",
        "size": 500
    }
    
    formatted = notes_creator._format_metadata(metadata)
    assert "**Size:** 500 bytes" in formatted

def test_format_metadata_custom_fields(notes_creator):
    """Test metadata formatting with custom fields."""
    metadata = {
        "filename": "test.md",
        "custom_field": "custom value",
        "another_field": "another value"
    }
    
    formatted = notes_creator._format_metadata(metadata)
    assert "**Custom Field:** custom value" in formatted
    assert "**Another Field:** another value" in formatted

def test_format_metadata_empty(notes_creator):
    """Test metadata formatting with empty metadata."""
    formatted = notes_creator._format_metadata({})
    assert formatted == ""
    
    formatted = notes_creator._format_metadata(None)
    assert formatted == ""

def test_convert_markdown_to_html_basic(notes_creator):
    """Test basic markdown to HTML conversion."""
    markdown_content = "# Heading\n\nThis is **bold** and *italic* text with `code`."
    html_content = notes_creator._convert_markdown_to_html(markdown_content)
    
    assert "<h1>Heading</h1>" in html_content
    assert "<strong>bold</strong>" in html_content
    assert "<em>italic</em>" in html_content
    assert "<code>code</code>" in html_content

def test_convert_markdown_to_html_lists(notes_creator):
    """Test markdown list conversion."""
    markdown_content = "- First item\n- Second item with **bold**"
    html_content = notes_creator._convert_markdown_to_html(markdown_content)
    
    assert "<ul>" in html_content
    assert "<li>First item</li>" in html_content
    assert "<li>Second item with <strong>bold</strong></li>" in html_content

def test_convert_markdown_to_html_code_blocks(notes_creator):
    """Test markdown code block conversion."""
    markdown_content = "```python\nprint('hello')\n```"
    html_content = notes_creator._convert_markdown_to_html(markdown_content)
    
    assert "<pre><code" in html_content
    assert "print('hello')" in html_content

def test_convert_markdown_to_html_empty(notes_creator):
    """Test empty markdown conversion."""
    assert notes_creator._convert_markdown_to_html("") == ""
    assert notes_creator._convert_markdown_to_html(None) == ""

def test_generate_unique_folder_name():
    """Test unique folder name generation."""
    folder_name = AppleNotesCreator.generate_unique_folder_name()
    assert folder_name.startswith("md2note-")
    # md2note- = 8, YYYY = 4, MM = 2, DD = 2, - = 1, HH = 2, MM = 2, SS = 2
    # Total: 8 + 4 + 2 + 2 + 1 + 2 + 2 + 2 = 23
    assert len(folder_name) == 23

def test_create_note_with_custom_folder(notes_creator, mock_subprocess):
    """Test note creation with custom folder."""
    result = notes_creator.create_note("Test Title", "Test Content", None, "Custom Folder")
    assert result is True
    
    # Verify the script includes folder creation logic
    note_creation_call = mock_subprocess.call_args_list[1]  # Second call is note creation
    script = note_creation_call[0][0][2]
    assert "Custom Folder" in script
    assert "make new folder" in script

def test_create_note_with_default_folder(notes_creator, mock_subprocess):
    """Test note creation with default folder (None)."""
    result = notes_creator.create_note("Test Title", "Test Content", None, None)
    assert result is True
    
    # Verify the script uses "Notes" as default folder
    note_creation_call = mock_subprocess.call_args_list[1]  # Second call is note creation
    script = note_creation_call[0][0][2]
    assert '"Notes"' in script

def test_create_note_folder_with_special_characters(notes_creator, mock_subprocess):
    """Test note creation with folder containing special characters."""
    folder_with_quotes = 'Folder "with quotes"'
    result = notes_creator.create_note("Test Title", "Test Content", None, folder_with_quotes)
    assert result is True
    
    # Verify the script properly escapes the folder name
    note_creation_call = mock_subprocess.call_args_list[1]  # Second call is note creation  
    script = note_creation_call[0][0][2]
    assert 'Folder \\"with quotes\\"' in script 