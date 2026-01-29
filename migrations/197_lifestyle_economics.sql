-- Phase 197: Social Class Maintenance (SCM) & CLEW
-- Purpose: Track UHNW-specific inflation (CLEW) and generational wealth dilution.

CREATE TABLE IF NOT EXISTS clew_inflation_basket (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    category VARCHAR(50) NOT NULL, -- TUITION, AVIATION, STAFF, CLUB_DUES
    weight_pct DECIMAL(5, 4),      -- percentage of annual spend
    annual_inflation_rate DECIMAL(5, 4), -- e.g., 0.07 (7%)
    
    last_updated TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS family_generations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patriarch_id UUID NOT NULL,
    generation_level INTEGER DEFAULT 1, -- 1=Founder, 2=Children, 3=Grandchildren
    
    total_heirs_count INTEGER DEFAULT 1,
    projected_dilution_factor DECIMAL(5, 2), -- 1 / heirs_count
    
    target_wealth_per_capita DECIMAL(20, 2),
    current_wealth_per_capita DECIMAL(20, 2),
    
    status VARCHAR(20) DEFAULT 'MAINTAINING_CLASS', -- MAINTAINING_CLASS, DROPPING_CLASS
    
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexing
CREATE INDEX IF NOT EXISTS idx_clew_user ON clew_inflation_basket(user_id);
CREATE INDEX IF NOT EXISTS idx_family_patriarch ON family_generations(patriarch_id);
