# Phase 53: Global Macro & Commodities Heatmaps

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Core Strategy Team

---

## 📋 Overview

**Description**: Map global trade, political alpha, and commodity term structures. "Macro" dictates the tide that lifts or sinks all boats. Visualization is key here.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 53

---

## 🎯 Sub-Deliverables

### 53.1 Interactive D3 World Map `[ ]`

**Acceptance Criteria**: Develop an Interactive D3 World Map displaying `POLITICAL_INSIDER` nodes (Phase 63) and shipping congestion clusters to visualize supply chain risks.

| Component | File Path | Status |
|-----------|-----------|--------|
| World Map | `frontend2/src/components/Maps/MacroWorld.jsx` | `[ ]` |

---

### 53.2 Futures Curve Visualizer `[ ]`

**Acceptance Criteria**: Implement a Futures Curve Visualizer for plotting Contango and Backwardation in energy/agri markets. X-Axis: Month, Y-Axis: Price.

| Component | File Path | Status |
|-----------|-----------|--------|
| Curve Chart | `frontend2/src/components/Charts/FuturesCurve.jsx` | `[ ]` |

---

### 53.3 Inflation Sensitivity Matrix (Neo4j) `[ ]`

**Acceptance Criteria**: Configure an Inflation-Sensitive Asset Correlation Matrix within Neo4j. Cluster assets by sensitivity to CPI (Correlation > 0.7).

| Component | File Path | Status |
|-----------|-----------|--------|
| Sensitivity Graph | `services/neo4j/inflation_cluster.py` | `[ ]` |

---

### 53.4 Low-Latency Futures Stream `[ ]`

**Acceptance Criteria**: Ensure futures price updates (ES=F, CL=F, GC=F) maintain < 200ms latency via the Redpanda bus.

| Component | File Path | Status |
|-----------|-----------|--------|
| Stream Config | `config/kafka/futures_priority.json` | `[ ]` |

---

### 53.5 Localized Macro Data Linking `[ ]`

**Acceptance Criteria**: Link clickable map regions to localized macro data (CPI, PPI, Interest Rates) in the `useMacroStore`. Click "Germany" -> See "DAX" and "Bund Yields".

| Component | File Path | Status |
|-----------|-----------|--------|
| Macro Store | `frontend2/src/stores/macroStore.js` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py macro show-map` | Render map data | `[ ]` |
| `python cli.py macro check-cpi <country>` | Get inflation | `[ ]` |

---

*Last verified: 2026-01-25*
