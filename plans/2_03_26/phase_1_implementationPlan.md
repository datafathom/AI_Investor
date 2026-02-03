# Phase 1: Application Discovery & Comprehensive Mapping
## Implementation Plan - Source of Truth

**Parent Roadmap**: [ROADMAP_2_03_26.md](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/2_03_26/ROADMAP_2_03_26.md)

---

## 📋 Phase Overview

| Attribute | Value |
|-----------|-------|
| **Phase Number** | 1 |
| **Focus Area** | Application Discovery & Mapping |
| **Deliverables** | 2 (Frontend Routes + API Inventory) |
| **Estimated Effort** | 3-4 days |
| **Dependencies** | None (Foundation phase) |

---

## 1.1 Frontend Route Inventory

### Goal
Create a comprehensive JSON inventory of every page route in the frontend application.

### Target Artifact
`notes/FrontendPages.json`

---

### Detailed Implementation

#### Backend Files to Create/Modify

| File | Action | Purpose |
|------|--------|---------|
| [scripts/runners/frontend_docs.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/runners/frontend_docs.py) | **CREATE** | Main script for extracting frontend routes |
| [config/cli_configuration.json](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/config/cli_configuration.json) | **MODIFY** | Register `docs frontend-routes` command |

#### Implementation Steps

1. **Create Route Extraction Script**
   ```python
   # scripts/runners/frontend_docs.py
   
   Functions to implement:
   - extract_routes_from_app_jsx() -> List[RouteInfo]
   - parse_route_component(component_path: str) -> Optional[str]  # Extract description
   - build_frontend_pages_json(routes: List[RouteInfo]) -> dict
   - save_artifact(data: dict, output_path: str) -> None
   ```

2. **Route Detection Logic**
   - Parse `frontend2/src/App.jsx` for all `<Route>` elements
   - Extract: `path`, `element` component name
   - Resolve component file to extract page description from:
     - JSDoc comments
     - Component docstrings
     - File header comments
   - Support nested routes (children)
   - Support dynamic segments (`:id`, `:symbol`, etc.)

3. **Output Schema**
   ```json
   [
     {
       "pageTitle": "Dashboard",
       "pageDescription": "Main dashboard with portfolio overview, market data widgets, and quick actions",
       "pageUrl": "http://localhost:5173/dashboard",
       "componentPath": "pages/Dashboard.jsx",
       "routeType": "protected",
       "dynamicParams": []
     }
   ]
   ```

---

### Frontend Files Referenced (Read-Only during Phase 1)

These are the source files that will be **parsed** to extract route information:

| File | Line Count | Purpose |
|------|------------|---------|
| [App.jsx](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/frontend2/src/App.jsx) | ~1200 | Main router with all route definitions |

#### Pages Directory (130 files to catalog)
<details>
<summary>Click to expand full pages list</summary>

