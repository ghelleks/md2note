# MD2Note - Markdown to Apple Notes Converter

A Python application that converts Markdown files to Apple Notes, preserving formatting and metadata.

## Features

- Converts Markdown files to Apple Notes
- Preserves formatting and metadata
- Handles nested directory structures
- Supports special characters and Unicode
- **Folder organization** - Place notes in custom or auto-generated folders
- **Batch recovery** - Auto-generated unique folder names for easy import management
- Comprehensive error handling and logging
- Command-line interface for easy automation

## Requirements

- Python 3.9 or higher
- macOS (for Apple Notes integration)
- AppleScript support

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/md2note.git
cd md2note
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Convert markdown files to Apple Notes:
```bash
python md2note.py --source /path/to/markdown/files
```

With custom clean directory:
```bash
python md2note.py --source /path/to/markdown/files --clean /path/to/clean/directory
```

### Folder Organization

Place notes in a custom folder:
```bash
python md2note.py --source /path/to/markdown/files --folder "My Import Batch"
```

Auto-generate unique folder for batch recovery:
```bash
python md2note.py --source /path/to/markdown/files --auto-folder
```

The auto-generated folder uses the format: `md2note-YYYYMMDD-HHMMSS` (e.g., `md2note-20250622-143022`)

### Complete Examples

Import with custom folder and clean directory:
```bash
python md2note.py --source ~/Documents/markdown --folder "Blog Posts" --clean ~/Documents/processed
```

Batch import with auto-generated folder for easy recovery:
```bash
python md2note.py --source ~/Downloads/notes --auto-folder --clean ~/Documents/clean
```

## Folder Organization vs Labels

This application uses Apple Notes' native **folder system** for organization instead of labels/tags. This approach was chosen because:

- **Apple Notes doesn't support tags/labels** via AppleScript
- **Folders provide the same organizational benefits** as labels
- **Native integration** with Apple Notes' built-in folder system
- **Batch recovery** is easy with unique folder names

### Use Cases

**Custom Folders**: Group related imports (e.g., "Blog Posts", "Meeting Notes", "Research")

**Auto-Generated Folders**: Perfect for batch recovery scenarios where you need to:
- Identify and delete a problematic import batch
- Re-import files after fixing formatting issues  
- Keep different import sessions separate and organized

## Project Structure

```
md2note/
├── src/
│   ├── md2note.py        # Main application entry point
│   ├── applescript.py    # AppleScript integration
│   ├── file_mover.py     # File management
│   └── metadata.py       # Markdown processing
├── tests/
│   ├── test_main.py
│   ├── test_applescript.py
│   ├── test_file_mover.py
│   ├── test_metadata.py
│   └── test_integration.py
├── docs/
│   ├── cli-documentation.md
│   └── project-requirements.md
├── requirements.txt
└── README.md
```

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- AppleScript for Notes integration
- Python's pathlib for file handling
- pytest for testing framework 