-- Enable the pgvector extension to work with embeddings
CREATE EXTENSION IF NOT EXISTS vector;

-- Agent Memories table (Semantic Experience Storage)
CREATE TABLE IF NOT EXISTS agent_memories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dept_id INTEGER NOT NULL,
    mission_id TEXT,
    content TEXT NOT NULL,
    embedding vector(768), -- Optimized for models like nomic-embed-text or sentence-transformers
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- HNSW index for high-performance semantic search
-- m=16, ef_construction=64 are good defaults for sub-million row datasets
CREATE INDEX IF NOT EXISTS idx_agent_memories_embedding ON agent_memories 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Index for mission-specific recall
CREATE INDEX IF NOT EXISTS idx_agent_memories_mission_id ON agent_memories(mission_id);

-- Index for departmental analysis
CREATE INDEX IF NOT EXISTS idx_agent_memories_dept_id ON agent_memories(dept_id);

-- Row-Level Security (RLS) for Write-Once-Read-Many (WORM) patterns
ALTER TABLE agent_memories ENABLE ROW LEVEL SECURITY;

-- Allow anyone to read
CREATE POLICY select_agent_memories ON agent_memories
    FOR SELECT USING (true);

-- Allow anyone to insert
CREATE POLICY insert_agent_memories ON agent_memories
    FOR INSERT WITH CHECK (true);

-- Prevent any updates or deletes (WORM)
CREATE POLICY update_agent_memories ON agent_memories
    FOR UPDATE USING (false);

CREATE POLICY delete_agent_memories ON agent_memories
    FOR DELETE USING (false);

COMMENT ON TABLE agent_memories IS 'Stores vectorized agent experiences for semantic retrieval and long-term memory. WORM-protected through RLS.';

