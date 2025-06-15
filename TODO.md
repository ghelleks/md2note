# Project Plan: Markdown to Apple Notes Converter

## Phase 1: Project Setup
**Tasks:**
- [x] Initialize project repository
- [x] Set up virtual environment
- [x] Create basic project structure
- [x] Define project requirements

**Deliverables:**
- Requirements document with acceptance criteria
- Git repository with initial commit
- Project directory structure documented in README.md
- requirements.txt with all dependencies
- Project structure diagram or documentation

## Phase 2: Core Functionality
### 2.1 Directory Scanning
**Tasks:**
- [x] Implement directory scanning

**Deliverables:**
- Python module with directory scanning functionality
- Unit test suite with test cases for directory scanning
- Test coverage report showing >80% coverage
- Documentation of supported file patterns and filters

### 2.2 Markdown Metadata Extraction
**Tasks:**
- [x] Implement markdown metadata extraction

**Deliverables:**
- Python module for markdown parsing and metadata extraction
- Unit test suite with test cases for YAML front matter and file properties
- Test coverage report showing >80% coverage
- Documentation of metadata extraction rules and fallback behavior

### 2.3 AppleScript Note Creation
**Tasks:**
- [x] Implement AppleScript note creation

**Deliverables:**
- Python module for AppleScript integration
- Unit test suite with mocked AppleScript calls
- Test coverage report showing >80% coverage
- Documentation of AppleScript interface and error handling

### 2.4 File Movement
**Tasks:**
- [x] Implement file movement to clean directory

**Deliverables:**
- Python module for file movement operations
- Unit test suite with test cases for file operations
- Test coverage report showing >80% coverage
- Documentation of file movement rules and error handling

### 2.5 Component Coordination
**Tasks:**
- [x] Coordinate components and provide CLI interface

**Deliverables:**
- Main application module with component integration
- CLI interface with argument parsing
- Unit test suite for CLI functionality
- Documentation of CLI commands and options

## Phase 3: Testing and Documentation
**Tasks:**
- [x] Write unit tests for each component
- [x] Document code and usage
- [x] Create README and installation instructions

**Deliverables:**
- Complete test suite with >80% coverage
- API documentation for all modules
- User guide with installation and usage instructions
- Error handling documentation with examples
- README.md with project overview and setup instructions

## Phase 4: Integration Testing and Deployment
**Tasks:**
- [x] Integration Testing
  - [x] Test CLI interface and argument parsing
  - [x] Test end-to-end workflows with real files
  - [x] Verify error handling and logging in production scenarios
- [x] Package the application
- [x] Create distribution package
- [ ] Deploy and verify in production environment

**Deliverables:**
- [x] Integration test suite with test cases for full workflow
- [x] Test report documenting successful and failure scenarios
- [x] CLI interface test results
- [x] End-to-end test results with real files
- [x] Production deployment package
- [ ] Deployment verification report
- [ ] Production environment configuration documentation

## Phase 5: Google Docs Export Implementation
**Tasks:**
- [x] Research Google Docs API capabilities and authentication methods
- [x] Analyze current codebase architecture and identify extension points  
- [x] Design export strategy pattern to support multiple destinations
- [x] Add Google API client libraries to requirements.txt
- [x] Implement Google Docs exporter class with authentication and document creation
- [x] Refactor existing AppleScript functionality into exporter class
- [x] Add CLI options for export destination and Google Drive folder selection
- [x] Implement Google OAuth2 authentication flow with credential management
- [x] Implement markdown to Google Docs rich text conversion
- [x] Extend error handling for Google API errors and network issues
- [x] Write comprehensive unit tests for Google Docs exporter
- [x] Write integration tests for end-to-end Google Docs workflow
- [x] Update README and CLI documentation for Google Docs export feature

**Deliverables:**
- [x] Export strategy pattern with DocumentExporter abstract base class
- [x] GoogleDocsExporter implementation with OAuth2 authentication
- [x] AppleNotesExporter refactored to use strategy pattern
- [x] CLI interface with --export-to and --gdocs-folder options
- [x] Comprehensive unit test suite for all exporter components
- [x] Integration tests for end-to-end Google Docs workflow
- [x] Updated documentation and usage examples
- [x] Google Cloud setup instructions for OAuth2 credentials

## Open Issues
- [x] Add initial formatting to the Note (#1) ✅
- [ ] Create an option to export to Google Docs (#3) ⌛️ **In Progress**

## Testing Summary
- **Unit Tests:** Directory scanning, markdown parsing, metadata extraction, note creation (mocked), file movement, error handling
- **Integration Tests:** End-to-end workflow, error scenarios, user prompts, CLI interface, production scenarios 