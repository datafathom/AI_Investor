-- Phase 109: Tax Deferral Strategy Tracking
-- Tracks installment sales, opportunity zones, and 1031 exchanges

CREATE TABLE IF NOT EXISTS tax_deferral_strategies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID NOT NULL REFERENCES private_banking_clients(id),
    
    -- Strategy Details
    strategy_type VARCHAR(50) NOT NULL,       -- INSTALLMENT_SALE, OPPORTUNITY_ZONE, 1031_EXCHANGE, OPTION_TIMING
    description TEXT,
    
    -- Amounts
    gain_deferred DECIMAL(20, 2) NOT NULL,
    tax_savings_estimate DECIMAL(20, 2),
    
    -- Timeline
    initiation_date DATE NOT NULL,
    expiration_date DATE,
    days_remaining INTEGER,
    
    -- Status
    status VARCHAR(20) DEFAULT 'ACTIVE',
    compliance_verified BOOLEAN DEFAULT FALSE,
    
    -- Opportunity Zone Specific
    oz_investment_id UUID,
    oz_holding_period_start DATE,
    oz_10_year_exclusion_eligible BOOLEAN,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tax_deferral_client ON tax_deferral_strategies(client_id);
