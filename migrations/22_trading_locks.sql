-- Phase 22: Trading Locks Architecture
-- Stores behavioral and circuit breaker locks

CREATE TABLE IF NOT EXISTS trading_locks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    lock_type VARCHAR(50) NOT NULL, -- 'CIRCUIT_BREAKER', 'TILT', 'MANUAL_ADMIN', 'BEHAVIORAL'
    reason TEXT,
    
    start_time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    duration_minutes INTEGER NOT NULL,
    
    -- Calculated unlock time for easier querying
    unlock_time TIMESTAMPTZ GENERATED ALWAYS AS (start_time + (duration_minutes * INTERVAL '1 minute')) STORED,
    
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for finding active locks quickly
CREATE INDEX IF NOT EXISTS idx_active_trading_locks ON trading_locks (user_id) WHERE is_active = TRUE;
