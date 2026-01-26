# Phase 177: Bespoke PPLI High-Income Tax Shield

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Insurance Team

---

## 📋 Overview

**Description**: Highly customized Private Placement Life Insurance (PPLI) for UHNW income shielding. Unlike standard PPLI (Phase 168), this focuses on wrapping high-yield, tax-inefficient assets like Private Credit and Hedge Funds to convert Ordinary Income (37%+) into Tax-Free Growth.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch IX Phase 17

---

## 🎯 Sub-Deliverables

### 177.1 High-Yield Asset Selection Algorithm `[ ]`

**Acceptance Criteria**: Algorithm to select the *most* tax-inefficient assets for the PPLI wrapper. Prioritize Short-Term Gains and Ordinary Income over Long-Term Capital Gains.

```python
class TaxEfficiencyRanker:
    """
    Rank assets by 'Tax Drag' to prioritize PPLI placement.
    
    Formula: Tax Drag = (Yield * OrdRate) + (Turnover * STRate)
    """
    def rank_assets(self, assets: list[Asset]) -> list[RankedAsset]:
        # High Yield Debt -> Priority #1
        # Quant Funds (High Turnover) -> Priority #2
        # Index Funds -> Priority #Last
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Asset Ranker | `services/insurance/efficiency_ranker.py` | `[ ]` |

---

### 177.2 Insurance Carrier Diversification Graph `[ ]`

**Acceptance Criteria**: Ensure diversification across Insurance Carriers. UHNW clients placing >$50M in PPLI should not have 100% exposure to one carrier's solvency risk.

#### Neo4j Schema (Docker-compose: neo4j service)

```cypher
(:CARRIER {name: "Lombard"})<-[:ISSUED_BY]-(:POLICY_A)
(:CARRIER {name: "Zurich"})<-[:ISSUED_BY]-(:POLICY_B)
(:CLIENT)-[:OWNS]->(:POLICY_A)
(:CLIENT)-[:OWNS]->(:POLICY_B)

// Query: Carrier Exposure
MATCH (c:CLIENT)-[:OWNS]->(p:POLICY)-[:ISSUED_BY]->(carrier:CARRIER)
RETURN carrier.name, sum(p.cash_value) as exposure
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Carrier Graph | `services/neo4j/carrier_graph.py` | `[ ]` |

---

### 177.3 Premium Deposit Cadence Optimizer `[ ]`

**Acceptance Criteria**: Optimize premium payments to maximize cash value while avoiding MEC status. Determine if "Dump-In" (large upfront) or "Level Pay" (spread out) is better for IRR.

| Component | File Path | Status |
|-----------|-----------|--------|
| Premium Optimizer | `services/insurance/premium_opt.py` | `[ ]` |

---

### 177.4 Policy Loan Exit Strategy Modeler `[ ]`

**Acceptance Criteria**: Model the "End Game". How to access cash in retirement via loans without crashing the policy.

| Component | File Path | Status |
|-----------|-----------|--------|
| Exit Modeler | `services/simulation/policy_exit.py` | `[ ]` |

---

### 177.5 Jurisdictional Arb (Domestic vs. Offshore) `[ ]`

**Acceptance Criteria**: Compare PPLI jurisdictions (Delaware/South Dakota vs. Bermuda/Cayman). Offshore policies often have lower costs and wider asset flexibility but higher compliance ("953(d) election").

| Component | File Path | Status |
|-----------|-----------|--------|
| Jurisdiction Compare | `services/reporting/jurisdiction_arb.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Tax Shield Simulator | `frontend2/src/components/Insurance/TaxShieldSim.jsx` | `[ ]` |
| Carrier Exposure Chart | `frontend2/src/components/Charts/CarrierExposure.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py ppli optimize-premium` | Calculate payments | `[ ]` |
| `python cli.py ppli rank-assets` | Find tax-heavy assets | `[ ]` |

---

*Last verified: 2026-01-25*
