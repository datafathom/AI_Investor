# Script: create_rollback.py / clean_rollbacks.py

## Overview
These scripts manage the lifecycle of SQL rollback files.

## Core Functionality
- **Rollback Generation**: `create_rollback.py` helps automate the generation of "Down" migrations by analyzing the changes in an "Up" migration (simplified).
- **Housekeeping**: `clean_rollbacks.py` identifies and removes orphaned or redundant rollback files that no longer correspond to active forward migrations.

## Status
**Support Utility**: helpful for maintaining a clean and accurate migration history.
