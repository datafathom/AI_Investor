# Phase 15: Estate Planning & Inheritance Protocol Wizard

> **Phase 58** | Status: `[x]` Completed  
> Last Updated: 2026-01-18 | Verified: Yes (Screenshot stored)  
> Strategic Importance: Extends the 'Life' of the financial ecosystem beyond the primary warden.

---

## Overview

Configurator for succession logic and the 'Dead Man's Switch' to ensure wealth preservation across generations.

---

## Sub-Deliverable 58.1: Dead Man's Switch Configuration Interface

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Estate/DeadMansSwitch.jsx` | Main widget |
| `[NEW]` | `frontend2/src/widgets/Estate/DeadMansSwitch.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/Estate/HeartbeatConfig.jsx` | Heartbeat settings |
| `[NEW]` | `frontend2/src/services/estateService.js` | Estate API service |

### Verbose Acceptance Criteria

1. **Visual Countdown Timer**
   - [ ] Display "Time to Trigger" prominently
   - [ ] Color gradient: Green (>30 days) → Yellow (7-30) → Red (<7)
   - [ ] "Reset" button with biometric confirmation
   - [ ] Historical reset activity log

2. **Multi-Channel Verification**
   - [ ] Configure heartbeat channels: SMS, Email, App Push
   - [ ] Require response from at least 2 channels
   - [ ] Configurable heartbeat interval (7-90 days)
   - [ ] Fallback escalation path

3. **Beneficiary Key Encryption**
   - [ ] Keys encrypted until trigger fires
   - [ ] AES-256 encryption with split-key scheme
   - [ ] "Test Trigger" mode for verification (not actual trigger)
   - [ ] Emergency contact notification on trigger

4. **Legal Disclaimer**
   - [ ] Required acknowledgment before activation
   - [ ] Recommendation to consult estate attorney
   - [ ] Document storage link for legal papers

### Backend Requirements

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/estate/dead-mans-switch` | GET/PUT | Configuration |
| `/api/v1/estate/heartbeat` | POST | Record heartbeat |
| `/api/v1/estate/test-trigger` | POST | Test mode |

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `DeadMansSwitch.test.jsx` | Timer displays, reset works, channel config |
| `HeartbeatConfig.test.jsx` | Interval settings, channel toggles |
| `estateService.test.js` | API calls, encryption handling |

### Test Coverage Target: **90%** (safety-critical)

---

## Sub-Deliverable 58.2: Beneficiary Asset Allocation Mapping

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Estate/BeneficiaryMap.jsx` | Allocation widget |
| `[NEW]` | `frontend2/src/widgets/Estate/BeneficiaryMap.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/Estate/BeneficiaryNode.jsx` | Individual node |

### Verbose Acceptance Criteria

1. **Drag-and-Drop Allocation Nodes**
   - [ ] Visual tree with beneficiary nodes
   - [ ] Drag to assign asset percentages
   - [ ] Real-time percentage balance checking (must sum to 100%)
   - [ ] Error state when allocation invalid

2. **Document Vault Integration**
   - [ ] Link specific assets to Trust deeds
   - [ ] Click to view linked legal document
   - [ ] "Missing Document" warning for unlinked assets
   - [ ] Upload new documents inline

3. **Estate Tax Impact Simulation**
   - [ ] Calculate estimated estate tax per beneficiary
   - [ ] Consider federal vs state exemptions
   - [ ] "What-if" sliders for asset values
   - [ ] Total tax burden summary

4. **Beneficiary Management**
   - [ ] Add/remove beneficiaries
   - [ ] Set contingent beneficiaries
   - [ ] Relationship type: Spouse, Child, Trust, Charity
   - [ ] Contact information for each

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `BeneficiaryMap.test.jsx` | Tree renders, drag allocation, validation |
| `BeneficiaryNode.test.jsx` | Node display, edit mode |

### Test Coverage Target: **85%**

---

## Sub-Deliverable 58.3: Trust/Entity Legal Structure Visualizer (Neo4j)

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Estate/EntityGraph.jsx` | Graph widget |
| `[NEW]` | `frontend2/src/widgets/Estate/EntityGraph.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/Estate/EntityDetails.jsx` | Detail panel |

### Verbose Acceptance Criteria

1. **Neo4j Node Types**
   - [ ] Node types: `ENTITY` (LLC, Corp), `TRUST`, `INDIVIDUAL`
   - [ ] Edge types: `OWNS`, `BENEFICIARY_OF`, `MANAGES`
   - [ ] Distinct visual styling per node type
   - [ ] Ownership percentages on edges

2. **Hover State Details**
   - [ ] Show Tax ID (EIN/SSN partially masked)
   - [ ] Jurisdiction: Delaware LLC, Wyoming Trust, etc.
   - [ ] Formation date and status (active/dissolved)
   - [ ] Primary contact/registered agent

3. **Corporate Resolution Generator**
   - [ ] One-click generate common resolutions
   - [ ] Templates: Add Member, Remove Member, Asset Transfer
   - [ ] Pre-fill with entity details
   - [ ] Export as PDF for signing

4. **Structure Operations**
   - [ ] Visualize "before and after" for restructuring
   - [ ] Simulate new entity addition
   - [ ] Tax impact of structural changes
   - [ ] "Optimize Structure" AI suggestion

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `EntityGraph.test.jsx` | Graph renders, nodes clickable, edges display |
| `EntityDetails.test.jsx` | Detail panel, masked IDs, jurisdiction |

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/strategist/estate`

**Macro Task:** The Strategist

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Individual phase plan |

