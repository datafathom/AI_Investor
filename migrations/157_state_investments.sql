
-- Migration for Phase 157: State 529 Plan Investments
CREATE TABLE IF NOT EXISTS state_529_investments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    state_code VARCHAR(2) NOT NULL,
    plan_name VARCHAR(100) NOT NULL,
    
    -- Investment Option
    fund_ticker VARCHAR(10),
    fund_name VARCHAR(255),
    asset_class VARCHAR(50),
    expense_ratio DECIMAL(5, 4),
    
    -- Restrictions
    is_open_to_non_residents BOOLEAN,
    min_contribution DECIMAL(10, 2),
    
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_529_state_code ON state_529_investments(state_code);
