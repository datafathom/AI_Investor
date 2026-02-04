-- Phase 196: Market Integrity & Anomalies
-- Purpose: Track market manipulation signatures, social promo volume, and restricted stock status.

CREATE TABLE IF NOT EXISTS market_anomalies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticker VARCHAR(10) NOT NULL,
    detection_date DATE DEFAULT CURRENT_DATE,
    
    -- Metrics
    price_change_pct DECIMAL(10, 4),
    volume_change_pct DECIMAL(10, 4),
    divergence_score DECIMAL(5, 2), -- 0-100
    
    anomaly_type VARCHAR(50), -- PRICE_VOL_DIVERGENCE, UNUSUAL_PREMARKET
    risk_level VARCHAR(20),   -- LOW, MEDIUM, CRITICAL
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS social_bot_activity (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticker VARCHAR(10) NOT NULL,
    observation_time TIMESTAMPTZ DEFAULT NOW(),
    
    total_mentions_1h INTEGER,
    unique_authors_1h INTEGER,
    bot_suspicion_score DECIMAL(5, 2), -- % of volume from new/low-quality accounts
    
    sentiment_polarity DECIMAL(4, 3), -- -1.0 to 1.0
    is_promo_attack BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS restricted_legend_status (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_id UUID NOT NULL,
    
    security_type VARCHAR(50) DEFAULT 'Restricted Stock Unit',
    acquisition_date DATE NOT NULL,
    
    -- Status
    is_reporting_issuer BOOLEAN DEFAULT TRUE,
    holding_period_months INTEGER,
    
    legend_removal_eligible_date DATE,
    opinion_letter_requested BOOLEAN DEFAULT FALSE,
    current_status VARCHAR(20) DEFAULT 'LOCKED', -- LOCKED, ELIGIBLE, CLEARED
    
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexing
CREATE INDEX IF NOT EXISTS idx_anomalies_ticker ON market_anomalies(ticker, detection_date);
CREATE INDEX IF NOT EXISTS idx_bot_activity_ticker ON social_bot_activity(ticker, observation_time);
CREATE INDEX IF NOT EXISTS idx_legend_asset ON restricted_legend_status(asset_id);
