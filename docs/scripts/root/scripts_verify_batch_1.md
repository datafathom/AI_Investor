# Script: verify_batch_1.py

## Overview
`verify_batch_1.py` is a functional test runner for the "Batch 1" set of API endpoints.

## Core Functionality
- **Auth Acquisition**: Performs an administrative login to acquire a fresh JWT bearer token.
- **Endpoint Probing**: Executes a series of GET/POST requests against critical Batch 1 endpoints (Onboarding Status, Analytics Performance, AI Briefing, Trailing Stop Execution) and validates the status codes and response structures.

## Status
**Essential (Integration)**: The primary tool for verifying the health of the core application API layer.
