-- Phase 2 Migration: Fear & Greed Index
-- Created: 2026-01-18

CREATE TABLE IF NOT EXISTS fear_greed_index (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    score INTEGER NOT NULL CHECK (score >= 0 AND score <= 100),
    rating VARCHAR(50) NOT NULL, -- e.g., "Extreme Fear"
    components JSONB DEFAULT '{}' -- Store individual component scores (VIX, Momentum, etc.)
);

CREATE INDEX IF NOT EXISTS idx_fear_greed_timestamp ON fear_greed_index(timestamp DESC);
