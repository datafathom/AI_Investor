-- Phase 21: Portfolio Circuit Breaker Audit
-- Purpose: Records global "Zen Mode" freeze events and session-level drawdowns.

CREATE TABLE IF NOT EXISTS circuit_breaker_audit (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    start_equity DECIMAL(20, 8) NOT NULL,
    current_equity DECIMAL(20, 8) NOT NULL,
    drawdown_pct DECIMAL(10, 4) NOT NULL,
    action_taken VARCHAR(50) NOT NULL, -- e.g., 'SYSTEM_FREEZE', 'ADMIN_LOCK'
    reason TEXT,
    is_demo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS idx_cb_audit_time ON circuit_breaker_audit(timestamp DESC);
