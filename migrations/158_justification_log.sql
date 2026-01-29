-- Phase 158: Fiduciary Best Interest Justification Log
-- Purpose: Immutable record of why specific financial recommendations were made.

CREATE TABLE IF NOT EXISTS fiduciary_justifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recommendation_id UUID NOT NULL,
    client_id UUID NOT NULL,
    advisor_id UUID NOT NULL,
    
    -- The "Why"
    rationale_code VARCHAR(50) NOT NULL, -- REBALANCE, TAX_LOSS, RISK_REDUCTION, LOWER_COST
    rationale_text TEXT NOT NULL,
    
    -- Comparison
    considered_alternatives JSONB,
    cost_comparison_result VARCHAR(50), -- LOWER_TOTAL_COST, HIGHER_AFTER_TAX_RETURN
    
    recorded_at TIMESTAMPTZ DEFAULT NOW(),
    is_immutable BOOLEAN DEFAULT TRUE
);

-- Indexing for compliance audits
CREATE INDEX IF NOT EXISTS idx_fiduciary_client ON fiduciary_justifications(client_id);
CREATE INDEX IF NOT EXISTS idx_fiduciary_date ON fiduciary_justifications(recorded_at);
