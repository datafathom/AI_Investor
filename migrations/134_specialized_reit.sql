-- Phase 134: Specialized REIT Metrics
-- Tracks sector-specific data for Data Centers and Farmland

CREATE TABLE IF NOT EXISTS specialized_reit_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticker VARCHAR(20) NOT NULL,
    sector VARCHAR(20) NOT NULL, -- DATA_CENTER, FARMLAND
    
    -- Common Metrics
    occupancy_rate DECIMAL(6, 4),
    rental_rate_growth DECIMAL(6, 4),
    
    -- Data Center Specific
    power_utilization DECIMAL(6, 4), -- % of Megawatt capacity used
    interconnection_count INTEGER,
    
    -- Farmland Specific
    harvest_yield_index DECIMAL(8, 2), -- Production index
    irrigation_coverage DECIMAL(6, 4),
    
    period_date DATE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_specialized_ticker ON specialized_reit_metrics(ticker);
CREATE INDEX IF NOT EXISTS idx_specialized_sector ON specialized_reit_metrics(sector);
