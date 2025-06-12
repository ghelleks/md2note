#!/usr/bin/env python3
"""
Main application module for the Markdown to Apple Notes converter.
This module provides the command-line interface and coordinates the conversion process.
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional, List

from src.md2note import DirectoryScanner
from src.applescript import AppleNotesCreator
from src.metadata import MarkdownMetadataExtractor
from src.file_mover import FileMover

class MD2Note:
    """Main application class for converting Markdown files to Apple Notes."""
    
    def __init__(self, source_dir: str, clean_dir: Optional[str] = None):
        """
        Initialize the MD2Note application.
        
        Args:
            source_dir: Path to the directory containing Markdown files
            clean_dir: Optional path to the directory for processed files
        """
        self.source_dir = Path(source_dir)
        self.clean_dir = Path(clean_dir) if clean_dir else self.source_dir / "clean"
        
        # Initialize components
        self.directory_scanner = DirectoryScanner(self.source_dir)
        self.apple_script = AppleNotesCreator()
        self.file_processor = MarkdownMetadataExtractor
        self.file_mover = FileMover(self.source_dir, self.clean_dir)
        
        # Set up logging
        self._setup_logging()
    
    def _setup_logging(self) -> None:
        """Configure logging for the application."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('md2note.log')
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def process_file(self, file_path: Path) -> bool:
        """
        Process a single Markdown file.
        
        Args:
            file_path: Path to the Markdown file
            
        Returns:
            bool: True if processing was successful, False otherwise
        """
        try:
            self.logger.info(f"Processing file: {file_path}")
            
            # Process the file
            processor = self.file_processor(str(file_path))
            content = processor.get_content()
            metadata = processor.extract()
            if not content:
                self.logger.error(f"Failed to process file: {file_path}")
                return False
            
            # Create note
            note_created = self.apple_script.create_note(metadata.get('title', file_path.stem), content, metadata)
            if not note_created:
                self.logger.error(f"Failed to create note for file: {file_path}")
                return False
            
            # Move file to clean directory
            self.file_mover.move_file(file_path)
            
            self.logger.info(f"Successfully processed file: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing file {file_path}: {str(e)}")
            return False
    
    def run(self) -> None:
        """Run the main conversion process."""
        try:
            self.logger.info(f"Starting conversion process from {self.source_dir}")
            
            # Scan for Markdown files
            markdown_files = self.directory_scanner.scan_for_markdown()
            if not markdown_files:
                self.logger.warning("No Markdown files found in the source directory")
                return
            
            self.logger.info(f"Found {len(markdown_files)} Markdown files")
            
            # Process each file
            successful = 0
            failed = 0
            
            for file_path in markdown_files:
                if self.process_file(file_path):
                    successful += 1
                else:
                    failed += 1
            
            # Log summary
            self.logger.info(f"Conversion complete. Successful: {successful}, Failed: {failed}")
            
        except Exception as e:
            self.logger.error(f"Error during conversion process: {str(e)}")
            raise

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Convert Markdown files to Apple Notes"
    )
    parser.add_argument(
        "--source",
        required=True,
        help="Source directory containing Markdown files"
    )
    parser.add_argument(
        "--clean",
        help="Directory to move processed files to (default: source/clean)"
    )
    return parser.parse_args()

def main() -> None:
    """Main entry point for the application."""
    args = parse_args()
    
    try:
        app = MD2Note(args.source, args.clean)
        app.run()
    except Exception as e:
        logging.error(f"Application error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 