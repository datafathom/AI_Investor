-- Phase 66: Institutional Data Schema
-- Stores historical 13F holdings

CREATE TABLE IF NOT EXISTS fund_holdings (
    fund_id UUID,
    quarter_end DATE,
    ticker VARCHAR(10),
    shares BIGINT,
    value_usd DECIMAL(20, 2),
    change_from_prev_qtr BIGINT,
    
    PRIMARY KEY (fund_id, quarter_end, ticker)
);

CREATE INDEX IF NOT EXISTS idx_holdings_ticker ON fund_holdings (ticker);
