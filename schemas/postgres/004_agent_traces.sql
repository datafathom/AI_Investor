-- Persistent Trace Storage for Agent Observability
CREATE TABLE IF NOT EXISTS agent_traces (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id TEXT NOT NULL,
    parent_job_id TEXT,
    step_id TEXT,
    label TEXT NOT NULL,
    content TEXT NOT NULL,
    type TEXT DEFAULT 'info', -- 'thought', 'tool_call', 'redaction', 'error', 'info'
    metadata JSONB DEFAULT '{}',
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for retrieving traces for a specific agent during a mission
CREATE INDEX IF NOT EXISTS idx_agent_traces_lookup ON agent_traces (agent_id, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_agent_traces_job ON agent_traces (parent_job_id);

COMMENT ON TABLE agent_traces IS 'Captured telemetry, thoughts, and tool signatures for every agent action.';
