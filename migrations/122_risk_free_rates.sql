-- Phase 122: Risk-Free Rates
-- Tracks daily Treasury bond yields for use in risk-adjusted return calculations

CREATE TABLE IF NOT EXISTS risk_free_rates (
    id BIGSERIAL PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    rate_10y DECIMAL(8, 6) NOT NULL, -- 10-Year Treasury
    rate_2y DECIMAL(8, 6),           -- 2-Year Treasury
    rate_3m DECIMAL(8, 6),           -- 3-Month Treasury
    source VARCHAR(50) DEFAULT 'FRED',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Check if TimescaleDB extension is available
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'timescaledb') THEN
        PERFORM create_hypertable('risk_free_rates', 'date', if_not_exists => TRUE);
    END IF;
END $$;

CREATE INDEX IF NOT EXISTS idx_rfr_date ON risk_free_rates(date DESC);
