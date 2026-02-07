# Script: frontend_audit_suite.py

## Overview
`frontend_audit_suite.py` is an advanced wrapper around `audit_frontend.py` that provides a complete auditing workflow, including pre-flight checks and organized reporting.

## Core Functionality
- **Workflow Orchestration**:
  1. Verifies service connectivity.
  2. Runs the full route audit.
  3. Aggregates results into a high-level summary.
- **Enhanced Reliability**: Implements more aggressive retry logic and longer timeouts than the base audit script, making it suitable for CI/CD environments.

## Status
**Essential (CI)**: This is the actual entry point for automated frontend audits in the build pipeline.
