
-- Migration for Phase 147: CRT Distributions
CREATE TABLE IF NOT EXISTS crt_distributions (
    id UUID DEFAULT gen_random_uuid(),
    trust_id UUID NOT NULL,
    year INTEGER NOT NULL,
    
    -- Rules
    payout_type VARCHAR(10),               -- CRUT (%), CRAT (Fixed $)
    payout_rate DECIMAL(5, 4),             -- e.g. 0.06 (6%)
    
    -- Calculation
    trust_value_jan1 DECIMAL(20, 2),
    required_distribution DECIMAL(20, 2),
    
    -- Execution
    distributed_amount DECIMAL(20, 2),
    distribution_date DATE NOT NULL, -- Made NOT NULL for partitioning
    tier_source VARCHAR(50),               -- ORDINARY, CAP_GAIN, EXEMPT, CORPUS
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (id, distribution_date)
);

SELECT create_hypertable('crt_distributions', 'distribution_date', if_not_exists => TRUE);
CREATE INDEX IF NOT EXISTS idx_crt_trust_id ON crt_distributions(trust_id);
