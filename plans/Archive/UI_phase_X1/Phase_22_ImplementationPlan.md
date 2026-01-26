# Phase 22: Mobile Portfolio Quick-Actions (V2)

> **Phase 65** | Status: `[x]` Completed  
> Last Updated: 2026-01-18 | Verified: Yes (Screenshot stored)  
> Strategic Importance: Empowers the 'Warden' with remote intervention capabilities from anywhere on Earth.

---

## Overview

Advanced mobile features for system oversight and emergency control when away from desktop.

---

## Sub-Deliverable 65.1: Biometric 'Kill Switch' for Android/iOS

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/mobile/BiometricKill.jsx` | Kill switch |
| `[NEW]` | `frontend2/src/mobile/BiometricKill.css` | Styling |
| `[NEW]` | `frontend2/src/hooks/useBiometricAuth.js` | Biometric hook |
| `[NEW]` | `frontend2/src/mobile/HapticFeedback.js` | Haptic utilities |

### Verbose Acceptance Criteria

1. **3-Second Long Press**
   - [ ] Require 3-second continuous press to activate
   - [ ] Progress indicator during press
   - [ ] Haptic feedback at 1s, 2s, and activation
   - [ ] Accidental press prevention

2. **Kafka Emergency Broadcast**
   - [ ] Immediate broadcast to `emergency-kill` topic
   - [ ] Target latency: <100ms
   - [ ] Retry logic if network delay
   - [ ] Acknowledgment confirmation

3. **Desktop Push Notification**
   - [ ] Push notification to all linked desktop instances
   - [ ] "Emergency Kill Activated by Mobile"
   - [ ] Timestamp and device info
   - [ ] Open Frozen Overlay on desktop

4. **Biometric Verification**
   - [ ] FaceID or TouchID required
   - [ ] Fallback to PIN
   - [ ] "Trust this device" option
   - [ ] Session timeout configuration

### Backend Requirements

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/mobile/kill-switch` | POST | Trigger emergency kill |
| `/api/v1/mobile/devices` | GET | Linked devices list |

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `BiometricKill.test.jsx` | Long-press detection, broadcast trigger |
| `useBiometricAuth.test.js` | Auth flow, fallback PIN |

### Test Coverage Target: **90%** (safety-critical)

---

## Sub-Deliverable 65.2: Push-Notification Trade Authorization (OAuth 2.0)

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/mobile/TradeAuth.jsx` | Authorization widget |
| `[NEW]` | `frontend2/src/mobile/TradeAuth.css` | Styling |
| `[NEW]` | `frontend2/src/mobile/TradePreview.jsx` | Trade details |

### Verbose Acceptance Criteria

1. **Deep-Link to Logic Summary**
   - [ ] Notification links to AI reasoning summary
   - [ ] View Debate Chamber discussion
   - [ ] "Why this trade?" explanation
   - [ ] Quick approve without full navigation

2. **Biometric Signature for Large Trades**
   - [ ] Required for trades >$10,000
   - [ ] Configurable threshold
   - [ ] Multiple biometric attempts allowed
   - [ ] Lock after 3 failures

3. **60-Second Auto-Cancel Window**
   - [ ] Visual countdown timer
   - [ ] Trade auto-cancelled if no response
   - [ ] "Extend Time" button for complex decisions
   - [ ] Notification when trade cancelled

4. **Trade Details Display**
   - [ ] Symbol, Direction, Quantity, Price
   - [ ] P&L impact estimate
   - [ ] Risk rating badge
   - [ ] Historical performance of similar trades

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `TradeAuth.test.jsx` | Auth flow, countdown, approval |
| `TradePreview.test.jsx` | Trade details display |

### Test Coverage Target: **90%**

---

## Sub-Deliverable 65.3: Haptic-Feedback Real-time Alert Vibrations

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/mobile/HapticAlerts.jsx` | Alert patterns |
| `[NEW]` | `frontend2/src/mobile/HapticAlerts.css` | Styling |
| `[NEW]` | `frontend2/src/mobile/AlertSettings.jsx` | Settings UI |

### Verbose Acceptance Criteria

1. **Severity-Based Vibration Patterns**
   - [ ] Single sharp pulse: INFO alerts
   - [ ] Double pulse: WARNING alerts
   - [ ] Long heavy vibration: CRITICAL alerts
   - [ ] Pattern library configurable

2. **Dynamic Intensity**
   - [ ] Vibration frequency tied to Fear Index
   - [ ] Intensity tied to Margin Danger
   - [ ] More urgent = more intense
   - [ ] Configurable sensitivity

3. **Quiet Hours Configuration**
   - [ ] User-defined quiet hours
   - [ ] Override for "Black Swan" alerts
   - [ ] Weekend/holiday settings
   - [ ] Per-alert-type overrides

4. **Testing Mode**
   - [ ] "Test Vibrations" button
   - [ ] Preview each pattern
   - [ ] Adjust intensity after testing
   - [ ] Reset to defaults

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `HapticAlerts.test.jsx` | Pattern triggering, intensity |
| `AlertSettings.test.jsx` | Settings save, quiet hours |

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/mobile/*` (React Native / PWA)

**Macro Task:** Cross-cutting (all macro tasks)

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Individual phase plan |

