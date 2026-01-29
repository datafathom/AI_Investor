# Phase 90: Geopolitical Risk Map (Neo4j)

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Macro Strategy Team

---

## 📋 Overview

**Description**: Map countries, alliances, and conflicts. `(:COUNTRY {name: "Russia"})-[:SANCTIONED_BY]->(:COUNTRY {name: "USA"})`. Used to assess "Sovereign Risk" and "Supply Chain Fractures".

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 90

---

## 🎯 Sub-Deliverables

### 90.1 Country-Alliance Graph Schema `[x]`

**Acceptance Criteria**: Schema for NATO, BRICS, OPEC. Analyze bloc power.

| Component | File Path | Status |
|-----------|-----------|--------|
| Graph Schema | `services/neo4j/geo_schema.py` | `[x]` |

---

### 90.2 Conflict Zone Alert `[x]`

**Acceptance Criteria**: If portfolio has exposure to a conflict zone (e.g., Taiwan Semi during tension), flag High Risk.

| Component | File Path | Status |
|-----------|-----------|--------|
| Conflict Alert | `services/alerts/conflict_zone.py` | `[x]` |

---

### 90.3 Sovereign Debt Risk Scorer (CDS) `[x]`

**Acceptance Criteria**: Ingest Credit Default Swap (CDS) spreads for sovereign debt. High spread = Default Risk.

| Component | File Path | Status |
|-----------|-----------|--------|
| CDS Monitor | `services/market/sovereign_cds.py` | `[x]` |

---

### 90.4 Currency Peg Break Risk `[x]`

**Acceptance Criteria**: Monitor fixed pegs (e.g., HKD, SAR). If reserves drop, peg break risk rises. (Black Swan event).

| Component | File Path | Status |
|-----------|-----------|--------|
| Peg Monitor | `services/analysis/peg_break.py` | `[x]` |

### 90.5 Interactive Conflict Map `[x]`

**Acceptance Criteria**: UI Map showing "Hot Zones". Overlay Portfolio Exposure.

| Component | File Path | Status |
|-----------|-----------|--------|
| Conflict Map | `frontend2/src/components/Maps/HotZones.jsx` | `[x]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py geo check-exposure` | List risky assets | `[x]` |
| `python cli.py geo show-alliances` | Graph dump | `[x]` |

---

*Last verified: 2026-01-25*
