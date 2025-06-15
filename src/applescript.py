"""
AppleScript interface for creating notes in Apple Notes.
"""

import subprocess
from typing import Dict, Any, Optional
import json
import logging
import datetime
import markdown

logger = logging.getLogger(__name__)

class AppleNotesCreator:
    """Handles creation of notes in Apple Notes via AppleScript."""

    def __init__(self):
        """Initialize the AppleNotesCreator."""
        self._verify_notes_app()

    @staticmethod
    def generate_unique_folder_name() -> str:
        """
        Generate a unique folder name using timestamp.
        
        Returns:
            str: Unique folder name in format "md2note-YYYYMMDD-HHMMSS"
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        return f"md2note-{timestamp}"

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

    def create_note(self, title: str, content: str, metadata: Optional[Dict[str, Any]] = None, folder: Optional[str] = None) -> bool:
        """
        Create a new note in Apple Notes.

        Args:
            title (str): The title of the note
            content (str): The content of the note (markdown format)
            metadata (Dict[str, Any], optional): Additional metadata to include in the note
            folder (str, optional): The folder name to place the note in. If None, uses default "Notes" folder.

        Returns:
            bool: True if note was created successfully, False otherwise
        """
        # Convert markdown content to HTML
        html_content = self._convert_markdown_to_html(content)
        
        # Build the complete note content: Metadata + Content
        # The title will be set as the note name in Apple Notes
        content_parts = []
        
        # Add formatted metadata if provided
        if metadata:
            metadata_section = self._format_metadata(metadata)
            metadata_html = self._convert_markdown_to_html(metadata_section)
            content_parts.append(metadata_html)
        
        # Add the main content
        content_parts.append(html_content)
        
        # Join all parts with line breaks
        full_content = "<br><br>".join(content_parts)

        # Escape special characters for AppleScript
        title = self._escape_for_applescript(title)
        full_content = self._escape_for_applescript(full_content)

        # Determine target folder
        target_folder = folder if folder else "Notes"
        target_folder = self._escape_for_applescript(target_folder)

        script = f'''
        tell application "Notes"
            tell account "iCloud"
                try
                    set targetFolder to folder "{target_folder}"
                on error
                    set targetFolder to make new folder with properties {{name:"{target_folder}"}}
                end try
                set newNote to make new note at targetFolder with properties {{name:"{title}", body:"{full_content}"}}
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

    def _convert_markdown_to_html(self, md_content: str) -> str:
        """
        Convert markdown content to HTML for rich text display in Apple Notes.
        
        Args:
            md_content: Markdown content string
            
        Returns:
            str: HTML content
        """
        if not md_content or md_content is None:
            return ""
            
        # Configure markdown with extensions for better formatting
        md = markdown.Markdown(extensions=[
            'markdown.extensions.fenced_code',
            'markdown.extensions.tables',
            'markdown.extensions.nl2br'
        ])
        
        return md.convert(md_content)

    def _format_metadata(self, metadata: Dict[str, Any]) -> str:
        """
        Format metadata as human-readable key-value pairs.
        
        Args:
            metadata: Dictionary of metadata to format
            
        Returns:
            str: Formatted metadata string
        """
        if not metadata:
            return ""
            
        formatted_lines = ["📄 **File Info:**"]
        
        # Format specific metadata fields
        if "filename" in metadata:
            formatted_lines.append(f"• **Filename:** {metadata['filename']}")
        
        if "filepath" in metadata:
            formatted_lines.append(f"• **File Path:** {metadata['filepath']}")
            
        if "modified_time" in metadata:
            # Format ISO datetime to readable format
            try:
                dt = datetime.datetime.fromisoformat(metadata['modified_time'])
                formatted_time = dt.strftime("%B %d, %Y at %I:%M %p")
                formatted_lines.append(f"• **Modified:** {formatted_time}")
            except:
                formatted_lines.append(f"• **Modified:** {metadata['modified_time']}")
        
        if "size" in metadata:
            size_kb = metadata['size'] / 1024
            if size_kb < 1:
                size_str = f"{metadata['size']} bytes"
            else:
                size_str = f"{size_kb:.1f} KB"
            formatted_lines.append(f"• **Size:** {size_str}")
            
        # Add any other metadata fields not specifically handled
        handled_fields = {"filename", "filepath", "modified_time", "created_time", "size"}
        for key, value in metadata.items():
            if key not in handled_fields:
                formatted_lines.append(f"• **{key.replace('_', ' ').title()}:** {value}")
        
        return "\n".join(formatted_lines)

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