# Phase 1: Foundation - Semantic Memory & Worker Abstraction

## Overview
This phase establishes the high-performance, asynchronous infrastructure required for a Sovereign OS. We are moving away from standard synchronous processing to an event-driven, "Experience-aware" architecture. This involves upgrading our database to support high-dimensional vector embeddings and decoupling heavy agent logic into specialized worker processes.

## Deliverables

### 1. Vectorized Database Infrastructure
**Description**: Upgrade PostgreSQL to support the `pgvector` extension and configure specialized indexing for semantic search.
- **Acceptance Criteria**:
  - `docker-compose.yml` uses `pgvector/pgvector:16-alpine` and passes health checks.
  - `CREATE EXTENSION vector;` executes successfully in the `investor_db`.
  - HNSW index is created on `agent_memories.embedding` to support sub-50ms similarity queries.

### 2. Isolated Experience Storage (WORM-Compatible)
**Description**: Implementation of the `agent_memories` table designed for Write-Once-Read-Many (WORM) patterns to ensure audit integrity.
- **Acceptance Criteria**:
  - Table schema includes `id` (UUID), `dept_id` (INT), `content` (TEXT), `embedding` (VECTOR(768)), and `metadata` (JSONB).
  - Row-level security (RLS) is applied to prevent unauthorized modification of historical experiences.
  - Successful insertion and retrieval of 768-dimension vectors verified via SQL queries.

### 3. ARQ Asynchronous Task Queue
**Description**: Deployment of Redis as a message broker and `ARQ` as the native asyncio task queue.
- **Acceptance Criteria**:
  - Redis 8.0 container is operational with password authentication and `internal-network` isolation.
  - Worker process (`worker.py`) establishes a stable connection to Redis and maintains a persistent database pool.
  - Enqueued jobs appear in the Redis `arq:queue` and are processed in the correct priority order.

### 4. Semantic Memory Service (Python)
**Description**: A service layer that translates raw text into semantic vectors using local embedding models.
- **Acceptance Criteria**:
  - `SentenceTransformer` loads the `nomic-embed-text-v1.5` model successfully on the internal network.
  - `store_experience` correctly redacts PII before generating embeddings.
  - `recall_memories` returns a list of relevant content with a similarity score > 0.7.

### 5. Hot-Path Security Scrubber
**Description**: High-speed regex and entropy-based engine to prevent sensitive data from ever reaching the vector index.
- **Acceptance Criteria**:
  - Successfully identifies and redacts 100% of test EVM private keys and 12-word seed phrases.
  - Correctly redacts IPv4 and IPv6 addresses from log strings.
  - Performance audit shows < 5ms processing time per 1KB of text.

### 6. Decoupled API Integration
**Description**: Bridge between the FastAPI web gateway and the background workers.
- **Acceptance Criteria**:
  - `POST /tasks/run` returns a `job_id` and a `202 Accepted` status within 20ms.
  - API process remains responsive and maintains Socket.io heartbeats during an active 30-second worker task.
  - Job status updates are transmitted back to the UI via Redis-backed Socket.io manager.

## Proposed Changes

### [Infra] [Docker]
- [MODIFY] [docker-compose.yml](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/infra/docker-compose.yml): Update Postgres image and add Redis service with strict port binding.

### [Backend] [Schemas]
- [NEW] [003_vector_memory.sql](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/schemas/postgres/003_vector_memory.sql): Schema for memory storage.

### [Backend] [Services]
- [NEW] [memory_service.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/services/memory_service.py): Core logic for RAG.
- [NEW] [worker.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/worker.py): Asynchronous worker entry point.
- [NEW] [scrubber.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/utils/scrubber.py): Pre-ingestion safety engine.

## Verification Plan

### Automated Tests
- `pytest tests/infra/test_vector_engine.py`
- `pytest tests/core/test_queue_latency.py`

### Manual Verification
- Verify `agent_memories` population via `PGAdmin` or `psql`.
- Confirm worker log output shows task execution.
