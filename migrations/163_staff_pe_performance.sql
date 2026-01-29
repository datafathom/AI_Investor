-- Phase 163/164: FO Staff Comp & PE Performance
-- Purpose: Tracking the humans and the high-ticket deals.

CREATE TABLE IF NOT EXISTS staff_hr_comp (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    employee_id UUID NOT NULL,
    role_title VARCHAR(50) NOT NULL,
    base_salary DECIMAL(20, 2),
    target_bonus_pct DECIMAL(5, 2),
    is_active BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS pe_vc_performance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    deal_name VARCHAR(100) NOT NULL,
    asset_type VARCHAR(20) NOT NULL, -- LBO, VC, GROWTH
    invested_capital DECIMAL(20, 2),
    current_nav DECIMAL(20, 2),
    realized_distributions DECIMAL(20, 2),
    
    -- Calculated Metrics (Snapshot)
    moic DECIMAL(5, 2),
    irr_pct DECIMAL(10, 2),
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexing
CREATE INDEX IF NOT EXISTS idx_staff_role ON staff_hr_comp(role_title);
CREATE INDEX IF NOT EXISTS idx_pe_asset ON pe_vc_performance(asset_type);
