# Script: find_remaining_batches.py

## Overview
`find_remaining_batches.py` is a project management utility that identifies test files that have not yet been assigned to a verification batch.

## Core Functionality
- **Test Inventory**: Scans the `tests/` directory for Python files matching the `test_*.py` pattern.
- **Batch Matching**: Reads the project's verification plan or batch configuration (e.g., `gen_task_batches.py` output) and performs a diff against the full inventory.
- **Output**: Lists all "unaccounted for" tests, helping maintainers ensure 100% test coverage in automated pipelines.

## Status
**Essential (QC)**: Prevents "silent regressions" by ensuring that every new test file added to the codebase is eventually integrated into a CI batch.
