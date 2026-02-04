-- Rollback migration for phase1_001_user_workspaces.sql
-- Generated automatically - review before using

DROP TRIGGER IF EXISTS workspace_updated ON user_workspaces;
DROP FUNCTION IF EXISTS update_workspace_timestamp() CASCADE;
DROP INDEX IF EXISTS idx_user_workspaces_default;
DROP INDEX IF EXISTS idx_user_workspaces_user_id;
DROP TABLE IF EXISTS user_workspaces;
