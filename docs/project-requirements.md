# Project Requirements

## 1. Introduction
This project aims to develop a Python application that processes a directory of markdown files and exports them to a configurable destination (Apple Notes or Google Docs) for each file, preserves metadata from the file contents or the file itself, and moves successfully processed files to a new directory (default: 'clean'). The application will prompt the user for more information or to quit if any issues arise.

## 2. Stakeholders
- Users who manage markdown files and wish to convert them into Apple Notes
- Users who manage markdown files and wish to convert them into Google Docs
- Developers responsible for implementing the Python application

## 3. Functional Requirements
| ID  | Requirement Description                | Priority (High/Med/Low) | Notes           |
|-----|----------------------------------------|-------------------------|-----------------|
| FR1 | Process a directory of markdown files  | High                    | Must handle multiple files |
| FR2 | Export markdown files to the specified destination (Apple Notes via AppleScript or Google Docs via API) | High | Must preserve metadata |
| FR3 | Move successfully processed files to a new directory | High | Default: 'clean' |
| FR4 | Support Google Docs as an export destination | High | Alternative to Apple Notes |
| FR5 | Allow user to specify Google Docs folder location | Medium | For organization |
| FR6 | Provide command-line option to choose export destination | High | User choice between Apple Notes/Google Docs |

## 4. Non-Functional Requirements
| ID  | Requirement Description                | Priority (High/Med/Low) | Notes           |
|-----|----------------------------------------|-------------------------|-----------------|
| NFR1| Preserve metadata from markdown files  | High                    | Prioritize metadata from file contents |
| NFR2| Prompt user for more information or to quit if an error occurs | High | Must handle errors gracefully |
| NFR3| Support Google Docs API authentication | High | Required for Google Docs integration |
| NFR4| Maintain cross-platform compatibility where possible | Medium | Google Docs doesn't require macOS |

## 5. Assumptions and Dependencies
- For Apple Notes export: The Python application has access to the AppleScript environment.
- For Google Docs export: Python application has access to Google Docs API.
- User has valid Google account and API credentials configured (for Google Docs export).
- The markdown files are in a readable format.

## 6. Constraints
- For Apple Notes export: The application must be compatible with the latest version of macOS.
- For Google Docs export: The application must support Google API authentication.
- The application must handle errors without crashing.

## 7. Acceptance Criteria
- The application successfully processes all markdown files in the specified directory.
- User can choose between Apple Notes and Google Docs as export destination.
- For Apple Notes export: Each markdown file is converted into a note in the Apple Notes app via AppleScript.
- For Google Docs export: Each markdown file is converted into a Google Doc with preserved formatting.
- User can specify target Google Drive folder for exported documents (Google Docs export).
- Successfully processed files are moved to the 'clean' directory.
- The application prompts the user for more information or to quit if any issues arise.

## 8. Out of Scope
- Handling non-markdown files.
- Modifying the content of the markdown files.

## 9. Glossary
| Term | Definition |
|------|------------|
| AppleScript | A scripting language created by Apple Inc. for automating tasks on macOS. |
| Markdown | A lightweight markup language with plain text formatting syntax. |
| Google Docs API | Google's REST API for creating and managing Google Docs documents. |
| Google Drive | Google's cloud storage service where Google Docs are stored. |

---

## Implementation Notes
- Metadata extraction is implemented to prefer YAML front matter, falling back to file properties if not present.
- AppleScript integration is handled via a dedicated Python module that creates notes in Apple Notes, with robust error handling and test coverage.

*Last updated: 2025-06-15* 