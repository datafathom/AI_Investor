-- Production Database Initialization Script
-- This script runs when the database container is first created

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- TimescaleDB extension (if using TimescaleDB)
-- CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Set timezone
SET timezone = 'UTC';

-- Create schema_migrations table (if not exists)
CREATE TABLE IF NOT EXISTS schema_migrations (
    version VARCHAR(255) PRIMARY KEY,
    applied_at TIMESTAMPTZ DEFAULT NOW(),
    description TEXT
);

-- Initial migration record
INSERT INTO schema_migrations (version, description)
VALUES ('000_initial', 'Initial database setup')
ON CONFLICT (version) DO NOTHING;
