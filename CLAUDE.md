# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This is a Python application that converts Markdown files to either Apple Notes (via AppleScript) or Google Docs (via Google API). The application processes directories of markdown files, preserves metadata and formatting, and moves successfully processed files to a clean directory.

## Essential Commands

### Development Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

### Testing
```bash
# Run all tests with coverage
python -m pytest tests/ -v --cov=src

# Run specific test file
python -m pytest tests/test_google_docs_exporter.py -v

# Run integration tests only
python -m pytest tests/test_integration.py tests/test_integration_gdocs.py -v

# Run single test
pytest tests/test_applescript.py::TestAppleNotesCreator::test_create_note_success -v
```

### Running the Application
```bash
# Apple Notes export (default)
python src/md2note.py --source /path/to/markdown/files

# Google Docs export
python src/md2note.py --source /path/to/markdown/files --export-to google_docs

# Google Docs with specific folder
python src/md2note.py --source /path/to/markdown/files --export-to google_docs --gdocs-folder "My Documents"

# With custom clean directory
python src/md2note.py --source /path/to/markdown/files --clean /path/to/clean

# Using installed console script
md2note --source /path/to/markdown/files
```

### Packaging
```bash
# Build distribution package
python setup.py sdist bdist_wheel

# Install from local package
pip install dist/md2note-0.1.0-py3-none-any.whl
```

## Architecture Overview

### Strategy Pattern for Export Destinations
The codebase uses a strategy pattern to support multiple export destinations:

- `DocumentExporter` (abstract base class) - Defines the export interface
- `AppleNotesExporter` - Implements Apple Notes export via AppleScript
- `GoogleDocsExporter` - Implements Google Docs export via Google API
- `ExporterFactory` - Creates appropriate exporter instances

### Core Application Flow
1. `MD2Note` class orchestrates the entire process
2. `DirectoryScanner` finds markdown files recursively  
3. `MarkdownMetadataExtractor` parses YAML front matter and file content
4. Appropriate `DocumentExporter` handles the export
5. `FileMover` moves successfully processed files to clean directory

### Key Components
- `src/app.py` - Main `MD2Note` application class with dependency injection support
- `src/exporters.py` - Abstract base class and factory for export strategies
- `src/apple_notes_exporter.py` - AppleScript integration for Apple Notes
- `src/google_docs_exporter.py` - Google API integration with OAuth2 authentication
- `src/metadata.py` - Markdown parsing with YAML front matter extraction
- `src/directory_scanner.py` - Recursive file discovery
- `src/file_mover.py` - File management after successful processing
- `src/md2note.py` - CLI entry point with argument parsing

### Key Design Patterns
- **Dependency Injection**: All components can be injected into `MD2Note` for testing
- **Strategy Pattern**: Export destinations are pluggable via abstract interface
- **Error Handling**: Each component handles errors gracefully and logs appropriately
- **Metadata Prioritization**: YAML frontmatter takes precedence over file system metadata

## Google Docs Integration
- Requires OAuth2 credentials (`credentials.json` in project root)
- Uses Google Docs API and Google Drive API
- Supports folder organization in Google Drive
- Handles markdown to rich text conversion
- Stores authentication tokens in `token.pickle`

## Project Management Files
- **`docs/project-requirements.md`**: Canonical requirements document - all changes must comply
- **`TODO.md`**: Project plan with completion status (✅ = complete, ⌛️ = in progress)
- **`README.md`**: User-facing documentation for installation and usage

Always update `TODO.md` when completing tasks and ensure compliance with `docs/project-requirements.md`.

## AppleScript Integration Notes
The AppleScript integration creates notes with preserved formatting. Test AppleScript functionality carefully as it requires macOS and Apple Notes to be available. Mock AppleScript calls in unit tests using the provided test framework.

## Testing Strategy
- Unit tests for all individual components with mocked dependencies
- Integration tests for end-to-end workflows
- Mocked external dependencies (AppleScript, Google API)
- Test coverage target: >80%
- Separate integration tests for Google Docs workflows

## Error Handling
- Comprehensive logging to both console and `md2note.log`
- Graceful degradation on individual file failures
- User prompts for authentication issues
- Validation of exporter configurations before processing