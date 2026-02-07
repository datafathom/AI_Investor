# Script: migration_manager.py

## Overview
`migration_manager.py` is an advanced supervisor for the migration life cycle, providing tools for creating, validating, and rolling back migrations.

## Core Functionality
- **Migration Creation**: provides a scaffolding tool to generate timestamped forward and rollback SQL templates (`create` command).
- **Automated Validation**: parses migration files for basic syntax errors and identifies "dangerous" operations (like `TRUNCATE` or `DROP DATABASE`) before they are applied.
- **State Persistence**: maintains its own `migration_metadata.json` as a secondary source of truth for the migration state.

## Usage
```bash
python scripts/database/migration_manager.py create --name add_investor_profile
```

## Status
**Essential (Developer Tool)**: used by developers to reliably author and test new database schema changes.
