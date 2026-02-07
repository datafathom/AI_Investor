# Script: migrate_phase_1.py / migrate_phase_2.py

## Overview
These scripts are dedicated runners for the Phase 1 and Phase 2 database migrations respectively.

## Core Functionality
- **Isolated Migration**: Each script focuses on applying the SQL schema changes associated with defensive core and alpha strategies.
- **Order Enforcement**: they ensure that prerequisite tables (Users, Audits) are created before dependent tables (Portfolios, Trades) are attempted.

## Status
**Essential (Database)**: used during the initial setup of the production environment to establish the core data model.
