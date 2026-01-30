-- Phase 0: Linked Accounts Table
-- Extracted from SocialAuthService for reliability

CREATE TABLE IF NOT EXISTS linked_accounts (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    provider VARCHAR(50) NOT NULL,
    vendor_id TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    UNIQUE(provider, vendor_id)
);

-- Index for lookup
CREATE INDEX IF NOT EXISTS idx_linked_provider_vendor ON linked_accounts(provider, vendor_id);
CREATE INDEX IF NOT EXISTS idx_linked_user_id ON linked_accounts(user_id);
