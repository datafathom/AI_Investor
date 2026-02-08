# Phase 3 Implementation Plan: Blue-Green Deployment & Operations

> **Phase**: 3 of 33  
> **Status**: 🔴 Not Started  
> **Priority**: CRITICAL  
> **Estimated Duration**: 4 days  
> **Dependencies**: Phase 1, Phase 2

---

## Overview

Phase 3 implements operational control interfaces for blue-green deployments, batch job management, workspace isolation, environment configuration, and feature flags.

### Services Covered
| Service | Directory | Primary Files |
|---------|-----------|---------------|
| `blue_green` | `services/blue_green/` | `controller.py`, `traffic_manager.py` |
| `operations` | `services/operations/` | `ops_manager.py`, `job_scheduler.py`, `feature_flags.py` |
| `workspace` | `services/workspace/` | `manager.py`, `tenant_isolation.py` |
| `system` | `services/system/` | `env_manager.py`, `config_service.py` |

---

## Deliverable 1: Deployment Controller Page

### 1.1 Description
Full-page interface (`/admin/deployments`) for managing blue-green environments, traffic splitting, and rollback operations.

### 1.2 Frontend Implementation

| Component | Path | Type |
|-----------|------|------|
| `DeploymentController.jsx` | `frontend/src/pages/admin/DeploymentController.jsx` | Page |
| `EnvironmentCard.jsx` | `frontend/src/components/cards/EnvironmentCard.jsx` | Card |
| `TrafficSlider.jsx` | `frontend/src/components/controls/TrafficSlider.jsx` | Control |
| `DeploymentTimeline.jsx` | `frontend/src/components/admin/DeploymentTimeline.jsx` | Widget |
| `RollbackConfirmModal.jsx` | `frontend/src/components/modals/RollbackConfirmModal.jsx` | Modal |

### 1.3 Backend Implementation

| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/admin/deployments/environments` | `list_environments()` |
| GET | `/api/v1/admin/deployments/current` | `get_current_deployment()` |
| POST | `/api/v1/admin/deployments/switch` | `switch_environment()` |
| POST | `/api/v1/admin/deployments/traffic` | `update_traffic_split()` |
| POST | `/api/v1/admin/deployments/rollback` | `trigger_rollback()` |
| GET | `/api/v1/admin/deployments/history` | `get_deployment_history()` |

### 1.4 End-to-End Acceptance Criteria

#### Functional Requirements
- [ ] **F3.1.1**: Show blue/green environments with version, status, health
- [ ] **F3.1.2**: Traffic slider allows 0-100% split between environments
- [ ] **F3.1.3**: One-click switch moves 100% traffic to selected environment
- [ ] **F3.1.4**: Rollback returns to previous stable deployment
- [ ] **F3.1.5**: Timeline shows deployment history with duration, status

#### Integration Requirements
- [ ] **I3.1.1**: Traffic update sends `{ blue: 30, green: 70 }` percentages
- [ ] **I3.1.2**: Switch requires confirmation with environment name
- [ ] **I3.1.3**: Rollback creates audit log entry
- [ ] **I3.1.4**: WebSocket updates traffic percentages in real-time

#### Response Handling
- [ ] **R3.1.1**: Environment schema: `{ name, version, status, health, traffic_pct }`
- [ ] **R3.1.2**: 409 Conflict if deployment in progress
- [ ] **R3.1.3**: Rollback success shows previous version restored

---

## Deliverable 2: Operations Dashboard Page

### 2.1 Description
Page (`/admin/ops`) displaying scheduled jobs, cron tasks, batch processes with status, logs, and manual trigger capabilities.

### 2.2 Frontend Implementation

| Component | Path | Type |
|-----------|------|------|
| `OperationsDashboard.jsx` | `frontend/src/pages/admin/OperationsDashboard.jsx` | Page |
| `JobScheduleTable.jsx` | `frontend/src/components/admin/JobScheduleTable.jsx` | Table |
| `JobRunHistory.jsx` | `frontend/src/components/admin/JobRunHistory.jsx` | Widget |
| `JobLogsViewer.jsx` | `frontend/src/components/admin/JobLogsViewer.jsx` | Panel |
| `TriggerJobModal.jsx` | `frontend/src/components/modals/TriggerJobModal.jsx` | Modal |

### 2.3 Backend Implementation

| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/admin/ops/jobs` | `list_scheduled_jobs()` |
| GET | `/api/v1/admin/ops/jobs/{job_id}` | `get_job_details()` |
| POST | `/api/v1/admin/ops/jobs/{job_id}/trigger` | `trigger_job()` |
| GET | `/api/v1/admin/ops/jobs/{job_id}/runs` | `get_job_runs()` |
| GET | `/api/v1/admin/ops/jobs/{job_id}/runs/{run_id}/logs` | `get_run_logs()` |
| PATCH | `/api/v1/admin/ops/jobs/{job_id}` | `update_job_schedule()` |

