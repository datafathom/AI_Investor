-- Phase 103: Emergency Fund Status Table
-- Tracks liquid cash vs monthly expenses

CREATE TABLE IF NOT EXISTS emergency_fund_status (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL, -- Assuming users table exists from previous phases
    
    -- Cash Reserves
    total_liquid_cash DECIMAL(20, 2) NOT NULL,
    checking_balance DECIMAL(20, 2),
    savings_balance DECIMAL(20, 2),
    money_market_balance DECIMAL(20, 2),
    
    -- Expense Tracking
    monthly_expenses DECIMAL(20, 2) NOT NULL,
    annual_expenses DECIMAL(20, 2) GENERATED ALWAYS AS (monthly_expenses * 12) STORED,
    
    -- Coverage Metrics
    months_of_coverage DECIMAL(6, 2) GENERATED ALWAYS AS (
        CASE WHEN monthly_expenses > 0 
        THEN total_liquid_cash / monthly_expenses 
        ELSE 0 END
    ) STORED,
    
    -- Risk Assessment
    coverage_tier VARCHAR(20),   -- CRITICAL, LOW, ADEQUATE, STRONG, FORTRESS
    income_stability_score DECIMAL(5, 2),
    career_risk_factor DECIMAL(5, 2),
    
    -- Metadata
    last_calculated TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Convert to hypertable for time-series analysis of liquidity
SELECT create_hypertable('emergency_fund_status', 'last_calculated', if_not_exists => TRUE);

CREATE INDEX IF NOT EXISTS idx_emergency_user ON emergency_fund_status(user_id, last_calculated DESC);
