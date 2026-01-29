-- Phase 113: Index Reconstitution Laggard Log
-- Tracks stocks entering indices due to relegation (poor performance)

CREATE TABLE IF NOT EXISTS index_reconstitution_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticker VARCHAR(10) NOT NULL,
    reconstitution_date DATE NOT NULL,
    old_index VARCHAR(100),
    new_index VARCHAR(100),
    event_type VARCHAR(20) NOT NULL, -- PROMOTION, RELEGATION
    market_cap_at_event DECIMAL(20, 2),
    performance_prev_12m DECIMAL(8, 6),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Check if TimescaleDB extension is available
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'timescaledb') THEN
        PERFORM create_hypertable('index_reconstitution_log', 'reconstitution_date', if_not_exists => TRUE);
    END IF;
END $$;

CREATE INDEX IF NOT EXISTS idx_reconst_ticker ON index_reconstitution_log(ticker);
