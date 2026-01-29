-- Phase 105: IRA Optimization Profiles
-- Tracks tax situations and recommended strategies for contribution types

CREATE TABLE IF NOT EXISTS ira_optimization_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    
    -- Current Tax Situation
    current_marginal_rate DECIMAL(5, 4) NOT NULL,  -- e.g., 0.32 = 32%
    current_effective_rate DECIMAL(5, 4),
    current_agi DECIMAL(20, 2),
    filing_status VARCHAR(20),  -- SINGLE, MARRIED_JOINT, HEAD_OF_HOUSEHOLD
    
    -- Projected Retirement Tax Situation
    projected_retirement_rate DECIMAL(5, 4),
    projected_retirement_income DECIMAL(20, 2),
    expected_social_security DECIMAL(20, 2),
    expected_pension_income DECIMAL(20, 2),
    
    -- Time Horizon
    current_age INTEGER NOT NULL,
    retirement_age INTEGER NOT NULL,
    life_expectancy INTEGER DEFAULT 90,
    years_to_retirement INTEGER GENERATED ALWAYS AS (retirement_age - current_age) STORED,
    
    -- Recommendation
    recommended_strategy VARCHAR(20),  -- TRADITIONAL, ROTH, SPLIT
    split_percentage_roth DECIMAL(5, 2),
    recommendation_confidence DECIMAL(5, 2),
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_ira_user ON ira_optimization_profiles(user_id);
