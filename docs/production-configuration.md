# Production Environment Configuration Guide

**Project:** MD2Note - Markdown to Apple Notes & Google Docs Converter  
**Version:** 1.0.0  
**Last Updated:** 2025-06-17

## Overview

This document provides comprehensive guidance for configuring and deploying the MD2Note application in production environments. It covers system requirements, installation procedures, security considerations, and operational best practices.

## System Requirements

### Hardware Requirements
- **CPU:** 1+ cores (2+ recommended for large file processing)
- **RAM:** 2GB minimum (4GB recommended)
- **Disk Space:** 1GB for application + space for processing files
- **Network:** Internet connectivity required for Google Docs export

### Software Requirements
- **Operating System:** macOS 10.14+ (required for Apple Notes integration)
- **Python:** 3.9 or higher
- **Internet Access:** Required for Google Docs API and OAuth2 authentication

### Third-Party Dependencies
- **Apple Notes:** Pre-installed on macOS
- **Google Cloud Account:** Required for Google Docs export functionality
- **OAuth2 Credentials:** Required for Google API access

## Installation and Setup

### 1. Application Installation

```bash
# Clone the repository
git clone https://github.com/ghelleks/md2note.git
cd md2note

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install the package (optional)
pip install -e .
```

### 2. Google Cloud Configuration

