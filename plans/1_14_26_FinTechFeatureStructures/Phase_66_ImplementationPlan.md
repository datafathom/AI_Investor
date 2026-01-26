# Phase 66: 13F Institutional Holdings Analyzer

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Quantitative Team

---

## 📋 Overview

**Description**: Track "Smart Money" funds (Hedge Funds like Bridgewater, Renaissance). What are they buying? 13F filings are delayed (45 days), so we look for "Persistent Accumulation" trends.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 66

---

## 🎯 Sub-Deliverables

### 66.1 13F XML Parser `[ ]`

**Acceptance Criteria**: Parse massive XML 13F files from SEC. Extract CUSIP, Value, Shares. Handle restatements (13F-HR/A).

| Component | File Path | Status |
|-----------|-----------|--------|
| XML Parser | `services/ingestion/13f_parser.py` | `[ ]` |

---

### 66.2 'Whale Wisdom' Database `[ ]`

**Acceptance Criteria**: Store fund holdings history in TimescaleDB. "How has Berkshire Hathaway's AAPL position changed over 5 years?"

#### Postgres Schema

```sql
CREATE TABLE fund_holdings (
    fund_id UUID,
    quarter_end DATE,
    ticker VARCHAR(10),
    shares BIGINT,
    value_usd DECIMAL(20, 2),
    change_from_prev_qtr BIGINT
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/66_fund_data.sql` | `[ ]` |

---

### 66.3 Consensus Buy List Generator `[ ]`

**Acceptance Criteria**: Generate a list of "Consensus Buys". Which stocks were bought by the top 10 best performing funds this quarter?

| Component | File Path | Status |
|-----------|-----------|--------|
| Consensus Engine | `services/analysis/consensus_buys.py` | `[ ]` |

---

### 66.4 Clone Portfolio Strategy `[ ]`

**Acceptance Criteria**: Implement a "Clone" strategy. "Create a portfolio that tracks Bill Ackman's Pershing Square".

| Component | File Path | Status |
|-----------|-----------|--------|
| Clone Strat | `services/strategies/clone_fund.py` | `[ ]` |

### 66.5 Fund Rotation Visualizer `[ ]`

**Acceptance Criteria**: Visualize sector rotation of major funds. "Bridgewater is rotating from Tech to Consumer Staples."

| Component | File Path | Status |
|-----------|-----------|--------|
| Rotation Chart | `frontend2/src/components/Charts/FundRotation.jsx` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py 13f parse <file>` | Ingest XML | `[ ]` |
| `python cli.py 13f top-buys` | Consenus list | `[ ]` |

---

*Last verified: 2026-01-25*
