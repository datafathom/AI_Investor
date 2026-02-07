# Script: audit_codebase.py

## Overview
`audit_codebase.py` is a specialized static analysis utility designed to scan the AI Investor project for indicators of incomplete implementation or external vendor dependencies. It focuses on identifying hardcoded mock responses and direct API calls to third-party services.

## Core Functionality
The script perform a recursive scan of the project directory (excluding common non-source folders like `venv`, `.git`, and `node_modules`) using regular expressions to find specific patterns.

### Mock Detection
Scans for keywords and patterns that suggest placeholder data or unfinished tasks:
- `mock_response`
- `dummy_data`
- `placeholder data`
- `todo: remove mock`
- `return {"mock": ...}`

### Vendor API Detection
Identifies direct integrations with external financial and AI service providers:
- HTTP clients: `requests.get/post`, `axios`, `fetch`
- Service domains: `googleapis.com`, `stripe.com`, `plaid.com`, `polygon.io`, `openai.com`, `anthropic.com`

## Implementation Details
- **Path Handling**: Utilizes `pathlib.Path` for cross-platform compatibility.
- **Reporting**: Generates two JSON reports in the `notes/` directory:
  - `mocks_found.json`: Detailed list of all detected mock patterns with file paths and line numbers.
  - `vendors_found.json`: Detailed list of all detected vendor API integrations.
- **Exclusion Logic**: Hardcoded `EXCLUDES` dictionary prevents the script from scanning build artifacts, third-party libraries, and Git internals.

## Usage
```bash
python scripts/audit_codebase.py
```

## Status
**Essential**: Critical for ensuring the transition from a development/mocked state to a production-ready, fully-integrated system. It serves as a quality gate for code reviews.
