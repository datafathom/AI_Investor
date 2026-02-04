-- Migration Phase 178: SFO Family Constitution
CREATE TABLE IF NOT EXISTS family_constitution (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    family_id UUID NOT NULL,
    sections JSONB,                    -- {"Mission": "...", "Values": "...", "Voting": "..."}
    last_ratified_date DATE,
    ratified_by UUID[],                -- Array of Family Member IDs who signed
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_constitution_family ON family_constitution(family_id);
