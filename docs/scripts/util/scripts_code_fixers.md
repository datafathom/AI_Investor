# Utility: Code Correction and Fixers

## Overview
These utilities are designed to automate bulk code repairs, refactorings, and sanitization across the entire AI Investor codebase.

## Key Utilities

### [absolute_fix.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/util/absolute_fix.py) / [definitive_fix.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/util/definitive_fix.py) / [master_fix.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/util/master_fix.py)
A hierarchy of increasingly complex refactoring scripts used to resolve persistent linting errors, import cycles, and syntax issues. They use recursive file scanning and AST manipulation to enforce architectural rules (e.g., proper error handling blocks, consistent naming).

### [sanitize_all.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/util/sanitize_all.py) / [sanitize_app.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/util/sanitize_app.py)
Removes debug logs, print statements, and temporary comments from production-bound source files.

### [strip_local_imports.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/util/strip_local_imports.py)
Refactors cross-module imports to use the project's standardized relative path structure, preventing "ModuleNotFound" errors when running code in containerized environments.

## Status
**Essential (Maintenance)**: these tools are used to keep the codebase clean and compliant with the project's strict high-quality coding standards.
