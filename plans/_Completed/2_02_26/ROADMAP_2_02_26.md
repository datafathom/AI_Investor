# Project Roadmap - February 2, 2026

This document serves as the **Source of Truth** for the full implementation of the macro deliverables defined in [project_macro_deliverables.txt](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/2_02_26/project_macro_deliverables.txt).

---

## 🗺️ Execution Phases

### Phase 1: Application Discovery & Mapping
The goal of this phase is to produce a comprehensive technical audit of the current application state.

| Item | Description | Target Artifact |
| :--- | :--- | :--- |
| **1.1 Frontend Inventory** | List every page route with title and description. | `notes/FrontendPages.json` |
| **1.2 Backend API Inventory** | Detailed JSON of all API endpoints (methods, params, bodies, errors, auth, rate-limits). | `notes/api_routes.json` |

### Phase 2: Dependency & Mock Audit
Identifying external dependencies and internal "shortcuts" that need to be replaced with real implementations.

| Item | Description | Target Artifact |
| :--- | :--- | :--- |
| **2.1 Mock Response Tracking** | Verbose list of all non-testing code using mock data. | `notes/MockResponses_needImplemenetation.json` |
| **2.2 Vendor API Inventory** | Exhaustive list of third-party APIs used/needed. | `notes/Vendor_API_Needed.json` |

### Phase 3: Agent Clean-up (Externalized Prompts)
Architectural decoupling of agent logic from LLM instructions.

- [ ] **Directory Standardization**: Ensure `agents/prompts/` mirrors the `agents/` logic structure.
- [ ] **Prompt Extraction**: Zero hardcoded prompts in agent Python files.
- [ ] **Verification**: Ensure agents still initialize and process events correctly.

### Phase 4: Unified Testing Infrastructure (X)
A major cleanup to ensure the testing suite is maintainable and logically organized.

- **Centralization**: All backend tests must reside in `/tests/` in the project root.
- **Logical Grouping**: Subfolders like `agents/`, `billing/`, `wave/`, etc.
- **Semantic Naming**: No more "Phase-based" naming. Filenames must reflect the domain being tested.
- **CLI Integration**: Update `cli.py` to ensure help text and test runners reflect the new structure.

---

## 🚦 Status Summary

- **Total Tasks**: 10
- **Completed**: 0
- **Blocked**: 0
- **Progress**: [░░░░░░░░░░] 0%

---

## 📝 Change Log

- **2026-02-02**: Roadmap initialized based on `project_macro_deliverables.txt`.
