"""
Google Docs exporter implementation.
"""

import os
import pickle
import logging
from typing import Dict, Any, Optional
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import markdown

from .exporters import DocumentExporter

logger = logging.getLogger(__name__)

# Google Docs API scopes
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']


class GoogleDocsExporter(DocumentExporter):
    """Handles creation of documents in Google Docs via Google API."""

    def __init__(self, gdocs_folder: Optional[str] = None):
        """
        Initialize the GoogleDocsExporter.

        Args:
            gdocs_folder (str, optional): Target Google Drive folder for documents
        """
        self.gdocs_folder = gdocs_folder
        self.credentials = None
        self.docs_service = None
        self.drive_service = None
        self.folder_id = None

    def validate_configuration(self) -> bool:
        """
        Validate that Google Docs API is properly configured.

        Returns:
            bool: True if configuration is valid, False otherwise
        """
        try:
            # Check for credentials file
            creds_file = Path('credentials.json')
            if not creds_file.exists():
                logger.error("credentials.json not found. Please download OAuth2 credentials from Google Cloud Console.")
                return False

            # Try to authenticate
            if not self._authenticate():
                logger.error("Failed to authenticate with Google API")
                return False

            # If folder is specified, try to find it
            if self.gdocs_folder:
                self.folder_id = self._find_or_create_folder(self.gdocs_folder)
                if not self.folder_id:
                    logger.error(f"Failed to find or create folder: {self.gdocs_folder}")
                    return False

            return True
        except Exception as e:
            logger.error(f"Failed to validate Google Docs configuration: {str(e)}")
            return False

    def export(self, title: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Create a new document in Google Docs.

        Args:
            title (str): The title of the document
            content (str): The content of the document (markdown format)
            metadata (Dict[str, Any], optional): Additional metadata to include

        Returns:
            bool: True if document was created successfully, False otherwise
        """
        try:
            if not self.docs_service or not self.drive_service:
                if not self._authenticate():
                    logger.error("Failed to authenticate with Google API")
                    return False

            # Create the document
            document = {
                'title': title
            }

            # Create document in Google Docs
            doc_result = self.docs_service.documents().create(body=document).execute()
            document_id = doc_result.get('documentId')

            # Convert markdown to Google Docs format and insert content
            if not self._insert_content(document_id, content, metadata):
                logger.error(f"Failed to insert content into document: {title}")
                return False

            # Move to specified folder if provided
            if self.folder_id:
                if not self._move_to_folder(document_id, self.folder_id):
                    logger.warning(f"Created document but failed to move to folder: {title}")

            logger.info(f"Successfully created Google Doc: {title}")
            return True

        except HttpError as e:
            logger.error(f"Google API error creating document '{title}': {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error creating Google Doc '{title}': {str(e)}")
            return False

    def _authenticate(self) -> bool:
        """
        Authenticate with Google API using OAuth2.

        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            creds = None
            token_file = Path('token.pickle')

            # Load existing credentials
            if token_file.exists():
                with open(token_file, 'rb') as token:
                    creds = pickle.load(token)

            # If there are no valid credentials, request authorization
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                
                # Save credentials for future use
                with open(token_file, 'wb') as token:
                    pickle.dump(creds, token)

            self.credentials = creds
            self.docs_service = build('docs', 'v1', credentials=creds)
            self.drive_service = build('drive', 'v3', credentials=creds)
            return True

        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            return False

    def _insert_content(self, document_id: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Insert formatted content into the Google Doc.

        Args:
            document_id (str): The ID of the Google Doc
            content (str): Markdown content to insert
            metadata (Dict[str, Any], optional): Metadata to include

        Returns:
            bool: True if content insertion successful, False otherwise
        """
        try:
            requests = []

            # Insert metadata if provided
            if metadata:
                metadata_text = self._format_metadata(metadata)
                requests.append({
                    'insertText': {
                        'location': {'index': 1},
                        'text': metadata_text + '\n\n'
                    }
                })

            # Convert markdown to plain text for now (rich formatting can be added later)
            # For now, we'll insert the markdown as plain text
            plain_content = self._convert_markdown_to_text(content)
            
            requests.append({
                'insertText': {
                    'location': {'index': 1},
                    'text': plain_content
                }
            })

            # Execute the batch update
            if requests:
                self.docs_service.documents().batchUpdate(
                    documentId=document_id,
                    body={'requests': requests}
                ).execute()

            return True

        except Exception as e:
            logger.error(f"Failed to insert content: {str(e)}")
            return False

    def _convert_markdown_to_text(self, md_content: str) -> str:
        """
        Convert markdown content to plain text.
        
        Args:
            md_content: Markdown content string
            
        Returns:
            str: Plain text content
        """
        if not md_content:
            return ""
            
        # For now, convert markdown to HTML then extract text
        # This is a simple implementation - could be enhanced for better formatting
        html = markdown.markdown(md_content)
        
        # Simple HTML tag removal (basic implementation)
        import re
        text = re.sub(r'<[^>]+>', '', html)
        
        # Decode HTML entities
        import html as html_module
        text = html_module.unescape(text)
        
        return text

    def _format_metadata(self, metadata: Dict[str, Any]) -> str:
        """
        Format metadata as human-readable text.
        
        Args:
            metadata: Dictionary of metadata to format
            
        Returns:
            str: Formatted metadata string
        """
        if not metadata:
            return ""
            
        formatted_lines = ["📄 File Info:"]
        
        # Format specific metadata fields
        if "filename" in metadata:
            formatted_lines.append(f"• Filename: {metadata['filename']}")
        
        if "filepath" in metadata:
            formatted_lines.append(f"• File Path: {metadata['filepath']}")
            
        if "modified_time" in metadata:
            formatted_lines.append(f"• Modified: {metadata['modified_time']}")
        
        if "size" in metadata:
            size_kb = metadata['size'] / 1024
            if size_kb < 1:
                size_str = f"{metadata['size']} bytes"
            else:
                size_str = f"{size_kb:.1f} KB"
            formatted_lines.append(f"• Size: {size_str}")
            
        # Add any other metadata fields
        handled_fields = {"filename", "filepath", "modified_time", "created_time", "size"}
        for key, value in metadata.items():
            if key not in handled_fields:
                formatted_lines.append(f"• {key.replace('_', ' ').title()}: {value}")
        
        return "\n".join(formatted_lines)

    def _find_or_create_folder(self, folder_name: str) -> Optional[str]:
        """
        Find or create a folder in Google Drive.

        Args:
            folder_name (str): Name of the folder

        Returns:
            str: Folder ID if successful, None otherwise
        """
        try:
            # Search for existing folder
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
            results = self.drive_service.files().list(q=query).execute()
            items = results.get('files', [])

            if items:
                return items[0]['id']

            # Create folder if it doesn't exist
            folder_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = self.drive_service.files().create(body=folder_metadata).execute()
            return folder.get('id')

        except Exception as e:
            logger.error(f"Failed to find or create folder '{folder_name}': {str(e)}")
            return None

    def _move_to_folder(self, file_id: str, folder_id: str) -> bool:
        """
        Move a file to a specific folder in Google Drive.

        Args:
            file_id (str): ID of the file to move
            folder_id (str): ID of the target folder

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Get the file's current parents
            file = self.drive_service.files().get(fileId=file_id, fields='parents').execute()
            previous_parents = ','.join(file.get('parents'))

            # Move the file to the new folder
            self.drive_service.files().update(
                fileId=file_id,
                addParents=folder_id,
                removeParents=previous_parents,
                fields='id, parents'
            ).execute()

            return True

        except Exception as e:
            logger.error(f"Failed to move file to folder: {str(e)}")
            return False