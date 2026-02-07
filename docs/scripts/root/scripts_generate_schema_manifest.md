# Script: generate_schema_manifest.py

## Overview
`generate_schema_manifest.py` creates a directory manifest for SQL migration files to control their execution order.

## Core Functionality
- **File Sorting**: Scans `schemas/postgres/` for `.sql` files and sorts them based on specific naming conventions (e.g., numeric prefixes or date stamps).
- **Manifest Creation**: writes `schema_manifest.json`, which is used by the `MigrationRunner` to ensure migrations are applied in the correct sequence.

## Status
**Essential (Database)**: prevents order-of-operation errors during database schema updates.
