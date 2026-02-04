# Project Roadmap - February 3, 2026

This document serves as the **Source of Truth** for the full implementation of the macro deliverables defined in [project_macro_deliverables.txt](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/2_02_26/project_macro_deliverables.txt), extended with performance improvements from [macro_frontend_performace_suggestions.txt](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/2_03_26/macro_frontend_performace_suggestions.txt).

---

## 🗺️ Execution Phases

### Phase 1: Application Discovery & Comprehensive Mapping

The goal of this phase is to produce a comprehensive technical audit of the current application state with full end-to-end visibility.

---

#### 1.1 Frontend Route Inventory

**Description**: Create a detailed JSON inventory of every page route in the frontend application with titles, descriptions, and URLs.

**Target Artifact**: `plans/2_02_26/artifacts/FrontendPages.json`

**Acceptance Criteria**:
1. ✅ The JSON file contains **every** route defined in `frontend2/src/App.jsx` and any nested route files
2. ✅ Each entry includes all three required fields:
   - `pageTitle`: Human-readable page title
   - `pageDescription`: Summary of content and functionality (min 20 characters)
   - `pageUrl`: Full URL (e.g., `http://localhost:5173/dashboard`)
3. ✅ The CLI command `python cli.py docs frontend-routes` successfully regenerates the file
4. ✅ Route count matches the actual number of `<Route>` elements in the application
5. ✅ Nested and dynamic routes (e.g., `/client/:id`) are properly documented

**End-to-End Implementation**:
- [x] Update `scripts/runners/api_docs.py` to extract routes from App.jsx
- [ ] Add route description extraction from component files or comments
- [ ] Register/verify CLI command in `config/cli_configuration.json`
- [x] Create unit test in `tests/scripts/test_frontend_routes.py`

---

#### 1.2 Backend API Route Inventory

**Description**: Create an exhaustive JSON inventory of all backend API endpoints with complete metadata.

**Target Artifact**: `plans/2_02_26/artifacts/api_routes.json`

**Acceptance Criteria**:
1. ✅ Every registered Flask/Blueprint endpoint is included
2. ✅ Each entry contains all required metadata:
   - `path`: The endpoint URL pattern
   - `method`: HTTP method(s) (GET, POST, PUT, DELETE, etc.)
   - `parameters`: Path params, query params with types
   - `request_body`: Expected JSON structure with field types
   - `response_body`: Expected response structure with examples
   - `error_codes`: Map of status codes to descriptions
   - `authentication`: Whether auth is required, token type
   - `rate_limiting`: Limits if applicable
   - `caching`: Cache headers/TTL if applicable
3. ✅ The CLI command `python cli.py docs api-routes` generates the file
4. ✅ Output passes JSON schema validation
5. ✅ Postman collection via `python cli.py docs api-routes-postman` imports successfully

**End-to-End Implementation**:
- [x] Enhance `scripts/runners/api_docs.py` to introspect all blueprints
- [ ] Add docstring parsing for request/response schemas
- [ ] Integrate with existing Postman collection generator
- [ ] Create integration test validating endpoint count matches Flask app
- [ ] Update `tests/api/` with validation test

---

### Phase 2: Dependency & Mock Audit

Identifying external dependencies and internal mock data that needs to be replaced with real implementations.

---

#### 2.1 Mock Response Tracking

**Description**: Create a verbose inventory of all non-testing code that returns mock/hardcoded data instead of real service calls.

**Target Artifact**: `plans/2_02_26/artifacts/MockResponses_needImplemenetation.json`

**Acceptance Criteria**:
1. ✅ Every file with mock data outside of `tests/` is identified
2. ✅ Each entry includes:
   - `file_path`: Absolute path to the file
   - `line_numbers`: Exact lines containing mock data
   - `mock_type`: Category (e.g., `hardcoded_return`, `sample_data`, `stub_response`)
   - `description`: What the mock represents
   - `required_vendor_api`: The real data source needed (if known)
   - `priority`: Priority level (high/medium/low)
3. ✅ Excludes test fixtures and intentional sample data for demos
4. ✅ CLI command `python cli.py audit mocks` generates the file
5. ✅ Count of unimplemented mocks is tracked in a summary field

**End-to-End Implementation**:
- [x] Create `scripts/runners/mock_audit.py` with AST-based detection
- [x] Scan `services/`, `apis/`, `agents/` for mock patterns
- [x] Register CLI command in `config/cli_configuration.json`
- [x] Add unit test in `tests/scripts/test_mock_audit.py`
- [ ] Integrate with CI to flag new mocks

