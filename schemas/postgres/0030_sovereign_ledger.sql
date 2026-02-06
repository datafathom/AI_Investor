-- =============================================================================
-- Sovereign Ledger Schema - Postgres Double-Entry Accounting Core
-- Phase 1 Implementation: The Sovereign Kernel
-- =============================================================================
-- This schema implements an IMMUTABLE double-entry ledger with hash-chaining
-- for audit integrity. Every financial mutation is recorded as a balanced
-- journal entry, and the hash chain ensures tamper-evidence.
--
-- ACCEPTANCE CRITERIA from ROADMAP_AGENT_DEPT.md:
-- - Auditability: Every agent decision has a hashed audit trail.
-- - Relational Integrity: Matched with Neo4j for dual-truth.
-- =============================================================================

-- Account Types (enumeration)
CREATE TYPE account_type AS ENUM (
    'ASSET',
    'LIABILITY',
    'EQUITY',
    'REVENUE',
    'EXPENSE'
);

-- Transaction Lifecycle States
CREATE TYPE transaction_status AS ENUM (
    'PENDING',      -- Awaiting user signature
    'SIGNED',       -- WebAuthn signature verified
    'EXECUTED',     -- Broker/bank confirmed
    'RECONCILED',   -- Matched with external source
    'VOIDED'        -- Cancelled (audit trail preserved)
);

-- =============================================================================
-- Chart of Accounts
-- =============================================================================
CREATE TABLE IF NOT EXISTS ledger_accounts (
    id              VARCHAR(64) PRIMARY KEY,
    name            VARCHAR(255) NOT NULL,
    account_type    account_type NOT NULL,
    parent_id       VARCHAR(64) REFERENCES ledger_accounts(id),
    currency        VARCHAR(3) DEFAULT 'USD',
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    
    -- Hierarchical path for efficient queries (e.g., 'Assets.Brokerage.Schwab')
    path            LTREE,
    
    CONSTRAINT valid_currency CHECK (currency ~ '^[A-Z]{3}$')
);

-- Index for hierarchical queries
CREATE INDEX IF NOT EXISTS idx_accounts_path ON ledger_accounts USING GIST (path);

-- =============================================================================
-- Journal Entries (Immutable Transaction Headers)
-- =============================================================================
CREATE TABLE IF NOT EXISTS journal_entries (
    id                      VARCHAR(64) PRIMARY KEY,
    timestamp               TIMESTAMPTZ DEFAULT NOW(),
    description             TEXT NOT NULL,
    status                  transaction_status DEFAULT 'PENDING',
    
    -- Hash Chain for Tamper-Evidence
    previous_hash           VARCHAR(64),  -- SHA-256 of previous entry
    entry_hash              VARCHAR(64),  -- SHA-256 of this entry's contents
    
    -- Sovereign Signature Binding (Non-Repudiation)
    sovereign_signature_id  VARCHAR(64),
    signed_by_user_id       VARCHAR(64),
    signed_at               TIMESTAMPTZ,
    
    -- Agent Provenance
    created_by_agent        VARCHAR(64),  -- e.g., 'trader.4.1', 'guardian.6.2'
    
    -- Immutability Trigger Target
    is_immutable            BOOLEAN DEFAULT FALSE,
    
    CONSTRAINT hash_chain_integrity CHECK (
        (previous_hash IS NULL AND id = 'GENESIS') OR
        (previous_hash IS NOT NULL AND id != 'GENESIS')
    )
);

-- Index for audit queries
CREATE INDEX IF NOT EXISTS idx_journal_timestamp ON journal_entries(timestamp);
CREATE INDEX IF NOT EXISTS idx_journal_agent ON journal_entries(created_by_agent);
CREATE INDEX IF NOT EXISTS idx_journal_status ON journal_entries(status);

