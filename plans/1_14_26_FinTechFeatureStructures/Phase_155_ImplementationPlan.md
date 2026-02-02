# Phase 155: Heir Litigation & Family Conflict Risk Mapper

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-30  
> **Owner**: Estate Planning & Legal Team

---

## 📋 Overview

**Description**: Using a "Pre-Mortem" analysis to predict and prevent family litigation. Identify potential conflict points and implement legal/technical guardrails to minimize the risk of a Will contest.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch VIII Phase 15

---

## 🎯 Sub-Deliverables

### 155.1 Family Conflict Score `[x]`

**Acceptance Criteria**: Algorithm that assigns a "Litigation Risk Score" (0-100).

**Implementation**: `ConflictAssessor` class:
- Blended family detection (+25 risk)
- Unequal distribution detection (+20 risk)
- Illiquid concentration analysis (+15 risk)
- Auto-recommends In Terrorem clauses and professional trustees

| Component | File Path | Status |
|-----------|-----------|--------|
| Conflict Assessor | `services/estate/conflict_assessor.py` | `[x]` |

---

### 155.2 Neo4j Litigant Heir → Trust Friction Mapping `[x]`

**Acceptance Criteria**: Graph modeling of asset conflict points (KEEP vs SELL desires).

| Component | File Path | Status |
|-----------|-----------|--------|
| Friction Graph | `services/neo4j/friction_graph.py` | `[x]` |

---

### 155.3 Well-Defined Wills Prioritization Logic `[x]`

**Acceptance Criteria**: Specific > General > Residual bequest priority.

**Implementation**: `BequestPrioritizer` class with priority map.

| Component | File Path | Status |
|-----------|-----------|--------|
| Bequest Prioritizer | `services/estate/bequest_prioritizer.py` | `[x]` |

---

### 155.4 Postgres Fairness Dispute Mediation Log `[x]`

**Acceptance Criteria**: Immutable log of family meetings as evidence of intent.

| Component | File Path | Status |
|-----------|-----------|--------|
| Evidence Locker | `services/compliance/evidence_locker.py` | `[x]` |

---

### 155.5 Asset Liquidation Protocol for Disagreements `[x]`

**Acceptance Criteria**: Automatic "Tie-Breaker" after 90-day deadlock.

**Implementation**: `LiquidationEnforcer` class:
- Triggers FORCE_LIQUIDATION after 90 days
- Distributes cash equally to resolve deadlock

| Component | File Path | Status |
|-----------|-----------|--------|
| Liquidation Protocol | `services/estate/liquidation_enforcer.py` | `[x]` |

---

## 📊 Phase Status: `[x]` COMPLETED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py estate assess-conflict` | Calculate risk score | `[x]` |
| `python cli.py estate find-friction` | Query Neo4j conflicts | `[x]` |

---

*Last verified: 2026-01-30*

