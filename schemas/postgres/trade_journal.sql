-- Phase 10: TimescaleDB Trade Journaling Schema
-- PURPOSE: Develop the time-series schema for the high-fidelity trade journal.

CREATE TABLE IF NOT EXISTS trade_journal (
    id BIGSERIAL,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    trade_id UUID NOT NULL,
    
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
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (trade_id, timestamp)
);

-- Convert to hypertable for TimescaleDB optimization
SELECT create_hypertable('trade_journal', 'timestamp', if_not_exists => TRUE);

-- Core indexes for retrieval
CREATE INDEX IF NOT EXISTS idx_journal_trade_id ON trade_journal(trade_id);
CREATE INDEX IF NOT EXISTS idx_journal_symbol ON trade_journal(symbol);
CREATE INDEX IF NOT EXISTS idx_journal_agent ON trade_journal(agent_id);
CREATE INDEX IF NOT EXISTS idx_journal_status ON trade_journal(status);

-- GIN index for JSONB full-text search and specific key searching
CREATE INDEX IF NOT EXISTS idx_journal_reason_gin ON trade_journal USING GIN (trade_reason);

-- Text search indexing for trade thesis justification
CREATE INDEX IF NOT EXISTS idx_journal_thesis_text ON trade_journal 
    USING GIN (to_tsvector('english', trade_thesis));
