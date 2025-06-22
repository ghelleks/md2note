# Command Line Interface Documentation

## Overview
The Markdown to Apple Notes Converter provides a command-line interface for converting Markdown files to Apple Notes. The interface is designed to be simple and intuitive, with clear error messages and logging.

## Usage

```bash
python md2note.py --source /path/to/markdown/files [--clean /path/to/clean/directory] [--folder "folder_name" | --auto-folder]
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

### Folder Organization Arguments (Mutually Exclusive)

- `--folder "folder_name"`: Specify a custom folder name in Apple Notes
  - Creates the folder if it doesn't exist
  - All imported notes will be placed in this folder
  - Supports spaces and special characters (properly escaped)
  - Example: `--folder "My Import Batch"`

- `--auto-folder`: Auto-generate a unique folder name for this import batch
  - Uses format: `md2note-YYYYMMDD-HHMMSS`
  - Perfect for batch recovery scenarios
  - Each import session gets a unique folder
  - Example generated name: `md2note-20250622-143022`

**Note**: `--folder` and `--auto-folder` cannot be used together. If neither is specified, notes will be placed in the default Notes folder.

## Examples

### Basic Usage

1. Basic usage with default clean directory:
```bash
python md2note.py --source ~/Documents/notes
```

2. Specify custom clean directory:
```bash
python md2note.py --source ~/Documents/notes --clean ~/Documents/processed
```

### Folder Organization Examples

3. Import notes into a custom folder:
```bash
python md2note.py --source ~/Documents/notes --folder "Meeting Notes"
```

4. Auto-generate unique folder for batch recovery:
```bash
python md2note.py --source ~/Downloads/markdown --auto-folder
```

5. Complete example with custom folder and clean directory:
```bash
python md2note.py --source ~/Documents/markdown --folder "Blog Posts" --clean ~/Documents/processed
```

6. Batch import with auto-folder and custom clean location:
```bash
python md2note.py --source ~/Downloads/notes --auto-folder --clean ~/Documents/imported
```

### Use Case Examples

**For regular imports with organization:**
```bash
python md2note.py --source ~/Documents/work-notes --folder "Work Notes 2025"
```

**For experimental/risky imports (easy to delete if needed):**
```bash
python md2note.py --source ~/Downloads/unknown-quality --auto-folder
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

4. Folder creation errors:
   - Handles folder creation failures gracefully
   - Falls back to default Notes folder if needed
   - Logs folder-related errors for debugging

## Exit Codes

- `0`: Successful execution
- `1`: Error occurred during execution

## Best Practices

1. Always backup your Markdown files before processing
2. Test with a small set of files first
3. Check the log file for detailed information
4. Use absolute paths to avoid confusion

### Folder Organization Best Practices

5. Use `--auto-folder` for experimental imports:
   - Easy to identify and delete if import fails
   - Unique folder names prevent conflicts
   - Perfect for testing unknown markdown quality

6. Use `--folder` for regular organized imports:
   - Group related content logically
   - Use descriptive folder names
   - Consider date-based naming for ongoing projects

7. Folder naming conventions:
   - Use quotes for folder names with spaces: `--folder "Meeting Notes"`
   - Be descriptive: `--folder "Project Alpha Documentation"`
   - Consider including dates: `--folder "Blog Posts 2025"` 