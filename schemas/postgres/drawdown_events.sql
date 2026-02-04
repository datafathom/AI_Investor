-- Phase 123: Drawdown Events Ledger
-- Tracks portfolio peak-to-trough declines for risk analysis

CREATE TABLE IF NOT EXISTS drawdown_events (
    id UUID DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL,
    
    -- Drawdown Details
    peak_date DATE NOT NULL,
    peak_value DECIMAL(20, 2) NOT NULL,
    trough_date DATE,
    trough_value DECIMAL(20, 2),
    recovery_date DATE,
    
    -- Metrics
    drawdown_pct DECIMAL(8, 6) NOT NULL, -- e.g., 0.1500 = 15%
    duration_days INTEGER,
    recovery_days INTEGER,
    
    -- Classification
    severity VARCHAR(20), -- MINOR (<5%), MODERATE (5-10%), SEVERE (>10%)
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (id, peak_date)
);

-- Check if TimescaleDB extension is available
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'timescaledb') THEN
        PERFORM create_hypertable('drawdown_events', 'peak_date', if_not_exists => TRUE);
    END IF;
END $$;

CREATE INDEX IF NOT EXISTS idx_drawdown_portfolio ON drawdown_events(portfolio_id);
