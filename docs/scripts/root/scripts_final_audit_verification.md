# Script: final_audit_verification.py

## Overview
`final_audit_verification.py` is a variant of the frontend audit tool optimized for a final "clean room" verification. It focuses specifically on the most critical paths and ensuring no SEVERE errors remain.

## Core Functionality
- **Targeted Audit**: Navigates through a list of critical application routes (Dashboard, Strategy, Performance, Onboarding).
- **Console Validation**: Filters and reports any console logs with a level of `SEVERE`.
- **Evidence Collection**: Saves screenshots to a specific `final_audit/` directory for audit trailing.

## Usage
```bash
python scripts/final_audit_verification.py
```

## Status
**Essential (Deployment Gate)**: Usually run as the final step before merging a major feature branch to ensure zero regression in the frontend runtime.
