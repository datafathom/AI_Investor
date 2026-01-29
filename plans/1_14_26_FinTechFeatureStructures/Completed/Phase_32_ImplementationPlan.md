# Phase 32: Market Breadth Pipometer (Kafka Feed)

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Frontend Team

---

## 📋 Overview

**Description**: Deploy a real-time "Pipometer" widget that measures the velocity and distance of market movements for Major Pairs. This helps traders visualize "how fast" the market is moving, detecting high-momentum breakouts versus lethargic accumulation.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 32

---

## 🎯 Sub-Deliverables

### 32.1 60 FPS Pip Velocity Stream (WebSockets) `[x]`

**Acceptance Criteria**: Implement a 60 FPS visual feed. Frontend subscribes to WebSocket. Backend pushes `pips_per_second` metrics derived from Kafka.

| Component | File Path | Status |
|-----------|-----------|--------|
| Socket Manager | `api/sockets/pipometer.py` | `[x]` |
| Velocity Calc | `services/market/velocity_calc.py` | `[x]` |

---

### 32.2 'Flash Crash' Velocity Detector `[x]`

**Acceptance Criteria**: Implement detection logic based on abnormal spikes in pip velocity (e.g., > 50 pips/sec). Trigger immediate alerts.

| Component | File Path | Status |
|-----------|-----------|--------|
| Crash Detector | `services/alerts/flash_crash.py` | `[x]` |

---

### 32.3 React Pipometer Widget (Canvas/D3) `[x]`

**Acceptance Criteria**: Visual gauge. Needle moves based on velocity. Color shifts Green (Fast Up) to Red (Fast Down).

| Component | File Path | Status |
|-----------|-----------|--------|
| Widget | `frontend2/src/components/Market/Pipometer.jsx` | `[x]` |

---

### 32.4 Historical Volatility Distribution `[x]`

**Acceptance Criteria**: Visualize the historical distribution of pip movement using D3.js. "Is 10 pips/sec normal for this hour?"

| Component | File Path | Status |
|-----------|-----------|--------|
| Distro Chart | `frontend2/src/components/Charts/VolDistribution.jsx` | `[x]` |

---

### 32.5 Multi-Pair Support `[x]`

**Acceptance Criteria**: Allow user to switch the Pipometer target (EURUSD, GBPJPY, XAUUSD) instantly.

| Component | File Path | Status |
|-----------|-----------|--------|
| Pair Selector | `frontend2/src/components/Market/PairSelector.jsx` | `[x]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py pipometer stream` | Debug stream | `[x]` |
| `python cli.py pipometer stats` | Show peak velocity | `[x]` |

---

*Last verified: 2026-01-25*
