-- Phase 181/182: Valuation Gaps & Passive Saturation
-- Purpose: Track hidden macro risks and index fund density.

CREATE TABLE IF NOT EXISTS valuation_nav_gaps (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_id UUID NOT NULL,
    proxy_ticker VARCHAR(10),
    reported_nav_change DECIMAL(10, 4),
    proxy_market_change DECIMAL(10, 4),
    current_gap_pct DECIMAL(10, 4),
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS passive_saturation_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticker VARCHAR(10) NOT NULL,
    passive_pct DECIMAL(10, 4),
    is_saturated_flag BOOLEAN DEFAULT FALSE,
    observation_date DATE DEFAULT CURRENT_DATE,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexing
CREATE INDEX IF NOT EXISTS idx_nav_gap_asset ON valuation_nav_gaps(asset_id);
CREATE INDEX IF NOT EXISTS idx_passive_ticker ON passive_saturation_log(ticker, observation_date);
