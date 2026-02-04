-- Rollback migration for phase2_002_fear_greed.sql
-- Generated automatically - review before using

DROP INDEX IF EXISTS idx_fear_greed_composite_timestamp;
DROP TABLE IF EXISTS fear_greed_composite;
