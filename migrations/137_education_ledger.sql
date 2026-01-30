-- Phase 137: Education Plan Ledger
-- Tracks principal vs earnings for tax-advantaged 529 plans

CREATE TABLE IF NOT EXISTS education_plan_ledger (
    id UUID DEFAULT gen_random_uuid(),
    plan_id UUID NOT NULL,
    transaction_date DATE NOT NULL,
    transaction_type VARCHAR(20) NOT NULL, -- CONTRIBUTION, DISTRIBUTION, EARNINGS
    
    -- Amounts
    amount DECIMAL(24, 2) NOT NULL,
    principal_portion DECIMAL(24, 2), -- Return of basis
    earnings_portion DECIMAL(24, 2), -- Gain/Loss
    
    -- Distribution Details
    is_qualified_expense BOOLEAN,
    expense_category VARCHAR(50), -- TUITION, ROOM_BOARD, BOOKS, COMPUTER, STUDENT_LOAN
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (id, transaction_date)
);

-- Hypertable if TimescaleDB
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'timescaledb') THEN
        PERFORM create_hypertable('education_plan_ledger', 'transaction_date', if_not_exists => TRUE);
    END IF;
END $$;

CREATE INDEX IF NOT EXISTS idx_529_plan ON education_plan_ledger(plan_id);
