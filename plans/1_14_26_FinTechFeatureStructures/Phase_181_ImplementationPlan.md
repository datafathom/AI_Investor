# Phase 181: Ostrich in the Sand Volatility Monitor

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Risk Management Team

---

## 📋 Overview

**Description**: "Head in the Sand" Risk. Private markets (PE/VC/Real Estate) report smoothed volatility because they aren't marked-to-market daily. This phase calculates the "True" (hidden) volatility of private assets by using public market proxies, revealing the actual risk exposure.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch X Phase 1

---

## 🎯 Sub-Deliverables

### 181.1 MTM vs. Discretionary Valuation Gap Analyzer `[ ]`

**Acceptance Criteria**: Logic to calculate the gap between "Mark-to-Model" valuations (private) and "Mark-to-Market" (public equivalents). If Public SaaS is down 50%, Private SaaS shouldn't be flat.

```python
class GapAnalyzer:
    """
    detect valuation lags.
    """
    def measure_gap(self, private_asset: Asset, public_proxy_ticker: str) -> GapMetrics:
        proxy_drawdown = self.market_data.get_drawdown(public_proxy_ticker)
        private_drawdown = private_asset.reported_drawdown
        
        # If Proxy down 30% and Private down 0%, Gap is 30%
        return GapMetrics(gap_pct=proxy_drawdown - private_drawdown)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Gap Analyzer | `services/risk/gap_analyzer.py` | `[ ]` |
| Proxy Mapper | `services/risk/proxy_mapper.py` | `[ ]` |

---

### 181.2 Postgres Public Sector Basket vs. PE NAV Table `[ ]`

**Acceptance Criteria**: DB tracking the correlation. "Growth Equity Fund IV" mapped to "QQQ/ARKK Basket".

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE valuation_gaps (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    private_fund_id UUID NOT NULL,
    proxy_ticker VARCHAR(20),
    
    date DATE NOT NULL,
    private_nav DECIMAL(20, 2),
    proxy_index_value DECIMAL(20, 2),
    
    -- Metrics
    implied_private_value DECIMAL(20, 2), -- What it *should* be
    gap_percentage DECIMAL(5, 4),
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/181_valuation_gaps.sql` | `[ ]` |
| Gap Tracker | `services/risk/gap_tracker.py` | `[ ]` |

---

### 181.3 Kafka Liquidity Event Markdown Trigger `[ ]`

**Acceptance Criteria**: If a major public liquidity event happens (e.g., WeWork IPO failure), trigger a markdown review for all related private assets.

| Component | File Path | Status |
|-----------|-----------|--------|
| Event Trigger | `services/kafka/markdown_trigger.py` | `[ ]` |

---

### 181.4 Neo4j 'Head in the Sand' Over-Allocation Relationship `[ ]`

**Acceptance Criteria**: Graph query to identify clients who are over-allocated to private assets *because* they think they are low volatility (when they are actually high risk).

```cypher
(:CLIENT)-[:HAS_PERCEPTION {volatility: "LOW"}]->(:ASSET:PRIVATE_EQUITY)
(:ASSET:PRIVATE_EQUITY)-[:HAS_TRUE_RISK {volatility: "HIGH"}]->(:RISK_MODEL)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Perception Graph | `services/neo4j/perception_graph.py` | `[ ]` |

---

### 181.5 Hidden Volatility Score for PE/VC Funds `[ ]`

**Acceptance Criteria**: A score (0-100) representing how much risk is being hidden by lack of marking.

| Component | File Path | Status |
|-----------|-----------|--------|
| Scorer | `services/risk/hidden_vol_score.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| True Risk Dashboard | `frontend2/src/components/Risk/TrueRisk.jsx` | `[ ]` |
| Gap Chart | `frontend2/src/components/Charts/ValuationGap.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py risk calc-gap` | Show val gaps | `[ ]` |
| `python cli.py risk true-vol` | Calc unsmoothed vol | `[ ]` |

---

*Last verified: 2026-01-25*
