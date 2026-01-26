# Phase 92: Supply Chain Dependency Mapping

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Fundamental Analysis Team

---

## 📋 Overview

**Description**: Map "Who supplies whom". Apple depends on TSMC. Boeing depends on Spirit Aerosystems. If a supplier crashes, short the customer.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 92

---

## 🎯 Sub-Deliverables

### 92.1 Supplier-Customer Graph (Neo4j) `[ ]`

**Acceptance Criteria**: Ingest FactSet/Bloomberg supply chain data (or scrape 10-Ks). `(:COMPANY {ticker: "TSM"})-[:SUPPLIES]->(:COMPANY {ticker: "AAPL"})`.

| Component | File Path | Status |
|-----------|-----------|--------|
| Chain Graph | `services/neo4j/supply_chain.py` | `[ ]` |

---

### 92.2 Bottleneck Identification `[ ]`

**Acceptance Criteria**: Identify nodes with high Centrality. "Single Points of Failure". (e.g., ASML).

| Component | File Path | Status |
|-----------|-----------|--------|
| Bottleneck Algo | `services/analysis/bottleneck.py` | `[ ]` |

---

### 92.3 Disruption Simulator `[ ]`

**Acceptance Criteria**: Sim: "If TSMC halts, calculate revenue hit for NVDA, AAPL, AMD".

| Component | File Path | Status |
|-----------|-----------|--------|
| Disruption Sim | `services/simulation/supply_shock.py` | `[ ]` |

---

### 92.4 Inventory Build-up Monitor `[ ]`

**Acceptance Criteria**: Track Days Sales of Inventory (DSI). Rising inventory = Demand Slowdown.

| Component | File Path | Status |
|-----------|-----------|--------|
| Inventory Mon | `services/analysis/inventory_track.py` | `[ ]` |

### 92.5 Tier-N Dependency Visualizer `[ ]`

**Acceptance Criteria**: Visualize Tier 1, Tier 2, Tier 3 suppliers. "How deep is the risk?"

| Component | File Path | Status |
|-----------|-----------|--------|
| Tier Viz | `frontend2/src/components/Analysis/SupplyTiers.jsx` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py supply check <ticker>` | Show suppliers | `[ ]` |
| `python cli.py supply simulate-halt` | Risk assessment | `[ ]` |

---

*Last verified: 2026-01-25*
