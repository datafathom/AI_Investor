-- Phase 124: REIT Holdings Schema
-- Tracks real estate investment trust positions with property-type granularity

CREATE TABLE IF NOT EXISTS reit_holdings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL,
    reit_ticker VARCHAR(20) NOT NULL,
    
    -- Property Exposure
    property_type VARCHAR(50), -- RETAIL, DATA_CENTER, RESIDENTIAL, AGRICULTURE, OFFICE
    geographic_focus VARCHAR(255),
    
    -- Holdings
    shares DECIMAL(24, 6),
    cost_basis DECIMAL(20, 2),
    current_value DECIMAL(20, 2),
    weight_in_portfolio DECIMAL(8, 6),
    
    -- Income
    annual_dividend DECIMAL(20, 2),
    dividend_yield DECIMAL(8, 6),
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_reit_portfolio ON reit_holdings(portfolio_id);
CREATE INDEX IF NOT EXISTS idx_reit_type ON reit_holdings(property_type);
