# Script: rename_schemas.py

## Overview
`rename_schemas.py` is a cleanup utility for standardizing individual SQL migration filenames.

## Core Functionality
- **Pattern Stripping**: Removes non-essential prefixes (like `schema_`) and leading digits from SQL filenames in the `schemas/postgres/` directory to create descriptive, human-readable names focused on the table or feature being migrated.

## Status
**Support Utility**: Used to improve the maintainability and readability of the database schema history.
