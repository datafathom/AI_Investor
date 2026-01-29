-- Phase 108: Spending Categories and Benchmarks
-- Tracks categorized monthly spending and peer group benchmarks

CREATE TABLE IF NOT EXISTS spending_categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    month DATE NOT NULL,
    
    -- Core Categories
    housing DECIMAL(20, 2) DEFAULT 0,
    transportation DECIMAL(20, 2) DEFAULT 0,
    food_groceries DECIMAL(20, 2) DEFAULT 0,
    food_dining DECIMAL(20, 2) DEFAULT 0,
    healthcare DECIMAL(20, 2) DEFAULT 0,
    insurance DECIMAL(20, 2) DEFAULT 0,
    
    -- Lifestyle
    education DECIMAL(20, 2) DEFAULT 0,
    childcare DECIMAL(20, 2) DEFAULT 0,
    entertainment DECIMAL(20, 2) DEFAULT 0,
    travel DECIMAL(20, 2) DEFAULT 0,
    subscriptions DECIMAL(20, 2) DEFAULT 0,
    
    -- Financial
    debt_payments DECIMAL(20, 2) DEFAULT 0,
    savings_contributions DECIMAL(20, 2) DEFAULT 0,
    investments DECIMAL(20, 2) DEFAULT 0,
    
    -- Calculated
    total_spending DECIMAL(20, 2) GENERATED ALWAYS AS (
        housing + transportation + food_groceries + food_dining + 
        healthcare + insurance + education + childcare + 
        entertainment + travel + subscriptions + debt_payments
    ) STORED,
    savings_rate DECIMAL(8, 6),
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Check if TimescaleDB extension is available before creating hypertable
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'timescaledb') THEN
        PERFORM create_hypertable('spending_categories', 'month', if_not_exists => TRUE);
    END IF;
END $$;

CREATE INDEX IF NOT EXISTS idx_spending_user ON spending_categories(user_id, month DESC);

CREATE TABLE IF NOT EXISTS spending_benchmarks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    income_bracket VARCHAR(50) NOT NULL,
    category VARCHAR(100) NOT NULL,
    benchmark_percentage DECIMAL(8, 6) NOT NULL,
    benchmark_amount DECIMAL(20, 2),
    peer_group VARCHAR(50),
    data_source VARCHAR(100),
    year INTEGER NOT NULL
);
