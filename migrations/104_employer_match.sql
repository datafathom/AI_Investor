-- Phase 104: Employer Matching and Contribution History
-- Tracks employer matches for 401k/plans and contribution history

CREATE TABLE IF NOT EXISTS employer_match_config (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    employer_name VARCHAR(255) NOT NULL,
    
    -- Matching Formula
    match_type VARCHAR(20) NOT NULL,        -- DOLLAR_FOR_DOLLAR, PARTIAL, TIERED
    match_percentage DECIMAL(5, 2) NOT NULL, -- e.g., 50% = 0.50
    max_match_percentage DECIMAL(5, 2),      -- Max % of salary matched
    annual_match_cap DECIMAL(20, 2),         -- Dollar cap on match
    
    -- Tiered Matching (if applicable)
    tier_1_employee_pct DECIMAL(5, 2),       -- e.g., First 3%
    tier_1_employer_pct DECIMAL(5, 2),       -- e.g., 100% match
    tier_2_employee_pct DECIMAL(5, 2),       -- e.g., Next 2%
    tier_2_employer_pct DECIMAL(5, 2),       -- e.g., 50% match
    
    -- Vesting Schedule
    vesting_type VARCHAR(20),                -- IMMEDIATE, CLIFF, GRADED
    vesting_cliff_months INTEGER,
    vesting_schedule JSONB,                  -- {"12": 0.20, "24": 0.40, ...}
    
    -- Status
    effective_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS contribution_history (
    id UUID DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    account_id UUID NOT NULL,
    contribution_date DATE NOT NULL,
    
    -- Contribution Details
    employee_contribution DECIMAL(20, 2) NOT NULL,
    employer_match DECIMAL(20, 2) NOT NULL,
    total_contribution DECIMAL(20, 2) GENERATED ALWAYS AS 
        (employee_contribution + employer_match) STORED,
    
    -- Running Totals (YTD)
    ytd_employee_total DECIMAL(20, 2),
    ytd_employer_total DECIMAL(20, 2),
    ytd_total DECIMAL(20, 2),
    
    -- Limits
    annual_limit DECIMAL(20, 2),           -- IRS limit for year
    remaining_room DECIMAL(20, 2),
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (id, contribution_date)
);

-- Check if TimescaleDB extension is available before creating hypertable
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'timescaledb') THEN
        PERFORM create_hypertable('contribution_history', 'contribution_date', if_not_exists => TRUE);
    END IF;
END $$;

CREATE INDEX IF NOT EXISTS idx_contrib_user ON contribution_history(user_id, contribution_date DESC);
CREATE INDEX IF NOT EXISTS idx_match_user ON employer_match_config(user_id);
