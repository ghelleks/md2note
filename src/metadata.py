import frontmatter
from pathlib import Path
from typing import Any, Dict, Optional
import datetime
import os

class MarkdownMetadataExtractor:
    """
    Extracts metadata from markdown files, preferring YAML front matter,
    and falling back to file properties if not present.
    """
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists() or not self.file_path.is_file():
            raise ValueError(f"File does not exist: {file_path}")
        self._post = None

    def extract(self) -> Dict[str, Any]:
        """
        Extract metadata from the markdown file.
        Returns:
            dict: Metadata dictionary combining frontmatter and file properties
        """
        # Start with file properties as base
        metadata = self._extract_file_properties()
        
        # Merge frontmatter metadata, allowing it to override file properties
        frontmatter_metadata = self._extract_frontmatter()
        if frontmatter_metadata:
            metadata.update(frontmatter_metadata)
            
        return metadata

    def _extract_frontmatter(self) -> Optional[Dict[str, Any]]:
        try:
            post = frontmatter.load(self.file_path)
            self._post = post
            if post.metadata:
                return dict(post.metadata)
        except Exception:
            pass
        return None

    def _extract_file_properties(self) -> Dict[str, Any]:
        stat = self.file_path.stat()
        return {
            "filename": self.file_path.name,
            "filepath": str(self.file_path.resolve()),
            "modified_time": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "created_time": datetime.datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "size": stat.st_size,
        }

    def get_content(self) -> str:
        """
        Get the markdown content (without front matter if present).
        Returns:
            str: Markdown content
        """
        if self._post is None:
            try:
                self._post = frontmatter.load(self.file_path)
            except Exception:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return f.read()
        return self._post.content if self._post else ""

    def get_title(self) -> str:
        """
        Extract title from markdown content or filename.
        Prioritizes H1 headers, falls back to filename without extension.
        Returns:
            str: Note title
        """
        content = self.get_content()
        
        # Look for H1 header at start of content
        lines = content.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('# '):
                return line[2:].strip()
            elif line and not line.startswith('#'):
                # Stop at first non-header content
                break
        
        # Fall back to filename without extension
        return self.file_path.stem 