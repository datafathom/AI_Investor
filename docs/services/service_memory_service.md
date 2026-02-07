# Backend Service: Memory Service (Long-Term Agent Memory)

## Overview
The **Memory Service** is the platform's "Hippocampus"—providing the infrastructure for agents to store and recall long-term experiences. It enables experiential learning by transforming textual agent logs into high-dimensional semantic vectors. These vectors are indexed in a high-performance vector database (Postgres + `pgvector`), allowing agents to perform RAG (Retrieval-Augmented Generation) on their own past successes and failures. Crucially, the service includes a "Scrubber" layer to ensure that all stored memories are redacted of sensitive PII/PHI before being permanented.

## Core Components

### 1. Semantic Embedding Engine (`memory_service.py`)
Transformers agent actions into searchable vectors.
- **Model Orchestration**: Utilizes the `nomic-ai/nomic-embed-text-v1.5` model to generate 768-dimensional embeddings. It uses specific prefixes (`search_document:` vs `search_query:`) to optimize the vector space for retrieval tasks.
- **Lazy Loading**: The model is lazily loaded only when a memory operation is performed, optimizing system memory for lightweight agent instances.

### 2. Experience Archival & Scrubbing (`memory_service.py`)
Ensures safe and permanent retention of agent history.
- **PII/PHI Scrubber**: Before any experience is vectorized, it is passed through the `scrubber` utility to redact names, addresses, and sensitive financial identifiers, ensuring compliance with privacy standards even in long-term storage.
- **pgvector Persistence**: Stores memories in a specialized `agent_memories` table with HNSW indexing for sub-millisecond similarity search.

### 3. Semantic Recall System (`memory_service.py`)
Enables agents to "remember" relevant context.
- **Similarity Search**: Performs a cosine similarity search (`<=>` operator) against the stored vector space to retrieve the top-N memories most relevant to a current query or task.
- **Similarity Thresholding**: Allows for fine-grained control over recall quality by filtering results below a certain similarity score (e.g., 0.70).

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Agent Command** | Memory Frequency Pulse | `memory_service.store_experience()` |
| **Agent Command** | Knowledge Retrieval Terminal| `memory_service.recall_memories()` |
| **System Admin** | Vector Index Status | `memory_service.pgvector_context` |
| **Governance Hub** | Redaction Audit Ledger | `memory_service.scrubber` |
| **Portfolio Detail** | Agent Experience Tooltip | `memory_service.recall_memories()` |

## Dependencies
- `sentence-transformers`: The core engine for generating semantic embeddings.
- `numpy`: Used for internal vector manipulation.
- `pgvector`: (Database Extension) Provides vector-specific indices and operators in Postgres.
- `utils.scrubber`: Redacts sensitive information from experiences.

## Usage Examples

### Storing a New Agent Experience
```python
from services.memory_service import memory_service

# Agent records a successful trade execution strategy
await memory_service.store_experience(
    dept_id=1, # Trading Dept
    mission_id="mission_123",
    content="Successfully avoided slippage by splitting orders across 4 liquidity providers.",
    metadata={"strategy": "VWAP_SPLIT", "success": True}
)
```

### Recalling Relevant Memories for a Current Task
```python
from services.memory_service import memory_service

# Agent is planning a new large order and wants to 'recall' past experiences
query = "How to minimize slippage on large block trades?"
memories = await memory_service.recall_memories(
    query=query,
    limit=3,
    min_similarity=0.75
)

for m in memories:
    print(f"[{m['similarity']:.2f}] Memory: {m['content']}")
    print(f"Metadata: {m['metadata']}")
```
