# Script: backup_db.py

## Overview
`backup_db.py` is a simplified deployment-time backup script, often used during blue-green or canary deployments to take a quick snapshot before applying changes.

## Core Functionality
- **Quick Snapshot**: executes a standard `pg_dump` of the `ai_investor` database and stores it in the `backups/` directory with a timestamp.
- **Simplicity**: unlike the main `database/backup.py`, this script is designed for minimal dependencies and speed, making it suitable for pre-deployment hooks.

## Status
**Essential (Deployment)**: used as a safety net in the automated deployment pipeline.
