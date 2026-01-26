# Phase 19: Automated Stop Loss 'Sentinels'

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Trading Team

---

## 📋 Overview

**Description**: Deploy automated, non-negotiable stop-loss orders as 'Sentinels' for every open position to ensure zero unprotected exposure.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)

---

## 🎯 Sub-Deliverables

### 19.1 Mandatory Stop-Loss Validation `[ ]`

**Acceptance Criteria**: Verify that the brokerage API call fails if a trade request is submitted without a valid stop-loss parameter.

| Component | File Path | Status |
|-----------|-----------|--------|
| SL Validator | `services/trading/stop_loss_validator.py` | `[ ]` |
| Order Validator | `services/trading/order_validator.py` | `[ ]` |

---

### 19.2 Sentinel Distance Monitor `[ ]`

**Acceptance Criteria**: Implement 'Sentinel' logic that monitors the distance of current price to the stop-loss level every 100ms.

| Component | File Path | Status |
|-----------|-----------|--------|
| Sentinel Monitor | `services/risk/sentinel_monitor.py` | `[ ]` |
| Distance Calculator | `services/risk/sl_distance.py` | `[ ]` |

---

### 19.3 Stop-Loss Removal Block `[ ]`

**Acceptance Criteria**: Block all manual or autonomous commands to remove a stop-loss without liquidating the entire position.

| Component | File Path | Status |
|-----------|-----------|--------|
| Removal Blocker | `services/risk/sl_removal_blocker.py` | `[ ]` |
| Compliance Gate | `services/compliance/sl_compliance.py` | `[ ]` |

---

### 19.4 Emergency Kill Topic Broadcasting `[ ]`

**Acceptance Criteria**: Broadcast all stop-loss trigger events to the `emergency-kill` Kafka topic with < 100ms latency.

| Component | File Path | Status |
|-----------|-----------|--------|
| Kill Publisher | `services/kafka/kill_publisher.py` | `[ ]` |
| Emergency Handler | `services/trading/emergency_handler.py` | `[ ]` |

---

### 19.5 Stop-Loss Audit Trail `[ ]`

**Acceptance Criteria**: Persist all stop-loss modification events (trailing stops) in the TimescaleDB audit log for compliance.

| Component | File Path | Status |
|-----------|-----------|--------|
| SL Audit Logger | `services/audit/sl_audit.py` | `[ ]` |
| Migration | `migrations/019_sl_audit.sql` | `[ ]` |

---

## 📊 Phase Completion Summary

| Deliverable | Status | E2E Verified |
|-------------|--------|--------------|
| 19.1 Mandatory Validation | `[ ]` | `[ ]` |
| 19.2 Sentinel Monitor | `[ ]` | `[ ]` |
| 19.3 Removal Block | `[ ]` | `[ ]` |
| 19.4 Kill Broadcasting | `[ ]` | `[ ]` |
| 19.5 Audit Trail | `[ ]` | `[ ]` |

**Phase Status**: `[ ]` NOT STARTED

---

*Last verified: 2026-01-25*
