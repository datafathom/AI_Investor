
-- Migration for Phase 155: Mediation Evidence Log
CREATE TABLE IF NOT EXISTS mediation_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    estate_plan_id UUID NOT NULL,
    session_date TIMESTAMPTZ NOT NULL,
    
    -- Attendees
    attendees JSONB,                   -- ["Grantor", "Heir A", "Attorney"]
    
    -- Evidence
    recording_url VARCHAR(255),        -- S3 link to video/audio
    transcript_text TEXT,
    
    -- Outcome
    topics_discussed TEXT,
    consensus_reached BOOLEAN,
    signed_waiver_received BOOLEAN,    -- Estoppel Key
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_estate_plan_id ON mediation_sessions(estate_plan_id);
