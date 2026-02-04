-- Phase 152: Probate Thresholds & Metadata
-- Purpose: Store state-specific limits for 'Small Estate' simplified procedures vs Full Probate.

CREATE TABLE IF NOT EXISTS probate_metadata (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    state_code VARCHAR(2) NOT NULL UNIQUE,
    small_estate_limit DECIMAL(20, 2) NOT NULL,
    default_probate_duration_months INTEGER DEFAULT 18,
    statutory_fee_model VARCHAR(50) DEFAULT 'CA_TIERED',
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Seed data for primary states
INSERT INTO probate_metadata (state_code, small_estate_limit, statutory_fee_model)
VALUES 
('CA', 184500.00, 'CA_TIERED'),
('NY', 50000.00, 'FIXED_PCT'),
('FL', 75000.00, 'FIXED_PCT')
ON CONFLICT (state_code) DO NOTHING;
