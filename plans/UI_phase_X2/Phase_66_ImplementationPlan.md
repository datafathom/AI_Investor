# Phase 66: API Marketplace & Integration Manager

> **Phase ID**: 66 | Status: `[x]` Completed
> Last Updated: 2026-01-18
> Strategic Importance: Allows the ecosystem to ingest 'New Senses' and adapt to changing market landscapes.

---

## Overview

Hub for connecting third-party data providers and external webhooks.

---

## Sub-Deliverable 66.1: Third-party Data Connector (Alpha Vantage, Polygon, FRED)

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/API/DataConnector.jsx` | Provider manager |
| `[NEW]` | `frontend2/src/widgets/API/DataConnector.css` | Styling |
| `[NEW]` | `frontend2/src/stores/apiStore.js` | API state |
| `[NEW]` | `services/integration/api_connector_service.py` | Connector logic |
| `[NEW]` | `web/api/integration_api.py` | REST endpoints |

### Verbose Acceptance Criteria

1. **Real-time Ping Status**
   - [ ] Sub-second health polling per provider
   - [ ] Green/Yellow/Red status indicators
   - [ ] Latency measurement display

2. **Rate Limit Gauges**
   - [ ] Visual utilization bars
   - [ ] Prevent data-tap "Starvation"
   - [ ] Quota reset countdown

3. **Automatic Failover**
   - [ ] Toggle for secondary provider failover
   - [ ] Seamless data continuity
   - [ ] Failover event logging

### Test Coverage Target: **80%**

---

## Sub-Deliverable 66.2: API Key Encryption/Vaulting UI

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/API/KeyVault.jsx` | Key management |
| `[NEW]` | `frontend2/src/widgets/API/KeyVault.css` | Styling |

### Verbose Acceptance Criteria

1. **Masked Display**
   - [ ] Keys hidden by default (•••••)
   - [ ] Biometric re-auth to reveal
   - [ ] Copy-to-clipboard with auto-clear

2. **Audit Trail**
   - [ ] Track which agent/user accessed vault
   - [ ] Timestamp and action logging
   - [ ] Anomaly detection alerts

3. **HashiCorp Vault Integration**
   - [ ] Secure backend credential isolation
   - [ ] Secret rotation support
   - [ ] Lease management

### Test Coverage Target: **80%**

---

## Sub-Deliverable 66.3: Custom Webhook Trigger Configuration

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/API/WebhookBuilder.jsx` | Webhook config |
| `[NEW]` | `frontend2/src/widgets/API/WebhookBuilder.css` | Styling |

### Verbose Acceptance Criteria

1. **Payload Builder**
   - [ ] Visual template editor
   - [ ] Liquid template support
   - [ ] Dynamic JSON data insertion

2. **Test Functionality**
   - [ ] 'Send Test' button
   - [ ] Real-time response log
   - [ ] Status code display

3. **Filtering Options**
   - [ ] Filter by alert severity
   - [ ] Filter by Kafka topic
   - [ ] Filter by agent persona

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/architect/api`

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 66 |
