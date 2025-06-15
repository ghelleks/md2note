"""
Main application class for the Markdown to Apple Notes converter.
"""
import logging
from pathlib import Path
from typing import Optional

from .directory_scanner import DirectoryScanner
from .applescript import AppleNotesCreator
from .file_mover import FileMover
from .metadata import MarkdownMetadataExtractor
from .exporters import ExporterFactory

class MD2Note:
    """Main application class for converting markdown files to Apple Notes."""

    def __init__(
        self,
        source_dir: str,
        clean_dir: Optional[str] = None,
        export_type: str = "apple_notes",
        gdocs_folder: Optional[str] = None,
        directory_scanner=None,
        exporter=None,
        file_processor=None,
        file_mover=None
    ):
        """
        Initialize the MD2Note application.

        Args:
            source_dir (str): Directory containing markdown files
            clean_dir (str, optional): Directory to move processed files to
            export_type (str): Export destination type ('apple_notes' or 'google_docs')
            gdocs_folder (str, optional): Google Drive folder for Google Docs export
            directory_scanner: Optional custom directory scanner (for testing)
            exporter: Optional custom exporter (for testing)
            file_processor: Optional custom file processor class (for testing)
            file_mover: Optional custom file mover (for testing)
        """
        self.source_dir = Path(source_dir)
        self.clean_dir = Path(clean_dir) if clean_dir else self.source_dir / "clean"

        # Initialize components (allow dependency injection for testing)
        self.scanner = directory_scanner or DirectoryScanner(str(self.source_dir))
        self.exporter = exporter or ExporterFactory.create_exporter(export_type, gdocs_folder=gdocs_folder)
        self.file_processor = file_processor or MarkdownMetadataExtractor
        self.file_mover = file_mover or FileMover(str(self.source_dir), str(self.clean_dir))

        # Set up logging
        self._setup_logging()

    def _setup_logging(self) -> None:
        """Set up logging configuration."""
        self.logger = logging.getLogger("src.app")
        self.logger.setLevel(logging.INFO)
        
        # Create a file handler
        log_file = Path("md2note.log")
        log_file.touch(exist_ok=True)  # Create the log file if it doesn't exist
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create a formatter and add it to the handlers
        formatter = logging.Formatter('%(levelname)-8s %(name)s:%(lineno)d %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # Print the handlers attached to the logger
        print("Handlers attached to logger:", self.logger.handlers)
        
        # Force a flush on each handler
        for handler in self.logger.handlers:
            handler.flush()

    def process_file(self, file_path: Path) -> bool:
        """Process a single markdown file."""
        try:
            processor = self.file_processor(str(file_path))
            content = processor.get_content()
            metadata = processor.extract()
            title = processor.get_title()
            if self.exporter.export(title, content, metadata):
                self.file_mover.move_file(file_path)
                self.logger.info(f"Successfully processed {file_path}")
                return True
            else:
                self.logger.error(f"Failed to export document for {file_path}")
                return False
        except Exception as e:
            self.logger.error(f"Error processing {file_path}: {str(e)}")
            return False

    def run(self) -> None:
        """Run the markdown to document conversion process."""
        try:
            self.logger.info("Starting conversion process")
            
            # Validate exporter configuration
            if not self.exporter.validate_configuration():
                self.logger.error("Exporter configuration validation failed")
                raise RuntimeError("Exporter not properly configured")
            
            # Create clean directory if it doesn't exist
            self.clean_dir.mkdir(parents=True, exist_ok=True)

            # Get list of markdown files
            markdown_files = self.scanner.scan_for_markdown()
            total_files = len(markdown_files)

            if total_files == 0:
                self.logger.warning(f"No markdown files found in {self.source_dir}")
                return

            self.logger.info(f"Found {total_files} markdown files to process")

            # Process each file
            successful = 0
            failed = 0

            for file_path in markdown_files:
                if self.process_file(file_path):
                    successful += 1
                else:
                    failed += 1

            # Log summary
            self.logger.info(f"Processing complete. {successful} files processed successfully, {failed} failed.")

        except Exception as e:
            self.logger.error(f"Application error: {str(e)}")
            raise 