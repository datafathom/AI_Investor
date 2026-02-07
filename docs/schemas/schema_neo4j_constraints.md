# Schema: Neo4j Constraints

## File Location
`schemas/neo4j/neo4j_constraints.cypher`

## Purpose
Cypher schema definitions for database constraints and indexes. Executed during database initialization to ensure data integrity and query performance.

---

## Uniqueness Constraints

### Agent Node
```cypher
CREATE CONSTRAINT agent_id_unique IF NOT EXISTS 
FOR (a:Agent) REQUIRE a.id IS UNIQUE;
```
- **Purpose**: Ensures no duplicate agent IDs
- **Property**: `id`
- **Enforcement**: Database-level, prevents duplicate insertions

---

### Asset Node
```cypher
CREATE CONSTRAINT asset_symbol_unique IF NOT EXISTS 
FOR (s:Asset) REQUIRE s.symbol IS UNIQUE;
```
- **Purpose**: Ensures no duplicate asset symbols
- **Property**: `symbol`
- **Enforcement**: Database-level, ticker symbols must be unique

---

## Performance Indexes

### Agent Status Index
```cypher
CREATE INDEX agent_status_idx IF NOT EXISTS 
FOR (a:Agent) ON (a.status);
```
- **Purpose**: Accelerates queries filtering by agent status
- **Use Case**: Finding all active/idle/error agents

---

### Asset Sector Index
```cypher
CREATE INDEX asset_sector_idx IF NOT EXISTS 
FOR (s:Asset) ON (s.sector);
```
- **Purpose**: Accelerates queries filtering by sector
- **Use Case**: Sector-based analytics, sector rotation strategies

---

## Initialization Script

These constraints and indexes should be run once during database setup:

```cypher
// Run as initialization script
:source neo4j_constraints.cypher

// Or execute via Python
from neo4j import GraphDatabase

driver = GraphDatabase.driver(uri, auth=(user, password))
with driver.session() as session:
    with open('schemas/neo4j/neo4j_constraints.cypher', 'r') as f:
        for statement in f.read().split(';'):
            if statement.strip():
                session.run(statement)
```

---

## Constraint Verification

```cypher
// List all constraints
SHOW CONSTRAINTS

// List all indexes
SHOW INDEXES

// Verify specific constraint
SHOW CONSTRAINTS WHERE name = 'agent_id_unique'
```

---

## Integration Points

| Service | Usage |
|---------|-------|
| `Neo4jConnectionManager` | Database initialization |
| `MigrationService` | Schema versioning |
| `HealthCheckService` | Constraint verification |

## Best Practices

1. **Always use IF NOT EXISTS** - Prevents errors on re-runs
2. **Create constraints before bulk loading** - Improves import performance
3. **Monitor index usage** - Drop unused indexes to reduce write overhead
4. **Use composite indexes** for multi-property queries
