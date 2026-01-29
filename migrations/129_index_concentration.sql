-- Phase 129: Index Concentration
-- Tracks overconcentration in cap-weighted indices

CREATE TABLE IF NOT EXISTS index_concentration_snapshots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    snapshot_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    index_ticker VARCHAR(20) NOT NULL,
    
    top_5_weight DECIMAL(8, 6) NOT NULL,
    top_10_weight DECIMAL(8, 6) NOT NULL,
    top_20_weight DECIMAL(8, 6) NOT NULL,
    
    herfindahl_index DECIMAL(10, 8),
    effective_holdings INTEGER,
    
    concentration_level VARCHAR(20), -- NORMAL, ELEVATED, HIGH, CRITICAL
    threshold_breached BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Check if TimescaleDB extension is available
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'timescaledb') THEN
        PERFORM create_hypertable('index_concentration_snapshots', 'snapshot_timestamp', if_not_exists => TRUE);
    END IF;
END $$;

CREATE INDEX IF NOT EXISTS idx_index_snapshot_ticker ON index_concentration_snapshots(index_ticker);
