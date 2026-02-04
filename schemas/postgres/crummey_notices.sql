
-- Migration for Phase 156: Crummey Power Notices
CREATE TABLE IF NOT EXISTS crummey_notices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ilit_id UUID NOT NULL,
    gift_id UUID NOT NULL,
    
    -- Notification Details
    beneficiary_id UUID NOT NULL,
    notice_sent_date DATE NOT NULL,
    withdrawal_window_days INTEGER DEFAULT 30,
    -- PostgreSQL GENERATED ALWAYS logic
    withdrawal_deadline DATE GENERATED ALWAYS AS (notice_sent_date + (withdrawal_window_days * INTERVAL '1 day')) STORED,
    
    -- Status
    status VARCHAR(20),                -- SENT, RECEIVED, WAIVED, EXPIRED
    proof_of_receipt_url VARCHAR(255), -- PDF Scan
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_ilit_id ON crummey_notices(ilit_id);
CREATE INDEX IF NOT EXISTS idx_beneficiary_id ON crummey_notices(beneficiary_id);
