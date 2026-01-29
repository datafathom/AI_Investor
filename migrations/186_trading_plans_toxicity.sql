-- Phase 186/190: trading Plans & Toxicity
-- Purpose: Automate safe selling and detect market stress.

CREATE TABLE IF NOT EXISTS trading_plans_10b51 (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    insider_id UUID NOT NULL,
    ticker VARCHAR(10) NOT NULL,
    creation_date DATE NOT NULL,
    cooling_off_period_days INTEGER DEFAULT 90,
    
    total_shares_to_sell INTEGER,
    shares_per_trade INTEGER,
    frequency_days INTEGER,
    
    status VARCHAR(20) DEFAULT 'COOLING_OFF', -- COOLING_OFF, ACTIVE, TERMINATED
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS global_market_toxicity (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticker VARCHAR(10) NOT NULL,
    vpin_score DECIMAL(5, 4),
    is_liquidity_at_risk BOOLEAN DEFAULT FALSE,
    observation_time TIMESTAMPTZ DEFAULT NOW()
);

-- Indexing
CREATE INDEX IF NOT EXISTS idx_10b51_status ON trading_plans_10b51(status);
CREATE INDEX IF NOT EXISTS idx_toxicity_ticker ON global_market_toxicity(ticker, observation_time DESC);
