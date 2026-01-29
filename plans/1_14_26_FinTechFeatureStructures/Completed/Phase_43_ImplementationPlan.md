# Phase 43: Multi-Asset Net Worth Dashboard

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Frontend Team

---

## 📋 Overview

**Description**: A unified D3.js visualization of Total Wealth. Aggregates Stocks, Crypto, Real Estate, and Cash into a single "Net Worth" number. This is the North Star metric.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 43

---

## 🎯 Sub-Deliverables

### 43.1 Circular Allocation Gauges `[x]`

**Acceptance Criteria**: Implement circular gauges visualizing Liquid (Stocks/Crypto) vs. Illiquid (Real Estate) asset allocation percentages.

| Component | File Path | Status |
|-----------|-----------|--------|
| Gauges | `frontend2/src/components/Dashboard/AllocGauges.jsx` | `[x]` |

---

### 43.2 Real-Time Net Worth Pulse `[x]`

**Acceptance Criteria**: Verify real-time Net Worth updates as price feeds oscillate through the Redpanda bus. The number should "breathe" with the market.

| Component | File Path | Status |
|-----------|-----------|--------|
| Net Worth Store | `frontend2/src/stores/netWorthStore.js` | `[x]` |

---

### 43.3 Framer Motion Transitions `[x]`

**Acceptance Criteria**: Apply Framer Motion animations for smooth segment transitions when switching views (e.g., from 'Asset Class' view to 'Geography' view).

| Component | File Path | Status |
|-----------|-----------|--------|
| Animation Wrapper | `frontend2/src/components/UI/Transitions.jsx` | `[x]` |

---

### 43.4 The 'Enough' Metric `[x]`

**Acceptance Criteria**: Ensure the 'Enough' metric (Target Net Worth vs Current) is the central focal point. Visual progress bar to Financial Independence.

| Component | File Path | Status |
|-----------|-----------|--------|
| FI Progress | `frontend2/src/components/Dashboard/FIProgressBar.jsx` | `[x]` |

### 43.5 Postgres Daily Snapshot `[x]`

**Acceptance Criteria**: Persist daily Net Worth snapshots in Postgres to track long-term wealth homeostasis and generate "Wealth Growth" charts.

| Component | File Path | Status |
|-----------|-----------|--------|
| Snapshot Job | `services/jobs/daily_snapshot.py` | `[x]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py wealth snapshot` | Take snapshot | `[x]` |
| `python cli.py wealth status` | Show current NW | `[x]` |

---

*Last verified: 2026-01-25*
