
-- Migration for Phase 150: 1031 Exchange Timers
CREATE TABLE IF NOT EXISTS exchange_timers (
    id UUID DEFAULT gen_random_uuid(),
    exchange_id UUID NOT NULL,
    
    -- Deadlines
    sale_closed_date DATE NOT NULL,
    identification_deadline DATE GENERATED ALWAYS AS (sale_closed_date + INTERVAL '45 days') STORED,
    closing_deadline DATE GENERATED ALWAYS AS (sale_closed_date + INTERVAL '180 days') STORED,
    
    -- Status
    identified_date DATE,
    purchase_closed_date DATE,
    status VARCHAR(20) DEFAULT 'PENDING',            -- PENDING, IDENTIFIED, COMPLETED, FAILED
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (id, created_at)
);

SELECT create_hypertable('exchange_timers', 'created_at', if_not_exists => TRUE);
CREATE INDEX IF NOT EXISTS idx_exchange_id ON exchange_timers(exchange_id);
