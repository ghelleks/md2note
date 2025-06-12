"""
File movement functionality for processed markdown files.
"""

import os
import shutil
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class FileMover:
    """Handles moving processed files to a clean directory."""

    def __init__(self, source_dir: str, clean_dir: Optional[str] = None):
        """
        Initialize the FileMover.

        Args:
            source_dir (str): Source directory containing processed files
            clean_dir (str, optional): Directory to move files to. Defaults to 'clean' subdirectory.
        """
        self.source_dir = Path(source_dir)
        if not self.source_dir.exists() or not self.source_dir.is_dir():
            raise ValueError(f"Source directory does not exist: {source_dir}")

        # Set up clean directory
        if clean_dir is None:
            self.clean_dir = self.source_dir / 'clean'
        else:
            self.clean_dir = Path(clean_dir)

        # Create clean directory if it doesn't exist
        self.clean_dir.mkdir(parents=True, exist_ok=True)

    def move_file(self, file_path: str) -> bool:
        """
        Move a processed file to the clean directory.

        Args:
            file_path (str): Path to the file to move

        Returns:
            bool: True if file was moved successfully, False otherwise
        """
        try:
            source_path = Path(file_path)
            if not source_path.exists():
                logger.error(f"File does not exist: {file_path}")
                return False

            # Calculate destination path, preserving subdirectory structure
            rel_path = source_path.relative_to(self.source_dir)
            dest_path = self.clean_dir / rel_path

            # Create parent directories if they don't exist
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            # Move the file
            shutil.move(str(source_path), str(dest_path))
            logger.info(f"Moved {file_path} to {dest_path}")
            return True

        except Exception as e:
            logger.error(f"Error moving file {file_path}: {str(e)}")
            return False

    def get_clean_directory(self) -> Path:
        """
        Get the path to the clean directory.

        Returns:
            Path: Path to the clean directory
        """
        return self.clean_dir 