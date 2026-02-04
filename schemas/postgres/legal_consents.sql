-- Phase 30: Legal Automation
-- Table for tracking user consents to legal agreements

CREATE TABLE IF NOT EXISTS user_consents (
    user_id TEXT NOT NULL,
    agreement_type TEXT NOT NULL, -- e.g., 'TOS', 'RISK_DISCLAIMER'
    version TEXT NOT NULL,
    accepted_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (user_id, agreement_type)
);

-- Index for fast lookup
CREATE INDEX IF NOT EXISTS idx_user_consents_uid ON user_consents(user_id);
