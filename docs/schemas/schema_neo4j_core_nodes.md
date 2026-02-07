# Schema: Neo4j Core Nodes

## File Location
`schemas/neo4j/core_nodes.cypher`

## Purpose
Cypher schema definitions for core Neo4j node labels, uniqueness constraints, and performance indexes. Establishes the fundamental graph structure for entities, assets, agents, and jurisdictions.

---

## Node Labels

### ASSET
**Represents tradeable financial assets (stocks, ETFs, crypto, commodities).**

| Constraint/Index | Type | Property | Description |
|-----------------|------|----------|-------------|
| `asset_id` | Uniqueness Constraint | `id` | Ensures unique asset identifiers |
| `asset_symbol` | Index | `symbol` | Performance index for symbol lookups |

**Common Properties:**
- `id` (string): Unique asset identifier (UUID)
- `symbol` (string): Ticker symbol (e.g., AAPL, BTC)
- `name` (string): Full asset name
- `asset_type` (string): Type (EQUITY, ETF, CRYPTO, COMMODITY)
- `sector` (string): Sector classification

---

### AGENT
**Represents AI agents in the autonomous workforce.**

| Constraint/Index | Type | Property | Description |
|-----------------|------|----------|-------------|
| `agent_id` | Uniqueness Constraint | `id` | Ensures unique agent identifiers |
| `agent_persona` | Index | `persona` | Performance index for persona-based queries |

**Common Properties:**
- `id` (string): Unique agent identifier (e.g., `trader.4.1`)
- `persona` (string): Agent persona type
- `department` (string): Assigned department
- `status` (string): Operational status

---

### ENTITY
**Represents users, organizations, or other actors in the system.**

| Constraint/Index | Type | Property | Description |
|-----------------|------|----------|-------------|
| `entity_id` | Uniqueness Constraint | `id` | Ensures unique entity identifiers |

**Common Properties:**
- `id` (string): Unique entity identifier (UUID)
- `entity_type` (string): Type (USER, ORGANIZATION, TRUST)
- `name` (string): Entity name

---

### JURISDICTION
**Represents legal/regulatory jurisdictions.**

| Constraint/Index | Type | Property | Description |
|-----------------|------|----------|-------------|
| `jurisdiction_id` | Uniqueness Constraint | `code` | Ensures unique jurisdiction codes |

**Common Properties:**
- `code` (string): Jurisdiction code (e.g., US, EU, UK)
- `name` (string): Full jurisdiction name
- `regulatory_body` (string): Primary regulator

---

## Usage Examples

```cypher
// Find all assets in a sector
MATCH (a:ASSET {sector: 'Technology'})
RETURN a.symbol, a.name

// Find all active agents in a department
MATCH (ag:AGENT {department: 'Trading', status: 'ACTIVE'})
RETURN ag.id, ag.persona

// Find entities in a jurisdiction
MATCH (e:ENTITY)-[:SUBJECT_TO]->(j:JURISDICTION {code: 'US'})
RETURN e.name, e.entity_type
```

---

## Integration Points

| Service | Usage |
|---------|-------|
| `Neo4jConnectionManager` | Database connectivity |
| `AssetGraphService` | Asset relationship queries |
| `AgentGraphService` | Agent relationship management |
| `ComplianceService` | Jurisdiction-based compliance checks |
