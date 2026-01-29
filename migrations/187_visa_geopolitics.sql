-- Phase 187/188: Geopolitics & Mobility
-- Purpose: Track country risks and citizenship hedge assets.

CREATE TABLE IF NOT EXISTS country_risk_profiles (
    country_code CHAR(2) PRIMARY KEY,
    sovereign_rating VARCHAR(10),
    sanction_status VARCHAR(20) DEFAULT 'NONE',
    tech_supply_chain_weight DECIMAL(5, 4),
    
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS golden_visa_tracker (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    country_code CHAR(2),
    investment_amount_usd DECIMAL(20, 2),
    holding_period_expiry DATE,
    residency_days_ytd INTEGER DEFAULT 0,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexing
CREATE INDEX IF NOT EXISTS idx_visa_user ON golden_visa_tracker(user_id);