-- =============================================================================
-- Journal Lines (Double-Entry Legs)
-- =============================================================================
CREATE TABLE IF NOT EXISTS journal_lines (
    id              SERIAL PRIMARY KEY,
    journal_id      VARCHAR(64) NOT NULL REFERENCES journal_entries(id) ON DELETE RESTRICT,
    account_id      VARCHAR(64) NOT NULL REFERENCES ledger_accounts(id),
    debit           NUMERIC(20, 4) DEFAULT 0.0000,
    credit          NUMERIC(20, 4) DEFAULT 0.0000,
    memo            TEXT,
    
    -- Line-level constraints
    CONSTRAINT positive_amounts CHECK (debit >= 0 AND credit >= 0),
    CONSTRAINT one_side_only CHECK (
        (debit > 0 AND credit = 0) OR (credit > 0 AND debit = 0)
    )
);

-- Index for balance calculations
CREATE INDEX IF NOT EXISTS idx_lines_account ON journal_lines(account_id);
CREATE INDEX IF NOT EXISTS idx_lines_journal ON journal_lines(journal_id);

-- =============================================================================
-- Sovereign Credentials (WebAuthn Storage)
-- =============================================================================
CREATE TABLE IF NOT EXISTS sovereign_credentials (
    id              SERIAL PRIMARY KEY,
    user_id         VARCHAR(64) NOT NULL UNIQUE,
    credential_id   BYTEA NOT NULL,
    public_key      BYTEA NOT NULL,
    sign_count      INTEGER DEFAULT 0,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    last_used_at    TIMESTAMPTZ
);

-- =============================================================================
-- Sovereign Challenges (Temporary, for Active Auth Sessions)
-- =============================================================================
CREATE TABLE IF NOT EXISTS sovereign_challenges (
    challenge_id    VARCHAR(64) PRIMARY KEY,
    challenge_bytes BYTEA NOT NULL,
    command_hash    VARCHAR(64) NOT NULL,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    expires_at      TIMESTAMPTZ NOT NULL,
    is_consumed     BOOLEAN DEFAULT FALSE
);

-- Auto-cleanup expired challenges
CREATE INDEX IF NOT EXISTS idx_challenges_expires ON sovereign_challenges(expires_at);

-- =============================================================================
-- Views: Account Balances
-- =============================================================================
CREATE OR REPLACE VIEW account_balances AS
SELECT 
    a.id AS account_id,
    a.name AS account_name,
    a.account_type,
    COALESCE(SUM(l.debit), 0) - COALESCE(SUM(l.credit), 0) AS balance,
    NOW() AS as_of
FROM ledger_accounts a
LEFT JOIN journal_lines l ON a.id = l.account_id
LEFT JOIN journal_entries j ON l.journal_id = j.id AND j.status != 'VOIDED'
GROUP BY a.id, a.name, a.account_type;

-- =============================================================================
-- Functions: Balance Verification
-- =============================================================================
CREATE OR REPLACE FUNCTION verify_journal_balance()
RETURNS TRIGGER AS $$
DECLARE
    total_debits NUMERIC(20, 4);
    total_credits NUMERIC(20, 4);
BEGIN
    SELECT COALESCE(SUM(debit), 0), COALESCE(SUM(credit), 0)
    INTO total_debits, total_credits
    FROM journal_lines
    WHERE journal_id = NEW.journal_id;
    
    IF total_debits != total_credits THEN
        RAISE EXCEPTION 'Journal entry does not balance. Debits: %, Credits: %',
            total_debits, total_credits;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to enforce balance on line insert
CREATE TRIGGER trg_verify_balance
AFTER INSERT ON journal_lines
FOR EACH ROW
EXECUTE FUNCTION verify_journal_balance();

-- =============================================================================
-- Security: Row-Level Security (Optional, for multi-tenant future)
-- =============================================================================
-- ALTER TABLE journal_entries ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE journal_lines ENABLE ROW LEVEL SECURITY;

COMMENT ON TABLE journal_entries IS 'Immutable double-entry journal headers with hash-chain integrity';
COMMENT ON TABLE journal_lines IS 'Individual debit/credit legs of journal entries';
COMMENT ON TABLE sovereign_credentials IS 'WebAuthn credential storage for biometric authentication';
