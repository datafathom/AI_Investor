# Script: refactor_models.py

## Overview
`refactor_models.py` is a backend migration utility that renames and relocates data models to a unified `schemas` directory.

## Core Functionality
- **Import Rewriting**: Replaces all instances of `from models...` with `from schemas...` throughout the codebase.
- **Directory Consolidation**: Moves files from the legacy `models/` directory into the modern `schemas/` directory, maintaining internal module relationships.

## Status
**Essential (Maintenance)**: Used to enforce the project's architectural decision to use Pydantic schemas as the primary data transfer and persistence models.
