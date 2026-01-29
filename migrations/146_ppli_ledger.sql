-- Phase 146: PPLI Cash Value & Loan Ledger
-- Purpose: Track policy value, loans (tax-free withdrawals), and cost of insurance.

CREATE TABLE IF NOT EXISTS ppli_ledger (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    policy_id UUID NOT NULL,
    transaction_date DATE NOT NULL,
    
    -- Values
    cash_value DECIMAL(20, 2) NOT NULL,
    loan_balance DECIMAL(20, 2) DEFAULT 0.0,
    
    -- Charges
    cost_of_insurance DECIMAL(10, 2),    -- COI / M&E charges
    admin_fees DECIMAL(10, 2),
    
    -- Status
    lapse_risk_years INTEGER,            -- Projected years until lapse at current drain
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexing for performance
CREATE INDEX IF NOT EXISTS idx_ppli_ledger_policy_id ON ppli_ledger(policy_id);
