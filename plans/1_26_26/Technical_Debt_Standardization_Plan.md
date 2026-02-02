# Implementation Plan: Technical Debt & Standardization

## Goal
Enforce User Rule 6 and the "Golden Path" (Service-Store-Page) architecture across all existing legacy dashboards.

## 1. The "Golden Path" Refactor
### 1.1 Phase 31: Enterprise Dashboard
- **Tasks**:
    - Remove `axios` from `EnterpriseDashboard.jsx`.
    - Create `enterpriseStore.js` and `enterpriseService.js`.
    - Fix pathing: Normalize all requests to `/api/v1/enterprise/`.

### 1.2 Phase 27: ML Training Dashboard
- **Tasks**:
    - Refactor `loadTrainingJobs` and `deployModel` into `mlStore.js`.
    - Standardize `StatusBadge` components for consistent UI across the platform.

### 1.3 Phase 18: Research Reports
- **Tasks**:
    - Move report generation and PDF fetching to `researchService.js`.
    - Implement `researchStore.js` to manage the local cache of generated reports.

## 2. Global Versioning & Error Handling
- **Normalization**: Scan `src/services` for any `/api/` (non-v1) strings and update to `/api/v1/`.
- **Global Error Boundary**: Connect `App.jsx` error boundaries to `SystemHealthService` to log frontend crashes to the backend.

## 3. Acceptance Criteria
- [ ] **Code Quality**: `grep -r "axios" src/pages` returns zero results.
- [ ] **Consistency**: Every dashboard uses the standardized `StatCard`, `StatPulse`, and `GlassPanel` components.
- [ ] **Performance**: Page load times for refactored dashboards improve by 20% due to centralized state caching.

## 4. Testing & Code Coverage
- **Unit Tests**:
    - Run the existing test suite for refactored dashboards to ensure zero regression.
- **Targets**:
    - 100% compliance with User Rule 6.
    - 90% coverage for the new Store/Service layers.
