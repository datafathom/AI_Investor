-- Phase 101: Advisor Table with Fiduciary Status
-- Establish core data structures for advisors

CREATE TABLE IF NOT EXISTS advisors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    
    -- Fiduciary Status
    fiduciary_status BOOLEAN NOT NULL DEFAULT FALSE,
    fiduciary_type VARCHAR(50),  -- RIA, BROKER_DEALER, HYBRID
    
    -- Registration
    registration_type VARCHAR(20) NOT NULL,  -- SEC, STATE
    registration_number VARCHAR(50),
    registration_state VARCHAR(2),
    sec_crd_number VARCHAR(20),
    
    -- Firm Details
    firm_name VARCHAR(255),
    firm_type VARCHAR(50),  -- RIA, WIREHOUSE, INDEPENDENT
    
    -- Compliance
    aum_under_management DECIMAL(20, 2),
    fee_structure VARCHAR(50),  -- FEE_ONLY, COMMISSION, HYBRID
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_advisors_fiduciary ON advisors(fiduciary_status);
CREATE INDEX IF NOT EXISTS idx_advisors_registration ON advisors(registration_type);
