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