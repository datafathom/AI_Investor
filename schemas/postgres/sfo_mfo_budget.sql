-- Phase 161/162: Family Office Economic Tables
-- Purpose: Track institutional-grade budgets and trade-level allocations.

CREATE TABLE IF NOT EXISTS sfo_operating_budget (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    office_name VARCHAR(100) NOT NULL,
    fiscal_year INTEGER NOT NULL,
    
    -- Categories
    compensation_total DECIMAL(20, 2), -- CIO, Analysts, Accountants
    technology_total DECIMAL(20, 2),     -- Bloomberg, Trading Systems
    rent_ops_total DECIMAL(20, 2),
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS trade_blocks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    symbol VARCHAR(10) NOT NULL,
    total_shares DECIMAL(20, 6) NOT NULL,
    avg_price DECIMAL(20, 4),
    execution_status VARCHAR(20) DEFAULT 'PENDING', -- PENDING, FILLED
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS block_allocations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    block_id UUID NOT NULL REFERENCES trade_blocks(id),
    family_id UUID NOT NULL,
    allocated_shares DECIMAL(20, 6) NOT NULL,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexing
CREATE INDEX IF NOT EXISTS idx_budget_year ON sfo_operating_budget(fiscal_year);
CREATE INDEX IF NOT EXISTS idx_block_symbol ON trade_blocks(symbol);