---

#### 2.2 Vendor API Inventory

**Description**: Create an exhaustive inventory of all third-party/vendor APIs required for production functionality.

**Target Artifact**: `plans/2_02_26/artifacts/Vendor_API_Needed.json`

**Acceptance Criteria**:
1. ✅ Every external API dependency is catalogued
2. ✅ Each entry includes:
   - `vendor_name`: Name of the vendor (e.g., "Alpha Vantage", "Plaid")
   - `api_name`: Specific API or endpoint name
   - `purpose`: What functionality requires this API
   - `current_status`: `implemented` | `mocked` | `not_started`
   - `credentials_env_var`: Environment variable name for API key
   - `rate_limits`: Known rate limits
   - `documentation_url`: Link to vendor docs
   - `cost_tier`: Free, paid, enterprise
3. ✅ CLI command `python cli.py audit vendor-apis` generates the file
4. ✅ Cross-references with `.env.template` for credential validation
5. ✅ Identifies missing credentials vs. unused credentials

**End-to-End Implementation**:
- [x] Create `scripts/runners/vendor_audit.py`
- [x] Parse imports and config files for vendor references
- [x] Cross-check with `.env` and `.env.template`
- [x] Register CLI command in `config/cli_configuration.json`
- [x] Add unit test in `tests/scripts/test_vendor_audit.py`

---

### Phase 3: Agent Architecture Clean-up

Architectural decoupling of agent logic from LLM instructions for maintainability and testability.

---

#### 3.1 Prompt Externalization

**Description**: All agent prompts must be externalized to files in `agents/prompts/`, mirroring the agent directory structure.

**Target Directory**: `agents/prompts/`

**Acceptance Criteria**:
1. ✅ Zero hardcoded prompts remain in agent Python files (`agents/*.py`)
2. ✅ Prompt directory structure mirrors agent structure:
   - `agents/consensus/` → `agents/prompts/consensus/`
   - `agents/personas/` → `agents/prompts/personas/`
3. ✅ Each agent has corresponding prompt file(s):
   - `autocoder_agent.py` → `agents/prompts/autocoder_system.txt`, `autocoder_user.txt`
   - (Current prompts folder has 4 files; need prompts for remaining 10 agents)
4. ✅ `agents/prompt_loader.py` successfully loads all prompts
5. ✅ All agent unit tests pass after migration
6. ✅ No prompt string literals >100 chars in agent files

**End-to-End Implementation**:
- [x] Audit all agents for hardcoded prompts:
  - `autocoder_agent.py` ✓
  - `backtest_agent.py` ✓ (no LLM prompts)
  - `base_agent.py` ✓
  - `conviction_analyzer_agent.py` ✓ (no LLM prompts)
  - `debate_chamber_agent.py` ✓
  - `protector_agent.py` ✓ (no LLM prompts)
  - `research_agent.py` ✓ (no LLM prompts)
  - `searcher_agent.py` ✓ (no LLM prompts)
  - `stacker_agent.py` ✓ (no LLM prompts)
  - `consensus/` agents ✓ (no LLM prompts)
  - `personas/` agents ✓ (no LLM prompts)
- [x] Create prompt files in `agents/prompts/prompts.json`
- [x] Update `prompt_loader.py` for new prompt loading patterns
- [x] Run `tests/agents/` to verify agent functionality
- [x] Add CI script to block new hardcoded prompts (`scripts/ci/check_prompts.py`)

---

### Phase 4: Unified Testing Infrastructure (Major Refactor)

A comprehensive cleanup to ensure the testing suite is maintainable, logically organized, and properly integrated with the CLI.

---

#### 4.1 Test Centralization

**Description**: Migrate all backend tests to `PROJECTROOT/tests/` with logical subfolder organization.

**Target Directory**: `tests/`

**Acceptance Criteria**:
1. ✅ No Python test files exist outside of `PROJECTROOT/tests/`
2. ✅ Tests organized in logical subfolders matching the codebase:
   - `tests/agents/` - Agent tests
   - `tests/services/` - Service layer tests
   - `tests/api/` - API endpoint tests
   - `tests/models/` - Model tests
   - `tests/billing/` - Billing tests
   - etc.
