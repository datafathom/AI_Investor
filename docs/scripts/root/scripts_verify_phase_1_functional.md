# Script: verify_phase_1_functional.py

## Overview
`verify_phase_1_functional.py` is an E2E test for the core backend services introduced in the early development phases, specifically the `memory_service` and the Redis-based job queue (`arq`).

## Core Functionality
- **Memory Service Audit**: stores an "experience" containing simulated PII (Personally Identifiable Information) and then recalls it to verify that the redaction engine is correctly obfuscating sensitive data before retrieval.
- **Job Queue Verification**: Enqueues a mock agent task to Redis via `arq` and checks for job completion and result availability.

## Status
**Essential (Back-end Verification)**: validates the foundational data privacy and asynchronous execution modules of the platform.
