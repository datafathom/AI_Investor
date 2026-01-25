# Phase 23: API Marketplace & Integration Manager

> **Phase 66** | Status: `[x]` Completed
> Last Updated: 2026-01-18
> Verification: Verified via browser (Screenshot: `screenshots/Phase_23_API_Dashboard.png`)
> Strategic Importance: Allows the ecosystem to ingest 'New Senses' and adapt to changing market landscapes.

---

## Overview

Hub for connecting third-party data providers and external webhooks for system extensibility.

---

## Sub-Deliverable 66.1: Third-party Data Connector (Alpha Vantage, Polygon, FRED)

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/API/DataConnectors.jsx` | Connector widget |
| `[NEW]` | `frontend2/src/widgets/API/DataConnectors.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/API/ConnectorCard.jsx` | Per-provider card |
| `[NEW]` | `frontend2/src/services/apiIntegrationService.js` | Integration service |

### Verbose Acceptance Criteria

1. **Real-time Ping Status**
   - [ ] "Ping" status for all active data providers
   - [ ] Green (healthy), Yellow (slow), Red (down)
   - [ ] Last response time display
   - [ ] Auto-refresh every 30 seconds

2. **Rate-Limit Utilization Gauges**
   - [ ] Visual gauge per provider
   - [ ] Daily/monthly usage vs limit
   - [ ] "Near Limit" warning at 80%
   - [ ] Historical usage chart

3. **Automatic Failover**
   - [ ] Toggle to enable failover
   - [ ] Configure primary → backup provider
   - [ ] Failover triggers transparently
   - [ ] Notification when failover active

4. **Provider Management**
   - [ ] Add new provider configuration
   - [ ] Test connection before save
   - [ ] Disable/enable providers
   - [ ] Priority ordering

### Backend Requirements

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/integrations` | GET/POST | List/add integrations |
| `/api/v1/integrations/:id/ping` | GET | Health check |
| `/api/v1/integrations/:id/usage` | GET | Rate limit usage |

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `DataConnectors.test.jsx` | Connectors list, ping status |
| `ConnectorCard.test.jsx` | Status display, rate gauge |
| `apiIntegrationService.test.js` | Health check, failover logic |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 66.2: API Key Encryption/Vaulting UI

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/API/KeyVault.jsx` | Vault widget |
| `[NEW]` | `frontend2/src/widgets/API/KeyVault.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/API/KeyAccess.jsx` | Access log |

### Verbose Acceptance Criteria

1. **Masked Key Display**
   - [ ] Keys masked by default: `sk-***...***abc`
   - [ ] "Reveal" button with session re-auth
   - [ ] Auto-hide after 30 seconds
   - [ ] Copy button (copies full key)

2. **Access Audit Log**
   - [ ] Log who (user or agent) accessed vault
   - [ ] Timestamp and IP address
   - [ ] Action type: View, Create, Delete, Use
   - [ ] Export for security review

3. **HashiCorp Vault Integration**
   - [ ] Backend integration with Vault
   - [ ] Secret rotation support
   - [ ] Version history per key
   - [ ] Lease expiration management

4. **Key Management**
   - [ ] Add/rotate/delete keys
   - [ ] Labels for organization
   - [ ] Expiration reminders
   - [ ] "About to Expire" alerts

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `KeyVault.test.jsx` | Mask/reveal, add/delete keys |
| `KeyAccess.test.jsx` | Audit log display, filter |

### Test Coverage Target: **90%** (security-critical)

---

## Sub-Deliverable 66.3: Custom Webhook Trigger Configuration

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/API/WebhookConfig.jsx` | Webhook widget |
| `[NEW]` | `frontend2/src/widgets/API/WebhookConfig.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/API/PayloadBuilder.jsx` | Payload editor |

### Verbose Acceptance Criteria

1. **Visual Payload Builder**
   - [ ] Liquid-template support for dynamic messages
   - [ ] Variable picker: {{ticker}}, {{price}}, {{alert_type}}
   - [ ] JSON preview
   - [ ] Template validation

2. **Test Send Button**
   - [ ] "Send Test" button
   - [ ] Real-time response log
   - [ ] Success/failure indicator
   - [ ] Debug information for failures

3. **Integration Targets**
   - [ ] Slack webhook URL
   - [ ] Discord webhook URL
   - [ ] PagerDuty integration key
   - [ ] Custom HTTP endpoint

4. **Filtering Configuration**
   - [ ] Filter by alert severity
   - [ ] Filter by specific agent persona
   - [ ] Schedule: Active hours only
   - [ ] Rate limiting to prevent spam

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `WebhookConfig.test.jsx` | Config save, test send |
| `PayloadBuilder.test.jsx` | Template editing, variable insertion |

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/architect/api`

**Macro Task:** The Architect

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Individual phase plan |

