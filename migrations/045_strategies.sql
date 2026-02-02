-- Phase 45: Strategy Persistence
-- PURPOSE: Move trading strategies from transient cache to permanent system-of-record storage.

CREATE TABLE IF NOT EXISTS strategies (
    strategy_id VARCHAR(100) PRIMARY KEY,
    user_id UUID NOT NULL,
    strategy_name VARCHAR(255) NOT NULL,
    description TEXT,
    rules JSONB NOT NULL DEFAULT '[]',
    status VARCHAR(20) DEFAULT 'draft',
    portfolio_id VARCHAR(100),
    risk_limits JSONB NOT NULL DEFAULT '{}',
    last_executed TIMESTAMPTZ,
    created_date TIMESTAMPTZ DEFAULT NOW(),
    updated_date TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_strategies_user ON strategies(user_id);
CREATE INDEX IF NOT EXISTS idx_strategies_status ON strategies(status);
