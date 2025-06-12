"""
MD2Note - Convert markdown files to Apple Notes
"""

import os
from pathlib import Path
from typing import List, Optional


class DirectoryScanner:
    """Handles scanning directories for markdown files."""

    def __init__(self, directory: str):
        """
        Initialize the directory scanner.

        Args:
            directory (str): Path to the directory to scan
        """
        self.directory = Path(directory)
        if not self.directory.exists():
            raise ValueError(f"Directory does not exist: {directory}")
        if not self.directory.is_dir():
            raise ValueError(f"Path is not a directory: {directory}")

    def scan_for_markdown(self) -> List[Path]:
        """
        Scan the directory for markdown files.

        Returns:
            List[Path]: List of paths to markdown files
        """
        markdown_files = []
        for file_path in self.directory.glob("**/*.md"):
            if file_path.is_file():
                markdown_files.append(file_path)
        return markdown_files

    def get_file_count(self) -> int:
        """
        Get the total number of markdown files in the directory.

        Returns:
            int: Number of markdown files
        """
        return len(self.scan_for_markdown())
