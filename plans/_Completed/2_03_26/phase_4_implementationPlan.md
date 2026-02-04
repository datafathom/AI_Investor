# Phase 4: Unified Testing Infrastructure
## Implementation Plan - Source of Truth

**Parent Roadmap**: [ROADMAP_2_03_26.md](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/2_03_26/ROADMAP_2_03_26.md)

---

## 📋 Phase Overview

| Attribute | Value |
|-----------|-------|
| **Phase Number** | 4 |
| **Focus Area** | Testing Infrastructure Cleanup |
| **Deliverables** | 3 (Centralization Gatekeeper, Semantic Naming, CLI Integration) |
| **Estimated Effort** | 4-5 days |
| **Dependencies** | None |

> [!CAUTION]
> This is a **major refactoring phase**. We found 84 existing test subdirectories. We must preserve this structure while ensuring NO test leaks out.

---

## 4.1 Test Centralization (App-Wide Enforcer)

### Goal
Ensure `tests/` is the **exclusive** home for testing logic.

### Current State (Verified)
- **Stranded Tests**: We found `scripts/util/debug_fastapi_test.py`. This is technically a utility, but arguably belongs in `tests/scripts/`.
- **Test Directory**: `tests/` contains 84 subdirectories (e.g., `tests/api`, `tests/agents`). This is good! The goal is to **lock this down**.

### Detailed Implementation

#### 1. The "Gatekeeper" Script
We will create a script `scripts/ci/check_test_locations.py` that fails the build if **Any** file matching `test_*.py` or `*_test.py` is found outside `tests/` (excluding `venv`, `node_modules`).

```python
# scripts/ci/check_test_locations.py
ALLOWED_ROOTS = ["tests/"]
FORBIDDEN_PATTERNS = ["test_*.py", "*_test.py"]

def scan():
    # ... logic to scan project root ...
    # Fail if "./services/my_service/test_logic.py" is found.
    pass
```

#### 2. Migration of Strays
We identified `scripts/util/debug_fastapi_test.py`.
- **Action**: Move to `tests/scripts/debug_fastapi_manual_test.py` or simply whitelist it if it's a dev tool not a test suite.
- **Decision**: Whitelist `scripts/util/` if usage is purely manual debugging, OR move to `tests/manual/`. Recommendation: Move to `tests/manual/`.

## 4.2 Semantic Test Naming (App-Wide)

### Goal
Remove "Phase X" or "Sprint Y" from filenames. Tests must be named after *what they test*.

### Implementation
1.  **Scanner**: `scripts/ci/check_test_names.py`.
    - Fails if file matches `*phase*`, `*sprint*`.
2.  **Renaming Campaign**:
    - `tests/unit/test_phase_62_telemetry.py` -> `tests/system/test_telemetry.py`
    - `tests/api/test_p45_portfolio.py` -> `tests/api/test_portfolio_api.py`

## 4.3 CLI Test Integration (App-Wide)

### Goal
A single entry point for all 84 test suites.

### Detailed Implementation

#### 1. `tests` Command Group (in `cli.py`)
We will expose granular commands mapping to the extensive folder structure found.

| Command | Subfolder Target |
|---------|------------------|
| `python cli.py tests all` | `tests/` |
| `python cli.py tests agents` | `tests/agents/` |
| `python cli.py tests api` | `tests/api/` |
| `python cli.py tests services` | `tests/services/` |
| `python cli.py tests frontend-util` | `tests/frontend_utils/` (if Python exist) |
| `python cli.py tests integration` | `tests/integration/` |
| `python cli.py tests unit` | `tests/unit/` |

#### 2. `pytest.ini` Configuration
- Ensure `testpaths = tests`
- Ensure `python_files = test_*.py`
- Add markers for `slow`, `integration`, `e2e` to allow filtering via CLI flags (e.g., `python cli.py tests all --quick`).

## 📊 Verification Plan
### Automated Tests
1.  **Gatekeeper Test**: `tests/scripts/test_check_test_locations.py`
    - Create a dummy `stranded_test.py` in root.
    - Run the check script -> Assert Failure.
    - Remove dummy -> Assert Success.
2.  **Naming Test**: `tests/scripts/test_check_test_names.py`
    - Create `tests/unit/test_phase_99.py`.
    - Run check -> Assert Failure.

### Manual Verification
- Run `python cli.py tests all --collect-only`.
    - **Success Criteria**: It must list tests from ALL 84 subdirectories. If it misses any folder (e.g., due to missing `__init__.py`), we must fix that folder immediately.
