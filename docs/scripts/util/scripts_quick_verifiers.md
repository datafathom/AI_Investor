# Utility: Quick Verification Scripts

## Overview
Lightweight scripts designed for fast, frequent verification of specific system components.

## Key Utilities

### [verify_routes.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/util/verify_routes.py)
Peforms a fast HTTP-only check of all registered API routes to ensure they return a valid status (200/401/405) instead of a 404 or 500.

### [verify_frontend.ps1](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/util/verify_frontend.ps1) / [verify_frontend.sh](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/util/verify_frontend.sh)
Cross-platform scripts that trigger linting and type-checking for the React application.

### [verify_remote_infra.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/util/verify_remote_infra.py)
Validates that remote infrastructure components (e.g., staging database, remote Kafka cluster) are reachable and responding to heartbeat requests.

## Status
**Essential (QC)**: provide the "inner loop" verification that developers run multiple times a day to ensure their local environment is stable.
