-- Phase 173/175: Deal Priorities & Operations
-- Purpose: Track scarce deal allocations and shared MFO services.

CREATE TABLE IF NOT EXISTS deal_waitlist (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    deal_id UUID NOT NULL,
    user_id UUID NOT NULL,
    requested_amount DECIMAL(20, 2),
    allocated_amount DECIMAL(20, 2) DEFAULT 0,
    priority_bucket VARCHAR(20),
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS concierge_tickets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    family_id UUID NOT NULL,
    request_type VARCHAR(50),
    request_summary TEXT,
    staff_assigned UUID,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexing
CREATE INDEX IF NOT EXISTS idx_waitlist_deal ON deal_waitlist(deal_id, created_at);
CREATE INDEX IF NOT EXISTS idx_concierge_family ON concierge_tickets(family_id);
