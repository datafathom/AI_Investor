-- Phase 122: Risk-Free Rates
-- Tracks daily Treasury bond yields for use in risk-adjusted return calculations

CREATE TABLE IF NOT EXISTS risk_free_rates (
    id BIGSERIAL,
    date DATE NOT NULL, -- Removed UNIQUE since it conflicts with hypertable unless (date, something) is unique. Wait, RFR is strictly daily. So (date) should be unique.
    -- But hypertable chunking requires date in PK.
    -- So PRIMARY KEY (id, date) works.
    -- UNIQUE(date) fails if it's partitioned?
    -- Timescale docs: Unique constraints must include partitioning column. So UNIQUE(date) is fine.
    
    rate_10y DECIMAL(8, 6) NOT NULL, -- 10-Year Treasury
    rate_2y DECIMAL(8, 6),           -- 2-Year Treasury
    rate_3m DECIMAL(8, 6),           -- 3-Month Treasury
    source VARCHAR(50) DEFAULT 'FRED',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (id, date)
);

-- Check if TimescaleDB extension is available
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'timescaledb') THEN
        PERFORM create_hypertable('risk_free_rates', 'date', if_not_exists => TRUE);
    END IF;
END $$;

CREATE INDEX IF NOT EXISTS idx_rfr_date ON risk_free_rates(date DESC);
