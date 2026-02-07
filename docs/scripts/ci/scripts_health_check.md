# Script: health_check.sh

## Overview
`health_check.sh` is a shell-based utility for container readiness and CI health probing.

## Core Functionality
- **Endpoint Probing**: uses `curl` to check the `/health` endpoint of the backend service.
- **Docker Integration**: often used as a `HEALTHCHECK` command in Dockerfiles or as a wait-script in CI pipelines before starting E2E tests.

## Status
**Essential (DevOps)**: provides a simple, platform-independent way to verify service liveness.
