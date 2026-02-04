-- Phase 132: Operational Workload Tracker
-- Tracks resource consumption for different investment strategies

CREATE TABLE IF NOT EXISTS operational_workload (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    strategy_type VARCHAR(20) NOT NULL, -- ACTIVE, PASSIVE, HYBRID
    model_name VARCHAR(100),
    
    -- Resource Usage
    research_hours_monthly DECIMAL(10, 2) DEFAULT 0,
    trading_minutes_monthly DECIMAL(10, 2) DEFAULT 0,
    monitoring_hours_monthly DECIMAL(10, 2) DEFAULT 0,
    
    -- Costs
    data_subscription_cost DECIMAL(10, 2) DEFAULT 0,
    tool_cost DECIMAL(10, 2) DEFAULT 0,
    
    log_date DATE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_ops_strategy ON operational_workload(strategy_type);
