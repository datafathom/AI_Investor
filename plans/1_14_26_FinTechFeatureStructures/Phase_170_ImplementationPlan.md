# Phase 170: Descendant Employment & Discretionary Override

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-30  
> **Owner**: HR & Governance Team

---

## 📋 Overview

**Description**: Family member employment with nepotism flags and KPI overrides.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch IX Phase 10

---

## 🎯 Sub-Deliverables

### 170.1 Neo4j Descendant Employee Nodes `[x]`

**Acceptance Criteria**: Map family member employment relationships.

| Component | File Path | Status |
|-----------|-----------|--------|
| Heir Governance | `services/hr/heir_governance_svc.py` | `[x]` |

---

### 170.2 'Cushy Job' Low-Demand Role Flag `[x]`

**Acceptance Criteria**: Flag high salary / low KPI roles.

| Component | File Path | Status |
|-----------|-----------|--------|
| Role Evaluator | `services/hr/heir_governance_svc.py` | `[x]` |

---

### 170.3 Postgres Discretionary KPI Override for Heirs `[x]`

**Acceptance Criteria**: Soft vs Hard KPI tracking.

| Component | File Path | Status |
|-----------|-----------|--------|
| KPI Manager | `services/hr/heir_governance_svc.py` | `[x]` |

---

### 170.4 Employment Outlet Productivity Model `[x]`

**Acceptance Criteria**: Social value employment model.

| Component | File Path | Status |
|-----------|-----------|--------|
| Productivity Model | `services/analysis/productivity_model.py` | `[x]` |

---

### 170.5 Social Perception vs. Actual Productivity Mapping `[x]`

**Acceptance Criteria**: Gap analysis reporting.

| Component | File Path | Status |
|-----------|-----------|--------|
| Perception Mapper | `services/reporting/perception_gap.py` | `[x]` |

---

## 📊 Phase Status: `[x]` COMPLETED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py governance list-heirs` | Show employed family | `[x]` |
| `python cli.py governance audit-kpi` | Check overrides | `[x]` |

---

*Last verified: 2026-01-30*

