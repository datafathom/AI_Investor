# Phase 58: Estate Planning & Inheritance Protocol Wizard

> **Phase ID**: 58 | Status: `[x]` Completed
> Last Updated: 2026-01-18
> Strategic Importance: Extends the 'Life' of the financial ecosystem beyond the primary warden.

---

## Overview

Configurator for succession logic and the 'Dead Man's Switch'.

---

## Sub-Deliverable 58.1: Dead Man's Switch Configuration Interface

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Estate/DeadManSwitch.jsx` | Safety mechanism |
| `[NEW]` | `frontend2/src/widgets/Estate/DeadManSwitch.css` | Styling |
| `[NEW]` | `frontend2/src/stores/estateStore.js` | Estate state management |
| `[NEW]` | `services/security/estate_service.py` | Succession logic |
| `[NEW]` | `web/api/estate_api.py` | REST endpoints |

### Verbose Acceptance Criteria

1. **Countdown Timer**
   - [ ] Visual 'Time to Trigger' with high-contrast colors
   - [ ] Configurable heartbeat interval (7-90 days)
   - [ ] Reset on any platform activity

2. **Multi-Channel Verification**
   - [ ] SMS, Email, App push for heartbeat
   - [ ] Configurable channels
   - [ ] Fallback chain

3. **Encrypted Beneficiary Keys**
   - [ ] Keys encrypted until trigger fires
   - [ ] Verified via immutable audit log
   - [ ] Multi-sig option for high-value estates

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `DeadManSwitch.test.jsx` | Countdown displays, reset works, channels configurable |
| `estateStore.test.js` | Timer persistence, trigger logic |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/security/test_estate_service.py` | `test_heartbeat_detection`, `test_key_encryption`, `test_trigger_execution` |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 58.2: Beneficiary Asset Allocation Mapping

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Estate/BeneficiaryTree.jsx` | Allocation tree |
| `[NEW]` | `frontend2/src/widgets/Estate/BeneficiaryTree.css` | Styling |

### Verbose Acceptance Criteria

1. **Drag-and-Drop Allocation**
   - [ ] Percentage balance checking (must sum to 100%)
   - [ ] Real-time validation
   - [ ] Visual split indicators

2. **Document Vault Linking**
   - [ ] Link specific assets to Trust deeds
   - [ ] Corporate resolution references
   - [ ] Document status indicators

3. **Estate Tax Simulation**
   - [ ] Per-beneficiary tax impact
   - [ ] Based on jurisdictional law
   - [ ] What-if scenarios

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `BeneficiaryTree.test.jsx` | Drag works, percentages validate, tax displays |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/security/test_estate_service.py` | `test_allocation_validation`, `test_tax_calculation`, `test_document_linking` |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 58.3: Trust/Entity Legal Structure Visualizer (Neo4j)

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Estate/EntityGraph.jsx` | Graph visualization |
| `[NEW]` | `frontend2/src/widgets/Estate/EntityGraph.css` | Styling |

### Verbose Acceptance Criteria

1. **Node Types**
   - [ ] `ENTITY`, `TRUST`, `INDIVIDUAL` node types
   - [ ] `OWNS`, `BENEFICIARY_OF` edge types
   - [ ] Color-coded by type

2. **Hover Details**
   - [ ] Tax ID display
   - [ ] Jurisdiction (Delaware LLC, Wyoming Trust)
   - [ ] Formation date

3. **Corporate Resolution Generator**
   - [ ] One-click generation for structural changes
   - [ ] Stored in Document Vault
   - [ ] Template library

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `EntityGraph.test.jsx` | Graph renders, hover works, resolution generates |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/security/test_estate_service.py` | `test_entity_graph_query`, `test_resolution_template`, `test_vault_storage` |

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/strategist/estate`

**Macro Task:** Ecosystem Life Extension

---

## Verification Plan

### Unit Tests
```bash
# Frontend
cd frontend2 && npm run test -- --coverage --testPathPattern=Estate

# Backend
.\venv\Scripts\python.exe -m pytest tests/security/test_estate_service.py -v --cov=services/security
```

### E2E Browser Tests
```bash
.\venv\Scripts\python.exe cli.py dev
# Navigate to http://localhost:5173/strategist/estate
# Verify: Dead man's switch configurable, allocation tree works, entity graph displays
```

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 58 detailed implementation plan |
