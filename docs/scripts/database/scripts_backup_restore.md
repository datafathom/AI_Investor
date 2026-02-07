# Script: backup.py / restore.py

## Overview
These scripts handle the automated backup and restoration of the AI Investor PostgreSQL and Neo4j databases.

## Core Functionality
- **Dual-Database Support**: orchestrates backups for both the relational (Postgres) and graph (Neo4j) databases to ensure cross-database referential integrity.
- **Archive Management**: creates compressed tarballs of the database dumps, including timestamping and storage in the `backups/` directory.
- **Rollback Capability**: `restore.py` allows for point-in-time recovery by applying specific backup archives to a fresh or existing database instance.

## Usage
```bash
python scripts/database/backup.py
python scripts/database/restore.py --file backups/backup_2026.tar.gz
```

## Status
**Essential (Operational)**: Critical for disaster recovery and maintaining data safety in production environments.
