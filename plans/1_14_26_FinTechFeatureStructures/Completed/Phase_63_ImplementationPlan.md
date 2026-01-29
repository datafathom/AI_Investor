# Phase 63: Political Insider Trading Tracker (The Nancy Index)

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Alternative Data Team

---

## 📋 Overview

**Description**: Track political insider trading. If Congress members are buying Nvidia before a Chips Act vote, we want to know. This is "Geopolitical Alpha".

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 63

---

## 🎯 Sub-Deliverables

### 63.1 House/Senate Disclosure Scraper `[x]`

**Acceptance Criteria**: Scraper that monitors house.gov and senate.gov for PTR (Periodic Transaction Report) filings. OCR PDF support required.

| Component | File Path | Status |
|-----------|-----------|--------|
| Scraper | `services/ingestion/congress_scraper.py` | `[x]` |

---

### 63.2 `POLITICAL_INSIDER` Neo4j Nodes `[x]`

**Acceptance Criteria**: Map politicians to committees and assets. `(:POLITICIAN)-[:SITS_ON]->(:COMMITTEE {name: "Armed Services"})-[:OVERSEES]->(:SECTOR {name: "Defense"})`.

```cypher
MATCH (p:POLITICIAN)-[:BOUGHT]->(a:ASSET)
MATCH (p)-[:SITS_ON]->(c:COMMITTEE)
RETURN p, a, c
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Graph Mapper | `services/neo4j/politics_graph.py` | `[x]` |

---

### 63.3 Anomaly Detection (Timing vs Legislation) `[x]`

**Acceptance Criteria**: Detect trades timed < 30 days before major legislative votes. Flag as "High Suspicion".

| Component | File Path | Status |
|-----------|-----------|--------|
| Anomaly Detector | `services/analysis/political_alpha.py` | `[x]` |

---

### 63.4 The 'Nancy Pelosi' Copy-Trade Strategy `[x]`

**Acceptance Criteria**: Create a strategy that automatically mimics trades of high-performing politicians (with a lag, as disclosures are delayed).

| Component | File Path | Status |
|-----------|-----------|--------|
| Copy Trader | `services/strategies/pelosi_copy.py` | `[x]` |

### 63.5 Disclosure Lag Analysis `[x]`

**Acceptance Criteria**: Analyze the "Reporting Lag" (Trade Date vs Disclosure Date). Filter out politicians who report 45 days late (useless data).

| Component | File Path | Status |
|-----------|-----------|--------|
| Lag Analyzer | `services/analysis/reporting_lag.py` | `[x]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py politics scrape` | Run scraper | `[x]` |
| `python cli.py politics show-trades` | Recent filings | `[x]` |

---

*Last verified: 2026-01-25*
