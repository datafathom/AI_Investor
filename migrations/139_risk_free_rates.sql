-- Phase 139: Risk-Free Rate History
-- Tracks daily Treasury yields for risk calculations

CREATE TABLE IF NOT EXISTS risk_free_rates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rate_date DATE NOT NULL UNIQUE,
    
    -- Yields (as decimals, e.g. 0.045 for 4.5%)
    yield_3mo DECIMAL(6, 4),
    yield_2yr DECIMAL(6, 4),
    yield_10yr DECIMAL(6, 4),
    yield_30yr DECIMAL(6, 4),
    
    -- Inversion logic
    is_inverted_10y_2y BOOLEAN GENERATED ALWAYS AS (yield_10yr < yield_2yr) STORED,
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Hypertable if TimescaleDB
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'timescaledb') THEN
        PERFORM create_hypertable('risk_free_rates', 'rate_date', if_not_exists => TRUE);
    END IF;
END $$;
