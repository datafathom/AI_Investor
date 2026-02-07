# Documentation: `tests/unit/test_kafka_foundation.py` & `test_neo4j_rebuild.py`

## Overview
These tests validate the data persistence and streaming foundation. They ensure that market data is correctly structured (Kafka) and that the system's "Mental Model" (Neo4j Graph) is accurately reconstructed.

## Components Under Test
- `services.schema_registry.SchemaRegistryService`: Management of AVRO/JSON schemas.
- `services.validators.kafka_validators.KafkaValidatorService`: Payload enforcement.
- `services.neo4j.node_factory.NodeFactory`: Graph node generation.

## Key Test Scenarios

### 1. Schema Enforcement (Kafka)
- **Goal**: Ensure all messages on the bus follow strict formats.
- **Assertions**:
    - Critical `market_telemetry` schema is correctly loaded from the registry.
    - Payload validation fails if required fields (e.g., `symbol`, `price`) are missing.

### 2. Graph Reconstruction (Neo4j)
- **Goal**: Verify the structure of the systemic knowledge graph.
- **Assertions**:
    - `NodeFactory` generates valid ASSET and AGENT nodes with correct metadata (e.g., Symbol, Persona).
    - `RelationshipBuilder` correctly links entities with `OWNS` or `FOLLOWS` edges, including edge properties like `quantity`.

## Holistic Context
This "Foundation Layer" ensures that the AI's memory (Neo4j) and its nervous system (Kafka) speak a common language. Without this consistency, the agents would suffer from data hallucinations or misinterpret relationship-based risks.
