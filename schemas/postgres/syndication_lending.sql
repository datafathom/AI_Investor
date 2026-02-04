-- Phase 166/167: Deal Economics & Lending Analysis
-- Purpose: Track private waterfalls and stock-based borrowing scenarios.

CREATE TABLE IF NOT EXISTS syndication_economics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    deal_name VARCHAR(100) NOT NULL,
    pref_return_pct DECIMAL(5, 4) DEFAULT 0.08,
    gp_promote_pct DECIMAL(5, 4) DEFAULT 0.20,
    lp_capital_total DECIMAL(20, 2),
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS lending_tax_simulation (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    estimated_tax_hit DECIMAL(20, 2),
    annual_interest_cost DECIMAL(20, 2),
    recommended_action VARCHAR(20), -- BORROW, SELL
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexing
CREATE INDEX IF NOT EXISTS idx_syndication_name ON syndication_economics(deal_name);
CREATE INDEX IF NOT EXISTS idx_lending_user ON lending_tax_simulation(user_id);