| Page Component | Path Pattern |
|----------------|--------------|
| `Dashboard.jsx` | `/dashboard` |
| `AIAssistantDashboard.jsx` | `/ai-assistant` |
| `AIPredictionsDashboard.jsx` | `/ai-predictions` |
| `APIDashboard.jsx` | `/api` |
| `AdvancedChartingDashboard.jsx` | `/charting` |
| `AdvancedOrdersDashboard.jsx` | `/orders` |
| `AdvancedPortfolioAnalytics.jsx` | `/portfolio/analytics` |
| `AdvancedRiskDashboard.jsx` | `/risk` |
| `AlgorithmicTradingDashboard.jsx` | `/algo-trading` |
| `AnalyticsOptions.jsx` | `/options/analytics` |
| `AssetsDashboard.jsx` | `/assets` |
| `AuditDashboard.jsx` | `/audit` |
| `AutoCoderDashboard.jsx` | `/autocoder` |
| `AutoCoderSandbox.jsx` | `/autocoder/sandbox` |
| `BacktestPortfolio.jsx` | `/backtest` |
| `BillPaymentDashboard.jsx` | `/bills` |
| `Billing.jsx` | `/billing` |
| `BrokerageAccount.jsx` | `/brokerage` |
| `BudgetingDashboard.jsx` | `/budgeting` |
| `CashFlowDashboard.jsx` | `/cash-flow` |
| `Chat.jsx` | `/chat` |
| `CommunityForumsDashboard.jsx` | `/community` |
| `ComplianceDashboard.jsx` | `/compliance` |
| `CorporateDashboard.jsx` | `/corporate` |
| `CreditMonitoringDashboard.jsx` | `/credit` |
| `CryptoDashboard.jsx` | `/crypto` |
| `CurrencyDashboard.jsx` | `/currency` |
| `DebateRoom.jsx` | `/debate` |
| `DesignSystem.jsx` | `/design-system` |
| `DeveloperPlatformDashboard.jsx` | `/developer` |
| `EducationPlatformDashboard.jsx` | `/education` |
| `EnterpriseDashboard.jsx` | `/enterprise` |
| `EstateDashboard.jsx` | `/estate` |
| `EstatePlanningDashboard.jsx` | `/estate-planning` |
| `EvolutionDashboard.jsx` | `/evolution` |
| `FinancialPlanningDashboard.jsx` | `/planning` |
| `FixedIncomeDashboard.jsx` | `/fixed-income` |
| `GlobalScanner.jsx` | `/scanner` |
| `GoogleAuthCallback.jsx` | `/auth/google/callback` |
| `ImpactDashboard.jsx` | `/impact` |
| `InstitutionalToolsDashboard.jsx` | `/institutional` |
| `IntegrationsDashboard.jsx` | `/integrations` |
| `MLTrainingDashboard.jsx` | `/ml-training` |
| `MacroDashboard.jsx` | `/macro` |
| `MarginDashboard.jsx` | `/margin` |
| `MarketplaceDashboard.jsx` | `/marketplace` |
| `MasterOrchestrator.jsx` | `/orchestrator` |
| `MissionControl.jsx` | `/mission-control` |
| `MobileDashboard.jsx` | `/mobile` |
| `NewsSentimentDashboard.jsx` | `/news` |
| `OptionsAnalytics.jsx` | `/options` |
| `OptionsStrategyDashboard.jsx` | `/options/strategy` |
| `PaperTradingDashboard.jsx` | `/paper-trading` |
| `PoliticalAlpha.jsx` | `/political` |
| `PortfolioAttribution.jsx` | `/portfolio/attribution` |
| `PortfolioOptimizationDashboard.jsx` | `/portfolio/optimization` |
| `ResearchReportsDashboard.jsx` | `/research` |
| `RetirementPlanningDashboard.jsx` | `/retirement` |
| `RoleOverview.jsx` | `/roles` |
| `ScenarioDashboard.jsx` | `/scenarios` |
| `SentinelStrategyDashboard.jsx` | `/sentinel` |
| `Settings.jsx` | `/settings` |
| `SocialClassMaintenance.jsx` | `/social-class` |
| `SocialTradingDashboard.jsx` | `/social-trading` |
| `StrategyDistillery.jsx` | `/strategy` |
| `SystemHealthDashboard.jsx` | `/system-health` |
| `TaxDashboard.jsx` | `/tax` |
| `TaxOptimizationDashboard.jsx` | `/tax/optimization` |
| `Telemetry.jsx` | `/telemetry` |
| `TenantDashboard.jsx` | `/tenant` |
| `TerminalWorkspace.jsx` | `/terminal` |
| `VRCockpit.jsx` | `/vr` |
| `WatchlistsAlertsDashboard.jsx` | `/watchlists` |
| `Web3Dashboard.jsx` | `/web3` |
| `ZenMode.jsx` | `/zen` |

</details>

---

### Testing Requirements

#### Backend Tests (Python)

| Test File | Action | Coverage |
|-----------|--------|----------|
| `tests/scripts/test_frontend_docs.py` | **CREATE** | Unit tests for route extraction |

```python
# tests/scripts/test_frontend_docs.py

class TestFrontendDocs:
    def test_extract_routes_from_app_jsx(self):
        """Verify all routes are extracted from App.jsx"""
        
    def test_route_count_matches_expectation(self):
        """Ensure we capture approximately 70+ routes"""
        
    def test_dynamic_route_param_extraction(self):
        """Verify :id, :symbol params are captured"""
        
    def test_nested_routes_flattened(self):
        """Verify nested routes are properly handled"""
        
    def test_output_json_schema_valid(self):
        """Validate output against expected schema"""
```

**Run Command**:
```powershell
.\venv\Scripts\python.exe -m pytest tests/scripts/test_frontend_docs.py -v
```

#### Frontend Tests (Jest) - For this phase: NONE

> Phase 1.1 is backend-only (generating documentation). No frontend code changes occur.

---

### Acceptance Criteria Checklist

- [x] `python cli.py docs frontend-routes` executes without error
- [x] `FrontendPages.json` contains all routes from App.jsx
- [x] Each entry has `pageTitle`, `pageDescription`, `pageUrl`
- [x] Dynamic routes documented with parameter names
- [x] Route count ≥ 70 entries
- [x] JSON file passes schema validation
- [x] Unit tests pass: `pytest tests/scripts/test_frontend_docs.py`

---

## 1.2 Backend API Route Inventory

### Goal
Create an exhaustive JSON inventory of all backend API endpoints with complete metadata.

### Target Artifact
`notes/api_routes.json`

---

### Detailed Implementation

#### Backend Files to Create/Modify

| File | Action | Purpose |
|------|--------|---------|
| [scripts/runners/api_docs.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/runners/api_docs.py) | **MODIFY** | Enhance API introspection |
| [config/cli_configuration.json](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/config/cli_configuration.json) | **MODIFY** | Verify `docs api-routes` command |

#### Implementation Steps

1. **Enhance API Introspection**
   - Iterate through all Flask blueprints registered in the app
   - For each endpoint, extract:
     - URL rule pattern
     - HTTP methods allowed
     - View function name
     - Docstring for parameter documentation
     - Request body schema (from Pydantic models if available)
     - Response schema

