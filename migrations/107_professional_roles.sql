-- Phase 107: Professional Roles and Permissions
-- Strictly separates roles like Wealth Manager vs Asset Manager

CREATE TABLE IF NOT EXISTS professional_roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role_code VARCHAR(50) NOT NULL UNIQUE,
    role_name VARCHAR(100) NOT NULL,
    role_category VARCHAR(50) NOT NULL,     -- FIDUCIARY, NON_FIDUCIARY
    fiduciary_standard BOOLEAN NOT NULL,
    
    -- Revenue Model
    can_earn_commissions BOOLEAN DEFAULT FALSE,
    can_earn_aum_fees BOOLEAN DEFAULT TRUE,
    can_earn_performance_fees BOOLEAN DEFAULT FALSE,
    
    -- Conflict Rules
    exclusive_with JSONB DEFAULT '[]',       -- List of incompatible role codes
    requires_disclosure JSONB DEFAULT '[]',  -- Required disclosures
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- User Role Assignments
CREATE TABLE IF NOT EXISTS user_role_assignments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    role_id UUID NOT NULL REFERENCES professional_roles(id),
    client_id UUID,                          -- NULL for global, or specific client
    
    -- Assignment Status
    is_active BOOLEAN DEFAULT TRUE,
    assigned_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ,
    assigned_by UUID,
    
    -- Audit
    conflict_check_passed BOOLEAN NOT NULL,
    conflict_check_timestamp TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(user_id, role_id, client_id)
);

-- Permission Matrix
CREATE TABLE IF NOT EXISTS role_permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role_id UUID NOT NULL REFERENCES professional_roles(id),
    permission_code VARCHAR(100) NOT NULL,
    permission_scope VARCHAR(50) NOT NULL,   -- PORTFOLIO, CLIENT, TRADE, REPORT
    can_create BOOLEAN DEFAULT FALSE,
    can_read BOOLEAN DEFAULT FALSE,
    can_update BOOLEAN DEFAULT FALSE,
    can_delete BOOLEAN DEFAULT FALSE,
    
    UNIQUE(role_id, permission_code)
);

-- Seed Data (Basic)
INSERT INTO professional_roles (role_code, role_name, role_category, fiduciary_standard, can_earn_commissions, exclusive_with) 
VALUES
('WEALTH_MANAGER', 'Wealth Manager', 'FIDUCIARY', TRUE, FALSE, '["BROKER_DEALER"]'),
('ASSET_MANAGER', 'Asset Manager', 'NON_FIDUCIARY', FALSE, TRUE, '["FEE_ONLY_PLANNER"]'),
('FINANCIAL_PLANNER', 'Financial Planner', 'FIDUCIARY', TRUE, FALSE, '[]'),
('FEE_ONLY_PLANNER', 'Fee-Only Financial Planner', 'FIDUCIARY', TRUE, FALSE, '["ASSET_MANAGER", "BROKER_DEALER"]'),
('PRIVATE_BANKER', 'Private Banker', 'NON_FIDUCIARY', FALSE, TRUE, '[]'),
('BROKER_DEALER', 'Broker-Dealer', 'NON_FIDUCIARY', FALSE, TRUE, '["WEALTH_MANAGER", "FEE_ONLY_PLANNER"]')
ON CONFLICT (role_code) DO NOTHING;