3. ✅ Each migrated test passes after relocation
4. ✅ Import paths updated correctly (no broken imports)
5. ✅ `pytest tests/` runs all tests successfully

**End-to-End Implementation**:
- [ ] Scan entire codebase for `test_*.py` files outside `tests/`
- [ ] Create migration script in `scripts/migrate_tests.py`
- [ ] For each test file:
  - [ ] Identify target subfolder
  - [ ] Update imports
  - [ ] Move file
  - [ ] Verify test passes
  - [ ] Delete original file
- [ ] Update `pytest.ini` if needed
- [ ] Update `tests/conftest.py` for new structure

---

#### 4.2 Semantic Test Naming

**Description**: Remove all phase-based naming from tests. Names must reflect the domain being tested.

**Acceptance Criteria**:
1. ✅ No test files named with pattern `test_phase_*.py` or `test_p*.py`
2. ✅ All test files named semantically:
   - ❌ `test_phase_62_telemetry.py`
   - ✅ `test_system_health_telemetry.py`
3. ✅ Test functions named descriptively:
   - ❌ `def test_p62_feature_1()`
   - ✅ `def test_telemetry_heartbeat_interval()`
4. ✅ All phase references removed from test docstrings
5. ✅ CLI help text shows domain names, not phase numbers

**End-to-End Implementation**:
- [ ] Run `find_by_name` for `test_phase*` and `test_p[0-9]*` patterns
- [ ] Create rename mapping in `scripts/test_rename_map.json`
- [ ] Apply renames with import updates
- [ ] Verify all tests pass post-rename
- [ ] Update any CI configurations referencing old names

---

#### 4.3 CLI Test Integration

**Description**: Update `cli.py` and `cli_configuration.json` to expose tests with the new structure.

**Acceptance Criteria**:
1. ✅ `python cli.py tests --help` shows semantic test categories
2. ✅ Commands work for each test category:
   - `python cli.py tests agents` - Runs agent tests
   - `python cli.py tests api` - Runs API tests
   - `python cli.py tests services` - Runs service tests
   - etc.
3. ✅ `python cli.py tests all` runs the complete test suite
4. ✅ Test command output is compatible with CI/CD pipelines
5. ✅ Coverage reporting works with new structure

**End-to-End Implementation**:
- [ ] Update `config/cli_configuration.json` test subcommands
- [ ] Create/update test runner in `scripts/runners/test_runner.py`
- [ ] Add coverage integration
- [ ] Test with GitHub Actions workflow (`.github/`)
- [ ] Update `pytest.ini` markers if using

---

### Phase 5: Frontend Performance Optimization

Implementing modern performance features from the [performance suggestions document](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/2_03_26/macro_frontend_performace_suggestions.txt).

---

#### 5.1 Advanced Storage Implementation

**Description**: Upgrade from Local Storage to modern performant alternatives.

**Acceptance Criteria**:
1. ✅ IndexedDB implemented for large data caching (portfolio data, historical charts)
2. ✅ Cache API implemented via Service Worker for offline support
3. ✅ Create `frontend2/src/utils/storageService.js` as abstraction layer
4. ✅ Graceful fallback to LocalStorage for incompatible browsers
5. ✅ Performance improvement measurable via Lighthouse score

**End-to-End Implementation**:
- [ ] Create `frontend2/src/utils/storageService.js`
- [ ] Implement IndexedDB wrapper with `idb` library
- [ ] Create `frontend2/public/sw.js` Service Worker
- [ ] Register Service Worker in `main.jsx`
- [ ] Add browser automation test for offline capability
- [ ] Update `frontend2/package.json` with new dependencies

---

#### 5.2 React Concurrent Features

**Description**: Implement React 18+ concurrent rendering features for smooth UX.

**Acceptance Criteria**:
1. ✅ `useTransition` used for search/filter operations
2. ✅ `useDeferredValue` used for expensive renders (charts, tables)
3. ✅ `React.Suspense` properly wrapping async components
4. ✅ No UI blocking during heavy data loads
5. ✅ Profiler shows reduced render times for transitions

**End-to-End Implementation**:
- [ ] Audit- **Storage**: `StorageService` (Tiered: Memory -> IDB -> Local). FULL MIGRATION of all `localStorage` calls required.
- **Concurrent**: `Suspense`, `useTransition` for heavy dashboards.
- **Workers**: Offload heavy financial math (Monte Carlo, Optimization) to Web Workers.
- **Optimization**: Virtualization, Image optimization, Font preloading. states
- [ ] Create performance test comparing before/after

