import os
import tempfile
import time
import pytest
from pathlib import Path
from src.metadata import MarkdownMetadataExtractor

def create_markdown_file(tmpdir, content: str, filename: str = "test.md") -> Path:
    file_path = tmpdir / filename
    file_path.write_text(content, encoding="utf-8")
    return file_path

def test_extract_with_yaml_frontmatter(tmp_path):
    md_content = """---
title: Test Title
author: Test Author
tags:
  - tag1
  - tag2
---

# Heading
Some content here.
"""
    file_path = create_markdown_file(tmp_path, md_content)
    extractor = MarkdownMetadataExtractor(str(file_path))
    metadata = extractor.extract()
    assert metadata["title"] == "Test Title"
    assert metadata["author"] == "Test Author"
    assert metadata["tags"] == ["tag1", "tag2"]
    content = extractor.get_content()
    assert "# Heading" in content
    assert "Test Title" not in content  # front matter should be stripped

def test_extract_without_yaml_frontmatter(tmp_path):
    md_content = "# No Front Matter\nJust some content."
    file_path = create_markdown_file(tmp_path, md_content, "nofront.md")
    extractor = MarkdownMetadataExtractor(str(file_path))
    metadata = extractor.extract()
    assert metadata["filename"] == "nofront.md"
    assert "modified_time" in metadata
    assert "created_time" in metadata
    assert "size" in metadata
    content = extractor.get_content()
    assert "Just some content." in content

def test_invalid_file_raises():
    with pytest.raises(ValueError):
        MarkdownMetadataExtractor("/nonexistent/file.md")

def test_extract_with_empty_file(tmp_path):
    file_path = create_markdown_file(tmp_path, "", "empty.md")
    extractor = MarkdownMetadataExtractor(str(file_path))
    metadata = extractor.extract()
    assert metadata["filename"] == "empty.md"
    content = extractor.get_content()
    assert content == ""

def test_get_title_from_h1_header(tmp_path):
    md_content = "# My Great Title\n\nSome content here."
    file_path = create_markdown_file(tmp_path, md_content, "titled.md")
    extractor = MarkdownMetadataExtractor(str(file_path))
    title = extractor.get_title()
    assert title == "My Great Title"

def test_get_title_from_filename_fallback(tmp_path):
    md_content = "Some content without h1 header."
    file_path = create_markdown_file(tmp_path, md_content, "my-great-file.md")
    extractor = MarkdownMetadataExtractor(str(file_path))
    title = extractor.get_title()
    assert title == "my-great-file"

def test_get_title_ignores_non_h1_headers(tmp_path):
    md_content = "## This is H2\n\n### This is H3\n\nContent here."
    file_path = create_markdown_file(tmp_path, md_content, "headers.md")
    extractor = MarkdownMetadataExtractor(str(file_path))
    title = extractor.get_title()
    assert title == "headers" 