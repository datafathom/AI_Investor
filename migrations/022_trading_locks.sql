-- Phase 22: Trading Cooldowns & Locks
-- Purpose: Tracks mandatory cooling-off periods and behavioral audit logs.

CREATE TABLE IF NOT EXISTS trading_locks (
    id BIGSERIAL PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    lock_type VARCHAR(50) NOT NULL, -- e.g., 'TILT', 'CIRCUIT_BREAKER'
    start_time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    duration_minutes INTEGER NOT NULL,
    unlock_time TIMESTAMPTZ NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    reason TEXT,
    metadata JSONB
);

CREATE INDEX IF NOT EXISTS idx_locks_user ON trading_locks(user_id, active);
CREATE INDEX IF NOT EXISTS idx_locks_unlock ON trading_locks(unlock_time);
