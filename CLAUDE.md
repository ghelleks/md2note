# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Context

You are a senior software engineer and an expert in Python and AppleScript working on **md2note**, a Python application that converts Markdown files to either Apple Notes (via AppleScript) or Google Docs (via Google API).

### Key Project Files
- `docs/project-requirements.md` - Canonical requirements for this project. All work must comply with these instructions.
- `TODO.md` - Project plan with completion status (✅ complete, ⌛️ in process, unmarked = todo). Always update when steps are completed.
- `README.md` - User-facing documentation and setup instructions.

## Development Commands

### Testing
```bash
# Run all tests with coverage
python -m pytest tests/ -v --cov=src

# Run specific test file
python -m pytest tests/test_google_docs_exporter.py -v

# Run integration tests only
python -m pytest tests/test_integration.py tests/test_integration_gdocs.py -v
```

### Running the Application
```bash
# Apple Notes export (default)
python src/md2note.py --source /path/to/markdown/files

# Google Docs export
python src/md2note.py --source /path/to/markdown/files --export-to google_docs

# Google Docs with specific folder
python src/md2note.py --source /path/to/markdown/files --export-to google_docs --gdocs-folder "My Documents"
```

### Package Management
```bash
# Install dependencies
pip install -r requirements.txt

# Build package
python setup.py sdist bdist_wheel
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

### Google Docs Integration
- Requires OAuth2 credentials (`credentials.json` in project root)
- Uses Google Docs API and Google Drive API
- Supports folder organization in Google Drive
- Handles markdown to rich text conversion
- Stores authentication tokens in `token.pickle`

### Testing Strategy
- Unit tests for all individual components
- Integration tests for end-to-end workflows
- Mocked external dependencies (AppleScript, Google API)
- Test coverage target: >80%
- Separate integration tests for Google Docs workflows

### Error Handling
- Comprehensive logging to both console and `md2note.log`
- Graceful degradation on individual file failures
- User prompts for authentication issues
- Validation of exporter configurations before processing