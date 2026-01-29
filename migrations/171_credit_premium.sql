-- Phase 171/172: Credit Tapes & Premium Terms
-- Purpose: Track underlying loan granularities and liquidity lock-ups.

CREATE TABLE IF NOT EXISTS credit_loan_tape (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fund_id UUID NOT NULL,
    borrower_sector VARCHAR(50),
    principal_balance DECIMAL(20, 2),
    interest_spread_bps INTEGER,
    default_status VARCHAR(20) DEFAULT 'CURRENT',
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS asset_liquidity_terms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_id UUID NOT NULL,
    lockup_period_months INTEGER,
    notice_period_days INTEGER DEFAULT 90,
    liquidity_frequency VARCHAR(20), -- QUARTERLY, ANNUALLY
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexing
CREATE INDEX IF NOT EXISTS idx_credit_fund ON credit_loan_tape(fund_id);
CREATE INDEX IF NOT EXISTS idx_asset_liquidity ON asset_liquidity_terms(asset_id);
