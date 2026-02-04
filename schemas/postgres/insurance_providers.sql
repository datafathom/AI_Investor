-- Phase 111: Insurance Providers and Policies
-- Tracks insurance carriers and client coverage details

CREATE TABLE IF NOT EXISTS insurance_providers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    provider_type VARCHAR(50), -- CARRIER, BROKER, AGENT
    am_best_rating VARCHAR(10),
    specializations JSONB, -- ["LIFE", "PPLI", "PROPERTY"]
    licensed_states JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS insurance_policies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID NOT NULL,
    provider_id UUID REFERENCES insurance_providers(id),
    
    -- Policy Details
    policy_type VARCHAR(50) NOT NULL, -- TERM_LIFE, WHOLE_LIFE, PPLI, UMBRELLA
    policy_number VARCHAR(100),
    
    -- Coverage
    death_benefit DECIMAL(20, 2),
    cash_value DECIMAL(20, 2),
    annual_premium DECIMAL(20, 2),
    
    -- Term Details
    effective_date DATE,
    expiration_date DATE,
    
    -- Status
    status VARCHAR(20) DEFAULT 'ACTIVE',
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_insurance_client ON insurance_policies(client_id);
