-- Phase 106: Concentration Risk Alerts
-- Detects and logs portfolio concentration risks

CREATE TABLE IF NOT EXISTS concentration_alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL,
    user_id UUID NOT NULL,
    
    -- Concentration Details
    concentration_type VARCHAR(50) NOT NULL,  -- ASSET_CLASS, SECTOR, SINGLE_HOLDING
    entity_id UUID NOT NULL,
    entity_name VARCHAR(255),
    
    -- Metrics
    current_weight DECIMAL(8, 6) NOT NULL,
    threshold_weight DECIMAL(8, 6) NOT NULL,
    excess_weight DECIMAL(8, 6) GENERATED ALWAYS AS 
        (current_weight - threshold_weight) STORED,
    
    -- Alert Status
    alert_level VARCHAR(20) NOT NULL,        -- WARNING, CRITICAL
    acknowledged BOOLEAN DEFAULT FALSE,
    acknowledged_at TIMESTAMPTZ,
    
    -- Timestamps
    triggered_at TIMESTAMPTZ DEFAULT NOW(),
    resolved_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_concentration_portfolio ON concentration_alerts(portfolio_id);
CREATE INDEX IF NOT EXISTS idx_concentration_level ON concentration_alerts(alert_level);
