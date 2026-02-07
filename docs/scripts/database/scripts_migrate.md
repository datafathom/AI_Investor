# Script: migrate.py

## Overview
`migrate.py` is the primary database migration runner for the project. It handles the application and tracking of SQL schema changes.

## Core Functionality
- **Migration Tracking**: maintains a `schema_migrations` table in the database to record which versions have been applied.
- **Manifest-Based Ordering**: reads `schema_manifest.json` to determine the exact order in which to execute `.sql` files found in the `schemas/postgres/` directory.
- **Transactional Safety**: applies each migration within a database transaction to ensure that partial failures don't leave the schema in an inconsistent state.

## Usage
```bash
python scripts/database/migrate.py up
python scripts/database/migrate.py status
```

## Status
**Essential (Database)**: the core tool for managing the evolution of the relational data model.
