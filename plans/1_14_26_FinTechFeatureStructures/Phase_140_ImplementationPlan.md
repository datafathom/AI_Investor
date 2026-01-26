# Phase 140: Transition to Tax & Trust Legal Module

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Core Architecture Team

---

## 📋 Overview

**Description**: Bridge Epoch VII (Portfolio Theory) to Epoch VIII (Tax & Trust Legal Structures). This phase ensures that the portfolio engines (Risk, Returns, REITs) can now interface with legal entity wrappers (Trusts, LLCs) and tax optimization layers (Harvesting, Deferral).

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch VII Phase 20

---

## 🎯 Sub-Deliverables

### 140.1 Phase 21-39 Metrics → Wealth Manager Link `[ ]`

**Acceptance Criteria**: Ensure all risk/return metrics calculated in previous phases are accessible to the Wealth Manager persona dashboard via a unified API gateway.

| Component | File Path | Status |
|-----------|-----------|--------|
| Metrics Aggregator | `services/reporting/metrics_aggregator.py` | `[ ]` |
| Wealth Manager API | `web/api/dashboard/wealth_manager.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Client Overview | `frontend2/src/components/Dashboard/ClientOverview.jsx` | `[ ]` |
| Key Metrics Card | `frontend2/src/components/Dashboard/KeyMetrics.jsx` | `[ ]` |

---

### 140.2 REIT/Diversification → Estate Planning Access `[ ]`

**Acceptance Criteria**: Expose real estate and diversification data to the Estate Planning module, allowing trusts to "see" the assets they hold.

#### Neo4j Schema

```cypher
// Link Portfolio to Estate Plan
(:PORTFOLIO)-[:FUNDED_BY]->(:TRUST {type: "REVOCABLE"})

// Asset Visibility
(:TRUST)-[:HAS_VISIBILITY]->(:REIT_HOLDINGS)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Asset Bridge | `services/estate/asset_bridge.py` | `[ ]` |

---

### 140.3 Portfolio Risk Summary Export `[ ]`

**Acceptance Criteria**: Generate a comprehensive PDF/JSON risk summary report including Sharpe, Sortino, VaR, and Drawdown history for client meetings.

| Component | File Path | Status |
|-----------|-----------|--------|
| Report Generator | `services/reporting/risk_summary_pdf.py` | `[ ]` |
| PDF Template | `templates/reports/risk_summary.html` | `[ ]` |

---

### 140.4 Kafka Bridge to Phase 141 Tax Loss Harvesting `[ ]`

**Acceptance Criteria**: Establish the Kafka infrastructure required for real-time tax loss harvesting triggers in the next epoch.

#### Kafka Topic Configuration

```json
{
    "topic": "tax-harvesting-triggers",
    "partitions": 4,
    "schema": {
        "account_id": "uuid",
        "ticker": "string",
        "unrealized_loss_pct": "decimal",
        "loss_amount": "decimal",
        "opportunity_score": "decimal",
        "timestamp": "timestamp"
    }
}
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Loss Monitor Producer | `services/kafka/loss_monitor_producer.py` | `[ ]` |

---

### 140.5 Neo4j Core Portfolio Root for Trusts `[ ]`

**Acceptance Criteria**: Define the root node structure in Neo4j that allows a single Trust entity to own multiple underlying portfolios (e.g., "Main Trust" owns "Growth Portfolio" and "Income Portfolio").

#### Neo4j Schema

```cypher
(:TRUST {name: "Smith Family Trust"})-[:OWNS]->(:PORTFOLIO {name: "Growth"})
(:TRUST)-[:OWNS]->(:PORTFOLIO {name: "Income"})
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Trust Root Service | `services/neo4j/trust_root_service.py` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py bridge status` | Check epoch transition status | `[ ]` |
| `python cli.py report generate-risk <id>` | Generate risk PDF | `[ ]` |

---

*Last verified: 2026-01-25*
