# MD2Note - Markdown to Apple Notes & Google Docs Converter

A Python application that converts Markdown files to Apple Notes or Google Docs, preserving formatting and metadata.

## Features

- Converts Markdown files to Apple Notes or Google Docs
- Preserves formatting and metadata
- Handles nested directory structures
- Supports special characters and Unicode
- Google Drive folder organization
- OAuth2 authentication for Google Docs
- Comprehensive error handling and logging
- Command-line interface for easy automation

## Requirements

- Python 3.9 or higher
- macOS (for Apple Notes integration)
- AppleScript support (for Apple Notes export)
- Google Cloud project with Docs API enabled (for Google Docs export)
- OAuth2 credentials (for Google Docs export)

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

### Apple Notes (Default)
```bash
python src/md2note.py --source /path/to/markdown/files
```

### Google Docs Export
```bash
python src/md2note.py --source /path/to/markdown/files --export-to google_docs
```

### Google Docs with Custom Folder
```bash
python src/md2note.py --source /path/to/markdown/files --export-to google_docs --gdocs-folder "My Documents"
```

### Custom Clean Directory
```bash
python src/md2note.py --source /path/to/markdown/files --clean /path/to/clean/directory
```

## Google Docs Setup

For Google Docs export, you need to:

1. **Create a Google Cloud Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one

2. **Enable APIs**
   - Enable Google Docs API
   - Enable Google Drive API

3. **Create OAuth2 Credentials**
   - Go to APIs & Services > Credentials
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop application"
   - Download the credentials as `credentials.json`
   - Place `credentials.json` in the project root directory

4. **First Run Authentication**
   - On first run, the application will open a browser for OAuth2 consent
   - Grant permissions for Google Docs and Drive access
   - Credentials will be saved to `token.pickle` for future use

## Project Structure

```
md2note/
├── src/
│   ├── md2note.py                 # Main application entry point
│   ├── app.py                     # Application orchestration
│   ├── exporters.py               # Export strategy pattern base
│   ├── apple_notes_exporter.py    # Apple Notes integration
│   ├── google_docs_exporter.py    # Google Docs integration
│   ├── applescript.py             # Legacy AppleScript integration
│   ├── file_mover.py              # File management
│   ├── metadata.py                # Markdown processing
│   └── directory_scanner.py       # File scanning
├── tests/
│   ├── test_main.py
│   ├── test_exporters.py
│   ├── test_apple_notes_exporter.py
│   ├── test_google_docs_exporter.py
│   ├── test_integration_gdocs.py
│   ├── test_applescript.py
│   ├── test_file_mover.py
│   ├── test_metadata_extractor.py
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