2. **Docstring Parsing**
   - Parse docstrings for:
     - `:param` declarations → request parameters
     - `:returns` declarations → response structure
     - `:raises` declarations → error codes

3. **Output Schema**
   ```json
   [
     {
       "path": "/api/v1/portfolio/holdings",
       "method": "GET",
       "summary": "Get current portfolio holdings",
       "parameters": {
         "path": [],
         "query": [
           {"name": "account_id", "type": "string", "required": true}
         ]
       },
       "request_body": null,
       "response_body": {
         "type": "array",
         "items": {"$ref": "#/definitions/Holding"}
       },
       "error_codes": {
         "401": "Unauthorized - Missing or invalid JWT token",
         "404": "Account not found"
       },
       "authentication": "JWT Bearer Token",
       "rate_limiting": "100 requests/minute",
       "caching": "Cache-Control: max-age=60"
     }
   ]
   ```

---

### Backend Files Referenced (Introspection Sources)

The script will introspect all registered blueprints. Key directories:

| Directory | File Count | Purpose |
|-----------|------------|---------|
| [web/routes/](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/web/routes/) | ~50+ | Flask blueprint route files |
| [services/](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/services/) | 989 | Service layer (for docstrings) |
| [models/](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/models/) | 46 | Pydantic/SQLAlchemy models |

---

### Testing Requirements

#### Backend Tests (Python)

| Test File | Action | Coverage |
|-----------|--------|----------|
| `tests/scripts/test_api_docs.py` | **CREATE** | Unit tests for API introspection |

```python
# tests/scripts/test_api_docs.py

class TestApiDocs:
    def test_introspect_all_blueprints(self):
        """Verify all registered blueprints are discovered"""
        
    def test_api_route_count(self):
        """Ensure we capture 200+ API endpoints"""
        
    def test_http_methods_extracted(self):
        """Verify GET, POST, PUT, DELETE are captured"""
        
    def test_docstring_params_parsed(self):
        """Verify :param declarations become parameters"""
        
    def test_postman_collection_generated(self):
        """Verify Postman export works"""
```

**Run Command**:
```powershell
.\venv\Scripts\python.exe -m pytest tests/scripts/test_api_docs.py -v
```

#### Frontend Tests (Jest) - For this phase: NONE

> Phase 1.2 is backend-only (generating documentation). No frontend code changes occur.

---

### CLI Integration

| Command | Handler | Output |
|---------|---------|--------|
| `python cli.py docs api-routes` | `scripts.runners.api_docs:build_api_routes` | `api_routes.json` |
| `python cli.py docs api-routes-postman` | `scripts.runners.api_docs:build_api_routes_postman` | Postman collection |

---

### Acceptance Criteria Checklist

- [x] `python cli.py docs api-routes` executes without error
- [x] `api_routes.json` contains all registered endpoints
- [x] Each entry has: `path`, `method`, `parameters`, `request_body`, `response_body`, `error_codes`, `authentication`
- [x] Endpoint count ≥ 200 entries
- [ ] Postman collection imports successfully into Postman app
- [x] JSON file passes schema validation
- [x] Unit tests pass: `pytest tests/scripts/test_api_docs.py`

---

## 📊 Phase 1 Summary

### Files to Create

| File Path | Type | Purpose |
|-----------|------|---------|
| `scripts/runners/frontend_docs.py` | Python | Frontend route extraction |
| `tests/scripts/test_frontend_docs.py` | Python | Unit tests |
| `tests/scripts/test_api_docs.py` | Python | Unit tests |
| `plans/2_02_26/artifacts/FrontendPages.json` | JSON | Artifact output |
| `notes/api_routes.json` | JSON | Artifact output |

### Files to Modify

| File Path | Changes |
|-----------|---------|
| `scripts/runners/api_docs.py` | Enhance introspection logic |
| `config/cli_configuration.json` | Ensure commands registered |

### Frontend Changes

**None** - Phase 1 is entirely backend documentation work.

### Jest Test Requirements

**None** - No frontend code changes in this phase.

---

## ✅ Verification Plan

### Automated Tests

1. **Unit Tests**
   ```powershell
   .\venv\Scripts\activate
   python -m pytest tests/scripts/test_frontend_docs.py -v
   python -m pytest tests/scripts/test_api_docs.py -v
   ```

2. **CLI Command Verification**
   ```powershell
   python cli.py docs frontend-routes
   python cli.py docs api-routes
   python cli.py docs api-routes-postman
   ```

3. **Artifact Validation**
   - Verify JSON files exist at expected paths
   - Validate JSON schema
   - Check route/endpoint counts

### Manual Verification

1. Import Postman collection into Postman app
2. Execute sample requests against running backend
3. Verify all routes in `FrontendPages.json` are accessible in browser

---

## 📝 Change Log

- **2026-02-03**: Phase 1 implementation plan created with detailed file specifications.
