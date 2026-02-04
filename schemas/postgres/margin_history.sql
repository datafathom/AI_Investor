-- Phase 136: Margin History
-- Tracks borrowing, collateral, and interest costs over time

CREATE TABLE IF NOT EXISTS margin_history (
    id UUID DEFAULT gen_random_uuid(),
    account_id UUID NOT NULL,
    log_date DATE NOT NULL,
    
    -- Balances
    debit_balance DECIMAL(24, 2) NOT NULL, -- Amount borrowed
    equity_balance DECIMAL(24, 2) NOT NULL, -- Client's money
    market_value DECIMAL(24, 2) NOT NULL, -- Total gross value
    
    -- Leverage Metrics
    margin_ratio DECIMAL(8, 6), -- Debt / Equity
    maintenance_excess DECIMAL(24, 2), -- Buffer before call
    
    -- Cost
    interest_rate_apr DECIMAL(6, 4),
    daily_interest_cost DECIMAL(12, 2),
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (id, log_date)
);

-- Check if TimescaleDB extension is available
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'timescaledb') THEN
        PERFORM create_hypertable('margin_history', 'log_date', if_not_exists => TRUE);
    END IF;
END $$;

CREATE INDEX IF NOT EXISTS idx_margin_account ON margin_history(account_id);
