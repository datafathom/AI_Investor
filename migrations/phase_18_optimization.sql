-- Phase 18 Migration: Database Optimization (TimescaleDB & Materialized Views)
-- Created: 2026-01-19

-- 1. Enable TimescaleDB extension if not already present
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- 2. Convert high-frequency tables to Hypertables
-- Fear & Greed Index
SELECT create_hypertable('fear_greed_index', 'timestamp', if_not_exists => TRUE);

-- Social Sentiment (HypeMeter)
SELECT create_hypertable('social_sentiment', 'timestamp', if_not_exists => TRUE);

-- 3. Create Materialized View for Daily Sentiment Summary
-- This improves dashboard load times by pre-aggregating data.
CREATE MATERIALIZED VIEW IF NOT EXISTS daily_sentiment_agg AS
SELECT 
    time_bucket('1 day', timestamp) AS day,
    symbol,
    AVG(sentiment_score) AS avg_sentiment,
    SUM(magnitude) AS total_magnitude,
    COUNT(*) AS signal_count
FROM social_sentiment
GROUP BY day, symbol;

-- Index the materialized view for rapid filtering
CREATE INDEX IF NOT EXISTS idx_daily_sentiment_day_symbol ON daily_sentiment_agg(day DESC, symbol);

-- 4. Refresh Policy (Simulated for demo - in production use TimescaleDB's continuous aggregation)
-- SELECT add_continuous_aggregate_policy('daily_sentiment_agg', 
--     start_offset => INTERVAL '1 month',
--     end_offset => INTERVAL '1 hour',
--     schedule_interval => INTERVAL '1 hour');
