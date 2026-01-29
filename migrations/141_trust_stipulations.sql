-- Phase 141: Trust Stipulations
-- Stores legal clauses and distribution conditions for trust entities

CREATE TABLE IF NOT EXISTS trust_stipulations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trust_id UUID NOT NULL,
    clause_type VARCHAR(50) NOT NULL, -- DISTRIBUTION, INVESTMENT, SUCCESSION, TAX
    description TEXT NOT NULL,
    
    -- Logic triggers
    trigger_condition VARCHAR(100), -- e.g., 'AGE > 25', 'GRADUATION'
    enforcement_level VARCHAR(20) DEFAULT 'STRICT', -- STRICT, DISCRETIONARY
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_trust_stipulations_id ON trust_stipulations(trust_id);
CREATE INDEX IF NOT EXISTS idx_trust_clause_type ON trust_stipulations(clause_type);
