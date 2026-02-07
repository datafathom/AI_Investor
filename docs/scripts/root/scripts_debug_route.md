# Script: debug_route.py

## Overview
`debug_route.py` is a targeted debugging tool for investigating console errors on a specific frontend route. It provides more interactive and verbose output than the full audit suite.

## Core Functionality
- **Isolated Debugging**: Launches a headless Chrome browser targeting a single user-specified route.
- **Enhanced Logging**: Bypasses authentication and captures all console entries (Warnings, Errors, and Info logs).
- **Interactive Option**: Can be modified to run in headed mode to allow for manual inspection of the DOM and network state while viewing real-time logs in the terminal.

## Usage
Modify the `route` variable in the script and run:
```bash
python scripts/debug_route.py
```

## Status
**Essential (Developer Tool)**: Indispensable for fixing specific UI bugs detected by the automated audit. It significantly speeds up the "Fix -> Verify" loop for individual components.
