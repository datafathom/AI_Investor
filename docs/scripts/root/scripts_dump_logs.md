# Script: dump_logs.py

## Overview
`dump_logs.py` is a utility for extracting the raw current browser console logs from the Strategy dashboard.

## Core Functionality
- **Log Extraction**: Navigates to `/analytics/strategy`, waits for the page to reach a stable state (10 seconds), and then pulls the entire browser log buffer.
- **Terminal Output**: Prints the logs directly to standard output, making it easy to pipe to grep or save to a file for analysis.

## Usage
```bash
python scripts/dump_logs.py
```

## Status
**Obsolete (Redundant)**: This script's functionality is a subset of `debug_route.py` and `get_logs.py`. It is maintained primarily for backwards compatibility with older CI pipelines.
