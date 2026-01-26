# Phase 62: Jurisdictional Arbitrage Mapper

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Legal Team

---

## 📋 Overview

**Description**: Map jurisdictional relationships in Neo4j (e.g., "Nevada has 0% state tax"). The AI uses this to suggest "Location Optimization" for assets. "Move this patent to a Delaware LLC".

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 62

---

## 🎯 Sub-Deliverables

### 62.1 Jurisdiction Node Schema `[ ]`

**Acceptance Criteria**: Create `JURISDICTION` nodes in Neo4j with attributes: `capital_gains_rate`, `corporate_tax_rate`, `asset_protection_score` (1-10).

```cypher
(:JURISDICTION {name: "Wyoming", type: "STATE", tax_rate: 0.0})
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Graph Seed | `scripts/seed/jurisdictions.cypher` | `[ ]` |

---

### 62.2 Tax Efficiency Scorer `[ ]`

**Acceptance Criteria**: Calculator that compares a User's current location vs. optimal locations. "You are paying 13% in CA. In NV, you would pay 0%."

| Component | File Path | Status |
|-----------|-----------|--------|
| Tax Scorer | `services/tax/jurisdiction_compare.py` | `[ ]` |

---

### 62.3 'Treaty Network' Graph `[ ]`

**Acceptance Criteria**: For international usage, map Tax Treaties (Double Taxation Agreements) between countries.

| Component | File Path | Status |
|-----------|-----------|--------|
| Treaty Mapper | `services/neo4j/tax_treaties.py` | `[ ]` |

---

### 62.4 Asset Protection Scorecard `[ ]`

**Acceptance Criteria**: Score entities based on "Charging Order Protection". (e.g., Wyoming LLC > California LLC for protection against creditors).

| Component | File Path | Status |
|-----------|-----------|--------|
| Protection Calc | `services/legal/protection_score.py` | `[ ]` |

### 62.5 Migration Workflow Wizard `[ ]`

**Acceptance Criteria**: UI Wizard showing the steps to "Redomicile" an entity.

| Component | File Path | Status |
|-----------|-----------|--------|
| Wizard UI | `frontend2/src/components/Legal/MigrationWizard.jsx` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py legal compare <state1> <state2>` | Show tax diff | `[ ]` |
| `python cli.py legal best-entity` | Suggest structure | `[ ]` |

---

*Last verified: 2026-01-25*
