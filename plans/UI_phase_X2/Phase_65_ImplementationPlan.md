# Phase 65: Mobile Portfolio Quick-Actions (V2)

> **Phase ID**: 65 | Status: `[x]` Completed
> Last Updated: 2026-01-18
> Strategic Importance: Empowers the 'Warden' with remote intervention capabilities from anywhere on Earth.

---

## Overview

Advanced mobile features for system oversight and emergency control.

---

## Sub-Deliverable 65.1: Biometric 'Kill Switch' for Android/iOS

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Mobile/KillSwitch.jsx` | Emergency button |
| `[NEW]` | `frontend2/src/widgets/Mobile/KillSwitch.css` | Styling |
| `[NEW]` | `services/emergency/mobile_kill_service.py` | Mobile integration |

### Verbose Acceptance Criteria

1. **Long Press Activation**
   - [ ] 3-second hold requirement
   - [ ] Haptic feedback intensity 1.0
   - [ ] Visual progress ring
   - [ ] Prevent accidental trigger

2. **Kafka Broadcast**
   - [ ] Immediate `emergency-kill` topic publish
   - [ ] < 100ms latency target
   - [ ] Confirmation receipt

3. **Desktop Sync**
   - [ ] Push notification to all linked instances
   - [ ] State synchronization
   - [ ] Audit trail entry

### Test Coverage Target: **80%**

---

## Sub-Deliverable 65.2: Push-Notification Trade Authorization (OAuth 2.0)

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Mobile/TradeAuth.jsx` | Authorization flow |
| `[NEW]` | `frontend2/src/widgets/Mobile/TradeAuth.css` | Styling |

### Verbose Acceptance Criteria

1. **Deep-Link Logic Summary**
   - [ ] Link to LLM Debate summary before approval
   - [ ] Trade rationale displayed
   - [ ] Risk assessment included

2. **Biometric Signature**
   - [ ] Required for trades > $10,000
   - [ ] OAuth 2.0 secure flow
   - [ ] Session expiry handling

3. **Time-Limited Approval**
   - [ ] 60-second window before auto-cancel
   - [ ] Visual countdown timer
   - [ ] Extension request option

### Test Coverage Target: **80%**

---

## Sub-Deliverable 65.3: Haptic-Feedback Real-time Alert Vibrations

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Mobile/HapticAlerts.jsx` | Vibration config |
| `[NEW]` | `frontend2/src/widgets/Mobile/HapticAlerts.css` | Styling |

### Verbose Acceptance Criteria

1. **Pattern Differentiation**
   - [ ] Single sharp pulse for 'Info'
   - [ ] Long heavy vibration for 'Critical'
   - [ ] Pattern library with previews

2. **Dynamic Intensity**
   - [ ] Frequency increases with Fear Index
   - [ ] Margin Danger level correlation
   - [ ] User sensitivity settings

3. **Quiet Hours**
   - [ ] Configurable quiet periods
   - [ ] Mandatory override for Black Swan events
   - [ ] Do Not Disturb integration

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/mobile/settings`

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 65 |
