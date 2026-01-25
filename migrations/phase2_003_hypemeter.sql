-- Phase 2 Migration: HypeMeter (Social Sentiment)
-- Created: 2026-01-18

CREATE TABLE IF NOT EXISTS social_sentiment (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    source VARCHAR(50) NOT NULL, -- e.g., 'Reddit', 'Twitter', 'News'
    symbol VARCHAR(20) NOT NULL,
    sentiment_score FLOAT NOT NULL CHECK (sentiment_score >= -1.0 AND sentiment_score <= 1.0),
    magnitude FLOAT DEFAULT 0.0,
    raw_text TEXT,
    entities JSONB DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_sentiment_symbol_time ON social_sentiment(symbol, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_sentiment_source ON social_sentiment(source);