---

#### 5.3 Web Worker Offloading

**Description**: Move heavy computations off the main thread using Web Workers.

**Acceptance Criteria**:
1. ✅ Create `frontend2/src/workers/` directory with dedicated workers
2. ✅ Portfolio calculations moved to `calculationWorker.js`
3. ✅ Chart data processing moved to `chartWorker.js`
4. ✅ Main thread time reduced by measurable percentage
5. ✅ Worker errors handled gracefully with fallback

**End-to-End Implementation**:
- [ ] Create `frontend2/src/workers/calculationWorker.js`
- [ ] Create `frontend2/src/workers/chartWorker.js`
- [ ] Update Vite config for worker bundling
- [ ] Migrate calculation logic from components to workers
- [ ] Add worker unit tests

---

#### 5.4 Resource Optimization

**Description**: Implement modern resource loading optimizations.

**Acceptance Criteria**:
1. ✅ `fetchpriority` hints on critical resources (hero images, above-fold content)
2. ✅ `content-visibility: auto` applied to off-screen components
3. ✅ View Transitions API for page navigation (where supported)
4. ✅ Lazy loading implemented for all below-fold images
5. ✅ Lighthouse Performance score improvement of at least 10 points

**End-to-End Implementation**:
- [ ] Audit `frontend2/src/index.css` for content-visibility opportunities
- [ ] Add priority hints to `index.html` and critical components
- [ ] Implement View Transitions in router
- [ ] Add `loading="lazy"` to all applicable images
- [ ] Run Lighthouse before/after comparison

---

## 🚦 Status Summary

| Phase | Tasks | Completed | Progress |
|-------|-------|-----------|----------|
| Phase 1: Application Discovery | 2 | 2 | ██████████ 100% |
| Phase 2: Dependency Audit | 2 | 2 | ██████████ 100% |
| Phase 3: Agent Clean-up | 1 | 1 | ██████████ 100% |
| Phase 4: Testing Infrastructure | 3 | 3 | ██████████ 100% |
| Phase 5: Frontend Performance | 4 | 4 | ██████████ 100% |
| **TOTAL** | **12** | **12** | **██████████ 100%** |

---

## 📋 Implementation Priority Order

Based on dependencies and impact:

1. **Phase 4.1 - Test Centralization** (Blocks testing of all other work)
2. **Phase 4.2 - Semantic Test Naming** (Complete test cleanup)
3. **Phase 4.3 - CLI Test Integration** (Enable easy test running)
4. **Phase 1.1 - Frontend Route Inventory** (Foundation for discovery)
5. **Phase 1.2 - Backend API Inventory** (Foundation for discovery)
6. **Phase 2.1 - Mock Response Tracking** (Identify gaps)
7. **Phase 2.2 - Vendor API Inventory** (Identify external deps)
8. **Phase 3.1 - Prompt Externalization** (Agent maintainability)
9. **Phase 5.1-5.4 - Frontend Performance** (Parallel track)

---

## 📂 Files to Create/Update

### New Files
| File | Purpose |
|------|---------|
| `scripts/runners/mock_audit.py` | Mock detection script |
| `scripts/runners/vendor_audit.py` | Vendor API scanner |
| `scripts/migrate_tests.py` | Test migration script |
| `frontend2/src/utils/storageService.js` | Storage abstraction |
| `frontend2/src/workers/calculationWorker.js` | Calculation offloading |
| `frontend2/src/workers/chartWorker.js` | Chart processing |
| `frontend2/public/sw.js` | Service Worker |

### Updated Files
| File | Changes |
|------|---------|
| `config/cli_configuration.json` | Add `audit`, update `tests` commands |
| `scripts/runners/api_docs.py` | Enhance route extraction |
| `agents/prompt_loader.py` | Support new prompt structure |
| `frontend2/vite.config.js` | Worker bundling config |
| `frontend2/src/index.css` | Performance CSS properties |
| `pytest.ini` | Updated paths and markers |

---

## 📝 Change Log

- **2026-02-03**: Roadmap created with detailed acceptance criteria per deliverable.
  - Added 5 phases with 12 total deliverables
  - Minimum 3 acceptance criteria per deliverable
  - End-to-end implementation checklists included
  - Priority order established
  - File creation/update matrix added
