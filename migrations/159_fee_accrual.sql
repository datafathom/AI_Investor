-- Phase 159: Management Fee Accruals
-- Purpose: Track daily accruals for AUM-based and performance-based fees.

CREATE TABLE IF NOT EXISTS fee_accruals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID NOT NULL,
    accrual_date DATE NOT NULL,
    
    -- Values
    daily_aum DECIMAL(20, 2),
    mgmt_fee_rate_annual DECIMAL(5, 4) DEFAULT 0.02, -- 2% Default
    accrued_mgmt_fee DECIMAL(15, 2),
    
    -- Performance Tracking
    is_performance_billed BOOLEAN DEFAULT FALSE,
    peak_nav DECIMAL(20, 2), -- For High Water Mark logic
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexing
CREATE INDEX IF NOT EXISTS idx_accrual_account ON fee_accruals(account_id, accrual_date);
