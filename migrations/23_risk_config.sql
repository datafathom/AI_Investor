-- Phase 23: Risk Guardrail Schema
-- Versions global risk parameters

CREATE TABLE IF NOT EXISTS risk_configurations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Parameters
    max_position_size_pct DECIMAL(5, 4) DEFAULT 0.01,  -- 1%
    daily_drawdown_limit_pct DECIMAL(5, 4) DEFAULT 0.03, -- 3%
    max_leverage_ratio DECIMAL(5, 2) DEFAULT 1.0,      -- 1x (No margin)
    
    -- Audit
    reason_for_change TEXT,
    approved_by_agent_id UUID,
    
    -- Temporal
    valid_from TIMESTAMPTZ DEFAULT NOW(),
    valid_to TIMESTAMPTZ,                              -- NULL = Current
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for finding active config
CREATE UNIQUE INDEX IF NOT EXISTS idx_active_config ON risk_configurations (valid_from) WHERE valid_to IS NULL;
