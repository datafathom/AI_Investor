-- Phase 142: Trust Funding Status
-- Tracks whether assets are correctly titled in the trust's name

CREATE TABLE IF NOT EXISTS trust_funding_status (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trust_id UUID NOT NULL,
    asset_id UUID NOT NULL,
    
    -- Status
    is_titled_correctly BOOLEAN DEFAULT FALSE,
    titling_verification_date DATE,
    
    -- Risk
    probate_risk_level VARCHAR(20) DEFAULT 'HIGH', -- HIGH (Not funded), LOW (Funded)
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_trust_funding_id ON trust_funding_status(trust_id);
CREATE INDEX IF NOT EXISTS idx_asset_funding_id ON trust_funding_status(asset_id);
