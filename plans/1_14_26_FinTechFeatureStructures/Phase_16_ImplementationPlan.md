# Phase 16: The 1% Position Sizing Rule Integration

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Risk Management Team

---

## 📋 Overview

**Description**: Enforce the Percentage-of-Balance approach for all automated and manual trade entries within the position sizing module.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)

---

## 🎯 Sub-Deliverables

### 16.1 1% Risk Hard Constraint `[ ]`

**Acceptance Criteria**: Implement a hard constraint within the sizing microservice limiting risk to exactly 1.0% (0.01) of total equity.

| Component | File Path | Status |
|-----------|-----------|--------|
| Position Sizer | `services/risk/position_sizer.py` | `[ ]` |
| Risk Constraint | `services/risk/risk_constraint.py` | `[ ]` |
| Config | `config/risk_limits.py` | `[ ]` |

---

### 16.2 Conservative 0.5% Preset `[ ]`

**Acceptance Criteria**: Configure a 0.5% (0.005) risk preset for conservative regimes as identified by the Warden.

| Risk Mode | Max Risk % | Trigger |
|-----------|------------|---------|
| Normal | 1.0% | Default |
| Conservative | 0.5% | High VIX (>25) |
| Ultra-Safe | 0.25% | Circuit Breaker Active |

---

### 16.3 Balance Query <10ms `[ ]`

**Acceptance Criteria**: Ensure that account balance is queried from TimescaleDB < 10ms prior to position size calculation.

| Component | File Path | Status |
|-----------|-----------|--------|
| Fast Balance Query | `services/portfolio/fast_balance.py` | `[ ]` |
| Cache Layer | `services/cache/balance_cache.py` | `[ ]` |

---

### 16.4 Bypass Prevention `[ ]`

**Acceptance Criteria**: Verify that any attempt to bypass the 1% rule results in an immediate trade block and audit log entry.

| Component | File Path | Status |
|-----------|-----------|--------|
| Bypass Detector | `services/risk/bypass_detector.py` | `[ ]` |
| Audit Logger | `services/audit/risk_audit.py` | `[ ]` |

---

### 16.5 Formula Documentation `[ ]`

**Acceptance Criteria**: Document the mathematical formula: (Balance × Risk%) / Stop Loss Distance = Position Size in the system manual.

| Component | File Path | Status |
|-----------|-----------|--------|
| Documentation | `docs/POSITION_SIZING.md` | `[ ]` |

---

## 📊 Phase Completion Summary

| Deliverable | Status | E2E Verified |
|-------------|--------|--------------|
| 16.1 1% Hard Constraint | `[ ]` | `[ ]` |
| 16.2 0.5% Preset | `[ ]` | `[ ]` |
| 16.3 Balance Query | `[ ]` | `[ ]` |
| 16.4 Bypass Prevention | `[ ]` | `[ ]` |
| 16.5 Documentation | `[ ]` | `[ ]` |

**Phase Status**: `[ ]` NOT STARTED

---

*Last verified: 2026-01-25*
