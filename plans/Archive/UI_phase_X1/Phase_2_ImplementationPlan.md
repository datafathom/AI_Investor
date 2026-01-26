# Phase 2: Navigation & Core Widgets

> **Phases 45, 12, 6.2** | Status: `[ ]` Not Started  
> Last Updated: 2026-01-18

---

## Overview

Establishes specialized routes mirroring institutional-grade navigation (thinkorswim, Fidelity ATP) and implements core monitoring widgets for Fear/Greed sentiment and Kafka system health.

---

## 45: Advanced Logical Workspace Routing

### 45.1 Breadcrumb Navigation

**Files to Create/Modify:**
- `[NEW]` `frontend2/src/components/Navigation/Breadcrumbs.jsx`
- `[NEW]` `frontend2/src/components/Navigation/Breadcrumbs.css`

**Acceptance Criteria:**
- [ ] Dynamic path tracking: "Workspace > Terminal > AI Agent"
- [ ] Each segment is clickable for instant navigation
- [ ] Support deep-linking to agent-ID configurations: `/terminal/agent/abc123`
- [ ] Zustand integration for navigation state

**Jest Tests Required:**
- [ ] `Breadcrumbs.test.jsx`: Renders path segments, click navigation works

---

### 45.2 Analytics Options Route

**Files to Create/Modify:**
- `[NEW]` `frontend2/src/pages/AnalyticsOptions.jsx`
- `[NEW]` `frontend2/src/pages/AnalyticsOptions.css`

**Route:** `/analytics/options`

**Acceptance Criteria:**
- [ ] Fama-French 5-Factor model decomposition widget
- [ ] Gamma Exposure (GEX) metrics widget
- [ ] IV surface visualization placeholder
- [ ] Responsive grid layout

**Jest Tests Required:**
- [ ] `AnalyticsOptions.test.jsx`: Page renders, widgets mount correctly

---

### 45.3 Zustand State Persistence

**Files to Create/Modify:**
- `[MODIFY]` `frontend2/src/stores/navigationStore.js`

**Acceptance Criteria:**
- [ ] Full state persistence across route transitions
- [ ] No re-rendering lag on navigation
- [ ] State includes: current route, open windows, active symbol

**Jest Tests Required:**
- [ ] `navigationStore.test.js`: State persists across simulated route changes

---

### 45.4 Deep-Linking Support

**Acceptance Criteria:**
- [ ] URL params parsed on load: `/terminal?agent=abc123&symbol=AAPL`
- [ ] Browser back/forward preserves state
- [ ] Shareable configuration URLs

---

## 12: D3.js Fear & Greed Composite Gauge

### 12.1 SVG Needle Implementation

**Files to Create/Modify:**
- `[MODIFY]` `frontend2/src/components/FearGreedGauge.jsx`
- `[NEW]` `frontend2/src/widgets/FearGreedWidget.jsx`

**Acceptance Criteria:**
- [ ] D3.js SVG-based semi-circular gauge
- [ ] Needle updates every 60 seconds via Kafka SignalEvents
- [ ] Score range: 0-100
- [ ] Needle rotation: `transform: rotate(${score * 1.8 - 90}deg)`

**Jest Tests Required:**
- [ ] `FearGreedWidget.test.jsx`: Renders correctly, updates on score change

---

### 12.2 Color Zones

**Acceptance Criteria:**
- [ ] Red zone (0-20): Extreme Fear
- [ ] Yellow zone (21-79): Neutral/Mixed
- [ ] Green zone (80-100): Extreme Greed
- [ ] CSS gradient arcs for each zone

---

### 12.3 Hover Tooltips

**Acceptance Criteria:**
- [ ] Tooltip displays composite weights:
  - VIX contribution (%)
  - Google Trends "Margin Call" spikes (%)
  - Social Sentiment score (%)
- [ ] Tooltip positioned near cursor

**Jest Tests Required:**
- [ ] `FearGreedWidget.test.jsx`: Tooltip appears on hover with data

---

### 12.4 Framer Motion Needle Transitions

**Acceptance Criteria:**
- [ ] `motion.g` wrapper on needle group
- [ ] Spring animation: `type: "spring", stiffness: 100, damping: 15`
- [ ] No visual jarring on subtle sentiment shifts

---

## 6.2: Kafka Nervous System Stream Monitor

### 6.2.1 Scrolling Activity Log

**Files to Create/Modify:**
- `[NEW]` `frontend2/src/widgets/KafkaStreamMonitor.jsx`
- `[NEW]` `frontend2/src/widgets/KafkaStreamMonitor.css`

**Acceptance Criteria:**
- [ ] Virtualized list (react-window) for 10,000+ messages
- [ ] Columns: Timestamp, Topic, Event Type, Summary
- [ ] Auto-scroll to latest with pause on hover
- [ ] Max buffer: 5,000 messages

**Jest Tests Required:**
- [ ] `KafkaStreamMonitor.test.jsx`: Virtualization works, filters apply

---

### 6.2.2 D3.js Latency Graph

**Files to Create/Modify:**
- `[NEW]` `frontend2/src/widgets/LatencyGraph.jsx`

**Acceptance Criteria:**
- [ ] Real-time line graph of API-to-Kafka ingestion speed
- [ ] Target line at 200ms (green dashed)
- [ ] Red fill when latency exceeds threshold
- [ ] Last 60 data points displayed

**Jest Tests Required:**
- [ ] `LatencyGraph.test.jsx`: Renders SVG path, threshold indicator

---

### 6.2.3 Color-Coded Event Classification

**Acceptance Criteria:**
| Color | Event Type |
|-------|------------|
| Blue (`#3498db`) | Price Data |
| Purple (`#9b59b6`) | Sentiment |
| Orange (`#e67e22`) | Risk Warning |
| Green (`#2ecc71`) | Execution |

---

### 6.2.4 Topic Filtering

**Acceptance Criteria:**
- [ ] Multi-select dropdown for Kafka topics
- [ ] Topics: `options-flow`, `reddit-mentions`, `market-data`, `risk-alerts`
- [ ] Filter state persisted in Zustand
- [ ] "Clear All" / "Select All" quick actions

**Jest Tests Required:**
- [ ] `KafkaStreamMonitor.test.jsx`: Filter reduces displayed messages

---

## Backend Requirements

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/market/fear-greed` | GET | Current Fear/Greed score |
| `/api/v1/kafka/stats` | GET | Topic latency statistics |
| `/ws/kafka-stream` | WS | Real-time Kafka event stream |

---

## Widget Registry Entries

```javascript
// Add to WidgetCatalog
{
  id: 'fear-greed-gauge',
  name: 'Fear & Greed Index',
  component: FearGreedWidget,
  category: 'Sentiment',
  defaultSize: { width: 300, height: 280 }
},
{
  id: 'kafka-monitor',
  name: 'Kafka Stream Monitor',
  component: KafkaStreamMonitor,
  category: 'System',
  defaultSize: { width: 500, height: 400 }
}
```

---

## Test Coverage Requirements

| Component | Unit Tests | Integration Tests |
|-----------|------------|-------------------|
| Breadcrumbs | ✓ | - |
| AnalyticsOptions | ✓ | ✓ |
| navigationStore | ✓ | - |
| FearGreedWidget | ✓ | ✓ |
| KafkaStreamMonitor | ✓ | ✓ |
| LatencyGraph | ✓ | - |

**Minimum Coverage Target:** 80%

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Initial specification with Jest requirements |

