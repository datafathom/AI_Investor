-- Rollback Migration: User Onboarding and Preferences
-- Description: Rollback for phase6_005_user_onboarding
-- Created: 2026-01-21
-- ID: phase6_005_user_onboarding

BEGIN;

DROP INDEX IF EXISTS idx_user_preferences_user_id;
DROP INDEX IF EXISTS idx_user_onboarding_completed;
DROP INDEX IF EXISTS idx_user_onboarding_user_id;

DROP TABLE IF EXISTS user_preferences;
DROP TABLE IF EXISTS user_onboarding;

COMMIT;
