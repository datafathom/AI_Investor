-- Phase 110: Digital Platform Ledger
-- Immutable ledger with SHA-256 hashing for audit integrity

CREATE TABLE IF NOT EXISTS platform_ledger (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entry_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Transaction Details
    transaction_type VARCHAR(50) NOT NULL,
    account_id UUID NOT NULL,
    custodian_id UUID NOT NULL,
    
    -- Amounts
    amount DECIMAL(20, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    
    -- Counterparty
    from_account VARCHAR(100),
    to_account VARCHAR(100),
    counterparty_name VARCHAR(255),
    
    -- Verification
    custodian_confirmation_id VARCHAR(100),
    custodian_confirmed_at TIMESTAMPTZ,
    is_reconciled BOOLEAN DEFAULT FALSE,
    reconciled_at TIMESTAMPTZ,
    
    -- Audit Trail
    created_by UUID,
    ip_address INET,
    user_agent TEXT,
    
    -- Immutability Hash
    previous_hash VARCHAR(64),
    entry_hash VARCHAR(64) NOT NULL,
    hash_verified BOOLEAN DEFAULT FALSE
);

-- Check if TimescaleDB extension is available
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'timescaledb') THEN
        PERFORM create_hypertable('platform_ledger', 'entry_timestamp', if_not_exists => TRUE);
    END IF;
END $$;

CREATE INDEX IF NOT EXISTS idx_ledger_account ON platform_ledger(account_id);
CREATE INDEX IF NOT EXISTS idx_ledger_hash ON platform_ledger(entry_hash);
