# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This is a Python application that converts Markdown files to Apple Notes using AppleScript integration. The application processes directories of markdown files, preserves metadata and formatting, and moves successfully processed files to a clean directory.

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
pytest -v --cov=src

# Run specific test file
pytest tests/test_integration.py -v

# Run single test
pytest tests/test_applescript.py::TestAppleNotesCreator::test_create_note_success -v
```

### Running the Application
```bash
# Basic usage
python src/md2note.py --source /path/to/markdown/files

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

The application follows a modular architecture with dependency injection for testability:

- **`src/app.py`**: Main application orchestrator (`MD2Note` class) that coordinates all components
- **`src/directory_scanner.py`**: Scans directories for markdown files recursively
- **`src/metadata.py`**: Extracts metadata from markdown files (YAML frontmatter + file properties)
- **`src/applescript.py`**: Interfaces with Apple Notes via AppleScript to create notes
- **`src/file_mover.py`**: Handles moving processed files to clean directory
- **`src/md2note.py`**: CLI entry point with argument parsing

### Key Design Patterns
- **Dependency Injection**: All components can be injected into `MD2Note` for testing
- **Error Handling**: Each component handles errors gracefully and logs appropriately
- **Metadata Prioritization**: YAML frontmatter takes precedence over file system metadata

## Project Management Files
- **`docs/project-requirements.md`**: Canonical requirements document - all changes must comply
- **`TODO.md`**: Project plan with completion status (✅ = complete, ⌛️ = in progress)
- **`README.md`**: User-facing documentation for installation and usage

Always update `TODO.md` when completing tasks and ensure compliance with `docs/project-requirements.md`.

## AppleScript Integration Notes
The AppleScript integration creates notes with preserved formatting. Test AppleScript functionality carefully as it requires macOS and Apple Notes to be available. Mock AppleScript calls in unit tests using the provided test framework.

## Testing Strategy
- Unit tests for individual components with mocked dependencies
- Integration tests for end-to-end workflows
- AppleScript calls are mocked in unit tests but tested in integration scenarios
- Target >80% test coverage as specified in project requirements