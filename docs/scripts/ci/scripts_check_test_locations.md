# Script: check_test_locations.py

## Overview
`check_test_locations.py` is a CI script that ensures all test files are centralized within the `tests/` directory.

## Core Functionality
- **Location Enforcement**: Scans the entire project for files matching `test_*.py` or `*_test.py`. It flags any test file found outside the root `tests/` directory.
- **Folder Exclusion**: correctly ignores files in `node_modules`, `venv`, and build caches.

## Status
**Essential (CI)**: Keeps the project structure clean and ensures that the test runners (pytest) don't miss tests scattered across the source folders.
