-- Phase 138: Risk Metrics History
-- Stores daily snapshots of risk-adjusted performance ratios

CREATE TABLE IF NOT EXISTS risk_metrics_history (
    id UUID DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL,
    metric_date DATE NOT NULL,
    
    -- Annualized Ratios
    sharpe_ratio DECIMAL(10, 4),
    sortino_ratio DECIMAL(10, 4),
    treynor_ratio DECIMAL(10, 4),
    information_ratio DECIMAL(10, 4),
    calmar_ratio DECIMAL(10, 4),
    
    -- Inputs
    annualized_return DECIMAL(10, 6),
    annualized_volatility DECIMAL(10, 6),
    max_drawdown DECIMAL(10, 6),
    beta DECIMAL(10, 6),
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (id, metric_date)
);

-- Hypertable if TimescaleDB
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'timescaledb') THEN
        PERFORM create_hypertable('risk_metrics_history', 'metric_date', if_not_exists => TRUE);
    END IF;
END $$;

CREATE INDEX IF NOT EXISTS idx_risk_portfolio_date ON risk_metrics_history(portfolio_id, metric_date);
