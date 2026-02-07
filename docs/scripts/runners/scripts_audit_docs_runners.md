# Runners: Audit and Documentation

## Overview
These runners automate the generation of technical documentation and the execution of compliance/quality audits.

## Key Runners

### [api_docs.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/runners/api_docs.py)
Triggers the full API documentation generation-to-web-display pipeline. It runs the extractor, formats the Markdown, and notifies the documentation server of updates.

### [frontend_docs.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/runners/frontend_docs.py) / [frontend_docs_runner.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/runners/frontend_docs_runner.py)
Orchestrates the generation of frontend-specific documentation (e.g., component manifests, route lists) and their integration into the main docs portal.

### [mock_audit.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/runners/mock_audit.py) / [vendor_audit.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/runners/vendor_audit.py)
Wrappers around the core codebase auditing logic. They provide structured CLI interfaces for scanning the project for development shortcuts (mocks) and external service dependencies (vendors).

### [test_runner.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/runners/test_runner.py)
The comprehensive entry point for the test suite. It supports running unit, integration, and E2E tests with various flags for verbosity, coverage, and parallelization.

## Status
**Essential (Maintenance)**: ensures that the system's documentation and quality gates are automatically maintained.
