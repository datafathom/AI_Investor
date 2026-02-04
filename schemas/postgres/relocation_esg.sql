-- Phase 191/193: Relocation Taxes & ESG Rules
-- Purpose: Track mobility tax ROI and moral exclusion lists.

CREATE TABLE IF NOT EXISTS relocation_tax_scenarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    current_jurisdiction CHAR(2),
    target_jurisdiction CHAR(2),
    projected_annual_savings DECIMAL(20, 2),
    estimated_exit_tax DECIMAL(20, 2),
    breakeven_years DECIMAL(5, 2),
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS client_esg_exclusions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID NOT NULL,
    sector_code VARCHAR(20), -- OIL, TOBACCO, FIREARMS
    restriction_level INTEGER DEFAULT 5, -- 1-10
    is_hard_block BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexing
CREATE INDEX IF NOT EXISTS idx_relocation_user ON relocation_tax_scenarios(user_id);
CREATE INDEX IF NOT EXISTS idx_esg_client ON client_esg_exclusions(client_id);
