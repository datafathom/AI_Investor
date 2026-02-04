-- Phase 29: Immutable Audit Trail
-- Creating activity_logs table if it doesn't exist, with hash chaining columns.

CREATE TABLE IF NOT EXISTS activity_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT NOT NULL,
    activity_type TEXT NOT NULL,
    details JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    previous_hash TEXT,
    verification_hash TEXT
);

-- Index for fast lookup by user (GDPR export) and time
CREATE INDEX IF NOT EXISTS idx_activity_logs_user ON activity_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_activity_logs_created_at ON activity_logs(created_at);

-- Optional: Hypertable conversion if using TimescaleDB (if compatible with updates, but logs are usually insert-only)
-- SELECT create_hypertable('activity_logs', 'created_at', if_not_exists => TRUE);
