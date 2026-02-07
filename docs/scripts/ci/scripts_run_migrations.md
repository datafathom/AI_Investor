# Script: run_migrations.sh

## Overview
`run_migrations.sh` is a convenience wrapper for running database migrations in a Unix-like environment.

## Core Functionality
- **Execution**: calls `python scripts/database/migrate.py up` while ensuring the correct virtual environment is active and environment variables are loaded.

## Status
**Essential (Deployment)**: The standard entry point for applying database schema changes during deployment or post-build steps.
