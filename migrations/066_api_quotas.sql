-- Phase 66: API Quota Persistence
-- PURPOSE: Track API usage across restarts to strictly enforce daily and monthly limits.

CREATE TABLE IF NOT EXISTS api_quotas (
    provider VARCHAR(50) PRIMARY KEY,
    day_used INTEGER DEFAULT 0,
    last_reset_day DATE DEFAULT CURRENT_DATE,
    total_calls_lifetime BIGINT DEFAULT 0,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Seed with current providers
INSERT INTO api_quotas (provider)
SELECT unnest(ARRAY[
    'ALPHA_VANTAGE', 'FRED', 'GIVINGBLOCK', 'OPENAI', 'ANTHROPIC', 
    'GEMINI', 'PERPLEXITY', 'REDDIT', 'GOOGLE_TRENDS', 'SEC_EDGAR', 
    'SOLANA', 'FACEBOOK', 'STOCKTWITS', 'DISCORD', 'YOUTUBE', 
    'QUANDL', 'NEWSAPI', 'TWILIO', 'SENDGRID', 'PLAID', 
    'FINNHUB', 'GMAIL', 'GOOGLE_CALENDAR'
])
ON CONFLICT (provider) DO NOTHING;
