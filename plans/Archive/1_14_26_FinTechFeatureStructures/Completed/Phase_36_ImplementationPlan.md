# Phase 36: Index Fund Exposure Tracker

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Portfolio Team

---

## 📋 Overview

**Description**: Integrate trackers for S&P 500 (SPY/VOO) and Nasdaq (QQQ) to monitor market-wide beta exposure and concentration. Before seeking Alpha, we must measure our Beta.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 36

---

## 🎯 Sub-Deliverables

### 36.1 Real-Time Index Holdings Monitor `[x]`

**Acceptance Criteria**: Implement real-time monitoring of SPY and QQQ holdings within the central portfolio dashboard. Fetch prices via Kafka.

| Component | File Path | Status |
|-----------|-----------|--------|
| Index Monitor | `services/portfolio/index_monitor.py` | `[x]` |

---

### 36.2 Exposure Warning System (>40%) `[x]`

**Acceptance Criteria**: Alert the Warden if total index fund exposure exceeds 40.0% of the aggregate net worth. (Or whatever the user's config is). Too much beta = "Closet Indexing".

| Component | File Path | Status |
|-----------|-----------|--------|
| Concentration Alert | `services/alerts/concentration.py` | `[x]` |

---

### 36.3 Beta-Weighted Exposure Calculator `[x]`

**Acceptance Criteria**: Calculate the Beta-weighted exposure. If I own $10k of 3x Leveraged TQQQ, that's $30k of Exposure.

```python
class BetaCalculator:
    def calculate_exposure(self, portfolio: Portfolio) -> float:
        total_beta_exposure = 0
        for asset in portfolio.assets:
            total_beta_exposure += asset.value * asset.beta
        return total_beta_exposure
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Beta Calc | `services/analysis/beta_calc.py` | `[x]` |

---

### 36.4 Dividend Payout Schedule (TimescaleDB) `[x]`

**Acceptance Criteria**: Verify that dividend payout schedules for major indices are tracked and projected.

#### Postgres Schema

```sql
CREATE TABLE dividend_schedule (
    ticker VARCHAR(10) NOT NULL,
    ex_date DATE NOT NULL,
    pay_date DATE NOT NULL,
    amount DECIMAL(10, 4),
    frequency VARCHAR(20) -- QUARTERLY
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Schedule Tracker | `services/portfolio/div_schedule.py` | `[x]` |

---

### 36.5 Neo4j Constituent Mapper `[x]`

**Acceptance Criteria**: Map index constituents in Neo4j to detect hidden sector correlations. (e.g., holding AAPL stock AND SPY ETF means double exposure to Apple).

```cypher
(:ETF {ticker: "SPY"})-[:HOLDS]->(:STOCK {ticker: "AAPL"})
(:PORTFOLIO)-[:OWNS]->(:ETF {ticker: "SPY"})
(:PORTFOLIO)-[:OWNS]->(:STOCK {ticker: "AAPL"})
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Constituent Graph | `services/neo4j/constituents.py` | `[x]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py index check-beta` | Show total beta | `[x]` |
| `python cli.py index list-overlap` | Show duplicate exposure | `[x]` |

---

*Last verified: 2026-01-25*
