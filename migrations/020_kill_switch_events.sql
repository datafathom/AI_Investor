-- Phase 20: Asset Kill Switch Audit
-- Purpose: Records all nuclear-level liquidation events.

CREATE TABLE IF NOT EXISTS kill_switch_audit (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    symbol VARCHAR(20) NOT NULL,
    entry_price DECIMAL(20, 8) NOT NULL,
    trigger_price DECIMAL(20, 8) NOT NULL,
    drawdown_pct DECIMAL(10, 4) NOT NULL,
    reason TEXT NOT NULL,
    market_snapshot JSONB,
    is_demo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS idx_ks_audit_symbol ON kill_switch_audit(symbol, timestamp DESC);
