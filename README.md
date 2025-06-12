# Markdown to Apple Notes Converter

A Python application that converts Markdown files to Apple Notes, preserving formatting and structure.

## Features

- Scans directories for Markdown files
- Converts Markdown to Apple Notes format
- Preserves formatting and structure
- Handles metadata and frontmatter
- Moves processed files to a clean directory while preserving structure
- Comprehensive error handling and logging

## Project Status

The project is currently in active development. The following components have been implemented:

- ✅ Directory scanning functionality
- ✅ AppleScript integration for note creation
- ✅ Markdown to note conversion
- ✅ File movement with structure preservation
- 🔄 Main application (in progress)
- ⏳ Integration testing
- ⏳ Performance optimization
- ⏳ User experience improvements

## Requirements

- Python 3.9+
- macOS (for AppleScript integration)
- Apple Notes application

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/md2note.git
cd md2note
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

The application is currently in development. Once completed, it will be used as follows:

```bash
python src/main.py --source /path/to/markdown/files
```

## Development

### Project Structure

```
md2note/
├── src/
│   ├── directory_scanner.py
│   ├── apple_script_handler.py
│   ├── file_processor.py
│   ├── file_mover.py
│   └── main.py
├── tests/
│   ├── test_directory_scanner.py
│   ├── test_apple_script_handler.py
│   ├── test_file_processor.py
│   └── test_file_mover.py
├── docs/
│   ├── implementation-status.md
│   └── api-documentation.md
├── requirements.txt
└── README.md
```

### Running Tests

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

- AppleScript documentation
- Python Markdown libraries
- Apple Notes API 