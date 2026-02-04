-- Migration Phase 179: SFO Network CRM
CREATE TABLE IF NOT EXISTS network_contacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    organization VARCHAR(100),
    role VARCHAR(50),
    
    -- Network Value Metrics
    deal_source_score INTEGER DEFAULT 5, -- 1-10
    expert_domain VARCHAR(50),          -- TECH, ENERGY, etc.
    relationship_strength INTEGER DEFAULT 3, -- 1-5
    
    owner_id UUID NOT NULL,             -- SFO User/Owner
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_network_domain ON network_contacts(expert_domain);
CREATE INDEX idx_network_owner ON network_contacts(owner_id);
