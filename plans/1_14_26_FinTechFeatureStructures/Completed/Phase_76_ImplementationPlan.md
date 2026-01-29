# Phase 76: Sector Rotation & Business Cycle Clock

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Macro Strategy Team

---

## 📋 Overview

**Description**: Implement the "Investment Clock". Rotate sectors based on the business cycle (Early Cycle -> Financials, Mid -> Tech, Late -> Energy, Recession -> Utilities).

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 76

---

## 🎯 Sub-Deliverables

### 76.1 Business Cycle Classifier (ML) `[x]`

**Acceptance Criteria**: ML model inputs: PMI, Yield Curve, Inflation. Outputs: `RECOVERY`, `EXPANSION`, `SLOWDOWN`, `CONTRACTION`.

| Component | File Path | Status |
|-----------|-----------|--------|
| Classifier | `services/ai/cycle_classifier.py` | `[x]` |

---

### 76.2 Sector Relative Strength Matrix `[x]`

**Acceptance Criteria**: Matrix showing XLK vs XLE, XLF vs XLU. Identify which sectors are leading.

| Component | File Path | Status |
|-----------|-----------|--------|
| RS Matrix | `services/analysis/sector_rs.py` | `[x]` |

---

### 76.3 Automated Rotation Suggestions `[x]`

**Acceptance Criteria**: Suggest rotation. "Cycle shifting to Slowdown. Overweight Staples (XLP) and Healthcare (XLV)."

| Component | File Path | Status |
|-----------|-----------|--------|
| Rotation Engine | `services/strategies/sector_rotation.py` | `[x]` |

---

### 76.4 Neo4j Cycle-Asset Correlation `[x]`

**Acceptance Criteria**: Map assets to cycle phases in Neo4j. `(:ASSET {ticker: "JPM"})-[:PERFORMS_IN]->(:PHASE {name: "EARLY_CYCLE"})`.

| Component | File Path | Status |
|-----------|-----------|--------|
| Cycle Mapper | `services/neo4j/cycle_map.py` | `[x]` |

### 76.5 Cycle Clock Visualization `[x]`

**Acceptance Criteria**: Visual "Clock" UI showing current phase pointer.

| Component | File Path | Status |
|-----------|-----------|--------|
| Clock UI | `frontend2/src/components/Macro/CycleClock.jsx` | `[x]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py cycle status` | Current phase | `[x]` |
| `python cli.py cycle top-sectors` | Leaders | `[x]` |

---

*Last verified: 2026-01-25*
