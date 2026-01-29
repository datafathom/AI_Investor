-- Phase 144: Spendthrift Trust Rules
-- Enforces withdrawal firewalls and creditor protection logic

CREATE TABLE IF NOT EXISTS spendthrift_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trust_id UUID NOT NULL,
    beneficiary_id UUID NOT NULL,
    
    -- Rules (e.g. $5k/month max)
    allowance_amount DECIMAL(20, 2) NOT NULL,
    allowance_frequency VARCHAR(20) DEFAULT 'MONTHLY',
    
    -- Overrides
    emergency_access_allowed BOOLEAN DEFAULT FALSE,
    emergency_approval_by_trustee BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_spendthrift_trust ON spendthrift_rules(trust_id, beneficiary_id);
