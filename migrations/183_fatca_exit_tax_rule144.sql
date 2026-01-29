-- Phase 183/185: FATCA, Exit Tax & Rule 144
-- Purpose: Track global asset reporting and insider selling caps.

CREATE TABLE IF NOT EXISTS fatca_foreign_assets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    institution_name VARCHAR(100),
    country_code CHAR(2),
    max_value_ytd DECIMAL(20, 2),
    account_type VARCHAR(20), -- DEPOSITORY, CUSTODIAL
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS rule144_volume_limits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticker VARCHAR(10) PRIMARY KEY, -- Unique per stock
    shares_outstanding BIGINT,
    avg_weekly_vol_4wk BIGINT,
    last_updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS expat_exit_status (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL,
    is_covered_expatriate BOOLEAN DEFAULT FALSE,
    estimated_exit_tax_bill DECIMAL(20, 2),
    renunciation_date DATE,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexing
CREATE INDEX IF NOT EXISTS idx_fatca_user ON fatca_foreign_assets(user_id);
CREATE INDEX IF NOT EXISTS idx_expat_user ON expat_exit_status(user_id);
