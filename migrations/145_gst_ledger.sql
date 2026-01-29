-- Phase 145: Generation-Skipping Transfer (GST) Exemption Ledger
-- Purpose: Trace allocation of GST exemption and ensure the trust remains GST Exempt.

CREATE TABLE IF NOT EXISTS gst_exemption_ledger (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trust_id UUID NOT NULL,
    transaction_date DATE NOT NULL,
    
    -- Contribution
    contribution_amount DECIMAL(20, 2),
    gst_exemption_allocated DECIMAL(20, 2),
    
    -- Ratios
    inclusion_ratio DECIMAL(5, 4) DEFAULT 0.0,         -- 0.0 = Fully Exempt, 1.0 = Fully Taxable
    applicable_fraction DECIMAL(5, 4) DEFAULT 1.0,     -- 1 - Inclusion Ratio
    
    -- Tax Event
    taxable_distribution_amount DECIMAL(20, 2) DEFAULT 0.0,
    gst_tax_due DECIMAL(20, 2) DEFAULT 0.0,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexing for performance
CREATE INDEX IF NOT EXISTS idx_gst_ledger_trust_id ON gst_exemption_ledger(trust_id);
