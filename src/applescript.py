"""
AppleScript interface for creating notes in Apple Notes.
"""

import subprocess
from typing import Dict, Any, Optional
import json
import logging

logger = logging.getLogger(__name__)

class AppleNotesCreator:
    """Handles creation of notes in Apple Notes via AppleScript."""

    def __init__(self):
        """Initialize the AppleNotesCreator."""
        self._verify_notes_app()

    def _verify_notes_app(self) -> None:
        """Verify that Apple Notes is available."""
        script = '''
        tell application "System Events"
            set notesRunning to exists (processes where name is "Notes")
        end tell
        '''
        result = self._run_script(script)
        if not result:
            raise RuntimeError("Apple Notes is not running. Please start Notes.app first.")

    def create_note(self, title: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Create a new note in Apple Notes.

        Args:
            title (str): The title of the note
            content (str): The content of the note
            metadata (Dict[str, Any], optional): Additional metadata to include in the note

        Returns:
            bool: True if note was created successfully, False otherwise
        """
        # Prepare the note content with metadata if provided
        full_content = content
        if metadata:
            metadata_str = json.dumps(metadata, indent=2)
            full_content = f"Metadata:\n{metadata_str}\n\n---\n\n{content}"

        # Escape special characters for AppleScript
        title = self._escape_for_applescript(title)
        full_content = self._escape_for_applescript(full_content)

        script = f'''
        tell application "Notes"
            tell account "iCloud"
                make new note at folder "Notes" with properties {{name:"{title}", body:"{full_content}"}}
            end tell
        end tell
        '''
        
        try:
            result = self._run_script(script)
            if result:
                logger.info(f"Successfully created note: {title}")
                return True
            else:
                logger.error(f"Failed to create note: {title}")
                return False
        except Exception as e:
            logger.error(f"Error creating note: {str(e)}")
            return False

    def _run_script(self, script: str) -> bool:
        """
        Run an AppleScript and return whether it was successful.

        Args:
            script (str): The AppleScript to run

        Returns:
            bool: True if script executed successfully, False otherwise
        """
        try:
            process = subprocess.Popen(
                ['osascript', '-e', script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                logger.error(f"AppleScript error: {stderr.decode('utf-8')}")
                return False
            return True
        except Exception as e:
            logger.error(f"Error running AppleScript: {str(e)}")
            return False

    def _escape_for_applescript(self, text: str) -> str:
        """
        Escape special characters for AppleScript.

        Args:
            text (str): The text to escape

        Returns:
            str: Escaped text
        """
        # Replace double quotes with escaped double quotes
        text = text.replace('"', '\\"')
        # Replace newlines with literal newlines
        text = text.replace('\n', '\\n')
        return text 