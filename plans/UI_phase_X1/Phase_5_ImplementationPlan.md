# Phase 5: Risk Management & Safety

> **Phases 48, 48.1, 48.2** | Status: `[x]` Completed
> Last Updated: 2026-01-18 | Verified: Yes (Screenshots stored)

---

## Overview

Implements critical safety systems including AI-assisted pre-trade risk checks, global kill switch for emergency freezing, and notification engine for institutional activity alerts.

---

## 48: Execution Shield - AI Risk Modal

### 48.1 Mandatory Risk Display

**Files to Create/Modify:**
- `[NEW]` `frontend2/src/components/Modals/PreTradeRiskModal.jsx`
- `[NEW]` `frontend2/src/components/Modals/PreTradeRiskModal.css`

**Acceptance Criteria:**
- [ ] Position Size display (shares/contracts)
- [ ] Margin Impact calculation (% of available margin)
- [ ] Sector Concentration check (max 25% per sector)
- [ ] "Confirm" button disabled until all checks pass

**Jest Tests Required:**
- [ ] `PreTradeRiskModal.test.jsx`: All fields render, button enable/disable logic

---

### 48.2 AI Risk Rating Badge

**Acceptance Criteria:**
- [ ] Badge colors: SAFE (green), CAUTION (yellow), DANGER (red)
- [ ] One-sentence logic justification from LLM
- [ ] Example: "CAUTION: This trade increases tech sector exposure to 28%"
- [ ] Prominent display at top of modal

**Jest Tests Required:**
- [ ] `PreTradeRiskModal.test.jsx`: Badge color matches risk level

---

### 48.3 Nancy Pelosi Index Display

**Acceptance Criteria:**
- [ ] Show if ticker has recent congressional trading activity
- [ ] Display trade direction, date, and volume
- [ ] Political alpha signal integration from Phase 37

---

### 48.4 Focus-Trap Implementation

**Acceptance Criteria:**
- [ ] Background workspace blurred (20px backdrop-filter)
- [ ] Tab navigation trapped within modal
- [ ] ESC or X closes modal
- [ ] Click outside does NOT close (intentional safety measure)

---

## 48.1: Global Kill Switch

### 48.1.1 Floating Kill Switch Button

**Files to Create/Modify:**
- `[NEW]` `frontend2/src/components/KillSwitch/KillSwitch.jsx`
- `[NEW]` `frontend2/src/components/KillSwitch/KillSwitch.css`

**Acceptance Criteria:**
- [ ] Persistent floating button (bottom-right corner)
- [ ] Red with warning icon (⚠️)
- [ ] Requires 3-second long-press to activate
- [ ] Socket.io/SignalR broadcast in <1 second

**Jest Tests Required:**
- [ ] `KillSwitch.test.jsx`: Long-press detection, broadcast trigger

---

### 48.1.2 Priority Kafka Bypass

**Acceptance Criteria:**
- [ ] Kill command supersedes all other outgoing messages
- [ ] Message format: `{ type: 'EMERGENCY_KILL', timestamp, userId }`
- [ ] Backend immediately halts all agent activity

---

### 48.1.3 System Frozen Overlay

**Files to Create/Modify:**
- `[NEW]` `frontend2/src/components/KillSwitch/FrozenOverlay.jsx`

**Acceptance Criteria:**
- [ ] Full-screen red-tinted overlay
- [ ] "SYSTEM FROZEN" text with timestamp
- [ ] Passcode entry field to unlock
- [ ] 6-digit numeric PIN

**Jest Tests Required:**
- [ ] `FrozenOverlay.test.jsx`: Overlay renders, passcode validation

---

### 48.1.4 Broker API Confirmation

**Acceptance Criteria:**
- [ ] Visual confirmation from Alpaca/Robinhood API within 1.5s
- [ ] Status: "Orders Cancelled", "Positions Closed" (if configured)
- [ ] Error handling if broker unreachable

---

## 48.2: Notification Engine

### 48.2.1 Toast Notifications

**Files to Create/Modify:**
- `[MODIFY]` `frontend2/src/components/Toaster.jsx`
- `[NEW]` `frontend2/src/hooks/useNotifications.js`

**Acceptance Criteria:**
- [ ] Non-blocking toast notifications
- [ ] Severity colors: INFO (blue), WARN (orange), CRITICAL (red)
- [ ] Auto-dismiss: INFO 5s, WARN 10s, CRITICAL requires manual dismiss
- [ ] Stack up to 5 notifications

**Jest Tests Required:**
- [ ] `useNotifications.test.js`: Add, dismiss, severity handling

---

### 48.2.2 Deep-Linking from Whale Flow

**Acceptance Criteria:**
- [ ] Click "Whale Flow Detected" notification
- [ ] Opens Options Chain widget with that ticker selected
- [ ] Pre-filters to relevant strike range

---

### 48.2.3 Heuristic-Based CRITICAL Alerts

**Acceptance Criteria:**
- [ ] Delta threshold: |Δ| > 0.8 on sweep
- [ ] OI threshold: Volume > 5x average OI
- [ ] Only significant institutional sweeps trigger CRITICAL

---

### 48.2.4 Alert Toggle Menu

**Files to Create/Modify:**
- `[NEW]` `frontend2/src/components/NotificationCenter/AlertSettings.jsx`

**Acceptance Criteria:**
- [ ] Toggle categories: Social Mentions, Risk Alerts, Whale Flow
- [ ] Persist preferences in localStorage
- [ ] "Do Not Disturb" master toggle

**Jest Tests Required:**
- [ ] `AlertSettings.test.jsx`: Toggle states persist, DND mode works

---

## Widget Registry Entries

```javascript
{
  id: 'kill-switch',
  name: 'Emergency Kill Switch',
  component: KillSwitch,
  category: 'Risk',
  defaultSize: { width: 80, height: 80 },
  isFloating: true
}
```

---

## Test Coverage Requirements

| Component | Unit Tests | Integration Tests |
|-----------|------------|-------------------|
| PreTradeRiskModal | ✓ | ✓ |
| KillSwitch | ✓ | ✓ |
| FrozenOverlay | ✓ | - |
| useNotifications | ✓ | - |
| AlertSettings | ✓ | - |

**Minimum Coverage Target:** 90% (critical safety systems)

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Higher test coverage for safety components |

