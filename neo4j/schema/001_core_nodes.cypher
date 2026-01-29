// Core Node Labels and Constraints

// ASSET: Uniqueness on ID
CREATE CONSTRAINT asset_id IF NOT EXISTS FOR (a:ASSET) REQUIRE a.id IS UNIQUE;

// AGENT: Uniqueness on ID
CREATE CONSTRAINT agent_id IF NOT EXISTS FOR (a:AGENT) REQUIRE a.id IS UNIQUE;

// ENTITY: Uniqueness on ID
CREATE CONSTRAINT entity_id IF NOT EXISTS FOR (e:ENTITY) REQUIRE e.id IS UNIQUE;

// JURISDICTION: Uniqueness on Code
CREATE CONSTRAINT jurisdiction_id IF NOT EXISTS FOR (j:JURISDICTION) REQUIRE j.code IS UNIQUE;

// Indexes for performance
CREATE INDEX asset_symbol IF NOT EXISTS FOR (a:ASSET) ON (a.symbol);
CREATE INDEX agent_persona IF NOT EXISTS FOR (a:AGENT) ON (a.persona);
