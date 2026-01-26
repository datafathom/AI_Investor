# Phase 185: Rule 144 Volume & Affiliate Restriction Engine

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Compliance Team

---

## 📋 Overview

**Description**: Manage restrictions for "Affiliates" (Insiders) under SEC Rule 144. They cannot just sell stock. They are limited to selling 1% of outstanding shares or the average weekly trading volume (whichever is greater) every 3 months.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch X Phase 5

---

## 🎯 Sub-Deliverables

### 185.1 Postgres 1% Outstanding Shares Limit Table `[ ]`

**Acceptance Criteria**: Track "Shares Outstanding" for every company where a client is an insider. Calculate the 1% cap.

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE rule_144_limits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticker VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    
    -- Inputs
    shares_outstanding BIGINT,
    avg_weekly_volume BIGINT,
    
    -- Limits
    limit_1_pct BIGINT GENERATED ALWAYS AS (shares_outstanding * 0.01) STORED,
    limit_volume BIGINT GENERATED ALWAYS AS (avg_weekly_volume) STORED,
    max_sale_quantity BIGINT, -- GREATEST(limit_1_pct, limit_volume)
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/185_rule144.sql` | `[ ]` |
| Limit Calculator | `services/compliance/rule144_calc.py` | `[ ]` |

---

### 185.2 Kafka Trailing 4-Week Average Volume Consumer `[ ]`

**Acceptance Criteria**: Stream trading volume to calculate the "Average Weekly Volume" (AWTV) limit dynamically.

| Component | File Path | Status |
|-----------|-----------|--------|
| Volume Consumer | `services/kafka/volume_consumer.py` | `[ ]` |

---

### 185.3 Neo4j Affiliate/Insider Rule 144 Node `[ ]`

**Acceptance Criteria**: Flag clients as "Affiliates". If flagged, all sell orders for that ticker MUST pass the Rule 144 check.

```cypher
(:CLIENT {name: "CEO"})-[:IS_AFFILIATE_OF]->(:COMPANY {ticker: "TSLA"})
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Affiliate Graph | `services/neo4j/affiliate_graph.py` | `[ ]` |

---

### 185.4 Volume Promo Social Media Detector `[ ]`

**Acceptance Criteria**: Monitoring tool. SEC forbids "Solicitation" of buy orders to pump volume before selling. Detect if client is tweeting about the stock while selling.

| Component | File Path | Status |
|-----------|-----------|--------|
| Promo Monitor | `services/compliance/promo_monitor.py` | `[ ]` |

---

### 185.5 IPO Lock-up Period Compliance Verifier `[ ]`

**Acceptance Criteria**: Track IPO Lock-up dates (usually 180 days post-IPO). Hard block on selling until lock-up expires.

| Component | File Path | Status |
|-----------|-----------|--------|
| Lockup Verifier | `services/compliance/lockup_verifier.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Insider Dashboard | `frontend2/src/components/Compliance/InsiderDash.jsx` | `[ ]` |
| Sell Limit Gauge | `frontend2/src/components/Charts/Rule144Gauge.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py 144 check-limit <ticker>` | Show max sell qty | `[ ]` |
| `python cli.py 144 status` | Are you an affiliate? | `[ ]` |

---

*Last verified: 2026-01-25*
