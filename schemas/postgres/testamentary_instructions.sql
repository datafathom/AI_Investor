
-- Migration for Phase 153: Testamentary Instructions
CREATE TABLE IF NOT EXISTS testamentary_instructions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    will_id UUID NOT NULL,
    
    -- Creation Triggers
    trigger_condition VARCHAR(100),    -- IF_SPOUSE_PREDECEASED
    trust_name VARCHAR(100),           -- "Children's Trust"
    
    -- Terms
    trustee_id UUID,
    distribution_ages JSONB,           -- {25: 0.33, 30: 0.33, 35: 0.34}
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_will_id ON testamentary_instructions(will_id);
