# Script: check_readiness.py

## Overview
`check_readiness.py` is the final pre-flight verification script run immediately before promoting a build to production.

## Core Functionality
- **End-to-End Health**: calls the backend's `/health` endpoint to ensure the core process is up and reports `overall: UP`.
- **Secret Audit**: perform a critical check of environment variables (e.g., `DATABASE_URL`, `JWT_SECRET`). It flags if any are set to development defaults (like "dev_secret_key") when the environment is marked as "production".
- **Launch Block**: exits with a non-zero code if any critical readiness check fails, effectively blocking a broken or insecure deployment.

## Status
**Essential (Production Gate)**: the final human-readable confirmation that the system is ready for live traffic.
