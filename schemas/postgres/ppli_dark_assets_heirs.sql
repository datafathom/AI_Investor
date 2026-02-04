-- Phase 168/170: PPLI Ledgers & Heir KPI Overrides
-- Purpose: Track tax-free growth and family HR governance.

CREATE TABLE IF NOT EXISTS ppli_transaction_ledger (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    policy_id UUID NOT NULL,
    amount DECIMAL(20, 2) NOT NULL,
    tx_type VARCHAR(20) NOT NULL, -- PREMIUM, LOAN, GAIN
    is_tax_exempt BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS dark_asset_ledger (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    office_id UUID NOT NULL,
    asset_name_obfuscated VARCHAR(255) NOT NULL,
    current_value DECIMAL(20, 2),
    is_manually_synced BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS heir_kpi_overrides (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    heir_employee_id UUID NOT NULL,
    bonus_override_amount DECIMAL(20, 2),
    justification_text TEXT,
    is_market_aligned BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexing
CREATE INDEX IF NOT EXISTS idx_ppli_policy ON ppli_transaction_ledger(policy_id);
CREATE INDEX IF NOT EXISTS idx_heir_override ON heir_kpi_overrides(heir_employee_id);
