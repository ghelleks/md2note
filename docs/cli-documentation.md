# Command Line Interface Documentation

## Overview
The Markdown to Apple Notes Converter provides a command-line interface for converting Markdown files to Apple Notes. The interface is designed to be simple and intuitive, with clear error messages and logging.

## Usage

```bash
python src/main.py --source /path/to/markdown/files [--clean /path/to/clean/directory]
```

## Arguments

### Required Arguments

- `--source`: Path to the directory containing Markdown files to be converted
  - Must be a valid directory path
  - Will be scanned recursively for `.md` files

### Optional Arguments

- `--clean`: Path to the directory where processed files will be moved
  - If not specified, defaults to `source/clean`
  - Will be created if it doesn't exist
  - Preserves the original directory structure

## Examples

1. Basic usage with default clean directory:
```bash
python src/main.py --source ~/Documents/notes
```

2. Specify custom clean directory:
```bash
python src/main.py --source ~/Documents/notes --clean ~/Documents/processed
```

## Output

The application provides the following output:

1. Console output:
   - Progress information
   - Success/failure messages
   - Error messages if something goes wrong

2. Log file (`md2note.log`):
   - Detailed logging of all operations
   - Timestamps for each operation
   - Error details and stack traces if applicable

## Error Handling

The CLI handles various error conditions:

1. Invalid source directory:
   - Checks if directory exists
   - Verifies read permissions
   - Provides clear error messages

2. Invalid clean directory:
   - Attempts to create if missing
   - Verifies write permissions
   - Provides clear error messages

3. File processing errors:
   - Logs detailed error information
   - Continues processing other files
   - Reports success/failure counts

## Exit Codes

- `0`: Successful execution
- `1`: Error occurred during execution

## Best Practices

1. Always backup your Markdown files before processing
2. Test with a small set of files first
3. Check the log file for detailed information
4. Use absolute paths to avoid confusion 