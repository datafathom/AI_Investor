# Script: fix_warnings.py

## Overview
`fix_warnings.py` is a backend refactoring utility aimed at modernizing the codebase and removing deprecation warnings, specifically targeting Pydantic V2 migrations.

## Core Functionality
- **Pydantic Updates**: Replaces deprecated Pydantic V1 patterns (like `dict()`) with their V2 counterparts (like `model_dump()`).
- **DateTime Standardization**: Fixes "un-timezone-aware" datetime warnings by ensuring all `datetime.now()` calls include UTC information.
- **Bulk Safe-Refactor**: Performs these changes across all `.py` files in the project, excluding the `venv` directory.

## Status
**Essential (Maintenance)**: Keeps the codebase current and prevents "log spam" from deprecation warnings, which can obscure real runtime errors.
