"""
Apple Notes exporter implementation.
"""

import subprocess
from typing import Dict, Any, Optional
import logging
import datetime
import markdown
from .exporters import DocumentExporter

logger = logging.getLogger(__name__)


class AppleNotesExporter(DocumentExporter):
    """Handles creation of notes in Apple Notes via AppleScript."""

    def __init__(self):
        """Initialize the AppleNotesExporter."""
        pass

    def validate_configuration(self) -> bool:
        """
        Validate that Apple Notes is available.

        Returns:
            bool: True if Apple Notes is accessible, False otherwise
        """
        script = '''
        tell application "System Events"
            set notesRunning to exists (processes where name is "Notes")
        end tell
        '''
        try:
            result = self._run_script(script)
            return result
        except Exception as e:
            logger.error(f"Failed to validate Apple Notes configuration: {str(e)}")
            return False

    def export(self, title: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Create a new note in Apple Notes.

        Args:
            title (str): The title of the note
            content (str): The content of the note (markdown format)
            metadata (Dict[str, Any], optional): Additional metadata to include in the note

        Returns:
            bool: True if note was created successfully, False otherwise
        """
        # Remove the first H1 header from content if it matches the title
        # This prevents title duplication in the note
        content_without_title = self._remove_title_header(content, title)
        
        # Convert markdown content to HTML
        html_content = self._convert_markdown_to_html(content_without_title)
        
        # Build the complete note content: Content + Separator + Metadata
        content_parts = []
        
        # Add the main content first
        content_parts.append(html_content)
        
        # Add formatted metadata at the end if provided
        if metadata:
            # Add a visual separator before metadata
            separator = "<hr><br>"
            content_parts.append(separator)
            
            metadata_section = self._format_metadata(metadata)
            metadata_html = self._convert_markdown_to_html(metadata_section)
            content_parts.append(metadata_html)
        
        # Join all parts
        full_content = "".join(content_parts)

        # Escape special characters for AppleScript
        title = self._escape_for_applescript(title)
        full_content = self._escape_for_applescript(full_content)

        script = f'''
        tell application "Notes"
            tell account "iCloud"
                set newNote to make new note at folder "Notes" with properties {{name:"{title}", body:"{full_content}"}}
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

    def _remove_title_header(self, content: str, title: str) -> str:
        """
        Remove the first H1 header from content if it matches the title.
        This prevents title duplication in Apple Notes.
        
        Args:
            content: The markdown content
            title: The extracted title
            
        Returns:
            str: Content with title header removed if it was a duplicate
        """
        if not content or not title:
            return content
            
        lines = content.strip().split('\n')
        if not lines:
            return content
            
        # Check if first non-empty line is an H1 that matches the title
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            if line.startswith('# '):
                header_title = line[2:].strip()
                if header_title == title:
                    # Remove this line and return the rest
                    remaining_lines = lines[i+1:]
                    # Remove any immediately following empty lines
                    while remaining_lines and not remaining_lines[0].strip():
                        remaining_lines.pop(0)
                    return '\n'.join(remaining_lines)
            # If we hit non-header content, stop looking
            break
            
        return content

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