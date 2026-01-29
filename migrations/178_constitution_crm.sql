-- Phase 178/179: Constitutions, CRM & Networks
-- Purpose: Track generational values and external relationship nodes.

CREATE TABLE IF NOT EXISTS family_constitution (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    family_id UUID NOT NULL,
    mission_statement TEXT,
    core_values JSONB,
    governance_rules JSONB,
    
    version INTEGER DEFAULT 1,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sfo_crm_contacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    office_id UUID NOT NULL,
    contact_name VARCHAR(150),
    organization VARCHAR(150),
    deal_priority_score INTEGER DEFAULT 5, -- 1-10
    has_signed_nda BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexing
CREATE INDEX IF NOT EXISTS idx_constitution_family ON family_constitution(family_id);
CREATE INDEX IF NOT EXISTS idx_crm_office ON sfo_crm_contacts(office_id);
