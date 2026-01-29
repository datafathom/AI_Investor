-- Phase 194/195: Cash Yield & DRS Custody
-- Purpose: Track yield arbitrage and direct registration status (UCC Article 8).

CREATE TABLE IF NOT EXISTS bank_yield_arbitrage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    office_id UUID NOT NULL,
    daily_balance DECIMAL(20, 2),
    lost_yield_bps INTEGER, -- Difference in BPS (e.g., 500)
    recaptured_revenue_ytd DECIMAL(20, 2),
    
    observation_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS security_registration_ledger (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_id UUID NOT NULL,
    registration_type VARCHAR(20), -- STREET_NAME, DRS, PHYSICAL
    transfer_agent_name VARCHAR(100),
    is_rehypothecation_allowed BOOLEAN DEFAULT FALSE,
    
    last_verified_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexing
CREATE INDEX IF NOT EXISTS idx_yield_office ON bank_yield_arbitrage(office_id, observation_date);
CREATE INDEX IF NOT EXISTS idx_drs_asset ON security_registration_ledger(asset_id);
