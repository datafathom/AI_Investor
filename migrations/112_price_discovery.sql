-- Phase 112: Price Discovery Delay Log
-- Tracks delays in market price adjustment attributed to passive dominance

CREATE TABLE IF NOT EXISTS price_discovery_delays (
    id UUID DEFAULT gen_random_uuid(),
    event_timestamp TIMESTAMPTZ NOT NULL,
    ticker VARCHAR(10) NOT NULL,
    
    -- Event Details
    event_type VARCHAR(50), -- EARNINGS, ANALYST, NEWS, MACRO
    expected_impact DECIMAL(8, 6),
    
    -- Delay Measurement
    discovery_delay_seconds INTEGER, -- Time to 90% price adjustment
    passive_pct_at_event DECIMAL(8, 6),
    
    -- Analysis
    attributed_to_passive BOOLEAN,
    correlation_score DECIMAL(5, 4),
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (id, event_timestamp)
);

-- Check if TimescaleDB extension is available
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'timescaledb') THEN
        PERFORM create_hypertable('price_discovery_delays', 'event_timestamp', if_not_exists => TRUE);
    END IF;
END $$;

CREATE INDEX IF NOT EXISTS idx_discovery_ticker ON price_discovery_delays(ticker, event_timestamp DESC);
