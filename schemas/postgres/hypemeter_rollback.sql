-- Rollback migration for phase2_003_hypemeter.sql
-- Generated automatically - review before using

DROP INDEX IF EXISTS idx_hypemeter_timestamp;
DROP TABLE IF EXISTS hypemeter;
