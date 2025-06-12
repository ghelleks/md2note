import logging
import sys
from pathlib import Path
from typing import Optional, Any

from src.md2note import DirectoryScanner
from src.applescript import AppleNotesCreator
from src.metadata import MarkdownMetadataExtractor
from src.file_mover import FileMover

class MD2Note:
    """Main application class for converting Markdown files to Apple Notes."""
    def __init__(
        self,
        source_dir: str,
        clean_dir: Optional[str] = None,
        directory_scanner: Optional[Any] = None,
        apple_script: Optional[Any] = None,
        file_processor: Optional[Any] = None,
        file_mover: Optional[Any] = None,
    ):
        self.source_dir = Path(source_dir)
        self.clean_dir = Path(clean_dir) if clean_dir else self.source_dir / "clean"
        self.directory_scanner = directory_scanner or DirectoryScanner(self.source_dir)
        self.apple_script = apple_script or AppleNotesCreator()
        self.file_processor = file_processor or MarkdownMetadataExtractor
        self.file_mover = file_mover or FileMover(self.source_dir, self.clean_dir)
        self._setup_logging()

    def _setup_logging(self) -> None:
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
        try:
            self.logger.info(f"Processing file: {file_path}")
            processor = self.file_processor(str(file_path))
            content = processor.get_content()
            metadata = processor.extract()
            if not content:
                self.logger.error(f"Failed to process file: {file_path}")
                return False
            note_created = self.apple_script.create_note(metadata.get('title', file_path.stem), content, metadata)
            if not note_created:
                self.logger.error(f"Failed to create note for file: {file_path}")
                return False
            self.file_mover.move_file(file_path)
            self.logger.info(f"Successfully processed file: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error processing file {file_path}: {str(e)}")
            return False

    def run(self) -> None:
        try:
            self.logger.info(f"Starting conversion process from {self.source_dir}")
            markdown_files = self.directory_scanner.scan_for_markdown()
            if not markdown_files:
                self.logger.warning("No Markdown files found in the source directory")
                return
            self.logger.info(f"Found {len(markdown_files)} Markdown files")
            successful = 0
            failed = 0
            for file_path in markdown_files:
                if self.process_file(file_path):
                    successful += 1
                else:
                    failed += 1
            self.logger.info(f"Conversion complete. Successful: {successful}, Failed: {failed}")
        except Exception as e:
            self.logger.error(f"Error during conversion process: {str(e)}")
            raise 