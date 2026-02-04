-- Phase 102: Index Fund Master Table
-- Tracks major ETFs and Index Funds

CREATE TABLE IF NOT EXISTS index_fund_master (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticker VARCHAR(10) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    fund_type VARCHAR(50) NOT NULL,  -- ETF, MUTUAL_FUND, INDEX
    benchmark_index VARCHAR(100),    -- S&P 500, NASDAQ 100, Russell 2000
    
    -- Fund Details
    expense_ratio DECIMAL(6, 4) NOT NULL,
    aum DECIMAL(20, 2),              -- Assets Under Management
    inception_date DATE,
    issuer VARCHAR(100),             -- Vanguard, BlackRock, State Street
    
    -- Trading Info
    avg_volume BIGINT,
    avg_spread DECIMAL(8, 6),
    tradability VARCHAR(20) DEFAULT 'HIGHLY_LIQUID',
    
    -- Classification
    asset_class VARCHAR(50),         -- EQUITY, FIXED_INCOME, COMMODITY
    sector_focus VARCHAR(50),        -- BROAD_MARKET, TECH, HEALTHCARE
    market_cap_focus VARCHAR(20),    -- LARGE_CAP, MID_CAP, SMALL_CAP
    geography VARCHAR(50),           -- US, INTERNATIONAL, EMERGING
    
    -- Metadata
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_index_fund_ticker ON index_fund_master(ticker);
CREATE INDEX IF NOT EXISTS idx_index_fund_type ON index_fund_master(fund_type);
CREATE INDEX IF NOT EXISTS idx_index_fund_benchmark ON index_fund_master(benchmark_index);
