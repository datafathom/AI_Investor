# Phase 31: Staging Environment & CICD Finalization
> **Phase ID**: 31
> **Status**: Planning
> **Date**: 2026-01-20

## Overview
Prepare the application for a professional staging environment and finalize the Continuous Integration / Continuous Deployment (CICD) pipelines. This ensures that every change is automatically tested and deployed to a production-like environment before reaching final users.

## Objectives
- [ ] Configure **GitHub Actions** workflows for automated testing and staging deployment.
- [ ] Implement a robust **Environment Configuration Manager** to handle different settings for `LOCAL`, `STAGING`, and `PRODUCTION`.
- [ ] Create a **Smoke Test Suite** that runs against the deployed staging environment.
- [ ] Finalize Docker Compose configurations for staging-specific services (e.g., managed DB connections).
- [ ] Implement a `HealthCheckService` that monitors intra-service connectivity (Postgres, Redis, Neo4j, Kafka).

## Files to Modify/Create
1.  `.github/workflows/staging-deploy.yml` **[NEW]**
2.  `config/environment_manager.py` **[NEW]**
3.  `tests/smoke/test_staging_health.py` **[NEW]**
4.  `plans/Performance_Security_GoingLive/Phase_31_ImplementationPlan.md` **[NEW]**

## Technical Design
- **Config Management**: Uses `pydantic-settings` to load environment variables with validation and defaults based on `APP_ENV`.
- **CICD**: GitHub Actions will trigger on `pull_request` to `staging` branch, running linting, unit tests, and then building/pushing images.

## Verification Plan
### Automated Tests
- `pytest tests/smoke/test_staging_health.py`: Verifies that `HealthCheckService` reports all critical systems as `UP`.

### Manual Verification
1. Push a dummy change to a feature branch.
2. Open a PR to `staging`.
3. Verify that the GitHub Action triggers, passes, and (simulated) deploys to staging.
4. Access the staging health endpoint: `GET /api/v1/health`.
