-- Phase 116: International Holdings and SOE Flags
-- Tracks international assets and flags state-owned enterprises

CREATE TABLE IF NOT EXISTS international_holdings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticker VARCHAR(20) NOT NULL,
    company_name VARCHAR(255),
    country_code VARCHAR(10),
    
    -- SOE Status
    is_state_owned BOOLEAN DEFAULT FALSE,
    government_ownership_pct DECIMAL(5, 4), -- e.g., 0.5100 = 51%
    controlling_entity VARCHAR(255),
    
    -- Risk Factors
    sanction_risk VARCHAR(20), -- NONE, LOW, MEDIUM, HIGH, CRITICAL
    repatriation_risk VARCHAR(20),
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_intl_ticker ON international_holdings(ticker);
CREATE INDEX IF NOT EXISTS idx_intl_soe ON international_holdings(is_state_owned) WHERE is_state_owned = TRUE;
