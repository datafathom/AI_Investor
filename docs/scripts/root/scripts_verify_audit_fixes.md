# Script: verify_audit_fixes.py

## Overview
`verify_audit_fixes.py` is an incremental verification tool that reruns audits only on previously failed routes.

## Core Functionality
- **Incremental Audit**: Reads a specific Audit Result JSON file, identifies all routes marked as "Failed", and then uses Selenium to re-examine those specific routes.
- **Dynamic Update**: If a route now passes, the script updates the JSON file status to "Success" and logs the new page load time.

## Status
**Essential (Workflow)**: Allows developers to quickly verify fixes for specific audit failures without waiting for a complete 15-minute full system audit.
