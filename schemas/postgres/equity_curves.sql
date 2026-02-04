-- Phase 17: Equity History Hypertable
-- Purpose: Tracks account equity, balance, and unrealized PnL over time.

CREATE TABLE IF NOT EXISTS equity_history (
    time TIMESTAMPTZ NOT NULL,
    account_id VARCHAR(100) NOT NULL,
    balance DECIMAL(20, 8) NOT NULL,
    unrealized_pnl DECIMAL(20, 8) NOT NULL,
    equity DECIMAL(20, 8) NOT NULL,
    margin_used DECIMAL(20, 8) DEFAULT 0,
    free_margin DECIMAL(20, 8) DEFAULT 0,
    is_demo BOOLEAN NOT NULL DEFAULT TRUE,
    metadata JSONB
);

-- Convert to hypertable for time-series optimization
SELECT create_hypertable('equity_history', 'time', if_not_exists => TRUE);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_equity_account_time ON equity_history(account_id, time DESC);

-- View for daily drawdown calculation
CREATE OR REPLACE VIEW daily_equity_stats AS
SELECT 
    account_id,
    time_bucket('1 day', time) as day,
    first(equity, time) as opening_equity,
    last(equity, time) as current_equity,
    min(equity) as session_low,
    max(equity) as session_high
FROM equity_history
GROUP BY account_id, day;
