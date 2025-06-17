"""
Abstract base class and implementations for document exporters.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class DocumentExporter(ABC):
    """Abstract base class for document exporters."""

    @abstractmethod
    def export(self, title: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Export a document to the target destination.

        Args:
            title (str): The title of the document
            content (str): The content of the document (markdown format)
            metadata (Dict[str, Any], optional): Additional metadata to include

        Returns:
            bool: True if export was successful, False otherwise
        """
        pass

    @abstractmethod
    def validate_configuration(self) -> bool:
        """
        Validate that the exporter is properly configured.

        Returns:
            bool: True if configuration is valid, False otherwise
        """
        pass


class ExporterFactory:
    """Factory class for creating document exporters."""

    @staticmethod
    def create_exporter(export_type: str, **kwargs) -> DocumentExporter:
        """
        Create an exporter instance based on the export type.

        Args:
            export_type (str): Type of exporter ('apple_notes' or 'google_docs')
            **kwargs: Additional arguments for exporter configuration

        Returns:
            DocumentExporter: An instance of the appropriate exporter

        Raises:
            ValueError: If export_type is not supported
        """
        if export_type == "apple_notes":
            from .apple_notes_exporter import AppleNotesExporter
            return AppleNotesExporter()
        elif export_type == "google_docs":
            from .google_docs_exporter import GoogleDocsExporter
            gdocs_folder = kwargs.get('gdocs_folder')
            return GoogleDocsExporter(gdocs_folder=gdocs_folder)
        else:
            raise ValueError(f"Unsupported export type: {export_type}")