-- Phase 114: Fee Schedules and Billing Records
-- Tracks client fee structures (AUM, Performance) and billing cycles

CREATE TABLE IF NOT EXISTS fee_schedules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID NOT NULL,
    advisor_id UUID NOT NULL,
    
    -- Fee Structure
    fee_type VARCHAR(20) NOT NULL, -- AUM, FLAT, HOURLY, PERFORMANCE
    base_fee_pct DECIMAL(8, 6),
    
    -- Tiered Fees (Declining Balance)
    tier_1_max DECIMAL(20, 2), -- First $1M
    tier_1_rate DECIMAL(8, 6), -- 1.0%
    tier_2_max DECIMAL(20, 2), -- $1M - $5M
    tier_2_rate DECIMAL(8, 6), -- 0.75%
    tier_3_rate DECIMAL(8, 6), -- >$5M: 0.50%
    
    -- Billing
    billing_frequency VARCHAR(20), -- MONTHLY, QUARTERLY, ANNUALLY
    billing_method VARCHAR(20), -- ADVANCE, ARREARS
    
    effective_date DATE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS billing_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fee_schedule_id UUID REFERENCES fee_schedules(id),
    billing_period_start DATE,
    billing_period_end DATE,
    
    -- Amounts
    aum_at_billing DECIMAL(20, 2),
    gross_fee DECIMAL(20, 2),
    proration_factor DECIMAL(8, 6),
    net_fee DECIMAL(20, 2),
    
    -- Status
    status VARCHAR(20) DEFAULT 'PENDING',
    invoiced_at TIMESTAMPTZ,
    paid_at TIMESTAMPTZ,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_billing_schedule ON billing_records(fee_schedule_id);
CREATE INDEX IF NOT EXISTS idx_fee_client ON fee_schedules(client_id);
