-- Phase 109: Private Banking Clients and Team Assignments
-- Tracks UHNW clients and assigned relationship teams

CREATE TABLE IF NOT EXISTS private_banking_clients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    
    -- Qualification
    verified_net_worth DECIMAL(20, 2) NOT NULL,
    qualification_date DATE NOT NULL,
    verification_method VARCHAR(50), 
    last_verification TIMESTAMPTZ,
    
    -- Status
    tier VARCHAR(20) NOT NULL, -- PRIVATE ($10M+), ULTRA ($50M+), FAMILY_OFFICE ($100M+)
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Assigned Team
    relationship_manager_id UUID,
    investment_specialist_id UUID,
    lending_specialist_id UUID,
    estate_attorney_id UUID,
    
    -- Service Level
    service_level VARCHAR(50), -- WHITE_GLOVE, CONCIERGE, STANDARD
    max_clients_per_rm INTEGER DEFAULT 50,
    
    -- Metadata
    onboarded_at TIMESTAMPTZ DEFAULT NOW(),
    annual_review_date DATE
);

CREATE INDEX IF NOT EXISTS idx_pb_net_worth ON private_banking_clients(verified_net_worth);
CREATE INDEX IF NOT EXISTS idx_pb_tier ON private_banking_clients(tier);
