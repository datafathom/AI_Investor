# Phase 10: TimescaleDB Trade Journaling Schema

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Database Team

---

## 📋 Overview

**Description**: Develop the time-series schema for the high-fidelity trade journal to record every system decision and R-Multiple outcome.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)

---

## 🎯 Sub-Deliverables

### 10.1 Trade Journal Hypertable `[ ]`

**Acceptance Criteria**: Create a TimescaleDB hypertable for `trade_journal` with columns for Entry/Exit, Stop Loss, and Agent Logic.

#### Database Schema

```sql
CREATE TABLE trade_journal (
    id BIGSERIAL,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    trade_id UUID NOT NULL UNIQUE,
    
    -- Trade Details
    symbol VARCHAR(20) NOT NULL,
    direction VARCHAR(10) NOT NULL,  -- LONG, SHORT
    entry_price DECIMAL(20, 8) NOT NULL,
    exit_price DECIMAL(20, 8),
    stop_loss DECIMAL(20, 8) NOT NULL,
    take_profit DECIMAL(20, 8),
    position_size DECIMAL(20, 8) NOT NULL,
    
    -- Execution
    entry_time TIMESTAMPTZ NOT NULL,
    exit_time TIMESTAMPTZ,
    status VARCHAR(20) NOT NULL DEFAULT 'OPEN',  -- OPEN, CLOSED, STOPPED, CANCELLED
    
    -- Performance
    pnl_pips DECIMAL(10, 2),
    pnl_dollars DECIMAL(20, 2),
    r_multiple DECIMAL(10, 2),
    
    -- Agent Logic
    agent_id VARCHAR(100) NOT NULL,
    trade_thesis TEXT NOT NULL,
    trade_reason JSONB NOT NULL,
    confidence_score DECIMAL(5, 4),
    
    -- Audit
    is_demo BOOLEAN NOT NULL DEFAULT TRUE,
    hash_sha256 VARCHAR(64),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

SELECT create_hypertable('trade_journal', 'timestamp');

CREATE INDEX idx_journal_trade_id ON trade_journal(trade_id);
CREATE INDEX idx_journal_symbol ON trade_journal(symbol);
CREATE INDEX idx_journal_agent ON trade_journal(agent_id);
CREATE INDEX idx_journal_status ON trade_journal(status);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/005_trade_journal.sql` | `[ ]` |
| Model | `models/trade_journal.py` | `[ ]` |
| Service | `services/trade_journal_service.py` | `[ ]` |

---

### 10.2 R-Multiple Calculation `[ ]`

**Acceptance Criteria**: Implement automated calculation of R-Multiple for every trade closure, persisted as a float in Postgres.

#### Backend Implementation

```python
def calculate_r_multiple(entry_price: Decimal, exit_price: Decimal, 
                          stop_loss: Decimal, direction: str) -> Decimal:
    """
    Calculate R-Multiple: How many times the initial risk was gained/lost.
    
    R = (Exit - Entry) / (Entry - StopLoss)  for LONG
    R = (Entry - Exit) / (StopLoss - Entry)  for SHORT
    
    Example:
        Entry: 1.1000, Exit: 1.1100, StopLoss: 1.0950
        R = (1.1100 - 1.1000) / (1.1000 - 1.0950) = 0.01 / 0.005 = 2.0R
    """
    pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| R-Multiple Calculator | `services/r_multiple_calculator.py` | `[ ]` |
| Performance Tracker | `services/performance_tracker.py` | `[ ]` |

---

### 10.3 Trade Reason Indexing `[ ]`

**Acceptance Criteria**: Configure indexing for the `trade_reason` column to allow for forensic natural language searching via the UI.

```sql
-- GIN index for JSONB full-text search
CREATE INDEX idx_journal_reason_gin ON trade_journal USING GIN (trade_reason);

-- Text search on thesis
CREATE INDEX idx_journal_thesis_text ON trade_journal 
    USING GIN (to_tsvector('english', trade_thesis));

-- Example query
SELECT * FROM trade_journal 
WHERE trade_reason @> '{"market_structure": "Higher High"}';
```

---

### 10.4 SHA-256 Entry Hashing `[ ]`

**Acceptance Criteria**: Ensure that every journal entry is SHA-256 hashed to guarantee the integrity of the performance audit trail.

#### Backend Implementation

```python
import hashlib
import json

def hash_trade_entry(trade: TradeJournal) -> str:
    """
    Create SHA-256 hash of immutable trade fields.
    """
    data = json.dumps({
        'trade_id': str(trade.trade_id),
        'symbol': trade.symbol,
        'direction': trade.direction,
        'entry_price': str(trade.entry_price),
        'stop_loss': str(trade.stop_loss),
        'entry_time': trade.entry_time.isoformat(),
        'agent_id': trade.agent_id,
        'trade_thesis': trade.trade_thesis,
    }, sort_keys=True)
    return hashlib.sha256(data.encode()).hexdigest()
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Hash Generator | `services/trade_hash_generator.py` | `[ ]` |
| Integrity Validator | `services/journal_integrity.py` | `[ ]` |

---

### 10.5 High-Frequency Entry Handling `[ ]`

**Acceptance Criteria**: Verify that the journaling service can handle 1,000+ simultaneous entries during high-frequency agent activity.

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Write Throughput | 1,000 entries/sec | - | `[ ]` |
| Read Latency (single) | < 10ms | - | `[ ]` |
| Read Latency (1000) | < 100ms | - | `[ ]` |

| Component | File Path | Status |
|-----------|-----------|--------|
| Batch Writer | `services/journal_batch_writer.py` | `[ ]` |
| Load Test | `tests/load/test_journal_throughput.py` | `[ ]` |

---

## 📊 Phase Completion Summary

| Deliverable | Status | E2E Verified |
|-------------|--------|--------------|
| 10.1 Trade Journal Hypertable | `[ ]` | `[ ]` |
| 10.2 R-Multiple Calculation | `[ ]` | `[ ]` |
| 10.3 Trade Reason Indexing | `[ ]` | `[ ]` |
| 10.4 SHA-256 Hashing | `[ ]` | `[ ]` |
| 10.5 High-Frequency Handling | `[ ]` | `[ ]` |

**Phase Status**: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py journal-list` | List recent trades | `[ ]` |
| `python cli.py journal-stats` | Show journal statistics | `[ ]` |
| `python cli.py journal-verify` | Verify hash integrity | `[ ]` |

---

*Last verified: 2026-01-25*