### 2.4 End-to-End Acceptance Criteria

#### Functional Requirements
- [ ] **F3.2.1**: Table shows all jobs with schedule, next run, last status
- [ ] **F3.2.2**: Click job shows run history with duration, exit codes
- [ ] **F3.2.3**: Manual trigger starts job immediately with confirmation
- [ ] **F3.2.4**: Logs viewer shows stdout/stderr with search
- [ ] **F3.2.5**: Edit schedule via cron expression input with preview

#### Integration Requirements
- [ ] **I3.2.1**: Jobs list includes running jobs with elapsed time
- [ ] **I3.2.2**: Trigger returns run ID for subsequent polling
- [ ] **I3.2.3**: Logs stream via Server-Sent Events during execution
- [ ] **I3.2.4**: Schedule update validates cron expression server-side

#### Response Handling
- [ ] **R3.2.1**: Job schema: `{ id, name, schedule, next_run, last_run, status }`
- [ ] **R3.2.2**: Run schema: `{ id, started_at, ended_at, exit_code, duration_ms }`
- [ ] **R3.2.3**: 423 Locked if job already running

---

## Deliverable 3: Workspace Manager Page

### 3.1 Description
Page (`/admin/workspaces`) for managing multi-tenant workspace isolation, user assignments, and resource quotas.

### 3.2 Frontend Implementation

| Component | Path | Type |
|-----------|------|------|
| `WorkspaceManager.jsx` | `frontend/src/pages/admin/WorkspaceManager.jsx` | Page |
| `WorkspaceCard.jsx` | `frontend/src/components/cards/WorkspaceCard.jsx` | Card |
| `UserAssignmentTable.jsx` | `frontend/src/components/admin/UserAssignmentTable.jsx` | Table |
| `QuotaSettings.jsx` | `frontend/src/components/admin/QuotaSettings.jsx` | Form |
| `CreateWorkspaceModal.jsx` | `frontend/src/components/modals/CreateWorkspaceModal.jsx` | Modal |

### 3.3 Backend Implementation

| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/admin/workspaces` | `list_workspaces()` |
| POST | `/api/v1/admin/workspaces` | `create_workspace()` |
| GET | `/api/v1/admin/workspaces/{ws_id}` | `get_workspace_details()` |
| DELETE | `/api/v1/admin/workspaces/{ws_id}` | `delete_workspace()` |
| GET | `/api/v1/admin/workspaces/{ws_id}/users` | `list_workspace_users()` |
| POST | `/api/v1/admin/workspaces/{ws_id}/users` | `assign_user()` |
| PUT | `/api/v1/admin/workspaces/{ws_id}/quotas` | `update_quotas()` |

### 3.4 End-to-End Acceptance Criteria

#### Functional Requirements
- [ ] **F3.3.1**: List all workspaces with user count, resource usage
- [ ] **F3.3.2**: Create workspace with name, description, initial quotas
- [ ] **F3.3.3**: Assign/remove users from workspace with role selection
- [ ] **F3.3.4**: Set quotas for storage, API calls, concurrent users
- [ ] **F3.3.5**: Delete workspace (soft delete with 30-day retention)

#### Integration Requirements
- [ ] **I3.3.1**: Workspace isolation verified in all data queries
- [ ] **I3.3.2**: User assignment sends `{ user_id, role }` body
- [ ] **I3.3.3**: Quota update validates against minimum requirements
- [ ] **I3.3.4**: Delete requires "delete" confirmation text input

#### Response Handling
- [ ] **R3.3.1**: Workspace schema: `{ id, name, users_count, storage_used_gb, api_calls_today }`
- [ ] **R3.3.2**: 403 Forbidden if user not workspace admin
- [ ] **R3.3.3**: 409 Conflict if workspace name already exists

---

## Deliverable 4: Environment Variables Modal

### 4.1 Description
Modal component accessible from Admin Settings for viewing and managing runtime environment configuration (read-only in production).

### 4.2 Frontend Implementation

| Component | Path | Type |
|-----------|------|------|
| `EnvironmentVariablesModal.jsx` | `frontend/src/components/modals/EnvironmentVariablesModal.jsx` | Modal |
| `EnvVarTable.jsx` | `frontend/src/components/admin/EnvVarTable.jsx` | Table |
| `EnvVarEditor.jsx` | `frontend/src/components/admin/EnvVarEditor.jsx` | Form |
| `EnvVarMaskToggle.jsx` | `frontend/src/components/controls/EnvVarMaskToggle.jsx` | Toggle |

### 4.3 Backend Implementation

| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/admin/env` | `list_env_vars()` |
| GET | `/api/v1/admin/env/{key}` | `get_env_var()` |
| PUT | `/api/v1/admin/env/{key}` | `set_env_var()` |
| DELETE | `/api/v1/admin/env/{key}` | `unset_env_var()` |
| GET | `/api/v1/admin/env/schema` | `get_env_schema()` |

