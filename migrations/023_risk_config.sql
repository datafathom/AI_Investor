-- Phase 23: Postgres Risk Guardrail Schema
-- Purpose: Defines structured tables for versioned and signed risk parameters.

CREATE TABLE IF NOT EXISTS risk_configurations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Versioning & Audit
    version INT NOT NULL,
    valid_from TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    valid_to TIMESTAMPTZ, -- NULL means current active
    
    -- Risk Parameters
    max_position_size_pct DECIMAL(5, 4) NOT NULL DEFAULT 0.0100, -- 1.0%
    daily_drawdown_limit_pct DECIMAL(5, 4) NOT NULL DEFAULT 0.0300, -- 3.0%
    max_leverage_ratio DECIMAL(5, 2) NOT NULL DEFAULT 1.00,
    min_stop_loss_pips DECIMAL(10, 2) NOT NULL DEFAULT 10.00,
    
    -- Security & Integrity
    configuration_hash CHAR(64) NOT NULL, -- SHA-256
    approved_by_agent_id VARCHAR(100) NOT NULL,
    reason_for_change TEXT,
    
    metadata JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Ensure only one active configuration exists per temporal window
CREATE UNIQUE INDEX IF NOT EXISTS idx_active_risk_config ON risk_configurations (valid_from) WHERE (valid_to IS NULL);

-- Index for temporal lookups
CREATE INDEX IF NOT EXISTS idx_risk_config_history ON risk_configurations (valid_from DESC, valid_to DESC);
