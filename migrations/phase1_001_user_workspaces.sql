-- Phase 1 Migration: User Workspaces
-- Created: 2026-01-18
-- Description: Adds persistence for OS-style window layouts

CREATE TABLE IF NOT EXISTS user_workspaces (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL, -- FK constraint would normally require users table, assuming it exists or logic handles it
    workspace_name VARCHAR(255) NOT NULL,
    layout_json JSONB NOT NULL,
    is_default BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, workspace_name)
);

CREATE INDEX IF NOT EXISTS idx_user_workspaces_user_id ON user_workspaces(user_id);
CREATE INDEX IF NOT EXISTS idx_user_workspaces_default ON user_workspaces(user_id, is_default) WHERE is_default = true;

-- Trigger for updated_at
CREATE OR REPLACE FUNCTION update_workspace_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS workspace_updated ON user_workspaces;
CREATE TRIGGER workspace_updated
    BEFORE UPDATE ON user_workspaces
    FOR EACH ROW EXECUTE FUNCTION update_workspace_timestamp();
