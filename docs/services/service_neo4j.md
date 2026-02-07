# Backend Service: Neo4j (Knowledge Graph)

## Overview
The **Neo4j Service** transforms the platform from a simple database into a **Knowledge Graph**. While Postgres stores *what* happened (transactions, balances), Neo4j stores *why* it matters (relationships, ownership, influence, risk contagion). It serves as the "Master Brain," merging disjointed data domains (Legal, Tax, Finance, Personal) into a single, queryable semantic network.

## Core Components

### 1. Master Graph Orchestrator (`master_graph.py`)
The unified query engine.
- **Global Unification**: Periodically runs Cypher queries to link isolated nodes (e.g., connecting a `Trust` in the Legal domain to a `Portfolio` in the Finance domain via a `BENEFICIARY_OF` relationship).
- **Reflexivity Engine**: Simulates "financial contagion." If an asset collapses, the `trigger_reflexivity_shock()` method traverses the graph to identify every downstream entity (Trust, LLC, Family Member) that gets hit, calculating a "Contagion Velocity."

### 2. Graph-Ledger Sync (`graph_ledger_sync.py`)
Ensures "Dual-State Consistency."
- **Real-Time Mirroring**: Listens for Postgres ledger commits and immediately updates the corresponding Graph nodes.
- **SLA**: Targets a <100ms sync latency to ensure that if a user buys a stock (Postgres), the Risk Graph (Neo4j) reflects the new exposure instantly.
- **Integrity Check**: The `verify_graph_ledger_integrity()` method audits both databases to ensure zero variance in account balances or entity counts.

### 3. Neo4j Driver (`neo4j_service.py`)
High-performance connection pooling.
- **Singleton Pattern**: Manages the Bolt driver connection lifecycle, ensuring efficient reuse across thousands of async requests.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Estate Planner** | Entity Graph Visualizer | `master_graph.get_graph_data()` | **Implemented** (`EntityGraph.jsx`) |
| **Orchestrator** | Network Map | `master_graph.get_search_entities()` | **Implemented** (`NetworkMap.jsx`) |
| **System Health** | Neo4j Vitals | `neo4j_service.driver.verify_connectivity()`| **Implemented** (`Neo4jHealthVitals.jsx`) |
| **Risk Dashboard** | Contagion Sim | `master_graph.trigger_reflexivity_shock()` | **Partial** (`OrchestratorGraph.jsx`) |

## Dependencies
- `neo4j`: The official Python driver for Neo4j.
- `decimal`: Required for high-precision financial calculations during sync.
- `networkx`: (Implicit/Future) usage for complex graph algorithms like centrality or max-flow.

## Usage Examples

### Triggering a "Black Swan" Simulation
```python
from services.neo4j.master_graph import MasterGraph

brain = MasterGraph()

# Simulate a 50% collapse in a Commercial Real Estate holding
shock_result = brain.trigger_reflexivity_shock(
    asset_id="asset_cre_tower_1",
    magnitude=0.50 
)

print(f"Contagion Velocity: {shock_result['contagion_velocity']}")
for victim in shock_result['affected_nodes']:
    print(f"Impacted: {victim['group']} | Loss Est: ${victim['impact']:,.2f}")
```

### Querying Global Risk Exposure
```python
from services.neo4j.master_graph import MasterGraph

# "How much are we exposed to 'Geopolitical Instability' across ALL trusts?"
results = brain.query_global_exposure(risk_factor="Geopolitical_Zone_B")

total_exposure = sum(r['exposure'] for r in results)
print(f"Total Geopolitical Risk: ${total_exposure:,.2f}")
```
