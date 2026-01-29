-- Phase 180: Global Risk & Multi-Currency Ledger
-- Purpose: Prepping for Geopolitical volatility and multi-nation oversight.

CREATE TABLE IF NOT EXISTS global_macro_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type VARCHAR(50) NOT NULL, -- GEOPOLITICAL, MONETARY
    country_code CHAR(2),
    severity_rank INTEGER, -- 1-10
    description TEXT,
    
    impacted_assets UUID[],
    event_time TIMESTAMPTZ DEFAULT NOW()
);

-- multi-currency support columns for existing ledgers
-- (Simulated for this migration)
-- ALTER TABLE ppli_transaction_ledger ADD COLUMN local_currency_code CHAR(3) DEFAULT 'USD';
-- ALTER TABLE ppli_transaction_ledger ADD COLUMN fx_rate_to_usd DECIMAL(15, 6) DEFAULT 1.0;

-- Indexing
CREATE INDEX IF NOT EXISTS idx_macro_type ON global_macro_events(event_type);
CREATE INDEX IF NOT EXISTS idx_macro_country ON global_macro_events(country_code);
