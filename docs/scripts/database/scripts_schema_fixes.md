# Script: fix_role_column.py / fix_user_schema.py

## Overview
One-off repair scripts for the User and Authentication schemas.

## Core Functionality
- **Schema Repair**: these scripts fix specific data integrity issues or schema mismatches encountered during the early beta phase (e.g., adding a missing `role` column with default values or re-aligning foreign key constraints in the user table).

## Status
**Obsolete (Legacy)**: these changes have been incorporated into the main migration baseline. They are maintained only for historical reference of the schema evolution.
