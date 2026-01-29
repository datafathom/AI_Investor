-- Phase 13: Agent Swarm Consensus & Debate Logs
-- PURPOSE: Store detailed records of agent decision processes and dissent.

CREATE TABLE IF NOT EXISTS debate_logs (
    id BIGSERIAL PRIMARY KEY,
    proposal_id UUID NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    decision VARCHAR(20) NOT NULL,  -- APPROVED, REJECTED
    votes_json JSONB NOT NULL,      -- Full record of all agent votes and weights
    metadata JSONB,                 -- Contextual data (market conditions at time of vote)
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexing for forensics search
CREATE INDEX IF NOT EXISTS idx_debate_proposal ON debate_logs(proposal_id);
CREATE INDEX IF NOT EXISTS idx_debate_symbol ON debate_logs(symbol);
CREATE INDEX IF NOT EXISTS idx_debate_status ON debate_logs(decision);

-- Optional: GIN index for deep vote searching
CREATE INDEX IF NOT EXISTS idx_debate_votes_gin ON debate_logs USING GIN (votes_json);
