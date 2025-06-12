# MD2Note - Markdown to Apple Notes Converter

A Python application that converts Markdown files to Apple Notes, preserving formatting and metadata.

## Features

- Converts Markdown files to Apple Notes
- Preserves formatting and metadata
- Handles nested directory structures
- Supports special characters and Unicode
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

Basic usage:
```bash
python src/main.py /path/to/markdown/files
```

With custom clean directory:
```bash
python src/main.py /path/to/markdown/files /path/to/clean/directory
```

## Project Structure

```
md2note/
├── src/
│   ├── main.py           # Main application entry point
│   ├── applescript.py    # AppleScript integration
│   ├── file_mover.py     # File management
│   └── markdown.py       # Markdown processing
├── tests/
│   ├── test_main.py
│   ├── test_applescript.py
│   ├── test_file_mover.py
│   ├── test_markdown.py
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