### 4.4 End-to-End Acceptance Criteria

#### Functional Requirements
- [ ] **F3.4.1**: Table shows all non-secret env vars with values
- [ ] **F3.4.2**: Secret vars show masked values (********)
- [ ] **F3.4.3**: Click reveal button shows secret temporarily (10 seconds)
- [ ] **F3.4.4**: Edit vars in development mode only (read-only in prod)
- [ ] **F3.4.5**: Schema shows expected type, description, default

#### Integration Requirements
- [ ] **I3.4.1**: Secret vars require additional authentication step
- [ ] **I3.4.2**: Changes require server restart notification
- [ ] **I3.4.3**: Audit log records all view/edit actions
- [ ] **I3.4.4**: Validation against schema before save

#### Response Handling
- [ ] **R3.4.1**: Var schema: `{ key, value, is_secret, source, description }`
- [ ] **R3.4.2**: 403 Forbidden for secret access without elevated perms
- [ ] **R3.4.3**: 422 if value doesn't match expected type

---

## Deliverable 5: Feature Flags Page

### 5.1 Description
Page (`/admin/features`) for managing experimental feature toggles with user percentage targeting and A/B testing configuration.

### 5.2 Frontend Implementation

| Component | Path | Type |
|-----------|------|------|
| `FeatureFlagsPage.jsx` | `frontend/src/pages/admin/FeatureFlagsPage.jsx` | Page |
| `FeatureFlagCard.jsx` | `frontend/src/components/cards/FeatureFlagCard.jsx` | Card |
| `FlagTargetingConfig.jsx` | `frontend/src/components/admin/FlagTargetingConfig.jsx` | Form |
| `ABTestResults.jsx` | `frontend/src/components/admin/ABTestResults.jsx` | Widget |
| `CreateFlagModal.jsx` | `frontend/src/components/modals/CreateFlagModal.jsx` | Modal |

### 5.3 Backend Implementation

| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/admin/features` | `list_feature_flags()` |
| POST | `/api/v1/admin/features` | `create_feature_flag()` |
| PUT | `/api/v1/admin/features/{flag_id}` | `update_feature_flag()` |
| DELETE | `/api/v1/admin/features/{flag_id}` | `delete_feature_flag()` |
| GET | `/api/v1/admin/features/{flag_id}/evaluate` | `evaluate_flag()` |
| GET | `/api/v1/admin/features/{flag_id}/stats` | `get_flag_stats()` |

### 5.4 End-to-End Acceptance Criteria

#### Functional Requirements
- [ ] **F3.5.1**: List all flags with status, rollout percentage, targeting rules
- [ ] **F3.5.2**: Create flag with name, description, default value
- [ ] **F3.5.3**: Configure percentage rollout (0-100% of users)
- [ ] **F3.5.4**: Target by user role, workspace, or specific user IDs
- [ ] **F3.5.5**: A/B test results show conversion rates per variant

#### Integration Requirements
- [ ] **I3.5.1**: Flag evaluation includes user context for targeting
- [ ] **I3.5.2**: Stats show impressions, conversions per variant
- [ ] **I3.5.3**: Changes take effect immediately (no restart)
- [ ] **I3.5.4**: Audit log records flag state changes

#### Response Handling
- [ ] **R3.5.1**: Flag schema: `{ id, name, enabled, rollout_pct, targeting, variants[] }`
- [ ] **R3.5.2**: Evaluate returns `{ variant, context_matched }`
- [ ] **R3.5.3**: Stats schema: `{ impressions, conversions, conversion_rate }`

---

## Testing Requirements

### Unit Tests
| Component | Test File | Coverage Target |
|-----------|-----------|-----------------|
| DeploymentController | `tests/frontend/admin/DeploymentController.test.jsx` | 80% |
| OperationsDashboard | `tests/frontend/admin/OperationsDashboard.test.jsx` | 80% |
| blue_green_api | `tests/backend/api/test_blue_green_api.py` | 90% |
| ops_api | `tests/backend/api/test_ops_api.py` | 90% |

### Integration Tests
| Test Suite | Description |
|------------|-------------|
| `test_phase3_deployment_e2e.py` | Traffic split → switch → rollback |
| `test_phase3_jobs_e2e.py` | Schedule job → trigger → view logs |
| `test_phase3_workspace_e2e.py` | Create workspace → assign user → set quotas |
| `test_phase3_features_e2e.py` | Create flag → target users → evaluate |

---

## Deployment Checklist

- [ ] Blue-green infrastructure provisioned
- [ ] Job scheduler database tables created
- [ ] Workspace isolation middleware configured
- [ ] Feature flag SDK integrated in frontend
- [ ] Admin navigation updated
- [ ] RBAC policies for workspace admins configured
- [ ] Documentation complete

---

## Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Developer | | | |
| Reviewer | | | |
| QA | | | |
| Product Owner | | | |

---

*Phase 3 Implementation Plan - Version 1.0*
