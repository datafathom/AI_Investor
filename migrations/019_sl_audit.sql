-- Phase 19: Stop Loss Audit Trail
-- Purpose: Records all sentinel triggers and stop-loss modifications.

CREATE TABLE IF NOT EXISTS stop_loss_audit (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    trade_id UUID NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    action_type VARCHAR(50) NOT NULL, -- e.g., 'TRIGGERED', 'TIGHTENED', 'REMOVAL_BLOCKED'
    current_sl DECIMAL(20, 8),
    new_sl DECIMAL(20, 8),
    trigger_price DECIMAL(20, 8),
    reason TEXT,
    agent_id VARCHAR(100),
    is_demo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS idx_sl_audit_trade ON stop_loss_audit(trade_id, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_sl_audit_type ON stop_loss_audit(action_type);
