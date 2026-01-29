# Implementation Plan: Sprint 3 - The Brain (Spatial & Graph)

## Goal
Integrate the Neo4j "Super-Graph" into the UI to visualize systemic risk propagation and complex entity relationships.

## 1. Graph & Spatial Logic
### 1.1 Neo4j Bolt Proxy
- **Purpose**: Facilitate high-speed graph queries without exposing Neo4j credentials to the browser.
- **Backend**: `master_orchestrator_api.py` proxying to `neo4j_service.py`.
- **Frontend**: D3.js integration in `MasterOrchestrator.jsx`.

### 1.2 Reflexivity Propagation Engine
- **Logic**: 
    - Receive "Shock" input (e.g., Asset X -20%).
    - Traverse Neo4j links to identify affected Nodes (Trusts, Property, Entities).
    - Calculate and display "Contagion Velocity".

## 2. Sprint 3 Widgets (Graph & Entity)
| Widget | Purpose | Technical Logic |
|--------|---------|-----------------|
| `NodeConnectionHeatmap` | Density map | Identifies "Single Points of Failure" in the entity graph. |
| `SpatialAssetBubble` | Volumetric view | Uses Three.js to render assets in 3D based on Lat/Long/Value. |
| `ReflexivityEcho` | Shock ripple | Animated "wave" effect propagation across graph nodes. |
| `Neo4jHealthVitals` | Memory/Lock stats | Visualizes `CALL dbms.components()` output. |
| `EntityOwnershipMatrix` | Layered view | Tree-grid display of Parent -> Child equity stakes. |
| `GraphTimeScrubber` | Snapshot view | Queries Neo4j based on `valid_from` / `valid_to` timestamps. |

## 3. Acceptance Criteria
- [ ] **Performance**: Neo4j graph nodes render in < 50ms using the Bolt-over-WebSocket proxy.
- [ ] **Simulation**: Injecting a shock into a "Base Asset" correctly highlights the "Ultimate Beneficiary" node in red.
- [ ] **Spatial**: `SpatialAssetBubble` renders 100+ properties in a 3D cockpit without frame drops.
- [ ] **Accuracy**: `EntityOwnershipMatrix` correctly sums multi-layered stakes through intermediate shells.

## 4. Testing & Code Coverage
- **Unit Tests**:
    - `reflexivity_logic.test.js`: Mock graph topologies and verify propagation math.
    - `spatial_service.py`: Verify coordinate projection from Lat/Long to X/Y/Z.
- **E2E Tests**:
    - `test_graph_interaction.py`: Click a node, verify popover data, and trigger a "What-If" shock.
- **Targets**:
    - 100% logic coverage for contagion calculations.
    - 75% coverage for GL/Three.js render components.
