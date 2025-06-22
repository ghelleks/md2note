# Project Requirements

## 1. Introduction
This project aims to develop a Python application that processes a directory of markdown files, calls AppleScript to create a note in the Apple Notes app for each file, optionally places notes in a user-specified or auto-generated folder for organization, preserves metadata from the file contents or the file itself, and moves successfully processed files to a new directory (default: 'clean'). The application will prompt the user for more information or to quit if any issues arise.

## 2. Stakeholders
- Users who manage markdown files and wish to convert them into Apple Notes
- Developers responsible for implementing the Python application

## 3. Functional Requirements
| ID  | Requirement Description                | Priority (High/Med/Low) | Notes           |
|-----|----------------------------------------|-------------------------|-----------------|
| FR1 | Process a directory of markdown files  | High                    | Must handle multiple files |
| FR2 | Call AppleScript to create a note in Apple Notes for each markdown file | High | Must preserve metadata |
| FR3 | Move successfully processed files to a new directory | High | Default: 'clean' |
| FR4 | Support optional folder organization of imported notes | Medium | User can specify custom folder or use auto-generated unique folder |
| FR5 | Generate unique folders for batch imports when requested | Medium | Facilitates recovery from bad imports |

## 4. Non-Functional Requirements
| ID  | Requirement Description                | Priority (High/Med/Low) | Notes           |
|-----|----------------------------------------|-------------------------|-----------------|
| NFR1| Preserve metadata from markdown files  | High                    | Prioritize metadata from file contents |
| NFR2| Prompt user for more information or to quit if an error occurs | High | Must handle errors gracefully |

## 5. Assumptions and Dependencies
- The Python application has access to the AppleScript environment.
- The markdown files are in a readable format.
- Apple Notes supports folder creation and organization via AppleScript.

## 6. Constraints
- The application must be compatible with the latest version of macOS.
- The application must handle errors without crashing.

## 7. Acceptance Criteria
- The application successfully processes all markdown files in the specified directory.
- Each markdown file is converted into a note in the Apple Notes app via AppleScript.
- Successfully processed files are moved to the 'clean' directory.
- The application prompts the user for more information or to quit if any issues arise.
- The application allows users to specify an optional folder for imported notes.
- When no folder is specified, the application can generate a unique folder for the import batch.
- Folders are properly created and notes are placed in them via AppleScript.

## 8. Out of Scope
- Handling non-markdown files.
- Modifying the content of the markdown files.

## 9. Glossary
| Term | Definition |
|------|------------|
| AppleScript | A scripting language created by Apple Inc. for automating tasks on macOS. |
| Markdown | A lightweight markup language with plain text formatting syntax. |
| Folder | An organizational container in Apple Notes used to group related notes for batch management. |

---

## Implementation Status

### ✅ Completed Features
- **FR1**: Directory processing with recursive scanning
- **FR2**: AppleScript note creation with metadata preservation  
- **FR3**: File movement to clean directory with structure preservation
- **FR4**: Custom folder organization via `--folder` argument ✅ **Phase 2 Complete**
- **FR5**: Auto-generated unique folders via `--auto-folder` argument ✅ **Phase 2 Complete**
- **NFR1**: YAML front matter and file property metadata extraction
- **NFR2**: Comprehensive error handling and user prompting

### 🧪 Testing Status
- **Unit Tests**: 55/55 passing (100% success rate)
- **Code Coverage**: 91% across all modules
- **Integration Tests**: End-to-end workflows validated ✅ **Phase 3 Complete**

### 📚 Documentation Status
- **User Documentation**: README.md updated with folder usage examples ✅ **Phase 4 Complete**
- **CLI Documentation**: Complete argument reference and examples ✅ **Phase 4 Complete**
- **Requirements Documentation**: Updated to reflect implementation status ✅ **Phase 4 Complete**

## Implementation Notes
- Metadata extraction is implemented to prefer YAML front matter, falling back to file properties if not present.
- AppleScript integration is handled via a dedicated Python module that creates notes in Apple Notes, with robust error handling and test coverage.
- Folder functionality supports both user-specified folders and auto-generated unique folder names.
- Auto-generated folders use timestamp-based naming for uniqueness (format: md2note-YYYYMMDD-HHMMSS).
- AppleScript integration includes folder creation and note placement capabilities.
- CLI interface provides mutually exclusive `--folder` and `--auto-folder` options for organization flexibility.

*Last updated: 2025-06-22* 