#### Prerequisites
1. **Create Google Cloud Project**
   - Navigate to [Google Cloud Console](https://console.cloud.google.com/)
   - Create new project or select existing one
   - Note the Project ID for reference

2. **Enable Required APIs**
   ```bash
   # Enable APIs via gcloud CLI (optional)
   gcloud services enable docs.googleapis.com
   gcloud services enable drive.googleapis.com
   ```
   
   Or enable via Console:
   - Google Docs API
   - Google Drive API

#### OAuth2 Credentials Setup
1. **Configure OAuth Consent Screen**
   - Go to APIs & Services > OAuth consent screen
   - Choose "External" user type
   - Fill required fields:
     - App name: "MD2Note"
     - User support email: Your email
     - Developer contact: Your email
   - Add scopes:
     - `https://www.googleapis.com/auth/documents`
     - `https://www.googleapis.com/auth/drive`

2. **Create OAuth2 Credentials**
   - Go to APIs & Services > Credentials
   - Click "Create Credentials" > "OAuth client ID"
   - Application type: "Desktop application"
   - Name: "MD2Note Desktop Client"
   - Download credentials JSON file

3. **Install Credentials**
   ```bash
   # Place credentials file in project root
   mv ~/Downloads/client_secret_*.json ./credentials.json
   
   # Verify file exists and is readable
   ls -la credentials.json
   ```

### 3. Environment Configuration

#### Directory Structure
```
/opt/md2note/                    # Application root
├── src/                         # Application source code
├── docs/                        # Documentation
├── credentials.json             # Google OAuth2 credentials
├── token.pickle                 # Generated OAuth2 tokens (auto-created)
├── md2note.log                  # Application logs
├── requirements.txt             # Python dependencies
└── venv/                        # Python virtual environment
```

#### File Permissions
```bash
# Set appropriate permissions
chmod 600 credentials.json       # Protect OAuth credentials
chmod 755 src/md2note.py         # Make executable
chmod 644 requirements.txt       # Read-only dependencies
```

## Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MD2NOTE_LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `MD2NOTE_LOG_FILE` | `md2note.log` | Log file path |
| `MD2NOTE_CREDENTIALS_PATH` | `credentials.json` | Google OAuth2 credentials file path |
| `MD2NOTE_TOKEN_PATH` | `token.pickle` | OAuth2 token storage path |

### CLI Configuration

#### Basic Usage
```bash
# Apple Notes export (default)
python src/md2note.py --source /path/to/markdown/files

# Google Docs export
python src/md2note.py --source /path/to/markdown/files --export-to google_docs

# Google Docs with custom folder
python src/md2note.py --source /path/to/markdown/files --export-to google_docs --gdocs-folder "My Documents"

# Custom clean directory
python src/md2note.py --source /path/to/markdown/files --clean /path/to/clean/directory
```

#### Advanced Configuration
```bash
# Set log level
export MD2NOTE_LOG_LEVEL=DEBUG

# Custom credential locations
export MD2NOTE_CREDENTIALS_PATH=/secure/path/credentials.json
export MD2NOTE_TOKEN_PATH=/secure/path/token.pickle

# Run with custom settings
python src/md2note.py --source /data/markdown --export-to google_docs --gdocs-folder "Production Documents"
```

## Security Configuration

### Credential Management

#### Best Practices
1. **File Permissions**
   ```bash
   # Restrict access to credentials
   chmod 600 credentials.json token.pickle
   chown appuser:appgroup credentials.json token.pickle
   ```

2. **Storage Location**
   ```bash
   # Store credentials outside application directory
   mkdir -p /etc/md2note/credentials
   mv credentials.json /etc/md2note/credentials/
   export MD2NOTE_CREDENTIALS_PATH=/etc/md2note/credentials/credentials.json
   ```

3. **Backup and Recovery**
   ```bash
   # Backup credentials securely
   cp credentials.json /secure/backup/location/
   
   # Document recovery procedures
   echo "Credential recovery: Download from Google Cloud Console" > /etc/md2note/RECOVERY.md
   ```

### Network Security

#### Firewall Configuration
```bash
# Allow HTTPS for Google API access
# Port 443 (HTTPS) - Required for Google API
# Port 80 (HTTP) - May be required for OAuth redirect
```

#### SSL/TLS Considerations
- Google API requires HTTPS (handled automatically by libraries)
- OAuth2 flow uses secure HTTPS endpoints
- No additional SSL configuration required

## Operational Configuration

### Logging Configuration

#### Log Levels
- **DEBUG:** Detailed debugging information
- **INFO:** General application flow (default)
- **WARNING:** Warning messages
- **ERROR:** Error conditions

#### Log Rotation
```bash
# Setup logrotate for application logs
cat > /etc/logrotate.d/md2note << EOF
/opt/md2note/md2note.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 appuser appgroup
}
EOF
```

### Monitoring and Alerting

#### Key Metrics to Monitor
- Application execution success/failure rates
- Google API response times and error rates
- File processing throughput
- Disk space usage in source and clean directories
- Authentication token expiry

#### Health Check Script
```bash
#!/bin/bash
# /opt/md2note/bin/health-check.sh

# Check application dependencies
python3 -c "import src.app; print('Application: OK')" || echo "Application: FAILED"

# Check Google API connectivity
python3 -c "from src.google_docs_exporter import GoogleDocsExporter; print('Google API: OK')" || echo "Google API: FAILED"

# Check credentials
test -f credentials.json && echo "Credentials: OK" || echo "Credentials: MISSING"

# Check token
test -f token.pickle && echo "Token: OK" || echo "Token: MISSING"
```

### Backup and Recovery

#### Backup Strategy
```bash
# Backup script
#!/bin/bash
BACKUP_DIR="/backup/md2note/$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"

# Backup credentials and tokens
cp credentials.json "$BACKUP_DIR/"
cp token.pickle "$BACKUP_DIR/" 2>/dev/null || true

# Backup configuration
cp -r docs/ "$BACKUP_DIR/"
cp requirements.txt "$BACKUP_DIR/"

# Backup logs
cp md2note.log "$BACKUP_DIR/" 2>/dev/null || true

echo "Backup completed: $BACKUP_DIR"
```

#### Recovery Procedures
1. **Credential Recovery**
   - Download new credentials from Google Cloud Console
   - Place in correct location with proper permissions
   - Remove token.pickle to force re-authentication

2. **Application Recovery**
   - Restore application files from backup
   - Recreate virtual environment
   - Reinstall dependencies
   - Test authentication flow

## Performance Tuning

### File Processing Optimization
```bash
# Process files in batches
for dir in /data/markdown/batch*; do
    python src/md2note.py --source "$dir" --export-to google_docs
    sleep 60  # Rate limiting pause
done
```

### Google API Rate Limiting
- Default quotas: 100 requests per 100 seconds per user
- Monitor usage in Google Cloud Console
- Implement backoff strategies for rate limit errors

### Memory Management
```bash
# Monitor memory usage
ps aux | grep python | grep md2note

# Set memory limits if needed
ulimit -v 2097152  # 2GB virtual memory limit
```

## Troubleshooting Guide

### Common Issues

#### Authentication Errors
```bash
# Error: credentials.json not found
# Solution: Verify file path and permissions
ls -la credentials.json
export MD2NOTE_CREDENTIALS_PATH=/correct/path/credentials.json

# Error: Token expired
# Solution: Remove token and re-authenticate
rm token.pickle
python src/md2note.py --source test --export-to google_docs
```

#### Google API Errors
```bash
# Error: Rate limit exceeded
# Solution: Implement delays between requests
# Check quota usage in Google Cloud Console

# Error: Insufficient permissions
# Solution: Verify OAuth2 scopes and consent screen
```

#### File Processing Errors
```bash
# Error: Permission denied
# Solution: Check file permissions
chmod -R 644 /path/to/markdown/files
chmod -R 755 /path/to/directories

# Error: Disk space full
# Solution: Monitor and clean up processed files
df -h
rm -rf /path/to/clean/old_files
```

### Diagnostic Commands
```bash
# Test Google API connectivity
python3 -c "
from src.google_docs_exporter import GoogleDocsExporter
exporter = GoogleDocsExporter()
print('Validation:', exporter.validate_configuration())
"

# Test Apple Notes connectivity
python3 -c "
from src.apple_notes_exporter import AppleNotesExporter
exporter = AppleNotesExporter()
print('Validation:', exporter.validate_configuration())
"

# View recent logs
tail -f md2note.log

# Check system resources
top -p $(pgrep -f md2note)
```

## Maintenance Procedures

### Regular Maintenance Tasks

#### Weekly
- Review application logs for errors
- Check disk space usage
- Verify backup integrity
- Monitor Google API quota usage

#### Monthly
- Rotate and archive logs
- Update dependencies (after testing)
- Review and update documentation
- Test recovery procedures

#### Quarterly
- Review security settings and permissions
- Update OAuth2 credentials if needed
- Performance tuning and optimization
- Disaster recovery testing

### Update Procedures
```bash
# Update application
cd /opt/md2note
git fetch origin
git checkout main
git pull origin main

# Update dependencies
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Test after update
python -m pytest tests/ -v
```

## Support and Escalation

### Log Analysis
- Application logs: `md2note.log`
- System logs: `/var/log/system.log` (macOS)
- Google API logs: Google Cloud Console > Logging

### Performance Monitoring
- Monitor file processing rates
- Track API response times
- Watch for memory leaks or resource exhaustion

### Emergency Contacts
- **Application Issues:** Development team
- **Google API Issues:** Google Cloud Support
- **Infrastructure Issues:** System administrators

---

**Document Version:** 1.0  
**Created By:** Senior Software Developer  
**Review Schedule:** Quarterly  
**Next Review:** 2025-09-17