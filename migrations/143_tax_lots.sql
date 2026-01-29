-- Phase 143: Tax Lot Tracking & Harvesting
-- Granular tracking of cost basis for automated harvesting triggers

CREATE TABLE IF NOT EXISTS tax_lots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID NOT NULL,
    ticker VARCHAR(20) NOT NULL,
    
    -- Cost Basis
    quantity DECIMAL(20, 6) NOT NULL,
    cost_basis_per_share DECIMAL(20, 4) NOT NULL,
    purchase_date DATE NOT NULL,
    
    -- Current Status (Snapshot)
    current_price DECIMAL(20, 4),
    unrealized_pl DECIMAL(20, 2),
    unrealized_pl_pct DECIMAL(10, 4),
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Opportunities for harvesting
CREATE TABLE IF NOT EXISTS harvesting_opportunities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lot_id UUID NOT NULL REFERENCES tax_lots(id),
    
    potential_loss DECIMAL(24, 2) NOT NULL,
    harvest_priority VARCHAR(20) DEFAULT 'MEDIUM', -- HIGH, MEDIUM, LOW
    status VARCHAR(20) DEFAULT 'OPEN', -- OPEN, TRIGGERED, EXECUTED, IGNORED
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tax_lots_account ON tax_lots(account_id);
CREATE INDEX IF NOT EXISTS idx_tax_lots_ticker ON tax_lots(ticker);
