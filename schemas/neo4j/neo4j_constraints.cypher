// Phase 2: Neo4j Constraints & Indexes
// To run via Neo4j Browser or startup script

// Ensure uniqueness for Agents
CREATE CONSTRAINT agent_id_unique IF NOT EXISTS FOR (a:Agent) REQUIRE a.id IS UNIQUE;

// Ensure uniqueness for Assets/Symbols
CREATE CONSTRAINT asset_symbol_unique IF NOT EXISTS FOR (s:Asset) REQUIRE s.symbol IS UNIQUE;

// Indexes for performance
CREATE INDEX agent_status_idx IF NOT EXISTS FOR (a:Agent) ON (a.status);
CREATE INDEX asset_sector_idx IF NOT EXISTS FOR (s:Asset) ON (s.sector);

// Relationship constraints aren't direct, but we ensure node integrity first.
