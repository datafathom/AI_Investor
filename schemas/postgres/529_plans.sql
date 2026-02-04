-- Phase 108: 529 College Savings Plans
-- Tracks 529 plan details, beneficiaries, and glide paths

CREATE TABLE IF NOT EXISTS plans_529 (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    beneficiary_id UUID NOT NULL,
    
    -- Plan Details
    plan_name VARCHAR(255) NOT NULL,
    state VARCHAR(2) NOT NULL,
    is_resident_plan BOOLEAN DEFAULT FALSE,
    custodian VARCHAR(100),
    
    -- Beneficiary Info
    beneficiary_name VARCHAR(255),
    beneficiary_birth_date DATE NOT NULL,
    target_college_year INTEGER GENERATED ALWAYS AS (
        EXTRACT(YEAR FROM beneficiary_birth_date) + 18
    ) STORED,
    years_to_enrollment INTEGER,
    
    -- Funding
    current_balance DECIMAL(20, 2) DEFAULT 0,
    monthly_contribution DECIMAL(20, 2) DEFAULT 0,
    
    -- Goals
    target_college VARCHAR(100),
    estimated_cost DECIMAL(20, 2),
    projected_gap DECIMAL(20, 2),
    
    -- Portfolio
    portfolio_type VARCHAR(50), 
    current_equity_allocation DECIMAL(8, 6),
    target_equity_allocation DECIMAL(8, 6),
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS glide_paths_529 (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plan_id UUID NOT NULL REFERENCES plans_529(id),
    years_to_enrollment INTEGER NOT NULL,
    equity_allocation DECIMAL(8, 6) NOT NULL,
    fixed_income_allocation DECIMAL(8, 6) NOT NULL,
    money_market_allocation DECIMAL(8, 6) NOT NULL,
    UNIQUE (plan_id, years_to_enrollment)
);

CREATE INDEX IF NOT EXISTS idx_529_user ON plans_529(user_id);
