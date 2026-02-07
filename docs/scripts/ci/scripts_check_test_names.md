# Script: check_test_names.py

## Overview
`check_test_names.py` is a CI enforcer that mandates semantic naming for test files.

## Core Functionality
- **Semantic Naming**: blocks the use of temporal terms like "phase", "sprint", or "milestone" in test filenames (e.g., `test_phase1.py` is forbidden).
- **Enforcement**: requires that tests be named after the feature they verify (e.g., `test_billing.py`), which improves the long-term maintainability of the test suite as project management phases pass.

## Status
**Essential (CI)**: Prevents technical debt in the testing layer by enforcing feature-centric naming.
